"""Build /colleges/: the undergraduate ranking vertical.

One index with the full table, one page per college, and a methodology page. The
data comes from data/colleges/ (see extract_colleges.py); the score comes from
college_score.py, which explains what it measures and what it refuses to measure.
"""
import datetime
import html
import json
import os
import pathlib
import sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials                      # noqa: E402
import college_score as CS           # noqa: E402
import validate_colleges             # noqa: E402

SITE = "https://startfromnowhere.com"
OUTDIR = ROOT / "colleges"
LEGAL = ("College data from the US Department of Education College Scorecard, a public "
         "domain federal dataset. The SFN College Score is our own composite and is not "
         "endorsed by the Department of Education.")


CSS_HREF = "/colleges/colleges.css"


def write_shared_css(base_css):
    """One stylesheet for the whole vertical.

    Inlining it put nine kilobytes of identical CSS into every one of 1451 pages,
    about thirteen megabytes of pure duplication, and made the browser re-parse it on
    every navigation instead of reading it from cache once.
    """
    out = OUTDIR / "colleges.css"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(partials.apply_chrome_css(base_css), encoding="utf-8")
    return CSS_HREF


def esc(s):
    return html.escape(str(s), quote=True)


def fv(c, name):
    return (c.get("profile", {}).get(name) or {}).get("v")


def money(v):
    return "$" + format(int(v), ",d") if isinstance(v, (int, float)) else "&mdash;".replace("&mdash;", "-")


def pct(v, nd=1):
    return ("%." + str(nd) + "f%%") % v if isinstance(v, (int, float)) else "-"


def plain(v):
    if v is None:
        return "-"
    if isinstance(v, float):
        return ("%.1f" % v).rstrip("0").rstrip(".")
    if isinstance(v, int):
        return format(v, ",d")
    return str(v)


def stat_row(label, value, note=""):
    return ('<div class="stat"><span class="k">%s</span><span class="v">%s</span>'
            '<span class="s">%s</span></div>' % (esc(label), value, esc(note)))


def score_panel(c, n_ranked):
    if c.get("sfn_score") is None:
        return ('<div class="unranked"><strong>Listed but not ranked.</strong> %s '
                'Everything the Scorecard does report for this school is shown below.'
                '</div>' % esc(c.get("unranked_reason", "")))
    labels = {"completion": "Completion", "earnings": "Earnings",
              "cost": "Cost and debt", "access": "Access"}
    bars = []
    for k in ("completion", "earnings", "cost", "access"):
        v = c["sfn_components"].get(k)
        if v is None:
            bars.append('<div class="comp"><span>%s</span><span class="note">not reported'
                        '</span><span></span></div>' % labels[k])
            continue
        bars.append('<div class="comp"><span>%s</span><span class="bar"><i style="width:%.0f%%">'
                    '</i></span><span class="v">%.0f</span></div>' % (labels[k], v, v))
    return ('<div class="panel"><div class="scorehead"><div><div class="bigscore">%s</div>'
            '<div class="l note">SFN College Score</div></div>'
            '<div><div class="bigscore">#%d</div><div class="l note">of %d ranked</div></div>'
            '</div>%s<p class="note">Each component is a percentile rank within the %d '
            'ranked colleges, so the score says how this school compares with the rest of '
            'the library, not how good it is in the abstract. '
            '<a href="/colleges/methodology/">How this is calculated</a>.</p></div>'
            % (c["sfn_score"], c["sfn_rank"], n_ranked, "".join(bars), n_ranked))


