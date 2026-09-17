"""GMAT Verbal: Analysis / Critique and Plan / Construct.

Critical reasoning looks like the least generatable category on the exam, because the
answer is a judgement about an argument rather than a number. It becomes generatable once
the argument itself is built from a structure rather than written as prose: if the draw
records what the evidence is, what the conclusion is, and what the gap between them is,
then the assumption, the weakener, the strengthener and the flaw are all determined by
that structure, and each one is produced from it rather than chosen by taste.

Every schema here is a named reasoning gap that real arguments actually have:

  cause        a correlation is reported and a cause is concluded. The gap is the
               alternative explanation that the draw names and then uses.
  sample       a subgroup is surveyed and a population is concluded about. The gap is
               whether the subgroup resembles the population in the relevant respect.
  percent      a share moves and a count is concluded about. The gap is the denominator.
  necessary    something common to every success is treated as what produces success.
  plan         an action is proposed to reach a goal. The gap is the condition the action
               needs in order to have the effect claimed.

The distractors are the four ways an answer choice goes wrong on this question type, and
they are built from the same draw so they stay on topic: restating a premise, addressing
the right subject in the wrong direction, raising something the argument never depends on,
and answering a different question than the one asked. Each is named in the item.

The length discipline from the verbal rewrite applies: a key that carries a mechanism and
its evidence while distractors carry one clause is a key spottable by length alone. Here
every option is a single clause of comparable weight, and test.js measures what came out.
"""
from framework import Gen, ItemError, balance

# Each scenario supplies the nouns. The reasoning is in the schema, not here, so a new
# scenario multiplies every schema without touching any of them.
CAUSE = [
    dict(place="the town of Averly", thing="a riverside cycle path",
         effect="the number of residents cycling to work", rose="rose by a third",
         alt="the town's main employer moved its offices to a site the path passes",
         alt_short="the employer relocated onto the path's route",
         short="the cycle path", people="residents of Averly",
         other="the cost of a monthly bus pass rose sharply in the same year"),
    dict(place="Calder District", thing="a free evening homework club",
         effect="pass rates at the district's secondary schools", rose="rose by eight points",
         alt="the district replaced its examination board in the same term",
         alt_short="the examination board changed at the same time",
         short="the homework club", people="families in Calder District",
         other="two schools in the district merged the following year"),
    dict(place="Norbury Hospital", thing="a new triage procedure",
         effect="the average wait in the emergency department", rose="fell by 40 minutes",
         alt="a second emergency department opened nearby and took a share of the arrivals",
         alt_short="a nearby department opened and took some arrivals",
         short="the new procedure", people="staff at Norbury Hospital",
         other="the hospital renamed two of its wards that spring"),
    dict(place="Pell Valley", thing="a ban on winter salt on the roads",
         effect="the number of fish counted in the valley's streams", rose="rose by half",
         alt="an upstream factory closed the year the ban took effect",
         alt_short="an upstream factory closed in the same year",
         short="the salt ban", people="residents of Pell Valley",
         other="the counting was carried out by the same team as before"),
    dict(place="Westmere Library", thing="a Sunday opening trial",
         effect="the number of books borrowed each week", rose="rose by a quarter",
         alt="the library began stocking a popular series it had not carried before",
         alt_short="the stock changed at the same time",
         short="the Sunday trial", people="users of Westmere Library",
         other="the library repainted its entrance hall during the trial"),
    dict(place="Rossiter Foods", thing="a four day working week",
         effect="the number of units leaving the packing line each week", rose="rose by a fifth",
         alt="the company replaced the packing line's machinery in the same month",
         alt_short="the machinery was replaced at the same time",
         short="the shorter week", people="employees at Rossiter Foods",
         other="the company changed the colour of its packaging that quarter"),
]

SAMPLE = [
    dict(who="subscribers to a cycling magazine", pop="residents of the city",
         claim="most residents would use a new bicycle lane on Mill Road",
         why="people who subscribe to a cycling magazine cycle far more than residents in general",
         topic="the bicycle lane"),
    dict(who="visitors leaving the museum's paid exhibition", pop="the museum's visitors",
         claim="most visitors are willing to pay for exhibitions",
         why="everyone asked had already chosen to pay for an exhibition",
         topic="willingness to pay"),
    dict(who="employees who attended the optional training", pop="the company's employees",
         claim="the training is valued across the company",
         why="attending was optional, so those asked had already chosen to go",
         topic="the training"),
    dict(who="customers who returned a warranty card", pop="the product's buyers",
         claim="buyers are satisfied with the product",
         why="customers who take the trouble to return a card are not typical buyers",
         topic="satisfaction"),
    dict(who="parents who came to the evening meeting", pop="parents at the school",
         claim="parents support moving the school day an hour later",
         why="the meeting was held in the evening, which suits some parents' schedules and not others",
         topic="the change to the school day"),
]

