# S03 — Caption Việt — dòng chốt lớn

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Talking head Việt hoặc footage minh chứng có caption

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Sans trắng đậm, shadow mềm; dòng chốt lớn hơn; cụm khoảng 4–5 từ giữ trọn nghĩa.

## Ảnh / graphic

Chữ ở ngực dưới mặt; có thể qua cảnh b-roll nhưng vẫn giữ vùng đọc.

## Motion

Ảnh chụp chỉ cho biết trạng thái chữ/opacity, không xác định đường easing hay thời gian vào.

## Flow

Nêu ý → cụm dẫn → từ/cụm chốt lớn hơn → trở lại cỡ thường.

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

Không phóng to mọi từ, không để phụ đề dài suốt câu; không lấy số view làm nội dung.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Sans trắng đậm, shadow mềm; dòng chốt lớn hơn; cụm khoảng 4–5 từ giữ trọn nghĩa.
- **layoutAndAssets:** Chữ ở ngực dưới mặt; có thể qua cảnh b-roll nhưng vẫn giữ vùng đọc.

## Các sự kiện nguồn



## Chưa xác minh

- Motion/easing/timing: không xác minh từ screenshot
- Font gốc chưa định danh
- Nhạc/SFX không có bằng chứng từ ảnh
