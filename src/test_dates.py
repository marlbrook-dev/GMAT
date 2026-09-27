"""The SAT, ACT and LSAT test dates, read from the pages their makers print them on.

    python3 src/test_dates.py --write   rebuild data/test_dates.json from the three pages
    python3 src/test_dates.py --check   re-read them and report any difference

The test date pages under /exams/<exam>/test-dates/ show every date a student plans around:
the test day, the registration deadline, the late and change deadlines, and when scores come
out. A wrong date costs a student a sitting, so nothing in the data file is typed: --write
parses each maker's own table, row by row under the header it expects, and refuses a row
whose dates do not run in order. A sentence the pages quote is kept only if the maker's page
prints it word for word.

Makers publish the next year's dates months ahead and sometimes move one, so the weekly
source job runs --check, which fails when a date, a row or a table no longer matches.
Exit codes: 0 in step, 1 different, 2 unreadable.
"""
import datetime
import html
import json
import pathlib
import re
import sys
import urllib.request

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
from check_sources import UA, ssl_context

OUT = ROOT / "data" / "test_dates.json"
SAT_URL = "https://satsuite.collegeboard.org/sat/dates-deadlines"
SAT_SCORES_URL = "https://satsuite.collegeboard.org/scores/score-release-dates"
ACT_URL = "https://www.act.org/content/act/en/products-and-services/the-act/registration/test-dates.html"
LSAT_URL = "https://www.lsac.org/LSATdates"

MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8,
          "sep": 9, "oct": 10, "nov": 11, "dec": 12}
# "Aug. 22, 2026", "Sept. 12, 2026", "March 6, 2027", "Sep 11, 2027", "August 14"
NAMED = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2})(?:,\s*(\d{4}))?\b")
NUMERIC = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b")

SAT_HEADER = ["SAT Test Date*", "Registration Deadline",
              "Deadline for Changes, Regular Cancellation, and Late Registration**"]
SAT_SCHOOL_HEADER = ["In-School Assessment", "Testing Window"]
SAT_SCORES_HEADER = ["Test Date", "Student Score Release", "Educator Score Release"]
ACT_HEADER = ["Test Date", "Registration Deadline (Late fee applies after this date)", "Late Deadline",
              "Photo Upload & Standby Deadline", "Paper Initial Score Release"]
LSAT_HEADER = ["Administration", "Primary test dates", "LSAT Argumentative Writing opens",
               "Registration deadline *", "Scheduling opens **", "Score release", ""]

# Sentences the pages quote, each kept only if its page prints it word for word.
QUOTES = {
    "sat": ["SAT Weekend deadlines expire at 11:59 p.m. ET, U.S.",
            "Late registration is available worldwide.",
            "Students taking SAT School Day or PSAT assessments do not need to register on their own."],
    "act": ["The ACT is offered 7 times per year at test centers across the United States.",
            "National test dates are for the United States, US territories, and Puerto Rico.",
            "Deadlines occur at 11:59 pm Central Time.",
            "Projected test dates are subject to change."],
    "lsat": ["All dates are listed in Eastern Time (ET), and all receipt deadlines are by 11:59 p.m. ET.",
             "Registered test takers will receive an email when scheduling becomes available.",
             "Note: These dates are subject to change."],
}


class Unreadable(Exception):
    pass


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60, context=ssl_context()) as r:
        return r.read().decode("utf-8", errors="replace")


