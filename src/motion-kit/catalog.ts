export const textPresets = [
  {id:'hold', name:'Giữ chữ ổn định', use:'Cụm phụ đề liên tiếp; không fade lại ở mỗi cụm.'},
  {id:'rise', name:'Trượt lên mềm', use:'Phụ đề thường; chuyển động nhẹ, giữ chữ ổn định.'},
  {id:'mask-up', name:'Mở chữ từ dưới', use:'Đổi ý hoặc mở một câu mới.'},
  {id:'soft-pop', name:'Nhấn rồi ổn định', use:'Câu chốt; không dùng ở mọi cụm.'},
  {id:'word-rise', name:'Lên lần lượt theo cụm', use:'Hook ngắn; đây là hiệu ứng vào, không phải karaoke theo giọng.'},
  {id:'slide-left', name:'Trượt ngang nhẹ', use:'Chuyển sang ý đối chiếu.'},
  {id:'blur-in', name:'Rõ dần', use:'Tiêu đề ngắn; tránh dùng liên tục cho phụ đề.'},
  {id:'wipe', name:'Mở từ trái sang phải', use:'Headline hoặc câu kết ngắn.'},
  {id:'tracking', name:'Thu khoảng chữ', use:'Headline; thay đổi khoảng chữ rất nhẹ.'},
  {id:'silk-rise', name:'Trượt tinh tế', use:'Dịch nhẹ 8px, không nảy; phụ đề premium.'},
  {id:'quiet-reveal', name:'Mở dòng gọn', use:'Mở qua mask, giữ đường chân chữ ổn định.'},
  {id:'soft-focus', name:'Lấy nét nhẹ', use:'Rõ dần trong thời gian ngắn, không phóng chữ.'},
] as const;
export type TextPreset = typeof textPresets[number]['id'];
export const emphasisPresets = [
  {id:'color',name:'Đổi màu'}, {id:'underline',name:'Gạch chân vẽ vào'},
  {id:'marker',name:'Quét bút đánh dấu'}, {id:'ring',name:'Khoanh nét mảnh'},
] as const;
export type EmphasisPreset = typeof emphasisPresets[number]['id'];
export const graphicPresets = [
  {id:'photo-window',name:'Ảnh mở qua khung'},
  {id:'photo-circle',name:'Crop tròn'},
  {id:'photo-collage',name:'Collage hai ảnh'},
  {id:'line-arrow',name:'Mũi tên vẽ nét'},
  {id:'focus-ring',name:'Vòng nhấn'},
  {id:'steps',name:'Ba bước nối tiếp'},
  {id:'icon',name:'Minh họa vẽ nét'},
  {id:'photo-mat',name:'Ảnh có viền phẳng'},
  {id:'photo-diptych',name:'Hai ảnh thẳng hàng'},
  {id:'photo-detail',name:'Ảnh và crop chi tiết'},
  {id:'ui-grid',name:'Lưới giải thích Uiverse'},
  {id:'ui-glass',name:'Card kính Uiverse'},
  {id:'ui-notification',name:'Thông báo Uiverse'},
] as const;
export type GraphicPreset = typeof graphicPresets[number]['id'];
export const rules = {
  maxCaptionWords:5, maxSimultaneousGraphics:1, defaultTextPreset:'rise',
  defaultAccent:'#F3CE83', maxEntryFraction:.35,
  sfxPolicy:'Chỉ gắn vào điểm nhấn có chủ ý, không gắn tự động vào mọi phụ đề.',
};
