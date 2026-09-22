"""SAT Algebra (m_alg) generators.

Every distractor below is a mistake a real student makes: forgetting to divide by
the coefficient, dropping a sign when a term crosses the equals sign, reading the
intercept as the slope. That is the whole point of a distractor.
"""
from framework import Gen, num, money, frac
from fractions import Fraction as Fr


class LinearOneStep(Gen):
    id = "sat_alg_linear1"
    skill = "m_alg"
    section = "M"
    sub = "Linear equations in one variable"
    diff = 1

    def build(self, rng):
        a = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        x = rng.choice([-9, -7, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8])
        b = rng.choice([-19, -15, -11, -7, -5, 3, 5, 7, 9, 13, 17])
        c = a * x + b
        return {
            "stem": "If %dx %s %d = %d, what is the value of x?"
            % (a, "+" if b >= 0 else "-", abs(b), c),
            "answer": x,
            "distractors": [
                (c - b, "stopping after the subtraction and never dividing by the coefficient."),
                (Fr(c + b, a), "adding %d to both sides instead of subtracting it." % abs(b)),
                (-x, "solving correctly and then dropping the sign."),
                (Fr(c, a), "dividing before moving the constant across."),
            ],
            "expl": "Subtract %d from both sides to get %dx = %d, then divide both sides by %d, "
            "which gives x = %s." % (b, a, c - b, a, num(x))
            if b >= 0
            else "Add %d to both sides to get %dx = %d, then divide both sides by %d, which "
            "gives x = %s." % (abs(b), a, c - b, a, num(x)),
        }


class LinearDistribute(Gen):
    id = "sat_alg_distribute"
    skill = "m_alg"
    section = "M"
    sub = "Linear equations in one variable"
    diff = 2

    def build(self, rng):
        a = rng.choice([2, 3, 4, 5, 6])
        b = rng.choice([-7, -5, -3, -2, 2, 3, 4, 6])
        c = rng.choice([1, 2, 3, 7, 8, 9])
        while c == a:
            c = rng.choice([1, 2, 7, 8, 9])
        d = rng.choice([-13, -9, -6, 4, 5, 11, 15])
        # a(x + b) = cx + d  ->  x(a - c) = d - ab
        x = Fr(d - a * b, a - c)
        return {
            "stem": "If %d(x %s %d) = %dx %s %d, what is the value of x?"
            % (a, "+" if b >= 0 else "-", abs(b), c, "+" if d >= 0 else "-", abs(d)),
            "answer": x,
            "distractors": [
                (Fr(d + a * b, a - c), "distributing %d to x but not to the constant inside the parentheses." % a),
                (Fr(d - a * b, a + c), "adding the x coefficients instead of subtracting to collect them on one side."),
                (-x, "collecting the variable terms on the left but the constants on the left as well, which flips the sign."),
                (Fr(d - b, a - c), "forgetting to multiply the constant inside the parentheses by %d at all." % a),
            ],
            "expl": "Distribute on the left to get %dx %s %d = %dx %s %d. Collect the x terms on "
            "one side and the constants on the other: %sx = %s, so x = %s."
            % (a, "+" if a * b >= 0 else "-", abs(a * b), c, "+" if d >= 0 else "-", abs(d),
               num(a - c), num(d - a * b), num(x)),
        }


class SlopeFromPoints(Gen):
    id = "sat_alg_slope"
    skill = "m_alg"
    section = "M"
    sub = "Linear functions"
    diff = 2

    def build(self, rng):
        x1 = rng.randint(-8, 6)
        x2 = x1 + rng.choice([1, 2, 3, 4, 5, 6])
        y1 = rng.randint(-9, 9)
        y2 = rng.randint(-9, 9)
        while y2 == y1:
            y2 = rng.randint(-9, 9)
        m = Fr(y2 - y1, x2 - x1)
        return {
            "stem": "A line in the xy-plane passes through the points (%d, %d) and (%d, %d). "
            "What is the slope of the line?" % (x1, y1, x2, y2),
            "answer": m,
            "distractors": [
                (frac(x2 - x1, y2 - y1), "inverting the slope formula, putting the run over the rise."),
                (-m, "subtracting the coordinates in opposite orders, once as point two minus point one and once the other way."),
                (frac(y2 + y1, x2 + x1), "adding the coordinates instead of subtracting them."),
                (Fr(y1 - y2, x2 - x1), "subtracting the y values in one order and the x values in the other."),
                (y2 - y1, "reporting the rise alone and never dividing by the run."),
                (x2 - x1, "reporting the run alone."),
                (Fr(y2 - y1, x2 - x1) + 1, "an off by one slip while subtracting coordinates."),
            ],
            "expl": "Slope is the change in y over the change in x: (%d - %d) divided by "
            "(%d - %d), which is %s over %s, or %s."
            % (y2, y1, x2, x1, num(y2 - y1), num(x2 - x1), num(m)),
        }


