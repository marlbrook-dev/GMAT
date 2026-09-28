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
does not contain, or prints only away from every word of the fact, in a menu, a counter or
another passage, and outside any table (INC-0174).

A fact may carry numbers it derives by arithmetic on its source, stated with the working:

    "derived": {"171": "50 + 45 + 36 + 40, the section question counts"}

A derived number is not looked for itself; the numbers in its working are, so the
arithmetic has to rest on figures the source prints. A number counted off the page, such
as the entries in a list, says so: "count: the US schools listed, counted 2026-09-26". What this finds is a report for a
person rather than a fix: a miss can be a paraphrase (five for 5) as easily as a wrong
figure, and only reading the source tells which.

A school figure that is right but sits where this cannot read it, drawn as a graphic, held
in a chart's data, printed in an image or worked from a second page, is recorded in
data/source_triage.json once a person has read it, with the numbers this cannot find, why,
and the date (INC-0154). Those are reported apart, so the list of findings, and the exit
status the weekly job opens an issue on, holds only what nobody has judged. A figure worked
from two pages names the second in also_urls, and both are read.

A page that prints none of the figures cited to it is reported with what it prints beside
each figure's label (INC-0158). Other numbers there mean the page has probably moved on to a
newer class or been revised; nothing there means a person has to read it. Either way it
counts as a finding until every figure on it is fixed or triaged, because to a check that
looks for numbers, a page whose every figure changed looks exactly like one that never loaded.

An exam fact with no number at all, a delivery or a used-for line, is read by its words: each
content word must be on one of its pages, in some form, and the summary counts those facts
apart, since 20 of them were once counted as checked with nothing to look for (INC-0180).

It needs the network, so it runs in the weekly audit rather than in the build.
"""
import datetime
import hashlib
import html
import html.parser
import io
import json
import os
import pathlib
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMS = ROOT / "data" / "exams.json"
SCHOOLS = ROOT / "data" / "schools"
TRIAGE = ROOT / "data" / "source_triage.json"
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
# A bot challenge is a page of its own, and Imperva's on mba.com runs to 726 characters, so
# it passed MIN_TEXT and every number in a fact was reported missing from it (INC-0156).
# Short reads in a challenge's words are not the page; a long page that mentions a security
# check in passing is.
CHALLENGE = re.compile(r"Additional security check is required|protected and accelerated by Imperva|"
                       r"Incapsula incident|Just a moment\.\.\.|Checking your browser|Attention Required! \| Cloudflare|"
                       r"Verify(?:ing)? you are (?:a )?human|Please enable (?:cookies|JavaScript) to continue|"
                       r"Access Denied.{0,80}You don't have permission|Request unsuccessful|"
                       r"Performing security verification|uses a security service to protect against malicious bots|"
                       r"detected unusual activity from your computer network|let us know you're not a robot", re.I)
CHALLENGE_MAX = 3000
CHALLENGED = set()
# A site that refuses a script can still serve a browser: Baylor's pages answer 403 to the
# plain read and render in Chromium under the same user agent, while Columbia's and Michigan
# Ross's answer the browser with Cloudflare's verification page, which is then reported.
# Fordham's pages send a script round a redirect loop, setting a cookie a browser keeps and
# a script does not, and render in the browser too; urllib raises the redirect's own code
# only when it gives up on a loop, since it follows every other redirect itself.
REFUSED = {301, 302, 303, 307, 308, 401, 403, 429}


def challenged(text):
    """True when a read is a bot challenge rather than the page it was sent for."""
    return len(text) < CHALLENGE_MAX and bool(CHALLENGE.search(text))


# A PDF laid out in boxes can come out of the text extractor with each figure glued to its
# label: UMass Amherst's class profile reads "INTERNATIONAL STUDENTS39%" and "GPA3.45", and
# NUM reads no number that follows a letter, so the page showed none of its figures
# (INC-0158). A number is split from a word of three or more letters glued before it; codes
# such as H1B and Q3 are left alone.
GLUED = re.compile(r"(?<=[A-Za-z]{3})(?=\d)")


def unglue(text):
    return GLUED.sub(" ", text)


# A counter that counts up once scrolled into view is served as 0, with the figure it stops
# at in an attribute: Auburn's page as served reads "0 Average Undergraduate GPA" (INC-0158).
# A reader sees the figure it stops at, so that is what is read.
COUNTER = re.compile(r"(<([a-z][a-z0-9]*)\b[^>]*?\bdata-(?:target|count|to|end|number)\s*=\s*[\"']\s*"
                     r"(\d[\d,]*(?:\.\d+)?)\s*[\"'][^>]*>)\s*0?\s*(</\2\s*>)", re.I)
# An Excel workbook is an OLE2 compound file, and decoded as text it is noise with none of its
# figures in it: Chicago Booth publishes its employment statistics as one (INC-0158).
OLE2 = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


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


# A grade range names school years, never a figure. ACT's page stopped giving an attempt
# limit, and its "Students & Parents K-12" menu link went on confirming the 12 the record
# still claimed (INC-0172).
GRADES = re.compile(r"(?:\bPre-?)?\bK\s?[-\u2013]\s?\d{1,2}\b")


def numbers(text, words=False):
    text = GRADES.sub(" ", str(text or ""))
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
    """The readable text of a fetched page, PDF or Excel workbook."""
    if body[:5] == b"%PDF-" or "pdf" in ctype:
        try:
            from pdfminer.high_level import extract_text
        except ImportError:
            raise RuntimeError("a PDF, and pdfminer.six is not installed")
        return extract_text(io.BytesIO(body))
    if body[:8] == OLE2 or "excel" in ctype:
        return xls_text(body)
    # Any other binary file decoded as text reads as noise with none of its figures in it,
    # which the report would show as a page missing every figure, so it is unreadable instead.
    if b"\x00" in body[:4096]:
        raise RuntimeError("a binary file (%s) this check cannot read" % (ctype.split(";")[0] or "no content type"))
    t = body.decode("utf-8", errors="replace")
    # A comment is markup no reader sees. Kept, its text read as printed, and Arizona
    # State's 43 percent women was confirmed from a row the school had commented out
    # (INC-0152). It goes first, because a comment can hold tags and scripts.
    t = re.sub(r"<!--[\s\S]*?-->", " ", t)
    t = re.sub(r"<(script|style|noscript)[\s\S]*?</\1>", " ", t, flags=re.I)
    t = COUNTER.sub(lambda m: m.group(1) + m.group(3) + m.group(4), t)
    # An image's alt text is the words a page gives for the image, read out in its place to
    # anyone who cannot see it. Berkeley Haas and Pitt Katz draw their figures as images and
    # write the figures into the alt text, so it is read as part of the page (INC-0154).
    # An image the markup hides is shown to nobody, so its alt text is not read.
    hidden = re.compile(r"\shidden(?:[\s=>/]|$)|display\s*:\s*none|visibility\s*:\s*hidden", re.I)
    t = re.sub(r"<img\b[^>]*?\balt\s*=\s*(\"[^\"]*\"|'[^']*')[^>]*>",
               lambda m: " " if hidden.search(m.group(0)) else " %s " % m.group(1)[1:-1], t, flags=re.I)
    return markup_text(t)


class _Text(html.parser.HTMLParser):
    """The text of a page's markup, with a space where each tag was."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_data(self, data):
        self.out.append(data)

    def handle_starttag(self, tag, attrs):
        self.out.append(" ")

    def handle_endtag(self, tag):
        self.out.append(" ")


