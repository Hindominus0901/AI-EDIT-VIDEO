# Video Editor Việt 1.5

## Thay đổi có trong renderer

- `editorial-c`: font Manrope Bold + Playfair Display Italic được đóng gói local; không đổi mặc định Studio của người dùng mới. Portrait C phủ khung hình, landscape có bố cục riêng. Điểm nhấn serif chỉ ở cụm mạnh; không đổi font cả câu.
- Phụ đề liên tiếp dùng `hold`, không chạy fade vào/ra lại ở mọi cụm. Khoảng trống <=160ms được lấp bằng giữ cụm trước. Các câu mới và điểm nhấn vẫn có motion.
- Nhánh focused/clean thực thi camera cues từ EDL; quintic easing trở về khung cơ sở ở cuối cue. Chữ/graphic không zoom theo hình. Cue nối nhau không tạo bước nhảy scale.
- B-roll thật có offset nguồn, chuyển mờ ngắn và muted; giọng nguồn vẫn phát bên dưới. Validator chặn cue quá dài so với footage, clip lặp mặc định và graphic chồng B-roll.
- `reviewed_cuts.py` nhận các khoảng nguồn đã được AI biên tập, căn về frame và ánh xạ word timestamps. Chặn cắt giữa từ theo timestamp (dung sai 35ms). Không tự hiểu hoặc xóa vấp theo từ khóa. Mỗi nối có văn bản trước/sau và cờ chưa nghe duyệt.
- Setup kiểm tra thêm Pillow; gói phát hành có font local, công cụ mới và 21 đặc tả style, không kèm media khách hàng.
- `render-edit.py --preview-seconds 8` xuất thử đoạn đầu từ EDL đã có, không chạy lại STT hoặc thay timeline. Xuất lại tự dùng hậu tố -v2, -v3 để giữ MP4 trước đó.

## Host plan dùng được

Đọc thuc-thi.md của skill cho các lệnh tạo EDL/render. Ví dụ các trường bổ sung, thời gian dưới đây chỉ minh họa:

```json
{
  "clip": "raw/du-an/source-cut.mp4",
  "timebase": "edited-clip",
  "premiumSet": "editorial-c",
  "captions": [{"startMs": 0, "endMs": 1600, "text": "Giữ lại điều quan trọng"}],
  "moments": [],
  "camera": [{"startMs": 0, "endMs": 3500, "type": "punch-in", "scale": 1.08}],
  "broll": [{"startMs": 4000, "endMs": 7000, "src": "stock/clip.mp4", "offsetSec": 2, "fadeSec": 0.23, "reason": "Minh họa đúng luận điểm"}]
}
```

Các thời gian ở edited-clip; camera 1–1.15, cửa sổ >=800ms, cues cùng loại không chồng nhau. Host kiểm tra ý nghĩa asset và giấy phép. B-roll src phải là video local trong public/. Đây là B-roll phủ vùng footage; collage video nhiều ô chưa được bổ sung. Không tự lặp footage ngắn.

## Rút gọn lời theo ý

Plan mẫu: `{"status":"reviewed","keep":[{"startMs":0,"endMs":2800,"reason":"Giữ hook và từ phủ định"},{"startMs":5100,"endMs":9000,"reason":"Giữ luận điểm tiếp theo"}]}`. Chỉ dùng thời gian đã đối chiếu nguồn thật.

```text
python scripts/reviewed_cuts.py --source public/raw/du-an/source.mp4 --transcript out/du-an/transcript-source.json --plan out/du-an/keep.json --out-dir out/du-an/cut-v2 --render
```

Yêu cầu transcript gồm durationSec và words[{text,startMs,endMs}], nguồn có video và audio. Thư mục đầu ra phải mới. `source-cut.mp4`, transcript.json và timeline.json chung thời gian; dùng transcript mới tạo caption/graphic. Chép source-cut.mp4 sang public/raw/du-an/ trước khi truyền clip cho renderer. Không đưa timing nguồn cũ vào host plan mới.

Chỉ có word timestamps chưa chứng minh nối lời tự nhiên; nghe các mốc joins trước khi công bố. Không đổi tốc độ nói, không tạo lời mới. Bộ cắt có một lần encode hình; dùng nguồn gốc cho chất lượng tốt nhất.

## Giới hạn

21 gói ref vẫn là đặc tả/form, không phải 21 renderer tự động. Chưa thêm timeline kéo thả, nhận diện ngữ nghĩa vấp tự động hay MCP render server. Font C chạy local; các style cũ vẫn có font Google riêng. Chưa xác minh cài đặt trực tiếp trên mọi tài khoản Work. Các tính năng mới cần được chọn trong plan, không tự làm mọi video thành cùng một gu.
