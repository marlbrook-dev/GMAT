"""GMAT Data Sufficiency (di_ds).

Sufficiency is never argued here, it is enumerated. Each schema hands a domain of
candidate assignments plus the question and the two statements as predicates to
framework.sufficiency(), which checks whether each statement pins the answer down.
The statement TEXT and the statement PREDICATE are built from the same parameters
in the same place, because the way these items go wrong is the prose drifting away
from the logic it is supposed to describe.
"""
from framework import FixedGen, sufficiency, ItemError, num

DS_CHOICES = [
    'Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.',
    'Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.',
    'BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.',
    'EACH statement ALONE is sufficient.',
    'Statements (1) and (2) TOGETHER are NOT sufficient.',
]

LETTER = "ABCDE"
WHY = {
    0: "Statement (1) settles the question on its own and statement (2) leaves more than one answer open.",
    1: "Statement (2) settles the question on its own and statement (1) leaves more than one answer open.",
    2: "Neither statement decides the question alone, but the two together leave only one answer.",
    3: "Either statement decides the question by itself, so neither one needs the other.",
    4: "Even taken together the statements admit more than one answer.",
}


class DSBase(FixedGen):
    skill = "di_ds"
    section = "DI"
    type = "DS"
    sub = "Data Sufficiency"

    def assemble(self, question_text, t1, t2, domain, q, s1, s2, expl_bits, diff, qskill):
        ans = sufficiency(domain, q, s1, s2)
        if ans is None:
            raise ItemError("%s drew a statement no case satisfies" % self.id)
        return {
            "stem": "%s\n\n(1) %s\n(2) %s" % (question_text, t1, t2),
            "choices": DS_CHOICES,
            "answer": ans,
            "diff": diff,
            "qskill": qskill,
            "domain": "math",
            "expl": "%s %s The answer is %s." % (expl_bits, WHY[ans], LETTER[ans]),
            "wrong": "Data Sufficiency asks only whether the question can be answered, "
                     "never what the answer is. A statement that narrows the possibilities "
                     "without settling them is not sufficient.",
        }


class DSLinearValue(DSBase):
    id = "gmat_ds_linear"

    def build(self, rng):
        a = rng.choice([2, 3, 4, 5, 6])
        b = rng.choice([-9, -5, -3, 2, 4, 7])
        dom = [{"x": x} for x in range(-30, 31)]
        q = lambda c: c["x"]
        kind1 = rng.choice(["exact", "range", "abs"])
        kind2 = rng.choice(["exact", "range", "abs", "multiple"])
        k = rng.choice([-6, -4, -2, 3, 5, 8])

        def mk(kind):
            if kind == "exact":
                return ("%dx %s %d = %d" % (a, "+" if b >= 0 else "-", abs(b), a * k + b),
                        lambda c: a * c["x"] + b == a * k + b)
            if kind == "range":
                lo = k - rng.choice([2, 3, 4])
                return ("x is greater than %d" % lo, lambda c, lo=lo: c["x"] > lo)
            if kind == "abs":
                return ("the absolute value of x is %d" % abs(k),
                        lambda c, kk=abs(k): abs(c["x"]) == kk)
            m = rng.choice([2, 3, 4])
            return ("x is a multiple of %d" % m, lambda c, m=m: c["x"] % m == 0)

        t1, s1 = mk(kind1)
        t2, s2 = mk(kind2)
        # The domain enumerated below is the integers, so the stem has to SAY x is an
        # integer. Without that, a statement like "the absolute value of x is 6" reads
        # as sufficient here while admitting 5.5 in the real world, and the item would
        # be wrong in exactly the way that is hardest to notice.
        return self.assemble(
            "If x is an integer, what is the value of x?", t1, t2, dom, q, s1, s2,
            "A value question needs the statements to leave exactly one possible x.",
            rng.choice([2, 3]), "q_alg")


class DSInequality(DSBase):
    id = "gmat_ds_inequality"

    def build(self, rng):
        t = rng.choice([0, 1, 2, 3, 5, 10])
        dom = [{"x": x} for x in range(-25, 26)]
        q = lambda c: c["x"] > t

        def mk():
            kind = rng.choice(["square", "range", "sign", "abs", "exact"])
            if kind == "square":
                s = rng.choice([4, 9, 16, 25, 36])
                return ("x squared is greater than %d" % s,
                        lambda c, s=s: c["x"] ** 2 > s)
            if kind == "range":
                lo = rng.choice([-4, -1, 0, 2, 4, 6, 9, 11])
                return ("x is greater than %d" % lo, lambda c, lo=lo: c["x"] > lo)
            if kind == "sign":
                return ("x is positive", lambda c: c["x"] > 0)
            if kind == "abs":
                v = rng.choice([3, 6, 8, 12])
                return ("the absolute value of x is less than %d" % v,
                        lambda c, v=v: abs(c["x"]) < v)
            v = rng.choice([-3, 1, 4, 7, 12])
            return ("x equals %d" % v, lambda c, v=v: c["x"] == v)

        t1, s1 = mk()
        t2, s2 = mk()
        return self.assemble(
            "If x is an integer, is x greater than %d?" % t, t1, t2, dom, q, s1, s2,
            "A yes or no question is settled when every case a statement allows gives "
            "the same answer, even if x itself is never pinned down.",
            rng.choice([3, 4]), "q_alg")


