"""Builds the test date pages under /exams/<exam>/test-dates/.

    /exams/sat/test-dates/    SAT Weekend dates and deadlines, in-school windows, next year's
    /exams/act/test-dates/    ACT national dates, deadlines and score release, next year's
    /exams/lsat/test-dates/   LSAT administrations, deadlines, scheduling and score release

Every date comes from data/test_dates.json, which src/test_dates.py parses from each maker's
own table and the weekly source job re-reads. Nothing about a date is typed here: the page
states a gap between two dates only by working it out, and only when every row agrees.

The page leads with where registration stands: the next date a student can still register
for, and any nearer test whose deadlines have passed. Pointing at the next test date alone
told a reader on September 27 to register for October 3 by September 18. The build picks
from its own date, and a small script picks again from the reader's, choosing among notes
that are all in the markup, so no copy moves into script.

Each test date also downloads as a calendar file holding its deadlines and the test day,
with reminders, so a student's own calendar does the reminding (GROWTH.md, what brings
people back).
"""
import datetime
import html
import json
import os
import pathlib
import re
import sys

D = pathlib.Path(__file__).parent
ROOT = D.parent
sys.path.insert(0, str(D))
import partials

SITE = "https://startfromnowhere.com"
DATA = ROOT / "data" / "test_dates.json"
HOSTS = {"sat": "https://satsuite.collegeboard.org/", "act": "https://www.act.org/", "lsat": "https://www.lsac.org/"}


def fail(msg):
    print("build_test_dates: " + msg, file=sys.stderr)
    sys.exit(1)


def esc(s):
    return html.escape(str(s), quote=True)


def d(iso):
    return datetime.date.fromisoformat(iso)


def long(iso):
    t = d(iso)
    return "%s %d, %d" % (t.strftime("%B"), t.day, t.year)


def weekday(iso):
    return d(iso).strftime("%A")


def span(first, last):
    a, b = d(first), d(last)
    if a == b:
        return long(first)
    if a.year == b.year and a.month == b.month:
        return "%s %d to %d, %d" % (a.strftime("%B"), a.day, b.day, a.year)
    return "%s to %s" % (long(first), long(last))


def days_text(days):
    """Test days as a range when they run on consecutive days, as LSAC's do."""
    ds = [d(x) for x in days]
    if all((b - a).days == 1 for a, b in zip(ds, ds[1:])):
        return span(days[0], days[-1])
    return ", ".join(long(x) for x in days)


def season(first, last):
    return "%d-%s" % (d(first).year, str(d(last).year)[2:])


def check(data):
    """The file, checked before anything is built from it: each exam cites its maker's
    own page, every date parses, and every row's dates run in order."""
    bad = []
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(data.get("read", ""))):
        bad.append("no read date")
    for exam, host in HOSTS.items():
        e = data.get(exam) or {}
        if not str(e.get("url", "")).startswith(host):
            bad.append("%s must cite a page on %s" % (exam, host))
        for q in e.get("quotes") or []:
            if re.search("[\u2013\u2014]", q):
                bad.append("%s quote has a dash: %r" % (exam, q))
    try:
        sat = data["sat"]["weekend"]
        for r in sat:
            if not d(r["register_by"]) < d(r["late_by"]) < d(r["test"]):
                bad.append("SAT %s is out of order" % r["test"])
            if "scores_student" in r and not d(r["test"]) < d(r["scores_student"]) <= d(r["scores_educator"]):
                bad.append("SAT %s score release is out of order" % r["test"])
        if not str(data["sat"].get("scores_url", "")).startswith(HOSTS["sat"]):
            bad.append("SAT score release must cite College Board")
        if [r["test"] for r in sat] != sorted(r["test"] for r in sat):
            bad.append("SAT dates are not in order")
        act = data["act"]["national"]
        for r in act:
            if not d(r["register_by"]) < d(r["late_by"]) < d(r["photo_standby_by"]) < d(r["test"]) < d(r["scores_paper"]):
                bad.append("ACT %s is out of order" % r["test"])
        if [r["test"] for r in act] != sorted(r["test"] for r in act):
            bad.append("ACT dates are not in order")
        for r in data["lsat"]["administrations"]:
            days = [d(x) for x in r["days"]]
            if not days or days != sorted(days) or not d(r["register_by"]) < d(r["scheduling_opens"]) < days[0] < d(r["scores"]):
                bad.append("LSAT %s is out of order" % r["administration"])
        if not data["sat"]["anticipated"] or not data["act"]["projected"]:
            bad.append("no next-year dates")
    except (KeyError, ValueError, TypeError) as e:
        bad.append("malformed: %r" % e)
    if bad:
        fail("data/test_dates.json: " + "; ".join(bad))


