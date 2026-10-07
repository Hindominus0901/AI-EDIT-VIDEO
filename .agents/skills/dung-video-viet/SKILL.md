---
name: dung-video-viet
description: Dựng hoặc sửa video cho người Việt bằng Video Editor Kit; thiết lập lần đầu, hỏi nhu cầu còn thiếu, cắt lời tự nhiên, phụ đề tiếng Việt, ảnh và đồ họa gọn, xuất MP4 và SRT. Dùng khi người dùng nói dựng video, edit clip, chỉnh phụ đề, nhớ gu hoặc setup bộ dựng. Không dùng cho trò chuyện chung không liên quan video.
---

# Dựng video Việt

Giao tiếp bằng tiếng Việt dễ hiểu, xưng hô theo người dùng. Người dùng chỉ cần nói nhu cầu; không bắt họ học tên preset, JSON, terminal hay lệnh `/biz-...`. Chỉ dẫn cụ thể của họ và lựa chọn trong cuộc trò chuyện ưu tiên hơn mọi mặc định dưới đây.

## Nhận việc

1. Đọc ngữ cảnh hiện có; không hỏi lại tỷ lệ, gu, tệp hay quyền đã được xác nhận. Nếu là sửa bản cũ, mở đúng dự án và sửa đúng phạm vi.
2. Lần đầu: đọc [thiết lập và câu hỏi](references/bat-dau.md). Kiểm tra công cụ/tệp thực sự có trong phiên, rồi hỏi tối đa 3 câu còn thiếu về nội dung/người xem, nơi đăng/thời lượng, gu. Cho phép “bạn tự chọn”. Không cố điền một bảng câu hỏi khi brief đã đủ.
3. Tìm bộ dựng và kiểm tra bằng [quy trình thực thi](references/thuc-thi.md). Không giả định có shell, Python, FFmpeg, quyền đọc ổ C hay Claude CLI. Work trên cloud không tự có tệp ở máy người dùng. Thiếu quyền/tệp: nêu đúng thứ còn thiếu bằng một câu, tiếp tục phần độc lập có thể làm.
4. Đọc hồ sơ đúng kênh nếu có. Lựa chọn lượt này > hồ sơ đã lưu > mặc định. Nói lại phương án ngắn rồi thực hiện; không thêm vòng duyệt chỉ vì đã hỏi vài câu.

## Chuẩn dựng cho người Việt

- Tự nhận ngôn ngữ nguồn từ nội dung; giao tiếp tiếng Việt không có nghĩa video luôn nói tiếng Việt. Không ép STT tiếng Việt lên nguồn tiếng Anh. Chỉ dịch khi người dùng muốn; nếu cần dịch, căn theo cụm lời và không bịa timestamp từng từ đã dịch.
- Sửa tên riêng/thuật ngữ theo thông tin người dùng; giữ từ phủ định, điều kiện, số liệu và giọng nói. Chưa chắc một từ thì đối chiếu âm thanh hoặc hỏi đúng từ đó.
- Mỗi phụ đề thường 4–5 từ, có thể ngắn hơn để trọn ý; đếm từ theo dấu cách, giữ cụm nghĩa như “thương hiệu”, “cá nhân”. Font có dấu đầy đủ. Một vùng chữ chính; nhấn chọn lọc một cụm, để chữ đứng yên đủ lâu sau khi vào.
- Mặc định mới: “Gọn và chuyên nghiệp” (Studio). Các lựa chọn: “Nhẹ và tinh tế” (Paper), “Đen trắng rõ ý” (Mono), “Gu sạch đã dùng” (clean). Giữ gu cũ khi đã có hồ sơ; không đổi mặc định của người đang dùng.
- Người nói là trọng tâm. Một ảnh/đồ họa hỗ trợ tại một thời điểm; đưa trực tiếp vào bố cục khi phù hợp. Không dùng ảnh ngẫu nhiên để đủ số lượng. Đồ họa hết khi ý đó kết thúc.
- Cắt theo ý và nghe điểm nối; chỉ tự rút khoảng im lặng đã xác minh. Vấp, lặp, tiếng đệm là chỗ cần đánh giá, không phải danh sách từ để xóa. Không ép video dài vào 30 giây nếu chưa được yêu cầu.
- Ưu tiên tài nguyên đã đưa, sau đó tài nguyên có giấy phép rõ. “Miễn phí bản quyền” không đồng nghĩa không bao giờ có Content ID. Ghi nguồn và credit nếu cần. Chỉ tạo ảnh/video mới khi phù hợp yêu cầu, công cụ và ngân sách đã cho phép.
- Nhạc dưới giọng, SFX thưa. Kiểm tra mức âm thực tế; không dùng cố định một volume cho mọi bài. Không áp LUT chung cho mọi nguồn hoặc hứa khôi phục chi tiết từ nguồn kém.

