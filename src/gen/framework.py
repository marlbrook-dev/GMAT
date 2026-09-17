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
import json
import random
import re
from fractions import Fraction

DASH = re.compile(r"[–—]")


class ItemError(Exception):
    pass


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
        if len(kept) < choices_n - 1:
            raise ItemError("only %d distinct distractors for %s" % (len(kept), self.id))
        want = shape(fmt(right))
        target_len = len(fmt(right))
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
        need = choices_n - 1
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
        if len(good) < choices_n - 1:
            self.shape_misses = getattr(self, "shape_misses", 0) + 1
            raise ItemError(
                "%s could not fill %d same shaped distractors (%s)"
                % (self.id, choices_n - 1, want))
        kept = good[: choices_n - 1]
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
            "expl": spec["expl"],
            "wrong": spec.get("wrong") or self._wrong_line(why_at, first_at),
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
        for k in ("stem", "expl"):
            if not item[k] or not str(item[k]).strip():
                raise ItemError("%s missing %s" % (self.id, k))


STEM_NUM = re.compile(r"-?\d+(?:/\d+)?")


def as_value(t):
    """Numeric value of a rendered choice, or None if it is not a bare number."""
    t = str(t).replace(",", "").replace("$", "").rstrip("%")
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
    body += "|" + "|".join(str(c) for c in item.get("choices", ()))
    body += "|" + "|".join(str(c) for c in item.get("columns", ()))
    body += "|" + re.sub(r"\s+", " ", item.get("passageHtml", "")).strip()
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
    if len(out) < target:
        errors.append("filled %d of %d; widen the exhausted schemas: %s"
                      % (len(out), target, ", ".join(sorted(exhausted)) or "none"))
    return out, dropped, errors, made


JS_ESC = {"\\": "\\\\", "'": "\\'", "\n": "\\n", "\r": "", "\t": " "}


def jstr(s):
    return "'" + "".join(JS_ESC.get(ch, ch) for ch in str(s)) + "'"


def to_js(items, const, header):
    """Emit a bank file in the same shape as the hand written banks."""
    lines = [header.rstrip(), "const %s = [" % const]
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
