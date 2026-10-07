# R01 — Editorial Việt — chiều sâu

Gói phương pháp dựng, form và bằng chứng. Không phải preset renderer một nút.

[Thông số lớp hình, chữ và motion](recipe.json) · [Form kế hoạch](form.json)

Recipe mô tả một cảnh đặc trưng với vị trí 9:16/16:9, font, vào/giữ/ra và cue theo nghĩa. Thông số chuyển thể tách khỏi bằng chứng đo; các layout còn lại phải đọc ref và triển khai riêng.

## Dùng khi

Nội dung quan điểm, thương hiệu cá nhân

## Font đề xuất

Be Vietnam Pro — chưa xác nhận font gốc

## Phân cấp chữ

Sans nặng, chữ trắng; dòng chốt lớn hơn dòng dẫn; hook có chữ sau đầu.

## Ảnh / graphic

Cảnh ngữ cảnh, trang hồ sơ, title card trắng; mỗi hình chứng minh đúng một ý.

## Motion

Hook fade khoảng 0,07–0,23s; footage lùi độc lập; body giữ chữ sau khi vào.

## Flow

Luận điểm → ngữ cảnh thật → câu chốt toàn màn → trở về người nói.

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

Không mask từng phụ đề; không dùng cùng cảnh ngữ cảnh cho nhiều luận điểm.

## Form sử dụng

1. Chọn đúng gói cho nội dung.
2. Chốt câu chuyện và điểm cắt.
3. Mỗi beat ghi ý nghĩa, layout, ref-event, ảnh mới và vào/giữ/ra.
4. Gặp thiếu ảnh thì giữ người nói, không lặp tranh cũ.
5. Chạy kiểm tra plan, đối chiếu đoạn thử với ref, rồi mới xuất dài.

Giới hạn mặc định là quyết định để tránh lặp/rối của dự án, không phải số liệu đo được của bản gốc. Mỗi ảnh chỉ xuất hiện một lần; callback phải cùng ý, ghi rõ beat trước và cách ít nhất 30 giây.

## Những gì đã quan sát ở ref

- **typography:** Heavy compact sans serif with Vietnamese diacritics, tight letter spacing and a soft dark shadow. Large opening letters pass visually behind the head. Captions use different sizes within one phrase: the second line can become the emphasis. Font identity remains unconfirmed.
- **captionMotion:** A phrase fades in and holds; a more important second line can arrive later. At the opening, faint text is visible around 0.07–0.10s, layered headline by 0.13s, strong opacity around 0.23s; it clears around 0.9–1.1s. The text does not continuously bounce. Some stretches deliberately have no caption.
- **footageMotion:** Opening image pulls back quickly and decelerates, independently of the typography. Background feature match estimates about 25% shrink from 0 to 1s, with some rotation/translation; this walking shot has lower transform confidence than the stationary-camera examples. Later footage contains real walking, hand movement and handheld parallax. These are separate from an edit zoom.
- **layoutAndAssets:** Base talking head alternates with contextual meeting/working footage, full off-white title cards, tilted profile-page cards, and an isolated speaker over dark explanatory material. Strong hierarchy and temporary changes of visual mode provide variety.
- **transitions:** Most contextual changes are direct cuts. Title text uses a readable fade/build. The opening masking effect and simultaneous image pullback are distinct layers; the original masking method cannot be recovered from the flattened MP4.
- **colorAndLighting:** Natural daylight and green foliage; interiors are warmer. Black/white editorial cards create contrast. Context footage is sometimes darkened behind text. No exact LUT or camera exposure values identified.
- **visualFlow:** Talking head establishes the argument, a context insert illustrates it, a large title punctuates a key idea, then attention returns to the speaker. Graphic treatment is episodic rather than continuously busy.

## Các sự kiện nguồn

- **0–1.1s** — Layered headline entrance over a decelerating pullback.
- **5.07–8.60; 13.63–16.90; 25.17–30.60s** — Meeting, outdoor group and workshop coverage.
- **39.27–43.63; 50.10–54.13s** — Computer and meeting coverage, then speaker returns.
- **59.73–61.43; 74.90–77.50; 88.20–91.17; 128.03–131.93s** — Full off-white headline cards with black type.
- **66.60–70.30; 82.87–85.03s** — Projection and whiteboard context.
- **102.77–105.10s** — Floating page/profile cards on a light field.
- **110.43–114.07; 118.30–120.90s** — Isolated speaker over dark note/checklist material.
- **120.90–124.20; 132–149s** — Seminar insert, then seated outdoor closing; large final like prompt.

## Chưa xác minh

- Exact font family and font-file version
- Original keyframes and easing curves
- Original LUT or grading parameters
- Music, SFX and synchronization: not listened to in this audit
- Speech-edit semantics and natural audio joins: not assessed
