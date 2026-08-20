"""Build The Study Room (blog) from src/blog/*.html post files.

Each post file: an HTML comment front-matter block with JSON metadata,
followed by the article body (h2/h3/p/table/ul only, no h1).

    <!--meta
    { "slug": "...", "title": "...", ... }
    -->
    <p>Body...</p>

Outputs (all gitignored; Cloudflare Pages runs this at deploy):
    blog/index.html            blog hub, per design/ui_kits/website/blog.html
    blog/<slug>/index.html     article pages
    sitemap.xml                whole-site sitemap

Validation is strict and fails the build: standing content rules live here
(design/guidelines/seo-content.md is the strategy source of truth).
"""
import json, pathlib, re, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import partials

SITE = "https://startfromnowhere.com"  # confirm owned domain; single place to change
SRC = pathlib.Path(__file__).parent
ROOT = SRC.parent
POSTS_DIR = SRC / "blog"
CATEGORIES = {
    "Exam Guides": "quant", "Study Science": "data", "Admissions": "verbal",
    "Success Stories": "green", "Company News": "gold",
}
# Pen names of the SFN editorial team. Bylines only: no invented credentials or bios.
AUTHORS = ["Maya Chen", "Sarah Whitfield", "Elena Rodriguez", "Aisha Thompson",
           "David Okafor", "James Corbett", "SFN Team"]
PALETTES = {
    "quant": ("var(--blue-600)", "var(--blue-50)"),
    "verbal": ("var(--violet-600)", "var(--violet-50)"),
    "data": ("var(--teal-600)", "var(--teal-50)"),
    "gold": ("var(--gold-700)", "var(--gold-50)"),
    "green": ("var(--green-700)", "var(--green-50)"),
    "gray": ("var(--gray-700)", "var(--gray-100)"),
    "navy": ("var(--gold-500)", "var(--navy-800)"),
}
BANNED_SOURCES = ("gmatclub", "quora.com", "wikipedia.org", "gyandhan", "pagalguy")
MONTHS = "January February March April May June July August September October November December".split()

def fail(msg): sys.exit(f"build_blog: {msg}")

def fmt_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m)-1]} {int(d)}, {y}"

def load_posts():
    posts = []
    for f in sorted(POSTS_DIR.glob("*.html")):
        text = f.read_text()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", text, re.S)
        if not m: fail(f"{f.name}: missing <!--meta {{...}} --> front matter")
        try: meta = json.loads(m.group(1))
        except json.JSONDecodeError as e: fail(f"{f.name}: bad JSON front matter: {e}")
        meta["body"] = text[m.end():].strip()
        meta["file"] = f.name
        posts.append(meta)
    if not posts: fail("no posts found in src/blog/")
    return posts

def split_live(posts):
    import datetime, os
    today = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
    live = [p for p in posts if p.get("date", "9999") <= today]
    held = len(posts) - len(live)
    if held: print(f"build_blog: holding {held} future-dated post(s); they publish on deploys after their date")
    if not live: fail("no publishable posts found in src/blog/")
    return live

def validate(posts):
    slugs = {p["slug"] for p in posts}
    for p in posts:
        n = p["file"]
        for k in ("slug", "title", "description", "category", "date", "author", "read_min", "hero", "faq"):
            if k not in p: fail(f"{n}: missing '{k}'")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p["slug"]): fail(f"{n}: bad slug")
        if p["file"] != p["slug"] + ".html": fail(f"{n}: filename must match slug")
        if len(p["title"]) > 65: fail(f"{n}: title over 65 chars ({len(p['title'])})")
        if len(p["description"]) > 160: fail(f"{n}: description over 160 chars")
        if p["category"] not in CATEGORIES: fail(f"{n}: unknown category {p['category']}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p["date"]): fail(f"{n}: date must be YYYY-MM-DD")
        if "updated" in p and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p["updated"]): fail(f"{n}: bad updated date")
        if not 3 <= len(p["faq"]) <= 5: fail(f"{n}: FAQ must have 3 to 5 items")
        if p["author"] not in AUTHORS: fail(f"{n}: author must be one of AUTHORS")
        if p["category"] != "Company News" and not re.search(r'href="https://', p["body"]):
            print(f"build_blog: WARNING {n} has no outbound source link")
        if p["hero"].get("palette") not in PALETTES: fail(f"{n}: hero.palette must be one of {list(PALETTES)}")
        everything = p["title"] + p["description"] + p["body"] + json.dumps(p["faq"])
        if "—" in everything or "–" in everything:
            fail(f"{n}: em or en dash found; house style forbids them")
        for b in BANNED_SOURCES:
            if b in everything.lower(): fail(f"{n}: references banned source '{b}'")
        if re.search(r"<h1[\s>]", p["body"]): fail(f"{n}: body must not contain h1")
        if p["category"] != "Company News":
            sib = re.findall(r'href="/blog/([a-z0-9-]+)/"', p["body"])
            missing = [s for s in sib if s not in slugs]
            if missing: fail(f"{n}: links to unknown posts {missing}")
            if len(set(sib)) < 2: fail(f"{n}: needs at least 2 internal links to sibling posts")

