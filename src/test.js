// Bank validation and engine simulation, run once per exam in the registry.
// node test.js  (from src/)
const fs=require('fs');
// The bank file lists and the VM boot live in exam_harness.js so this file and the
// review bots cannot drift apart when an exam gains a bank file.
const harness=require('./exam_harness.js');
const {GMAT,SAT,GRE,LSAT,ACT}={GMAT:harness.byId['gmat-focus'],SAT:harness.byId['sat'],
 GRE:harness.byId['gre'],LSAT:harness.byId['lsat'],ACT:harness.byId['act']};

// A phrase said twice back to back where two pieces of text meet: a clause appended to a
// choice that already ended with it (INC-0119), a unit written by a template and again by
// the code filling it (INC-0120). The same rule as said_twice in build_banks.py, which
// covers the deferred generated chunks this file does not load. A comma between the two is
// ordinary prose ("Before the pilot, the pilot department") and passes, and so does a run
// of single letters such as a coin toss sequence. Passages are not read: prose there can
// repeat itself on purpose ("piece by piece by gangs of longshoremen").
const DOUBLED=/\b((?:[A-Za-z']+ )+[A-Za-z']+) \1\b/g;
// The copy a seam leaves need not be exact: LC041 said "to particular facts to the
// particular facts", because the appended clause added "the" (INC-0194). So each text is
// read a second time with a, an and the taken out, as said_twice does. Capital A stays,
// since in a note it is usually a choice or a passage.
const ARTICLES=/\b(?:a|an|the|An|The) /g;
function saidTwice(q){
 for(const k of ['stem','prompt','choices','statements','expl','wrong']){
  for(const t of [].concat(q[k]||[])){
   if(typeof t!=='string') continue;
   for(const s of [t,t.replace(ARTICLES,'')]){
    DOUBLED.lastIndex=0; let m;
    while((m=DOUBLED.exec(s))){ if(m[1].split(' ').some(w=>w.length>1)) return k+' "'+m[0]+'"'; }
   }
  }
 }
 return null;
}

// The choices a Watch for note names, as indices, by letter or by position (INC-0189). The
// notes were written against the order the author wrote the choices in, and a shuffle moved
// the choices and left the letters, so on 124 items the note named the correct answer as a
// trap. C to J are always choices. A and B are also the article and, in a two passage set,
// Passage A and Passage B, so outside such a set they count only where they read as a choice,
// and inside one they do not count at all. A note that says a letter "is right" is naming
// the key on purpose and is not read.
const ORD={first:0,second:1,third:2,fourth:3,fifth:4};
function noteNames(q){
 const t=String(q.wrong||''), n=q.choices.length, out=[];
 if(!t||/\b(?:is|was) (?:right|correct|the answer)\b/i.test(t)) return out;
 const pair=/\bpassages\b|[Pp]assage [AB]\b/.test((q.stem||'')+' '+q.choices.join(' '));
 const add=L=>{ const i='ABCDEFGHIJ'.indexOf(L); if(i>=0&&i<n&&!(pair&&i<2)) out.push(i); };
 for(const m of t.matchAll(/\(([A-J])\)/g)) add(m[1]);
 for(const m of t.matchAll(/\b(?:[Cc]hoices?|[Oo]ptions?)\s+\(?([A-J](?:\)?(?:\s*,\s*|,?\s+(?:and|or)\s+)\(?[A-J])*)\b/g))
  for(const L of m[1].match(/[A-J]/g)) add(L);
 for(const m of t.matchAll(/(?<![A-Za-z'])([A-J](?:(?:\s*,\s*[A-J])+(?:,?\s+(?:and|or)\s+[A-J])?|,?\s+(?:and|or)\s+[A-J]))(?![A-Za-z'])/g))
  for(const L of m[1].match(/[A-J]/g)) add(L);
 for(const m of t.matchAll(/(?:^|[.;:!?]\s+|,\s+(?:and\s+|but\s+)?)([B-J])\s+(?=[a-z])/g)) add(m[1]);
 for(const m of t.matchAll(/(?:^|[.;:!?]\s+|,\s+(?:and\s+)?)A\s+(?=(?:is|are|was|and|or|goes|reverses|confuses|overstates|restates|contradicts|describes|names|misreads|supports|strengthens|weakens|concerns|imposes|picks)\b)/g)) add('A');
 for(const m of t.matchAll(/\b(first|second|third|fourth|fifth|last)\s+(?:option|choice)\b/gi))
  out.push(m[1].toLowerCase()==='last'?n-1:ORD[m[1].toLowerCase()]);
 for(const m of t.matchAll(/(?:^|[.;:]\s+|,\s+(?:and\s+)?)[Tt]he\s+(first|second|third|fourth|fifth)((?:\s+and\s+(?:first|second|third|fourth|fifth))?)(?=\s+(?:reverses|reverse|reason|reasons|applies|contradict|contradicts|overstates|restates|misreads|drops|keeps|disputes|denies|overreaches|confuses|misstates|concern|concerns|weakens|strengthens|supports|is|are)\b)/g)){
  out.push(ORD[m[1]]); const more=m[2].match(/first|second|third|fourth|fifth/); if(more) out.push(ORD[more[0]]); }
 return out;
}

let failures=0;
function fail(msg){ failures++; console.log('  FAIL: '+msg); }
function check(label,list){ if(list.length){ fail(label+' '+JSON.stringify(list.slice(0,8))+(list.length>8?' (+'+(list.length-8)+' more)':'')); } else { console.log('  ok: '+label); } }

function runExam(exam){
 console.log('\n=== '+exam.id+' ===');
 // The generated bank is part of the shipped product, so it is part of the test. Testing
 // only the hand written items would leave thousands of items unchecked, which is exactly
 // the situation generation makes easy to fall into.
 // The generated bank is part of the shipped product, so it is part of the test. Testing
 // only the hand written items would leave thousands of items unchecked, which is exactly
 // the situation generation makes easy to fall into.
 const api=harness.load(exam);
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
  const twice=saidTwice(q); if(twice) bad.push('said twice '+q.id+' '+twice);
 });
 const secCount={}; BANK.forEach(q=>secCount[q.section]=(secCount[q.section]||0)+1);
 console.log('  bank '+BANK.length+' '+JSON.stringify(secCount)+' cards '+CARDS.length+' playbook '+PLAYBOOK.length);
 check('bank integrity',bad);
 // ETS says the GRE's Quantitative measure "doesn't include trigonometry, calculus or other
 // higher-level mathematics", and the trainer served about 195 questions on the tangent of an
 // angle because a schema list was copied from the SAT's (INC-0209). gen/mapping.py refuses
 // the schema; this catches the content in any item, hand written or generated.
 if(exam.id==='gre'){
  const quant=new Set(SKILLS.filter(s=>s.section==='Q').map(s=>s.id));
  check('no GRE quantitative item asks for a trigonometric function (INC-0209)',
   BANK.filter(q=>quant.has(q.skill)&&/\b(?:sine|cosine)\b|\b(?:sin|cos|tan)\s*\(|\btangent of (?:an |the )?angle\b/i
     .test(q.stem+' '+(q.choices||[]).join(' ')+' '+(q.expl||''))).map(q=>q.id+' '+(q.gen||'hand')));
 }
 check('no Watch for note names the correct answer among the wrong ones',
   BANK.filter(q=>typeof q.answer==='number'&&Array.isArray(q.choices)&&noteNames(q).includes(q.answer))
     .map(q=>q.id+' ('+'ABCDEFGHIJ'[q.answer]+'): '+String(q.wrong).slice(0,70)));
 // A reader who never reads the question can answer a stated question by choosing the option
 // with the largest share of its words in the passage, when the key was written by copying the
 // sentence that answers it (INC-0192). INC-0117 caps this shortcut for the generated schemas;
 // these are the hand written ones, which is where the copying happened. It may do no better
 // than a blind guess: 29 of 44 GMAT keys and 22 of 30 LSAT keys fell to it before.
 { const hand=new Set();
   exam.files.filter(f=>f.startsWith('bank_')).forEach(f=>{
    const src=fs.readFileSync(require('path').join(__dirname,f),'utf8');
    for(const m of src.matchAll(/\{\s*id: ?['"]([A-Za-z0-9_]+)['"]/g)) hand.add(m[1]); });
   const STOP=new Set(('that this which with from into have been were their there where when what about than more '+
    'most other only also such these those them they then some over under after before because between within without').split(' '));
   const words=t=>new Set((String(t).match(/[A-Za-z]{5,}/g)||[]).map(w=>w.toLowerCase()).filter(w=>!STOP.has(w)));
   const stated=BANK.filter(q=>hand.has(q.id)&&q.passage&&Array.isArray(q.choices)&&typeof q.answer==='number'&&
    /according to the passage|the passage states|passage [ab] states|\bstates that\b/i.test(q.stem||'')&&!/infer|suggest|impl/i.test(q.stem||''));
   const hits=stated.filter(q=>{ const P=words(q.passage);
    const sc=q.choices.map(c=>{ const w=[...words(c)]; return w.filter(x=>P.has(x)).length/Math.max(1,w.length); });
    const best=Math.max(...sc); return best>0&&sc.filter(s=>s===best).length===1&&sc[q.answer]===best; });
   if(stated.length){
    const pct=Math.round(hits.length/stated.length*100), cap=Math.round(100/exam.choices);
    console.log('  stated questions answered by matching passage words: '+hits.length+' of '+stated.length+' ('+pct+' percent, a blind guess is '+cap+')');
    check('stated questions are not answerable by matching passage words',
     stated.length>=5&&pct>cap?[hits.length+' of '+stated.length+': '+hits.map(q=>q.id).join(' ')]:[]); } }

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
  // Two different failure modes, so two different measurements.
  //
  // On a VERBAL item, length is content: the longest option is the most hedged and
  // most qualified, and a writer who is not careful makes it the key. That is the
  // classic pitfall, and it is worth a hard guard in both directions.
  //
  // On a NUMERIC item, length is only a proxy for magnitude, and the property that
  // actually matters is where the key sits in the ORDER of the values. If the key is
  // never the largest, "skip the biggest number" beats guessing. So numeric items are
  // checked on value rank, which is the thing a student could exploit, rather than on
  // a character count that just tracks the number of digits.
  const numeric=q=>q.choices.every(c=>/^\$?-?[\d,]+(\.\d+)?(\/\d+)?$/.test(String(c).trim()));
  const val=c=>{ const t=String(c).replace(/[$,]/g,'').trim();
   if(t.indexOf('/')>0){ const p=t.split('/'); return Number(p[0])/Number(p[1]); } return Number(t); };
  const wordy=mc.filter(q=>!numeric(q)), nums=mc.filter(numeric);

  // Measured per SECTION, not per exam. Adding 500 unbiased Data Sufficiency items
  // pulled the GMAT aggregate from 41 percent down to 33 without a single verbal item
  // changing, which is dilution, not repair. Per section, a bias has nowhere to hide.
  // Recorded debt in hand written content, measured per section so nothing dilutes it.
  // These are the worst the bank is allowed to be, not a target. GMAT V is the serious
  // one: the longest choice is the key on 81 percent of items, so a student who picks
  // the longest option and never reads the question scores 81 percent. That is a bank
  // defect, not a difficulty setting, and it needs the choices rewritten so the correct
  // answer is not the only one carrying its full qualification. The quantitative entries
  // are the mirror image, short correct values against long error derived ones.
  // Lower each number as items are rewritten; delete the entry once it is in tolerance.
  // Tightened to the measured values now that the generated bank is genuinely
  // reproducible. It was not before: build_banks.py seeded from Python's hash(),
  // which is randomised per process, so these numbers drifted a few points every
  // build and the caps had to be loose enough to absorb noise that should not have
  // existed. Each number here is now the exact current measurement, so any movement
  // is a real change in the bank.
  // GMAT verbal is no longer listed here. It was 81 percent, meaning a student who
  // always picked the longest option and never read the question scored 81 against a
  // chance level of 20. The cause was structural: keys carried two clauses, a mechanism
  // and the evidence for it, while distractors carried one, so the shape of the option
  // gave the answer away before anyone read the words. After rewriting the choices on
  // about 120 items it sits at 22 percent, inside normal tolerance, and the ordinary
  // guard below now covers it.
  // Both quantitative entries are gone. They recorded a tell that turned out to be an
  // artefact of how it was measured: "25 percent" among other two digit percents counted
  // as the shortest option even though three choices tied at that length, which is no tell
  // at all. Scoring only items with a UNIQUE shortest and longest option puts every
  // section at or near chance, so there is nothing left to record. One real fix went in
  // alongside: the percent change schema rendered the divide by the new value distractor
  // as "100/3 percent" against a key of "25 percent", which was a genuine difference in
  // form, and it now renders as "33.3 percent" like every other option.
  const DEBT={};
  // Per file recorded debt, filled in below from the measurement so the ratchet starts
  // where the bank actually is. Lower each number as a file is rewritten and delete the
  // entry when the file is inside normal tolerance, which the check below insists on.
  //
  // Empty, and it stayed empty. The table existed for one commit and held the eight files
  // that were still out of tolerance when the per file check was written; all eight were
  // rewritten in the same change, so every entry came off. Any file that fails now fails
  // against the ordinary tolerance, which is what a new bank should be held to.
  //
  // If an entry is ever added, it is a MEASURED value and not a guess, and the check
  // below insists that it be removed once the file is inside tolerance rather than
  // leaving that to whoever notices.
  //
  // The 'rank' number is the one that matters most. A file can sit at an ordinary
  // longest is key figure and still be playable, because extending ONE distractor per
  // item moves the pile from longest to second longest and leaves it exactly as
  // findable. That is INC-0062, and it is why the rank column exists at all.
  const FILE_DEBT={};
  const bySec={};
  wordy.forEach(q=>{ (bySec[q.section]=bySec[q.section]||[]).push(q); });
  Object.keys(bySec).sort().forEach(sec=>{
   const list=bySec[sec];
   if(list.length<40) return;
   let longest=0, shortest=0, scored=0;
   // An item only carries a length tell if the extreme is UNIQUE. Three options tied at
   // ten characters give a guesser nothing, so counting the key as "the shortest" there
   // measured a coincidence rather than a strategy: it was why "25 percent" among other
   // two digit percents registered as a tell. Both ends are now required to be unique
   // before the item is scored at all, and the recorded numbers below are on this basis.
   list.forEach(q=>{ const len=q.choices.map(c=>String(c).length);
    const max=Math.max(...len), min=Math.min(...len);
    if(len.filter(l=>l===max).length>1 || len.filter(l=>l===min).length>1) return;
    scored++;
    if(len[q.answer]===max) longest++; if(len[q.answer]===min) shortest++; });
   if(!scored) return;
   const pctLong=Math.round(longest/scored*100), pctShort=Math.round(shortest/scored*100);
   const evenPct=Math.round(100/exam.choices);
   console.log('  wording ['+sec+']: longest is key on '+pctLong+' percent of '+scored+
    ' items, shortest on '+pctShort+' percent (even would be '+evenPct+' each)');
   const key=exam.id+'.'+sec;
   const cap=DEBT[key]||{}, capLong=cap.long||Math.round(evenPct*1.8), capShort=cap.short||Math.round(evenPct*1.8);
   const bad=[];
   if(pctLong>capLong) bad.push(sec+': the longest wording is key on '+pctLong+' percent, above the recorded '+capLong+' (chance is '+evenPct+')');
   if(pctShort>capShort) bad.push(sec+': the shortest wording is key on '+pctShort+' percent, above the recorded '+capShort+' (chance is '+evenPct+')');
   if(cap.long&&pctLong<=evenPct*1.8&&pctShort<=evenPct*1.8)
    bad.push(key+' is now inside normal tolerance; remove its DEBT entry in test.js');
   check('length bias within tolerance ['+sec+']', bad);
  });

  // The same statistic per SOURCE FILE, which is the grain the defect exists at.
  //
  // A section mixes hand written items with generated ones, and the generated ones are
  // flat by construction because the schemas assemble the choices mechanically. For SAT
  // Reading and Writing the generated bank supplied 160 of 348 items at 7 percent, which
  // pulled a hand written file sitting at 88 percent down to a section figure of 35 and
  // under the recorded tolerance of 36 (INC-0069). A student does not meet a section.
  // They meet items, and the items arrive from one file at a time, each written by one
  // person in one sitting with one set of habits.
  //
  // Numeric answer banks are excluded. Character length is the wrong measure for a
  // number, and the numeric rank check below is the right one; counting "7" as the
  // shortest option among "12", "18" and "24" measures the arithmetic, not the wording.
  const fileOf={};
  exam.files.filter(f=>f.startsWith('bank_')).forEach(f=>{
   const src=require('fs').readFileSync(require('path').join(__dirname,f),'utf8');
   for(const m of src.matchAll(/\{\s*id: ?['"]([A-Za-z0-9_]+)['"]/g)) fileOf[m[1]]=f;
  });
  const byFile={};
  wordy.forEach(q=>{ const f=fileOf[q.id]; if(f) (byFile[f]=byFile[f]||[]).push(q); });
  const fileBad=[];
  Object.keys(byFile).sort().forEach(f=>{
   const list=byFile[f];
   // Twenty is where one item stops moving the figure by five points or more.
   if(list.length<20) return;
   const numericish=list.filter(q=>q.choices.every(c=>/^[-+$]?[\d.,/\s%]+$/.test(String(c)))).length;
   if(numericish>list.length/2) return;
   let longest=0, shortest=0, scored=0;
   const rank=new Array(exam.choices).fill(0);
   list.forEach(q=>{ const len=q.choices.map(c=>String(c).length);
    const ord=len.map((v,i)=>i).sort((a,b)=>len[a]-len[b]);
    rank[ord.indexOf(q.answer)]++;
    const max=Math.max(...len), min=Math.min(...len);
    if(len.filter(l=>l===max).length>1 || len.filter(l=>l===min).length>1) return;
    scored++;
    if(len[q.answer]===max) longest++; if(len[q.answer]===min) shortest++; });
   if(!scored) return;
   const pctLong=Math.round(longest/scored*100), pctShort=Math.round(shortest/scored*100);
   const bestRank=Math.round(Math.max(...rank)/list.length*100);
   const evenPct=Math.round(100/exam.choices);
   const rec=FILE_DEBT[f];
   const capLong=rec?rec.long:Math.round(evenPct*1.8);
   const capShort=rec?rec.short:Math.round(evenPct*1.8);
   const capRank=rec?rec.rank:Math.round(evenPct*1.8);
   console.log('  wording <'+f+'>: '+list.length+' items, longest is key on '+pctLong+
    ' percent, shortest on '+pctShort+' percent, best single rank '+bestRank+
    ' percent (even would be '+evenPct+')');
   if(pctLong>capLong) fileBad.push(f+': longest is key on '+pctLong+' percent, above the recorded '+capLong);
   if(pctShort>capShort) fileBad.push(f+': shortest is key on '+pctShort+' percent, above the recorded '+capShort);
   if(bestRank>capRank) fileBad.push(f+': one length rank holds '+bestRank+' percent of the keys, above the recorded '+capRank);
   if(rec && pctLong<=Math.round(evenPct*1.8) && pctShort<=Math.round(evenPct*1.8)
      && bestRank<=Math.round(evenPct*1.8))
    fileBad.push(f+' is now inside normal tolerance; remove its FILE_DEBT entry in test.js');
  });
  check('length bias within tolerance, per source file', fileBad);

  if(nums.length>=40){
   // Where does the key fall once the choices are put in numeric order? Flat is the
   // goal; a spike at either end is a strategy that needs no arithmetic.
   const rank=new Array(exam.choices).fill(0); let scored=0;
   nums.forEach(q=>{ const vs=q.choices.map(val);
    if(vs.some(v=>!isFinite(v))) return;
    const sorted=vs.slice().sort((a,b)=>a-b);
    const r=sorted.indexOf(vs[q.answer]);
    if(r<0||r>=rank.length) return;
    rank[r]++; scored++; });
   const share=rank.map(n=>n/scored), even=1/exam.choices;
   console.log('  numeric: key by value rank '+rank.join(' ')+' of '+scored+
    ' (even would be '+Math.round(scored/exam.choices)+' each)');
   const bad=[];
   const lowest=share[0], highest=share[share.length-1];
   if(lowest<even/3) bad.push('the key is the smallest value on only '+Math.round(lowest*100)+' percent of items, so skipping the smallest beats guessing');
   if(highest<even/3) bad.push('the key is the largest value on only '+Math.round(highest*100)+' percent of items, so skipping the largest beats guessing');
   if(lowest>even*2) bad.push('the key is the smallest value on '+Math.round(lowest*100)+' percent of items');
   if(highest>even*2) bad.push('the key is the largest value on '+Math.round(highest*100)+' percent of items');
   check('numeric answers are not gameable by size', bad);
  }
 }

 // every tracked skill has items, and every playbook skill is real
 const covered=new Set(BANK.map(q=>q.skill));
 check('every skill has items',SKILLS.filter(s=>!covered.has(s.id)).map(s=>s.id));
 // Stored reviews keyed on an old numbered id are dropped on load (INC-0127), so that form
 // must never be the id of an item that ships, and dropping has to leave everything else.
 { const st={review:{},seen:{}}; BANK.forEach(q=>{ st.review[q.id]={due:0}; st.seen[q.id]=1; });
   st.review.ZM0042={due:0}; st.seen.ZG12345=2;
   const gone=api.forgetNumberedIds(st);
   check('dropping numbered ids keeps every live item',
     BANK.filter(q=>!st.review[q.id]||!st.seen[q.id]).map(q=>q.id));
   check('dropping numbered ids removes the old form',
     gone===2&&!st.review.ZM0042&&!st.seen.ZG12345?[]:['removed '+gone+' of 2']); }
 // A new state carries no name, and a stored one from before nameSet existed loses only the
 // owner's first name the trainer used to give everyone who never typed one (INC-0210).
 { const bad=[]; const fresh=api.newState();
   if(fresh.settings.name) bad.push('a new state is named '+fresh.settings.name);
   const old={settings:{name:'Hunter'}}; api.forgetDefaultName(old);
   if(old.settings.name!==''||old.settings.nameSet!==false) bad.push('the old default survived: '+JSON.stringify(old.settings));
   const once=JSON.stringify(old.settings); api.forgetDefaultName(old);
   if(JSON.stringify(old.settings)!==once) bad.push('a second run changed the state');
   const typed={settings:{name:'Hunter',nameSet:true}}; api.forgetDefaultName(typed);
   if(typed.settings.name!=='Hunter') bad.push('a name typed as Hunter was cleared');
   const older={settings:{name:'Sam'}}; api.forgetDefaultName(older);
   if(older.settings.name!=='Sam'||older.settings.nameSet!==true) bad.push('a name typed before the mark was not kept as typed: '+JSON.stringify(older.settings));
   check('no default name, and the old one forgotten',bad); }
 check('playbook skills exist',PLAYBOOK.filter(pb=>pb.sec!=='G'&&!SKILLS.find(s=>s.id===pb.skill)).map(pb=>pb.skill));
 check('card sections valid',CARDS.filter(c=>c.sec!=='G'&&!SECTION_META[c.sec]).map(c=>c.id));
 // The bank has had a per-skill floor since the start and the deck was checked only for
 // valid section codes, so the deck was measured by its total. A total over twelve skills
 // hides one of them holding a single card, which is what it was hiding: LSAT stated
 // information and inference had one card each, and the exam total of 33 looked fine
 // (INC-0085). Same shape of check as the bank one directly above.
 const CARD_FLOOR=8;
 const cardBySkill={}; CARDS.forEach(c=>{ if(c.skill) cardBySkill[c.skill]=(cardBySkill[c.skill]||0)+1; });
 check('every skill has at least '+CARD_FLOOR+' cards',
   SKILLS.filter(s=>(cardBySkill[s.id]||0)<CARD_FLOOR).map(s=>s.id+' has '+(cardBySkill[s.id]||0)));

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
  // Twenty draws per section, not one. The picker is random, and a single draw passed
  // while one section in three was leaving two skills untested: the check was right and
  // simply had not been asked often enough to see it.
  SECTIONS.forEach(sec=>{
   const want=SECTION_META[sec].questions;
   for(let d=0;d<20;d++){
    const mq=api.pickMockSection(BANK,st,sec);
    if(mq.length!==want) mbad.push(sec+' len '+mq.length+'!='+want);
    if(new Set(mq.map(q=>q.id)).size!==mq.length) mbad.push(sec+' dup items');
    if(mq.some(q=>q.section!==sec)) mbad.push(sec+' wrong section item');
    const cov=new Set(mq.map(q=>q.skill));
    SKILLS.filter(s=>s.section===sec).forEach(s=>{ if(!cov.has(s.id)) mbad.push(sec+' missing skill '+s.id); });
    const seen={}; mq.forEach((q,i)=>{ if(q.passageId){ if(seen[q.passageId]!==undefined&&seen[q.passageId]!==i-1) mbad.push(sec+' split group '+q.passageId); seen[q.passageId]=i; } });
    // A reading question with nothing to read is not a question (INC-0099).
    mq.forEach(q=>{ if((q.type==='RC'||q.type==='R')&&!q.passage&&!q.passageHtml) mbad.push(sec+' '+q.id+' reading item with no passage'); });
   }
  });
  check('mock sections',[...new Set(mbad)]);
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
   // An exam whose maker publishes no section scores must not invent them. The LSAT reports a
   // single 120 to 180 number and nothing per section, so its scale carries no sectionMin and
   // every section score has to come back null rather than as a plausible looking subscore.
   if(sc.sectionMin==null){
    if(eMany.hasSectionScores) bad.push('claims section scores on an exam that reports none');
    eMany.sections.forEach(x=>{ if(x.score!==null) bad.push('section '+x.section+' invented a subscore: '+x.score); });
   } else {
    if(!eMany.hasSectionScores) bad.push('exam has a section scale but reports no section scores');
    eMany.sections.forEach(x=>{
     if(x.score<sc.sectionMin||x.score>sc.sectionMax) bad.push('section '+x.section+' score '+x.score+' out of range');
    });
   }
   // Sections the exam excludes from its headline score must still be rated and reported. The
   // ACT dropped Science from the Composite in 2025 but still scores it 1 to 36.
   const outside=SECTIONS.filter(sec=>(SECTION_META[sec]||{}).inComposite===false);
   outside.forEach(sec=>{ if(!eMany.sections.some(x=>x.section===sec))
    bad.push(sec+' is excluded from the total and vanished from the report entirely'); });
   if(outside.length) console.log('  outside the headline score: '+outside.join(', ')+
    ' (rated and reported, not averaged in)');
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

[GMAT,SAT,GRE,LSAT,ACT].forEach(runExam);
console.log('\n'+(failures?failures+' FAILURE(S)':'all checks passed'));
process.exit(failures?1:0);
