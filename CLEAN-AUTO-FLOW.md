# Luồng clean đã duyệt

`generate-edl.py` và `run-pipeline.py` mặc định dùng `--edit-style clean`. Chế độ này tạo EDL `style.layout: focused`, đọc được trực tiếp bởi Reel, giữ bố cục và font Inter của V7. `--edit-style legacy` chọn luồng nhiều pass cũ khi cần một style khác.

## Quyết định dựng

1. Cắt và chọn nội dung trước; bảo toàn nhịp nói, câu điều kiện/phủ định. Transcript sau cắt dùng đúng trục thời gian của clip đã cắt.
2. Host xem nội dung, dịch nếu cần và chọn các điểm có ý nghĩa. Kế hoạch không dùng timestamp nguồn gốc sau khi clip đã bị cắt.
3. Chia phụ đề 3–5 từ, tối đa 5. Khi có timestamp từng từ, bộ chia dùng phân hoạch tối ưu, ưu tiên chỗ dừng và tránh tách cụm tiếng Việt quen thuộc. Không tự bịa timestamp từng từ cho bản dịch.
4. Phần lớn caption dùng rise. Hook dùng word-rise; đổi ý dùng mask-up; câu chốt dùng soft-pop. Highlight chỉ khi tìm thấy từ ở đúng caption gần thời điểm chỉ định.
5. Graphic chỉ xuất hiện khi có nội dung/asset phù hợp và đủ khoảng trống. Mặc định kết thúc cùng caption hỗ trợ; host có thể cấp endSec nếu ý kéo qua nhiều caption, vẫn giới hạn 3.2 giây. Khoảng cách bắt đầu graphic ít nhất 6.5 giây. Không có quota tối thiểu.
6. SFX là lựa chọn có chủ ý trong moment, không gắn vào mọi graphic/caption. Nhạc local, giọng gốc giữ âm lượng riêng.
7. Kiểm tra timing/asset/mật độ trước render. Không bắt buộc video dài phải có transition hay phải phủ SFX theo phần trăm.

Host plan được cung cấp một lần; bước chọn preset và render không gọi thêm CLI/LLM. Nếu không có kế hoạch, fallback local dùng từ điển nhỏ, có nhãn rõ trong edit-plan.json. Nó không hiểu toàn bộ câu chuyện như editor và không tự tạo bản dịch.

## Host plan tối thiểu

```json
{
  "clip": "raw/clip-da-cat.mp4",
  "timebase": "edited-clip",
  "captions": [
    {"startMs": 4000, "endMs": 5600, "text": "Tạo bằng chứng thật"}
  ],
  "moments": [
    {"sec": 4, "keyword": "bằng chứng", "role": "proof", "asset": "proof", "sound": true,
     "reason": "Đưa ra bằng chứng cho luận điểm."}
  ],
  "music": {"src": "music/cc0/contemplation.mp3", "volume": 0.035, "loop": true, "fadeOutSec": 1.5}
}
```

Các role: hook, shift, proof, example, emphasis, close. `asset` nhận ID vector của Motion Kit. Có thể thay bằng `images: ["images/a.jpg"]` và `graphic: "photo-window" | "photo-circle" | "photo-collage"`. Collage cần hai ảnh local có liên quan; không tự lấy ảnh ngẫu nhiên khi thiếu. `endSec` chỉ dùng khi graphic hỗ trợ một ý dài hơn caption đầu.

`captions` có thể bỏ qua nếu dùng nguyên ngôn ngữ nguồn. Kế hoạch có cue thời gian phải có timebase như trên; clip không trùng sẽ báo lỗi. Ví dụ ở trên chỉ minh họa schema; dùng timestamp thực tế của clip đã cắt.

## Chạy bằng tài nguyên có sẵn

```powershell
# Đã có transcript.json trong thư mục riêng: chỉ lập EDL, không chạy STT.
python scripts/generate-edl.py --clip raw/clip-da-cat.mp4 --out-dir out/du-an --plan out/du-an/host-plan.json --edit-style clean --aspect 9:16

# Xuất hai tỷ lệ từ đúng một EDL, một bản phụ đề, không lập kế hoạch lại.
python scripts/render-edit.py --out-dir out/du-an --aspect both

# Nguồn mới: STT cache -> cắt khoảng im lặng đã xác minh -> EDL -> hai tỷ lệ.
python scripts/run-pipeline.py raw/du-an/clip.mp4 --out-dir out/du-an --edit-style clean --llm offline --aspect both --render
```

Đầu ra: final-9x16.mp4, final-16x9.mp4, captions.srt. Lệnh render độc lập đọc edl.json đang làm, không edl.generated.json. Không ghi đè EDL khi tạo biến thể tỷ lệ. SRT được tạo lại từ chính bản đang xuất. Máy có `.venv` thì dùng `.venv/Scripts/python.exe`.

## Trạng thái và giới hạn

- Luồng mới chạy local trong dự án này; các đường dẫn media trong EDL là tương đối với public/.
- Nội dung video và vị trí mặt vẫn cần review. Khung nguồn ngang dùng bố cục V7; nguồn dọc/nguồn nhỏ được fit để tránh upscale. Các tỷ lệ đầu ra được chọn độc lập với kích thước nguồn.
- Focused layout dành cho caption và clean-motion; validator báo khi EDL chứa track mà bố cục này chưa hỗ trợ.
- Đây là nâng cấp luồng dựng/render. Timeline kéo thả và chạy thực tế trên ChatGPT Work chưa được kiểm chứng/hoàn thành bởi lượt này.

## Kiểm tra

`python -m unittest discover -s tests`, `npm run typecheck`, `npm run goldens -- --motion`. Với video cuối: lint EDL, xem frame ở điểm nhấn/chuyển ý, giải mã toàn bộ MP4 và đo âm thanh. Tests mới kiểm tra bảo toàn từ/phủ định, giới hạn 5 từ, trục thời gian, không match từ khóa bên trong từ khác, kết thúc graphic đúng ý và giữ bản EDL đã sửa tay.

## Optional premium sets

For the more refined visual treatment, add `"premiumSet":"studio"`, `"paper"`, or `"mono"` at the top level of a reviewed host plan. This maps to `style.premiumSet` in the focused EDL. Timing and source audio stay unchanged. Omitting the key retains the approved V7/V8 baseline. Library and exact rules: `asset-library/premium-kit/README.md`; preview: `asset-library/premium-kit/premium-sets.mp4`.
