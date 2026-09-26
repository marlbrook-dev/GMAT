"""Builds /daily/: one question per exam per day, the same one for everyone.

    /daily/                      today's question for every exam, and how streaks work
    /daily/<exam>/               today's question, answerable, with the streak and a share
    /daily/<exam>/<YYYY-MM-DD>/  every past day, with its answer and explanation
    /daily/<exam>/feed.xml       the last thirty days, for feed readers

Why this exists. Search brings people once; a reason to come back tomorrow brings them
again. The mechanics that do that best in the products studied for GROWTH.md are a single
shared daily puzzle, a result you can share without spoiling it, and a streak that
protects the habit rather than punishing a wrong answer. College Board runs exactly this
for the SAT. The house rules shape the rest: no leaderboard, no count of other people, no
score but your own.

The schedule is data/daily/schedule.json, written by src/daily.js, and only ever appended
to. Archive pages are built for scheduled dates up to the build date, never ahead of it.
The live page carries the scheduled day either side of the build date, because the site
redeploys at 14:00 UTC and a visitor in Asia reaches a new calendar date hours before the
deploy that contains it; the page picks by the visitor's own date.
"""
import datetime
import html
import json
import os
import pathlib
import subprocess
import sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials

SITE = "https://startfromnowhere.com"
SCHEDULE = ROOT / "data" / "daily" / "schedule.json"
ORDER = ["gmat-focus", "sat", "gre", "lsat", "act"]
# The name people search with. "GMAT Focus" is the product; "GMAT question of the day" is
# the query.
SEARCH_NAME = {"gmat-focus": "GMAT", "sat": "SAT", "gre": "GRE", "lsat": "LSAT", "act": "ACT"}
# The shared footer already carries the GMAT and SAT marks (partials.LEGAL_LINE); these
# pages add the three exams it does not name, and no mark is printed twice.
LEGAL = ("GRE is a registered trademark of ETS. LSAT is a registered trademark of the Law School "
         "Admission Council (LSAC). ACT is a registered trademark of ACT Education Corp. None of them "
         "endorses this site. Every question here is original and written for Start From Nowhere.")
LETTERS = "ABCDE"
RUNWAY_WARN = 30


def esc(s):
    return html.escape(str(s), quote=True)


def build_date():
    return datetime.date.fromisoformat(os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat())


def load_schedule():
    if not SCHEDULE.exists():
        return None
    return json.loads(SCHEDULE.read_text(encoding="utf-8"))


def long_date(iso):
    d = datetime.date.fromisoformat(iso)
    return "%s %d, %d" % (d.strftime("%B"), d.day, d.year)


def short_date(iso):
    d = datetime.date.fromisoformat(iso)
    return "%s %d, %d" % (d.strftime("%b"), d.day, d.year)


def app_window(exam_id, today=None):
    """The scheduled item ids around the build date, for the trainer's Question of the Day.
    Only ids travel: every scheduled item is hand written, and every hand-written item ships
    in the blocking bank.js, so the trainer already holds it."""
    s = load_schedule()
    slug = {"gmat-focus": "gmat", "sat": "sat", "gre": "gre", "lsat": "lsat", "act": "act"}[exam_id]
    if not s:
        return {"slug": slug, "days": {}}
    t = today or build_date()
    lo, hi = (t - datetime.timedelta(days=2)).isoformat(), (t + datetime.timedelta(days=2)).isoformat()
    return {"slug": slug, "days": {d: r[exam_id] for d, r in s["days"].items() if lo <= d <= hi and r.get(exam_id)}}


def streak_js():
    return (D / "daily_streak.js").read_text(encoding="utf-8")


def export(first, last):
    out = subprocess.run(["node", str(D / "daily.js"), "export", first, last],
                         capture_output=True, text=True, cwd=str(ROOT))
    if out.returncode:
        raise SystemExit("build_daily: export failed: " + out.stderr[-800:])
    return json.loads(out.stdout)


def check():
    out = subprocess.run(["node", str(D / "daily.js"), "check"], capture_output=True, text=True, cwd=str(ROOT))
    if out.returncode:
        raise SystemExit("build_daily: the schedule names items that cannot be served:\n" + out.stdout[-2000:])
    return out.stdout.strip()


