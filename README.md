# Video Editor Kit — dành cho người Việt

Bắt đầu với [BAT-DAU.md](BAT-DAU.md) hoặc [trang hướng dẫn](bat-dau.html). Hướng dẫn chi tiết: [HUONG-DAN.md](HUONG-DAN.md).

Người dùng nói nhu cầu bằng tiếng Việt. AI hỏi tối đa ba câu còn thiếu, kiểm tra môi trường, đọc hồ sơ kênh và dựng một bản hoàn chỉnh. Gói plugin điều phối cùng engine trên host có đủ quyền và công cụ; không đồng nghĩa đã cài hay đã kiểm thử trên mọi tài khoản Work.

## Luồng hiện tại

Nguồn → transcript có cache → cắt khoảng im lặng đã xác minh → AI duyệt nội dung và viết kế hoạch → EDL được bảo vệ → Remotion xuất MP4/SRT. Tách mỗi video vào `out/<ma-du-an>` và `public/raw/<ma-du-an>`.

Luồng clean không gọi thêm LLM: AI trong cuộc trò chuyện chọn nội dung, ảnh, chữ và âm thanh một lần. Chỉ `--edit-style legacy` mới dùng các nhà cung cấp CLI cũ. Không cần API key cho luồng clean local.

## Dành cho người triển khai

- Python 3.10+, Node.js 18+, FFmpeg/ffprobe.
- Kiểm tra: `python scripts/doctor.py --json`.
- Chuẩn bị phụ thuộc dự án: `python scripts/setup-runtime.py --install`.
- Windows có `.venv`: dùng `.venv/Scripts/python.exe`; npm dùng `npm.cmd`.
- Kiểm thử: `python -m unittest discover -s tests` và `npm run typecheck`.
- Đóng gói: `python scripts/pack-kit.py`. Chỉ các tệp trong danh sách cho phép được đưa vào gói; không có video cá nhân, bản dựng hay hồ sơ kênh.

Hướng dẫn engine/host plan: [CLEAN-AUTO-FLOW.md](CLEAN-AUTO-FLOW.md). Skill chuẩn: [Dựng video Việt](integrations/video-editor-viet/skills/dung-video-viet/SKILL.md) trong mã nguồn; bản cài local trong `.agents/skills/dung-video-viet`.

## Bộ gu

[Studio, Paper, Mono](asset-library/premium-kit/index.html) có chữ vào nhẹ, nhấn từ khóa, ảnh và đồ họa theo ý. Gu clean hiện có vẫn dùng tiếp nếu người dùng đã chọn. Người mới chưa có hồ sơ được đề xuất Studio. Motion mở rộng: `asset-library/motion-kit`.

## Giới hạn được giữ rõ

Engine không tự hiểu câu chuyện dài chỉ bằng cắt im lặng. AI phải duyệt nội dung và điểm nối. Tỷ lệ 9:16/16:9 dùng chung kế hoạch nhưng cần kiểm tra bố cục riêng. Chưa có timeline kéo thả hoàn chỉnh; kiểm thử Work thực tế cần một phiên Work có quyền và công cụ tương ứng.
