"""Reading comprehension: generated questions over authored passages.

The honest position on this category, established by measurement rather than assumed:
a reading question worded the same way across two different passages is ONE item under
the dedup key, because the stem and the choices are identical. So item count here is
gated on how many PASSAGES exist, and no amount of generator cleverness changes that.
What the generator can do is extract the largest honest number of distinct questions from
each passage, which is what this module is built to do.

The passages are written, not generated. Each one is stored as complete sentences under
named roles, and the module assembles them and derives the questions. That keeps the prose
at the standard of the hand written passages, because a person wrote every sentence, while
the questions stay computable from the structure.

Every passage follows the revision narrative, which is what most academic reading passages
actually are: a received view, the reason it was held, the thing it could not explain, two
findings with specifics, the revised account, and a qualification.

Two question families come out of that, and they are the two the GMAT reports separately:

  Stated idea asks what the passage says. The key is a sentence the passage contains, and
  the distractors are other sentences it also contains, which are true but do not answer
  the stem. That is the real trap on this question type, and it is decidable.

  Inferred idea asks what follows. Each passage carries two conditionals of the form
  "every X that showed A also had B", paired with a case that lacks B. Modus tollens gives
  a key that must be true, and the distractors are the converse and inverse errors, which
  are the mistakes this question type is actually testing for.

Nothing here asserts a key. What the passage states is data; what follows from it is
derived by the same rule every time.
"""
from framework import Gen, ItemError, balance