def lead_paragraph(c, n_ranked):
    """The sentences an answer engine can quote.

    A model asked what a college costs lifts a sentence, not a table cell, because a
    cell carries no subject and no year. Same figures as the panels below, written so
    they can be quoted whole. Residency is stated explicitly wherever a number depends
    on it, since that is the difference between a useful answer and a wrong one.
    """
    g = lambda k: fv(c, k)
    out = []
    where = ", ".join(x for x in (c.get("city"), c.get("state")) if x)
    out.append("%s is a %s four-year college in %s."
               % (c["name"], c["type"].lower(), where or c["state"]))
    ug = g("undergrads")
    if ug:
        out.append("It enrolls %s undergraduates." % format(int(ug), ",d"))
    adm = g("admit_rate_pct")
    if adm is not None:
        out.append("The admission rate is %s percent." % plain(adm))
    ti, to = g("tuition_in_state_usd"), g("tuition_out_state_usd")
    if ti and to and to > ti:
        out.append("Tuition and fees are %s a year for in-state students and %s for "
                   "out-of-state students, a difference of %s."
                   % (money(ti), money(to), money(to - ti)))
    elif ti:
        out.append("Tuition and fees are %s a year, the same for in-state and "
                   "out-of-state students." % money(ti))
    npv = g("net_price_usd")
    if npv:
        out.append("The average net price after grant aid is %s%s."
                   % (money(npv), " for in-state students" if c["type"] == "Public" else ""))
    gr = g("grad_rate_6yr_pct")
    if gr is not None:
        out.append("%s percent of students graduate within six years." % plain(gr))
    ea = g("earnings_10yr_usd")
    if ea:
        out.append("Median earnings ten years after entry are %s." % money(ea))
    if c.get("sfn_score") is not None:
        out.append("Start From Nowhere ranks it number %d of the %d colleges it scores, on "
                   "completion, earnings, cost and access."
                   % (c["sfn_rank"], n_ranked))
    out.append("Every figure comes from the US Department of Education College Scorecard "
               "and links to this college's own record there.")
    return " ".join(out)


def title_bits(c):
    """Promise only what this page holds, in the words people search with."""
    have = []
    if fv(c, "admit_rate_pct") is not None:
        have.append("Acceptance Rate")
    if fv(c, "net_price_usd") or fv(c, "tuition_in_state_usd"):
        have.append("Cost")
    if fv(c, "sat_avg") or fv(c, "act_mid"):
        have.append("SAT Scores")
    if fv(c, "grad_rate_6yr_pct") is not None:
        have.append("Graduation Rate")
    if len(have) >= 3:
        return "%s, %s, and %s" % (have[0], have[1], have[2])
    if len(have) == 2:
        return "%s and %s" % (have[0], have[1])
    if have:
        return have[0]
    return "Costs and Outcomes"


