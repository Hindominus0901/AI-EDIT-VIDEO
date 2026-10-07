# R11 — Headline — phân tầng trên footage

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Mở bài ngắn và giải thích một cấu trúc

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Dòng dẫn thường → từ khóa lớn đậm → dòng bổ trợ; body canh trái, rule mảnh.

## Ảnh / graphic

Footage tối vừa đủ; phân đoạn theo tầng nội dung, không thêm ảnh minh họa rời.

## Motion

Keyword bật ở frame 19→20 (~0,67s); dòng bổ trợ ~1,33s; chữ neo khi nền trôi.

## Flow

Vấn đề → ba tầng giải thích → kết luận; tăng thời gian đọc so với bản gốc.

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

Không mô tả text snap thành slide; không sao phần chữ dày lướt quá nhanh.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Three headline roles: regular small setup, substantially larger bold keyword, regular small support. Body sections use a left-aligned heading, thin horizontal rule and compact bullets. Tight spacing is visible, but source font identity is not established.
- **captionMotion:** Opening hierarchy builds in stages: setup early, keyword appears fully between frames 19 and 20 at about 0.67s, support around 1.33s. These observed additions are abrupt, not a smooth text slide. Text stays anchored while the footage moves.
- **footageMotion:** From 0.60 to 3.00s, background matching estimates 3.1% shrink, image-center displacement about 8.4% of canvas width left and 2.6% of height upward, with slight rotation. This is rendered-image drift; physical camera versus edit pan is unconfirmed.
- **layoutAndAssets:** Centered opening headline changes to left-aligned funnel-section content. TOF, MOF and BOF each use a different background/section state, retaining a consistent rule and text hierarchy.
- **transitions:** Direct section/background changes around 3.57, 5.31, 7.14 and 8.81s. Some body text has little reading time in this ten-second source.
- **colorAndLighting:** Warm, darkened lifestyle/work footage beneath white text. Contrast is achieved largely by suppressing the plate rather than outlining each letter heavily.
- **visualFlow:** Opening problem, three structured stages, closing. Typographic hierarchy provides coherence even when the underlying shot moves.

## Các sự kiện nguồn

- **0–3.3s** — Anchored three-stage title above drifting/receding footage.
- **3.57–5.31s** — Top-of-funnel section.
- **5.31–7.14s** — Middle-of-funnel section.
- **7.14–8.81s** — Bottom-of-funnel section.
- **8.81–10.1s** — Closing message.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
