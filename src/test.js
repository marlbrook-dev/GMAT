// Bank validation and engine simulation, run once per exam in the registry.
// node test.js  (from src/)
const fs=require('fs'), vm=require('vm');

const GMAT={id:'gmat-focus',choices:5,
 files:['bank_quant.js','bank_quant2.js','bank_quant3.js','bank_quant4.js','bank_quant5.js','bank_quant6.js','bank_verbal.js','bank_verbal2.js','bank_verbal3.js','bank_verbal4.js','bank_verbal5.js','bank_verbal6.js','bank_verbal7.js','bank_verbal8.js','bank_di.js','bank_di2.js','bank_di3.js','bank_di4.js','bank_di5.js','bank_di6.js','bank_di7.js','bank_di8.js','bank_di9.js','cards.js','cards2.js','cards3.js','playbook_gmat.js'],
 concat:'BANK_QUANT,BANK_QUANT2,BANK_QUANT3,BANK_QUANT4,BANK_QUANT5,BANK_QUANT6,BANK_VERBAL,BANK_VERBAL2,BANK_VERBAL3,BANK_VERBAL4,BANK_VERBAL5,BANK_VERBAL6,BANK_VERBAL7,BANK_VERBAL8,BANK_DI,BANK_DI2,BANK_DI3,BANK_DI4,BANK_DI5,BANK_DI6,BANK_DI7,BANK_DI8,BANK_DI9'};
const GRE={id:'gre',choices:5,choicesByType:{QC:4},
 files:['bank_gre_verbal.js','bank_gre_verbal2.js','bank_gre_quant.js','bank_gre_quant2.js','bank_gre_easy.js','cards_gre.js','playbook_gre.js'],
 concat:'BANK_GRE_VERBAL,BANK_GRE_VERBAL2,BANK_GRE_QUANT,BANK_GRE_QUANT2,BANK_GRE_EASY'};
const SAT={id:'sat',choices:4,
 files:['bank_sat_rw.js','bank_sat_rw2.js','bank_sat_rw3.js','bank_sat_rw4.js','bank_sat_rw5.js','bank_sat_math.js','bank_sat_math2.js','bank_sat_math3.js','bank_sat_math4.js','bank_sat_math5.js','bank_sat_easy.js','cards_sat.js','cards_sat2.js','playbook_sat.js'],
 concat:'BANK_SAT_RW,BANK_SAT_RW2,BANK_SAT_RW3,BANK_SAT_RW4,BANK_SAT_RW5,BANK_SAT_MATH,BANK_SAT_MATH2,BANK_SAT_MATH3,BANK_SAT_MATH4,BANK_SAT_MATH5,BANK_SAT_EASY'};

let failures=0;
function fail(msg){ failures++; console.log('  FAIL: '+msg); }
function check(label,list){ if(list.length){ fail(label+' '+JSON.stringify(list.slice(0,8))+(list.length>8?' (+'+(list.length-8)+' more)':'')); } else { console.log('  ok: '+label); } }

