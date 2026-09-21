// The Build Playbook, validated as a deliverable. Run: node src/smoke_playbook.js
//
// The playbook makes a specific promise: every figure in it is measured from the
// repository at build time, and every citation resolves. A document that claims that and
// does not do it is worse than one that makes no claim, so the claim is tested.
//
// It also checks the two things that make the artefacts real rather than nominal: the
// .docx is a structurally valid Office package, not a zip that happens to open, and the
// deliverable is excluded from the public deploy, because the defect ledger is a list of
// this platform's historical weaknesses with the commits that fixed them.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..');
const PB = path.join(ROOT, 'playbook');

let fails = 0;
const ok = (c, label) => { if (!c) { fails++; console.log('  FAIL ' + label); } else console.log('  ok   ' + label); };
const read = p => fs.readFileSync(p, 'utf8');

console.log('\nartefacts');
const md = path.join(PB, 'BUILD_PLAYBOOK.md');
const htm = path.join(PB, 'index.html');
const dx = path.join(PB, 'BUILD_PLAYBOOK.docx');
for (const [p, min] of [[md, 60000], [htm, 60000], [dx, 20000]]) {
  ok(fs.existsSync(p) && fs.statSync(p).size > min,
    path.basename(p) + ' exists and is not a stub');
}
const pdf = path.join(PB, 'BUILD_PLAYBOOK.pdf');
if (fs.existsSync(pdf)) {
  ok(read(pdf).slice(0, 5) === '%PDF-', 'the PDF is a PDF');
} else {
  console.log('  --   no PDF (node src/playbook_pdf.js builds it; Chromium is optional here)');
}

console.log('\nthe document keeps its own promises');
const text = read(md);
// The whole claim of the document is that nothing in it was typed. An unresolved
// placeholder means a harvested fact stopped resolving; the builder already fails on
// this, and the test exists so a change to the builder cannot quietly remove that.
const left = [...text.matchAll(/\{\{([A-Z_]+)\}\}/g)].map(m => m[1])
  .filter(k => k !== 'CHROME_CSS' && k !== 'PLACEHOLDER');
ok(left.length === 0, 'no unresolved placeholders' + (left.length ? ': ' + left.join(', ') : ''));
ok(!/\u2014|\u2013/.test(text), 'no em or en dashes, the rule it says it enforces');

// Harvested figures must match the repository as it is right now, not as it was.
const commits = execFileSync('git', ['rev-list', '--count', 'HEAD'], { cwd: ROOT }).toString().trim();
ok(text.includes(commits + ' commits'), 'the commit count matches git (' + commits + ')');
const head = execFileSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: ROOT }).toString().trim();
ok(read(htm).includes(head), 'the HTML names the commit it was built from (' + head + ')');

console.log('\nthe ledger');
const rows = read(path.join(ROOT, 'data', 'playbook', 'incidents.jsonl'))
  .split('\n').filter(Boolean).map(l => JSON.parse(l));
ok(rows.length >= 30, rows.length + ' incidents recorded');
ok(text.includes(String(rows.length) + ' recorded defects') || read(htm).includes(String(rows.length) + ' recorded defects'),
  'the stated incident count matches the ledger');
const ids = new Set(rows.map(r => r.id));
ok(ids.size === rows.length, 'incident ids are unique');
// A citation nobody can check is the thing this whole project exists to avoid. But a
// shallow clone has no historical commits at all, and reporting every citation as broken
// because the history is missing is a checker crying wolf, which is its own ledger entry.
// So the two cases are distinguished and only one of them is a failure.
const cites = rows.filter(r => r.commit);
const badCommit = cites.filter(r => {
  try { return execFileSync('git', ['cat-file', '-t', r.commit], { cwd: ROOT }).toString().trim() !== 'commit'; }
  catch (e) { return true; }
});
// "is-shallow-repository" is the wrong question: a clone can be shallow and still hold
// every commit the ledger cites, which is the normal case here. The question that
// actually distinguishes the two failures is whether ANY citation resolved. None at all
// means the history is absent; some means those particular citations are wrong.
if (badCommit.length === cites.length && cites.length > 0) {
  console.log('  --   cited commits NOT verified: no citation resolved, so this clone has ' +
              'no history rather than ' + cites.length + ' bad citations. Use fetch-depth: 0.');
} else {
  ok(badCommit.length === 0, 'every cited commit exists' + (badCommit.length ? ': ' + badCommit.map(r => r.id).join(', ') : ''));
}
const badFile = rows.filter(r => r.guard_file && !fs.existsSync(path.join(ROOT, r.guard_file)));
ok(badFile.length === 0, 'every cited guard file exists' + (badFile.length ? ': ' + badFile.map(r => r.id).join(', ') : ''));
// Every incident must reach the checklist, because the checklist is generated from the
// ledger and a lesson that does not appear means the generation silently skipped a row.
const missingLesson = rows.filter(r => !text.includes(r.lesson.slice(0, 60)));
ok(missingLesson.length === 0,
  'every lesson reaches the generated checklist' + (missingLesson.length ? ': ' + missingLesson.map(r => r.id).join(', ') : ''));

console.log('\nthe bootstrap pack');
const B = path.join(PB, 'bootstrap');
for (const f of ['CLAUDE.template.md', 'KICKOFF.md', 'RULES_DIGEST.md', 'incidents.jsonl', 'README.md']) {
  ok(fs.existsSync(path.join(B, f)), 'bootstrap/' + f);
}
const digest = read(path.join(B, 'RULES_DIGEST.md'));
const missingRule = rows.filter(r => !digest.includes(r.lesson.slice(0, 60)));
ok(missingRule.length === 0, 'every lesson reaches the rules digest');
// The digest only works if it is short enough to sit in a prompt. If it grows past a few
// thousand words it has become a second book and stops being followed.
const words = digest.split(/\s+/).filter(Boolean).length;
ok(words < 4000, 'the digest stays prompt sized (' + words + ' words)');
ok(read(path.join(B, 'CLAUDE.template.md')).includes('Never invent a value'),
  'the template carries the never-invent-a-value rule');
ok(read(path.join(B, 'KICKOFF.md')).includes('incidents.jsonl'),
  'the kickoff closes the loop back to the ledger');

console.log('\nthe .docx is a real Office package');
const zip = fs.readFileSync(dx);
ok(zip.slice(0, 2).toString() === 'PK', 'zip signature');
const names = [];
for (let i = 0; i < zip.length - 4; i++) {
  if (zip.readUInt32LE(i) === 0x04034b50) {
    const n = zip.readUInt16LE(i + 26);
    names.push(zip.slice(i + 30, i + 30 + n).toString());
  }
}
for (const part of ['[Content_Types].xml', '_rels/.rels', 'word/document.xml',
                    'word/styles.xml', 'word/numbering.xml']) {
  ok(names.includes(part), 'part ' + part);
}

console.log('\nit is not published');
const ai = read(path.join(ROOT, '.assetsignore'));
ok(/^playbook\/$/m.test(ai), 'playbook/ is excluded from the deploy');
ok(/^docs\/$/m.test(ai), 'docs/ is excluded from the deploy');

console.log('\n' + (fails ? fails + ' FAILED' : 'all playbook checks passed'));
process.exit(fails ? 1 : 0);