PERCENT = [
    dict(subject="accidents involving drivers under 21", share="fell from 18 percent to 12 percent",
         conclude="drivers under 21 are having fewer accidents than before",
         gap="the total number of accidents", direction="rose sharply over the same period",
         unit="accidents"),
    dict(subject="complaints about late deliveries", share="fell from a quarter to a sixth of all complaints",
         conclude="late deliveries are becoming less common",
         gap="the total number of complaints", direction="more than doubled over the same period",
         unit="complaints"),
    dict(subject="the share of the council's budget spent on road repair",
         share="fell from 9 percent to 6 percent",
         conclude="the council is spending less on repairing roads",
         gap="the council's total budget", direction="grew by half over the same period",
         unit="pounds"),
    dict(subject="the proportion of graduates entering teaching",
         share="fell from 11 percent to 8 percent",
         conclude="fewer graduates are becoming teachers",
         gap="the number of graduates", direction="rose by two thirds over the same period",
         unit="graduates"),
]

PLAN = [
    dict(who="Hollis City Council", goal="reduce traffic on Bridge Street",
         action="make parking on Bridge Street free after six in the evening",
         needs="the traffic on Bridge Street is mostly drivers circling in search of a space",
         fails="most of the traffic is through traffic with no intention of stopping",
         check="what share of the traffic on Bridge Street stops there at all"),
    dict(who="Aldergate Hospital", goal="cut the number of missed appointments",
         action="send every patient a reminder by text the day before",
         needs="patients miss appointments because they forget them",
         fails="most missed appointments are missed because patients cannot get there",
         check="why patients who missed an appointment say they missed it"),
    dict(who="Marden Publishing", goal="raise the number of manuscripts it reviews each month",
         action="hire two more editors",
         needs="reviewing is limited by how many editors are available",
         fails="manuscripts wait longest at the legal check, which the new editors do not do",
         check="which stage of the process manuscripts spend the longest waiting at"),
    dict(who="the Thorne Museum", goal="increase weekday attendance",
         action="open two hours earlier on weekdays",
         needs="there are people who would visit on a weekday but cannot come at the current hours",
         fails="weekday visitors already arrive well after opening and leave before closing",
         check="when weekday visitors currently arrive and leave"),
    dict(who="Bellwood Transit", goal="reduce the time buses spend at stops",
         action="require passengers to pay before boarding",
         needs="the time at a stop is mostly taken up by passengers paying as they board",
         fails="most of the time at a stop is taken by passengers finding seats after boarding",
         check="how the time a bus spends at a stop is currently divided"),
]

NECESSARY = [
    dict(common="trained at the Fenwick track", group="every runner who won the county title "
         "in the last ten years", conclude="training at the Fenwick track is what produces "
         "county champions", why="the Fenwick track is the only one in the county, so every "
         "competitive runner trains there whether they win or not"),
    dict(common="used the same accountancy firm", group="each of the four companies that "
         "survived the downturn", conclude="using that firm is what carried them through",
         why="the firm is used by most companies in the region, including those that did not "
         "survive"),
    dict(common="began with a grant from the Halloran Fund",
         group="all six of the laboratory's patented discoveries",
         conclude="a Halloran grant is what makes a discovery patentable",
         why="the Halloran Fund supplies the starting grant for nearly all of the "
         "laboratory's work, patented or not"),
]


PLAN += [
    dict(who="Ferndale School", goal="raise the number of pupils walking to school",
         action="close the road outside the gates to cars at drop off time",
         needs="the pupils who are driven live close enough to walk",
         fails="most pupils who are driven live several miles away",
         check="how far from the school the pupils who are driven actually live"),
    dict(who="Calloway Insurance", goal="shorten the time taken to settle a claim",
         action="allow claims to be submitted through an app as well as by post",
         needs="the delay is in getting the claim to the assessor",
         fails="claims already reach the assessor within a day and wait weeks after that",
         check="where in the process a claim currently spends the most time"),
    dict(who="the Whitcombe Estate", goal="reduce water used on the gardens",
         action="water the beds at dawn rather than at midday",
         needs="a large share of the water applied at midday is lost to evaporation",
         fails="the beds are watered below the surface, where evaporation is negligible",
         check="how much of the water applied at midday is currently lost before it reaches "
               "the roots"),
]


