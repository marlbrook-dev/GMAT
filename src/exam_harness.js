// One place that knows how to boot an exam: its bank files, its globals, and the engine.
//
// This used to live inside test.js as five consts. The review bots need exactly the same
// thing, and a second copy of a list of thirty bank filenames is a list that goes stale the
// first time somebody adds bank_quant7.js to one of them. So both load from here.
//
// Nothing about an exam's CONTENT lives here. The bot reads EXAM, SECTIONS, SECTION_META
// and SKILLS back out of the engine, because the engine resolves those from EXAM_ID and it
// is the only thing entitled to say what a section key is. A bot that hardcoded 'Q' or 'RW'
// would be asserting the structure it is supposed to be checking.
const fs = require('fs'), vm = require('vm'), path = require('path');

const SRC = __dirname;

const EXAM_FILES = [
 {id:'gmat-focus', choices:5,
  files:['bank_quant.js','bank_quant2.js','bank_quant3.js','bank_quant4.js','bank_quant5.js','bank_quant6.js','bank_verbal.js','bank_verbal2.js','bank_verbal3.js','bank_verbal4.js','bank_verbal5.js','bank_verbal6.js','bank_verbal7.js','bank_verbal8.js','bank_di.js','bank_di2.js','bank_di3.js','bank_di4.js','bank_di5.js','bank_di6.js','bank_di7.js','bank_di8.js','bank_di9.js','cards.js','cards2.js','cards3.js','playbook_gmat.js'],
  concat:'BANK_QUANT,BANK_QUANT2,BANK_QUANT3,BANK_QUANT4,BANK_QUANT5,BANK_QUANT6,BANK_VERBAL,BANK_VERBAL2,BANK_VERBAL3,BANK_VERBAL4,BANK_VERBAL5,BANK_VERBAL6,BANK_VERBAL7,BANK_VERBAL8,BANK_DI,BANK_DI2,BANK_DI3,BANK_DI4,BANK_DI5,BANK_DI6,BANK_DI7,BANK_DI8,BANK_DI9', gen:'gmat'},
 {id:'gre', choices:5, choicesByType:{QC:4},
  files:['bank_gre_verbal.js','bank_gre_verbal2.js','bank_gre_quant.js','bank_gre_quant2.js','bank_gre_easy.js','writing_gre.js','cards_gre.js','playbook_gre.js'],
  concat:'BANK_GRE_VERBAL,BANK_GRE_VERBAL2,BANK_GRE_QUANT,BANK_GRE_QUANT2,BANK_GRE_EASY', gen:'gre'},
 // The LSAT carries no generated bank: its items are arguments and passages, with no
 // parameterised schema behind them, so gen is null and the run skips that file.
 {id:'lsat', choices:5,
  files:['bank_lsat_lr.js','bank_lsat_lr2.js','bank_lsat_rc.js','bank_lsat_rc2.js','cards_lsat.js','playbook_lsat.js'],
  concat:'BANK_LSAT_LR,BANK_LSAT_LR2,BANK_LSAT_RC,BANK_LSAT_RC2', gen:null},
 {id:'act', choices:4,
  files:['bank_act_english.js','bank_act_reading.js','bank_act_science.js','cards_act.js','playbook_act.js'],
  concat:'BANK_ACT_ENGLISH,BANK_ACT_READING,BANK_ACT_SCIENCE', gen:'act'},
 {id:'sat', choices:4,
  files:['bank_sat_rw.js','bank_sat_rw2.js','bank_sat_rw3.js','bank_sat_rw4.js','bank_sat_rw5.js','bank_sat_math.js','bank_sat_math2.js','bank_sat_math3.js','bank_sat_math4.js','bank_sat_math5.js','bank_sat_easy.js','cards_sat.js','cards_sat2.js','playbook_sat.js'],
  concat:'BANK_SAT_RW,BANK_SAT_RW2,BANK_SAT_RW3,BANK_SAT_RW4,BANK_SAT_RW5,BANK_SAT_MATH,BANK_SAT_MATH2,BANK_SAT_MATH3,BANK_SAT_MATH4,BANK_SAT_MATH5,BANK_SAT_EASY', gen:'sat'},
];

const byId = {};
EXAM_FILES.forEach(e => { byId[e.id] = e; });

// engine.js declares with const, which stays in the script's lexical scope rather than
// becoming a property of the context, so the script itself has to hand the pieces back out.
const EXPORTS = 'BANK,SKILLS,SECTION_META,SECTIONS,PLAYBOOK,CARDS,EXAM,newState,pickQuestions,' +
 'recordAttempt,skillStats,sectionSummary,pickMockSection,pickSatModule,satRoute,' +
 'satDomainTargets,gradeChosen,timingFlag,scoreEstimate,sectionAbility,itemInfo,eloToTheta,' +
 'pCorrect,DIFF_ELO';

/** Boot one exam and return its engine api plus the spec it was booted from. */
function load(spec, opts) {
 opts = opts || {};
 const rng = opts.random || Math.random;
 const genFile = spec.gen ? path.join('generated', 'bank_gen_' + spec.gen + '.js') : null;
 if (genFile && !fs.existsSync(path.join(SRC, genFile))) {
  throw new Error('missing ' + genFile + '; run python3 src/build_banks.py first');
 }
 const names = spec.files.concat(genFile ? [genFile] : []).concat(['engine.js']);
 const src = names.map(f => fs.readFileSync(path.join(SRC, f), 'utf8')).join('\n');

 // Math is passed through with a swappable random so a bot run can be made deterministic.
 // Everything else about the engine sees the ordinary globals it expects.
 const M = Object.create(Math);
 M.random = rng;
 const ctx = { console, Date, JSON, Set, Map, Math: M, EXAM_ID: spec.id };
 vm.createContext(ctx);
 const allBanks = spec.concat + (spec.gen ? (',BANK_GEN_' + spec.gen.toUpperCase()) : '');
 vm.runInContext(
  'var EXAM_ID=' + JSON.stringify(spec.id) + ';\n' + src +
  '\nvar BANK=[].concat(' + allBanks + ');\nglobalThis.__api={' + EXPORTS + '};', ctx);
 return ctx.__api;
}

/** A small deterministic generator, so a failing bot run can be reproduced exactly. */
function seeded(seed) {
 let s = seed >>> 0 || 1;
 return function () {
  s ^= s << 13; s >>>= 0;
  s ^= s >> 17;
  s ^= s << 5; s >>>= 0;
  return s / 4294967296;
 };
}

module.exports = { EXAM_FILES, byId, load, seeded, SRC };
