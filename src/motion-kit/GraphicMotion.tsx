import React from 'react';
import {Img, staticFile} from 'remotion';
import assets from './assets.json';
import type {GraphicPreset} from './catalog';
import pureEditSystem from '../pure-edit-system.json';

export type AssetId=keyof typeof assets;
export type MotionGraphicCue={
  start:number;end:number;kind:GraphicPreset;
  images?:string[];asset?:AssetId;accent?:string;text?:string;
};
const ease=(n:number)=>1-Math.pow(1-Math.max(0,Math.min(1,n)),3);
export const LineAsset:React.FC<{asset:AssetId;progress:number;color?:string}> = ({asset,progress,color='#F3CE83'})=><svg viewBox="0 0 96 96" width="100%" height="100%" fill="none" stroke={color} strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
  {assets[asset].paths.map((d,i)=><path key={i} d={d} pathLength="1" strokeDasharray="1" strokeDashoffset={1-ease((progress-i*.1)/.7)}/>)}
</svg>;

// The caller owns the safe rectangle. Graphics never add their own captions.
export const MotionGraphic:React.FC<{
  cue:MotionGraphicCue;elapsed:number;duration:number;style?:React.CSSProperties;
}> = ({cue,elapsed,duration,style})=>{
  const entry=Math.min(pureEditSystem.motion.entryMs/1000+.06,duration*.25);
  const p=ease(elapsed/Math.max(.01,entry));
  const opacity=Math.min(Math.max(0,elapsed/.08),1,Math.max(0,(duration-elapsed)/.14));
  const accent=cue.accent??'#F3CE83';
  const label=cue.text?.trim()||'Điểm chính';
  const photo=(i:number)=>cue.images?.[i]?<Img src={staticFile(cue.images[i])} style={{width:'100%',height:'100%',objectFit:'cover',filter:'saturate(.85)'}}/>:null;
  const isPhoto=cue.kind.startsWith('photo');
  return <div style={{width:'100%',height:'100%',position:'relative',...style,opacity}}>
    {cue.kind==='photo-mat'&&<div style={{position:'absolute',inset:0,padding:10,background:'#eae7dd',overflow:'hidden',clipPath:`inset(0 ${(1-p)*100}% 0 0)`}}>{photo(0)}</div>}
    {cue.kind==='photo-diptych'&&[0,1].map(i=><div key={i} style={{position:'absolute',left:i?'51.5%':0,top:0,width:'48.5%',height:'100%',overflow:'hidden',clipPath:`inset(${(1-ease((elapsed-i*.07)/entry))*100}% 0 0 0)`}}>{photo(i)}</div>)}
    {cue.kind==='photo-detail'&&<><div style={{position:'absolute',inset:'0 19% 9% 0',overflow:'hidden'}}>{photo(0)}</div><div style={{position:'absolute',right:0,bottom:0,width:'35%',height:'63%',overflow:'hidden',border:'4px solid #080b09'}}><div style={{height:'100%',transform:'scale(1.65)',transformOrigin:'45% 40%'}}>{photo(0)}</div></div></>}
    {cue.kind==='photo-window'&&<div style={{position:'absolute',inset:0,overflow:'hidden',borderRadius:12,clipPath:`inset(${(1-p)*12}% ${(1-p)*50}% round 12px)`}}><div style={{height:'100%',transform:`scale(${1.04-.04*p})`}}>{photo(0)}</div></div>}
    {cue.kind==='photo-circle'&&<div style={{height:'100%',aspectRatio:'1',margin:'auto',overflow:'hidden',borderRadius:'50%',clipPath:`circle(${p*50}%)`}}>{photo(0)}</div>}
    {cue.kind==='photo-collage'&&[0,1].map(i=>{
      const cp=ease((elapsed-i*.11)/Math.max(.01,entry));
      return <div key={i} style={{position:'absolute',left:i?'46%':'5%',top:i?'15%':'3%',width:'49%',height:'80%',overflow:'hidden',borderRadius:7,border:'3px solid #eae7dd',boxShadow:'0 8px 20px #0004',opacity:cp,transform:`translateY(${20*(1-cp)}px) rotate(${i?5:-5}deg)`}}>{photo(i)}</div>;
    })}
    {cue.kind==='ui-grid'&&<div style={{position:'absolute',inset:0,borderRadius:18,overflow:'hidden',
      backgroundColor:'#191a1a',backgroundImage:'linear-gradient(0deg,transparent 24%,#72727238 25%,#72727238 26%,transparent 27%,transparent 74%,#72727238 75%,#72727238 76%,transparent 77%),linear-gradient(90deg,transparent 24%,#72727238 25%,#72727238 26%,transparent 27%,transparent 74%,#72727238 75%,#72727238 76%,transparent 77%)',backgroundSize:'50px 50px',
      clipPath:`inset(0 ${(1-p)*100}% 0 0 round 18px)`,boxShadow:'0 14px 36px #0005'}}>
      <div style={{position:'absolute',left:24,right:24,bottom:22,fontSize:28,lineHeight:1.15,fontWeight:700,color:'#fff',textShadow:'0 2px 8px #000'}}>{label}</div>
    </div>}
    {cue.kind==='ui-glass'&&<div style={{position:'absolute',inset:0,borderRadius:21,overflow:'hidden',background:'#c8c8c8',boxShadow:`0 15px 40px -5px ${accent}55`,transform:`translateY(${12*(1-p)}px) scale(${.98+.02*p})`}}>
      {[[-18,-45,'#ff930f'],[63,-8,accent],[-14,55,'#ff1b6b'],[58,76,'#0061ff']].map(([left,top,color],i)=><div key={i} style={{position:'absolute',left:`${left}%`,top:`${top}%`,width:'70%',aspectRatio:'1',borderRadius:'50%',background:String(color),opacity:.72}}/>)}
      <div style={{position:'absolute',inset:0,display:'flex',alignItems:'flex-end',padding:26,background:'linear-gradient(#ffffff72,#96969640)',backdropFilter:'blur(20px)',color:'#fff',fontSize:30,lineHeight:1.12,fontWeight:750,textShadow:'0 2px 10px #0008'}}>{label}</div>
    </div>}
    {cue.kind==='ui-notification'&&<div style={{position:'absolute',inset:0,display:'flex',alignItems:'center',justifyContent:'center',transform:`translateY(${8*(1-p)}px)`}}>
      <div style={{width:82,height:82,borderRadius:'50%',padding:7,background:'#181818',boxShadow:'6px 4px 30px #0005',zIndex:2}}><div style={{width:'100%',height:'100%',borderRadius:'50%',display:'grid',placeItems:'center',background:accent,color:'#fff',fontSize:34,fontWeight:850}}>✓</div></div>
      <div style={{height:70,width:`${p*270}px`,marginLeft:-18,overflow:'hidden',borderRadius:'0 14px 14px 0',background:'#181818',color:'#fff',display:'flex',alignItems:'center',boxShadow:'0 10px 28px #0004'}}><div style={{padding:'0 20px 0 34px',whiteSpace:'nowrap',opacity:ease((elapsed-.06)/Math.max(.01,entry)),fontSize:27,fontWeight:650}}>{label}</div></div>
    </div>}
    {!isPhoto&&<div style={{position:'absolute',inset:0,transform:`translateY(${8*(1-p)}px)`}}>
      {cue.kind==='icon'&&<LineAsset asset={cue.asset??'target'} progress={Math.min(1,elapsed/Math.max(.01,entry))} color={accent}/>}
      {cue.kind==='line-arrow'&&<svg width="100%" height="100%" viewBox="0 0 360 220" fill="none" stroke={accent} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M35 176C55 195 141 196 169 99C190 29 252 26 315 50M281 23L316 51 279 74" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p}/></svg>}
      {cue.kind==='focus-ring'&&<svg width="100%" height="100%" viewBox="0 0 360 220" fill="none" stroke={accent} strokeWidth="3" strokeLinecap="round"><path d="M284 43C172 0 30 28 30 109C30 205 314 223 330 123C340 56 250 25 171 27" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p}/></svg>}
      {cue.kind==='steps'&&<svg width="100%" height="100%" viewBox="0 0 360 220" fill="none" stroke={accent} strokeWidth="2.5"><path d="M57 156H151V110H249V62H317" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p}/>{[[57,156],[151,110],[249,62]].map(([x,y],i)=><circle key={i} cx={x} cy={y} r="10" fill="#080b09" opacity={ease((elapsed-i*.12)/.22)}/>)}</svg>}
    </div>}
  </div>;
};
