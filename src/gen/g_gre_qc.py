"""GRE Quantitative Comparison.

ETS lists Quantitative Comparison first among the four types of question on the
Quantitative Reasoning measure, and the GRE trainer had 11 of them, all hand written,
because its generated quantitative items are SAT schemas with five choices. These schemas
write the type directly.

A comparison has four fixed answers, so there are no distractors to invent; the whole
question is which relationship holds, and that is never asserted here. It is decided:

  With no variable, both quantities are computed exactly, as fractions or integers, and
  compared.

  With a variable that the condition limits to a few integers, every allowed value is
  tried, so the answer is the enumeration and not a sample of it.

  With a real variable, A minus B is written as a product of factors whose roots and
  poles are listed with it. Between consecutive roots and poles the difference cannot
  change sign, so one exact test value in each piece of the condition's interval decides
  the sign there, and a root inside the interval is a value where the two are equal. The
  listed factorization is checked against the two quantities at a dozen exact values
  before it is used, so a wrong list of roots fails the draw instead of the student.

"Cannot be determined" is only ever the answer when the item's own explanation can name
two allowed values that order the quantities differently, and the explanation names them.
"""
from collections import Counter
from fractions import Fraction as F

from framework import FixedGen, ItemError

# The same four answers, in the same order, as the hand written comparisons in
# bank_gre_quant.js; the engine shows a comparison's choices in this order.
QC_CHOICES = ["Quantity A is greater", "Quantity B is greater",
              "The two quantities are equal",
              "The relationship cannot be determined from the information given"]
LETTER = "ABCD"
# How an explanation ends. No letter: a comparison's letters sit beside "Quantity A" and
# "Quantity B", and "the answer is A" read beside them invites the wrong one.
ENDING = ["Quantity A is greater", "Quantity B is greater", "the two quantities are equal",
          "the relationship cannot be determined from the information given"]
CD = '"cannot be determined"'


