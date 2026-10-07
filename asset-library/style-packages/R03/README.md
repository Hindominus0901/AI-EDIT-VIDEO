# R03 — Bài giảng — từng chương

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Nội dung thực sự có các bước hoặc chương

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Caption trắng đậm; tiêu đề chương hồng trên đen; dòng quan trọng lớn hơn.

## Ảnh / graphic

Một sơ đồ đang học; bước hiện tại sáng, bước khác lùi; cảnh minh chứng xen kẽ.

## Motion

Nguồn push khoảng +21,3% trong 3s; chữ tách lớp; hàng sơ đồ hiện theo lời.

## Flow

Mở vấn đề → bước → giải thích → ví dụ → bước tiếp → tổng kết.

## Cắt cảnh

Cắt theo ý, giữ phủ định/điều kiện/hơi thở. Nghe điểm nối trước khi gọi là tự nhiên.

## Màu / ánh sáng

Giữ đặc tính nguồn, chỉnh exposure/WB theo shot; không bịa LUT gốc từ MP4.

## Nhạc / SFX

Chưa định danh nhạc/SFX gốc. Chọn tài nguyên có giấy phép, nhạc dưới giọng, SFX theo điểm có nghĩa; đo mức âm và nghe mix.

## 9:16

Lấy geometry từ ref; chừa vùng mặt/miệng/tay và UI nền tảng. Cận mặt cần dịch hoặc giảm nhóm hình, không ép khung mẫu.

## 16:9

Bản chuyển thể 16:9: người nói và vùng nội dung chia ngang, caption theo vùng đọc; không kéo giãn bố cục dọc. Chưa có ref landscape đối chiếu.

## Không làm

Không tự chia chương vô nghĩa; không đặt mọi sơ đồ nhỏ cạnh mặt.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Bold Vietnamese sans serif over footage with soft black shadow; black chapter cards use pink headings and explanatory text. Emphasis is created by line size, not constant colored karaoke. Some small diagram labels are too small to copy literally.
- **captionMotion:** At 0.9–1.1s the first line resolves; a larger second line appears faintly around 1.6s and is bright by 1.8–1.9s. Text holds at the neck/chest while the source image enlarges. No obvious bounce or word travel in this sampled phrase.
- **footageMotion:** A centered push increases background image scale about 21.3% from 0 to 3s, with almost zero rotation/center drift. Repeated wider resets separate passages; it is not one uninterrupted zoom across the entire video.
- **layoutAndAssets:** Talking head, short contextual footage, isolated portrait on black, black/pink chapter cards, and a progressively populated business diagram. The current step brightens while other information remains subordinate.
- **transitions:** Direct cuts between speaker, coverage and chapter plates. Caption phrases stage in opacity; explanatory rows build over time. Diagram motion is distinct from source framing.
- **colorAndLighting:** Daylight greens and white clothing; selected B-roll is deliberately darkened under white type. Black/pink graphic mode marks sections. Exact LUT remains unknown.
- **visualFlow:** Four chapter markers create macro structure. The edit returns to the speaker after examples and uses a short text-only pause for a question or key message.

## Các sự kiện nguồn

- **0–3.30s** — Centered image push with independent two-stage caption emphasis.
- **3.67–8.40s** — Beach then laptop coverage.
- **14.40–17; 21.10–24.30s** — Isolated grayscale portrait, later expert interview.
- **29.90–34.87s** — Step 1 chapter/diagram sequence.
- **39–49; 55–56s** — Working/scale/boxing examples, then pink-on-black question.
- **57–59.93; 74.30–76.73; 83.77–86.60s** — Steps 2, 3 and 4.
- **60–67; 72–74; 79.27–83.77; 92–95s** — Contextual and interview coverage.
- **101.37–105.70; 113.17–116.60s** — Three-line story/process build; text-only key-message moment.
- **120.17–124.90s** — Seminar coverage before the talking-head close.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
