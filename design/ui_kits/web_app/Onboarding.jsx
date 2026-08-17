const EXAM_DATA={
'GMAT':{color:'var(--section-quant)',goals:['Score 675+ for M7 programs','Fix my Quant from the diagnostic','Balance all three sections','Retake — beat my 615'],tools:[['Quick 10','Adaptive daily rounds — the core loop',true],['Timed sprint','Pace training for Data Insights',true],['Flashcards','Idioms and formula recall',false],['Mock section','Full 45-minute exam-rules section',false]]},
'GRE':{color:'var(--section-verbal)',goals:['Score 325+ for PhD programs','Grow my Verbal vocab fast','Quant refresh after years out'],tools:[['Quick 10','Adaptive daily rounds',true],['Flashcards','Vocabulary decks — the GRE staple',true],['Timed sprint','Pace training',false],['Essay outliner','AWA structure drills',false]]},
'LSAT':{color:'var(--section-data)',goals:['Score 170+ for T14 schools','Master Logic Games','Speed up Reading Comp'],tools:[['Logic drills','Argument-pattern rounds',true],['Timed sprint','Section pacing',true],['Flashcards','Flaw types and conditionals',false],['Mock section','Full timed section',false]]},
'MCAT':{color:'var(--status-error)',goals:['Score 515+ for MD programs','CARS is my weak spot','Content review before practice'],tools:[['Quick 10','Adaptive daily rounds',true],['Flashcards','High-yield content recall',true],['CARS passages','Daily timed passage',true],['Mock section','Full-length section',false]]},
'Executive Assessment':{color:'var(--gold-600)',goals:['Hit 155+ for EMBA','Study around a full-time job'],tools:[['Quick 10','Adaptive daily rounds',true],['Timed sprint','IR pacing',true],['Flashcards','Formula recall',false]]}};
function FloatCard({style,children}){return <div aria-hidden="true" style={{position:'absolute',background:'var(--surface-card)',border:'1px solid var(--border-default)',borderRadius:'var(--radius-lg)',boxShadow:'var(--shadow-lg)',padding:16,opacity:.55,pointerEvents:'none',...style}}>{children}</div>;}
function Onboarding({open,onClose,onComplete}){
const NS=window.GMATStudyGuideDesignSystem_efe656;
const {Button}=NS;
const[step,setStep]=React.useState(0);
const[exam,setExam]=React.useState(null);
const[goal,setGoal]=React.useState('');
const[hours,setHours]=React.useState('3–5 hrs / week');
const[tools,setTools]=React.useState({});
const[first,setFirst]=React.useState('');
const[last,setLast]=React.useState('');
const[email,setEmail]=React.useState('');
const[consent,setConsent]=React.useState(false);
const[plan,setPlan]=React.useState('Quarterly');
React.useEffect(()=>{if(exam){const t={};EXAM_DATA[exam].tools.forEach(([n,,on])=>t[n]=on);setTools(t);}},[exam]);
React.useEffect(()=>{const onKey=(e)=>{if(e.key==='Escape')onClose();};if(open){document.addEventListener('keydown',onKey);return()=>document.removeEventListener('keydown',onKey);}},[open]);
if(!open)return null;
const d=exam?EXAM_DATA[exam]:null;
const suggestions=d?d.goals.filter(g=>!goal||g.toLowerCase().includes(goal.toLowerCase())||goal.length<3).slice(0,4):[];
const total=6;
const acctOk=first.trim().length>0&&email.includes('@')&&consent;
const canNext=[true,!!exam,goal.trim().length>0,true,true,acctOk,true][step];
const finish=()=>onComplete({exam:exam||'GMAT',goal:goal||(d?d.goals[0]:''),hours,tools,account:{first,last,email,consent},plan});
const chip=(active)=>({fontFamily:'var(--font-display)',fontWeight:600,fontSize:14,color:active?'#fff':'var(--text-heading)',background:active?'var(--brand-primary)':'var(--surface-card)',border:'1px solid '+(active?'var(--brand-primary)':'var(--border-strong)'),borderRadius:999,padding:'9px 18px',cursor:'pointer',transition:'background var(--duration-fast) var(--ease-out),border-color var(--duration-fast) var(--ease-out)'});
const sugLabel=<span style={{display:'inline-flex',alignItems:'center',gap:7}}><img src="../../assets/logo.svg" width="16" height="16" alt=""/><span style={{fontFamily:'var(--font-display)',fontWeight:700,fontSize:13,color:'var(--text-heading)'}}>Suggestions</span></span>;
return <div style={{position:'fixed',inset:0,background:'var(--navy-50)',zIndex:'var(--z-modal)',overflow:'auto',isolation:'isolate'}}>
<FloatCard style={{top:'14%',left:'4%',width:150,transform:'rotate(-5deg)'}}><div style={{fontFamily:'var(--font-mono)',fontSize:22,color:'var(--navy-800)'}}>645</div><div style={{height:6,background:'var(--surface-sunken)',borderRadius:999,marginTop:8}}><div style={{width:'62%',height:'100%',background:'var(--gold-500)',borderRadius:999}}></div></div><div style={{height:6,background:'var(--surface-sunken)',borderRadius:999,marginTop:6}}><div style={{width:'40%',height:'100%',background:'var(--section-quant)',borderRadius:999}}></div></div></FloatCard>
<FloatCard style={{bottom:'12%',left:'9%',width:170,transform:'rotate(4deg)'}}><div style={{fontFamily:'var(--font-serif-display)',fontWeight:700,fontSize:14,color:'var(--navy-900)'}}>Weighted average</div><div style={{fontSize:11,color:'var(--text-muted)',marginTop:6}}>The mean leans toward the larger group…</div></FloatCard>
<FloatCard style={{top:'18%',right:'5%',width:160,transform:'rotate(5deg)'}}><div style={{display:'flex',gap:8,alignItems:'center'}}><span style={{width:22,height:22,borderRadius:6,background:'var(--brand-primary)',color:'#fff',display:'inline-flex',alignItems:'center',justifyContent:'center',fontFamily:'var(--font-display)',fontWeight:700,fontSize:11}}>B</span><span style={{fontSize:12,color:'var(--text-heading)'}}>x = 12</span></div><div style={{display:'flex',gap:8,alignItems:'center',marginTop:8}}><span style={{width:22,height:22,borderRadius:6,background:'var(--surface-sunken)',display:'inline-flex',alignItems:'center',justifyContent:'center',fontFamily:'var(--font-display)',fontWeight:700,fontSize:11,color:'var(--text-body)'}}>C</span><span style={{fontSize:12,color:'var(--text-muted)'}}>x = 14</span></div></FloatCard>
<FloatCard style={{bottom:'16%',right:'8%',width:150,transform:'rotate(-4deg)'}}><div style={{fontFamily:'var(--font-mono)',fontSize:18,color:'var(--navy-800)'}}>01:47</div><div style={{fontSize:11,color:'var(--text-muted)',marginTop:4}}>12 / 20 correct</div></FloatCard>
<div style={{position:'relative',display:'flex',alignItems:'center',justifyContent:'space-between',padding:'22px 36px'}}>
<span style={{display:'flex',alignItems:'center',gap:9}}><img src="../../assets/logo.svg" width="26" height="26" alt=""/><span style={{fontFamily:'var(--font-serif-display)',fontWeight:700,fontSize:18,color:'var(--navy-900)'}}>Meridian <span style={{color:'var(--gold-600)'}}>Prep</span></span></span>
<button onClick={onClose} style={{border:'none',background:'none',cursor:'pointer',fontFamily:'var(--font-display)',fontWeight:700,fontSize:14,color:'var(--text-heading)'}}>Skip to dashboard →</button>
</div>
<div style={{position:'relative',maxWidth:760,margin:'4vh auto 40px',padding:'0 24px'}}>
<div role="dialog" aria-modal="true" aria-label="Start a new study program" style={{background:'var(--surface-card)',borderRadius:'var(--radius-lg)',boxShadow:'var(--shadow-lg)',padding:'0 0 28px',overflow:'hidden'}}>
{step>0&&<div style={{padding:'28px 56px 0'}}><div style={{height:3,background:'var(--gray-200)',borderRadius:999}}><div style={{height:'100%',width:(step/total*100)+'%',background:'var(--brand-primary)',borderRadius:999,transition:'width var(--duration-base) var(--ease-out)'}}></div></div></div>}
<div style={{padding:'40px 56px 8px',textAlign:'center',minHeight:330}}>
{step===0&&<div style={{paddingTop:24}}>
<img src="../../assets/logo.svg" width="48" height="48" alt=""/>
<h1 style={{fontSize:36,marginTop:20,textWrap:'pretty'}}>Let's build your study program</h1>
<p style={{fontSize:16,color:'var(--text-muted)',maxWidth:440,margin:'14px auto 0'}}>Answer a few questions in your own words and get a plan that fits your exam, your goal, and your schedule.</p>
<div style={{display:'flex',gap:18,justifyContent:'center',alignItems:'center',marginTop:32}}>
<Button size="lg" onClick={()=>setStep(1)}>Let's go</Button>
<button onClick={finish} style={{border:'none',background:'none',cursor:'pointer',fontFamily:'var(--font-display)',fontWeight:700,fontSize:15,color:'var(--text-heading)',textDecoration:'underline'}}>Skip the questions</button>
</div>
</div>}
{step===1&&<div>
<h1 style={{fontSize:34,marginTop:24}}>First, which exam is it?</h1>
<p style={{fontSize:14,color:'var(--text-muted)',margin:'10px 0 0'}}>Sections, games, and the score model all adjust to your exam.</p>
<div style={{display:'flex',gap:10,justifyContent:'center',flexWrap:'wrap',marginTop:28,maxWidth:520,marginLeft:'auto',marginRight:'auto'}}>
{Object.keys(EXAM_DATA).map(name=><button key={name} onClick={()=>setExam(name)} aria-pressed={exam===name} style={chip(exam===name)}>{name}</button>)}
</div>
</div>}
{step===2&&<div>
<h1 style={{fontSize:34,marginTop:24}}>What are your goals?</h1>
<input autoFocus value={goal} onChange={e=>setGoal(e.target.value)} placeholder={'Enter or select your goal'} style={{width:'100%',maxWidth:560,boxSizing:'border-box',font:'inherit',fontSize:16,color:'var(--text-heading)',border:'1.5px solid var(--border-strong)',borderRadius:'var(--radius-md)',padding:'14px 18px',marginTop:28,outline:'none',textAlign:'left'}} onFocus={e=>{e.target.style.borderColor='var(--brand-primary)';e.target.style.boxShadow='var(--focus-ring)';}} onBlur={e=>{e.target.style.borderColor='var(--border-strong)';e.target.style.boxShadow='none';}}/>
<div style={{maxWidth:560,margin:'20px auto 0',textAlign:'left'}}>
{sugLabel}
<div style={{display:'flex',gap:8,flexWrap:'wrap',marginTop:12}}>
{suggestions.map(s=><button key={s} onClick={()=>setGoal(s)} style={{fontFamily:'var(--font-display)',fontWeight:600,fontSize:13,color:'var(--text-heading)',background:'var(--surface-card)',border:'1px solid var(--border-strong)',borderRadius:999,padding:'7px 14px',cursor:'pointer'}}>{s}</button>)}
</div>
<p style={{fontSize:12,color:'var(--text-muted)',marginTop:14}}>Suggestions come from goals of {exam} students with similar diagnostics.</p>
</div>
</div>}
{step===3&&<div>
<h1 style={{fontSize:34,marginTop:24}}>How much time can you give it?</h1>
<p style={{fontSize:14,color:'var(--text-muted)',margin:'10px 0 0'}}>Honest beats ambitious — the plan rebuilds itself if life gets in the way.</p>
<div style={{display:'flex',gap:10,justifyContent:'center',flexWrap:'wrap',marginTop:28}}>
{['Under 3 hrs / week','3–5 hrs / week','6–10 hrs / week','10+ hrs / week'].map(h=><button key={h} onClick={()=>setHours(h)} aria-pressed={hours===h} style={chip(hours===h)}>{h}</button>)}
</div>
</div>}
{step===4&&<div>
<h1 style={{fontSize:34,marginTop:24,textWrap:'pretty'}}>Add tools to reach your goal</h1>
<p style={{fontSize:14,color:'var(--text-muted)',margin:'10px 0 0'}}>You can add or remove them later.</p>
<div style={{maxWidth:560,margin:'22px auto 0',textAlign:'left'}}>
{d.tools.map(([name,why])=><button key={name} onClick={()=>setTools({...tools,[name]:!tools[name]})} aria-pressed={!!tools[name]} style={{display:'flex',alignItems:'center',gap:14,width:'100%',textAlign:'left',padding:'15px 4px',background:'none',border:'none',borderBottom:'1px solid var(--border-default)',cursor:'pointer'}}>
<span style={{width:19,height:19,borderRadius:'var(--radius-sm)',flexShrink:0,border:tools[name]?'none':'1.5px solid var(--border-strong)',background:tools[name]?'var(--brand-primary)':'transparent',display:'inline-flex',alignItems:'center',justifyContent:'center',transition:'background var(--duration-fast) var(--ease-out)'}}>{tools[name]&&<svg viewBox="0 0 24 24" width="12" height="12" style={{stroke:'#fff',fill:'none',strokeWidth:3.5,strokeLinecap:'round',strokeLinejoin:'round'}}><path d="m5 13 4 4L19 7"/></svg>}</span>
<span style={{fontSize:15,color:'var(--text-body)'}}><strong style={{fontFamily:'var(--font-display)',fontWeight:700,color:'var(--text-heading)'}}>{name}</strong> — {why}</span>
</button>)}
</div>
</div>}
{step===5&&<div>
<h1 style={{fontSize:34,marginTop:24}}>Create your account</h1>
<p style={{fontSize:14,color:'var(--text-muted)',margin:'10px 0 0'}}>Basic info for your account and study personalization.</p>
<div style={{maxWidth:400,margin:'24px auto 0',display:'grid',gap:14,textAlign:'left'}}>
<div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12}}>
<label style={{display:'grid',gap:6}}><span style={{fontSize:13,fontWeight:600,color:'var(--text-heading)'}}>First name</span><input value={first} onChange={e=>setFirst(e.target.value)} style={{font:'inherit',fontSize:15,color:'var(--text-heading)',border:'1.5px solid var(--border-strong)',borderRadius:'var(--radius-md)',padding:'10px 12px',outline:'none'}}/></label>
<label style={{display:'grid',gap:6}}><span style={{fontSize:13,fontWeight:600,color:'var(--text-heading)'}}>Last name</span><input value={last} onChange={e=>setLast(e.target.value)} style={{font:'inherit',fontSize:15,color:'var(--text-heading)',border:'1.5px solid var(--border-strong)',borderRadius:'var(--radius-md)',padding:'10px 12px',outline:'none'}}/></label>
</div>
<label style={{display:'grid',gap:6}}><span style={{fontSize:13,fontWeight:600,color:'var(--text-heading)'}}>Email</span><input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@school.edu" style={{font:'inherit',fontSize:15,color:'var(--text-heading)',border:'1.5px solid var(--border-strong)',borderRadius:'var(--radius-md)',padding:'10px 12px',outline:'none'}}/></label>
<label style={{display:'flex',alignItems:'flex-start',gap:10,cursor:'pointer',fontSize:13,color:'var(--text-body)'}} onClick={()=>setConsent(!consent)}>
<span style={{width:18,height:18,marginTop:1,borderRadius:'var(--radius-sm)',flexShrink:0,border:consent?'none':'1.5px solid var(--border-strong)',background:consent?'var(--brand-primary)':'transparent',display:'inline-flex',alignItems:'center',justifyContent:'center'}}>{consent&&<svg viewBox="0 0 24 24" width="11" height="11" style={{stroke:'#fff',fill:'none',strokeWidth:3.5,strokeLinecap:'round',strokeLinejoin:'round'}}><path d="m5 13 4 4L19 7"/></svg>}</span>
<span>I agree to the <a href="../website/terms.html" target="_blank" onClick={e=>e.stopPropagation()}>Terms of Use</a> and <a href="#" onClick={e=>{e.preventDefault();e.stopPropagation();}}>Privacy Policy</a></span>
</label>
<p style={{display:'flex',gap:8,fontSize:12,color:'var(--text-muted)',margin:'4px 0 0'}}><svg viewBox="0 0 24 24" width="14" height="14" style={{stroke:'var(--gold-600)',fill:'none',strokeWidth:2,strokeLinecap:'round',strokeLinejoin:'round',flexShrink:0}}><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg><span><strong style={{color:'var(--text-heading)'}}>Your data is safe with us.</strong> Email creates your account and syncs progress across devices.</span></p>
</div>
</div>}
{step===6&&<div>
<h1 style={{fontSize:34,marginTop:24}}>Choose your plan</h1>
<p style={{fontSize:14,color:'var(--text-muted)',margin:'10px 0 0'}}>Study when and how you want. Cancel anytime.</p>
<div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:14,maxWidth:600,margin:'26px auto 0'}}>
{[['Monthly','$19.99','$19.99/mo · billed monthly',null],['Quarterly','$44.99','$15.00/mo · billed every 3 months','Save 25%'],['Annual','$119.99','$10.00/mo · billed annually','Save 50%']].map(([name,price,detail,save])=><button key={name} onClick={()=>setPlan(name)} aria-pressed={plan===name} style={{position:'relative',textAlign:'center',padding:'22px 14px 18px',borderRadius:'var(--radius-lg)',cursor:'pointer',background:plan===name?'var(--brand-primary-soft)':'var(--surface-card)',border:'1.5px solid '+(plan===name?'var(--brand-primary)':'var(--border-default)'),transition:'border-color var(--duration-fast) var(--ease-out)'}}>
{save&&<span style={{position:'absolute',top:-10,left:'50%',transform:'translateX(-50%)',fontFamily:'var(--font-display)',fontWeight:700,fontSize:11,color:'var(--navy-900)',background:'var(--gold-500)',borderRadius:999,padding:'2px 10px',whiteSpace:'nowrap'}}>{save}</span>}
<span style={{display:'block',fontFamily:'var(--font-display)',fontWeight:700,fontSize:15,color:'var(--text-heading)'}}>{name}</span>
<span style={{display:'block',fontFamily:'var(--font-mono)',fontSize:24,color:'var(--navy-800)',marginTop:6}}>{price}</span>
<span style={{display:'block',fontSize:11,color:'var(--text-muted)',marginTop:6}}>{detail}</span>
</button>)}
</div>
<p style={{fontSize:13,marginTop:20}}><a href="#" onClick={e=>e.preventDefault()}>Or try your first 20 questions free</a> — no card required.</p>
</div>}
</div>
{step>0&&<div style={{display:'flex',alignItems:'center',justifyContent:'space-between',padding:'18px 56px 0'}}>
<button onClick={()=>setStep(step-1)} style={{border:'none',background:'none',cursor:'pointer',fontFamily:'var(--font-display)',fontWeight:700,fontSize:15,color:'var(--text-heading)',display:'inline-flex',alignItems:'center',gap:6}}><svg viewBox="0 0 24 24" width="14" height="14" style={{stroke:'currentColor',fill:'none',strokeWidth:2.5,strokeLinecap:'round',strokeLinejoin:'round'}}><path d="m15 18-6-6 6-6"/></svg>Back</button>
<div style={{display:'flex',alignItems:'center',gap:22}}>
{step<6&&step!==5&&<button onClick={()=>setStep(step+1)} style={{border:'none',background:'none',cursor:'pointer',fontFamily:'var(--font-display)',fontWeight:700,fontSize:15,color:'var(--text-muted)'}}>Skip</button>}
{step<6?<Button disabled={!canNext} onClick={()=>setStep(step+1)}>Continue</Button>:<Button onClick={finish}>Start studying</Button>}
</div>
</div>}
</div>
<p style={{textAlign:'center',fontSize:12,color:'var(--text-muted)',marginTop:18}}>Assist can make mistakes — your plan stays fully editable.</p>
</div>
</div>;}
Object.assign(window,{Onboarding,EXAM_DATA});