class CRBase(Gen):
    section = "V"
    type = "CR"
    domain = "nonmath"

    def emit(self, rng, choices_n, stem, right, wrongs, expl, diff, skill, sub):
        # Each schema offers MORE named wrong answer types than an item has slots, and each
        # item draws a different subset. That is the honest way to get variety out of a
        # small scenario pool: reshuffling one item's options produces the same question
        # with the letters moved, while a different subset of wrong answers is a different
        # question, because what the student has to rule out has changed.
        pool = [w for w in wrongs if w[0] != right]
        if len(pool) < choices_n - 1:
            raise ItemError("%s has only %d wrong answer types" % (self.id, len(pool)))
        # Straddle the key's length rather than sampling blind. A correct answer on a
        # critical reasoning item tends to be the one carrying a mechanism, which makes it
        # the longest option, and "pick the longest" then beats reading the argument.
        opts = [right] + [w for w, _ in balance(rng, right, pool, choices_n - 1)]
        if len(opts) < choices_n or len(set(opts)) != choices_n:
            raise ItemError("%s could not build %d distinct options" % (self.id, choices_n))
        why = {w: r for w, r in wrongs}
        if len(set(opts)) != choices_n:
            raise ItemError("%s drew a repeated option" % self.id)
        rng.shuffle(opts)
        first = next((o for o in opts if o in why), None)
        item = {
            "id": None, "section": "V", "type": "CR", "sub": sub, "skill": skill,
            "diff": diff, "stem": stem, "choices": opts, "answer": opts.index(right),
            "expl": expl, "gen": self.id, "domain": "nonmath",
            "wrong": ("Choice " + "ABCDE"[opts.index(first)] + " " + why[first] + "."
                      if first else ""),
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


# --- Analysis / Critique -----------------------------------------------------------
class CauseWeaken(CRBase):
    id = "cr_cause_weaken"
    skill = "v_ac"
    sub = "Weaken the argument"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(CAUSE)
        stem = ("After " + d["place"] + " opened " + d["thing"] + ", " + d["effect"]
                + " " + d["rose"] + ". Officials concluded that " + d["short"]
                + " was responsible for the change.\n\nWhich of the following, if true, "
                "most seriously weakens the officials' conclusion?")
        right = d["alt"].capitalize() + "."
        wrongs = [
            ("No other district in the region opened anything comparable in the same period.",
             "rules out a rival explanation elsewhere, which supports the conclusion rather "
             "than weakening it"),
            (d["other"].capitalize() + ".",
             "reports something that happened at the same time but that could not affect "
             + d["effect"]),
            ("Officials had expected the change to take longer than it did.",
             "comments on how the result compared with expectations, which bears on nobody's "
             "forecasting rather than on the cause"),
            (d["effect"].capitalize() + " has been measured the same way for twenty years.",
             "defends the measurement, which the argument was not being challenged on"),
            ("Some of the " + d["people"] + " said they welcomed " + d["short"] + ".",
             "reports approval, which is not the same as showing the change was caused by it"),
            ("The change was larger than officials in " + d["place"] + " had predicted.",
             "compares the result with a prediction, which bears on the forecast rather than "
             "on the cause"),
            ("Two neighbouring districts recorded no comparable change in the same period.",
             "reports the absence of the effect where the cause was also absent, which is "
             "evidence for the conclusion rather than against it"),
            (d["short"].capitalize() + " cost less to build than had been budgeted.",
             "addresses cost, which the causal conclusion says nothing about"),
        ]
        expl = ("The conclusion moves from a correlation to a cause, so it is weakened by an "
                "alternative explanation for the same change. " + d["alt"].capitalize()
                + ", which would produce the same movement in " + d["effect"]
                + " with or without " + d["short"] + ".")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([2, 3, 3, 4]), "v_ac", self.sub)


