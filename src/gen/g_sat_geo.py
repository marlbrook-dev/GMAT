"""SAT Geometry and Trigonometry (m_geo): angles, triangles, circles, volume, trig ratios."""
from framework import Gen, num, frac, ItemError
from fractions import Fraction as Fr
import math


class TriangleAngles(Gen):
    id = "sat_geo_angles"
    skill = "m_geo"
    section = "M"
    sub = "Lines, angles, and triangles"
    diff = 1

    def build(self, rng):
        a = rng.randint(25, 95)
        b = rng.randint(25, 150 - a)
        c = 180 - a - b
        if c < 15:
            raise ItemError("third angle too small to be readable")
        return {
            "stem": "In a triangle, two of the interior angles measure %d degrees and %d "
            "degrees. What is the measure of the third interior angle?" % (a, b),
            "answer": c,
            "distractors": [
                (360 - a - b, "using 360 degrees for the angle sum of a triangle instead of 180."),
                (180 - a, "subtracting only one of the two given angles."),
                (a + b, "adding the two given angles rather than subtracting their sum from 180."),
                (90 - a if 90 - a > 0 else 90 + a, "assuming the triangle is right and working from 90 degrees."),
                (c + 10, "an arithmetic slip in the subtraction."),
            ],
            "expl": "The interior angles of a triangle sum to 180 degrees, so the third angle "
            "is 180 minus %d minus %d, which is %d degrees." % (a, b, c),
        }


class Pythagorean(Gen):
    id = "sat_geo_pythag"
    skill = "m_geo"
    section = "M"
    sub = "Right triangles and trigonometry"
    diff = 2

    TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15),
               (6, 8, 10), (20, 21, 29), (12, 16, 20), (10, 24, 26), (15, 20, 25)]

    def build(self, rng):
        a, b, c = rng.choice(self.TRIPLES)
        k = rng.choice([1, 1, 2, 3])
        a, b, c = a * k, b * k, c * k
        find_hyp = rng.choice([True, False])
        if find_hyp:
            stem = ("A right triangle has legs of length %d and %d. What is the length of "
                    "the hypotenuse?" % (a, b))
            val = c
            ds = [(a + b, "adding the legs instead of using the Pythagorean theorem."),
                  (b - a if b > a else a - b, "subtracting the legs."),
                  (a * a + b * b, "stopping at the sum of the squares without taking the square root."),
                  (c + 1, "an arithmetic slip taking the square root."),
                  (max(a, b), "reporting the longer leg as the hypotenuse.")]
        else:
            stem = ("A right triangle has a hypotenuse of length %d and one leg of length %d. "
                    "What is the length of the other leg?" % (c, a))
            val = b
            ds = [(c - a, "subtracting the two given lengths instead of subtracting their squares."),
                  (c + a, "adding the two given lengths."),
                  (c * c - a * a, "stopping at the difference of the squares without taking the square root."),
                  (b + 1, "an arithmetic slip taking the square root."),
                  (c, "reporting the hypotenuse again.")]
        return {"stem": stem, "answer": val, "distractors": ds,
                "expl": "By the Pythagorean theorem the legs %d and %d and the hypotenuse %d "
                        "satisfy %d squared plus %d squared equals %d squared, so the missing "
                        "length is %d." % (a, b, c, a, b, c, val)}


class CircleAreaCircumference(Gen):
    id = "sat_geo_circle"
    skill = "m_geo"
    section = "M"
    sub = "Circles"
    diff = 2

    def build(self, rng):
        r = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
        ask = rng.choice(["area", "circumference"])
        given_d = rng.choice([True, False])
        given = 2 * r if given_d else r
        word = "diameter" if given_d else "radius"
        val = r * r if ask == "area" else 2 * r
        unit = "pi square units" if ask == "area" else "pi units"
        return {
            "stem": "A circle has a %s of %d units. What is the %s of the circle, in %s?"
            % (word, given, ask, unit),
            "answer": val,
            "distractors": [
                ((2 * r) ** 2 if ask == "area" and given_d else (r * r if ask == "circumference" else 2 * r),
                 "using the diameter where the formula calls for the radius, or the reverse."),
                (2 * r if ask == "area" else r * r, "using the formula for the other quantity."),
                (r, "reporting the radius rather than the quantity asked for."),
                (val * 2, "doubling the correct result."),
                (val + r, "adding the radius to the result."),
            ],
            "expl": "The radius is %d. Area is pi times the radius squared, which is %d pi, and "
            "circumference is 2 pi times the radius, which is %d pi. The question asks for the "
            "%s, so the answer is %d." % (r, r * r, 2 * r, ask, val),
        }


class RectangleArea(Gen):
    id = "sat_geo_rect"
    skill = "m_geo"
    section = "M"
    sub = "Area and volume"
    diff = 1

    def build(self, rng):
        w = rng.randint(3, 22)
        h = rng.randint(3, 22)
        if w == h:
            raise ItemError("square hides the area versus perimeter confusion")
        ask = rng.choice(["area", "perimeter"])
        val = w * h if ask == "area" else 2 * (w + h)
        return {
            "stem": "A rectangle has a width of %d units and a length of %d units. What is its "
            "%s?" % (w, h, ask),
            "answer": val,
            "distractors": [
                (2 * (w + h) if ask == "area" else w * h,
                 "computing the other quantity: area multiplies the sides, perimeter adds them all."),
                (w + h, "adding the two sides once instead of going all the way around."),
                (val + w, "an arithmetic slip adding one side too many."),
                (val * 2, "doubling the correct result."),
                (abs(w - h) if abs(w - h) > 1 else w * h + 1, "subtracting the sides."),
            ],
            "expl": "Area is width times length, which is %d. Perimeter is twice the sum of the "
            "sides, which is %d. The question asks for the %s, so the answer is %d."
            % (w * h, 2 * (w + h), ask, val),
        }


