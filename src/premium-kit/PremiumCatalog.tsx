import React from 'react';
import {AbsoluteFill,Audio,Sequence,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {loadFont as loadInter} from '@remotion/google-fonts/Inter';
import {loadFont as loadVietnamese} from '@remotion/google-fonts/BeVietnamPro';
import {loadFont as loadNewsreader} from '@remotion/google-fonts/Newsreader';
import {PremiumText,clamp,settle} from './PremiumText';
import {PremiumGraphic} from './PremiumGraphic';
import {premiumSets,type PremiumSet} from './theme';
import type {TextPreset} from '../motion-kit/catalog';

loadInter('normal',{weights:['500','600','700'],subsets:['latin','vietnamese']});
loadVietnamese('normal',{weights:['500','600'],subsets:['latin','vietnamese']});
loadNewsreader('normal',{weights:['500','600'],subsets:['latin','vietnamese']});
const ids=['studio','paper','mono'] as const;
const copy={studio:['Rõ ý.','Có chiều sâu.'],paper:['Cho câu chuyện','khoảng thở.'],mono:['Ít chi tiết.','Đúng trọng tâm.']};
const photos=['images/editorial-v4/ocean.jpg','images/editorial-v4/pond.jpg'];

// One set per chapter. Labels belong to this specimen film, never the edited video.
export const PremiumCatalog:React.FC=()=>{
  const {fps}=useVideoConfig(),f=useCurrentFrame(),time=f/fps;
  const chapter=Math.min(2,Math.floor(time/8)),local=time-chapter*8,set=ids[chapter],theme=premiumSets[set];
  const photoStage=local>=2.4&&local<5.6,diagramStage=local>=5.6;
  const stageTime=photoStage?local-2.4:diagramStage?local-5.6:local;
  const stageDuration=photoStage?3.2:2.4;
  const phrase=photoStage?['Giữ lại điều quan trọng.','Khung hình có chiều sâu.','Hai góc nhìn. Một ý.'][chapter]:['Luôn có chỗ cho bạn.','Uy tín từ việc thật.','Lắng nghe để tốt hơn.'][chapter];
  return <AbsoluteFill style={{background:theme.background,color:theme.foreground,fontFamily:theme.font}}>
    <div style={{position:'absolute',left:108,top:80,fontSize:23,fontWeight:500,letterSpacing:'.025em',color:theme.muted}}>PREMIUM SETS / {theme.name}</div>
    <div style={{position:'absolute',right:108,top:80,fontSize:23,color:theme.muted}}>0{chapter+1} / 03</div>
    {!photoStage&&!diagramStage?<div style={{position:'absolute',left:108,top:330,width:1704}}>
      <PremiumText text={copy[set][0]} elapsed={local} duration={2.4} set={set} preset={theme.entry as TextPreset}
        style={{fontSize:104,textAlign:'left',fontFamily:set==='paper'?'Newsreader':theme.font,fontWeight:set==='mono'?600:500,lineHeight:1.16}}/>
      <PremiumText text={copy[set][1]} elapsed={Math.max(0,local-.12)} duration={2.28} set={set} preset={theme.entry as TextPreset}
        keyword={{text:copy[set][1]}} style={{fontSize:104,textAlign:'left',fontFamily:set==='paper'?'Newsreader':theme.font,lineHeight:1.16}}/>
    </div>:<>
      <PremiumGraphic cue={{start:0,end:stageDuration,kind:photoStage?(['photo-mat','photo-detail','photo-diptych'] as const)[chapter]:'icon',images:photos,asset:(['compass','time','chat'] as const)[chapter]}}
        elapsed={stageTime} duration={stageDuration} set={set} style={{position:'absolute',left:540,top:242,width:840,height:480}}/>
      <PremiumText text={phrase} elapsed={stageTime} duration={stageDuration} set={set} preset={theme.entry as TextPreset}
        keyword={{text:photoStage?['quan trọng','chiều sâu','Một ý'][chapter]:['chỗ','việc thật','Lắng nghe'][chapter],strong:diagramStage}}
        style={{position:'absolute',left:260,top:782,width:1400,fontSize:49}}/>
    </>}
    <div style={{position:'absolute',left:108,bottom:66,fontSize:21,color:theme.muted,opacity:clamp(local/.3)}}>
      {photoStage?['Photo mat','Detail crop','Aligned diptych'][chapter]:diagramStage?'Concept illustration':`${set==='paper'?'Newsreader + Be Vietnam Pro':theme.font} · Vietnamese`}
    </div>
    <div style={{position:'absolute',right:108,bottom:72,display:'flex',gap:10}}>{ids.map((id,i)=><div key={id} style={{width:48,height:2,background:i===chapter?theme.accent:theme.line,opacity:i===chapter?settle(local/.3):.6}}/>)}</div>
    <Audio src={staticFile('music/cc0/contemplation.mp3')} trimBefore={240} volume={frame=>Math.min(1,frame/fps)*Math.min(1,(24-frame/fps)/1.5)}/>
    {[2.4,10.4,18.4].map(sec=><Sequence key={sec} from={Math.round(sec*fps)} durationInFrames={30}><Audio src={staticFile('sfx/kenney/drop_002.ogg')} volume={.025}/></Sequence>)}
  </AbsoluteFill>;
};
