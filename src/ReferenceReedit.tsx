import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/BeVietnamPro';

const {fontFamily} = loadFont('normal', {weights:['600','700','800'], subsets:['latin','vietnamese']});
const clamp = (v:number) => Math.max(0, Math.min(1,v));
const ease = (v:number) => 1 - Math.pow(1-clamp(v),3);
const accent = '#F0D5A3';
export type ReferenceCaption = {
  startMs:number; endMs:number; text:string;
  lines?:string[]; keyword?:string; emphasis?:boolean; entry?:'rise'|'resolve';
};
export type ReferenceCard = {src:string; start:number; end:number; slot:'center'|'left'|'right';};
export type ReferenceReeditProps = {
  clip:string; durationSec:number; captions:ReferenceCaption[];
  originalPicture?:{src:string;segments:{from:number;duration:number;trimBefore:number}[];tailFrame:string;tailFrom:number};
  cards:ReferenceCard[];
  framing:{start:number; end:number; from:number; to:number}[];
  music:{src:string; volume:number; startSec:number};
  sounds:{sec:number; src:string; gain:number}[];
};

const Caption:React.FC<{cue:ReferenceCaption;t:number}> = ({cue,t}) => {
  const elapsed=t-cue.startMs/1000, duration=(cue.endMs-cue.startMs)/1000;
  const progress=ease(elapsed/Math.min(.27,duration*.23));
  const alpha=clamp(elapsed/.07)*clamp((duration-elapsed)/.055);
  const lines=cue.lines??[cue.text];
  const draw=ease((elapsed-.15)/.34);
  return <div style={{position:'absolute',left:64,top:1162,width:952,textAlign:'center',color:'#FAF8F4',
    fontFamily,fontSize:61,fontWeight:700,lineHeight:1.23,letterSpacing:'-.047em',
    textShadow:'0 3px 5px #000b, 0 6px 22px #0007',opacity:alpha,
    transform:`translateY(${12*(1-progress)}px)`,
    filter:cue.entry==='resolve'?`blur(${3.5*(1-progress)}px)`:undefined}}>
    {lines.map((line,i)=>{
      const index=cue.keyword?line.toLocaleLowerCase('vi').indexOf(cue.keyword.toLocaleLowerCase('vi')):-1;
      const before=index<0?line:line.slice(0,index),word=index<0?'':line.slice(index,index+cue.keyword!.length),after=index<0?'':line.slice(index+cue.keyword!.length);
      const larger=Boolean(cue.emphasis&&i===lines.length-1);
      // The emphasized line has its own brief reveal; its final baseline stays stable.
      const stage=larger&&lines.length>1?ease((elapsed-.10)/.24):1;
      return <div key={i} style={{padding:'8px 0 5px',fontSize:larger?84:61,fontWeight:larger?800:700,
        opacity:stage,transform:`translateY(${larger?8*(1-stage):0}px)`,whiteSpace:'nowrap'}}>
        {before}{word&&<span style={{position:'relative',color:accent,display:'inline-block'}}>{word}
          {cue.emphasis&&<span style={{position:'absolute',left:2,right:2,bottom:-5,height:3,borderRadius:3,background:accent,
            transform:`scaleX(${draw})`,transformOrigin:'left'}}/>}
        </span>}{after}
      </div>;
    })}
  </div>;
};

const Illustration:React.FC<{cue:ReferenceCard;t:number}> = ({cue,t}) => {
  const elapsed=t-cue.start,remaining=cue.end-t;
  const entry=ease(elapsed/.36),exit=clamp(remaining/.18);
  const width=cue.slot==='center'?370:310;
  const left=cue.slot==='center'?(1080-width)/2:cue.slot==='left'?218:552;
  return <div style={{position:'absolute',left,top:1356,width,height:cue.slot==='center'?274:256,
    overflow:'hidden',borderRadius:9,background:'#F1EEE6',boxShadow:'0 12px 32px #0005',
    opacity:clamp(elapsed/.17)*exit,transform:`translateY(${22*(1-entry)+6*(1-exit)}px) scale(${.975+.025*entry})`}}>
    <Img src={staticFile(cue.src)} style={{width:'100%',height:'100%',objectFit:'contain'}}/>
  </div>;
};

// Project-specific revision; existing approved compositions and EDLs are untouched.
export const ReferenceReedit:React.FC<ReferenceReeditProps> = (p) => {
  const frame=useCurrentFrame(),{fps}=useVideoConfig(),t=frame/fps;
  const movement=p.framing.find(x=>t>=x.start&&t<x.end)??p.framing[p.framing.length-1];
  const zoom=movement?interpolate(t,[movement.start,movement.end],[movement.from,movement.to],
    {extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:ease}):1;
  const cue=p.captions.find(x=>t>=x.startMs/1000&&t<x.endMs/1000);
  return <AbsoluteFill style={{backgroundColor:'#0A0A09',fontFamily}}>
    <div style={{position:'absolute',left:0,top:80,width:1080,height:1230,overflow:'hidden'}}>
      {p.originalPicture?<>
        {p.originalPicture.segments.map((segment,i)=><Sequence key={i} from={segment.from} durationInFrames={segment.duration} layout="none">
          <OffthreadVideo src={staticFile(p.originalPicture!.src)} muted trimBefore={segment.trimBefore}
            style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'50% 50%',transform:`scale(${zoom})`,transformOrigin:'50% 47%'}}/>
        </Sequence>)}
        <Sequence from={p.originalPicture.tailFrom} layout="none"><Img src={staticFile(p.originalPicture.tailFrame)}
          style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'50% 50%',transform:`scale(${zoom})`,transformOrigin:'50% 47%'}}/></Sequence>
      </>:<OffthreadVideo src={staticFile(p.clip)} muted
        style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'50% 50%',
          transform:`scale(${zoom})`,transformOrigin:'50% 47%'}}/>}
      <AbsoluteFill style={{background:'linear-gradient(180deg,#0A0A09 0%,transparent 9%,transparent 72%,#0A0A0920 81%,#0A0A09 100%)'}}/>
    </div>
    {cue&&<Caption cue={cue} t={t}/>}
    {p.cards.filter(x=>t>=x.start&&t<x.end).map((c,i)=><Illustration key={`${c.src}-${i}`} cue={c} t={t}/>)}
    <Audio src={staticFile(p.clip)} volume={1}/>
    {p.music.src&&<Audio src={staticFile(p.music.src)} trimBefore={Math.round(p.music.startSec*fps)}
      volume={f=>p.music.volume*clamp(f/fps/1.15)*clamp((p.durationSec-f/fps)/1.45)}/>}
    {p.sounds.map((s,i)=><Sequence key={i} from={Math.round(s.sec*fps)}>
      <Audio src={staticFile(s.src)} volume={s.gain}/>
    </Sequence>)}
  </AbsoluteFill>;
};

export const referenceReeditDefaults:ReferenceReeditProps = {
  clip:'raw/personal-brand-test/continuation.mp4',durationSec:26.7,captions:[],cards:[],
  framing:[{start:0,end:26.7,from:1,to:1}],music:{src:'',volume:0,startSec:0},sounds:[],
};
