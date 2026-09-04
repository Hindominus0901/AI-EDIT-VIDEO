# Video Editor Kit — Bộ dựng video AI chạy trên máy của bạn

## Bộ Kit này là gì?

Đây là một "editor AI" hoàn chỉnh chạy ngay trên máy tính của bạn, điều khiển
bằng cách **nói chuyện với Claude**. Bạn đưa video thô, mô tả gu mình thích,
và nhận về video đã dựng hoàn chỉnh: cắt gọn, caption theo lời nói, đồ họa
nhấn ý, nhạc nền. Không cần biết dùng Premiere hay CapCut, không cần API key,
video của bạn **không bị tải lên mạng** (mọi thứ xử lý trên máy).

### Làm được 2 loại video

| Loại | Dành cho | Kit tự làm gì |
|---|---|---|
| **Video người nói** (talking-head) | Bạn ngồi nói trước máy quay: chia sẻ kiến thức, bán hàng, kể chuyện | Cắt khoảng lặng và từ thừa, chèn caption karaoke theo từng lời, thêm đồ họa nhấn đúng ý đang nói (con số, so sánh, lộ trình...), zoom nhấn nhá |
| **Video b-roll + hook** | Cảnh quay đẹp (biển, quán, sản phẩm...) cần chèn chữ thu hút | Tiêu đề lớn trên nền dải đen, dòng chữ viết tay đồng cảm, lời kêu gọi hành động, nhạc nền tự lặp và fade mượt |

### Điểm khác biệt

- **Nói chuyện tự nhiên**: "sửa chữ ở giây 20", "bớt đồ họa đi", "đổi màu ấm hơn" — kit hiểu và chỉ sửa đúng chỗ đó.
- **Có gu**: 7 phong cách dựng sẵn (bán hàng rực rỡ, tối giản chuyên gia, nữ tính nhẹ nhàng...) — hoặc bạn tự mô tả gu bằng lời, kit tự hiểu.
- **Càng dùng càng hiểu bạn**: mỗi lần bạn nói "keep it", kit ghi nhớ gu của bạn và lần sau hỏi ít hơn.
- **Tiếng Việt chuẩn**: nhận giọng nói tiếng Việt, font chữ hiển thị dấu đẹp.

## Máy cần có gì?

- Windows 10/11 (macOS/Linux cũng chạy được)
- [Node.js 18+](https://nodejs.org) và [Python 3.10+](https://python.org)
- ffmpeg (nếu thiếu, kit sẽ chỉ cách cài hoặc cài giúp bạn)
- [Claude Code](https://claude.ai/code) (gói Claude có Claude Code)
- Khoảng 3GB trống (lần đầu kit tự tải mô hình nhận giọng nói ~460MB)

## Cài đặt (một lần duy nhất, ~10 phút)

1. Giải nén file zip ra chỗ tùy thích, ví dụ `C:\video-editor-kit`
2. Mở folder đó, gõ vào thanh địa chỉ chữ `cmd` rồi Enter (mở terminal tại đây)
3. Chạy lần lượt 2 lệnh:
   ```
   npm install
   pip install -r requirements.txt
   ```
4. Gõ `claude` để mở Claude Code ngay trong folder này
5. Gõ `/biz-help` — kit tự kiểm tra máy, thiếu gì sẽ chỉ cách sửa (hoặc sửa giúp), xong hiện menu

> Từ lần sau chỉ cần: mở folder → `cmd` → `claude` → làm việc.

## Cách dùng

### Tạo video người nói

```
/biz-edit-video C:\Videos\clip-cua-toi.mp4 tối giản trắng đen
```

- Dán đường dẫn video (mẹo: chuột phải vào file → "Copy as path" → dán)
- Tả gu ngay trong lệnh nếu muốn: "tối giản", "rực rỡ bán hàng", "sang trọng vàng đen"... — không tả thì kit hỏi 1 câu với các lựa chọn dễ hiểu
- Không nhớ video nằm đâu? Cứ nói **"tìm video tôi quay hôm qua"** — kit quét máy, đưa danh sách, hiện khung hình để bạn xác nhận
- Kit báo trước: **chờ khoảng 7-12 phút**, xong tự mở video

### Tạo video b-roll + hook

```
/biz-broll-video C:\Videos\canh-bien.mp4 chủ đề: 3 thói quen buổi sáng, vibe nữ nhẹ nhàng
```

- Chỉ cần đưa chủ đề — kit soạn sẵn **3 phương án chữ hoàn chỉnh** cho bạn chọn
- Kit hỏi file nhạc nền (mp3); chưa có thì render không nhạc trước
- Nhanh hơn nhiều: **chờ khoảng 1-3 phút**

### Sau khi có video: chỉnh bằng lời nói

Kit luôn kết thúc bằng menu. Bạn chỉ cần:

- **Muốn sửa**: nói tự nhiên — "sửa chữ ở giây 20", "nhiều đồ họa quá, bớt đi", "đổi nhạc", "hạ tiêu đề xuống thấp hơn". Mỗi lần sửa chờ ~5-7 phút (b-roll ~1-2 phút).
- **Muốn soi kỹ trước khi đăng**: gõ `/biz-review-video` — hội đồng ảo (giám đốc nghệ thuật + editor + khán giả) xem và góp ý, kèm đề nghị sửa luôn.
- **Ưng rồi**: nói **"keep it"** — kit lưu video thành file riêng và ghi nhớ gu của bạn.

### Video nằm ở đâu?

- Video vừa dựng: `out\final.mp4` (kit tự mở cho bạn xem)
- Khi nói "keep it": lưu thêm bản tên riêng trong `out\`
- Làm video mới: bản cũ tự cất vào `out\archive\` — **không bao giờ mất**

## Bảng lệnh (chỉ có 4)

| Lệnh | Việc |
|---|---|
| `/biz-help` | Kiểm tra máy + xem menu (gõ đầu tiên) |
| `/biz-edit-video` | Dựng video người nói |
| `/biz-broll-video` | Dựng video cảnh quay + chữ hook + nhạc |
| `/biz-review-video` | Hội đồng chuyên môn review video vừa dựng |

## Câu hỏi thường gặp

**Video đầu tiên sao lâu thế / máy như bị treo?**
Lần đầu kit tải mô hình nhận giọng nói (~460MB) trong im lặng. Máy không treo, đợi vài phút là chạy tiếp. Chỉ lần đầu.

**Caption sai chính tả vài chỗ?**
Nhận giọng tiếng Việt đôi khi nhầm dấu. Cứ nói "sửa chữ ở giây X thành ..." — kit sửa và render lại phần đó.

**Nhạc dài hơn video thì sao?**
Kit tự cắt đúng độ dài video kèm fade nhỏ dần ở cuối. Nhạc ngắn hơn thì tự lặp. Muốn vào thẳng đoạn hay của bài: nói "bắt đầu nhạc từ giây 15".

**Video của tôi có bị gửi đi đâu không?**
Không. Nhận giọng nói, dựng, render đều chạy trên máy bạn.

**Tôi lỡ tay muốn làm lại từ đầu?**
Nói "làm lại từ đầu" — kit sẽ hỏi xác nhận trước (vì các chỉnh sửa tay sẽ mất) rồi mới chạy lại.
