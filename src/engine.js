// Adaptive engine: skill Elo, item selection, spaced repetition, timing flags. No UI dependencies.
const SKILLS = [
 {id:'q_rrp',section:'Q',label:'Rates / Ratios / Percent'},
 {id:'q_vof',section:'Q',label:'Value / Order / Factors'},
 {id:'q_alg',section:'Q',label:'Equalities / Inequalities / Algebra'},
 {id:'q_csp',section:'Q',label:'Counting / Sets / Series / Prob / Stats'},
 {id:'v_ac',section:'V',label:'Analysis / Critique'},
 {id:'v_pc',section:'V',label:'Plan / Construct'},
 {id:'v_inf',section:'V',label:'Identify Inferred Idea'},
 {id:'v_st',section:'V',label:'Identify Stated Idea'},
 {id:'di_ds',section:'DI',label:'Data Sufficiency'},
 {id:'di_gt',section:'DI',label:'Graphs and Tables'},
 {id:'di_msr',section:'DI',label:'Multi-Source Reasoning'},
 {id:'di_tpa',section:'DI',label:'Two-Part Analysis'}
];
const SECTION_META = {Q:{name:'Quantitative Reasoning',allot:128,questions:21},V:{name:'Verbal Reasoning',allot:117,questions:23},DI:{name:'Data Insights',allot:135,questions:20}};
// Exam registry. The engine is exam-agnostic: each exam supplies its own sections, skills and pacing; item banks carry exam ids.
// Adding an exam (SAT, GRE, LSAT...) = a new entry here + a tagged bank. Progress is stored per exam.
const EXAMS = { 'gmat-focus': {id:'gmat-focus',name:'GMAT Focus Edition',sections:SECTION_META,skills:SKILLS,scoreScale:'205-805',sectionScale:'60-90'} };
const CURRENT_EXAM='gmat-focus';
const DIFF_ELO = {1:800,2:950,3:1100,4:1250,5:1400};
const START_R = 1000, MASTERY_R = 1250;
const ERROR_REASONS = [
 {id:'concept',label:'Concept gap: did not know the rule or method'},
 {id:'setup',label:'Setup / translation: knew the math, built it wrong'},
 {id:'calc',label:'Calculation slip'},
 {id:'misread',label:'Misread the question or a choice'},
 {id:'timing',label:'Ran out of time / rushed'},
 {id:'guess',label:'Guessed'},
 {id:'trap',label:'Fell for a trap answer'}
];

function newState(){
 const skills={}; SKILLS.forEach(s=>{skills[s.id]={r:START_R,n:0,c:0,t:0,hist:[]};});
 return {version:2,exam:CURRENT_EXAM,created:Date.now(),skills,attempts:[],review:{},sessions:[],seen:{},settings:{name:'Hunter',testDate:'',dailyGoal:20}};
}
function expected(r,itemR){return 1/(1+Math.pow(10,(itemR-r)/400));}
function kFor(n){return n<10?32:(n<30?24:16);}

function updateSkill(state,skillId,itemR,correct,secs,weight){
 const s=state.skills[skillId]; if(!s) return;
 const e=expected(s.r,itemR); const k=kFor(s.n)*(weight||1);
 s.r=Math.round(s.r+k*((correct?1:0)-e)); s.n+=1; if(correct) s.c+=1; s.t+=secs;
 s.hist.push(s.r); if(s.hist.length>60) s.hist.shift();
}

function timingFlag(section,secs){
 const a=SECTION_META[section].allot; if(secs>1.3*a) return 'slow'; if(secs<0.6*a) return 'fast'; return 'ok';
}

