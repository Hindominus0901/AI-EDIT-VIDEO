# Studio · Paper · Mono

Ba bộ gu dùng chung nhịp lời và thời gian của bản dựng. Xem `index.html` hoặc `premium-sets.mp4`.

- **Studio — gọn và chuyên nghiệp:** Inter, nền than, điểm nhấn xanh nhạt; hợp nội dung chuyên môn và talking head.
- **Paper — nhẹ và tinh tế:** Be Vietnam Pro cho phụ đề; Newsreader dùng cho tiêu đề mẫu. Nền trắng ấm, ảnh và khoảng thở.
- **Mono — đen trắng rõ ý:** Inter, tương phản đen trắng, ảnh cặp và chữ mở nhẹ.

Một vùng chữ chính, thường 4–5 từ; một hình hỗ trợ mỗi thời điểm. Chuyển động vào ngắn, có thời gian đứng yên để đọc. Màu nguồn giữ nguyên nếu chưa có lý do điều chỉnh. Không ép nhạc/SFX vào mọi điểm nhấn.

## Áp dụng cho AI

Thêm `"premiumSet":"studio"`, `"paper"` hoặc `"mono"` vào host plan đã duyệt. Không có key thì giữ clean hiện tại. Trong EDL, giá trị nằm ở `style.premiumSet`; kiểu bố cục phải là `focused`.

Xuất từ EDL đã có bằng `python scripts/render-edit.py --out-dir out/ma-du-an --aspect 9:16`. Dùng `both` chỉ khi cần cả hai tỷ lệ. Không chạy STT lại để đổi gu. Nhạc phải đo trên file thật; không sao chép một hệ số âm lượng cho mọi bài.

Token: `src/premium-kit/sets.json`. Chữ vào: silk-rise, quiet-reveal, soft-focus. Ảnh: photo-mat, photo-diptych, photo-detail. Nguồn tài nguyên và giấy phép: [TAI-NGUYEN.md](../TAI-NGUYEN.md).
