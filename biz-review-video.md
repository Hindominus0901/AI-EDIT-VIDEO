---
description: Review the finished video like a pro panel (art director + editor + viewer) and list fixes
---

Review the most recent render (`out/final.mp4`) for the user.

- Quick review: launch the `video-critic` agent (`.claude/agents/video-critic.md`).
- Thorough review (user says "deep", "kỹ", or is about to publish): run the
  `video-review` workflow (`.claude/workflows/video-review.js`) - three
  reviewers in parallel, merged fix list.

Translate the findings for a NON-technical user: no EDL jargon in the summary;
say "the text at 0:32 covers your face" not "graphic@32000 collides with
captions". Offer to apply the fixes yourself (edit `out/edl.json`, then
`npm run render:edl`, ~5-7 min - announce it).

End with the next-step guide:

> - Want me to fix these? Say "fix them" (about 5-7 minutes)
> - Happy anyway? Say "keep it"
> - New video? Type `/biz-edit-video` or `/biz-broll-video`
