function AppShell({active,onNav,children,view='user',onToggleView,onAccount}){
const {Badge}=window.GMATStudyGuideDesignSystem_efe656;
return <div style={{minHeight:'100vh',background:'var(--surface-page)'}}>
<header style={{background:'var(--surface-card)',borderBottom:'1px solid var(--border-default)',position:'sticky',top:0,zIndex:20}}>
<div style={{maxWidth:'var(--container-max)',margin:'0 auto',padding:'0 var(--space-6)',height:60,display:'flex',alignItems:'center',gap:32}}>
<div style={{display:'flex',alignItems:'center',gap:9,whiteSpace:'nowrap'}}><img src="../../assets/logo.svg" width="30" height="30" alt=""/><span style={{fontFamily:'var(--font-serif-display)',fontWeight:700,fontSize:19,color:'var(--navy-900)'}}>Meridian <span style={{color:'var(--gold-600)'}}>Prep</span></span></div>
<nav style={{display:'flex',gap:4,flex:1}}>
{['Dashboard','Practice','Review'].map(t=><button key={t} onClick={()=>onNav(t)} style={{border:'none',cursor:'pointer',fontFamily:'var(--font-display)',fontWeight:700,fontSize:14,padding:'7px 14px',borderRadius:'var(--radius-md)',background:active===t?'var(--brand-primary-soft)':'transparent',color:active===t?'var(--brand-primary)':'var(--text-muted)'}}>{t}</button>)}
</nav>
<Badge tone="accent">Streak ×7</Badge>
<span style={{display:'inline-flex',border:'1px solid var(--border-strong)',borderRadius:'var(--radius-pill)',padding:2,gap:2}} title="Prototype only: switch between user and owner views">
{['User','Owner'].map(v=><button key={v} onClick={()=>onToggleView&&onToggleView(v.toLowerCase())} aria-pressed={view===v.toLowerCase()} style={{border:'none',cursor:'pointer',fontFamily:'var(--font-display)',fontWeight:700,fontSize:11,padding:'4px 10px',borderRadius:999,background:view===v.toLowerCase()?'var(--navy-800)':'transparent',color:view===v.toLowerCase()?'#fff':'var(--text-muted)'}}>{v}</button>)}
</span>
<button onClick={()=>onAccount&&onAccount()} aria-label="Account" style={{width:34,height:34,borderRadius:'50%',background:'var(--navy-100)',color:'var(--navy-800)',border:'none',cursor:'pointer',display:'flex',alignItems:'center',justifyContent:'center',fontFamily:'var(--font-display)',fontWeight:800,fontSize:13}}>JW</button>
</div></header>
<main style={{maxWidth:'var(--container-max)',margin:'0 auto',padding:'var(--space-8) var(--space-6)'}}>{children}</main>
</div>;}
Object.assign(window,{AppShell});
