"""ACT Science: Interpretation of Data, Scientific Investigation, and Evaluation of
Scientific Arguments and Models.

ACT Science is a reading test about data, not a recall test about science. Nothing on it
requires knowledge beyond an introductory course; what it requires is reading a table,
working out what an experiment varied and what it held fixed, and judging whether a claim
survives the results. All three of those are decidable from the data, which is why this
category can be generated without a key ever being asserted.

Each item draws a study: an independent variable at four or five levels, a dependent
variable computed from it, and a second study that changes exactly one condition. Because
the second study is a controlled variant of the first, the same draw supports all three
reporting categories at once, and the questions stay honest:

  Interpretation of Data reads values and trends straight off the drawn table.
  Scientific Investigation asks what was varied and what was held constant, which the
  scenario records rather than implies.
  Evaluation of Scientific Arguments checks a claim against the drawn numbers, and the
  claim is judged by evaluating it, not by writing down the answer.

One scenario deliberately has a second study where the changed condition does NOT move the
result, because "the variable you changed turned out not to matter" is a real finding and
a student who assumes every manipulation must produce an effect should get that wrong.
"""
from framework import Gen, ItemError


def n1(x):
    """One decimal place, or a whole number when it is one."""
    v = round(float(x), 1)
    return str(int(v)) if v == int(v) else ("%.1f" % v)


# iv: (name, unit, levels)         dv: (name, unit)
# mod: (what Study 2 changed, Study 1 setting, Study 2 setting, multiplier applied)
# A multiplier of 1.0 means the change made no measurable difference.
SCEN = [
    dict(key="enzyme", title="reaction rate of the enzyme amylase",
         iv=("Substrate concentration", "mM"), dv=("Reaction rate", "micromol per minute"),
         levels=[2, 4, 8, 16, 32], base=6.0, step=1.8, rising=True,
         mod=("Temperature of the reaction mixture", "25 degrees C", "35 degrees C", 1.6),
         fixed=["the volume of enzyme solution added", "the pH of the buffer",
                "the total reaction time"]),
    dict(key="solubility", title="solubility of a salt in water",
         iv=("Water temperature", "degrees C"), dv=("Salt dissolved", "g per 100 g water"),
         levels=[10, 20, 40, 60, 80], base=14.0, step=0.9, rising=True,
         mod=("The salt used", "potassium nitrate", "sodium chloride", 0.55),
         fixed=["the mass of water used", "the stirring time",
                "the method of deciding that no more salt would dissolve"]),
    dict(key="pendulum", title="period of a swinging pendulum",
         iv=("String length", "cm"), dv=("Period", "seconds"),
         levels=[20, 40, 60, 80, 100], base=0.9, step=0.011, rising=True,
         mod=("Mass of the bob", "50 g", "200 g", 1.0),
         fixed=["the angle of release", "the number of swings timed",
                "the place where the timing was taken"]),
    dict(key="plants", title="growth of seedlings under lamps",
         iv=("Hours of light per day", "hours"), dv=("Height gained in 14 days", "mm"),
         levels=[4, 8, 12, 16, 20], base=11.0, step=2.4, rising=True,
         mod=("Nitrogen in the nutrient solution", "full strength", "one quarter strength", 0.6),
         fixed=["the seed variety", "the volume of solution given each day",
                "the air temperature in the growth chamber"]),
    dict(key="resistor", title="current through a circuit element",
         iv=("Applied voltage", "volts"), dv=("Current", "milliamps"),
         levels=[2, 4, 6, 8, 10], base=0.0, step=7.5, rising=True,
         mod=("Resistance in the circuit", "200 ohms", "400 ohms", 0.5),
         fixed=["the temperature of the element", "the meter used to read the current",
                "the length of the connecting wires"]),
    dict(key="evaporation", title="evaporation from an open dish",
         iv=("Air speed over the dish", "cm per second"), dv=("Water lost in 6 hours", "g"),
         levels=[0, 10, 20, 30, 40], base=2.0, step=0.14, rising=True,
         mod=("Relative humidity of the air", "30 percent", "70 percent", 0.45),
         fixed=["the surface area of the dish", "the air temperature",
                "the starting mass of water"]),
    dict(key="catalyst", title="gas produced by a decomposition reaction",
         iv=("Mass of catalyst", "mg"), dv=("Gas collected in 5 minutes", "mL"),
         levels=[10, 20, 30, 40, 50], base=4.0, step=1.3, rising=True,
         mod=("Shape of the reaction vessel", "tall and narrow", "short and wide", 1.0),
         fixed=["the concentration of the reactant", "the temperature",
                "the volume of reactant used"]),
    # A falling relationship where scaling the second study stays physical. An earlier
    # draft used a cooling block and multiplied its temperature by 1.12 for the insulated
    # run, which put Study 2 above the temperature the block started at. Insulation slows
    # cooling; it does not reheat the block.
    dict(key="lamp", title="light reaching a sensor from a lamp",
         iv=("Distance from the lamp", "cm"), dv=("Light reaching the sensor", "lux"),
         levels=[10, 20, 40, 60, 80], base=90.0, step=-0.95, rising=False,
         mod=("Power of the lamp", "60 watts", "25 watts", 0.45),
         fixed=["the sensor used", "the alignment of the sensor with the lamp",
                "the level of background light in the room"]),
]


