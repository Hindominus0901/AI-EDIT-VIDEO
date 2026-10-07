# R05 — Danh sách — một ảnh mỗi ví dụ

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Liệt kê công cụ, ví dụ hoặc ứng dụng

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Headline đen trong pill trắng; caption trắng nhỏ; số thứ tự vàng riêng.

## Ảnh / graphic

Một ảnh thấp dưới ngực; thay bằng ảnh MỚI khi đổi mục; cuối clip trả mặt sạch.

## Motion

Ảnh thay nhanh; mẫu đổi ảnh 9→8 giữa 9,5–9,6s; header đứng yên.

## Flow

Giới thiệu → số mục + ảnh đúng mục → giải thích → bỏ ảnh → mục sau.

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

Không dùng cùng ảnh cho mục khác; không chèn ba ảnh vì thiếu tư liệu.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Black sans headline in a white rounded pill; small regular white body captions; small yellow item number above a lower image. These are three distinct text roles.
- **captionMotion:** Stable header and chest-level caption zone. The body phrase changes with the speech visually; exact spoken synchronization is unassessed. Number/image swaps are quick rather than a long animated transition.
- **footageMotion:** The desk plate is visually stable in the inspected sequence, while the person and hands move. No high-confidence persistent global zoom was established.
- **layoutAndAssets:** One image at a time covers the lower torso/table. A yellow countdown number identifies each topic. The image heights/aspect treatments vary in the source; this should not be mistaken for a single consistent frame size.
- **transitions:** At 9.5s image 9 remains; by 9.6s it is replaced by image 8. Header stays fixed. Clearing the lower card near the end returns visual attention to the person.
- **colorAndLighting:** Natural desk/room lighting with a blue shirt. White/black title pill and restrained yellow numbering; inserted screenshots have their own colors.
- **visualFlow:** The repeated number → image → explanation structure gives predictable navigation. Each replacement marks a new example rather than decorating every phrase.

## Các sự kiện nguồn

- **0–4.33s** — Speaker and permanent headline, without the first lower image.
- **4.40–9.50s** — First numbered image held.
- **9.60; 16.7; 21.5; 28.9; 33; 38.7; 44; 48s** — Approximate subsequent item/image replacements.
- **54–60s** — Image layer clears for the closing speaker passage.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
