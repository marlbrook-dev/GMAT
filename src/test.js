const fs=require('fs');
const src=['bank_quant.js','bank_quant2.js','bank_verbal.js','bank_verbal2.js','bank_di.js','bank_di2.js','cards.js','engine.js'].map(f=>fs.readFileSync(f,'utf8')).join('\n');
const vm=require('vm'); const ctx={console,Date,Math,JSON,Set}; vm.createContext(ctx);
vm.runInContext(src+`
var BANK=[].concat(BANK_QUANT,BANK_QUANT2,BANK_VERBAL,BANK_VERBAL2,BANK_DI,BANK_DI2);
console.log('bank',BANK.length,'Q',BANK_QUANT.length,'V',BANK_VERBAL.length,'DI',BANK_DI.length);
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
`,ctx);
