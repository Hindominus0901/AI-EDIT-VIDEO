import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont as inter} from '@remotion/google-fonts/Inter';
import {loadFont as newsreader} from '@remotion/google-fonts/Newsreader';

const {fontFamily: sans} = inter('normal', {weights:['500','600','700'], subsets:['latin','vietnamese']});
const {fontFamily: serif} = newsreader('normal', {weights:['500'], subsets:['latin','vietnamese']});
type Beat = {start:number; end:number; kind:'question'|'context'|'proof'|'contrast'|'niche'|'close'; title:string; kicker:string; image?:string; lines:string[]; note?:string; imageLabel?:string};
export type EditorialProps = {
  clip:string; durationSec:number; vertical:boolean; headline:string; emphasis:string; sourceLabel:string;
  captions:{start:number;end:number;text:string}[];
  beats:Beat[];
  music:string;
  sounds:{sec:number;src:string;gain:number}[];
};
export const editorialDefaults:EditorialProps={clip:'samples/setup-test.mp4',durationSec:3,vertical:true,headline:'Bắt đầu từ một',emphasis:'ngách nhỏ.',sourceLabel:'TRÍCH ĐOẠN / PHỤ ĐỀ VIỆT',captions:[],beats:[],music:'',sounds:[]};
const ink='#202622', paper='#f1eee6', green='#3c6454', muted='#71746a';
const ease=(x:number)=>1-Math.pow(1-Math.max(0,Math.min(1,x)),3);

const Photo:React.FC<{src:string;w:number;h:number;rotation?:number;progress:number;label:string}> = ({src,w,h,rotation=0,progress,label}) =>
  <div style={{width:w, background:'#fffcf6',padding:13,boxShadow:'0 12px 28px #20262220',transform:`rotate(${rotation}deg) translateY(${(1-progress)*28}px)`,opacity:progress}}>
    <div style={{width:w-26,height:h,overflow:'hidden'}}><Img src={staticFile(src)} style={{width:'100%',height:'100%',objectFit:'cover',transform:`scale(${1.025-progress*.025})`,filter:'saturate(.72)'}}/></div>
    <div style={{fontSize:20,marginTop:13,letterSpacing:1,color:ink}}>{label}</div>
  </div>;

const Art:React.FC<{beat:Beat;t:number;wide:boolean}> = ({beat,t,wide}) => {
  const p=ease(t/.55);
  const area=wide?690:900;
  const shared:React.CSSProperties={position:'absolute',width:area,height:440,transform:`translateY(${(1-p)*20}px)`,opacity:p};
  if(beat.kind==='question') return <div style={shared}>
    <div style={{fontFamily:serif,fontSize:64,lineHeight:1.08,marginTop:25}}>{beat.lines[0]}<br/>{beat.lines[1]}</div>
    <div style={{position:'absolute',right:30,top:250,transform:'rotate(-5deg)',background:green,color:paper,padding:'20px 30px',fontSize:26}}>{beat.note}</div>
    <div style={{position:'absolute',bottom:42,left:0,fontSize:24,color:muted}}>{beat.imageLabel}</div>
  </div>;
  if(beat.kind==='context') return <div style={shared}>
    <div style={{fontSize:21,letterSpacing:2,color:muted}}>ĐIỂM XUẤT PHÁT</div>
    <div style={{fontFamily:serif,fontSize:74,lineHeight:1.05,marginTop:26}}>{beat.lines[0]}<br/>{beat.lines[1]}</div>
    <svg width={area} height="80" style={{marginTop:20}}><path d={`M 4 30 Q ${area*.36} 5 ${area*.64} 30`} fill="none" stroke={green} strokeWidth="4" strokeDasharray="700" strokeDashoffset={700*(1-ease((t-.25)/.7))}/></svg>
  </div>;
  if(beat.kind==='proof') return <div style={shared}>
    <div style={{position:'absolute',left:wide?380:510,top:28,transform:`rotate(${5-2*p}deg)`,width:230,height:280,background:'#d3d7cb',border:'1px solid #afb6a6'}}/>
    <div style={{position:'absolute',left:wide?355:475,top:12,transform:'rotate(-4deg)'}}>
      <Img src={staticFile('images/editorial/proof.svg')} style={{width:265,height:310,objectFit:'cover',boxShadow:'0 10px 25px #20262220'}}/>
    </div>
    <div style={{position:'absolute',left:0,top:48,fontFamily:serif,fontSize:wide?52:74,lineHeight:1.1}}>{beat.lines[0]}<br/><span style={{color:green}}>{beat.lines[1]}</span></div>
    <div style={{position:'absolute',left:5,bottom:48,fontSize:25,color:muted}}>{beat.note}</div>
  </div>;
  if(beat.kind==='contrast') return <div style={shared}>
    <div style={{position:'absolute',right:wide?0:30,top:4}}><Photo src={beat.image!} w={wide?310:380} h={240} rotation={4} progress={p} label={beat.imageLabel??""}/></div>
    <div style={{position:'absolute',left:0,top:36,fontFamily:serif,fontSize:wide?64:78,lineHeight:1.02}}>{beat.lines[0]}<br/>{beat.lines[1]}</div>
    <svg width={area} height="65" style={{position:'absolute',left:0,bottom:42}}><path d="M 6 35 Q 130 15 380 32" stroke="#ac664b" strokeWidth="5" fill="none" strokeDasharray="400" strokeDashoffset={400*(1-ease((t-.2)/.6))}/></svg>
  </div>;
  if(beat.kind==='niche') return <div style={shared}>
    <div style={{position:'absolute',left:15,top:8}}><Photo src={beat.image!} w={wide?290:365} h={245} rotation={-4} progress={p} label={beat.imageLabel??""}/></div>
    <div style={{position:'absolute',left:wide?340:440,top:38,fontFamily:serif,fontSize:wide?63:83,lineHeight:1.02}}>{beat.lines[0]}<br/><span style={{color:green}}>{beat.lines[1]}</span></div>
    <div style={{position:'absolute',left:wide?340:440,top:245,fontSize:24,lineHeight:1.5,color:muted}}>{beat.note}</div>
    <svg width={area} height="440" style={{position:'absolute',left:0,top:0,pointerEvents:'none'}}>
      <ellipse cx={wide?158:196} cy="143" rx={wide?126:165} ry="112" fill="none" stroke="#e7bd73" strokeWidth="5" strokeDasharray="1000" strokeDashoffset={1000*(1-ease((t-.6)/.7))}/>
    </svg>
  </div>;
  return <div style={shared}>
    {beat.lines.map((line,i)=> {
      const enter=ease((t-i*1.15)/.45);
      return <div key={line} style={{display:'flex',alignItems:'baseline',gap:24,marginBottom:28,opacity:enter,transform:`translateX(${(1-enter)*25}px)`}}>
        <span style={{fontSize:19,color:muted}}>0{i+1}</span><span style={{fontFamily:serif,fontSize:wide?56:69,lineHeight:1.12,color:i===2?green:ink}}>{line}</span>
      </div>;
    })}
  </div>;
};

