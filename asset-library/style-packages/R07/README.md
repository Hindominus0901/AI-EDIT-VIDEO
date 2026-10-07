# R07 — Mnemonic — danh sách sang demo

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Giải thích một quy trình có ví dụ giao diện

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Chữ đầu cyan neo trái; nhãn trắng đậm; caption body nhỏ; hook có chữ brush.

## Ảnh / graphic

Danh sách nhường chỗ cho UI; chữ gõ trong UI là một lớp riêng.

## Motion

Nhãn xuất hiện lần lượt; UI rise/blur 13,7–14,4s; flash trắng ở chuyển hook.

## Flow

Hook → chữ viết tắt → demo thao tác → hoàn thành danh sách → giải thích sạch.

## Cắt cảnh

Cắt theo ý, giữ phủ định/điều kiện/hơi thở. Nghe điểm nối trước khi gọi là tự nhiên.

## Màu / ánh sáng

Giữ đặc tính nguồn, chỉnh exposure/WB theo shot; không bịa LUT gốc từ MP4.

## Nhạc / SFX

Chưa định danh nhạc/SFX gốc. Chọn tài nguyên có giấy phép, nhạc dưới giọng, SFX theo điểm có nghĩa; đo mức âm và nghe mix.

## 9:16

Lấy geometry từ ref; chừa vùng mặt/miệng/tay và UI nền tảng. Cận mặt cần dịch hoặc giảm nhóm hình, không ép khung mẫu.

## 16:9

Bản chuyển thể 16:9: người nói và vùng nội dung chia ngang, caption theo vùng đọc; không kéo giãn bố cục dọc. Chưa có ref landscape đối chiếu.

## Không làm

Không chồng UI lên danh sách đã đầy; không bịa thao tác hay kết quả công cụ.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Wide heavy white capitals and cyan brush accent in the hook; cyan initials with white bold uppercase labels in the list; smaller regular white captions in the closing body. Strong role-based typography.
- **captionMotion:** Blurred energetic hook resolves. List labels append progressively while their initials keep a stable left edge. The UI demonstration slides upward and resolves from blur/opacity, with typed text inside; these are separate animations.
- **footageMotion:** Front desk talking head with crop changes and natural gestures. UI and list movement cannot be used as evidence of a camera zoom.
- **layoutAndAssets:** Vertical A/G/E/N/T mnemonic, a large rounded dark UI card with cyan border/input/icon, then simpler body captions and a final CTA. The list yields space to the UI instead of permanently stacking both.
- **transitions:** A white flash around 2.93–3.2s separates the hook and explanation. Around 13.7–14.4s the UI rises while the previous list fades. Later it clears and list explanation resumes.
- **colorAndLighting:** Warm wood/desk base with navy clothing. White/cyan graphic palette. Dark UI surface gives the cyan control a clear focus.
- **visualFlow:** Hook → mnemonic → practical UI example → completed mnemonic → quiet explanation → CTA. Motion carries the teaching sequence.

## Các sự kiện nguồn

- **0–3.20s** — Energetic mixed typography, then white flash.
- **3.80–3.90; 7.5; 12–13; 19.5; 24–25s** — Progressive mnemonic labels.
- **13.70–18.90s** — UI card entrance, typing and tool/access state changes.
- **25–38s** — Completed list held while the speaker continues.
- **39–49; 50–51s** — Quiet body captions, event name accent, then large final CTA.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
