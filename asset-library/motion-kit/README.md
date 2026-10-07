# Motion Kit tiếng Việt

Mở `index.html` để chọn nhóm và xem mẫu, hoặc xem trực tiếp `motion-catalog.mp4` (40 giây, không tiếng). Bộ mẫu dùng chính component xuất video. Các nút HTML chọn đoạn trong MP4, chưa phải timeline kéo thả.

## Bộ mới

- 8 kiểu chữ vào: rise, mask-up, soft-pop, word-rise, slide-left, blur-in, wipe, tracking.
- 4 cách nhấn từ: color, underline, marker, ring. Có tùy chọn tăng nhẹ cỡ từ quan trọng.
- 7 graphic: photo-window, photo-circle, photo-collage (hai ảnh), line-arrow, focus-ring, steps, icon.
- 8 vector gốc: target, proof, chat, idea, growth, time, compass, spark. SVG nằm trong `public/graphics/motion-kit`; bản vẽ nét động dùng chung dữ liệu `src/motion-kit/assets.json`.
- Danh mục `manifest.json` được tạo từ catalog của renderer.

## Dùng trong FocusedPreview

Thêm các trường này vào props có clip, durationSec, vertical, beats và music:

```json
{
  "captionMotion": "library", "defaultEntry": "rise",
  "captions": [{
    "start": 1, "end": 2.5, "text": "Bắt đầu từ ngách nhỏ",
    "entry": "mask-up", "mark": "underline",
    "emphasis": {"text": "ngách nhỏ", "style": "strong"}
  }],
  "motionGraphics": [{"start": 1, "end": 3, "kind": "icon", "asset": "target"}],
  "soundEffects": true,
  "sounds": [{"sec": 1.08, "src": "sfx/kenney/tick_001.ogg", "gain": 0.04}]
}
```

Media tương đối với `public/`. `motionGraphics` thay vùng ảnh legacy; renderer chỉ lấy một graphic đang hoạt động. `vertical: false` cho 16:9. `soundEffects: false` tắt SFX. Không tự gắn SFX vào caption.

## Dùng trong EDL của Reel

`captions[].motion` nhận `entry`, `keyword`, `mark`, `strong`. `graphics[]` nhận `type: "clean-motion"`, `motion: {kind, images?, asset?}`, `anchor: "top" | "center" | "bottom"`. EDL dùng mili giây; FocusedPreview dùng giây. Không ghi đè EDL của người dùng khi thử mẫu.

Graphic EDL trong layout standard dùng khung 34% chiều ngang, 17% chiều cao. Chọn anchor theo footage, tránh mặt/chữ và không xếp nhiều graphic cùng lúc. Layout focused có vùng riêng ngoài mặt và caption. Pipeline hiện mặc định clean, tự gán preset theo role từ host plan hoặc fallback local có giới hạn; xem `CLEAN-AUTO-FLOW.md` ở root. Các kiểu mở rộng vẫn có thể chọn trực tiếp trong EDL.

## Quy tắc chọn

- Một kiểu vào nhẹ cho phần lớn phụ đề; đổi kiểu ở mở bài, đổi ý hoặc câu chốt, không bốc ngẫu nhiên.
- 4–5 từ/cụm; 3 từ khi giữ ý tốt hơn. Chữ vào tối đa 35% thời lượng cue, rồi giữ yên cho dễ đọc.
- `word-rise` lệch thời gian vào theo cụm tối đa 90 ms; đây không phải đồng bộ từ dịch với giọng gốc.
- Một vùng chữ và tối đa một graphic. Không ring + marker + underline cùng từ. Collage hai ảnh chỉ khi cần đối chiếu.
- Inter subset Vietnamese trong FocusedPreview và catalog; Be Vietnam Pro trong Reel opt-in. Có khoảng đệm cho dấu tiếng Việt.
- SFX thưa và nhẹ; nguồn Kenney CC0 đi kèm có giấy phép trong thư viện.

## Tạo lại bộ mẫu

Chạy `npm run motion:catalog` trong engine để xuất lại catalog. Chỉ dựng lại khi cần kiểm tra thay đổi component, không chạy ở mỗi video khách hàng. File preview không phải timeline kéo thả.

SRT tách riêng không chứa màu hoặc hiệu ứng chữ. Nguồn ảnh, nhạc và giấy phép: `asset-library/TAI-NGUYEN.md`. Vector được viết trực tiếp trong dự án.