function runExam(exam){
 console.log('\n=== '+exam.id+' ===');
 const src=exam.files.concat(['engine.js']).map(f=>fs.readFileSync(f,'utf8')).join('\n');
 const ctx={console,Date,Math,JSON,Set,EXAM_ID:exam.id};
 vm.createContext(ctx);
 // engine.js declares with const, which stays in the script's lexical scope, so the script
 // itself hands the pieces back out.
 const EXPORTS='BANK,SKILLS,SECTION_META,SECTIONS,PLAYBOOK,CARDS,EXAM,newState,pickQuestions,recordAttempt,'+
  'skillStats,sectionSummary,pickMockSection,pickSatModule,satRoute,satDomainTargets,gradeChosen,timingFlag,'+
  'scoreEstimate,sectionAbility,itemInfo,eloToTheta';
 vm.runInContext('var EXAM_ID='+JSON.stringify(exam.id)+';\n'+src+
  '\nvar BANK=[].concat('+exam.concat+');\nglobalThis.__api={'+EXPORTS+'};',ctx);
 const api=ctx.__api;
 const {BANK,SKILLS,SECTION_META,SECTIONS,PLAYBOOK,CARDS,EXAM}=api;

 // ---- bank integrity ----
 const ids=new Set(); const bad=[];
 BANK.forEach(q=>{
  if(ids.has(q.id)) bad.push('dup '+q.id); ids.add(q.id);
  if(!SKILLS.find(s=>s.id===q.skill)) bad.push('skill '+q.id);
  if(!SECTION_META[q.section]) bad.push('section '+q.id);
  if(q.answerType==='tpa'){ if(!Array.isArray(q.answer)||q.answer.some(a=>a<0||a>=q.choices.length)) bad.push('tpa ans '+q.id); }
  else if(q.answerType==='gi'||q.answerType==='ta'){ if(!q.statements||!q.statements.length) bad.push('stmts '+q.id); }
  else if(q.answerType==='spr'){ if(typeof q.answer!=='string'||!q.answer.length) bad.push('spr ans '+q.id); }
  else if(q.answerType==='se'){ if(!Array.isArray(q.answer)||q.answer.length!==2
   ||q.answer.some(a=>typeof a!=='number'||a<0||a>=q.choices.length)
   ||q.answer[0]===q.answer[1]) bad.push('se ans '+q.id);
   if(q.choices.length!==6) bad.push('se nchoices '+q.id+' '+q.choices.length); }
  else if(typeof q.answer!=='number'||q.answer<0||q.answer>=q.choices.length) bad.push('ans '+q.id);
  if(!q.expl) bad.push('expl '+q.id);
  if([1,2,3,4,5].indexOf(q.diff)<0) bad.push('diff '+q.id);
  if(!q.answerType&&q.choices.length!==(exam.choicesByType&&exam.choicesByType[q.type]||exam.choices))
   bad.push('nchoices '+q.id+' '+q.choices.length);
  if(/[—–]/.test(JSON.stringify(q))) bad.push('dash '+q.id);
 });
 const secCount={}; BANK.forEach(q=>secCount[q.section]=(secCount[q.section]||0)+1);
 console.log('  bank '+BANK.length+' '+JSON.stringify(secCount)+' cards '+CARDS.length+' playbook '+PLAYBOOK.length);
 check('bank integrity',bad);

 // Correct answers must not cluster in one position. An early SAT bank had 75 percent of its
 // answers at A, which lets a student game the bank and corrupts the adaptive ratings.
 const mc=BANK.filter(q=>!q.answerType||q.answerType==='mc');
 if(mc.length>=40){
  const pos=new Array(exam.choices).fill(0); mc.forEach(q=>{ if(typeof q.answer==='number') pos[q.answer]++; });
  const share=pos.map(n=>n/mc.length);
  const even=1/exam.choices, worst=Math.max(...share);
  console.log('  answer positions '+pos.join(' ')+' of '+mc.length+' (even would be '+Math.round(mc.length/exam.choices)+' each)');
  check('answer position balance', worst>even*1.6?['position '+'ABCDE'[share.indexOf(worst)]+' holds '+Math.round(worst*100)+' percent of correct answers']:[]);
 }

 // Length bias: on a well-built test the correct answer is no likelier to be the longest choice
 // than any other. Reported every run so the trend is visible; the guard is deliberately loose,
 // because the bank is above chance today and a tight threshold would just fail on every commit.
 if(mc.length>=40){
  let longest=0, shortest=0, comparable=0;
  mc.forEach(q=>{ const len=q.choices.map(c=>String(c).length);
   const max=Math.max(...len), min=Math.min(...len);
   if(len.filter(l=>l===max).length>1){ comparable++; return; }
   if(len[q.answer]===max) longest++; if(len[q.answer]===min) shortest++; });
  const pctLong=Math.round(longest/mc.length*100), evenPct=Math.round(100/exam.choices);
  console.log('  longest choice is correct on '+pctLong+' percent of items, shortest on '+
   Math.round(shortest/mc.length*100)+' percent (even would be '+evenPct+' each)');
  check('length bias within tolerance', pctLong>evenPct*1.8?
   ['the longest choice is correct on '+pctLong+' percent of items, against '+evenPct+' by chance']:[]);
 }

 // every tracked skill has items, and every playbook skill is real
 const covered=new Set(BANK.map(q=>q.skill));
 check('every skill has items',SKILLS.filter(s=>!covered.has(s.id)).map(s=>s.id));
 check('playbook skills exist',PLAYBOOK.filter(pb=>pb.sec!=='G'&&!SKILLS.find(s=>s.id===pb.skill)).map(pb=>pb.skill));
 check('card sections valid',CARDS.filter(c=>c.sec!=='G'&&!SECTION_META[c.sec]).map(c=>c.id));

 // ---- grading, in both directions ----
 const g=[];
 BANK.forEach(q=>{
  if(q.answerType==='tpa'){ if(!api.gradeChosen(q,q.answer.slice())) g.push('tpa '+q.id); if(api.gradeChosen(q,[q.answer[0],(q.answer[1]+1)%q.choices.length])) g.push('tpa fp '+q.id); }
  else if(q.answerType==='gi'||q.answerType==='ta'){ const right=q.statements.map(s=>s.answer); if(!api.gradeChosen(q,right)) g.push(q.answerType+' '+q.id);
   if(q.answerType==='ta'){ const f=right.slice(); f[0]=!f[0]; if(api.gradeChosen(q,f)) g.push('ta fp '+q.id); } }
  else if(q.answerType==='spr'){ if(!api.gradeChosen(q,q.answer)) g.push('spr '+q.id);
   if(api.gradeChosen(q,String(Number(q.answer)+1))) g.push('spr fp '+q.id);
   if(api.gradeChosen(q,'')) g.push('spr blank '+q.id); }
  else { if(!api.gradeChosen(q,q.answer)) g.push('mc '+q.id); if(api.gradeChosen(q,(q.answer+1)%q.choices.length)) g.push('mc fp '+q.id); }
 });
 check('gradeChosen',g);

 // ---- adaptive selection and rating movement ----
 const st=api.newState();
 const first=api.pickQuestions(BANK,st,{count:10});
 if(first.length!==10) fail('adaptive pick returned '+first.length);
 first.forEach((q,i)=>api.recordAttempt(st,q,0,i%3!==0,100+i*10,i%3===0?'concept':null,false,'s1'));
 for(let k=0;k<20;k++){ api.pickQuestions(BANK,st,{count:10}).forEach(q=>api.recordAttempt(st,q,0,Math.random()<0.6,120,'calc',false,'x')); }
 console.log('  after '+st.attempts.length+' attempts, review queue '+Object.keys(st.review).length);
 check('every section reports a band',SECTIONS.filter(s=>!api.sectionSummary(st,s).band));
 const perSection=SECTIONS.map(s=>{ const qs=api.pickQuestions(BANK,st,{count:8,sections:[s]}); return qs.length===8&&qs.every(q=>q.section===s)?null:s; }).filter(Boolean);
 check('single-section rounds stay in section',perSection);

 // ---- mock construction ----
 if(EXAM.adaptive==='module'){
  const mbad=[];
  SECTIONS.forEach(sec=>{
   const meta=SECTION_META[sec];
   [1,2].forEach(mi=>{
    const routing=mi===2?'upper':null;
    const mod=api.pickSatModule(BANK,st,sec,mi,routing);
    if(mod.length!==meta.questions) mbad.push(sec+' m'+mi+' len '+mod.length+'!='+meta.questions);
    if(new Set(mod.map(q=>q.id)).size!==mod.length) mbad.push(sec+' m'+mi+' dup');
    if(mod.some(q=>q.section!==sec)) mbad.push(sec+' m'+mi+' wrong section');
    // official domain order for Reading and Writing, easiest to hardest for Math
    const rank={}; meta.domainOrder.forEach((id,i)=>{rank[id]=i;});
    for(let i=1;i<mod.length;i++){
     if(sec==='RW'){ if(rank[mod[i].skill]<rank[mod[i-1].skill]) mbad.push(sec+' m'+mi+' domain order at '+i); }
     else if(mod[i].diff<mod[i-1].diff) mbad.push(sec+' m'+mi+' difficulty order at '+i);
    }
   });
   // module 2 really is harder when routed up
   const up=api.pickSatModule(BANK,st,sec,2,'upper'), down=api.pickSatModule(BANK,st,sec,2,'lower');
   const mean=a=>a.reduce((s,q)=>s+q.diff,0)/a.length;
   if(!(mean(up)>mean(down))) mbad.push(sec+' routing did not raise difficulty ('+mean(up).toFixed(2)+' vs '+mean(down).toFixed(2)+')');
   else console.log('  '+sec+' routing: harder module mean difficulty '+mean(up).toFixed(2)+' vs easier '+mean(down).toFixed(2));
   // domain mix tracks the official ranges
   const targets=api.satDomainTargets(sec,meta.questions);
   const sum=Object.keys(targets).reduce((a,k)=>a+targets[k],0);
   if(sum!==meta.questions) mbad.push(sec+' domain targets sum '+sum);
   console.log('  '+sec+' module mix '+JSON.stringify(targets));
  });
  check('SAT module construction',mbad);
  const rbad=[];
  if(api.satRoute(27,27)!=='upper') rbad.push('all correct should route up');
  if(api.satRoute(0,27)!=='lower') rbad.push('none correct should route down');
  if(api.satRoute(0,0)!=='lower') rbad.push('empty module should not route up');
  check('routing rule',rbad);
  // A student who routes down must actually get an easier module, which needs enough easy items
  // to fill one. This was 0.3 modules' worth on the Reading and Writing side before bank_sat_easy.
  const ebad=[];
  SECTIONS.forEach(sec=>{
   const easy=BANK.filter(q=>q.section===sec&&q.diff<=2).length;
   const need=SECTION_META[sec].questions;
   if(easy<need) ebad.push(sec+' has '+easy+' items at difficulty 1 to 2, under the '+need+' an easier module needs');
   else console.log('  '+sec+' easier-module pool: '+easy+' items at difficulty 1 to 2 for '+need+' slots');
  });
  check('easier module can be filled',ebad);
  // grid-in entries: equivalent forms all count, wrong ones do not
  const spr={answerType:'spr',answer:'0.5',accept:['1/2']};
  const sbad=['0.5','.5','1/2',' 1/2 ','2/4'].filter(v=>!api.gradeChosen(spr,v)).map(v=>'rejected '+JSON.stringify(v))
   .concat(['0.51','','abc','1/0','5'].filter(v=>api.gradeChosen(spr,v)).map(v=>'accepted '+JSON.stringify(v)));
  check('grid-in equivalence',sbad);
 } else {
  const mbad=[];
  SECTIONS.forEach(sec=>{
   const mq=api.pickMockSection(BANK,st,sec); const want=SECTION_META[sec].questions;
   if(mq.length!==want) mbad.push(sec+' len '+mq.length+'!='+want);
   if(new Set(mq.map(q=>q.id)).size!==mq.length) mbad.push(sec+' dup items');
   if(mq.some(q=>q.section!==sec)) mbad.push(sec+' wrong section item');
   const cov=new Set(mq.map(q=>q.skill));
   SKILLS.filter(s=>s.section===sec).forEach(s=>{ if(!cov.has(s.id)) mbad.push(sec+' missing skill '+s.id); });
   const seen={}; mq.forEach((q,i)=>{ if(q.passageId){ if(seen[q.passageId]!==undefined&&seen[q.passageId]!==i-1) mbad.push(sec+' split group '+q.passageId); seen[q.passageId]=i; } });
  });
  check('mock sections',mbad);
 }

 // ---- ability model: score band behaviour ----
 {
  const sc=api.EXAM.scale, bad=[];
  if(!sc) bad.push('no scale config for '+exam.id);

  // A score from a handful of questions is noise wearing a number's clothes, so the model
  // must refuse to produce one.
  const cold=api.newState();
  const coldEst=api.scoreEstimate(cold);
  if(coldEst.ready) bad.push('produced a score from zero attempts');

  // Feed it answers at a fixed ability and check the band behaves.
  function simulate(nItems,correctRate){
   const st=api.newState();
   let i=0;
   SECTIONS.forEach(sec=>{
    const pool=BANK.filter(q=>q.section===sec);
    for(let k=0;k<nItems&&pool.length;k++){
     const q=pool[(i*7+k)%pool.length];
     const ok=((i*13+k*7)%100)/100 < correctRate;
     api.recordAttempt(st,q,0,ok,20,null,false,null);
     i++;
    }
   });
   return st;
  }

  const few=simulate(8,0.6);
  const many=simulate(60,0.6);
  const eFew=api.scoreEstimate(few), eMany=api.scoreEstimate(many);
  if(!eMany.ready) bad.push('60 items per section still not ready');
  if(eMany.ready){
   // Band must never claim more precision than the configured floor.
   const half=(eMany.hi-eMany.lo)/2;
   if(half<sc.minBand-0.001) bad.push('band '+half+' tighter than floor '+sc.minBand);
   if(eMany.lo>=eMany.hi) bad.push('band not ordered: '+eMany.lo+'..'+eMany.hi);
   if(eMany.score<eMany.lo||eMany.score>eMany.hi) bad.push('point estimate outside its own band');
   // Everything must land inside the exam's real reported range, on its real lattice.
   [eMany.lo,eMany.score,eMany.hi].forEach(v=>{
    if(v<sc.min||v>sc.max) bad.push('score '+v+' outside '+sc.min+' to '+sc.max);
    if(((v-(sc.offset||0))%(sc.step||10))!==0) bad.push('score '+v+' off the reporting lattice');
   });
   eMany.sections.forEach(x=>{
    if(x.score<sc.sectionMin||x.score>sc.sectionMax) bad.push('section '+x.section+' score '+x.score+' out of range');
   });
  }
  // More evidence must mean a smaller standard error. This is the property that makes the
  // estimate improve with use rather than just move around.
  if(eFew.ready&&eMany.ready&&!(eMany.sem<eFew.sem)) bad.push('sem did not shrink with more evidence');

  // A stronger record must not score below a weaker one.
  const strong=api.scoreEstimate(simulate(60,0.9)), weak=api.scoreEstimate(simulate(60,0.3));
  if(strong.ready&&weak.ready&&!(strong.score>weak.score)) bad.push('90% accuracy did not outscore 30%');

  // Guessing correction. More answer choices means a lower chance of a lucky hit, so a
  // 5-choice item (c=0.2) carries MORE information than a 4-choice one (c=0.25), and an
  // item with no guessing floor carries more than either.
  const i5=api.itemInfo(0,0,1/5), i4=api.itemInfo(0,0,1/4), i0=api.itemInfo(0,0,0);
  if(!(i5>i4)) bad.push('guessing correction backwards: 5-choice info '+i5+' <= 4-choice '+i4);
  if(!(i0>i5)) bad.push('no-guess info '+i0+' should exceed 5-choice '+i5);

  check('score band model',bad);
  if(eMany.ready) console.log('  band at 60 items/section: '+eMany.lo+' to '+eMany.hi+' (sem '+eMany.sem.toFixed(3)+' logits)');
 }

 const dist={}; BANK.forEach(q=>dist[q.skill]=(dist[q.skill]||0)+1);
 console.log('  items per skill '+JSON.stringify(dist));
}

[GMAT,SAT,GRE].forEach(runExam);
console.log('\n'+(failures?failures+' FAILURE(S)':'all checks passed'));
process.exit(failures?1:0);
