import React from 'react';
export function Tabs({items=[],active,defaultActive,onChange,style}){
const[cur,setCur]=React.useState(defaultActive??items[0]);
const a=active!==undefined?active:cur;
return <div role="tablist" style={{display:'flex',gap:'var(--space-6)',borderBottom:'1px solid var(--border-default)',fontFamily:'var(--font-display)',...style}}>
{items.map(t=><button key={t} role="tab" aria-selected={t===a} onClick={()=>{setCur(t);onChange&&onChange(t);}} onFocus={e=>{if(e.target.matches(':focus-visible'))e.target.style.boxShadow='var(--focus-ring)';}} onBlur={e=>{e.target.style.boxShadow='none';}} style={{borderRadius:'var(--radius-sm)',border:'none',background:'none',cursor:'pointer',padding:'10px 2px',fontFamily:'inherit',fontSize:15,fontWeight:700,color:t===a?'var(--brand-primary)':'var(--text-muted)',borderBottom:'2px solid '+(t===a?'var(--brand-primary)':'transparent'),marginBottom:-1,outline:'none',transition:'box-shadow var(--duration-fast) var(--ease-out),'+'color var(--duration-fast) var(--ease-out)'}}>{t}</button>)}
</div>;}