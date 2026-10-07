import {useEffect,useMemo} from 'react';
import {cancelRender,continueRender,delayRender,staticFile} from 'remotion';
let loading:Promise<void>|undefined;
export const useEditorialFonts=(enabled:boolean)=>{
  const handle=useMemo(()=>enabled?delayRender('Loading bundled editorial fonts'):null,[enabled]);
  useEffect(()=>{
    if(handle===null)return;
    loading??=Promise.all([
      new FontFace('Manrope Editorial',`url(${staticFile('fonts/editorial-c/Manrope.ttf')})`,{weight:'700'}),
      new FontFace('Playfair Editorial',`url(${staticFile('fonts/editorial-c/Playfair.ttf')})`,{weight:'650',style:'italic'}),
    ].map(async f=>{await f.load();document.fonts.add(f);})).then(()=>undefined);
    loading.then(()=>continueRender(handle)).catch(cancelRender);
  },[handle]);
};
