# Uiverse curated for video

Ba component MIT từ `uiverse-io/galaxy` được giữ nguyên trong `sources/` để truy nguồn. Renderer dùng bản chuyển thể React/Remotion trong `src/motion-kit/GraphicMotion.tsx`:

- `ui-grid`: nền lưới cho giải thích có cấu trúc;
- `ui-glass`: card kính cho một ý hoặc con số nổi bật;
- `ui-notification`: thông báo cho bằng chứng, kết quả hoặc milestone.

Host plan chỉ truyền ID và nhãn ngắn. Không đọc các file HTML này trong lúc dựng và không quét toàn bộ Galaxy. Giữ tối đa một primary visual tại một thời điểm.
