---
name: video-editor
description: Automatically edit video reels with video-editor-kit (local-first, Remotion). Use when the user wants to edit a talking-head video (silence cutting, captions, graphics, zoom), add a hook caption to b-roll, or says "edit this video", "make a reel", "edit talking-head clip", "add hook text to b-roll", "auto edit TikTok/Reels", "edit video này", "dựng reel", "dựng video ngắn", "cắt video người nói", "sửa caption", or wants to re-edit an already rendered video (change style, fix captions, add/remove graphics).
---

# Video Editor Skill

Orchestrates the `video-editor-kit` engine: raw clip → STT → silence cut → EDL → Remotion render.
You (the agent) are the reasoning layer, no API key or external LLM needed.

## Engine root

This skill ships INSIDE the kit folder as `.claude/skills/video-editor` - the engine
root is the kit folder itself (where `package.json` lives). Open Claude Code in the
kit folder; all commands run with cwd = kit root.

## Non-negotiable principles (locked-in taste)

1. **The graphic quota is a CEILING, not a floor**, never stuff graphics to "fill empty space". Better too few than too many.
2. Clean captions, no grain, dense visuals but with intent (the "v7" baseline).
3. **Overwrite guard:** `out/edl.json` is the working copy; the machine always writes new output to `out/edl.generated.json`. The pipeline auto-updates `edl.json` only when it has not been hand-edited; **once hand-edited, regen requires `--force-regen`**, if you forget the flag the pipeline still continues and renders the OLD version. `--render` only blocks when `edl.json` belongs to a different clip. Iteration details: workflow-talking-head.md Step 5.

## Workflow

### Step 0, Context and learning
- Read `.claude/skills/video-editor/memory/user-style-profile.md` if it exists → learn the user's taste (favorite styles, graphic density, past feedback) to pre-select at the interview step.
- First run on a machine: `python scripts/doctor.py` (reports errors in Vietnamese, exit 0 = ready).

### Step 1, Interview: edit type
If the user has NOT made it clear, ask via `AskUserQuestion` (skip if already clear from the request):

> **Which kind of edit do you want?**
> 1. **Talking-head**, a video of someone speaking: auto-cut silences/filler words, word-synced captions, graphics + zoom to emphasize points.
> 2. **B-roll + caption hook**, you already have footage, overlay hook text + captions on the video.

### Step 2, Interview: style
- Read [references/style-menu.md](references/style-menu.md) (7 style families).
- Based on the **content topic** (heard/guessed from the clip, or quickly ask "what is the video about?") + user-style-profile, pick the **3 best-fit families** + a "Pick for me based on the topic" option as the 4 `AskUserQuestion` options, each with a 1-line color/vibe description. Put the family the user picks most often (per profile) first, marked "(Recommended)".
- Power users may specify a theme key directly (20 keys in `src/style-themes.json`), allow the override.
- **Enforce theme:** the chosen style is only guaranteed via `prefed` mode (the agent sets the theme in the host-plan itself). If running `claude-cli`/`offline`: after gen, check `strategy.theme` in `out/edit-plan.json`; if it drifted, fix the `style` block in `edl.json` using the correct theme key (tokens from `src/style-themes.json`). A misspelled theme key makes the engine silently fall back to `sunset`.

### Step 3, Route workflow

| Edit type | Reference |
|---|---|
| Talking-head | [references/workflow-talking-head.md](references/workflow-talking-head.md) |
| B-roll + caption hook | [references/workflow-broll-hook.md](references/workflow-broll-hook.md) |

### Step 4, After render
- Open the video for the user (`--open` or the `out/final.mp4` path).
- **Multiple clips:** run clips sequentially; `out/` (final.mp4, edl.json) is overwritten each run, copy `out/final.mp4` to its own name (e.g. `out/<clip>-final.mp4`) before starting the next clip.
- Ask for quick feedback (happy? want changes?). If the user wants edits: edit `out/edl.json` DIRECTLY (keep the parts they like) then `npm run render:edl`, do NOT rerun the pipeline from scratch.
- Record feedback into the learning layer (Phase 05; if `.claude/skills/video-editor/memory/` does not exist yet, skip for now).

