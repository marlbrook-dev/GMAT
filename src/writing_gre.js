// writing_gre.js - GRE Analytical Writing: one Analyze an Issue task in 30 minutes.
//
// What this is and is not. ETS states the Analytical Writing measure "assesses your
// critical thinking and analytical writing skills by assessing your ability to: articulate
// and support complex ideas, construct arguments, sustain a focused and coherent
// discussion," and that the reported score "ranges from 0 to 6, in half-point increments."
// The Analyze an Issue task "presents an opinion on an issue and instructions on how to
// respond," and asks the writer to "evaluate the issue, consider its complexities and
// develop an argument with reasons and examples to support your views."
//
// This trainer does NOT score the essay. Scoring one requires trained raters working to a
// calibrated guide, and inventing a number here would be exactly the kind of false
// precision the rest of the product refuses. What it does instead: give a real prompt under
// a real clock, report the facts about the response that can be measured rather than
// judged, and hand over a self-assessment built from the dimensions ETS itself names.
//
// Issue statements are original and written for Start From Nowhere. The instruction lines
// follow the standard published task formats, which is what makes the practice realistic.
const WRITING = {
 task:'Analyze an Issue',
 minutes:30,
 scale:'0 to 6, in half-point increments',
 source:'ETS, GRE Analytical Writing measure and scoring',
 sourceUrl:'https://www.ets.org/gre/test-takers/general-test/prepare/content/analytical-writing.html',
 // The six things ETS names, turned into questions a writer can actually answer about
 // their own draft. Deliberately not weighted and not summed: a self-assessment that
 // produced a number would be a fake score wearing a rubric.
 rubric:[
  {id:'position',label:'A clear position',ask:'Does the response take a position on the issue and hold it from the first paragraph to the last, rather than surveying both sides and never landing?'},
  {id:'reasons',label:'Reasons, not assertions',ask:'Is each main claim supported by a reason that explains why it follows, rather than restated in different words?'},
  {id:'examples',label:'Specific examples',ask:'Are the examples concrete and particular, or are they generic gestures that would fit any argument?'},
  {id:'counter',label:'The strongest objection',ask:'Does the response address the most compelling case against its position, rather than the easiest one?'},
  {id:'structure',label:'Focus and coherence',ask:'Can a reader state what each paragraph is doing? Does the argument develop, or does it circle?'},
  {id:'mechanics',label:'Control of language',ask:'Are sentences varied and word choice precise? Do errors of grammar or usage interrupt meaning anywhere?'}],
 prompts:[
  {id:'W001',diff:2,
   issue:'Institutions should reward employees for the results they produce rather than for the hours they spend producing them.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the statement and explain your reasoning for the position you take. In developing and supporting your position, you should consider ways in which the statement might or might not hold true.'},
  {id:'W002',diff:3,
   issue:'A society that cannot preserve its historic buildings has already lost the culture those buildings were built to serve.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the claim. In developing and supporting your position, be sure to address the most compelling reasons or examples that could be used to challenge your position.'},
  {id:'W003',diff:3,
   issue:'The best way to understand a field is to study its failures rather than its successes.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the statement and explain your reasoning for the position you take. In developing and supporting your position, you should consider ways in which the statement might or might not hold true.'},
  {id:'W004',diff:4,
   issue:'Governments should fund scientific research only when its practical benefits can be described in advance.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the recommendation and explain your reasoning. In developing and supporting your position, describe specific circumstances in which adopting the recommendation would or would not be advantageous.'},
  {id:'W005',diff:3,
   issue:'People are more honest in writing than in speech, because writing gives them time to consider what they are committing to.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the claim. In developing and supporting your position, be sure to address the most compelling reasons or examples that could be used to challenge your position.'},
  {id:'W006',diff:4,
   issue:'A leader who admits uncertainty in public weakens the organisation they lead.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the statement and explain your reasoning for the position you take. In developing and supporting your position, you should consider ways in which the statement might or might not hold true.'},
  {id:'W007',diff:2,
   issue:'Cities should limit the number of visitors allowed at their most popular sites, even though doing so denies access to some.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the recommendation and explain your reasoning. In developing and supporting your position, describe specific circumstances in which adopting the recommendation would or would not be advantageous.'},
  {id:'W008',diff:5,
   issue:'Expertise is less valuable than it once was, because the information experts once held privately is now available to anyone.',
   instruction:'Write a response in which you discuss the extent to which you agree or disagree with the claim. In developing and supporting your position, be sure to address the most compelling reasons or examples that could be used to challenge your position.'}],
 // Facts about a draft, not judgements of it. Word count, time, paragraphing and whether
 // the writer ever signals a concession are all observable; none of them is a score, and
 // the copy in the app says so.
 measures:function(text,secs){
  const t=(text||'').trim();
  const words=t?t.split(/\s+/).length:0;
  const paras=t?t.split(/\n\s*\n/).filter(p=>p.trim()).length:0;
  const sentences=t?(t.match(/[.!?](\s|$)/g)||[]).length:0;
  const concessive=/\b(however|although|admittedly|granted|critics|opponents|one might object|it could be argued|to be sure|conversely|on the other hand)\b/i.test(t);
  const specifics=(t.match(/\b(for (?:example|instance)|such as|in \d{4}|consider the case)\b/gi)||[]).length;
  return {words:words,paras:paras,sentences:sentences,
          avgSentence:sentences?Math.round(words/sentences):0,
          concessive:concessive,specifics:specifics,
          minutes:Math.round((secs||0)/60)};
 }
};
