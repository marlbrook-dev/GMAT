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
// GRE General Test. Structure from ETS: Analytical Writing, then Verbal Reasoning in two
// sections of 12 and 15 questions (18 and 23 minutes), then Quantitative Reasoning in two
// sections of 12 and 15 (21 and 26 minutes), about 1 hour 58 minutes of testing. Verbal and
// Quantitative are section-level adaptive: the difficulty of the second section depends on
// performance on the first, which is the same shape as the digital SAT, so the module
// machinery is shared rather than duplicated.
//
// We train Verbal and Quantitative. Analytical Writing is a single 30-minute essay scored
// 0 to 6 by a human and an engine; scoring an essay is not something this trainer does, so
// it is documented on the exam guide and deliberately not simulated here.
const GRE_SKILLS = [
 {id:'gre_rc',section:'V',label:'Reading Comprehension',range:'roughly half of the Verbal questions',lo:12,hi:14,
  points:['Main idea and primary purpose','Inference from incomplete data','Author assumptions and perspective','Text structure and the function of a sentence','Strengthen and weaken an argument','Vocabulary in context']},
 {id:'gre_tc',section:'V',label:'Text Completion',range:'roughly a quarter of the Verbal questions',lo:6,hi:8,
  points:['One blank with five choices','Two or three blanks with three choices each','Reading the whole passage before committing to a blank','Signal words that reverse or continue a thought']},
 {id:'gre_se',section:'V',label:'Sentence Equivalence',range:'roughly a quarter of the Verbal questions',lo:6,hi:8,
  points:['Six choices, select exactly two','Both choices must produce sentences alike in meaning','Traps built from near synonyms that change the sentence','Predicting the blank before reading the choices']},
 {id:'gre_arith',section:'Q',label:'Arithmetic',range:'arithmetic topics',lo:6,hi:8,
  points:['Integers, divisibility, remainders','Fractions, decimals and percents','Ratios and proportion','Exponents and roots','Absolute value and number line reasoning']},
 {id:'gre_alg',section:'Q',label:'Algebra',range:'algebra topics',lo:6,hi:8,
  points:['Linear and quadratic equations','Inequalities','Simultaneous equations','Functions and sequences','Word problems translated into algebra']},
 {id:'gre_geo',section:'Q',label:'Geometry',range:'geometry topics',lo:5,hi:7,
  points:['Lines, angles and triangles','Circles','Polygons and area','Three-dimensional figures and volume','Coordinate geometry']},
 {id:'gre_data',section:'Q',label:'Data Analysis',range:'data analysis topics',lo:6,hi:8,
  points:['Mean, median, mode and range','Standard deviation and distributions','Counting, permutations and combinations','Probability','Reading graphs and tables']}
];
// Verbal 12 then 15 in 18 then 23 minutes; Quantitative 12 then 15 in 21 then 26 minutes.
// allot is the per-question pace those lengths imply. moduleSizes carries the unequal pair,
// which is the one structural difference from the SAT, whose modules are equal.
const GRE_SECTIONS = {
 V:{name:'Verbal Reasoning',short:'Verbal',allot:90,questions:12,minutes:18,modules:2,
    moduleSizes:[12,15],moduleMinutes:[18,23],domainOrder:['gre_rc','gre_tc','gre_se']},
 Q:{name:'Quantitative Reasoning',short:'Quantitative',allot:105,questions:12,minutes:21,modules:2,
    moduleSizes:[12,15],moduleMinutes:[21,26],domainOrder:['gre_arith','gre_alg','gre_geo','gre_data']}
};
// LSAT. Structure from LSAC: four 35-minute multiple-choice sections, one Reading
// Comprehension, two Logical Reasoning and one unscored variable section that can be either
// type and can appear anywhere, plus a 10-minute intermission between the second and third
// sections. Three sections are scored. Scores are reported 120 to 180; the raw score is the
// number of questions answered correctly with no deduction for wrong answers, so there is no
// guessing penalty to model. Five answer choices, confirmed against LSAC sample questions.
//
// LSAC does not publish a subscore breakdown, so the skills below are LSAC's own published
// lists of what each section measures, grouped so that a single practice section can cover
// every one of them. Each group carries the published wording as its points.
//
// We train one Logical Reasoning section; the real exam delivers two. LSAT Argumentative
// Writing is a separately administered, unscored essay, so it is documented on the exam guide
// and deliberately not simulated here, the same call the GRE trainer makes on its essay.
const LSAT_SKILLS = [
 {id:'lsat_lr_struct',section:'LR',label:'Argument Parts and Structure',range:'Logical Reasoning',lo:3,hi:5,
  points:['Recognizing the parts of an argument and their relationships','Telling a premise from a conclusion','The role a claim plays in the argument']},
 {id:'lsat_lr_concl',section:'LR',label:'Drawing Well-Supported Conclusions',range:'Logical Reasoning',lo:3,hi:5,
  points:['Drawing well-supported conclusions','What must be true on the stated evidence','Reading quantity words exactly as written']},
 {id:'lsat_lr_assum',section:'LR',label:'Detecting Assumptions',range:'Logical Reasoning',lo:3,hi:5,
  points:['Detecting assumptions made by particular arguments','Necessary versus sufficient assumptions','The gap between evidence and conclusion']},
 {id:'lsat_lr_flaw',section:'LR',label:'Identifying Flaws in Arguments',range:'Logical Reasoning',lo:3,hi:5,
  points:['Identifying flaws in arguments','Naming the error rather than disagreeing with it','Common patterns of bad reasoning']},
 {id:'lsat_lr_evid',section:'LR',label:'Effect of Additional Evidence',range:'Logical Reasoning',lo:3,hi:5,
  points:['Determining how additional evidence affects an argument','Strengthening and weakening','Ruling out an alternative explanation']},
 {id:'lsat_lr_prin',section:'LR',label:'Principles, Rules and Analogy',range:'Logical Reasoning',lo:2,hi:4,
  points:['Identifying and applying principles or rules','Reasoning by analogy','Matching a case to the rule that governs it']},
 {id:'lsat_lr_expl',section:'LR',label:'Explanations and Parallel Reasoning',range:'Logical Reasoning',lo:2,hi:4,
  points:['Identifying explanations','Recognizing similarities and differences between patterns of reasoning','Recognizing misunderstandings or points of disagreement']},
 {id:'lsat_rc_main',section:'RC',label:'Main Idea and Primary Purpose',range:'Reading Comprehension',lo:3,hi:5,
  points:['The main idea or primary purpose','Holding the whole passage in view','Separating the thesis from the supporting material']},
 {id:'lsat_rc_stated',section:'RC',label:'Explicitly Stated Information',range:'Reading Comprehension',lo:3,hi:5,
  points:['Information that is explicitly stated','Finding the line that settles the question','Rejecting choices the passage never makes']},
 {id:'lsat_rc_inf',section:'RC',label:'Inference and Implication',range:'Reading Comprehension',lo:4,hi:7,
  points:['Information or ideas that can be inferred','Staying inside what the passage supports','The difference between implied and merely plausible']},
 {id:'lsat_rc_struct',section:'RC',label:'Meaning, Structure and Tone',range:'Reading Comprehension',lo:4,hi:6,
  points:['The meaning or purpose of words or phrases as used in context','The organization or structure','Attitude of the author as revealed in tone or language']},
 {id:'lsat_rc_app',section:'RC',label:'Application and Comparative Reading',range:'Reading Comprehension',lo:4,hi:7,
  points:['The application of information in the selection to a new context','Principles that function in the selection','Analogies to claims or arguments in the selection','The impact of new information on claims or arguments','Relationships between the two passages in comparative reading']}
];
// LSAC publishes 35 minutes per section. For Reading Comprehension it also publishes the shape
// of the section: four sets, each a selection followed by five to eight questions, with three or
// four single passages and one or no comparative pair, so a section runs 20 to 32 questions and
// our 26 sits inside that published range. LSAC does not publish a Logical Reasoning question
// count anywhere, so the 25 below is OUR practice-section length, chosen to fit the published
// 35 minutes, and is labeled as ours on the exam guide rather than presented as an LSAT fact.
const LSAT_SECTIONS = {
 LR:{name:'Logical Reasoning',short:'Logical Reasoning',allot:84,questions:25,minutes:35},
 RC:{name:'Reading Comprehension',short:'Reading Comprehension',allot:81,questions:26,minutes:35}
};
// ACT. Structure from ACT's own 2026-2027 "Preparing for the ACT Test" booklet: English 50
// questions in 35 minutes, Mathematics 45 in 50, Reading 36 in 40, and an optional Science
// section of 40 in 40. Every section carries embedded unscored field-test questions, so the
// scored counts are lower than the administered ones (English 40, Mathematics 41, Reading 27,
// Science 34). act.org states the whole multiple-choice test as 171 questions in 2 hours 45
// minutes, which is these four sections added up.
//
// Two things here are easy to get wrong from memory and are checked against ACT's own
// materials. First, the enhanced ACT uses FOUR answer choices in every section including
// Mathematics, which carried five on the legacy test. Second, the Composite is the average of
// English, Mathematics and Reading only: ACT removed Science from the Composite for national
// online testing in April 2025 and for all testing modes in September 2025. Science is still
// scored 1 to 36 and still reported, it just does not feed the Composite, which is why it
// carries inComposite:false below.
const ACT_SKILLS = [
 {id:'act_e_pow',section:'E',label:'Production of Writing',range:'38 to 43 percent of the section',lo:19,hi:22,
  points:['Topic development in terms of purpose and focus','Organization, unity and cohesion','Whether a text has met its intended goal']},
 {id:'act_e_kol',section:'E',label:'Knowledge of Language',range:'18 to 23 percent of the section',lo:9,hi:12,
  points:['Precise and concise word choice','Consistency in style and tone','Cutting redundancy']},
 {id:'act_e_cse',section:'E',label:'Conventions of Standard English',range:'38 to 43 percent of the section',lo:19,hi:22,
  points:['Sentence structure and formation','Punctuation','Usage']},
 {id:'act_m_nq',section:'M',label:'Number and Quantity',range:'10 to 12 percent of the section',lo:5,hi:6,
  points:['Real and complex number systems','Integer and rational exponents','Vectors and matrices']},
 {id:'act_m_alg',section:'M',label:'Algebra',range:'17 to 20 percent of the section',lo:8,hi:9,
  points:['Linear, polynomial, radical and exponential relationships','Systems of equations','Solutions applied to real-world contexts']},
 {id:'act_m_fun',section:'M',label:'Functions',range:'17 to 20 percent of the section',lo:8,hi:9,
  points:['Definition, notation and representation','Linear, radical, piecewise, polynomial, exponential and logarithmic functions','Manipulating and translating functions','Interpreting features of graphs']},
 {id:'act_m_geo',section:'M',label:'Geometry',range:'17 to 20 percent of the section',lo:8,hi:9,
  points:['Congruence and similarity','Surface area and volume','Missing values in triangles, circles and other figures','Trigonometric ratios and conic sections']},
 {id:'act_m_sp',section:'M',label:'Statistics and Probability',range:'12 to 15 percent of the section',lo:6,hi:7,
  points:['Center and spread of distributions','Data collection methods','Relationships in bivariate data','Probability and sample spaces']},
 {id:'act_m_ies',section:'M',label:'Integrating Essential Skills',range:'20 percent of the section',lo:9,hi:9,
  points:['Rates and percentages','Proportional relationships','Area, surface area and volume','Average and median','Expressing numbers in different ways','Non-routine problems combining skills in chains of steps']},
 {id:'act_r_kid',section:'R',label:'Key Ideas and Details',range:'44 to 52 percent of the section',lo:16,hi:19,
  points:['Central ideas and themes','Summarizing information accurately','Logical inferences and conclusions','Sequential, comparative and cause-effect relationships']},
 {id:'act_r_cs',section:'R',label:'Craft and Structure',range:'26 to 33 percent of the section',lo:9,hi:12,
  points:['Word and phrase meanings','Analyzing word choice rhetorically','Text structure','Purpose and perspective of the author','Points of view of characters']},
 {id:'act_r_iki',section:'R',label:'Integration of Knowledge and Ideas',range:'19 to 26 percent of the section',lo:7,hi:9,
  points:['Claims and evidence in arguments','Integrating information from multiple texts','Comparing sources that disagree']},
 {id:'act_s_iod',section:'S',label:'Interpretation of Data',range:'38 to 50 percent of the section',lo:15,hi:20,
  points:['Reading tables, graphs and diagrams','Recognizing trends in data','Interpolating and extrapolating','Translating tabular data into graphs']},
 {id:'act_s_si',section:'S',label:'Scientific Investigation',range:'18 to 32 percent of the section',lo:7,hi:13,
  points:['Experimental tools, procedures and design','Identifying controls and variables','Comparing, extending and modifying experiments','Predicting the results of additional trials']},
 {id:'act_s_esa',section:'S',label:'Evaluation of Scientific Arguments and Models',range:'24 to 38 percent of the section',lo:10,hi:15,
  points:['Judging the validity of scientific information','Formulating conclusions and predictions','Deciding which explanation new findings support','Weighing conflicting viewpoints']}
];
// allot is the per-question pace each published section length implies, rounded to the second.
// scored carries ACT's published scored count, which is what the section score is built from;
// questions is what the examinee actually answers.
const ACT_SECTIONS = {
 E:{name:'English',short:'English',allot:42,questions:50,scored:40,minutes:35},
 M:{name:'Mathematics',short:'Math',allot:67,questions:45,scored:41,minutes:50},
 R:{name:'Reading',short:'Reading',allot:67,questions:36,scored:27,minutes:40},
 S:{name:'Science',short:'Science',allot:60,questions:40,scored:34,minutes:40,optional:true,inComposite:false}
};
// Exam registry. Adding an exam (GRE, LSAT, ACT...) = a new entry here plus a tagged bank.
// Progress is stored per exam, so a student can train for two exams without the ratings mixing.
const EXAMS = {
 'gmat-focus': {id:'gmat-focus',name:'GMAT Focus Edition',short:'GMAT Focus',sections:GMAT_SECTIONS,skills:GMAT_SKILLS,
   scoreScale:'205-805',sectionScale:'60-90',choices:5,adaptive:'question',
   // Total scores are reported in 10-point steps ending in 5, so round to that lattice.
   appPath:'/app/',blurb:'Focus Edition, live',
   official:{label:'an official practice exam at mba.com',url:'https://www.mba.com/exams/gmat-exam/prepare'},
   crunch:'Which is bigger? No-calculator number sense, timed.',
   crunchLong:'Which is bigger? Sixty seconds of no-calculator number sense, the Quant survival skill.',
   goals:['Score 675+ for M7 programs','Fix my Quant from the diagnostic','Balance all three sections','Retake and beat my last score'],
   scale:{min:205,max:805,step:10,offset:5,center:555,slope:70,
          sectionMin:60,sectionMax:90,sectionCenter:75,sectionSlope:4.5,
          minBand:30,minAttempts:40,calibration:'internal'}},
 'sat': {id:'sat',name:'SAT',short:'SAT',sections:SAT_SECTIONS,skills:SAT_SKILLS,
   scoreScale:'400-1600',sectionScale:'200-800',choices:4,adaptive:'module',
   appPath:'/sat/app/',blurb:'digital format, live',
   official:{label:'an official Bluebook practice test from College Board',url:'https://bluebook.collegeboard.org/'},
   crunch:'Which is bigger? Estimate faster than you could type it.',
   crunchLong:'Which is bigger? Sixty seconds of estimation. Bluebook gives you Desmos, but typing costs seconds you do not have.',
   goals:['Clear 1400 for my target schools','Fix my Math from the diagnostic','Raise Reading and Writing accuracy','Retake and beat my last score'],
   scale:{min:400,max:1600,step:10,offset:0,center:1000,slope:200,
          sectionMin:200,sectionMax:800,sectionCenter:500,sectionSlope:100,
          minBand:30,minAttempts:40,calibration:'internal'}},
 // GRE reports 130 to 170 per measure in 1-point steps. The 260 to 340 total is the
 // conventional sum rather than a scale ETS publishes, so it is labeled as a range across
 // the two measures we train. The band floor is 5 points, which is the same share of the
 // scale that 30 points is on the GMAT, not a tighter claim on a smaller scale.
 'gre': {id:'gre',name:'GRE General Test',short:'GRE',sections:GRE_SECTIONS,skills:GRE_SKILLS,
   scoreScale:'260-340',sectionScale:'130-170',choices:5,adaptive:'module',
   appPath:'/gre/app/',blurb:'Verbal and Quant, live',
   official:{label:'an official POWERPREP practice test from ETS',url:'https://www.ets.org/gre/test-takers/general-test/prepare.html'},
   crunch:'Which is bigger? No-calculator number sense, timed.',
   crunchLong:'Which is bigger? Sixty seconds of no-calculator number sense, the Quant survival skill.',
   goals:['Break 320 for my target programs','Fix my Quant from the diagnostic','Raise Verbal accuracy','Retake and beat my last score'],
   scale:{min:260,max:340,step:1,offset:0,center:300,slope:14,
          sectionMin:130,sectionMax:170,sectionCenter:150,sectionSlope:7,
          minBand:5,minAttempts:40,calibration:'internal'}},
 // LSAT reports ONE number, 120 to 180, and no section scores at all, so the scale block
 // deliberately carries no sectionMin/sectionMax. scoreEstimate reads that absence and
 // suppresses per-section scores rather than inventing a subscore LSAC does not report.
 // The band floor of 3 points is the same share of a 60-point scale that 30 points is of the
 // GMAT's 600, not a tighter claim on a narrower scale.
 'lsat': {id:'lsat',name:'LSAT',short:'LSAT',sections:LSAT_SECTIONS,skills:LSAT_SKILLS,
   scoreScale:'120-180',sectionScale:null,choices:5,adaptive:'question',
   appPath:'/lsat/app/',blurb:'Logical Reasoning and RC, live',
   official:{label:'an official LSAT PrepTest on LSAC LawHub',url:'https://www.lsac.org/lsat/prepare/official-lsat-practice-tests'},
   crunch:'Which is bigger? Sixty seconds of number sense to keep timing instincts sharp.',
   crunchLong:'Which is bigger? Sixty seconds of number sense. The LSAT has no math section, but pace under a clock is the same muscle.',
   goals:['Break 170 for my target law schools','Fix my Logical Reasoning accuracy','Get through four RC passages in time','Retake and beat my last score'],
   scale:{min:120,max:180,step:1,offset:0,center:151,slope:10,
          minBand:3,minAttempts:40,calibration:'internal'}},
 // ACT reports each section 1 to 36 and a Composite that is the average of English,
 // Mathematics and Reading ONLY, rounded to the nearest whole number. Science is scored and
 // reported but excluded from the Composite, which SECTION_META marks with inComposite:false.
 'act': {id:'act',name:'ACT',short:'ACT',sections:ACT_SECTIONS,skills:ACT_SKILLS,
   scoreScale:'1-36',sectionScale:'1-36',choices:4,adaptive:'question',
   appPath:'/act/app/',blurb:'enhanced format, live',
   official:{label:'an official ACT practice test at act.org',url:'https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/free-act-test-prep.html'},
   crunch:'Which is bigger? Estimate faster than you could reach for the calculator.',
   crunchLong:'Which is bigger? Sixty seconds of estimation. The ACT gives you 60 seconds a question on Math, so reaching for the calculator has a price.',
   goals:['Reach a 30+ Composite','Fix my Math from the diagnostic','Speed up on Reading','Retake and beat my last score'],
   scale:{min:1,max:36,step:1,offset:0,center:20,slope:6,
          sectionMin:1,sectionMax:36,sectionCenter:20,sectionSlope:6,
          minBand:2,minAttempts:40,calibration:'internal'}}
};
// Exams with a guide page but no trainer yet. Kept here so the onboarding picker stays honest
// about what exists; mirrors LIVE in src/build_exams.py.
const UPCOMING_EXAMS = ['MCAT','Executive Assessment'];
// EXAM_ID is injected by the build (one app per exam). Node test runs default to the GMAT.
const CURRENT_EXAM = (typeof EXAM_ID !== 'undefined' && EXAMS[EXAM_ID]) ? EXAM_ID : 'gmat-focus';
const EXAM = EXAMS[CURRENT_EXAM];
const SKILLS = EXAM.skills;
const SECTION_META = EXAM.sections;
const SECTIONS = Object.keys(SECTION_META);
const DIFF_ELO = {1:800,2:950,3:1100,4:1250,5:1400};
const START_R = 1000, MASTERY_R = 1250;
// ---------------------------------------------------------------------------
// Ability model: from per-skill Elo to a scaled score band.
//
// Grounding. Pelanek, "Applications of the Elo rating system in adaptive educational
// systems" (Computers and Education, 2016) shows the Elo update used here,
//   P(correct) = 1 / (1 + e^-(theta - d)),  theta := theta + K(correct - P)
// is the Rasch (one-parameter IRT) model in everything but the estimation procedure. That
// is what lets us read an Elo rating as an IRT ability and attach a standard error to it,
// without the large-sample item pretesting a true IRT calibration would need.
//
// What is real here and what is ours, stated plainly because the distinction matters:
//   REAL      the Rasch functional form, the guessing-corrected information function, and
//             the standard error that falls out of it. Those are standard psychometrics.
//   OURS      the mapping from ability onto each exam's reported scale (the center and
//             slope in EXAM.scale). No public equating table exists for either exam, so
//             those constants are our calibration, not the test maker's. This is why the
//             product never calls the output a predicted score.
//
// The band narrows as someone practices, because information accumulates and the standard
// error shrinks with it. That is the system improving with use, and it is arithmetic
// rather than a promise.

