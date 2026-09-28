"""Schema and source-policy validator for the school library.

Called by build_rankings.py before anything is computed. Hard failures stop
the build; soft warnings (weak sources queued for replacement) are printed.
Policy source: CLAUDE.md. Every published figure needs src, year, and url;
unverifiable values are null, never guesses; GMAT editions are never mixed
or converted.
"""
import json
import pathlib
import re
import sys

REGIONS = {"Northeast", "Midwest", "South", "West"}
_GENERIC = {"the", "school", "college", "graduate", "of", "business", "management", "and", "at",
            "administration", "economics", "faculty", "institute"}
TYPES = {"Private", "Public"}

# The source policy lives in src/sources.py so the three published corpora
# (schools, colleges, exams) cannot drift apart on what counts as a bad source.
# Re-exported here because data/research/merge_results.py imports both names
# from this module.
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sources import BANNED_SOURCES, WEAK_SOURCES  # noqa: E402,F401

RANGES = {
    "gmat_focus": (205, 805), "gmat_classic": (200, 800),
    "gre_quant": (130, 170), "gre_verbal": (130, 170),
    "gpa": (2.5, 4.0), "accept_rate_pct": (0, 100),
    "class_size": (10, 2000), "work_exp_years": (0, 15),
    "women_pct": (0, 100), "intl_pct": (0, 100),
    "tuition_usd": (10000, 150000), "salary_median_usd": (40000, 300000),
    "program_cost_usd": (15000, 250000),
    "employment_rate_pct": (0, 100),
}

RANK_KEYS = {"usnews", "ft", "bloomberg", "qs", "pq"}


def _figures(s):
    """Every sourced figure in a school file, with where it sits: (path, figure)."""
    for block in ("profile", "federal", "scholarship"):
        for f, fv in ((s.get(block) or {}).items()):
            if isinstance(fv, dict) and fv.get("v") is not None:
                yield "%s.%s" % (block, f), fv


# A search result's snippet is an excerpt a search engine made of a page, not the page.
# Rice's GMAT was taken from one and cited to the article it linked, which never prints
# the number; only the figure's note said snippet (INC-0151).
_SNIPPET = re.compile(r"\bsnippets?\b", re.I)


# A stat is printed beside its figure on the school's page, so it is copy: one that stops
# mid-word is published as it stands. Cincinnati's tuition note ended "; B" (INC-0141).
_CUT_ENDINGS = (",", ";", "(", " and", " or", " the", " of", " to", " for", " with", " plus")


def _cut_off(stat):
    """True when a stat's text stops partway: a last clause of one or two letters, or an
    ending on a separator or a word that needs something after it."""
    stat = str(stat or "").rstrip()
    if not stat:
        return False
    last = re.split(r"[;,(]", stat)[-1].strip()
    return bool(re.fullmatch(r"[A-Za-z]{1,2}", last)) or stat.endswith(_CUT_ENDINGS)


# tuition_usd is one year, and everything that reads it (the tuition column and filter,
# the fit card's two-year arithmetic) reads it as one year. BYU's two-year total sat in it
# with the caveat only in its note, so the page called it tuition per year (INC-0144).
_WHOLE_PROGRAM = re.compile(r"\b(?:program total|total program|whole program|entire (?:two|2)[- ]year)\b", re.I)
_ONE_YEAR = re.compile(r"\b(?:one|1)[- ]year\b|\b1[0-2][- ]month\b|\bone academic year\b", re.I)


def _total_as_year(stat):
    """True when a yearly tuition figure's note says it is the whole program's total and
    the program is not a one-year program, whose total is its year."""
    stat = str(stat or "")
    return bool(_WHOLE_PROGRAM.search(stat)) and not _ONE_YEAR.search(stat)


TRIAGE = pathlib.Path(__file__).resolve().parent.parent / "data" / "source_triage.json"

# A GMAT figure is filed under an edition only when its source says which (INC-0157). The
# stat says so in the source's words: the edition's name, its 200 to 800 or 205 to 805 scale,
# or the other edition named beside it. A figure whose source names neither may still carry
# a proof in edition_proof, such as a class that took the test before the Focus Edition
# existed, with the pages that show it. Eleven figures had been filed by guesses, from a
# class year, a last digit or how high a number was, none of which settles the edition.
_GMAT_LABEL = {
    "gmat_focus": re.compile(r"focus|205 to 805|205-805|"
                             r"(?:beside|alongside) a separate (?:\w+ ){0,2}GMAT (?:10th Edition|Classic|Legacy)", re.I),
    "gmat_classic": re.compile(r"classic|10th edition|legacy|previous (?:edition|format|version)|traditional|older version|"
                               r"200 to 800|200-800|(?:beside|alongside) a separate (?:\w+ ){0,2}GMAT Focus", re.I),
}
_GMAT_GUESS = re.compile(r"not label|consistent with|scale cap|not producible|not attainable|inferred|classified as|predates", re.I)


