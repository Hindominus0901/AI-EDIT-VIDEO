# Gu dựng — phản hồi ngày 20/09/2026

## Ưu tiên mới ngày 29/09/2026

- Bổ sung trực tiếp: “upgrade toàn tập”, muốn edit như Iman Gadzhi, Alex Hormozi và Dan Martell. Ưu tiên ba hướng này khi chọn cách dựng mới; một hướng chính theo nội dung, không tự gộp cả ba. Demo 1.6 chưa được duyệt; không áp thay đổi hồi tố vào dự án cũ.

- Người dùng phản hồi bộ dựng quá tốn token và bản edit thiếu hồn; yêu cầu nghiên cứu kỹ và học từ video reference.
- Cấu trúc nội dung, nhịp người nói, khoảng nghỉ và hình có ý nghĩa phải dẫn quyết định dựng. Không chữa bằng thêm preset, graphic hoặc SFX hàng loạt.
- Nghiên cứu ref một lần, lưu bằng chứng và bài học theo điều kiện áp dụng; mỗi dự án chỉ đọc phần cần dùng. Sửa nhỏ không phân tích lại cả clip.
- Quy trình tại skill `references/hoc-tu-reference.md`; sổ nghiên cứu `asset-library/reference-learning/RESEARCH.md`. Đây là hướng làm đã được yêu cầu, chưa phải một bản video mới được duyệt.

Yêu cầu của người dùng: clean, giản dị, chuyên nghiệp; đa dạng hình, chữ, motion và âm thanh nhưng không rối.

Gu hiện tại: người dùng đã duyệt hướng V7. Bản V4 editorial trước đó bị đánh giá rối mắt, không lấy làm mặc định.

Quy tắc áp dụng cho lần dựng tiếp theo:
- Người nói và ý đang nói là trọng tâm.
- Một vùng chữ chính mỗi thời điểm; headline dùng ngắn ở mở đầu hoặc thay phụ đề khi phù hợp, không chồng headline + phụ đề + chữ giải thích.
- Một hình minh họa chính tại một thời điểm. Đa dạng theo thời gian, không dồn nhiều lớp cùng lúc.
- Không mặc định dùng nhãn chương, footer, số mục, đường kẻ, giấy texture hay bảng thông tin.
- Font tiếng Việt; một họ sans cho phụ đề. Chỉ thêm họ thứ hai nếu thực sự cần phân cấp.
- Hiệu ứng âm thanh thưa và nhẹ. Không gắn tiếng vào mọi lần đổi chữ/đổi hình.
- Nhịp nói tự nhiên và chất lượng nguồn vẫn phải được giữ.

V5 là bản thử đơn giản hóa để phản hồi đúng nhận xét này, chưa được người dùng duyệt. Nguồn 1280x720 được crop giữa thành 960x720 và hiển thị 960x720: giữ 75% chiều ngang, không upscale. Chỉ xuất 9:16 ở lần sửa này.

## Bổ sung: phụ đề ngắn và có điểm nhấn

- Người dùng yêu cầu chữ có hiệu ứng vào, không chỉ bật hiện tĩnh.
- Mỗi cụm khoảng 4–5 từ cách nhau bằng dấu cách; có thể 3 từ để không phá ý. Không để cả câu dài nằm nhiều giây.
- Căn cụm theo ý/lời nói. Khi dịch từ ngôn ngữ khác, không giả định thời gian từng từ tiếng Việt là timestamp STT.
- Một chuyển động vào thống nhất: trượt lên nhẹ + scale settle khoảng 0.3 giây. Giữ cụm ổn định sau khi vào để đọc.
- Highlight chọn lọc một từ/cụm quan trọng; phần còn lại màu trắng. Chỉ các câu chốt cần tăng cỡ chữ và gạch chân.
- V6 minh họa hướng này với Inter; chưa được người dùng duyệt.

## Nhiều lựa chọn chuyển động, ngày 20/09/2026