// Record one attempt. chosen: index or [i,j] for TPA. reason: error reason id or null. guessed: bool.
function recordAttempt(state,q,chosen,correct,secs,reason,guessed,sessionId){
 const itemR=DIFF_ELO[q.diff]||1100;
 updateSkill(state,q.skill,itemR,correct,secs,1);
 if(q.qskill) updateSkill(state,q.qskill,itemR,correct,secs,0.5);
 const flag=timingFlag(q.section,secs);
 state.attempts.push({qid:q.id,skill:q.skill,section:q.section,diff:q.diff,correct,secs:Math.round(secs),flag,reason:reason||null,guessed:!!guessed,ts:Date.now(),sid:sessionId||null,chosen});
 state.seen[q.id]=(state.seen[q.id]||0)+1;
 // spaced repetition
 const day=86400000; const rv=state.review[q.id]||{interval:0,due:0,lapses:0};
 if(!correct||guessed||flag==='fast'&&!correct){ rv.interval=1; rv.due=Date.now()+day; rv.lapses+=1; state.review[q.id]=rv; }
 else if(state.review[q.id]){ rv.interval=rv.interval===0?1:Math.min(Math.round(rv.interval*2.5),30); rv.due=Date.now()+rv.interval*day; if(rv.interval>=14) delete state.review[q.id]; else state.review[q.id]=rv; }
 return flag;
}

function skillStats(state,id){
 const s=state.skills[id]; const acc=s.n?s.c/s.n:null; const avg=s.n?s.t/s.n:null;
 const trend=s.hist.length>=6?s.hist[s.hist.length-1]-s.hist[s.hist.length-6]:0;
 let status='untested'; if(s.n>0&&s.n<5) status='calibrating'; else if(s.n>0){ status = (s.r>=MASTERY_R&&s.n>=15&&acc>=0.75)?'green':(s.r>=1100?'amber':'red'); }
 return {r:s.r,n:s.n,acc,avg,trend,status};
}

