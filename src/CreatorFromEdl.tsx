import React from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,Sequence,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import type {Edl} from './edl-types';
import type {Director} from './creator-schema';
import profiles from './creator-profiles.json';
import {useEditorialFonts} from './premium-kit/local-fonts';
import {cameraScale,smoothstep} from './camera-motion';
import {SFX_FILE_BY_CUE} from './components/Sfx';

const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const rise=(elapsed:number,duration:number)=>1-Math.pow(1-clamp(elapsed/duration),3);

export const CreatorFromEdl:React.FC<{edl:Edl}>=({edl})=>{
  useEditorialFonts(true);
  const frame=useCurrentFrame(),{fps,width,height}=useVideoConfig();
  const d=edl.director;
  if(!d)throw new Error('Creator layout requires an authored director plan');
  const theme=profiles[d.profile],ms=frame/fps*1000,portrait=height>width;
  const scale=width/(portrait?1080:1920),u=(v:number)=>v*scale;
  const scene=d.scenes.find(s=>ms>=s.startMs&&ms<s.endMs);
  const panel=scene&&scene.layout!=='speaker';
  const statement=scene?.layout==='statement';
  const cap=edl.tracks.captions.find(c=>ms>=c.startMs&&ms<c.endMs);
  const shot=panel&&!statement
    ?portrait?{left:0,top:0,width,height:u(970)}:{left:u(60),top:u(100),width:u(850),height:u(735)}
    :{left:0,top:0,width,height};
  const framing=d.framing;
  const captionSize=u(theme.captionSize*(portrait?1:.82));
  const capText=cap?.text??'',keyword=cap?.motion?.keyword;
  const k=keyword?capText.toLocaleLowerCase('vi').indexOf(keyword.toLocaleLowerCase('vi')):-1;
  const fadeIn=cap?.motion?.entry==='hold'?1:rise(ms-(cap?.startMs??0),theme.entryMs);
  const bounds=portrait?{left:u(80),top:u(1040),width:u(920),height:u(500)}:{left:u(1010),top:u(155),width:u(810),height:u(650)};
  const elapsed=scene?ms-scene.startMs:0;
  const enter=scene?.motion==='cut'?1:rise(elapsed,theme.entryMs);
  const headlineFont=theme.serif?'Playfair Editorial':'Manrope Editorial';
  const graphic:React.CSSProperties={position:'absolute',...bounds,opacity:enter,
    transform:`translateY(${u(scene?.motion==='lift'?(1-enter)*28:0)}px)`};
  return <AbsoluteFill style={{background:theme.background,color:'#FAFAF7',fontFamily:'Manrope Editorial'}}>
    <div style={{position:'absolute',...shot,overflow:'hidden',opacity:statement?.14:1}}>
      <OffthreadVideo src={staticFile(edl.source.clip)} volume={edl.music?.clipVolume??edl.source.volume}
        style={{width:'100%',height:'100%',objectFit:panel?'cover':framing.fit,objectPosition:`${framing.focusX}% ${framing.focusY}%`,transform:`scale(${cameraScale(ms,edl.tracks.effects)})`}}/>
    </div>
    {edl.tracks.broll.filter(b=>b.src).map((b,i)=>{
      const from=Math.round(b.startMs*fps/1000),duration=Math.round(b.endMs*fps/1000)-from;
      const fade=Math.min(b.fadeSec*1000,(b.endMs-b.startMs)/2);
      const opacity=fade?Math.min(smoothstep((ms-b.startMs)/fade),smoothstep((b.endMs-ms)/fade)):1;
      return <Sequence key={i} from={from} durationInFrames={Math.max(1,duration)}>
        <div style={{position:'absolute',...shot,opacity,overflow:'hidden'}}><OffthreadVideo muted src={staticFile(b.src!)} trimBefore={Math.round(b.offsetSec*fps)} style={{width:'100%',height:'100%',objectFit:framing.fit}}/></div>
      </Sequence>;
    })}
    {!panel&&<AbsoluteFill style={{background:'linear-gradient(0deg,rgba(0,0,0,.62),transparent 48%)',pointerEvents:'none'}}/>}
    {statement&&scene&&<div style={{position:'absolute',left:width*.09,top:height*.31,width:width*.82,opacity:enter,transform:`translateY(${u((1-enter)*24)}px)`}}>
      <div style={{width:u(70),height:u(5),background:theme.accent,marginBottom:u(36)}}/>
      <div style={{fontFamily:headlineFont,fontStyle:theme.serif?'italic':'normal',fontSize:u(theme.headlineSize),lineHeight:1.25,fontWeight:700,overflowWrap:'anywhere'}}>{scene.title}</div>
    </div>}
    {scene?.layout==='content-flood'&&<div style={{position:'absolute',top:portrait?u(1030):u(125),left:portrait?u(65):u(1030),width:portrait?u(950):u(760),height:portrait?u(760):u(680),overflow:'hidden'}}>
      <div style={{fontSize:u(63),fontWeight:900,color:theme.accent,letterSpacing:u(1),lineHeight:1.04}}>{scene.title}</div>
      <div style={{display:'grid',gridTemplateColumns:'repeat(7,1fr)',gap:u(14),marginTop:u(39),transform:`translateY(${u(-((elapsed/1000)*13)%32)}px)`}}>
        {Array.from({length:42},(_,i)=>{const appeared=clamp((elapsed-i*26)/500);const focus=i===23;return <div key={i} style={{height:u(90),borderRadius:u(7),background:focus?theme.accent:i%4===0?'#6E7278':'#35383D',opacity:(focus?.95:.52)*appeared,transform:`scale(${.6+.4*appeared})`,boxShadow:focus?`0 0 ${u(35)}px ${theme.accent}`:'none'}}/>})}
      </div>
    </div>}
    {scene?.layout==='salt-ocean'&&<div style={{position:'absolute',left:portrait?u(65):u(1010),top:portrait?u(1020):u(125),width:portrait?u(950):u(770),height:portrait?u(780):u(620),overflow:'hidden'}}>
      <div style={{fontSize:u(63),fontWeight:900,color:theme.accent,letterSpacing:u(1)}}>{scene.title}</div>
      <div style={{position:'absolute',left:0,right:0,bottom:0,height:u(480),borderRadius:'45% 45% 0 0',background:'linear-gradient(170deg,#267895,#10465F 46%,#071D32)',transform:`translateY(${u(16*Math.sin(elapsed/380))}px)`,boxShadow:`0 -${u(16)}px ${u(72)}px #2D9BBA88`}}/>
      {Array.from({length:19},(_,i)=>{const drop=clamp((elapsed-260-i*37)/800),x=(i*127)%890;return <div key={i} style={{position:'absolute',left:u(x),top:u(135+drop*340),width:u(i%3===0?17:11),height:u(i%3===0?17:11),borderRadius:'35%',background:'#FFF9D7',opacity:drop<.99?drop:clamp(1-(elapsed-260-i*37-800)/500),transform:`translateX(${u((i%2?1:-1)*drop*26)}px) rotate(${drop*70}deg)`}}/>})}
      <div style={{position:'absolute',bottom:u(95),left:u(34),fontSize:u(72),fontWeight:900,letterSpacing:u(-2),textShadow:'0 4px 16px #001'}}>BIỂN NỘI DUNG</div>
    </div>}
    {panel&&!statement&&scene&&!['content-flood','salt-ocean'].includes(scene.layout)&&<div style={graphic}>
      <div style={{fontSize:u(portrait?48:50),lineHeight:1.25,fontWeight:700,marginBottom:u(28),color:theme.accent}}>{scene.title}</div>
      {(scene.layout==='compare'||scene.layout==='steps')&&<div style={{display:'flex',flexDirection:scene.layout==='steps'?'column':'row',gap:u(18)}}>
        {scene.items?.map((item,i)=>{
          const visible=elapsed>=item.atMs,e=rise(elapsed-item.atMs,theme.entryMs);
          return <div key={i} style={{flex:1,background:theme.surface,borderRadius:u(d.profile==='hormozi'?4:18),borderLeft:`${u(4)}px solid ${theme.accent}`,
            padding:u(scene.layout==='steps'?22:28),opacity:visible?e:0,transform:`translateY(${u((1-e)*16)}px)`,minWidth:0,
            display:scene.layout==='steps'?'flex':'block',gap:u(22),alignItems:'center'}}>
            <div style={{color:theme.accent,fontSize:u(30),marginBottom:scene.layout==='steps'?0:u(20),fontWeight:700}}>{String(i+1).padStart(2,'0')}</div>
            <div style={{fontSize:u(scene.layout==='steps'?36:40),lineHeight:1.3,overflowWrap:'anywhere'}}>{item.text}</div>
          </div>;
        })}
      </div>}
      {scene.layout==='evidence'&&scene.image&&<Img src={staticFile(scene.image)} style={{width:'100%',height:u(portrait?370:475),objectFit:'contain',objectPosition:'left top'}}/>}
    </div>}
    {cap&&!statement&&<div style={{position:'absolute',left:width*.075,width:width*.85,bottom:height*(portrait?(panel?.485:.20):.075),textAlign:'center',fontSize:captionSize,lineHeight:1.13,
      textTransform:d.profile==='hormozi'?'uppercase':'none',fontWeight:850,textShadow:'0 5px 18px #000,0 2px 2px #000',opacity:fadeIn,transform:`translateY(${u((1-fadeIn)*16)}px)`,
      WebkitTextStroke:d.profile==='hormozi'?`${u(2)}px #111`:'none',paintOrder:'stroke fill'}}>
      {k<0?capText:<>{capText.slice(0,k)}<span style={{color:theme.accent}}>{capText.slice(k,k+keyword!.length)}</span>{capText.slice(k+keyword!.length)}</>}
    </div>}
    {edl.music&&<Audio src={staticFile(edl.music.src)} trimBefore={Math.round(edl.music.startSec*fps)} loop={edl.music.loop} loopVolumeCurveBehavior="extend" volume={f=>{
      const t=f/fps,now=t*1000;
      const cue=d.audioCues.find(c=>now>=c.startMs&&now<c.endMs);
      const mix=cue?1-(1-cue.gain)*Math.min(smoothstep((now-cue.startMs)/120),smoothstep((cue.endMs-now)/120)):1;
      const spoken=edl.tracks.captions.some(c=>now>=c.startMs-80&&now<c.endMs+140);
      // Smooth speech duck, not an audio loudness normalization claim.
      let duck=1;
      if(spoken){const distance=Math.min(...edl.tracks.captions.map(c=>now<c.startMs?c.startMs-now:now>c.endMs?now-c.endMs:0));duck=1-.45*clamp(1-distance/140);}
      const fade=edl.music!.fadeOutSec;
      return edl.music!.volume*mix*duck*clamp(t/.6)*(fade?clamp((edl.source.durationSec-t)/fade):1);
    }}/>} 
    {edl.tracks.sfx.map((s,i)=><Sequence key={`sfx-${i}`} from={Math.max(0,Math.round((s.startMs-s.preRollMs)*fps/1000))}><Audio src={staticFile(SFX_FILE_BY_CUE[s.sound])} volume={s.volume}/></Sequence>)}
  </AbsoluteFill>;
};