def college_page(c, tpl, css_href, n_ranked, n_total):
    p = c["profile"]
    cost = "".join([
        stat_row("Average net price", money(fv(c, "net_price_usd")),
                 "in-state" if c["type"] == "Public" else "after grant aid"),
        stat_row("Cost of attendance", money(fv(c, "cost_attendance_usd")), "sticker price"),
        stat_row("Tuition and fees, in state", money(fv(c, "tuition_in_state_usd"))),
        stat_row("Tuition and fees, out of state", money(fv(c, "tuition_out_state_usd")),
                 "same as in-state" if c.get("out_state_premium") == 0 else ""),
        stat_row("Out-of-state premium",
                 ("+" + money(c["out_state_premium"])) if c.get("out_state_premium")
                 else ("none" if c.get("out_state_premium") == 0 else "-"),
                 "what a non-resident pays on top"),
        stat_row("Median debt at graduation", money(fv(c, "median_debt_usd"))),
        stat_row("Students with federal loans", pct(fv(c, "federal_loan_pct"))),
    ])
    out = "".join([
        stat_row("Graduation rate, six years", pct(fv(c, "grad_rate_6yr_pct"))),
        stat_row("First year retention", pct(fv(c, "retention_pct"))),
        stat_row("Median earnings, ten years after entry", money(fv(c, "earnings_10yr_usd"))),
        stat_row("Students receiving Pell grants", pct(fv(c, "pell_pct"))),
        stat_row("Undergraduate enrollment", plain(fv(c, "undergrads"))),
    ])
    adm = "".join([
        stat_row("Admission rate", pct(fv(c, "admit_rate_pct"))),
        stat_row("SAT average", plain(fv(c, "sat_avg"))),
        stat_row("SAT reading midpoint", plain(fv(c, "sat_reading_mid"))),
        stat_row("SAT math midpoint", plain(fv(c, "sat_math_mid"))),
        stat_row("ACT midpoint", plain(fv(c, "act_mid"))),
        stat_row("Test policy", esc(fv(c, "test_policy") or "-")),
    ])
    sch = c.get("scholarship") or {}
    if any((sch.get(k) or {}).get("v") is not None for k in ("pct_receiving", "avg_award_usd")):
        schol = "".join([
            stat_row("Students receiving institutional aid", pct((sch.get("pct_receiving") or {}).get("v"))),
            stat_row("Average institutional award", money((sch.get("avg_award_usd") or {}).get("v"))),
            stat_row("Automatically considered", esc((sch.get("auto_considered") or {}).get("v") or "-")),
        ])
    else:
        schol = ('<p class="note">The College Scorecard does not report institutional '
                 'scholarship policy, and we have not yet verified it for this school from '
                 'its own aid pages. Rather than estimate it, this is left blank. The '
                 'federal aid picture above (net price, Pell share, median debt) is '
                 'reported and sourced. For outside awards, see our '
                 '<a href="/funding/">funding and scholarships guide</a>.</p>')

    if c.get("sfn_score") is not None:
        rank_line = ('<p>Ranked <strong>#%d of %d</strong> on the SFN College Score, which '
                     'weighs completion, earnings, cost and access and ignores selectivity.</p>'
                     % (c["sfn_rank"], n_ranked))
    else:
        rank_line = '<p>Listed with full data, not ranked.</p>'

    bits = []
    if fv(c, "net_price_usd"):
        bits.append("average net price %s" % money(fv(c, "net_price_usd")))
    if fv(c, "grad_rate_6yr_pct"):
        bits.append("%s six-year graduation rate" % pct(fv(c, "grad_rate_6yr_pct")))
    if fv(c, "earnings_10yr_usd"):
        bits.append("median earnings %s ten years after entry" % money(fv(c, "earnings_10yr_usd")))
    desc = "%s in %s, %s: %s. Every figure from the US Department of Education College Scorecard." % (
        c["name"], c.get("city") or c["state"], c["state"], "; ".join(bits) or "full reported data")

    ld = {"@context": "https://schema.org", "@type": "CollegeOrUniversity",
          "name": c["name"], "url": c.get("website") or c["scorecard"],
          "address": {"@type": "PostalAddress", "addressLocality": c.get("city"),
                      "addressRegion": c["state"], "addressCountry": "US"},
          "identifier": {"@type": "PropertyValue", "propertyID": "IPEDS UNITID",
                         "value": str(c["unitid"])}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "College Rankings", "item": SITE + "/colleges/"},
        {"@type": "ListItem", "position": 2, "name": c["name"], "item": "%s/colleges/%s/" % (SITE, c["slug"])}]}

    car = " · " + esc(c["carnegie"]) if c.get("carnegie") else ""
    site_line = ('<p class="note">Official site: <a href="%s" rel="nofollow noopener" '
                 'target="_blank">%s</a></p>' % (esc(c["website"]), esc(c["website"]))
                 ) if c.get("website") else ""
    out_html = (tpl.replace("{{CSS_HREF}}", css_href)
                .replace("{{TITLE_BITS}}", esc(title_bits(c)))
                .replace("{{LEAD}}", esc(lead_paragraph(c, n_ranked)))
                .replace("{{NAME}}", esc(c["name"]))
                .replace("{{SLUG}}", esc(c["slug"]))
                .replace("{{DESC}}", esc(desc))
                .replace("{{TYPE}}", esc(c["type"]))
                .replace("{{CITY}}", esc(c.get("city") or ""))
                .replace("{{STATE}}", esc(c["state"]))
                .replace("{{CARNEGIE_BIT}}", car)
                .replace("{{RANK_LINE}}", rank_line)
                .replace("{{SCORE_PANEL}}", score_panel(c, n_ranked))
                .replace("{{COST_ROWS}}", cost)
                .replace("{{OUTCOME_ROWS}}", out)
                .replace("{{ADMIT_ROWS}}", adm)
                .replace("{{SCHOL}}", schol)
                .replace("{{SCORECARD}}", esc(c["scorecard"]))
                .replace("{{RELEASE}}", esc(next(
                    (f.get("release") for f in c["profile"].values() if f.get("release")),
                    "most recent release")))
                .replace("{{WEBSITE_LINE}}", site_line)
                .replace("{{N}}", format(n_total, ",d"))
                .replace("{{LD}}", json.dumps(ld))
                .replace("{{BREADCRUMB_LD}}", json.dumps(bc)))
    return partials.apply_chrome(out_html, LEGAL)


