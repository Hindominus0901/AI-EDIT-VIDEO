# Hướng dẫn cho người dùng Việt

Bắt đầu nhanh ở [BAT-DAU.md](BAT-DAU.md). Bạn giao việc bằng lời; AI phụ trách kiểm tra máy, chọn cách dựng, tìm tài nguyên phù hợp và xuất tệp.

## Chuẩn bị lần đầu

Đưa một video nguồn và cho AI biết kênh đang làm. Nếu đã có ảnh, logo, nhạc hoặc video mẫu, gửi cùng. File video mẫu giúp đánh giá chuyển động và nhịp cắt; ảnh chụp chỉ cho thấy bố cục tại một thời điểm. Link không đọc được thì AI phải nói rõ, không giả vờ đã xem.

AI kiểm tra Python, Node.js, FFmpeg/ffprobe, Remotion và công cụ nhận giọng. Phần phụ thuộc của dự án được cài vào thư mục riêng khi cần; lần đầu cần mạng để tải. Không cần tài khoản Claude hay API key cho luồng clean dùng AI trong cuộc trò chuyện. Thiếu phần mềm hệ thống hoặc quyền thì AI nêu đúng thứ còn thiếu, không chạy vòng lặp cài đặt.

Sau kiểm tra, AI xuất thử một đoạn ngắn có dấu tiếng Việt. Việc tìm thấy công cụ chưa chứng minh xuất video thành công. Tốc độ thực tế tùy thời lượng, cấu hình máy và độ phức tạp.

## Chọn cách dựng

| Cách nói với AI | Kiểu dựng | Hợp với |
|---|---|---|
| Gọn và chuyên nghiệp | Studio | Chia sẻ chuyên môn, người nói trước máy quay |
| Nhẹ và tinh tế | Paper | Kể chuyện, ảnh, nội dung có khoảng thở |
| Đen trắng rõ ý | Mono | Quan điểm, so sánh, câu chốt ngắn |
| Giữ gu sạch đang dùng | Clean | Tiếp tục bản dựng đã quen |

Không phải chọn mỗi lần. Người mới chưa có gu dùng Studio; người đã có hồ sơ giữ gu cũ. Mặc định một bản dựng, một tỷ lệ; chỉ thêm bản ngang/dọc khi bạn cần. Không đổi chất lượng cuối để giảm thời gian mà không nói rõ.

## Bạn sẽ nhận gì?

- MP4 có hình, phụ đề được thiết kế và âm thanh đã chọn.
- SRT chứa lời và thời gian để dùng lại. SRT không lưu màu, font hay hiệu ứng chữ.
- Một ghi chú ngắn về thay đổi chính và phần cần kiểm tra nếu công cụ không xem/nghe được.

AI chia phụ đề thường 4–5 từ, có thể ngắn hơn để trọn ý; không tách cụm như “thương hiệu” chỉ để đủ số. Giữ đúng dấu Việt, tên riêng, số liệu và từ phủ định. Nguồn tiếng Anh không tự đổi thành tiếng Việt trừ khi bạn yêu cầu dịch.

## Đưa nhạc, ảnh và hiệu ứng

Bạn có thể đưa tài nguyên sẵn hoặc nói “tự tìm nhạc nhẹ, ấm, không lời”. AI ưu tiên tài nguyên của bạn rồi nguồn có giấy phép rõ; ghi nguồn và credit nếu giấy phép yêu cầu. Thư viện kèm gói có nhạc CC0 và âm thanh Kenney CC0. Giấy phép sử dụng không đảm bảo mọi nền tảng sẽ không phát sinh Content ID.

Ví dụ: “chỉ dùng ảnh tôi gửi”, “không nhạc”, “thêm tiếng chuyển nhẹ ở hai ý chính”, “có thể tạo thêm ảnh khi thật sự cần”. Nếu cần công cụ tạo ảnh/video có phí, AI phải tuân theo ngân sách và quyền đang có; gói này không tự cung cấp tài khoản dịch vụ tạo video.

## Nhớ gu và nhiều kênh

Nói “nhớ cho kênh kiến thức: dọc, gọn, không nhạc”. AI lưu những lựa chọn đó vào hồ sơ riêng của kênh, chỉ báo đã nhớ khi ghi thành công. Video tiếp theo có thể dùng lại. Nói “riêng video này dùng ngang” chỉ thay đổi lượt này.

Hồ sơ nằm trong `.video-editor/profiles/` ở thư mục làm việc. Chuyển máy hoặc đổi thư mục thì cần mang đúng hồ sơ theo; đây không phải bộ nhớ tự đồng bộ giữa mọi tài khoản ChatGPT. Không dùng hồ sơ của khách hàng khác. Bạn có thể yêu cầu xem, sửa hoặc xóa hồ sơ kênh cụ thể.

## Góp ý dễ sửa nhất

> 00:08–00:11 giữ nhịp nói chậm hơn. Phụ đề nhỏ lại một chút, không đổi nội dung. Bỏ ảnh ở 00:18. Giữ các phần khác.

Chỉ sửa chữ, âm lượng hay gu thì dùng lại nguồn và transcript. Đổi điểm cắt phải cập nhật thời gian phụ đề. AI bảo vệ EDL đã chỉnh tay và giữ tệp nguồn; các bản xuất cần lưu phiên bản khi bạn muốn giữ bản cũ.

## Khi có vấn đề

| Hiện tượng | Cách xử lý |
|---|---|
| AI không đọc được video trên máy | Dùng Work locally với quyền thư mục, hoặc đưa tệp vào môi trường cloud |
| Không tự nhận skill trong chat mới | Kiểm tra plugin đã cài/bật; thử gọi skill trực tiếp hoặc đưa BAT-DAU.md vào chat |
| Thiếu công cụ dựng | AI chạy kiểm tra, cài phần phụ thuộc được phép, hướng dẫn phần còn thiếu |
| Nhận giọng sai | Xác minh ngôn ngữ nguồn, nghe tên riêng; chỉ xử lý lại phần cần thiết |
| Dấu Việt lỗi hoặc chữ che mặt | Kiểm tra font hỗ trợ tiếng Việt và frame thực tế ở đúng tỷ lệ |
| Video mờ | Kiểm tra nguồn gốc; xuất 1080p không khôi phục chi tiết đã mất |
| Render lâu | Dùng lại transcript, xuất một tỷ lệ trước, thử ngắn trước khi xuất dài |
| Máy báo thiếu dung lượng | Giữ nguồn/bản cuối; chỉ dọn file tạm trong đúng dự án sau khi xác định |

## Khả năng hiện tại

Có bộ dựng local, MP4/SRT, ba bộ gu mới, phụ đề và motion tiếng Việt, lưu gu theo kênh, hướng dẫn AI và gói plugin. Chưa có timeline kéo thả hoàn chỉnh. Gói plugin cần được cài bằng cơ chế host hỗ trợ; chưa được kiểm thử đầu-cuối trên một tài khoản ChatGPT Work thật.

Xử lý media bằng engine local khi chạy local; nội dung đưa vào trò chuyện, công cụ tạo/tìm tài nguyên và môi trường cloud vẫn theo chính sách của dịch vụ đó. Không coi mọi chế độ là “không dữ liệu nào rời máy”.

Tài liệu nền tảng: [Work](https://learn.chatgpt.com/docs/get-started-with-work), [Skills](https://learn.chatgpt.com/docs/build-skills), [Plugins](https://learn.chatgpt.com/docs/build-plugins), đối chiếu ngày 20/09/2026.