def word(v):
    """A number as the trainer prints one: integers plain, other fractions as a over b."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return "%d/%d" % (v.numerator, v.denominator)


def order(a, b):
    """0 when a is greater, 1 when b is, 2 when they are equal."""
    return 0 if a > b else 1 if b > a else 2


def witnesses(wit):
    """Two cases that order the quantities differently, preferring one each way."""
    if 0 in wit and 1 in wit:
        return [(0, wit[0]), (1, wit[1])]
    return list(wit.items())[:2]


def relation(pairs):
    """The answer index over every case the item allows, and a witness for each order seen.

    pairs is a list of (case, a, b) covering EVERY admissible case, never a sample. Returns
    (index, {order: case}).
    """
    seen = {}
    for case, a, b in pairs:
        seen.setdefault(order(a, b), case)
    if not seen:
        raise ItemError("no case satisfies the condition")
    if len(seen) == 1:
        return next(iter(seen)), seen
    return 3, seen


class Contradiction(Exception):
    """A decided comparison that a random allowed value contradicts. Not an ItemError: a
    draw that fails this is a wrong decision procedure, and the build must stop on it."""


def falsify(ans, points, fa, fb, what):
    """Raise Contradiction when any point orders the quantities against a decided answer."""
    if ans == 3:
        return
    for t in points:
        if order(fa(t), fb(t)) != ans:
            raise Contradiction("%s decided %s, but x = %s gives %s against %s"
                                % (what, LETTER[ans], t, fa(t), fb(t)))


def sample_in(rng, lo, hi, n):
    """n exact values strictly inside (lo, hi), unbounded ends allowed."""
    out = []
    for _ in range(n):
        a = lo if lo is not None else (hi - 50 if hi is not None else F(-50))
        b = hi if hi is not None else (lo + 50 if lo is not None else F(50))
        t = a + (b - a) * F(rng.randint(1, 9999), 10000)
        if (lo is None or t > lo) and (hi is None or t < hi):
            out.append(t)
    return out


class QCBase(FixedGen):
    section = "Q"
    type = "QC"
    sub = "Quantitative comparison"
    item_cap = 300

    def __init__(self):
        # Thin whichever answer is running ahead, as the Data Sufficiency schemas do and for
        # the same reason: what a comparison comes to falls out of its parameters, and a
        # schema whose items mostly say "Quantity A" teaches a student to say it unread
        # (INC-0081). The count belongs to the rng it was drawn from (INC-0123).
        self._rng, self._seen = None, Counter()

    def make(self, rng, choices_n):
        if rng is not self._rng:
            self._rng, self._seen = rng, Counter()
        it = super().make(rng, choices_n)
        a = it["answer"]
        total = sum(self._seen.values())
        if total >= 40:
            share = self._seen[a] / float(total)
            even = 1.0 / max(1, len(self._seen))
            if share > even and rng.random() < min(0.9, (share - even) / share):
                raise ItemError("%s is thinning %s, which is at %d percent"
                                % (self.id, LETTER[a], round(100 * share)))
        self._seen[a] += 1
        return it

    def assemble(self, cond, qa, qb, ans, expl, wrong, diff):
        stem = ("%s\n\n" % cond if cond else "") + "Quantity A: %s\nQuantity B: %s" % (qa, qb)
        return {"stem": stem, "choices": QC_CHOICES, "answer": ans, "diff": diff,
                "expl": "%s So %s." % (expl, ENDING[ans]),
                "wrong": wrong}


# ---------------------------------------------------------------- arithmetic

class QCPercentSwap(QCBase):
    """p percent of q against another percent of another number, often its own swap."""
    id = "gre_qc_percent"
    skill = "gre_arith"
    sub = "Quantitative comparison, percents"

    def build(self, rng):
        p = rng.choice([12, 15, 18, 20, 24, 25, 30, 35, 40, 45, 60, 75])
        q = rng.choice([16, 20, 36, 40, 48, 50, 60, 64, 80, 120, 150, 240])
        if p == q:
            raise ItemError("same number twice")
        kind = rng.choice(["swap", "swap", "near", "near"])
        if kind == "swap":
            r, s = q, p
        else:
            r = p + rng.choice([-10, -5, 5, 10])
            s = q + rng.choice([-20, -10, 10, 20])
            if r <= 0 or s <= 0 or (r, s) == (q, p):
                raise ItemError("not a usable pair")
        a, b = F(p * q, 100), F(r * s, 100)
        ans = order(a, b)
        expl = ("%d percent of %d is %d times %d over 100, which is %s, and %d percent of %d "
                "is %d times %d over 100, which is %s."
                % (p, q, p, q, word(a), r, s, r, s, word(b)))
        if kind == "swap":
            wrong = ("Choosing the quantity with the larger percent misses that p percent of "
                     "q and q percent of p are the same product, pq over 100.")
        else:
            wrong = ("Comparing the percents alone, or the base numbers alone, ignores that "
                     "each quantity is a product of the two. Multiply before comparing.")
        return self.assemble("", "%d percent of %d" % (p, q), "%d percent of %d" % (r, s),
                             ans, expl, wrong, 2 if kind == "swap" else 3)


class QCPowers(QCBase):
    """Two powers with different bases and exponents, compared through a common exponent."""
    id = "gre_qc_powers"
    skill = "gre_arith"
    sub = "Quantitative comparison, exponents"

    def build(self, rng):
        g = rng.choice([5, 6, 8, 10, 12])
        # A base that is itself a power, written both ways, is the same number: 8 to the
        # 10 is 2 to the 30. That is where "equal" comes from.
        powers = {4: (2, 2), 8: (2, 3), 9: (3, 2), 16: (2, 4), 25: (5, 2), 27: (3, 3)}
        if rng.random() < 0.3:
            x = rng.choice(sorted(powers))
            base, k = powers[x]
            sides = [(x, g), (base, k * g)]
            rng.shuffle(sides)
            (a, m), (b, n) = sides
            ans = 2
            expl = ("%d is %d to the power of %d, so %d to the power of %d is %d to the power "
                    "of %d times %d, which is %d to the power of %d. The two are the same "
                    "number." % (x, base, k, x, g, base, k, g, base, k * g))
        else:
            x, y = rng.sample([2, 3, 4, 5, 8, 9, 16, 25, 27], 2)
            a, ka = powers.get(x, (x, 1))
            b, kb = powers.get(y, (y, 1))
            m, n = ka * g, kb * g
            if ka == kb:
                raise ItemError("same exponent on both sides is not a comparison worth asking")
            ans = order(a ** m, b ** n)
            if ans != order(x, y):
                raise ItemError("rewriting did not preserve the order")

            def as_g(base, k, v, e):
                if k == 1:
                    return "%d to the power of %d is already a power with exponent %d" % (base, e, g)
                return ("%d to the power of %d is (%d to the power of %d) to the power of %d, "
                        "which is %d to the power of %d" % (base, e, base, k, g, v, g))
            expl = ("Write both with the exponent %d. %s, and %s. The same positive exponent "
                    "keeps the order, so compare %d with %d."
                    % (g, as_g(a, ka, x, m), as_g(b, kb, y, n), x, y))
        if (a, m) == (b, n):
            raise ItemError("same power twice")
        wrong = ("Comparing the exponents alone, or the bases alone, is the trap. There are "
                 "no variables here, so %s is never right; rewrite both with one exponent."
                 % CD)
        return self.assemble("", "%d to the power of %d" % (a, m),
                             "%d to the power of %d" % (b, n), ans, expl, wrong, 3)


class QCIntegerRange(QCBase):
    """An integer limited to a short range, with a linear and a quadratic quantity."""
    id = "gre_qc_intrange"
    skill = "gre_arith"
    sub = "Quantitative comparison, integers"

    def build(self, rng):
        lo = rng.choice([-3, -2, -1, 0, 1, 2, 3])
        hi = lo + rng.choice([3, 4, 5])
        k = rng.choice([2, 3, 4, 5])
        c = rng.choice([-6, -3, 0, 2, 4, 6, 8])
        d = rng.choice([-4, -2, 0, 1, 3])
        xs = list(range(lo + 1, hi))           # lo < x < hi, x an integer
        pairs = [(x, F(k * x + c), F(x * x + d)) for x in xs]
        ans, wit = relation(pairs)
        cond = "x is an integer and %d < x < %d." % (lo, hi)
        qa = "%dx %s %d" % (k, "+" if c >= 0 else "-", abs(c)) if c else "%dx" % k
        qb = "x squared %s %d" % ("+" if d >= 0 else "-", abs(d)) if d else "x squared"
        vals = (", ".join(str(x) for x in xs[:-1]) + " and " + str(xs[-1])) if len(xs) > 1 else str(xs[0])
        if ans == 3:
            (o1, x1), (o2, x2) = witnesses(wit)
            expl = ("The allowed values are %s. At x = %d, Quantity A is %d and Quantity B is "
                    "%d; at x = %d, Quantity A is %d and Quantity B is %d. The order changes "
                    "with x."
                    % (vals, x1, k * x1 + c, x1 * x1 + d, x2, k * x2 + c, x2 * x2 + d))
            wrong = ("Testing one value, or only the positive ones, misses a value where the "
                     "order flips. With few allowed values, test every one.")
        else:
            rows = "; ".join("x = %d gives %d and %d" % (x, k * x + c, x * x + d) for x in xs)
            expl = "The allowed values are %s, and each gives the same order: %s." % (vals, rows)
            wrong = ("Choosing %s without testing the allowed values misses that the "
                     "condition leaves only %d of them, and each orders the quantities the "
                     "same way." % (CD, len(xs)))
        return self.assemble(cond, qa, qb, ans, expl, wrong, 3 if ans == 3 else 2)


# ------------------------------------------------------------------- algebra

# Each pair is (Quantity A, Quantity B, A minus B, the factorization of A minus B in words,
# its roots and poles). A minus B is checked against the factorization before use.
POWER_PAIRS = [
    ("x squared", "x", lambda x: x * x, lambda x: x, lambda x: x * (x - 1),
     "x times (x minus 1)", [F(0), F(1)], []),
    ("x cubed", "x squared", lambda x: x ** 3, lambda x: x * x, lambda x: x * x * (x - 1),
     "x squared times (x minus 1)", [F(0), F(1)], []),
    ("x", "1/x", lambda x: x, lambda x: 1 / x, lambda x: (x - 1) * (x + 1) / x,
     "(x minus 1) times (x plus 1), divided by x", [F(-1), F(1)], [F(0)]),
    ("x cubed", "x", lambda x: x ** 3, lambda x: x, lambda x: x * (x - 1) * (x + 1),
     "x times (x minus 1) times (x plus 1)", [F(-1), F(0), F(1)], []),
    # x cubed minus 1 has the one real root 1, since x squared plus x plus 1 is never zero.
    ("x squared", "1/x", lambda x: x * x, lambda x: 1 / x, lambda x: (x ** 3 - 1) / x,
     "(x cubed minus 1) divided by x", [F(1)], [F(0)]),
    ("2x", "x squared", lambda x: 2 * x, lambda x: x * x, lambda x: x * (2 - x),
     "x times (2 minus x)", [F(0), F(2)], []),
    ("x squared", "x cubed", lambda x: x * x, lambda x: x ** 3, lambda x: x * x * (1 - x),
     "x squared times (1 minus x)", [F(0), F(1)], []),
]
INF = None
# The condition, as open intervals of x (None is unbounded), and how the stem states it.
CONDITIONS = [
    ("x > 1", [(F(1), INF)]),
    ("0 < x < 1", [(F(0), F(1))]),
    ("x < 0", [(INF, F(0))]),
    ("-1 < x < 0", [(F(-1), F(0))]),
    ("x < -1", [(INF, F(-1))]),
    ("x > 0", [(F(0), INF)]),
    ("x > 2", [(F(2), INF)]),
    ("1 < x < 2", [(F(1), F(2))]),
]


def inside(lo, hi):
    """An exact value strictly inside the open interval (lo, hi)."""
    if lo is None and hi is None:
        return F(0)
    if lo is None:
        return hi - 1
    if hi is None:
        return lo + 1
    return (lo + hi) / 2


class QCPowerOfX(QCBase):
    """A power of x against another, under a condition on x."""
    id = "gre_qc_xpowers"
    skill = "gre_alg"
    sub = "Quantitative comparison, powers of a variable"

    def build(self, rng):
        qa, qb, fa, fb, diff, factored, roots, poles = rng.choice(POWER_PAIRS)
        cond, ivals = rng.choice(CONDITIONS)
        # The factorization is a claim, so it is checked before anything rests on it.
        for t in (F(-7, 3), F(-3, 2), F(-1, 3), F(1, 4), F(2, 3), F(5, 4), F(3), F(9, 2),
                  F(-5), F(7, 5), F(-2, 7), F(11, 3)):
            if fa(t) - fb(t) != diff(t):
                raise ItemError("factorization of %s minus %s is wrong at %s" % (qa, qb, t))
        def within(c, lo, hi):
            return (lo is None or c > lo) and (hi is None or c < hi)
        cases = []
        for lo, hi in ivals:
            if any(within(c, lo, hi) for c in poles):
                raise ItemError("the condition allows a value where %s is undefined" % qb)
            cuts = sorted(c for c in roots + poles if within(c, lo, hi))
            edges = [lo] + cuts + [hi]
            for i in range(len(edges) - 1):
                t = inside(edges[i], edges[i + 1])
                cases.append((t, fa(t), fb(t)))
            # A root inside the interval is a value where the two quantities are equal.
            for c in roots:
                if within(c, lo, hi):
                    cases.append((c, fa(c), fb(c)))
        ans, wit = relation(cases)
        # The sign argument decides; 200 random allowed values try to refute it.
        pts = [s for lo, hi in ivals for s in sample_in(rng, lo, hi, 200)]
        falsify(ans, pts, fa, fb, "%s against %s for %s" % (qa, qb, cond))
        if ans == 3:
            picks = witnesses(wit)
            bits = []
            for o, t in picks:
                bits.append("x = %s gives %s for Quantity A and %s for Quantity B"
                            % (word(t), word(fa(t)), word(fb(t))))
            expl = ("Try values the condition allows: %s. One value makes the quantities "
                    "order one way and the other another way, so the relationship depends on x."
                    % "; ".join(bits))
            wrong = ("Testing only one kind of number is the trap. Try zero, negatives, "
                     "fractions and numbers greater than 1 where the condition allows them.")
        else:
            t = next(iter(wit.values()))
            sign = {0: "positive", 1: "negative", 2: "zero"}[ans]
            expl = ("Quantity A minus Quantity B is %s, and for %s every factor keeps one "
                    "sign, so the difference is %s for every allowed x. For example, x = %s "
                    "gives %s against %s."
                    % (factored, cond, sign, word(t), word(fa(t)), word(fb(t))))
            wrong = ("Choosing %s by testing values outside the condition is the trap. "
                     "Within %s the order never changes." % (CD, cond))
        return self.assemble(cond, qa, qb, ans, expl, wrong, 4 if ans == 3 else 3)


class QCSystem(QCBase):
    """Two linear equations in x and y, comparing expressions in the solution."""
    id = "gre_qc_system"
    skill = "gre_alg"
    sub = "Quantitative comparison, systems of equations"

    def build(self, rng):
        x0, y0 = rng.choice(range(-4, 9)), rng.choice(range(-4, 9))
        a1, b1 = rng.choice([1, 2, 3]), rng.choice([1, 2, -1])
        a2, b2 = rng.choice([1, 2, -1]), rng.choice([-1, -2, 1, 3])
        if a1 * b2 - a2 * b1 == 0:
            raise ItemError("the equations are not independent")
        c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
        # Solve again from the equations as printed, by Cramer's rule, rather than trusting
        # the values they were built from.
        det = a1 * b2 - a2 * b1
        xs = F(c1 * b2 - c2 * b1, det)
        ys = F(a1 * c2 - a2 * c1, det)
        if (xs, ys) != (x0, y0):
            raise ItemError("the system does not solve to its own values")

        def eq(a, b, c):
            ta = ("" if a == 1 else "-" if a == -1 else str(a)) + "x"
            tb = ("+ " if b > 0 else "- ") + ("" if abs(b) == 1 else str(abs(b))) + "y"
            return "%s %s = %d" % (ta, tb, c)
        shift = rng.choice([0, 0, 1, 2, -1])
        qa = "x"
        qb = "y" if shift == 0 else ("y %s %d" % ("+" if shift > 0 else "-", abs(shift)))
        va, vb = xs, ys + shift
        ans = order(va, vb)
        expl = ("Solving the equations together gives x = %s and y = %s, so Quantity A is %s "
                "and Quantity B is %s." % (word(xs), word(ys), word(va), word(vb)))
        wrong = ("Choosing %s because there are two variables is the trap: two independent "
                 "equations fix both of them." % CD)
        cond = "%s and %s" % (eq(a1, b1, c1), eq(a2, b2, c2))
        return self.assemble(cond, qa, qb, ans, expl, wrong, 3)


class QCRanges(QCBase):
    """Two variables in separate open intervals, compared directly."""
    id = "gre_qc_ranges"
    skill = "gre_alg"
    sub = "Quantitative comparison, inequalities"

    def build(self, rng):
        a = rng.choice(range(-5, 8))
        b = a + rng.choice([2, 3, 4, 5])
        c = rng.choice(range(-5, 10))
        d = c + rng.choice([2, 3, 4])
        k = rng.choice([1, 1, 2])
        # Quantity A is k times x, so its range is k times x's.
        la, ha = F(k * a), F(k * b)
        lb, hb = F(c), F(d)
        cond = "%d < x < %d and %d < y < %d" % (a, b, c, d)
        qa = "x" if k == 1 else "%dx" % k
        if ha <= lb or hb <= la:
            # Try to refute the decision with random allowed pairs before stating it.
            for _ in range(200):
                x = a + (b - a) * F(rng.randint(1, 9999), 10000)
                y = c + (d - c) * F(rng.randint(1, 9999), 10000)
                if order(k * x, y) != (1 if ha <= lb else 0):
                    raise Contradiction("ranges decided wrongly at x = %s, y = %s" % (x, y))
        if ha <= lb:
            ans = 1
            expl = ("Quantity A is less than %s and Quantity B is greater than %s, and %s is "
                    "at most %s, so B is greater for every allowed x and y."
                    % (word(ha), word(lb), word(ha), word(lb)))
        elif hb <= la:
            ans = 0
            expl = ("Quantity A is greater than %s and Quantity B is less than %s, and %s is "
                    "at most %s, so A is greater for every allowed x and y."
                    % (word(la), word(hb), word(hb), word(la)))
        else:
            ans = 3
            lo, hi = max(la, lb), min(ha, hb)    # the overlap, an open interval
            m = (lo + hi) / 2
            e = (hi - lo) / 4
            # Two allowed pairs that order the quantities differently, checked here.
            p1 = ((m + e) / k, m - e)
            p2 = ((m - e) / k, m + e)
            for x, y in (p1, p2):
                if not (a < x < b and c < y < d):
                    raise ItemError("witness outside the condition")
            if not (k * p1[0] > p1[1] and k * p2[0] < p2[1]):
                raise ItemError("witnesses do not differ")
            expl = ("The ranges overlap between %s and %s. With x = %s and y = %s, Quantity A "
                    "is %s and B is %s, so A is greater; with x = %s and y = %s, A is %s and B "
                    "is %s, so B is greater."
                    % (word(lo), word(hi), word(p1[0]), word(p1[1]), word(k * p1[0]),
                       word(p1[1]), word(p2[0]), word(p2[1]), word(k * p2[0]), word(p2[1])))
        wrong = ("Comparing the upper or lower ends alone is the trap. Ask whether the two "
                 "ranges overlap: if they do, either quantity can be the greater.")
        return self.assemble(cond, qa, "y", ans, expl, wrong, 3)


# ------------------------------------------------------------------ geometry

class QCTriangleSides(QCBase):
    """Two sides of a triangle, ordered by the angles opposite them."""
    id = "gre_qc_triangle"
    skill = "gre_geo"
    sub = "Quantitative comparison, triangles"

    def build(self, rng):
        p = rng.choice(range(30, 91, 5))
        q = rng.choice(range(20, 111, 5))
        r = 180 - p - q
        if r < 10:
            raise ItemError("not a triangle")
        # Side QR is opposite angle P, PR is opposite Q, and PQ is opposite R.
        sides = {"QR": ("P", p), "PR": ("Q", q), "PQ": ("R", r)}
        sa, sb = rng.sample(sorted(sides), 2)
        (va_name, va), (vb_name, vb) = sides[sa], sides[sb]
        ans = order(va, vb)
        cond = ("In triangle PQR, the measure of angle P is %d degrees and the measure of "
                "angle Q is %d degrees." % (p, q))
        expl = ("Angle R is 180 minus %d minus %d, which is %d degrees. In a triangle the "
                "longer side is opposite the larger angle, and equal angles face equal sides. "
                "Side %s is opposite angle %s, which is %d degrees, and side %s is opposite "
                "angle %s, which is %d degrees."
                % (p, q, r, sa, va_name, va, sb, vb_name, vb))
        wrong = ("Choosing %s because no lengths are given is the trap: the three angles fix "
                 "the order of the three sides." % CD)
        return self.assemble(cond, "the length of side %s" % sa, "the length of side %s" % sb,
                             ans, expl, wrong, 3)


def dec1(v):
    """A positive value to one decimal place, for an approximation the explanation shows."""
    return "%.1f" % float(v)


# pi lies strictly between these two, so a comparison that both bounds decide the same way
# is decided; one they disagree on is not drawn.
PI_LO, PI_HI = F(314159, 100000), F(314160, 100000)


class QCCircleSquare(QCBase):
    """A circle and a square, compared by area or by the distance around."""
    id = "gre_qc_circle"
    skill = "gre_geo"
    sub = "Quantitative comparison, circles"

    def build(self, rng):
        r = rng.choice(range(2, 11))
        s = rng.choice(range(3, 19))
        kind = rng.choice(["area", "around"])
        if kind == "area":
            lo, hi = PI_LO * r * r, PI_HI * r * r
            vb = F(s * s)
            qa, qb = "the area of the circle", "the area of the square"
            circ = "pi times %d squared, which is %d pi, about %s" % (r, r * r, dec1(lo))
            sq = "%d squared, which is %d" % (s, s * s)
            three = 3 * r * r
        else:
            lo, hi = 2 * PI_LO * r, 2 * PI_HI * r
            vb = F(4 * s)
            qa, qb = "the circumference of the circle", "the perimeter of the square"
            circ = "2 times pi times %d, which is %d pi, about %s" % (r, 2 * r, dec1(lo))
            sq = "4 times %d, which is %d" % (s, 4 * s)
            three = 6 * r
        if lo <= vb <= hi:
            raise ItemError("too close to call with these bounds on pi")
        ans = 0 if lo > vb else 1
        cond = "A circle has radius %d, and a square has sides of length %d." % (r, s)
        expl = "The circle's measure is %s; the square's is %s." % (circ, sq)
        if (three > vb) != (ans == 0) or three == vb:
            wrong = ("Using 3 for pi gives %d, which reverses or ties the comparison. Pi is a "
                     "little more than 3.14, and here that difference decides it." % three)
        else:
            wrong = ("Comparing the radius with the side length is the trap; the formulas "
                     "multiply the radius by pi, so compute both measures.")
        return self.assemble(cond, qa, qb, ans, expl, wrong, 3)


# ---------------------------------------------------------------------- data

def mean(xs):
    return F(sum(xs), len(xs))


def median(xs):
    s = sorted(xs)
    n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


class QCMeanMedian(QCBase):
    """The mean and the median of one list."""
    id = "gre_qc_meanmed"
    skill = "gre_data"
    sub = "Quantitative comparison, mean and median"

    def build(self, rng):
        n = rng.choice([5, 6, 7])
        shape = rng.choice(["skew_up", "skew_down", "even"])
        base = sorted(rng.sample(range(2, 30), n))
        if shape == "skew_up":
            base[-1] += rng.choice([15, 25, 40])
        elif shape == "skew_down":
            base[0] = max(0, base[0] - rng.choice([10, 15]))
        else:
            mid = rng.choice(range(8, 20))
            step = rng.choice([1, 2, 3])
            half = [mid - step * (i + 1) for i in range(n // 2)]
            base = sorted(half + [mid + step * (i + 1) for i in range(n // 2)]
                          + ([mid] if n % 2 else []))
            if min(base) < 0:
                raise ItemError("negative value")
        xs = base[:]
        rng.shuffle(xs)
        va, vb = mean(xs), median(xs)
        ans = order(va, vb)
        listed = ", ".join(str(x) for x in xs)
        expl = ("The values sum to %d, so the mean is %d divided by %d, which is %s. In order "
                "they are %s, so the median is %s."
                % (sum(xs), sum(xs), n, word(va), ", ".join(str(x) for x in sorted(xs)),
                   word(vb)))
        wrong = ("Assuming the mean and median match is the trap. One far value pulls the mean "
                 "toward it and leaves the median where it was.")
        return self.assemble("List L: %s" % listed, "the mean of List L", "the median of List L",
                             ans, expl, wrong, 2)


def variance(xs):
    m = mean(xs)
    return sum((F(x) - m) ** 2 for x in xs) / len(xs)


class QCSpread(QCBase):
    """The standard deviations of two lists, one built from the other."""
    id = "gre_qc_spread"
    skill = "gre_data"
    sub = "Quantitative comparison, standard deviation"

    def build(self, rng):
        n = rng.choice([4, 5])
        a = sorted(rng.sample(range(1, 20), n))
        kind = rng.choice(["shift", "scale", "shrink"])
        if kind == "shift":
            k = rng.choice([3, 5, 10, 20])
            b = [x + k for x in a]
            how = "adds %d to each value of List A" % k
        elif kind == "scale":
            k = rng.choice([2, 3])
            b = [x * k for x in a]
            how = "multiplies each value of List A by %d" % k
        else:
            # List B is List A with every value moved halfway to the mean, built from B so
            # every value is a whole number: A is B pushed twice as far from the same mean.
            m = rng.choice(range(9, 16))
            b = rng.sample(range(m - 6, m + 7), n - 1)
            last = n * m - sum(b)
            if last in b or abs(last - m) > 6:
                raise ItemError("no whole number list with that mean")
            b = sorted(b + [last])
            a = [2 * y - m for y in b]
            if min(a) < 0:
                raise ItemError("negative value")
            how = "moves each value of List A halfway to the mean, %d" % m
        if len(set(a)) < 2:
            raise ItemError("no spread")
        # Standard deviations are compared through their squares, which keep the order.
        va, vb = variance(a), variance(b)
        ans = order(va, vb)
        expl = ("List B %s. The variance of List A is %s and of List B is %s, and the standard "
                "deviation is the square root of the variance, so the two compare the same "
                "way." % (how, word(va), word(vb)))
        wrong = {"shift": "Adding the same number to every value moves the mean, not the "
                          "spread, so the standard deviation does not change.",
                 "scale": "Multiplying every value by a number multiplies the standard "
                          "deviation by it too; the spread grows with the values.",
                 "shrink": "Moving every value toward the mean narrows the spread, even though "
                           "the mean itself stays put."}[kind]
        cond = ("List A: %s\nList B: %s" % (", ".join(map(str, a)), ", ".join(map(str, b))))
        return self.assemble(cond, "the standard deviation of List A",
                             "the standard deviation of List B", ans, expl, wrong, 3)


ARITH = [QCPercentSwap(), QCPowers(), QCIntegerRange()]
ALG = [QCPowerOfX(), QCSystem(), QCRanges()]
GEO = [QCTriangleSides(), QCCircleSquare()]
DATA = [QCMeanMedian(), QCSpread()]
GENS = ARITH + ALG + GEO + DATA