def _gmat_edition_errors(slug, field, fv):
    """Why a published GMAT figure does not show which edition its source gives it."""
    proof = fv.get("edition_proof")
    if proof is not None:
        if not (isinstance(proof, dict) and len(str(proof.get("why") or "")) >= 60
                and isinstance(proof.get("urls"), list) and proof["urls"]
                and all(str(u).startswith("https://") for u in proof["urls"])
                and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(proof.get("checked") or ""))):
            return [f"{slug}.{field}: edition_proof needs a why, the https urls that show it, and a checked date"]
        return []
    errs = []
    if not _GMAT_LABEL[field].search(str(fv.get("stat") or "")):
        errs.append(f"{slug}.{field}: its stat does not say which edition its source gives it; quote the source's label, "
                    f"or prove the edition in edition_proof, or leave the figure blank (INC-0157)")
    said = _GMAT_GUESS.search(" ".join(str(fv.get(k) or "") for k in ("stat", "note")))
    if said:
        errs.append(f"{slug}.{field}: its stat or note reasons about the edition ({said.group(0)!r}); a GMAT "
                    f"figure is filed only under the edition its source names or edition_proof shows (INC-0157)")
    return errs


def _triage_errors(schools, path=TRIAGE):
    """data/source_triage.json records figures a person read and found right where the
    source check cannot read them (INC-0154). An entry holds for the figure it judged and no
    other: the figure has to exist with the same value, and still carry every number the
    entry says the check misses, or the entry is refused and the figure has to be read again."""
    if not path.exists():
        return []
    from check_sources import norm, school_numbers
    errors, seen = [], set()
    by_slug = {s.get("slug"): s for s in schools}
    for e in json.loads(path.read_text()).get("entries", []):
        key = str(e.get("key") or "")
        if key in seen:
            errors.append(f"source_triage: {key} is listed twice")
        seen.add(key)
        parts = key.split(".")
        s = by_slug.get(parts[0]) if len(parts) == 3 else None
        fv = ((s or {}).get(parts[1]) or {}).get(parts[2]) if s else None
        if not isinstance(fv, dict) or fv.get("v") is None:
            errors.append(f"source_triage: {key} names no published figure; remove the entry")
            continue
        if e.get("v") != fv["v"]:
            errors.append(f"source_triage: {key} was read as {e.get('v')!r} and is now {fv['v']!r}; "
                          f"read the figure on its page again and update or remove the entry")
        near = e.get("near")
        if near is not None:
            # A figure found beside another program's name and read as this program's: the
            # entry names the programs it was read beside, and nothing else is judged by it.
            if not isinstance(near, list) or not near or not all(isinstance(n, str) and n.strip() for n in near):
                errors.append(f"source_triage: {key} needs near, the other programs' names the check "
                              f"finds beside the figure")
        else:
            missing = {norm(str(n)) for n in e.get("missing") or []}
            gone = sorted(missing - school_numbers(fv))
            if not missing or gone:
                errors.append(f"source_triage: {key} lists missing numbers {sorted(missing)} that the figure "
                              f"no longer carries ({gone}); read it again and update the entry")
        why = str(e.get("why") or "")
        if len(why) < 40:
            errors.append(f"source_triage: {key} needs a why that says where the page shows the figure")
        if "\u2014" in why or "\u2013" in why:
            errors.append(f"source_triage: {key}: em/en dash in why")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(e.get("checked") or "")):
            errors.append(f"source_triage: {key} needs the date it was read, as YYYY-MM-DD")
    return errors


