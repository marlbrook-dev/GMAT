import React from 'react';
export function StatTile({label,value,delta,deltaTone='success',style}){
return <div style={{background:'var(--surface-card)',border:'1px solid var(--border-default)',borderRadius:'var(--radius-lg)',boxShadow:'var(--shadow-sm)',padding:'var(--space-5)',fontFamily:'var(--font-body)',...style}}>
<div style={{fontSize:12,fontWeight:600,letterSpacing:'var(--tracking-caps)',textTransform:'uppercase',color:'var(--text-muted)'}}>{label}</div>
<div style={{display:'flex',alignItems:'baseline',gap:10,marginTop:6}}>
<span style={{fontFamily:'var(--font-mono)',fontSize:30,fontWeight:500,color:'var(--text-heading)',fontVariantNumeric:'tabular-nums'}}>{value}</span>
{delta&&<span style={{fontSize:13,fontWeight:600,color:deltaTone==='success'?'var(--status-success)':deltaTone==='error'?'var(--status-error)':'var(--text-muted)'}}>{delta}</span>}
</div></div>;}