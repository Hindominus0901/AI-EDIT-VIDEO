---
name: edit-video-thuan
description: Dựng hoặc sửa một video từ media và brief của lượt hiện tại, không đọc cache nội dung, hồ sơ người dùng, project-context, lịch sử dự án hay thư viện nghiên cứu. Dùng khi người dùng yêu cầu edit thuần, no-cache, làm mới hoàn toàn hoặc ưu tiên giảm token. Không dùng cho onboarding, nghiên cứu reference, ghi nhớ gu hay đóng gói plugin.
---

# Edit video thuần

Chỉ dựng video đang được giao. Dùng media, brief, transcript và reference được người dùng chỉ định trong lượt hiện tại. Không mở các nguồn sau:

- `.cache/`, transcript hoặc ASR của lần chạy trước;
- `.video-editor/profiles/`, memory, lịch sử chat hoặc hồ sơ kênh;
- `project-context.json`, style-package catalog, sổ nghiên cứu reference;
- bản dựng cũ, trừ khi người dùng yêu cầu sửa chính bản đó.

Không gọi model lồng, subagent, web research hoặc quy trình phân tích nhiều vòng. Không tạo package, tài liệu nghiên cứu hay cập nhật hồ sơ. Cache kỹ thuật của runtime như model STT đã cài, npm và codec được phép dùng vì chúng không chứa quyết định nội dung và không tiêu token hội thoại.

## Luồng dựng

1. Xác định media và yêu cầu từ lượt hiện tại. Nếu brief chưa nêu tỷ lệ, giữ tỷ lệ nguồn. Nếu chưa nêu thời lượng, giữ đủ ý thay vì ép vào một mốc cố định.
2. Kiểm tra media bằng `ffprobe`. Tạo thư mục output mới để không đè dự án cũ.
3. Nếu người dùng đã đưa SRT/transcript, dùng đúng file đó. Nếu chưa có, chạy STT local mới từ media; với pipeline chuẩn dùng `scripts/run-pipeline.py --no-cache`. Không đọc hoặc ghi transcript cache.
4. Đọc transcript mới một lần. Viết beat sheet ngắn gồm mở ý, phát triển, điểm nhấn và kết. Với pipeline clean, ưu tiên host plan nhỏ: `{"timebase":"edited-clip","pureEdit":true,"look":"quiet","moments":[...]}`. Không chép toàn transcript hoặc các rule thẩm mỹ vào plan; code tự chia caption và mở rộng visual system.
5. Chọn một look: `quiet` cho chuyên gia/talking head, `editorial` cho kể chuyện/giáo dục, `direct` cho lập luận mạnh. Với talking-head, mặc định giữ footage full-bleed và caption đè trên hình. Caption dùng timestamp từng từ: nói đến đâu từ hiện đến đó, từ đang nói có lift/accent ngắn. Ba giây đầu phải có hook được viết riêng, một camera move và tối đa hai cue âm thanh. Trong thân video, dùng flash/zoom, typography beat hoặc sound cue tại chỗ đổi claim, proof, metaphor hay consequence; không chỉ nhấn trong caption. Khi cần minh hoạ, dùng B-roll chuyển động theo thứ tự: video người dùng cung cấp, stock video có nguồn và quyền sử dụng rõ ràng, rồi video chân thực được tạo riêng. Ảnh có chuyển động Ken Burns chỉ là phương án cuối. Không mặc định dùng vector, line-art hoặc card UI; chỉ dùng UI khi câu nói thật sự nói về giao diện hay sản phẩm. Chọn preset và asset bằng ID ngắn từ `asset-library/editing-library/manifest.json`; không đọc lại reference dài ở mỗi video. Mỗi B-roll phải giải thích đúng câu đang nói; thiếu asset phù hợp thì giữ người nói. Motion vào nhanh theo ease-out, ra nhanh hơn, một điểm nhấn chính tại một thời điểm. Không tạo hiệu ứng chỉ để cảnh trông bận.
6. Xử lý âm thanh trên nguồn hiện tại: lọc rumble nhẹ khi cần, compressor vừa phải, cân loudness, đặt nhạc dưới giọng và duck theo giọng. LUT/color phải dựa vào shot hiện tại; không dùng một LUT chung nếu da hoặc highlight xấu đi.
7. Render một bản hoàn chỉnh. Chạy `scripts/pure-edit-audit.py <out-dir>/edl.json --out <out-dir>/pure-edit-audit.json`, rồi kiểm tra decode, kích thước, thời lượng, caption, khung mặt, loudness và true peak. Sửa lỗi audit trước khi giao. Nếu chỉ xem frame hoặc đo âm, nói đúng phạm vi; không nhận là đã nghe/xem toàn bộ.

Để tiết kiệm token, dùng host plan ngắn bằng preset ID và timestamp; không đọc lại reference hoặc content cache. Chỉ chạy STT lần hai cho từ confidence thấp. Render `--preview-seconds 10` với log quiet trước, sửa trên EDL hiện tại, rồi render full đúng một lần. QA bằng một contact sheet, một lượt decode và một lượt loudness.

Đầu ra tối thiểu: MP4 mở được và SRT nếu video có lời. Báo ngắn phần đã dựng, kiểm tra đã chạy và giới hạn review còn lại.

## Giới hạn token

Mỗi lượt chỉ đọc các file cần cho video hiện tại. Các bài học thiết kế đã được nén vào `src/pure-edit-system.json` và code renderer; không mở lại Uiverse, repo thiết kế, Gumroad, toàn bộ AGENTS, tài liệu nâng cấp, thư viện ref hoặc log usage khi dựng. Sửa nhỏ thì chỉ mở EDL/plan và đoạn media liên quan. “No-cache” ở đây là không đọc cache **nội dung** của bộ dựng; prompt cache do nền tảng Codex quản lý không thể tắt từ skill.
