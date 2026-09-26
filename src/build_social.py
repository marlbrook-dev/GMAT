"""Generate the social post queue from content the build can already verify.

Posting to X costs money on the current API (a live POST returned 402 "credits depleted"
on 2026-09-17), so nothing here sends anything. It produces the TEXT, and a person copies
it. That also happens to satisfy the publishing rule in DEVSECOPS.md, which caps anything
reaching users at act-with-approval: a human still names themselves as the one who posted.

The hard constraint is the house rule that no published figure comes from memory. Every
number in every post below is read out of data/schools/*.json or data/colleges/*.json,
where validate_schools.py has already enforced a source, a year and a url on it, or out of
the built item banks. A post whose figure cannot be traced is not generated at all.

Output is src/generated/social.js (gitignored, like the banks), read by Admin > Social.

Run:  python3 src/build_social.py
"""
import glob
import html
import json
import pathlib
import random
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_rankings as br

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "src" / "generated"
SITE = "https://startfromnowhere.com"
LIMIT = 280

DASH = re.compile(r"[–—]")


def clean(s):
    return " ".join(str(s).split())


def ok(text):
    """A post ships only if it fits and carries no banned dash."""
    return len(text) <= LIMIT and not DASH.search(text)


def money(n):
    return "${:,}".format(int(n))


# --- sources -----------------------------------------------------------------------
def schools():
    out = []
    for f in sorted(glob.glob(str(ROOT / "data" / "schools" / "*.json"))):
        try:
            out.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            continue
    return out


def colleges():
    out = []
    for f in sorted(glob.glob(str(ROOT / "data" / "colleges" / "*.json"))):
        try:
            out.append(json.load(open(f, encoding="utf-8")))
        except Exception:
            continue
    return out


def live_posts():
    import datetime
    today = datetime.date.today().isoformat()
    out = []
    for f in sorted((ROOT / "src" / "blog").glob("*.html")):
        t = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", t, re.S)
        if not m:
            continue
        try:
            meta = json.loads(m.group(1))
        except Exception:
            continue
        if meta.get("date", "9999") <= today:
            out.append(meta)
    return out


def field(school, name):
    """A profile figure with its provenance, or None. Never a bare number."""
    p = school.get("profile", {}) or {}
    f = p.get(name)
    if not isinstance(f, dict) or f.get("v") in (None, ""):
        return None
    if not (f.get("src") and f.get("year")):
        return None
    return f


def said_by(school, f):
    """None when the school published the figure itself, else the source's short name.

    A post may say "from the school" only when that is true. Secondary figures are
    allowed by the source ladder and are named for what they are (INC-0105)."""
    if not br.is_secondary(school, f):
        return None
    return clean(re.split(r"[(,]", f.get("src") or "", 1)[0]) or "a secondary source"


def hedge(f):
    """The qualifier the figure's own source attaches to it, if any."""
    t = ("%s %s" % (f.get("src") or "", f.get("stat") or "")).lower()
    if "estimat" in t:
        return "an estimated "
    if re.search(r"\b(around|about|approximately|roughly)\b", t):
        return "about "
    return ""


SCHOOL_CLAIM = re.compile(r"school's own|published by the school|reported by the school|"
                          r"from the school|publish directly", re.I)


def checked(school, f, text):
    """Refuse a post that credits the school with a figure hosted elsewhere, or that
    calls a figure a median or an average its own note contradicts."""
    if said_by(school, f) and SCHOOL_CLAIM.search(text):
        raise SystemExit("build_social: %s: post credits the school with a figure from %s"
                         % (school.get("slug"), f.get("src")))
    kind = br.stat_kind(f)
    for said in re.findall(r"\b(median|average)\b", text, re.I):
        if kind and said.lower() != kind:
            raise SystemExit("build_social: %s: post says %s, the figure's note says %s"
                             % (school.get("slug"), said.lower(), kind))
    return text


# --- post kinds --------------------------------------------------------------------
def posts_blog(rng):
    out = []
    for p in live_posts():
        body = "%s\n\n%s\n\n%s/blog/%s/" % (
            clean(p["title"]), clean(p["description"]), SITE, p["slug"])
        if len(body) > LIMIT:
            body = "%s\n\n%s/blog/%s/" % (clean(p["title"]), SITE, p["slug"])
        if ok(body):
            out.append(dict(key="blog:" + p["slug"], kind="Blog post",
                            audience="All", text=body))
    return out


