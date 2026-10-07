# R08 — Danh sách hai cột — dùng có chọn lọc

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Checklist nhiều mục khi người dùng chủ động cần

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Pill trắng tiêu đề đen; nguồn có chữ danh sách rất nhỏ và viền mạnh.

## Ảnh / graphic

Hai cột tích lũy. Bản Việt chia trang 4–6 mục để đọc được trên điện thoại.

## Motion

Hàng thêm trực tiếp tại vị trí cố định; không đo được tween phức tạp.

## Flow

Nêu nhóm → hiện từng mục → giữ đủ đọc → xóa nhóm rồi sang nhóm mới.

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

Không sao lỗi 30 mục phủ kín mặt; mặc định không chọn gói này cho clean.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Large black regular sans in a white rounded headline pill; small white supporting text and very small outlined list text. The source uses outlines much more heavily than the clean editorial examples.
- **captionMotion:** Items append abruptly into fixed rows. In the close sample, additional rows become visible around 1.4s and 1.8s. No elaborate tween is established for those additions.
- **footageMotion:** Talking-head plate appears stable while gestures continue. Dense overlays dominate the image; global-motion analysis is not a reliable substitute for layer separation here.
- **layoutAndAssets:** Two columns, numbered 1–15 on the left and 16–30 on the right. Approximate left edges x=14% and 62% of the 720px canvas. Row spacing is roughly 2.3% of canvas height; visible letter height around 1.7% is very small.
- **transitions:** Mostly accumulative appearance and hold, without clearing early rows. Little negative space remains at the end.
- **colorAndLighting:** White pill, white text with dark outline over normal room footage. No restrained accent palette distinguishes list levels.
- **visualFlow:** The list is a completion/counting device. It shows a mechanism for accumulation but also demonstrates the clutter and readability risks the user wants to avoid.

## Các sự kiện nguồn

- **0–10s** — Left column fills progressively.
- **10–20s** — Right column fills to thirty items.
- **20–21s** — Dense completed list remains visible.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
