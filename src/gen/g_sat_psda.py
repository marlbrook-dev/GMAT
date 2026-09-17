"""SAT Problem Solving and Data Analysis (m_psda): ratios, rates, percents, statistics, probability."""
from framework import Gen, num, money, frac, ItemError
from fractions import Fraction as Fr


class PercentOf(Gen):
    id = "sat_psda_percent"
    skill = "m_psda"
    section = "M"
    sub = "Percentages"
    diff = 1

    def build(self, rng):
        pct = rng.choice([4, 5, 8, 12, 15, 18, 20, 24, 25, 30, 35, 40, 60, 75])
        base = rng.choice([40, 60, 80, 120, 150, 180, 200, 250, 320, 400, 450, 500])
        val = Fr(pct, 100) * base
        return {
            "stem": "What is %d percent of %d?" % (pct, base),
            "answer": val,
            "distractors": [
                (Fr(base, pct) if pct else None, "dividing the base by the percent instead of multiplying by the percent as a decimal."),
                (pct * base, "multiplying by the percent as a whole number and never dividing by 100."),
                (base - val, "finding the part that remains rather than the part asked for."),
                (Fr(pct, 100) * base * 10, "misplacing the decimal point by one place."),
                (val + pct, "adding the percent to the answer."),
            ],
            "expl": "%d percent is %s as a fraction, and %s of %d is %s."
            % (pct, num(Fr(pct, 100)), num(Fr(pct, 100)), base, num(val)),
        }


def pctstr(fr):
    """A percentage as a number, not as an improper fraction.

    Dividing by the new value rather than the original one rarely lands on a whole number,
    and rendering the result as "100/3 percent" made that distractor visibly different from
    every other option. The key was then the SHORTEST choice on 88 percent of these items,
    which is a tell a student can use without doing the arithmetic. One decimal place puts
    every option in the same form, and it is how an answer choice would really be written.
    """
    v = float(fr)
    if abs(v - round(v)) < 1e-9:
        return "%d percent" % int(round(v))
    return "%.1f percent" % v


class PercentChange(Gen):
    id = "sat_psda_pctchange"
    skill = "m_psda"
    section = "M"
    sub = "Percentages"
    diff = 3

    def build(self, rng):
        old = rng.choice([40, 50, 60, 80, 120, 150, 200, 250, 400])
        pct = rng.choice([10, 15, 20, 25, 30, 40, 50, 60])
        up = rng.choice([True, False])
        new = old + (Fr(pct, 100) * old if up else -Fr(pct, 100) * old)
        return {
            "stem": "A value %s from %d to %s. What was the percent %s?"
            % ("increased" if up else "decreased", old, num(new),
               "increase" if up else "decrease"),
            "answer": "%s percent" % num(pct),
            "distractors": [
                (pctstr(Fr(abs(new - old) * 100, new)) if new else None,
                 "dividing the change by the new value instead of the original value."),
                ("%s percent" % num(abs(new - old)), "reporting the raw change instead of converting it to a percent."),
                (pctstr(Fr(new * 100, old)), "reporting the new value as a percent of the old rather than the change."),
                ("%s percent" % num(pct + 10), "an arithmetic slip in the division."),
                ("%s percent" % num(100 - pct), "subtracting from 100, which answers what fraction remains, not how much it changed."),
            ],
            "expl": "Percent change is the change divided by the original value: %s divided by "
            "%d is %s, which is %d percent."
            % (num(abs(new - old)), old, num(Fr(abs(new - old), old)), pct),
            "fmt": str,
        }