HEAD_CSS = """*{box-sizing:border-box}body{margin:0;font-family:var(--body);color:var(--gray-700);background:#fff;font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
:root{--navy-900:#0C1F3A;--navy-800:#122B4E;--navy-600:#2C4E80;--navy-100:#DCE5F1;--navy-50:#F2F6FB;--gold-700:#8A6A25;--gold-600:#A8842F;--gold-500:#C7A252;--gold-100:#F0E4C8;--gold-50:#FAF5E8;--gray-900:#111827;--gray-700:#374151;--gray-500:#6B7280;--gray-300:#D1D5DB;--gray-200:#E5E7EB;--gray-100:#F3F4F6;--gray-50:#F9FAFB;--blue-600:#2563EB;--blue-50:#EFF6FF;--violet-600:#7C3AED;--violet-50:#F5F3FF;--teal-600:#0D9488;--teal-50:#F0FDFA;--green-700:#15803D;--green-100:#DCFCE7;--green-50:#F0FDF4;
--serif:'Source Serif 4',Georgia,serif;--display:'Manrope',system-ui,sans-serif;--body:'IBM Plex Sans',system-ui,sans-serif;--mono:'IBM Plex Mono',ui-monospace,monospace;--ease:cubic-bezier(.16,1,.3,1)}
h1,h2,h3{font-family:var(--serif);color:var(--navy-900);letter-spacing:-.01em;line-height:1.2;margin:0}
a{color:var(--navy-600)}.wrap{max-width:1120px;margin:0 auto;padding:0 24px}.narrow{max-width:720px;margin:0 auto;padding:0 24px}
header.site{border-bottom:1px solid var(--gray-200);background:#fff}header.site .wrap{height:68px;display:flex;align-items:center;gap:18px}
.wordmark{display:flex;align-items:center;gap:9px;font-family:var(--serif);font-weight:700;font-size:20px;color:var(--navy-900);text-decoration:none}.wordmark b{color:var(--navy-900)}
.roomtag{font-family:var(--serif);font-style:italic;font-size:17px;color:var(--gray-500);text-decoration:none}
.btn{font-family:var(--display);font-weight:700;font-size:14px;color:#fff;background:var(--navy-800);border-radius:8px;padding:9px 18px;text-decoration:none;white-space:nowrap}.btn:hover{background:var(--navy-900)}
.cat{font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.04em;text-decoration:none}
.postcard{display:block;text-decoration:none;border:1px solid var(--gray-200);border-radius:10px;overflow:hidden;background:#fff;box-shadow:0 1px 2px rgba(8,21,39,.06);transition:box-shadow 160ms var(--ease)}.postcard:hover{box-shadow:0 2px 8px rgba(8,21,39,.08)}
.postcard h2,.postcard h3{text-wrap:pretty}
footer.site{border-top:1px solid var(--gray-200);margin-top:64px}footer.site .wrap{padding:24px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;font-size:13px;color:var(--gray-500)}
footer.site nav{display:flex;gap:22px}footer.site a{color:var(--gray-500)}
article h2{font-size:26px;margin:40px 0 12px}article h3{font-size:19px;margin:28px 0 10px}article p{margin:0 0 16px}article ul,article ol{margin:0 0 16px;padding-left:24px}article li{margin-bottom:6px}
article table{border-collapse:collapse;width:100%;margin:8px 0 20px;font-size:14.5px}article th{font-family:var(--display);font-weight:700;font-size:13px;text-align:left;color:var(--navy-900);background:var(--gray-50)}article th,article td{border:1px solid var(--gray-200);padding:9px 12px;vertical-align:top}
article .tablewrap{overflow-x:auto}article strong{color:var(--gray-900)}
.faq{border:1px solid var(--gray-200);border-radius:10px;margin-top:8px}.faq details{border-bottom:1px solid var(--gray-200)}.faq details:last-child{border-bottom:0}.faq summary{cursor:pointer;font-family:var(--display);font-weight:700;font-size:15px;color:var(--navy-900);padding:14px 18px}.faq div{padding:0 18px 14px;font-size:15px}
.cta{background:var(--gold-50);border:1px solid var(--gold-100);border-radius:10px;padding:22px 24px;margin:40px 0 8px;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap}
@media(max-width:860px){.grid3{grid-template-columns:1fr!important}.feature{grid-template-columns:1fr!important}.feature .fhero{min-height:200px}}"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,600;0,8..60,700;1,8..60,400&family=Manrope:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">"""
FAVICON = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='12' fill='%23122B4E'/%3E%3Cpath d='M13 33 22 22l6 5 8.5-10' fill='none' stroke='%23fff' stroke-width='3.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3Cpath d='M29.5 16.5H37V24' fill='none' stroke='%23fff' stroke-width='3.4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">"""
LOGO = """<svg viewBox="0 0 48 48" width="30" height="30" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#122B4E"/><path d="M13 33 22 22l6 5 8.5-10" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M29.5 16.5H37V24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

BEACON = """<!-- sfn beacon: first-party, no third parties, raw IP never stored -->
<script>(function(){try{
var U="https://ftsqwbzhkzuudogkvoqa.supabase.co/rest/v1/site_events?apikey=sb_publishable_GToT4fK6RiwCZpPFE3bGiw_ThXq9qel";
var s=sessionStorage.getItem("sfn_sid");if(!s){s=Math.random().toString(36).slice(2)+Math.random().toString(36).slice(2,10);sessionStorage.setItem("sfn_sid",s);}
var p=location.pathname,t0=Date.now(),done=false;
function send(o){o.sid=s;o.path=p;try{fetch(U,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(o),keepalive:true});}catch(e){}}
send({kind:"pageview",ref:(document.referrer||"").slice(0,290)||null,utm:location.search.indexOf("utm_")>-1?location.search.slice(1,190):null,device:/Mobi|Android/i.test(navigator.userAgent)?"mobile":"desktop",vw:innerWidth});
function dur(){if(done)return;done=true;send({kind:"duration",dur_ms:Date.now()-t0});}
document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden")dur();});
addEventListener("pagehide",dur);
}catch(e){}})();</script>"""

def page(title, description, canonical, body, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Start From Nowhere">
<meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary">
{FONTS}
{FAVICON}
{extra_head}<style>{HEAD_CSS}
{partials.CHROME_CSS}</style></head><body>
{partials.header_html()}
{body}
{partials.footer_html()}
{BEACON}
</body></html>"""

