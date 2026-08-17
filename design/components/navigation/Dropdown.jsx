import React from 'react';
export function Dropdown({label,items=[],onSelect,align='left'}){
const[open,setOpen]=React.useState(false);
const[fv,setFv]=React.useState(false);
const ref=React.useRef(null);
React.useEffect(()=>{
if(!open)return;
const onDoc=(e)=>{if(ref.current&&!ref.current.contains(e.target))setOpen(false);};
const onKey=(e)=>{if(e.key==='Escape')setOpen(false);};
document.addEventListener('mousedown',onDoc);document.addEventListener('keydown',onKey);
return()=>{document.removeEventListener('mousedown',onDoc);document.removeEventListener('keydown',onKey);};
},[open]);
return <div ref={ref} style={{position:'relative',display:'inline-block',isolation:'isolate'}}>
<button aria-haspopup="menu" aria-expanded={open} onClick={()=>setOpen(!open)} onFocus={e=>setFv(e.target.matches(':focus-visible'))} onBlur={()=>setFv(false)} style={{display:'inline-flex',alignItems:'center',gap:7,fontFamily:'var(--font-display)',fontWeight:700,fontSize:14,color:'var(--text-heading)',background:'var(--surface-card)',border:'1px solid var(--border-strong)',borderRadius:'var(--radius-md)',padding:'8px 14px',cursor:'pointer',outline:'none',boxShadow:fv?'var(--focus-ring)':'none'}}>
{label}
<svg viewBox="0 0 24 24" width="14" height="14" style={{stroke:'var(--text-muted)',fill:'none',strokeWidth:2,strokeLinecap:'round',strokeLinejoin:'round',transform:open?'rotate(180deg)':'none',transition:'transform var(--duration-fast) var(--ease-out)'}}><path d="m6 9 6 6 6-6"/></svg>
</button>
{open&&<div role="menu" style={{position:'absolute',top:'calc(100% + 8px)',[align==='right'?'right':'left']:0,minWidth:200,background:'var(--surface-card)',border:'1px solid var(--border-default)',borderRadius:'var(--radius-lg)',boxShadow:'var(--shadow-lg)',padding:6,display:'grid',zIndex:'var(--z-dropdown)'}}>
{items.map(it=>{const v=it.value??it,l=it.label??it;
return <button key={v} role="menuitem" onClick={()=>{setOpen(false);onSelect&&onSelect(v);}}
style={{textAlign:'left',border:'none',background:'transparent',cursor:'pointer',padding:'9px 12px',borderRadius:'var(--radius-md)',fontFamily:'var(--font-display)',fontWeight:600,fontSize:14,color:'var(--text-heading)'}}
onMouseEnter={e=>{e.currentTarget.style.background='var(--brand-primary-soft)';e.currentTarget.style.color='var(--brand-primary)';}}
onMouseLeave={e=>{e.currentTarget.style.background='transparent';e.currentTarget.style.color='var(--text-heading)';}}>{l}</button>;})}
</div>}
</div>;}
