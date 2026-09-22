"""ACT Mathematics: Number and Quantity.

ACT's Number and Quantity category covers integer and rational exponents, radicals,
scientific notation, sequences, matrices, complex numbers and proportional reasoning with
units. The SAT pool this bank remaps from has only two schemas that genuinely sit here
(exponent rules and radical equations), which is why the category was thin; the rest of
what ACT asks about here has no SAT counterpart, so it is written directly.

Same contract as everything else: parameters are drawn, the answer is computed, and every
distractor is the result of a specific arithmetic error that the explanation names.
"""
from fractions import Fraction

from framework import Gen, ItemError, num


def commas(n):
    return "{:,}".format(int(n))


class NQBase(Gen):
    section = "M"
    skill = "act_m_nq"
    sub = "Number and quantity"
    diff = 2


class ScientificNotation(NQBase):
    id = "act_nq_scinot"

    def build(self, rng):
        a = round(rng.uniform(1.1, 9.4), 1)
        b = round(rng.uniform(1.1, 9.4), 1)
        m = rng.randint(3, 11)
        n = rng.randint(2, 9)
        op = rng.choice(["mul", "div"])
        if op == "mul":
            coef, exp = a * b, m + n
            shown = "(" + str(a) + " x 10^" + str(m) + ")(" + str(b) + " x 10^" + str(n) + ")"
            wrongexp, wrongname = m * n, "multiplying the exponents instead of adding them"
        else:
            coef, exp = a / b, m - n
            shown = "(" + str(a) + " x 10^" + str(m) + ") / (" + str(b) + " x 10^" + str(n) + ")"
            wrongexp, wrongname = m + n, "adding the exponents instead of subtracting them"
        coef = round(coef, 2)
        while coef >= 10:
            coef, exp = round(coef / 10, 3), exp + 1
        while coef < 1:
            coef, exp = round(coef * 10, 3), exp - 1
        coef = round(coef, 2)
        if coef in (0, 10):
            raise ItemError("coefficient landed on a boundary")
        fmt = lambda c, e: str(c) + " x 10^" + str(e)
        right = fmt(coef, exp)
        cands = [
            (fmt(coef, wrongexp), wrongname),
            (fmt(round(coef * 10, 2), exp - 1), "leaving the coefficient outside the range "
             "1 to 10 that scientific notation requires"),
            (fmt(round(coef / 10, 3), exp + 1), "shifting the point the wrong way when "
             "normalising the coefficient"),
            (fmt(round(a + b if op == "mul" else a - b, 2), exp),
             "adding the coefficients instead of " + ("multiplying" if op == "mul" else "dividing")
             + " them"),
            (fmt(coef, -exp), "reversing the sign of the exponent"),
            # Shorter than the key. Every candidate above carries either an extra digit in
            # the coefficient or an extra one in the exponent, so the key was the shortest
            # option on 73 percent of this schema's items (INC-0079). Rounding the
            # coefficient away is a real slip and is the only wrong answer here that is
            # shorter than the right one.
            (fmt(int(round(coef)), exp),
             "rounding the coefficient to a whole number, which throws away the precision "
             "the calculation actually gives"),
            # And one longer than the key, for the same reason: with candidates on one
            # side only, the balancer has nowhere to put the key and it piles up at one
            # rank whichever side that is.
            (fmt(round(coef * 100, 2), exp - 2),
             "shifting the decimal point two places while moving the exponent only two, "
             "which leaves the coefficient far outside the range 1 to 10"),
        ]
        return dict(stem="What is " + shown + ", expressed in scientific notation?",
                    answer=right, fmt=str, distractors=cands, diff=rng.choice([2, 3]),
                    expl="Handle the coefficients and the powers of ten separately. The "
                         "coefficients give " + str(a) + (" x " if op == "mul" else " / ")
                         + str(b) + ", and the powers give 10^" + str(m)
                         + (" x 10^" if op == "mul" else " / 10^") + str(n) + " = 10^"
                         + str(m + n if op == "mul" else m - n) + ". Normalising so the "
                         "coefficient sits between 1 and 10 gives " + right + ".")


