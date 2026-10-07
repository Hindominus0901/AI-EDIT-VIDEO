# Dựng video bằng AI — bắt đầu ở đây

Bạn chỉ cần đưa video và nói muốn làm gì. AI sẽ hỏi tối đa 3 câu còn thiếu, kiểm tra bộ dựng rồi làm một bản hoàn chỉnh. Không cần nhớ lệnh hay tên hiệu ứng.

Có thể yêu cầu hướng **Iman Gadzhi**, **Alex Hormozi** hoặc **Dan Martell**. Bộ dựng 1.6 hỗ trợ cảnh theo ý, so sánh, từng bước và bằng chứng; gửi ref cụ thể để đối chiếu đúng gu. Các hướng đang là bản chuyển thể, không phải bản sao mặc định. Xem [nâng cấp 1.6](UPGRADE-1.6.md).

**Câu bắt đầu để sao chép:**

> Đọc BAT-DAU.md và hướng dẫn Dựng video Việt trong thư mục này. Hãy kiểm tra và thiết lập bộ dựng giúp tôi. Tôi muốn dựng video cho người Việt; chỉ hỏi những điều còn thiếu, tối đa 3 câu, rồi làm một bản MP4 kèm phụ đề SRT.

## Nếu dùng ChatGPT Work

1. Giải nén gói vào một thư mục riêng. Phần chạy dựng nằm trong thư mục `engine`.
2. Với video trên máy tính, chọn **Work locally** nếu tài khoản có lựa chọn này. Cho phiên làm việc truy cập thư mục bộ dựng và video bạn muốn dùng.
3. Đưa file hướng dẫn này vào cuộc trò chuyện và gửi câu bắt đầu ở trên. AI phải kiểm tra quyền đọc/ghi, công cụ và xuất thử trước khi báo sẵn sàng.
4. Muốn AI tự nhận biết trong những cuộc trò chuyện sau: cài plugin `video-editor-viet` bằng cơ chế plugin mà Work của bạn hỗ trợ. Đọc [cách tích hợp](.agents/skills/dung-video-viet/references/chatgpt-work.md). Đính kèm ZIP hoặc Markdown đơn thuần chưa có nghĩa đã cài plugin.

Chạy trên cloud cần đưa tệp vào môi trường đó và có đủ công cụ dựng; một đường dẫn `C:\...` không cấp quyền truy cập máy tính. Nếu chưa có tùy chọn cài plugin, vẫn có thể dùng hướng dẫn này làm ngữ cảnh cho từng phiên có đủ công cụ.

## AI có thể hỏi gì?

- Video nói về gì, dành cho ai?
- Đăng ở đâu, muốn dài khoảng bao lâu? Video dọc **9:16** hay ngang **16:9**?
- Bạn thích **gọn và chuyên nghiệp**, **nhẹ và tinh tế**, hay **đen trắng rõ ý**? Có thể trả lời “bạn tự chọn”.

Đã nói rồi thì AI bỏ qua câu đó. Nếu đã có gu của kênh, AI dùng tiếp; yêu cầu của video hiện tại luôn được ưu tiên.

## Một yêu cầu đủ để bắt đầu

> Dựng video này cho người mới kinh doanh, đăng Reels dọc 9:16 khoảng 60 giây. Giữ giọng tự nhiên, chữ tiếng Việt 4–5 từ mỗi lần, nhấn từ khóa vừa phải. Chèn ảnh trực tiếp khi có ích, nhạc nhẹ dưới giọng, ít âm thanh hiệu ứng. Giao một bản MP4 và SRT; bạn tự chọn các chi tiết còn lại.

## Sau bản đầu

Nói cụ thể như “đoạn 00:12 chữ che mặt”, “bỏ nhạc”, “bớt cắt ở đầu”, hoặc “giữ kiểu này cho kênh kiến thức”. AI sửa từ bản đang có, dùng lại transcript; không nhận giọng lại chỉ để đổi font.

Xem [hướng dẫn đầy đủ](HUONG-DAN.md) hoặc mở [trang hướng dẫn](bat-dau.html). Bộ mẫu: [ba kiểu dựng](asset-library/premium-kit/index.html).

---

**Dành cho AI:** đọc `.agents/skills/dung-video-viet/SKILL.md`, làm theo ngữ cảnh người dùng và quyền hiện có. Tìm engine thật trước khi chạy; không báo “đã cài” hoặc “đã ghi nhớ” khi chưa thực hiện thành công.
