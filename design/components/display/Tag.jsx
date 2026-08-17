import React from 'react';
export function Tag({children,onRemove,style}){
return <span style={{display:'inline-flex',alignItems:'center',gap:6,background:'var(--surface-sunken)',color:'var(--text-body)',borderRadius:'var(--radius-sm)',padding:'3px 8px',fontFamily:'var(--font-body)',fontSize:13,fontWeight:500,...style}}>{children}
{onRemove&&<button onClick={onRemove} aria-label="Remove" style={{border:'none',background:'none',cursor:'pointer',padding:0,display:'inline-flex',color:'var(--text-muted)'}}><svg viewBox="0 0 24 24" width="12" height="12" style={{stroke:'currentColor',fill:'none',strokeWidth:2.5,strokeLinecap:'round'}}><path d="M18 6 6 18M6 6l12 12"/></svg></button>}
</span>;}