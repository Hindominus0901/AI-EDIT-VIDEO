/**
 * Remotion root — registers the Reel composition (9:16, 30fps).
 * Duration is derived from the EDL source duration via calculateMetadata.
 */
import React from "react";
import { Composition } from "remotion";
import { Reel } from "./Reel";
import { edlSchema, type Edl } from "./edl-types";
import demoEdl from "./fixtures/demo-edl.json";
import {CleanPreview, cleanDefaults} from './CleanPreview';
import {EditorialPreview, editorialDefaults} from './EditorialPreview';
import {FocusedPreview} from './FocusedPreview';
import {MotionCatalog} from './MotionCatalog';
import {PremiumCatalog} from './premium-kit/PremiumCatalog';
import {ReferenceReedit,referenceReeditDefaults} from './ReferenceReedit';

export const RemotionRoot: React.FC = () => {
  return (
    <>
    <Composition id="ReferenceReedit" component={ReferenceReedit} defaultProps={referenceReeditDefaults}
      width={1080} height={1920} fps={30} durationInFrames={801}
      calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.durationSec*30)})}/>
    <Composition id="PremiumCatalog" component={PremiumCatalog} width={1920} height={1080} fps={30} durationInFrames={720}/>
    <Composition id="MotionCatalog" component={MotionCatalog} width={1920} height={1080} fps={30} durationInFrames={1200}/>
    <Composition id="FocusedPreview" component={FocusedPreview} defaultProps={editorialDefaults}
      width={1080} height={1920} fps={30} durationInFrames={240}
      calculateMetadata={({props}) => ({width:props.vertical?1080:1920,height:props.vertical?1920:1080,durationInFrames:Math.ceil(props.durationSec*30)})}/>
    <Composition id="EditorialPreview" component={EditorialPreview} defaultProps={editorialDefaults}
      width={1080} height={1920} fps={30} durationInFrames={240}
      calculateMetadata={({props}) => ({width:props.vertical?1080:1920,height:props.vertical?1920:1080,durationInFrames:Math.ceil(props.durationSec*30)})}/>
    <Composition id="CleanPreview" component={CleanPreview} defaultProps={cleanDefaults}
      width={1920} height={1080} fps={30} durationInFrames={240}
      calculateMetadata={({props}) => ({width: props.vertical ? 1080 : 1920,
        height: props.vertical ? 1920 : 1080, durationInFrames: Math.ceil(props.durationSec * 30)})} />
    <Composition
      id="Reel"
      component={Reel}
      width={1080}
      height={1920}
      fps={30}
      durationInFrames={300}
      defaultProps={{ edl: demoEdl as unknown as Edl }}
      calculateMetadata={({ props }) => {
        const edl = edlSchema.parse(props.edl);
        const { w, h, fps } = edl.format;
        return {
          width: w,
          height: h,
          fps,
          durationInFrames: Math.ceil(edl.source.durationSec * fps),
          props: { edl },
        };
      }}
    />
    </>
  );
};
