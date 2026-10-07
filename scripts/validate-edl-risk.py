"""
EDL risk validator — catches common render/visual problems before Remotion render.

This is not a schema validator. Zod already validates shape at render time. This
script checks editorial/render risks that still pass schema:
  - overlapping non-transition graphics
  - data visuals without data
  - text likely too long for fixed-format components
  - missing sourceClip files for embedded mockup scenes
  - invalid clean caption timing, missing local graphics and crowding

Usage:
  python scripts/validate-edl-risk.py out/edl.json
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

TRANSITION_TYPES = {"color-wipe"}
STRUCTURAL_TYPES = {"hook", "cta"}
DATA_TYPES = {"number-counter", "donut-stat", "bar-stat", "stat-compare", "info-table"}
ITEM_TYPES = {"step-flow", "list-reveal", "premium-roadmap"}
COMPARE_TYPES = {"comparison", "dual-icon-cards"}
SFX_TYPES = {
    "hook", "cta", "kinetic", "lower-third", "color-wipe", "kinetic-statement",
    "mask-reveal", "glass-strip", "badge", "callout", "highlight-reveal",
    "number-counter", "donut-stat", "bar-stat", "progress-bar", "glass-card",
    "step-flow", "comparison", "list-reveal", "lower-third-pro", "info-table",
    "stat-compare", "illus-mark", "path-mark", "shape-3d", "premium-roadmap",
    "neon-icon-card", "negative-slash-card", "dual-icon-cards", "diamond-label",
    "ad-comparison-scene",
}


def ms(sec):
    return int(sec * 1000)


def warn(out, code, message):
    out.append({"code": code, "message": message})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("edl")
    ap.add_argument("--public-dir", default=str(PUBLIC))
    a = ap.parse_args()

    edl_path = Path(a.edl)
    public_dir = Path(a.public_dir)
    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    tracks = edl.get("tracks", {})
    graphics = sorted(tracks.get("graphics", []), key=lambda g: g.get("startMs", 0))
    transitions = sorted(tracks.get("transitions", []), key=lambda t: t.get("startMs", 0))
    explicit_sfx = tracks.get("sfx", [])
    captions = tracks.get("captions", [])
    duration_ms = ms(float(edl.get("source", {}).get("durationSec", 0)))
    warnings = []
    if edl.get('style',{}).get('layout') == 'creator':
        from creator_director import validate_director
        from clean_edit import validate_captions, checked_asset
        from clean_media import media_tracks
        try:
            validate_director(edl.get('director',{}),duration_ms,public_dir)
            validate_captions(captions,duration_ms)
            checked_asset(public_dir,edl['source']['clip'])
            media_tracks({'camera':tracks.get('effects',[]),'broll':tracks.get('broll',[])},duration_ms,public_dir,checked_asset)
            if graphics or transitions:
                raise ValueError('Creator layout uses director scenes; legacy graphics/transitions are unsupported')
            for scene in edl['director']['scenes']:
                if scene['layout']!='speaker' and any(scene['startMs']<b['endMs'] and scene['endMs']>b['startMs'] for b in tracks.get('broll',[])):
                    raise ValueError('B-roll overlaps creator scene')
            if edl.get('music'):
                checked_asset(public_dir,edl['music']['src'])
            elif edl['director'].get('audioCues'):
                raise ValueError('audioCues require music')
        except (ValueError,KeyError,TypeError) as error:
            raise SystemExit(f'Creator validation failed: {error}')
    clean = edl.get('style',{}).get('layout') in ('focused','creator')
    premium = edl.get('style',{}).get('premiumSet')
    if premium:
        from clean_edit import PREMIUM_SETS
        if not clean or premium not in PREMIUM_SETS:
            warn(warnings,'premium-layout','Premium sets require focused layout and a known set name.')
    if clean:
        for name in ('transitions',):
            if tracks.get(name):
                warn(warnings,'clean-unsupported-track',f'Focused layout does not render {name}; use an appropriate layout.')
        from clean_media import media_tracks
        from clean_edit import checked_asset
        try:
            media_tracks({'camera':tracks.get('effects',[]),'broll':tracks.get('broll',[])},duration_ms,public_dir,checked_asset)
            for g in graphics:
                if any(g['startMs']<b['endMs'] and g['endMs']>b['startMs'] for b in tracks.get('broll',[])):
                    warn(warnings,'clean-visual-overlap','Graphic overlaps B-roll; choose one visual emphasis.')
        except (ValueError,KeyError) as e:warn(warnings,'clean-media',str(e))
        if any(g.get('type')!='clean-motion' for g in graphics):
            warn(warnings,'clean-unsupported-graphic','Focused layout requires clean-motion graphics.')

    body = [g for g in graphics if g.get("type") not in STRUCTURAL_TYPES | TRANSITION_TYPES]
    for prev, cur in zip(body, body[1:]):
        if cur.get("startMs", 0) < prev.get("endMs", 0) - 80:
            warn(
                warnings,
                "graphic-overlap",
                f"{prev.get('type')}@{prev.get('startMs')} overlaps {cur.get('type')}@{cur.get('startMs')}",
            )

    for g in graphics:
        t = g.get("type")
        txt = str(g.get("text", "") or "")
        if t == 'clean-motion':
            motion = g.get('motion',{})
            images = motion.get('images',[])
            kind = motion.get('kind')
            needed = 2 if kind in ('photo-collage','photo-diptych') else 1 if str(kind).startswith('photo-') else 0
            if not kind or len(images)<needed:
                warn(warnings,'motion-incomplete',f'clean-motion@{g.get("startMs")} missing kind/images')
            for image in images:
                target = (public_dir/image).resolve()
                if not target.is_relative_to(public_dir.resolve()) or not target.is_file():
                    warn(warnings,'asset-missing',f'clean-motion missing local image: {image}')
        if len(txt) > 52 and t in {"badge", "diamond-label", "highlight-reveal", "negative-slash-card"}:
            warn(warnings, "text-too-long", f"{t}@{g.get('startMs')} has {len(txt)} chars")
        if t in DATA_TYPES:
            has_data = bool(g.get("value") or g.get("rows") or g.get("leftVal") or g.get("rightVal"))
            if not has_data:
                warn(warnings, "data-empty", f"{t}@{g.get('startMs')} has no usable data")
        if t in ITEM_TYPES and not g.get("items"):
            warn(warnings, "items-empty", f"{t}@{g.get('startMs')} has no items")
        if t in COMPARE_TYPES and not (g.get("left") and g.get("right")):
            warn(warnings, "compare-incomplete", f"{t}@{g.get('startMs')} lacks left/right")
        if g.get("sourceClip"):
            clip = Path(str(g["sourceClip"]))
            if not clip.is_absolute():
                clip = public_dir / clip
            if not clip.exists():
                warn(warnings, "sourceclip-missing", f"{t}@{g.get('startMs')} missing {g['sourceClip']}")
        if g.get("endMs", 0) > duration_ms + 100:
            warn(warnings, "beyond-duration", f"{t}@{g.get('startMs')} ends after source duration")

    legacy_transition_count = sum(1 for g in graphics if g.get("type") in TRANSITION_TYPES)
    transition_count = len(transitions) + legacy_transition_count
    if not clean and duration_ms >= 30000 and transition_count == 0:
        warn(warnings, "no-transitions", "No transition graphics in a 30s+ EDL")

    sfx_candidates = len(explicit_sfx) or (
        sum(1 for g in graphics if g.get("type") in SFX_TYPES)
        + sum(1 for t in transitions if t.get("type") in SFX_TYPES)
    )
    event_count = len(graphics) + len(transitions)
    if not clean and event_count and sfx_candidates / event_count < 0.65:
        warn(warnings, "sfx-low-coverage", f"SFX mapping covers {sfx_candidates}/{event_count} events")

    if captions:
        long_caps = [c for c in captions if len(str(c.get("text", "")).split())>5] if clean else [c for c in captions if len(str(c.get("text", ""))) > 34]
        if long_caps:
            warn(warnings, "caption-long", f"{len(long_caps)} captions exceed {'5 words' if clean else '34 chars'}")
        if clean:
            from clean_edit import validate_captions
            try: validate_captions(captions,duration_ms)
            except ValueError as e: warn(warnings,'caption-timing',str(e))
            for c in captions:
                keyword=c.get('motion',{}).get('keyword')
                if keyword and keyword.lower() not in c['text'].lower():
                    warn(warnings,'keyword-missing',f'{keyword}@{c["startMs"]} absent from caption')

    out = {
        "edl": str(edl_path),
        "graphics": len(graphics),
        "captions": len(captions),
        "transitions": transition_count,
        "sfx": len(explicit_sfx),
        "warnings": warnings,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if warnings:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