class ArithmeticSequence(NQBase):
    id = "act_nq_arithseq"

    def build(self, rng):
        first = rng.randint(-14, 30)
        d = rng.choice([-9, -7, -5, -4, -3, 3, 4, 5, 6, 7, 8, 11])
        n = rng.randint(9, 40)
        ans = first + (n - 1) * d
        cands = [
            (first + n * d, "using n terms of the difference instead of n minus 1"),
            (first + (n - 2) * d, "using two fewer terms of the difference than the sequence has"),
            (first * d ** (n - 1) if abs(d) <= 2 else first + (n - 1) * abs(d),
             "treating the sequence as though the difference were always added, whatever "
             "its sign" if d < 0 else "reading the difference off the wrong pair of terms"),
            ((n - 1) * d, "leaving out the first term"),
            (first + (n - 1) * (d + 1), "reading the common difference off by one"),
        ]
        return dict(stem="In an arithmetic sequence the first term is " + num(first)
                         + " and each term after the first is " + num(d if d > 0 else -d)
                         + (" more" if d > 0 else " less") + " than the term before it. "
                         "What is the " + ordinal(n) + " term?",
                    answer=ans, distractors=cands, diff=rng.choice([1, 2, 2, 3]),
                    expl="The nth term of an arithmetic sequence is the first term plus "
                         "(n - 1) common differences, because the first term needs none. "
                         "Here that is " + num(first) + " + (" + str(n) + " - 1)("
                         + num(d) + ") = " + num(first) + " + " + num((n - 1) * d)
                         + " = " + num(ans) + ".")


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return str(n) + suf


class GeometricSequence(NQBase):
    id = "act_nq_geomseq"

    def build(self, rng):
        first = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
        r = rng.choice([2, 3, -2, -3])
        n = rng.randint(4, 8)
        ans = first * r ** (n - 1)
        cands = [
            (first * r ** n, "using n factors of the ratio instead of n minus 1"),
            (first * r * (n - 1), "multiplying by the ratio once and then by the term count"),
            (first + (n - 1) * r, "treating the sequence as arithmetic"),
            (abs(ans), "dropping the sign that an odd number of negative factors produces"
             if r < 0 else "reporting the magnitude of a different term"),
            (first * abs(r) ** (n - 1), "ignoring the sign of the common ratio"),
        ]
        return dict(stem="In a geometric sequence the first term is " + num(first)
                         + " and the common ratio is " + num(r) + ". What is the "
                         + ordinal(n) + " term?",
                    answer=ans, distractors=cands, diff=rng.choice([2, 3, 3]),
                    expl="The nth term is the first term multiplied by the common ratio "
                         "(n - 1) times: " + num(first) + " x (" + num(r) + ")^"
                         + str(n - 1) + " = " + num(ans) + ".")


class MatrixOps(NQBase):
    id = "act_nq_matrix"
    fmt = staticmethod(str)

    def build(self, rng):
        def m2(): return [[rng.randint(-6, 9) for _ in range(2)] for _ in range(2)]
        A, B = m2(), m2()
        k = rng.choice([2, 3, -1, -2, 4])
        op = rng.choice(["add", "scale", "sub"])
        if op == "add":
            R = [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]
            shown = "A + B"
            bad = [([[A[i][j] - B[i][j] for j in range(2)] for i in range(2)],
                    "subtracting the matrices instead of adding them"),
                   ([[A[i][j] + B[j][i] for j in range(2)] for i in range(2)],
                    "adding B transposed, that is, pairing each entry with the wrong one")]
        elif op == "sub":
            R = [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]
            shown = "A - B"
            bad = [([[A[i][j] + B[i][j] for j in range(2)] for i in range(2)],
                    "adding the matrices instead of subtracting them"),
                   ([[B[i][j] - A[i][j] for j in range(2)] for i in range(2)],
                    "subtracting in the wrong order")]
        else:
            R = [[k * A[i][j] for j in range(2)] for i in range(2)]
            shown = num(k) + "A"
            bad = [([[k * A[i][j] if (i, j) == (0, 0) else A[i][j] for j in range(2)]
                     for i in range(2)], "scaling only the first entry rather than every entry"),
                   ([[A[i][j] + k for j in range(2)] for i in range(2)],
                    "adding the scalar to each entry instead of multiplying by it")]
        def show(M):
            return "[" + "; ".join(" ".join(num(v) for v in row) for row in M) + "]"
        cands = [(show(M), why) for M, why in bad]
        cands += [(show([[R[1][0], R[1][1]], [R[0][0], R[0][1]]]), "writing the rows in the "
                   "wrong order"),
                  (show([[R[0][0], R[1][0]], [R[0][1], R[1][1]]]), "transposing the result"),
                  (show([[-v for v in row] for row in R]), "changing the sign of every entry")]
        return dict(stem="If A = " + show(A) + " and B = " + show(B) + ", where each matrix "
                         "is written row by row with rows separated by a semicolon, what is "
                         + shown + "?",
                    answer=show(R), fmt=str, distractors=cands, diff=rng.choice([2, 3]),
                    expl="Matrices of the same size are combined entry by entry, and a "
                         "scalar multiplies every entry. Working through position by "
                         "position gives " + show(R) + ".")


