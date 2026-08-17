import React from 'react';
export function Radio({label,checked,onChange,disabled,name,value}){
return <label style={{display:'inline-flex',alignItems:'center',gap:10,cursor:disabled?'default':'pointer',opacity:disabled?0.5:1,fontFamily:'var(--font-body)',fontSize:15,color:'var(--text-heading)',userSelect:'none'}} onClick={()=>!disabled&&onChange&&onChange(value)}>
<span style={{width:18,height:18,borderRadius:'50%',border:'1.5px solid '+(checked?'var(--brand-primary)':'var(--border-strong)'),background:'var(--surface-card)',display:'inline-flex',alignItems:'center',justifyContent:'center'}}>
{checked&&<span style={{width:10,height:10,borderRadius:'50%',background:'var(--brand-primary)'}}></span>}
</span>{label}</label>;}