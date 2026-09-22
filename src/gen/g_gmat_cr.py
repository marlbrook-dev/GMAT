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
from framework import Gen, ItemError, balance, check_clause_splice, upfirst

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
    dict(who="Hollis City Council", goal="reduce traffic on Bridge Street", goal_np="reducing traffic on Bridge Street",
         action="make parking on Bridge Street free after six in the evening",
         needs="the traffic on Bridge Street is mostly drivers circling in search of a space",
         fails="most of the traffic is through traffic with no intention of stopping",
         check="most of the traffic on Bridge Street stops there rather than passing through"),
    dict(who="Aldergate Hospital", goal="cut the number of missed appointments", goal_np="cutting the number of missed appointments",
         action="send every patient a reminder by text the day before",
         needs="patients miss appointments because they forget them",
         fails="most missed appointments are missed because patients cannot get there",
         check="patients who missed an appointment say they forgot it rather than could not reach it"),
    dict(who="Marden Publishing", goal="raise the number of manuscripts it reviews each month", goal_np="raising the number of manuscripts it reviews each month",
         action="hire two more editors",
         needs="reviewing is limited by how many editors are available",
         fails="manuscripts wait longest at the legal check, which the new editors do not do",
         check="manuscripts wait longest at the reviewing stage rather than at some later one"),
    dict(who="the Thorne Museum", goal="increase weekday attendance", goal_np="increasing weekday attendance",
         action="open two hours earlier on weekdays",
         needs="there are people who would visit on a weekday but cannot come at the current hours",
         fails="weekday visitors already arrive well after opening and leave before closing",
         check="there are people who would visit on a weekday but cannot come at the current hours"),
    dict(who="Bellwood Transit", goal="reduce the time buses spend at stops", goal_np="reducing the time buses spend at stops",
         action="require passengers to pay before boarding",
         needs="the time at a stop is mostly taken up by passengers paying as they board",
         fails="most of the time at a stop is taken by passengers finding seats after boarding",
         check="most of the time a bus spends at a stop is taken up by passengers paying as they board"),
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
    dict(who="Ferndale School", goal="raise the number of pupils walking to school", goal_np="raising the number of pupils walking to school",
         action="close the road outside the gates to cars at drop off time",
         needs="the pupils who are driven live close enough to walk",
         fails="most pupils who are driven live several miles away",
         check="the pupils who are driven live close enough to walk"),
    dict(who="Calloway Insurance", goal="shorten the time taken to settle a claim", goal_np="shortening the time taken to settle a claim",
         action="allow claims to be submitted through an app as well as by post",
         needs="the delay is in getting the claim to the assessor",
         fails="claims already reach the assessor within a day and wait weeks after that",
         check="the delay in settling a claim is in getting it to the assessor rather than after that"),
    dict(who="the Whitcombe Estate", goal="reduce water used on the gardens", goal_np="reducing water used on the gardens",
         action="water the beds at dawn rather than at midday",
         needs="a large share of the water applied at midday is lost to evaporation",
         fails="the beds are watered below the surface, where evaporation is negligible",
         check="a large share of the water applied at midday is lost before it "
               "reaches the roots"),
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
        # goal and action are stored as infinitive phrases for the stem; neither is a
        # clause, so neither may follow a sentence initial That or Whether (INC-0074).
        check_clause_splice(self.id, [stem] + opts + [expl],
                            [d["goal"] for d in PLAN] + [d["action"] for d in PLAN])
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
        right = upfirst(d["alt"]) + "."
        wrongs = [
            ("No other place in the region opened anything comparable in the same period.",
             "rules out a rival explanation elsewhere, which supports the conclusion rather "
             "than weakening it"),
            (upfirst(d["other"]) + ".",
             "reports something that happened at the same time but that could not affect "
             + d["effect"]),
            ("Officials had expected the change to take longer than it did.",
             "comments on how the result compared with expectations, which bears on nobody's "
             "forecasting rather than on the cause"),
            (upfirst(d["effect"]) + " has been measured the same way for twenty years.",
             "defends the measurement, which the argument was not being challenged on"),
            ("Some of the " + d["people"] + " said they welcomed " + d["short"] + ".",
             "reports approval, which is not the same as showing the change was caused by it"),
            ("The change was larger than officials in " + d["place"] + " had predicted.",
             "compares the result with a prediction, which bears on the forecast rather than "
             "on the cause"),
            ("Two comparable places recorded no change of the kind in the same period.",
             "reports the absence of the effect where the cause was also absent, which is "
             "evidence for the conclusion rather than against it"),
            (upfirst(d["short"]) + " cost less than had been budgeted.",
             "addresses cost, which the causal conclusion says nothing about"),
        ]
        expl = ("The conclusion moves from a correlation to a cause, so it is weakened by an "
                "alternative explanation for the same change. " + upfirst(d["alt"])
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
            (upfirst(d["short"]) + " was the least expensive of the measures available "
             "to " + d["place"] + " for producing a change of this kind.",
             "argues about cost, which the conclusion about cause does not rest on"),
            ("Every one of the " + d["people"] + " was aware that " + d["short"]
             + " had opened before the change in " + d["effect"] + " was recorded.",
             "demands universal awareness, which the argument never needs"),
            (upfirst(d["effect"]) + " will go on changing in the same direction for as "
             "long as " + d["short"] + " remains in place.",
             "predicts the future, while the conclusion is about what caused a change "
             "already observed"),
            ("Officials in " + d["place"] + " consulted those affected before deciding to "
             "open " + d["thing"] + ".",
             "concerns the process followed, not whether the cause claimed is the real one"),
            (upfirst(d["short"]) + " will remain in place for at least a decade, so "
             "that its effects can be measured over the long term.",
             "concerns how long the measure lasts, not whether it caused what has happened"),
            ("No measure comparable to " + d["short"] + " had been tried anywhere in "
             + d["place"] + " before this one was opened.",
             "asserts novelty, which the conclusion about cause does not rest on"),
            (upfirst(d["effect"]) + " had been stable for several years before "
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
        right = upfirst(d["gap"]) + " " + d["direction"] + "."
        wrongs = [
            (upfirst(d["gap"]) + " was unchanged over the same period.",
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
            # One short and two long. The key is the denominator sentence and every
            # distractor above sat within a few characters of it, so the key never came
            # out shortest and one rank held 49 percent of this schema's items
            # (INC-0079).
            ("The period was five years.",
             "restates the span the figures cover, which is in the argument already"),
            ("The share was reported to the nearest percentage point throughout the "
             "period, so a movement of less than a point would not have shown up in the "
             "figures at all.",
             "raises the precision of the reporting, which bears on how the share was "
             "measured rather than on the step from a share to a count"),
            ("A second body publishing its own figures for the same period recorded the "
             "same fall in the share, using a method it describes in detail and the "
             "commentator does not.",
             "corroborates the share, which is not the part of the argument in question"),
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
        right = upfirst(d["why"]) + "."
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
            # Short ones. The key is the one specific sentence and every distractor above
            # was a long generic one, so the key was the shortest option on 57 percent of
            # this schema's items (INC-0079).
            ("The group described is a small one.",
             "counts the cases, which does not bear on what they have in common"),
            ("The pattern has held for a decade.",
             "restates the evidence rather than testing the step taken from it"),
            ("No alternative has been proposed.",
             "notes that nobody has offered another account, which is not a reason to "
             "accept this one"),
            ("The advantage is expensive to obtain.",
             "reports a cost, which says nothing about who else has had it"),
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
            # goal_np, not goal: the field the stem uses is a bare infinitive and this
            # slot is a subject (INC-0074).
            ("That " + d["who"] + " has no goal more urgent than " + d["goal_np"] + ".",
             "ranks the goal against other goals, which the plan's success does not "
             "turn on"),
            ("That no other body has objected to the measure.",
             "raises opposition, which bears on whether the measure happens rather than on "
             "whether it works"),
            ("That the measure can be reversed if it does not work.",
             "concerns what happens afterwards, not whether the effect follows"),
            ("That " + d["who"] + " has tried to " + d["goal"] + " before.",
             "asks about history, which the plan's prospects do not depend on"),
            # One short and one long, for the same reason as the schemas beside it: with
            # every distractor written at about the key's length, one rank held 42 percent
            # of this schema's 1,077 items (INC-0079).
            ("That the measure is lawful.",
             "asks whether the measure may be taken, not whether taking it would work"),
            ("That the people the measure is aimed at will notice that it has been taken, "
             "and will understand what it is for well enough to change what they do in "
             "response to it.",
             "supposes a further condition about awareness, which the plan does not need: "
             "the action is claimed to work by removing the constraint, not by persuading "
             "anyone"),
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
        right = upfirst(d["fails"]) + "."
        wrongs = [
            (upfirst(d["needs"]) + ".",
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
            # Long ones, for the same reason the evaluate schema needed short ones: the
            # key is the one specific sentence and every distractor above is a short
            # generic one, which made the key the longest option on 65 percent of this
            # schema's items (INC-0079).
            ("A comparable body in another region carried out a measure of the same kind "
             "and reported no change in the first two years, though it did not publish "
             "the figures it relied on.",
             "reports an outcome elsewhere without saying whether the conditions were the "
             "same, which does not bear on this case"),
            ("The measure was recommended by an adviser whose earlier proposals for "
             + d["who"] + " were adopted and then reversed within a year of being put in "
             "place.", "attacks the source of the recommendation rather than the "
             "reasoning behind it"),
            ("Several of those affected have said that they would have preferred "
             + d["who"] + " to spend the same money on something else entirely, and have "
             "written to say so.",
             "reports a preference about priorities, which does not show the measure "
             "ineffective"),
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
        # "Whether " plus a clause, not plus a wh clause with a tail bolted on (INC-0075).
        right = "Whether " + d["check"] + "."
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
            # Short ones. Every distractor above is a long generic question and the key is
            # a short specific one, which made the key the shortest option on 98 percent
            # of this schema's items (INC-0079). These are the same kind of wrong answer,
            # written at the length a real one would be.
            ("Whether the measure has been costed.", "asks about cost rather than effect"),
            ("Whether the measure is popular.", "asks about reception rather than effect"),
            ("Whether the measure is reversible.",
             "asks what happens afterwards rather than whether the effect follows"),
            ("Whether anyone else has tried it.",
             "asks for precedent, which does not test this case"),
            ("Whether " + d["who"] + " can afford it.",
             "tests affordability rather than effect"),
        ]
        expl = ("A question is useful for evaluating a plan when the two possible answers "
                "point in opposite directions. Establish whether " + d["check"]
                + ", and one answer means the measure addresses the cause while the other "
                "means it does not. The remaining choices are worth knowing but leave the "
                "plan's prospects unchanged either way.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([3, 4, 4]), "v_pc", self.sub)


GENS = [CauseWeaken(), CauseAssume(), SampleFlaw(), PercentFlaw(), NecessaryFlaw(),
        PlanAssume(), PlanWeaken(), PlanEvaluate()]


# v_pc shipped 833 items of a 3300 target off eight scenarios, so most of those items
# were the same three arguments with a different subset of wrong answers. A scenario
# multiplies all three plan schemas, so this is where the category was actually short.
# Each one is a bottleneck misidentification: the action addresses one cause, the plan
# needs that to be the cause, and it fails if the real constraint sits elsewhere.
#
# Every entry carries goal as a bare infinitive AND goal_np as a noun phrase, because
# the templates need both and a field carries no record of which shape it is in
# (INC-0074). check reads after "Whether" (INC-0075).
PLAN += [
    dict(who="Restwick Harbour Authority", goal="shorten the time cargo waits on the quay",
         goal_np="shortening the time cargo waits on the quay",
         action="add two more cranes",
         needs="unloading is what holds cargo on the quay",
         fails="cargo is unloaded within hours and then waits for customs clearance",
         check="cargo spends longer being unloaded than waiting for customs clearance"),
    dict(who="Larkfield Utilities", goal="reduce the number of calls its helpline receives",
         goal_np="reducing the number of calls its helpline receives",
         action="publish a page of answers to common questions on its website",
         needs="callers ring because they cannot find the answer themselves",
         fails="most callers ring because the answer they found did not fit their account",
         check="callers ring because they could not find an answer rather than because the "
               "answer did not fit"),
    dict(who="Marchmont Stores", goal="shorten the queues at its checkouts",
         goal_np="shortening the queues at its checkouts",
         action="install four self service tills",
         needs="the queues form because there are too few tills",
         fails="the queues form at the one hour when too few staff are on to open the "
               "tills already installed",
         check="the existing tills are all staffed at the times when the queues are longest"),
    dict(who="Ledbury Borough Council",
         goal="raise the share of household waste that is recycled",
         goal_np="raising the share of household waste that is recycled",
         action="give every household a larger recycling bin",
         needs="households recycle less than they would because their bins fill up",
         fails="most households put out bins that are less than half full",
         check="the recycling bins households put out are usually full"),
    dict(who="Ashcombe Farm", goal="increase the yield of its apple orchard",
         goal_np="increasing the yield of its apple orchard",
         action="place twice as many hives at the orchard edge",
         needs="the crop is limited by how much of the blossom is pollinated",
         fails="the blossom is already fully pollinated and the crop is limited by water "
               "in late summer",
         check="a meaningful share of the blossom currently goes unpollinated"),
    dict(who="Tallis Systems", goal="cut the number of support tickets it reopens",
         goal_np="cutting the number of support tickets it reopens",
         action="require every engineer to write a summary before closing a ticket",
         needs="tickets are reopened because the fix was recorded unclearly",
         fails="tickets are reopened because the underlying fault recurs whatever is "
               "written down",
         check="reopened tickets describe a fault that had been fixed rather than one "
               "that came back"),
    dict(who="the Brackenbury Theatre", goal="fill more seats at its weekday performances",
         goal_np="filling more seats at its weekday performances",
         action="cut the price of a weekday ticket by a third",
         needs="the people who stay away on weekdays are put off by the price",
         fails="weekday audiences are limited by how few people can reach the theatre "
               "before the curtain",
         check="the people who stay away on weekdays are kept away by the price"),
    dict(who="Hallamshire Veterinary Practice",
         goal="reduce the number of animals brought in with advanced illness",
         goal_np="reducing the number of animals brought in with advanced illness",
         action="offer a free annual examination to every registered animal",
         needs="illness goes undetected because animals are not examined often enough",
         fails="the illnesses that arrive late are ones a routine examination does not reveal",
         check="the illnesses that arrive late are detectable at a routine examination"),
    dict(who="the Denholme Estate", goal="raise the survival rate of the saplings it plants",
         goal_np="raising the survival rate of the saplings it plants",
         action="plant in autumn rather than in spring",
         needs="the saplings that die are lost to drought in their first summer",
         fails="most losses are to deer browsing, which the planting season does not affect",
         check="the saplings that die are lost to drought rather than to browsing"),
    dict(who="Kirkhaven Post", goal="reduce the number of parcels returned as undelivered",
         goal_np="reducing the number of parcels returned as undelivered",
         action="text each recipient on the morning of delivery",
         needs="parcels are returned because nobody is at home when the van calls",
         fails="most returns are caused by addresses written incompletely at the point of sale",
         check="returned parcels were addressed correctly in the first place"),
    dict(who="Ravensworth Leisure Centre", goal="raise the number of members who renew",
         goal_np="raising the number of members who renew",
         action="extend its opening hours into the late evening",
         needs="the members who leave cannot get to the centre while it is open",
         fails="the members who leave say the equipment they came for is always in use",
         check="the members who do not renew were kept away by the opening hours"),
    dict(who="Wrenfield Bakery", goal="cut the amount of bread it throws away each day",
         goal_np="cutting the amount of bread it throws away each day",
         action="bake a second, smaller batch in the afternoon",
         needs="the waste is bread baked in the morning that does not sell by closing",
         fails="the waste is bread returned unsold by the shops it supplies, which order "
               "in the morning",
         check="the bread thrown away is bread left in the shop rather than bread "
               "returned by other shops"),
    dict(who="Cleveley Rail", goal="improve the punctuality of its evening services",
         goal_np="improving the punctuality of its evening services",
         action="add three minutes to the timetable at each of the two busiest stations",
         needs="the delay accumulates while trains stand at those two stations",
         fails="evening trains leave the depot late and lose no further time on the route",
         check="evening trains are on time when they reach the two busiest stations"),
    dict(who="the Corbridge Museum shop", goal="raise the value of the average sale",
         goal_np="raising the value of the average sale",
         action="move the higher priced items to the counter",
         needs="visitors buy what they happen to see on the way out",
         fails="most purchases are decided before a visitor enters the shop",
         check="visitors decide what to buy after entering the shop rather than before"),
    dict(who="the Ardley University Library",
         goal="reduce the number of books returned late",
         goal_np="reducing the number of books returned late",
         action="double the fine charged for a late return",
         needs="books are kept late by readers who are choosing to accept the fine",
         fails="most late returns are by readers who have forgotten the due date",
         check="readers who return a book late were aware it was due"),
    dict(who="the Salterton Inn", goal="shorten the wait between ordering and serving",
         goal_np="shortening the wait between ordering and serving",
         action="take on a second chef",
         needs="the wait is created in the kitchen",
         fails="orders reach the kitchen late because one server covers every table",
         check="an order spends longer in the kitchen than it does waiting to reach it"),
    dict(who="Penhale Water", goal="reduce the volume of water lost from its network",
         goal_np="reducing the volume of water lost from its network",
         action="replace the oldest mile of pipe in each district",
         needs="most of the loss is from the oldest pipe",
         fails="most of the loss is from joints and fittings of every age",
         check="the oldest pipe accounts for most of the water lost"),
    dict(who="the Nettleford Trust",
         goal="increase the number of volunteers who stay past a year",
         goal_np="increasing the number of volunteers who stay past a year",
         action="offer every volunteer a training course in their first month",
         needs="volunteers leave because they feel unprepared for the work",
         fails="volunteers leave because the shifts they are offered do not fit around "
               "their jobs",
         check="volunteers who leave felt unprepared rather than badly scheduled"),
    dict(who="Caldbeck Airport", goal="reduce the time passengers spend at security",
         goal_np="reducing the time passengers spend at security",
         action="open two more scanning lanes",
         needs="the queue at security is limited by how many lanes are open",
         fails="the queue is limited by how many staff are trained to run a lane, and no "
               "more are",
         check="there are staff available to run more lanes than are currently open"),
    dict(who="Ryedale Housing", goal="cut the time an empty flat stays empty",
         goal_np="cutting the time an empty flat stays empty",
         action="redecorate every flat as soon as it is vacated",
         needs="flats stand empty while they are being made ready",
         fails="flats are ready within a week and then wait for an applicant to be approved",
         check="an empty flat spends longer being made ready than waiting for an approved "
               "applicant"),
    dict(who="Oakhanger Tools",
         goal="raise the number of finished tools it ships each week",
         goal_np="raising the number of finished tools it ships each week",
         action="run the grinding shop for an extra shift",
         needs="output is limited by grinding capacity",
         fails="output is limited by the supply of castings, which an extra grinding "
               "shift does not increase",
         check="grinding is the stage at which unfinished work accumulates"),
    dict(who="Thurlby School", goal="increase the number of pupils taking a hot lunch",
         goal_np="increasing the number of pupils taking a hot lunch",
         action="add three new dishes to the menu",
         needs="pupils avoid the hot lunch because the choice is too narrow",
         fails="pupils avoid it because the lunch break is too short to queue and eat",
         check="the pupils who do not take a hot lunch are put off by the choice"),
    dict(who="Barrowfield Energy", goal="reduce the heat lost from its district network",
         goal_np="reducing the heat lost from its district network",
         action="insulate the pipes running between buildings",
         needs="most of the loss happens in the pipes between buildings",
         fails="most of the loss happens inside the buildings, at the heat exchangers",
         check="more heat is lost between the buildings than inside them"),
    dict(who="Oakmere Coaches", goal="reduce the fuel its fleet uses",
         goal_np="reducing the fuel its fleet uses",
         action="fit every coach with a device that limits its top speed",
         needs="the fuel is used mainly on long stretches at high speed",
         fails="the fleet runs almost entirely on town routes where the limit is never reached",
         check="the fleet runs a meaningful share of its mileage above the speed the "
               "device would impose"),
]


# v_ac shipped 1422 items of a 3300 target off eighteen scenarios across four corpora.
# Same reasoning as the PLAN block above: a scenario multiplies every schema that draws
# on it, and CAUSE feeds two.
CAUSE += [
    dict(place="Harlow Green", thing="a weekend park and ride service",
         effect="the number of cars parked in the town centre", rose="fell by a fifth",
         alt="a large employer in the town centre moved to an out of town site that year",
         alt_short="a town centre employer moved out that year",
         short="the park and ride", people="shopkeepers in Harlow Green",
         other="the town centre gained a new pedestrian crossing that autumn"),
    dict(place="Sedgley College", thing="a drop in mathematics clinic",
         effect="the pass rate in first year mathematics", rose="rose by twelve points",
         alt="the college raised its entry requirement for the course in the same year",
         alt_short="the entry requirement rose in the same year",
         short="the clinic", people="students at Sedgley College",
         other="the college repainted the mathematics building that summer"),
    dict(place="Ravenstone", thing="a set of cycle racks outside every shop",
         effect="the number of bicycles counted on the high street", rose="rose by half",
         alt="the bus service through Ravenstone was cut to two journeys a day that spring",
         alt_short="the bus service was cut that spring",
         short="the cycle racks", people="traders in Ravenstone",
         other="the high street was resurfaced the following year"),
    dict(place="the Ashford Clinic", thing="an online booking system",
         effect="the number of appointments left unfilled each week", rose="fell by a third",
         alt="the clinic took on two more doctors in the same month",
         alt_short="two more doctors joined in the same month",
         short="the booking system", people="patients at the Ashford Clinic",
         other="the clinic changed its telephone number that year"),
    dict(place="Cranbourne Prison", thing="a reading programme",
         effect="the share of released prisoners reconvicted within two years",
         rose="fell by a quarter",
         alt="the prison began releasing prisoners into a new housing scheme in the same period",
         alt_short="a new housing scheme began in the same period",
         short="the reading programme", people="staff at Cranbourne Prison",
         other="the prison replaced its kitchen that winter"),
    dict(place="Bramfield", thing="a farmers market on Saturday mornings",
         effect="the takings of the shops on the square", rose="rose by a fifth",
         alt="a supermarket two streets away closed in the same month",
         alt_short="a nearby supermarket closed in the same month",
         short="the market", people="shopkeepers in Bramfield",
         other="the square was fitted with new lighting that autumn"),
    dict(place="the Ellerby Works", thing="a training scheme for new machinists",
         effect="the number of parts rejected at inspection", rose="fell by two fifths",
         alt="the works replaced its oldest lathe in the same quarter",
         alt_short="the oldest lathe was replaced in the same quarter",
         short="the training scheme", people="machinists at the Ellerby Works",
         other="the works changed its inspection shift pattern that year"),
    dict(place="Holbeck Library", thing="a homework space for teenagers",
         effect="the number of teenagers holding a library card", rose="rose by a third",
         alt="a youth centre two streets away closed in the same term",
         alt_short="a nearby youth centre closed in the same term",
         short="the homework space", people="families in Holbeck",
         other="the library began stocking a new magazine that year"),
    dict(place="Denby Vale", thing="a free flu clinic at the village hall",
         effect="the working days lost to illness at the village's largest employer",
         rose="fell by a sixth",
         alt="the employer introduced home working in the same winter",
         alt_short="home working began in the same winter",
         short="the flu clinic", people="residents of Denby Vale",
         other="the village hall was re-roofed that spring"),
    dict(place="Marsden Docks", thing="a night shift at the container gate",
         effect="the average time a lorry spends waiting at the gate",
         rose="fell by 25 minutes",
         alt="a second container terminal opened along the coast and took a share of the traffic",
         alt_short="a second terminal opened and took some of the traffic",
         short="the night shift", people="drivers using Marsden Docks",
         other="the docks repainted their gate signs that year"),
    dict(place="Alderholt", thing="a set of traffic islands on its residential streets",
         effect="the number of collisions recorded on those streets", rose="fell by a third",
         alt="the through route was diverted away from the village in the same year",
         alt_short="the through route was diverted in the same year",
         short="the traffic islands", people="residents of Alderholt",
         other="the village renamed two of its streets that year"),
    dict(place="Whitstone Hospital", thing="a discharge lounge",
         effect="the average length of a stay on the medical wards",
         rose="fell by half a day",
         alt="a community rehabilitation unit opened nearby in the same period",
         alt_short="a rehabilitation unit opened nearby in the same period",
         short="the discharge lounge", people="staff at Whitstone Hospital",
         other="the hospital replaced its bed linen supplier that year"),
    dict(place="Netherby", thing="a community orchard on the old allotments",
         effect="the number of households joining the gardening society",
         rose="rose by two thirds",
         alt="the society halved its membership fee in the same year",
         alt_short="the membership fee was halved in the same year",
         short="the orchard", people="residents of Netherby",
         other="the society changed the night of its monthly meeting"),
    dict(place="Tarnbrook", thing="a second recycling point at the top of the village",
         effect="the weight of glass collected for recycling", rose="rose by a third",
         alt="a bottle deposit scheme began across the county in the same month",
         alt_short="a county deposit scheme began in the same month",
         short="the recycling point", people="residents of Tarnbrook",
         other="the village replaced its street nameplates that year"),
]

SAMPLE += [
    dict(who="people who replied to a questionnaire printed in the local paper",
         pop="residents of the town",
         claim="most residents want the market moved to the square",
         why="the people who reply to a printed questionnaire are the ones who already "
             "read the paper closely",
         topic="the market"),
    dict(who="listeners who telephoned the programme", pop="the station's listeners",
         claim="listeners are opposed to the new timetable",
         why="telephoning a programme takes an effort that only those with strong views make",
         topic="the timetable"),
    dict(who="members of the ramblers association", pop="users of the footpath",
         claim="users would accept a longer route around the field",
         why="members of a ramblers association walk further by choice than other users "
             "of a footpath",
         topic="the length of the route"),
    dict(who="passengers travelling on the eight o'clock service", pop="the line's passengers",
         claim="passengers would pay more for a faster journey",
         why="the eight o'clock service carries people travelling to work, who value "
             "speed more than other passengers do",
         topic="journey time"),
    dict(who="patients who kept their follow up appointment",
         pop="patients treated at the clinic",
         claim="patients are satisfied with the treatment",
         why="the patients who were dissatisfied are the ones least likely to come back",
         topic="satisfaction"),
    dict(who="staff who filled in the survey during working hours",
         pop="the department's staff",
         claim="staff have time for an additional weekly meeting",
         why="the staff with least to do are the ones who had time to fill in a survey at work",
         topic="how much time staff have"),
    dict(who="households that agreed to have a meter fitted",
         pop="households in the district",
         claim="households in the district use less water than the regional average",
         why="a household that volunteers for a meter usually expects to benefit from one",
         topic="water use"),
    dict(who="visitors who stayed to the end of the tour", pop="visitors to the house",
         claim="visitors find the whole tour interesting",
         why="the visitors who were losing interest had already left before the end",
         topic="how interesting the tour is"),
    dict(who="teachers who attended the optional conference",
         pop="teachers in the authority",
         claim="teachers welcome the new curriculum",
         why="a teacher who gives up a Saturday for a conference on the curriculum is "
             "already engaged with it",
         topic="the curriculum"),
    dict(who="drivers who renewed with the same insurer", pop="the insurer's customers",
         claim="customers consider the price fair",
         why="the customers who thought the price unfair had already gone elsewhere",
         topic="the price"),
    dict(who="shoppers interviewed at the entrance to the new car park",
         pop="shoppers in the town",
         claim="shoppers prefer to drive into town",
         why="everyone interviewed had just arrived by car",
         topic="how shoppers travel"),
]

PERCENT += [
    dict(subject="the share of library loans that were audiobooks",
         share="fell from 22 percent to 15 percent",
         conclude="fewer audiobooks are being borrowed than before",
         gap="the total number of loans", direction="more than doubled over the same period",
         unit="loans"),
    dict(subject="the proportion of the hospital's admissions that were emergencies",
         share="fell from 40 percent to 30 percent",
         conclude="the hospital is admitting fewer emergencies",
         gap="the total number of admissions",
         direction="rose by three quarters over the same period", unit="admissions"),
    dict(subject="the share of the company's sales made in its home market",
         share="fell from 60 percent to 45 percent",
         conclude="the company is selling less at home",
         gap="the company's total sales", direction="nearly doubled over the same period",
         unit="units"),
    dict(subject="the proportion of journeys in the county made by bus",
         share="fell from 30 percent to 24 percent",
         conclude="fewer journeys in the county are being made by bus",
         gap="the total number of journeys made",
         direction="rose by half over the same period", unit="journeys"),
    dict(subject="the share of planning applications that were refused",
         share="fell from 16 percent to 11 percent",
         conclude="the council is refusing fewer applications",
         gap="the number of applications submitted",
         direction="rose by four fifths over the same period", unit="applications"),
    dict(subject="the proportion of the museum's visitors who were children",
         share="fell from 35 percent to 28 percent",
         conclude="fewer children are visiting the museum",
         gap="the total number of visitors",
         direction="rose by two thirds over the same period", unit="children"),
    dict(subject="the share of the farm's land sown with barley",
         share="fell from 45 percent to 33 percent",
         conclude="the farm is growing less barley",
         gap="the area the farm has under cultivation",
         direction="doubled over the same period", unit="hectares"),
    dict(subject="the share of orders that were returned",
         share="fell from 12 percent to 9 percent",
         conclude="fewer orders are being returned",
         gap="the total number of orders",
         direction="more than tripled over the same period", unit="orders"),
    dict(subject="the proportion of the town's households without a car",
         share="fell from 28 percent to 21 percent",
         conclude="fewer households in the town are without a car",
         gap="the number of households in the town",
         direction="rose by two fifths over the same period", unit="households"),
    dict(subject="the share of the charity's income that came from legacies",
         share="fell from 34 percent to 25 percent",
         conclude="the charity is receiving less in legacies",
         gap="the charity's total income",
         direction="rose by four fifths over the same period", unit="pounds"),
]

NECESSARY += [
    dict(common="used the practice rooms in the basement",
         group="each of the students who won a place at the conservatoire",
         conclude="the basement practice rooms are what prepare a student for the audition",
         why="the basement rooms are the only ones in the building, so every student uses "
             "them whether they win a place or not"),
    dict(common="were fitted with the workshop's own bearings",
         group="all nine of the machines that ran for a decade without failing",
         conclude="the workshop's bearings are what give a machine its working life",
         why="the workshop fits its own bearings to every machine it builds, including "
             "the ones that failed early"),
    dict(common="had been treated with the nursery's standard rooting compound",
         group="every cutting that took root",
         conclude="the rooting compound is what makes a cutting take",
         why="the nursery treats every cutting with the compound, including the great "
             "many that fail to take"),
    dict(common="submitted their application through the online portal",
         group="each of the twelve candidates offered a place",
         conclude="applying through the portal is what secures an offer",
         why="the portal is the only way to apply, so every unsuccessful candidate used "
             "it as well"),
    dict(common="had read the department's style guide",
         group="every paper the journal accepted last year",
         conclude="reading the style guide is what gets a paper accepted",
         why="the guide is sent to every author on submission, including the authors of "
             "the papers that were rejected"),
    dict(common="trained on the club's indoor pitch over the winter",
         group="all of the players promoted to the first team",
         conclude="winter training on the indoor pitch is what earns promotion",
         why="the whole squad trains on the indoor pitch in winter, including the players "
             "who were not promoted"),
    dict(common="were stored in the cold room before firing",
         group="every one of the pots that survived the kiln",
         conclude="storing a pot in the cold room is what carries it through the firing",
         why="the studio stores every pot in the cold room, including those that cracked "
             "in the kiln"),
    dict(common="had attended the induction week",
         group="each of the apprentices who completed the four year programme",
         conclude="the induction week is what carries an apprentice through to the end",
         why="induction week is compulsory, so the apprentices who left early had "
             "attended it too"),
    dict(common="were grown from seed saved on the farm",
         group="all of the varieties that yielded well in the dry summer",
         conclude="seed saved on the farm is what makes a variety drought tolerant",
         why="the farm grows everything from its own saved seed, including the varieties "
             "that failed in the dry summer"),
]