# --- the corpus --------------------------------------------------------------------
# Each entry is one passage. Fields are written sentences, not templates:
#   old        the received view, as a full sentence
#   old_why    the reasoning that supported it
#   problem    what it could not account for
#   ev1/ev2    a finding: who, where, what (the finding), detail (a methodological fact)
#   revision   the account the evidence supports
#   caveat     a limit the author acknowledges
#   cond1/2    (universal, case, conclusion): every X with A had B; this case lacks B;
#              therefore it is not an X with A. Written so all three read naturally.
#   about      what the passage is primarily concerned with, in this passage's own terms
#   implies    what the caveat implies, in this passage's own terms
P = [
 dict(key="tundra", topic="Arctic carbon",
  old="Until the late 1980s, ecologists treated the Arctic tundra as a permanent carbon sink.",
  old_why="Cold soils decompose organic matter far more slowly than plants deposit it, so the balance seemed certain to run one way.",
  problem="The account rested entirely on measurements taken during the brief summer, when photosynthesis is at its peak.",
  ev1who="Oechsner and colleagues", ev1where="a monitoring station on the Alaskan North Slope",
  ev1what="the soil released more carbon between October and April than the vegetation had taken up across the whole of the preceding summer",
  ev1detail="their instruments ran continuously for three years rather than being read seasonally",
  ev2who="A later survey", ev2where="eleven sites across northern Canada",
  ev2what="the same winter reversal appeared wherever the snowpack exceeded forty centimetres",
  ev2detail="deep snow insulates the soil well enough for microbes to stay active beneath it",
  revision="whether the tundra is a sink depends on the season in which it is measured and on how much snow falls",
  caveat="None of the sites studied lies south of the treeline, where soils are warmer and the snowpack thinner.",
  cond1=("every site in the Canadian survey that showed the winter reversal had a snowpack deeper than forty centimetres",
         "the Kivalliq site recorded a snowpack of twenty-two centimetres",
         "the Kivalliq site did not show the winter reversal", "the Kivalliq site"),
  cond2=("every reading that captured the reversal was taken by an instrument running through the winter",
         "the Barrow readings were taken only in July and August",
         "the Barrow readings did not capture the reversal", "the Barrow readings"),
  about="revising a settled account of Arctic carbon by showing that it rested on measurements taken in one season only",
  implies="the revised account has not been tested in the warmer conditions south of the treeline"),

 dict(key="guilds", topic="English craft guilds",
  old="Historians long explained the decline of the English craft guilds as a consequence of industrial machinery.",
  old_why="Machinery is assumed to have made the guild workshop uneconomic almost as soon as it arrived.",
  problem="The chronology has never fit, because most guilds lost their membership decades before machinery reached their trades.",
  ev1who="Halloway", ev1where="the admission books of the Sheffield cutlers",
  ev1what="membership fell by half between 1790 and 1820, a generation before mechanised grinding entered the trade",
  ev1detail="the books record every admission with a date and a named sponsor",
  ev2who="A study of apprenticeship indentures", ev2where="four other Sheffield trades",
  ev2what="the same early fall appeared wherever the guild had lost its power to prosecute unlicensed work",
  ev2detail="that power was removed by statute at different dates in different trades",
  revision="the guilds were undone by the loss of their legal monopoly, and machinery arrived to find them already weakened",
  caveat="The Sheffield records are unusually complete, and no comparable series survives for the textile towns.",
  cond1=("every trade in the study that showed the early fall had already lost its power to prosecute unlicensed work",
         "the farriers retained that power until 1835",
         "the farriers did not show the early fall before 1835", "the farriers"),
  cond2=("every figure Halloway reports comes from a book that records a sponsor for each admission",
         "the cutlers' journeyman register records no sponsors",
         "Halloway's figures do not come from the journeyman register", "the journeyman register"),
  about="reordering the causes of an institutional decline by showing that the usual explanation arrives too late to account for it",
  implies="the argument may not extend to trades whose records have not survived"),

 dict(key="reefs", topic="coral colour",
  old="For most of the twentieth century, marine biologists attributed the bright colour of shallow water corals to the pigments of the algae living inside them.",
  old_why="The algae are the obvious source, since they are abundant, pigmented, and present in every healthy colony.",
  problem="The explanation cannot account for corals that stay vividly coloured after the algae have been expelled.",
  ev1who="Takeda", ev1where="a reef flat in the Ryukyu Islands",
  ev1what="bleached colonies went on fluorescing for up to nine weeks, long after any algal pigment would have degraded",
  ev1detail="the colonies were photographed each week under light of identical intensity",
  ev2who="Later laboratory work", ev2where="colonies raised without algae from the larval stage",
  ev2what="the coral itself produces the fluorescent proteins, in every colony kept under strong light",
  ev2detail="colonies held in shade produced almost none of the proteins",
  revision="the colour belongs to the coral, and the algae contribute to it only indirectly",
  caveat="Whether the proteins shield the coral from light, as is often suggested, remains untested.",
  cond1=("every colony in the laboratory work that produced the fluorescent proteins was kept under strong light",
         "the colonies in the fourth tank were held in shade throughout",
         "the colonies in the fourth tank did not produce the fluorescent proteins", "the colonies in the fourth tank"),
  cond2=("every colony Takeda photographed was recorded under light of identical intensity",
         "the colonies at the reef margin were photographed under whatever light the day provided",
         "the colonies at the reef margin were not among those Takeda photographed", "the colonies at the reef margin"),
  about="relocating the source of a familiar phenomenon from an organism's partner to the organism itself",
  implies="the function of the proteins remains an open question even though their source is now settled"),

 dict(key="roads", topic="road widening",
  old="Transport planners have generally assumed that widening a congested road reduces the time drivers spend on it.",
  old_why="The same traffic spread across more lanes should move faster, which is true of any fixed quantity of vehicles.",
  problem="The assumption treats the number of drivers as fixed, and it is not.",
  ev1who="Duranton and Turner", ev1where="the interstate network of 228 American cities",
  ev1what="vehicle miles travelled rose almost exactly in proportion to the lane miles added, leaving average speeds unchanged",
  ev1detail="their comparison covers the two decades to 2003",
  ev2who="A narrower study", ev2where="six corridors widened in the same period",
  ev2what="the new traffic appeared within five years wherever the corridor joined two growing suburbs",
  ev2detail="corridors between districts of stable population kept their improved speeds",
  revision="added capacity is taken up by drivers who did not previously make the trip, so widening relieves congestion only where surrounding demand is not growing",
  caveat="Every corridor studied is urban, and nothing here settles the case for rural routes.",
  cond1=("every corridor in the narrower study where new traffic appeared within five years joined two growing suburbs",
         "the Elkford corridor runs between districts whose population has been stable for thirty years",
         "new traffic did not appear within five years on the Elkford corridor", "the Elkford corridor"),
  cond2=("every figure Duranton and Turner report is drawn from the two decades to 2003",
         "the Pearson expansion was completed in 2011",
         "the Pearson expansion is not among the cases their figures cover", "the Pearson expansion"),
  about="explaining why a measure fails to produce its expected effect by identifying a quantity the usual reasoning treats as fixed",
  implies="the conclusion is drawn entirely from urban cases and may not hold elsewhere"),
]