def question_block(item, exam, static=True):
    """The question as HTML. Static pages list the choices; the live page turns the same
    markup into buttons."""
    meta = "%s · %s · difficulty %d of 5" % (exam["sections"].get(item["section"], item["section"]),
                                             exam["skills"].get(item["skill"], ""), int(item["diff"]))
    out = ['<p class="meta">%s</p>' % esc(meta)]
    if item.get("passage"):
        out.append('<div class="passage">%s</div>' % esc(item["passage"]))
    elif item.get("passageHtml"):
        # Our own bank's markup (tables and figures written for these items), rendered the
        # same way the trainer renders it.
        out.append('<div class="figure">%s</div>' % item["passageHtml"])
    out.append('<p class="stem">%s</p>' % esc(item["stem"]))
    if static:
        out.append('<ol class="static-opts" type="A">%s</ol>' %
                   "".join("<li>%s</li>" % esc(c) for c in item["choices"]))
    return "\n".join(out)


def answer_block(item):
    key = int(item["answer"])
    parts = ['<p><strong>The answer is %s: %s</strong></p>' % (LETTERS[key], esc(item["choices"][key])),
             '<div class="expl"><p>%s</p>' % esc(item["expl"])]
    if item.get("wrong"):
        parts.append('<h3>Why the Other Choices Fail</h3><p>%s</p>' % esc(item["wrong"]))
    parts.append("</div>")
    return "\n".join(parts)


def page(title, desc, path, body, ld, page_js="", feed=None):
    tpl = (D / "daily_template.html").read_text(encoding="utf-8")
    feed_link = ('<link rel="alternate" type="application/rss+xml" title="%s" href="%s">' % (esc(feed[0]), esc(feed[1]))
                 if feed else "")
    out = (tpl.replace("{{TITLE}}", esc(title)).replace("{{DESC}}", esc(desc))
              .replace("{{PATH}}", path).replace("{{FEED_LINK}}", feed_link)
              .replace("{{LD}}", json.dumps(ld))
              .replace("{{BODY}}", body).replace("{{STREAK_JS}}", streak_js())
              .replace("{{PAGE_JS}}", page_js))
    return partials.apply_chrome(out, extra_legal=LEGAL)


def crumbs(*pairs):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(pairs)]}


