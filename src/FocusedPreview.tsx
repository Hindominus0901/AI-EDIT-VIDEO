import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Inter';
import {loadFont as loadVietnamese} from '@remotion/google-fonts/BeVietnamPro';
import {PremiumText} from './premium-kit/PremiumText';
import {PremiumGraphic} from './premium-kit/PremiumGraphic';
import {premiumSets,type PremiumSet} from './premium-kit/theme';
import type {EditorialProps} from './EditorialPreview';
import {MotionText} from './motion-kit/TextMotion';
import {MotionGraphic, type MotionGraphicCue} from './motion-kit/GraphicMotion';
import type {EmphasisPreset, TextPreset} from './motion-kit/catalog';
import {cameraScale,smoothstep,type CameraCue} from './camera-motion';

const {fontFamily}=loadFont('normal',{weights:['500','600','700'],subsets:['latin','vietnamese']});
loadVietnamese('normal',{weights:['500','600'],subsets:['latin','vietnamese']});

export type FocusedCaption = EditorialProps['captions'][number] & {
  emphasis?: {text:string; style:'color'|'strong'};
  entry?:TextPreset;
  mark?:EmphasisPreset;
};
export type FocusedProps = Omit<EditorialProps,'captions'> & {
  captions:FocusedCaption[];
  captionMotion?:'none'|'phrase'|'library';
  defaultEntry?:TextPreset;
  motionGraphics?:MotionGraphicCue[];
  soundEffects?:boolean;
  sourceSize?:{width:number;height:number};
  voiceVolume?:number;
  musicVolume?:number;
  musicStartSec?:number;
  musicLoop?:boolean;
  musicFadeOutSec?:number;
  premiumSet?:PremiumSet;
  cameraCues?:CameraCue[];
  broll?:{startMs:number;endMs:number;src?:string;offsetSec?:number;fadeSec?:number}[];
};