# Calendar files (RFC 5545): all-day events, CRLF line ends, lines folded at 75 octets.
def ics_text(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    if len(line.encode("utf-8")) <= 75:
        return line
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > (75 if not out else 74):
            out.append(cur.decode("utf-8"))
            cur = b""
        cur += b
    out.append(cur.decode("utf-8"))
    return "\r\n ".join(out)


def ics(name, page_url, read, events):
    """events: (first_iso, last_iso, summary, description, reminder days before or None)."""
    stamp = read.replace("-", "") + "T000000Z"
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Start From Nowhere//Test Dates//EN",
             "CALSCALE:GREGORIAN", "METHOD:PUBLISH"]
    for i, (first, last, summary, desc, remind) in enumerate(events):
        end = (d(last) + datetime.timedelta(days=1)).isoformat()
        lines += ["BEGIN:VEVENT", "UID:%s-%d@startfromnowhere.com" % (name, i), "DTSTAMP:" + stamp,
                  "DTSTART;VALUE=DATE:" + first.replace("-", ""), "DTEND;VALUE=DATE:" + end.replace("-", ""),
                  "SUMMARY:" + ics_text(summary), "DESCRIPTION:" + ics_text(desc), "URL:" + page_url,
                  "TRANSP:TRANSPARENT"]
        if remind:
            lines += ["BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + ics_text(summary),
                      "TRIGGER:-P%dD" % remind, "END:VALARM"]
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in lines) + "\r\n"


def uniform_gap(rows, a, b):
    """The days from a to b when every row has the same gap, else None."""
    gaps = {(d(r[b]) - d(r[a])).days for r in rows}
    return gaps.pop() if len(gaps) == 1 else None


def gap_range(rows, a, b):
    gaps = sorted((d(r[b]) - d(r[a])).days for r in rows)
    return gaps[0], gaps[-1]


def status(rows, today):
    """Where registration stands on a day: the rows whose test is still ahead but whose last
    deadline has passed, and the first row a student can still register for. Each row carries
    key, end (last test day), reg (regular deadline) and late (last deadline)."""
    closed = [r for r in rows if r["late"] < today <= r["end"]]
    open_ = next((r for r in rows if r["late"] >= today), None)
    return closed, open_


def notes(rows, today, texts, none_text):
    """Every status note the page can show, all in the markup, with today's showing."""
    closed, open_ = status(rows, today)
    opened, shut_notes = [], []
    for r in rows:
        reg, late, shut = texts(r)
        opened.append('<p class="next" id="reg-%s"%s>%s</p>' % (
            r["key"], "" if r is open_ and today <= r["reg"] else " hidden", reg))
        if late:
            opened.append('<p class="next" id="late-%s"%s>%s</p>' % (
                r["key"], "" if r is open_ and today > r["reg"] else " hidden", late))
        shut_notes.append('<p class="next shut" id="closed-%s"%s>%s</p>' % (r["key"], "" if r in closed else " hidden", shut))
    none = '<p class="next" id="none"%s>%s</p>' % ("" if open_ is None else " hidden", none_text)
    # The date a reader can still act on leads; a nearer test that has closed follows it.
    return "\n".join(opened + [none] + shut_notes), closed, open_


def rows_json(rows):
    return json.dumps([{k: r[k] for k in ("key", "end", "reg", "late")} for r in rows], separators=(",", ":"))


def row_attrs(when, today):
    """The row's last test day for the page script, and past already at build time for a
    reader without scripts."""
    return ' data-when="%s"%s' % (when, ' class="past"' if when < today else "")


def cal_link(fname):
    return '<a class="cal" href="%s" download>Add to calendar</a>' % fname


def faq_block(faq):
    faq_html = "\n".join("<h3>%s</h3><p>%s</p>" % (esc(q), esc(a)) for q, a in faq)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
                        separators=(",", ":"))
    return faq_html, faq_ld


