// Adaptive engine: skill Elo, item selection, spaced repetition, timing flags. No UI dependencies.
// Exam-agnostic: every exam supplies its own sections, skills and pacing through the registry
// near the bottom of this block. SKILLS and SECTION_META resolve to the active exam, so every
// function below reads whichever exam the page was built for.
const GMAT_SKILLS = [
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
const GMAT_SECTIONS = {
 Q:{name:'Quantitative Reasoning',short:'Quantitative',allot:128,questions:21,minutes:45},
 V:{name:'Verbal Reasoning',short:'Verbal',allot:117,questions:23,minutes:45},
 DI:{name:'Data Insights',short:'Data Insights',allot:135,questions:20,minutes:45}
};
// SAT skills are the eight official content domains. Labels and the skills listed under each
// come from College Board's "What Are Content Domains?" page; the question ranges come from
// Tables 2 and 3 of the Digital SAT Suite of Assessments Specifications Overview. Both are
// cited on the page and in data/DATA.md; nothing here is estimated.
const SAT_SKILLS = [
 {id:'rw_cs',section:'RW',label:'Craft and Structure',range:'13 to 15 questions',lo:13,hi:15,
  points:['Words in Context','Text Structure and Purpose','Cross-Text Connections']},
 {id:'rw_ii',section:'RW',label:'Information and Ideas',range:'12 to 14 questions',lo:12,hi:14,
  points:['Central Ideas and Details','Command of Evidence','Inferences']},
 {id:'rw_sec',section:'RW',label:'Standard English Conventions',range:'11 to 15 questions',lo:11,hi:15,
  points:['Boundaries','Form, Structure, and Sense']},
 {id:'rw_eoi',section:'RW',label:'Expression of Ideas',range:'8 to 12 questions',lo:8,hi:12,
  points:['Rhetorical Synthesis','Transitions']},
 {id:'m_alg',section:'M',label:'Algebra',range:'13 to 15 questions',lo:13,hi:15,
  points:['Linear equations in one variable','Linear equations in two variables','Linear functions','Systems of two linear equations','Linear inequalities']},
 {id:'m_adv',section:'M',label:'Advanced Math',range:'13 to 15 questions',lo:13,hi:15,
  points:['Equivalent expressions','Nonlinear equations in one variable','Systems of equations in two variables','Nonlinear functions']},
 {id:'m_psda',section:'M',label:'Problem-Solving and Data Analysis',range:'5 to 7 questions',lo:5,hi:7,
  points:['Ratios, rates, proportional relationships, and units','Percentages','One-variable data','Two-variable data: models and scatterplots','Probability and conditional probability','Inference from sample statistics and margin of error','Evaluating statistical claims']},
 {id:'m_geo',section:'M',label:'Geometry and Trigonometry',range:'5 to 7 questions',lo:5,hi:7,
  points:['Area and volume','Lines, angles, and triangles','Right triangles and trigonometry','Circles']}
];
// Digital SAT section shape: two equal modules per section, module 2 routed by module 1
// performance. Reading and Writing is 2 x 27 questions in 32 minutes each; Math is 2 x 22 in
// 35 minutes each (College Board, SAT test structure). allot is the per-question pace those
// module lengths imply, rounded to the second.
const SAT_SECTIONS = {
 RW:{name:'Reading and Writing',short:'Reading and Writing',allot:71,questions:27,minutes:32,modules:2,
     domainOrder:['rw_cs','rw_ii','rw_sec','rw_eoi']},
 M:{name:'Math',short:'Math',allot:95,questions:22,minutes:35,modules:2,
     domainOrder:['m_alg','m_adv','m_psda','m_geo']}
};
// Exam registry. Adding an exam (GRE, LSAT, ACT...) = a new entry here plus a tagged bank.
// Progress is stored per exam, so a student can train for two exams without the ratings mixing.
const EXAMS = {
 'gmat-focus': {id:'gmat-focus',name:'GMAT Focus Edition',short:'GMAT Focus',sections:GMAT_SECTIONS,skills:GMAT_SKILLS,
   scoreScale:'205-805',sectionScale:'60-90',choices:5,adaptive:'question'},
 'sat': {id:'sat',name:'SAT',short:'SAT',sections:SAT_SECTIONS,skills:SAT_SKILLS,
   scoreScale:'400-1600',sectionScale:'200-800',choices:4,adaptive:'module'}
};
// EXAM_ID is injected by the build (one app per exam). Node test runs default to the GMAT.
const CURRENT_EXAM = (typeof EXAM_ID !== 'undefined' && EXAMS[EXAM_ID]) ? EXAM_ID : 'gmat-focus';
const EXAM = EXAMS[CURRENT_EXAM];
const SKILLS = EXAM.skills;
const SECTION_META = EXAM.sections;
const SECTIONS = Object.keys(SECTION_META);
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
 opts=opts||{}; const count=opts.count||10; const sections=opts.sections||SECTIONS;
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

// Student-produced response (SAT grid-in): normalize what the student typed to a number so
// 1/2, 0.5 and .5 all match. Returns null when the entry is not a number or simple fraction.
function sprValue(raw){
 if(raw===null||raw===undefined) return null;
 let s=String(raw).trim().replace(/\s+/g,'');
 if(!s) return null;
 if(s.indexOf('/')>-1){ const parts=s.split('/'); if(parts.length!==2) return null;
  const a=Number(parts[0]), b=Number(parts[1]); if(!isFinite(a)||!isFinite(b)||b===0) return null; return a/b; }
 const n=Number(s); return isFinite(n)?n:null;
}
// SAT grid-ins accept any equivalent form, so compare values, not strings. Items may also list
// extra acceptable entries in `accept` (a second correct solution, for instance).
function gradeSpr(q,raw){
 const v=sprValue(raw); if(v===null) return false;
 const ok=[q.answer].concat(q.accept||[]);
 return ok.some(a=>{ const av=sprValue(a); return av!==null&&Math.abs(av-v)<1e-9; });
}

// Grade a chosen answer against a question, independent of any UI. chosen: index, [i,j] for TPA, array for GI/TA, typed string for SPR.
function gradeChosen(q,chosen){
 if(q.answerType==='spr') return gradeSpr(q,chosen);
 if(q.answerType==='tpa') return Array.isArray(chosen)&&chosen[0]===q.answer[0]&&chosen[1]===q.answer[1];
 if(q.answerType==='gi') return Array.isArray(chosen)&&chosen.every((v,i)=>v===q.statements[i].answer);
 if(q.answerType==='ta') return Array.isArray(chosen)&&chosen.every((v,i)=>v===q.statements[i].answer);
 return chosen===q.answer;
}

// Mock section: a representative fixed-length section, not a weakness-weighted round.
// Even coverage across the section's skills, difficulty centered near each skill's rating
// with a mild spread, passage/prompt groups kept intact, fresh items preferred.
function pickMockSection(bank,state,section,countOverride){
 const meta=SECTION_META[section]; const count=countOverride||meta.questions;
 const pool=bank.filter(q=>q.section===section);
 const skillIds=SKILLS.filter(s=>s.section===section).map(s=>s.id).filter(id=>pool.some(q=>q.skill===id));
 const lastSeenIdx={}; state.attempts.forEach((a,i)=>{lastSeenIdx[a.qid]=i;});
 const recency=q=>lastSeenIdx[q.id]===undefined?1e9:(state.attempts.length-lastSeenIdx[q.id]);
 const used=new Set(); const chosen=[];
 function groupOf(q){ let g=[q];
  if(q.passageId) g=pool.filter(x=>x.passageId===q.passageId);
  else if(q.passageHtml&&['MSR','GI','TA'].includes(q.type)) g=pool.filter(x=>x.passageHtml===q.passageHtml&&x.type===q.type);
  return g.filter(x=>!used.has(x.id)).sort((a,b)=>a.id<b.id?-1:1); }
 let idx=0, guard=0;
 while(chosen.length<count&&guard<400){ guard++;
  const sk=skillIds[idx%skillIds.length]; idx++;
  const cands=pool.filter(q=>!used.has(q.id)&&q.skill===sk);
  if(!cands.length) continue;
  const skR=state.skills[sk]?state.skills[sk].r:START_R;
  const spread=[0,120,-120][idx%3]; const target=Math.max(DIFF_ELO[1],Math.min(DIFF_ELO[5],skR+spread));
  const best=cands.map(q=>{ const d=Math.abs(DIFF_ELO[q.diff]-target); const rec=recency(q); const fresh=rec>=1e9?0:Math.max(0,40-rec)*10; return {q,score:d+fresh+Math.random()*80}; }).sort((a,b)=>a.score-b.score)[0].q;
  groupOf(best).forEach(x=>{ if(chosen.length<count){ used.add(x.id); chosen.push(x); } }); }
 if(chosen.length<count){ const rest=pool.filter(q=>!used.has(q.id)).sort((a,b)=>recency(b)-recency(a)||Math.random()-0.5);
  for(const q of rest){ if(chosen.length>=count) break; used.add(q.id); chosen.push(q); } }
 return chosen.slice(0,count);
}

function sectionSummary(state,section){
 const ids=SKILLS.filter(s=>s.section===section).map(s=>s.id); const st=ids.map(id=>skillStats(state,id));
 const tested=st.filter(x=>x.n>0); const meanR=tested.length?Math.round(tested.reduce((a,b)=>a+b.r,0)/tested.length):null;
 const n=st.reduce((a,b)=>a+b.n,0); const c=ids.reduce((a,id)=>a+state.skills[id].c,0);
 let band='Not yet tested'; if(meanR!==null){ band = meanR<950?'Building (below baseline)':meanR<1100?'Developing':meanR<1250?'Competitive':'Strong (target zone)'; }
 return {meanR,n,acc:n?c/n:null,band};
}

// ---------- SAT: two-module section with routing ----------
// The digital SAT delivers each section as two equal modules; performance on module 1 decides
// whether module 2 is the harder or the easier form (College Board, SAT test structure).
// College Board does not publish its routing threshold, so ours is our own and is labeled as
// such in the app: 60% or better on module 1 routes to the harder module.
const SAT_ROUTE_CUT = 0.6;
function satRoute(correct,total){ return total&&(correct/total)>=SAT_ROUTE_CUT?'upper':'lower'; }

// How many items of each domain belong in one module, from the official per-section ranges
// scaled to module length. Ranges live on each skill (lo/hi); we use the midpoint and then
// hand any rounding remainder to the largest domains, so the counts always sum to `count`.
function satDomainTargets(section,count){
 const meta=SECTION_META[section]; const ids=meta.domainOrder;
 const mids=ids.map(id=>{ const s=SKILLS.find(x=>x.id===id); return (s.lo+s.hi)/2; });
 const sum=mids.reduce((a,b)=>a+b,0);
 const raw=mids.map(m=>m/sum*count);
 const out=raw.map(x=>Math.floor(x));
 let left=count-out.reduce((a,b)=>a+b,0);
 const order=raw.map((x,i)=>({i,frac:x-Math.floor(x)})).sort((a,b)=>b.frac-a.frac);
 for(let k=0;k<left;k++) out[order[k%order.length].i]++;
 const t={}; ids.forEach((id,i)=>{t[id]=out[i];});
 return t;
}

// Build one SAT module. Module 1 spreads difficulty around each domain rating; module 2 is
// pulled up or down by the routing decision. Reading and Writing arrives in the official domain
// order (Craft and Structure, Information and Ideas, Standard English Conventions, Expression of
// Ideas) with each group easiest to hardest; Math is easiest to hardest across the module.
function pickSatModule(bank,state,section,moduleIdx,routing,countOverride){
 const meta=SECTION_META[section]; const count=countOverride||meta.questions;
 const pool=bank.filter(q=>q.section===section);
 if(!pool.length) return [];
 const targets=satDomainTargets(section,count);
 const lastSeenIdx={}; state.attempts.forEach((a,i)=>{lastSeenIdx[a.qid]=i;});
 const recency=q=>lastSeenIdx[q.id]===undefined?1e9:(state.attempts.length-lastSeenIdx[q.id]);
 const shift=moduleIdx===2?(routing==='upper'?200:-200):0;
 const used=new Set(); const picked=[];
 function take(skillId,n){
  let added=0, guard=0;
  while(added<n&&guard<200){ guard++;
   const cands=pool.filter(q=>!used.has(q.id)&&q.skill===skillId);
   if(!cands.length) break;
   const skR=state.skills[skillId]?state.skills[skillId].r:START_R;
   const spread=moduleIdx===2?0:[0,110,-110][added%3];
   const target=Math.max(DIFF_ELO[1],Math.min(DIFF_ELO[5],skR+shift+spread));
   const best=cands.map(q=>{ const d=Math.abs(DIFF_ELO[q.diff]-target); const rec=recency(q);
     const fresh=rec>=1e9?0:Math.max(0,40-rec)*10; return {q,score:d+fresh+Math.random()*70}; })
    .sort((a,b)=>a.score-b.score)[0].q;
   used.add(best.id); picked.push(best); added++; }
  return added;
 }
 meta.domainOrder.forEach(id=>take(id,targets[id]||0));
 // Short domains in a young bank leave gaps; fill from anything left in the section.
 if(picked.length<count){ const rest=pool.filter(q=>!used.has(q.id)).sort((a,b)=>recency(b)-recency(a)||Math.random()-0.5);
  for(const q of rest){ if(picked.length>=count) break; used.add(q.id); picked.push(q); } }
 const out=picked.slice(0,count);
 const rank={}; meta.domainOrder.forEach((id,i)=>{rank[id]=i;});
 if(section==='RW') out.sort((a,b)=>(rank[a.skill]-rank[b.skill])||(a.diff-b.diff)||(a.id<b.id?-1:1));
 else out.sort((a,b)=>(a.diff-b.diff)||(rank[a.skill]-rank[b.skill])||(a.id<b.id?-1:1));
 return out;
}

// Flashcards: Leitner boxes. know -> box+1 (due in 1,2,4,8,16 days); still learning -> box 0 (due in 10 minutes)
const BOX_DAYS=[0,1,2,4,8,16];
function cardState(state,id){ if(!state.cards) state.cards={}; return state.cards[id]||(state.cards[id]={box:0,due:0,seen:0,known:0}); }
function rateCard(state,id,know){ const c=cardState(state,id); c.seen++; if(know){ c.known++; c.box=Math.min(5,c.box+1); c.due=Date.now()+BOX_DAYS[c.box]*86400000; } else { c.box=0; c.due=Date.now()+10*60000; } return c; }
function dueCards(state,deck,sec){ const now=Date.now(); return deck.filter(c=>(!sec||sec==='ALL'||c.sec===sec)).filter(c=>{ const st=state.cards&&state.cards[c.id]; return !st||st.due<=now; }); }