const PhraseCaption:React.FC<{caption:FocusedCaption;time:number;portrait:boolean}> = ({caption,time,portrait})=>{
  const elapsed=time-caption.start;
  const duration=caption.end-caption.start;
  const entry=Math.min(.3,duration*.3);
  const scale=interpolate(elapsed,[0,entry*.65,entry],[.93,1.015,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const y=interpolate(elapsed,[0,entry],[18,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:x=>1-Math.pow(1-x,3)});
  const opacity=Math.min(1,elapsed/.07,Math.max(0,(duration-elapsed)/.055));
  const emphasis=caption.emphasis;
  const index=emphasis?caption.text.toLocaleLowerCase('vi').indexOf(emphasis.text.toLocaleLowerCase('vi')):-1;
  const before=index<0?caption.text:caption.text.slice(0,index);
  const keyword=index<0?'':caption.text.slice(index,index+emphasis!.text.length);
  const after=index<0?'':caption.text.slice(index+emphasis!.text.length);
  const strong=emphasis?.style==='strong';
  const underline=interpolate(elapsed,[.13,.36],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <div style={{position:'absolute',left:portrait?76:390,top:portrait?1244:927,width:portrait?928:1140,
    fontSize:portrait?54:44,lineHeight:1.4,fontWeight:600,textAlign:'center',whiteSpace:'pre-wrap',
    textShadow:'0 2px 6px #0008',opacity,transform:`translateY(${y}px) scale(${scale})`,transformOrigin:'50% 50%',padding:'8px 0'}}>
    {before}{keyword&&<span style={{position:'relative',display:'inline-block',whiteSpace:'nowrap',color:'#F3CE83',fontWeight:700,fontSize:strong?'1.12em':'1em'}}>
      {keyword}
      {strong&&<span style={{position:'absolute',left:0,right:0,bottom:1,height:3,borderRadius:2,background:'#F3CE83',transform:`scaleX(${underline})`,transformOrigin:'left',opacity:.75}}/>}
    </span>}{after}
  </div>;
};

// A quiet alternative: one caption, and at most one supporting image.
// Portrait uses a native-size 960x720 crop of the 1280x720 source, retaining
// 75% of its width. The speaker is not enlarged by the old 2.67x cover crop.
export const FocusedPreview:React.FC<FocusedProps>=(p)=>{
  const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();const t=frame/fps;
  const cap=p.captions.find(c=>t>=c.start&&t<c.end);
  // Authored graphics take over the image lane. Never stack a legacy photo on them.
  const graphic=p.motionGraphics?.find(g=>t>=g.start&&t<g.end);
  const photo=p.motionGraphics?undefined:p.beats.find(b=>b.image&&t>=b.start&&t<Math.min(b.end,b.start+4.2));
  const portrait=p.vertical;
  const premium=p.premiumSet?premiumSets[p.premiumSet]:undefined;
  const editorial=p.premiumSet==='editorial-c';
  const zoom=cameraScale(t*1000,p.cameraCues??[]);
  let video=portrait?{x:60,y:475,w:960,h:720}:{x:320,y:180,w:1280,h:720};
  let fit:'cover'|'contain'='cover';
  if(p.sourceSize){
    const {width:sw,height:sh}=p.sourceSize;
    if(portrait&&sh>sw){
      const scale=Math.min(1,900/sw,1110/sh);
      const w=sw*scale,h=sh*scale;
      video={x:(width-w)/2,y:1200-h,w,h};fit='contain';
    }else if(!portrait){
      const scale=Math.min(1,1280/sw,720/sh);
      const w=sw*scale,h=sh*scale;
      video={x:(width-w)/2,y:900-h,w,h};fit='contain';
    }else if(sw<960||sh<720){
      video={x:(width-Math.min(960,sw))/2,y:1195-Math.min(720,sh),w:Math.min(960,sw),h:Math.min(720,sh)};
    }
  }
  // Keep native-resolution media and a stable reading lane across cues.
  if(premium&&portrait)video.y-=75;
  if(editorial&&portrait){video={x:0,y:0,w:width,h:height};fit='cover';}
  const captionStyle:React.CSSProperties={position:'absolute',left:portrait?76:340,
    top:portrait?(editorial?1460:1170):920,width:portrait?928:1240,fontSize:portrait?(editorial?74:52):52,
    ...(editorial?{textShadow:'0 3px 7px #180917cc',WebkitTextStroke:'1px #261521',paintOrder:'stroke fill',lineHeight:1.32}:{} )};
  const musicFade=Math.min(p.musicFadeOutSec??2,p.durationSec*.3);
  const musicIn=Math.min(1.5,p.durationSec*.3);
  const imageOpacity=photo?interpolate(t,[photo.start,photo.start+.35,Math.min(photo.end,photo.start+4.2)-.35,Math.min(photo.end,photo.start+4.2)],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}):0;
  return <AbsoluteFill style={{backgroundColor:premium?.background??'#080b09',color:premium?.foreground??'#fff',fontFamily}}>
    <div style={{position:'absolute',left:video.x,top:video.y,width:video.w,height:video.h,overflow:'hidden',borderRadius:premium?.radius??0}}>
      <OffthreadVideo src={staticFile(p.clip)} volume={p.voiceVolume??1} style={{width:'100%',height:'100%',objectFit:fit,objectPosition:'50% 50%',transform:`scale(${zoom})`}}/>
    </div>
    {(p.broll??[]).filter(b=>b.src).map((b,i)=>{
      const from=Math.round(b.startMs*fps/1000),duration=Math.max(1,Math.round(b.endMs*fps/1000)-from);
      const local=t-b.startMs/1000,total=(b.endMs-b.startMs)/1000,fade=Math.min(b.fadeSec??.23,total/2);
      const opacity=fade>0?Math.min(smoothstep(local/fade),smoothstep((total-local)/fade)):1;
      const bounds=portrait?video:{x:320,y:180,w:1280,h:720};
      return <Sequence key={`broll-${i}`} from={from} durationInFrames={duration}>
        <div style={{position:'absolute',left:bounds.x,top:bounds.y,width:bounds.w,height:bounds.h,overflow:'hidden',opacity}}>
          <OffthreadVideo src={staticFile(b.src!)} muted trimBefore={Math.round((b.offsetSec??0)*fps)} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
        </div>
      </Sequence>;
    })}
    {cap&&(p.premiumSet?<PremiumText text={cap.text} elapsed={t-cap.start} duration={cap.end-cap.start} set={p.premiumSet}
      preset={cap.entry} keyword={cap.emphasis?{text:cap.emphasis.text,style:cap.mark,strong:cap.emphasis.style==='strong'}:undefined} style={captionStyle}/>
      :p.captionMotion==='library'?<MotionText text={cap.text} elapsed={t-cap.start} duration={cap.end-cap.start}
      preset={cap.entry??p.defaultEntry??'rise'} keyword={cap.emphasis?{text:cap.emphasis.text,style:cap.mark??(cap.emphasis.style==='strong'?'underline':'color'),strong:cap.emphasis.style==='strong'}:undefined}
      style={{position:'absolute',left:portrait?76:390,top:portrait?1244:927,width:portrait?928:1140,fontSize:portrait?54:44,textShadow:'0 2px 6px #0008'}}/>
      :p.captionMotion==='phrase'?<PhraseCaption caption={cap} time={t} portrait={portrait}/>:<div style={{position:'absolute',left:portrait?76:390,top:portrait?1244:927,width:portrait?928:1140,fontSize:portrait?44:38,lineHeight:1.3,fontWeight:500,textAlign:'center',whiteSpace:'pre-line',textShadow:'0 2px 6px #0008'}}>{cap.text}</div>)}
    {photo&&<div style={{position:'absolute',left:portrait?(width-400)/2:1350,top:portrait?1420:605,width:portrait?400:240,height:portrait?272:200,opacity:imageOpacity,overflow:'hidden',borderRadius:8,boxShadow:'0 6px 25px #0005'}}>
      <Img src={staticFile(photo.image!)} style={{width:'100%',height:'100%',objectFit:'cover',filter:'saturate(.82)'}}/>
    </div>}
    {graphic&&(p.premiumSet&&(graphic.kind.startsWith('photo-')||graphic.kind==='icon')?<PremiumGraphic cue={graphic} elapsed={t-graphic.start} duration={graphic.end-graphic.start} set={p.premiumSet} compact={!portrait}
      style={{position:'absolute',left:portrait?270:1620,top:portrait?(editorial?1080:1340):430,width:portrait?540:270,height:portrait?285:225}}/>
      :<MotionGraphic cue={graphic} elapsed={t-graphic.start} duration={graphic.end-graphic.start}
      style={{position:'absolute',left:portrait?330:1620,top:portrait?(editorial?1100:1420):468,width:portrait?420:260,height:portrait?260:220}}/>)}
    {p.music&&<Audio src={staticFile(p.music)} loop={p.musicLoop??true} loopVolumeCurveBehavior="extend" trimBefore={Math.round((p.musicStartSec??0)*fps)} volume={f=>{
      const sec=f/fps;
      return (p.musicVolume??.035)*Math.min(1,sec/musicIn)* (musicFade>0?Math.min(1,Math.max(0,(p.durationSec-sec)/musicFade)):1);
    }}/>} 
    {p.soundEffects&&p.sounds.map((s,i)=><Sequence key={i} from={Math.round(s.sec*fps)}><Audio src={staticFile(s.src)} volume={s.gain}/></Sequence>)}
  </AbsoluteFill>;
};
