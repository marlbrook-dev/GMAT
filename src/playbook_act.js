// ACT playbook: the methods behind every reporting category the engine tracks.
const PLAYBOOK=[
 {skill:'act_e_pow',sec:'E',title:'Production of Writing',items:[
  'When the stem states a goal, the goal decides. The correct choice does the job the question names even if another choice reads better.',
  'On add or delete questions, ask whether the sentence supports the point of its paragraph. Interesting is not the standard; relevant to the stated purpose is.',
  'Place a sentence by following its pronouns and transitions. A sentence opening with this rule or that change must come after whatever it refers to.',
  'Choose a transition only after naming the relationship between the two sentences. If they simply continue, the answer is often no transition at all.']},
 {skill:'act_e_kol',sec:'E',title:'Knowledge of Language',items:[
  'Shortest grammatical choice that keeps the meaning. Redundancy is the most heavily tested error on the section.',
  'Match the tone of the passage rather than your own taste. Plain reporting rejects both inflated praise and choices so clipped that information is lost.',
  'Precise means precise. Near synonyms are built to be wrong, so read the sentence for what is actually being claimed before choosing.',
  'Watch for a shift in register mid-passage. A formal essay does not suddenly use slang, and a personal narrative does not suddenly use bureaucratic phrasing.']},
 {skill:'act_e_cse',sec:'E',title:'Conventions of Standard English',items:[
  'Comma before and only when it joins two independent clauses. Two verbs sharing a subject take no comma between them.',
  'Punctuate nonessential phrases in matching pairs: two commas, two dashes or two parentheses. A single comma or a mismatched pair is wrong.',
  'Find the subject by crossing out prepositional phrases. The plural noun nearest the verb is usually the trap in an agreement question.',
  'The noun after an opening participial phrase must be the one performing that action, or the modifier dangles.',
  'Use the past perfect only when one past action finished before another. On this test had is wrong more often than it is right.']},
 {skill:'act_m_nq',sec:'M',title:'Number and Quantity',items:[
  'Exponent rules: same base multiplied adds exponents, divided subtracts, a power of a power multiplies, a negative exponent is a reciprocal, a fractional exponent is a root.',
  'Powers of i cycle every four, so reduce the exponent modulo 4 before evaluating.',
  'For radicals, simplify by pulling out perfect squares before combining. Only like radicals can be added.',
  'Matrix questions on this test are mostly scalar multiplication and addition, which apply entry by entry.']},
 {skill:'act_m_alg',sec:'M',title:'Algebra',items:[
  'Check the answer choices before solving. Testing four numbers is often faster than isolating a variable, and it cannot go wrong algebraically.',
  'Substitute when a variable is already isolated and eliminate when the coefficients line up.',
  'For inequalities, remember that multiplying or dividing by a negative flips the sign.',
  'When a word problem names a total and a difference, write both equations before touching either.']},
 {skill:'act_m_fun',sec:'M',title:'Functions',items:[
  'f(g(x)) applies g first. Composition is not multiplication and the order matters.',
  'Vertex form y = a(x - h)^2 + k gives the vertex at (h, k) and the axis of symmetry at x = h.',
  'To read a graph, find intercepts and turning points first; most questions are answered from those alone.',
  'A transformation inside the parentheses moves the graph horizontally and in the opposite direction from the sign; outside, it moves vertically in the direction of the sign.']},
 {skill:'act_m_geo',sec:'M',title:'Geometry',items:[
  'Learn the two special right triangles cold: 30-60-90 in the ratio 1, root 3, 2, and 45-45-90 in the ratio 1, 1, root 2.',
  'SOHCAHTOA applies only in a right triangle. If there is no right angle, look for one you can draw.',
  'The circle equation (x - h)^2 + (y - k)^2 = r^2 hides a sign flip: x + 3 puts the centre at negative 3.',
  'For composite figures, break the shape into pieces whose areas you know, then add or subtract.']},
 {skill:'act_m_sp',sec:'M',title:'Statistics and Probability',items:[
  'Outliers move the mean far more than the median, which is what most centre and spread questions actually test.',
  'For A or B, add and subtract the overlap. For independent events together, multiply.',
  'Without replacement changes the denominator on the second draw, and that is the usual trap.',
  'Read a scatterplot for direction and strength before estimating any line of best fit.']},
 {skill:'act_m_ies',sec:'M',title:'Integrating Essential Skills',items:[
  'Percent change is the difference over the original. A 20 percent rise followed by a 20 percent fall does not return to the start, because the base moved.',
  'Set up proportions with the units written in. If the units do not cancel to what the question asks for, the setup is wrong.',
  'Multi-step questions are where the section hides its difficulty. Write each step down; the arithmetic is rarely the problem, the sequence is.',
  'At about 67 seconds a question, protect the early items. Questions run roughly easiest to hardest, so an unchecked question 12 costs more than an unsolved question 40.']},
 {skill:'act_r_kid',sec:'R',title:'Key Ideas and Details',items:[
  'Take main idea and structure from the first read and leave the details where you can find them again.',
  'For a detail question, return to the text. The section rewards locating the line, not remembering it.',
  'Inference here means supported by the passage, not merely consistent with it.',
  'Do EXCEPT questions last within a part. Three choices must be found in the text, which is slow by design.']},
 {skill:'act_r_cs',sec:'R',title:'Craft and Structure',items:[
  'For a word in context, blank the word out, predict a replacement, then choose. The common meaning is usually the wrong one.',
  'Author perspective lives in adjectives and qualifiers, not in subject matter.',
  'A structure question asks what a paragraph does for the passage: it introduces, complicates, illustrates, or answers what came before.',
  'Distinguish the narrator voice from a character voice in literary narrative parts; questions regularly turn on which one a line belongs to.']},
 {skill:'act_r_iki',sec:'R',title:'Integration of Knowledge and Ideas',items:[
  'Read paired passages one at a time and answer the single-passage questions before any comparison.',
  'Comparison questions ask how the texts relate: whether one qualifies, extends or contradicts the other.',
  'For what would author A say about author B, find the claim both address. If they address different questions, the answer often says exactly that.',
  'When a part includes a chart or figure, treat it as another text and check whether it supports or complicates the prose.']},
 {skill:'act_s_iod',sec:'S',title:'Interpretation of Data',items:[
  'Start with the questions, not the introduction. Most items name a specific table or figure.',
  'Read axis labels, units and column headings before reading a single value. Units are where careless points go.',
  'For a trend, check the first value, the last, and one in the middle to catch a rise then fall.',
  'Interpolation between measured points is safe; extrapolation beyond them assumes the trend continues, which some questions are built to punish.']},
 {skill:'act_s_si',sec:'S',title:'Scientific Investigation',items:[
  'Whatever differs between two experiments is what they were designed to compare. Everything held constant is there to keep the comparison clean.',
  'A control group provides the baseline. Questions asking why a condition was included usually have this answer.',
  'To isolate a variable, hold the others fixed. A proposed follow-up experiment that changes two things at once is always wrong.',
  'Ask what a design cannot tell you. Small samples, short durations and single sites limit what a result can support.']},
 {skill:'act_s_esa',sec:'S',title:'Evaluation of Scientific Arguments and Models',items:[
  'On conflicting viewpoints, note the common ground first. Most questions turn on the single point where the two accounts part.',
  'New evidence strengthens a view only if it bears on the disputed point rather than on the shared background.',
  'The most informative test is a comparison in which one proposed cause is present and the other absent.',
  'To check a model against data, test the relationship it claims, not merely the direction. A quantity falling as another rises does not make the two inversely proportional.']}
];
