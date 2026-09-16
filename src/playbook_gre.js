// GRE playbook: the methods behind every skill the engine tracks.
const PLAYBOOK=[
 {skill:'gre_rc',sec:'V',title:'Reading Comprehension',items:[
  'Read for structure before detail. What is the claim, what supports it, where does the author turn. Most questions are answered by knowing the shape of the passage, not by rereading sentences.',
  'Primary purpose wants a verb covering the whole passage. A choice that is accurate about one paragraph is the most common wrong answer.',
  'Inference means must be true, not probably true. If you need a plausible story to connect the passage to the choice, it is not the answer.',
  'Function questions ask what a sentence does, not what it says. Usually it supports, qualifies, contrasts, or sets up what follows.',
  'On strengthen and weaken, find the exact link the argument depends on and attack or support that link, not the topic in general.']},
 {skill:'gre_tc',sec:'V',title:'Text Completion',items:[
  'Predict the blank in your own words before you look at the choices. Reading the choices first makes every one of them sound possible.',
  'Find the signal word. Although, despite and far from reverse the thought; moreover, indeed and a colon continue it.',
  'With two or three blanks, start with the blank the sentence constrains most, not the first one. Each blank has only three choices, so a firm one narrows the rest.',
  'Every blank must be right for the item to count, and there is no partial credit. Check the whole sentence reads properly before moving on.']},
 {skill:'gre_se',sec:'V',title:'Sentence Equivalence',items:[
  'Select exactly two of six, and both must be right. No partial credit.',
  'Predict first, then look for two choices that match your prediction. Choosing a synonym pair without checking the sentence is the trap the question is built around.',
  'If only one choice fits your prediction, your prediction is too narrow. Widen it rather than forcing a second choice.',
  'Watch for a matching pair that fits the grammar but reverses the meaning. A pair is necessary, not sufficient.']},
 {skill:'gre_arith',sec:'Q',title:'Arithmetic',items:[
  'Successive percent changes multiply. Adding them is the single most common arithmetic error on this exam.',
  'Percent change divides by the original value, always.',
  'For remainders, write the number as a multiple plus the remainder and carry the algebra through. Guessing a single value can mislead.',
  'To compare powers, rewrite them with a common base or a common exponent rather than estimating.']},
 {skill:'gre_alg',sec:'Q',title:'Algebra',items:[
  'Translate the words into an equation before doing any arithmetic. Most wrong answers on word problems come from a bad setup, not a bad calculation.',
  'For quadratics, the sum of the roots is the negative of the linear coefficient and the product is the constant. Use that when the question only wants one of them.',
  'Values between 0 and 1 behave backwards under powers: higher powers get smaller.',
  'Work and rate problems add rates, never times.']},
 {skill:'gre_geo',sec:'Q',title:'Geometry',items:[
  'Learn the common right triangles cold: 3-4-5, 5-12-13, 8-15-17, 45-45-90 and 30-60-90.',
  'Figures are not drawn to scale unless the problem says so. Do not measure the picture.',
  'Scaling a length by k scales area by k squared and volume by k cubed.',
  'On coordinate questions, the distance formula is the Pythagorean theorem with the horizontal and vertical gaps as legs.']},
 {skill:'gre_data',sec:'Q',title:'Data Analysis',items:[
  'Mean follows outliers, median does not. When a question mentions a single very large or very small value, that is the point.',
  'Standard deviation measures spread, not size. Identical values give zero.',
  'Decide whether order matters before counting. Committees are unordered; rankings are ordered.',
  'Without replacement, the denominator shrinks on each draw.',
  'Average speed is total distance over total time. Averaging the speeds is a trap whenever the distances are equal.']},
];
