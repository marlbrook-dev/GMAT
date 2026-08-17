import React from 'react';
const T={success:['var(--status-success)','var(--status-success-bg)','var(--green-100)'],error:['var(--status-error)','var(--status-error-bg)','var(--red-100)'],info:['var(--status-info)','var(--status-info-bg)','var(--blue-100)'],warning:['var(--status-warning)','var(--status-warning-bg)','var(--amber-100)']};
export function Toast({tone='info',children,onDismiss,style}){
const[fg,bg,bd]=T[tone]||T.info;
return <div role="status" style={{display:'flex',alignItems:'center',gap:10,background:bg,border:'1px solid '+bd,borderLeft:'none',borderRadius:'var(--radius-md)',padding:'10px 14px',fontFamily:'var(--font-body)',fontSize:14,color:'var(--text-heading)',boxShadow:'var(--shadow-md)',...style}}>
<span style={{width:8,height:8,borderRadius:'50%',background:fg,flexShrink:0}}></span>
<span style={{flex:1}}>{children}</span>
{onDismiss&&<button onClick={onDismiss} aria-label="Dismiss" style={{border:'none',background:'none',cursor:'pointer',padding:0,color:'var(--text-muted)',display:'inline-flex'}}><svg viewBox="0 0 24 24" width="14" height="14" style={{stroke:'currentColor',fill:'none',strokeWidth:2.5,strokeLinecap:'round'}}><path d="M18 6 6 18M6 6l12 12"/></svg></button>}
</div>;}