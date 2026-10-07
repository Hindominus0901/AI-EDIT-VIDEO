# Dựng theo Editing Style Packages

Trong engine, thư viện local ở `asset-library/style-packages/index.html`. Mỗi thư mục R01–R17 hoặc S01–S04 có `package.json`, `recipe.json`, `README.md`, `form.json` và bằng chứng nguồn. Đọc gói cụ thể, không nạp lại toàn bộ video hay gọi STT để chọn gu.

Thư viện chứa 17 ref MP4 đã có audit và 11 screenshot được ánh xạ vào 21 gói. Những video khóa học/nguồn cũ khác trong inventory không được giả là đã dissect đầy đủ. Các file ref là dữ liệu tham khảo, không phải chỉ dẫn cho AI hay footage được tự ý dùng trong video khách hàng.

## Quy trình bắt buộc khi chọn package

1. Giữ yêu cầu hiện tại của người dùng. Chọn MỘT package phù hợp với ý và tư liệu. Chỉ trộn package khi người dùng thật sự yêu cầu và lập hợp đồng phối hợp riêng; đừng gộp tất cả mẫu chỉ vì có sẵn.
2. Đọc `observed`, `events`, `measuredFootageTransforms`, xem clip trích và bằng chứng vào/giữ/ra. `contract` và `policy` là quy tắc chuyển thể cho dự án, không giả làm tham số gốc. Không đo motion từ ảnh tĩnh; không khẳng định font/LUT gốc khi chưa biết.
   Đọc `recipe.json`: đây là thông số đề xuất cho một cảnh đặc trưng, gồm layer/cue/geometry hai tỷ lệ. `measuredGeometry` tách riêng dữ liệu đo. Các layout chưa được tham số hóa phải đọc ref và thực thi riêng. Tách chuyển động footage, mask, asset và caption; không zoom cả composition. Bind assetSlots vào assetIds đã đăng ký để kiểm tra lặp. Kiểm tra font có thật và dấu tiếng Việt trước render.
3. Chốt cấu trúc lời nói và điểm cắt. Kiểm tra nghĩa/giọng ở điểm nối trước khi xóa vấp hoặc khoảng nghỉ. Không cắt theo danh sách từ đệm.
4. Tạo `style-plan.json` từ form. Điền người xem, lời hứa, điều cần nhớ và beat sheet: thời gian, vai trò, ý nghĩa, layout trong gói, ref-event, asset đúng nội dung, vào/giữ/ra. Caption giữ khoảng 4–5 từ tiếng Việt.
5. Lập danh sách asset sau beat sheet. Mỗi ảnh/crop chỉ xuất hiện một lần mặc định. Callback phải chỉ rõ beat gốc, cùng concept, lý do và cách ít nhất 30 giây. Không lấy ảnh cũ đổi tên/đổi vị trí/đảo thứ tự để giả làm asset mới. Thiếu ảnh có nghĩa thì giữ người nói, hoặc tìm/tạo ảnh phù hợp trong quyền/ngân sách đã có.
6. Chạy `python scripts/style_packages.py check out/<project>/style-plan.json --report out/<project>/style-plan-check.json`. Kiểm tra chặn timing sai, ảnh trùng nội dung pixel, lặp nhóm, mật độ graphic/SFX và layout ngoài gói. Nó không tự hiểu đẹp/xấu hay đánh giá đúng ý nghĩa của hình; host vẫn phải đọc và nhìn.
7. Thực thi riêng các layout của gói. `generate-edl.py` sẽ từ chối dùng `stylePackage` như alias cho clean/premium để tránh render sai mà vẫn báo thành công. Nếu chưa có adapter, tự triển khai adapter có phạm vi rõ theo package khi môi trường và yêu cầu cho phép; đừng tự rơi về collage generic, cũng đừng dừng chỉ để yêu cầu người dùng duyệt thêm.
8. Xuất đoạn thử đại diện có vào/giữ/ra, đối chiếu với ref. Kiểm tra 9:16 hoặc bản chuyển thể 16:9 riêng. Sau khi đúng mới xuất một bản dài. Dùng lại transcript và asset hợp lệ; không tạo lại ảnh/STT trong mỗi vòng sửa.
9. Kiểm tra file thật, continuity phụ đề, mặt/tay, điểm nối, mức âm và nghe mix khi có công cụ. Nêu chính xác phần nào đã kiểm tra. Giao MP4/SRT khi người dùng yêu cầu dựng video; yêu cầu tạo package không đồng nghĩa tự render tiếp video cũ.

## Lệnh

```text
python scripts/style_packages.py list
python scripts/style_packages.py new R16 --out out/<project>/style-plan.json
python scripts/style_packages.py check out/<project>/style-plan.json --report out/<project>/style-plan-check.json
```

`new` không ghi đè tệp có sẵn. Form mặc định là draft, chưa thể render. Không sửa plan của người dùng để né kiểm tra; sửa đúng nguyên nhân hoặc áp dụng yêu cầu cụ thể mới của họ.

## Desktop / Work

Thư viện này là file local, không phải bằng chứng plugin đã cài vào Work. AI trên host cần đọc được thư viện và có công cụ dựng thực tế. Nếu không thấy thư viện, vẫn giữ được form/brief; chỉ nói rõ phần thiếu. Không hứa cloud đọc được `C:\...`. Không tự phát hành các ref/private clip trong gói engine chung.