def hero_block(p, big=False):
    fg, bg = PALETTES[p["hero"]["palette"]]
    inner = f"""<div style="text-align:center;padding:16px"><div style="font-family:var(--{p['hero'].get('font','serif')});font-weight:700;font-size:{'52px' if big else '26px'};color:{fg}">{html.escape(p['hero']['text'])}</div>"""
    if p["hero"].get("sub"):
        inner += f"""<div style="font-family:var(--display);font-weight:700;font-size:13px;color:{'var(--navy-100)' if p['hero']['palette']=='navy' else 'var(--gray-500)'};margin-top:8px">{html.escape(p['hero']['sub'])}</div>"""
    inner += "</div>"
    h = "min-height:340px" if big else "height:150px"
    return f"""<div class="fhero" style="background:{bg};{h};display:flex;align-items:center;justify-content:center">{inner}</div>"""

def card(p):
    fg, _ = PALETTES[CATEGORIES[p["category"]]]
    return f"""<a href="/blog/{p['slug']}/" class="postcard" data-cat="{p['category']}" data-title="{html.escape(p['title'].lower(), quote=True)}">{hero_block(p)}
<div style="padding:20px 22px"><span class="cat" style="color:{fg}">{p['category']}</span>
<h3 style="font-size:18px;margin-top:8px">{html.escape(p['title'])}</h3>
<div style="font-size:12px;color:var(--gray-500);margin-top:10px">{fmt_date(p['date'])} · {p['read_min']} min</div></div></a>"""