## The user is NOT technical (assume this always)

- **Getting the video: never ask them to "upload" or attach a file.** They
  paste a file path (teach it once, plainly: "right-click the video, choose
  Copy as path, paste it here"). If they do not know where the video is,
  launch the `video-finder` agent (`.claude/agents/video-finder.md`), videos
  are usually scattered across Downloads/Desktop/phone-sync folders, and
  present a numbered shortlist to pick from. Confirm the pick by showing one
  extracted frame ("Is this the one?").
- **Every AskUserQuestion must be self-explanatory**: each option carries one
  plain-language line describing what the RESULT will look like ("hot orange,
  big shouty text, good for selling"), never bare jargon like theme keys.
  Always include a "You pick for me (Recommended)" option.
- **Delegate to helper agents to keep it simple**: `video-finder` for locating
  files, `video-critic` for reviews. The user never sees raw tool noise.

## Response pattern (MANDATORY every round)

1. **Announce BEFORE running long commands**: full pipeline ~7-12 minutes (STT + analysis + render), re-render ~5-7 minutes, b-roll ~1-3 minutes. Run in the background when possible, report as soon as it finishes.
2. **The end of every step that renders** ALWAYS includes 3 parts: the video path (+ open it for the user), elapsed time, and the menu:
   > Next you can: (1) Change something, just say it naturally (captions, graphics, colors...) | (2) Happy with it, say "keep it" | (3) Next video: type `/biz-edit-video` or `/biz-broll-video`
3. **The end of every session round guides the next step BY COMMAND**: name the exact `/biz-...` command to type (`/biz-help` shows the full menu). A non-technical user should never wonder "what do I type now?".
4. The engine auto-archives the previous project to `out/archive/<clip>/` when a new clip starts, hand edits are NOT lost.

## Spoken-command dictionary (mass-market users)

| User says | Action |
|---|---|
| "edit this video" + file/path | Copy the clip into `public/raw/` → doctor (first run, in background) → interview ≤2 questions → pipeline |
| "fix the caption at second X" | Find the caption in `tracks.captions[]`, quote old/new to confirm, edit `text` + `tokens[].text` → `render:edl` |
| "fewer graphics" / "too many" | Remove the lowest-value graphics (quota is a CEILING) → `render:edl`, list what was removed and at which seconds |
| "change style" / "change colors" | Style interview → edit the `style` block with the theme tokens → `render:edl` |
| "redo from scratch" | CONFIRM hand edits will be lost → pipeline with `--force-regen` |
| "preview" | `npm run studio:edl` (remind: restart after each edl.json edit) |
| "looks good" / "I like it" | Copy final to its own name + record feedback into `.claude/skills/video-editor/memory/user-style-profile.md` |
| "add background music" / "change music" | (workflow B) add/edit the `music` block in `edl.json` or rerun with `--music <file>` → `render:edl`. The kit ships no music, ask the user for a file |
| "next video" | Run the new clip (engine auto-archives the old one); ask "same taste as last time?" if a profile exists |

Principle: **small edits = edit `edl.json` + `render:edl`; do NOT rerun the pipeline** unless the direction changes significantly.

## Quick commands

```powershell
python scripts/doctor.py                                        # preflight
python scripts/run-pipeline.py raw/<clip>.mp4 --smart --render  # one command to out/final.mp4 (claude-cli mode; prefer prefed when reasoning yourself)
npm run studio:edl                                              # live EDL preview (restart after editing edl.json)
npm run render:edl                                              # re-render from the edited edl.json
python scripts/validate-edl-risk.py out/edl.json                # lint the EDL before render
```