LIVE_JS = r"""<script>
(function(){
 var D=JSON.parse(document.getElementById('daily-data').textContent);
 var S=SFNDaily, today=S.today(), L='ABCDE';
 function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
 var pick=null; D.days.forEach(function(x){ if(x.date===today) pick=x; });
 var live=!!pick;
 if(!pick){ var le=D.days.filter(function(x){return x.date<=today;}); pick=le.length?le[le.length-1]:D.days[D.days.length-1]; }
 if(!pick) return;
 var q=pick.item, root=document.getElementById('q');
 document.getElementById('qdate').textContent=live?'Today, '+D.longDates[pick.date]:'Latest question, '+D.longDates[pick.date];
 if(!live) document.getElementById('stale').hidden=false;
 var h='<p class="meta">'+esc(D.sections[q.section]||q.section)+' · '+esc(D.skills[q.skill]||'')+' · difficulty '+q.diff+' of 5</p>';
 if(q.passage) h+='<div class="passage">'+esc(q.passage)+'</div>'; else if(q.passageHtml) h+='<div class="figure">'+q.passageHtml+'</div>';
 h+='<p class="stem">'+esc(q.stem)+'</p><ol class="opts">'+q.choices.map(function(c,i){return '<li><button type="button" class="opt" data-i="'+i+'"><span class="l">'+L[i]+'</span><span class="t">'+esc(c)+'</span></button></li>';}).join('')+'</ol>';
 root.innerHTML=h;
 var t0=Date.now(), res=document.getElementById('res');
 function paint(chosen,secs,correct){
  root.querySelectorAll('.opt').forEach(function(b,i){ b.disabled=true; if(i===q.answer) b.classList.add('right'); else if(i===chosen) b.classList.add('wrong'); b.setAttribute('aria-pressed',i===chosen?'true':'false'); });
  var st=S.stats(D.slug,today);
  var r='<div class="result '+(correct?'ok':'no')+'"><h2>'+(correct?'Correct':'Not This Time')+'</h2>'
   +'<p>The answer is '+L[q.answer]+'. '+(chosen>=0&&chosen!==q.answer?'You chose '+L[chosen]+'. ':'')+'Answered in '+S.clock(secs)+'.</p>'
   +(live?'<p>'+(st.current>1?st.current+' day streak.':'Day one of your streak.')+' A day counts whether you get it right or not.</p>':'<p>This is not today\'s question, so it does not count toward a streak.</p>')
   +'</div><div class="expl"><h3>Explanation</h3><p>'+esc(q.expl)+'</p>'+(q.wrong?'<h3>Why the Other Choices Fail</h3><p>'+esc(q.wrong)+'</p>':'')+'</div>'
   +'<div class="row" style="margin:16px 0">'+(live?'<button type="button" class="btn" id="share">Share Result</button>':'')
   +'<a class="btn sec" href="'+esc(D.appPath)+'">Practice '+esc(D.skills[q.skill]||'This Skill')+'</a></div>'
   +'<p class="small">The share text says whether you solved it and how fast. It never includes the question or the answer, so it cannot spoil it for anyone.</p>';
  res.innerHTML=r; streak();
  var sb=document.getElementById('share');
  if(sb) sb.addEventListener('click',function(){
   var txt=S.shareText(D.slug,D.short,pick.date,correct,secs,S.stats(D.slug,today).current);
   if(navigator.share){ navigator.share({text:txt}).catch(function(){}); return; }
   if(navigator.clipboard){ navigator.clipboard.writeText(txt).then(function(){ sb.textContent='Copied'; },function(){ window.prompt('Copy this:',txt); }); return; }
   window.prompt('Copy this:',txt);
  });
 }
 var done=S.days(D.slug)[pick.date];
 if(live&&done){ paint(typeof done.ch==='number'?done.ch:(done.c?q.answer:-1),done.s,!!done.c); }
 else root.querySelectorAll('.opt').forEach(function(b){ b.addEventListener('click',function(){
  var i=+b.getAttribute('data-i'), secs=(Date.now()-t0)/1000, ok=i===q.answer;
  if(live) S.record(D.slug,pick.date,ok,secs,i);
  // The same unlinkable row the trainer sends for every answer (privacy.html, section 1):
  // which item, which option, right or wrong, how long. No account, session or device, so
  // it cannot be tied to a person; it is how we learn whether daily questions are answered.
  try{ fetch(D.itemEventsUrl,{method:'POST',headers:{'Content-Type':'application/json','Prefer':'return=minimal'},
   body:JSON.stringify({exam:D.examId,qid:q.id,skill:q.skill||null,section:q.section||null,diff:q.diff||null,
    chosen:i,correct:ok,secs:Math.max(0,Math.min(3600,Math.round(secs))),mode:live?'daily':'daily_late'}),keepalive:true}).catch(function(){}); }catch(e){}
  paint(i,secs,ok);
 }); });
 function streak(){
  var st=S.stats(D.slug,today), el=document.getElementById('streak');
  el.innerHTML='<div class="tiles"><div class="tile"><div class="n">'+st.current+'</div><div class="k">Day Streak</div></div>'
   +'<div class="tile"><div class="n">'+st.freezes+'</div><div class="k">Freezes</div></div>'
   +'<div class="tile"><div class="n">'+st.bestRun+'</div><div class="k">Best Run</div></div></div>'
   +'<p class="small">'+(st.doneToday?'Done for today. The next question arrives at midnight, your time.':'Answer today to keep it going.')+' Best streak '+st.best+' days; '+st.correct+' of '+st.answered+' answered correctly.</p>';
 }
 streak();
})();
</script>"""