class UnitRate(Gen):
    id = "sat_psda_rate"
    skill = "m_psda"
    section = "M"
    sub = "Ratios, rates, and proportions"
    diff = 2

    SETUPS = [
        ("A machine produces {a} parts in {b} minutes at a constant rate.", "parts", "minutes", "How many parts does it produce in {c} minutes?"),
        ("A car travels {a} miles on {b} gallons of fuel.", "miles", "gallons", "How many miles does it travel on {c} gallons?"),
        ("A printer prints {a} pages in {b} seconds at a constant rate.", "pages", "seconds", "How many pages does it print in {c} seconds?"),
    ]

    def build(self, rng):
        setup, unit, per, ask = rng.choice(self.SETUPS)
        b = rng.choice([2, 3, 4, 5, 6, 8])
        rate = rng.choice([3, 5, 6, 7, 9, 12, 15, 20, 25])
        a = rate * b
        c = rng.choice([9, 10, 12, 14, 15, 18, 20, 24, 30])
        val = rate * c
        return {
            "stem": setup.format(a=a, b=b) + " " + ask.format(c=c),
            "answer": val,
            "distractors": [
                (Fr(a * b, c) if c else None, "inverting the rate, dividing by the wrong quantity."),
                (a + c, "adding the two numbers instead of scaling by the rate."),
                (Fr(c * b, a) if a else None, "setting up the proportion upside down."),
                (a * c, "multiplying by the total rather than by the rate per unit."),
                (rate, "finding the rate and stopping before applying it to %d %s." % (c, per)),
            ],
            "expl": "The rate is %d %s divided by %d %s, which is %d %s per %s. Over %d %s that "
            "gives %d %s." % (a, unit, b, per, rate, unit, per[:-1], c, per, val, unit),
        }


