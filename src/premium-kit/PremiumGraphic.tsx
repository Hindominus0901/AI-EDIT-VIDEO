import React from 'react';
import {Img,staticFile} from 'remotion';
import {LineAsset, type MotionGraphicCue} from '../motion-kit/GraphicMotion';
import {premiumSets, type PremiumSet} from './theme';
import {clamp,settle} from './PremiumText';
import pureEditSystem from '../pure-edit-system.json';

// Concept drawings are illustrations, never quantitative charts or invented evidence.
export const PremiumGraphic:React.FC<{cue:MotionGraphicCue;elapsed:number;duration:number;set:PremiumSet;compact?:boolean;style?:React.CSSProperties}>=({cue,elapsed,duration,set,compact=false,style})=>{
  const theme=premiumSets[set],entry=Math.min(pureEditSystem.motion.entryMs/1000+.06,duration*.25),p=settle(elapsed/entry);
  const alpha=clamp(elapsed/.10)*clamp((duration-elapsed)/(pureEditSystem.motion.exitMs/1000));
  const photo=(i:number,position='50% 50%')=>cue.images?.[i]?<Img src={staticFile(cue.images[i])} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:position,filter:set==='mono'?'grayscale(1)':undefined}}/>:null;
  const cell:React.CSSProperties={position:'absolute',overflow:'hidden',borderRadius:theme.radius};
  const isPhoto=cue.kind.startsWith('photo-');
  const viewBox=compact?(cue.asset==='time'||cue.asset==='proof'?'100 20 280 200':cue.asset==='chat'?'60 35 350 175':cue.asset==='compass'||cue.asset==='target'?'38 38 402 160':'0 0 480 240'):'0 0 480 240';
  return <div style={{position:'relative',...style,opacity:alpha,transform:`translateY(${10*(1-p)}px)`}}>
    {isPhoto&&(cue.kind==='photo-diptych'||cue.kind==='photo-collage')?[0,1].map(i=>{
      const q=settle((elapsed-i*.07)/entry);
      return <div key={i} style={{...cell,left:i?'51.5%':0,top:0,width:'48.5%',height:'100%',clipPath:`inset(${(1-q)*100}% 0 0 0 round ${theme.radius}px)`}}>{photo(i)}</div>;
    }):isPhoto&&cue.kind==='photo-detail'?<>
      <div style={{...cell,inset:'0 19% 9% 0',clipPath:`inset(0 ${(1-p)*100}% 0 0)`}}>{photo(0)}</div>
      <div style={{...cell,right:0,bottom:0,width:'35%',height:'63%',border:`5px solid ${theme.background}`,transform:`translateX(${12*(1-p)}px)`}}>
        <div style={{width:'100%',height:'100%',transform:'scale(1.65)',transformOrigin:'45% 40%'}}>{photo(0)}</div>
      </div>
    </>:isPhoto?<div style={{...cell,...(cue.kind==='photo-circle'?{left:'50%',top:0,height:'100%',aspectRatio:'1',maxWidth:'100%',transform:'translateX(-50%)'}:{inset:0}),padding:cue.kind==='photo-mat'?12:0,background:theme.surface,borderRadius:cue.kind==='photo-circle'?'50%':theme.radius,clipPath:`inset(${(1-p)*9}% ${(1-p)*46}% round ${theme.radius}px)`}}>
      <div style={{width:'100%',height:'100%',overflow:'hidden',borderRadius:cue.kind==='photo-circle'?'50%':Math.max(0,theme.radius-6)}}>{photo(0)}</div>
    </div>:<svg viewBox={viewBox} width="100%" height="100%" fill="none" strokeWidth={compact?1.7:1} strokeLinecap="round" strokeLinejoin="round">
      {cue.asset==='compass'||cue.asset==='target'?<>
        {[52,183,314].map((x,i)=><g key={x} opacity={settle((elapsed-i*.06)/entry)} transform={`translate(0 ${12*(1-settle((elapsed-i*.06)/entry))})`}>
          <rect x={x} y="53" width="114" height="132" rx={theme.radius} fill={theme.surface} stroke={i===2?theme.accent:theme.line} strokeWidth={i===2?1.8:compact?1.7:1}/>
          {i<2?<><path d={`M${x+25} 88h64 M${x+25} 106h43`} stroke={theme.line} strokeWidth="3"/><circle cx={x+57} cy="148" r="10" fill={theme.line}/></>:<path d={`M${x+41} 119h32 M${x+57} 103v32`} stroke={theme.accent} strokeWidth="2.5"/>}
        </g>)}
      </>:cue.asset==='time'||cue.asset==='proof'?<>
        {[0,1,2].map(i=><rect key={i} x={114+i*21} y={34+i*23} width="210" height="120" rx={theme.radius} fill={i===2?theme.surface:theme.background} stroke={i===2?theme.accent:theme.line} opacity={settle((elapsed-i*.06)/entry)}/>)}
        <path d="M183 120h107 M183 138h76" stroke={theme.line} strokeWidth="3"/>
        <circle cx="331" cy="172" r="24" fill={theme.background} stroke={theme.accent}/>
        <path d="m321 171 7 7 13-14" stroke={theme.accent} strokeWidth="2" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p}/>
      </>:cue.asset==='chat'?<>
        <rect x="77" y="48" width="224" height="145" rx={theme.radius} fill={theme.surface} stroke={theme.line}/>
        <path d="M104 81h138 M104 103h92 M104 125h112" stroke={theme.line} strokeWidth="3"/>
        <path d="M267 92h110q18 0 18 18v46q0 18-18 18h-65l-26 21v-21h-19q-18 0-18-18v-46q0-18 18-18Z" fill={theme.background} stroke={theme.accent} opacity={settle((elapsed-.1)/entry)}/>
        <path d="m302 132 12 12 23-26" stroke={theme.accent} strokeWidth="2.5" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p}/>
      </>:<foreignObject x="130" y="20" width="220" height="200"><LineAsset asset={cue.asset??'idea'} progress={p} color={theme.accent}/></foreignObject>}
    </svg>}
  </div>;
};
