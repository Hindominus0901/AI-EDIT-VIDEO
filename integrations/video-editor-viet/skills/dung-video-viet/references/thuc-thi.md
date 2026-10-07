# Quy trình thực thi cho AI

## Tìm và chuẩn bị bộ dựng

Tìm `package.json` có name `video-editor-kit`, `src/Root.tsx`, `scripts/doctor.py` trong thư mục người dùng đưa. Gói phân phối đặt engine cạnh thư mục `skills` ở `<plugin>/engine`. Trong mã nguồn phát triển, engine là thư mục cha của `integrations/video-editor-viet`. Không quét toàn ổ đĩa.

Nếu engine nằm trong cache plugin chỉ đọc, sao chép engine vào thư mục làm việc người dùng đã chọn, hoặc thư mục `Video-AI` trong khu vực làm việc được phép. Kiểm tra đích và giữ nguyên dự án có sẵn. Không lưu profile/output vào thư mục plugin dùng chung.

Chọn Python trong `.venv` nếu có; nếu host cấp runtime sẵn, dùng đường dẫn host cung cấp. Các lệnh dưới đây dùng `python` làm ký hiệu cho runtime đã tìm. Luôn đặt cwd là engine. Windows dùng `npm.cmd`/`npx.cmd` khi cần. Không tự cài Claude CLI.

```text
python scripts/doctor.py --mode all --json
python scripts/setup-runtime.py --install
```

`doctor` chỉ kiểm tra; `--mode render` dùng khi có EDL/transcript, không ép cài STT. Chỉ chạy `--install` trong phạm vi yêu cầu setup hoặc quyền cài đã có, theo chính sách host. Script cài vào `.venv` và `node_modules`; không cài phần mềm hệ thống hay sửa quyền. Thiếu Node/FFmpeg thì hướng dẫn đúng nền tảng, không lặp cài khi lỗi mạng/quyền. Tối đa một lần sửa theo nguyên nhân đã xác định; lỗi tương tự thì báo cụ thể.

## Mỗi video một dự án

Dùng `out/<ma-du-an>/` riêng, mã ASCII ngắn; giữ `brief.json`, `transcript.json`, `host-plan.json`, `edl.json`, MP4 và SRT. Không chia sẻ hồ sơ hoặc clip giữa khách hàng. Copy nguồn vào `public/raw/<ma-du-an>/` với tên duy nhất, giữ tệp gốc. Kiểm tra số luồng audio/video bằng ffprobe trước STT; nguồn không có giọng thì dùng nhánh cảnh quay + chữ, không ép nhận giọng.

Với nguồn mới, pipeline hỗ trợ thư mục riêng và cache transcript:

```text
python scripts/run-pipeline.py raw/<ma-du-an>/nguon.mp4 --out-dir out/<ma-du-an> --edit-style clean --llm offline --language vi --aspect 9:16
```

Chỉ truyền `--language vi` khi đã xác minh nguồn Việt; nguồn khác dùng mã phù hợp. Chạy bước này không `--render` để có transcript/đề xuất cắt. Kiểm tra `cut-report.json`, đối chiếu nguồn ở điểm vấp/ngắt và chọn đoạn có nghĩa. Pipeline tự cắt khoảng im lặng, không tự chọn câu chuyện trong video dài. Nếu cần chọn lại câu/đoạn, tạo một bản nguồn đã cắt riêng và ánh xạ lại transcript trước khi viết host plan.

Nguồn có transcript đã đúng thì dùng lại. Không chạy lại STT chỉ vì sửa chữ/nhạc/preset/tỷ lệ. Đọc `edl.json.source.clip` để biết file sau cắt; không đoán tên `-tight.mp4`.

## Từ hồ sơ sang bản dựng

Từ bản 1.5: đọc `UPGRADE-1.5.md` ở engine khi cần font C, camera/B-roll có timing hoặc rút gọn theo ý. `premiumSet: editorial-c` đã có renderer thật và font local. `camera`/`broll` trong host plan được kiểm tra và đưa vào focused renderer; không dùng chúng như alias cho một ref package chưa triển khai. Với video dài, host chọn khoảng nguồn trong keep plan rồi dùng reviewed_cuts.py để remap transcript; vẫn cần nghe các điểm nối, không coi timestamp là chứng minh cắt tự nhiên.

Đọc kết quả `user_profile.py resolve`:

- style studio/paper/mono/editorial-c → `premiumSet` trong host plan; clean → bỏ key.
- aspect → tham số `--aspect` và bản xuất; `both` tạo một edit và hai bố cục, không lập kế hoạch hai lần.
- music none → bỏ `music`; sfx none → đặt `sound:false` cho mọi moment và bỏ cue SFX của EDL khi sửa.
- provided-only → chỉ chọn asset người dùng đưa; generation-allowed là sở thích, không thay thế kiểm tra công cụ/ngân sách cụ thể.
- captionLanguage khác nguồn → AI dịch ngắn theo ý và cấp cue đã rà soát. Không dịch bằng thay từ đơn lẻ.
- targetDurationSec là mục tiêu biên tập, không tự tăng tốc hoặc cắt ngang câu để vừa thời lượng.

Viết `host-plan.json` một lần từ nội dung đã hiểu. Ví dụ hình dạng, không dùng thời gian minh họa cho clip thật:

```json
{"clip":"raw/ma-du-an/nguon-da-cat.mp4","timebase":"edited-clip","premiumSet":"studio","captions":[{"startMs":0,"endMs":1600,"text":"Bắt đầu từ điều nhỏ"}],"moments":[{"sec":0,"keyword":"điều nhỏ","role":"hook","sound":false}]}
```

Role: hook/shift/proof/example/emphasis/close. Ảnh: `images` và `graphic` photo-window/photo-circle/photo-collage/photo-mat/photo-diptych/photo-detail; collage/diptych cần 2 ảnh. Đọc thêm `CLEAN-AUTO-FLOW.md` trong engine khi cần schema đầy đủ.

```text
python scripts/generate-edl.py --clip raw/<clip-da-cat>.mp4 --out-dir out/<ma-du-an> --plan out/<ma-du-an>/host-plan.json --llm prefed --edit-style clean --aspect 9:16
python scripts/validate-edl-risk.py out/<ma-du-an>/edl.json
python scripts/render-edit.py --out-dir out/<ma-du-an> --aspect 9:16
```

`edl.json` là bản đang dùng; máy sinh `edl.generated.json`. Khi bản đang dùng đã sửa tay, không mù quáng `--force-regen`: hợp nhất có chủ đích hoặc tạo revision mới. Sửa nhỏ trực tiếp EDL rồi chỉ render. Nghe/xem tệp cuối khi có công cụ; nếu không, nêu giới hạn review. `SRT` chỉ chứa lời và thời gian, hiệu ứng chữ nằm trong MP4.

Khi cài lần đầu, chạy `python scripts/smoke-test.py --aspect 9:16` để xuất thử 3 giây có dấu Việt bằng nguồn tổng hợp. Script xác minh decode; AI vẫn phải xem frame để kiểm tra font. Đây là test môi trường, không thay cho video thật. Không dùng clip cá nhân của người trước để demo cho người mới.