class CauseAssume(CRBase):
    id = "cr_cause_assume"
    skill = "v_ac"
    sub = "Identify the assumption"
    diff = 4

    def make(self, rng, choices_n):
        d = rng.choice(CAUSE)
        stem = ("After " + d["place"] + " opened " + d["thing"] + ", " + d["effect"]
                + " " + d["rose"] + ". Officials concluded that " + d["short"]
                + " was responsible for the change.\n\nThe officials' conclusion depends on "
                "which of the following assumptions?")
        right = ("No other change in the same period was sufficient on its own to move "
                 + d["effect"] + ".")
        wrongs = [
            (d["short"].capitalize() + " was the least expensive of the measures available "
             "to " + d["place"] + " for producing a change of this kind.",
             "argues about cost, which the conclusion about cause does not rest on"),
            ("Every one of the " + d["people"] + " was aware that " + d["short"]
             + " had opened before the change in " + d["effect"] + " was recorded.",
             "demands universal awareness, which the argument never needs"),
            (d["effect"].capitalize() + " will go on changing in the same direction for as "
             "long as " + d["short"] + " remains in place.",
             "predicts the future, while the conclusion is about what caused a change "
             "already observed"),
            ("Officials in " + d["place"] + " consulted those affected before deciding to "
             "open " + d["thing"] + ".",
             "concerns the process followed, not whether the cause claimed is the real one"),
            (d["short"].capitalize() + " will remain in place for at least a decade, so "
             "that its effects can be measured over the long term.",
             "concerns how long the measure lasts, not whether it caused what has happened"),
            ("No measure comparable to " + d["short"] + " had been tried anywhere in "
             + d["place"] + " before this one was opened.",
             "asserts novelty, which the conclusion about cause does not rest on"),
            (d["effect"].capitalize() + " had been stable for several years before "
             + d["short"] + " opened.",
             "describes the period before the change, which makes the conclusion more "
             "plausible rather than being something it requires"),
            ("The change in " + d["effect"] + " was recorded by a body independent of the "
             "officials who drew the conclusion.",
             "vouches for who took the measurement, not for the cause of what was measured"),
        ]
        expl = ("A causal conclusion drawn from a change over time needs the gap closed "
                "between the two: if something else could have produced the same movement, "
                "the conclusion does not follow. Negate the correct choice and the argument "
                "collapses, which is the test of an assumption; negate any of the others and "
                "the argument stands.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([3, 4, 4]), "v_ac", self.sub)


class SampleFlaw(CRBase):
    id = "cr_sample"
    skill = "v_ac"
    sub = "Identify the flaw"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(SAMPLE)
        stem = ("A survey of " + d["who"] + " found strong support for the proposal. The "
                "surveyor concluded that " + d["claim"] + ".\n\nThe reasoning in the "
                "argument is most vulnerable to criticism on the grounds that it:")
        right = ("treats a group with a particular interest in " + d["topic"]
                 + " as though it represented " + d["pop"] + " generally")
        wrongs = [
            ("assumes that support expressed in a survey will translate into action once "
             "those surveyed are asked to do something about it",
             "names a real gap between saying and doing, which is not the gap this argument "
             "turns on"),
            ("fails to specify how many people were asked, leaving the strength of the "
             "evidence impossible to judge from the report alone",
             "asks for a number, when the problem is who was asked rather than how many"),
            ("relies on what people said in a survey rather than on records of what "
             "they have actually done in comparable situations",
             "objects to surveys as such, which would condemn every survey equally"),
            ("does not consider whether the proposal could be paid for out of the funds "
             "that are currently available for such things",
             "raises cost, which the conclusion about support never claims anything about"),
            ("treats the absence of objection from those surveyed as though it were "
             "positive enthusiasm for the proposal",
             "describes a different overreach from the one the argument commits"),
            ("assumes that the proposal will be carried out in the form that was described "
             "to the people who were asked about it",
             "questions implementation, which the conclusion about support does not depend on"),
            ("draws a conclusion about what people will want in future from evidence about "
             "what they say they want at present",
             "names a timing gap, while the gap here is between one group and another"),
            ("overlooks the possibility that some of those asked misunderstood the question "
             "they were answering and replied to a different one",
             "raises a problem with the instrument rather than with who was put in front of it"),
        ]
        expl = ("The evidence covers " + d["who"] + " and the conclusion covers " + d["pop"]
                + ". That step holds only if the two resemble each other in the relevant "
                "respect, and here " + d["why"] + ".")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([2, 3, 3]), "v_ac", self.sub)