class MeanMedian(Gen):
    id = "sat_psda_center"
    skill = "m_psda"
    section = "M"
    sub = "One variable data: distributions and measures of center and spread"
    diff = 3

    def build(self, rng):
        n = rng.choice([5, 7])
        vals = sorted(rng.sample(range(2, 60), n))
        # Nudge the last value so the mean is a whole number. A mean that lands on
        # a fraction forces fractional distractors into a question whose other
        # measures are integers, and the odd one out gives the answer away.
        rem = sum(vals) % n
        if rem:
            bump = n - rem
            vals[-1] += bump
            vals = sorted(vals)
        mean = sum(vals) // n
        median = vals[n // 2]
        rng_val = vals[-1] - vals[0]
        ask = rng.choice(["mean", "median", "range"])
        val = {"mean": mean, "median": median, "range": rng_val}[ask]
        others = {"mean": [median, rng_val], "median": [mean, rng_val],
                  "range": [mean, median]}[ask]
        return {
            "stem": "A data set consists of the values %s. What is the %s of the data set?"
            % (", ".join(str(v) for v in vals), ask),
            "answer": val,
            "distractors": [
                (others[0], "computing a different measure of the same data than the one named."),
                (others[1], "computing another measure of the same data than the one named."),
                (vals[n // 2 - 1], "picking a value next to the middle one rather than the middle one."),
                (sum(vals) // (n - 1), "dividing by one fewer than the number of values."),
                (vals[-1], "reporting the largest value."),
                (vals[0], "reporting the smallest value."),
                (val + 1, "an off by one slip while counting positions or adding."),
            ],
            "expl": "In order the values are %s. The mean is %d, the median is %d, and the "
            "range is %d, so the %s is %d."
            % (", ".join(str(v) for v in vals), mean, median, rng_val, ask, val),
        }


class Probability(Gen):
    id = "sat_psda_prob"
    skill = "m_psda"
    section = "M"
    sub = "Probability and conditional probability"
    diff = 3

    def build(self, rng):
        a = rng.choice([3, 4, 5, 6, 7, 8, 9, 12])
        b = rng.choice([5, 6, 7, 8, 10, 11, 13, 15])
        total = a + b
        p = Fr(a, total)
        return {
            "stem": "A bag contains %d red marbles and %d blue marbles and no others. If one "
            "marble is selected at random, what is the probability that it is red?" % (a, b),
            "answer": p,
            "distractors": [
                (Fr(a, b), "putting the red count over the blue count instead of over the total."),
                (Fr(b, total), "finding the probability of the other colour."),
                (Fr(total, a), "inverting the probability."),
                (Fr(a, total) * 2, "double counting the favourable outcomes."),
                (Fr(b, a), "inverting the ratio of the two colours."),
            ],
            "expl": "There are %d marbles in all and %d are red, so the probability is %d over "
            "%d, which is %s." % (total, a, a, total, num(p)),
        }


class TwoWayTable(Gen):
    id = "sat_psda_table"
    skill = "m_psda"
    section = "M"
    sub = "Two variable data"
    diff = 4

    def build(self, rng):
        a, b = rng.randint(12, 60), rng.randint(12, 60)
        c, d = rng.randint(12, 60), rng.randint(12, 60)
        rowtot = a + b
        p = Fr(a, rowtot)
        return {
            "stem": "In a survey, %d students chose option one and %d chose option two among "
            "the first group, while %d chose option one and %d chose option two among the "
            "second group. If a student is selected at random from the first group, what is "
            "the probability that the student chose option one?" % (a, b, c, d),
            "answer": p,
            "distractors": [
                (Fr(a, a + b + c + d), "dividing by the total of everyone surveyed instead of by the first group only."),
                (Fr(a, a + c), "dividing by the total who chose option one rather than by the group."),
                (Fr(b, rowtot), "finding the probability of the other option."),
                (Fr(a + c, a + b + c + d), "combining both groups when the question restricts to one."),
                (Fr(rowtot, a), "inverting the probability."),
            ],
            "expl": "The first group has %d + %d = %d students, and %d of them chose option "
            "one, so the probability is %s." % (a, b, rowtot, a, num(p)),
        }


class LinearModelInterpret(Gen):
    id = "sat_psda_model"
    skill = "m_psda"
    section = "M"
    sub = "Two variable data: models and scatterplots"
    diff = 3

    def build(self, rng):
        b = rng.choice([12, 18, 25, 30, 42, 55, 64])
        m = rng.choice([3, 4, 5, 7, 8, 11])
        thing = rng.choice(["weeks", "months", "years"])
        return {
            "stem": "A line of best fit for a data set is given by y = %dx + %d, where x is the "
            "number of %s since the study began. Which statement best interprets the number %d "
            "in this model?" % (m, b, thing, m),
            "answer": "The predicted value of y increases by %d for each additional %s." % (m, thing[:-1]),
            "distractors": [
                ("The predicted value of y is %d when the study begins." % m,
                 "reading the slope as the starting value, which is what the other constant reports."),
                ("The predicted value of y increases by %d for each additional %s." % (b, thing[:-1]),
                 "swapping the two constants in the model."),
                ("The predicted value of y is %d after one %s." % (m, thing[:-1]),
                 "treating the rate of change as a single predicted value."),
                ("The predicted value of y decreases by %d for each additional %s." % (m, thing[:-1]),
                 "reading a positive slope as a decrease."),
            ],
            "expl": "In y = mx + b the coefficient m is the rate of change: each additional %s "
            "adds %d to the predicted value of y. The constant %d is the predicted value at "
            "x = 0." % (thing[:-1], m, b),
            "fmt": str,
        }


class UnitConversion(Gen):
    id = "sat_psda_units"
    skill = "m_psda"
    section = "M"
    sub = "Ratios, rates, and proportions"
    diff = 2

    def build(self, rng):
        per, unit_a, unit_b = rng.choice([(12, "inches", "foot"), (3, "feet", "yard"),
                                          (60, "minutes", "hour"), (16, "ounces", "pound"),
                                          (100, "centimeters", "meter")])
        n = rng.choice([4, 5, 6, 7, 8, 9, 11, 12, 15])
        val = per * n
        return {
            "stem": "There are %d %s in one %s. How many %s are in %d %ss?"
            % (per, unit_a, unit_b, unit_a, n, unit_b),
            "answer": val,
            "distractors": [
                (Fr(n, per), "dividing when the conversion calls for multiplying."),
                (per + n, "adding the conversion factor instead of applying it."),
                (Fr(per, n), "inverting the conversion."),
                (per, "reporting the conversion factor without applying it to %d." % n),
                (val * 2, "applying the conversion twice."),
            ],
            "expl": "Each %s holds %d %s, so %d %ss hold %d times %d, which is %d %s."
            % (unit_b, per, unit_a, n, unit_b, n, per, val, unit_a),
        }


GENS = [PercentOf(), PercentChange(), UnitRate(), MeanMedian(), Probability(),
        TwoWayTable(), LinearModelInterpret(), UnitConversion()]