// Question selection
function pickQuestions(bank,state,opts){
 opts=opts||{}; const count=opts.count||10; const sections=opts.sections||['Q','V','DI'];
 let pool=bank.filter(q=>sections.includes(q.section));
 if(opts.skills&&opts.skills.length) pool=pool.filter(q=>opts.skills.includes(q.skill)||(q.qskill&&opts.skills.includes(q.qskill)));
 if(opts.diffMin) pool=pool.filter(q=>q.diff>=opts.diffMin); if(opts.diffMax) pool=pool.filter(q=>q.diff<=opts.diffMax);
 if(opts.types&&opts.types.length) pool=pool.filter(q=>opts.types.includes(q.type));
 if(!pool.length) return [];
 const now=Date.now(); const chosen=[]; const used=new Set();
 const lastSeenIdx={}; state.attempts.forEach((a,i)=>{lastSeenIdx[a.qid]=i;});
 const recency=q=>lastSeenIdx[q.id]===undefined?1e9:(state.attempts.length-lastSeenIdx[q.id]);
 function addWithGroup(q){ if(used.has(q.id)) return;
   let group=[q];
   if(q.passageId) group=pool.filter(x=>x.passageId===q.passageId);
   else if(q.passageHtml&&['MSR','GI','TA'].includes(q.type)) group=pool.filter(x=>x.passageHtml===q.passageHtml&&x.type===q.type);
   group=group.filter(x=>!used.has(x.id)).sort((a,b)=>a.id<b.id?-1:1);
   group.forEach(x=>{ if(chosen.length<count||x.id===q.id){ used.add(x.id); chosen.push(x); } }); }
 if(opts.mode==='custom'){
   const sorted=pool.slice().sort((a,b)=>recency(b)-recency(a)||Math.random()-0.5);
   for(const q of sorted){ if(chosen.length>=count) break; addWithGroup(q); }
   return chosen.slice(0,count);
 }
 // adaptive
 const due=pool.filter(q=>state.review[q.id]&&state.review[q.id].due<=now).sort((a,b)=>state.review[a.id].due-state.review[b.id].due);
 const nReview=Math.min(due.length,Math.round(count*0.15)); for(let i=0;i<nReview;i++) addWithGroup(due[i]);
 const skillIds=[...new Set(pool.map(q=>q.skill))]; const ranked=skillIds.map(id=>({id,r:state.skills[id].r,n:state.skills[id].n})).sort((a,b)=>a.r-b.r||a.n-b.n);
 const untested=ranked.filter(s=>s.n<3).map(s=>s.id);
 if(untested.length>ranked.length/2){ // diagnostic mode: round-robin across under-sampled skills at difficulty 3
   let idx=0, guard=0; const order=untested.slice().sort(()=>Math.random()-0.5);
   while(chosen.length<count&&guard<300){ guard++; const sk=order[idx%order.length]; idx++;
     const cands=pool.filter(q=>!used.has(q.id)&&q.skill===sk).sort((a,b)=>Math.abs(a.diff-3)-Math.abs(b.diff-3)||recency(b)-recency(a)||Math.random()-0.5);
     if(cands.length) addWithGroup(cands[0]); }
   if(chosen.length>=count) return chosen.slice(0,count); }
 const weak=ranked.slice(0,3).map(s=>s.id); const mid=ranked.slice(3).map(s=>s.id);
 const nWeak=Math.round((count-chosen.length)*0.7);
 function bestFor(skillSet,n){ let added=0; let guard=0;
   while(added<n&&guard<200){ guard++;
     const cands=pool.filter(q=>!used.has(q.id)&&(skillSet.includes(q.skill)));
     if(!cands.length) break;
     const scored=cands.map(q=>{ const sk=state.skills[q.skill]; const target=sk.n<6?1100:sk.r-150; // calibrate at difficulty 3 first, then ~70% expected success
        const d=Math.abs(DIFF_ELO[q.diff]-target); const rec=recency(q); const fresh=rec>=1e9?0:Math.max(0,40-rec)*10; return {q,score:d+fresh+Math.random()*60}; }).sort((a,b)=>a.score-b.score);
     const before=chosen.length; addWithGroup(scored[0].q); added+=chosen.length-before; }
   return added; }
 bestFor(weak,nWeak); bestFor(mid.length?mid:weak,count-chosen.length);
 if(chosen.length<count) bestFor(skillIds,count-chosen.length);
 return chosen.slice(0,count);
}

function sectionSummary(state,section){
 const ids=SKILLS.filter(s=>s.section===section).map(s=>s.id); const st=ids.map(id=>skillStats(state,id));
 const tested=st.filter(x=>x.n>0); const meanR=tested.length?Math.round(tested.reduce((a,b)=>a+b.r,0)/tested.length):null;
 const n=st.reduce((a,b)=>a+b.n,0); const c=ids.reduce((a,id)=>a+state.skills[id].c,0);
 let band='Not yet tested'; if(meanR!==null){ band = meanR<950?'Building (below baseline)':meanR<1100?'Developing':meanR<1250?'Competitive':'Strong (target zone)'; }
 return {meanR,n,acc:n?c/n:null,band};
}

// Flashcards: Leitner boxes. know -> box+1 (due in 1,2,4,8,16 days); still learning -> box 0 (due in 10 minutes)
const BOX_DAYS=[0,1,2,4,8,16];
function cardState(state,id){ if(!state.cards) state.cards={}; return state.cards[id]||(state.cards[id]={box:0,due:0,seen:0,known:0}); }
function rateCard(state,id,know){ const c=cardState(state,id); c.seen++; if(know){ c.known++; c.box=Math.min(5,c.box+1); c.due=Date.now()+BOX_DAYS[c.box]*86400000; } else { c.box=0; c.due=Date.now()+10*60000; } return c; }
function dueCards(state,deck,sec){ const now=Date.now(); return deck.filter(c=>(!sec||sec==='ALL'||c.sec===sec)).filter(c=>{ const st=state.cards&&state.cards[c.id]; return !st||st.due<=now; }); }
