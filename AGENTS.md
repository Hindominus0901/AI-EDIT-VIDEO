# Video Editor Kit

For ordinary video editing, setup, Vietnamese onboarding or profile requests, read `.agents/skills/dung-video-viet/SKILL.md` and only the relevant references. When the user asks for pure editing, no-cache, a fresh edit, or minimum token use, read `.agents/skills/edit-video-thuan/SKILL.md` instead and do not load the general skill or its references. User instructions and existing project decisions take precedence. Preserve manual EDL edits and source media.

User entry: `BAT-DAU.md`; detailed guide: `HUONG-DAN.md`. Canonical skills live in `integrations/video-editor-viet/skills/`. The `.agents` copies are synced by `scripts/pack-kit.py`.

Windows: use `.venv/Scripts/python.exe` when present and `npm.cmd` / `npx.cmd`. Clean mode uses the current host AI, not a required nested Claude CLI. Check runtime before claiming readiness. Do not claim an installed plugin, live Work support or a drag/drop timeline based on these files alone.