- Người dùng yêu cầu thêm chữ xuất hiện, hiệu ứng, graphic và asset. Bộ mới ở `src/motion-kit`; xem `asset-library/motion-kit/index.html` hoặc MP4 cùng thư mục.
- "Một chuyển động vào thống nhất" là kiểu chủ đạo cho phần lớn caption, không cấm đổi kiểu ở hook, đổi ý và câu chốt. Không random một kiểu mới mỗi cụm.
- Có 8 kiểu chữ, 4 cách nhấn từ, 7 graphic/ảnh và 8 vector. Đa dạng lựa chọn không đồng nghĩa tăng mật độ.
- V7 có phụ đề 3–5 từ, 4 điểm graphic riêng, 3 SFX nhẹ; đã được người dùng duyệt ở lượt tiếp theo.

## Đã duyệt V7

Người dùng phản hồi “oke đấy, triển tiếp đi”. Dùng hướng V7 làm mặc định clean cho lượt mới: Inter tiếng Việt, caption 3–5 từ, màu kem nhấn chọn lọc, một graphic hỗ trợ, motion vào rồi giữ ổn định. Bộ preset được duyệt; không hiểu là cần chèn đủ mọi loại vào mỗi video.

Luồng clean tự gán motion theo vai trò câu và dùng kế hoạch host khi có. Từ điển local chỉ là fallback có giới hạn, không thay cho xem nội dung/nghe nhịp dựng. Giữ nguyên bản V7 đã duyệt trong thư mục riêng.

## Premium request

The user requested "more premium and professional and clean editing set" after approving the V8 direction. The new opt-in library contains Studio, Paper and Mono. Studio is the proposed talking-head treatment, not yet user-approved. Keep the existing clean baseline available. Use restrained entrances, consistent type size, selective accents and aligned image layouts; do not interpret premium as more layers or more sound effects.

## Phản hồi 23/09/2026 — bản SnapVid

- Màu kem highlight của bản đầu bị đánh giá quá nhạt. Với nền sáng/áo trắng cần màu nhấn đậm và tách bạch hơn; không dùng kem nhạt làm mặc định trong trường hợp này.
- Chuyển động chữ bản đầu chưa mượt. Giữ kích thước glyph ổn định, ưu tiên easing giảm tốc rồi đứng yên; tránh co giãn và blur lặp lại ở mọi cụm.
- Người dùng thấy dựng còn đơn giản. Cần thêm các điểm đồ họa có ý nghĩa theo lời nói và thay đổi bố cục ở ý chính, vẫn giữ khoảng nghỉ và một minh họa trọng tâm.
- V2 đang thử vàng #FFD43B, chuyển động theo khung hình và minh họa sách/cơ chế ghi nhớ/nhịp giọng. Đây là phương án đang thử, chưa coi là người dùng đã duyệt.

## Sửa lỗi chớp phụ đề — 23/09/2026

- Người dùng tiếp tục báo V2 bị giật/chớp. Kiểm tra từng frame đã xác nhận 24 khung mất chữ ngay trong một cụm, do đoạn animation bị làm tròn về thời lượng 0 ở đơn vị centisecond của ASS. Kiểm tra contact sheet cách quãng trước đó không đủ để phát hiện.
- Mỗi dòng caption phải là một event liên tục khi có thể. Nếu lấy mẫu motion theo frame, start/end phải dùng cùng hệ thời gian và không tạo đoạn trống khi chuyển sang hold.
- Caption lời nói liên tiếp giữ opacity/cỡ chữ/vị trí ổn định. Chỉ thêm resolve ở các ý chính hoặc sau khoảng nghỉ; không làm mờ rồi sáng lại ở mọi cụm.
- Kiểm tra caption trên toàn bộ khung hình bằng `scripts/audit-snapvid-captions.py --revision v3 --require-clean`, rồi xem các khung liền nhau trên MP4 thật. Không coi decode thành công hoặc vài ảnh preview là đủ để xác nhận hết chớp.
- V3 là bản sửa đang thử; chưa ghi nhận người dùng duyệt.

## Dựng toàn bộ hình và âm thanh — 23/09/2026

