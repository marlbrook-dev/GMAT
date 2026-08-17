function Results({score,total,onRetry,onHome}){
const {Card,Button,Badge,StatTile,ProgressBar}=window.GMATStudyGuideDesignSystem_efe656;
const pct=Math.round((score/total)*100);
return <div style={{maxWidth:'var(--container-narrow)',margin:'0 auto',display:'grid',gap:'var(--space-6)'}}>
<div style={{textAlign:'center'}}>
<div style={{fontFamily:'var(--font-mono)',fontSize:56,fontWeight:500,color:'var(--brand-primary)'}}>{score} / {total}</div>
<h1 style={{fontSize:'var(--text-xl)',fontWeight:800,marginTop:4}}>{pct>=67?'Strong round.':'Good reps — keep going.'}</h1>
<p style={{margin:'6px 0 0',color:'var(--text-muted)'}}>Quick 10 · Quant &amp; Data Insights · 5 min 12 sec</p>
</div>
<div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'var(--space-4)'}}>
<StatTile label="Accuracy" value={pct+'%'}/>
<StatTile label="Avg. pace" value="1:44" delta="−0:08"/>
<StatTile label="Est. score" value="645" delta="+5"/>
</div>
<Card title="This round">
<div style={{display:'grid',gap:8}}>
{window.BANK.map((q,idx)=><div key={idx} style={{display:'flex',alignItems:'center',gap:12,padding:'10px 12px',background:'var(--surface-sunken)',borderRadius:'var(--radius-md)'}}>
<span style={{fontFamily:'var(--font-mono)',fontSize:12,color:'var(--text-muted)',width:18}}>{idx+1}</span>
<span style={{flex:1,fontSize:14,color:'var(--text-heading)',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{q.q}</span>
<Badge tone="neutral">{q.tag}</Badge>
<Badge tone={idx<2?'success':'error'}>{idx<2?'Correct':'Missed'}</Badge>
</div>)}
</div>
</Card>
<div style={{display:'flex',justifyContent:'center',gap:'var(--space-3)'}}>
<Button variant="secondary" onClick={onHome}>Back to dashboard</Button>
<Button onClick={onRetry}>Practice again</Button>
</div>
</div>;}
Object.assign(window,{Results});