def check_corpus():
    """A malformed passage would produce a question with no defensible key, so the shape
    is checked at import rather than trusted."""
    seen = set()
    need = ("old old_why problem ev1who ev1where ev1what ev1detail ev2who ev2where "
            "ev2what ev2detail revision caveat about implies").split()
    for p in P:
        if p["key"] in seen:
            raise ItemError("duplicate passage key %r" % p["key"])
        seen.add(p["key"])
        for f in need:
            if not p.get(f) or not str(p[f]).strip():
                raise ItemError("passage %s is missing %s" % (p["key"], f))
        for c in ("cond1", "cond2"):
            if len(p[c]) != 4 or not all(str(x).strip() for x in p[c]):
                raise ItemError("passage %s has a malformed %s" % (p["key"], c))


check_corpus()


def text(p):
    """The passage as the reader sees it: two paragraphs of the authored sentences."""
    one = " ".join([p["old"], p["old_why"], p["problem"]])
    two = ("%s examined %s and found that %s; %s. %s of %s found that %s, and %s. "
           "Taken together the two results suggest that %s. %s") % (
        p["ev1who"], p["ev1where"], p["ev1what"], p["ev1detail"],
        p["ev2who"], p["ev2where"], p["ev2what"], p["ev2detail"],
        p["revision"], p["caveat"])
    return one + "\n\n" + two


def sentences(p):
    """Everything the passage states, as candidate answers. A distractor drawn from here
    is TRUE of the passage and simply does not answer the stem, which is the trap this
    question type is really about."""
    return {
        "old": p["old"].rstrip("."),
        "old_why": p["old_why"].rstrip("."),
        "problem": p["problem"].rstrip("."),
        "ev1what": p["ev1what"],
        "ev2what": p["ev2what"],
        "ev1detail": p["ev1detail"],
        "ev2detail": p["ev2detail"],
        "revision": p["revision"],
        "caveat": p["caveat"].rstrip("."),
    }


def lower1(s):
    return s[0].lower() + s[1:] if s else s


