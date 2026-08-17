import React from 'react';
export function Switch({label,checked,defaultChecked=false,onChange,disabled}){
const[on,setOn]=React.useState(defaultChecked);
const c=checked!==undefined?checked:on;
const toggle=()=>{if(disabled)return;setOn(!c);onChange&&onChange(!c);};
return <label onClick={toggle} style={{display:'inline-flex',alignItems:'center',gap:10,cursor:disabled?'default':'pointer',opacity:disabled?0.5:1,fontFamily:'var(--font-body)',fontSize:15,color:'var(--text-heading)',userSelect:'none'}}>
<span style={{width:36,height:20,borderRadius:'var(--radius-pill)',background:c?'var(--brand-primary)':'var(--gray-300)',position:'relative',transition:'background var(--duration-base) var(--ease-out)',flexShrink:0}}>
<span style={{position:'absolute',top:2,left:c?18:2,width:16,height:16,borderRadius:'50%',background:'#fff',boxShadow:'var(--shadow-sm)',transition:'left var(--duration-base) var(--ease-out)'}}></span>
</span>{label}</label>;}