"""Checks each exam fact's figures against the page it cites (INC-0130).

    python3 src/check_sources.py              fetch every cited source and report
    python3 src/check_sources.py --cache DIR  keep what was fetched in DIR between runs
    python3 src/check_sources.py --render     read pages built by JavaScript in Chromium
    python3 src/check_sources.py --schools    check the MBA school library instead

The school library cites a College Scorecard figure to the Scorecard's data page, which
offers the dataset rather than printing any one school's numbers, so those figures are
counted and set aside: checking them means reading the dataset, not the page.

validate_exams.py proves that every published exam figure names a source, a year and a
URL. It cannot prove the source says it, and the GRE guide credited ETS with a combined
260 to 340 score that the ETS page it cited never mentions (INC-0130). This fetches every
page or PDF that data/exams.json cites and reports each number in a fact that its source
does not contain.

A fact may carry numbers it derives by arithmetic on its source, stated with the working:

    "derived": {"171": "50 + 45 + 36 + 40, the section question counts"}

A derived number is not looked for itself; the numbers in its working are, so the
arithmetic has to rest on figures the source prints. A number counted off the page, such
as the entries in a list, says so: "count: the US schools listed, counted 2026-09-26". What this finds is a report for a
person rather than a fix: a miss can be a paraphrase (five for 5) as easily as a wrong
figure, and only reading the source tells which.

It needs the network, so it runs in the weekly audit rather than in the build.
"""
import datetime
import hashlib
import html
import io
import json
import os
import pathlib
import re
import ssl
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMS = ROOT / "data" / "exams.json"
SCHOOLS = ROOT / "data" / "schools"
# Where a fact keeps numbers its source must print. An exam fact's note carries sourced
# detail (a fee's regional prices); a school figure's note is our own commentary, such as
# why a score must be on the classic scale, so --schools leaves it out.
FIELDS = ["text", "note", "stat"]
UA = "Mozilla/5.0 (compatible; StartFromNowhere source check; +https://startfromnowhere.com)"
# A number as a fact writes it: thousands commas allowed, decimals allowed. The commas are
# dropped before comparing, so 2,004,965 on the page matches 2004965 anywhere.
NUM = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.,])\d+(?:\.\d+)?")
# Sources write small numbers as words ("up to five times"), and a fact that writes 5 is
# saying the same thing, so the words count as their numbers on the source side.
WORDS = {w: str(i) for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen twenty".split())}
WORDS.update({"thirty": "30", "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70",
              "eighty": "80", "ninety": "90", "hundred": "100", "once": "1", "twice": "2"})
# A page that yields less readable text than this served a bot challenge or builds itself
# with JavaScript, and a number missing from it says nothing about the fact.
MIN_TEXT = 400


def norm(n):
    n = n.replace(",", "")
    return n.rstrip("0").rstrip(".") if "." in n else n


# "2026-27" names two years; the page may print "2026-2027", so both are read in full.
# Pages write a year range with a hyphen, a slash or an en dash; our data, by house rule, never
# with an en dash, so both sides must read the same way (INC-0140).
SPAN = re.compile(r"\b((?:19|20)(\d\d))[-/\u2013](\d\d)\b")


# "$175K" and "$47 M" are 175000 and 47000000 on the page, and a fact records them in full.
SUFFIX = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s?([kKmM])\b")
# "$30-70 k" puts the suffix on both ends of the range.
RANGE_SUFFIX = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s?[\u2013\u2014-]\s?\d[\d,]*(?:\.\d+)?\s?([kKmM])\b")
# Constants a derivation may use that no source needs to print: months in a year and the
# base of a percentage.
UNIT = {"12", "100"}


def numbers(text, words=False):
    text = SPAN.sub(lambda m: "%s %s%s" % (m.group(1), m.group(1)[:2], m.group(3)), str(text or ""))
    out = {norm(n) for n in NUM.findall(text)}
    for n, unit in SUFFIX.findall(text) + RANGE_SUFFIX.findall(text):
        out.add(norm("%.6f" % (float(n.replace(",", "")) * (1000 if unit in "kK" else 1000000))))
    if words:
        out |= {WORDS[w] for w in re.findall(r"[a-z]+", text.lower()) if w in WORDS}
    return out


def facts(exams):
    """(slug, where, fact) for every published figure that cites a URL."""
    out = []

    def walk(slug, where, o):
        if isinstance(o, dict):
            if o.get("url") and (o.get("text") is not None or o.get("v") is not None):
                out.append((slug, where, o))
            for k, v in o.items():
                walk(slug, "%s.%s" % (where, k) if where else k, v)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(slug, "%s[%d]" % (where, i), v)
    for e in exams:
        walk(e.get("slug"), "", e)
    return out


def ssl_context():
    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
        if os.environ.get(var) and os.path.exists(os.environ[var]):
            return ssl.create_default_context(cafile=os.environ[var])
    if os.path.exists("/root/.ccr/ca-bundle.crt"):
        return ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    return ssl.create_default_context()


def to_text(body, ctype):
    """The readable text of a fetched page or PDF."""
    if body[:5] == b"%PDF-" or "pdf" in ctype:
        try:
            from pdfminer.high_level import extract_text
        except ImportError:
            raise RuntimeError("a PDF, and pdfminer.six is not installed")
        return extract_text(io.BytesIO(body))
    t = body.decode("utf-8", errors="replace")
    # A comment is markup no reader sees. Kept, its text read as printed, and Arizona
    # State's 43 percent women was confirmed from a row the school had commented out
    # (INC-0152). It goes first, because a comment can hold tags and scripts.
    t = re.sub(r"<!--[\s\S]*?-->", " ", t)
    t = re.sub(r"<(script|style|noscript)[\s\S]*?</\1>", " ", t, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def render(url):
    """The page as a person reading it sees it, for a source that builds its text with
    JavaScript. src/render_page.js scrolls the page and reads every frame, because an
    embedded chart is its own document and may draw its figures only once scrolled into
    view (INC-0146)."""
    import subprocess
    r = subprocess.run(["node", str(ROOT / "src" / "render_page.js"), url, UA],
                       capture_output=True, text=True, timeout=180, cwd=str(ROOT))
    if r.returncode != 0:
        raise RuntimeError("could not render: " + (r.stderr.strip()[:200] or "no output"))
    return r.stdout


def fetch(url, cache, rendered=False):
    key = hashlib.sha1((("render:" if rendered else "") + url).encode()).hexdigest()
    if cache:
        hit = cache / (key + ".txt")
        if hit.exists():
            return hit.read_text(encoding="utf-8")
    if rendered:
        text = render(url)
    else:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45, context=ssl_context()) as r:
            text = to_text(r.read(), r.headers.get("Content-Type", "").lower())
    text = re.sub(r"\s+", " ", text)
    if cache:
        (cache / (key + ".txt")).write_text(text, encoding="utf-8")
    return text


def printed(fact):
    """The numbers a fact expects its source to print, leaving out the ones it derives."""
    want = set().union(*(numbers(fact.get(k)) for k in FIELDS))
    if isinstance(fact.get("v"), (int, float)):
        want.add(norm("%g" % fact["v"]))
    return want - set(fact.get("derived") or {})


def check(fact, source_nums):
    """The numbers in a fact that its source does not print, as (number, why)."""
    derived = fact.get("derived") or {}
    want = set().union(*(numbers(fact.get(k)) for k in FIELDS))
    if isinstance(fact.get("v"), (int, float)):
        want.add(norm("%g" % fact["v"]))
    missing = []
    for n in sorted(want, key=lambda x: float(x)):
        if n in source_nums:
            continue
        if n in derived:
            if str(derived[n]).startswith("count:"):
                continue
            inputs = numbers(derived[n]) - {n} - UNIT
            gone = sorted(inputs - source_nums, key=float)
            if gone:
                missing.append((n, "derived from %s, which the source does not print"
                                % ", ".join(gone)))
            continue
        missing.append((n, "not in the source"))
    return missing


# A number found on the page is not the fact found. Columbia's MBA class carried five years
# of work experience because the article says "an average of five years of work experience",
# in its paragraph on the 46-student MBAxMS cohort (INC-0150). For the school figures whose
# numbers are small enough to turn up anywhere, the number must also sit beside a word that
# says what it counts, and a passage about another program does not count.
LABELS = {
    "gpa": r"GPA|grade point",
    "work_exp_years": r"experience|years|months|worked|workforce",
    "women_pct": r"women|female",
    "intl_pct": r"international|countries|citizens|non-U\.?S|abroad|foreign|overseas",
    "accept_rate_pct": r"accept|admit|admission|selectiv",
    "employment_rate_pct": r"employ|offer|job|seeking|placement|graduation|accepted",
    "class_size": r"student|class|enrol|cohort|incoming|matriculat",
    "gmat_focus": r"GMAT|Focus|Edition",
    "gmat_classic": r"GMAT|Legacy|Classic|10th|Edition",
    "gre_quant": r"GRE|Quant",
    "gre_verbal": r"GRE|Verbal",
}
# Names of other programs. A dual degree such as the JD/MBA is left out: its students sit in
# the MBA class, and class profiles footnote them beside the figures.
OTHER_PROGRAM = re.compile(r"MBAxMS|MBA ?x ?MS\b|Executive MBA|\bEMBA\b|part[- ]time|\bevening\b|\bweekend\b|"
                           r"professional MBA|online MBA|hybrid MBA|Master of Science|\bMS in\b|\bMSx\b|"
                           r"Sloan Fellows", re.I)
NEAR, PASSAGE = 200, 200


def beside_label(field, fact, text):
    """None when a school figure's number sits beside its label in a passage about this
    program. Otherwise ("none", why) when it never does, which the report counts as not
    found, or ("other", why) when it does only near another program's name. Comparison
    tables and footnotes put other programs beside figures that are right, so that second
    kind is a list for a person to read rather than a failure; it is how Columbia's
    MBAxMS figure would have surfaced (INC-0150)."""
    label = LABELS.get(field)
    v = fact.get("v")
    if not label or not isinstance(v, (int, float)) or not text:
        return None
    forms = {norm("%g" % v)}
    derived = fact.get("derived") or {}
    for n in list(forms):
        if n in derived:
            if str(derived[n]).startswith("count:"):
                return None
            forms = numbers(derived[n]) - {n} - UNIT
    if not forms:
        return None
    alts = [r"(?<![\d.,])" + re.escape(n) + (r"0*" if "." in n else r"(?:\.0+)?") + r"(?![\d]|,\d)" for n in forms]
    alts += [r"\b%s\b" % w for w, n in WORDS.items() if n in forms]
    own = " ".join(str(fact.get(k) or "") for k in ("stat", "src"))
    other = set()
    for m in re.finditer("|".join(alts), text, re.I):
        if not re.search(label, text[max(0, m.start() - NEAR): m.end() + NEAR], re.I):
            continue
        near = {x.group(0) for x in OTHER_PROGRAM.finditer(text[max(0, m.start() - PASSAGE): m.end() + PASSAGE])
                if not re.search(re.escape(x.group(0)), own, re.I)}
        if not near:
            return None
        other |= near
    if other:
        return ("other", "beside its label only near another program's name (%s)" % ", ".join(sorted(other)[:3]))
    return ("none", "not beside a word that says what it counts")


# A page that describes itself as covering a year: "For the 2025-2026 testing year, the LSAT
# fee is $253." LSAC left that page up after the year ended, and a fact cited to it stayed
# wrong in words the number check could not see (INC-0136).
PERIOD = re.compile(r"\b[Ff]or the (\d{4})[-\u2013](\d{4}|\d{2}) (?:testing|academic|school|application|"
                    r"admissions|award|reporting) year\b")


def ended_periods(text, today):
    """The periods a page says it covers that ended before `today`, as 'YYYY-YYYY'. A
    testing or school year ends by June 30 of its second year."""
    out = set()
    for a, b in PERIOD.findall(text):
        end = int(b) if len(b) == 4 else int(a[:2] + b)
        if datetime.date(end, 6, 30) < today:
            out.add("%s-%d" % (a, end))
    return sorted(out)


def _selfcheck():
    """INC-0140: a year range reads as both years however the page punctuates it.
    INC-0150: a school figure is found only beside its label, in a passage about its program.
    INC-0152: a figure only inside an HTML comment is not printed; the same figure outside one is."""
    row = '<p class="tableItem Title">Female</p> <p class="tableItem">43%</p>'
    for page, want in (("<div>Class composition International 32%</div><!-- <div>" + row + "</div> -->", False),
                       ("<div>Class composition International 32%</div><div>" + row + "</div>", True)):
        if ("43" in numbers(to_text(page.encode(), "text/html"))) != want:
            sys.exit("check_sources: a figure %s an HTML comment was %s" % (
                ("inside", "read as printed") if not want else ("outside", "not found")))
    for sep in ("-", "/", "\u2013"):
        got = numbers("rates for 2026%s27" % sep)
        if not {"2026", "2027"} <= got:
            sys.exit("check_sources: a year range written with %r reads as %s, not 2026 and 2027"
                     % (sep, sorted(got)))
    mbaxms = ("Applications 7,477 5,876. Columbia has also updated the profile for its MBAxMS cohort. The incoming "
              "class includes 46 students with an average GPA of 3.54 and an average of five years of work experience.")
    for field, fact, text, want in (
            ("work_exp_years", {"v": 5, "stat": "average"}, mbaxms, "another program"),
            ("gpa", {"v": 3.28}, "Average Undergraduate GPA 3.28 Dual degree students include those pursuing the JD/MBA", None),
            ("intl_pct", {"v": 24}, "almost a quarter, 24% of students come to the program from abroad", None),
            ("work_exp_years", {"v": 5.25}, "Average Years of Work Experience 5.25 Average Undergraduate GPA 3.31", None),
            ("gpa", {"v": 3.7}, "Average GPA 3.70 (4.0 scale)", None),
            ("women_pct", {"v": 44}, "Class of 2027: 44% Women, 26% International", None),
            ("women_pct", {"v": 44}, "Room 44 is on the second floor of the business school building.", "not beside"),
            ("work_exp_years", {"v": 5.7, "derived": {"5.7": "68 months / 12"}}, "Average 68 months worked", None)):
        got = beside_label(field, fact, text)
        if (want is None) != (got is None) or (want and want not in got[1]):
            sys.exit("check_sources: beside_label(%s, %r) on %r gave %r" % (field, fact, text[:60], got))


def main(argv):
    _selfcheck()
    cache = None
    if "--cache" in argv:
        cache = pathlib.Path(argv[argv.index("--cache") + 1])
        cache.mkdir(parents=True, exist_ok=True)
    if "--schools" in argv:
        records = [json.loads(p.read_text()) for p in sorted(SCHOOLS.glob("*.json"))]
        FIELDS[:] = ["text", "stat"]
    else:
        records = json.loads(EXAMS.read_text())
    todo = facts(records)
    dataset = [t for t in todo if "scorecard" in str(t[2].get("src", "")).lower()]
    todo = [t for t in todo if t not in dataset]
    sources, unread, periods, texts = {}, {}, {}, {}
    today = datetime.date.fromisoformat(os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat())
    for url in sorted({f["url"] for _, _, f in todo}):
        try:
            text = fetch(url, cache)
            # A page that builds itself with JavaScript reads as nearly empty, or as
            # navigation without its figures, until a browser runs it. If the browser
            # cannot load it either, the static text is still evidence when there is
            # enough of it, so it is kept rather than thrown away.
            cited = [f for _, _, f in todo if f["url"] == url]
            misses = lambda t: sum(len(check(f, numbers(t, True))) for f in cited)
            if "--render" in argv and (len(text) < MIN_TEXT or misses(text)):
                try:
                    shown = fetch(url, cache, rendered=True)
                    # The browser's read replaces the page as served only when it is at
                    # least as good a witness: a render that comes back as a challenge
                    # page, or shorter, must not hide figures the served page printed.
                    if len(shown) >= MIN_TEXT and (len(text) < MIN_TEXT or misses(shown) <= misses(text)):
                        text = shown
                except Exception as e:
                    print("render failed for %s, using the page as served (%s)"
                          % (url, str(e).splitlines()[0][:120]))
            if len(text) < MIN_TEXT:
                raise RuntimeError("only %d characters of text, a bot challenge or a page "
                                   "built by JavaScript" % len(text))
            sources[url] = numbers(text, words=True)
            texts[url] = text
            periods[url] = ended_periods(text, today)
        except Exception as e:
            unread[url] = "%s: %s" % (type(e).__name__, e)
    # A page that prints none of the figures cited to it, when two or more are, has not
    # shown its data at all: a class profile drawn by JavaScript reads as prose with no
    # numbers until a browser runs it. Every figure on it would be reported as missing,
    # which says nothing about the figures, so the page is reported once instead.
    by_url = {}
    for _, _, f in todo:
        by_url.setdefault(f["url"], []).append(f)
    # Years do not count as evidence: "Class of 2027" is in the prose of a class profile
    # whose statistics never rendered.
    year = re.compile(r"(19|20)\d\d")
    evidence = lambda f: {n for n in printed(f) if not year.fullmatch(n)}
    blank = set()
    for u, fs in by_url.items():
        counted = [f for f in fs if evidence(f)]
        if u in sources and len(counted) >= 2 and not any(evidence(f) & sources[u] for f in counted):
            blank.add(u)
    bad, worth = 0, []
    for slug, where, f in todo:
        if f["url"] not in sources or f["url"] in blank:
            continue
        miss = check(f, sources[f["url"]])
        if "--schools" in argv and where.startswith("profile.") and not miss:
            got = beside_label(where.split(".", 1)[1], f, texts.get(f["url"]))
            if got and got[0] == "none":
                miss = [(norm("%g" % f["v"]), got[1])]
            elif got:
                worth.append("%s.%s  %s\n    %s: %s" % (slug, where, f["url"], norm("%g" % f["v"]), got[1]))
        if miss:
            bad += 1
            print("%s.%s  %s" % (slug, where, f["url"]))
            print("    %s" % str(f.get("text") or f.get("v"))[:220])
            for n, why in miss:
                print("    %s: %s" % (n, why))
    # The exam guides only: a school's fee page naming last year is the tuition queue's
    # business, and a reason to read the page rather than a fact about the exam.
    stale = 0
    if "--schools" not in argv:
        for slug, where, f in todo:
            ended = periods.get(f["url"]) or []
            seen = set((f.get("period_checked") or {}).get("periods") or [])
            if ended and not set(ended) <= seen:
                stale += 1
                print("%s.%s  %s" % (slug, where, f["url"]))
                print("    %s" % str(f.get("text") or f.get("v"))[:220])
                print("    the page says it covers the %s %s, which has ended: read the fact against a "
                      "current page, and if it still holds record that in its period_checked"
                      % (", ".join(ended), "year" if len(ended) == 1 else "years"))
    if worth:
        print("\nWorth reading: found beside its label only near another program's name, which a "
              "comparison table or footnote explains as often as a figure from the wrong program:")
        for w in worth:
            print(w)
        print()
    for url in sorted(blank):
        print("shows none of its %d figures, probably built by JavaScript: %s"
              % (len(by_url[url]), url))
    for url, why in sorted(unread.items()):
        print("could not read %s (%s)" % (url, why))
    print("\n%d facts checked against %d sources; %d with a number their source does not "
          "print; %d resting on a page about a period that has ended; %d sources unreadable, "
          "%d showing none of their figures; %d worth reading beside another program's name%s"
          % (len(todo), len(sources), bad, stale, len(unread), len(blank), len(worth),
          "; %d dataset figures set aside" % len(dataset) if dataset else ""))
    return 1 if bad or stale else (2 if unread else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