class RCBase(Gen):
    section = "V"
    type = "RC"
    domain = "nonmath"

    def emit(self, rng, choices_n, p, stem, right, pool, expl, diff, skill, sub):
        cands = [(w, "") for w in pool if w != right]
        if len(cands) < choices_n - 1:
            raise ItemError("%s has only %d distractors" % (self.id, len(cands)))
        opts = [right] + [w for w, _ in balance(rng, right, cands, choices_n - 1)]
        if len(set(opts)) != choices_n:
            raise ItemError("%s drew a repeated option" % self.id)
        rng.shuffle(opts)
        item = {
            "id": None, "section": "V", "type": "RC", "sub": sub, "skill": skill,
            "diff": diff, "passage": text(p), "passageId": "GP_" + p["key"],
            "stem": stem, "choices": opts, "answer": opts.index(right),
            "expl": expl, "gen": self.id, "domain": "nonmath",
            # Identity is the passage plus the question asked of it, never which other
            # sentences of the same passage were offered as distractors.
            "canon_ignores_choices": True,
            "wrong": "Every other choice states something the passage also says. They are "
                     "true, and none of them answers the question that was asked, which is "
                     "what makes them tempting.",
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


class StatedIdea(RCBase):
    """What the passage says. Six askable sentences per passage, each its own question."""
    id = "rc_stated"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 2

    ASKS = [
        ("ev1what", lambda p: "According to the passage, %s found that" % p["ev1who"]),
        ("ev2what", lambda p: "According to the passage, %s of %s found that"
                              % (p["ev2who"], p["ev2where"])),
        ("old_why", lambda p: "The passage indicates that the earlier view was held on the "
                              "grounds that"),
        ("problem", lambda p: "According to the passage, the earlier account failed to "
                              "address the fact that"),
        ("ev1detail", lambda p: "The passage states that, in the work of %s," % p["ev1who"]),
        ("ev2detail", lambda p: "According to the passage, the second set of results also "
                                "established that"),
    ]

    def make(self, rng, choices_n):
        p = rng.choice(P)
        field, stem = rng.choice(self.ASKS)
        s = sentences(p)
        right = lower1(s[field])
        pool = [lower1(v) for k, v in s.items() if k != field]
        expl = ("The passage says exactly this, and the question asks only what it says. "
                "Each of the other choices is also drawn from the passage, so each is true; "
                "none of them is what the stem asked about.")
        return self.emit(rng, choices_n, p, stem(p), right, pool, expl,
                         rng.choice([1, 2, 2, 3]), "v_st", self.sub)


class MainIdea(RCBase):
    """Primary concern, worded in this passage's own terms so it is a distinct item."""
    id = "rc_main"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 3

    def make(self, rng, choices_n):
        p = rng.choice(P)
        others = [q for q in P if q["key"] != p["key"]]
        if len(others) < choices_n - 1:
            raise ItemError("rc_main needs more passages for distractors")
        right = p["about"]
        pool = [q["about"] for q in others]
        expl = ("The passage opens with the received view, shows what it cannot account "
                "for, presents two findings, and states what they support. That is the "
                "shape of the whole passage, and the correct choice describes it. The other "
                "choices describe what a different passage on a different subject does.")
        return self.emit(rng, choices_n, p, "The passage is primarily concerned with",
                         right, pool, expl, rng.choice([2, 3, 3]), "v_st", self.sub)


class Inference(RCBase):
    """Modus tollens over a conditional the passage states.

    The key MUST be true given two things the passage says. The distractors are the two
    classic invalid moves, the converse and the inverse, plus statements the passage does
    not license at all. That is what this question type tests, so the distractors are the
    misconceptions rather than decoration.
    """
    id = "rc_infer"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 4

    def make(self, rng, choices_n):
        p = rng.choice(P)
        cond = rng.choice([p["cond1"], p["cond2"]])
        univ, case, concl, subject = cond
        other = p["cond2"] if cond is p["cond1"] else p["cond1"]
        right = concl[0].upper() + concl[1:] + "."
        pool = [
            # The converse: having the property does not make it a member.
            "Any case with the property described in the passage must be one of those the "
            "passage's generalisation covers.",
            # The inverse: denying the antecedent.
            "Cases outside the passage's generalisation cannot have the property it "
            "describes.",
            other[2][0].upper() + other[2][1:] + ".",
            lower1(p["revision"])[0].upper() + lower1(p["revision"])[1:] + " in every case.",
            p["caveat"].rstrip(".") + " for the same reason.",
        ]
        expl = ("The passage states that %s. It also states that %s. If every case of the "
                "one kind has the property, then a case lacking the property is not a case "
                "of that kind, so %s. The two tempting wrong answers reverse that reasoning: "
                "one assumes that having the property makes a case a member, and the other "
                "assumes that a non-member cannot have it. Neither follows."
                % (univ, case, concl))
        # The stem names the case it asks about. Both conditionals in a passage otherwise
        # produce the identical stem "which of the following can be inferred", so the two
        # collapse into one item and half the inference questions in the corpus vanish.
        stem = ("Which of the following can be properly inferred from the passage about %s?"
                % subject)
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([3, 4, 4, 5]), "v_inf", self.sub)


class CaveatImplication(RCBase):
    """What the author's qualification implies, worded per passage."""
    id = "rc_caveat"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 3

    def make(self, rng, choices_n):
        p = rng.choice(P)
        others = [q for q in P if q["key"] != p["key"]]
        if len(others) < choices_n - 1:
            raise ItemError("rc_caveat needs more passages for distractors")
        right = p["implies"]
        pool = [q["implies"] for q in others]
        expl = ("The closing sentence names a limit on the evidence rather than a doubt "
                "about it, so what it implies is that the revised account has not been "
                "tested outside the range the studies covered. The other choices state "
                "limits that belong to a different passage.")
        stem = "The author's closing observation most strongly suggests that"
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([2, 3, 3, 4]), "v_inf", self.sub)


GENS = [StatedIdea(), MainIdea(), Inference(), CaveatImplication()]