# Column order for the compact payload. Arrays rather than objects: with 1451 rows,
# repeating fifteen key names on every one costs more than the data.
COLS = ["rank", "score", "name", "slug", "city", "state", "type", "net", "grad",
        "ret", "earn", "debt", "pell", "admit", "sat", "act", "tin", "tout", "prem"]

# How many rows are written into the HTML itself. Every college has its own indexed
# page, so the index does not need all 1451 in the DOM to be found; it needs to be
# fast to open and complete once someone starts searching. The rest arrive from the
# payload the moment anyone filters, sorts, or asks to see them all.
SEED_ROWS = 300

APP_JS = r"""
// The table has two states. On load it shows the rows the server wrote into the HTML,
// so the page is useful with no JavaScript and cheap to open. The moment anyone
// searches, sorts, or asks for the full list, it re-renders from the payload, which
// holds every college. One source of data either way, including the CSV.
(function(){
 var tb=document.getElementById('tb'); if(!tb||!window.__COLLEGES__) return;
 var COLS=window.__COLS__, DATA=window.__COLLEGES__, I={};
 COLS.forEach(function(k,i){ I[k]=i; });
 var q=document.getElementById('q'), st=document.getElementById('st'),
     ty=document.getElementById('ty'), cnt=document.getElementById('cnt'),
     more=document.getElementById('more');
 var sortKey='rank', sortDir=1, expanded=false;
 function money(v){ return (v===null||v==='')?'-':'$'+Number(v).toLocaleString('en-US'); }
 function pc(v){ return (v===null||v==='')?'-':Math.round(Number(v))+'%'; }
 function plain(v){ return (v===null||v==='')?'-':String(v); }
 function esc(s){ return String(s).replace(/[&<>"]/g,function(c){
   return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
 function match(r){
  var needle=(q.value||'').trim().toLowerCase();
  if(needle && String(r[I.name]).toLowerCase().indexOf(needle)<0) return false;
  if(st.value && r[I.state]!==st.value) return false;
  if(ty.value && r[I.type]!==ty.value) return false;
  return true;
 }
 function render(){
  var rows=DATA.filter(match);
  var withVal=[], without=[];
  rows.forEach(function(r){ var v=r[I[sortKey]];
   // A college that reports nothing for a column is neither best nor worst at it, so
   // it sorts to the bottom in both directions instead of leading an ascending sort.
   if(v===null||v==='') without.push(r); else withVal.push(r); });
  var isText=(sortKey==='name');
  withVal.sort(function(a,b){
   var x=a[I[sortKey]], y=b[I[sortKey]];
   if(isText){ x=String(x).toLowerCase(); y=String(y).toLowerCase(); }
   return x<y?-sortDir:x>y?sortDir:0; });
  var all=withVal.concat(without);
  cnt.textContent=all.length.toLocaleString('en-US')+(all.length===1?' college':' colleges');
  var show=expanded?all:all.slice(0,SEED);
  tb.innerHTML=show.map(function(r){
   return '<tr><td class="rank">'+(r[I.rank]?('#'+r[I.rank]):'<span class="note">nr</span>')+'</td>'
    +'<td class="num">'+(r[I.score]===null?'-':'<strong>'+r[I.score]+'</strong>')+'</td>'
    +'<td><a href="/colleges/'+encodeURIComponent(r[I.slug])+'/"><strong>'+esc(r[I.name])+'</strong></a>'
    +'<div class="sloc">'+esc(r[I.city])+', '+esc(r[I.state])+' &middot; '+esc(r[I.type])+'</div></td>'
    +'<td class="num">'+money(r[I.net])+'</td><td class="num">'+pc(r[I.grad])+'</td>'
    +'<td class="num hidesm">'+pc(r[I.ret])+'</td><td class="num">'+money(r[I.earn])+'</td>'
    +'<td class="num hidesm">'+money(r[I.debt])+'</td><td class="num">'+pc(r[I.pell])+'</td>'
    +'<td class="num hidesm">'+pc(r[I.admit])+'</td><td class="num hidesm">'+plain(r[I.sat])+'</td>'
    +'<td class="num">'+money(r[I.tout])+'</td>'
    +'<td class="num hidesm">'+(r[I.prem]?('+'+money(r[I.prem])):'-')+'</td></tr>';
  }).join('');
  if(all.length>show.length){ more.hidden=false;
   more.textContent='Show all '+all.length.toLocaleString('en-US')+' colleges'; }
  else more.hidden=true;
 }
 var SEED=Number(tb.getAttribute('data-seed'))||300;
 function sortBy(k){
  if(sortKey===k) sortDir=-sortDir; else { sortKey=k; sortDir=(k==='rank'||k==='name')?1:-1; }
  document.querySelectorAll('th[data-k]').forEach(function(th){
   th.setAttribute('aria-sort', th.getAttribute('data-k')===k?(sortDir===1?'ascending':'descending'):'none'); });
  render();
 }
 document.querySelectorAll('th[data-k]').forEach(function(th){
  th.style.cursor='pointer';
  th.addEventListener('click', function(){ sortBy(th.getAttribute('data-k')); }); });
 [q,st,ty].forEach(function(el){
  el.addEventListener('input', function(){ render(); });
  el.addEventListener('change', function(){ render(); }); });
 document.getElementById('clear').addEventListener('click', function(){
  q.value=''; st.value=''; ty.value=''; expanded=false; render(); });
 more.addEventListener('click', function(){ expanded=true; render(); });
 document.getElementById('csv').addEventListener('click', function(){
  var head=['Rank','Score','College','City','State','Type','Net price','Graduation rate',
            'Retention','Earnings 10yr','Median debt','Pell share','Admit rate','SAT average','ACT',
            'In-state tuition','Out-of-state tuition','Out-of-state premium'];
  var keys=['rank','score','name','city','state','type','net','grad','ret','earn','debt','pell','admit','sat','act','tin','tout','prem'];
  var out=[head.join(',')];
  DATA.filter(match).forEach(function(r){
   out.push(keys.map(function(k){ var v=r[I[k]]; if(v===null||v===undefined) v='';
    v=String(v); return /[",]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v; }).join(',')); });
  var blob=new Blob([out.join('\n')],{type:'text/csv'});
  var a=document.createElement('a'); a.href=URL.createObjectURL(blob);
  a.download='sfn-college-rankings.csv'; document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); },100); });
 render();
})();
"""


