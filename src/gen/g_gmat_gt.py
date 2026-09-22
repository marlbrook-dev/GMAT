"""GMAT Data Insights: Graphs and Tables.

A GT item is a table plus a question that can only be answered by reading it. The
generator therefore draws the table first and computes every answer from the drawn
numbers, exactly as the rest of the framework does: nothing here asserts a key.

The distractors are the misreadings that actually happen at a table. Dividing by the
row total instead of the column total, using the later value as the base of a percent
change, ranking on the absolute increase when the question asked for the percent one,
reading the neighbouring column. Each one is named in the item, because a distractor
whose origin cannot be stated is a distractor nobody learns from.

Two rules the draws have to respect, or the item is unfair rather than hard:

  A percent answer is rounded, so every distractor has to sit far enough away that
  rounding cannot reach it. GAP below is that distance, and a draw that cannot hold
  it is dropped rather than shipped.

  Ranking questions need a strict winner. Ties are checked for and dropped.
"""
import random

from framework import Gen, ItemError, upfirst

GAP = 3          # percentage points a percent distractor must clear the key by
RATIO_GAP = 0.2  # same idea for "how many times" answers


# --- scenarios ------------------------------------------------------------------
# Each scenario names what the rows are, what the columns are, and what a cell counts.
# The wording of every question is built from these, so a new scenario adds hundreds of
# items without touching a single generator.
SCEN = [
    dict(key="stores", caption="Units sold by quarter at the five retail locations of Halstead Outfitters",
         rowlab="Store", rows=["Ashford", "Belmont", "Carlisle", "Dunmore", "Eastgate"],
         cols=["Q1", "Q2", "Q3", "Q4"], colnoun="quarter", thing="units sold", lo=140, hi=960),
    dict(key="clinics", caption="Patient visits by month at the five clinics of the Rowan Health Network",
         rowlab="Clinic", rows=["Northside", "Lakeview", "Fairmont", "Westgate", "Cedar Park"],
         cols=["April", "May", "June"], colnoun="month", thing="patient visits", lo=220, hi=1480),
    dict(key="titles", caption="Copies shipped by month for five titles published by Marlow House",
         rowlab="Title", rows=["Harbor Light", "The Quiet Season", "Field Notes", "Ten Winters", "Salt and Stone"],
         cols=["January", "February", "March", "April"], colnoun="month", thing="copies shipped", lo=90, hi=740),
    dict(key="lines", caption="Boardings by weekday on the four lines of the Kestrel Transit Authority",
         rowlab="Line", rows=["Green", "Amber", "Violet", "Slate"],
         cols=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         colnoun="weekday", thing="boardings", lo=1200, hi=8800, prep="on"),
    dict(key="plants", caption="Tonnes processed by quarter at the five plants of Arden Materials",
         rowlab="Plant", rows=["Brixton", "Calder", "Dunbar", "Elsmere", "Fenwick"],
         cols=["Q1", "Q2", "Q3", "Q4"], colnoun="quarter", thing="tonnes processed", lo=310, hi=2400),
    dict(key="regions", caption="New subscriptions by month in the four regions served by Pelham Media",
         rowlab="Region", rows=["North", "South", "East", "West"],
         cols=["July", "August", "September"], colnoun="month", thing="new subscriptions", lo=260, hi=1900),
    dict(key="courses", caption="Enrolments by term in five courses at Ellery Technical College",
         rowlab="Course", rows=["Statistics", "Metallurgy", "Accounting", "Hydrology", "Logistics"],
         cols=["Autumn", "Winter", "Spring"], colnoun="term", thing="enrolments", lo=45, hi=480),
    dict(key="farms", caption="Litres collected by week at the four dairies of the Thornbury Cooperative",
         rowlab="Dairy", rows=["Ashby", "Crompton", "Merefield", "Rushmore"],
         cols=["Week 1", "Week 2", "Week 3", "Week 4"], colnoun="week", thing="litres collected",
         lo=2600, hi=15800),
]


