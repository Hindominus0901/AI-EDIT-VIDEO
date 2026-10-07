# R13 — Cửa sổ — mở từ một đường mảnh

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Đoạn mở yên hoặc chuyển sang cụm footage có chủ đích

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

POV nhỏ hai dòng trên cửa sổ; không dùng cỡ chữ đó làm phụ đề dài.

## Ảnh / graphic

Canvas đen, cửa sổ bo góc, khoảng trống rộng; các shot thay bên trong cùng khung.

## Motion

Mask cao 6px→434px trong ~0,17–2,00s ở canvas 720×1280; không phải zoom footage.

## Flow

Giữ một nhịp → mở khung → vài shot trong khung → trả về nội dung chính.

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

Không thu nhỏ người nói cả bài; không tự rút reveal xuống 0,2s và gọi là giống mẫu.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Very small centered two-line white POV heading above the image window. Upper line is bolder than the quoted second line; large negative space makes the tiny heading visible but does not make it appropriate for subtitles.
- **captionMotion:** Headline remains anchored. Main entrance motion belongs to the window mask: a horizontal slit opens vertically into a rounded landscape image over about two seconds.
- **footageMotion:** After the reveal, different activity shots cut inside the same window geometry. The window expansion is not a footage zoom and is not reversed playback.
- **layoutAndAssets:** Black portrait canvas, central rounded landscape window, small heading above. Thresholded visible image around 2s is approximately x=80, y=422, w=557, h=434 on 720×1280. This is an approximate visible-content box, not a recovered matte or proof of a standard aspect ratio.
- **transitions:** Mask/reveal opening: visible height grows from about 6px at 0.17s to 65px at 0.50s, 217px at 1.00s, 381px at 1.50s and 434px at 2.00s. Subsequent interior shots cut while the outer canvas stays fixed.
- **colorAndLighting:** Black negative space surrounds mixed daylight/night work scenes. Rounded edges and restrained white text define the look more than a strong accent color.
- **visualFlow:** Slow reveal creates an opening pause, then brief activity cuts maintain interest inside a stable frame.

## Các sự kiện nguồn

- **0–2.00s** — Vertical reveal of the image window from a thin slit.
- **2–10.9s** — Stable outer layout; alternating activity/day/night imagery inside.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
