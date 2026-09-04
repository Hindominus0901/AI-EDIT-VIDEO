---
description: Turn footage (b-roll) into a hook video - title strips + handwritten sub-hook + CTA + music. Style and vibe can be described in free words.
argument-hint: [clip path] [topic or full hook text] [optional: style/vibe words]
---

Create a b-roll hook video (TikTok "text over footage" format). The user is NOT
technical: plain language, guide every step.

Input: $ARGUMENTS (clip path, topic/hook wording, and optionally style words -
in any order, any language).

**Getting the clip (never ask them to "upload"):**
- Path given: verify, continue.
- Missing: if their words hint at a video, launch the `video-finder` agent
  with the hint and confirm the pick with one extracted frame. Otherwise teach
  the "Copy as path" trick once.

**Understanding what they want (the advanced part):**
- Extract and LOOK at 2-3 frames to read the footage mood before writing text.
- If the user described a style/vibe in any words ("nhẹ nhàng nữ tính", "clean
  minimal", "warm docu feel"), MAP it to the closest theme in
  `references/style-menu.md` yourself, confirm in one line, and proceed. No
  menu re-asking.
- If they gave full hook wording, use it verbatim (split title lines with |).
  If they gave only a topic, DRAFT 3 complete hook options (title 1-2 lines +
  sub-hook in parentheses + CTA) per the formula in
  `references/workflow-broll-hook.md`, shown as the FULL on-screen text so
  they just pick what reads best.
- Music: ask plainly for an mp3 path ("right-click the song file, Copy as
  path"); offer to render without music first if they have none. Defaults:
  source audio muted, music 0.7, 1.5s fade-out, `--music-start <sec>` for long
  intros.

**Run** (announce "about 1-3 minutes", background):
`python scripts/run-broll-pipeline.py raw/<clip>.mp4 --hook "Line 1|Line 2"
--subhook "(...)" --cta "..." --theme <key> --music <file> --render`

**End of every round (mandatory):** open the video + location + elapsed time,
then guide by command:

> What next?
> - Change words/colors/music? Just tell me
> - Happy? Say "keep it" and I will remember your style
> - Another video? Type `/biz-broll-video` or `/biz-edit-video` (talking video)
