"""The source policy from CLAUDE.md, in one place, for every published corpus.

Three corpora publish sourced figures: data/schools/, data/colleges/ and
data/exams.json. Each has a validator, and each used to carry its own idea of
what a bad source was, which is how data/exams.json came to publish nine facts
sourced to test prep companies (INC-0082). The lists live here so the three
cannot drift apart again.

CLAUDE.md bans six sites by name AND the category "coaching-site blogs". The
original list kept the six and dropped the category, so it refused GMAT Club by
name and accepted Kaplan. BANNED_SOURCES now carries both halves.

A blocklist can only ever refuse the sites somebody thought of, which is why
validate_exams.py does not rely on one: it requires the url host to be the test
maker's own domain. Where an allowlist is possible it is the stronger check, and
the blocklist below is the backstop for the corpora where one is not.
"""

# Fatal anywhere: a figure carrying one of these as its source is refused.
# The first row is the six CLAUDE.md names; the rest is the category it also
# bans, which is test prep and admissions consulting publishing as a source.
BANNED_SOURCES = [
    "gmat club", "gmatclub", "quora", "wikipedia", "gyandhan", "pagalguy",
    "reddit", "forum",
    # Coaching-site blogs, banned by category in CLAUDE.md.
    "kaplan", "princeton review", "magoosh", "manhattan prep", "manhattan review",
    "prepscholar", "applerouth", "menlo coaching", "achievable", "uworld",
    "veritas prep", "target test prep", "crackverbal", "e-gmat", "testmasters",
    "powerscore", "7sage", "blueprint lsat", "admissionado", "mbamission",
    "collegevine", "bestcolleges", "niche.com", "appily", "sallie mae",
]

# Allowed for now on the school library, queued for replacement with official
# pages. Warned, not fatal. Not accepted at all on data/exams.json, where the
# maker publishes every fact we need.
WEAK_SOURCES = ["clear admit", "stacy blackman", "search snippet", "f1gmat", "leland"]


def banned(src):
    """The banned entry a source matches, or None. Case insensitive substring."""
    s = str(src or "").lower()
    for b in BANNED_SOURCES:
        if b in s:
            return b
    return None


def host_of(url):
    """The lowercased host of a url, or '' if it has none."""
    try:
        from urllib.parse import urlparse
        return (urlparse(str(url or "")).netloc or "").lower()
    except Exception:
        return ""


def host_within(host, domain):
    """True when host is domain or a subdomain of it."""
    host, domain = str(host).lower(), str(domain).lower()
    return host == domain or host.endswith("." + domain)


# For prose rather than a src field. A blog post may legitimately use the word
# "forum" (this site runs one) or "blueprint", so scanning prose for the source
# NAMES above cries wolf; a post linking to kaplan.com as a source does not.
# Domains are the decidable version of the same policy. Used by the CI house
# rules sweep over generated pages.
BANNED_LINK_DOMAINS = [
    "gmatclub.com", "quora.com", "wikipedia.org", "gyandhan.com", "pagalguy.com",
    "reddit.com",
    "kaplan.com", "princetonreview.com", "magoosh.com", "manhattanprep.com",
    "manhattanreview.com", "prepscholar.com", "applerouth.com", "menlocoaching.com",
    "achievable.me", "uworld.com", "veritasprep.com", "targettestprep.com",
    "crackverbal.com", "e-gmat.com", "powerscore.com", "7sage.com",
    "blueprintprep.com", "admissionado.com", "mbamission.com", "collegevine.com",
    "bestcolleges.com", "niche.com", "appily.com", "sallie.com",
]


# For prose: the names a citation uses. Unambiguous proper nouns ONLY. "Achievable"
# and "Blueprint" are deliberately absent because both are ordinary English that
# appears in item text, and "forum" and "Niche" because this project runs a forum
# and logs a fetch failure against niche.com. A guard that cries wolf gets switched
# off, so this list buys precision by giving up the ambiguous names, which the src
# field check in validate_exams still catches where context is unambiguous.
BANNED_PROSE_NAMES = [
    "Princeton Review", "Applerouth", "Menlo Coaching", "UWorld", "Sallie Mae",
    "Kaplan", "Magoosh", "Manhattan Prep", "Manhattan Review", "PrepScholar",
    "Veritas Prep", "Target Test Prep", "CrackVerbal", "PowerScore", "7Sage",
    "GMAT Club", "GyanDhan", "PagalGuy", "Admissionado", "mbaMission",
    "CollegeVine", "BestColleges", "Appily",
]

# A citation in this project reads "(Source, 2026)". Matching the name inside a
# parenthetical that carries a year is what separates a citation from policy prose:
# EDITORIAL.md and DATA.md both name the banned sites legitimately, as the list of
# what not to cite, and a bare name scan fails on the rule that forbids the thing.
import re as _re

_YEAR = _re.compile(r"(?:19|20)\d\d")

# How far after a source name a year still counts as that name's citation. Wide
# enough for "Applerouth's enhanced-ACT coverage (2025)", where the name sits
# outside the parenthetical; the first version of this only matched names INSIDE
# "(Name, year)" and walked straight past that one.
_CITE_WINDOW = 80


def banned_citations(text):
    """Every citation in text that credits a banned source.

    A citation here is a banned name with a year close behind it, which covers
    both "(The Princeton Review, 2026)" and "Applerouth's coverage (2025)". The
    year is what separates a citation from policy prose: EDITORIAL.md, DATA.md
    and PROTOCOL.md all name these sites legitimately, as the list of what never
    to cite, and a bare name scan fails on the rule that forbids the thing.
    """
    t = str(text)
    low = t.lower()
    out = []
    for n in BANNED_PROSE_NAMES:
        nl = n.lower()
        start = 0
        while True:
            i = low.find(nl, start)
            if i < 0:
                break
            start = i + len(nl)
            window = t[start:start + _CITE_WINDOW]
            m = _YEAR.search(window)
            if m:
                out.append((n, (n + window[:m.end()]).strip()))
    return out
