# R02 — Editorial Việt — card & khoảng nghỉ

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Giải thích khái niệm, chia sẻ có chiều sâu

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Hai cấp sans đậm; shadow nhẹ trên footage, trắng/đen rõ trên title card.

## Ảnh / graphic

Card hồ sơ vào riêng rồi rời riêng; một insert bo góc; sơ đồ nhỏ khi thật sự cần.

## Motion

Card rõ dần; title 34,72–35,32s blur-to-clear; đổi nền trước rồi mới đổi chữ.

## Flow

Người nói → cụm minh chứng → xóa cụm → title chốt → người nói.

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

Không giữ card ở mọi đoạn; không bật blur cho tất cả caption.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Heavy Vietnamese sans serif, white on footage or black cards, black on light cards. Two-line emphasis uses a noticeably larger key line. Soft black shadow is visible over footage; full-screen cards rely on contrast rather than a large outline.
- **captionMotion:** Selective emphasis rather than a subtitle on every moment. Three profile cards resolve from blur/low opacity and later fade separately. The black title at 34.72s begins blurred and is readable around 35.32s. An inversion sequence changes the background first, then fades in the new dark phrase.
- **footageMotion:** Main front-facing desk shot with occasional side angle and closer crops. Crop steps include a visible change around 3.48s and another around 41.5s. Stable typography is separate from those framing changes.
- **layoutAndAssets:** Warm desk/lamp base; three floating dark profile cards form a temporary composition around the speaker. Later: individual profile cards, a rounded film insert over a blurred base, a compact equation, books, and a bookmark/cursor CTA.
- **transitions:** Cards enter in a stagger, hold, and clear before the next caption. Around 8.08s, black switches to off-white; the replacement black phrase resolves from gray by about 8.48s. This is not a generic sliding transition.
- **colorAndLighting:** Warm amber practical lamp and soft indoor skin tones. Off-white/black cards keep visual contrast. Yellow is reserved for the final bookmark accent; no original grade recovered.
- **visualFlow:** Quiet speaker passages alternate with concentrated editorial moments. The reference creates polish through staging and clearing, not by putting several permanent overlays around the face.

## Các sự kiện nguồn

- **0.30–3.60s** — Profile cards arrive left, right, lower-center; sharp by about 1.2s. Staggered clearing around 2.4–3.28s, caption returns by 3.6s.
- **6.76–9.36s** — Black Worldbuilding card, then light thế giới riêng card.
- **9.36–10.68; 55.52–60.92s** — Side-angle coverage.
- **14; 18–20s** — Individual profile/page references.
- **22–28s** — Closer talking-head framing.
- **29.40–33.60s** — Rounded action-film insert over blurred speaker background.
- **34.72–37.36s** — Blur-to-clear black headline card.
- **45–49s** — Emphasis heading, compact value equation, then book cards.
- **53–57; 61–64s** — Two-tier captions; bookmark icon becomes yellow with cursor cue and final emphasis.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
