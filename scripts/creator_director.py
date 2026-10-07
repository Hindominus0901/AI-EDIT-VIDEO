"""Authored editorial scenes -> deterministic render. No nested models or quotas."""
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = json.loads((ROOT/'src/creator-profiles.json').read_text(encoding='utf-8'))
LAYOUTS = {'speaker', 'statement', 'compare', 'steps', 'evidence', 'content-flood', 'salt-ocean'}


def finite(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{name}: expected finite number in [{low}, {high}]')
    return value


def text(value, name, limit=180):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f'{name}: required text, at most {limit} characters')


def validate_director(director, duration_ms, public_dir):
    from clean_edit import checked_asset
    if director.get('profile') not in PROFILES:
        raise ValueError('Unknown creatorStyle')
    story = director.get('story', {})
    for field in ('audience', 'premise', 'payoff'):
        text(story.get(field), f'story.{field}')
    framing = director.get('framing', {})
    if framing.get('fit', 'contain') not in ('cover', 'contain'):
        raise ValueError('framing.fit must be cover or contain')
    for name in ('focusX', 'focusY'):
        finite(framing.get(name, 50), name, 0, 100)
    scenes = director.get('scenes', [])
    if not scenes:
        raise ValueError('Authored scenes required; no automatic keyword fallback')
    end = 0
    seen = {}
    ids = set()
    for scene in scenes:
        text(scene.get('id'), 'scene.id', 60)
        if scene['id'] in ids:
            raise ValueError('Duplicate scene id')
        ids.add(scene['id'])
        start = finite(scene.get('startMs'), 'scene.startMs', 0, duration_ms)
        stop = finite(scene.get('endMs'), 'scene.endMs', 0, duration_ms)
        if start < end or stop-start < 600:
            raise ValueError('Scenes must be ordered, non-overlapping and at least 600ms')
        end = stop
        if scene.get('layout') not in LAYOUTS:
            raise ValueError('Unsupported creator scene layout')
        for name in ('meaning', 'reason'):
            text(scene.get(name), name, 300)
        if scene.get('motion', 'lift') not in ('lift', 'fade', 'cut'):
            raise ValueError('Unknown scene motion')
        if scene['layout'] != 'speaker':
            text(scene.get('title'), 'scene.title', 85)
        if scene['layout'] in ('compare', 'steps'):
            items = scene.get('items', [])
            if (scene['layout'] == 'compare' and len(items) != 2) or not 2 <= len(items) <= 3:
                raise ValueError('compare needs 2 items; steps needs 2–3')
            previous = -1
            for item in items:
                text(item.get('text'), 'item.text', 60)
                at = finite(item.get('atMs'), 'item.atMs (relative to scene)', 0, stop-start-600)
                if at < previous:
                    raise ValueError('Item reveals must follow their authored order')
                previous = at
        if scene['layout'] == 'evidence':
            name = checked_asset(public_dir, scene.get('image', ''))
            if Path(name).suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
                raise ValueError('Evidence needs a local raster image')
            text(scene.get('assetSource'), 'assetSource', 300)
            digest = hashlib.sha256((public_dir/name).read_bytes()).hexdigest()
            if digest in seen:
                if scene.get('callbackTo') != seen[digest]:
                    raise ValueError('Repeated evidence image requires callbackTo and callbackReason')
                text(scene.get('callbackReason'), 'callbackReason', 300)
            seen[digest] = scene['id']
    end = 0
    for cue in director.get('audioCues', []):
        start = finite(cue.get('startMs'), 'audio.startMs', 0, duration_ms)
        stop = finite(cue.get('endMs'), 'audio.endMs', 0, duration_ms)
        if stop <= start or start < end:
            raise ValueError('Audio cues must be ordered and not overlap')
        finite(cue.get('gain'), 'audio.gain', 0, 1)
        text(cue.get('reason'), 'audio.reason')
        end = stop


def compose_creator(transcript, plan, clip, public_dir, aspect):
    from clean_edit import compose_clean
    if plan.get('timebase') != 'edited-clip':
        raise ValueError('Creator plan requires edited-clip timebase')
    if plan.get('premiumSet') or plan.get('stylePackage'):
        raise ValueError('creatorStyle cannot be combined with premiumSet/stylePackage')
    director = {key: copy.deepcopy(plan.get(key, default)) for key, default in
                [('story', {}), ('scenes', []), ('framing', {}), ('audioCues', [])]}
    director['profile'] = plan['creatorStyle']
    validate_director(director, round(transcript['durationSec']*1000), public_dir)
    base = copy.deepcopy(plan)
    base.pop('creatorStyle')
    base['moments'] = base.get('moments', [])
    if any(m.get('images') or m.get('asset') for m in base['moments']):
        raise ValueError('Creator visuals belong in scenes, not legacy moment graphics')
    edl, report = compose_clean(transcript, base, clip, public_dir, aspect)
    for scene in director['scenes']:
        if scene['layout'] != 'speaker' and any(scene['startMs'] < b['endMs'] and scene['endMs'] > b['startMs'] for b in edl['tracks']['broll']):
            raise ValueError('B-roll overlaps an authored scene; choose one visual focus')
    edl['style']['layout'] = 'creator'
    edl['director'] = director
    for cue in plan.get('soundCues', []):
        finite(cue.get('startMs'), 'sound.startMs', 0, transcript['durationSec']*1000-1)
        finite(cue.get('volume'), 'sound.volume', 0, .3)
        text(cue.get('reason'), 'sound.reason')
        if cue.get('sound') not in {'kit-tick','kit-drop','kit-scroll'}:
            raise ValueError('Creator sound cue must use a bundled kit sound')
        edl['tracks']['sfx'].append({**cue,'preRollMs':0,'priority':5})
    report.update(policy='creator-director-v1', creatorStyle=director['profile'],
                  scenes=len(director['scenes']), nestedModelCalls=0,
                  sfx=len(edl['tracks']['sfx']),
                  listeningReview='pending', fidelity='proposed-adaptation-not-exact-clone')
    report['warnings'] = []
    if director['framing'].get('fit') == 'cover':
        report['warnings'].append('Review face/hands and crop on the actual source.')
    if director['audioCues'] and not edl.get('music'):
        raise ValueError('audioCues require a supplied music track')
    return edl, report