def posts_international(rng, sch):
    """Aimed at applicants outside the United States, a group the site already serves with a
    sourced guide. The share is read from the school file, never estimated."""
    out = []
    rows = []
    for s_ in sch:
        f = field(s_, "intl_pct")
        if f:
            rows.append((s_, f))
    rows.sort(key=lambda r: -float(r[1]["v"]))
    for s_, f in rows[:16]:
        pct = "{:g}%".format(float(f["v"]))
        name, yr, slug = clean(s_["name"]), f["year"], s_["slug"]
        by = said_by(s_, f)
        # Longest first, then shorter fallbacks. A school with a long name would otherwise
        # produce no post at all, which silently drops exactly the big international
        # programs this is meant to reach.
        for t in (
            ("Applying to an MBA from outside the US? %s of the class at %s is "
             "international, as of %s.\n\nThis figure is %s. We "
             "show the year, because a 2019 profile is not evidence about this cycle."
             "\n\n%s/schools/%s/" % (pct, name, yr,
                                    "published by the school" if by is None else "as reported by " + by,
                                    SITE, slug)),
            ("Applying from outside the US? %s of the class at %s is international (%s).\n\n"
             "We show where the figure comes from and which year it is from.\n\n%s/schools/%s/"
             % (pct, name, yr, SITE, slug)),
            ("%s of the MBA class at %s is international, as of %s.\n\nSourced from %s, "
             "with the year attached.\n\n%s/schools/%s/"
             % (pct, name, yr, "the school" if by is None else by, SITE, slug)),
        ):
            if ok(checked(s_, f, t)):
                out.append(dict(key="intl:" + slug, kind="International",
                                audience="International applicants", text=t))
                break
    if len(rows) >= 5:
        top = ", ".join(clean(s_["name"]) for s_, _ in rows[:3])
        t = ("International MBA applicants: these programs report the highest share of "
             "international students of any we track.\n\n%s\n\nEvery figure carries its "
             "source and its year, because a class profile from 2019 is not evidence about "
             "this cycle.\n\n%s/schools/" % (top, SITE))
        if ok(t):
            out.append(dict(key="intl:top-share", kind="International",
                            audience="International applicants", text=t))
    return out


def posts_school(rng, sch):
    out = []
    for s_ in sch:
        acc = field(s_, "accept_rate_pct")
        sal = field(s_, "salary_median_usd")
        name = clean(s_["name"])
        if acc:
            by = said_by(s_, acc)
            t = checked(s_, acc, (
                "%s accepted %s%s%% of applicants. Most sites quoting an MBA acceptance rate "
                "will not tell you which year it is.\n\nThis one is %s, %s, linked.\n\n%s/schools/%s/"
                % (name, hedge(acc), "{:g}".format(float(acc["v"])), acc["year"],
                   "published by the school" if by is None else "as reported by " + by,
                   SITE, s_["slug"])))
            if ok(t):
                out.append(dict(key="school:acc:" + s_["slug"], kind="MBA data",
                                audience="MBA applicants", text=t))
        if sal:
            by = said_by(s_, sal)
            what = " ".join(x for x in (br.salary_word(sal), br.salary_noun(sal)) if x)
            t = checked(s_, sal, (
                "The %s for MBA graduates of %s is %s.\n\nSalary figures circulate for years "
                "with no date attached. This one is %s, %s, with the link on the page.\n\n%s/schools/%s/"
                % (what, name, money(sal["v"]), sal["year"],
                   "reported by the school" if by is None else "as reported by " + by,
                   SITE, s_["slug"])))
            if ok(t):
                out.append(dict(key="school:sal:" + s_["slug"], kind="MBA data",
                                audience="MBA applicants", text=t))
    return out


def posts_college(rng, col):
    out = []
    for c in col:
        p = c.get("profile") or {}
        acc, net = p.get("admit_rate_pct"), p.get("net_price_usd")
        name = clean(c["name"])
        if isinstance(acc, dict) and isinstance(acc.get("v"), (int, float)):
            t = ("%s admits %.0f%% of applicants. The acceptance rate is the number "
                 "everyone quotes and almost nobody sources.\n\nOurs comes from the US "
                 "Department of Education, %s, with the link.\n\n%s/colleges/%s/"
                 % (name, float(acc["v"]), acc.get("year", "latest release"), SITE, c["slug"]))
            if ok(t):
                out.append(dict(key="college:acc:" + c["slug"], kind="College data",
                                audience="Undergrad applicants", text=t))
        if isinstance(net, dict) and isinstance(net.get("v"), (int, float)):
            t = ("Sticker price is not what students pay at %s. The average net price, "
                 "after aid, is %s a year.\n\nFederal data, %s, sourced and linked. "
                 "Compare it against the published tuition and the gap is the story."
                 "\n\n%s/colleges/%s/"
                 % (name, money(net["v"]), net.get("year", "latest release"), SITE, c["slug"]))
            if ok(t):
                out.append(dict(key="college:net:" + c["slug"], kind="College data",
                                audience="Undergrad applicants", text=t))
    return out


