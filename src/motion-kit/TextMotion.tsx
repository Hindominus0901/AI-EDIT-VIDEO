import React from 'react';
import {interpolate} from 'remotion';
import type {EmphasisPreset, TextPreset} from './catalog';
import pureEditSystem from '../pure-edit-system.json';

export type Keyword = {text:string; style?:EmphasisPreset; strong?:boolean};
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const ease=(n:number)=>1-Math.pow(1-clamp(n),3);

// Pure frame-time animation: the same component powers the catalog and exports.
// Entry takes <=35% of a cue, leaving most of the cue fully readable.
export const MotionText:React.FC<{
  text:string; elapsed:number; duration:number; preset?:TextPreset;
  keyword?:Keyword; accent?:string; style?:React.CSSProperties; keywordStyle?:React.CSSProperties;
  visibleWords?:number; activeWord?:number; activeProgress?:number;
}> = ({text,elapsed,duration,preset='rise',keyword,accent='#F3CE83',style,keywordStyle,
  visibleWords,activeWord,activeProgress=1})=>{
  const entry=Math.min(pureEditSystem.motion.entryMs/1000,Math.max(.01,duration*.30));
  const p=ease(elapsed/entry);
  const fade=clamp(elapsed/Math.min(.075,entry))*clamp((duration-elapsed)/.05);
  const index=keyword?.text?text.toLocaleLowerCase('vi').indexOf(keyword.text.toLocaleLowerCase('vi')):-1;
  const chunks:{text:string;key:boolean}[]=index<0?[{text,key:false}]:[
    {text:text.slice(0,index),key:false},
    {text:text.slice(index,index+keyword!.text.length),key:true},
    {text:text.slice(index+keyword!.text.length),key:false},
  ];
  const units=chunks.flatMap(c=>c.text.split(/(\s+)/).filter(Boolean).map(t=>({text:t,key:c.key})));
  const count=units.filter(u=>u.text.trim()).length;
  let word=0;
  const draw=ease((elapsed-entry*.25)/(entry*.95));
  const motion:React.CSSProperties={opacity:preset==='hold'?1:fade};
  if(preset==='rise') motion.transform=`translateY(${28*(1-p)}px)`;
  if(preset==='mask-up') motion.clipPath=`inset(${(1-p)*100}% -5% -10% -5%)`;
  if(preset==='soft-pop') motion.transform=`scale(${interpolate(clamp(elapsed/entry),[0,.62,1],[.82,1.045,1])})`;
  if(preset==='slide-left') motion.transform=`translateX(${24*(1-p)}px)`;
  if(preset==='blur-in') {motion.filter=`blur(${5*(1-p)}px)`;motion.transform=`translateY(${7*(1-p)}px)`;}
  if(preset==='wipe') motion.clipPath=`inset(-10% ${(1-p)*105}% -10% -5%)`;
  if(preset==='tracking') motion.letterSpacing=`${.065*(1-p)}em`;
  if(preset==='silk-rise')motion.transform=`translateY(${8*(1-p)}px)`;
  if(preset==='quiet-reveal')motion.clipPath=`inset(${(1-p)*100}% -2% -10% -2%)`;
  if(preset==='soft-focus'){motion.filter=`blur(${2*(1-p)}px)`;motion.transform=`translateY(${6*(1-p)}px)`;}
  return <div style={{lineHeight:1.45,fontWeight:600,textAlign:'center',...style}}>
    <div style={{padding:'.15em .2em',...motion}}>
      {units.map((u,i)=>{
        const whitespace=!u.text.trim();
        const spread=Math.min(.09,entry*.28);
        const wordIndex=whitespace?-1:word++;
        const offset=whitespace?0:(wordIndex/Math.max(1,count-1))*spread;
        const wp=ease((elapsed-offset)/Math.max(.01,entry-spread));
        const karaoke=visibleWords!==undefined&&!whitespace;
        const revealed=!karaoke||wordIndex<visibleWords!;
        const active=karaoke&&wordIndex===activeWord;
        const kp=clamp(activeProgress);
        const unit:React.CSSProperties={display:'inline-block',whiteSpace:'pre',verticalAlign:'baseline',
          opacity:revealed?(active?kp:1):0,
          transform:active?`translateY(${10*(1-kp)}px) scale(${.96+.08*kp})`:
            (preset==='word-rise'&&!whitespace?`translateY(${32*(1-wp)}px) scale(${.94+.06*wp})`:undefined),
          color:active&&!u.key?accent:undefined,
          textShadow:active?`0 0 24px ${accent}66`:undefined};
        if(!u.key)return <span key={i} style={unit}>{u.text}</span>;
        const mark=keyword?.style??'color';
        return <span key={i} style={{...unit,position:'relative',isolation:'isolate',color:mark==='marker'?'#fff':accent,fontWeight:700,fontSize:keyword?.strong?'1.16em':undefined,paddingInline:mark==='ring'?'.12em':undefined,marginInline:mark==='ring'?'.04em':undefined,...keywordStyle}}>
          {mark==='marker'&&<span style={{position:'absolute',inset:'15% -.07em 8%',zIndex:-1,background:accent,opacity:.28,borderRadius:3,transform:`scaleX(${draw})`,transformOrigin:'left'}}/>}
          {u.text}
          {mark==='underline'&&<svg viewBox="0 0 200 14" preserveAspectRatio="none" style={{position:'absolute',width:'104%',height:'.18em',left:'-2%',bottom:'-.06em',overflow:'visible'}}><path d="M2 9 Q84 1 197 7" fill="none" stroke={accent} strokeWidth="4.5" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1-draw}/></svg>}
          {mark==='ring'&&<svg viewBox="0 0 200 70" preserveAspectRatio="none" style={{position:'absolute',left:'-2%',top:'1%',width:'104%',height:'105%',overflow:'visible'}}><path d="M172 10C97-6 6 5 4 34C1 67 185 78 196 40C201 18 156 5 114 5" fill="none" stroke={accent} strokeWidth="1.8" pathLength="1" strokeDasharray="1" strokeDashoffset={1-draw}/></svg>}
        </span>;
      })}
    </div>
  </div>;
};
