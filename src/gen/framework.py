"""Item generation framework.

The trainer needs thousands of items per category, and hand authoring cannot get
there. What it must never do is invent an answer key. So every generator here
works the same way:

  1. Draw parameters from a seeded RNG, so a build is reproducible.
  2. Compute the answer in Python. The key is never asserted, it is derived.
  3. Build each distractor from a NAMED misconception, and write the explanation
     of that misconception into the item. A distractor nobody would pick teaches
     nothing and inflates the difficulty estimate.
  4. Self-verify before emitting: exactly one choice equals the computed answer,
     all choices distinct, difficulty in range, no dashes, ids unique.

An item that fails any check is dropped, not patched, and the run reports how
many were dropped. Silence about a dropped item would be the same bug as an
invented key.
"""
import hashlib
import itertools
import json
import random
import re
from fractions import Fraction

DASH = re.compile(r"[–—]")


class ItemError(Exception):
    """This draw did not work; the runner tries again with new numbers.

    Raised by a schema's build() for a parameter combination that does not make a
    question: a square where the item is about area versus perimeter, a repeated root
    where the item asks for a sum. That is a deliberate filter and costs nothing.
    """


class AssemblyError(ItemError):
    """build() produced a question and make() could not turn it into an item.

    A different animal from the one above, and the reason it has its own name. The
    schema did its job; what it offered could not be assembled into choices this exam
    can show, because the wrong answers collapsed into each other or into the key, or
    because too few of them render the way the key does. That is a schema that cannot
    serve this exam, not a parameter draw that did not suit, and it is measured
    separately (INC-0092). It stays an ItemError so every existing caller still treats
    it as a draw to retry.
    """


# Words that end in s and are singular anyway, so a singular verb after one of them is
# correct. Not a dictionary: the ones that have actually turned up in these corpora.
SINGULAR_S = set("""gas mass class glass loss plus bus lens axis basis analysis crisis
series species campus census focus status surplus virus process access address business
witness progress success stress press illness fitness dress chaos bias news physics
mathematics statistics logistics""".split())


def plural_head(phrase):
    """Does this short noun phrase end in a plural noun?

    For a stored phrase that a template drops in front of a singular verb: "the cycle
    racks was responsible", "two independent reviews is needed". It reads the LAST word,
    which is the head of a short noun phrase like these, and it does not try to parse
    English. Applied to a field that lands anywhere other than a bare subject slot it is
    almost all false alarms, because a plural noun is usually not the subject: the sum of
    the solutions IS twelve, each of its players IS known, every one of the drivers WAS
    aware. So it is asserted of named fields, at the module that owns them, and never
    swept across item text (INC-0096).
    """
    words = re.sub(r"[^a-z ]", " ", str(phrase).lower()).split()
    if not words:
        return False
    w = words[-1]
    return (w.endswith("s") and not w.endswith(("ss", "us", "is"))
            and w not in SINGULAR_S)


SHAPE_INT = re.compile(r"^-?\d{1,3}(,\d{3})*$|^-?\d+$")
SHAPE_FRAC = re.compile(r"^-?\d+/\d+$")
SHAPE_DEC = re.compile(r"^-?\d*\.\d+$")
SHAPE_MONEY = re.compile(r"^\$")
SHAPE_PCT = re.compile(r"^-?\d+(\.\d+)?%$")


def shape(s):
    """What a choice looks like at a glance.

    A distractor that does not look like the answer is never chosen, which makes
    the item a free point and tells the adaptive model the student knows more
    than they do. So distractors are ranked by whether they match the answer's
    shape, and a mismatched one is used only when nothing better exists.
    """
    s = str(s)
    if SHAPE_MONEY.match(s):
        return "money"
    # A percent among bare integers is visibly the odd one out, so percents are their
    # own shape rather than falling through to text with every word answer.
    if SHAPE_PCT.match(s):
        return "pct"
    if SHAPE_FRAC.match(s):
        return "frac"
    if SHAPE_DEC.match(s):
        return "dec"
    if SHAPE_INT.match(s):
        return "int"
    return "text"


def frac(n, d):
    """A distractor that would divide by zero on this draw simply is not available."""
    if d == 0:
        return None
    return Fraction(n, d)


