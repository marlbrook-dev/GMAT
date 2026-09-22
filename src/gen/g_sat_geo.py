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
        # Three question forms, not two, and the third is here for the shape of its
        # answer as much as for the skill. Asked forward, the key is r squared or 2r,
        # and two distractors are larger than it by construction while only the radius
        # is smaller, so the key landed at value rank 2 or 3 on every single draw and
        # never at rank 1, 4 or 5. Working backwards from the area or circumference to
        # the radius puts the key at the bottom of the set instead, which is both a real
        # question form and the missing half of the distribution (INC-0088 recorded the
        # tell; this is the fix rather than another recorded figure).
        roll = rng.random()
        if roll < 0.28:
            return self._backwards(rng)
        if roll < 0.50:
            return self._across(rng)
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

    def _across(self, rng):
        """Given the circumference, find the area.

        The third shape of answer this schema needed. Asked forward the key sits at
        value rank 2 or 3 and never higher, because the doubling errors are always
        above it; asked backwards for the radius it sits at rank 1. Here it is the area,
        which is larger than the radius, the diameter and twice the diameter, so the key
        lands near the top and the distribution finally covers the range (INC-0088).
        """
        r = rng.choice([5, 6, 7, 8, 9, 10, 12])
        return {
            "stem": "A circle has a circumference of %d pi units. What is the area of the "
                    "circle, in pi square units?" % (2 * r),
            "answer": r * r,
            "distractors": [
                (2 * r, "reporting the circumference given rather than the area."),
                (r, "reporting the radius rather than the area."),
                (4 * r, "squaring the 2 in 2 pi r instead of squaring the radius."),
                (2 * r * r, "doubling the area."),
                (4 * r * r, "squaring the diameter rather than the radius."),
            ],
            "expl": "A circumference of %d pi means 2 r equals %d, so the radius is %d. The "
                    "area is pi times the radius squared, which is %d pi square units."
                    % (2 * r, 2 * r, r, r * r),
        }

    def _backwards(self, rng):
        """Given the area or the circumference, find the radius.

        r starts at 3 rather than 2 because at r equal to 2 the distractors collapse:
        the diameter and the area are both 4, and twice the area and four times the
        radius are both 8, which leaves two distinct wrong answers where four are needed.
        """
        # 4 is left out: there the area and twice the radius are both 16 and the pool
        # collapses to three distinct wrong answers where four are needed. 2 is out for
        # the same reason one step down.
        r = rng.choice([3, 5, 6, 7, 8, 9, 10, 12])
        from_area = rng.choice([True, False])
        given = r * r if from_area else 2 * r
        what = "an area of %d pi square units" % given if from_area \
            else "a circumference of %d pi units" % given
        # Five named misconceptions, not four, because the number given in the question
        # is itself one of the others in each case: it is the area when the area is
        # given and the diameter when the circumference is. Four survive either way,
        # which is what a five choice item needs.
        return {
            "stem": "A circle has %s. What is the radius of the circle, in units?" % what,
            "answer": r,
            "distractors": [
                (2 * r, "reporting the diameter rather than the radius."),
                (4 * r, "doubling the diameter."),
                (r * r, "computing the area rather than reading off the radius."),
                (2 * r * r, "doubling the area instead of working back to the radius."),
                (given, "reporting the number given in the question rather than working "
                        "back from it."),
            ],
            "expl": "Area is pi times the radius squared and circumference is 2 pi times the "
            "radius, so %s gives a radius of %d. The question asks for the radius itself, "
            "not the diameter, which is %d." % (what, r, 2 * r),
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
        # Split by what is asked, because the two questions need wrong answers on
        # different sides of the key. Every characteristic slip on an area question
        # lands BELOW the product and every one on a perimeter question lands above it,
        # so a single shared list left the key at the same value rank on two items in
        # five. Each list now reaches both ways: the fence post count and the area plus
        # perimeter sum sit above an area key, and counting one pair of sides once or
        # not at all sits below a perimeter key.
        wrong = {
            "area": [
                (2 * (w + h), "computing the perimeter: area multiplies the sides, perimeter adds them all."),
                (w + h, "adding the two sides once instead of multiplying them."),
                (val + w, "an arithmetic slip adding one side to the product."),
                (val * 2, "doubling the correct result."),
                (abs(w - h) if abs(w - h) > 1 else w + h + 1, "subtracting the sides."),
                ((w + 1) * (h + 1), "counting the grid lines rather than the squares between them."),
                (val + 2 * (w + h), "adding the perimeter to the area, which are not the same kind of quantity."),
            ],
            "perimeter": [
                (w * h, "computing the area: perimeter adds the sides, area multiplies them."),
                (w + h, "adding the two sides once instead of going all the way around."),
                (2 * w + h, "doubling one pair of sides and counting the other pair once."),
                (val * 2, "doubling the correct result."),
                (abs(w - h) if abs(w - h) > 1 else w + h + 1, "subtracting the sides."),
                (4 * max(w, h), "treating the rectangle as a square on its longer side."),
                (4 * min(w, h), "treating the rectangle as a square on its shorter side."),
            ],
        }[ask]
        return {
            "stem": "A rectangle has a width of %d units and a length of %d units. What is its "
            "%s?" % (w, h, ask),
            "answer": val,
            "distractors": wrong,
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
            # Almost every slip on a volume question is a smaller number than the
            # product of three edges, so the key sat at the same value rank on close to
            # half the items with only one wrong answer above it. Cubing the longest
            # edge and doubling every edge both land above, and the sum of the three
            # face areas lands below, which gives the rank somewhere to move.
            "distractors": [
                (2 * (a * b + b * c + a * c), "computing the surface area rather than the volume."),
                (a + b + c, "adding the edge lengths instead of multiplying them."),
                (a * b, "multiplying only two of the three edges, which gives an area."),
                (4 * (a + b + c), "computing the total edge length."),
                (val * 2, "doubling the correct result."),
                (a * b + b * c + a * c, "adding the three face areas instead of multiplying the edges."),
                (max(a, b, c) ** 3, "cubing the longest edge as though the box were a cube."),
                (8 * val, "doubling every edge length, which multiplies the volume by eight."),
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

    # Twelve primitive triples rather than five, and either leg may be the opposite one.
    # Five triples times three functions is fifteen scenarios, which is why this schema
    # shipped twenty items and why its answer sat at one value rank on half of them: a
    # rank distribution over fifteen cases is fifteen points, not a distribution. Twelve
    # triples times two orientations times three functions is seventy two, and the
    # orientation swap is not padding, since the sine of one acute angle is the cosine of
    # the other and the two give genuinely different ratios.
    TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29),
               (9, 40, 41), (12, 35, 37), (28, 45, 53), (11, 60, 61), (16, 63, 65),
               (33, 56, 65), (48, 55, 73)]

    def build(self, rng):
        o, a, h = rng.choice(self.TRIPLES)
        if rng.random() < 0.5:
            o, a = a, o
        fn = rng.choice(["sine", "cosine", "tangent"])
        val = {"sine": Fr(o, h), "cosine": Fr(a, h), "tangent": Fr(o, a)}[fn]
        # Written out per function rather than as three parallel lookups, because the
        # lookups hid two faults. Swapping the legs and inverting the ratio are the same
        # arithmetic for the tangent, so it offered three distinct wrong answers where
        # the five choice exams need four, and every tangent item raised rather than
        # built: a third of the schema was missing from the GRE and nobody could see it
        # from the table. And every wrong answer here is built by making the ratio LARGER
        # (inverting) or by trading a leg for the longer hypotenuse, so the key was the
        # smallest of five options on half the items and the largest on none of them.
        # Dividing by the sum of the two legs is the one common slip that lands BELOW the
        # right answer, which is why each function carries it.
        wrong = {
            "sine": [
                (Fr(a, h), "using the adjacent side where the sine wants the opposite one."),
                (Fr(h, o), "inverting the ratio."),
                (Fr(o, a), "giving the tangent ratio instead of the sine."),
                (Fr(a, o), "combining an inversion with the wrong pair of sides."),
                (Fr(h, a), "inverting the ratio and taking the adjacent side as well."),
                (Fr(o, o + a), "dividing by the sum of the two legs rather than by the hypotenuse."),
                (Fr(o, o + a + h), "dividing by the perimeter of the triangle rather than by the hypotenuse."),
            ],
            "cosine": [
                (Fr(o, h), "using the opposite side where the cosine wants the adjacent one."),
                (Fr(h, a), "inverting the ratio."),
                (Fr(o, a), "giving the tangent ratio instead of the cosine."),
                (Fr(a, o), "combining an inversion with the wrong pair of sides."),
                (Fr(h, o), "inverting the ratio and taking the opposite side as well."),
                (Fr(a, o + a), "dividing by the sum of the two legs rather than by the hypotenuse."),
                (Fr(a, o + a + h), "dividing by the perimeter of the triangle rather than by the hypotenuse."),
            ],
            "tangent": [
                (Fr(a, o), "inverting the ratio, which gives the tangent of the other acute angle."),
                (Fr(o, h), "giving the sine ratio instead of the tangent."),
                (Fr(a, h), "giving the cosine ratio instead of the tangent."),
                (Fr(h, o), "inverting the sine ratio."),
                (Fr(h, a), "inverting the cosine ratio."),
                (Fr(o, o + a), "dividing by the sum of the two legs rather than by the adjacent one."),
                (Fr(o, o + a + h), "dividing by the perimeter of the triangle rather than by the adjacent side."),
            ],
        }[fn]
        return {
            "stem": "In right triangle ABC, the right angle is at C. The side opposite angle A "
            "has length %d, the side adjacent to angle A has length %d, and the hypotenuse has "
            "length %d. What is the %s of angle A?" % (o, a, h, fn),
            "answer": val,
            "distractors": wrong,
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