class Volume(Gen):
    id = "sat_geo_volume"
    skill = "m_geo"
    section = "M"
    sub = "Area and volume"
    diff = 3

    def build(self, rng):
        a, b, c = rng.randint(2, 12), rng.randint(2, 12), rng.randint(2, 12)
        val = a * b * c
        return {
            "stem": "A rectangular box has edge lengths of %d, %d, and %d units. What is the "
            "volume of the box, in cubic units?" % (a, b, c),
            "answer": val,
            "distractors": [
                (2 * (a * b + b * c + a * c), "computing the surface area rather than the volume."),
                (a + b + c, "adding the edge lengths instead of multiplying them."),
                (a * b, "multiplying only two of the three edges, which gives an area."),
                (4 * (a + b + c), "computing the total edge length."),
                (val * 2, "doubling the correct result."),
            ],
            "expl": "Volume of a rectangular box is the product of its three edge lengths: "
            "%d times %d times %d equals %d cubic units." % (a, b, c, val),
        }


class SimilarTriangles(Gen):
    id = "sat_geo_similar"
    skill = "m_geo"
    section = "M"
    sub = "Lines, angles, and triangles"
    diff = 3

    def build(self, rng):
        k = rng.choice([2, 3, 4, 5])
        a = rng.choice([3, 4, 5, 6, 7, 8, 9])
        b = rng.choice([4, 6, 8, 10, 12, 14])
        if a == b:
            raise ItemError("equal sides remove the scaling question")
        val = b * k
        return {
            "stem": "Triangle ABC is similar to triangle DEF, with side AB corresponding to "
            "side DE. If AB = %d, DE = %d, and BC = %d, what is the length of EF?"
            % (a, a * k, b),
            "answer": val,
            "distractors": [
                (b + (a * k - a), "adding the difference between the corresponding sides rather than applying the ratio."),
                (Fr(b, k), "dividing by the scale factor when the second triangle is the larger one."),
                (b, "copying the corresponding side without scaling it."),
                (a * k, "reporting the side that was given rather than the one asked for."),
                (val + k, "an arithmetic slip applying the scale factor."),
            ],
            "expl": "The scale factor from ABC to DEF is %d divided by %d, which is %d. "
            "Multiplying BC by that factor gives EF = %d times %d = %d."
            % (a * k, a, k, b, k, val),
        }


class TrigRatio(Gen):
    id = "sat_geo_trig"
    skill = "m_geo"
    section = "M"
    sub = "Right triangles and trigonometry"
    diff = 4

    TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]

    def build(self, rng):
        o, a, h = rng.choice(self.TRIPLES)
        fn = rng.choice(["sine", "cosine", "tangent"])
        val = {"sine": Fr(o, h), "cosine": Fr(a, h), "tangent": Fr(o, a)}[fn]
        return {
            "stem": "In right triangle ABC, the right angle is at C. The side opposite angle A "
            "has length %d, the side adjacent to angle A has length %d, and the hypotenuse has "
            "length %d. What is the %s of angle A?" % (o, a, h, fn),
            "answer": val,
            "distractors": [
                ({"sine": Fr(a, h), "cosine": Fr(o, h), "tangent": Fr(a, o)}[fn],
                 "swapping the opposite and adjacent sides, which turns each ratio into a different one."),
                ({"sine": Fr(h, o), "cosine": Fr(h, a), "tangent": Fr(a, o)}[fn],
                 "inverting the ratio."),
                (Fr(o, a) if fn != "tangent" else Fr(o, h),
                 "using the ratio for a different trigonometric function."),
                (Fr(a, o) if fn != "tangent" else Fr(h, o), "combining an inversion with the wrong pair of sides."),
            ],
            "expl": "Sine is opposite over hypotenuse, cosine is adjacent over hypotenuse, and "
            "tangent is opposite over adjacent. Here that gives %s of angle A equal to %s."
            % (fn, num(val)),
        }


class ParallelLinesAngles(Gen):
    id = "sat_geo_parallel"
    skill = "m_geo"
    section = "M"
    sub = "Lines, angles, and triangles"
    diff = 2

    def build(self, rng):
        a = rng.randint(28, 152)
        rel = rng.choice(["corresponding", "alternate interior", "same side interior"])
        val = a if rel != "same side interior" else 180 - a
        if val == a and rel == "same side interior":
            raise ItemError("degenerate right angle case")
        return {
            "stem": "Two parallel lines are cut by a transversal. One angle measures %d "
            "degrees. What is the measure of its %s angle?" % (a, rel),
            "answer": val,
            "distractors": [
                (180 - a if val == a else a,
                 "applying the supplementary rule where the angles are equal, or the reverse."),
                (90 - a if 90 - a > 0 else 90 + a, "assuming the angles are complementary."),
                (360 - a, "working from a full turn instead of a straight line."),
                (val + 10, "an arithmetic slip in the subtraction."),
                (2 * a if 2 * a < 180 else a // 2, "doubling or halving the given angle."),
            ],
            "expl": "When parallel lines are cut by a transversal, corresponding angles and "
            "alternate interior angles are equal, while same side interior angles are "
            "supplementary. Here the %s angle measures %d degrees." % (rel, val),
        }


GENS = [TriangleAngles(), Pythagorean(), CircleAreaCircumference(), RectangleArea(),
        Volume(), SimilarTriangles(), TrigRatio(), ParallelLinesAngles()]