def page(exam, e, data, cfg):
    tpl = (D / "test_dates_template.html").read_text()
    url = "%s/exams/%s/test-dates/" % (SITE, exam)
    src_link = '<a href="%s" rel="noopener" target="_blank">%s</a>' % (esc(e["url"]), esc(e["src"]))
    faq_html, faq_ld = faq_block(cfg["faq"])
    out = (tpl.replace("{{TITLE}}", esc(cfg["title"]))
              .replace("{{DESC}}", esc(cfg["desc"]))
              .replace("{{CANON}}", url)
              .replace("{{FAQ_LD}}", faq_ld)
              .replace("{{EXAM}}", esc(cfg["short"]))
              .replace("{{EXAM_SLUG}}", exam)
              .replace("{{H1}}", esc(cfg["h1"]))
              .replace("{{LEDE}}", cfg["lede"])
              .replace("{{NEXT}}", cfg["next"])
              .replace("{{ROWS_JSON}}", cfg["rows_json"])
              .replace("{{TABLE}}", cfg["table"])
              .replace("{{AFTER_TABLE}}", cfg["after_table"])
              .replace("{{MORE}}", cfg["more"])
              .replace("{{SOURCE}}", "Source: %s, read %s." % (src_link, esc(long(data["read"]))))
              .replace("{{FAQ_HTML}}", faq_html)
              .replace("{{LINKS}}", cfg["links"]))
    return partials.apply_chrome(out)


def quote(e, start):
    """A sentence the maker's page prints word for word, kept by test_dates.py, or ''."""
    return next((q for q in e.get("quotes") or [] if q.startswith(start)), "")