def build_index(posts):
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    feat = next((p for p in posts if p.get("featured")), posts[0])
    rest = [p for p in posts if p is not feat]
    fg, _ = PALETTES[CATEGORIES[feat["category"]]]
    cats = [c for c in CATEGORIES if any(p["category"] == c for p in posts)]
    chips = """<a href="#" class="cat chip active" data-cat="All" style="border-radius:999px;padding:8px 18px">All</a>""" + "".join(
        f"""<a href="#" class="cat chip" data-cat="{c}" style="border-radius:999px;padding:8px 18px">{c}</a>""" for c in cats)
    featured = f"""<a href="/blog/{feat['slug']}/" class="postcard feature" style="display:grid;grid-template-columns:1.1fr 1fr;align-items:center">{hero_block(feat, big=True)}
<div style="padding:40px 48px"><span class="cat" style="color:{fg}">{feat['category']}</span>
<h2 style="font-size:32px;margin-top:10px">{html.escape(feat['title'])}</h2>
<p style="font-size:15px;color:var(--gray-500);margin:12px 0 0">{html.escape(feat['description'])}</p>
<div style="font-size:13px;color:var(--gray-500);margin-top:16px"><span style="font-family:var(--display);font-weight:700;color:var(--navy-900)">{html.escape(feat['author'])}</span> · {fmt_date(feat['date'])} · {feat['read_min']} min read</div>
</div></a>"""
    body = f"""<section class="wrap" style="padding:64px 24px 40px;text-align:center">
<h1 style="font-size:44px;text-wrap:pretty">Insight for your next big exam</h1>
<nav aria-label="Categories" style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:26px">{chips}</nav>
<div style="margin-top:18px"><input type="search" id="q" placeholder="Search articles" aria-label="Search blog" style="font:inherit;font-size:14px;border:1px solid var(--gray-300);border-radius:999px;padding:8px 18px;width:260px;outline:none"></div>
</section>
<section class="wrap" style="padding:0 24px 56px">
{featured}
<div class="grid3" style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:20px" id="grid">
{"".join(card(p) for p in rest)}
</div>
<div style="display:flex;align-items:center;justify-content:center;gap:16px;margin-top:28px;font-size:14px">
<button id="pgPrev" aria-label="Previous page" style="font:inherit;border:1px solid var(--gray-300);background:#fff;border-radius:8px;padding:7px 14px;cursor:pointer">&larr;</button>
<span id="pgInfo" style="font-family:var(--display);font-weight:600;color:var(--navy-900)"></span>
<button id="pgNext" aria-label="Next page" style="font:inherit;border:1px solid var(--gray-300);background:#fff;border-radius:8px;padding:7px 14px;cursor:pointer">&rarr;</button>
<label style="color:var(--gray-500)">Show <select id="pgSize" style="font:inherit;border:1px solid var(--gray-300);border-radius:6px;padding:4px 6px"><option>6</option><option>12</option><option>24</option></select> per page</label>
</div>
</section>
<section style="background:var(--gray-50);border-top:1px solid var(--gray-200)">
<div class="narrow" style="padding:64px 24px">
<div style="text-align:center"><h2 style="font-size:30px">Share your story</h2>
<p style="font-size:15px;color:var(--gray-500);margin:10px auto 0;max-width:480px">Passed your exam? Found a study method that worked? Submit your story or article. Our editors review every submission for publication.</p></div>
<form id="submitForm" style="display:grid;gap:14px;margin-top:28px">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
<label style="display:grid;gap:6px;font-size:13px;font-weight:600;color:var(--navy-900)">Your name<input required name="name" style="font:inherit;font-size:15px;border:1.5px solid var(--gray-300);border-radius:8px;padding:11px 14px"></label>
<label style="display:grid;gap:6px;font-size:13px;font-weight:600;color:var(--navy-900)">Email<input type="email" required name="email" style="font:inherit;font-size:15px;border:1.5px solid var(--gray-300);border-radius:8px;padding:11px 14px"></label>
</div>
<label style="display:grid;gap:6px;font-size:13px;font-weight:600;color:var(--navy-900)">Title of your story or article<input required name="title" placeholder="e.g. How I studied for the LSAT with a newborn" style="font:inherit;font-size:15px;border:1.5px solid var(--gray-300);border-radius:8px;padding:11px 14px"></label>
<label style="display:grid;gap:6px;font-size:13px;font-weight:600;color:var(--navy-900)">Your story<textarea required name="story" rows="6" placeholder="Paste your draft or outline. 300 words is plenty to start." style="font:inherit;font-size:15px;border:1.5px solid var(--gray-300);border-radius:8px;padding:11px 14px"></textarea></label>
<div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap">
<span style="font-size:12px;color:var(--gray-500)">Submissions open your mail app addressed to editors@startfromnowhere.com. If we publish, we credit you and confirm edits with you first.</span>
<button type="submit" class="btn" style="border:none;font-size:15px;padding:12px 26px;cursor:pointer">Submit for review</button>
</div>
</form>
</div>
</section>
<script>
document.getElementById('submitForm').addEventListener('submit',function(e){{e.preventDefault();var f=this,b='Name: '+f.name.value+'\\nEmail: '+f.email.value+'\\n\\n'+f.story.value;location.href='mailto:editors@startfromnowhere.com?subject='+encodeURIComponent('[Story] '+f.title.value)+'&body='+encodeURIComponent(b);}});
(function(){{var chips=document.querySelectorAll('.chip'),cards=Array.prototype.slice.call(document.querySelectorAll('#grid .postcard')),q=document.getElementById('q'),cat='All',page=0,size=6;
var prev=document.getElementById('pgPrev'),next=document.getElementById('pgNext'),info=document.getElementById('pgInfo'),sizeSel=document.getElementById('pgSize');
function apply(){{var s=q.value.toLowerCase();var vis=cards.filter(function(c){{return (cat==='All'||c.dataset.cat===cat)&&(!s||c.dataset.title.indexOf(s)>=0);}});
var pages=Math.max(1,Math.ceil(vis.length/size)); if(page>=pages) page=pages-1; if(page<0) page=0;
cards.forEach(function(c){{c.style.display='none';}}); vis.slice(page*size,(page+1)*size).forEach(function(c){{c.style.display='';}});
info.textContent='Page '+(page+1)+' of '+pages; prev.disabled=page===0; next.disabled=page>=pages-1;
prev.style.opacity=prev.disabled?'.4':'1'; next.style.opacity=next.disabled?'.4':'1';}}
prev.addEventListener('click',function(){{page--;apply();window.scrollTo(0,0);}});
next.addEventListener('click',function(){{page++;apply();window.scrollTo(0,0);}});
sizeSel.addEventListener('change',function(){{size=+sizeSel.value;page=0;apply();}});
chips.forEach(function(ch){{ch.addEventListener('click',function(e){{e.preventDefault();cat=ch.dataset.cat;page=0;chips.forEach(function(o){{o.classList.remove('active');o.style.background='';o.style.color='';o.style.border='1px solid var(--gray-300)';}});ch.style.background='var(--navy-800)';ch.style.color='#fff';ch.style.border='1px solid var(--navy-800)';apply();}});}});
chips.forEach(function(o){{o.style.border='1px solid var(--gray-300)';o.style.color='var(--navy-900)';}});var a=document.querySelector('.chip');a.style.background='var(--navy-800)';a.style.color='#fff';a.style.border='1px solid var(--navy-800)';
q.addEventListener('input',function(){{page=0;apply();}});apply();}})();
</script>"""
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "The Study Room",
          "description": "Study plans, exam guides, and score strategies from the Start From Nowhere team.",
          "url": f"{SITE}/blog/", "publisher": {"@type": "Organization", "name": "Start From Nowhere", "url": SITE}}
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    return page("The Study Room | GMAT and MBA Study Guides | Start From Nowhere",
                "Study plans, exam guides, and score strategies for the GMAT Focus Edition and beyond, from the Start From Nowhere team.",
                f"{SITE}/blog/", body, extra)

