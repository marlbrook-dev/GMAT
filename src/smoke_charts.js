// The chart library's arithmetic, asserted without a browser.
//
//   node src/smoke_charts.js
//
// Geometry is separated from rendering in src/charts.js precisely so this can exist. The
// bugs worth catching in a chart are numbers in the wrong place: an axis that labels a
// value the plot never reaches, a stacked series that loses a segment, a histogram that
// drops its own maximum, a gap in the data drawn as a straight line across the hole.
// None of those need a DOM to catch, and none of them are caught by looking at a picture.
const C = require('./charts.js');

let failures = 0;
function fail(m) { failures++; console.log('  FAIL: ' + m); }
function ok(m) { console.log('  ok: ' + m); }
function eq(a, b, m) { if (JSON.stringify(a) !== JSON.stringify(b)) fail(m + '\n        expected ' + JSON.stringify(b) + '\n        got      ' + JSON.stringify(a)); }

console.log('\n=== chart geometry ===');

// ---- ticks -----------------------------------------------------------------
// An axis must never label a value outside the band it draws, and must never stop
// short of the data: a bar taller than the top gridline reads as a rendering bug.
(function () {
  const cases = [[0, 100], [0, 7], [0, 1], [0, 3500], [12, 88], [0, 0.4], [-20, 60]];
  let bad = [];
  for (const [lo, hi] of cases) {
    const t = C.ticks(lo, hi, 4);
    if (t[0] > lo) bad.push('ticks(' + lo + ',' + hi + ') starts above the minimum');
    if (t[t.length - 1] < hi) bad.push('ticks(' + lo + ',' + hi + ') stops below the maximum');
    if (t.length < 2) bad.push('ticks(' + lo + ',' + hi + ') gave fewer than two');
    for (let i = 1; i < t.length; i++) {
      const step = C.round(t[i] - t[i - 1], 6);
      const first = C.round(t[1] - t[0], 6);
      if (step !== first) bad.push('ticks(' + lo + ',' + hi + ') step is not uniform: ' + JSON.stringify(t));
    }
  }
  bad.length ? bad.forEach(fail) : ok(cases.length + ' tick ranges cover the data and step evenly');
})();

// Floating point is how tick rows get 0.30000000000000004 in them.
(function () {
  const t = C.ticks(0, 1, 5);
  const bad = t.filter(v => String(v).length > 6);
  bad.length ? fail('tick values carry float noise: ' + JSON.stringify(bad)) : ok('tick values are clean at fractional scale');
})();

// Degenerate input must not throw or produce NaN. A dashboard shows empty states.
(function () {
  const probes = [C.ticks(0, 0), C.ticks(5, 5), C.extent([]), C.extent([null, undefined]), C.histogram([], 5)];
  const bad = probes.filter(p => p === undefined || JSON.stringify(p).indexOf('null') > -1 && !Array.isArray(p));
  const nan = JSON.stringify(probes).indexOf('NaN') > -1;
  nan ? fail('degenerate input produced NaN: ' + JSON.stringify(probes)) : ok('empty and flat inputs degrade without NaN');
})();

// ---- scale -----------------------------------------------------------------
(function () {
  const s = C.scale(0, 100, 200, 0);              // inverted range, as a y axis is
  eq(s(0), 200, 'scale puts the domain minimum at the range start');
  eq(s(100), 0, 'scale puts the domain maximum at the range end');
  eq(s(50), 100, 'scale is linear through the middle');
  const flat = C.scale(5, 5, 0, 100);
  eq(flat(5), 50, 'a zero width domain centres rather than dividing by zero');
  if (!failures) ok('scale maps domain to range, including the degenerate case');
})();

// ---- line path -------------------------------------------------------------
// A missing week is a hole in the line. Drawing straight through it invents data.
(function () {
  const d = C.linePath([{ x: 0, y: 0 }, { x: 1, y: 1 }, { x: 2, y: null }, { x: 3, y: 3 }]);
  const moves = (d.match(/M/g) || []).length;
  if (moves !== 2) fail('a null point should break the line into two subpaths, got ' + moves + ': ' + d);
  else if (/NaN/.test(d)) fail('line path contains NaN: ' + d);
  else ok('a gap in the series breaks the line rather than bridging it');
})();

// ---- stacking --------------------------------------------------------------
(function () {
  const st = C.stack([[1, 2], [3, 4], [5, 6]]);
  eq(st[0], [[0, 1], [0, 2]], 'first series stacks from the baseline');
  eq(st[1], [[1, 4], [2, 6]], 'second series sits on the first');
  eq(st[2], [[4, 9], [6, 12]], 'third series sits on the running total');
  const tops = st[st.length - 1].map(p => p[1]);
  eq(tops, [9, 12], 'the top of the stack equals the column total');
  if (!failures) ok('stacking accumulates and the top equals the total');
})();

