# R12 — Kể chuyện — sơ đồ lược bỏ

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Giải thích hệ thống sau các ví dụ thật

## Font đề xuất

Inter — chưa xác nhận font gốc

## Phân cấp chữ

Caption trắng gọn; sơ đồ chữ đen trên trắng, một dải highlight lime.

## Ảnh / graphic

Sơ đồ đi từ nhiều chủ đề xuống một hệ thống, connector rồi luận điểm.

## Motion

Thu/xóa nhãn → lớn lên → dời lên → vẽ dây → quét highlight; khác camera zoom.

## Flow

Ví dụ thật → vấn đề phức tạp → lược bỏ → một cơ chế → trở về người nói.

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

Không thêm graph nếu không có quan hệ thật; không sao lỗi chữ bị cắt bên trái.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Compact white sans phrase captions around the center of the portrait canvas, medium weight in the inspected sample. The graphic sequence switches to black labels on white and one lime highlighter accent.
- **captionMotion:** Short caption fragments hold while the background changes. In the conceptual graphic, topic labels shrink away; SYSTEMS grows from tiny, moves upward, a connector draws, then a lime highlight wipes left-to-right as a phrase builds.
- **footageMotion:** Varied archival/context shots and current talking head. A slow push is supported in the speaker passage around 22–24s. Graphic label scaling must not be mistaken for camera movement.
- **layoutAndAssets:** The white diagram is a landscape band letterboxed on black inside the portrait export. It is a sustained explanatory scene, not a white flash. The final sentence is clipped at the left edge in the source.
- **transitions:** Context footage mostly hard cuts. The diagram uses scale-down/removal, scale-up, repositioning, line drawing, highlight wipe and staged phrase addition. It cuts back to the speaker around 48.17s.
- **colorAndLighting:** Mixed archival lighting and warmer current footage. Diagram mode uses white, black and lime. Source clipping is a layout defect to avoid reproducing.
- **visualFlow:** Examples and biography lead into a simplifying visual argument: remove excess topics, leave a system, explain what it does, return to the speaker. The order of animation carries meaning.

## Các sự kiện nguồn

- **0–21s** — Archival, interview and process coverage intercut with a speaker.
- **22–28s** — Current talking head with a gentle push.
- **29–39s** — Work/process and close interview coverage.
- **39.5–43.9s** — Topic network on a white landscape band; topics recede and clear.
- **44.29–45.90s** — SYSTEMS grows, shifts upward, connector begins.
- **45.75–48.17s** — Lime wipe plus building → building profitable → personal brands phrase development; then cut back.
- **48.17–60s** — Speaker and event/network/stage coverage.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