def payload_row(c):
    g = lambda k: fv(c, k)
    return [c["sfn_rank"], c["sfn_score"], c["name"], c["slug"], c.get("city") or "",
            c["state"], c["type"], g("net_price_usd"), g("grad_rate_6yr_pct"),
            g("retention_pct"), g("earnings_10yr_usd"), g("median_debt_usd"),
            g("pell_pct"), g("admit_rate_pct"), g("sat_avg"), g("act_mid"),
            g("tuition_in_state_usd"), g("tuition_out_state_usd"), c.get("out_state_premium")]


def row_html(c):
    g = lambda k: fv(c, k)
    rank = "#%d" % c["sfn_rank"] if c["sfn_rank"] else '<span class="note">nr</span>'
    score = ('<strong>%s</strong>' % c["sfn_score"]) if c["sfn_score"] is not None else "-"
    return ('<tr><td class="rank">%s</td><td class="num">%s</td>'
            '<td><a href="/colleges/%s/"><strong>%s</strong></a>'
            '<div class="sloc">%s, %s · %s</div></td>'
            '<td class="num">%s</td><td class="num">%s</td><td class="num hidesm">%s</td>'
            '<td class="num">%s</td><td class="num hidesm">%s</td><td class="num">%s</td>'
            '<td class="num hidesm">%s</td><td class="num hidesm">%s</td>'
            '<td class="num">%s</td><td class="num hidesm">%s</td></tr>'
            % (rank, score, esc(c["slug"]), esc(c["name"]),
               esc(c.get("city") or ""), esc(c["state"]), esc(c["type"]),
               money(g("net_price_usd")), pct(g("grad_rate_6yr_pct"), 0),
               pct(g("retention_pct"), 0), money(g("earnings_10yr_usd")),
               money(g("median_debt_usd")), pct(g("pell_pct"), 0),
               pct(g("admit_rate_pct"), 0), plain(g("sat_avg")),
               money(g("tuition_out_state_usd")),
               ("+" + money(c["out_state_premium"])) if c.get("out_state_premium") else "-"))


