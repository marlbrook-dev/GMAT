import React from 'react';
export function Dialog({open,title,children,footer,onClose,width=440}){
if(!open)return null;
return <div onClick={onClose} style={{position:'fixed',inset:0,background:'rgba(11,18,32,.45)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:'var(--z-modal)',padding:24}}>
<div onClick={e=>e.stopPropagation()} style={{background:'var(--surface-card)',borderRadius:'var(--radius-lg)',boxShadow:'var(--shadow-lg)',width,maxWidth:'100%',padding:'var(--space-6)',fontFamily:'var(--font-body)'}}>
<div style={{fontFamily:'var(--font-display)',fontWeight:800,fontSize:20,color:'var(--text-heading)',marginBottom:'var(--space-3)'}}>{title}</div>
<div style={{color:'var(--text-body)',fontSize:15}}>{children}</div>
{footer&&<div style={{display:'flex',justifyContent:'flex-end',gap:'var(--space-3)',marginTop:'var(--space-6)'}}>{footer}</div>}
</div></div>;}