class DSAverage(DSBase):
    id = "gmat_ds_average"

    def build(self, rng):
        dom = [{"a": a, "b": b} for a in range(1, 13) for b in range(1, 13)]
        q = lambda c: (c["a"] + c["b"]) / 2

        def mk():
            kind = rng.choice(["sum", "one", "diff", "both", "ratio"])
            if kind == "sum":
                s = rng.choice([8, 10, 12, 14, 16])
                return ("a + b = %d" % s, lambda c, s=s: c["a"] + c["b"] == s)
            if kind == "one":
                v = rng.choice([3, 4, 5, 6, 7])
                return ("a = %d" % v, lambda c, v=v: c["a"] == v)
            if kind == "diff":
                dv = rng.choice([1, 2, 3, 4])
                return ("b - a = %d" % dv, lambda c, dv=dv: c["b"] - c["a"] == dv)
            if kind == "ratio":
                return ("b is twice a", lambda c: c["b"] == 2 * c["a"])
            v1, v2 = rng.choice([3, 4, 5]), rng.choice([6, 7, 8])
            return ("a = %d and b = %d" % (v1, v2),
                    lambda c, v1=v1, v2=v2: c["a"] == v1 and c["b"] == v2)

        t1, s1 = mk()
        t2, s2 = mk()
        return self.assemble(
            "If a and b are positive integers, what is the average of a and b?",
            t1, t2, dom, q, s1, s2,
            "The average depends only on the sum, so anything that fixes a + b is enough "
            "and nothing less is.",
            rng.choice([2, 3, 4]), "q_csp")


class DSRectangle(DSBase):
    id = "gmat_ds_rectangle"

    def build(self, rng):
        dom = [{"w": w, "h": h} for w in range(1, 13) for h in range(1, 13)]
        ask = rng.choice(["area", "perimeter"])
        q = (lambda c: c["w"] * c["h"]) if ask == "area" else (lambda c: 2 * (c["w"] + c["h"]))

        def mk():
            kind = rng.choice(["area", "perim", "side", "square", "ratio"])
            if kind == "area":
                v = rng.choice([12, 16, 24, 36])
                return ("the area of the rectangle is %d" % v,
                        lambda c, v=v: c["w"] * c["h"] == v)
            if kind == "perim":
                v = rng.choice([14, 16, 20, 24])
                return ("the perimeter of the rectangle is %d" % v,
                        lambda c, v=v: 2 * (c["w"] + c["h"]) == v)
            if kind == "side":
                v = rng.choice([3, 4, 6, 8])
                return ("the width is %d" % v, lambda c, v=v: c["w"] == v)
            if kind == "square":
                return ("the rectangle is a square", lambda c: c["w"] == c["h"])
            return ("the length is twice the width", lambda c: c["h"] == 2 * c["w"])

        t1, s1 = mk()
        t2, s2 = mk()
        return self.assemble(
            "A rectangle has integer width and length. What is the %s of the rectangle?" % ask,
            t1, t2, dom, q, s1, s2,
            "Area and perimeter each need both dimensions, and neither one determines the other.",
            rng.choice([3, 4]), "q_alg")


class DSPercentMix(DSBase):
    id = "gmat_ds_percent"

    def build(self, rng):
        dom = [{"boys": b, "girls": g} for b in range(1, 25) for g in range(1, 25)]
        ask = rng.choice(["ratio", "total", "boys"])
        q = {"ratio": lambda c: c["boys"] / c["girls"],
             "total": lambda c: c["boys"] + c["girls"],
             "boys": lambda c: c["boys"]}[ask]
        label = {"ratio": "the ratio of boys to girls",
                 "total": "the total number of students",
                 "boys": "the number of boys"}[ask]

        def mk():
            kind = rng.choice(["pct", "count", "total", "diff"])
            if kind == "pct":
                p = rng.choice([25, 40, 50, 60, 75])
                return ("%d percent of the students are boys" % p,
                        lambda c, p=p: c["boys"] * 100 == p * (c["boys"] + c["girls"]))
            if kind == "count":
                v = rng.choice([6, 8, 10, 12])
                return ("there are %d boys" % v, lambda c, v=v: c["boys"] == v)
            if kind == "total":
                v = rng.choice([20, 24, 30, 32])
                return ("there are %d students in all" % v,
                        lambda c, v=v: c["boys"] + c["girls"] == v)
            v = rng.choice([2, 4, 6])
            return ("there are %d more girls than boys" % v,
                    lambda c, v=v: c["girls"] - c["boys"] == v)

        t1, s1 = mk()
        t2, s2 = mk()
        return self.assemble(
            "In a certain class every student is either a boy or a girl, and there is at "
            "least one of each. What is %s?" % label,
            t1, t2, dom, q, s1, s2,
            "A ratio needs relative sizes only, while a count needs an actual number, so "
            "the same statement can be enough for one and useless for the other.",
            rng.choice([3, 4]), "q_rrp")


GENS = [DSLinearValue(), DSInequality(), DSAverage(), DSRectangle(), DSPercentMix()]