def delink_held(body, live_slugs):
    return re.sub(r'<a href="/blog/([a-z0-9-]+)/">(.*?)</a>',
                  lambda m: m.group(0) if m.group(1) in live_slugs else m.group(2), body)

def build_post(p, posts):
    fg, _ = PALETTES[CATEGORIES[p["category"]]]
    faq_vis = "".join(
        f"""<details><summary>{html.escape(f['q'])}</summary><div>{f['a']}</div></details>""" for f in p["faq"])
    related = [x for x in posts if x["slug"] in p.get("related", []) and x["slug"] != p["slug"]][:3]
    rel_html = ""
    if related:
        rel_html = f"""<section class="narrow" style="padding:8px 24px 0"><h2 style="font-size:22px;margin:32px 0 14px">Keep reading</h2>
<div class="grid3" style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{"".join(card(x) for x in related)}</div></section>"""
    updated = p.get("updated", p["date"])
    upd_note = f" · Updated {fmt_date(updated)}" if updated != p["date"] else ""
    body = f"""<article>
<div class="narrow" style="padding:52px 24px 0">
<nav style="font-size:13px" aria-label="Breadcrumb"><a href="/blog/">The Study Room</a> <span style="color:var(--gray-300)">/</span> <span class="cat" style="color:{fg}">{p['category']}</span></nav>
<h1 style="font-size:40px;margin-top:14px;text-wrap:pretty">{html.escape(p['h1'] if 'h1' in p else p['title'])}</h1>
<div style="font-size:14px;color:var(--gray-500);margin:16px 0 8px"><span style="font-family:var(--display);font-weight:700;color:var(--navy-900)">{html.escape(p['author'])}</span> · {fmt_date(p['date'])}{upd_note} · {p['read_min']} min read</div>
<hr style="border:none;border-top:1px solid var(--gray-200);margin:20px 0 28px">
{p['body']}
<div class="cta"><div><div style="font-family:var(--display);font-weight:800;font-size:17px;color:var(--navy-900)">Put this into practice</div>
<div style="font-size:14px;color:var(--gray-500);margin-top:4px">Run a free adaptive round. No account needed; the trainer finds your weak skills in one session.</div></div>
<a class="btn" href="/app/" style="font-size:15px;padding:12px 22px">Start a free round</a></div>
<h2 style="font-size:24px">Frequently asked questions</h2>
<div class="faq">{faq_vis}</div>
</div>
</article>
{rel_html}"""
    ld_article = {"@context": "https://schema.org", "@type": "BlogPosting",
        "headline": p["title"], "description": p["description"],
        "datePublished": p["date"], "dateModified": updated,
        "author": {"@type": "Person", "name": p["author"], "worksFor": {"@type": "Organization", "name": "Start From Nowhere"}},
        "publisher": {"@type": "Organization", "name": "Start From Nowhere", "url": SITE},
        "mainEntityOfPage": f"{SITE}/blog/{p['slug']}/"}
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["a"])}} for f in p["faq"]]}
    ld_crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "The Study Room", "item": f"{SITE}/blog/"},
        {"@type": "ListItem", "position": 2, "name": p["title"], "item": f"{SITE}/blog/{p['slug']}/"}]}
    extra = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>\n' for x in (ld_article, ld_faq, ld_crumb))
    extra += '<meta property="article:published_time" content="%s">\n' % p["date"]
    return page(p["title"] + " | Start From Nowhere", p["description"], f"{SITE}/blog/{p['slug']}/", body, extra)