def prep(scen):
    return scen.get("prep", "in")


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


def word(n):
    """Small counts read as words in prose. "all 5 plants" is a data entry, not a sentence."""
    return WORDS.get(n, str(n))


def commas(n):
    return "{:,}".format(int(round(n)))


def draw(rng, scen):
    """A table of integers, rounded to a readable step for the magnitudes in play."""
    step = 10 if scen["hi"] <= 1000 else (50 if scen["hi"] <= 3000 else 100)
    data = [[rng.randrange(scen["lo"], scen["hi"], step) for _ in scen["cols"]]
            for _ in scen["rows"]]
    return data


def render(scen, data):
    head = "".join("<th>" + c + "</th>" for c in scen["cols"])
    body = "".join(
        "<tr><td>" + scen["rows"][i] + "</td>"
        + "".join("<td>" + commas(v) + "</td>" for v in row) + "</tr>"
        for i, row in enumerate(data))
    return ("<table class=\"dtable\"><thead><tr><th>" + scen["rowlab"] + "</th>"
            + head + "</tr></thead><tbody>" + body + "</tbody></table>"
            + "<p class=\"dnote\">" + scen["caption"]
            + "; every figure is a count of " + scen["thing"] + ".</p>")


def pct(x):
    return "%d%%" % int(round(x))


def spaced(key, cands, gap):
    """Drop any distractor rounding could confuse with the key, or with each other."""
    out, taken = [], [key]
    for v, why in cands:
        if v is None:
            continue
        if all(abs(v - t) >= gap for t in taken):
            out.append((v, why))
            taken.append(v)
    return out


class GTBase(Gen):
    section = "DI"
    type = "GT"
    skill = "di_gt"

    def table(self, rng):
        scen = rng.choice(SCEN)
        return scen, draw(rng, scen)

    def wrap(self, scen, data, spec):
        spec["passageHtml"] = render(scen, data)
        spec["domain"] = "math"
        spec["qskill"] = "q_rrp"
        return spec


# --- what percent of the column total ------------------------------------------
class ShareOfColumn(GTBase):
    id = "gt_share"
    sub = "Table"
    fmt = staticmethod(pct)

    def build(self, rng):
        scen, data = self.table(rng)
        ci = rng.randrange(len(scen["cols"]))
        ri = rng.randrange(len(scen["rows"]))
        col = [row[ci] for row in data]
        tot = sum(col)
        v = data[ri][ci]
        ans = 100.0 * v / tot
        rowtot = sum(data[ri])
        grand = sum(sum(r) for r in data)
        other = (ci + 1) % len(scen["cols"])
        cands = spaced(ans, [
            (100.0 * v / rowtot, "dividing by the row's own total across every "
             + scen["colnoun"] + " instead of by the column total"),
            (100.0 * v / grand, "dividing by every figure in the table rather than by the "
             + scen["cols"][ci] + " column alone"),
            (100.0 * v / (tot - v), "dividing by the rest of the column instead of by the whole of it"),
            (100.0 * v / max(col), "comparing with the largest "
             + scen["rowlab"].lower() + " rather than with the total"),
            (100.0 * data[ri][other] / sum(row[other] for row in data),
             "reading the " + scen["cols"][other] + " column by mistake"),
        ], GAP)
        if len(cands) < 4:
            raise ItemError("share draw too tight")
        return self.wrap(scen, data, dict(
            stem=upfirst(prep(scen)) + " " + scen["cols"][ci] + ", " + scen["thing"]
                 + " at " + scen["rows"][ri] + " were approximately what percent of "
                 + scen["thing"] + " at all " + word(len(scen["rows"])) + " "
                 + scen["rowlab"].lower() + "s combined?",
            answer=ans, distractors=cands, diff=rng.choice([1, 2, 2]),
            expl=scen["cols"][ci] + " totals " + " + ".join(commas(x) for x in col)
                 + " = " + commas(tot) + ". " + scen["rows"][ri] + " accounts for "
                 + commas(v) + ", and " + commas(v) + "/" + commas(tot) + " is about "
                 + pct(ans) + "."))