def plain(fragment):
    t = re.sub(r"<!--[\s\S]*?-->", " ", fragment)
    t = re.sub(r"<(script|style|noscript)[\s\S]*?</\1>", " ", t, flags=re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()


def tables(page):
    """Every table on the page as rows of cell text."""
    page = re.sub(r"<!--[\s\S]*?-->", " ", page)
    out = []
    for tb in re.findall(r"<table[\s\S]*?</table>", page, re.I):
        rows = []
        for tr in re.findall(r"<tr[\s\S]*?</tr>", tb, re.I):
            rows.append([plain(c) for c in re.findall(r"<t[hd][^>]*>([\s\S]*?)</t[hd]>", tr, re.I)])
        out.append(rows)
    return out


def table(page, header, what):
    for rows in tables(page):
        if rows and rows[0] == header:
            return rows[1:]
    raise Unreadable("no %s table with the header %r" % (what, header))


def named(text, year=None):
    """Every month-and-day date in the text as ISO, taking the year it prints or the one given."""
    got = []
    for m in NAMED.finditer(text):
        y = int(m.group(3)) if m.group(3) else year
        if y is None:
            raise Unreadable("a date without a year: %r" % m.group(0))
        got.append(datetime.date(y, MONTHS[m.group(1).lower()], int(m.group(2))))
    return got


def numeric(text):
    return [datetime.date(int(y), int(mo), int(d)) for mo, d, y in NUMERIC.findall(text)]


def one(dates, what, row):
    if len(dates) != 1:
        raise Unreadable("%s in %r is not one date" % (what, row))
    return dates[0]


def ordered(*dates):
    return all(a < b for a, b in zip(dates, dates[1:]))


def quotes(page, exam):
    text = plain(page)
    kept = [q for q in QUOTES[exam] if q in text]
    missing = [q for q in QUOTES[exam] if q not in text]
    return kept, missing


def after(text, start, end):
    i = text.find(start)
    if i < 0:
        raise Unreadable("no %r on the page" % start)
    j = text.find(end, i)
    return text[i + len(start): j if j > 0 else None]


def sat(page, scores_page):
    # College Board's score release page lists the weekend dates whose release it has set,
    # the fall ones by September; a date it does not list yet has no release date here.
    released = {}
    for row in table(scores_page, SAT_SCORES_HEADER, "SAT Weekend score release"):
        if len(row) != 3:
            raise Unreadable("SAT score release row %r" % row)
        test, student, educator = (one(named(c), h, row) for c, h in zip(row, ("test date", "student release", "educator release")))
        if not ordered(test, student, educator):
            raise Unreadable("SAT score release row %r is out of order" % row)
        released[test.isoformat()] = (student.isoformat(), educator.isoformat())
    weekend = []
    for row in table(page, SAT_HEADER, "SAT Weekend"):
        if len(row) != 3:
            continue  # the footnote row spans the table
        test, reg, late = (one(named(c), h, row) for c, h in zip(row, ("test date", "deadline", "late deadline")))
        if not ordered(reg, late, test):
            raise Unreadable("SAT row %r: registration, late deadline and test date are out of order" % row)
        entry = {"test": test.isoformat(), "register_by": reg.isoformat(), "late_by": late.isoformat()}
        if test.isoformat() in released:
            entry["scores_student"], entry["scores_educator"] = released.pop(test.isoformat())
        weekend.append(entry)
    school = []
    for label, window in table(page, SAT_SCHOOL_HEADER, "in-school"):
        # "October 1–30, 2026" or "March 1–April 30, 2027": the end carries the year
        m = re.fullmatch(r"(\w+) (\d{1,2})\W+(?:(\w+) )?(\d{1,2}), (\d{4})", window)
        if not m:
            raise Unreadable("in-school window %r" % window)
        y = int(m.group(5))
        start = datetime.date(y, MONTHS[m.group(1)[:3].lower()], int(m.group(2)))
        end = datetime.date(y, MONTHS[(m.group(3) or m.group(1))[:3].lower()], int(m.group(4)))
        school.append({"tests": re.sub(r"^For (Fall|Spring) \d{4}: ", "", label),
                       "season": re.match(r"For (\w+ \d{4})", label).group(1), "from": start.isoformat(), "to": end.isoformat()})
    if released:
        raise Unreadable("score release dates for SAT dates the dates page does not list: %s" % sorted(released))
    text = plain(page)
    nxt = named(after(text, "Anticipated SAT Weekend", "Resources"))
    kept, missing = quotes(page, "sat")
    return {"src": "College Board, SAT Suite Test Dates and Deadlines", "url": SAT_URL,
            "scores_src": "College Board, Score Release Dates for Students and Educators", "scores_url": SAT_SCORES_URL,
            "weekend": weekend, "in_school": school,
            "anticipated": [d.isoformat() for d in nxt], "quotes": kept}, missing


def near_year(month_day, test, before):
    """The year of a date printed without one: a deadline falls before its test, a score
    release after it."""
    d = one(named(month_day, test.year), "date", month_day)
    if before and d > test:
        d = d.replace(year=d.year - 1)
    if not before and d < test:
        d = d.replace(year=d.year + 1)
    return d


def act(page):
    national = []
    for row in table(page, ACT_HEADER, "ACT national"):
        if len(row) != 5:
            raise Unreadable("ACT row %r" % row)
        test = one(named(row[0]), "test date", row)
        reg, late, photo = (near_year(c, test, True) for c in row[1:4])
        scores = near_year(row[4], test, False)
        if not ordered(reg, late, photo, test, scores):
            raise Unreadable("ACT row %r is out of order" % row)
        national.append({"test": test.isoformat(), "register_by": reg.isoformat(), "late_by": late.isoformat(),
                         "photo_standby_by": photo.isoformat(), "scores_paper": scores.isoformat()})
    text = plain(page)
    projected = named(after(text, "Projected 2027-2028 National Test Dates", "Projected test dates are subject"))
    kept, missing = quotes(page, "act")
    return {"src": "ACT, ACT Exam Test Dates and Deadlines", "url": ACT_URL, "national": national,
            "projected": [d.isoformat() for d in projected], "quotes": kept}, missing


def lsat_rows(rows, region):
    out = []
    for row in rows:
        if len(row) != 7:
            raise Unreadable("LSAT row %r" % row)
        # "February 2027: LSAT, Puerto Rico" (a dash on the page) is an administration for one
        # place only; it keeps the place so the page never offers it as everyone's next LSAT.
        m = re.match(r"^(.*?):\s*LSAT\W+(.+)$", row[0])
        label, place = (m.group(1) + ", " + m.group(2), m.group(2)) if m else (row[0], None)
        days = numeric(row[1])
        writing, reg, sched, scores = (one(numeric(c), h, row) for c, h in
                                       zip(row[2:6], ("writing", "registration", "scheduling", "scores")))
        if not days or not ordered(reg, sched, days[0]) or not ordered(*days) or not ordered(days[-1], scores) \
                or not writing <= days[0]:
            raise Unreadable("LSAT row %r is out of order" % row)
        out.append({"administration": label, "region": region, **({"place": place} if place else {}),
                    "days": [d.isoformat() for d in days],
                    "writing_opens": writing.isoformat(), "register_by": reg.isoformat(),
                    "scheduling_opens": sched.isoformat(), "scores": scores.isoformat()})
    return out


def lsat(page):
    found = [rows[1:] for rows in tables(page) if rows and rows[0] == LSAT_HEADER]
    if len(found) != 2:
        raise Unreadable("expected LSAC's U.S. and Canada table and its international table, found %d" % len(found))
    home, abroad = found
    if not all("(international)" in r[0] for r in abroad) or any("(international)" in r[0] for r in home):
        raise Unreadable("the LSAT tables are not the U.S. and Canada one and the international one")
    kept, missing = quotes(page, "lsat")
    return {"src": "LSAC, Upcoming LSAT Dates", "url": LSAT_URL,
            "administrations": lsat_rows(home, "us_canada") + lsat_rows(abroad, "international"),
            "quotes": kept}, missing


def read_all():
    data, missing = {}, {}
    data["sat"], missing["sat"] = sat(fetch(SAT_URL), fetch(SAT_SCORES_URL))
    for exam, url, parse in (("act", ACT_URL, act), ("lsat", LSAT_URL, lsat)):
        data[exam], missing[exam] = parse(fetch(url))
    return data, missing


def write(read_date):
    data, missing = read_all()
    for exam, qs in missing.items():
        for q in qs:
            print("test_dates: %s no longer prints %r; it is left out" % (exam, q))
    data = {"read": read_date, **data}
    s = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    if re.search("[–—]", s):
        sys.exit("test_dates: an em or en dash reached the data file")
    OUT.write_text(s)
    print("wrote %s: %d SAT, %d ACT and %d LSAT administrations" % (
        OUT.relative_to(ROOT), len(data["sat"]["weekend"]), len(data["act"]["national"]),
        len(data["lsat"]["administrations"])))


def check():
    have = json.loads(OUT.read_text())
    try:
        now, _ = read_all()
    except (Unreadable, OSError) as e:
        print("test_dates: could not read the makers' pages: %s" % e)
        return 2
    diffs = []
    for exam in ("sat", "act", "lsat"):
        a, b = have.get(exam), now[exam]
        for key in sorted(set(a) | set(b)):
            if a.get(key) != b.get(key):
                diffs.append("%s.%s: the file has %s, the page now gives %s" % (
                    exam, key, json.dumps(a.get(key))[:300], json.dumps(b.get(key))[:300]))
    for d in diffs:
        print("test_dates:", d)
    if diffs:
        print("test_dates: %d difference(s); run python3 src/test_dates.py --write, read the diff, and rebuild" % len(diffs))
        return 1
    print("test_dates: in step with College Board, ACT and LSAC (read %s)" % have.get("read"))
    return 0


if __name__ == "__main__":
    if "--write" in sys.argv:
        write(datetime.date.today().isoformat())
    elif "--check" in sys.argv:
        sys.exit(check())
    else:
        sys.exit(__doc__)
