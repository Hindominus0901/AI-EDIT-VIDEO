# Học cách biên tập từ reference

Áp dụng khi nghiên cứu ref hoặc dựng theo ref. Yêu cầu ngày 29/09/2026: nghiên cứu kỹ, bản dựng có chủ ý và giảm token. Đọc cùng style-packages.md; không thay gu đã duyệt bằng preset mới.

## Hai công việc tách biệt

- Nghiên cứu: làm một lần cho nguồn chưa hiểu; lưu bằng chứng có timestamp và bài học có điều kiện áp dụng.
- Dựng: lấy bài học phù hợp nội dung mới; không đọc lại toàn thư viện, đo lại ref hoặc chạy lại STT mỗi video.

Trong engine, chạy `python scripts/reference-index.py` để chọn ref theo nội dung. Chỉ đọc package và bằng chứng của ref đã chọn. Sổ nghiên cứu hiện tại: `asset-library/reference-learning/RESEARCH.md`. Không nạp catalog JSON lớn, toàn bộ lịch sử sửa, hay mọi contact sheet để chọn gu.

Đọc `asset-library/reference-learning/LESSONS.md` để lấy bài học ngắn đã có trước khi phân tích lại. Chi tiết R14/R15/R16 ở từng file `Rxx-study.md`; ASR có hash/cache trong `out/reference-learning/`. Các bài học hiện mới dựa trên lời ASR và frame, chưa chứng nhận nghe mix hoặc chuyển thể thành công. Đừng biến chúng thành quota mới.

## Một ref chỉ được coi là đã nghiên cứu đầy đủ khi có

1. Cấu trúc toàn bài: lời hứa, cách triển khai, tương phản, điểm đọng lại; ghi rõ thông tin đến từ transcript đã rà, caption nguồn hay nghe trực tiếp.
2. Beat có bằng chứng: khoảng nguồn, lời/ý, người xem đang cần hiểu gì, hành động dựng và vào/giữ/ra. Phân biệt quan sát với suy luận về dụng ý của editor.
3. Nhịp hình: cả cảnh nhấn và cảnh để yên, chuyển động footage riêng chữ/asset. Không suy easing từ ảnh tĩnh hay gán cùng animation cho mọi câu.
4. Nhịp tiếng: đã nghe khoảng nào; hơi thở, điểm nối, ngừng trước/sau câu chốt, nhạc và SFX tương tác thế nào. Đo loudness hoặc transcript không thay nghe. Công cụ không hỗ trợ nghe thì ghi pending, tiếp tục phần nhìn/đo độc lập.
5. Điều kiện chuyển thể: dùng khi nào, tránh khi nào, cần footage gì, yếu tố nào được thay theo nguồn mới. Số đo của ref không tự thành quota chung.
6. Bài thử chuyển thể: một đoạn đại diện đủ setup → nhấn → nghỉ/reset, thường 20–30 giây nếu nội dung phù hợp. So với ref về vai trò/nhịp/phân cấp; không chỉ đối chiếu màu/font. Không lấy media ref làm asset sản xuất.

Không yêu cầu người dùng duyệt thêm nếu đã được quyền dựng. Khi nhiệm vụ chỉ là nghiên cứu, lưu bài học và lỗ hổng; không tự dựng lại clip cũ.

## Trước khi chọn hiệu ứng

Viết ngắn trong kế hoạch dự án: người xem cần nhớ gì; câu nào dẫn vào; đoạn nào bỏ/giữ và vì sao; khoảnh khắc mạnh nhất; chỗ nào cố ý để yên. Sau đó lập beat sheet và chọn asset.

Mỗi can thiệp đáng kể có: ý nguồn → tác dụng mong muốn → dẫn chứng ref → cách chuyển thể → điều kiện bỏ can thiệp. Ví dụ: bỏ hình mà ý vẫn rõ và không mất cảm xúc thì cân nhắc giữ người nói. Không ép mọi beat phải có graphic; không dùng câu giải thích chung như “tăng engagement” cho tất cả.

## Chi phí và vòng sửa

- AI hiện tại hiểu nội dung và ra quyết định một lần; code chia caption/căn thời gian/kiểm tra/render. Không gọi LLM lồng hay panel nhiều agent mặc định.
- Giữ một hồ sơ ngắn trong dự án: brief, ref chính, quyết định đã chốt, vấn đề còn lại, đường dẫn transcript/EDL/asset. Cập nhật phần thay đổi, không chép lại toàn bộ.
- Dùng lại phân tích/cache theo đúng nguồn và phiên bản. Chỉ xem lại khoảng có sửa hoặc bằng chứng còn thiếu; không giảm chất lượng xuất cuối âm thầm.
- Trước bản dài kiểm tra đoạn đại diện. Sau render kiểm tra kỹ thuật tự động và review hình/tiếng trong phạm vi công cụ thật sự hỗ trợ.
- Khi chưa có telemetry token, chỉ báo số thao tác/lượt gọi đã tránh; không hứa phần trăm tiết kiệm hoặc báo số token ước đoán như số đo thật.
