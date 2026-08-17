import React from 'react';
export function Select({label,options=[],style,...rest}){
return <label style={{display:'grid',gap:6,fontFamily:'var(--font-body)',...style}}>
{label&&<span style={{fontSize:13,fontWeight:600,color:'var(--text-heading)'}}>{label}</span>}
<span style={{position:'relative',display:'block'}}>
<select style={{font:'inherit',fontSize:15,color:'var(--text-heading)',background:'var(--surface-card)',border:'1px solid var(--border-strong)',borderRadius:'var(--radius-md)',padding:'9px 34px 9px 12px',width:'100%',appearance:'none',outline:'none'}} {...rest}>
{options.map(o=><option key={o.value??o} value={o.value??o}>{o.label??o}</option>)}
</select>
<svg viewBox="0 0 24 24" width="16" height="16" style={{position:'absolute',right:10,top:'50%',transform:'translateY(-50%)',pointerEvents:'none',stroke:'var(--text-muted)',fill:'none',strokeWidth:2,strokeLinecap:'round',strokeLinejoin:'round'}}><path d="m6 9 6 6 6-6"/></svg>
</span></label>;}