class SystemOfEquations(Gen):
    id = "sat_alg_system"
    skill = "m_alg"
    section = "M"
    sub = "Systems of two linear equations"
    diff = 3

    def build(self, rng):
        x = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])
        y = rng.choice([-6, -4, -3, -2, 2, 3, 5, 7])
        a1, b1 = rng.choice([2, 3, 4, 5]), rng.choice([1, 2, 3, -2, -3])
        a2, b2 = rng.choice([1, 2, 5, 6]), rng.choice([4, 5, -1, -4])
        if a1 * b2 - a2 * b1 == 0:
            raise __import__("framework").ItemError("degenerate system")
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        ask = rng.choice(["x", "y", "sum"])
        val = {"x": x, "y": y, "sum": x + y}[ask]
        label = {"x": "the value of x", "y": "the value of y", "sum": "the value of x + y"}[ask]
        return {
            "stem": "In the system of equations %dx %s %dy = %d and %dx %s %dy = %d, what is %s?"
            % (a1, "+" if b1 >= 0 else "-", abs(b1), c1,
               a2, "+" if b2 >= 0 else "-", abs(b2), c2, label),
            "answer": val,
            "distractors": [
                ({"x": y, "y": x, "sum": x - y}[ask], "solving the system correctly and then reporting the wrong one of the two values."),
                (val + 1, "an arithmetic slip of one while eliminating a variable."),
                (-val, "multiplying one equation through to eliminate a variable but forgetting to change the sign on the constant."),
                (x - y, "subtracting the two solutions when the question asks for something else."),
                (val * 2, "doubling one equation to eliminate and then forgetting to undo that scaling at the end."),
            ],
            "expl": "Solving the system gives x = %d and y = %d, so %s is %s."
            % (x, y, label, num(val)),
            "diff": 3 if ask != "sum" else 4,
        }


class LinearInequality(Gen):
    id = "sat_alg_inequality"
    skill = "m_alg"
    section = "M"
    sub = "Linear inequalities"
    diff = 3

    def build(self, rng):
        a = rng.choice([-7, -5, -4, -3, -2, 2, 3, 4, 5, 6])
        b = rng.choice([-12, -8, -5, 3, 6, 9, 14])
        k = rng.choice([-10, -6, -3, 4, 8, 12, 18])
        bound = Fr(k - b, a)
        flips = a < 0
        rel = ">" if not flips else "<"
        return {
            "stem": "Which of the following describes all values of x that satisfy "
            "%dx %s %d > %d?" % (a, "+" if b >= 0 else "-", abs(b), k),
            "answer": "x %s %s" % (rel, num(bound)),
            # The sign flip is what this item tests, so it is always on the paper. It is
            # also the same length as the key, which is what stops the key being the
            # uniquely longest option.
            "require": ["x %s %s" % (">" if flips else "<", num(bound))],
            "distractors": [
                ("x %s %s" % (">" if flips else "<", num(bound)),
                 "forgetting that dividing by a negative number reverses the inequality sign."
                 if flips else "reversing the inequality sign when nothing required it."),
                ("x %s %s" % (rel, num(Fr(k + b, a))), "adding %d to both sides instead of subtracting it." % abs(b)),
                ("x %s %s" % (rel, num(Fr(k, a))), "dividing before moving the constant across."),
                ("x %s %s" % (rel, num(k - b)), "stopping after the subtraction and never dividing by %d." % a),
            ],
            "expl": "Subtract %d from both sides to get %dx > %d. Dividing by %d %s, so the "
            "solution is x %s %s."
            % (b, a, k - b, a,
               "reverses the inequality because %d is negative" % a if flips
               else "keeps the inequality direction because %d is positive" % a,
               rel, num(bound)),
            "diff": 3 if flips else 2,
        }
    fmt = staticmethod(str)


class ParallelPerpendicular(Gen):
    id = "sat_alg_parperp"
    skill = "m_alg"
    section = "M"
    sub = "Linear functions"
    diff = 3

    def build(self, rng):
        p, q = rng.choice([1, 2, 3, 4, 5, 7]), rng.choice([2, 3, 4, 5, 8])
        m = Fr(rng.choice([-1, 1]) * p, q)
        b = rng.randint(-9, 9)
        kind = rng.choice(["parallel", "perpendicular"])
        want = m if kind == "parallel" else -1 / m
        return {
            "stem": "Line k is %s to the line y = %sx %s %d in the xy-plane. What is the slope "
            "of line k?" % (kind, num(m), "+" if b >= 0 else "-", abs(b)),
            "answer": want,
            "distractors": [
                (m if kind == "perpendicular" else -1 / m,
                 "using the rule for the other relationship, parallel instead of perpendicular or the reverse."),
                (-m, "negating the slope without taking the reciprocal, which is neither rule."),
                (1 / m, "taking the reciprocal but leaving off the negative sign."),
                (b, "reading the y intercept as the slope."),
                (m + 1, "an arithmetic slip while copying the slope out of the equation."),
                (-m - 1, "combining a sign error with a copying slip."),
                (0, "treating every perpendicular slope as zero rather than a negative reciprocal."),
            ],
            "expl": "Parallel lines have equal slopes; perpendicular slopes are negative "
            "reciprocals. The given slope is %s, so a %s line has slope %s."
            % (num(m), kind, num(want)),
        }


