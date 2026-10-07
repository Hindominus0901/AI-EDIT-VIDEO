# Thử trực tiếp trong ChatGPT Work

Đây là kịch bản kiểm thử đã chuẩn bị; chưa phải kết quả chạy trên Work.

## Bước 1 — người dùng mới

Gắn gói video-editor-viet và cho Work quyền đọc thư mục đã giải nén. Với Work locally, dùng thư mục engine trong gói. Với cloud, đưa gói vào môi trường cloud; không gửi đường dẫn ổ C như thể Work đã đọc được.

Gửi:

> Hãy đọc BAT-DAU.md trong engine và dùng skill Dựng video Việt đi kèm. Tôi muốn thiết lập bộ dựng cho một kênh nội dung tiếng Việt. Hãy hỏi tối đa ba câu cần thiết để hiểu nhu cầu rồi kiểm tra môi trường. Chưa cần dựng video thật; trước hết dùng nguồn tổng hợp trong bộ dựng để xác minh setup. Đừng báo đã cài plugin chỉ vì đã đọc file.

Kỳ vọng: AI đọc đúng hướng dẫn, kiểm tra quyền và chỉ hỏi nhóm thông tin chưa có. Thiếu runtime hoặc quyền phải báo cụ thể; không hứa chạy trên máy khi đang ở cloud.

## Bước 2 — trả lời thử

> Kênh thử tên kiem-thu-work, chia sẻ kiến thức cho người mới kinh doanh. Dọc 9:16, gọn chuyên nghiệp, không nhạc và không hiệu ứng âm thanh. Nhớ lựa chọn này cho kênh thử. Bạn tự xử lý các chi tiết còn lại. Hãy xuất đoạn thử 3 giây có dấu tiếng Việt và SRT để xác minh setup, dùng nguồn tổng hợp, không dùng video khách hàng.

Kỳ vọng: lưu đúng hồ sơ kênh, cài phần phụ thuộc cần thiết trong thư mục làm việc được phép, chạy smoke-test, kiểm tra tệp thật. MP4 1080x1920, H.264, lời thử có dấu; SRT đúng nội dung/thời gian. Clip thử không có lời nói nên không đánh dấu STT đã được kiểm thử.

## Bước 3 — sửa một lượt

> Riêng bản thử này xuất thêm ngang 16:9. Giữ nguyên gu, đừng nhận giọng hoặc lập lại kế hoạch. Cho tôi xem hồ sơ kênh sau khi xuất.

Kỳ vọng: thêm bản 1920x1080 từ EDL có sẵn, không chạy STT; gu mặc định kênh vẫn là dọc 9:16. Không thay đổi file nguồn hay EDL đã chỉnh tay.

## Bằng chứng cần lưu

Host và chế độ Work thật, phiên bản công cụ, kết quả kiểm tra môi trường, đường dẫn MP4/SRT, metadata video, nội dung hồ sơ trước/sau và điều còn chưa kiểm chứng. Chỉ xác nhận tự nhận skill trong chat mới sau khi plugin đã thực sự được cài/bật bằng cơ chế host hỗ trợ.

Cài bằng hướng dẫn một phiên và cài plugin để tự nhận trong các phiên sau là hai phép thử riêng. Không lấy kết quả local từ Codex để điền vào kết quả Work.
