import React from 'react';
import type {Keyword} from '../motion-kit/TextMotion';
import type {TextPreset} from '../motion-kit/catalog';
import {premiumSets, type PremiumSet} from './theme';
import {useEditorialFonts} from './local-fonts';
import pureEditSystem from '../pure-edit-system.json';

export const clamp=(n:number)=>Math.max(0,Math.min(1,n));
export const settle=(n:number)=>1-Math.pow(1-clamp(n),4);

// No spring overshoot or word-size changes. Accent geometry does not move the baseline.
export const PremiumText:React.FC<{
  text:string; elapsed:number; duration:number; set:PremiumSet;
  keyword?:Keyword; preset?:TextPreset; style?:React.CSSProperties;
}> = ({text,elapsed,duration,set,keyword,preset,style})=>{
  const theme=premiumSets[set];
  useEditorialFonts(set==='editorial-c');
  const entry=Math.min(pureEditSystem.motion.entryMs/1000,duration*.28);
  const p=settle(elapsed/Math.max(.01,entry));
  const mode=preset??theme.entry;
  const opacity=mode==='hold'?1:clamp(elapsed/Math.min(.10,entry))*clamp((duration-elapsed)/(pureEditSystem.motion.exitMs/1000));
  const at=keyword?.text?text.toLocaleLowerCase('vi').indexOf(keyword.text.toLocaleLowerCase('vi')):-1;
  const head=at<0?text:text.slice(0,at), word=at<0?'':text.slice(at,at+keyword!.text.length),tail=at<0?'':text.slice(at+keyword!.text.length);
  const reveal=mode==='quiet-reveal'||mode==='mask-up'||mode==='wipe';
  const soft=mode==='soft-focus'||mode==='blur-in';
  const draw=settle((elapsed-.08)/Math.min(.32,duration*.3));
  return <div style={{fontFamily:theme.font,color:theme.foreground,fontWeight:theme.weight,lineHeight:1.5,letterSpacing:'-.022em',textAlign:'center',...style}}>
    <div style={{padding:'.14em .18em .22em',opacity,transform:mode==='hold'?'none':`translateY(${(reveal?10:8)*(1-p)}px)`,
      filter:soft?`blur(${2*(1-p)}px)`:undefined,clipPath:reveal?`inset(${(1-p)*100}% -2% -10% -2%)`:undefined}}>
      {head}{word&&<span style={{display:'inline-block',position:'relative',whiteSpace:'nowrap',color:theme.accent,fontWeight:set==='editorial-c'?(keyword?.strong?650:700):set==='mono'?700:600,
        fontFamily:set==='editorial-c'&&keyword?.strong?'Playfair Editorial':undefined,fontStyle:set==='editorial-c'&&keyword?.strong?'italic':undefined}}>
        {word}{(keyword?.strong||keyword?.style==='underline')&&<span style={{position:'absolute',left:0,right:0,bottom:'.05em',height:2,background:theme.accent,opacity:.6,transform:`scaleX(${draw})`,transformOrigin:'left'}}/>}
      </span>}{tail}
    </div>
  </div>;
};