CONTROLS = """
<div class="controls" style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:16px 0 10px">
<input id="q" type="search" placeholder="Search colleges" aria-label="Search colleges"
 style="flex:1 1 220px;min-width:180px;padding:9px 12px;border:1px solid var(--gray-300);border-radius:8px;font:inherit">
<select id="st" aria-label="Filter by state" style="padding:9px 10px;border:1px solid var(--gray-300);border-radius:8px;font:inherit"><option value="">All states</option>{{STATES}}</select>
<select id="ty" aria-label="Filter by type" style="padding:9px 10px;border:1px solid var(--gray-300);border-radius:8px;font:inherit"><option value="">Public and private</option><option>Public</option><option>Private nonprofit</option></select>
<button id="clear" class="pill" type="button">Clear</button>
<button id="csv" class="pill" type="button">Download CSV</button>
<span id="cnt" class="note" aria-live="polite"></span>
</div>
<button id="more" class="pill" type="button" hidden style="margin:0 0 10px"></button>
<p class="note">Click any column heading to sort. Colleges that do not report a figure sort to the bottom rather than to the top.</p>
"""

TABLE_HEAD = ('<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse">'
              '<thead><tr>'
              '<th data-k="rank" aria-sort="ascending">Rank</th><th data-k="score" class="num">Score</th>'
              '<th data-k="name">College</th>'
              '<th data-k="net" class="num">Net Price</th><th data-k="grad" class="num">Grad Rate</th>'
              '<th data-k="ret" class="num hidesm">Retention</th><th data-k="earn" class="num">Earnings</th>'
              '<th data-k="debt" class="num hidesm">Debt</th><th data-k="pell" class="num">Pell</th>'
              '<th data-k="admit" class="num hidesm">Admit</th><th data-k="sat" class="num hidesm">SAT</th>'
              '<th data-k="tout" class="num">Out-of-State Tuition</th>'
              '<th data-k="prem" class="num hidesm">Premium</th>'
              '</tr></thead>')