def markup_text(t):
    """A tag ends at the first > outside its quotes, which a pattern cannot see. ETS keeps a
    copy of each text block in a data attribute, markup and all, with the markup's > left
    raw; <[^>]+> ended the tag there and read the rest of the attribute as page text, and an
    element id's 5 confirmed GRE's five-year score validity on a page that never states it
    (INC-0173). A parser keeps a quoted attribute whole."""
    p = _Text()
    p.feed(t)
    p.close()
    return "".join(p.out)


def cell_text(v, fmt):
    """A number as a workbook cell shows it through its format: Booth's 0.8782771535580525
    under 0.0% is 87.8%, and 175000 under "$"#,##0 is 175,000."""
    part = re.sub(r'"[^"]*"|\[[^\]]*\]|\\.', "", str(fmt or "")).split(";")[0]
    if not re.search(r"[0#?]", part):
        return "%d" % v if float(v).is_integer() else "%.10g" % v
    places = re.search(r"\.([0#?]+)", part)
    pct = "%" in part
    shown = ("{:,.%df}" if "," in part else "{:.%df}") % (len(places.group(1)) if places else 0)
    return shown.format(v * 100 if pct else v) + ("%" if pct else "")


def xls_text(body):
    """An Excel workbook as its cells show it, a row to a line."""
    try:
        import xlrd
    except ImportError:
        raise RuntimeError("an Excel workbook, and xlrd is not installed")
    book = xlrd.open_workbook(file_contents=body, formatting_info=True)
    lines = []
    for sheet in book.sheets():
        for r in range(sheet.nrows):
            cells = []
            for cell in sheet.row(r):
                if cell.ctype == xlrd.XL_CELL_DATE:
                    d = xlrd.xldate_as_datetime(cell.value, book.datemode)
                    cells.append("%s %d, %d" % (d.strftime("%B"), d.day, d.year))
                elif cell.ctype == xlrd.XL_CELL_NUMBER:
                    f = book.format_map.get(book.xf_list[cell.xf_index].format_key)
                    cells.append(cell_text(cell.value, f.format_str if f else ""))
                elif cell.ctype == xlrd.XL_CELL_TEXT and cell.value.strip():
                    cells.append(cell.value.strip())
            if cells:
                lines.append(" ".join(cells))
    return "\n".join(lines)


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


RETRY_WAIT = 5


def plain_read(url):
    """The body and content type of a plain read of url."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45, context=ssl_context()) as r:
        return r.read(), r.headers.get("Content-Type", "").lower()


def script_challenge(body):
    """True when a read is Imperva's script challenge: a short page whose only content is a
    script from /_Incapsula_Resource."""
    return len(body) < CHALLENGE_MAX and b"_Incapsula_Resource" in body


def fetch(url, cache, rendered=False):
    key = hashlib.sha1((("render:" if rendered else "") + url).encode()).hexdigest()
    if cache:
        hit = cache / (key + ".txt")
        if hit.exists():
            return hit.read_text(encoding="utf-8")
    if rendered:
        text = render(url)
        # Imperva answers mba.com with its challenge on some reads and not others (INC-0156),
        # and a read a few seconds later is often the page: two of three reads of the GMAT
        # fee table were on September 27, 2026. One more read, then the challenge stands.
        if challenged(re.sub(r"\s+", " ", text)):
            time.sleep(RETRY_WAIT)
            text = render(url)
    else:
        body, ctype = plain_read(url)
        # Imperva's script challenge is one script tag and no words, so it reads as an empty
        # page rather than as a challenge: mba.com served it for GMAC's policies PDF on some
        # reads and the PDF on others (INC-0175). One more read, then the challenge stands.
        if script_challenge(body):
            time.sleep(RETRY_WAIT)
            body, ctype = plain_read(url)
            if script_challenge(body):
                CHALLENGED.add(url)
                return ""
        text = to_text(body, ctype)
    text = unglue(re.sub(r"\s+", " ", text))
    # A challenge says nothing about the page, so it is neither returned nor cached; the
    # caller sees an empty read, tries the browser, and reports the source as unreadable.
    if challenged(text):
        CHALLENGED.add(url)
        return ""
    # A read too short to be evidence is returned, for the caller to report, but not kept:
    # a one-character read of GMAC's policies PDF, cached, made every later run report the
    # PDF unreadable from the cache rather than from the site (INC-0175).
    if cache and len(text) >= MIN_TEXT:
        (cache / (key + ".txt")).write_text(text, encoding="utf-8")
    return text


# A fact's number words are its numbers, as a page's are: the LSAT guide's "roughly three
# weeks" went unchecked because only the page side read words (INC-0177). The school library
# is read without them, since its text is a figure's description rather than the figure.
FACT_WORDS = [True]


def printed(fact):
    """The numbers a fact expects its source to print, leaving out the ones it derives."""
    want = set().union(*(numbers(fact.get(k), FACT_WORDS[0]) for k in FIELDS))
    if isinstance(fact.get("v"), (int, float)):
        want.add(norm("%g" % fact["v"]))
    return want - set(fact.get("derived") or {})


def school_numbers(fact):
    """The numbers a school figure puts to its source: its value and every number in its
    text and stat, as --schools reads them, leaving out the ones it derives."""
    want = set().union(*(numbers(fact.get(k)) for k in ("text", "stat")))
    if isinstance(fact.get("v"), (int, float)):
        want.add(norm("%g" % fact["v"]))
    return want - set(fact.get("derived") or {})


def pages(fact):
    """Every page a fact is read against: its url, and for a figure worked from two pages,
    the ones in also_urls."""
    return [fact["url"]] + [u for u in (fact.get("also_urls") or []) if u]


def load_triage(path=TRIAGE):
    """data/source_triage.json's entries by figure key ('slug.profile.field')."""
    if not path.exists():
        return {}
    return {e["key"]: e for e in json.loads(path.read_text()).get("entries", [])}