def validate(schools):
    errors, warnings = [], []
    seen = set()
    weak_count = 0
    for s in schools:
        slug = s.get("slug") or "?"
        if slug in seen:
            errors.append(f"{slug}: duplicate slug")
        seen.add(slug)
        for key in ["slug", "name", "university", "city", "state", "region", "type", "ranks", "profile"]:
            if key not in s:
                errors.append(f"{slug}: missing key {key}")
        # A page prints the name alone, in its title, heading and every answer, so the name
        # has to say which school it is. Five records held a business school's own short name,
        # "School of Business", which is plain under its university's banner and anonymous in a
        # page title (INC-0153).
        if s.get("name") and all(w.lower() in _GENERIC for w in re.findall(r"[A-Za-z]+", s["name"])):
            errors.append(f"{slug}: name {s['name']!r} does not say which school it is; use the "
                          f"standalone name its own site gives, such as the university's name with it")
        if s.get("region") not in REGIONS:
            errors.append(f"{slug}: bad region {s.get('region')!r}")
        if s.get("type") not in TYPES:
            errors.append(f"{slug}: bad type {s.get('type')!r}")
        for k, r in (s.get("ranks") or {}).items():
            if k not in RANK_KEYS:
                errors.append(f"{slug}: unknown rank source {k}")
            if r and r.get("rank") is not None and not (1 <= r["rank"] <= 200):
                errors.append(f"{slug}: implausible {k} rank {r['rank']}")
        for f, fv in (s.get("profile") or {}).items():
            if not isinstance(fv, dict):
                if f == "class_year":
                    # A bare year does not say what it is: a graduating class, an entering
                    # class, or the year a page was read. Five records meant the last and
                    # were printed as the first (INC-0147).
                    if re.fullmatch(r"\s*\d{4}\s*", str(fv or "")):
                        errors.append(f"{slug}.class_year: {fv!r} is a bare year; write what it names "
                                      f"('Class of {str(fv).strip()}', 'Fall {str(fv).strip()} entering class') "
                                      f"or 'Typical class profile (no class year stated)'")
                    continue
                errors.append(f"{slug}.{f}: not an object")
                continue
            v = fv.get("v")
            if v is None:
                continue
            for req in ["src", "year"]:
                if not fv.get(req):
                    errors.append(f"{slug}.{f}: published value without {req}")
            if not fv.get("url", "").startswith("http"):
                errors.append(f"{slug}.{f}: published value without a source url")
            if not isinstance(fv.get("year"), int) or not (2018 <= fv["year"] <= 2027):
                errors.append(f"{slug}.{f}: implausible source year {fv.get('year')!r}")
            src = str(fv.get("src", "")).lower()
            if any(b in src for b in BANNED_SOURCES):
                errors.append(f"{slug}.{f}: banned source {fv.get('src')!r}")
            if any(w in src for w in WEAK_SOURCES):
                weak_count += 1
                warnings.append(f"{slug}.{f}: weak source {fv.get('src')!r}")
            lo_hi = RANGES.get(f)
            if lo_hi and isinstance(v, (int, float)) and not (lo_hi[0] <= v <= lo_hi[1]):
                errors.append(f"{slug}.{f}: value {v} outside plausible range {lo_hi}")
            for sval in [fv.get("src"), fv.get("stat"), fv.get("url")]:
                if isinstance(sval, str) and ("—" in sval or "–" in sval):
                    errors.append(f"{slug}.{f}: em/en dash in metadata")
            if _cut_off(fv.get("stat")):
                errors.append(f"{slug}.{f}: stat stops partway: {str(fv['stat'])[-40:]!r}")
            # stat describes a figure as its source states it, and is printed and checked;
            # note is our commentary, and is neither. A description filed under note left six
            # figures bare on their pages and unchecked (INC-0143).
            if fv.get("note") and not fv.get("stat"):
                errors.append(f"{slug}.{f}: has a note but no stat; a note is commentary beside a "
                              f"description, so the description goes in stat")
            if f in _GMAT_LABEL:
                errors += _gmat_edition_errors(slug, f, fv)
            if f == "tuition_usd" and _total_as_year(fv.get("stat")):
                errors.append(f"{slug}.tuition_usd: its note calls it a program total, and the field "
                              f"is one year; a whole-program figure goes in program_cost_usd")
        # official_hosts: places outside the school's own domain where the school itself
        # publishes (its storage bucket, an alias domain). Each needs the evidence that it is
        # the school's and the date that was checked, because this field changes a figure's
        # label from secondary to official and must not be a way to launder a publisher.
        # The federal block is sourced like any other figure, and a figure that names the
        # College Scorecard has to point at it. Every one of them once cited the program's
        # own site, which passed a check that only asked whether a url was there (INC-0125).
        for f, fv in ((s.get("federal") or {}).items()):
            if not isinstance(fv, dict) or fv.get("v") is None:
                continue
            for req in ("src", "year", "url"):
                if not fv.get(req):
                    errors.append(f"{slug}.federal.{f}: published value without {req}")
        for where, fv in _figures(s):
            if "college scorecard" in str(fv.get("src", "")).lower() and \
                    not str(fv.get("url", "")).startswith("https://collegescorecard.ed.gov/"):
                errors.append(f"{slug}.{where}: cites the College Scorecard but its url "
                              f"{fv.get('url')!r} is not on collegescorecard.ed.gov")
            # A figure worked from two pages names the second, and the source check reads both
            # (INC-0154). Each is a source like the first, under the same policy.
            also = fv.get("also_urls")
            if also is not None:
                if not (isinstance(also, list) and also and all(str(u).startswith("https://") for u in also)):
                    errors.append(f"{slug}.{where}: also_urls must be a list of https urls")
                elif any(b in str(u).lower() for u in also for b in BANNED_SOURCES):
                    errors.append(f"{slug}.{where}: also_urls names a banned source")
            said = next((k for k in ("stat", "note", "src") if _SNIPPET.search(str(fv.get(k) or ""))), None)
            if said:
                errors.append(f"{slug}.{where}: its {said} says it was read from a snippet; read the "
                              f"figure on its page, and say what the page prints, before publishing it")
        for oh in (s.get("official_hosts") or []):
            if not (isinstance(oh, dict) and str(oh.get("prefix", "")).startswith("https://")
                    and oh.get("evidence") and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(oh.get("checked", "")))):
                errors.append(f"{slug}.official_hosts: each entry needs an https prefix, evidence and a checked date")
            elif any(b in str(oh.get("prefix", "")).lower() for b in ("poetsandquants", "usnews", "gmac.com", "bloomberg", "ft.com", "topuniversities", "businessbecause")):
                errors.append(f"{slug}.official_hosts: {oh.get('prefix')} is a publisher, not the school")
        # Scholarship block. Same provenance rules as every other figure, plus a checked
        # date, because award terms change every admissions cycle and a 2024 number quoted
        # in 2026 is misinformation even when it was true when written.
        sch = s.get("scholarship")
        if sch is not None:
            if not isinstance(sch, dict):
                errors.append(f"{slug}.scholarship: not an object")
            else:
                checked = sch.get("checked")
                if not (isinstance(checked, str) and len(checked) == 10 and checked[4] == "-"):
                    errors.append(f"{slug}.scholarship: missing or malformed checked date "
                                  f"{checked!r} (want YYYY-MM-DD)")
                review = sch.get("review")
                if review is not None and review.get("v") not in ("automatic", "separate"):
                    errors.append(f"{slug}.scholarship.review: value must be 'automatic' or "
                                  f"'separate', got {review.get('v')!r}")
                for f in ("review", "pct_receiving", "avg_award_usd"):
                    fv = sch.get(f)
                    if fv is None:
                        continue
                    if not isinstance(fv, dict):
                        errors.append(f"{slug}.scholarship.{f}: not an object")
                        continue
                    if fv.get("v") is None:
                        continue
                    for req in ("src", "year", "stat"):
                        if not fv.get(req):
                            errors.append(f"{slug}.scholarship.{f}: published value without {req}")
                    if not str(fv.get("url", "")).startswith("http"):
                        errors.append(f"{slug}.scholarship.{f}: published value without a source url")
                    src = str(fv.get("src", "")).lower()
                    if any(b in src for b in BANNED_SOURCES):
                        errors.append(f"{slug}.scholarship.{f}: banned source {fv.get('src')!r}")
                    for sval in (fv.get("src"), fv.get("stat"), fv.get("url")):
                        if isinstance(sval, str) and ("\u2014" in sval or "\u2013" in sval):
                            errors.append(f"{slug}.scholarship.{f}: em/en dash in metadata")
                    if _cut_off(fv.get("stat")):
                        errors.append(f"{slug}.scholarship.{f}: stat stops partway: "
                                      f"{str(fv['stat'])[-40:]!r}")
                pct = sch.get("pct_receiving")
                if pct and isinstance(pct.get("v"), (int, float)) and not (0 <= pct["v"] <= 100):
                    errors.append(f"{slug}.scholarship.pct_receiving: {pct['v']} is not a percentage")
                amt = sch.get("avg_award_usd")
                if amt and isinstance(amt.get("v"), (int, float)) and not (1000 <= amt["v"] <= 250000):
                    errors.append(f"{slug}.scholarship.avg_award_usd: {amt['v']} outside a plausible "
                                  f"annual award range")

    errors += _triage_errors(schools)
    if warnings:
        print(f"validate_schools: {weak_count} figures still on weak sources "
              f"(Clear Admit / Stacy Blackman / snippets), replacement queued", file=sys.stderr)
    if errors:
        for e in errors[:40]:
            print("validate_schools ERROR:", e, file=sys.stderr)
        print(f"validate_schools: {len(errors)} error(s)", file=sys.stderr)
        sys.exit(1)
    return warnings