def build_study(rng, scen):
    """Two tables of numbers, and every fact about them that a question could need."""
    jitter = rng.choice([0.85, 0.9, 1.0, 1.1, 1.2])
    s1 = [round(scen["base"] * jitter + scen["step"] * jitter * x, 1) for x in scen["levels"]]
    if any(v <= 0 for v in s1):
        raise ItemError("study 1 produced a non positive reading")
    mult = scen["mod"][3]
    s2 = [round(v * mult, 1) for v in s1]
    if any(v <= 0 for v in s2):
        raise ItemError("study 2 produced a non positive reading")
    # A trend question needs a strict direction, and a cross study question needs the two
    # studies to be tellable apart. Both are checked rather than assumed.
    up = all(b > a for a, b in zip(s1, s1[1:]))
    down = all(b < a for a, b in zip(s1, s1[1:]))
    if not (up or down):
        raise ItemError("study 1 is not monotone")
    same = all(abs(a - b) < 0.05 for a, b in zip(s1, s2))
    if not same and any(abs(a - b) < 0.05 for a, b in zip(s1, s2)):
        raise ItemError("the two studies agree at some levels but not others")
    return dict(scen=scen, s1=s1, s2=s2, up=up, same=same)


def render(st):
    scen = st["scen"]
    ivn, ivu = scen["iv"]
    dvn, dvu = scen["dv"]
    what, set1, set2, _ = scen["mod"]
    head = ("<tr><th>" + ivn + " (" + ivu + ")</th><th>Study 1: " + dvn + " (" + dvu
            + ")</th><th>Study 2: " + dvn + " (" + dvu + ")</th></tr>")
    rows = "".join("<tr><td>" + n1(x) + "</td><td>" + n1(a) + "</td><td>" + n1(b)
                   + "</td></tr>" for x, a, b in zip(scen["levels"], st["s1"], st["s2"]))
    return ("<p><b>Studies 1 and 2: " + scen["title"] + "</b></p>"
            + "<p>In Study 1, students varied the " + ivn.lower() + " and recorded the "
            + dvn.lower() + " at each setting, with " + what.lower() + " held at " + set1
            + ". Study 2 repeated Study 1 exactly, except that " + what.lower()
            + " was " + set2 + ". In both studies " + ", ".join(scen["fixed"][:-1])
            + " and " + scen["fixed"][-1] + " were kept the same.</p>"
            + "<table class=\"dtable\"><thead>" + head + "</thead><tbody>" + rows
            + "</tbody></table>")


