# Video Editor Kit

Local-first talking-head reel editor. The pipeline turns a raw clip into an
`edl.json`, then Remotion renders the final video.

```text
raw clip
-> local STT
-> silence cut
-> local face-zone detection
-> local/CLI EDL reasoning
-> edl.json
-> Remotion render
```

## Default Providers

The default path does not require an API key.

| Layer | Default | Notes |
|---|---|---|
| Speech-to-text | `faster-whisper` local | word timestamps |
| Edit reasoning | Claude CLI | configurable via `CLAUDE_CLI_CMD` |
| Offline fallback | deterministic rules | `--llm offline` |
| Face detection | OpenCV local | no network |
| Media | ffmpeg / ffprobe | local |
| Render | Remotion | local |

## Install

```powershell
npm install
pip install -r requirements.txt
```

Also install these on PATH:

- Node.js 18+
- Python 3.10+
- ffmpeg + ffprobe
- Claude CLI, if using `--llm claude-cli`

For Claude CLI command customization:

```powershell
$env:CLAUDE_CLI_CMD = "claude -p"
```

## Use with Claude Code (recommended)

The kit ships as a self-contained Claude Code project: skills, slash commands,
agents and workflows live in `.claude/` and load automatically.

```powershell
cd path\to\video-editor-kit
npm install
pip install -r requirements.txt
claude
```

Then, inside Claude Code:

- `/biz-help` - start here: checks the machine is ready + shows the menu
- `/biz-edit-video D:\clips\talk.mp4 minimal black-white` - talking-head:
  auto captions, graphics, cuts; describe the style you want in free words
- `/biz-broll-video D:\clips\beach.mp4 "3 morning habits" soft feminine` -
  b-roll: hook strips + handwritten sub-hook + CTA + background music
- `/biz-review-video` - pro-panel review of the finished video
- or just type naturally: "edit this video for me: D:\clips\video.mp4"
  (don't know where the file is? say "find my video from yesterday")

Claude asks at most 2 questions (edit type + style), announces how long the
run takes (~7-12 min talking-head, ~1-3 min b-roll), opens `out/final.mp4`,
then takes natural-language tweaks ("fix the caption at 0:20", "fewer
graphics", "change the style"). Switching to a new clip auto-archives the
previous project to `out/archive/<clip>/`.

Package a build for distribution: `python scripts/pack-kit.py` (whitelist
copy + zip into `dist/`).

## Run manually (CLI)

Check the environment first (friendly Vietnamese messages):

```powershell
python scripts\doctor.py
```

Place source clips under `public/raw/`, then one command renders `out/final.mp4`:

```powershell
python scripts\run-pipeline.py raw\clip.mp4 --smart --render
```

Without `--render` the pipeline stops after writing `out/edl.json`. Edit it by
hand, preview with `npm run studio:edl`, then render with `npm run render:edl`.
(`studio:edl` snapshots props at startup — restart it after editing `edl.json`.)
Re-running the pipeline never overwrites an existing `edl.json` (your manual
edits are safe); the fresh machine output lands in `out/edl.generated.json`,
and `--force-regen` promotes it explicitly.

Fully offline deterministic mode:

```powershell
python scripts\run-pipeline.py raw\clip.mp4 --llm offline --render
```

Render-only demo:

```powershell
npm run studio
npx remotion render Reel out\demo.mp4
```

## Structure

```text
scripts/
  run-pipeline.py          local-first orchestrator
  transcribe.py            local faster-whisper STT
  local_llm.py             Claude CLI + offline fallback
  silence-cut.py           silence/filler cut + timestamp remap
  detect-face-zones.py     local OpenCV face-zone detection
  generate-edl.py          EDL planner
  edl_passes.py            provider-neutral JSON prompts

src/
  edl-types.ts             EDL v2 schema
  Reel.tsx                 Remotion composition
  components/              graphics, transitions, captions, SFX
  style-themes.json        design-system theme tokens
```

## Useful Validation

```powershell
python scripts\validate-edl-risk.py out\edl.json
npm run typecheck
```
