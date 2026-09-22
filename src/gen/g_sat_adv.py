"""SAT Advanced Math (m_adv) generators: quadratics, exponentials, polynomials, radicals."""
from framework import Gen, num, frac, ItemError
from fractions import Fraction as Fr


class QuadraticRoots(Gen):
    id = "sat_adv_quadroots"
    skill = "m_adv"
    section = "M"
    sub = "Nonlinear equations in one variable"
    diff = 3

    def build(self, rng):
        r1 = rng.choice([-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
                         1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        r2 = rng.choice([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
                         1, 2, 3, 4, 5, 6, 7, 9, 11, 12])
        if r1 == r2:
            raise ItemError("repeated root makes the sum question trivial")
        b, c = -(r1 + r2), r1 * r2
        ask = rng.choice(["sum", "product", "larger"])
        val = {"sum": r1 + r2, "product": r1 * r2, "larger": max(r1, r2)}[ask]
        label = {"sum": "the sum of the solutions", "product": "the product of the solutions",
                 "larger": "the greater solution"}[ask]
        return {
            "stem": "In the equation x squared %s %dx %s %d = 0, what is %s?"
            % ("+" if b >= 0 else "-", abs(b), "+" if c >= 0 else "-", abs(c), label),
            "answer": val,
            "distractors": [
                (-val, "reading the coefficients straight off the equation without the sign change that factoring introduces."),
                ({"sum": r1 * r2, "product": r1 + r2, "larger": min(r1, r2)}[ask],
                 "answering a different question about the same two roots."),
                (b, "reporting the coefficient of x rather than a fact about the solutions."),
                (c, "reporting the constant term rather than a fact about the solutions."),
                (val + 1, "an off by one slip while finding the factor pair."),
            ],
            "expl": "The expression factors as (x %s %d)(x %s %d), so the solutions are %d and "
            "%d, and %s is %d."
            % ("-" if r1 >= 0 else "+", abs(r1), "-" if r2 >= 0 else "+", abs(r2),
               r1, r2, label, val),
        }


class VertexForm(Gen):
    id = "sat_adv_vertex"
    skill = "m_adv"
    section = "M"
    sub = "Nonlinear functions"
    diff = 3

    def build(self, rng):
        a = rng.choice([1, 1, 2, -1, -2, 3])
        h = rng.choice([-6, -4, -3, -2, -1, 1, 2, 3, 5])
        k = rng.choice([-11, -8, -5, -2, 3, 6, 9, 14])
        ask = rng.choice(["x", "y"])
        val = h if ask == "x" else k
        return {
            "stem": "The function f is defined by f(x) = %s(x %s %d) squared %s %d. What is the "
            "%s coordinate of the vertex of the graph of f in the xy-plane?"
            % (num(a), "+" if -h >= 0 else "-", abs(h), "+" if k >= 0 else "-", abs(k),
               "x" if ask == "x" else "y"),
            "answer": val,
            "distractors": [
                (-val, "reading the number inside the parentheses at face value instead of flipping its sign, which is exactly backwards."),
                (k if ask == "x" else h, "reading the wrong coordinate off vertex form."),
                (a, "reading the leading coefficient as a coordinate."),
                (val + a, "combining the leading coefficient into the coordinate, which vertex form never requires."),
                (val * 2, "doubling the coordinate for no reason the form supports."),
            ],
            "expl": "In vertex form f(x) = a(x - h) squared + k, the vertex is (h, k). Here h = %d "
            "and k = %d, so the %s coordinate is %d." % (h, k, "x" if ask == "x" else "y", val),
        }


class ExponentialGrowth(Gen):
    id = "sat_adv_exponential"
    skill = "m_adv"
    section = "M"
    sub = "Nonlinear functions"
    diff = 3

    def build(self, rng):
        p0 = rng.choice([40, 50, 80, 120, 150, 200, 250, 300])
        pct = rng.choice([5, 10, 20, 25, 50])
        n = rng.choice([2, 3, 4])
        grow = rng.choice([True, False])
        mult = Fr(100 + pct, 100) if grow else Fr(100 - pct, 100)
        val = p0 * mult ** n
        word = "increases" if grow else "decreases"
        return {
            "stem": "A quantity begins at %d and %s by %d percent each year. What is the quantity "
            "after %d years?" % (p0, word, pct, n),
            "answer": val,
            "distractors": [
                (p0 + (p0 * Fr(pct, 100) * n if grow else -p0 * Fr(pct, 100) * n),
                 "applying the percent change as a flat amount each year rather than compounding it."),
                (p0 * mult, "applying the change for a single year instead of %d." % n),
                (p0 * mult ** (n + 1), "applying the change one extra time."),
                (p0 * Fr(pct, 100) ** n, "using the percent itself as the multiplier instead of one plus or minus the percent."),
            ],
            "expl": "Each year multiplies the quantity by %s, so after %d years the quantity is "
            "%d times %s to the power %d, which is %s."
            % (num(mult), n, p0, num(mult), n, num(val)),
        }


class PolynomialValue(Gen):
    id = "sat_adv_polyfactor"
    skill = "m_adv"
    section = "M"
    sub = "Equivalent expressions"
    diff = 3

    def build(self, rng):
        a = rng.choice([1, 2, 3, 4, 5])
        b = rng.choice([-9, -8, -7, -6, -5, -3, -2, 2, 3, 4, 6, 7])
        c = rng.choice([-9, -7, -6, -4, -2, 3, 4, 5, 8, 9])
        # (ax + b)(x + c) expanded
        A, B, C = a, a * c + b, b * c
        ask = rng.choice(["b", "c"])
        val = B if ask == "b" else C
        return {
            "stem": "The expression (%dx %s %d)(x %s %d) is equivalent to %dx squared + bx + c, "
            "where b and c are constants. What is the value of %s?"
            % (a, "+" if b >= 0 else "-", abs(b), "+" if c >= 0 else "-", abs(c), A, ask),
            "answer": val,
            "distractors": [
                (b + c if ask == "b" else b + c,
                 "adding the two constants and stopping, which skips the cross terms entirely."),
                (C if ask == "b" else B, "computing the other coefficient."),
                (-val, "expanding correctly and then dropping a sign."),
                (b * c if ask == "b" else b * a, "multiplying the wrong pair of terms."),
                (val + a, "folding the leading coefficient in a second time."),
            ],
            "expl": "Expanding gives %dx squared %s %dx %s %d, so b = %d and c = %d."
            % (A, "+" if B >= 0 else "-", abs(B), "+" if C >= 0 else "-", abs(C), B, C),
        }


class RadicalEquation(Gen):
    id = "sat_adv_radical"
    skill = "m_adv"
    section = "M"
    sub = "Nonlinear equations in one variable"
    diff = 4

    def build(self, rng):
        k = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        b = rng.choice([-13, -11, -9, -8, -7, -6, -5, -3, -2,
                        2, 3, 4, 5, 6, 7, 9, 11, 13])
        # sqrt(x + b) = k  ->  x = k^2 - b
        x = k * k - b
        return {
            "stem": "If the square root of (x %s %d) equals %d, what is the value of x?"
            % ("+" if b >= 0 else "-", abs(b), k),
            "answer": x,
            "distractors": [
                (k - b, "squaring nothing at all and simply moving the constant across."),
                (k * k + b, "adding the constant when it should be subtracted, or the reverse."),
                (2 * k - b, "doubling the number instead of squaring it."),
                (k * k, "squaring correctly but forgetting the constant inside the radical."),
                (-x, "solving correctly and then dropping the sign."),
            ],
            "expl": "Square both sides to get x %s %d = %d, then solve for x, which gives x = %d."
            % ("+" if b >= 0 else "-", abs(b), k * k, x),
        }


class RationalExpression(Gen):
    id = "sat_adv_rational"
    skill = "m_adv"
    section = "M"
    sub = "Equivalent expressions"
    diff = 4

    def build(self, rng):
        r = rng.choice([-9, -8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8, 9])
        s = rng.choice([-9, -8, -7, -6, -5, -4, -3, -2, 3, 4, 5, 6, 8, 9])
        if r == s:
            raise ItemError("cancelling factor must differ")
        k = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        val = k - s
        return {
            "stem": "For x not equal to %d, the expression (x squared %s %dx %s %d) divided by "
            "(x %s %d) is equivalent to x %s %d. What is the value of the expression when x = %d?"
            % (r,
               "+" if -(r + s) >= 0 else "-", abs(r + s),
               "+" if r * s >= 0 else "-", abs(r * s),
               "-" if r >= 0 else "+", abs(r),
               "-" if s >= 0 else "+", abs(s), k),
            "answer": val,
            "distractors": [
                (k - r, "cancelling the wrong factor and keeping the one that divides out."),
                (k + s, "keeping the sign of the remaining root instead of subtracting it."),
                (k * k - (r + s) * k + r * s, "substituting into the numerator and never dividing."),
                (val * -1, "sign slip after the cancellation."),
                (val + 1, "an off by one slip in the factor pair."),
            ],
            "expl": "The numerator factors as (x %s %d)(x %s %d). Cancelling (x %s %d) leaves "
            "x %s %d, and at x = %d that is %d."
            % ("-" if r >= 0 else "+", abs(r), "-" if s >= 0 else "+", abs(s),
               "-" if r >= 0 else "+", abs(r), "-" if s >= 0 else "+", abs(s), k, val),
        }


class SystemLineParabola(Gen):
    id = "sat_adv_nonlinsys"
    skill = "m_adv"
    section = "M"
    sub = "Systems of equations"
    diff = 4

    def build(self, rng):
        p = rng.choice([-5, -4, -3, -2, 1, 2, 3, 4])
        q = rng.choice([-4, -2, 1, 3, 5, 6])
        if p == q:
            raise ItemError("tangent case has one solution")
        # y = x^2 and y = (p+q)x - pq intersect at x = p and x = q
        m, b = p + q, -p * q
        ask = rng.choice(["sum", "larger"])
        val = p + q if ask == "sum" else max(p, q)
        label = "the sum of the x coordinates" if ask == "sum" else "the greater x coordinate"
        return {
            "stem": "In the xy-plane, the graph of y = x squared intersects the line "
            "y = %dx %s %d at two points. What is %s of those points?"
            % (m, "+" if b >= 0 else "-", abs(b), label),
            "answer": val,
            "distractors": [
                (-val, "setting the quadratic equal to zero with the signs of the line reversed."),
                (min(p, q) if ask == "larger" else p * q,
                 "answering about the other intersection, or about the product instead of the sum."),
                (b, "reporting the intercept of the line rather than an x coordinate."),
                (val * val, "reporting the y coordinate, which is the square of the x coordinate."),
                (val + 1, "an off by one slip while factoring."),
            ],
            "expl": "Setting x squared = %dx %s %d gives x squared %s %dx %s %d = 0, which "
            "factors to (x %s %d)(x %s %d) = 0. The x coordinates are %d and %d, so %s is %d."
            % (m, "+" if b >= 0 else "-", abs(b),
               "-" if m >= 0 else "+", abs(m), "+" if -b >= 0 else "-", abs(b),
               "-" if p >= 0 else "+", abs(p), "-" if q >= 0 else "+", abs(q),
               p, q, label, val),
        }


class ExponentRules(Gen):
    id = "sat_adv_exprules"
    skill = "m_adv"
    section = "M"
    sub = "Equivalent expressions"
    diff = 2

    def build(self, rng):
        m = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        n = rng.choice([2, 3, 4, 5, 6, 7])
        op = rng.choice(["mul", "div", "pow"])
        if op == "mul":
            stem = "The expression x to the %d times x to the %d is equivalent to x to the k. What is k?" % (m, n)
            val, wrong1, why1 = m + n, m * n, "multiplying the exponents, which is the rule for a power raised to a power, not for a product."
            wrong2, why2 = abs(m - n), "subtracting the exponents, which is the rule for a quotient, not for a product."
        elif op == "div":
            if m <= n:
                m, n = n + rng.choice([1, 2, 3]), n
            stem = "The expression x to the %d divided by x to the %d is equivalent to x to the k. What is k?" % (m, n)
            val, wrong1, why1 = m - n, Fr(m, n), "dividing the exponents rather than subtracting them."
            wrong2, why2 = m + n, "adding the exponents, which is the rule for a product, not for a quotient."
        else:
            stem = "The expression (x to the %d) raised to the power %d is equivalent to x to the k. What is k?" % (m, n)
            val, wrong1, why1 = m * n, m + n, "adding the exponents, which is the rule for multiplying like bases, not for a power of a power."
            wrong2, why2 = abs(m - n), "subtracting the exponents, which is the rule for a quotient, not for a power of a power."
        return {
            "stem": stem,
            "answer": val,
            "distractors": [
                (wrong1, why1),
                (m, "keeping only the first exponent."),
                (n, "keeping only the second exponent."),
                (val + 1, "an off by one slip applying the rule."),
                (wrong2, why2),
            ],
            "expl": "Like bases combine by adding exponents when multiplied, subtracting when "
            "divided, and multiplying when a power is raised to a power. Here k = %s." % num(val),
        }


GENS = [QuadraticRoots(), VertexForm(), ExponentialGrowth(), PolynomialValue(),
        RadicalEquation(), RationalExpression(), SystemLineParabola(), ExponentRules()]