def sat(data, today):
    e = data["sat"]
    rows = e["weekend"]
    url = SITE + "/exams/sat/test-dates/"
    read = long(data["read"])
    deadline = quote(e, "SAT Weekend deadlines expire")
    late_fee = quote(e, "Late registration is available worldwide")
    st = [{"key": r["test"], "end": r["test"], "reg": r["register_by"], "late": r["late_by"], "row": r} for r in rows]

    def texts(s):
        r = s["row"]
        day = "%s, %s" % (weekday(r["test"]), long(r["test"]))
        return (("<strong>Registration is open for the SAT on %s.</strong> Register by %s; changes, regular cancellation and "
                 "late registration close %s." % (esc(day), esc(long(r["register_by"])), esc(long(r["late_by"])))),
                ("<strong>Late registration is open for the SAT on %s, until %s.</strong> Regular registration closed %s, and "
                 "late registration carries an additional fee." % (esc(day), esc(long(r["late_by"])), esc(long(r["register_by"])))),
                ("The SAT on %s, is still ahead, but registration for it closed %s." % (esc(day), esc(long(r["late_by"])))))

    nxt_html, closed, open_ = notes(st, today, texts, "<strong>Registration has closed for every SAT date College Board lists "
                                    "for %s.</strong> Its anticipated dates for the next year are below."
                                    % esc(span(rows[0]["test"], rows[-1]["test"])))
    files, trs = {}, []
    for r in rows:
        name = "sat-%s" % r["test"]
        desc = ("%s Source: %s, %s, read %s. Dates can change, so confirm on College Board's site before you register. "
                "From %s" % (deadline, e["src"], e["url"], read, url)).strip()
        files[name + ".ics"] = ics(name, url, data["read"], [
            (r["register_by"], r["register_by"], "SAT registration deadline (test on %s)" % long(r["test"]), desc, 3),
            (r["late_by"], r["late_by"], "SAT late registration and changes close (test on %s)" % long(r["test"]), desc, 1),
            (r["test"], r["test"], "SAT test day", desc, 1)]
            + ([(r["scores_student"], r["scores_student"], "SAT scores released to students (test on %s)" % long(r["test"]),
                 "Source: %s, %s, read %s. From %s" % (e["scores_src"], e["scores_url"], read, url), None)]
               if r.get("scores_student") else []))
        trs.append('<tr%s><td>%s, %s<span class="pastlbl"> (past)</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            row_attrs(r["test"], today), esc(weekday(r["test"])), esc(long(r["test"])), esc(long(r["register_by"])),
            esc(long(r["late_by"])),
            esc(long(r["scores_student"])) if r.get("scores_student") else '<span class="nr">Not yet listed</span>',
            cal_link(name + ".ics")))
    table = ('<div class="tablewrap"><table class="dates"><thead><tr><th>SAT test date</th><th>Register by</th>'
             '<th>Changes, cancellation and late registration by</th><th>Scores to students</th><th>Calendar</th></tr></thead>'
             '<tbody>\n%s\n</tbody></table></div>'
             % "\n".join(trs))
    reg_gap, late_gap = uniform_gap(rows, "register_by", "test"), uniform_gap(rows, "late_by", "test")
    after = ""
    if reg_gap and late_gap:
        after += ("<p>In College Board's table for this year, every registration deadline falls %d days before its test "
                  "date, and every deadline for changes and late registration %d days before.</p>" % (reg_gap, late_gap))
    said = [q for q in (deadline, late_fee) if q]
    if said:
        after += '<p class="src">College Board: %s Late registration carries an additional fee.</p>' % " ".join('"%s"' % esc(q) for q in said)
    listed = [r for r in rows if r.get("scores_student")]
    if listed:
        after += ('<p class="src">Score release dates: <a href="%s" rel="noopener" target="_blank">%s</a>, read %s. So far College Board '
                  'lists them for the tests from %s; this page adds the rest when it does.</p>'
                  % (esc(e["scores_url"]), esc(e["scores_src"]), esc(read),
                     esc(span(listed[0]["test"], listed[-1]["test"]) if len(listed) > 1 else long(listed[0]["test"]))))
    school_note = quote(e, "Students taking SAT School Day")
    school = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (esc(w["season"]), esc(w["tests"]), esc(span(w["from"], w["to"])))
                     for w in e["in_school"])
    antic = e["anticipated"]
    more = ('<h2>SAT and PSAT Testing at School</h2><p>%s Schools choose their testing days inside these windows.</p>'
            '<div class="tablewrap"><table class="dates"><thead><tr><th>Season</th><th>Tests</th><th>Testing window</th></tr></thead>'
            '<tbody>%s</tbody></table></div>'
            '<h2>Anticipated SAT Dates for %s</h2><p>College Board lists these anticipated SAT Weekend dates: %s. It publishes '
            'their deadlines later, and this page adds them once it does.</p>'
            % (('College Board: "%s"' % esc(school_note)) if school_note else "", school,
               esc(season(antic[0], antic[-1])), esc(", ".join(long(x) for x in antic))))
    faq = []
    if open_:
        o = open_["row"]
        lead = ""
        if closed:
            c = closed[0]["row"]
            lead = "The next SAT is on %s, %s, but registration for it closed %s. " % (weekday(c["test"]), long(c["test"]), long(c["late_by"]))
        faq.append(("When is the next SAT?", lead + "The next date open for registration is %s, %s: register by %s, and changes, "
                    "regular cancellation and late registration close %s (College Board, read %s)."
                    % (weekday(o["test"]), long(o["test"]), long(o["register_by"]), long(o["late_by"]), read)))
    faq.append(("How many SAT dates are there this year?", "College Board lists %d SAT Weekend dates from %s to %s (College "
                "Board, read %s)." % (len(rows), long(rows[0]["test"]), long(rows[-1]["test"]), read)))
    if reg_gap and late_gap:
        faq.append(("When is the SAT registration deadline?", "In College Board's table for this year, %d days before each test "
                    "date, and changes and late registration close %d days before. %s" % (reg_gap, late_gap, deadline)))
    faq.append(("When are the SAT dates for next year?", "College Board lists anticipated SAT Weekend dates of %s (College "
                "Board, read %s)." % (", ".join(long(x) for x in antic), read)))
    s = season(rows[0]["test"], rows[-1]["test"])
    cfg = {"short": "SAT", "title": "SAT Test Dates %s: Registration Deadlines" % s,
           "desc": "Every SAT test date for %s with its registration and late deadlines, from College Board, the anticipated "
                   "dates after that, and a calendar file for each date." % s,
           "h1": "SAT Test Dates %s" % s,
           "lede": ("College Board lists %d SAT Weekend dates from %s to %s. Each row gives the day to register by and the last "
                    "day for changes and late registration, and its calendar file puts both and the test day in your calendar "
                    "with reminders." % (len(rows), esc(long(rows[0]["test"])), esc(long(rows[-1]["test"])))),
           "next": nxt_html, "rows_json": rows_json(st), "table": table, "after_table": after, "more": more, "faq": faq,
           "links": ('<a class="btn" href="/sat/app/">Start SAT Practice Free</a><a class="btn sec" href="/exams/sat/">SAT Guide</a>'
                     '<a class="btn sec" href="/exams/sat/score-calculator/">SAT Score Calculator</a>'
                     '<a class="btn sec" href="/exams/sat/psat-calculator/">PSAT/NMSQT Calculator</a>')}
    return page("sat", e, data, cfg), files


