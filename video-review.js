export const meta = {
  name: 'video-review',
  description: 'Panel-review the rendered video (art director + editor + viewer in parallel), then merge into one fix list',
  whenToUse: 'After rendering out/final.mp4, when the user wants a thorough multi-perspective review before publishing',
  phases: [
    { title: 'Review', detail: 'three lenses in parallel' },
    { title: 'Merge', detail: 'dedupe + rank fixes' },
  ],
}

// Each lens looks at the same render independently; blind spots differ.
const LENSES = [
  {
    key: 'art-director',
    prompt: `You are a demanding art director. Working dir: the video-editor kit root.
Extract 8-10 frames from out/final.mp4 at graphic moments (read out/edl.json for startMs values;
ffmpeg -v error -ss <sec> -i out/final.mp4 -frames:v 1 -vf scale=540:-1 f<i>.jpg -y) and LOOK at them.
Judge: theme consistency, typography, text covering faces or other text, machine-made tells.
Return findings only, each with a timestamp and a concrete fix. No em dashes.`,
  },
  {
    key: 'editor',
    prompt: `You are a professional video editor. Working dir: the video-editor kit root.
Cross-check out/edl.json against out/transcript.json (if present): do graphics land while their
keyword is spoken (±0.5s)? Any leftover STT errors in captions? Graphic density: quota is a CEILING,
flag stuffing rather than gaps. Verify audio with ffmpeg volumedetect (music present, source muted as configured).
Return findings only, each naming the exact EDL entry (type + startMs) and the fix. No em dashes.`,
  },
  {
    key: 'viewer',
    prompt: `You are the target viewer scrolling TikTok. Working dir: the video-editor kit root.
Extract frames in chronological order from out/final.mp4 (every ~5s plus the first 2s) and read them
in sequence like a scroll-by. Answer: does 0-3s stop the scroll? can you read every line in the time
it shows? do you know what to do at the end? where do you swipe away and why?
Return findings only, plain language. No em dashes.`,
  },
]

const results = await Promise.all(
  LENSES.map((l) => agent(l.prompt, { label: `review:${l.key}`, phase: 'Review' })),
)

phase('Merge')
const merged = await agent(
  `Merge these three review reports into ONE ranked fix list for out/edl.json.
Dedupe overlapping findings, keep each fix actionable (exact entry + change + "render:edl only?" flag),
rank by viewer impact. Cap at 8 fixes. Reports:\n\n` +
    results.filter(Boolean).map((r, i) => `=== ${LENSES[i].key} ===\n${r}`).join('\n\n'),
  { label: 'merge-fixes', phase: 'Merge' },
)

return merged