class SciBase(Gen):
    section = "S"
    type = "S"
    diff = 2

    def study(self, rng):
        return build_study(rng, rng.choice(SCEN))

    def frame(self, st, spec):
        spec["passageHtml"] = render(st)
        return spec

    def choice_item(self, rng, st, stem, right, wrong, expl, diff, choices_n):
        """An item whose options are sentences: build the set directly and verify."""
        opts = [right] + [w for w in wrong if w != right]
        opts = opts[:choices_n]
        if len(opts) < choices_n or len(set(opts)) != choices_n:
            raise ItemError("%s could not build %d distinct options" % (self.id, choices_n))
        rng.shuffle(opts)
        item = {
            "id": None, "section": "S", "type": "S", "sub": self.sub, "skill": self.skill,
            "diff": diff, "stem": stem, "choices": opts, "answer": opts.index(right),
            "expl": expl, "wrong": "", "gen": self.id, "passageHtml": render(st),
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


# --- Interpretation of Data -------------------------------------------------------
class ReadValue(SciBase):
    id = "act_s_read"
    skill = "act_s_iod"
    sub = "Reading a value"
    fmt = staticmethod(n1)

    def build(self, rng):
        st = self.study(rng)
        scen = st["scen"]
        i = rng.randrange(len(scen["levels"]))
        which = rng.choice([1, 2])
        vals = st["s1"] if which == 1 else st["s2"]
        other = st["s2"] if which == 1 else st["s1"]
        ans = vals[i]
        cands = []
        if not st["same"]:
            cands.append((other[i], "reading the other study's column at the same setting"))
        if i + 1 < len(vals):
            cands.append((vals[i + 1], "reading one row further down the table"))
        if i > 0:
            cands.append((vals[i - 1], "reading one row further up the table"))
        cands += [(round(sum(vals) / len(vals), 1), "averaging the whole column instead of "
                   "reading the row asked about"),
                  (float(scen["levels"][i]), "reporting the setting rather than the reading"),
                  (round(vals[-1], 1), "reading the last row whatever the question asked")]
        if len(set(n1(v) for v, _ in cands if v is not None)) < 3:
            raise ItemError("not enough distinct readings")
        return self.frame(st, dict(
            stem="According to Study " + str(which) + ", when the "
                 + scen["iv"][0].lower() + " was " + n1(scen["levels"][i]) + " "
                 + scen["iv"][1] + ", the " + scen["dv"][0].lower() + " was closest to "
                 "which of the following, in " + scen["dv"][1] + "?",
            answer=ans, distractors=cands, diff=1,
            expl="In the Study " + str(which) + " column, the row for "
                 + n1(scen["levels"][i]) + " " + scen["iv"][1] + " reads " + n1(ans)
                 + " " + scen["dv"][1] + "."))


class Interpolate(SciBase):
    id = "act_s_interp"
    skill = "act_s_iod"
    sub = "Interpolating between readings"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        i = rng.randrange(len(scen["levels"]) - 1)
        lo, hi = scen["levels"][i], scen["levels"][i + 1]
        if hi - lo < 2:
            raise ItemError("no room between the settings")
        mid = (lo + hi) / 2.0
        a, b = st["s1"][i], st["s1"][i + 1]
        loY, hiY = min(a, b), max(a, b)
        right = "between " + n1(loY) + " and " + n1(hiY)
        pairs = []
        for j in range(len(st["s1"]) - 1):
            x, y = min(st["s1"][j], st["s1"][j + 1]), max(st["s1"][j], st["s1"][j + 1])
            pairs.append("between " + n1(x) + " and " + n1(y))
        wrong = [p for p in pairs if p != right]
        wrong += ["less than " + n1(min(st["s1"])), "greater than " + n1(max(st["s1"]))]
        expl = ("The " + scen["iv"][0].lower() + " of " + n1(mid) + " " + scen["iv"][1]
                + " lies between the settings of " + n1(lo) + " and " + n1(hi)
                + ", where Study 1 recorded " + n1(a) + " and " + n1(b) + ". A reading "
                "taken between two settings falls between the two values recorded at them.")
        stem = ("Suppose Study 1 had been repeated with the " + scen["iv"][0].lower()
                + " set to " + n1(mid) + " " + scen["iv"][1] + ". The "
                + scen["dv"][0].lower() + ", in " + scen["dv"][1]
                + ", would most likely have been:")
        return self.choice_item(rng, st, stem, right, wrong, expl, 2, choices_n)


class Trend(SciBase):
    id = "act_s_trend"
    skill = "act_s_iod"
    sub = "Describing a trend"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        rising = st["up"]
        right = ("increased only" if rising else "decreased only")
        wrong = ["decreased only" if rising else "increased only",
                 "increased, then decreased", "decreased, then increased",
                 "remained the same"]
        expl = ("Reading down the Study 1 column, the " + scen["dv"][0].lower()
                + " goes " + ", ".join(n1(v) for v in st["s1"])
                + ". Each reading is " + ("higher" if rising else "lower")
                + " than the one before it, with no reversal.")
        stem = ("As the " + scen["iv"][0].lower() + " increased in Study 1, the "
                + scen["dv"][0].lower() + ":")
        return self.choice_item(rng, st, stem, right, wrong, expl, 1, choices_n)


# --- Scientific Investigation ------------------------------------------------------
class WhatChanged(SciBase):
    id = "act_s_changed"
    skill = "act_s_si"
    sub = "Comparing two studies"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        right = what.lower() + " was " + set2 + " rather than " + set1
        wrong = [f + " was changed" for f in scen["fixed"]]
        wrong.append("the " + scen["dv"][0].lower() + " was set in advance rather than measured")
        expl = ("The description states that Study 2 repeated Study 1 exactly except that "
                + what.lower() + " was " + set2 + " instead of " + set1 + ". Everything else, "
                + ", ".join(scen["fixed"]) + ", was deliberately held the same, which is what "
                "makes the comparison between the two studies meaningful.")
        stem = "Study 2 differed from Study 1 in that, in Study 2:"
        return self.choice_item(rng, st, stem, right, wrong, expl, 2, choices_n)


class HeldConstant(SciBase):
    id = "act_s_constant"
    skill = "act_s_si"
    sub = "Controlling variables"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        right = rng.choice(scen["fixed"])
        wrong = [scen["iv"][0].lower(), what.lower(), scen["dv"][0].lower()]
        expl = ("The " + scen["iv"][0].lower() + " was the variable deliberately changed "
                "within each study, the " + scen["dv"][0].lower() + " was what the students "
                "measured in response, and " + what.lower() + " is precisely what Study 2 "
                "altered. Only " + right + " was held the same throughout both studies.")
        stem = "Which of the following was kept the same in both Study 1 and Study 2?"
        return self.choice_item(rng, st, stem, right, wrong, expl, 2, choices_n)


class NextStep(SciBase):
    id = "act_s_next"
    skill = "act_s_si"
    sub = "Designing a further test"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        extra = rng.choice(scen["fixed"])
        right = ("repeat Study 1 changing only " + extra + ", leaving every other condition "
                 "as it was")
        wrong = ["repeat Study 1 changing " + extra + " and the " + scen["iv"][0].lower()
                 + " at the same time",
                 "repeat Study 2 with " + what.lower() + " returned to " + set1,
                 "record the " + scen["dv"][0].lower() + " at a single setting only, with "
                 + extra + " unchanged"]
        expl = ("To find out whether " + extra + " affects the " + scen["dv"][0].lower()
                + ", that is the one thing that may differ between the new trial and Study 1. "
                "Changing it alongside the " + scen["iv"][0].lower()
                + " would leave the two effects impossible to separate; changing "
                + what.lower() + " tests something already tested; and a single setting gives "
                "nothing to compare.")
        stem = ("Suppose the students wanted to find out whether " + extra
                + " affects the " + scen["dv"][0].lower()
                + ". They would most likely design an experiment that would:")
        return self.choice_item(rng, st, stem, right, wrong, expl, 3, choices_n)


# --- Evaluation of Scientific Arguments and Models -----------------------------------
class ClaimCheck(SciBase):
    id = "act_s_claim"
    skill = "act_s_esa"
    sub = "Testing a claim against the data"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, mult = scen["mod"]
        higher = mult > 1.02
        lower = mult < 0.98
        claims = []
        if st["same"]:
            claims.append(("changing " + what.lower() + " from " + set1 + " to " + set2
                           + " would change the " + scen["dv"][0].lower(), False,
                           "the two columns record the same values at every setting, so the "
                           "change made no measurable difference"))
        elif higher:
            claims.append(("changing " + what.lower() + " to " + set2 + " would raise the "
                           + scen["dv"][0].lower(), True,
                           "every Study 2 reading is higher than the Study 1 reading at the "
                           "same setting"))
        elif lower:
            claims.append(("changing " + what.lower() + " to " + set2 + " would lower the "
                           + scen["dv"][0].lower(), True,
                           "every Study 2 reading is lower than the Study 1 reading at the "
                           "same setting"))
        if not claims:
            raise ItemError("no claim available for this draw")
        claim, holds, because = claims[0]
        yes = "Yes, because " + because
        no = "No, because " + because
        right = yes if holds else no
        # The two wrong "because" clauses are true statements that do not settle the claim,
        # which is the failure mode this question is actually about.
        other = ("the " + scen["dv"][0].lower() + " changes with the "
                 + scen["iv"][0].lower() + " in both studies")
        wrong = ["Yes, because " + other, "No, because " + other,
                 ("No, because " if holds else "Yes, because ")
                 + "the two studies used the same settings of the "
                 + scen["iv"][0].lower()]
        expl = ("Compare the two columns setting by setting: Study 1 reads "
                + ", ".join(n1(v) for v in st["s1"]) + " and Study 2 reads "
                + ", ".join(n1(v) for v in st["s2"]) + ". " + because.capitalize()
                + ", so the prediction is " + ("supported" if holds else "not supported") + ".")
        stem = ("A student predicts that, at any setting used in these studies, " + claim
                + ". Is this prediction consistent with the results?")
        return self.choice_item(rng, st, stem, right, wrong, expl, 3, choices_n)


class BestSupported(SciBase):
    id = "act_s_support"
    skill = "act_s_esa"
    sub = "Choosing the supported conclusion"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        rising = st["up"]
        iv, dv = scen["iv"][0].lower(), scen["dv"][0].lower()
        right = ("increasing the " + iv + " " + ("raises" if rising else "lowers")
                 + " the " + dv)
        wrong = ["increasing the " + iv + " " + ("lowers" if rising else "raises")
                 + " the " + dv,
                 "the " + dv + " is unaffected by the " + iv,
                 "the " + dv + " reaches its highest value at the lowest " + iv
                 if rising else
                 "the " + dv + " reaches its lowest value at the lowest " + iv]
        wrong.append("the " + iv + " is determined by the " + dv)
        expl = ("In Study 1 the " + dv + " runs " + ", ".join(n1(v) for v in st["s1"])
                + " as the " + iv + " runs " + ", ".join(n1(v) for v in scen["levels"])
                + ", and Study 2 shows the same direction. Only the conclusion that the "
                + dv + " " + ("rises" if rising else "falls")
                + " with the " + iv + " is supported by both.")
        stem = "The results of Studies 1 and 2 best support the conclusion that:"
        return self.choice_item(rng, st, stem, right, wrong, expl, 3, choices_n)


GENS = [ReadValue(), Interpolate(), Trend(), WhatChanged(), HeldConstant(), NextStep(),
        ClaimCheck(), BestSupported()]
