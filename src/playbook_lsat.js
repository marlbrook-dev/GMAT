// LSAT playbook: the methods behind every skill the engine tracks.
const PLAYBOOK=[
 {skill:'lsat_lr_struct',sec:'LR',title:'Argument Parts and Structure',items:[
  'Find the conclusion before anything else. Ask which claim the rest of the passage is offered to support; the conclusion is frequently in the middle, not at the end.',
  'Watch for the rival view. Many arguments open with a position the speaker is about to reject, and mistaking that opening for the conclusion reverses the whole argument.',
  'On a role of a claim question, describe the job in your own words first: main conclusion, support for it, an intermediate step, a rival view, or evidence against a rival view.',
  'An intermediate conclusion is supported by something and supports something else. If any part of the argument is a reason to believe it, it is not the main conclusion.']},
 {skill:'lsat_lr_concl',sec:'LR',title:'Drawing Well-Supported Conclusions',items:[
  'Read the stem first. Must be true and most strongly supported set different bars, and the same choice can be right under one and wrong under the other.',
  'Track quantity words exactly. Some means at least one and is compatible with all. Most means more than half. Two most statements about one group must overlap; two some statements need not.',
  'Never reverse a conditional. If all A are B, nothing follows about which B are A, and that reversal is the single commonest wrong answer on inference questions.',
  'Prefer the weak choice. A conclusion hedged with may or at least partly survives on thin evidence, while one using only, never or must usually asks for more than the statements give.']},
 {skill:'lsat_lr_assum',sec:'LR',title:'Detecting Assumptions',items:[
  'Name the two terms. Write down what the evidence is about and what the conclusion is about; the assumption almost always bridges that shift.',
  'Use the negation test for necessary assumptions. Negate the choice and ask whether the argument still stands. If it does, that choice was never required.',
  'Sufficient assumptions are stronger than they look. You are adding a premise that makes the conclusion follow, so a sweeping conditional is often correct where it would be wrong as a necessary assumption.',
  'Beware choices that are merely helpful. A fact that makes the conclusion more plausible is not thereby something the argument depends on.']},
 {skill:'lsat_lr_flaw',sec:'LR',title:'Identifying Flaws in Arguments',items:[
  'Describe the defect before reading the choices. If you can say what went wrong in a sentence, the matching answer is usually obvious and the traps stop working.',
  'The answer describes the reasoning, not the content. A choice saying the conclusion is false or a premise untrue is almost never right on a flaw question.',
  'Learn the recurring patterns: correlation taken for causation, an unrepresentative sample, a necessary condition treated as sufficient, an attack on the arguer, and a false choice between two options.',
  'Watch the averaging flaw specifically. Evidence about an average is repeatedly used to draw a conclusion about a particular subgroup, which the average cannot support.']},
 {skill:'lsat_lr_evid',sec:'LR',title:'Effect of Additional Evidence',items:[
  'Identify the exact link under attack. Strengthen and weaken answers act on the connection between evidence and conclusion, not on the topic in general.',
  'To weaken a causal claim: supply an alternative cause, show the effect without the cause, show the cause without the effect, or reverse the direction.',
  'To strengthen, rule out the most obvious rival explanation. Confirming that the comparison group matched on the confounding factor is the classic correct answer.',
  'Check whether the two measurements are comparable. If the test, the sample or the conditions changed between before and after, the numbers carry no weight.']},
 {skill:'lsat_lr_prin',sec:'LR',title:'Principles, Rules and Analogy',items:[
  'Treat a principle as a conditional and check every condition. A case that meets most of the stated conditions but not all of them does not conform.',
  'On parallel reasoning, match the form and ignore the subject. Diagram what is conditional, what is denied and what is concluded before comparing.',
  'A flawed original must pair with the same flaw. If the stimulus affirms the consequent, the answer does too, however reasonable the other choices sound.',
  'Reasoning by analogy fails when the two cases differ in the respect that matters. Ask what property the analogy needs, then check the second case has it.']},
 {skill:'lsat_lr_expl',sec:'LR',title:'Explanations and Parallel Reasoning',items:[
  'On explain the discrepancy, both stated facts stay true. The answer adds a fact that lets them coexist; a choice denying either half is wrong by construction.',
  'Look for the unmeasured consequence. A change often produces a side effect that offsets the benefit it was meant to deliver, and that is usually the explanation.',
  'On point at issue, both speakers must have a view on the claim. A claim only one addresses cannot be the point of disagreement, however central it feels.',
  'Speakers often accept each other facts and dispute their significance. The disagreement is then about what the facts show rather than about what they are.']},
 {skill:'lsat_rc_main',sec:'RC',title:'Main Idea and Primary Purpose',items:[
  'Read for structure on the first pass. The claim, who disagrees, and where the author stands are worth more than any detail, and detail can be found again.',
  'A main point answer must cover the whole passage. A choice that is true of one paragraph only is the most frequent trap in the section.',
  'Match the author strength of claim. If the passage hedges, an answer that asserts flatly is wrong even when its content is right.',
  'Primary purpose wants a verb: describe, revise, argue, reconcile, question. Pick the verb before you pick the object.']},
 {skill:'lsat_rc_stated',sec:'RC',title:'Explicitly Stated Information',items:[
  'Find the line. If you cannot point to the sentence that settles it, the choice is wrong however reasonable it sounds.',
  'Beware of paraphrase that shifts scope. A choice may restate the passage accurately but add all, only or never, and the addition makes it false.',
  'Check attribution. Passages often report what other people claim, and a choice presenting a reported view as the author own is a standard trap.',
  'Answer from the passage, not from what you know about the topic. Outside knowledge is never required and is frequently the bait.']},
 {skill:'lsat_rc_inf',sec:'RC',title:'Inference and Implication',items:[
  'Implied means the passage commits to it. If you supplied a step to get there, the choice goes beyond what the text supports.',
  'Extreme language is the usual disqualifier. Never, only, cannot and must take a choice past what a hedged passage will bear.',
  'Combine two sentences rather than stretching one. Many inference answers sit at the join between a claim in one paragraph and a qualification in another.',
  'Ask what the author would have to accept. An inference the author would resist is not supported, whatever the evidence seems to allow.']},
 {skill:'lsat_rc_struct',sec:'RC',title:'Meaning, Structure and Tone',items:[
  'On a function question, ask what the sentence does rather than what it says. It usually introduces a rival view, supports, qualifies, or supplies an example.',
  'For a word in context, blank it out, predict a replacement from the sentence, then choose. The common meaning of the word is often not the one in play.',
  'Read tone from the modifiers. Merely, so far, has yet to, and overstates tell you where the author stands while the subject matter tells you nothing.',
  'Neutral is a real answer. An author who lays out a dispute at length without endorsing either side is reporting, and the tone answer should say so.']},
 {skill:'lsat_rc_app',sec:'RC',title:'Application and Comparative Reading',items:[
  'State the rule in your own words before testing the cases. Application questions are unmanageable until you know exactly what is being applied.',
  'The right analogy matches the structure of the passage case, not its subject. Ask which features the passage argument actually relies on.',
  'On comparative reading, read each passage separately and only then ask how they relate: generalisation and instance, principle and application, or point and counterpoint.',
  'For a question about what one author would say of the other, find where their claims overlap. If the two passages address different questions, the answer often says so.']}
];