## Thực hiện và sửa

Khi người dùng muốn hướng Iman Gadzhi, Alex Hormozi hoặc Dan Martell, đọc [ba hướng creator](references/creator-directions.md) và `UPGRADE-1.6.md`. Đây là renderer theo scene có triển khai; fidelity phải đối chiếu ref, không chỉ chọn màu/font.

Khi nghiên cứu hoặc dựng theo reference, đọc [học cách biên tập từ ref](references/hoc-tu-reference.md). Học quan hệ giữa nội dung, nhịp hình và âm thanh; lưu bài học một lần để dùng lại. Chưa nghe/xem đầy đủ thì ghi rõ phạm vi, không coi đo motion hoặc tạo package là đã hiểu cách dựng.

Engine 1.5 có lựa chọn `editorial-c` (font C local), camera/B-roll theo timeline và công cụ căn lời sau khi chọn đoạn. Đọc `UPGRADE-1.5.md` ở engine khi dùng; đây là khả năng có triển khai, khác với các ref package chỉ có đặc tả. Không đổi gu đã lưu hoặc mặc định Studio chỉ vì có lựa chọn mới.

Khi người dùng có bộ ref hoặc yêu cầu dựng theo style package, đọc [gói dựng từ ref](references/style-packages.md) trước khi chọn hình/motion. Chọn một package chính, lập beat sheet theo nội dung rồi mới lấy asset. Không mặc định lặp một bộ tranh hay trộn các ref thành preset chung. Có package JSON không đồng nghĩa renderer đã thực thi đúng mọi layout.

Dùng [quy trình thực thi](references/thuc-thi.md) cho lệnh, trục thời gian và chỗ lưu. AI hiện tại lập kế hoạch; không gọi thêm LLM/Claude CLI để làm lại việc đã hiểu. Dùng lại transcript và asset, tạo một bản hoàn chỉnh; chỉ xuất cả hai tỷ lệ khi người dùng cần. Khi họ ưu tiên nhanh: giảm bản xuất và vòng thử, không hạ chất lượng tệp cuối một cách âm thầm.

Trước xuất dài, báo đang làm gì và ước lượng theo nguồn/máy, không hứa cứng 5 phút. Sau xuất, kiểm tra file thật, dấu tiếng Việt, vị trí mặt, nhịp vào/ra chữ, điểm cắt và âm lượng. Nếu chỉ kiểm tra frame/đo audio, không nói đã xem/nghe toàn bộ. Khi có công cụ review thì dùng trong phạm vi được phép; không phụ thuộc subagent riêng của Claude.

Giao video mở được, SRT, tỷ lệ và thời lượng. Người dùng có thể nói “bớt hiệu ứng”, “chữ nhỏ lại”, “giữ kiểu này”, “video tiếp theo”. Chỉ nói đã ghi nhớ sau khi ghi hồ sơ thành công; không gửi hồ sơ/tệp cá nhân kèm gói chia sẻ. Không tự đăng video hay mua tài nguyên.

## Phạm vi nền tảng

Đây là skill điều phối bộ dựng, không phải bằng chứng đã cài plugin, có timeline kéo thả, hoặc đã chạy thành công trên mọi tài khoản Work. Đọc [khả năng và cách cài](references/chatgpt-work.md) nếu cần thiết lập host. Nếu chỉ nhận file hướng dẫn trong chat, không nói skill đã được cài tự động.
