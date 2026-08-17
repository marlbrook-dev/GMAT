const BANK=[
{section:'Quantitative',tag:'Algebra',q:'If 3x − 7 = 2x + 5, what is the value of x?',opts:['x = 8','x = 10','x = 12','x = 14'],correct:2,explain:'Subtract 2x from both sides: x − 7 = 5, so x = 12.'},
{section:'Quantitative',tag:'Arithmetic',q:'A store marks up an item 25% and then discounts it 20%. The final price is what percent of the original?',opts:['95%','100%','102.5%','105%'],correct:1,explain:'1.25 × 0.80 = 1.00 — exactly the original price.'},
{section:'Data Insights',tag:'Data Sufficiency',q:'Is n even? (1) 3n is even. (2) n + 2 is even.',opts:['Statement 1 alone is sufficient','Statement 2 alone is sufficient','Each alone is sufficient','Both together are needed'],correct:2,explain:'If 3n is even, n is even. If n + 2 is even, n is even. Each works alone.'}];
function Practice({onFinish,onExit}){
const {Card,Button,Badge,ProgressBar,QuizOption}=window.GMATStudyGuideDesignSystem_efe656;
const[i,setI]=React.useState(0);
const[sel,setSel]=React.useState(null);
const[revealed,setRevealed]=React.useState(false);
const[score,setScore]=React.useState(0);
const q=BANK[i];
const next=()=>{if(i+1>=BANK.length){onFinish(score+(revealed&&sel===q.correct?0:0));}else{setI(i+1);setSel(null);setRevealed(false);}};
const submit=()=>{setRevealed(true);if(sel===q.correct)setScore(score+1);};
return <div style={{maxWidth:'var(--container-narrow)',margin:'0 auto',display:'grid',gap:'var(--space-4)'}}>
<div style={{display:'flex',alignItems:'center',gap:16}}>
<Badge tone={q.section==='Quantitative'?'success':'info'}>{q.section}</Badge>
<Badge tone="neutral">{q.tag}</Badge>
<div style={{flex:1}}><ProgressBar value={i+(revealed?1:0)} max={BANK.length} height={6}/></div>
<span style={{fontFamily:'var(--font-mono)',fontSize:14,color:'var(--text-muted)'}}>{i+1} / {BANK.length}</span>
<span style={{fontFamily:'var(--font-mono)',fontSize:14,fontWeight:500,color:'var(--text-heading)',background:'var(--surface-sunken)',padding:'4px 10px',borderRadius:'var(--radius-sm)'}}>01:47</span>
</div>
<Card padding="var(--space-8)">
<div style={{fontFamily:'var(--font-display)',fontWeight:700,fontSize:'var(--text-lg)',color:'var(--text-heading)',lineHeight:1.4,marginBottom:'var(--space-6)'}}>{q.q}</div>
<div style={{display:'grid',gap:10}}>
{q.opts.map((o,idx)=><QuizOption key={o} letter={'ABCD'[idx]} state={revealed?(idx===q.correct?'correct':idx===sel?'incorrect':'idle'):(idx===sel?'selected':'idle')} onClick={()=>!revealed&&setSel(idx)}>{o}</QuizOption>)}
</div>
{revealed&&<div style={{marginTop:'var(--space-5)',padding:'12px 14px',background:'var(--surface-sunken)',borderRadius:'var(--radius-md)',fontSize:14,color:'var(--text-body)'}}><strong style={{color:'var(--text-heading)'}}>Why:</strong> {q.explain}</div>}
<div style={{display:'flex',justifyContent:'space-between',marginTop:'var(--space-6)'}}>
<Button variant="ghost" onClick={onExit}>Exit round</Button>
{revealed?<Button onClick={next}>{i+1>=BANK.length?'See results':'Next question'}</Button>:<Button disabled={sel===null} onClick={submit}>Submit answer</Button>}
</div>
</Card>
</div>;}
Object.assign(window,{Practice,BANK});