def triaged(key, fact, miss, triage):
    """The triage entry that covers a flagged figure, or None. It covers the figure only
    while the value is the one a person read and every number the check misses is one they
    recorded, so a figure that changes, or starts missing another number, is new again."""
    e = triage.get(key)
    if not e or not isinstance(fact.get("v"), (int, float)) or e.get("v") != fact["v"]:
        return None
    return e if {n for n, _ in miss} <= {norm(str(n)) for n in e.get("missing") or []} else None


def check(fact, source_nums):
    """The numbers in a fact that its source does not print, as (number, why)."""
    derived = fact.get("derived") or {}
    want = set().union(*(numbers(fact.get(k), FACT_WORDS[0]) for k in FIELDS))
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
# Figures that are counts, scores or lengths of time, which a percentage can never be. A class
# profile prints "class" in nearly every heading, so Arizona State's old class size of 47 was
# found beside its label in "Class composition ... Business 47%" after the page had changed it
# to 45 (INC-0182).
NOT_PERCENT = {"class_size", "gmat_focus", "gmat_classic", "gre_quant", "gre_verbal", "gpa", "work_exp_years"}


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
        if field in NOT_PERCENT and re.match(r"\s*(?:%|percent\b)", text[m.end():m.end() + 9], re.I):
            continue
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


# How far from a label a figure is looked for on a page that shows none of the figures cited
# to it: a few words either side, the gap between a label and its figure in a table row.
BESIDE = 40


def beside_labels(field, text):
    """The numbers a page prints next to a school figure's label that could be that figure,
    nearest first: in the field's range, and not a year. A page that prints none of its
    figures but these has moved on or been revised: Kelley's printed "Average GPA 3.38"
    where the library had the Class of 2027's 3.48 (INC-0158)."""
    from validate_schools import RANGES
    label, span = LABELS.get(field), RANGES.get(field)
    if not label or not span or not text:
        return []
    near = []
    for m in re.finditer(label, text, re.I):
        after = [x for x in NUM.finditer(text, m.end(), m.end() + BESIDE + 12)
                 if x.start() <= m.end() + BESIDE][:1]
        before = list(NUM.finditer(text, max(0, m.start() - BESIDE), m.start()))[-1:]
        for gap, x in [(x.start() - m.end(), x) for x in after] + [(m.start() - x.end(), x) for x in before]:
            n = norm(x.group(0))
            if n != "0" and not re.fullmatch(r"(?:19|20)\d\d", n) and span[0] <= float(n) <= span[1]:
                near.append((gap, n))
    out = []
    for _, n in sorted(near, key=lambda g: g[0]):
        if n not in out:
            out.append(n)
    return out


# A number found on the page is not the fact found, for an exam fact either. GMAC's retake
# article confirmed the GMAT's five-year score validity with "up to 5 times", and its score
# release article confirmed "3 to 5 days" with the 3 of "0 out of 3 found this helpful"
# (INC-0174), after a K-12 menu link had confirmed an ACT attempt cap (INC-0172). So each
# number of an exam fact must also sit near a word of the fact's own, or, for a figure with
# no text, near the word its field is about. A table prints its labels once, at the head of
# a column, so a number with another number beside it is read as a cell and needs no word.
WORDS_NEAR = 160
FIELD_WORDS = {"validity_years": r"valid|reportable|expire"}
# Words every page about an exam uses, which say nothing about which fact a passage is about.
COMMON = set("""about after again their there where which while would could should these those other
every within before during through between under above below among being having doing years
students student tests exams score scores taken takes taking""".split())


def fact_words(where, fact):
    """What an exam fact is about, as a pattern: its own words of five letters or more, less
    the common ones, or its field's words for a figure with no text; None when it has none."""
    words = {w.lower() for w in re.findall(r"[A-Za-z]{5,}", " ".join(str(fact.get(k) or "") for k in FIELDS))}
    words -= COMMON
    if words:
        return r"\b(?:%s)" % "|".join(sorted(map(re.escape, words)))
    return FIELD_WORDS.get(re.sub(r"\[\d+\]", "", where).split(".")[-1])


# A number that is only part of a date is the date's, not a figure: the 3 of 3/3/2027 in
# LSAC's table of test dates would have confirmed the LSAT guide's "three weeks" (INC-0177).
DATE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b")