def build_sitemap(posts):
    urls = [(SITE + "/", None), (SITE + "/blog/", None), (SITE + "/schools/", None), (SITE + "/exams/", None), (SITE + "/pricing/", None), (SITE + "/community/", None), (SITE + "/terms.html", None), (SITE + "/privacy.html", None)]
    exams_data = ROOT / "data" / "exams.json"
    if exams_data.exists():
        import json as _json2
        urls += [(f"{SITE}/exams/{e['slug']}/", None) for e in _json2.loads(exams_data.read_text())]
    schools_data = ROOT / "data" / "schools.json"
    if schools_data.exists():
        import json as _json
        urls += [(f"{SITE}/schools/{s['slug']}/", None) for s in _json.loads(schools_data.read_text()) if not s.get("discontinued")]
    urls += [(f"{SITE}/blog/{p['slug']}/", p.get("updated", p["date"])) for p in sorted(posts, key=lambda p: p["date"], reverse=True)]
    items = "".join(
        f"<url><loc>{u}</loc>{f'<lastmod>{d}</lastmod>' if d else ''}</url>\n" for u, d in urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n"""

def main():
    posts = load_posts()
    validate(posts)  # validate everything, including held future posts
    live = split_live(posts)
    live_slugs = {p["slug"] for p in live}
    out = ROOT / "blog"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(build_index(live))
    for p in live:
        d = out / p["slug"]
        d.mkdir(exist_ok=True)
        p = dict(p, body=delink_held(p["body"], live_slugs))
        (d / "index.html").write_text(build_post(p, live))
    (ROOT / "sitemap.xml").write_text(build_sitemap(live))
    print(f"built blog/ with {len(live)} posts + index + sitemap.xml")

if __name__ == "__main__":
    main()
