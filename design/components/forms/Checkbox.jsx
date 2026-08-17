import React from 'react';
export function Checkbox({label,checked,defaultChecked=false,onChange,disabled}){
const[on,setOn]=React.useState(defaultChecked);
const c=checked!==undefined?checked:on;
const toggle=()=>{if(disabled)return;setOn(!c);onChange&&onChange(!c);};
return <label onClick={toggle} style={{display:'inline-flex',alignItems:'center',gap:10,cursor:disabled?'default':'pointer',opacity:disabled?0.5:1,fontFamily:'var(--font-body)',fontSize:15,color:'var(--text-heading)',userSelect:'none'}}>
<span style={{width:18,height:18,borderRadius:'var(--radius-sm)',border:'1.5px solid '+(c?'var(--brand-primary)':'var(--border-strong)'),background:c?'var(--brand-primary)':'var(--surface-card)',display:'inline-flex',alignItems:'center',justifyContent:'center',transition:'background var(--duration-fast) var(--ease-out)'}}>
{c&&<svg viewBox="0 0 24 24" width="12" height="12" style={{stroke:'#fff',fill:'none',strokeWidth:3.5,strokeLinecap:'round',strokeLinejoin:'round'}}><path d="m5 13 4 4L19 7"/></svg>}
</span>{label}</label>;}