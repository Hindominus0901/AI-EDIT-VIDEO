---
description: Edit a talking-head video end-to-end (auto captions, graphics, cuts, render). Style can be described in free words.
argument-hint: [video path] [optional: describe the style you want, e.g. "minimal black-white", "energetic orange, big text"]
---

Edit a talking-head video with the video-editor kit. The user is NOT technical:
plain language, no jargon, guide every step.

Input: $ARGUMENTS (a file path and, optionally, a free-text style description).

**Getting the video (never ask them to "upload"):**
- Path given: verify it exists, continue.
- No usable path: if their words hint at a video ("the one from yesterday",
  "my Da Lat clip"), launch the `video-finder` agent
  (`.claude/agents/video-finder.md`) with that hint and present a numbered
  shortlist; confirm the pick with one extracted frame ("Is this the one?").
  Otherwise teach the path trick once: right-click the file, "Copy as path",
  paste here.

**Understanding the style they want (this is the advanced part):**
- If the user DESCRIBED a style in any words, any language ("tối giản trắng
  đen", "soft feminine", "luxury gold vibe", "giống video trước"), MAP it
  yourself to the closest family/theme in `references/style-menu.md` plus
  tokens (`textFx`, `captionCase`) when relevant. Confirm in one line what you
  understood ("Minimal: calm sentence-case text, no gradients - correct?") and
  proceed. Do NOT re-ask with a menu.
- Only when NO style was described: one AskUserQuestion with 3 best-fit
  options + "You pick for me (Recommended)", each option described by what the
  result LOOKS like, plus check the profile in
  `.claude/skills/video-editor/memory/user-style-profile.md` first.

**Then follow the `video-editor` skill, workflow A**
(`references/workflow-talking-head.md`):

1. First run on this machine: `python scripts/doctor.py` silently; surface
   only problems, with the exact fix.
2. Copy the clip into `public/raw/` (no spaces in the filename).
3. Say clearly: "This takes about 7-12 minutes, I will tell you when it is
   done", then run in the background: transcript (`--llm offline`), write
   `out/host-plan.json` per `references/edl-reasoning-talking-head.md`, then
   `python scripts/generate-edl.py --clip "raw/<tight>.mp4" --llm prefed --force-regen`,
   fix STT errors in captions, `npm run render:edl`.
4. **End of every round (mandatory):** open the video + location + elapsed
   time, then guide by command:

   > What next?
   > - Want changes? Just tell me ("fix the caption at 0:20", "fewer graphics", "warmer color")
   > - Happy? Say "keep it" and I will remember your style
   > - New video? Type `/biz-edit-video` or `/biz-broll-video` (footage + hook)