# --- percent change between two columns ----------------------------------------
class PercentChange(GTBase):
    id = "gt_change"
    sub = "Table"
    fmt = staticmethod(pct)

    def build(self, rng):
        scen, data = self.table(rng)
        if len(scen["cols"]) < 2:
            raise ItemError("needs two columns")
        c1, c2 = sorted(rng.sample(range(len(scen["cols"])), 2))
        ri = rng.randrange(len(scen["rows"]))
        a, b = data[ri][c1], data[ri][c2]
        if a == b:
            raise ItemError("no change to measure")
        ans = 100.0 * (b - a) / a
        if abs(ans) < 6:
            raise ItemError("change too small to survive rounding")
        rose = b > a
        cands = spaced(ans, [
            (100.0 * (b - a) / b, "using the later figure as the base of the percent change"),
            (100.0 * b / a, "reporting the later figure as a percent OF the earlier one "
             "rather than the change between them"),
            (100.0 * (b - a) / sum(data[ri]), "dividing the change by the row's total "
             "instead of by the starting figure"),
            (-ans, "reading the two " + scen["colnoun"] + "s in the wrong order"),
            (100.0 * (b - a) / sum(row[c1] for row in data),
             "dividing by the whole " + scen["cols"][c1] + " column instead of by "
             + scen["rows"][ri] + " alone"),
            (100.0 * (b - a) / min(a, b), "dividing the change by the smaller of the two "
             "figures rather than by the earlier one"),
            (100.0 * abs(b - a) / (a + b), "dividing the change by the two figures added "
             "together instead of by the starting figure"),
            (100.0 * (b - a) / max(data[ri]), "dividing by the row's best "
             + scen["colnoun"] + " rather than by " + scen["cols"][c1]),
        ], GAP)
        if not rose:
            cands = [(v, w) for v, w in cands if abs(v) < 100]
        if len(cands) < 4:
            raise ItemError("change draw too tight")
        return self.wrap(scen, data, dict(
            stem="By approximately what percent did " + scen["thing"] + " at "
                 + scen["rows"][ri] + " " + ("increase" if rose else "decrease")
                 + " from " + scen["cols"][c1] + " to " + scen["cols"][c2] + "?",
            answer=abs(ans), fmt=pct, diff=rng.choice([2, 2, 3]),
            distractors=[(abs(v), w) for v, w in cands],
            expl=scen["rows"][ri] + " went from " + commas(a) + " in " + scen["cols"][c1]
                 + " to " + commas(b) + " in " + scen["cols"][c2] + ", a change of "
                 + commas(abs(b - a)) + ". The percent change is measured against the "
                 "starting figure: " + commas(abs(b - a)) + "/" + commas(a) + " is about "
                 + pct(abs(ans)) + "."))