// ---- histogram -------------------------------------------------------------
(function () {
  const vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  const bins = C.histogram(vals, 5);
  const total = bins.reduce((t, b) => t + b.n, 0);
  if (total !== vals.length) fail('histogram lost values: ' + total + ' of ' + vals.length);
  // The maximum belongs in the last bin, not in a sixth bin off the end.
  else if (bins[bins.length - 1].n < 1) fail('histogram dropped its maximum out of the last bin');
  else ok('histogram bins every value and keeps the maximum');
  const flat = C.histogram([7, 7, 7], 4);
  const ft = flat.reduce((t, b) => t + b.n, 0);
  ft === 3 ? ok('a constant series still bins') : fail('constant series lost values: ' + ft);
})();

// ---- number formatting -----------------------------------------------------
(function () {
  eq(C.fmtNum(0), '0', 'zero formats as zero rather than empty');
  eq(C.fmtNum(999), '999', 'small integers are untouched');
  eq(C.fmtNum(12500), '13k', 'five figures abbreviate');
  eq(C.fmtNum(2400000), '2.4m', 'millions abbreviate');
  eq(C.fmtNum(null), '', 'null formats as empty, not as the string null');
  eq(C.fmtNum(NaN), '', 'NaN formats as empty');
  if (!failures) ok('numbers format without leaking null or NaN into the page');
})();

// ---- palette contract ------------------------------------------------------
// The validated hexes live in CSS, so what this can assert is the contract around them:
// that slots are fixed and cycle rather than being generated, and that status colours are
// never reachable as a series colour.
(function () {
  const first = C.color(0), sixth = C.color(5);
  if (first !== sixth) fail('a sixth series must fold back to slot one, not invent a hue');
  else if (!/^var\(--sfnc-c[1-5]\)$/.test(first)) fail('series colours must be theme tokens, got ' + first);
  else ok('series colours are fixed tokens and cycle rather than generating');
  const statusTokens = Object.keys(C.STATUS).map(k => C.STATUS[k]);
  const seriesTokens = [0, 1, 2, 3, 4].map(C.color);
  const overlap = statusTokens.filter(t => seriesTokens.indexOf(t) > -1);
  overlap.length ? fail('a status colour is reachable as a series colour: ' + overlap.join(', '))
    : ok('status colours are reserved and never used for a series');
})();

// ---- dark theme token parity ------------------------------------------------
// The way a dark mode actually breaks is not a wrong colour, it is a MISSING one: a
// semantic token that only exists in the light block keeps its light value on a dark
// surface, and you get near black text on near black. That is invisible in code review
// and obvious to a user, so it is checked here rather than looked for.
(function () {
  const fs = require('fs'), path = require('path');
  const tpl = fs.readFileSync(path.join(__dirname, 'app_template.html'), 'utf8');
  const lightM = tpl.match(/:root\{([\s\S]*?)\}/);
  const darkM = tpl.match(/:root\[data-theme="dark"\]\{([\s\S]*?)\}/);
  if (!lightM || !darkM) { fail('could not find both the light and dark token blocks'); return; }
  const names = b => new Set((b.match(/--[a-z0-9-]+\s*:/g) || []).map(x => x.replace(/\s*:$/, '')));
  const light = names(lightM[1]), dark = names(darkM[1]);

  // Only the SEMANTIC COLOUR layer needs a dark value. Selected by what the value IS
  // rather than by what the name starts with, because --text-heading is a colour and
  // --text-xs is a font size and they share a prefix. The raw ramps are the source the
  // semantic tokens draw from and are meant to stay put.
  const val = (b, n) => { const m = b.match(new RegExp(n + '\\s*:\\s*([^;}]+)')); return m ? m[1].trim() : null; };
  const isColour = v => v !== null && /(#[0-9a-f]{3,8}|rgba?\(|var\(--(navy|gold|gray|green|red|amber|blue|violet|teal|white))/i.test(v);
  const semantic = [...light].filter(n =>
    /^--(surface|text|border|brand|status|section|focus|shadow|accent)/.test(n) && isColour(val(lightM[1], n)));
  const missing = semantic.filter(n => !dark.has(n));
  missing.length
    ? fail(missing.length + ' semantic token(s) have no dark value, so they keep their light one on a dark surface:\n        ' + missing.join('\n        '))
    : ok(semantic.length + ' semantic tokens all have a dark value');

  // A dark value that is not actually different is a token somebody forgot to finish.
  const same = semantic.filter(n => dark.has(n) && val(lightM[1], n) === val(darkM[1], n));
  same.length ? fail('dark value identical to light for: ' + same.join(', ')) : ok('every dark token differs from its light value');

  // The charts were validated against one specific dark surface. If the app's surface
  // moves, that validation is void and nobody would notice.
  const surf = val(darkM[1], '--surface-card');
  surf && surf.toLowerCase() === '#111827'
    ? ok('the dark card surface still matches the surface the chart palette was validated against')
    : fail('dark --surface-card is ' + surf + ' but the chart palette was validated against #111827; re-run the palette validator');
})();

console.log(failures ? '\nFAILED: ' + failures : '\npassed');
process.exit(failures ? 1 : 0);
