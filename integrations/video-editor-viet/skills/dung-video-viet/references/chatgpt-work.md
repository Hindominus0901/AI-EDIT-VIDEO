# ChatGPT Work: tích hợp có kiểm chứng

Tài liệu kiểm tra ngày 20/09/2026:

- [Bắt đầu với Work](https://learn.chatgpt.com/docs/get-started-with-work): desktop có thể dùng tài nguyên local khi công cụ có sẵn; chọn Work locally cho tệp/app trên máy.
- [Skills](https://learn.chatgpt.com/docs/build-skills): skill có thể được chọn theo mô tả; người dùng cũng có thể gõ @ để chọn trong ChatGPT. Skill trong plugin là cách phân phối dùng lại giữa các giao diện hỗ trợ.
- [Plugins](https://learn.chatgpt.com/docs/build-plugins): manifest, kiểm tra ở nguồn cục bộ, rồi cài và thử trong cuộc trò chuyện mới. Không suy ra việc xuất ZIP đồng nghĩa đã cài.

## Dùng ngay trong một phiên local

Người dùng giải nén gói và đưa `BAT-DAU.md` trong thư mục `engine` cho Work đọc, hoặc chỉ rõ đường dẫn thực sự truy cập được. Làm theo điểm vào đó; không cần Claude Code. Cách này cung cấp ngữ cảnh cho phiên, chưa cài skill toàn cục.

## Muốn AI tự nhận ra ở những lần sau

Gói có `.codex-plugin/plugin.json` và `skills/dung-video-viet/SKILL.md`. Dùng luồng cài plugin mà host hiện có; có thể gọi `@plugin-creator` để thêm thư mục plugin vào nguồn cục bộ và hướng dẫn cài. Kiểm tra những công cụ và nút có thật trước khi hướng dẫn chi tiết. Không bịa nút Upload ZIP hoặc hứa tự cài chỉ bằng kéo thả ZIP vào chat. Thử ở chat mới sau cài. Nếu tự nhận diện chưa kích hoạt, gõ @ và chọn “Dựng video Việt”.

## Kiểm tra trước khi nhận dựng

1. Thấy skill và bộ dựng thực sự?
2. Đọc được video và ghi được vào thư mục đầu ra?
3. Có công cụ chạy lệnh, Node/npm, Python, FFmpeg, Remotion? Nguồn mới có thư viện nhận giọng?
4. Xuất thử file ngắn và mở được trước khi báo cài đặt hoàn tất.

Cloud có thể làm phần mà công cụ của phiên cho phép. Nếu không có môi trường dựng hoặc nguồn local chưa được chuyển tới, bàn giao brief/plan và hướng dẫn tiếp bước local. Không dùng đường dẫn Windows như thể đã có trên cloud.

Gói này không kèm MCP render server và không giả lập timeline kéo thả bằng trang xem video. Các hướng dẫn, preflight, hồ sơ và dựng local có thể test riêng; kiểm thử trực tiếp trên tài khoản ChatGPT Work vẫn cần một phiên Work thật có gói được cài.