# --- which row leads on a derived quantity --------------------------------------
class LabelGen(GTBase):
    """Choices are the row labels themselves, so the framework's numeric distractor
    machinery does not apply. The key is still computed, a tie is still a dropped draw,
    and the label order is shuffled so position carries nothing."""

    def rank(self, scen, data):
        raise NotImplementedError

    def make(self, rng, choices_n):
        scen, data = self.table(rng)
        scores, stem, expl, trap = self.rank(rng, scen, data)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        if scores[order[0]] == scores[order[1]]:
            raise ItemError("%s drew a tie" % self.id)
        labels = list(scen["rows"])
        win = scen["rows"][order[0]]
        # Every item in a bank offers the same number of choices, because the exam does.
        # A scenario with fewer rows than the exam has options cannot carry a ranking
        # question, so the draw is dropped and another scenario comes up next time.
        if len(labels) < choices_n:
            raise ItemError("%s drew a %d row table for a %d choice exam"
                            % (self.id, len(labels), choices_n))
        if len(labels) > choices_n:
            keep = sorted(set([order[0]] + rng.sample(list(order[1:]), choices_n - 1)))
            labels = [scen["rows"][i] for i in keep]
        rng.shuffle(labels)
        if win not in labels:
            raise ItemError("%s lost its key in sampling" % self.id)
        item = {
            "id": None, "section": "DI", "type": "GT", "sub": "Table", "skill": "di_gt",
            "diff": self.diff, "stem": stem, "choices": labels,
            "answer": labels.index(win), "expl": expl, "wrong": trap,
            "gen": self.id, "passageHtml": render(scen, data),
            "domain": "math", "qskill": "q_rrp",
        }
        self.verify(item, win, len(labels), fmt=str)
        return item


class GreatestPercentGain(LabelGen):
    id = "gt_leader_pct"
    diff = 3

    def rank(self, rng, scen, data):
        if len(scen["cols"]) < 2:
            raise ItemError("needs two columns")
        c1, c2 = sorted(rng.sample(range(len(scen["cols"])), 2))
        scores = [100.0 * (r[c2] - r[c1]) / r[c1] for r in data]
        absol = [r[c2] - r[c1] for r in data]
        win = max(range(len(scores)), key=lambda i: scores[i])
        biggest = max(range(len(absol)), key=lambda i: absol[i])
        stem = ("Which " + scen["rowlab"].lower() + " had the greatest percent increase in "
                + scen["thing"] + " from " + scen["cols"][c1] + " to " + scen["cols"][c2] + "?")
        expl = ("Percent increase is the change divided by the starting figure. "
                + "; ".join(scen["rows"][i] + " " + commas(data[i][c1]) + " to "
                            + commas(data[i][c2]) + ", about " + pct(scores[i])
                            for i in range(len(data)))
                + ". " + scen["rows"][win] + " is the greatest.")
        trap = ("" if biggest == win else
                scen["rows"][biggest] + " is the trap: it added the most " + scen["thing"]
                + " in absolute terms, but from a larger base, so its percent increase is smaller.")
        return scores, stem, expl, trap


class GreatestTotal(LabelGen):
    id = "gt_leader_total"
    diff = 2

    def rank(self, rng, scen, data):
        scores = [sum(r) for r in data]
        ci = rng.randrange(len(scen["cols"]))
        lead = max(range(len(data)), key=lambda i: data[i][ci])
        win = max(range(len(scores)), key=lambda i: scores[i])
        stem = ("Which " + scen["rowlab"].lower() + " had the greatest total "
                + scen["thing"] + " across all " + word(len(scen["cols"])) + " "
                + scen["colnoun"] + "s shown?")
        expl = ("Totals: " + "; ".join(scen["rows"][i] + " " + commas(scores[i])
                                       for i in range(len(data)))
                + ". " + scen["rows"][win] + " is the greatest.")
        trap = ("" if lead == win else
                scen["rows"][lead] + " is the trap: it leads in " + scen["cols"][ci]
                + " on its own, which is not the same as leading over the whole period.")
        return scores, stem, expl, trap


# --- ratio between two rows ------------------------------------------------------
def times(x):
    return "%.1f" % x


