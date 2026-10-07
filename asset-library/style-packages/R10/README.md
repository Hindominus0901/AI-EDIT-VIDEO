# R10 — Lifestyle — hard cut có nhịp

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Bộ footage hoạt động có sẵn, kể bằng hình

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Caption trắng ngắn ở cùng một điểm giữa khung, thay nội dung theo cảnh.

## Ảnh / graphic

Full-frame footage thật; mỗi cảnh có hành động khác nhau; không cần collage.

## Motion

Hard cut đầu ở frame 47→48 (~2s); chưa có bằng chứng speed ramp hoặc đảo video.

## Flow

Hành động mở dài hơn → chuỗi cảnh ngắn → cảnh thoáng để kết.

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

Không tự suy rằng cảnh lùi là phát ngược; không ép cắt theo beat chưa nghe.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Small-to-medium bold white sans centered in the frame. The same typographic anchor is retained across different activities; the actual words change.
- **captionMotion:** Direct short-label replacement. At the first hard cut, choose real dopamine changes to deep work. It is the position that continues, not the caption content.
- **footageMotion:** Movement comes mainly from the shot action: curtain opening, work, exercise, writing and outdoors. No reliable evidence of reversed playback or a speed ramp was established.
- **layoutAndAssets:** Full-frame shots with a single central label. No extra illustration grid, banner or permanent decorative frame.
- **transitions:** Hard cut from curtain to desk between frames 47 and 48, approximately 1.960–2.002s. Other shots use short durations; no transition effect is required to create pace.
- **colorAndLighting:** Different lighting by location, generally natural and somewhat subdued. A source LUT cannot be inferred from this alone.
- **visualFlow:** Longer opening action followed by shorter activity shots and an outdoor release. Beat synchronization is not assessed without listening.

## Các sự kiện nguồn

- **0–2.00s** — Curtain-opening shot.
- **2.00–3.55s** — Two desk/work shots.
- **3.55–4.55s** — Meditation.
- **4.55–6.30s** — Exercise shots.
- **6.30–7.80s** — Short reading/writing shots.
- **7.80–9.8s** — Mountain and forest closing.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