HUB_JS = r"""<script>
(function(){
 var D=JSON.parse(document.getElementById('daily-data').textContent), S=SFNDaily, today=S.today();
 D.exams.forEach(function(e){
  var pick=null; e.days.forEach(function(x){ if(x.date===today) pick=x; });
  if(!pick){ var le=e.days.filter(function(x){return x.date<=today;}); pick=le.length?le[le.length-1]:null; }
  var card=document.getElementById('ex-'+e.slug); if(!card||!pick) return;
  card.querySelector('.meta').textContent=pick.meta;
  card.querySelector('.prev').textContent=pick.preview;
  var st=S.stats(e.slug,today), s=card.querySelector('.st');
  s.textContent=st.doneToday?(st.todayCorrect?'Solved today':'Answered today')+(st.current>1?', '+st.current+' day streak':''):(st.current>0?st.current+' day streak, answer today to keep it':'Not answered yet today');
 });
})();
</script>"""


def main():
    s = load_schedule()
    if not s:
        print("build_daily: no data/daily/schedule.json; skipping /daily/")
        return
    status = check()
    t = build_date()
    first = s["start"]
    last_built = t.isoformat()
    window_hi = (t + datetime.timedelta(days=1)).isoformat()
    window_lo = (t - datetime.timedelta(days=1)).isoformat()
    # Before the first scheduled day the window still has to reach it, or the section
    # would build empty on a deploy that lands a day early.
    if window_hi < first:
        window_hi = first
    data = export(first, window_hi)
    exams = data["exams"]
    by_date = {row["date"]: row["items"] for row in data["days"]}
    past = sorted(d for d in by_date if d <= last_built)
    out_root = ROOT / "daily"
    # Start from nothing. A dated page left by a build with a later date would otherwise
    # survive into this one, publishing a question before its day.
    if out_root.exists():
        import shutil
        shutil.rmtree(out_root)
    written = 0

    def write(rel, content):
        nonlocal written
        p = out_root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if "{{" in content:
            raise SystemExit("build_daily: unresolved placeholder in /daily/%s" % rel)
        p.write_text(content, encoding="utf-8")
        written += 1

    hub_exams = []
    for eid in ORDER:
        ex = exams[eid]
        slug, short, name = ex["slug"], ex["short"], SEARCH_NAME[eid]
        base = "/daily/%s/" % slug
        feed_title = "%s Question of the Day, Start From Nowhere" % name
        # --- archive pages, newest last so prev/next are simple ---
        dates = [d for d in past if eid in by_date[d]]
        for i, d in enumerate(dates):
            item = by_date[d][eid]
            skill = ex["skills"].get(item["skill"], "")
            title = "%s Question of the Day for %s" % (name, long_date(d))
            stem1 = " ".join(item["stem"].split())
            # Meta descriptions stay inside 155 characters (EDITORIAL.md): the lead, then as much
            # of the stem as fits, then the promise.
            lead = "%s %s question, %s: " % (name, ex["sections"].get(item["section"], ""), skill)
            tail = " Answer and full explanation."
            room = max(20, 155 - len(lead) - len(tail) - 3)
            desc = lead + (stem1 if len(stem1) <= room else stem1[:room].rsplit(" ", 1)[0] + "...") + tail
            prev_l = ('<a href="%s%s/">Previous: %s</a>' % (base, dates[i - 1], short_date(dates[i - 1]))) if i > 0 else "<span></span>"
            next_l = ('<a href="%s%s/">Next: %s</a>' % (base, dates[i + 1], short_date(dates[i + 1]))) if i + 1 < len(dates) else \
                     ('<a href="%s">Today\'s question</a>' % base)
            body = ('<p class="crumb"><a href="/daily/">Daily Questions</a> / <a href="%s">%s</a> / %s</p>'
                    '<div class="head"><p class="eyebrow">%s, Daily Question Archive</p><h1>%s</h1>'
                    '<p class="lede">The %s question of the day scheduled for %s. Work it before you open the answer; '
                    'the explanation names the trap each wrong choice sets.</p></div>'
                    '<div class="grid"><div>%s<details class="ans"><summary>Show the Answer and Explanation</summary>%s</details>'
                    '<div class="pager">%s%s</div></div>'
                    '<aside class="side"><div class="card"><p class="eyebrow">Today</p><h2>Answer Today\'s %s Question</h2>'
                    '<p>One question a day, the same one for everyone, and a streak that counts showing up.</p>'
                    '<a class="btn" href="%s">Today\'s Question</a></div>'
                    '<div class="card"><p class="eyebrow">Practice</p><h2>Train %s</h2><p>The %s trainer keeps a rating for %s and every other skill the score report names, and serves what you need next.</p>'
                    '<a class="btn sec" href="%s">Open the %s Trainer</a></div></aside></div>'
                    % (base, esc(name), esc(short_date(d)), esc(name), esc(title), esc(name), esc(long_date(d)),
                       question_block(item, ex), answer_block(item), prev_l, next_l, esc(name), base,
                       esc(skill), esc(short), esc(skill), esc(ex["appPath"]), esc(short)))
            ld = crumbs(("Daily Questions", "/daily/"), ("%s Question of the Day" % name, base), (long_date(d), "%s%s/" % (base, d)))
            write("%s/%s/index.html" % (slug, d), page(title, desc, "%s%s/" % (base, d), body, ld,
                                                        feed=(feed_title, base + "feed.xml")))
        # --- the live page ---
        win = [{"date": d, "item": by_date[d][eid]} for d in sorted(by_date) if window_lo <= d <= window_hi and eid in by_date[d]]
        if not win:
            raise SystemExit("build_daily: nothing scheduled for %s around %s; extend the schedule" % (eid, last_built))
        # The latest day not after the build date; before the first scheduled day, that day.
        past_win = [w for w in win if w["date"] <= last_built]
        fallback = past_win[-1] if past_win else win[0]
        payload = {"slug": slug, "examId": eid, "itemEventsUrl": partials.ITEM_EVENTS_URL,
                   "short": name, "appPath": ex["appPath"], "skills": ex["skills"],
                   "sections": ex["sections"], "days": win, "longDates": {w["date"]: long_date(w["date"]) for w in win}}
        recent = "".join('<li><a href="%s%s/">%s</a></li>' % (base, d, esc(long_date(d))) for d in reversed(dates[-60:]))
        body = ('<p class="crumb"><a href="/daily/">Daily Questions</a> / %s</p>'
                '<div class="head"><p class="eyebrow" id="qdate">%s</p><h1>%s Question of the Day</h1>'
                '<p class="lede">One question a day, the same one for every %s student. Answer it and the day '
                'counts toward your streak, right or wrong; your accuracy is kept separately as a personal best. '
                'Free, and no account needed.</p></div>'
                '<p class="small" id="stale" hidden>Today\'s question has not been published yet. This is the most recent one, '
                'and answering it will not count toward your streak.</p>'
                '<div class="grid"><div><div id="q">%s</div><div id="res" aria-live="polite"></div>'
                '<noscript><details class="ans"><summary>Show the Answer and Explanation</summary>%s</details></noscript></div>'
                '<aside class="side"><div class="card"><p class="eyebrow">Your Streak</p><div id="streak"><p class="small">Answer to start one.</p></div>'
                '<p class="small">A streak counts days you answered. Every seven days in a row earns a freeze, up to two, and a freeze covers a missed day automatically. It lives only in this browser.</p></div>'
                '<div class="card"><p class="eyebrow">Past Questions</p><ul class="days">%s</ul>'
                '<p class="small"><a href="%sfeed.xml">RSS feed</a></p></div></aside></div>'
                '<script type="application/json" id="daily-data">%s</script>'
                % (esc(name), esc("Today, " + long_date(fallback["date"])), esc(name), esc(name),
                   question_block(fallback["item"], ex), answer_block(fallback["item"]),
                   recent or "<li>The first question is today's.</li>", base,
                   json.dumps(payload).replace("</", "<\\/")))
        title = "%s Question of the Day: Free, With Explanations" % name
        desc = ("A free %s practice question every day, the same one for everyone, with a full explanation of "
                "the answer and every trap. Keep a streak, share your result." % name)
        ld = crumbs(("Daily Questions", "/daily/"), ("%s Question of the Day" % name, base))
        write("%s/index.html" % slug, page(title, desc, base, body, ld, LIVE_JS, feed=(feed_title, base + "feed.xml")))
        # --- RSS: the last thirty days, newest first ---
        items = []
        for d in reversed(dates[-30:]):
            it = by_date[d][eid]
            dt = datetime.datetime.fromisoformat(d + "T00:00:00+00:00")
            items.append("<item><title>%s</title><link>%s%s%s/</link><guid>%s%s%s/</guid><pubDate>%s</pubDate>"
                         "<description>%s</description></item>"
                         % (esc("%s Question of the Day for %s" % (name, long_date(d))), SITE, base, d, SITE, base, d,
                            dt.strftime("%a, %d %b %Y %H:%M:%S +0000"),
                            esc(" ".join(it["stem"].split())[:300] + " Answer and explanation on the page.")))
        rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>%s</title><link>%s%s</link>'
               '<description>%s</description><language>en-us</language>%s</channel></rss>\n'
               % (esc(feed_title), SITE, base, esc("One free %s practice question a day, with a full explanation." % name),
                  "".join(items)))
        write("%s/feed.xml" % slug, rss)
        # --- hub card data ---
        hub_exams.append({"slug": slug, "name": name, "short": short, "days": [
            {"date": w["date"], "meta": "%s · %s" % (ex["sections"].get(w["item"]["section"], ""), ex["skills"].get(w["item"]["skill"], "")),
             "preview": " ".join(w["item"]["stem"].split())[:220]} for w in win]})

    cards = []
    for e in hub_exams:
        fb = ([x for x in e["days"] if x["date"] <= last_built] or e["days"][:1])[-1]
        cards.append('<div class="card ex" id="ex-%s"><p class="eyebrow">%s</p><p class="meta">%s</p>'
                     '<p class="prev">%s</p><p class="small st">Not answered yet today</p><div class="grow"></div>'
                     '<a class="btn" href="/daily/%s/">Answer Today\'s %s Question</a></div>'
                     % (e["slug"], esc(e["name"]), esc(fb["meta"]), esc(fb["preview"]), e["slug"], esc(e["name"])))
    body = ('<div class="head"><p class="eyebrow">Free, Every Day</p><h1>Daily Questions</h1>'
            '<p class="lede">One question a day for each exam we train, the same one for everyone. Answer it, read '
            'the explanation, and keep a streak that counts showing up rather than punishing a miss.</p></div>'
            '<div class="exams">%s</div>'
            '<div class="how"><h2>How It Works</h2>'
            '<p>Each exam gets one original question a day, chosen from our hand-written bank and fixed in advance, so '
            'everyone answering today sees the same one. A new question arrives at midnight your time.</p>'
            '<ul><li><strong>Your streak counts days you answered</strong>, right or wrong. Showing up is the habit; '
            'accuracy is tracked separately as your best run of correct days.</li>'
            '<li><strong>Freezes protect it.</strong> Every seven days in a row earns one, you can hold two, and a freeze '
            'covers a missed day automatically. They are earned, never sold.</li>'
            '<li><strong>Your first answer counts.</strong> The explanation appears after you answer, with why each wrong '
            'choice fails.</li>'
            '<li><strong>No leaderboard.</strong> You compete with your own record. Streaks are stored only in this browser '
            'and are not sent anywhere.</li></ul>'
            '<p>Every past question stays online with its answer and explanation, and each exam has an RSS feed: '
            '%s.</p></div>'
            '<script type="application/json" id="daily-data">%s</script>'
            % ("".join(cards),
               ", ".join('<a href="/daily/%s/feed.xml">%s</a>' % (e["slug"], esc(e["name"])) for e in hub_exams),
               json.dumps({"exams": hub_exams}).replace("</", "<\\/")))
    title = "Daily GMAT, SAT, GRE, LSAT and ACT Practice Questions"
    desc = ("One free practice question a day for the GMAT, SAT, GRE, LSAT and ACT, the same for everyone, with full "
            "explanations and a streak that counts showing up.")
    write("index.html", page(title, desc, "/daily/", body, crumbs(("Daily Questions", "/daily/")), HUB_JS))

    runway = status.split(",")[-1].strip()
    print("built daily/: %d files, %d archive days per exam through %s; %s" % (written, len(past), last_built, runway))
    left = len([d for d in s["days"] if d > last_built])
    if left < RUNWAY_WARN:
        print("build_daily: WARNING only %d scheduled days remain; run node src/daily.js extend" % left)


if __name__ == "__main__":
    main()
