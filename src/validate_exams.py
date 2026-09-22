"""Source-policy validator for data/exams.json, the exam guide corpus.

Called by build_exams.py before anything is rendered. Same contract as
validate_schools.py and validate_colleges.py: every published figure carries a
source, a year and a url, and unverifiable facts are dropped rather than
guessed. This file existed for the other two corpora and not for this one, which
is how nine facts across the five exam guides came to cite test prep companies
(INC-0082).

The check here is stricter than the other two, because it can be. A school
statistic can legitimately come from many places, so that corpus is policed with
a blocklist of bad sources. An exam fact has exactly one authoritative publisher,
the test maker, so this is an allowlist: the url host must be the maker's own
domain. An allowlist refuses the prep company nobody thought to name; a blocklist
only ever refuses the ones somebody did.
"""
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from sources import banned, host_of, host_within  # noqa: E402

# The one authoritative publisher per exam, keyed by slug. Subdomains count, so
# satsuite. and support. and newsroom. all pass without being listed.
MAKER_DOMAIN = {
    "gmat": ["mba.com", "gmac.com"],
    "sat": ["collegeboard.org"],
    "gre": ["ets.org"],
    "lsat": ["lsac.org"],
    "act": ["act.org"],
    "mcat": ["aamc.org"],
    "ea": ["mba.com", "gmac.com"],
}

# Hosts allowed on any exam regardless of maker, each with the reason it is here.
# Kept deliberately short: an entry is a decision that a fact is better sourced
# somewhere other than the maker, and that is rarely true.
ALLOWED_ELSEWHERE = {
    "www.ed.gov": "US Department of Education",
    "nces.ed.gov": "National Center for Education Statistics",
}

# Fields on an exam record that are published figures and must carry provenance.
FIGURE_FIELDS = ["score_scale", "total_time", "cost_usd", "validity_years",
                 "delivery", "retake_policy", "score_release", "used_for",
                 "acceptance", "answer_choices", "section_shape",
                 "content_categories"]

RANGES = {"cost_usd": (0, 1000), "validity_years": (1, 10)}


def _check_figure(slug, where, fig, errors):
    """One published figure: provenance present, source allowed, host allowed."""
    if not isinstance(fig, dict):
        errors.append("%s.%s: not an object" % (slug, where))
        return
    # A figure with no value is not published, so it needs no provenance.
    if fig.get("text") is None and fig.get("v") is None:
        return
    for req in ("src", "year", "url"):
        if not fig.get(req):
            errors.append("%s.%s: published figure without %s" % (slug, where, req))
    hit = banned(fig.get("src"))
    if hit:
        errors.append("%s.%s: banned source %r (matched %r); CLAUDE.md bans coaching "
                      "sites outright" % (slug, where, fig.get("src"), hit))
    url = str(fig.get("url") or "")
    if url and not url.startswith("https://"):
        errors.append("%s.%s: source url is not https" % (slug, where))
    host = host_of(url)
    if host:
        allowed = MAKER_DOMAIN.get(slug, [])
        ok = any(host_within(host, d) for d in allowed) or host in ALLOWED_ELSEWHERE
        if not ok:
            errors.append("%s.%s: source host %r is not the test maker's (%s). An exam "
                          "fact comes from the maker or it does not ship."
                          % (slug, where, host, ", ".join(allowed) or "none recorded"))
    for key in ("text", "src", "url", "stat"):
        val = fig.get(key)
        if isinstance(val, str) and ("—" in val or "–" in val):
            errors.append("%s.%s: em or en dash in %s" % (slug, where, key))
    lo_hi = RANGES.get(where.split("[")[0])
    if lo_hi and isinstance(fig.get("v"), (int, float)):
        lo, hi = lo_hi
        if not (lo <= fig["v"] <= hi):
            errors.append("%s.%s: %r outside the plausible range %s to %s"
                          % (slug, where, fig["v"], lo, hi))