class RowRatio(GTBase):
    id = "gt_ratio"
    sub = "Table"
    fmt = staticmethod(times)
    diff = 2

    def build(self, rng):
        scen, data = self.table(rng)
        ci = rng.randrange(len(scen["cols"]))
        ra, rb = rng.sample(range(len(scen["rows"])), 2)
        if data[ra][ci] < data[rb][ci]:
            ra, rb = rb, ra
        a, b = data[ra][ci], data[rb][ci]
        if a == b or b == 0:
            raise ItemError("ratio draw not greater than one")
        ans = float(a) / b
        if ans < 1.2:
            raise ItemError("ratio too close to one")
        cands = spaced(ans, [
            (float(b) / a, "inverting the comparison"),
            (float(a - b) / b, "computing how many times LARGER rather than how many times as many"),
            # Larger than the key. Every candidate below is smaller than it by
            # construction, the draw forces the ratio above 1.2, and the key was the
            # largest value on 86 percent of this schema's items (INC-0079).
            (float(a + b) / b, "adding the two rows and comparing the total with the "
                               "smaller of them"),
            (float(a) / sum(row[ci] for row in data) * len(scen["rows"]),
             "comparing with the column average instead of with " + scen["rows"][rb]),
            (float(sum(data[ra])) / sum(data[rb]),
             "comparing the two rows over every " + scen["colnoun"] + " instead of in "
             + scen["cols"][ci] + " alone"),
        ], RATIO_GAP)
        if len(cands) < 4:
            raise ItemError("ratio draw too tight")
        return self.wrap(scen, data, dict(
            stem="In " + scen["cols"][ci] + ", " + scen["thing"] + " at " + scen["rows"][ra]
                 + " were approximately how many times " + scen["thing"] + " at "
                 + scen["rows"][rb] + "?",
            answer=ans, distractors=cands, diff=rng.choice([2, 3]),
            expl=scen["rows"][ra] + " recorded " + commas(a) + " and " + scen["rows"][rb]
                 + " recorded " + commas(b) + " in " + scen["cols"][ci] + ". "
                 + commas(a) + "/" + commas(b) + " is about " + times(ans) + "."))


