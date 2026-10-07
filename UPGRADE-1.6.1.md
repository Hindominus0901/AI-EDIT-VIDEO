# Creator edit 1.6.1 — sửa bản thử nhạt

Ngày 29/09/2026. Bản 1.6.0 có 3 preview 19 giây dùng layout chung, nhạc quá nhỏ và không có chuỗi hậu kỳ giọng/LUT. Người dùng đánh giá chưa đạt. Bản này thêm công cụ và một phép thử mới trên nguồn thật; chưa coi là bản sao hay đã được người dùng duyệt.

## Thay đổi chạy được

- Hai scene hình động theo nghĩa nguồn: `content-flood` làm hiện mật độ bài đăng; `salt-ocean` cho hạt muối rơi vào biển. Cả hai là đồ họa giải thích, không phải stock B-roll hay bằng chứng số liệu.
- Camera của scene chia khung dùng crop có chủ ý để tránh người nói bé giữa hai dải đen. Phụ đề scene đặt trên vùng video; phụ đề toàn khung lớn, đậm, có bóng và nhấn từ chọn lọc.
- `scripts/creator-finishing.py grade`: tạo bản dẫn xuất bằng LUT 3D warm-neutral-17, giữ nguyên camera original. LUT nhẹ này là look do kit tạo, không phải LUT của Iman/Alex/Dan. Chỉ dùng khi nguồn hưởng lợi; phải xem da/exposure thật.
- `scripts/creator-finishing.py mix`: highpass + compressor + loudnorm trên giọng, nhạc CC0 duck theo tín hiệu giọng thật, fade đầu/cuối, nhận SFX thưa từ video Remotion, xuất AAC. Đo loudness/true peak bản cuối; nếu quá nhỏ hoặc méo thì sửa filter.
- Nhạc, SFX, LUT chạy offline. Không thêm lượt LLM/STT khi sửa một clip đã có SRT.

## Phép thử thực tế

`out/creator-rebuild-v2/` chứa 37,1 giây từ source của dự án `new-video-1790145339792`, đủ cảnh báo → ẩn dụ → đáp án “niềm tin”. Có 29 caption, 8 scene, 3 cue âm thưa. `build.py` là beat sheet có thể tái tạo trong workspace nhưng không đóng gói vì tên/đường dẫn nguồn riêng của người dùng. Kế hoạch, EDL, SRT và file cuối được lưu cùng thư mục. Đọc [soi lại ref](asset-library/reference-learning/CREATOR-R01-REVIEW-20260929.md) để thấy bằng chứng và giới hạn.

QA kỹ thuật trên bản thử: 1080×1920, 30 fps, 37,1s; giải mã toàn bộ video/audio không lỗi; khoảng −16,12 LUFS và −1,91 dBTP; 46 unit test và TypeScript pass. Đã xem contact sheet tại các beat chính, chưa nghe bản mix bằng tai/loa. Các chỉ số không thay thế đánh giá thẩm mỹ và phản hồi của người dùng.

## Dùng cho video khác

Chọn một creator direction chính theo **luận điểm của nguồn**. Không nhét layout `content-flood` vào clip không nói về mật độ nội dung, không dùng `salt-ocean` nếu không có phép ví von tương ứng. Viết host plan, tạo EDL và SRT như 1.6; khi cần hoàn thiện audio/màu:

```text
python scripts/creator-finishing.py grade --source public/raw/project/source.mp4 --out public/raw/project/graded.mp4 --lut asset-library/luts/warm-neutral-17.cube --seconds 37.1
npx remotion render Reel out/project/picture.mp4 --props=out/project/props.json
python scripts/creator-finishing.py mix --render out/project/picture.mp4 --voice public/raw/project/source.mp4 --music public/music/cc0/chills.mp3 --out out/project/final.mp4 --seconds 37.1
```

EDL phải chỉ vào `graded.mp4` với source volume 0 để tránh giọng đôi; SFX nằm trong bản Remotion và được trộn ở bước cuối. Đặt thời lượng thật của clip, không sao chép `37.1`. Công cụ không tự chọn nhạc hay tự xác nhận gu bằng phép đo. Nếu chưa nghe bản cuối qua loa/tai nghe, ghi rõ review nghe còn thiếu.