def methodology_page(css_href, n_ranked, n_total, updated):
    body = """
<div class="wrap ppage">
<p class="crumb"><a href="/colleges/">College Rankings</a> / Methodology</p>
<h1 style="font-size:28px;margin:10px 0 6px">How the SFN College Score Works</h1>
<p class="note">Updated {UPDATED}. {NRANK} of {NTOTAL} colleges in the library are ranked.</p>

<div class="panel"><h2>What It Measures</h2>
<p>Four components, each a percentile rank within the ranked set, then weighted:</p>
<div class="stat"><span class="k">Completion</span><span class="v">30%</span><span class="s">six-year graduation (20) and first-year retention (10)</span></div>
<div class="stat"><span class="k">Earnings</span><span class="v">25%</span><span class="s">median earnings ten years after entry</span></div>
<div class="stat"><span class="k">Cost and debt</span><span class="v">25%</span><span class="s">net price (15) and median debt against earnings (10)</span></div>
<div class="stat"><span class="k">Access</span><span class="v">20%</span><span class="s">share of students on Pell grants</span></div>
<p class="note">Weights are renormalised over the components a school actually reports. A school is ranked only if it reports both completion and earnings; the rest are listed with their data and marked not ranked, with the reason stated on their page.</p></div>

<div class="panel"><h2>What It Refuses to Measure</h2>
<p>Admission rate, test score ranges, sticker price, endowment and reputation surveys are not scored. Admission rates and score ranges are reported on every school page because an applicant needs them to plan.</p>
<p>The reason is simple. Scoring selectivity rewards a school for turning more people away, which measures how many people applied, not what the school does for the ones it admits. A college that rejects 95 percent of applicants has not yet taught anybody anything. Reputation surveys mostly measure how well known a school already was, which makes them very hard for a good school to move and very easy for a famous one to coast on.</p></div>

<div class="panel"><h2>What to Watch Out For</h2>
<p><strong>Net price for a public university is the in-state figure.</strong> It is the only one the College Scorecard publishes. Public institutions therefore score better on cost than an out-of-state student would actually experience: across the ranked set the median net price is about 9,000 dollars lower at public institutions than private ones, and that feeds a quarter of the score.</p>
<p>So the out-of-state side is reported as its own published figures rather than buried. Every table row and every college page carries in-state tuition, out-of-state tuition, and the difference between them. 507 public colleges in this library charge a non-resident premium; the largest is 43,210 dollars. No private college charges one, which was checked rather than assumed: all 872 report identical in-state and out-of-state tuition.</p>
<p><strong>There is deliberately no second, out-of-state score.</strong> The obvious way to build one is to swap net price for published out-of-state tuition, and it produces a table that looks plausible and is wrong. Caltech falls sixteen points and Princeton nearly fourteen, when neither charges a non-resident a different price. What moved was the measure, from post-aid net price to sticker tuition, not the residency, so the column would mostly be reranking private colleges by how generous their aid is while claiming to describe out-of-state cost. The premium is a fact we can publish; that score is not.</p>
<p><strong>Earnings cover everyone who enrolled</strong>, not only graduates, and are not adjusted for what students study or where they come from. A school heavy in engineering will out-earn a school heavy in social work without being better at teaching.</p>
<p><strong>The score is relative.</strong> Each component is a percentile inside this library of four-year nonprofit and public institutions, so a score of 80 means better than 80 percent of them on the weighted mix, not 80 out of 100 in the abstract.</p>
<p><strong>Special focus medical and health professions institutions are listed but not ranked.</strong> They award a few bachelor's degrees alongside a mostly graduate professional mission, so their earnings reflect doctors and pharmacists, and several report no undergraduate graduation rate at all. Ranking them against undergraduate colleges would put them near the top for the wrong reason.</p></div>

<div class="panel"><h2>Where the Data Comes From</h2>
<p>Every figure comes from the <a href="https://collegescorecard.ed.gov/data/" rel="nofollow noopener" target="_blank">US Department of Education College Scorecard</a> institution file, the only national dataset that reports completion, earnings, debt and net price on a common definition for every accredited institution. Each college page links to that college's own Scorecard record so any number can be checked at source.</p>
<p>Nothing on these pages is estimated. A figure the Scorecard does not report is stored as null and renders as a dash. Institutional scholarship policy is not in the Scorecard, so it is blank until it has been verified from a school's own aid pages.</p>
<p>The library covers currently operating, predominantly bachelor's degree granting public and private nonprofit institutions with at least 500 undergraduates. For-profit institutions are excluded: their outcomes are reported on the same basis, but the sector's aid and completion profile differs enough that mixing them into one ranking would mislead.</p></div>

<p class="crumb"><a href="/colleges/">Back to the rankings</a> · <a href="/schools/">MBA rankings</a> · <a href="/sat/app/">Practice for the SAT</a></p>
</div>
""".replace("{UPDATED}", updated).replace("{NRANK}", format(n_ranked, ",d")).replace("{NTOTAL}", format(n_total, ",d"))
    page = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<link rel="manifest" href="/manifest.json">'
            '<link rel="icon" href="/icons/icon-192.png" type="image/png">'
            '<meta name="theme-color" content="#122B4E">'
            '<title>College Rankings Methodology: What We Score and What We Refuse To</title>'
            '<meta name="description" content="How the SFN College Score is calculated: completion 30 percent, earnings 25, cost and debt 25, access 20, and why admission rate and test scores are reported but never scored.">'
            '<link rel="canonical" href="https://startfromnowhere.com/colleges/methodology/">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&family=Manrope:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="' + css_href + '">'
            '<style>.ppage{max-width:820px}\n'
            '.stat{display:grid;grid-template-columns:1fr auto auto;gap:10px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--gray-100)}\n'
            '.stat .k{font-size:14px}.stat .v{font-family:var(--mono);font-weight:500;color:var(--navy-900);text-align:right}\n'
            '.stat .s{font-size:11px;color:var(--gray-500);text-align:right;max-width:230px}\n'
            '.panel{border:1px solid var(--gray-200);border-radius:12px;padding:16px 18px;margin:14px 0}\n'
            '.panel h2{font-size:19px;margin-bottom:8px}.panel p{font-size:14px}\n'
            '.crumb{font-size:12.5px;color:var(--gray-500);margin:14px 0}\n'
            '.note{font-size:12.5px;color:var(--gray-500)}</style></head><body>'
            '{{SITE_HEADER}}' + body + '{{SITE_FOOTER}}</body></html>')
    return partials.apply_chrome(page, LEGAL)


