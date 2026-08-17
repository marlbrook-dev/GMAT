import React from 'react';
export function ProgressBar({value=0,max=100,color='var(--brand-primary)',height=8,label,style}){
const pct=Math.max(0,Math.min(100,(value/max)*100));
return <div style={{fontFamily:'var(--font-body)',...style}}>
{label&&<div style={{display:'flex',justifyContent:'space-between',fontSize:12,fontWeight:600,color:'var(--text-muted)',marginBottom:6}}><span>{label}</span><span style={{fontFamily:'var(--font-mono)'}}>{Math.round(pct)}%</span></div>}
<div style={{height,background:'var(--surface-sunken)',borderRadius:'var(--radius-pill)',overflow:'hidden'}}>
<div style={{width:pct+'%',height:'100%',background:color,borderRadius:'var(--radius-pill)',transition:'width var(--duration-base) var(--ease-out)'}}></div>
</div></div>;}