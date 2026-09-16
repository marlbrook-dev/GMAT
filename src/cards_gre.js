// GRE flashcard deck: formulas, rules and method prompts. front = prompt, back = answer.
// sec: V | Q | G (general/pacing). Keyed to the seven skills the engine tracks for the GRE.
const CARDS = [
// ---------- Verbal ----------
{id:'g001',sec:'V',skill:'gre_se',front:'Sentence Equivalence: how many choices do you select?',back:'Exactly two, from six. Both must produce sentences alike in meaning, and there is no partial credit. If only one choice fits, you have misread the sentence.'},
{id:'g002',sec:'V',skill:'gre_se',front:'The commonest Sentence Equivalence trap',back:'A synonym pair that fits the grammar but not the meaning. Two words matching each other is not the test; both have to fit the sentence. Predict the blank before reading the choices.'},
{id:'g003',sec:'V',skill:'gre_tc',front:'Text Completion: how many choices per blank?',back:'One blank gives five choices. Two or three blanks give three choices each. Blanks are scored together: every blank must be right for the item to count.'},
{id:'g004',sec:'V',skill:'gre_tc',front:'Signal words that reverse a thought',back:'Although, despite, far from, yet, nonetheless, paradoxically. They flip the blank against the clause you just read. Underline them before choosing.'},
{id:'g005',sec:'V',skill:'gre_tc',front:'Signal words that continue a thought',back:'Moreover, indeed, in fact, similarly, and a colon. The blank agrees with what came before, often intensifying it.'},
{id:'g006',sec:'V',skill:'gre_rc',front:'Reading Comprehension: what does a primary purpose question want?',back:'What the passage as a whole does, in a verb. Describe, revise, argue, reconcile, question. A choice true of one paragraph only is wrong however accurate it is.'},
{id:'g007',sec:'V',skill:'gre_rc',front:'How to answer a function question',back:'Ask what the sentence is doing for the argument, not what it says. It usually supports, qualifies, contrasts with, or sets up the claim next to it.'},
{id:'g008',sec:'V',skill:'gre_rc',front:'Select-in-passage items',back:'You click a sentence in the passage rather than choose a letter. Match the exact demand of the stem; a sentence that is merely relevant will not do.'},
{id:'g009',sec:'V',skill:'gre_rc',front:'Inference on the GRE',back:'What must be true given the passage, not what is likely. If you need outside knowledge or a plausible story to get there, it is not the answer.'},
// ---------- Quantitative ----------
{id:'g010',sec:'Q',skill:'gre_arith',front:'The four Quantitative Comparison choices',back:'A: Quantity A is greater. B: Quantity B is greater. C: they are equal. D: cannot be determined. D is only available when a variable can change the outcome, never when both quantities are fixed numbers.'},
{id:'g011',sec:'Q',skill:'gre_arith',front:'Quantitative Comparison strategy',back:'Try to make the two sides equal, then try to break the tie. If you can produce both equal and unequal cases, the answer is D. If the quantities are pure numbers, D is impossible.'},
{id:'g012',sec:'Q',skill:'gre_arith',front:'Successive percent changes',back:'They multiply, they do not add. Down 25 percent then down 20 percent is 0.75 times 0.8, which is 0.6, a 40 percent fall, not 45.'},
{id:'g013',sec:'Q',skill:'gre_arith',front:'Percent change formula',back:'(new minus old) divided by old. Always divide by the original value. Dividing by the new value answers a different question.'},
{id:'g014',sec:'Q',skill:'gre_arith',front:'Comparing powers with different bases',back:'Rewrite to a common exponent. 2 to the 30 is 8 to the 10; 3 to the 20 is 9 to the 10. Now the comparison is obvious.'},
{id:'g015',sec:'Q',skill:'gre_alg',front:'Sum and product of quadratic roots',back:'For x squared plus bx plus c, the roots sum to negative b and multiply to c. Faster than factoring when the question only wants the sum.'},
{id:'g016',sec:'Q',skill:'gre_alg',front:'Powers of a number between 0 and 1',back:'Higher powers get smaller. For y between 0 and 1, y cubed is less than y squared is less than y. The usual intuition only holds above 1.'},
{id:'g017',sec:'Q',skill:'gre_alg',front:'Combined work rates',back:'Add the rates, not the times. One job in 6 hours plus one in 3 hours is one sixth plus one third, which is one half per hour, so 2 hours together.'},
{id:'g018',sec:'Q',skill:'gre_geo',front:'Common right triangles',back:'3-4-5 and its multiples, 5-12-13, 8-15-17. Also 45-45-90 with sides 1, 1, root 2 and 30-60-90 with 1, root 3, 2.'},
{id:'g019',sec:'Q',skill:'gre_geo',front:'Circle formulas',back:'Area is pi r squared, circumference is 2 pi r. Given the area, solve for r first; do not use the area value as the radius.'},
{id:'g020',sec:'Q',skill:'gre_geo',front:'Distance between two points',back:'Square root of the sum of the squared differences. It is the Pythagorean theorem with the horizontal and vertical gaps as legs.'},
{id:'g021',sec:'Q',skill:'gre_geo',front:'Scaling a solid',back:'Multiplying a length by k multiplies area by k squared and volume by k cubed. In a cylinder, doubling the radius quadruples the volume because the radius is squared.'},
{id:'g022',sec:'Q',skill:'gre_data',front:'Mean against median',back:'The mean follows outliers, the median does not. A single large value pulls the mean above the median and leaves the median unmoved.'},
{id:'g023',sec:'Q',skill:'gre_data',front:'Standard deviation in one line',back:'Spread around the mean. Identical values give a standard deviation of 0. Two lists can share a mean and have completely different spreads.'},
{id:'g024',sec:'Q',skill:'gre_data',front:'Combinations against permutations',back:'If order does not matter, use n choose r. A committee is unordered, a ranking is ordered. Dividing by r factorial converts one to the other.'},
{id:'g025',sec:'Q',skill:'gre_data',front:'Probability without replacement',back:'The denominator shrinks after each draw. Two reds from 4 red and 6 blue is 4 over 10 times 3 over 9, not 4 over 10 twice.'},
{id:'g026',sec:'Q',skill:'gre_data',front:'Average speed',back:'Total distance over total time, never the average of the speeds. Equal distances at different speeds always average below the midpoint, because more time is spent slow.'},
// ---------- General ----------
{id:'g027',sec:'G',skill:'gre_rc',front:'GRE section structure',back:'Analytical Writing first, one 30-minute Issue task. Then Verbal in two sections of 12 and 15 questions, and Quantitative in two of 12 and 15. About 1 hour 58 minutes of testing (ETS).'},
{id:'g028',sec:'G',skill:'gre_arith',front:'How the GRE adapts',back:'By section, not by question. Your performance on the first section of a measure sets the difficulty of the second. Within a section you can skip, return and change answers freely.'},
{id:'g029',sec:'G',skill:'gre_arith',front:'Calculator on the GRE',back:'A basic on-screen calculator is provided on the Quantitative measure. It will not save you from a bad setup, so translate the problem first and compute last.'},
{id:'g030',sec:'G',skill:'gre_rc',front:'Skipping and returning',back:'Because you can move freely within a section, take the cheap points first and flag the rest. Leaving a hard item for two minutes at the end costs nothing.'},
];