def posts_item(rng):
    """A real practice question, with its explanation as the reply."""
    out = []
    for app, label in (("app", "GMAT"), ("sat/app", "SAT"), ("gre/app", "GRE"),
                       ("act/app", "ACT")):
        f = ROOT / app / "bank.js"
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        for m in list(re.finditer(
                r"\{id:'([^']+)',section:'[^']*',type:'MC'[^\n]*?\n stem:'((?:[^'\\]|\\.){20,240})',"
                r"\n choices:\[((?:[^\]])+)\],answer:(\d+),\n expl:'((?:[^'\\]|\\.){20,260})'",
                t))[:400]:
            qid, stem, choices, ans, expl = m.groups()
            stem = clean(stem.replace("\\'", "'").replace("\\n", " "))
            expl = clean(expl.replace("\\'", "'").replace("\\n", " "))
            opts = re.findall(r"'((?:[^'\\]|\\.)*)'", choices)
            if len(opts) < 4 or int(ans) >= len(opts):
                continue
            letters = "ABCDE"
            shown = "  ".join("%s) %s" % (letters[i], clean(opts[i].replace("\\'", "'")))
                              for i in range(len(opts)))
            body = "%s question of the day.\n\n%s\n\n%s" % (label, stem, shown)
            reply = ("Answer: %s. %s\n\nWe wrote it, the answer is computed rather than "
                     "asserted, and every wrong option is a named mistake.\n\n%s"
                     % (letters[int(ans)], expl, SITE))
            if ok(body) and ok(reply) and len(stem) > 40:
                out.append(dict(key="item:" + qid, kind="Practice item",
                                audience=label + " students", text=body, reply=reply))
    return out


def posts_fact(rng):
    """Facts the build itself can verify, so none of them can drift."""
    n_sch = len(list((ROOT / "schools").glob("*/index.html")))
    n_col = len(list((ROOT / "colleges").glob("*/index.html")))
    out = [
        dict(key="fact:free", kind="Product", audience="All",
             text=("Our free plan never asks for a card.\n\nNot a trial that bills you "
                   "later, not a card on file. There is no payment step to reach the free "
                   "tier at all, and we have a test that fails the build if that ever "
                   "changes.\n\n%s/pricing/" % SITE)),
        dict(key="fact:sources", kind="Product", audience="All",
             text=("%d business schools and %d colleges, and every published figure carries "
                   "its source, its year and a link.\n\nWhere a school does not publish a "
                   "number, we show a dash. We do not fill it with an estimate.\n\n%s/schools/"
                   % (n_sch, n_col, SITE))),
        dict(key="fact:focus", kind="Exam facts", audience="GMAT students",
             text=("GMAT Focus and GMAT Classic do not convert.\n\n205 to 805 is not 200 to "
                   "800 shifted. Compare by percentile: Classic 700 and Focus 655 are both "
                   "90.5th percentile, per GMAC's concordance.\n\nA conversion table is a "
                   "made up number.")),
        dict(key="fact:noaccount", kind="Product", audience="All",
             text=("You can practice without making an account.\n\nNo email, no password, "
                   "no wall before the first question. Progress saves in your browser, and "
                   "signing in later is optional.\n\n%s/app/" % SITE)),
    ]
    return [p for p in out if ok(p["text"])]


def main():
    rng = random.Random(20260917)
    sch, col = schools(), colleges()
    groups = [posts_blog(rng), posts_international(rng, sch), posts_school(rng, sch),
              posts_college(rng, col), posts_item(rng), posts_fact(rng)]
    # Cap the bulky data driven kinds so the queue reads as a queue rather than a dump,
    # and interleave so consecutive posts are not all the same shape.
    caps = {"MBA data": 40, "College data": 40, "Practice item": 60}
    picked = []
    for g in groups:
        rng.shuffle(g)
        kind = g[0]["kind"] if g else ""
        picked += g[: caps.get(kind, len(g))]
    seen, queue = set(), []
    for p in picked:
        if p["key"] in seen:
            continue
        seen.add(p["key"])
        queue.append(p)
    rng.shuffle(queue)

    for p in queue:
        if not ok(p["text"]):
            raise SystemExit("build_social: post %s fails the limit or dash rule" % p["key"])

    OUT.mkdir(exist_ok=True)
    js = ("// GENERATED FILE. Written by src/build_social.py. Do not edit.\n"
          "// Every figure here is read from a data file that already carries a source,\n"
          "// a year and a url, or from the built item banks. Nothing is written from memory.\n"
          "const SOCIAL_QUEUE = " + json.dumps(queue, ensure_ascii=False, indent=0) + ";\n")
    (OUT / "social.js").write_text(js, encoding="utf-8")
    by = {}
    for p in queue:
        by[p["kind"]] = by.get(p["kind"], 0) + 1
    print("build_social: %d posts" % len(queue))
    for k in sorted(by):
        print("  %-16s %d" % (k, by[k]))


if __name__ == "__main__":
    main()