def in_table(text, start, end):
    """True when the number at text[start:end] has another number beside it, as a table's
    cells do: "160 82 50", or "150 36.56% 36.6%"."""
    return bool(re.search(r"\d[%)]?[\s|,;:]*$", text[max(0, start - 16):start])
                or re.match(r"[%)]?[\s|,;:]*\(?\$?\d", text[end:end + 16]))


def away_from_words(where, fact, texts):
    """The numbers of an exam fact that its pages print only away from every word of the
    fact and outside any table, as (number, why). A number printed nowhere is check()'s to
    report, and a derived one is judged by its inputs."""
    label = fact_words(where, fact)
    if not label:
        return []
    out = []
    for n in sorted(printed(fact), key=float):
        forms = [w for w, d in WORDS.items() if d == n]
        seen = beside = False
        for text in texts:
            text = GRADES.sub(" ", text)
            spots = [m.span() for m in NUM.finditer(text) if norm(m.group(0)) == n]
            if forms:
                spots += [m.span() for m in re.finditer(r"\b(?:%s)\b" % "|".join(forms), text, re.I)]
            dates = [m.span() for m in DATE.finditer(text)]
            for a, b in spots:
                seen = True
                if any(x <= a and b <= y for x, y in dates):
                    continue
                if in_table(text, a, b) or re.search(label, text[max(0, a - WORDS_NEAR): b + WORDS_NEAR], re.I):
                    beside = True
                    break
            if beside:
                break
        if seen and not beside:
            out.append((n, "printed only away from every word of the fact, as in a menu, a counter or "
                           "another passage"))
    return out


def blank_pages(cited, sources):
    """The pages that print none of the figures cited to them, when two or more are. Every
    figure on such a page would be reported as missing, which says nothing about the
    figures, so the page is reported once instead. A figure is read the way the findings
    read it, against every page it names and only when all of them were read: mba.com's
    payment page prints no fee until a country is chosen, and the GMAT's fees are read from
    the table it loads, named in also_urls (INC-0161)."""
    by_url = {}
    for f in cited:
        if all(u in sources for u in pages(f)):
            by_url.setdefault(f["url"], []).append(f)
    # Years do not count as evidence: "Class of 2027" is in the prose of a class profile
    # whose statistics never rendered.
    year = re.compile(r"(19|20)\d\d")
    evidence = lambda f: {n for n in printed(f) if not year.fullmatch(n)}
    blank = set()
    for u, fs in by_url.items():
        counted = [f for f in fs if evidence(f)]
        if len(counted) >= 2 and not any(evidence(f) & set().union(*(sources[x] for x in pages(f)))
                                         for f in counted):
            blank.add(u)
    return blank


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


# A fact with no number gives the checks above nothing to look for, and 20 of the 113 exam
# facts have none: the GMAT's delivery line kept "appointments available year round (no fixed
# testing windows)" after its page stopped saying so, and the check counted it as checked
# (INC-0180). Such a fact is read by its words instead: every content word must be on one of
# its pages, a plural or another tense of it counting, and a word that is not is reported the
# way a missing number is. It cannot tell a paraphrase from a change, so a fact is worded the
# way its page words it; and it cannot see a "not", so it finds a page that stopped saying
# something rather than proving what the page says.
STOPWORDS = frozenset("""
a an the of and or to for by in on at vs is are be been being it its with as from that this these those
can cannot not no nor but their your you they them which who whom whose has have had was were will would
may might must should could do does did than then so such also into onto over under about after before
between both each either neither other any all some most more much many few own same only just very
there here where when while what how why if because per via
says said notes describes lists calls explains states adds""".split())
# When a count was made is ours, not the page's: "counted on September 26, 2026".
COUNTED = re.compile(r"\bcounted(?: on)? (?:[A-Z][a-z]+ \d{1,2}, )?\d{4}")


def stem(word):
    """A word less its ending, so "decided" meets "decide" and "superscoring" meets
    "superscore"."""
    w = word.lower()
    for end, put in (("ies", "y"), ("ied", "y"), ("sses", "ss"), ("ss", "ss"), ("ing", ""), ("ed", ""),
                     ("es", ""), ("s", ""), ("ly", "")):
        if w.endswith(end) and len(w) - len(end) >= 3:
            w = w[:len(w) - len(end)] + put
            break
    return w[:-1] if w.endswith("e") and len(w) >= 4 else w


def page_stems(text):
    """Every word a page prints, stemmed; a hyphenated word also counts written solid, as
    GMAC writes "on-screen" on one page and "onscreen" on another."""
    low = text.lower()
    words = re.findall(r"[a-z]+", low) + [w.replace("-", "") for w in re.findall(r"[a-z]+(?:-[a-z]+)+", low)]
    return {stem(w) for w in words}


def unseen_words(fact, texts):
    """The content words of a fact that none of its pages prints, in the fact's order
    (INC-0180). A hyphenated word is found written solid or as its parts."""
    text = " ".join(str(fact.get(k) or "") for k in FIELDS)
    if any(str(v).startswith("count:") for v in (fact.get("derived") or {}).values()):
        text = COUNTED.sub(" ", text)
    seen = set().union(*(page_stems(t) for t in texts)) if texts else set()
    out = []
    for term in re.findall(r"[a-z]+(?:-[a-z]+)*", text.lower()):
        if term in STOPWORDS or len(term.replace("-", "")) < 3 or term in out:
            continue
        parts = [p for p in term.split("-") if p not in STOPWORDS and len(p) >= 3]
        if stem(term.replace("-", "")) not in seen and not (parts and all(stem(p) in seen for p in parts)):
            out.append(term)
    return out