// Elo uses a base-10 logistic on a 400-point spread; IRT works in natural-log logits.
// 400 / ln(10) = 173.7 converts between them.
const ELO_PER_LOGIT = 173.7;
const eloToTheta = r => (r - START_R) / ELO_PER_LOGIT;

// Probability of a correct answer under the shifted logistic, which credits the floor a
// multiple-choice test gives away. c comes from EXAM.choices, so a 5-choice GMAT item and a
// 4-choice SAT item are scored differently, as they should be.
function pCorrect(theta, d, c){
 const p = 1 / (1 + Math.exp(-(theta - d)));
 return c + (1 - c) * p;
}

// Fisher information for that item, the 3PL information function with discrimination fixed
// at 1. Guessing removes information, and the more answer choices an item has the smaller
// that loss is: a 5-choice GMAT item (c=0.2) is worth more evidence than a 4-choice SAT
// item (c=0.25), so the SAT needs slightly more items for the same precision. Falls back to
// the Rasch form when c is 0.
function itemInfo(theta, d, c){
 const P = pCorrect(theta, d, c);
 if (P <= 0 || P >= 1) return 0;
 if (!c) return P * (1 - P);
 return ((1 - P) / P) * Math.pow((P - c) / (1 - c), 2);
}

// Ability and its standard error for one section, from the attempts actually recorded.
// Every answered item contributes information at the difficulty it was answered at, which
// is why practising harder items tightens the band faster than drilling easy ones.
function sectionAbility(state, section){
 const c = 1 / (EXAM.choices || 4);
 const skills = SKILLS.filter(s => s.section === section);
 if (!skills.length) return {theta:0, sem:Infinity, n:0};
 let wSum = 0, tSum = 0, n = 0;
 skills.forEach(s => {
  const st = state.skills[s.id];
  if (!st) return;
  // Weight by evidence. A skill with 2 attempts should not move the section estimate as
  // much as one with 50.
  const w = Math.max(1, st.n || 0);
  tSum += eloToTheta(st.r) * w; wSum += w; n += (st.n || 0);
 });
 const theta = wSum ? tSum / wSum : 0;
 let info = 0;
 (state.attempts || []).forEach(a => {
  if (a.section !== section) return;
  const d = eloToTheta(DIFF_ELO[a.diff] || 1100);
  info += itemInfo(theta, d, c);
 });
 // Flashcards are recognition rather than full items, so they count, but at a quarter
 // weight. Counting them equally would shrink the band on evidence that is weaker than the
 // band implies.
 const cards = state.cards ? Object.keys(state.cards).length : 0;
 info += 0.25 * itemInfo(theta, theta, c) * Math.min(cards, 40);
 return {theta, sem: info > 0 ? 1/Math.sqrt(info) : Infinity, n};
}