def act(data, today):
    e = data["act"]
    rows = e["national"]
    url = SITE + "/exams/act/test-dates/"
    read = long(data["read"])
    tz = quote(e, "Deadlines occur")
    st = [{"key": r["test"], "end": r["test"], "reg": r["register_by"], "late": r["late_by"], "row": r} for r in rows]

    def texts(s):
        r = s["row"]
        day = "%s, %s" % (weekday(r["test"]), long(r["test"]))
        return (("<strong>Registration is open for the ACT on %s.</strong> Register by %s to avoid the late fee; the late "
                 "deadline is %s." % (esc(day), esc(long(r["register_by"])), esc(long(r["late_by"])))),
                ("<strong>Late registration is open for the ACT on %s, until %s.</strong> The regular deadline passed %s, so a "
                 "late fee applies." % (esc(day), esc(long(r["late_by"])), esc(long(r["register_by"])))),
                ("The ACT on %s, is still ahead, but its late deadline passed %s." % (esc(day), esc(long(r["late_by"])))))

    nxt_html, closed, open_ = notes(st, today, texts, "<strong>Registration has closed for every ACT national date for "
                                    "%s.</strong> ACT's projected dates for the next year are below."
                                    % esc(span(rows[0]["test"], rows[-1]["test"])))
    files, trs = {}, []
    for r in rows:
        name = "act-%s" % r["test"]
        desc = ("%s Source: %s, %s, read %s. Dates can change, so confirm on ACT's site before you register. From %s"
                % (tz, e["src"], e["url"], read, url)).strip()
        files[name + ".ics"] = ics(name, url, data["read"], [
            (r["register_by"], r["register_by"], "ACT registration deadline, late fee after (test on %s)" % long(r["test"]), desc, 3),
            (r["late_by"], r["late_by"], "ACT late registration deadline (test on %s)" % long(r["test"]), desc, 1),
            (r["photo_standby_by"], r["photo_standby_by"], "ACT photo upload and standby deadline (test on %s)" % long(r["test"]), desc, 1),
            (r["test"], r["test"], "ACT test day", desc, 1),
            (r["scores_paper"], r["scores_paper"], "ACT initial score release, paper (test on %s)" % long(r["test"]), desc, None)])
        trs.append('<tr%s><td>%s, %s<span class="pastlbl"> (past)</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            row_attrs(r["test"], today), esc(weekday(r["test"])), esc(long(r["test"])), esc(long(r["register_by"])),
            esc(long(r["late_by"])), esc(long(r["photo_standby_by"])), esc(long(r["scores_paper"])), cal_link(name + ".ics")))
    table = ('<div class="tablewrap"><table class="dates"><thead><tr><th>ACT test date</th><th>Register by (late fee after)</th>'
             '<th>Late deadline</th><th>Photo upload and standby by</th><th>Initial score release (paper)</th><th>Calendar</th></tr>'
             '</thead><tbody>\n%s\n</tbody></table></div>' % "\n".join(trs))
    lo, hi = gap_range(rows, "test", "scores_paper")
    said = [q for q in (quote(e, "National test dates"), tz) if q]
    after = ("<p>ACT lists an initial score release date for paper tests beside each date, %d to %d days after the test in "
             "this year's table.</p>" % (lo, hi))
    if said:
        after += '<p class="src">ACT: %s</p>' % " ".join('"%s"' % esc(q) for q in said)
    proj = e["projected"]
    subject = quote(e, "Projected test dates")
    more = ('<h2>Projected ACT Dates for %s</h2><p>ACT lists these projected national test dates: %s.%s</p>'
            % (esc(season(proj[0], proj[-1])), esc(", ".join(long(x) for x in proj)),
               (' In ACT\'s words: "%s"' % esc(subject)) if subject else ""))
    per_year = quote(e, "The ACT is offered")
    faq = []
    if open_:
        o = open_["row"]
        lead = ""
        if closed:
            c = closed[0]["row"]
            lead = "The next ACT is on %s, %s, but its late deadline passed %s. " % (weekday(c["test"]), long(c["test"]), long(c["late_by"]))
        faq.append(("When is the next ACT?", lead + "The next date open for registration is %s, %s: register by %s to avoid the "
                    "late fee, and the late deadline is %s (ACT, read %s)."
                    % (weekday(o["test"]), long(o["test"]), long(o["register_by"]), long(o["late_by"]), read)))
    if per_year and len(rows) == 7:
        faq.append(("How many times a year is the ACT offered?", 'ACT: "%s" Its table lists %d national dates from %s to %s '
                    "(ACT, read %s)." % (per_year, len(rows), long(rows[0]["test"]), long(rows[-1]["test"]), read)))
    faq.append(("When do ACT scores come out?", "ACT lists an initial score release date for paper tests beside each test "
                "date, %d to %d days after the test in its current table (ACT, read %s)." % (lo, hi, read)))
    faq.append(("When are the ACT dates for next year?", "ACT lists projected national test dates of %s (ACT, read %s)."
                % (", ".join(long(x) for x in proj), read)))
    s = season(rows[0]["test"], rows[-1]["test"])
    cfg = {"short": "ACT", "title": "ACT Test Dates %s: Deadlines and Score Release" % s,
           "desc": "Every ACT national test date for %s with its registration, late and photo deadlines and score release, "
                   "from ACT, plus a calendar file for each date." % s,
           "h1": "ACT Test Dates %s" % s,
           "lede": ("ACT lists %d national test dates from %s to %s. Each row gives the day to register by before a late fee, "
                    "the late and photo deadlines and the initial score release, and its calendar file puts them in your "
                    "calendar with reminders." % (len(rows), esc(long(rows[0]["test"])), esc(long(rows[-1]["test"])))),
           "next": nxt_html, "rows_json": rows_json(st), "table": table, "after_table": after, "more": more, "faq": faq,
           "links": ('<a class="btn" href="/act/app/">Start ACT Practice Free</a><a class="btn sec" href="/exams/act/">ACT Guide</a>'
                     '<a class="btn sec" href="/exams/act/score-calculator/">ACT Score Calculator</a>')}
    return page("act", e, data, cfg), files


