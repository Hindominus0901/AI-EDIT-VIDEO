# R16 — Collage — mỗi cụm một luận điểm

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Một ý cần 2–3 hình khác nhau để làm rõ

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Caption sans trắng đậm gọn, neo trên cụm ảnh; Inter 700 gần mẫu đã đối chiếu.

## Ảnh / graphic

Ba thẻ thẳng hàng dưới ngực, gutter 17–18px/720; hình mỗi cụm phải mới và đúng ý.

## Motion

Fade vào 0,22s; stagger 0/0,25/0,54s; giữ; rời lần lượt; pullback nguồn −17,1% độc lập.

## Flow

Người nói → một cụm ảnh cho một ý → giữ → xóa hết → người nói → ý mới.

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

Không tái dùng bộ tranh bằng cách đảo thứ tự; tối đa hai cụm collage mỗi phút mặc định.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Bold white compact phrase captions above the cards. Caption scale is stronger than R14 but quieter than a large hook. Most accents come from illustrations; a later CTA uses lime. No exact font family confirmed.
- **captionMotion:** Captions retain size and screen anchoring while the image underneath pushes or recedes. Three cards arrive sequentially: first partially visible at 6.01s, second 6.21s, third 6.51s, all stable around 6.72s. They hold rather than constantly floating.
- **footageMotion:** Multiple push/pull/reset passages. From 13.013 to 15.015s, background features shrink about 17.1%, with near-zero rotation/center drift. At 11.89s, a closer framing change coincides with the collage finishing its exit.
- **layoutAndAssets:** Mostly two- or three-image collages on the lower torso, mixed monochrome drawings and restrained color. Around 6.715s, visible card bounds are (47,831,191,182), (256,831,189,184), (462,833,210,184) on 720×1280: top around 65% height, gutters about 17–18px. These are visible light-card boxes, not original asset bounds.
- **transitions:** Staggered fades in and out. Group 1 holds through about 11.59s; left clears first around 11.72s, other cards follow, all absent by 11.89s. The simultaneous reframe makes the removal feel like a deliberate new passage.
- **colorAndLighting:** Natural green background, dark shirt and bright restrained illustration cards. No need for a colored background panel around every caption.
- **visualFlow:** Illustration clusters occur in selected passages, separated by clean speaker time and occasional context shots. Clearing a group, reframing, then building a new group creates the rhythm.

## Các sự kiện nguồn

- **0–2; 2.21–4.38s** — Opening pullback followed by short context footage.
- **6.01–11.89s** — First three-card build, hold, staggered exit and framing reset.
- **13.013–15.015s** — Smooth pullback under fixed caption styling; next collage starts around 14.8s.
- **15–17; 21–23; 26–32; 34s** — Further collage groups.
- **43–49.84; 52–54; 57–58; 68–70s** — Selected illustration groups, with clear intervals.
- **76–78; 87–91; 99; 101–105s** — Single centered asset, later collages, lime waterfall CTA, final collage group.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
