import React from 'react';
export function Tooltip({text,children}){
const[show,setShow]=React.useState(false);
return <span style={{position:'relative',display:'inline-flex'}} onMouseEnter={()=>setShow(true)} onMouseLeave={()=>setShow(false)}>
{children}
{show&&<span style={{position:'absolute',bottom:'calc(100% + 8px)',left:'50%',transform:'translateX(-50%)',background:'var(--surface-inverse)',color:'#fff',fontFamily:'var(--font-body)',fontSize:12,fontWeight:500,lineHeight:1.4,padding:'6px 10px',borderRadius:'var(--radius-sm)',whiteSpace:'nowrap',boxShadow:'var(--shadow-lg)',zIndex:10}}>{text}</span>}
</span>;}