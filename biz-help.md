---
description: Start here - checks this computer is ready and shows what the kit can do
---

The single onboarding command: setup check + menu in one.

**Part 1 - silent readiness check:**
Run `python scripts/doctor.py` quietly.
- All good: just say "Your computer is ready." (one line, no tool noise).
- Something missing: explain it like to a friend ("ffmpeg is the free tool
  that reads video files"), give the exact install command for THIS machine
  (winget on Windows, brew on macOS, apt on Linux), and OFFER to run it
  yourself where safe (ffmpeg via winget, `npm install`,
  `pip install -r requirements.txt`). Re-run doctor after fixing.
- Gentle heads-up (never blocking): the first video ever downloads a ~460MB
  speech model silently, the computer is not frozen.

**Part 2 - the menu** (adapt wording, keep commands exact):

> **What I can do:**
>
> | You want to... | Type this |
> |---|---|
> | Edit a video of you talking (auto captions + graphics + cuts) | `/biz-edit-video` |
> | Turn scenery/footage into a hook video (big title + music) | `/biz-broll-video` |
> | Review a finished video like a pro panel | `/biz-review-video` |
>
> You can describe the style you want right in the command, e.g.:
> `/biz-edit-video D:\clips\talk.mp4 minimal black-white style` or
> `/biz-broll-video soft feminine vibe, topic: 3 morning habits`
>
> Don't know where your video file is? Just say "find my video from
> yesterday" and I will locate it for you.
>
> Tip: to paste a file path on Windows, right-click the file and choose
> "Copy as path".
