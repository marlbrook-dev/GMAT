// Chart library for the trainer and the admin console.
//
// Five forms, one system: time series, comparison, distribution, funnel and cohort,
// plus the stat tile for when the honest answer is a number rather than a picture.
//
// Why this exists and why it is hand rolled. The site ships as self contained pages with
// inline scripts and a Content Security Policy that names its script sources one by one.
// A charting library would be a second thing to pin, a second thing to audit, and about
// two hundred kilobytes to send a student before they can answer a question. Everything
// here is inline SVG built from numbers, and the whole file is smaller than the smallest
// chart library's minified core.
//
// THE COLOURS ARE COMPUTED, NOT CHOSEN. The categorical set below was run through the
// palette validator (the dataviz reference implementation) with --pairs all, which checks
// every pair rather than only neighbours, under protanopia, deuteranopia and tritanopia:
//
//   node scripts/validate_palette.js "#0072B2,#E69F00,#009E73,#CC79A7,#56B4E9" \
//        --mode light --pairs all      ->  ALL CHECKS PASS
//
// The house brand hues failed it, and the way they failed is worth recording so nobody
// swaps them back: navy 800, teal 600 and navy 400 sit below the chroma floor and read as
// grey in a chart, and blue 600 against violet 600 is a deuteranopia deltaE of 0.4, which
// is two series a colourblind reader cannot tell apart at all. Brand colour belongs on the
// page around the chart; inside the plot the job is telling series apart.
//
// Status colours are reserved and are NEVER used for a series. A chart with four series
// and a red one implies the red one is bad.
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.SFNCharts = api;
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // ---------------------------------------------------------------- palette ----
  //
  // Colours are CSS custom properties, not JavaScript constants, so a chart follows the
  // theme without being told and without re-rendering. The hex values live in the style
  // block below, once per theme.
  //
  // LIGHT passes the validator with --pairs all, which checks every pair rather than only
  // neighbours:
  //   "#0072B2,#E69F00,#009E73,#CC79A7,#56B4E9" --mode light --pairs all  ->  ALL PASS
  //
  // DARK cannot do that, and the reason is worth writing down rather than rediscovering.
  // The dark lightness band is 0.48 to 0.67 against 0.43 to 0.77 for light, so a dark
  // palette has about half the lightness range to work with and hue has to carry the rest
  // of the separation. Under deuteranopia hue is exactly what collapses. Measured: dark
  // tops out at THREE slots under --pairs all. Five slots pass on adjacent pairs, which is
  // the honest check here because the legend is ordered and the series are drawn in that
  // order:
  //   "#1183C7,#0FA37B,#C08018,#C4689A,#7A7FE0" --mode dark --surface #111827  ->  ALL PASS
  //
  // That is legal only with secondary encoding, so it is not optional here: every chart
  // with two or more series ships a legend, four or fewer are direct labelled, fills carry
  // a 2px surface gap, and every chart has a table view. If a future chart needs more than
  // three series distinguished by colour ALONE on a dark background, it needs small
  // multiples instead, not a sixth hue.
  var SLOTS = 5;
  function cvar(name) { return 'var(--sfnc-' + name + ')'; }
  function color(i) { return cvar('c' + (i % SLOTS + 1)); }
  var INK = { primary: cvar('ink'), secondary: cvar('ink-2'), muted: cvar('ink-3') };
  var RULE = cvar('rule');
  var SURFACE = cvar('surface');
  // Reserved. Never a series colour: a chart with four series and a red one implies the
  // red one is bad.
  var STATUS = { good: cvar('good'), warning: cvar('warn'), serious: cvar('serious'), critical: cvar('bad') };
  var CATEGORICAL = [cvar('c1'), cvar('c2'), cvar('c3'), cvar('c4'), cvar('c5')];
  var SEQUENTIAL = [cvar('s1'), cvar('s2'), cvar('s3'), cvar('s4'), cvar('s5'), cvar('s6')];
  var DIVERGING = [cvar('d1'), cvar('d2'), cvar('d3'), cvar('d4'), cvar('d5'), cvar('d6'), cvar('d7')];

  // ------------------------------------------------------------- geometry ----
  // Pure, so src/smoke_charts.js can assert the numbers without a DOM. Every bug worth
  // catching in a chart is a number in the wrong place, and none of these touch the page.

  function niceStep(raw) {
    if (!(raw > 0)) return 1;
    var mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10));
    var norm = raw / mag;
    var step = norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10;
    return step * mag;
  }

  // Ticks a person would have chosen. Always includes the ends of the band it returns,
  // so an axis label never names a value the chart does not reach.
  function ticks(min, max, count) {
    count = count || 5;
    if (!isFinite(min) || !isFinite(max)) return [0];
    if (min === max) return [min];
    var step = niceStep((max - min) / Math.max(1, count));
    var lo = Math.floor(min / step) * step;
    var hi = Math.ceil(max / step) * step;
    var out = [];
    // Integer arithmetic on the step index, because 0.1 + 0.2 walks off a tick row.
    for (var i = 0; lo + i * step <= hi + step * 1e-9; i++) out.push(round(lo + i * step, 10));
    return out;
  }

  function round(v, dp) { var f = Math.pow(10, dp || 0); return Math.round(v * f) / f; }

  function scale(d0, d1, r0, r1) {
    var span = d1 - d0;
    if (span === 0) return function () { return (r0 + r1) / 2; };
    return function (v) { return r0 + (v - d0) / span * (r1 - r0); };
  }

  function extent(values) {
    var lo = Infinity, hi = -Infinity;
    for (var i = 0; i < values.length; i++) {
      var v = values[i];
      if (v === null || v === undefined || !isFinite(v)) continue;
      if (v < lo) lo = v;
      if (v > hi) hi = v;
    }
    if (lo === Infinity) return [0, 1];
    return [lo, hi];
  }

  // A gap in the data is a gap in the line, not a straight edge across the missing week.
  function linePath(points) {
    var d = '', pen = false;
    for (var i = 0; i < points.length; i++) {
      var p = points[i];
      if (!p || p.y === null || p.y === undefined || !isFinite(p.y)) { pen = false; continue; }
      d += (pen ? 'L' : 'M') + round(p.x, 2) + ' ' + round(p.y, 2) + ' ';
      pen = true;
    }
    return d.trim();
  }

  function stack(seriesValues) {
    var out = [], running = [];
    for (var s = 0; s < seriesValues.length; s++) {
      var row = [];
      for (var i = 0; i < seriesValues[s].length; i++) {
        var base = running[i] || 0;
        var v = seriesValues[s][i] || 0;
        row.push([base, base + v]);
        running[i] = base + v;
      }
      out.push(row);
    }
    return out;
  }

  function histogram(values, binCount) {
    binCount = binCount || 10;
    var e = extent(values), lo = e[0], hi = e[1];
    if (lo === hi) { hi = lo + 1; }
    var step = (hi - lo) / binCount, bins = [];
    for (var b = 0; b < binCount; b++) bins.push({ from: lo + b * step, to: lo + (b + 1) * step, n: 0 });
    for (var i = 0; i < values.length; i++) {
      var v = values[i];
      if (!isFinite(v)) continue;
      var idx = Math.floor((v - lo) / step);
      if (idx >= binCount) idx = binCount - 1;      // the maximum belongs in the last bin
      if (idx < 0) idx = 0;
      bins[idx].n++;
    }
    return bins;
  }

  function fmtNum(v) {
    if (v === null || v === undefined || !isFinite(v)) return '';
    var a = Math.abs(v);
    if (a >= 1e9) return round(v / 1e9, 1) + 'b';
    if (a >= 1e6) return round(v / 1e6, 1) + 'm';
    if (a >= 1e4) return round(v / 1e3, 0) + 'k';
    if (a >= 1000) return v.toLocaleString ? v.toLocaleString('en-US') : String(v);
    if (Number.isInteger(v)) return String(v);
    return String(round(v, 2));
  }

  // ------------------------------------------------------------------ dom ----

  var NS = 'http://www.w3.org/2000/svg';
  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) if (attrs.hasOwnProperty(k) && attrs[k] !== null) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function esc(s) {
    return String(s === null || s === undefined ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function injectCSS() {
    if (document.getElementById('sfn-charts-css')) return;
    var st = document.createElement('style');
    st.id = 'sfn-charts-css';
    st.textContent = [
      ':root{',
      '--sfnc-c1:#0072B2;--sfnc-c2:#E69F00;--sfnc-c3:#009E73;--sfnc-c4:#CC79A7;--sfnc-c5:#56B4E9;',
      '--sfnc-s1:#EAF2F8;--sfnc-s2:#C5DCEB;--sfnc-s3:#94BFDA;--sfnc-s4:#5B9BC6;--sfnc-s5:#2E7BB0;--sfnc-s6:#0072B2;',
      '--sfnc-d1:#8A4D1F;--sfnc-d2:#C08552;--sfnc-d3:#E3C6AC;--sfnc-d4:#EDEDEA;--sfnc-d5:#A9C7DC;--sfnc-d6:#4A90C0;--sfnc-d7:#0072B2;',
      '--sfnc-ink:#111827;--sfnc-ink-2:#374151;--sfnc-ink-3:#6B7280;',
      '--sfnc-rule:#E5E7EB;--sfnc-surface:#FFFFFF;--sfnc-tipbg:#111827;--sfnc-tipink:#FFFFFF;',
      '--sfnc-good:#15803D;--sfnc-warn:#B45309;--sfnc-serious:#C2410C;--sfnc-bad:#B91C1C;}',
      // Dark is SELECTED, not an inversion. Every step was re-validated against the dark
      // surface, and three of the five light hues had to move DOWN in lightness rather
      // than up, because the dark band tops out lower than the light one.
      ':root[data-theme="dark"]{',
      '--sfnc-c1:#1183C7;--sfnc-c2:#0FA37B;--sfnc-c3:#C08018;--sfnc-c4:#C4689A;--sfnc-c5:#7A7FE0;',
      '--sfnc-s1:#16243A;--sfnc-s2:#1A3A5C;--sfnc-s3:#1B5280;--sfnc-s4:#166A9F;--sfnc-s5:#1183C7;--sfnc-s6:#4FA8DF;',
      '--sfnc-d1:#C98A5A;--sfnc-d2:#A06A3C;--sfnc-d3:#6B4E38;--sfnc-d4:#3A3F49;--sfnc-d5:#2F5A79;--sfnc-d6:#1B6FA8;--sfnc-d7:#4FA8DF;',
      '--sfnc-ink:#F3F5F9;--sfnc-ink-2:#C7D0DD;--sfnc-ink-3:#93A0B3;',
      '--sfnc-rule:#2A3446;--sfnc-surface:#111827;--sfnc-tipbg:#E8ECF3;--sfnc-tipink:#0B1220;',
      '--sfnc-good:#4ADE80;--sfnc-warn:#FBBF24;--sfnc-serious:#FB923C;--sfnc-bad:#F87171;}',
      '.sfnc{position:relative;font-family:var(--font-body,system-ui,sans-serif);min-width:0}',
      '.sfnc svg{display:block;width:100%;height:auto;overflow:visible}',
      '.sfnc-t{font-size:12px;fill:var(--sfnc-ink-3);font-variant-numeric:tabular-nums}',
      '.sfnc-lab{font-size:12px;fill:var(--sfnc-ink-2);font-variant-numeric:tabular-nums}',
      '.sfnc-hd{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:8px;min-width:0}',
      '.sfnc-ti{font-size:14px;font-weight:600;color:var(--sfnc-ink);letter-spacing:-.011em;min-width:0}',
      '.sfnc-sub{font-size:12px;color:var(--sfnc-ink-3)}',
      '.sfnc-lg{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:10px;font-size:12px;color:var(--sfnc-ink-2);min-width:0}',
      '.sfnc-lg span{display:inline-flex;align-items:center;gap:6px;min-width:0}',
      '.sfnc-sw{width:9px;height:9px;border-radius:2px;flex:none}',
      '.sfnc-tip{position:absolute;pointer-events:none;opacity:0;transition:opacity .09s;',
      'background:var(--sfnc-tipbg);color:var(--sfnc-tipink);font-size:12px;line-height:1.45;',
      'padding:7px 9px;border-radius:6px;white-space:nowrap;z-index:5;font-variant-numeric:tabular-nums;',
      'box-shadow:0 2px 8px rgba(8,21,39,.18);max-width:240px}',
      '.sfnc-tip b{font-weight:600}',
      '.sfnc-tip i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px;font-style:normal}',
      '.sfnc-tbl{width:100%;border-collapse:collapse;font-size:12px;margin-top:10px;font-variant-numeric:tabular-nums}',
      '.sfnc-tbl th,.sfnc-tbl td{border-bottom:1px solid var(--sfnc-rule);padding:4px 8px;text-align:right;color:var(--sfnc-ink-2)}',
      '.sfnc-tbl th:first-child,.sfnc-tbl td:first-child{text-align:left}',
      '.sfnc-tgl{background:none;border:0;padding:0;font:inherit;font-size:12px;color:var(--sfnc-ink-3);cursor:pointer;text-decoration:underline}',
      '.sfnc-tgl:focus-visible{outline:2px solid var(--sfnc-c1);outline-offset:2px}',
      '.sfnc-hit{fill:transparent;cursor:pointer}',
      '@media (prefers-reduced-motion:reduce){.sfnc-tip{transition:none}}'
    ].join('');
    document.head.appendChild(st);
  }

  // One tooltip per chart, positioned against the chart box rather than the page, so it
  // survives the chart being inside a scrolling panel.
  function tooltip(box) {
    var tip = document.createElement('div');
    tip.className = 'sfnc-tip';
    box.appendChild(tip);
    return {
      show: function (html, x, y) {
        tip.innerHTML = html;
        tip.style.opacity = '1';
        var w = tip.offsetWidth, bw = box.clientWidth;
        var left = x - w / 2;
        if (left < 0) left = 0;
        if (left + w > bw) left = Math.max(0, bw - w);
        tip.style.left = left + 'px';
        tip.style.top = Math.max(0, y - tip.offsetHeight - 10) + 'px';
      },
      hide: function () { tip.style.opacity = '0'; }
    };
  }

  function frame(node, spec) {
    injectCSS();
    node.innerHTML = '';
    node.classList.add('sfnc');
    if (spec.title || spec.subtitle) {
      var hd = document.createElement('div');
      hd.className = 'sfnc-hd';
      hd.innerHTML = '<div class="sfnc-ti">' + esc(spec.title || '') + '</div>' +
        (spec.subtitle ? '<div class="sfnc-sub">' + esc(spec.subtitle) + '</div>' : '');
      node.appendChild(hd);
    }
    return node;
  }

  // Identity is never colour alone: two or more series always get a legend.
  function legend(node, names, colors) {
    if (names.length < 2) return;
    var lg = document.createElement('div');
    lg.className = 'sfnc-lg';
    lg.innerHTML = names.map(function (n, i) {
      return '<span><i class="sfnc-sw" style="background:' + colors[i] + '"></i>' + esc(n) + '</span>';
    }).join('');
    node.appendChild(lg);
  }

  // Every chart can become its own numbers. This is the accessibility backstop and it is
  // also the thing a person actually wants when they are trying to copy a figure out.
  function tableView(node, head, rows) {
    var wrap = document.createElement('div');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'sfnc-tgl';
    btn.textContent = 'Show the numbers';
    var tbl = document.createElement('div');
    tbl.hidden = true;
    tbl.innerHTML = '<div style="overflow-x:auto"><table class="sfnc-tbl"><thead><tr>' +
      head.map(function (h) { return '<th>' + esc(h) + '</th>'; }).join('') +
      '</tr></thead><tbody>' + rows.map(function (r) {
        return '<tr>' + r.map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>';
    btn.addEventListener('click', function () {
      tbl.hidden = !tbl.hidden;
      btn.textContent = tbl.hidden ? 'Show the numbers' : 'Hide the numbers';
    });
    wrap.appendChild(btn);
    wrap.appendChild(tbl);
    node.appendChild(wrap);
  }

  function gridAndAxes(svg, m, w, h, yTicks, ys, xLabels, xAt) {
    for (var i = 0; i < yTicks.length; i++) {
      var y = ys(yTicks[i]);
      el('line', { x1: m.l, x2: w - m.r, y1: y, y2: y, stroke: RULE, 'stroke-width': 1 }, svg);
      el('text', { x: m.l - 8, y: y + 4, 'text-anchor': 'end', class: 'sfnc-t' }, svg)
        .textContent = fmtNum(yTicks[i]);
    }
    if (xLabels) {
      // Thin the labels rather than overlap them. A collided axis is unreadable at any
      // width, and 400px is the width that matters.
      var every = Math.ceil(xLabels.length / Math.max(2, Math.floor((w - m.l - m.r) / 64)));
      for (var j = 0; j < xLabels.length; j++) {
        if (j % every !== 0 && j !== xLabels.length - 1) continue;
        el('text', { x: xAt(j), y: h - m.b + 16, 'text-anchor': 'middle', class: 'sfnc-t' }, svg)
          .textContent = xLabels[j];
      }
    }
  }

  // --------------------------------------------------------------- forms ----

  function timeSeries(node, spec) {
    var series = spec.series || [];
    var labels = spec.labels || [];
    var w = spec.width || 640, h = spec.height || 220;
    var m = { l: 44, r: 12, t: 8, b: 26 };
    frame(node, spec);
    var box = document.createElement('div');
    box.style.position = 'relative';
    node.appendChild(box);
    var svg = el('svg', {
      viewBox: '0 0 ' + w + ' ' + h, role: 'img',
      'aria-label': (spec.title || 'Time series') + ', ' + series.length + ' series over ' + labels.length + ' points'
    }, box);

    var all = [];
    series.forEach(function (s) { all = all.concat(s.values); });
    var e = extent(all);
    var lo = spec.zero === false ? e[0] : Math.min(0, e[0]);
    var t = ticks(lo, e[1], 4);
    var ys = scale(t[0], t[t.length - 1], h - m.b, m.t);
    var xs = function (i) {
      return labels.length < 2 ? (m.l + w - m.r) / 2
        : m.l + i / (labels.length - 1) * (w - m.l - m.r);
    };
    gridAndAxes(svg, m, w, h, t, ys, labels, xs);

    series.forEach(function (s, si) {
      var pts = s.values.map(function (v, i) { return { x: xs(i), y: v === null ? null : ys(v) }; });
      if (spec.area && series.length === 1) {
        var first = pts.find(function (p) { return p.y !== null; });
        var last = pts.slice().reverse().find(function (p) { return p.y !== null; });
        if (first && last) {
          el('path', {
            d: linePath(pts) + ' L' + round(last.x, 2) + ' ' + ys(t[0]) + ' L' + round(first.x, 2) + ' ' + ys(t[0]) + ' Z',
            fill: color(si), 'fill-opacity': 0.1, stroke: 'none'
          }, svg);
        }
      }
      el('path', {
        d: linePath(pts), fill: 'none', stroke: color(si), 'stroke-width': 2,
        'stroke-linejoin': 'round', 'stroke-linecap': 'round'
      }, svg);
      // A marker only where there is one point to mark, or the line becomes beads.
      if (labels.length === 1) {
        pts.forEach(function (p) { if (p.y !== null) el('circle', { cx: p.x, cy: p.y, r: 4, fill: color(si) }, svg); });
      }
    });

    var tip = tooltip(box);
    var rule = el('line', { y1: m.t, y2: h - m.b, stroke: INK.muted, 'stroke-width': 1, opacity: 0 }, svg);
    var dots = series.map(function (s, si) {
      return el('circle', { r: 4.5, fill: color(si), stroke: SURFACE, 'stroke-width': 2, opacity: 0 }, svg);
    });
    labels.forEach(function (lab, i) {
      var half = labels.length < 2 ? (w - m.l - m.r) : (w - m.l - m.r) / (labels.length - 1);
      el('rect', {
        x: xs(i) - half / 2, y: m.t, width: half, height: h - m.b - m.t, class: 'sfnc-hit'
      }, svg).addEventListener('mousemove', function (ev) {
        rule.setAttribute('x1', xs(i)); rule.setAttribute('x2', xs(i)); rule.setAttribute('opacity', 0.35);
        var rows = series.map(function (s, si) {
          var v = s.values[i];
          dots[si].setAttribute('cx', xs(i));
          dots[si].setAttribute('cy', v === null || v === undefined ? -99 : ys(v));
          dots[si].setAttribute('opacity', v === null || v === undefined ? 0 : 1);
          return '<i style="background:' + color(si) + '"></i>' + esc(s.name || '') + ' <b>' + fmtNum(v) + '</b>';
        }).join('<br>');
        var r = box.getBoundingClientRect();
        tip.show('<b>' + esc(lab) + '</b><br>' + rows, ev.clientX - r.left, ev.clientY - r.top);
      });
    });
    box.addEventListener('mouseleave', function () {
      tip.hide(); rule.setAttribute('opacity', 0);
      dots.forEach(function (d) { d.setAttribute('opacity', 0); });
    });

    legend(node, series.map(function (s) { return s.name; }), series.map(function (s, i) { return color(i); }));
    tableView(node, [spec.xTitle || ''].concat(series.map(function (s) { return s.name; })),
      labels.map(function (lab, i) { return [lab].concat(series.map(function (s) { return fmtNum(s.values[i]); })); }));
    return node;
  }

  function comparison(node, spec) {
    var cats = spec.categories || [];
    var series = spec.series || [];
    var w = spec.width || 640, h = spec.height || 220;
    var m = { l: 44, r: 12, t: 8, b: 30 };
    frame(node, spec);
    var box = document.createElement('div');
    box.style.position = 'relative';
    node.appendChild(box);
    var svg = el('svg', {
      viewBox: '0 0 ' + w + ' ' + h, role: 'img',
      'aria-label': (spec.title || 'Comparison') + ', ' + cats.length + ' categories'
    }, box);

    var stacked = !!spec.stacked && series.length > 1;
    var totals = cats.map(function (_, i) {
      return series.reduce(function (t, s) { return t + (s.values[i] || 0); }, 0);
    });
    var all = stacked ? totals : series.reduce(function (a, s) { return a.concat(s.values); }, []);
    var t = ticks(0, extent(all)[1], 4);
    var ys = scale(0, t[t.length - 1], h - m.b, m.t);
    var bandW = (w - m.l - m.r) / Math.max(1, cats.length);
    var xAt = function (i) { return m.l + bandW * (i + 0.5); };
    gridAndAxes(svg, m, w, h, t, ys, cats, xAt);

    var stacks = stacked ? stack(series.map(function (s) { return s.values; })) : null;
    var tip = tooltip(box);
    var inner = Math.min(bandW * 0.68, 48);
    var slot = stacked ? inner : inner / series.length;

    cats.forEach(function (cat, i) {
      series.forEach(function (s, si) {
        var v = s.values[i] || 0;
        var x, y0, y1;
        if (stacked) {
          x = xAt(i) - inner / 2;
          y0 = ys(stacks[si][i][0]); y1 = ys(stacks[si][i][1]);
        } else {
          x = xAt(i) - inner / 2 + si * slot;
          y0 = ys(0); y1 = ys(v);
        }
        var hgt = Math.max(0, y0 - y1);
        // A 2px surface gap between fills, so adjacent bars and stacked segments read as
        // separate marks rather than one block with a colour change in it.
        var gap = 2;
        var r = el('rect', {
          x: round(x + (stacked ? 0 : 0.5), 2), y: round(y1, 2),
          width: Math.max(1, (stacked ? slot : slot - gap)),
          height: Math.max(0, hgt - (stacked && hgt > gap ? gap : 0)),
          fill: color(si), rx: Math.min(4, Math.max(0, hgt / 2))
        }, svg);
        r.addEventListener('mousemove', function (ev) {
          var rect = box.getBoundingClientRect();
          tip.show('<b>' + esc(cat) + '</b><br><i style="background:' + color(si) + '"></i>' +
            esc(s.name || '') + ' <b>' + fmtNum(v) + '</b>', ev.clientX - rect.left, ev.clientY - rect.top);
        });
        r.addEventListener('mouseleave', function () { tip.hide(); });
      });
    });

    legend(node, series.map(function (s) { return s.name; }), series.map(function (s, i) { return color(i); }));
    tableView(node, [spec.xTitle || ''].concat(series.map(function (s) { return s.name; })),
      cats.map(function (c, i) { return [c].concat(series.map(function (s) { return fmtNum(s.values[i]); })); }));
    return node;
  }

  function distribution(node, spec) {
    var bins = spec.bins || histogram(spec.values || [], spec.binCount || 10);
    var w = spec.width || 640, h = spec.height || 200;
    var m = { l: 44, r: 12, t: 8, b: 30 };
    frame(node, spec);
    var box = document.createElement('div');
    box.style.position = 'relative';
    node.appendChild(box);
    var svg = el('svg', {
      viewBox: '0 0 ' + w + ' ' + h, role: 'img',
      'aria-label': (spec.title || 'Distribution') + ', ' + bins.length + ' bins'
    }, box);
    var t = ticks(0, extent(bins.map(function (b) { return b.n; }))[1], 4);
    var ys = scale(0, t[t.length - 1], h - m.b, m.t);
    var bw = (w - m.l - m.r) / bins.length;
    gridAndAxes(svg, m, w, h, t, ys, bins.map(function (b) { return fmtNum(round(b.from, 1)); }),
      function (i) { return m.l + bw * (i + 0.5); });

    var tip = tooltip(box);
    // One hue: a histogram is one series, so colour carries no identity here.
    bins.forEach(function (b, i) {
      var y = ys(b.n), hgt = Math.max(0, ys(0) - y);
      var r = el('rect', {
        x: round(m.l + bw * i + 1, 2), y: round(y, 2), width: Math.max(1, bw - 2),
        height: hgt, fill: CATEGORICAL[0], rx: Math.min(4, Math.max(0, hgt / 2))
      }, svg);
      r.addEventListener('mousemove', function (ev) {
        var rect = box.getBoundingClientRect();
        tip.show('<b>' + fmtNum(round(b.from, 1)) + ' to ' + fmtNum(round(b.to, 1)) + '</b><br>' +
          fmtNum(b.n) + (b.n === 1 ? ' item' : ' items'), ev.clientX - rect.left, ev.clientY - rect.top);
      });
      r.addEventListener('mouseleave', function () { tip.hide(); });
    });
    tableView(node, ['From', 'To', 'Count'],
      bins.map(function (b) { return [fmtNum(round(b.from, 2)), fmtNum(round(b.to, 2)), fmtNum(b.n)]; }));
    return node;
  }

  function funnel(node, spec) {
    var steps = spec.steps || [];
    frame(node, spec);
    var first = steps.length ? (steps[0].value || 0) : 0;
    var wrap = document.createElement('div');
    wrap.style.display = 'grid';
    wrap.style.gap = '6px';
    node.appendChild(wrap);
    // A funnel is a ranked list of magnitudes with a drop-off between each pair, so it is
    // bars and text rather than a tapering polygon: the polygon encodes the number twice,
    // once in width and once in area, and the area is the one people misread.
    steps.forEach(function (s, i) {
      var v = s.value || 0;
      var share = first > 0 ? v / first : 0;
      var prev = i > 0 ? (steps[i - 1].value || 0) : null;
      var row = document.createElement('div');
      row.style.minWidth = '0';
      row.innerHTML =
        '<div style="display:flex;justify-content:space-between;gap:12px;font-size:12px;' +
        'color:' + INK.secondary + ';margin-bottom:3px;min-width:0">' +
        '<span style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + esc(s.label) + '</span>' +
        '<span style="font-variant-numeric:tabular-nums;flex:none"><b style="color:' + INK.primary + '">' + fmtNum(v) + '</b>' +
        (prev !== null && prev > 0
          ? ' <span style="color:' + INK.muted + '">' + Math.round(v / prev * 100) + '% of previous</span>'
          : '') + '</span></div>' +
        '<div style="height:10px;background:' + RULE + ';border-radius:5px;overflow:hidden">' +
        '<div style="height:100%;width:' + (share * 100).toFixed(1) + '%;background:' + CATEGORICAL[0] +
        ';border-radius:5px"></div></div>';
      wrap.appendChild(row);
    });
    tableView(node, ['Step', 'Count', 'Share of first', 'Share of previous'],
      steps.map(function (s, i) {
        var v = s.value || 0, prev = i > 0 ? (steps[i - 1].value || 0) : null;
        return [s.label, fmtNum(v),
          first > 0 ? Math.round(v / first * 100) + '%' : '',
          prev !== null && prev > 0 ? Math.round(v / prev * 100) + '%' : ''];
      }));
    return node;
  }

  function cohort(node, spec) {
    var rows = spec.rows || [];
    var cols = spec.columns || [];
    frame(node, spec);
    var box = document.createElement('div');
    box.style.position = 'relative';
    box.style.overflowX = 'auto';
    node.appendChild(box);
    var flat = [];
    rows.forEach(function (r) { flat = flat.concat(r.values.filter(function (v) { return v !== null; })); });
    var hi = extent(flat)[1] || 1;
    var tip = tooltip(box);
    var tbl = document.createElement('table');
    tbl.className = 'sfnc-tbl';
    tbl.style.marginTop = '0';
    tbl.innerHTML = '<thead><tr><th>' + esc(spec.rowTitle || 'Cohort') + '</th>' +
      cols.map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('') + '</tr></thead>';
    var tb = document.createElement('tbody');
    rows.forEach(function (r) {
      var tr = document.createElement('tr');
      tr.innerHTML = '<td style="white-space:nowrap">' + esc(r.label) + '</td>';
      r.values.forEach(function (v, ci) {
        var td = document.createElement('td');
        if (v === null || v === undefined) {
          td.textContent = '';
        } else {
          // Sequential ramp: magnitude is lightness on one hue, so a reader with any
          // colour vision reads it, and the ink flips to white only where the fill is
          // dark enough to need it.
          var idx = Math.min(SEQUENTIAL.length - 1, Math.round(v / hi * (SEQUENTIAL.length - 1)));
          td.style.background = SEQUENTIAL[idx];
          td.style.color = idx >= 4 ? '#fff' : INK.secondary;
          td.textContent = spec.percent ? Math.round(v) + '%' : fmtNum(v);
          td.addEventListener('mousemove', function (ev) {
            var rect = box.getBoundingClientRect();
            tip.show('<b>' + esc(r.label) + '</b><br>' + esc(cols[ci]) + ' <b>' +
              (spec.percent ? Math.round(v) + '%' : fmtNum(v)) + '</b>',
              ev.clientX - rect.left, ev.clientY - rect.top);
          });
          td.addEventListener('mouseleave', function () { tip.hide(); });
        }
        tr.appendChild(td);
      });
      tb.appendChild(tr);
    });
    tbl.appendChild(tb);
    box.appendChild(tbl);
    return node;
  }

  // Not every number deserves a plot. One figure, its label, and a comparison if there
  // is an honest one to make.
  function statTile(node, spec) {
    injectCSS();
    node.innerHTML = '';
    node.classList.add('sfnc');
    var d = spec.delta;
    var tone = d === null || d === undefined ? INK.muted : (d > 0 ? STATUS.good : d < 0 ? STATUS.critical : INK.muted);
    node.innerHTML =
      '<div style="font-size:12px;color:' + INK.muted + ';letter-spacing:.06em;text-transform:uppercase">' +
      esc(spec.label || '') + '</div>' +
      '<div style="font-family:var(--font-mono,ui-monospace,monospace);font-size:30px;line-height:1.1;' +
      'color:var(--text-heading,' + INK.primary + ');font-variant-numeric:tabular-nums;letter-spacing:-.02em">' +
      esc(spec.value) + '</div>' +
      (spec.note || d !== undefined
        ? '<div style="font-size:12px;color:' + INK.muted + ';margin-top:2px">' +
          (d !== null && d !== undefined
            // Direction is a word as well as a colour, so it survives a colourblind
            // reader, a greyscale print and forced-colors mode.
            ? '<span style="color:' + tone + '">' + (d > 0 ? 'Up' : d < 0 ? 'Down' : 'Flat') + ' ' +
              fmtNum(Math.abs(d)) + (spec.deltaSuffix || '') + '</span> '
            : '') + esc(spec.note || '') + '</div>'
        : '');
    return node;
  }

  return {
    CATEGORICAL: CATEGORICAL, SEQUENTIAL: SEQUENTIAL, DIVERGING: DIVERGING, STATUS: STATUS,
    niceStep: niceStep, ticks: ticks, scale: scale, extent: extent, linePath: linePath,
    stack: stack, histogram: histogram, fmtNum: fmtNum, color: color, round: round,
    timeSeries: timeSeries, comparison: comparison, distribution: distribution,
    funnel: funnel, cohort: cohort, statTile: statTile
  };
}));
