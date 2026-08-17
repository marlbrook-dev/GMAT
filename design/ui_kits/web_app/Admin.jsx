const NSadm=window.GMATStudyGuideDesignSystem_efe656;
const EVENTS=[
['3:42 pm','u_18h2','round_completed','{exam:"GMAT", mode:"quick10", correct:8, secs:641}'],
['3:41 pm','u_2c91','question_answered','{qid:"ds_114", correct:false, secs:118}'],
['3:39 pm','u_9ak2','plan_selected','{plan:"quarterly", trial:false}'],
['3:38 pm','u_9ak2','account_created','{exam:"LSAT", source:"organic"}'],
['3:35 pm','u_77fe','round_started','{exam:"GRE", mode:"flashcards"}'],
['3:31 pm','u_18h2','wizard_completed','{exam:"GMAT", hours:"3-5", tools:3}']];
function Admin(){
const {Card,Button,Badge,Switch,Input,StatTile,Tabs}=NSadm;
return <div style={{display:'grid',gap:'var(--space-6)'}}>
<div style={{display:'flex',alignItems:'center',gap:12,background:'var(--brand-accent-soft)',border:'1px solid var(--gold-100)',borderRadius:'var(--radius-md)',padding:'10px 14px'}}>
<span style={{width:8,height:8,borderRadius:'50%',background:'var(--gold-600)'}}></span>
<span style={{fontFamily:'var(--font-display)',fontWeight:700,fontSize:13,color:'var(--gold-700)'}}>Owner view — users never see this. Changes publish instantly.</span>
</div>
<div style={{display:'flex',alignItems:'flex-end',justifyContent:'space-between'}}>
<div><h1 style={{fontSize:'var(--text-2xl)',fontWeight:800}}>Command center</h1><p style={{margin:'6px 0 0',color:'var(--text-muted)'}}>Last 7 days · all exams</p></div>
<Button variant="secondary">Export CSV</Button>
</div>
<div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:'var(--space-4)'}}>
<StatTile label="Signups" value="1,284" delta="+12%"/>
<StatTile label="Daily active" value="4,102" delta="+5%"/>
<StatTile label="Round completion" value="87%" delta="+1%"/>
<StatTile label="Free → paid" value="6.4%" delta="−0.3%" deltaTone="error"/>
</div>
<div style={{display:'grid',gridTemplateColumns:'1.5fr 1fr',gap:'var(--space-4)',alignItems:'start'}}>
<Card title="Live events" action={<Badge tone="success">Streaming</Badge>}>
<div style={{display:'grid',gap:6}}>
{EVENTS.map(([t,u,ev,props],i)=><div key={i} style={{display:'flex',alignItems:'center',gap:12,padding:'8px 10px',background:'var(--surface-sunken)',borderRadius:'var(--radius-sm)',fontFamily:'var(--font-mono)',fontSize:12}}>
<span style={{color:'var(--text-muted)',width:56,flexShrink:0}}>{t}</span>
<span style={{color:'var(--text-muted)',width:52,flexShrink:0}}>{u}</span>
<span style={{color:'var(--navy-800)',fontWeight:500,width:130,flexShrink:0}}>{ev}</span>
<span style={{color:'var(--text-muted)',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{props}</span>
</div>)}
</div>
<p style={{fontSize:12,color:'var(--text-muted)',margin:'12px 0 0'}}>Full schema in guidelines/data-analytics.md — every event, its properties, and retention rules.</p>
</Card>
<Card title="Site settings">
<div style={{display:'grid',gap:14}}>
<Switch label="Guarantee banner" defaultChecked/>
<Switch label="New-user wizard" defaultChecked/>
<Switch label="Promo pricing" />
<Input label="Banner text" defaultValue="Built for the current GMAT (Focus Edition) · 70-point improvement guarantee"/>
<Input label="Monthly price (USD)" defaultValue="19.99"/>
<div style={{display:'flex',justifyContent:'flex-end'}}><Button size="sm">Publish</Button></div>
</div>
</Card>
</div>
<Card title="Question bank" action={<Button size="sm" variant="secondary">Add question</Button>}>
<div style={{display:'grid',gap:6}}>
{[['ds_114','Is n even? (1) 3n is even…','Data Insights','Data Sufficiency','62% correct'],['al_078','If 3x − 7 = 2x + 5…','Quantitative','Algebra','81% correct'],['cr_201','The columnist argues that…','Verbal','Critical Reasoning','54% correct']].map(([id,q,section,tag,rate])=><div key={id} style={{display:'flex',alignItems:'center',gap:12,padding:'10px 12px',background:'var(--surface-sunken)',borderRadius:'var(--radius-md)'}}>
<span style={{fontFamily:'var(--font-mono)',fontSize:12,color:'var(--text-muted)',width:52,flexShrink:0}}>{id}</span>
<span style={{flex:1,fontSize:14,color:'var(--text-heading)',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{q}</span>
<Badge tone={section==='Quantitative'?'info':section==='Verbal'?'accent':'neutral'}>{tag}</Badge>
<span style={{fontFamily:'var(--font-mono)',fontSize:12,color:'var(--text-muted)',flexShrink:0}}>{rate}</span>
<Button size="sm" variant="ghost">Edit</Button>
</div>)}
</div>
</Card>
</div>;}
Object.assign(window,{Admin});
