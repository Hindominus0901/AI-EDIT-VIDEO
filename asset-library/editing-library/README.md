# Editing library

This is the reusable decision library for pure talking-head edits. It stores
caption grammar, video B-roll priority, image fallback motion, color recipes and
dialogue-first audio targets. It is deliberately small so the host can select
an ID instead of describing a style again on every video.

Use moving B-roll by default: user footage first, licensed stock second, and
generated video third. A generated still with restrained camera motion is only
the final fallback. Store each source URL or generation note beside the project
and record the semantic sentence that justified the insertion.
