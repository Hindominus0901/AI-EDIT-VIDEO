# Video Editor 1.6 — dựng theo ý, ba hướng creator

## Đã triển khai

`creatorStyle: iman | hormozi | martell` đi vào renderer riêng `CreatorFromEdl`, không alias sang Studio. Các hướng là bản chuyển thể đang thử, chưa phải bản sao đã đo đầy đủ từ một video cụ thể hoặc đã được người dùng duyệt.

- Story gồm người xem, luận điểm và điều cần nhớ. Scene có ý nghĩa, lý do và thời gian nguồn đã dựng.
- Năm layout thật: người nói; câu chốt toàn khung; hai vế so sánh; 2–3 bước xuất hiện theo lời; ảnh bằng chứng có nguồn.
- Hình bằng chứng lặp cần chỉ cảnh gốc và lý do hồi nhắc. Không áp quota số hiệu ứng để lấp clip.
- Chữ Việt dùng font local Manrope; điểm nhấn serif dùng Playfair. Ba cấu hình typography, màu và độ dài entrance riêng; không gọi đây là font/keyframe gốc của creator.
- Camera và B-roll do host chọn theo ý, dùng lại engine 1.5. Fit contain mặc định; cover và điểm focus phải review trên mặt/tay thật.
- Nhạc có envelope giảm nền quanh câu chốt, duck theo vùng caption lời; SFX phải cấp cue có lý do. Đây không phải phân tích âm giọng tự động hay loudness normalization.
- Kiểm tra trước render chặn cảnh chồng nhau, ngoài thời lượng, item vào quá muộn, ảnh thiếu/đường dẫn ngoài public, B-roll chồng cảnh đồ họa, audio cue không có nhạc.
- CLI mặc định `--llm offline`, không vô tình gọi Claude CLI. Host viết plan một lần, sửa EDL giữ cơ chế bảo vệ bản tay. Chỉ gọi provider legacy khi chủ động chọn.
- `project-context.json` được tạo từ EDL đang dùng khi generate/render: luận điểm, style, chỉ mục cảnh gọn và hash. Không nhét lại transcript vào ngữ cảnh. File này không chứng nhận đã nghe/duyệt bản dựng.
- Hồ sơ kênh nhận ba tên mới; giữ hồ sơ cũ, không tự trộn ba người trong một clip.

## Cách dùng qua hội thoại

“Dựng video này theo hướng Iman, ưu tiên kể chuyện và dẫn chứng thật.”

“Dựng theo hướng Hormozi, câu mở rõ và lập luận trực tiếp; giữ đủ phủ định.”

“Dựng theo hướng Dan Martell, giải thích quy trình theo từng bước.”

Host chọn một hướng chính theo yêu cầu, đọc reference cụ thể khi có, viết câu chuyện và beat trước asset. Sửa caption không chạy STT lại. Không mua/tạo media mới khi chưa có quyền/ngân sách phù hợp.

## Host plan chạy được

Ví dụ timing minh họa; phải thay bằng timing clip thật. `startMs/endMs` theo clip sau cắt; `items[].atMs` tương đối với đầu scene.

```json
{
  "clip":"raw/project/source.mp4",
  "timebase":"edited-clip",
  "creatorStyle":"martell",
  "story":{"audience":"Người mới","premise":"Một quy trình rõ","payoff":"Biết bước tiếp theo"},
  "framing":{"fit":"contain","focusX":50,"focusY":50},
  "moments":[],
  "scenes":[
    {"id":"intro","startMs":0,"endMs":3000,"layout":"speaker","meaning":"Đặt vấn đề","reason":"Giữ gương mặt và giọng thật"},
    {"id":"explain","startMs":3000,"endMs":7500,"layout":"steps","title":"Hai việc cần làm","meaning":"Trình tự thực hiện","reason":"Hiện từng bước đúng lời","items":[{"text":"Chọn một ý","atMs":0},{"text":"Đưa bằng chứng","atMs":1800}]}
  ]
}
```

Khoảng không có scene mặc định là người nói. Caption tự chia từ transcript đã đúng hoặc cấp `captions` như clean. `moments` chỉ dùng highlight lời, không truyền asset/ảnh kiểu cũ. `statement` chủ động thay caption bằng câu chốt trên khung, SRT vẫn giữ lời nguồn. `compare` cần đúng 2 item; `steps` cần 2–3; `evidence` cần image local và assetSource. Title tối đa 85 ký tự, item 60; vẫn cần nhìn độ vừa ở mỗi tỷ lệ.

`audioCues:[{"startMs":5000,"endMs":7000,"gain":0.2,"reason":"Hạ nền cho câu chốt"}]` giảm nhạc đã cấp, không tạo nhạc. `soundCues` nhận kit-tick/kit-drop/kit-scroll với startMs, volume 0–0.3, reason. Giới hạn gain không thay nghe/đo âm thanh.

```text
python scripts/generate-edl.py --clip raw/project/source.mp4 --out-dir out/project --plan out/project/host-plan.json --llm prefed --edit-style clean --aspect 9:16
python scripts/render-edit.py --out-dir out/project --aspect 9:16
```

Renderer dọc/ngang có bố cục riêng. Preview kỹ thuật dùng `creator-demo.py --render`; fixture mặc định 3 giây nguồn tổng hợp, không phải bản dựng hoàn chỉnh. Không phát hành video khách hàng cùng kit.

## Bằng chứng nghiên cứu và giới hạn

- [Iman — If I Was Broke In My 20s](https://www.youtube.com/watch?v=9CjCs0q6XmY): đã xuất transcript tự động; quan sát frame khoảng 8/15s. Mở bằng đạo cụ thẻ sưu tầm để giải thích tích lũy kỹ năng. Suy luận chuyển thể: vật/hình trung tâm phải gắn lập luận, không chỉ trang trí. Chưa đo motion toàn video; không suy phong cách mọi video từ mẫu này.
- [Dan — How To Buy Back Your Time & Increase Profit](https://www.youtube.com/watch?v=0n77p5b-Wu4): đã xuất transcript và xem frame 10s; nguồn [bài đăng chính chủ](https://www.danmartell.com/buy-back-your-time-boost-profits/) hỗ trợ cấu trúc nội dung. Đoạn mở trình bày nguyên lý rồi giới thiệu vấn đề và cách giải quyết. Các scene bước là chuyển thể, chưa xác nhận toàn bộ chuyển động gốc.
- [Alex — How to get what you want](https://www.youtube.com/watch?v=YaNX49ygr0I): xác minh trang chính chủ, công cụ không cung cấp transcript cho mẫu này. Nguồn local R18 mới có scope frame; chưa audit toàn bộ. Cấu hình Hormozi hiện là thiết kế đề xuất, chưa chứng minh bám một video gốc cụ thể.
- Chưa nghe trực tiếp mix các ref/bản thử. Việc video decode được hoặc có transcript không chứng minh nhịp cảm xúc đã đúng. Cần đối chiếu ref cụ thể người dùng thích và review bản chuyển thể trước khi gọi là đạt gu.

Không thêm timeline kéo thả, tự phân đoạn ngữ nghĩa bằng model riêng, auto color-match/LUT hay 21 adapter cho các package cũ trong bản này. Mọi khả năng trên là phạm vi 1.6; yêu cầu “như creator” vẫn cần lựa chọn biên tập trên từng nguồn.