class LinearWordProblem(Gen):
    id = "sat_alg_word"
    skill = "m_alg"
    section = "M"
    sub = "Linear functions"
    diff = 2

    SETUPS = [
        ("A technician charges a flat fee of {b} for a visit plus {r} for each hour of work.",
         "a visit lasting {n} hours", "total charge"),
        ("A pool contains {b} gallons of water and is filled at a constant rate of {r} gallons per minute.",
         "{n} minutes of filling", "number of gallons in the pool"),
        ("A membership costs {b} to join plus {r} for each class attended.",
         "a member who attends {n} classes", "total cost"),
    ]

    def build(self, rng):
        setup, whenf, ask = rng.choice(self.SETUPS)
        gallons = "gallons" in setup
        b = rng.choice([20, 24, 35, 40, 48, 55, 60, 75])
        r = rng.choice([3, 5, 6, 8, 9, 12, 15])
        n = rng.choice([4, 5, 6, 7, 8, 9, 11, 12])
        total = b + r * n
        f = (lambda v: num(v)) if gallons else (lambda v: money(v))
        return {
            "stem": (setup.format(b=f(b), r=f(r) + (" gallons per minute" if gallons else ""))
                     + " What is the %s for %s?" % (ask, whenf.format(n=n))),
            "answer": total,
            "distractors": [
                (r * n, "using only the per unit rate and forgetting the fixed starting amount."),
                (b + r, "adding a single unit of the rate instead of %d of them." % n),
                ((b + r) * n, "adding the fixed amount to the rate first and then multiplying, which charges the fixed amount %d times." % n),
                (b * n + r, "multiplying the fixed amount by %d and adding one unit of the rate, which reverses the roles." % n),
            ],
            "expl": "The fixed amount is %s and the variable part is %s times %d, which is %s. "
            "The total is %s." % (f(b), f(r), n, f(r * n), f(total)),
            "fmt": f,
        }


class FunctionEvaluate(Gen):
    id = "sat_alg_feval"
    skill = "m_alg"
    section = "M"
    sub = "Linear functions"
    diff = 2

    def build(self, rng):
        a = rng.choice([-6, -4, -3, -2, 2, 3, 4, 5, 7])
        b = rng.choice([-11, -8, -5, -1, 2, 6, 9, 13])
        k = rng.choice([-6, -5, -3, -2, 3, 4, 6, 8])
        val = a * k + b
        return {
            "stem": "The function f is defined by f(x) = %dx %s %d. What is the value of f(%d)?"
            % (a, "+" if b >= 0 else "-", abs(b), k),
            "answer": val,
            "distractors": [
                (a + k + b, "adding %d and %d instead of multiplying them." % (a, k)),
                (a * k - b, "subtracting the constant when the rule adds it, or the reverse."),
                (a * b + k, "substituting %d for the wrong symbol in the rule." % k),
                (-val, "evaluating correctly and then dropping the sign."),
                (a * (k + b), "adding the constant before multiplying instead of after."),
            ],
            "expl": "Substitute %d for x: f(%d) = %d times %d %s %d = %d."
            % (k, k, a, k, "plus" if b >= 0 else "minus", abs(b), val),
        }


class AbsoluteValue(Gen):
    id = "sat_alg_abs"
    skill = "m_alg"
    section = "M"
    sub = "Linear equations in one variable"
    diff = 3

    def build(self, rng):
        a = rng.choice([1, 2, 3, 4])
        b = rng.choice([-9, -6, -4, 3, 5, 7, 11])
        k = rng.choice([4, 6, 8, 10, 12, 15])
        hi = Fr(k - b, a)
        lo = Fr(-k - b, a)
        s = hi + lo
        return {
            "stem": "If |%dx %s %d| = %d, what is the sum of all possible values of x?"
            % (a, "+" if b >= 0 else "-", abs(b), k),
            "answer": s,
            "distractors": [
                (hi, "solving only the positive case and never setting the inside equal to negative %d." % k),
                (hi - lo, "subtracting the two solutions when the question asks for their sum."),
                (Fr(-2 * b, a) * -1, "getting both solutions but combining them with the wrong sign."),
                (lo, "solving only the negative case."),
            ],
            "expl": "The expression inside the bars equals %d or negative %d, giving x = %s and "
            "x = %s. Their sum is %s." % (k, k, num(hi), num(lo), num(s)),
        }


GENS = [
    LinearOneStep(), LinearDistribute(), SlopeFromPoints(), SystemOfEquations(),
    LinearInequality(), ParallelPerpendicular(), LinearWordProblem(),
    FunctionEvaluate(), AbsoluteValue(),
]
