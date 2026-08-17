const NSacct=window.GMATStudyGuideDesignSystem_efe656;
function Account({onNewProgram}){
const {Card,Button,Badge,Switch,Input}=NSacct;
return <div style={{maxWidth:'var(--container-narrow)',margin:'0 auto',display:'grid',gap:'var(--space-4)'}}>
<h1 style={{fontSize:'var(--text-2xl)',fontWeight:800}}>Account</h1>
<Card title="Profile">
<div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:14}}>
<Input label="First name" defaultValue="Jordan"/>
<Input label="Last name" defaultValue="Wells"/>
<Input label="Email" defaultValue="jordan@school.edu" hint="Used to sign in and sync progress" style={{gridColumn:'1 / -1'}}/>
</div>
<div style={{display:'flex',justifyContent:'flex-end',marginTop:16}}><Button size="sm" variant="secondary">Save changes</Button></div>
</Card>
<Card title="Study program" action={<Badge tone="info">Active</Badge>}>
<div style={{display:'grid',gap:8,fontSize:14}}>
<div style={{display:'flex',justifyContent:'space-between'}}><span style={{color:'var(--text-muted)'}}>Exam</span><strong style={{color:'var(--text-heading)'}}>GMAT</strong></div>
<div style={{display:'flex',justifyContent:'space-between'}}><span style={{color:'var(--text-muted)'}}>Goal</span><strong style={{color:'var(--text-heading)'}}>Score 675+ for M7 programs</strong></div>
<div style={{display:'flex',justifyContent:'space-between'}}><span style={{color:'var(--text-muted)'}}>Time budget</span><strong style={{color:'var(--text-heading)'}}>3–5 hrs / week</strong></div>
</div>
<div style={{display:'flex',gap:10,justifyContent:'flex-end',marginTop:16}}><Button size="sm" variant="ghost" onClick={onNewProgram}>Start another exam</Button><Button size="sm" variant="secondary">Edit program</Button></div>
</Card>
<Card title="Plan &amp; billing" action={<Badge tone="accent">Quarterly</Badge>}>
<div style={{display:'grid',gap:8,fontSize:14}}>
<div style={{display:'flex',justifyContent:'space-between'}}><span style={{color:'var(--text-muted)'}}>Price</span><strong style={{color:'var(--text-heading)',fontFamily:'var(--font-mono)'}}>$44.99 / 3 months</strong></div>
<div style={{display:'flex',justifyContent:'space-between'}}><span style={{color:'var(--text-muted)'}}>Renews</span><strong style={{color:'var(--text-heading)'}}>November 17, 2026</strong></div>
</div>
<div style={{display:'flex',gap:10,justifyContent:'flex-end',marginTop:16}}><Button size="sm" variant="ghost">Cancel plan</Button><Button size="sm" variant="secondary">Change plan</Button></div>
</Card>
<Card title="Notifications">
<div style={{display:'grid',gap:14}}>
<Switch label="Daily study reminder" defaultChecked/>
<Switch label="Weekly progress digest" defaultChecked/>
<Switch label="Product news" />
</div>
</Card>
<Card title="Privacy &amp; data">
<p style={{margin:0,fontSize:14,color:'var(--text-body)'}}>We store your answers, pace, and scores to power your adaptive plan. You can take a copy anytime or delete everything for good.</p>
<div style={{display:'flex',gap:10,justifyContent:'flex-end',marginTop:16}}><Button size="sm" variant="secondary">Download my data</Button><Button size="sm" variant="danger">Delete account</Button></div>
</Card>
</div>;}
Object.assign(window,{Account});