class PercentFlaw(CRBase):
    id = "cr_percent"
    skill = "v_ac"
    sub = "Weaken the argument"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(PERCENT)
        stem = ("Over the last five years, " + d["subject"] + " " + d["share"]
                + ". A commentator concluded that " + d["conclude"]
                + ".\n\nWhich of the following, if true, most seriously weakens the "
                "commentator's conclusion?")
        right = d["gap"].capitalize() + " " + d["direction"] + "."
        wrongs = [
            (d["gap"].capitalize() + " was unchanged over the same period.",
             "holds the denominator steady, which is the condition under which the "
             "conclusion would actually follow"),
            ("The figures were collected by the same body throughout the period.",
             "defends the consistency of the data rather than the inference drawn from it"),
            ("Similar changes were recorded in two neighbouring regions.",
             "reports the same pattern elsewhere, which does nothing about the step from a "
             "share to a count"),
            ("The commentator has written on this subject for many years.",
             "addresses the commentator rather than the argument"),
            ("Other regions recorded a similar fall in the same share.",
             "shows the pattern is widespread, which leaves the share to count step untouched"),
            ("The definition of " + d["subject"] + " was unchanged throughout the period.",
             "rules out a definitional artefact, which would be needed for the conclusion to "
             "hold rather than being a reason to doubt it"),
            ("The period studied includes two years of unusual weather.",
             "offers a possible cause of movement without addressing the share to count step"),
        ]
        expl = ("A share can fall while the count rises, if the total it is a share of rises "
                "faster. The conclusion is about a count in " + d["unit"] + " while the "
                "evidence is about a proportion, so a large enough rise in " + d["gap"]
                + " makes the conclusion false while every stated fact stays true.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([3, 3, 4]), "v_ac", self.sub)


class NecessaryFlaw(CRBase):
    id = "cr_necessary"
    skill = "v_ac"
    sub = "Identify the flaw"
    diff = 4

    def make(self, rng, choices_n):
        d = rng.choice(NECESSARY)
        stem = ("It has been noted that " + d["group"] + " " + d["common"] + ". It follows "
                "that " + d["conclude"] + ".\n\nWhich of the following, if true, most "
                "seriously undermines the conclusion?")
        right = d["why"].capitalize() + "."
        wrongs = [
            ("Some of those who achieved the same result elsewhere did so without any "
             "advantage comparable to the one described here.",
             "reports a different route to the result, which does not show "
             "that this one is not what produced it here"),
            ("The advantage described has been available to anyone who wanted it for a "
             "great many years before the period in question.",
             "dates the advantage without saying anything about who else had it"),
            ("Those involved regard the advantage as having been important to what they "
             "went on to achieve.",
             "cites the belief of the people involved, which supports the conclusion rather "
             "than undermining it"),
            ("No formal study of the question has been carried out, so the matter rests on "
             "the pattern described and nothing further.",
             "notes the absence of evidence either way, which leaves the conclusion exactly "
             "where it was"),
            ("The advantage has become considerably more expensive to obtain in recent "
             "years than it was over the period described.",
             "reports a change in cost, which says nothing about who else has had it"),
            ("Those who lacked the advantage were never asked what results they achieved, "
             "so their outcomes are simply unrecorded.",
             "points at a gap in the data, which weakens the evidence without showing the "
             "conclusion false"),
            ("The result in question is also achieved, though less often, by people well "
             "outside the group described here.",
             "shows the result is not unique to the group, which is a different objection"),
        ]
        expl = ("Something shared by every success is only a cause of success if it is not "
                "equally shared by the failures. The correct choice supplies exactly that: "
                "the same feature is common to those who did not achieve the result, so it "
                "cannot be what separates them.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([3, 4, 4, 5]), "v_ac", self.sub)


# --- Plan / Construct ---------------------------------------------------------------
class PlanAssume(CRBase):
    id = "cr_plan_assume"
    skill = "v_pc"
    sub = "Evaluate a plan"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(PLAN)
        stem = (d["who"] + " intends to " + d["goal"] + ". To that end it will "
                + d["action"] + ".\n\nThe plan's success depends on which of the following?")
        right = "That " + d["needs"] + "."
        wrongs = [
            ("That " + d["who"] + " can afford to carry out the measure.",
             "raises whether the measure can be paid for, which is a separate question from "
             "whether it would work"),
            ("That no other body has tried the same measure before.",
             "asks for novelty, which has no bearing on whether the measure produces the "
             "intended effect"),
            ("That the measure will be popular with those it affects.",
             "concerns how the measure is received rather than whether it achieves the goal"),
            ("That " + d["goal"] + " is the most urgent of the problems facing " + d["who"]
             + ".", "ranks the goal against other goals, which the plan's success does not "
             "turn on"),
            ("That no other body has objected to the measure.",
             "raises opposition, which bears on whether the measure happens rather than on "
             "whether it works"),
            ("That the measure can be reversed if it does not work.",
             "concerns what happens afterwards, not whether the effect follows"),
            ("That " + d["who"] + " has tried to " + d["goal"] + " before.",
             "asks about history, which the plan's prospects do not depend on"),
        ]
        expl = ("A plan works only if the cause of the problem is the one the action "
                "addresses. This action addresses the problem only if " + d["needs"]
                + "; if instead " + d["fails"] + ", the action changes nothing.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([2, 3, 3, 4]), "v_pc", self.sub)


class PlanWeaken(CRBase):
    id = "cr_plan_weaken"
    skill = "v_pc"
    sub = "Evaluate a plan"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(PLAN)
        stem = (d["who"] + " intends to " + d["goal"] + ". To that end it will "
                + d["action"] + ".\n\nWhich of the following, if true, provides the "
                "strongest reason to doubt that the plan will succeed?")
        right = d["fails"].capitalize() + "."
        wrongs = [
            (d["needs"].capitalize() + ".",
             "states the very condition the plan needs, so it supports the plan instead of "
             "casting doubt on it"),
            ("A similar measure elsewhere took two years to show any effect.",
             "bears on how quickly the plan would work rather than on whether it would"),
            ("Some of those affected have said they would prefer a different measure.",
             "reports a preference, which does not show the measure ineffective"),
            (d["who"] + " has not announced how the measure will be funded.",
             "notes an unanswered question about funding, not about effect"),
            ("The measure will take several months to put in place.",
             "bears on timing rather than on whether the goal is reached"),
            ("A different body rejected a comparable measure last year.",
             "reports someone else's decision, which is not evidence about the effect"),
            ("Staff at " + d["who"] + " were not consulted about the measure.",
             "concerns process, not effect"),
        ]
        expl = ("The plan assumes that " + d["needs"] + ". The correct choice denies exactly "
                "that: if " + d["fails"] + ", then carrying out the action leaves the "
                "problem where it was, however well the action is executed.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([2, 3, 3, 4]), "v_pc", self.sub)


class PlanEvaluate(CRBase):
    id = "cr_plan_eval"
    skill = "v_pc"
    sub = "Evaluate a plan"
    diff = 4

    def make(self, rng, choices_n):
        d = rng.choice(PLAN)
        stem = (d["who"] + " intends to " + d["goal"] + ". To that end it will "
                + d["action"] + ".\n\nWhich of the following would be most useful to "
                "establish in evaluating whether the plan will achieve its goal?")
        right = "Whether " + d["check"].capitalize()[0].lower() + d["check"][1:] + " is what "\
                "the measure would change."
        wrongs = [
            ("Whether " + d["who"] + " has the legal power to carry out a measure of this "
             "kind without seeking approval from anyone else.",
             "settles whether the plan can be done, not whether doing it would work"),
            ("Whether a measure of this kind has been tried by a comparable body elsewhere "
             "and what happened when it was.",
             "looks for precedent, which is useful background but does not test this case"),
            ("Whether the cost of putting the measure in place falls within the budget "
             + d["who"] + " has already set aside.",
             "tests affordability rather than effect"),
            ("Whether those affected by the measure were consulted at any point before it "
             "was announced publicly.",
             "tests the process rather than the outcome"),
            ("Whether " + d["who"] + " could put the measure fully in place before the end "
             "of the current year rather than the next one.",
             "tests how quickly it could be done, which does not bear on whether it "
             "would work"),
            ("Whether the measure would attract enough attention in the local press for "
             "those affected to hear about it.",
             "tests visibility rather than effect"),
            ("Whether any member of " + d["who"] + " opposed the measure at the point when "
             "it was put to a decision.",
             "tests agreement rather than effect"),
        ]
        expl = ("A question is useful for evaluating a plan when the two possible answers "
                "point in opposite directions. Establish " + d["check"]
                + ", and one answer means the measure addresses the cause while the other "
                "means it does not. The remaining choices are worth knowing but leave the "
                "plan's prospects unchanged either way.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([3, 4, 4]), "v_pc", self.sub)


GENS = [CauseWeaken(), CauseAssume(), SampleFlaw(), PercentFlaw(), NecessaryFlaw(),
        PlanAssume(), PlanWeaken(), PlanEvaluate()]