def lsat(data, today):
    e = data["lsat"]
    home = [r for r in e["administrations"] if r["region"] == "us_canada"]
    abroad = [r for r in e["administrations"] if r["region"] == "international"]
    url = SITE + "/exams/lsat/test-dates/"
    read = long(data["read"])
    tz = quote(e, "All dates are listed")
    files = {}

    def key(r):
        return re.sub(r"[^a-z0-9]+", "-", r["administration"].lower()).strip("-")

    # An administration held for one place only (Puerto Rico) stays in the table but is never
    # offered as everyone's next LSAT.
    st = [{"key": key(r), "end": r["days"][-1], "reg": r["register_by"], "late": r["register_by"], "row": r}
          for r in home if not r.get("place")]

    def texts(s):
        r = s["row"]
        return (("<strong>Registration is open for the %s LSAT, %s.</strong> Register by %s; scores are released %s."
                 % (esc(r["administration"]), esc(days_text(r["days"])), esc(long(r["register_by"])), esc(long(r["scores"])))),
                None,
                ("The %s LSAT, %s, is still ahead, but its registration deadline passed %s."
                 % (esc(r["administration"]), esc(days_text(r["days"])), esc(long(r["register_by"])))))

    nxt_html, closed, open_ = notes(st, today, texts, "<strong>Registration has closed for every LSAT administration LSAC "
                                    "lists for this testing year.</strong>")

    def rows_html(rows, prefix):
        trs = []
        for r in rows:
            name = "lsat-%s-%s" % (prefix, key(r))
            desc = ("%s Source: %s, %s, read %s. Dates can change, so confirm on LSAC's site before you register. From %s"
                    % (tz, e["src"], e["url"], read, url)).strip()
            files[name + ".ics"] = ics(name, url, data["read"], [
                (r["register_by"], r["register_by"], "LSAT registration deadline (%s)" % r["administration"], desc, 3),
                (r["scheduling_opens"], r["scheduling_opens"], "LSAT scheduling opens (%s)" % r["administration"], desc, None),
                (r["writing_opens"], r["writing_opens"], "LSAT Argumentative Writing opens (%s)" % r["administration"], desc, None),
                (r["days"][0], r["days"][-1], "LSAT test days (%s)" % r["administration"], desc, 1),
                (r["scores"], r["scores"], "LSAT score release (%s)" % r["administration"], desc, None)])
            trs.append('<tr%s><td>%s<span class="pastlbl"> (past)</span></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                row_attrs(r["days"][-1], today), esc(r["administration"]), esc(days_text(r["days"])), esc(long(r["register_by"])),
                esc(long(r["scheduling_opens"])), esc(long(r["writing_opens"])), esc(long(r["scores"])), cal_link(name + ".ics")))
        return ('<div class="tablewrap"><table class="dates"><thead><tr><th>Administration</th><th>Test days</th><th>Register by</th>'
                '<th>Scheduling opens</th><th>Argumentative Writing opens</th><th>Score release</th><th>Calendar</th></tr></thead>'
                '<tbody>\n%s\n</tbody></table></div>' % "\n".join(trs))

    table = rows_html(home, "us")
    lo, hi = gap_range([dict(r, last=r["days"][-1]) for r in home], "last", "scores")
    said = [q for q in (tz, quote(e, "Registered test takers")) if q]
    after = ("<p>In LSAC's current table, scores are released %d to %d days after the last test day of each administration.</p>"
             % (lo, hi))
    if said:
        after += '<p class="src">LSAC: %s</p>' % " ".join('"%s"' % esc(q) for q in said)
    more = ('<h2>International LSAT Dates</h2><p>LSAC lists these administrations for test takers outside the U.S. and Canada.</p>%s'
            % rows_html(abroad, "intl"))
    faq = []
    if open_:
        o = open_["row"]
        lead = ""
        if closed:
            c = closed[0]["row"]
            lead = "The next LSAT in the U.S. and Canada is the %s administration, %s, but its registration deadline passed %s. " % (
                c["administration"], days_text(c["days"]), long(c["register_by"]))
        faq.append(("When is the next LSAT?", lead + "The next administration open for registration is %s, %s: register by %s, "
                    "and scores are released %s (LSAC, read %s)."
                    % (o["administration"], days_text(o["days"]), long(o["register_by"]), long(o["scores"]), read)))
    faq.append(("How many LSAT administrations are there this testing year?", "LSAC lists %d administrations in the U.S. and "
                "Canada, from %s to %s, and %d for test takers elsewhere (LSAC, read %s)."
                % (len(home), home[0]["administration"], home[-1]["administration"], len(abroad), read)))
    faq.append(("When are LSAT scores released?", "LSAC lists a score release date for each administration, %d to %d days "
                "after its last test day in the current table (LSAC, read %s)." % (lo, hi, read)))
    s = season(home[0]["days"][0], home[-1]["days"][-1])
    cfg = {"short": "LSAT", "title": "LSAT Test Dates %s: Deadlines and Score Release" % s,
           "desc": "Every LSAT administration for %s with its registration deadline, scheduling and score release dates, "
                   "from LSAC, plus a calendar file for each." % s,
           "h1": "LSAT Test Dates %s" % s,
           "lede": ("LSAC lists %d LSAT administrations in the U.S. and Canada from %s to %s. Each row gives the test days, the "
                    "registration deadline, when scheduling and the Argumentative Writing section open and when scores are "
                    "released, and its calendar file puts them in your calendar with reminders."
                    % (len(home), esc(home[0]["administration"]), esc(home[-1]["administration"]))),
           "next": nxt_html, "rows_json": rows_json(st), "table": table, "after_table": after, "more": more, "faq": faq,
           "links": ('<a class="btn" href="/lsat/app/">Start LSAT Practice Free</a><a class="btn sec" href="/exams/lsat/">LSAT Guide</a>'
                     '<a class="btn sec" href="/exams/lsat/percentile-calculator/">LSAT Percentile Calculator</a>')}
    return page("lsat", e, data, cfg), files


def write(rel, html_page, files):
    if "{{" in html_page:
        fail("unresolved placeholder in /%s/" % rel)
    for blob in [html_page] + list(files.values()):
        if re.search("[\u2013\u2014]", blob):
            fail("em or en dash in /%s/" % rel)
    out = ROOT / rel
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.ics"):
        old.unlink()
    (out / "index.html").write_text(html_page)
    for name, body in files.items():
        (out / name).write_bytes(body.encode("utf-8"))
    print("built %s/ with %d calendar files" % (rel, len(files)))


def main():
    today = os.environ.get("BLOG_BUILD_DATE") or datetime.date.today().isoformat()
    data = json.loads(DATA.read_text())
    check(data)
    for exam, build in (("sat", sat), ("act", act), ("lsat", lsat)):
        html_page, files = build(data, today)
        write("exams/%s/test-dates" % exam, html_page, files)


if __name__ == "__main__":
    main()
