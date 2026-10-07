# R14 — Founder — lời nói dẫn hình

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Chia sẻ, kể chuyện hoặc lời khuyên cần cảm giác tự nhiên

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Sans trắng thường, cỡ vừa/nhỏ; không highlight liên tục; nhẹ hơn R16.

## Ảnh / graphic

Người nói là chính; chèn cảnh công việc cụ thể rồi trả về mặt; không có collage thường trực.

## Motion

Push nguồn +26,4% trong 4,004s; caption neo; có các reset rộng hơn.

## Flow

Người nói → ví dụ công việc thật → trở về lập luận → khoảng nghỉ → câu chốt.

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

Không tự thêm ảnh để lấp khoảng trống; không zoom liên tục suốt đoạn dài.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Regular white sans phrase captions with restrained shadow. Text is much smaller and quieter than R15/R16, despite similar outdoor talking-head material. No constant colored emphasis.
- **captionMotion:** Caption size and screen position stay stable through the opening push. Phrases change without conspicuous travel or bounce. This restraint is a specific source behavior, not evidence that every reference has static text.
- **footageMotion:** Opening background scale increases about 26.4% from 0 to 4.004s, near-zero rotation. Wider crop resets later include about 21.9–22.0s and 26.2–26.4s. Architectural footage near 46–53s has forward-moving perspective; physical camera mechanics remain unconfirmed.
- **layoutAndAssets:** Mostly full-frame speaker and purposeful work/lifestyle coverage, with one quiet caption layer. No persistent asset collage.
- **transitions:** Direct coverage cuts and occasional wider reset after a push. Text remains an anchor through shot changes.
- **colorAndLighting:** Soft natural green background on the speaker, warm/darker work interiors and architectural light. No exact LUT is identified.
- **visualFlow:** Speaker-led advice breathes between coverage passages. The restrained typography makes changes of framing and shot content more noticeable.

## Các sự kiện nguồn

- **0–4.004s** — Centered gradual push of roughly 26% rendered image scale.
- **4.3–7.17; 8.22–19.98s** — Panel and work/writing coverage.
- **20–28s** — Talking head with wider reframing changes.
- **29–31; 37–38s** — Work and lifestyle inserts.
- **46.42–52.76; 55–59s** — Architectural motion and later work coverage.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
