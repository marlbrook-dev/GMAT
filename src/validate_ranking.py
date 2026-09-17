"""Check the college score against published rankings.

The score is built from federal outcome data alone and deliberately does not copy
anybody else's list. But a ranking that shares almost no top 100 with every other
published ranking is not being independent, it is being wrong, and the only way to
tell the difference is to measure the overlap rather than argue about it.

Two reference lists, chosen because they disagree with each other:

  Washington Monthly national universities   outcomes, social mobility, service
  Times Higher Education, US institutions    research, reputation, citations

A score that tracks both is measuring something real. A score that tracks neither is
measuring an artifact of its own weights. Run this after any weight change.

Both lists are read from data/reference_rankings.json, captured from the publishers
with the date and URL recorded in that file. They are used only to check our list,
never to build it: no published rank is an input to the SFN College Score.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REF = os.path.join(ROOT, "data", "reference_rankings.json")

# Name forms the publishers use that our federal names spell differently.
ALIASES = {
    "ma institute of technology": "massachusetts institute of technology",
    "university of california, berkeley": "university of california berkeley",
    "university of california, los angeles": "university of california los angeles",
    "university of california, san diego": "university of california san diego",
    "university of california, davis": "university of california davis",
    "university of california, irvine": "university of california irvine",
    "university of california, santa barbara": "university of california santa barbara",
    "university of california, santa cruz": "university of california santa cruz",
    "university of california, riverside": "university of california riverside",
    "university of il-urbana-champaign": "university of illinois urbana champaign",
    "university of illinois at urbana-champaign": "university of illinois urbana champaign",
    "university of nc-chapel hill": "university of north carolina at chapel hill",
    "university of washington-seattle": "university of washington seattle campus",
    "university of michigan-ann arbor": "university of michigan ann arbor",
    "university of wisconsin-madison": "university of wisconsin madison",
    "university of minnesota-twin cities": "university of minnesota twin cities",
    "the university of texas at austin": "university of texas at austin",
    "texas a&m university": "texas a m university",
    "ohio state university": "ohio state university main campus",
    "pennsylvania state university": "pennsylvania state university main campus",
    "purdue university": "purdue university main campus",
    "indiana university": "indiana university bloomington",
    "rutgers university": "rutgers university new brunswick",
    "georgia institute of technology": "georgia institute of technology main campus",
    "university of colorado boulder": "university of colorado boulder",
    "arizona state university": "arizona state university campus immersion",
    "university of maryland, college park": "university of maryland college park",
    "university of pittsburgh": "university of pittsburgh pittsburgh campus",
    "virginia polytechnic institute and state university": "virginia tech",
    "suny stony brook": "stony brook university",
    "stony brook university, suny": "stony brook university",
    "university at buffalo": "university at buffalo",
    "case western reserve university": "case western reserve university",
    "the university of chicago": "university of chicago",
    "washington university in st louis": "washington university in st louis",
    "university of southern california": "university of southern california",
}


# Words that carry no identity: publishers keep or drop them freely, and leaving them
# in was scoring real matches as misses. "Columbia University in the City of New York"
# against "Columbia Univ. in the City of NY" was counted as a stranger in our top 25
# until this ran, which made the overlap look worse than it is.
NOISE = re.compile(
    r'\b(?:the|at|of|in|and|a|suny|cuny|univ|university|universities|college|colleges|'
    r'institute|institution|main|campus|city|new york|ny)\b')

STATE_WORDS = {
    'ca': 'california', 'ny': 'new york', 'tx': 'texas', 'pa': 'pennsylvania',
    'il': 'illinois', 'nc': 'north carolina', 'sc': 'south carolina',
    'va': 'virginia', 'wv': 'west virginia', 'ma': 'massachusetts',
    'md': 'maryland', 'mi': 'michigan', 'mn': 'minnesota', 'mo': 'missouri',
    'wi': 'wisconsin', 'wa': 'washington', 'fl': 'florida', 'ga': 'georgia',
    'oh': 'ohio', 'nj': 'new jersey', 'az': 'arizona', 'co': 'colorado',
}


def norm(name):
    """Reduce a college name to a comparable key.

    Publishers abbreviate differently ("MA Institute of Technology", "Univ. of
    IL-Urbana-Champaign", "CA State University, Long Beach"), so matching on the raw
    string undercounts badly. This expands the state abbreviations they use as words,
    applies the explicit aliases, then strips the words that carry no identity and
    compares what is left as a set.
    """
    n = name.lower()
    n = re.sub(r'\([^)]*\)', ' ', n)          # trailing state code in parentheses
    n = n.replace('&', ' and ').replace('.', ' ')
    n = re.sub(r'[^a-z0-9]+', ' ', n).strip()
    n = re.sub(r'\s+', ' ', n).strip()
    # "MA Institute of Technology" and "CA State University" use the postal code as a word
    n = ' '.join(STATE_WORDS.get(w, w) for w in n.split())
    n = ALIASES.get(n, n)
    n = NOISE.sub(' ', n)
    toks = sorted(set(w for w in n.split() if w))
    return ' '.join(toks)


def load_reference():
    if not os.path.exists(REF):
        return None
    return json.load(io.open(REF, encoding='utf8'))


def overlap(ours, theirs, n):
    """How many of our top n appear in their top n."""
    a = {norm(x) for x in ours[:n]}
    b = {norm(x) for x in theirs[:n]}
    return len(a & b)


def report(ranked, stream=sys.stdout):
    """Print the overlap summary. ranked is our list of school dicts, best first.

    Comparing our top 25 against one publisher's top 25 understates badly, because
    publishers split the universe into categories and we rank it as one table: our
    top 25 is mostly national universities, so it will never overlap a liberal arts
    top 25 no matter how good it is. So the headline numbers pool the categories.

      recognised   our top N that appears anywhere in any published list
      agreement    our top N that appears in some publisher's own top N
    """
    ref = load_reference()
    if ref is None:
        stream.write("validate_ranking: no data/reference_rankings.json, skipping\n")
        return None
    ours = [norm(s["name"]) for s in ranked]

    anywhere = set()
    for entry in ref["lists"].values():
        anywhere |= {norm(x) for x in entry["names"]}

    def published_top(n):
        s = set()
        for entry in ref["lists"].values():
            s |= {norm(x) for x in entry["names"][:n]}
        return s

    results = {}
    stream.write("\n  ranking check against %d published lists (%s)\n"
                 % (len(ref["lists"]), ref.get("captured", "")))
    stream.write("  %-12s %8s %8s %8s\n" % ("", "top 25", "top 50", "top 100"))
    rec, agr = [], []
    for n in (25, 50, 100):
        r = sum(1 for x in ours[:n] if x in anywhere) * 100 // n
        a = sum(1 for x in ours[:n] if x in published_top(n)) * 100 // n
        rec.append(r)
        agr.append(a)
    stream.write("  %-12s %7d%% %7d%% %7d%%   in any published list\n"
                 % ("recognised", rec[0], rec[1], rec[2]))
    stream.write("  %-12s %7d%% %7d%% %7d%%   in a published top N\n"
                 % ("agreement", agr[0], agr[1], agr[2]))
    results["recognised"], results["agreement"] = rec, agr

    # Ranking by selectivity is the cheap way to agree with everybody, and the one
    # thing this score refuses to do. A sharp move here means a weight change went
    # wrong, whatever the overlap numbers say.
    xs = [(s["sfn_score"], (s.get("profile", {}).get("admit_rate_pct") or {}).get("v"))
          for s in ranked]
    xs = [(a, b) for a, b in xs if b is not None]
    if len(xs) > 2:
        n = len(xs)
        mx = sum(a for a, _ in xs) / n
        my = sum(b for _, b in xs) / n
        sxy = sum((a - mx) * (b - my) for a, b in xs)
        sxx = sum((a - mx) ** 2 for a, _ in xs) ** .5
        syy = sum((b - my) ** 2 for _, b in xs) ** .5
        if sxx and syy:
            r = sxy / (sxx * syy)
            results["admit_corr"] = r
            stream.write("  score against admission rate: %+.2f "
                         "(strongly negative would mean a selectivity ranking)\n" % r)

    strangers = [s["name"] for s in ranked[:25] if norm(s["name"]) not in anywhere]
    if strangers:
        stream.write("  in our top 25 but in no published list: %s\n"
                     % ", ".join(strangers))
    return results


if __name__ == "__main__":
    print(__doc__)