def _selfcheck():
    """INC-0140: a year range reads as both years however the page punctuates it.
    INC-0150: a school figure is found only beside its label, in a passage about its program.
    INC-0152: a figure only inside an HTML comment is not printed; the same figure outside one is.
    INC-0154: a figure an image carries in its alt text is printed.
    INC-0156: a bot challenge page is not read as the page it was sent for.
    INC-0158: figures glued to their labels, in a counter's attribute or in a workbook cell are
    read as shown, and a page that moved on shows its new figures beside the labels.
    INC-0172: a grade range such as K-12 is not a figure.
    INC-0173: text inside a quoted attribute is not page text, whatever markup it holds.
    INC-0174: an exam fact's number counts only near a word of the fact's, or in a table.
    INC-0175: a read too short to be evidence is not cached, and Imperva's script challenge is
    read once more and then reported as a challenge.
    INC-0177: a fact's number words are numbers, and a number only in a date is no figure.
    INC-0180: a fact with no number is read by its words, in any of their forms."""
    # INC-0180: the GMAT's old delivery line against the register page it cited, as the page
    # read on September 27, 2026, and the line that replaced it against the page it cites now.
    register = ("Get started in 4 easy steps Create mba.com Account. Pick Online or Test Center. On your My Account "
                "page, click the Register button and choose how you want to test. 2. Test on your terms. Choose an "
                "online or test center appointment and schedule the GMAT around your application timeline. Your "
                "score remains valid for five years, giving you flexibility to apply when the time is right.")
    online = ("Taking the Exam at a Test Center Taking the Exam Online The GMAT exam delivered online is available "
              "in most locations, with the exception of: Mainland China, Cuba, Iran, North Korea, and Sudan due to "
              "regulatory and local data privacy rules.")
    ets = ("ETS Law schools that accept GRE General Test scores for admission to their JD programs. United States "
           "Albany Law School American University China Peking University")
    for fact, text, want in (
            ({"text": "At test centers or online, with appointments available year round (no fixed testing windows)"},
             register, ["available", "round", "fixed", "windows"]),
            ({"text": "At test centers and online; the exam delivered online is available in most locations, "
                      "with the exception of Mainland China, Cuba, Iran, North Korea and Sudan"}, online, []),
            ({"text": "Whether science is administered is decided at the contract level"},
             "The choice will continue to be at the contract level. Clients will decide whether to have science "
             "administered", []),
            ({"text": "ACT superscores average the best section scores"},
             "The ACT Superscore is the average of a student's best scores from each section", []),
            ({"text": "An on-screen calculator is available"}, "you have access to an onscreen calculator, available", []),
            ({"text": "ETS lists the law schools that accept GRE General Test scores for admission to their JD "
                      "programs: 128 in the United States and 1 in China, counted on September 26, 2026",
              "derived": {"128": "count: the schools", "1": "count: the schools", "26": "count: the date",
                          "2026": "count: the year"}}, ets, [])):
        got = unseen_words(fact, [text])
        if got != want:
            sys.exit("check_sources: unseen_words(%r) gave %s, not %s (INC-0180)" % (fact["text"][:50], got, want))
    # INC-0177: the LSAT guide's "roughly three weeks" against LSAC's table of dates, as the
    # page prints it: the only 3s are in dates, so the fact is flagged, not confirmed.
    lsac = ("Administration Primary test dates LSAT Argumentative Writing opens Registration deadline Scheduling "
            "opens Score release January 2027 1/13/2027 1/14/2027 1/15/2027 1/16/2027 1/5/2027 12/1/2026 12/22/2026 "
            "2/3/2027 Register for the January 2027 February 2027 2/12/2027 2/13/2027 2/4/2027 12/29/2026 1/26/2027 "
            "3/3/2027 Register for the February 2027")
    weeks = {"text": "Scores are released on published dates roughly three weeks after each administration"}
    if "3" not in printed(weeks) or [n for n, _ in away_from_words("score_release", weeks, [lsac])] != ["3"]:
        sys.exit("check_sources: a number written as a word, found only in dates, passed (INC-0177)")
    if [n for n, _ in away_from_words("score_release", weeks, ["Processing can take up to three weeks "
                                                               "after each administration's release is published"])]:
        sys.exit("check_sources: a number word beside the fact's words was not found (INC-0177)")
    # INC-0175: Imperva's script challenge, as mba.com served it for GMAC's policies PDF.
    script = (b'<html>\r\n<head>\r\n<META NAME="robots" CONTENT="noindex,nofollow">\r\n<script src="/_Incapsula_'
              b'Resource?SWJIYLWA=5074a744e2e3d891814e9a2dace20bd4">\r\n</script>\r\n<body>\r\n</body></html>')
    served = b"<html><body><p>" + b"The GMAT exam policies and procedures. " * 20 + b"</p></body></html>"
    real_read, real_wait = globals()["plain_read"], globals()["RETRY_WAIT"]
    globals()["RETRY_WAIT"] = 0
    try:
        for reads, want in (([script, served], True), ([script, script], False)):
            queue = list(reads)
            globals()["plain_read"] = lambda url: (queue.pop(0), "text/html")
            CHALLENGED.discard("https://example.org/policies.pdf")
            got = fetch("https://example.org/policies.pdf", None)
            if (len(got) >= MIN_TEXT) != want or ("https://example.org/policies.pdf" in CHALLENGED) == want:
                sys.exit("check_sources: Imperva's script challenge read as %r (INC-0175)" % got[:60])
        CHALLENGED.discard("https://example.org/policies.pdf")
    finally:
        globals()["plain_read"], globals()["RETRY_WAIT"] = real_read, real_wait
    # INC-0175: a short read is reported by the caller and fetched again next run, not kept.
    import tempfile
    real = globals()["render"]
    globals()["render"] = lambda url: "x"
    try:
        with tempfile.TemporaryDirectory() as d:
            fetch("https://example.org/short", pathlib.Path(d), rendered=True)
            if any(pathlib.Path(d).iterdir()):
                sys.exit("check_sources: a read too short to be evidence was cached (INC-0175)")
    finally:
        globals()["render"] = real
    # INC-0173: a quoted attribute is part of its tag, however much markup it holds.
    layer = ('<div data-cmp-data-layer="{&#34;text-5ae0eb3b6b&#34;:{&#34;xdm:text&#34;:&#34;&lt;p style=\\&#34;'
             'text-align: center;\\&#34;>Scores last 7 years&lt;/p>&#34;}}" id="text-5ae0eb3b6b" class="cmp-text">'
             '<p>The GRE General Test</p></div>')
    got = to_text(layer.encode(), "text/html")
    if "The GRE General Test" not in got or {"5", "7"} & numbers(got, True):
        sys.exit("check_sources: text inside a quoted attribute was read as page text (INC-0173): %r" % got)
    # INC-0174: the retake article's "5 times" and a helpfulness counter's 3 confirm nothing;
    # the same numbers beside the fact's words, or as cells of a table, do.
    retake = ("How Many Times Can I Take the GMAT? You may take the GMAT exam up to 5 times within a rolling "
              "12-month period. This limit includes: online and test center exams combined")
    valid = "GMAT scores are valid for five (5) years and available for reporting for up to 10 years."
    lsat = "An LSAT result is reportable for up to five testing years after the testing year in which the score was earned."
    release = ("Your official score report should be available within five (5) days. Although not typical, it can "
               "take up to 20 days for your exam to be scored Scores cannot be expedited. Related to GMAT Score "
               "Was this article helpful? Yes No 0 out of 3 found this helpful Have more questions? Submit a request")
    # ETS's Table 1B as its PDF reads: the scores down one column, then each measure's
    # percentiles down the next, so the cells sit far from the words that head them.
    table = ("Scaled Score Verbal Reasoning Quantitative Reasoning " + " ".join(map(str, range(170, 129, -1))) +
             " 99 99 98 97 96 95 93 90 88 85 82 79 76 72 68 64 59 54 48 43 39 34 30 27 24 21 18 16 14 11 10 8 6 5"
             " 4 3 2 2 1 1 89 85 80 75 72 67 63 60 57 53 50 47 45 42 39 37 34 31 29 26 23 21 19 16 14 12 10 9 7 6"
             " 5 4 3 2 2 1 1 1")
    for where, fact, text, want in (
            ("validity_years", {"v": 5}, retake, ["5"]),
            ("validity_years", {"v": 5}, valid, []),
            ("validity_years", {"v": 5}, lsat, []),
            ("score_release", {"text": "Official Score Report is typically available in your mba.com account within "
                                       "3 to 5 days (up to 20 days in some cases)"}, release, ["3"]),
            ("score_release", {"text": "Your official score report should be available within 5 days; although not "
                                       "typical, it can take up to 20 days"}, release, []),
            ("key_facts[4]", {"text": "160 is the 82nd percentile in Verbal Reasoning and the 50th in Quantitative "
                                      "Reasoning"}, table, [])):
        got = [n for n, _ in away_from_words(where, fact, [text])]
        if got != want:
            sys.exit("check_sources: away_from_words(%s, %r) gave %s, not %s (INC-0174)" % (where, fact, got, want))
    # INC-0172: a grade range in a menu confirms nothing; the same number as a figure does.
    if "12" in numbers("Students & Parents K-12 Workforce Higher Ed", True):
        sys.exit("check_sources: the 12 of K-12 was read as a figure (INC-0172)")
    if "12" not in numbers("can be taken up to 12 times in total", True):
        sys.exit("check_sources: a plain 12 was not read (INC-0172)")
    glued = unglue("CLASS PROFILEAVERAGE AGE32ENROLLED IN DUAL DEGREE22%INTERNATIONAL STUDENTS39%AVERAGE YEARS "
                   "WORK EXPERIENCE8AVERAGE UNDERGRAD GPA3.45AN EXCELLENT EDUCATION")
    if not {"39", "8", "3.45"} <= numbers(glued, True):
        sys.exit("check_sources: figures glued to their labels were not read: %s" % sorted(numbers(glued, True)))
    if "1" in numbers(unglue("sponsors an H1B visa"), True):
        sys.exit("check_sources: a code such as H1B was read as a number")
    counter = ('<li class="stat"><span class="stat-number countup" data-target="3.47" data-decimals="2">0</span>'
               '<div class="stat-label">Average Undergraduate GPA</div></li>')
    if "3.47" not in numbers(to_text(counter.encode(), "text/html")):
        sys.exit("check_sources: a counter's final value was not read")
    for v, fmt, want in ((0.8782771535580525, "0.0%", "87.8%"), (0.42, "0%", "42%"),
                         (175000.0, '"$"#,##0', "175,000"), (534.0, "General", "534")):
        if cell_text(v, fmt) != want:
            sys.exit("check_sources: a workbook cell of %r under %r reads %r, not %r" % (v, fmt, cell_text(v, fmt), want))
    try:
        to_text(b"PK\x03\x04\x14\x00\x06\x00", "application/octet-stream")
        sys.exit("check_sources: a binary file was read as text")
    except RuntimeError:
        pass
    # INC-0161: a figure is judged blank against every page it names, and only when all were read.
    pay, table = "https://example.org/pay", "https://example.org/table"
    two = [{"url": pay, "also_urls": [table], "text": "US$275 at a test center, US$300 online"},
           {"url": pay, "also_urls": [table], "text": "an additional score report costs US$35"}]
    for srcs, want in (({pay: {"4", "10"}, table: {"275", "300", "35"}}, set()),
                       ({pay: {"4", "10"}}, set()),
                       ({pay: {"4", "10"}, table: {"7"}}, {pay})):
        if blank_pages(two, srcs) != want:
            sys.exit("check_sources: blank_pages with %s read gave %s, not %s"
                     % (sorted(srcs), blank_pages(two, srcs), want))
    moved = ("Discover the MBA Class Profile of 2028 Class size 57 Women 35% International 39% Average years of "
             "full-time employment experience 6 Average GPA 3.38 Average GMAT 618* Average GRE Quantitative Score 161")
    counted = "3.47 Average Undergraduate GPA 1.81 Average Years of Work Experience"
    for field, text, want in (("gpa", moved, "3.38"), ("gmat_focus", moved, "618"), ("class_size", moved, "57"),
                              ("work_exp_years", moved, "6"), ("gpa", counted, "3.47"),
                              ("work_exp_years", counted, "1.81"),
                              ("gpa", "Students come from 22 countries and every industry.", None)):
        got = beside_labels(field, text)
        if (got[:1] or [None])[0] != want:
            sys.exit("check_sources: beside_labels(%s) on %r gave %r, not %r" % (field, text[:40], got, want))
    imperva = ("www.mba.com - Additional security check is required Why am I seeing this page? The website you "
               "are visiting is protected and accelerated by Imperva. Your computer may have been infected by malware.")
    cloudflare = "Just a moment... Enable JavaScript and cookies to continue"
    verifying = ("business.columbia.edu Performing security verification This website uses a security service to "
                 "protect against malicious bots. This page is displayed while the website verifies you are not a bot.")
    unusual = ("Bloomberg Need help? Contact us We've detected unusual activity from your computer network To continue, "
               "please click the box below to let us know you're not a robot. Why did this happen? " + "x" * 600)
    page = "Score reports. " * 250 + "Every account has an additional security check is required step at sign in."
    for text, want in ((imperva, True), (cloudflare, True), (verifying, True), (unusual, True), (page, False)):
        if challenged(text) != want:
            sys.exit("check_sources: challenged(%r) should be %s" % (text[:50], want))
    img = '<h3>GMAT Focus</h3><img src="GMAT%20Focus-3.svg" width="400" alt="637 to 725 middle 80% range; 675 median">'
    if "675" not in numbers(to_text(img.encode(), "text/html")):
        sys.exit("check_sources: a figure in an image's alt text was not read as printed")
    for tag in ('<img src="a.svg" style="display: none" alt="9.94 hidden">', '<img hidden src="a.svg" alt="9.94 hidden">'):
        if "9.94" in numbers(to_text(tag.encode(), "text/html")):
            sys.exit("check_sources: a hidden image's alt text was read as printed: %s" % tag)
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
            ("work_exp_years", {"v": 5.7, "derived": {"5.7": "68 months / 12"}}, "Average 68 months worked", None),
            # INC-0182: a percentage never confirms a head count, however close its label.
            ("class_size", {"v": 47}, "Size of entering class 45 Class composition International 33% "
                                      "Undergraduate major Business 47% Engineering 7%", "not beside"),
            ("class_size", {"v": 47}, "Size of entering class 47 Class composition International 32%", None),
            ("intl_pct", {"v": 33}, "Class composition International 33% Undergraduate major Business 47%", None)):
        got = beside_label(field, fact, text)
        if (want is None) != (got is None) or (want and want not in got[1]):
            sys.exit("check_sources: beside_label(%s, %r) on %r gave %r" % (field, fact, text[:60], got))
    # INC-0154: a triage entry covers a finding only for the value and numbers it recorded.
    entry = {"x.profile.gpa": {"key": "x.profile.gpa", "v": 3.67, "missing": ["3.67", "3.4", "3.91"]}}
    for fact, miss, want in (({"v": 3.67}, [("3.67", ""), ("3.91", "")], True),
                             ({"v": 3.68}, [("3.68", "")], False),
                             ({"v": 3.67}, [("3.67", ""), ("80", "")], False)):
        if (triaged("x.profile.gpa", fact, miss, entry) is not None) != want:
            sys.exit("check_sources: triage of %r missing %r should be %s" % (fact, miss, want))


