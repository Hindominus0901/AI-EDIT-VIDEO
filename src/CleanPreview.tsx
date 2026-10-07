import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/google-fonts/Inter';
const {fontFamily: CLEAN_FONT} = loadFont('normal', {weights: ['500', '600', '700'], subsets: ['latin', 'vietnamese']});

export type CleanPreviewProps = {
  clip: string;
  durationSec: number;
  vertical: boolean;
  headline: string;
  captions: {start: number; end: number; text: string}[];
  cards: {start: number; end: number; kicker: string; lines: string[]}[];
  music: string;
  images?: {start: number; end: number; src: string; label: string; slot: number}[];
};

export const cleanDefaults: CleanPreviewProps = {
  clip: 'samples/setup-test.mp4', durationSec: 3, vertical: false,
  headline: 'Xây thương hiệu cá nhân', captions: [], cards: [], music: '',
};

export const CleanPreview: React.FC<CleanPreviewProps> = (p) => {
  const f = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const sec = f / fps;
  const cap = p.captions.find(c => sec >= c.start && sec < c.end);
  const card = p.cards.find(c => sec >= c.start && sec < c.end);
  const images = (p.images ?? []).filter(c => sec >= c.start && sec < c.end);
  const unit = width / (p.vertical ? 1080 : 1920);
  const cardOpacity = card ? Math.min(1, (sec - card.start) / .24, (card.end - sec) / .24) : 0;
  const captionOpacity = cap ? Math.min(1, (sec - cap.start) / .09) * (1 - cardOpacity) : 0;
  const intro = interpolate(f, [0, 8, fps * 3.5, fps * 4], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{backgroundColor: '#101112', color: '#fff', fontFamily: CLEAN_FONT}}>
    <OffthreadVideo src={staticFile(p.clip)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 50%'}} />
    <AbsoluteFill style={{background: p.vertical
      ? 'linear-gradient(0deg,rgba(0,0,0,.6),transparent 36%,transparent 72%,rgba(0,0,0,.5))'
      : 'linear-gradient(0deg,rgba(0,0,0,.68),transparent 34%,transparent 74%,rgba(0,0,0,.35))'}} />
    {p.music && <Audio src={staticFile(p.music)} volume={frame => interpolate(frame,
      [0, fps, Math.max(fps + 1, durationInFrames - fps * 2), durationInFrames],
      [0, .075, .075, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />}
    {intro > 0 && !card && <div style={{position: 'absolute', top: p.vertical ? height * .09 : 48 * unit,
      left: '8%', width: '84%', textAlign: p.vertical ? 'center' : 'left', opacity: intro}}>
      <div style={{fontSize: 19 * unit, letterSpacing: 2 * unit, fontWeight: 500, opacity: .65, marginBottom: 18 * unit}}>THƯƠNG HIỆU CÁ NHÂN</div>
      <div style={{fontSize: (p.vertical ? 50 : 48) * unit, lineHeight: 1.24, letterSpacing: -.8 * unit, fontWeight: 600, maxWidth: p.vertical ? '100%' : '72%'}}>{p.headline}</div>
    </div>}
    {card && <AbsoluteFill style={{backgroundColor: '#101112', opacity: cardOpacity, justifyContent: 'center', alignItems: 'center', padding: width * .085}}>
      <div style={{fontSize: 19 * unit, fontWeight: 500, letterSpacing: 2 * unit, color: '#929995', marginBottom: 32 * unit}}>{card.kicker}</div>
      <div style={{textAlign: 'center', fontWeight: 600, lineHeight: 1.3, letterSpacing: -1.4 * unit, maxWidth: '100%'}}>
        {card.lines.map((line, i) => <div key={i} style={{fontSize: (i === 0 ? (p.vertical ? 52 : 64) : (p.vertical ? 74 : 90)) * unit, marginTop: i ? 12 * unit : 0, fontWeight: i ? 700 : 500}}>{line}</div>)}
      </div>
      <div style={{height: 2 * unit, width: 68 * unit, background: '#a9b5ab', marginTop: 40 * unit}} />
    </AbsoluteFill>}
    {images.map((im,i) => {
      const opacity = Math.min(1, (sec-im.start)/.22, (im.end-sec)/.22);
      const enter = Math.min(1, (sec-im.start)/.3);
      const size = (p.vertical ? 278 : 208) * unit;
      return <div key={im.src+im.start} style={{position:'absolute',
        left: p.vertical ? width*.085 + im.slot*(size+22*unit) : 94*unit + im.slot*(size+22*unit),
        bottom: height * (p.vertical ? .085 : .25), width:size, opacity,
        transform:`translateY(${(1-enter)*14*unit}px)`, textAlign:'center'}}>
        <Img src={staticFile(im.src)} style={{width:size,height:size*.8,objectFit:'contain',borderRadius:8*unit,boxShadow:'0 5px 18px rgba(0,0,0,.14)'}}/>
        <div style={{fontSize:(p.vertical ? 23 : 20)*unit,lineHeight:1.4,fontWeight:500,marginTop:10*unit,textShadow:'0 1px 4px #000'}}>{im.label}</div>
      </div>;
    })}
    {cap && <div style={{position: 'absolute', bottom: height * (p.vertical ? .285 : .085), opacity: captionOpacity,
      left: p.vertical ? '7%' : '15%', width: p.vertical ? '86%' : '70%', textAlign: 'center',
      fontSize: (p.vertical ? 46 : 40) * unit, fontWeight: 600, lineHeight: 1.32, letterSpacing: -.35 * unit,
      textShadow: '0 2px 5px rgba(0,0,0,.65)', whiteSpace: 'pre-line'}}>{cap.text}</div>}
    {p.cards.map((c,i) => <Sequence key={i} from={Math.round(c.start * fps)} durationInFrames={Math.round(fps * .4)}>
      <Audio src={staticFile('sfx/kenney/tick_001.ogg')} volume={.06} />
    </Sequence>)}
  </AbsoluteFill>;
};