const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
// Round onto the lattice the exam actually reports on (GMAT Focus totals end in 5).
function toLattice(v, sc){
 const step = sc.step || 10, off = sc.offset || 0;
 return clamp(Math.round((v - off) / step) * step + off, sc.min, sc.max);
}

// The headline estimate. Returns ready:false until there is enough evidence to say
// anything, because a score from six questions is noise wearing a number's clothes.
function scoreEstimate(state){
 const sc = EXAM.scale;
 if (!sc) return {ready:false, reason:'no scale'};
 const parts = SECTIONS.map(sec => ({sec, a: sectionAbility(state, sec)}));
 const n = parts.reduce((t, p) => t + p.a.n, 0);
 if (n < sc.minAttempts) return {ready:false, n, need: sc.minAttempts - n, reason:'more practice'};
 // Not every reported section feeds the headline score. The ACT Composite is the average of
 // English, Mathematics and Reading only, because ACT removed Science from the Composite in
 // 2025, so a section marked inComposite:false is still rated and still reported per section
 // but is kept out of the total. Everywhere else every section counts.
 const core = parts.filter(p => (SECTION_META[p.sec] || {}).inComposite !== false);
 const used = core.length ? core : parts;
 // Sections are equally weighted on every live exam; SECTION_META carries the shape if that
 // ever stops being true.
 const theta = used.reduce((t, p) => t + p.a.theta, 0) / used.length;
 // Independent section estimates, so the total standard error is the root mean square,
 // reduced by averaging across sections.
 const sem = Math.sqrt(used.reduce((t, p) => t + Math.pow(isFinite(p.a.sem) ? p.a.sem : 2, 2), 0)) / used.length;
 const raw = sc.center + sc.slope * theta;
 const half = Math.max(sc.minBand, sem * sc.slope);
 return {
  ready: true, n, theta, sem,
  score: toLattice(raw, sc),
  lo: toLattice(raw - half, sc),
  hi: toLattice(raw + half, sc),
  // A per-section score is only reported for exams whose maker reports one. The LSAT returns a
  // single 120 to 180 number and no section scores, so its scale block carries no sectionMin
  // and every section score here comes back null rather than as a subscore LSAC never gives.
  hasSectionScores: sc.sectionMin != null,
  sections: parts.map(p => ({
   section: p.sec,
   label: (SECTION_META[p.sec] || {}).short || p.sec,
   n: p.a.n,
   inComposite: (SECTION_META[p.sec] || {}).inComposite !== false,
   score: sc.sectionMin == null ? null
    : toLattice(sc.sectionCenter + sc.sectionSlope * p.a.theta,
                {min:sc.sectionMin, max:sc.sectionMax, step:1, offset:0})
  }))
 };
}

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
 if(q.answerType==='se') return Array.isArray(chosen)&&chosen.length===2&&Array.isArray(q.answer)&&q.answer.length===2
  &&chosen.slice().sort().join(',')===q.answer.slice().sort().join(',');
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
