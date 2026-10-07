# S01 — Headline serif — hai khối trắng

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Mở bài chia sẻ cá nhân

## Font đề xuất

Times New Roman — chưa xác nhận font gốc

## Phân cấp chữ

Serif đen thường; hai khối trắng nối, dòng hai hẹp hơn; không nhồi caption lên headline.

## Ảnh / graphic

Một speaker full-frame; headline nằm vùng trống trên đầu.

## Motion

Chỉ có ảnh: đề xuất fade 160ms rồi giữ, KHÔNG phải motion đo từ ref.

## Flow

Headline mở → thời gian đọc → bỏ headline → caption body sạch.

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

Không đặt chữ lên mắt; không tự khẳng định Times New Roman là font gốc.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Serif đen thường; hai khối trắng nối, dòng hai hẹp hơn; không nhồi caption lên headline.
- **layoutAndAssets:** Một speaker full-frame; headline nằm vùng trống trên đầu.

## Các sự kiện nguồn



## Chưa xác minh

- Motion/easing/timing: không xác minh từ screenshot
- Font gốc chưa định danh
- Nhạc/SFX không có bằng chứng từ ảnh
