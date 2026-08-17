import React from 'react';
export function IconButton({variant='subtle',size='md',label,disabled,children,style,...rest}){
const[h,setH]=React.useState(false);const[fv,setFv]=React.useState(false);
const px={sm:28,md:36,lg:44}[size];
const base={width:px,height:px,display:'inline-flex',alignItems:'center',justifyContent:'center',borderRadius:'var(--radius-md)',cursor:disabled?'default':'pointer',color:'var(--text-body)',transition:'background var(--duration-fast) var(--ease-out)',opacity:disabled?0.5:1,outline:'none',boxShadow:fv?'var(--focus-ring)':'none',background:variant==='outline'?'var(--surface-card)':'transparent',border:variant==='outline'?'1px solid var(--border-strong)':'1px solid transparent'};
if(h&&!disabled)base.background=variant==='outline'?'var(--gray-50)':'var(--gray-100)';
return <button aria-label={label} title={label} disabled={disabled} onMouseEnter={()=>setH(true)} onMouseLeave={()=>setH(false)} onFocus={e=>setFv(e.target.matches(':focus-visible'))} onBlur={()=>setFv(false)} style={{...base,...style}} {...rest}>{children}</button>;}