def num(x):
    """Format a number the way a test writer would write it."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return num(x.numerator)
        return "%d/%d" % (x.numerator, x.denominator)
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return num(int(round(x)))
        s = ("%.4f" % x).rstrip("0").rstrip(".")
        return s
    return str(x)


def money(x):
    """Dollar amounts with thousands separators and cents only when needed."""
    if isinstance(x, Fraction):
        x = float(x)
    if isinstance(x, float) and abs(x - round(x)) > 1e-9:
        return "$%s" % format(round(x, 2), ",.2f")
    return "$%s" % format(int(round(x)), ",d")


class Gen:
    """One problem schema.

    Subclasses set id, skill, section, sub, and implement build(rng) returning a
    dict with stem, answer (the value), distractors (list of (value, why)), expl,
    and optionally diff.
    """

    id = None
    skill = None
    section = None
    sub = None
    diff = 2
    type = "MC"
    fmt = staticmethod(num)

    def build(self, rng):
        raise NotImplementedError

    # -- emission ---------------------------------------------------------
    def make(self, rng, choices_n):
        spec = self.build(rng)
        # Before the distractors are chosen, because stem_numbers reads the stem and a
        # "1" that only existed as a unit coefficient is not a number the student saw.
        spec["stem"] = tidy_math(spec["stem"])
        fmt = spec.get("fmt") or self.fmt
        right = spec["answer"]
        pairs = list(spec["distractors"])
        seen = {fmt(right)}
        kept = []
        for val, why in pairs:
            if val is None:
                continue
            s = fmt(val)
            if s in seen:
                continue
            seen.add(s)
            kept.append((s, why))
        # There used to be a count of the surviving distractors here, failing the draw
        # before the stem's own numbers had been offered as candidates and without
        # regard to whether any of them render like the key. Both of those are settled
        # forty lines down, by a check that is stricter and better informed, so this one
        # could only reject draws the real check would have filled.
        want = shape(fmt(right))
        target_len = len(fmt(right))
        # A distractor a schema marks as required is the misconception the item exists to
        # test, and it goes in before anything is balanced. On the linear inequality
        # schema that is the same bound with the sign not flipped: without it the item
        # asks about a rule it never offers the student a chance to break, and because it
        # is the same string length as the key its absence is also what let the key be
        # uniquely the longest option on 43 percent of that schema's scored items.
        required = [p for p in kept if p[0] in set(map(fmt, spec.get("require") or []))]
        kept = [p for p in kept if p not in required]
        good = [p for p in kept if shape(p[0]) == want]
        rest = [p for p in kept if shape(p[0]) != want]
        # Characteristic errors skew long: an unsimplified sum or an undivided
        # product has more digits than the right answer. Left alone that makes the
        # correct choice reliably the SHORTEST one, and "never pick the longest"
        # then beats guessing without reading the question. Sorting by closeness is
        # not enough when every candidate is longer, so draw alternately from the
        # candidates shorter than the answer and those longer than it. The answer
        # then lands mid pack, and neither extreme carries information.
        # Always offer the stem's own numbers as candidates. They sit at the
        # answer's magnitude, so they populate the short side of the pool that
        # error derived distractors never reach.
        picked_texts = {p[0] for p in kept} | {fmt(right)}
        good = good + stem_numbers(spec["stem"], want, picked_texts)
        # Where the answer sits among the choices should carry no information. An
        # earlier version bracketed every item so the answer was never the extreme
        # value, which fixed one bias by creating another: among same shaped
        # numbers the largest value is also the longest string, so "never the
        # largest" became "never the longest" and still beat guessing. So aim for a
        # rank drawn uniformly instead: pick how many distractors should fall below
        # the answer, and fill from each side accordingly. Over a bank this leaves
        # the answer's position in both the value order and the length order flat.
        need = choices_n - 1 - len(required)
        if need < 0:
            raise AssemblyError("%s marks %d distractors required, more than the %d "
                                "slots this exam has" % (self.id, len(required), choices_n - 1))
        rv = as_value(fmt(right))
        if rv is not None:
            below, above, side = [], [], []
            for p in good:
                v = as_value(p[0])
                if v is None or v == rv:
                    side.append(p)
                elif v < rv:
                    below.append(p)
                else:
                    above.append(p)
        else:
            below = [p for p in good if len(p[0]) < target_len]
            above = [p for p in good if len(p[0]) > target_len]
            side = [p for p in good if len(p[0]) == target_len]
        want_below = rng.randint(0, need)
        picked = []
        for _ in range(min(want_below, len(below))):
            picked.append(below.pop(0))
        while len(picked) < need and above:
            picked.append(above.pop(0))
        # Whatever the preferred side could not supply comes from the other side,
        # then from the ties, so a thin pool still yields a full item.
        for bucket in (below, side, above):
            while len(picked) < need and bucket:
                picked.append(bucket.pop(0))
        good = picked
        # Every choice in a set must render the same way. A lone fraction among
        # integers is visibly the odd one out, and since the odd one out is almost
        # never the key, a mixed set leaks the answer on sight. Rather than pad with
        # a mismatched shape, drop the draw and let the runner try again.
        # There was a self.shape_misses counter here, incremented on every one of these
        # and read by nothing, in this file or any other. A number nobody reads is not
        # instrumentation, and this one was hiding the largest single loss in the bank:
        # one schema was discarding three draws in four (INC-0092). The count now comes
        # from the exception, which build_banks measures per schema per exam.
        if len(good) < need:
            raise AssemblyError(
                "%s could not fill %d same shaped distractors (%s)"
                % (self.id, need, want))
        kept = required + good[:need]
        # The correct answer lands in a random position; a generator that always
        # put it first would hand every student a free strategy.
        slot = rng.randrange(choices_n)
        texts = [t for t, _ in kept]
        texts.insert(slot, fmt(right))
        why_at = {}
        first_at = None
        k = 0
        for i in range(choices_n):
            if i == slot:
                continue
            why_at[i] = kept[k][1]
            if k == 0:
                first_at = i
            k += 1
        item = {
            "id": None,
            "section": spec.get("section", self.section),
            "type": spec.get("type", self.type),
            "sub": spec.get("sub", self.sub),
            "skill": spec.get("skill", self.skill),
            "diff": spec.get("diff", self.diff),
            "stem": spec["stem"],
            "choices": texts,
            "answer": slot,
            "expl": tidy_math(spec["expl"]),
            "wrong": tidy_math(spec.get("wrong") or self._wrong_line(why_at, first_at)),
            "gen": self.id,
        }
        # Data Insights items are read off a table or a set of sources rather than
        # out of the stem, so the rendered source travels with the item. domain and
        # qskill drive the half weight rating update the engine applies to these.
        for extra in ("passageHtml", "domain", "qskill", "answerType"):
            if spec.get(extra):
                item[extra] = spec[extra]
        self.verify(item, right, choices_n, fmt)
        return item

    def _wrong_line(self, why_at, first_at):
        """Name the misconception behind the distractor the schema ranked first."""
        if not why_at or first_at is None:
            return ""
        return "Choice %s comes from %s" % ("ABCDEF"[first_at], why_at[first_at])

    def verify(self, item, right, choices_n, fmt=None):
        fmt = fmt or self.fmt
        c = item["choices"]
        if len(c) != choices_n:
            raise ItemError("%s has %d choices, expected %d" % (self.id, len(c), choices_n))
        if len(set(c)) != len(c):
            raise ItemError("%s has duplicate choices: %r" % (self.id, c))
        if c[item["answer"]] != fmt(right):
            raise ItemError("%s key does not match computed answer" % self.id)
        if item["diff"] not in (1, 2, 3, 4, 5):
            raise ItemError("%s difficulty %r" % (self.id, item["diff"]))
        blob = json.dumps(item)
        if DASH.search(blob):
            raise ItemError("%s contains an em or en dash" % self.id)
        # A coefficient of one or zero left in, or a sign pair a person would not write.
        # tidy_math fixes what it is given; this is what proves it was given everything,
        # including a choice or a rendered source the pass does not reach (INC-0078).
        for k in ("stem", "expl", "wrong"):
            m = _MATH_BAD.search(str(item.get(k) or ""))
            if m:
                raise ItemError("%s %s has unwritten notation %r" % (self.id, k, m.group(0)))
        for ch in item["choices"]:
            m = _MATH_BAD.search(str(ch))
            if m:
                raise ItemError("%s choice has unwritten notation %r" % (self.id, m.group(0)))
        for k in ("stem", "expl"):
            if not item[k] or not str(item[k]).strip():
                raise ItemError("%s missing %s" % (self.id, k))


# Notation the schemas got wrong in eight places by each formatting a term where it stood
# (INC-0078). Every rule here is a convention of writing rather than of arithmetic, so no
# check on the computed answer could see any of them, and the give away was identical
# output in unrelated files: that is one missing function, not eight mistakes.
_MATH_FIXES = (
    # "8i + -4i" is a machine adding a negative, not a person writing algebra.
    (re.compile(r"\+ -"), "- "),
    # A coefficient of zero deletes its whole term: "y = 0x + 4" is "y = 4".
    (re.compile(r"(?<=[a-z0-9)]) [+] 0[xyi]\b"), ""),
    (re.compile(r"(?<=[a-z0-9)]) - 0[xyi]\b"), ""),
    (re.compile(r"(?<![0-9.])0[xyi] \+ "), ""),
    (re.compile(r"(?<![0-9.])0[xyi] - "), "-"),
    # A coefficient of one is not written.
    (re.compile(r"(?<![0-9.])1(?=[xyi]\b)"), ""),
    # A subtracted negative takes brackets: "2 - -1" is "2 - (-1)".
    (re.compile(r"- -(\d)"), r"- (-\1)"),
)
# What must not survive the pass, checked on the way out so a schema that formats a term
# by hand in future fails here instead of shipping.
_MATH_BAD = re.compile(r"(?<![0-9.])[01][xyi]\b|\+ -\d|(?<!\()-\s-\d")


def tidy_math(t):
    """Render algebraic notation the way a person writes it."""
    t = str(t)
    for pat, rep in _MATH_FIXES:
        t = pat.sub(rep, t)
    return t


def upfirst(t):
    """Raise the first character and touch nothing else.

    The standard library's string method of a similar name also lower cases every other
    character, which is right for a fragment of ordinary prose and destroys any fragment
    containing a name. The generators used it twenty one times and shipped 180 items
    reading "The fenwick track is the only one in the county", 70 of them as the key,
    two lines under a stem that spells it correctly (INC-0076). src/build.py now fails
    if that method appears anywhere under src/gen, so this is the only way to do it.
    """
    t = str(t)
    return t[:1].upper() + t[1:]


WH = ("what", "why", "which", "when", "how", "where", "whether")


def check_clause_splice(label, texts, not_clauses):
    """Refuse a rendered sentence whose That or Whether is followed by a non clause.

    A corpus field is written against the one sentence its author had in mind and carries
    no record of the grammatical shape it is in. Both slots take a str, so nothing
    upstream can see a mismatch. It happened twice in one file. A goal, stored as a bare
    infinitive for "X intends to <goal>", went into a subject slot and shipped 160 items
    saying "That shorten the time taken to settle a claim is the most urgent ..."
    (INC-0074). A check, stored as a wh clause for "Establish <check>, and ...", went
    after Whether and shipped 277, every key of its schema, saying "Whether what share of
    the traffic stops there at all is what the measure would change" (INC-0075).

    The guard written for the first could only see infinitives and let the second
    through, one screen away in the same file. So this one is stated over the class
    rather than over the token that was wrong first, and it tests two things:

      provenance   nothing in not_clauses, the fields the corpus stores in a shape that
                   is not a clause, may follow a sentence initial That or Whether.
      shape        no sentence initial That or Whether may be followed by a wh word,
                   which no grammatical English sentence does.

    The second is what makes it general: it needs no list, and it fires on a field the
    author of this function never saw.
    """
    for t in texts:
        for opener in sentence_starts(str(t)):
            for word in ("That ", "Whether "):
                if not opener.startswith(word):
                    continue
                rest = opener[len(word):]
                if rest.split(" ")[0].lower().strip(",") in WH:
                    raise ItemError("%s opens a sentence with %r plus a wh word: %r"
                                    % (label, word.strip(), opener[:90]))
                for bad in not_clauses:
                    if bad and rest.startswith(bad):
                        raise ItemError(
                            "%s splices a non clause corpus field after %r: %r"
                            % (label, word.strip(), (word + bad)[:90]))


def sentence_starts(t):
    """Every position in t where a sentence begins, as the text from there on."""
    out = []
    if t[:1].strip():
        out.append(t[:200])
    i = None
    for j, ch in enumerate(t):
        if ch in ".?!\n":
            i = None
        elif i is None and ch not in " \n":
            i = j
            if j:
                out.append(t[j:j + 200])
    return out


STEM_NUM = re.compile(r"-?\d+(?:/\d+)?")


UNIT_NUM = re.compile(r"^(\$?-?[\d,]+(?:\.\d+)?(?:/\d+)?) [a-z][a-z ]*$")


def as_value(t):
    """Numeric value of a rendered choice, or None if it is not a number.

    A trailing unit word is stripped first. "20 percent" is a number as far as a student
    guessing is concerned, and without this the balancer fell back to the character count
    for the whole percent change schema, which tracks the digits rather than the value
    (INC-0079). Two choices with different units and the same number compare equal here,
    which is harmless: this decides only which side of the key a candidate sits on.
    """
    t = str(t).strip()
    m = UNIT_NUM.match(t)
    if m:
        t = m.group(1)
    t = t.replace(",", "").replace("$", "").rstrip("%")
    try:
        if "/" in t:
            n, d = t.split("/", 1)
            return Fraction(int(n), int(d))
        if "." in t:
            return Fraction(t)
        return Fraction(int(t))
    except (ValueError, ZeroDivisionError):
        return None


def stem_numbers(stem, want_shape, exclude, limit=6):
    """Values lifted straight out of the question.

    Picking a number out of the stem instead of computing one is among the most
    common things a rushed student does, so these are real distractors and not
    filler. They also fix a structural problem: errors like a dropped sign or an
    unsimplified fraction always render LONGER than a clean answer, so a bank
    built only from them lets a student score above chance by never choosing the
    longest option. Numbers from the stem sit at the same magnitude as the answer,
    which puts the answer back in the middle of the pack.
    """
    out = []
    for m in STEM_NUM.finditer(stem):
        t = m.group(0)
        if shape(t) != want_shape or t in exclude:
            continue
        if t in [o[0] for o in out]:
            continue
        out.append((t, "a value copied straight from the question rather than computed."))
        if len(out) >= limit:
            break
    return out


def balance(rng, right, pool, need, own=(), k=0, target=None):
    """Choose `need` wrong answers so the key's LENGTH RANK is drawn uniformly.

    For a worded answer the only thing a guesser can measure without reading is length, so
    a key that is reliably the longest option is a free point. The numeric path solves this
    by targeting a uniform value rank; this is the same idea for text.

    It samples rather than sorts, because sorting is deterministic: an earlier version
    picked the same few subsets for a given pool, which balanced the lengths and destroyed
    the variety that having more wrong answer types than slots was there to provide. So it
    draws random subsets, keeps the first whose key rank matches a target drawn uniformly,
    and falls back to the closest it saw. Both properties survive.

    `own` are wrong answers about the same thing as the key, and at least `k` of them are
    offered on every draw (INC-0117). Which ones is chosen with the rank in mind, because
    forcing particular options pins it: two near misses that are both longer than the key
    make it impossible for the key to be the longest, and the ranks that remain fill up.
    Any `own` not chosen stays available to the rest of the draw. With no `own` the draw
    is exactly what it always was, so every other schema produces what it produced.

    `target` fixes the rank instead of drawing it. A schema that makes one item per
    passage ships few items, and a uniform draw over few items can still pile up on one
    rank: 12 of the 27 GRE main idea keys sat at the middle rank on the first build of
    that schema, although 3,000 draws spread evenly, and 7 of 14 LSAT caveat keys did the
    same after two passages were added (INC-0122). Such a schema assigns each passage a
    rank it can build (see buildable_ranks), so the bank that ships is even, not only the
    process that made it. Without a target, nothing changes for any other schema.
    """
    own = list(own)
    if k > len(own) or len(pool) + len(own) < need:
        raise ItemError("balance needs %d wrong answers, pool has %d" % (need, len(pool) + len(own)))
    if k:
        return _balance_own(rng, right, pool, need, own, k, target)
    target = rng.randint(0, need) if target is None else target
    keylen = len(str(right))
    best, best_gap = None, None
    for _ in range(40):
        pick = rng.sample(pool, need)
        rank = sum(1 for p in pick if len(str(p[0])) < keylen)
        if rank == target:
            return pick
        gap = abs(rank - target)
        if best_gap is None or gap < best_gap:
            best, best_gap = pick, gap
    return best


def _fits(first, own, pool, need, k, t, short):
    """Whether forcing the own options `first` leaves enough shorter and longer wrong
    answers to put the key at rank t. Returns (shorter, longer, forced shorter) or None.
    One test, used by _balance_own to build a draw and by buildable_ranks to say which
    ranks a draw can reach, so the two cannot disagree."""
    ns = sum(1 for o in first if short(o))
    if ns > t or k - ns > need - t:
        return None
    rest = [w for w in own if w not in first] + list(pool)
    s_ = [w for w in rest if short(w)]
    l_ = [w for w in rest if not short(w)]
    if len(s_) < t - ns or len(l_) < need - t - (k - ns):
        return None
    return s_, l_, ns


def buildable_ranks(right, pool, need, own=(), k=0):
    """The key length ranks balance() can reach from these options, as a list.

    A key longer than every option it can be offered with can only be the longest, and
    one shorter than all of them only the shortest. A schema that assigns ranks has to
    choose among these, and a passage with few of them is the one that piles the ranks up
    (INC-0122). Options are (text, note) pairs, as balance() takes them."""
    keylen = len(str(right))
    short = lambda w: len(str(w[0])) < keylen
    out = []
    for t in range(need + 1):
        if k:
            if any(_fits(first, own, pool, need, k, t, short) is not None
                   for first in itertools.combinations(own, k)):
                out.append(t)
        elif _fits((), (), list(own) + list(pool), need, 0, t, short) is not None:
            out.append(t)
    return out


def _balance_own(rng, right, pool, need, own, k, target=None):
    """balance() when some wrong answers must come from `own` (INC-0117).

    Built rather than sampled. Sampling forty random subsets and keeping one whose key
    rank hits the target works when every subset is possible; with k options forced from
    a short list, the extreme ranks need a particular combination that forty draws rarely
    find, the fallback lands on the middle, and the middle rank fills up. So the target
    is drawn from the ranks that can actually be built, and the draw is then assembled to
    hit it: the own options first, then the shorter and longer wrong answers the target
    calls for.
    """
    keylen = len(str(right))
    short = lambda w: len(str(w[0])) < keylen

    def assemble(first, t):
        fit = _fits(first, own, pool, need, k, t, short)
        if fit is None:
            return None
        s_, l_, ns = fit
        return list(first) + rng.sample(s_, t - ns) + rng.sample(l_, need - t - (k - ns))

    def build(t):
        # An assigned rank is one buildable_ranks found a way to build, so every choice of
        # the forced options is tried before giving up on it. Twelve random picks could
        # miss the one that works and fall back to a random rank, which undoes the
        # assignment (INC-0122). A drawn rank keeps the draw it always had.
        if target is not None:
            firsts = list(itertools.combinations(own, k))
            rng.shuffle(firsts)
            for first in firsts:
                pick = assemble(first, t)
                if pick is not None:
                    return pick
            return None
        for _ in range(12):
            pick = assemble(rng.sample(own, k), t)
            if pick is not None:
                return pick
        return None

    targets = list(range(need + 1))
    rng.shuffle(targets)
    if target is not None:
        targets.remove(target)
        targets.insert(0, target)
    for t in targets:
        pick = build(t)
        if pick is not None:
            return pick
    raise ItemError("balance could not assemble %d wrong answers with %d of its own" % (need, k))


def canon(item):
    """Dedup key: the schema, the stem, and the choices.

    The choices belong in the key. Some schemas put the whole of what varies into
    the options rather than the stem, a punctuation item whose stem is just "which
    choice conforms" being the clearest case, and keying on the stem alone made
    every one of those look like a repeat of the first. What the key is meant to
    catch is the same DRAW appearing twice, and a draw is the stem plus what it
    offers.
    """
    body = item["gen"] + "|" + re.sub(r"\s+", " ", item["stem"]).strip()
    # SORTED, because the answer's position is randomised on every draw and a reshuffle of
    # the same five options is the same question, not a new one. Keying on the order let a
    # schema with a small scenario pool "fill" a category by serving one question over and
    # over with its options rearranged, which is worse than being short: it looks full.
    body += "|" + "|".join(sorted(str(c) for c in item.get("choices", ())))
    body += "|" + "|".join(str(c) for c in item.get("columns", ()))
    # The source counts for a question READ off it: two share of total questions over
    # different tables are different questions. It must NOT count for a question about the
    # design of the study, where the answer is the same whatever the numbers say, so a
    # generator can drop it. Without that, a design question appears to produce hundreds of
    # items when it has produced one question with the figures changed underneath it.
    if not item.get("canon_ignores_source"):
        body += "|" + re.sub(r"\s+", " ", item.get("passageHtml", "")).strip()
    # A reading item is identified by its passage and the question asked of it. Which four
    # of the passage's other sentences happen to be offered alongside the key does NOT make
    # a second question: a student who has answered one has answered the other. Without
    # this, four passages produced five hundred "distinct" stated idea items, which is the
    # same inflation the sorted choice key was added to stop.
    if item.get("canon_ignores_choices"):
        body = item["gen"] + "|" + re.sub(r"\s+", " ", item["stem"]).strip()
        body += "|" + str(item.get("passageId") or "")
    return hashlib.sha1(body.encode("utf-8")).hexdigest()


def run(gens, target, choices_n, prefix, seed=20260916, start=1, existing=None):
    """Fill to a target count, cycling generators rather than quota-ing each one.

    A schema with a small parameter space runs dry long before a schema with a
    large one. Cycling lets the roomy schemas cover for the cramped ones, so the
    category still reaches its target, and the per schema report shows which
    schemas are carrying the load and need widening.
    """
    rng = random.Random(seed)
    out = []
    seen = set(existing or ())
    dropped = {"dup": 0, "error": 0, "math": 0}
    errors = []
    made = {g.id: 0 for g in gens}
    exhausted = set()
    n = start
    # A schema is retired after this many consecutive duplicates: its space is spent.
    STALE = 400
    stale = {g.id: 0 for g in gens}
    guard = 0
    while len(out) < target and len(exhausted) < len(gens):
        guard += 1
        if guard > target * 200 + 20000:
            errors.append("gave up after %d attempts with %d of %d" % (guard, len(out), target))
            break
        for g in gens:
            if len(out) >= target or g.id in exhausted:
                continue
            try:
                it = g.make(rng, choices_n)
            except ItemError as e:
                dropped["error"] += 1
                if len(errors) < 12 and str(e) not in errors:
                    errors.append(str(e))
                continue
            except ArithmeticError as e:
                dropped["math"] += 1
                msg = "%s raised %s: %s" % (g.id, type(e).__name__, e)
                if msg not in errors:
                    errors.append(msg)
                continue
            key = canon(it)
            if key in seen:
                dropped["dup"] += 1
                stale[g.id] += 1
                if stale[g.id] >= STALE:
                    exhausted.add(g.id)
                continue
            stale[g.id] = 0
            seen.add(key)
            it["id"] = "%s%04d" % (prefix, n)
            n += 1
            out.append(it)
            made[g.id] += 1
            # A schema may stop short of the category's target on purpose (item_cap),
            # when its question is one of several the category covers and filling the
            # target from it alone would misrepresent the category. The category then
            # reports itself under target, as any short category does.
            item_cap = getattr(g, "item_cap", None)
            if item_cap and made[g.id] >= item_cap:
                exhausted.add(g.id)
    if len(out) < target:
        errors.append("filled %d of %d; widen the exhausted schemas: %s"
                      % (len(out), target, ", ".join(sorted(exhausted)) or "none"))
    return out, dropped, errors, made


JS_ESC = {"\\": "\\\\", "'": "\\'", "\n": "\\n", "\r": "", "\t": " "}


def jstr(s):
    return "'" + "".join(JS_ESC.get(ch, ch) for ch in str(s)) + "'"


# Every field to_js writes, and every field it deliberately does not. A field a
# generator sets that is in neither list fails the build, because the alternative is
# what happened to passage: set on the item, read by the app, named nowhere here, and so
# correct in memory and absent from the file that ships (INC-0099). Adding a line to
# to_js means adding its name here; forgetting to is a loud failure rather than a quiet
# one, which is the direction this should fail in.
EMITTED_FIELDS = {
    "id", "section", "type", "sub", "skill", "diff", "gen", "answerType",
    "passageHtml", "passage", "passageId", "columns", "domain", "qskill",
    "stem", "choices", "answer", "expl", "wrong", "statements",
}
# Build time only: the two canon flags tell the dedup key what to ignore while the bank
# is being assembled, and nothing in the app reads them.
BUILD_ONLY_FIELDS = {"canon_ignores_source", "canon_ignores_choices"}


def to_js(items, const, header):
    """Emit a bank file in the same shape as the hand written banks.

    Every field the app reads has to be named here, and one that is not named is lost
    between a correct item in memory and the file that ships. passage was not named for
    as long as generated reading items have existed, so 280 of them reached the site
    with nothing to read (INC-0099). A passage is written once as a constant and
    referenced by name, which is what the hand written banks do, because the alternative
    is a 300 word passage repeated on every question asked about it.
    """
    unknown = set()
    for it in items:
        unknown |= {k for k, v in it.items()
                    if v is not None and v != "" and v != [] and v != {}}
    unknown -= EMITTED_FIELDS | BUILD_ONLY_FIELDS
    if unknown:
        raise SystemExit(
            "framework.to_js: %s sets field(s) this emitter does not write and has not "
            "been told to skip: %s. A field the app reads has to be written here; one "
            "that only matters during the build goes in BUILD_ONLY_FIELDS."
            % (const, ", ".join(sorted(unknown))))
    lines = [header.rstrip()]
    pvar = {}
    for it in items:
        text = it.get("passage")
        if text and text not in pvar:
            pvar[text] = "%s_P%d" % (const, len(pvar))
            lines.append("const %s = %s;" % (pvar[text], jstr(text)))
    if pvar:
        lines.append("")
    lines.append("const %s = [" % const)
    for it in items:
        parts = [
            "id:%s" % jstr(it["id"]),
            "section:%s" % jstr(it["section"]),
            "type:%s" % jstr(it["type"]),
            "sub:%s" % jstr(it["sub"]),
            "skill:%s" % jstr(it["skill"]),
            "diff:%d" % it["diff"],
            "gen:%s" % jstr(it["gen"]),
        ]
        if it.get("answerType"):
            parts.append("answerType:%s" % jstr(it["answerType"]))
        if it.get("passageHtml"):
            parts.append("passageHtml:%s" % jstr(it["passageHtml"]))
        if it.get("passage"):
            parts.append("passage:%s" % pvar[it["passage"]])
        # The app's game pools filter on passageId to keep passage based items out of
        # views that show no passage, so an item that loses it does not just lose its
        # text, it turns up where there was never anywhere to put it.
        if it.get("passageId"):
            parts.append("passageId:%s" % jstr(it["passageId"]))
        if it.get("columns"):
            parts.append("columns:[%s]" % ",".join(jstr(c) for c in it["columns"]))
        # Data Insights items carry the underlying quant skill and whether the item is
        # mathematical. The engine uses qskill for a half weight rating update and for
        # pool filtering, so leaving it out would quietly change how the app learns.
        for extra in ("domain", "qskill"):
            if it.get(extra):
                parts.append("%s:%s" % (extra, jstr(it[extra])))
        head = "{" + ",".join(parts) + ","
        body = " stem:%s," % jstr(it["stem"])
        if it.get("answerType") == "spr":
            ch = " answer:%s," % jstr(it["answer"])
        elif isinstance(it["answer"], (list, tuple)):
            ch = " choices:[%s],answer:[%s]," % (
                ",".join(jstr(c) for c in it["choices"]),
                ",".join(str(int(i)) for i in it["answer"]),
            )
        else:
            ch = " choices:[%s],answer:%d," % (
                ",".join(jstr(c) for c in it["choices"]),
                it["answer"],
            )
        tail = " expl:%s" % jstr(it["expl"])
        if it.get("wrong"):
            tail += ",\n wrong:%s" % jstr(it["wrong"])
        lines.append(head + "\n" + body + "\n" + ch + "\n" + tail + "},")
    lines.append("];")
    return "\n".join(lines) + "\n"


class FixedGen(Gen):
    """A schema whose choices are fixed and whose work is deciding which one is right.

    Data Sufficiency is the case this exists for: the five options never change, so
    there are no distractors to invent, and the entire question is which option the
    two statements actually justify. build() returns choices and an answer index,
    and the subclass is responsible for having DERIVED that index rather than
    decided it.
    """

    def make(self, rng, choices_n):
        spec = self.build(rng)
        choices = list(spec["choices"])
        ans = spec["answer"]
        if not isinstance(ans, int) or not 0 <= ans < len(choices):
            raise ItemError("%s answer index %r out of range" % (self.id, ans))
        item = {
            "id": None,
            "section": spec.get("section", self.section),
            "type": spec.get("type", self.type),
            "sub": spec.get("sub", self.sub),
            "skill": spec.get("skill", self.skill),
            "diff": spec.get("diff", self.diff),
            "stem": spec["stem"],
            "choices": choices,
            "answer": ans,
            "expl": spec["expl"],
            "wrong": spec.get("wrong", ""),
            "gen": self.id,
        }
        for k in ("qskill", "domain", "answerType"):
            if spec.get(k):
                item[k] = spec[k]
        if len(set(choices)) != len(choices):
            raise ItemError("%s has duplicate choices" % self.id)
        if item["diff"] not in (1, 2, 3, 4, 5):
            raise ItemError("%s difficulty %r" % (self.id, item["diff"]))
        if DASH.search(json.dumps(item)):
            raise ItemError("%s contains an em or en dash" % self.id)
        if not item["stem"] or not item["expl"]:
            raise ItemError("%s missing stem or explanation" % self.id)
        return item


def sufficiency(domain, question, s1, s2):
    """Decide a Data Sufficiency item by enumeration instead of by argument.

    domain is an iterable of candidate assignments. question maps an assignment to
    the answer being asked for; s1 and s2 are the statements as predicates. A
    statement is sufficient when every assignment it admits yields the same answer,
    which is exactly the definition, checked rather than asserted. Reasoning about
    sufficiency by hand is where these items go wrong, so nothing here reasons.

    Returns the index into the standard five options, or None when the item is
    degenerate (a statement admits nothing at all, so the premises contradict).
    """
    cases = list(domain)
    a1 = {question(c) for c in cases if s1(c)}
    a2 = {question(c) for c in cases if s2(c)}
    both = {question(c) for c in cases if s1(c) and s2(c)}
    if not a1 or not a2 or not both:
        return None
    suf1, suf2, sufb = len(a1) == 1, len(a2) == 1, len(both) == 1
    if suf1 and suf2:
        return 3
    if suf1:
        return 0
    if suf2:
        return 1
    if sufb:
        return 2
    return 4