# --- how many rows clear a threshold ---------------------------------------------
class CountAbove(GTBase):
    id = "gt_count"
    sub = "Table"
    diff = 1

    def build(self, rng):
        scen, data = self.table(rng)
        ci = rng.randrange(len(scen["cols"]))
        col = [r[ci] for r in data]
        lo, hi = min(col), max(col)
        if hi - lo < 200:
            raise ItemError("column too flat for a threshold")
        thr = rng.randrange(lo + 1, hi, max(10, (hi - lo) // 8))
        ans = sum(1 for v in col if v > thr)
        if ans in (0, len(col)):
            raise ItemError("threshold excludes everything or nothing")
        avg = sum(col) / float(len(col))
        cands = [(float(len(col) - ans), "counting the " + scen["rowlab"].lower()
                  + "s that fall below the threshold instead"),
                 (float(sum(1 for v in col if v > avg)),
                  "counting the rows above the column average rather than above " + commas(thr))]
        for oi in range(len(scen["cols"])):
            if oi == ci:
                continue
            cands.append((float(sum(1 for r in data if r[oi] > thr)),
                          "reading the " + scen["cols"][oi] + " column by mistake"))
        cands += [(float(ans + 1), "an off by one count"),
                  (float(max(0, ans - 1)), "an off by one count in the other direction")]
        cands = spaced(float(ans), cands, 1)
        if len(cands) < 4:
            raise ItemError("count draw too tight")
        return self.wrap(scen, data, dict(
            stem="For how many of the " + word(len(scen["rows"])) + " "
                 + scen["rowlab"].lower() + "s did " + scen["thing"] + " in "
                 + scen["cols"][ci] + " exceed " + commas(thr) + "?",
            answer=float(ans), distractors=cands, diff=1,
            expl=scen["cols"][ci] + " figures are " + ", ".join(commas(v) for v in col)
                 + ". Those above " + commas(thr) + " are "
                 + ", ".join(commas(v) for v in col if v > thr) + ", so the count is "
                 + str(ans) + "."))


class RowAverage(GTBase):
    id = "gt_avg"
    sub = "Table"
    diff = 2
    fmt = staticmethod(commas)

    def build(self, rng):
        scen, data = self.table(rng)
        ri = rng.randrange(len(scen["rows"]))
        row = data[ri]
        n = len(row)
        tot = sum(row)
        if tot % n:
            raise ItemError("average is not a whole number")
        ans = tot // n
        srt = sorted(row)
        med = srt[n // 2] if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2.0
        ci = rng.randrange(n)
        colavg = sum(r[ci] for r in data) / float(len(data))
        cands = spaced(float(ans), [
            (float(tot), "reporting the total rather than the average"),
            (med, "taking the middle figure rather than the mean"),
            (tot / float(n - 1), "dividing by one fewer " + scen["colnoun"] + " than the table shows"),
            (colavg, "averaging down the " + scen["cols"][ci]
             + " column instead of across " + scen["rows"][ri] + "'s row"),
            (float(max(row)), "reading off the best " + scen["colnoun"] + " instead of averaging"),
            (float(min(row)), "reading off the weakest " + scen["colnoun"] + " instead of averaging"),
        ], max(2, ans // 20))
        if len(cands) < 4:
            raise ItemError("average draw too tight")
        return self.wrap(scen, data, dict(
            stem="What was the average (arithmetic mean) number of " + scen["thing"]
                 + " per " + scen["colnoun"] + " at " + scen["rows"][ri] + " over the "
                 + word(n) + " " + scen["colnoun"] + "s shown?",
            answer=float(ans), distractors=cands, diff=rng.choice([1, 2]),
            expl=scen["rows"][ri] + " recorded " + " + ".join(commas(v) for v in row)
                 + " = " + commas(tot) + " over " + word(n) + " " + scen["colnoun"]
                 + "s, and " + commas(tot) + "/" + str(n) + " = " + commas(ans) + "."))


class RowGap(GTBase):
    id = "gt_gap"
    sub = "Table"
    diff = 2
    fmt = staticmethod(commas)

    def build(self, rng):
        scen, data = self.table(rng)
        ra, rb = rng.sample(range(len(scen["rows"])), 2)
        if sum(data[ra]) < sum(data[rb]):
            ra, rb = rb, ra
        ta, tb = sum(data[ra]), sum(data[rb])
        ans = ta - tb
        if ans < 60:
            raise ItemError("gap too small to distinguish")
        ci = rng.randrange(len(scen["cols"]))
        cands = spaced(float(ans), [
            (float(ta + tb), "adding the two totals instead of subtracting them"),
            (float(data[ra][ci] - data[rb][ci]), "comparing " + scen["cols"][ci]
             + " alone rather than every " + scen["colnoun"]),
            (float(ta), "reporting " + scen["rows"][ra] + "'s own total rather than the gap"),
            (float(tb), "reporting " + scen["rows"][rb] + "'s own total rather than the gap"),
            (float(ans) / len(scen["cols"]), "reporting the gap per "
             + scen["colnoun"] + " rather than over the whole period"),
            (float(sum(sum(r) for r in data)) - ta - tb, "totalling the other "
             + scen["rowlab"].lower() + "s by mistake"),
        ], max(5, ans // 25))
        if len(cands) < 4:
            raise ItemError("gap draw too tight")
        return self.wrap(scen, data, dict(
            stem="Over the " + word(len(scen["cols"])) + " " + scen["colnoun"]
                 + "s shown, how many more " + scen["thing"] + " were recorded at "
                 + scen["rows"][ra] + " than at " + scen["rows"][rb] + "?",
            answer=float(ans), distractors=cands, diff=rng.choice([2, 3]),
            expl=scen["rows"][ra] + " totals " + commas(ta) + " and " + scen["rows"][rb]
                 + " totals " + commas(tb) + ", so the difference is " + commas(ta)
                 + " - " + commas(tb) + " = " + commas(ans) + "."))


GENS = [ShareOfColumn(), PercentChange(), GreatestPercentGain(), GreatestTotal(),
        RowRatio(), CountAbove(), RowAverage(), RowGap()]
