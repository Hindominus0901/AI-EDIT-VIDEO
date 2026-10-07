# Iman Gadzhi, Alex Hormozi, Dan Martell

Yêu cầu workspace ngày 29/09/2026: nâng bộ dựng để hướng tới ba creator này, giữ chi phí token thấp. Không hiểu là đã duyệt mọi demo hoặc muốn trộn ba ngôn ngữ hình trong một clip.

1. Đọc `UPGRADE-1.6.md` và `UPGRADE-1.6.1.md` ở engine. `creatorStyle` có renderer thật nhưng fidelity vẫn là bản chuyển thể đang thử.
2. Chỉ chọn một hướng chính: Iman cho tuyến kể chuyện/vật neo/bằng chứng; Hormozi cho câu mở và lập luận trực tiếp; Martell cho vấn đề/quy trình/hành động. Đây là cách phân công của bộ dựng, không phải mô tả mọi video của họ.
3. Nghiên cứu ref người dùng đưa, hoặc nguồn chính chủ; ghi timestamp, phần đã nhìn/nghe và điều chưa biết. Không lấy thumbnail làm motion ref. Học cả câu chuyện và khoảng để yên.
4. Trước asset: audience/premise/payoff, câu mở, ý mạnh nhất, chỗ cần giữ biểu cảm. `scenes` ghi meaning/reason. Bằng chứng không có thì giữ người nói, không bịa biểu đồ/số liệu.
5. Thực thi layout thật, không đổi tên premiumSet. Hai layout hình động `content-flood` và `salt-ocean` chỉ dùng khi đúng phép so sánh nguồn; không biến thành hiệu ứng mặc định. Profile style iman/hormozi/martell map vào creatorStyle, không map vào premiumSet.
6. Âm nhạc: dùng tài nguyên hợp lệ, đo mức âm và nghe nếu có công cụ. Với creator edit cần hậu kỳ giọng/nhạc/màu, dùng `scripts/creator-finishing.py` theo nguồn cụ thể và kiểm tra mix cuối; không coi Remotion volume đơn thuần là xử lý âm. Không gán tiếng vào mọi cảnh. Không lược hơi thở chỉ để tăng tốc.
7. Đọc `project-context.json` trước (nếu có), xác nhận với EDL hiện tại khi file đã sửa; dùng một transcript và một host plan. Sửa nhỏ ở EDL đang dùng, chỉ đọc cảnh liên quan. Không đọc lại toàn thư viện, không gọi LLM lồng/agent panel mặc định. CLI offline không có nghĩa hiểu câu chuyện tự động.
8. Xuất đoạn đủ setup/nhấn/reset, kiểm tra chữ có dấu, mặt/tay, nhịp cảnh và âm. Demo kỹ thuật không phải bằng chứng đạt phong cách. Sau đó dựng toàn bộ trong phạm vi yêu cầu người dùng.