def main():
    src = ROOT / "data" / "colleges"
    files = sorted(src.glob("*.json"))
    if not files:
        print("build_colleges: no data/colleges/ yet; skipping /colleges/ build")
        return
    colleges = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    validate_colleges.validate(colleges)
    ranked, unranked = CS.rank_all(colleges)
    n_ranked, n_total = len(ranked), len(colleges)
    updated = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
    base_css = (D / "rankings_base.css").read_text(encoding="utf-8")
    css_href = write_shared_css(base_css)

    ordered = ranked + sorted(unranked, key=lambda c: c["name"])
    rows = "".join(row_html(c) for c in ordered[:SEED_ROWS])
    payload = json.dumps([payload_row(c) for c in ordered], separators=(",", ":"))
    states = "".join('<option>%s</option>' % s
                     for s in sorted({c["state"] for c in colleges}))
    ld_items = "".join(
        '{"@type":"ListItem","position":%d,"name":%s,"url":"%s/colleges/%s/"},'
        % (c["sfn_rank"], json.dumps(c["name"]), SITE, c["slug"])
        for c in ranked[:100]).rstrip(",")

    tpl = (D / "colleges_template.html").read_text(encoding="utf-8")
    tbody_open = '<tbody id="tb" data-seed="%d">' % SEED_ROWS
    index = (tpl.replace("{{CSS_HREF}}", css_href)
             .replace("{{N}}", format(n_total, ",d"))
             .replace("{{UPDATED}}", updated)
             .replace("{{LD_ITEMS}}", ld_items)
             .replace("{{CONTROLS}}", CONTROLS.replace("{{STATES}}", states))
             .replace("{{TABLE}}", TABLE_HEAD + tbody_open + rows + "</tbody></table></div>")
             .replace("{{DATA}}", payload)
             .replace("{{COLS}}", json.dumps(COLS, separators=(",", ":")))
             .replace("{{APP_JS}}", APP_JS))
    index = partials.apply_chrome(index, LEGAL)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "index.html").write_text(index, encoding="utf-8")
    meth = OUTDIR / "methodology"
    meth.mkdir(exist_ok=True)
    (meth / "index.html").write_text(
        methodology_page(css_href, n_ranked, n_total, updated), encoding="utf-8")

    ctpl = (D / "college_template.html").read_text(encoding="utf-8")
    for c in colleges:
        d = OUTDIR / c["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(
            college_page(c, ctpl, css_href, n_ranked, n_total), encoding="utf-8")
    print("built colleges/ index + methodology + %d college pages (%d ranked, %d unranked)"
          % (n_total, n_ranked, len(unranked)))


if __name__ == "__main__":
    main()
