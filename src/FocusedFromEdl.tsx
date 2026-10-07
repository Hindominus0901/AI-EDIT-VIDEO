import React from 'react';
import type {Edl} from './edl-types';
import {FocusedPreview} from './FocusedPreview';
import {SFX_FILE_BY_CUE} from './components/Sfx';
import {premiumSets} from './premium-kit/theme';

// Keep one editable EDL for both the automated pipeline and the approved layout.
export const FocusedFromEdl:React.FC<{edl:Edl}>=({edl})=><FocusedPreview
  clip={edl.source.clip} durationSec={edl.source.durationSec} vertical={edl.format.h>edl.format.w}
  sourceSize={edl.source.width&&edl.source.height?{width:edl.source.width,height:edl.source.height}:undefined}
  voiceVolume={edl.music?.clipVolume??edl.source.volume}
  premiumSet={edl.style.premiumSet}
  cameraCues={edl.tracks.effects} broll={edl.tracks.broll}
  headline="" emphasis="" sourceLabel="" beats={[]} captionMotion="library"
  captions={edl.tracks.captions.map(c=>({start:c.startMs/1000,end:c.endMs/1000,text:c.text,
    entry:c.motion?.entry??'rise',mark:c.motion?.mark,
    emphasis:c.motion?.keyword?{text:c.motion.keyword,style:c.motion.strong?'strong':'color'}:undefined}))}
  motionGraphics={edl.tracks.graphics.filter(g=>g.type==='clean-motion'&&g.motion).map(g=>({
    start:g.startMs/1000,end:g.endMs/1000,...g.motion!,accent:edl.style.premiumSet?premiumSets[edl.style.premiumSet].accent:edl.style.recipe.accent}))}
  music={edl.music?.src??''} musicVolume={edl.music?.volume} musicStartSec={edl.music?.startSec}
  musicLoop={edl.music?.loop} musicFadeOutSec={edl.music?.fadeOutSec}
  soundEffects sounds={edl.tracks.sfx.map(s=>({sec:Math.max(0,(s.startMs-s.preRollMs)/1000),src:SFX_FILE_BY_CUE[s.sound],gain:s.volume}))}
/>;