def validate(exams):
    """Raise SystemExit on any violation. Returns the list of warnings."""
    errors, warnings = [], []
    seen = set()
    for e in exams:
        slug = e.get("slug")
        if not slug:
            errors.append("an exam record has no slug")
            continue
        if slug in seen:
            errors.append("%s: duplicate slug" % slug)
        seen.add(slug)
        if slug not in MAKER_DOMAIN:
            errors.append("%s: no maker domain recorded, so no source can be checked. "
                          "Add one to MAKER_DOMAIN before publishing this exam." % slug)
        maker = e.get("maker") or {}
        reg = str(maker.get("register_url") or "")
        if reg:
            host = host_of(reg)
            if not any(host_within(host, d) for d in MAKER_DOMAIN.get(slug, [])):
                errors.append("%s.maker.register_url: host %r is not the maker's"
                              % (slug, host))
        for f in FIGURE_FIELDS:
            if f in e and e[f] is not None:
                _check_figure(slug, f, e[f], errors)
        for i, fact in enumerate(e.get("key_facts") or []):
            _check_figure(slug, "key_facts[%d]" % i, fact, errors)
        # The sections array carries question counts and minutes, which are
        # published exam facts, and it has no provenance fields at all. Warned
        # rather than fatal: making it fatal today would block the build on a gap
        # that predates this check, and the fix is to source them, not to delete
        # them. Recorded here so the gap is counted rather than forgotten.
        if e.get("sections") and not e.get("sections_src"):
            warnings.append("%s.sections: question counts and minutes carry no source, "
                            "year or url" % slug)
    if warnings:
        for w in warnings:
            print("validate_exams WARNING:", w, file=sys.stderr)
    if errors:
        for er in errors[:40]:
            print("validate_exams ERROR:", er, file=sys.stderr)
        print("validate_exams: %d error(s)" % len(errors), file=sys.stderr)
        sys.exit(1)
    return warnings


def selftest():
    """Prove the check fires and, just as importantly, that it does not overfire.

    A guard is only worth its line count if it has been seen to fail. check_bias
    taught this the hard way: a one-directional test passes forever once the
    thing it watches is fixed, and then it is watching nothing.
    """
    import copy
    base = {
        "slug": "gmat", "maker": {"register_url": "https://www.mba.com/x"},
        "score_scale": {"text": "Total 205 to 805", "src": "mba.com (GMAC)",
                        "year": 2025, "url": "https://www.mba.com/exams/gmat-exam/scores"},
        "key_facts": [],
    }
    cases = [
        ("a clean record passes", base, True),
        ("a coaching site by name is refused",
         {"score_scale": dict(base["score_scale"], src="Kaplan")}, False),
        ("a coaching site by name is refused even in a compound source",
         {"score_scale": dict(base["score_scale"], src="mba.com; Applerouth")}, False),
        ("a non maker host is refused even with a respectable looking source name",
         {"score_scale": dict(base["score_scale"], src="GMAC",
                              url="https://www.princetonreview.com/gmat")}, False),
        ("a published figure with no url is refused",
         {"score_scale": {k: v for k, v in base["score_scale"].items() if k != "url"}}, False),
        ("a published figure with no year is refused",
         {"score_scale": {k: v for k, v in base["score_scale"].items() if k != "year"}}, False),
        ("an em dash is refused",
         {"score_scale": dict(base["score_scale"], text="Total 205 — 805")}, False),
        ("a null figure needs no provenance",
         {"score_scale": {"text": None}}, True),
        ("a banned source inside key_facts is refused",
         {"key_facts": [dict(base["score_scale"], src="Magoosh")]}, False),
        ("an exam with no maker domain recorded is refused",
         {"slug": "nclex"}, False),
        ("http rather than https is refused",
         {"score_scale": dict(base["score_scale"],
                              url="http://www.mba.com/exams/gmat-exam/scores")}, False),
    ]
    failures = []
    for label, patch, should_pass in cases:
        rec = copy.deepcopy(base)
        rec.update(copy.deepcopy(patch))
        try:
            validate([rec])
            passed = True
        except SystemExit:
            passed = False
        if passed != should_pass:
            failures.append("%s: expected %s, got %s"
                            % (label, "pass" if should_pass else "refusal",
                               "pass" if passed else "refusal"))
    return failures


if __name__ == "__main__":
    import io, json as _json, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        fails = selftest()
    if fails:
        for f in fails:
            print("validate_exams SELFTEST:", f, file=sys.stderr)
        sys.exit(1)
    here = __file__.rsplit("/", 1)[0]
    with open(here + "/../data/exams.json") as fh:
        warns = validate(_json.load(fh))
    print("validate_exams: selftest ok, data/exams.json clean, %d warning(s)" % len(warns))
