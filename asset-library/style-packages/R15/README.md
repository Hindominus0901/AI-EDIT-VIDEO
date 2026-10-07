# R15 — Sách & sản phẩm — một nhóm thông tin

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Review sách, sản phẩm hoặc tài liệu xác định được

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Tên vật thể lime đậm, tác giả/nhãn phụ trắng nhỏ, caption lời nói trắng đậm riêng.

## Ảnh / graphic

Hook grid bìa sách; body một vật thể + tên + tác giả; hết ý thì cả nhóm biến mất.

## Motion

Nền trắng/cutout 0,58s; grid stagger 0,8–1,42s; body cover vào rồi nghiêng ổn định.

## Flow

Grid hứa danh sách → từng sản phẩm với luận điểm riêng → người nói sạch → kết.

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

Không dùng bìa một sách để nói sách khác; không giữ grid ở toàn bài.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Short bold white body captions, larger than R14. Book titles use lime bold sans, authors smaller white type. The intro uses lime words inside compact black rectangles. Titles, authors and spoken captions are separate roles.
- **captionMotion:** Book-title phrases reveal in stages; the cover enters with opacity and changing angle. At the second callout, number 2 appears, then Essentialism, then the author line. Source English body captions are often one-to-three words and should not be copied mechanically into Vietnamese.
- **footageMotion:** Hook isolates the person, then shrinks/repositions the cutout down/right as the grid grows. In body footage, pushes alternate with wider resets; the reset around 10.3s makes room for the next book callout.
- **layoutAndAssets:** Nine covers form a 3×3 grid on white in the hook. Later each book is a grouped title/author/cover object; several covers are tilted or shown with perspective. One grouped object is clearer than disconnected ornaments.
- **transitions:** Background whitens around 0.58s while the person remains; covers build around 0.8–1.42s and settle by about 1.6s. Return to full footage around 4.09s. At 10.3s, wider framing and the next object entrance are coordinated.
- **colorAndLighting:** White/black/lime graphic hook, natural green talking head, mixed book cover colors. The cover collection contributes color while the supporting typography stays consistent.
- **visualFlow:** Grid promises the list; sequential book callouts explain it; empty speaker passages prevent a permanent crowded wall of covers.

## Các sự kiện nguồn

- **0.58–1.60s** — Background removal appearance, cutout reposition/scale, staggered nine-book grid.
- **1.6–4.09s** — Completed hook layout held, then return to footage.
- **About 5; 11; 17; 29; 35; 51; 66; 80; 87s** — Nine book callout passages.
- **10.22–10.72s** — Close shot → wider reset → cover and number/title/author build.
- **96–99s** — Clean talking-head closing without the grid.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
