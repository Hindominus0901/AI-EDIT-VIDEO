# R06 — Podcast — hook mạnh, body yên

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Phỏng vấn, chuyên gia, lập luận bằng lời

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Hook condensed/brush và cyan; body sans trắng thường nhỏ hơn hẳn. Font brush gốc chưa rõ.

## Ảnh / graphic

Micro và người nói là hình chính; body không có lớp ảnh trang trí lặp.

## Motion

Hook vào theo lớp; flare 2,3–2,5s; punch +9% trong một frame ở 19,5s.

## Flow

Hook mạnh → chuyển một lần → giải thích sạch → punch đúng ý → kết.

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

Không dùng chữ hook suốt bài; không biến punch cut thành zoom ngẫu nhiên.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** The hook uses a very tall condensed white YOUR, cyan emphasis, wide heavy capitals and an italic brush accent. The body switches to a much quieter regular white sans. Treating the whole clip as one font preset would miss its defining contrast.
- **captionMotion:** Large hook words arrive in stages. From about 2.5s, small one-line body captions mostly replace directly and hold near the lower chest. Source English phrases can exceed the preferred Vietnamese word count.
- **footageMotion:** Abrupt crop changes rather than continuous body motion. Frame 584 at 19.4667s to frame 585 at 19.5000s has about 9.0% image enlargement plus a small downward/left reframe. This is a one-frame punch-in, independently verified with background matching.
- **layoutAndAssets:** Side-angle speaker with microphone and soft background. No recurring photo-card layer in the body. The hook is intentionally louder than the sustained edit.
- **transitions:** Orange/red film-burn-like flare around 2.3–2.4s covers a framing reset. This differs from the white flash in R07. Later crop changes are clean hard changes.
- **colorAndLighting:** Soft warm podcast environment with blue clothing and cyan hook accents. Flare warmth is transient, not the whole-video grade.
- **visualFlow:** High-energy opening, clean explanatory body, occasional reframing. Preserve that contrast rather than applying hook typography to every sentence.

## Các sự kiện nguồn

- **0–2.20s** — Tall condensed and mixed-width/brush hook typography.
- **2.30–2.50s** — Warm flare, crop reset, then quiet caption mode.
- **4.5–4.67; 19.4667–19.5000; 20.83–21s** — Measured or visually supported framing-change passages.
- **2.5–41s** — Mostly quiet single-line white captions and podcast footage.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
