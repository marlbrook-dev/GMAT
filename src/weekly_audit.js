// The weekly audit. One command that answers "is the site still good" and says what to
// fix, in priority order.
//
//   node src/weekly_audit.js           run everything, print a report
//   node src/weekly_audit.js --quick   skip the browser suites
//
// This exists so a check-in is a fixed, boring procedure rather than whatever the agent
// on duty happens to think of. Every gate below was added because something actually
// broke: the engine tests after a bank edit silently dropped a skill, the review bots
// after the score estimate sat on its starting value for forty questions, the build after
// a template change shipped an invisible button.
//
// Exit code is 0 only if nothing regressed. Anything else means read the report.
//
// What it deliberately does NOT do is change code. A check that can also fix itself is a
// check you stop trusting, because you can no longer tell a green run from a run that
// papered over the problem. It reports; a human or an agent decides.
const { execSync } = require('child_process');
const fs = require('fs'), path = require('path');

const QUICK = process.argv.includes('--quick');
const ROOT = path.join(__dirname, '..');
const CHROMIUM = (() => {
 try {
  return execSync('ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1',
   { encoding: 'utf8' }).trim();
 } catch (e) { return ''; }
})();

const results = [];
function gate(name, cmd, opts) {
 opts = opts || {};
 process.stdout.write('  running ' + name + ' ... ');
 const t0 = Date.now();
 let out = '', code = 0;
 try {
  out = execSync(cmd, {
   cwd: opts.cwd || ROOT, encoding: 'utf8', timeout: opts.timeout || 1800000,
   stdio: ['ignore', 'pipe', 'pipe'],
   env: Object.assign({}, process.env, { CHROMIUM_PATH: CHROMIUM }),
  });
 } catch (e) {
  code = e.status == null ? 1 : e.status;
  out = (e.stdout || '') + (e.stderr || '');
 }
 const secs = Math.round((Date.now() - t0) / 1000);
 console.log((code === 0 ? 'ok' : 'FAILED') + ' (' + secs + 's)');
 results.push({ name, code, out, secs, optional: !!opts.optional });
 return code === 0;
}

console.log('weekly audit  ' + new Date().toISOString().slice(0, 10) +
 (QUICK ? '  (quick: browser suites skipped)' : ''));
console.log('chromium: ' + (CHROMIUM || 'NOT FOUND, browser suites will fail'));
console.log('');

// The build is first because everything downstream reads what it produces, and because
// its own guards (inline script parsing, the dash rule, the count guard) are gates too.
gate('build', 'python3 src/build.py');
gate('blog', 'python3 src/build_blog.py', { optional: true });
gate('engine tests', 'node test.js', { cwd: path.join(ROOT, 'src') });
gate('review bots', 'node src/review_bot.js');
if (!QUICK) {
 gate('item rendering', 'node src/smoke_items.js');
 gate('consent and telemetry', 'node src/smoke_consent.js');
 gate('billing promises', 'node src/smoke_billing.js');
 gate('offline', 'node src/smoke_offline.js', { optional: true });
}

// ---- the report ------------------------------------------------------------------
console.log('\n' + '='.repeat(66));
const failed = results.filter(r => r.code !== 0 && !r.optional);
const softFailed = results.filter(r => r.code !== 0 && r.optional);

if (failed.length) {
 console.log('\nREGRESSIONS (' + failed.length + '), fix these first:\n');
 failed.forEach(r => {
  console.log('  ' + r.name);
  // The tail is where every one of these suites prints its summary, and the whole
  // output of a failing bank test is thousands of lines nobody reads.
  r.out.trim().split('\n').slice(-14).forEach(l => console.log('      ' + l));
  console.log('');
 });
}
if (softFailed.length) {
 console.log('Optional suites that did not pass: ' +
  softFailed.map(r => r.name).join(', ') + '\n');
}

// The review bots report findings even when they exit 0, and those findings are the
// backlog. Lift them out so the report says what to work on, not just what broke.
const bots = results.find(r => r.name === 'review bots');
if (bots) {
 const lines = bots.out.split('\n');
 const warn = lines.filter(l => /^\s{2}\[/.test(l));
 if (warn.length) {
  console.log('What the review bots want improved:\n');
  warn.forEach(l => console.log('  ' + l.trim()));
  console.log('');
 }
}

if (!failed.length) {
 console.log('No regressions. ' + results.filter(r => r.code === 0).length +
  ' of ' + results.length + ' suites green.\n');
}
console.log('Suggested order of work:');
console.log('  1. Anything under REGRESSIONS above.');
console.log('  2. Review bot findings, worst coverage number first.');
console.log('  3. Starving skills: the content gap the bots name by skill id and count.');
console.log('  4. Open items in ROADMAP.md.');

process.exit(failed.length ? 1 : 0);