export const EditorialPreview:React.FC<EditorialProps> = (p) => {
  const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();const sec=frame/fps;
  const beat=p.beats.find(b=>sec>=b.start&&sec<b.end);
  const caption=p.captions.find(c=>sec>=c.start&&sec<c.end);
  const vertical=p.vertical;
  // Entire 16:9 source is retained: 1080x607.5 on portrait, 1056x594 on landscape.
  const video={x:vertical?0:70,y:vertical?410:275,w:vertical?1080:1056,h:vertical?607.5:594};
  const musicGain=(f:number)=> {
    const s=f/fps;
    const envelope=interpolate(s,[0,1.5,p.durationSec-2,p.durationSec],[0,.055,.055,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
    // A deliberate quiet beat for the rejection/contrast, not a constant bed.
    const contrast=p.beats.find(b=>b.kind==='contrast');
    if(!contrast)return envelope;
    const duck=interpolate(s,[contrast.start-.2,contrast.start+.2,contrast.end-.35,contrast.end+.5],[1,.3,.3,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
    return envelope*duck;
  };
  return <AbsoluteFill style={{background:paper,color:ink,fontFamily:sans}}>
    <AbsoluteFill style={{opacity:.035,backgroundImage:'radial-gradient(#202622 0.7px,transparent 0.7px)',backgroundSize:'7px 7px'}}/>
    <div style={{position:'absolute',left:vertical?76:74,top:vertical?104:63,right:70,display:'flex',justifyContent:'space-between',fontSize:19,letterSpacing:3,color:muted}}>
      <span>GÓC NHÌN / THƯƠNG HIỆU</span><span>01</span>
    </div>
    <div style={{position:'absolute',left:vertical?74:70,top:vertical?179:119,right:65,fontFamily:serif,fontSize:vertical?83:68,lineHeight:1.06,letterSpacing:-1}}>
      {p.headline} <span style={{color:green}}>{p.emphasis}</span>
    </div>
    <div style={{position:'absolute',left:video.x,top:video.y,width:video.w,height:video.h,overflow:'hidden',background:'#111'}}>
      <OffthreadVideo src={staticFile(p.clip)} style={{width:'100%',height:'100%',objectFit:'contain'}}/>
      <div style={{position:'absolute',bottom:0,left:0,right:0,height:80,background:'linear-gradient(transparent,#0007)'}}/>
    </div>
    {beat&&<div style={{position:'absolute',left:vertical?76:1190,top:vertical?1190:270,fontSize:17,letterSpacing:3,color:muted}}>{beat.kicker}</div>}
    {p.beats.map(b=> {
      if(sec<b.start||sec>=b.end)return null;
      const opacity=Math.min(1,(sec-b.start)/.18,(b.end-sec)/.18);
      return <div key={b.start} style={{position:'absolute',left:vertical?80:1190,top:vertical?1250:330,opacity}}>
        <Art beat={b} t={sec-b.start} wide={!vertical}/>
      </div>;
    })}
    {caption&&<div style={{position:'absolute',left:vertical?75:92,top:vertical?1060:918,width:vertical?930:1010,fontSize:vertical?43:35,lineHeight:1.3,fontWeight:500,textAlign:'center',whiteSpace:'pre-line',opacity:Math.min(1,(sec-caption.start)/.065)}}>{caption.text}</div>}
    <div style={{position:'absolute',bottom:vertical?116:44,left:vertical?78:72,right:vertical?78:72,height:1,background:'#bfc2b6'}}/>
    <div style={{position:'absolute',bottom:vertical?75:18,left:vertical?78:72,fontSize:15,letterSpacing:1.3,color:muted}}>{p.sourceLabel}</div>
    {p.music&&<Audio src={staticFile(p.music)} volume={musicGain}/>}
    {p.sounds.map((s,i)=><Sequence key={i} from={Math.round(s.sec*fps)} durationInFrames={Math.min(30,Math.ceil((p.durationSec-s.sec)*fps))}><Audio src={staticFile(s.src)} volume={s.gain}/></Sequence>)}
  </AbsoluteFill>;
};
