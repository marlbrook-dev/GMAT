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
from framework import Gen, ItemError, balance, upfirst


def n1(x):
    """One decimal place, or a whole number when it is one.

    For a SETTING, which is the value a student dialled in: 2 mM, not 2.0 mM.
    """
    v = round(float(x), 1)
    return str(int(v)) if v == int(v) else ("%.1f" % v)


def n1f(x):
    """One decimal place, always.

    For a READING, which is what the instrument returned. A measurement column with
    uniform precision is how a real data table is printed, and it is also the only way
    this data can be offered as answer choices: a reading that lands on a whole number
    rendered as "6" beside a neighbour rendered as "7.2" is visibly a different kind of
    thing, so make() would not put them in the same item and threw away one draw in five
    of the schema that reads a value out of the table (INC-0092).
    """
    return "%.1f" % round(float(x), 1)


# iv: (name, unit, levels)         dv: (name, unit)
# mod: (what Study 2 changed, Study 1 setting, Study 2 setting, multiplier applied)
# A multiplier of 1.0 means the change made no measurable difference.
SCEN = [
    dict(key="enzyme", title="reaction rate of the enzyme amylase",
         iv=("Substrate concentration", "mM"), dv=("Reaction rate", "micromol per minute"),
         num=("sing", "sing"),
         levels=[2, 4, 8, 16, 32], base=6.0, step=1.8, rising=True,
         mod=("Temperature of the reaction mixture", "25 degrees C", "35 degrees C", 1.6),
         fixed=["the volume of enzyme solution added", "the pH of the buffer",
                "the total reaction time",
                "the make of the water bath", "the tube the reaction ran in"]),
    dict(key="solubility", title="solubility of a salt in water",
         iv=("Water temperature", "degrees C"), dv=("Salt dissolved", "g per 100 g water"),
         num=("sing", "sing"),
         levels=[10, 20, 40, 60, 80], base=14.0, step=0.9, rising=True,
         mod=("The salt used", "potassium nitrate", "sodium chloride", 0.55),
         fixed=["the mass of water used", "the stirring time",
                "the method of deciding that no more salt would dissolve",
                "the purity of the salt", "the balance used for weighing"]),
    dict(key="pendulum", title="period of a swinging pendulum",
         iv=("String length", "cm"), dv=("Period", "seconds"),
         num=("sing", "sing"),
         levels=[20, 40, 60, 80, 100], base=0.9, step=0.011, rising=True,
         mod=("Mass of the bob", "50 g", "200 g", 1.0),
         fixed=["the angle of release", "the number of swings timed",
                "the place where the timing was taken",
                "the stopwatch used", "the way the string was clamped"]),
    dict(key="plants", title="growth of seedlings under lamps",
         iv=("Light per day", "hours"), dv=("Height gained in 14 days", "mm"),
         num=("sing", "sing"),
         levels=[4, 8, 12, 16, 20], base=11.0, step=2.4, rising=True,
         mod=("Nitrogen in the nutrient solution", "full strength", "one quarter strength", 0.6),
         fixed=["the seed variety", "the volume of solution given each day",
                "the air temperature in the growth chamber",
                "the size of the pots", "the person who measured the seedlings"]),
    dict(key="resistor", title="current through a circuit element",
         iv=("Applied voltage", "volts"), dv=("Current", "milliamps"),
         num=("sing", "sing"),
         levels=[2, 4, 6, 8, 10], base=0.0, step=7.5, rising=True,
         mod=("Resistance in the circuit", "200 ohms", "400 ohms", 0.5),
         fixed=["the temperature of the element", "the meter used to read the current",
                "the length of the connecting wires",
                "the supply used to set the voltage", "the way the element was mounted"]),
    dict(key="evaporation", title="evaporation from an open dish",
         iv=("Air speed over the dish", "cm per second"), dv=("Water lost in 6 hours", "g"),
         num=("sing", "sing"),
         levels=[0, 10, 20, 30, 40], base=2.0, step=0.14, rising=True,
         mod=("Relative humidity of the air", "30 percent", "70 percent", 0.45),
         fixed=["the surface area of the dish", "the air temperature",
                "the starting mass of water",
                "the shape of the dish", "the balance used for weighing"]),
    dict(key="yeast", title="carbon dioxide produced by fermenting yeast",
         iv=("Sugar concentration", "g per litre"), dv=("Gas produced in 20 minutes", "mL"),
         num=("sing", "sing"),
         levels=[5, 10, 20, 40, 60], base=8.0, step=0.7, rising=True,
         mod=("Temperature of the flask", "20 degrees C", "30 degrees C", 1.5),
         fixed=["the mass of yeast added", "the volume of liquid in the flask",
                "the method of collecting the gas", "the type of sugar used",
                "the time for which gas was collected"]),
    dict(key="spring", title="extension of a steel spring under load",
         iv=("Load applied", "newtons"), dv=("Extension", "mm"),
         num=("sing", "sing"),
         levels=[2, 4, 6, 8, 10], base=0.0, step=3.1, rising=True,
         mod=("Thickness of the spring wire", "1.0 mm", "1.4 mm", 0.55),
         fixed=["the material of the spring", "the way the load was hung",
                "the ruler used to measure extension", "the temperature of the room",
                "the point from which extension was measured"]),
    dict(key="rust", title="mass of rust forming on iron nails",
         iv=("Time in the humid chamber", "days"), dv=("Mass of rust formed", "mg"),
         num=("sing", "sing"),
         levels=[2, 4, 6, 8, 10], base=1.0, step=2.7, rising=True,
         mod=("Coating on the nails", "bare iron", "painted", 0.3),
         fixed=["the size of the nails", "the humidity in the chamber",
                "the air temperature", "the balance used for weighing",
                "the way rust was separated before weighing"]),
    dict(key="filter", title="clarity of water after filtering",
         iv=("Depth of sand in the filter", "cm"), dv=("Particle count remaining", "per mL"),
         num=("sing", "sing"),
         levels=[5, 10, 15, 20, 25], base=520.0, step=-16.0, rising=False,
         mod=("Grain size of the sand", "coarse", "fine", 0.6),
         fixed=["the volume of water poured through", "the starting particle count",
                "the rate at which water was poured", "the diameter of the filter column",
                "the counting method used"]),
    dict(key="insulation", title="heat lost through a wall panel",
         iv=("Thickness of insulation", "mm"), dv=("Heat lost per hour", "watts"),
         num=("sing", "sing"),
         levels=[10, 20, 30, 40, 50], base=88.0, step=-1.3, rising=False,
         mod=("Material of the insulation", "mineral wool", "rigid foam", 0.72),
         fixed=["the area of the panel", "the temperature on each side of the panel",
                "the sensor used", "the length of each test",
                "the way the panel was sealed at its edges"]),
    dict(key="seedbed", title="germination of seeds at different depths",
         iv=("Sowing depth", "mm"), dv=("Germination rate", "percent"),
         num=("sing", "sing"),
         # A rate rather than a count of seeds, because a reading carries one decimal
         # place and two tenths of a seed does not germinate. The ceiling is the one
         # this quantity has by its own definition, and the base leaves headroom under
         # it at every jitter rather than relying on the check to catch the top one.
         levels=[5, 10, 20, 30, 40], base=88.0, step=-1.7, rising=False, cap=100,
         mod=("Soil type in the tray", "loam", "heavy clay", 0.8),
         fixed=["the seed variety", "the water given to each tray",
                "the temperature of the greenhouse", "the number of seeds sown per tray",
                "the number of days before counting"]),
    dict(key="sound", title="sound level measured from a speaker",
         iv=("Distance from the speaker", "m"), dv=("Sound level", "decibels"),
         num=("sing", "sing"),
         levels=[1, 2, 4, 8, 16], base=86.0, step=-1.1, rising=False,
         mod=("Surface behind the meter", "bare wall", "heavy curtain", 0.94),
         fixed=["the volume setting on the speaker", "the meter used",
                "the height of the meter above the floor", "the tone played",
                "the background noise in the room"]),
    dict(key="battery", title="running time of a torch on one cell",
         iv=("Cell capacity", "mAh"), dv=("Running time", "minutes"),
         num=("sing", "sing"),
         levels=[500, 1000, 1500, 2000, 2500], base=4.0, step=0.11, rising=True,
         mod=("Bulb fitted to the torch", "filament bulb", "light emitting diode", 2.2),
         fixed=["the make of the torch", "the starting condition of each cell",
                "the temperature of the room", "the way running time was judged to end",
                "the switch position used"]),
    dict(key="dye", title="uptake of dye by fabric squares",
         iv=("Time in the dye bath", "minutes"), dv=("Dye taken up", "mg per gram"),
         num=("sing", "sing"),
         levels=[5, 10, 20, 30, 45], base=3.0, step=0.42, rising=True,
         mod=("Fibre of the fabric", "cotton", "polyester", 0.4),
         fixed=["the concentration of the dye bath", "the temperature of the bath",
                "the mass of each fabric square", "the rinsing procedure",
                "the drying time before weighing"]),
    dict(key="concrete", title="strength of concrete cubes as they cure",
         iv=("Curing time", "days"), dv=("Crushing strength", "MPa"),
         num=("sing", "sing"),
         levels=[3, 7, 14, 21, 28], base=9.0, step=0.7, rising=True,
         mod=("Water added to the mix", "the standard amount", "one fifth more", 0.78),
         fixed=["the cement used", "the size of the cube moulds",
                "the temperature of the curing room", "the compaction method",
                "the press used for crushing"]),
    dict(key="algae", title="growth of algae in lit tanks",
         iv=("Nutrient added", "mg per litre"), dv=("Algae mass after 10 days", "mg dry mass"),
         num=("sing", "sing"),
         levels=[1, 2, 4, 8, 16], base=6.0, step=1.9, rising=True,
         mod=("Colour of the light", "white", "green", 0.65),
         fixed=["the volume of water in each tank", "the hours of light per day",
                "the starting quantity of algae", "the water temperature",
                "the way dry mass was measured"]),
    dict(key="friction", title="force needed to start a block sliding",
         iv=("Mass on the block", "g"), dv=("Force at the moment of sliding", "N"),
         num=("sing", "sing"),
         levels=[100, 200, 300, 400, 500], base=0.0, step=0.006, rising=True,
         mod=("Surface under the block", "varnished wood", "glass", 0.5),
         fixed=["the block used", "the way the force was applied",
                "the force meter used", "the cleanliness of the surface",
                "the temperature of the room"]),
    dict(key="catalyst", title="gas produced by a decomposition reaction",
         iv=("Mass of catalyst", "mg"), dv=("Gas collected in 5 minutes", "mL"),
         num=("sing", "sing"),
         levels=[10, 20, 30, 40, 50], base=4.0, step=1.3, rising=True,
         mod=("Shape of the reaction vessel", "tall and narrow", "short and wide", 1.0),
         fixed=["the concentration of the reactant", "the temperature",
                "the volume of reactant used",
                "the purity of the catalyst", "the way the gas was collected"]),
    # A falling relationship where scaling the second study stays physical. An earlier
    # draft used a cooling block and multiplied its temperature by 1.12 for the insulated
    # run, which put Study 2 above the temperature the block started at. Insulation slows
    # cooling; it does not reheat the block.
    dict(key="lamp", title="light reaching a sensor from a lamp",
         iv=("Distance from the lamp", "cm"), dv=("Light reaching the sensor", "lux"),
         num=("sing", "sing"),
         levels=[10, 20, 40, 60, 80], base=90.0, step=-0.95, rising=False,
         mod=("Power of the lamp", "60 watts", "25 watts", 0.45),
         fixed=["the sensor used", "the alignment of the sensor with the lamp",
                "the level of background light in the room",
                "the height of the lamp above the bench", "the warm up time before reading"]),
    # Ten scenarios whose reading falls as the setting rises. The corpus had fifteen
    # rising against five falling, so the answer to "as the setting increased, the reading"
    # was the rising option on 76 percent of the items the trend schema produced, and a
    # student who always picked it scored 76 without reading a table (INC-0081). The
    # direction is a property of the science, so it is fixed in the science rather than
    # by flipping a table the scenario does not support.
    dict(key="shielding", title="count rate through lead shielding",
         iv=("Thickness of the shielding", "mm"), dv=("Count rate", "counts per minute"),
         num=("sing", "sing"),
         levels=[1, 2, 4, 6, 8], base=90.0, step=-8.0, rising=False,
         mod=("The source used", "the stronger source", "the weaker source", 0.6),
         fixed=["the distance from source to detector", "the counting time",
                "the detector used", "the background count subtracted",
                "the alignment of the source with the detector"]),
    dict(key="ramp", title="time for a trolley to run down a ramp",
         iv=("Angle of the ramp", "degrees"), dv=("Time to reach the bottom", "s"),
         num=("sing", "sing"),
         levels=[5, 10, 15, 20, 25], base=4.6, step=-0.12, rising=False,
         mod=("Surface of the ramp", "a bare board", "a board with a cloth cover", 1.35),
         fixed=["the mass of the trolley", "the length of the ramp",
                "the point on the ramp the trolley started from",
                "the timing method", "the wheels fitted to the trolley"]),
    dict(key="wire", title="resistance of a wire of varying diameter",
         iv=("Diameter of the wire", "tenths of a mm"), dv=("Resistance", "ohms"),
         num=("sing", "sing"),
         levels=[2, 4, 6, 8, 10], base=9.5, step=-0.75, rising=False,
         mod=("Length of the wire", "1 metre", "2 metres", 1.9),
         fixed=["the metal the wire is made of", "the temperature of the wire",
                "the meter used", "the current passed through the wire",
                "the contacts the wire was held in"]),
    dict(key="layers", title="light passing through layers of filter paper",
         iv=("Number of layers", "layers"), dv=("Light reaching the sensor", "lux"),
         num=("sing", "sing"),
         levels=[1, 2, 3, 4, 5], base=520.0, step=-90.0, rising=False,
         mod=("The lamp used", "a 60 watt lamp", "a 40 watt lamp", 0.7),
         fixed=["the distance from lamp to sensor", "the make of filter paper",
                "the sensor used", "the level of background light",
                "the warm up time before reading"]),
    dict(key="oxygen", title="oxygen dissolved at depth in a lake",
         iv=("Depth below the surface", "m"), dv=("Oxygen dissolved", "mg per litre"),
         num=("sing", "sing"),
         levels=[1, 3, 5, 7, 9], base=11.0, step=-0.85, rising=False,
         mod=("Time of year sampled", "March", "August", 0.72),
         fixed=["the point on the lake sampled", "the time of day",
                "the sampling bottle used", "the method of measurement",
                "the depth gauge used"]),
    dict(key="signal", title="signal strength away from a transmitter",
         iv=("Distance from the transmitter", "km"), dv=("Signal strength", "dB"),
         num=("sing", "sing"),
         levels=[2, 4, 6, 8, 10], base=68.0, step=-5.2, rising=False,
         mod=("Height of the receiving aerial", "2 metres", "8 metres", 1.3),
         fixed=["the transmitter power", "the frequency used",
                "the receiver used", "the weather on the day",
                "the orientation of the aerial"]),
    dict(key="inhibitor", title="reaction rate with an inhibitor added",
         iv=("Concentration of the inhibitor", "mM"),
         dv=("Reaction rate", "micromol per minute"),
         num=("sing", "sing"),
         levels=[1, 2, 3, 4, 5], base=9.0, step=-1.4, rising=False,
         mod=("Temperature of the mixture", "20 degrees C", "30 degrees C", 1.45),
         fixed=["the volume of enzyme solution", "the substrate concentration",
                "the pH of the buffer", "the total reaction time",
                "the tube the reaction ran in"]),
    dict(key="battery", title="charge held by batteries of different ages",
         iv=("Age of the battery", "months"), dv=("Charge held after a day", "percent"),
         num=("sing", "sing"),
         levels=[3, 6, 9, 12, 15], base=97.0, step=-4.6, rising=False,
         mod=("Storage temperature", "5 degrees C", "25 degrees C", 0.85),
         fixed=["the make of battery", "the charger used",
                "the load drawn during the day", "the meter used",
                "the time allowed on charge"]),
    dict(key="heater", title="plate temperature away from a heater",
         iv=("Distance from the heater", "cm"),
         dv=("Temperature of the plate", "degrees C"),
         num=("sing", "sing"),
         levels=[10, 20, 30, 40, 50], base=62.0, step=-0.95, rising=False,
         mod=("Power of the heater", "500 watts", "300 watts", 0.72),
         fixed=["the material of the plate", "the room temperature",
                "the time allowed before reading", "the thermometer used",
                "the surface finish of the plate"]),
    dict(key="marble", title="time for marble chips to dissolve in acid",
         iv=("Concentration of the acid", "M"),
         dv=("Time for the chips to dissolve", "s"),
         num=("sing", "sing"),
         levels=[1, 2, 3, 4, 5], base=210.0, step=-33.0, rising=False,
         mod=("Size of the chips", "large chips", "small chips", 0.6),
         fixed=["the mass of marble used", "the volume of acid",
                "the temperature of the acid", "the stirring",
                "the point at which the reaction was called complete"]),
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
    # Some quantities have a ceiling in their own definition: a rate out of a hundred
    # cannot read 100.2, which the germination study did on a fifth of its draws because
    # nothing here knew the number meant anything (INC-0094). Positive was checked
    # because a negative reading looks wrong at a glance; this did not, and a question
    # about the trend was still answerable on top of it.
    top = scen.get("cap")
    if top is not None and any(v > top for v in s1 + s2):
        raise ItemError("a reading passed the %s ceiling of %s" % (scen["key"], top))
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
    rows = "".join("<tr><td>" + n1(x) + "</td><td>" + n1f(a) + "</td><td>" + n1f(b)
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
    canon_ignores_source = False

    def study(self, rng):
        return build_study(rng, rng.choice(SCEN))

    def frame(self, st, spec):
        spec["passageHtml"] = render(st)
        return spec

    def choice_item(self, rng, st, stem, right, wrong, expl, diff, choices_n,
                    require=()):
        """An item whose options are sentences: build the set directly and verify.

        Where a schema offers more wrong answers than the exam has slots, the subset is
        drawn to straddle the key's length. A correct answer on a design or argument
        question naturally carries a condition and so runs long, which left the key the
        longest option on more than half of these items until this was measured.
        """
        # A required option is the one the item exists to distinguish the key from, and it
        # goes in before anything is balanced. On the trend schema that is the opposite
        # direction, which is the same length as the key, so its presence is also what
        # stops the key being uniquely the shortest option (INC-0079).
        req = [w for w in require if w != right]
        pool = [w for w in wrong if w != right and w not in req]
        need = choices_n - 1 - len(req)
        if len(pool) > need:
            picked = balance(rng, right, [(w, "") for w in pool], need)
            opts = [right] + req + [w for w, _ in picked]
        else:
            opts = [right] + req + pool[:need]
        if len(opts) < choices_n or len(set(opts)) != choices_n:
            raise ItemError("%s could not build %d distinct options" % (self.id, choices_n))
        rng.shuffle(opts)
        item = {
            "id": None, "section": "S", "type": "S", "sub": self.sub, "skill": self.skill,
            "diff": diff, "stem": stem, "choices": opts, "answer": opts.index(right),
            "expl": expl, "wrong": "", "gen": self.id, "passageHtml": render(st),
            # Design and argument questions are answered from the description, not from the
            # figures, so redrawing the figures does not make a new question.
            "canon_ignores_source": self.canon_ignores_source,
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


# --- Interpretation of Data -------------------------------------------------------
class ReadValue(SciBase):
    id = "act_s_read"
    skill = "act_s_iod"
    sub = "Reading a value"
    fmt = staticmethod(n1f)

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
        if len(set(n1f(v) for v, _ in cands if v is not None)) < 3:
            raise ItemError("not enough distinct readings")
        return self.frame(st, dict(
            stem="According to Study " + str(which) + ", when the "
                 + scen["iv"][0].lower() + " was " + n1(scen["levels"][i]) + " "
                 + scen["iv"][1] + ", the " + scen["dv"][0].lower() + " was closest to "
                 "which of the following, in " + scen["dv"][1] + "?",
            answer=ans, distractors=cands, diff=1,
            expl="In the Study " + str(which) + " column, the row for "
                 + n1(scen["levels"][i]) + " " + scen["iv"][1] + " reads " + n1f(ans)
                 + " " + scen["dv"][1] + "."))


class Interpolate(SciBase):
    id = "act_s_interp"
    skill = "act_s_iod"
    sub = "Interpolating between readings"

    # Two of the options here name a bound rather than an interval, and while every
    # question asked about a setting BETWEEN two of the table's own, neither of them
    # could ever be the answer. A student who noticed that was choosing from three
    # options rather than four, and because the two are also the shortest, the key was
    # the longest option on half the schema. So a share of the questions now ask about a
    # setting past the end of the table, where naming a bound IS the answer, which is
    # extrapolation and a thing the exam asks for in its own right.
    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        lv, s1 = scen["levels"], st["s1"]
        rising = s1[-1] > s1[0]
        below = "less than " + n1f(min(s1))
        above = "greater than " + n1f(max(s1))
        pairs = []
        for j in range(len(s1) - 1):
            x, y = min(s1[j], s1[j + 1]), max(s1[j], s1[j + 1])
            pairs.append("between " + n1f(x) + " and " + n1f(y))
        where = rng.choice(["between", "between", "under", "over"])
        if where == "between":
            i = rng.randrange(len(lv) - 1)
            lo, hi = lv[i], lv[i + 1]
            if hi - lo < 2:
                raise ItemError("no room between the settings")
            mid = (lo + hi) / 2.0
            a, b = s1[i], s1[i + 1]
            right = "between " + n1f(min(a, b)) + " and " + n1f(max(a, b))
            # "A setting of" rather than the variable's own name, because several of
            # these names are plural (minutes in the dye bath, days of curing) and a
            # singular verb after one of them is not English.
            expl = ("A setting of " + n1(mid) + " " + scen["iv"][1]
                    + " lies between the settings of " + n1(lo) + " and " + n1(hi)
                    + ", where Study 1 recorded " + n1f(a) + " and " + n1f(b) + ". A reading "
                    "taken between two settings falls between the two values recorded at them.")
            diff = 2
        else:
            end = 0 if where == "under" else -1
            step = (lv[1] - lv[0]) if where == "under" else (lv[-1] - lv[-2])
            mid = (lv[0] - step / 2.0) if where == "under" else (lv[-1] + step / 2.0)
            if mid <= 0:
                raise ItemError("no room past the end of the table")
            # Past the low end a rising series keeps falling, and a falling one keeps
            # rising, so which bound is the answer depends on the trend and not on
            # which end of the table the question is about.
            goes_down = rising if where == "under" else not rising
            right = below if goes_down else above
            expl = ("A setting of " + n1(mid) + " " + scen["iv"][1]
                    + " lies " + ("below the lowest" if where == "under" else "above the highest")
                    + " setting Study 1 used, " + n1(lv[end]) + " " + scen["iv"][1]
                    + ", where it recorded " + n1f(s1[end]) + ". Study 1's readings "
                    + ("rise" if rising else "fall")
                    + " as the setting rises, so past the end of the table the reading "
                    "continues " + ("down" if goes_down else "up")
                    + " and leaves the range the table records.")
            diff = 3
        wrong = [p for p in pairs if p != right]
        wrong += [b for b in (below, above) if b != right]
        stem = ("Suppose Study 1 had been repeated with the " + scen["iv"][0].lower()
                + " set to " + n1(mid) + " " + scen["iv"][1] + ". The "
                + scen["dv"][0].lower() + ", in " + scen["dv"][1]
                + ", would most likely have been:")
        return self.choice_item(rng, st, stem, right, wrong, expl, diff, choices_n)


class Trend(SciBase):
    id = "act_s_trend"
    skill = "act_s_iod"
    sub = "Describing a trend"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        rising = st["up"]
        right = ("increased at every setting" if rising
                 else "decreased at every setting")
        mirror = "decreased at every setting" if rising else "increased at every setting"
        wrong = [mirror, "increased then decreased", "decreased then increased",
                 "stayed the same throughout", "changed by the same amount each time",
                 "rose and fell without a clear direction"]
        expl = ("Reading down the Study 1 column, the " + scen["dv"][0].lower()
                + " goes " + ", ".join(n1(v) for v in st["s1"])
                + ". Each reading is " + ("higher" if rising else "lower")
                + " than the one before it, with no reversal and no reading equal to "
                "the one before it.")
        stem = ("As the " + scen["iv"][0].lower() + " increased in Study 1, the "
                + scen["dv"][0].lower() + ":")
        return self.choice_item(rng, st, stem, right, wrong, expl, 1, choices_n,
                                require=[mirror])


# --- Scientific Investigation ------------------------------------------------------
class WhatChanged(SciBase):
    id = "act_s_changed"
    canon_ignores_source = True
    skill = "act_s_si"
    sub = "Comparing two studies"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        right = what.lower() + " was " + set2 + " rather than " + set1
        # Every wrong answer used to be the one long template, so the key was the shortest
        # option on 97 percent of this schema's items (INC-0079). Two changes. The
        # reversal is the error a student actually makes and is the same length as the
        # key, so it can no longer stand alone at the bottom. And the remaining wrongs
        # alternate between a short form and a long one, which is what lets balance place
        # the key rather than having only one side of it to draw from. Three forms and not
        # two, because with two the shortest of them was still longer than the key.
        wrong = [what.lower() + " was " + set1 + " rather than " + set2]
        forms = [" was changed",
                 " was changed rather than held the same",
                 " was changed while everything else stayed as it was in Study 1"]
        for j, f in enumerate(scen["fixed"]):
            wrong.append(f + forms[j % 3])
        wrong.append("the " + scen["dv"][0].lower() + " was set in advance rather than "
                     "measured in response to the setting")
        expl = ("The description states that Study 2 repeated Study 1 exactly except that "
                + what.lower() + " was " + set2 + " instead of " + set1 + ", and not the "
                "other way about. Everything else, "
                + ", ".join(scen["fixed"]) + ", was deliberately held the same, which is what "
                "makes the comparison between the two studies meaningful.")
        stem = "Study 2 differed from Study 1 in that, in Study 2:"
        return self.choice_item(rng, st, stem, right, wrong, expl, 2, choices_n)


class HeldConstant(SciBase):
    id = "act_s_constant"
    canon_ignores_source = True
    skill = "act_s_si"
    sub = "Controlling variables"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        right = rng.choice(scen["fixed"])
        wrong = [scen["iv"][0].lower(), what.lower(), scen["dv"][0].lower()]
        wrong += [w for w in scen["fixed"] if w != right][:2]
        expl = ("The " + scen["iv"][0].lower() + " was the variable deliberately changed "
                "within each study, the " + scen["dv"][0].lower() + " was what the students "
                "measured in response, and " + what.lower() + " is precisely what Study 2 "
                "altered. Only " + right + " was held the same throughout both studies.")
        stem = "Which of the following was kept the same in both Study 1 and Study 2?"
        return self.choice_item(rng, st, stem, right, wrong, expl, 2, choices_n)


class NextStep(SciBase):
    id = "act_s_next"
    canon_ignores_source = True
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
                 + extra + " unchanged",
                 "repeat Study 1 unchanged and compare the new readings with the old ones",
                 "change " + extra + " partway through a single run and note when the "
                 + scen["dv"][0].lower() + " moves"]
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
    canon_ignores_source = True
    skill = "act_s_esa"
    sub = "Testing a claim against the data"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, mult = scen["mod"]
        higher = mult > 1.02
        lower = mult < 0.98
        # Each study supports a claim that holds and the mirror claim that does not, and
        # the draw takes one of the two. Without the mirror there were three possible
        # correct answers in the whole schema and two of them opened with Yes, so a
        # student answering Yes was right on 70 percent of items without reading the
        # table (INC-0088 surfaced it; the schema was under the size anything was
        # measured at). The reason clause is the same either way, because what the data
        # show does not depend on what was predicted about them: only the verdict moves.
        claims = []
        if st["same"]:
            same_why = ("the two columns record the same values at every setting, so the "
                        "change made no measurable difference")
            claims.append(("changing " + what.lower() + " from " + set1 + " to " + set2
                           + " would change the " + scen["dv"][0].lower(), False, same_why))
            claims.append(("changing " + what.lower() + " from " + set1 + " to " + set2
                           + " would leave the " + scen["dv"][0].lower()
                           + " unchanged", True, same_why))
        elif higher:
            up_why = ("every Study 2 reading is higher than the Study 1 reading at the "
                      "same setting")
            claims.append(("changing " + what.lower() + " to " + set2 + " would raise the "
                           + scen["dv"][0].lower(), True, up_why))
            claims.append(("changing " + what.lower() + " to " + set2 + " would lower the "
                           + scen["dv"][0].lower(), False, up_why))
        elif lower:
            dn_why = ("every Study 2 reading is lower than the Study 1 reading at the "
                      "same setting")
            claims.append(("changing " + what.lower() + " to " + set2 + " would lower the "
                           + scen["dv"][0].lower(), True, dn_why))
            claims.append(("changing " + what.lower() + " to " + set2 + " would raise the "
                           + scen["dv"][0].lower(), False, dn_why))
        if not claims:
            raise ItemError("no claim available for this draw")
        claim, holds, because = rng.choice(claims)
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
                + ", ".join(n1(v) for v in st["s2"]) + ". " + upfirst(because)
                + ", so the prediction is " + ("supported" if holds else "not supported") + ".")
        stem = ("A student predicts that, at any setting used in these studies, " + claim
                + ". Is this prediction consistent with the results?")
        return self.choice_item(rng, st, stem, right, wrong, expl, 3, choices_n)


class BestSupported(SciBase):
    id = "act_s_support"
    canon_ignores_source = True
    skill = "act_s_esa"
    sub = "Choosing the supported conclusion"

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        rising = st["up"]
        iv, dv = scen["iv"][0].lower(), scen["dv"][0].lower()
        right = ("increasing the " + iv + " " + ("raises" if rising else "lowers")
                 + " the " + dv)
        mirror = ("increasing the " + iv + " " + ("lowers" if rising else "raises")
                  + " the " + dv)
        wrong = [mirror,
                 "the " + dv + " is unaffected by the " + iv,
                 "the " + dv + " reaches its highest value at the lowest " + iv
                 if rising else
                 "the " + dv + " reaches its lowest value at the lowest " + iv]
        wrong.append("the " + iv + " is determined by the " + dv)
        wrong.append("increasing the " + iv + " " + ("raises" if rising else "lowers")
                     + " the " + dv + " in Study 1 but has the opposite effect in Study 2")
        wrong.append("the " + dv + " depends on the " + iv
                     + " only above the lowest setting that was tested")
        expl = ("In Study 1 the " + dv + " runs " + ", ".join(n1(v) for v in st["s1"])
                + " as the " + iv + " runs " + ", ".join(n1(v) for v in scen["levels"])
                + ", and Study 2 shows the same direction. Only the conclusion that the "
                + dv + " " + ("rises" if rising else "falls")
                + " with the " + iv + " is supported by both.")
        stem = "The results of Studies 1 and 2 best support the conclusion that:"
        return self.choice_item(rng, st, stem, right, wrong, expl, 3, choices_n,
                                require=[mirror])


class WhyTwoStudies(SciBase):
    id = "act_s_why2"
    skill = "act_s_si"
    sub = "Purpose of a second study"
    canon_ignores_source = True
    diff = 2

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        right = ("find out whether " + what.lower() + " affects the " + scen["dv"][0].lower())
        wrong = ["confirm the Study 1 readings by repeating the whole of Study 1 with "
                 "nothing altered",
                 "test a wider range of " + scen["iv"][0].lower() + " than Study 1 covered",
                 "measure a quantity that Study 1 did not record at all",
                 "check that the " + scen["dv"][0].lower() + " can be measured reliably "
                 "before the real experiment begins",
                 "establish how much the " + scen["dv"][0].lower() + " varies between "
                 "repeats at a single setting"]
        expl = ("Study 2 repeated Study 1 with one thing altered: " + what.lower()
                + " went from " + set1 + " to " + set2 + ". Changing exactly one condition "
                "and holding the rest is how an experiment isolates that condition's effect, "
                "so that is what the second study was for. It was not a plain repeat, it used "
                "the same settings of the " + scen["iv"][0].lower() + ", and it recorded the "
                "same quantity.")
        stem = "Study 2 was most likely carried out in order to:"
        return self.choice_item(rng, st, stem, right, wrong, expl, 2, choices_n)


class IdentifyVariable(SciBase):
    id = "act_s_variable"
    skill = "act_s_si"
    sub = "Identifying the variables"
    canon_ignores_source = True
    diff = 1

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        right = scen["iv"][0].lower()
        wrong = [scen["dv"][0].lower(), what.lower(), rng.choice(scen["fixed"])]
        expl = ("Within each study the students chose the " + scen["iv"][0].lower()
                + " and set it to each of " + str(len(scen["levels"]))
                + " values, which makes it the variable being manipulated. The "
                + scen["dv"][0].lower() + " is what was measured in response, " + what.lower()
                + " is what distinguishes the two studies from each other, and "
                + wrong[2] + " was held the same throughout.")
        stem = "Within each study, which of the following was the variable deliberately changed?"
        return self.choice_item(rng, st, stem, right, wrong, expl, 1, choices_n)


class AttributeDifference(SciBase):
    """Whether a difference between the studies can be put down to the changed condition.

    Data dependent, unlike the other Scientific Investigation schemas here, because the
    stem quotes the two readings being compared. Two draws with different figures really
    are different questions, so this one keeps the source in its dedup key.
    """
    id = "act_s_attribute"
    skill = "act_s_si"
    sub = "Controlling variables"
    diff = 3

    def make(self, rng, choices_n):
        st = self.study(rng)
        if st["same"]:
            raise ItemError("no difference to attribute")
        scen = st["scen"]
        what, set1, set2, _ = scen["mod"]
        i = rng.randrange(len(scen["levels"]))
        a, b = st["s1"][i], st["s2"][i]
        right = ("every condition other than " + what.lower()
                 + " was the same in the two studies")
        wrong = ["the two studies were carried out by the same students using the same "
                 "apparatus throughout",
                 "the " + scen["dv"][0].lower() + " was measured more than once at each "
                 "setting and the readings averaged",
                 "the " + scen["iv"][0].lower() + " was set to the same "
                 + str(len(scen["levels"])) + " values in both studies",
                 "the readings in Study 2 were taken after those in Study 1 rather than "
                 "before them",
                 "the difference between the two readings is larger than the smallest "
                 "difference the instrument can detect",
                 "the two studies were run in the same week",
                 "every condition other than " + what.lower() + " was the same in the two "
                 "studies and the readings were taken by the same person working to the "
                 "same written procedure"]
        expl = ("At a " + scen["iv"][0].lower() + " of " + n1(scen["levels"][i]) + " "
                + scen["iv"][1] + ", Study 1 recorded " + n1(a) + " and Study 2 recorded "
                + n1(b) + ". A difference can be put down to " + what.lower()
                + " only if nothing else differed; if some other condition had changed too, "
                "the two effects could not be separated. Using the same settings and the same "
                "students matters for other reasons but would not rescue the comparison.")
        stem = ("At a " + scen["iv"][0].lower() + " of " + n1(scen["levels"][i]) + " "
                + scen["iv"][1] + ", the " + scen["dv"][0].lower() + " was " + n1(a)
                + " " + scen["dv"][1] + " in Study 1 and " + n1(b) + " " + scen["dv"][1]
                + " in Study 2. This difference can properly be attributed to " + what.lower()
                + " only if:")
        return self.choice_item(rng, st, stem, right, wrong, expl, 3, choices_n)


class ClaimAtSetting(SciBase):
    """A numeric prediction checked against the table.

    Data dependent by design: the threshold in the claim is drawn near the real reading, so
    the question cannot be answered from the description alone and every draw is a genuinely
    different question.
    """
    id = "act_s_threshold"
    skill = "act_s_esa"
    sub = "Testing a claim against the data"
    diff = 3

    def make(self, rng, choices_n):
        st = self.study(rng)
        scen = st["scen"]
        which = rng.choice([1, 2])
        vals = st["s1"] if which == 1 else st["s2"]
        i = rng.randrange(len(scen["levels"]))
        actual = vals[i]
        gap = max(0.4, round(abs(actual) * rng.choice([0.12, 0.18, 0.25]), 1))
        over = rng.choice([True, False])
        thresh = round(actual + (gap if over else -gap), 1)
        holds = actual >= thresh
        right = ("Yes, because the reading at that setting is " + n1(actual) + ", which is "
                 "at least " + n1(thresh)) if holds else \
                ("No, because the reading at that setting is " + n1(actual) + ", which is "
                 "below " + n1(thresh))
        opposite = ("No, because the reading at that setting is " + n1(actual)
                    + ", which is below " + n1(thresh)) if holds else \
                   ("Yes, because the reading at that setting is " + n1(actual)
                    + ", which is at least " + n1(thresh))
        other = st["s2"] if which == 1 else st["s1"]
        wrong = [opposite,
                 ("Yes, because the reading rises across the settings tested"
                  if st["up"] else "Yes, because the reading falls across the settings tested"),
                 "No, because the other study records " + n1(other[i]) + " at that setting",
                 "Yes, because the two studies were run under otherwise identical conditions",
                 "No, because a single reading cannot settle a prediction of this kind",
                 # Two long ones. The key carries a reading and a comparison, and only
                 # opposite was written at that length, so the pool had nothing above the
                 # key and balance could not place it: one rank held 60 percent of this
                 # schema's 3,200 items (INC-0079). Both are the same kind of wrong
                 # answer, written at the length a real one would be.
                 "Yes, because the reading at that setting is " + n1(actual)
                 + ", and the two studies agree at every setting that was tested",
                 "No, because the other study records " + n1(other[i])
                 + " at that setting, which is below " + n1(thresh)]
        expl = ("Read the Study " + str(which) + " column at a " + scen["iv"][0].lower()
                + " of " + n1(scen["levels"][i]) + " " + scen["iv"][1] + ": it records "
                + n1(actual) + " " + scen["dv"][1] + ". The prediction asks for at least "
                + n1(thresh) + ", so it is " + ("met" if holds else "not met")
                + ". The direction of the trend and the other study's reading are both true "
                "statements that do not answer the question asked.")
        stem = ("A student predicts that, in Study " + str(which) + ", the "
                + scen["dv"][0].lower() + " at a " + scen["iv"][0].lower() + " of "
                + n1(scen["levels"][i]) + " " + scen["iv"][1] + " is at least " + n1(thresh)
                + " " + scen["dv"][1] + ". Is this prediction consistent with the results?")
        return self.choice_item(rng, st, stem, right, wrong, expl, rng.choice([2, 3]), choices_n)


GENS = [ReadValue(), Interpolate(), Trend(), WhatChanged(), HeldConstant(), NextStep(),
        WhyTwoStudies(), IdentifyVariable(), AttributeDifference(),
        ClaimCheck(), BestSupported(), ClaimAtSetting()]


# A template is a promise about the grammar of what goes into it, and the promise is
# invisible: the code says scen["iv"][0] and the sentence around it needs a singular noun
# phrase. Seven of these scenarios were named with a plural one, added over time by
# somebody reading the neighbouring rows rather than the templates, and eight schemas
# shipped sentences like "when the minutes in the dye bath was 30 minutes" (INC-0093).
#
# So the requirement is written down beside the data rather than left in the templates,
# every scenario has to state it, and this refuses a plural. A plural name is not
# forbidden in principle; it is forbidden until the templates can take one, and the
# schema that wants one should change them and then change this.
SING_ONLY = ("Every ACT science variable name goes into a slot like 'the {name} was' "
             "and 'as the {name} rises', so the templates need a singular noun phrase. "
             "Rename the variable rather than declaring it plural, which is what the "
             "seven that were plural turned out to want anyway: four of them carried "
             "their own unit ('Days of curing (days)') and read better without it.")

# The verbs a template puts straight after a variable name, and what each looks like when
# the subject is plural. Rendered items are searched for the wrong pairing, because a
# declaration that nothing checks against the text is the same invisible promise one
# level up.
AGREEMENT = {"was": "were", "is": "are", "rises": "rise", "falls": "fall",
             "runs": "run", "moves": "move", "changes": "change", "goes": "go",
             "has": "have", "increases": "increase", "decreases": "decrease"}


def check_names(draws=400, choices_n=4):
    """Fail on a scenario that does not declare singular variables, or on an item whose
    text puts a variable name in front of a verb that disagrees with it."""
    import random as _random
    bad = []
    for sc in SCEN:
        got = sc.get("num")
        if not (isinstance(got, tuple) and len(got) == 2):
            bad.append("scenario %s does not declare the number of its variables. %s"
                       % (sc["key"], SING_ONLY))
        elif got != ("sing", "sing"):
            bad.append("scenario %s declares %r. %s" % (sc["key"], got, SING_ONLY))
    names = sorted({sc[k][0].lower() for sc in SCEN for k in ("iv", "dv")},
                   key=len, reverse=True)
    for g in GENS:
        rng = _random.Random(20260922)
        seen = set()
        for _ in range(draws):
            try:
                it = g.make(rng, choices_n)
            except (ItemError, ArithmeticError):
                continue
            text = " ".join([it["stem"], it["expl"], " ".join(map(str, it["choices"]))])
            low = " " + " ".join(text.lower().split()) + " "
            for name in names:
                for sing, plur in AGREEMENT.items():
                    # The singular verb is the one the templates write, so a plural name
                    # in front of it is the fault; the reverse would mean a template was
                    # changed to suit a plural and the rest were not.
                    for verb, wrong_when in ((sing, "plur"), (plur, "sing")):
                        if (" " + name + " " + verb + " ") in low:
                            num = [sc["num"][0 if sc["iv"][0].lower() == name else 1]
                                   for sc in SCEN
                                   if name in (sc["iv"][0].lower(), sc["dv"][0].lower())]
                            if wrong_when in num:
                                key = (g.id, name, verb)
                                if key not in seen:
                                    seen.add(key)
                                    bad.append("%s: '%s %s' does not agree"
                                               % (g.id, name, verb))
    return bad
