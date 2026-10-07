export type CameraCue={startMs:number;endMs:number;scale:number;type:'zoom'|'punch-in'};
export const smoothstep=(x:number)=>{const t=Math.max(0,Math.min(1,x));return t*t*t*(t*(t*6-15)+10);};
// Boundary scale and velocity return to the base crop. Never zoom typography.
export const cameraScale=(ms:number,cues:CameraCue[])=>{
  let amount=0;
  for(const c of cues){
    if(ms<c.startMs||ms>=c.endMs)continue;
    const duration=c.endMs-c.startMs;
    const attack=Math.min(c.type==='punch-in'?420:1600,duration*.4);
    const release=Math.min(1000,duration*.35);
    const envelope=Math.min(smoothstep((ms-c.startMs)/attack),smoothstep((c.endMs-ms)/release));
    amount=Math.max(amount,(c.scale-1)*envelope);
  }
  return 1+amount;
};
