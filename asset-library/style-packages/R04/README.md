# R04 — Teaser — headline giữ nguyên

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Thông điệp ngắn 5–10 giây, dẫn người xem đọc thêm

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Headline in hoa đậm, dòng phụ thường, số liệu đậm; CTA nghiêng.

## Ảnh / graphic

Một cảnh chuyển động làm nền; một cụm chữ phân cấp, không thêm sticker.

## Motion

Chữ giữ suốt cảnh; chuyển động đến từ video phía sau. Không có bằng chứng tween chữ.

## Flow

Một lời hứa rõ → thời gian đọc → CTA.

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

Không dùng form sáu giây này cho cả bài nói dài; không tự tạo phần trăm.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** White all-cap bold heading, regular support, bold percentage statement, downward arrow and italic CTA. The hierarchy mixes weight and case rather than multiple unrelated decorative faces.
- **captionMotion:** The text stack stays present through the six-second shot. No distinct caption entrance animation established; holding the message is an intentional part of this reference.
- **footageMotion:** Meeting-room footage contains a handheld pan and moving people. A failed global transform fit does not mean the video is static.
- **layoutAndAssets:** Centered text stack over a darkened room, with a small upper-right watermark. Generous separation between headline, explanation, arrow and CTA.
- **transitions:** One held composition; no full-scene cut observed in the timeline samples.
- **colorAndLighting:** Dark exposure treatment increases white-text contrast while the room remains visible. No exact grading parameters recovered.
- **visualFlow:** A brief teaser designed to send viewers to the caption. It does not demonstrate a long-form talking-head edit flow.

## Các sự kiện nguồn

- **0–5.9s decoded picture** — Text stack remains stable while the meeting footage moves beneath it.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
