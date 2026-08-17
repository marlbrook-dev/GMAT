import React from 'react';
export function Card({title,action,children,padding='var(--space-6)',hoverable=false,style,...rest}){
const[h,setH]=React.useState(false);
return <div onMouseEnter={()=>setH(true)} onMouseLeave={()=>setH(false)} style={{background:'var(--surface-card)',border:'1px solid var(--border-default)',borderRadius:'var(--radius-lg)',boxShadow:hoverable&&h?'var(--shadow-md)':'var(--shadow-sm)',padding,transition:'box-shadow var(--duration-base) var(--ease-out)',fontFamily:'var(--font-body)',...style}} {...rest}>
{(title||action)&&<div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:'var(--space-4)'}}>
<div style={{fontFamily:'var(--font-display)',fontWeight:700,fontSize:17,color:'var(--text-heading)'}}>{title}</div>{action}</div>}
{children}</div>;}