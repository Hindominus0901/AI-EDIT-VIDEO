# R17 — Motion explainer — bố cục theo ý

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Bài giải thích cơ chế/quy trình có nội dung đồ họa cụ thể

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Trắng/vàng; headline outline + solid + underline; body ngắn, không nhảy từng từ.

## Ảnh / graphic

Grid tối, glow amber thấp; cửa sổ người nói di chuyển nhường chỗ cho sơ đồ thật.

## Motion

Window dời/thu 17,4–17,8s; graph vẽ 32,27–33s; cutout dissolve 51,9–52,23s.

## Flow

Đặt câu hỏi → chọn layout → dựng một cơ chế → giữ để hiểu → xóa → layout tiếp.

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

Không dùng một card ba lần để giả vờ đa dạng; không bịa số liệu cho biểu đồ.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Bold compact Vietnamese sans captions with white text and moving yellow word emphasis. Headlines combine a small tracked uppercase eyebrow, outlined white lettering, solid yellow key phrase and a yellow underline. Dark labels and micro-copy are subordinate.
- **captionMotion:** The caption line remains anchored while yellow emphasis advances through words. Phrase replacement can fade from dim to full. Around 40.5–40.8s a red line draws left-to-right across a belief label; it then holds, rather than repeatedly crossing the text.
- **footageMotion:** Outer grid/glow stays fixed while the speaker window changes position, size and mask. Full portrait, smaller corner window, split layouts and cutout are distinct states. Window motion is not the same operation as cropping inside the source footage.
- **layoutAndAssets:** Near-black grid with amber glow; rounded video window, fine-border dark cards, yellow icons. Topic card stacks use tilt, scale/opacity and overlap; device cards, channel icons, a line chart, benefits and roadmap are built as different compositions.
- **transitions:** Window shrink/move around 17.4–17.8s; card stack builds around 21 and 22.7s; line chart draws around 32.27–33s; framed speaker blends into cutout around 51.9–52.23s; outline/yellow headline/underline/steps stage around 53.7–55.1s.
- **colorAndLighting:** Dark, restrained amber/yellow system with white lettering and a red correction accent. Fine grid and low-contrast glows add depth without competing with text.
- **visualFlow:** Each explanation gets a coordinated layout state: orient viewer, move the speaker, build one concept, hold, clear or transition. The content diagram is the motion, rather than unrelated embellishments.

## Các sự kiện nguồn

- **0–8.7s** — CTA pill, icons/questions, large one-minute marker and moving yellow caption emphasis.
- **9–17; 17.4–17.8s** — Office cards; speaker window shrinks/moves for the next section.
- **20.80–21.07; 22.53–22.80s** — Product-image card appears above the speaker; social-post card joins offset in front.
- **27–35s** — Personal-brand grouping, channel icons and progressive line chart.
- **40.40–41.50s** — Belief label: no strike at 40.4, begins 40.5, almost across by 40.7, held by 40.8.
- **48–55.1s** — Device cards, cutout transition and staged outline/yellow headline.
- **60–82s** — Three course/content groups built as card/icon/chart scenes.
- **84–98s** — Benefit stack, yellow CTA and final roadmap.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
