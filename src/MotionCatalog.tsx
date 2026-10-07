import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Inter';
import {textPresets, emphasisPresets, graphicPresets} from './motion-kit/catalog';
import {MotionText} from './motion-kit/TextMotion';
import {LineAsset, MotionGraphic, type AssetId} from './motion-kit/GraphicMotion';
import assets from './motion-kit/assets.json';
const {fontFamily}=loadFont('normal',{weights:['500','600','700'],subsets:['latin','vietnamese']});
const titles=['Chữ xuất hiện · Nhẹ và rõ','Chữ xuất hiện · Thêm lựa chọn','Nhấn đúng từ quan trọng','Ảnh, crop & graphic','Minh họa nét mảnh'];
const descriptions=['Một kiểu chính cho phụ đề. Đổi kiểu ở những câu có vai trò khác nhau.','Dùng chọn lọc cho hook, headline hoặc lúc đổi ý.','Chọn một cách nhấn cho mỗi cụm. Phần còn lại để người xem đọc dễ dàng.','Một hình hỗ trợ mỗi thời điểm. Collage dùng khi cần đối chiếu.','8 asset vector gốc, có thể đổi màu và vẽ nét theo thời gian.'];
export const MotionCatalog:React.FC=()=>{
  const frame=useCurrentFrame();const {fps}=useVideoConfig();
  const page=Math.min(4,Math.floor(frame/fps/8));
  const elapsed=(frame/fps%8)%4;
  const four=page<3;const columns=page===4?4:page===3?3:2;
  const list=page<2?textPresets.slice(page*4,page*4+4):page===2?emphasisPresets:page===3?graphicPresets.slice(0,6):Object.entries(assets).map(([id,a])=>({id,name:a.name}));
  return <AbsoluteFill style={{background:'#080b09',fontFamily,color:'#f6f5ef',padding:'64px 88px'}}>
    <div style={{display:'flex',alignItems:'center',gap:24,color:'#F3CE83',fontSize:22,letterSpacing:3,fontWeight:600}}><span>MOTION KIT</span><span style={{color:'#8c9690',letterSpacing:0}}>VIỆT / {String(page+1).padStart(2,'0')}</span></div>
    <div style={{fontSize:54,fontWeight:600,letterSpacing:-1.8,marginTop:18}}>{titles[page]}</div>
    <div style={{fontSize:23,color:'#a2aaa4',marginTop:13}}>{descriptions[page]}</div>
    <div style={{display:'grid',gridTemplateColumns:`repeat(${columns},1fr)`,gridTemplateRows:'repeat(2,1fr)',gap:24,marginTop:40,height:674}}>
      {list.map(item=><div key={item.id} style={{position:'relative',border:'1px solid #28312b',borderRadius:18,background:'#111713',overflow:'hidden'}}>
        <div style={{position:'absolute',left:28,top:24,fontSize:20,color:'#a2aaa4'}}>{item.name}</div>
        {page<2&&<div style={{position:'absolute',inset:'80px 16px 46px',display:'grid',placeItems:'center'}}><MotionText text="Bắt đầu từ ngách nhỏ" preset={textPresets.find(p=>p.id===item.id)!.id} elapsed={elapsed} duration={3.8} keyword={{text:'ngách nhỏ'}} style={{fontSize:46}}/></div>}
        {page===2&&<div style={{position:'absolute',inset:'80px 16px 46px',display:'grid',placeItems:'center'}}><MotionText text="Tạo bằng chứng thật" preset="rise" elapsed={elapsed} duration={3.8} keyword={{text:'bằng chứng',style:emphasisPresets.find(p=>p.id===item.id)!.id}} style={{fontSize:46}}/></div>}
        {page===3&&<MotionGraphic cue={{start:0,end:3.8,kind:graphicPresets.find(p=>p.id===item.id)!.id,images:['images/editorial-v4/ocean.jpg','images/editorial-v4/pond.jpg']}} elapsed={elapsed} duration={3.8} style={{position:'absolute',top:84,left:'16%',width:'68%',height:185}}/>}
        {page===4&&<div style={{position:'absolute',top:85,left:'32%',width:'36%',height:160,opacity:elapsed<3.8?1:0}}><LineAsset asset={item.id as AssetId} progress={Math.min(1,elapsed/.55)}/></div>}
        {four&&<div style={{position:'absolute',bottom:18,left:28,right:28,height:2,background:'#243027'}}><div style={{height:'100%',width:`${Math.min(100,elapsed/3.8*100)}%`,background:'#758679'}}/></div>}
      </div>)}
    </div>
    <div style={{position:'absolute',bottom:30,left:88,right:88,display:'flex',justifyContent:'space-between',color:'#77857b',fontSize:18}}><span>Inter · đủ dấu tiếng Việt · chuyển động theo frame</span><span>Mỗi mẫu lặp 2 lần · không kèm âm thanh</span></div>
  </AbsoluteFill>;
};
