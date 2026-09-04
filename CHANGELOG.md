# Changelog

Semver bắt đầu từ 1.1.0. Trước đó kit phát triển qua các vòng nội bộ "v1..v8"
(không phải semver — xem Lore bên dưới).

## [1.3.0] - 2026-07-08

V1 ship candidate: workflow B + distributable Claude Code package.

### Added
- **Workflow B (b-roll + hook)**: `run-broll-pipeline.py`, hook title strips (Baloo 2) + handwritten sub-hook/CTA (Patrick Hand, VN subsets verified), background music (`--music`, loop/fade-out 1.5s/`--music-start`), source audio muted by default, auto-shrink long hook lines.
- **Claude Code package layer** (English): `CLAUDE.md`, `.claude/skills/video-editor` (skill + 6 references, translated), `.claude/commands` (`/edit-video`, `/broll`, `/video-doctor`), `.claude/agents/video-critic`, `.claude/workflows/video-review.js`.
- `scripts/pack-kit.py`: whitelist pack -> `dist/` folder + zip; fail-loud on missing sfx/skill/CLAUDE.md (replaces pack-kit.ps1).
- `scripts/pipeline_common.py`: shared archive/theme/guarded-write/render helpers (both workflows).
- Auto-archive: switching clips moves the previous project's edl + final to `out/archive/<clip>/`.

### Changed
- Captions: sizes trimmed ~8%, positive letter-spacing (owner feedback: oversized + cramped).
- SKILL.md: mandatory response pattern (announce durations, end with 3-option menu) + spoken-command dictionary for mass users.
- Vietnamese skill source (`skill/`) replaced by the English `.claude/skills/video-editor` (VN version lives in git history).

## [1.2.0] - 2026-07-08

Phase 07-lite "V1 Taste Polish" (phương án chốt từ hội đồng 3 agent đa dạng hóa style).

### Fixed
- **Theme tokens giờ chảy vào render thật**: trước đây chỉ 4 field màu được copy từ `style-themes.json` vào recipe, mọi token chất liệu/motion bị bỏ rơi nên 20 theme render y hệt nhau trừ màu.
- Hook 0-3s: dim 0.78 → 0.5 (người nói không còn "biến mất"), gradient bỏ nốt trắng giữa.
- Từ nhấn chọn theo NGHĨA (số > danh từ dài; stopword mở rộng) ở cả engine (`pick_keyword_idx`) lẫn hook/kinetic (`src/text-emphasis.ts`) - hết highlight "THÌ/ĐẾN/THÔI" và từ-giữa-câu.
- Card graphics tôn trọng `anchor` (top/center/bottom) - hết cảnh card che miệng không né được.
- Caption active-word scale 1.08 → 1.05 + gap rộng hơn (hết dính chữ).

### Added
- Token `textFx` (gradient|solid) + `captionCase` (upper|sentence) - wire đủ Captions/KineticStatement/MaskReveal/GlassStrip/HookTitle/PersistentTitleHook. Theme `graphite-minimal` + `documentary-cream` bật solid + sentence: gu minimal thật.
- `npm run goldens`: 1 golden still/family (7 family) trên clip nền tự sinh - luật "family không có golden = không tồn tại".

### Changed
- Gộp family Clean Edu + Analysis Business → **Edu Analysis**; chốt 7 family là trần V1.
- Removed: ColorWipe (transition + graphic), OrbitRing ambient, dấu "—" trong mọi text lên hình (3 tầng: docs/playbook/engine filter).

## [1.1.0] — 2026-07-07

Nền móng cho việc đóng gói Skill Kit (Phase 01, plan `260707-2315-editor-kit-skills-packaging`).

### Added
- `scripts/doctor.py` — preflight check Node/Python/ffmpeg/whisper/Claude CLI, thông báo tiếng Việt, exit code rõ.
- `scripts/make-render-props.mjs` — sinh wrapper `out/edl-props.json` từ `out/edl.json` ngay trước render/studio (edl.json là nguồn sự thật duy nhất).
- `run-pipeline.py --render` / `--open` — 1 lệnh từ clip thô ra `out/final.mp4`.
- `generate-edl.py` ghi `out/edl.generated.json` (bản máy sinh); `out/edl.json` là bản làm việc, KHÔNG bị ghi đè nếu đã tồn tại — dùng `--force-regen` để ghi đè chủ đích.
- npm scripts: `studio:edl` (preview EDL thật trong Remotion Studio), `render:edl`, `doctor`.
- Git repo + tag `v-baseline`; `engines.node >= 18`.

### Removed
- `out/props.json` lưu trùng nội dung edl (nguồn gây render nhầm bản cũ).

### Changed
- Clip đã cắt lặng đặt tên theo clip nguồn: `public/raw/<clip>-tight.mp4` (trước là `tight.mp4` cố định, các project đè lẫn nhau).

## Lore các vòng nội bộ (trước semver)

- **v7** — baseline gu đã chốt: visual DÀY, caption sạch, không grain. Là chuẩn thẩm mỹ hiện hành.
- **v8** — bài học "v8 trap": nhồi graphic quá tay vì coi quota là sàn. Nguyên tắc rút ra: **quota graphic là TRẦN, không phải SÀN**.