class ComplexArithmetic(NQBase):
    id = "act_nq_complex"
    fmt = staticmethod(str)

    def build(self, rng):
        a, b, c, d = (rng.randint(-7, 9) for _ in range(4))
        if b == 0 or d == 0:
            raise ItemError("not a complex draw")
        re_, im = a * c - b * d, a * d + b * c
        def cx(r, i):
            if i == 0:
                return num(r)
            return num(r) + (" + " if i > 0 else " - ") + (num(abs(i)) if abs(i) != 1 else "") + "i"
        right = cx(re_, im)
        cands = [
            (cx(a * c + b * d, a * d + b * c), "treating i squared as 1 rather than as -1"),
            (cx(a * c, b * d), "multiplying the real parts and the imaginary parts separately"),
            (cx(a * c - b * d, a * c + b * d), "using the wrong products for the imaginary part"),
            (cx(re_, -im), "reversing the sign of the imaginary part"),
            (cx(a + c, b + d), "adding the two numbers instead of multiplying them"),
        ]
        return dict(stem="What is (" + cx(a, b) + ")(" + cx(c, d) + ")? (i squared equals -1.)",
                    answer=right, fmt=str, distractors=cands, diff=rng.choice([3, 3, 4]),
                    expl="Expanding gives " + num(a * c) + " + " + num(a * d) + "i + "
                         + num(b * c) + "i + " + num(b * d) + "i squared. Since i squared is "
                         "-1, the last term contributes " + num(-b * d)
                         + " to the real part, so the result is " + right + ".")


class ProportionUnits(NQBase):
    id = "act_nq_proportion"

    def build(self, rng):
        per = rng.choice([3, 4, 5, 6, 8, 9, 12])
        each = rng.choice([7, 11, 13, 14, 15, 18, 22, 25])
        want = rng.choice([2, 3, 5, 6, 7, 9]) * per
        ans = Fraction(want * each, per)
        if ans.denominator != 1:
            raise ItemError("draw does not land on a whole number")
        ans = int(ans)
        cands = [
            (int(Fraction(want * per, each)) if (want * per) % each == 0 else want * per // each,
             "inverting the rate, dividing by the quantity rather than by the group size"),
            (want * each, "multiplying without dividing by the group size"),
            (each + (want - per), "adding the extra units rather than scaling"),
            (int(Fraction(each * per, want)) if (each * per) % want == 0 else each * per // want,
             "putting the wanted quantity in the denominator"),
            (ans + each, "counting one extra group"),
            (max(1, ans - each), "counting one group too few"),
        ]
        thing, unit = rng.choice([("bricks", "a wall section"), ("litres of paint", "a room"),
                                  ("sheets of plywood", "a shelf unit"),
                                  ("metres of cable", "a lighting run"),
                                  ("kilograms of feed", "a pen of animals")])
        # The rate is a total across a GROUP of units, not a per unit figure. An earlier
        # draft wrote "require N bricks each", which made the computed answer wrong by a
        # factor of the group size while the explanation talked itself out of the error.
        return dict(stem=str(per) + " identical units of " + unit + " require " + str(each)
                         + " " + thing + " in total. At the same rate, how many " + thing
                         + " are required for " + str(want) + " such units?",
                    answer=ans, distractors=cands, diff=rng.choice([1, 2, 2]),
                    expl=str(per) + " units take " + str(each) + " " + thing + ", so one "
                         "unit takes " + str(each) + "/" + str(per) + " and " + str(want)
                         + " units take " + str(want) + " x " + str(each) + "/" + str(per)
                         + " = " + commas(ans) + " " + thing + ".")


GENS = [ScientificNotation(), ArithmeticSequence(), GeometricSequence(), MatrixOps(),
        ComplexArithmetic(), ProportionUnits()]
