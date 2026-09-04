# CLAUDE.md - Video Editor Kit

Local-first AI video editor for short-form content (Reels/TikTok/Shorts).
Two workflows: **talking-head** (auto captions + graphics + cuts) and
**b-roll + hook** (title strips + handwritten sub-hook + CTA + music).
You (Claude) are the reasoning layer; rendering is Remotion, all local, no API keys.

## Start here

- User wants to edit a video → activate the `video-editor` skill
  (`.claude/skills/video-editor/SKILL.md`). It owns the interview, the
  command dictionary, and the response pattern. Follow it strictly.
- Slash commands (all `biz-` prefixed, written for non-technical users):
  `/biz-help` (setup check + menu, the single entry point), `/biz-edit-video`
  (talking-head), `/biz-broll-video` (b-roll + hook), `/biz-review-video`
  (pro panel). The edit commands accept free-text style descriptions in any
  language and map them to themes themselves; locating scattered video files
  is handled inline by the `video-finder` agent, not a separate command.
- The user is assumed NON-technical: explain in plain words, never ask them to
  "upload" a file (they paste a path or you find it via the `video-finder`
  agent), announce durations before long runs, and END EVERY session round
  with next-step guidance that names the exact `/biz-...` command to type.
- First run on a machine: `python scripts/doctor.py` must exit 0.

## Engine map

```text
scripts/run-pipeline.py         talking-head: STT -> silence cut -> face zones -> EDL -> render
scripts/run-broll-pipeline.py   b-roll: hook/subhook/CTA + music -> EDL -> render (no STT)
scripts/generate-edl.py         EDL composer; --llm prefed reads out/host-plan.json (you write it)
scripts/pipeline_common.py      shared: project archiving, theme recipe, guarded EDL writes, render
scripts/doctor.py               preflight environment check
scripts/validate-edl-risk.py    EDL linter (overlaps, long text, empty data)
scripts/render-goldens.mjs      one reference still per style family (npm run goldens)
src/                            Remotion composition (Reel.tsx), components, EDL schema (edl-types.ts)
src/style-themes.json           SINGLE SOURCE of theme tokens (colors + material + typography)
out/                            per-project workspace; switching clips auto-archives to out/archive/<clip>/
```

Key npm scripts: `render:edl` (render out/edl.json), `studio:edl` (preview,
restart after edits), `doctor`, `goldens`, `typecheck`.

## Non-negotiable principles

1. **Graphic quota is a CEILING, not a floor.** Never add graphics to "fill
   gaps". Breathing room is professional; stuffing is the failure mode.
2. **`out/edl.json` is the working copy.** The machine writes to
   `out/edl.generated.json`; `edl.json` is only auto-updated when untouched.
   After manual edits, regenerating requires `--force-regen` (confirm with the
   user first: it discards their edits). Small fixes: edit `edl.json` directly,
   then `npm run render:edl`. Never rerun the full pipeline for a text fix.
3. **No em/en dashes in any on-screen text.** The engine filters them, but do
   not write them in hooks, captions, or graphic text.
4. **Announce durations before long runs** (full pipeline ~7-12 min, re-render
   ~5-7 min; b-roll ~1-3 min) and run them in the background. End every render
   round with: video path (open it) + elapsed time + a 3-option menu
   (tweak something / keep it / next video).
5. **Vietnamese text safety:** captions/graphics use fonts with verified
   Vietnamese subsets (Montserrat, Be Vietnam Pro, Baloo 2, Patrick Hand).
   When adding fonts, verify the `vietnamese` subset via
   `@remotion/google-fonts` `getInfo()` first.
6. After component/style changes run `npm run typecheck` and `npm run goldens`
   (a style family without a golden still does not exist).

## Testing

- No mocked renders: verify by extracting real frames
  (`ffmpeg -ss <sec> -i out/final.mp4 -frames:v 1 frame.jpg`) and looking at them.
- Audio checks: `ffmpeg -i out/final.mp4 -af volumedetect -f null -`.
