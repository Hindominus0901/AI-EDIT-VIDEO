# S02 — So sánh — khung tròn & cutout

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Hai vế cần đối chiếu rõ, nguồn có thể tách người sạch

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Hai nhãn đen, số/từ xanh và đỏ lớn; nhãn giải thích đen phía dưới.

## Ảnh / graphic

Canvas trắng ngà; nguồn trong khung tròn, đầu vượt mép; vùng chữ tách khỏi mặt.

## Motion

Chỉ có ảnh: timing từng nhãn và cutout là đề xuất, không có dữ liệu chuyển động gốc.

## Flow

Nêu tiêu chí → nhãn hai vế → giải thích lần lượt → bỏ bảng → trở về người nói.

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

Không ép cutout lên nguồn có chữ đóng vào tóc; đổi sang khung sạch nếu matte lỗi.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Hai nhãn đen, số/từ xanh và đỏ lớn; nhãn giải thích đen phía dưới.
- **layoutAndAssets:** Canvas trắng ngà; nguồn trong khung tròn, đầu vượt mép; vùng chữ tách khỏi mặt.

## Các sự kiện nguồn



## Chưa xác minh

- Motion/easing/timing: không xác minh từ screenshot
- Font gốc chưa định danh
- Nhạc/SFX không có bằng chứng từ ảnh
