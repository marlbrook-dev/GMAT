const fs=require('fs');
const src=['bank_quant.js','bank_quant2.js','bank_quant3.js','bank_quant4.js','bank_quant5.js','bank_quant6.js','bank_verbal.js','bank_verbal2.js','bank_verbal3.js','bank_verbal4.js','bank_verbal5.js','bank_verbal6.js','bank_di.js','bank_di2.js','bank_di3.js','bank_di4.js','bank_di5.js','bank_di6.js','cards.js','cards2.js','cards3.js','engine.js'].map(f=>fs.readFileSync(f,'utf8')).join('\n');
const vm=require('vm'); const ctx={console,Date,Math,JSON,Set}; vm.createContext(ctx);
vm.runInContext(src+`
var BANK=[].concat(BANK_QUANT,BANK_QUANT2,BANK_QUANT3,BANK_QUANT4,BANK_QUANT5,BANK_QUANT6,BANK_VERBAL,BANK_VERBAL2,BANK_VERBAL3,BANK_VERBAL4,BANK_VERBAL5,BANK_VERBAL6,BANK_DI,BANK_DI2,BANK_DI3,BANK_DI4,BANK_DI5,BANK_DI6);
console.log('bank',BANK.length,'Q',BANK_QUANT.length+BANK_QUANT2.length+BANK_QUANT3.length+BANK_QUANT4.length+BANK_QUANT5.length+BANK_QUANT6.length,'V',BANK_VERBAL.length+BANK_VERBAL2.length+BANK_VERBAL3.length+BANK_VERBAL4.length+BANK_VERBAL5.length+BANK_VERBAL6.length,'DI',BANK_DI.length+BANK_DI2.length+BANK_DI3.length+BANK_DI4.length+BANK_DI5.length+BANK_DI6.length,'cards',CARDS.length);
var ids=new Set(); var bad=[];
BANK.forEach(function(q){ if(ids.has(q.id)) bad.push('dup '+q.id); ids.add(q.id);
 if(!SKILLS.find(function(s){return s.id===q.skill})) bad.push('skill '+q.id);
 if(q.answerType==='tpa'){ if(!Array.isArray(q.answer)||q.answer.some(function(a){return a<0||a>=q.choices.length})) bad.push('tpa ans '+q.id); }
 else if(q.answerType==='gi'||q.answerType==='ta'){ if(!q.statements||!q.statements.length) bad.push('stmts '+q.id); } else if(typeof q.answer!=='number'||q.answer<0||q.answer>=q.choices.length) bad.push('ans '+q.id);
 if(!q.expl) bad.push('expl '+q.id); if([1,2,3,4,5].indexOf(q.diff)<0) bad.push('diff '+q.id);
 if(!q.answerType&&q.choices.length!==5) bad.push('nchoices '+q.id+' '+q.choices.length);
});
console.log('validation issues:',JSON.stringify(bad));
var st=newState(); var qs=pickQuestions(BANK,st,{count:10}); console.log('adaptive pick',qs.map(function(q){return q.id+'/'+q.skill+'/d'+q.diff}).join(' '));
qs.forEach(function(q,i){recordAttempt(st,q,0,i%3!==0,100+i*10,i%3===0?'concept':null,false,'s1')});
console.log('ratings',JSON.stringify(Object.fromEntries(Object.entries(st.skills).filter(function(e){return e[1].n}).map(function(e){return [e[0],e[1].r+'/'+e[1].n]}))));
console.log('review queue',Object.keys(st.review).length);
var q2=pickQuestions(BANK,st,{count:10,sections:['Q']}); console.log('quant pick',q2.map(function(q){return q.id}).join(' '));
var c=pickQuestions(BANK,st,{mode:'custom',count:8,types:['RC']}); console.log('custom RC',c.map(function(q){return q.id}).join(' '));
console.log('section',JSON.stringify(sectionSummary(st,'Q')));
var dist={}; BANK.forEach(function(q){dist[q.skill]=(dist[q.skill]||0)+1;}); console.log(JSON.stringify(dist));
// stress: 200 answers
for(var k=0;k<20;k++){ var set=pickQuestions(BANK,st,{count:10}); set.forEach(function(q,i){recordAttempt(st,q,0,Math.random()<0.6,120,'calc',false,'x')}); }
console.log('after 200 attempts, attempts=',st.attempts.length,'review=',Object.keys(st.review).length,'quant band',sectionSummary(st,'Q').band);
// mock sections: exact length, section purity, no duplicates, all section skills covered
var mockBad=[];
['Q','V','DI'].forEach(function(sec){
 var mq=pickMockSection(BANK,st,sec); var want=SECTION_META[sec].questions;
 if(mq.length!==want) mockBad.push(sec+' len '+mq.length+'!='+want);
 var mids=new Set(mq.map(function(q){return q.id})); if(mids.size!==mq.length) mockBad.push(sec+' dup items');
 if(mq.some(function(q){return q.section!==sec})) mockBad.push(sec+' wrong section item');
 var covered=new Set(mq.map(function(q){return q.skill}));
 SKILLS.filter(function(s){return s.section===sec}).forEach(function(s){ if(!covered.has(s.id)) mockBad.push(sec+' missing skill '+s.id); });
 // passage groups arrive adjacent
 var seenPassage={}; mq.forEach(function(q,i){ if(q.passageId){ if(seenPassage[q.passageId]!==undefined&&seenPassage[q.passageId]!==i-1) mockBad.push(sec+' split group '+q.passageId); seenPassage[q.passageId]=i; } });
});
console.log('mock section issues:',JSON.stringify(mockBad));
// grading helper
var gBad=[];
BANK.forEach(function(q){
 if(q.answerType==='tpa'){ if(!gradeChosen(q,q.answer.slice())) gBad.push('tpa '+q.id); if(gradeChosen(q,[q.answer[0],(q.answer[1]+1)%q.choices.length])) gBad.push('tpa fp '+q.id); }
 else if(q.answerType==='gi'){ var right=q.statements.map(function(s){return s.answer}); if(!gradeChosen(q,right)) gBad.push('gi '+q.id); }
 else if(q.answerType==='ta'){ var rightT=q.statements.map(function(s){return s.answer}); if(!gradeChosen(q,rightT)) gBad.push('ta '+q.id); var flipped=rightT.slice(); flipped[0]=!flipped[0]; if(gradeChosen(q,flipped)) gBad.push('ta fp '+q.id); }
 else { if(!gradeChosen(q,q.answer)) gBad.push('mc '+q.id); if(gradeChosen(q,(q.answer+1)%q.choices.length)) gBad.push('mc fp '+q.id); }
});
console.log('gradeChosen issues:',JSON.stringify(gBad));
`,ctx);
