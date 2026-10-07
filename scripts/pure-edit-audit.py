"""Deterministic quality gate for the compact pure-edit path; no model calls."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT/'src/pure-edit-system.json').read_text(encoding='utf-8'))


def audit(edl):
    failures, warnings = [], []
    duration_ms = round(float(edl['source']['durationSec']) * 1000)
    tracks = edl.get('tracks', {})
    captions = tracks.get('captions', [])
    graphics = tracks.get('graphics', [])
    broll = tracks.get('broll', [])
    effects = tracks.get('effects', [])
    max_words = RULES['captions']['maxWords']
    last_end = 0
    strong = []
    for i, cue in enumerate(captions):
        words = len(str(cue.get('text', '')).split())
        if not 1 <= words <= max_words:
            failures.append(f'caption[{i}] has {words} words; allowed 1-{max_words}')
        start, end = cue.get('startMs', -1), cue.get('endMs', -1)
        if not (0 <= start < end <= duration_ms + 1) or start < last_end:
            failures.append(f'caption[{i}] has invalid or overlapping timing')
        if end-start < RULES['captions']['minimumReadableMs']:
            warnings.append(f'caption[{i}] may be too fast to read')
        if cue.get('motion', {}).get('strong'):
            strong.append(start)
        last_end = end
    window = 10000
    for point in strong:
        if sum(point <= other < point+window for other in strong) > RULES['captions']['maxStrongPer10Sec']:
            failures.append('too many strong caption accents inside 10 seconds')
            break
    primary = sorted([
        (g['startMs'], g['endMs'], 'graphic') for g in graphics
    ] + [
        (b['startMs'], b['endMs'], 'broll') for b in broll
    ] + [
        (e['startMs'], e['endMs'], 'camera') for e in effects
    ])
    for i, (start, end, kind) in enumerate(primary):
        if not (0 <= start < end <= duration_ms + 1):
            failures.append(f'{kind}[{i}] is outside the timeline')
        for other_start, other_end, other_kind in primary[i+1:]:
            if other_start >= end:
                break
            if kind in ('graphic','broll') and other_kind in ('graphic','broll'):
                failures.append(f'{kind} overlaps {other_kind}; keep one primary visual at a time')
    music = edl.get('music')
    if music:
        if float(music.get('volume', 0)) > RULES['audio']['musicMaxVolume']:
            warnings.append('music volume exceeds the pure-edit dialogue-safe ceiling')
        if float(music.get('fadeOutSec', 0)) < RULES['audio']['minimumMusicFadeOutSec']:
            warnings.append('music fade-out is shorter than the polish floor')
    for i, cue in enumerate(tracks.get('sfx', [])):
        if float(cue.get('volume', 0)) > RULES['audio']['sfxMaxVolume']:
            warnings.append(f'sfx[{i}] exceeds the pure-edit ceiling')
    return {'ok':not failures,'systemVersion':RULES['version'],'failures':failures,
            'warnings':warnings,'counts':{'captions':len(captions),'strongAccents':len(strong),
                                         'graphics':len(graphics),'broll':len(broll),
                                         'camera':len(effects),'sfx':len(tracks.get('sfx', []))}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('edl', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    report = audit(json.loads(args.edl.read_text(encoding='utf-8')))
    payload = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding='utf-8')
    print(payload, end='')
    raise SystemExit(0 if report['ok'] else 2)


if __name__ == '__main__':
    main()