- Người dùng nhắc rõ: edit không chỉ là phụ đề. Mỗi lượt dựng phải xét cấu trúc nội dung, điểm cắt/nối, nhịp hình, bố cục/crop, ảnh và graphic, màu/ánh sáng, nhạc và SFX; chọn những phần có ích cho chính video đó.
- Sau khi sửa lỗi caption, cần hoàn thiện phần hình/âm thanh, không coi thêm highlight là đủ. Giữ những đoạn người nói tự nhiên và khoảng nghỉ thị giác; không tăng mật độ hiệu ứng để chứng minh có edit.
- Ảnh/collage có thể xuất hiện trực tiếp trong khung hình theo từng ý, khung người nói thay đổi mượt và không phóng vượt độ phân giải gốc. Nhạc nền thấp dưới giọng nói, SFX thưa ở điểm chuyển ý/hình.
- Bản SnapVid V4 bổ sung ảnh đọc/viết, collage tuần tự, bố cục giải thích cơ chế, chuyển khung người nói, nâng sáng nhẹ và phối nhạc/SFX. Giữ trọn lời nói vì lần này không có yêu cầu cắt ngắn. Đây là bản đang gửi xem, chưa được người dùng duyệt; không nhầm với V4 editorial cũ ở dự án khác đã bị chê rối.

## V4 bị chê “AI quá”, chưa wow — 23/09/2026

- Người dùng không duyệt SnapVid V4: thêm collage/ảnh/SFX vẫn chưa tạo cảm giác có người biên tập lựa chọn kỹ. Không xem số lượng lớp hoặc số đoạn graphic là thước đo chất lượng.
- Tránh lặp hai ảnh minh họa stock và cùng một chuyển động thu nhỏ người nói. Chọn hình có bằng chứng trong nguồn; motion phải diễn đạt đúng ý, có tương phản về tốc độ và độ mạnh giữa các khoảnh khắc.
- V5 thử rút đoạn kể vòng về thứ hạng cuộc thi, dùng hình nguồn, trang luyện đọc được thiết kế riêng, payoff đọc sách TO, chữ gấp so với chữ nhẹ nhàng. Không dùng hai ảnh AI của V4. Chưa được người dùng duyệt, không tự chuyển thành preset mặc định.

## Dựng theo ba mẫu Matt Gray — 23/09/2026

- Người dùng yêu cầu đúp cách dựng Matt Gray và xác nhận cả ba mẫu: áo đen/nền cây xanh với ba ảnh minh họa, so sánh đỏ–xanh trên nền trắng và khung tròn, headline serif trên hai khối trắng của mẫu “I'm 35”. Đây là chỉ dẫn cụ thể cho SnapVid, ưu tiên hơn phương án tự sáng tạo ở V4/V5.
- Mẫu collage có MP4 R16: đo khoảng cách, nhịp fade vào lệch nhau 0,25/0,54 giây, thẻ ảnh thẳng hàng và máy quay lùi độc lập với phụ đề. Hai mẫu còn lại hiện chỉ có screenshot; không coi chuyển động tự dựng là chuyển động đã đo từ video gốc.
- Phụ đề trắng, ngắn, có dấu Việt; không đổi mọi cụm sang vàng hoặc làm chữ nhấp nháy. Inter 700 là font khớp gần nhất trong các font đã đối chiếu, chưa xác nhận tên font gốc.
- V6 dùng minh họa nét mực mới theo nội dung đọc/viết/nói, bố cục so sánh và headline đã xác nhận. Bản xuất V6 vẫn đang chờ người dùng đánh giá; không tự coi là preset đã duyệt.

## V6 bị từ chối vì lặp ảnh — chuyển sang style packages

- Người dùng báo ảnh lặp đi lặp lại, yêu cầu dissect bộ ref và chuyển thành các editing style packages để làm theo form. Không tiếp tục render biến thể V6 hoặc coi V6 là gu được duyệt.
- Mỗi ref giữ ngôn ngữ riêng; chọn một package chính theo nội dung, không gộp mọi mẫu vào một clip. Thư viện local: `asset-library/style-packages/`.
- Lập beat sheet trước khi chọn hình. Một ảnh/crop chỉ một lần mặc định, không đảo thứ tự bộ tranh để giả thành cảnh mới. Callback phải có lý do cùng ý và khoảng cách rõ.
- Chặn sai bằng `scripts/style_packages.py check`: ảnh trùng pixel dù đổi tên, ảnh lặp, collage quá dày, thời gian/độ dài caption sai và layout ngoài gói. Kiểm tra này không thay thế đánh giá nội dung hoặc gu.
- 21 gói phân tích/form là sản phẩm thư viện, không phải 21 renderer đã hoàn thiện hoặc đã được người dùng duyệt. Motion chỉ suy từ screenshot phải ghi là đề xuất.
