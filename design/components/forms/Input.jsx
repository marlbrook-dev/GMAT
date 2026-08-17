import React from 'react';
export function Input({label,hint,error,style,inputStyle,...rest}){
const[f,setF]=React.useState(false);
return <label style={{display:'grid',gap:6,fontFamily:'var(--font-body)',...style}}>
{label&&<span style={{fontSize:13,fontWeight:600,color:'var(--text-heading)'}}>{label}</span>}
<input onFocus={()=>setF(true)} onBlur={()=>setF(false)} style={{font:'inherit',fontSize:15,color:'var(--text-heading)',background:'var(--surface-card)',border:'1px solid '+(error?'var(--status-error)':f?'var(--brand-primary)':'var(--border-strong)'),borderRadius:'var(--radius-md)',padding:'9px 12px',outline:'none',boxShadow:f?'var(--focus-ring)':'none',transition:'box-shadow var(--duration-fast) var(--ease-out)',...inputStyle}} {...rest}/>
{error?<span style={{fontSize:12,color:'var(--status-error)'}}>{error}</span>:hint?<span style={{fontSize:12,color:'var(--text-muted)'}}>{hint}</span>:null}
</label>;}