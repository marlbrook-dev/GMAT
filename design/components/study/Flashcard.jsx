import React from 'react';
export function Flashcard({front,back,frontLabel='TERM',backLabel='DEFINITION',width='100%',height=200,style}){
const[flip,setFlip]=React.useState(false);
const face={position:'absolute',inset:0,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',gap:12,borderRadius:'var(--radius-lg)',padding:'24px 28px',backfaceVisibility:'hidden',WebkitBackfaceVisibility:'hidden',textAlign:'center',boxSizing:'border-box'};
return <button onClick={()=>setFlip(!flip)} aria-pressed={flip} style={{display:'block',width,height,perspective:'1000px',border:'none',background:'none',padding:0,cursor:'pointer',...style}}>
<span style={{position:'relative',display:'block',width:'100%',height:'100%',transformStyle:'preserve-3d',transform:flip?'rotateX(180deg)':'none',transition:'transform 320ms var(--ease-out)'}}>
<span style={{...face,background:'var(--surface-card)',border:'1px solid var(--border-default)',boxShadow:'var(--shadow-md)'}}>
<span style={{fontSize:10,fontWeight:600,letterSpacing:'var(--tracking-caps)',color:'var(--text-muted)'}}>{frontLabel}</span>
<span style={{fontFamily:'var(--font-serif-display)',fontWeight:700,fontSize:22,color:'var(--text-heading)',lineHeight:1.3}}>{front}</span>
<span style={{fontSize:12,color:'var(--text-muted)'}}>Click to flip</span>
</span>
<span style={{...face,background:'var(--navy-900)',border:'1px solid var(--navy-900)',boxShadow:'var(--shadow-md)',transform:'rotateX(180deg)'}}>
<span style={{fontSize:10,fontWeight:600,letterSpacing:'var(--tracking-caps)',color:'var(--gold-500)'}}>{backLabel}</span>
<span style={{fontFamily:'var(--font-body)',fontSize:16,color:'#fff',lineHeight:1.5}}>{back}</span>
</span>
</span></button>;}