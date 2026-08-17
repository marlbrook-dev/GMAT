function Dashboard({onStart,onNewProgram}){
const {Card,Button,Badge,ProgressBar,StatTile,Tabs}=window.GMATStudyGuideDesignSystem_efe656;
return <div style={{display:'grid',gap:'var(--space-6)'}}>
<div style={{display:'flex',alignItems:'flex-end',justifyContent:'space-between',gap:16}}>
<div><h1 style={{fontSize:'var(--text-2xl)',fontWeight:800}}>Good morning, Jordan</h1>
<p style={{margin:'6px 0 0',color:'var(--text-muted)'}}>Test day is in 34 days. You're on pace.</p></div>
<div style={{display:'flex',gap:12}}><Button variant="secondary" size="lg" onClick={onNewProgram}>New program</Button><Button size="lg" onClick={onStart}>Start today's round</Button></div>
</div>
<div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:'var(--space-4)'}}>
<StatTile label="Est. score" value="645" delta="+15"/>
<StatTile label="Accuracy" value="78%" delta="+2%"/>
<StatTile label="Questions today" value="14" delta="of 30" deltaTone="neutral"/>
<StatTile label="Avg. pace" value="1:52" delta="−0:08"/>
</div>
<div style={{display:'grid',gridTemplateColumns:'1.4fr 1fr',gap:'var(--space-4)',alignItems:'start'}}>
<Card title="Section mastery" action={<Badge tone="info">Adaptive</Badge>}>
<div style={{display:'grid',gap:'var(--space-4)'}}>
<ProgressBar label="Quantitative" value={62} color="var(--section-quant)"/>
<ProgressBar label="Verbal" value={71} color="var(--section-verbal)"/>
<ProgressBar label="Data Insights" value={44} color="var(--section-data)"/>
</div>
<p style={{margin:'16px 0 0',fontSize:13,color:'var(--text-muted)'}}>Data Insights is your weakest area — today's round leans into table analysis.</p>
</Card>
<Card title="Today's plan" action={<Badge tone="accent">Day 12</Badge>}>
<div style={{display:'grid',gap:10}}>
{[['Quick 10 · Quant','~12 min',true],['Timed sprint · Data Insights','~10 min',false],['Flashcards · Idioms','~5 min',false]].map(([t,d,done])=><div key={t} style={{display:'flex',alignItems:'center',gap:10,padding:'10px 12px',background:'var(--surface-sunken)',borderRadius:'var(--radius-md)'}}>
<span style={{width:18,height:18,borderRadius:'50%',flexShrink:0,border:done?'none':'1.5px solid var(--border-strong)',background:done?'var(--status-success)':'transparent',display:'inline-flex',alignItems:'center',justifyContent:'center'}}>{done&&<svg viewBox="0 0 24 24" width="11" height="11" style={{stroke:'#fff',fill:'none',strokeWidth:3.5,strokeLinecap:'round',strokeLinejoin:'round'}}><path d="m5 13 4 4L19 7"/></svg>}</span>
<span style={{flex:1,fontSize:14,fontWeight:500,color:done?'var(--text-muted)':'var(--text-heading)',textDecoration:done?'line-through':'none'}}>{t}</span>
<span style={{fontFamily:'var(--font-mono)',fontSize:12,color:'var(--text-muted)'}}>{d}</span>
</div>)}
</div>
</Card>
</div>
<div>
<h2 style={{fontSize:'var(--text-lg)',fontWeight:800,marginBottom:'var(--space-4)'}}>Games</h2>
<div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:'var(--space-4)'}}>
{[['Quick 10','Ten adaptive questions, no timer.','var(--section-quant)','var(--section-quant-bg)'],['Timed sprint','Beat the clock — 2 min per question.','var(--section-data)','var(--section-data-bg)'],['Flashcards','Flip through formulas and idioms.','var(--section-verbal)','var(--section-verbal-bg)'],['Mock section','Full 45-minute section, exam rules.','var(--gray-700)','var(--gray-100)']].map(([t,d,fg,bg])=><Card key={t} hoverable padding="var(--space-5)" onClick={onStart} style={{cursor:'pointer'}}>
<span style={{display:'inline-block',width:34,height:34,borderRadius:'var(--radius-md)',background:bg,marginBottom:12,position:'relative'}}><span style={{position:'absolute',inset:11,borderRadius:3,background:fg}}></span></span>
<div style={{fontFamily:'var(--font-display)',fontWeight:700,fontSize:15,color:'var(--text-heading)'}}>{t}</div>
<div style={{fontSize:13,color:'var(--text-muted)',marginTop:4}}>{d}</div>
</Card>)}
</div>
</div>
</div>;}
Object.assign(window,{Dashboard});