def main(argv):
    _selfcheck()
    cache = None
    if "--cache" in argv:
        cache = pathlib.Path(argv[argv.index("--cache") + 1])
        cache.mkdir(parents=True, exist_ok=True)
    triage = {}
    if "--schools" in argv:
        records = [json.loads(p.read_text()) for p in sorted(SCHOOLS.glob("*.json"))]
        FIELDS[:] = ["text", "stat"]
        FACT_WORDS[0] = False
        triage = load_triage()
    else:
        records = json.loads(EXAMS.read_text())
    todo = facts(records)
    dataset = [t for t in todo if "scorecard" in str(t[2].get("src", "")).lower()]
    todo = [t for t in todo if t not in dataset]
    sources, unread, periods, texts, served = {}, {}, {}, {}, {}
    today = datetime.date.fromisoformat(os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat())
    for url in sorted({u for _, _, f in todo for u in pages(f)}):
        try:
            refused = None
            try:
                text = fetch(url, cache)
            except urllib.error.HTTPError as e:
                if "--render" not in argv or e.code not in REFUSED:
                    raise
                refused = e.code
                try:
                    text = fetch(url, cache, rendered=True)
                except Exception as e2:
                    raise RuntimeError("HTTP %d, and the browser could not read it either (%s)"
                                       % (e.code, str(e2).splitlines()[0][:120]))
            # A page that builds itself with JavaScript reads as nearly empty, or as
            # navigation without its figures, until a browser runs it. If the browser
            # cannot load it either, the static text is still evidence when there is
            # enough of it, so it is kept rather than thrown away.
            cited = [(w, f) for _, w, f in todo if url in pages(f)]
            misses = lambda t: sum(len(check(f, numbers(t, True)) or
                                       ([] if "--schools" in argv else away_from_words(w, f, [t]) or
                                        ([] if printed(f) else unseen_words(f, [t]))))
                                   for w, f in cited)
            if "--render" in argv and refused is None and (len(text) < MIN_TEXT or misses(text)):
                try:
                    shown = fetch(url, cache, rendered=True)
                    # The browser's read replaces the page as served only when it is at
                    # least as good a witness: a render that comes back as a challenge
                    # page, or shorter, must not hide figures the served page printed.
                    if len(shown) >= MIN_TEXT and (len(text) < MIN_TEXT or misses(shown) <= misses(text)):
                        served[url], text = text, shown
                except Exception as e:
                    print("render failed for %s, using the page as served (%s)"
                          % (url, str(e).splitlines()[0][:120]))
            if url in CHALLENGED and len(text) < MIN_TEXT:
                raise RuntimeError("%sthe site answered with a bot challenge, not the page"
                                   % ("HTTP %d to a script, and in the browser " % refused if refused else ""))
            if len(text) < MIN_TEXT:
                raise RuntimeError("only %d characters of text, a bot challenge or a page "
                                   "built by JavaScript" % len(text))
            sources[url] = numbers(text, words=True)
            texts[url] = text
            periods[url] = ended_periods(text, today)
        except Exception as e:
            unread[url] = "%s: %s" % (type(e).__name__, e)
    blank = blank_pages([f for _, _, f in todo], sources)
    bad, worded, by_words, worth, judged, read_ok, flagged = 0, 0, 0, [], [], set(), set()
    for slug, where, f in todo:
        if any(u not in sources for u in pages(f)) or f["url"] in blank:
            continue
        key = "%s.%s" % (slug, where)
        read_ok.add(key)
        # A figure worked from two pages is read against both, as one source.
        miss = check(f, set().union(*(sources[u] for u in pages(f))))
        if "--schools" not in argv and not miss:
            miss = away_from_words(where, f, [texts[u] for u in pages(f)])
        # A fact with no number to look for is read by its words, against both reads of each
        # page, since a browser leaves out what a closed accordion holds (INC-0180).
        if "--schools" not in argv and not printed(f):
            by_words += 1
            gone = unseen_words(f, [texts[u] + " " + served.get(u, "") for u in pages(f)])
            worded += bool(gone)
            miss = miss + [(w, "not on the page; with no number to look for, the fact is read by its words")
                           for w in gone]
        if "--schools" in argv and where.startswith("profile.") and not miss:
            got = beside_label(where.split(".", 1)[1], f, " ".join(texts.get(u, "") for u in pages(f)))
            if got and got[0] == "none":
                miss = [(norm("%g" % f["v"]), got[1])]
            elif got:
                worth.append("%s.%s  %s\n    %s: %s" % (slug, where, f["url"], norm("%g" % f["v"]), got[1]))
        if miss:
            flagged.add(key)
            entry = triaged(key, f, miss, triage)
            if entry:
                judged.append((key, f, entry))
                continue
            bad += 1
            print("%s.%s  %s" % (slug, where, f["url"]))
            print("    %s" % str(f.get("text") or f.get("v"))[:220])
            for n, why in miss:
                print("    %s: %s" % (n, why))
    # A page that shows none of its figures is a finding until a person has read it, because a
    # page whose every figure changed looks, to a check that looks for numbers, exactly like a
    # page that never loaded: Kelley's class profile had moved on to the Class of 2028 and was
    # reported as probably built by JavaScript (INC-0158). What the page prints beside each
    # figure's label says which it is, and a figure a person has read there is triaged.
    unseen = []
    for u in sorted(blank):
        rows = []
        for slug, where, f in todo:
            if f["url"] != u:
                continue
            key = "%s.%s" % (slug, where)
            read_ok.add(key)
            flagged.add(key)
            entry = triaged(key, f, check(f, set().union(*(sources.get(x, set()) for x in pages(f)))), triage)
            if entry:
                judged.append((key, f, entry))
            else:
                # Both reads, since a browser leaves out what a closed accordion holds and
                # Auburn's counters sit in one: the page as served showed them (INC-0158).
                rows.append((key, f, beside_labels(where.split(".", 1)[-1], texts[u] + " " + served.get(u, ""))))
        if rows:
            unseen.append((u, rows))
    # Figures a person has read and found right where this check cannot see them. They are
    # listed so the list stays visible, and apart, so a new finding is never one of 30.
    if judged:
        print("\nTriaged: read by a person and found right where this check cannot read them "
              "(data/source_triage.json):")
        for key, f, e in judged:
            print("  %s  %s, checked %s: %s" % (key, norm("%g" % f["v"]), e.get("checked"), e.get("why")))
    # An entry whose figure was read and is no longer flagged is not needed: the page now
    # prints the figure, or the figure changed and validate_schools refuses the entry.
    spare = sorted(k for k in triage if k in read_ok and k not in flagged)
    for k in spare:
        print("triage entry no longer needed, the check now finds the figure: %s" % k)
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
    for url, rows in unseen:
        if sum(1 for _, _, near in rows if near) >= min(2, len(rows)):
            print("prints none of its %d figures, and other numbers beside their labels, so it has probably "
                  "moved on to a newer class or been revised: read it and update them: %s" % (len(rows), url))
        else:
            print("prints none of its %d figures and no number beside their labels: read it, since it may draw "
                  "them as images, build them with JavaScript the browser did not run, or no longer carry them: %s"
                  % (len(rows), url))
        for key, f, near in rows:
            shown = norm("%g" % f["v"]) if isinstance(f.get("v"), (int, float)) else str(f.get("text"))[:80]
            print("    %s  %s%s" % (key, shown, "; beside its label the page prints %s" % ", ".join(near[:3])
                                     if near else ""))
    for url, why in sorted(unread.items()):
        print("could not read %s (%s)" % (url, why))
    # A fact read by its words is counted as that, so a clean report never passes off a fact
    # with nothing to check as a fact checked (INC-0180).
    print("\n%d facts checked against %d sources%s; %d with a number their source does not "
          "print%s; %d resting on a page about a period that has ended; %d sources unreadable, "
          "%d showing none of their figures; %d worth reading beside another program's name%s%s"
          % (len(todo), len(sources), ", %d of them by their words for want of a number" % by_words if by_words else "",
             bad - worded, "; %d with no number and a word their source does not print" % worded if by_words else "",
             stale, len(unread), len(unseen), len(worth),
             "; %d triaged" % len(judged) if triage else "",
             "; %d dataset figures set aside" % len(dataset) if dataset else ""))
    return 1 if bad or stale or unseen else (2 if unread else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
