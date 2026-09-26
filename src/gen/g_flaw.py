"""Named reasoning flaws, for the categories that ask what is wrong with an argument.

Written because lsat_lr_flaw could not be generated honestly from one schema. g_gmat_cr
has exactly one flaw schema, cr_sample, so every generated flaw item would have been an
unrepresentative sample, and a category whose published description promises the common
patterns of bad reasoning and delivers one of them teaches the wrong model of the
category. Three more patterns, each one a flaw LSAC and GMAC both name.

Same construction as g_gmat_cr, which is where CRBase lives: the draw records the
structure of the argument, and the correct answer is the description of the gap that
structure creates rather than a judgement made by taste. Each schema offers more named
wrong answers than an item has slots, so two items from one schema differ in what the
student has to rule out and not only in the letters.

  necsuff     a requirement is treated as a guarantee. The gap is the direction of the
              conditional, and the distractors include the converse stated as if it were
              the flaw, which is the error read back as a description of itself.
  partwhole   what holds of each part is concluded of the whole, or the reverse. The gap
              is whichever direction the draw took.
  authority   a claim is accepted or rejected on the strength of its source. The draw
              records why the source does not settle it: wrong field, an interest in the
              answer, or a consensus that is not evidence.
"""
from framework import plural_head, upfirst
from g_gmat_cr import CRBase

# --- necessary confused with sufficient ---------------------------------------------
# req: what is required. goal and goal_ing: what it is required for, written in both
# grammatical shapes because the stem needs the bare infinitive after "may" and the
# answer needs the gerund after "required for". Both written out rather than one
# derived from the other: the derivation is where the assumption hides (INC-0087).
# who: the case in hand.
NECSUFF = [
    dict(req="a licence from the board", goal="practise as a surveyor", goal_ing="practising as a surveyor",
         who="Aurelio", extra="has held a licence since 2019",
         also="the board licenses applicants who have passed the written examination, "
              "whether or not they have completed the supervised year"),
    dict(req="a deposit of two months' rent", goal="take a tenancy in the building", goal_ing="taking a tenancy in the building",
         who="the Navarro household", extra="has paid the deposit",
         also="the landlord also requires a reference from a previous tenancy"),
    dict(req="a pass in the entrance paper", goal="be admitted to the conservatoire", goal_ing="being admitted to the conservatoire",
         who="Wen", extra="passed the paper in the spring sitting",
         also="the panel admits only those it also hears audition in person"),
    dict(req="membership of the union", goal="work on the harbour crew", goal_ing="working on the harbour crew",
         who="Petrov", extra="joined the union last year",
         also="the crew is allocated by seniority among members"),
    dict(req="planning consent", goal="build on the meadow", goal_ing="building on the meadow",
         who="the trust", extra="obtained consent in March",
         also="building also requires the agreement of the commoners"),
    dict(req="a doctorate", goal="hold a chair in the faculty", goal_ing="holding a chair in the faculty",
         who="Okonkwo", extra="completed a doctorate at Leeds",
         also="chairs are filled by open competition among many who hold one"),
    dict(req="a signed release from the copyright holder", goal="reissue the recording", goal_ing="reissuing the recording",
         who="the label", extra="has the signed release",
         also="the performers' own consents are separately required"),
    dict(req="residence in the parish for a year", goal="vote in the vestry election", goal_ing="voting in the vestry election",
         who="Halloran", extra="has lived in the parish for three years",
         also="the roll is closed to anyone who has not registered by Michaelmas"),
    dict(req="a negative soil test", goal="certify the field as organic", goal_ing="certifying the field as organic",
         who="the Pryce farm", extra="returned a negative test",
         also="certification also requires three years without prohibited inputs"),
    dict(req="an invitation from a fellow", goal="dine at high table", goal_ing="dining at high table",
         who="Sandoval", extra="was invited by a fellow",
         also="the steward admits guests only when a place remains after the fellows sit"),
    dict(req="a rating above 1800", goal="enter the master section", goal_ing="entering the master section",
         who="Ferreira", extra="is rated 1930",
         also="the section is capped at sixty and fills by order of application"),
    dict(req="a second independent review", goal="publish in the journal", goal_ing="publishing in the journal",
         who="the Meier paper", extra="has a second independent review",
         also="the editor publishes only what the board then also approves"),
    dict(req="a permit from the harbour master", goal="moor overnight in the basin", goal_ing="mooring overnight in the basin",
         who="the Caldera", extra="holds a permit",
         also="the basin is allocated by draught, and deep hulled boats are turned away"),
    dict(req="a clean inspection report", goal="reopen the kitchen", goal_ing="reopening the kitchen",
         who="the Dunmore Arms", extra="has a clean report",
         also="the licence must also be restored by the council before service resumes"),
    dict(req="two sponsors already in the society", goal="stand for election to it", goal_ing="standing for election to it",
         who="Brannigan", extra="has two sponsors",
         also="nominations close a month before the ballot and Brannigan has not filed"),
    dict(req="a grade of distinction in the practical", goal="be entered for the diploma", goal_ing="being entered for the diploma",
         who="Achebe", extra="was graded distinction",
         also="the school enters only candidates who have also completed the portfolio"),
    dict(req="proof of continuous cover", goal="claim under the policy", goal_ing="claiming under the policy",
         who="the Rossi claim", extra="is supported by proof of cover",
         also="the insurer also requires the loss to fall inside the listed perils"),
    dict(req="a survey of the roof", goal="release the second tranche of the grant", goal_ing="releasing the second tranche of the grant",
         who="the chapel", extra="has had the roof surveyed",
         also="the trustees release funds only against invoices already paid"),
]


class NecSuff(CRBase):
    """A condition required for something is treated as one that produces it."""
    id = "cr_necsuff"
    skill = "v_ac"
    sub = "Identify the flaw"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(NECSUFF)
        stem = ("No one may " + d["goal"] + " without " + d["req"] + ". " + upfirst(d["who"])
                + " " + d["extra"] + ", so " + d["who"] + " may " + d["goal"]
                + ".\n\nThe reasoning above is most vulnerable to criticism on the grounds "
                "that it:")
        right = ("treats a condition that is required for " + d["goal_ing"]
                 + " as though meeting it were enough on its own")
        wrongs = [
            ("treats a condition that is enough for " + d["goal_ing"]
             + " as though it were also required",
             "describes the opposite confusion, which is the same error read backwards"),
            ("assumes without warrant that " + d["req"] + " cannot be withdrawn once granted",
             "raises a possibility about revocation, which the argument never relies on"),
            ("offers no evidence that " + d["who"] + " wishes to " + d["goal"],
             "objects that the conclusion is unmotivated, when the question is whether it "
             "follows"),
            ("relies on a rule stated in the negative rather than establishing the "
             "positive case directly",
             "objects to the phrasing of the rule, which is a matter of form and not of "
             "reasoning"),
            ("takes for granted that the rule applies to " + d["who"]
             + " in the same way it applies to anyone else",
             "raises an exemption the argument does not depend on, since the rule is given "
             "as general"),
            ("fails to consider whether " + d["req"]
             + " was obtained by a means the rule would not recognise",
             "questions the provenance of the condition rather than the step from it"),
            ("concludes that a permission exists from the mere absence of a prohibition",
             "names a different move, and a prohibition is exactly what the rule states"),
            ("draws a conclusion about a single case from a rule stated about a class",
             "objects to applying a general rule to an instance, which is what rules are for"),
            ("assumes that because a rule has been stated in one form it cannot also be "
             "subject to further conditions that the statement of it leaves unmentioned",
             "describes the very thing the argument overlooks as though the argument had "
             "asserted it, which reverses the criticism"),
            ("treats the satisfaction of a published requirement as though it removed the "
             "discretion of the people who administer the rule in individual cases",
             "raises discretion, which is one way the conclusion could fail but not the "
             "step the argument actually takes"),
            ("infers from the fact that one obstacle has been cleared that no further "
             "obstacle of any kind now stands between the case and the outcome sought",
             "comes close, and still describes an inference about obstacles in general "
             "rather than the confusion of a requirement with a guarantee"),
            ("supposes that the authority which set the requirement is also the authority "
             "that decides whether it has been met in any particular instance",
             "raises a question about who decides, which the argument neither asserts nor "
             "needs"),
        ]
        expl = ("The rule says that " + d["req"] + " is needed, not that it suffices. In "
                "fact " + d["also"] + ". A requirement rules people out; it does not let "
                "anyone in.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([2, 3, 3, 4]), "v_ac", self.sub)


# --- part and whole ------------------------------------------------------------------
# up=True means the argument runs from the parts to the whole.
PARTWHOLE = [
    dict(part="every player in the squad", whole="the squad", prop="quick over ten metres",
         why="a team can be slow to move the ball however quick its individuals are", up=True),
    dict(part="each department", whole="the company", prop="within its budget",
         why="costs shared between departments appear in none of their budgets", up=True),
    dict(part="every ingredient", whole="the dish", prop="wholesome on its own",
         why="a combination can be unwholesome when each part is not", up=True),
    dict(part="each movement", whole="the symphony", prop="brief",
         why="four brief movements make a work of ordinary length", up=True),
    dict(part="every clause", whole="the contract", prop="plainly worded",
         why="clauses that are clear separately can contradict one another", up=True),
    dict(part="each of the firm's funds", whole="the firm's portfolio", prop="diversified",
         why="funds diversified in the same way concentrate the same risk", up=True),
    dict(part="the orchestra", whole="each of its players", prop="internationally known",
         why="an ensemble can be famous while its members are not", up=False),
    dict(part="the collection", whole="each item in it", prop="valuable",
         why="the value can lie in the collection being complete", up=False),
    dict(part="the machine", whole="each of its components", prop="expensive",
         why="assembly and calibration can account for most of the price", up=False),
    dict(part="the report", whole="each chapter of it", prop="influential",
         why="influence can rest on one chapter that the rest merely supports", up=False),
    dict(part="every witness", whole="the testimony taken together", prop="consistent",
         why="two accounts can each be internally consistent and contradict each other", up=True),
    dict(part="each brick", whole="the wall", prop="light enough to lift",
         why="a property of a single unit says nothing about the assembly", up=True),
    dict(part="every chapter", whole="the argument of the book", prop="well supported",
         why="the chapters can each be sound and still not add up to the thesis", up=True),
    dict(part="each grant", whole="the funding programme", prop="modest in cost",
         why="a programme of many modest grants is not itself modest", up=True),
    dict(part="the choir", whole="each of its singers", prop="capable of the high part",
         why="an ensemble reaches notes that most of its members cannot", up=False),
    dict(part="the archive", whole="each document in it", prop="rare",
         why="rarity can belong to the assembly rather than to any single item", up=False),
]


class PartWhole(CRBase):
    """What holds of the parts is concluded of the whole, or the reverse."""
    id = "cr_partwhole"
    skill = "v_ac"
    sub = "Identify the flaw"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(PARTWHOLE)
        if d["up"]:
            stem = (upfirst(d["part"]) + " is " + d["prop"] + ". It follows that "
                    + d["whole"] + " is " + d["prop"] + " too.")
            right = ("assumes that what is true of each member of a group must be true of "
                     "the group taken together")
            first_wrong = ("assumes that what is true of a group must be true of each of "
                           "its members")
            first_why = ("describes the opposite move, which is the same error in the other "
                         "direction")
        else:
            stem = (upfirst(d["part"]) + " is " + d["prop"] + ". It follows that "
                    + d["whole"] + " is " + d["prop"] + " too.")
            right = ("assumes that what is true of a group taken together must be true of "
                     "each of its members")
            first_wrong = ("assumes that what is true of each member of a group must be "
                           "true of the group")
            first_why = ("describes the opposite move, which is the same error in the other "
                         "direction")
        stem += ("\n\nThe reasoning above is most vulnerable to criticism on the grounds "
                 "that it:")
        wrongs = [
            (first_wrong, first_why),
            ("takes a term to mean the same thing in the premise and the conclusion when "
             "it does not",
             "names equivocation, and the term here keeps one meaning throughout"),
            ("offers no evidence for the premise it begins from",
             "asks for support for a claim the argument is entitled to assume"),
            ("relies on a comparison with a case that differs in a relevant respect",
             "names a faulty analogy, and no comparison is drawn here"),
            ("presumes what it sets out to establish",
             "names circularity, and the premise here is not the conclusion restated"),
            ("infers that a property must have a single cause from the fact that it is "
             "widely shared",
             "names a causal move the argument does not make"),
            ("treats a matter of degree as though it were a matter of kind",
             "names a real failing, which this argument does not commit"),
            ("generalises from a number of cases too small to support the conclusion",
             "asks about sample size, when every member is covered by the premise"),
            ("treats evidence about how a group performs when acting collectively as "
             "though it settled a question about the capacities of its individual members",
             "describes one direction of the part and whole move in terms of performance, "
             "which is not the property this argument carries across"),
            ("relies on a generalisation drawn from cases that were selected precisely "
             "because they already exhibited the property the conclusion attributes",
             "names a selection effect, and the premise here covers every case rather than "
             "a chosen few"),
            ("assumes that a property which admits of degrees can be attributed without "
             "qualification to anything that possesses it to any extent at all",
             "names a move between degree and kind, which the argument does not make"),
            ("infers from the fact that a description fits every case that has been "
             "examined that it must also fit the cases that have not been examined",
             "raises an inductive gap, and the premise here is about all of them rather "
             "than a sample"),
        ]
        expl = ("The premise and the conclusion are about different things: one is about "
                + d["part"] + " and the other about " + d["whole"] + ". The step between "
                "them holds only if the property carries across, and " + d["why"] + ".")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([2, 3, 3]), "v_ac", self.sub)


# --- the source rather than the argument ---------------------------------------------
# mode: "reject" attacks the source, "accept" leans on it.
AUTHORITY = [
    dict(who="Dr Halvorsen", field="marine geology", claim="the harbour dredging will not "
         "disturb the oyster beds", topic="shellfish ecology", mode="accept",
         why="expertise in one field is not expertise in another"),
    dict(who="the chief engineer", field="bridge design", claim="the new tolls will raise "
         "the revenue forecast", topic="traffic economics", mode="accept",
         why="expertise in one field is not expertise in another"),
    dict(who="a panel of retired judges", field="the law", claim="the drug trial results "
         "were correctly analysed", topic="clinical statistics", mode="accept",
         why="expertise in one field is not expertise in another"),
    dict(who="the mill owner", field="", claim="the effluent is harmless", topic="",
         mode="interest", why="the person making the claim stands to gain if it is believed"),
    dict(who="the developer's surveyor", field="", claim="the site holds no remains",
         topic="", mode="interest",
         why="the person making the claim stands to gain if it is believed"),
    dict(who="the incumbent's campaign", field="", claim="the scheme has cut waiting times",
         topic="", mode="interest",
         why="the person making the claim stands to gain if it is believed"),
    dict(who="Vance", field="", claim="the treaty was a mistake", topic="", mode="reject",
         why="who is speaking has no bearing on whether the reasoning holds"),
    dict(who="the union's researcher", field="", claim="the plant is safe to reopen",
         topic="", mode="reject",
         why="who is speaking has no bearing on whether the reasoning holds"),
    dict(who="a former employee of the firm", field="", claim="the accounts were misstated",
         topic="", mode="reject",
         why="who is speaking has no bearing on whether the reasoning holds"),
    dict(who="Professor Lindqvist", field="eighteenth-century poetry",
         claim="the manuscript is a forgery", topic="paper and ink analysis", mode="accept",
         why="expertise in one field is not expertise in another"),
    dict(who="the club physician", field="sports medicine",
         claim="the stadium design is structurally sound", topic="structural engineering",
         mode="accept", why="expertise in one field is not expertise in another"),
    dict(who="the supplier's own laboratory", field="",
         claim="the batch meets the standard", topic="", mode="interest",
         why="the person making the claim stands to gain if it is believed"),
    dict(who="the agency that drafted the policy", field="",
         claim="the policy has worked as intended", topic="", mode="interest",
         why="the person making the claim stands to gain if it is believed"),
    dict(who="a candidate who failed the examination", field="",
         claim="the marking scheme is unsound", topic="", mode="reject",
         why="who is speaking has no bearing on whether the reasoning holds"),
    dict(who="the newspaper that opposed the scheme", field="",
         claim="the costs were understated", topic="", mode="reject",
         why="who is speaking has no bearing on whether the reasoning holds"),
]


class SourceFlaw(CRBase):
    """A claim settled by who made it rather than by what supports it."""
    id = "cr_authority"
    skill = "v_ac"
    sub = "Identify the flaw"
    diff = 3

    def make(self, rng, choices_n):
        d = rng.choice(AUTHORITY)
        if d["mode"] == "accept":
            stem = (upfirst(d["who"]) + ", an authority on " + d["field"] + ", holds that "
                    + d["claim"] + ". That settles the matter.")
            right = ("relies on the judgement of an authority whose expertise lies "
                     "outside " + d["topic"])
        elif d["mode"] == "interest":
            stem = (upfirst(d["who"]) + " maintains that " + d["claim"]
                    + ". There is no reason to doubt it.")
            right = ("accepts a claim from a source with an interest in its being believed, "
                     "without independent support")
        else:
            stem = (upfirst(d["who"]) + " argues that " + d["claim"]
                    + ", but there is no reason to take that seriously.")
            right = ("rejects a claim on the basis of its source rather than by addressing "
                     "the reasoning offered for it")
        stem += ("\n\nThe reasoning above is most vulnerable to criticism on the grounds "
                 "that it:")
        wrongs = [
            ("treats the absence of evidence against a claim as though it were evidence "
             "for the claim",
             "names a different move, and the argument here leans on a source rather than "
             "on silence"),
            ("assumes that a claim is true because it has not been shown to be false by "
             "anyone qualified to judge",
             "combines two different failings, neither of which is the step taken"),
            ("takes a widely held opinion as though popularity established it",
             "names an appeal to numbers, and one source is cited here rather than many"),
            ("presumes that what was true in the past will remain true",
             "raises a timing gap the argument does not depend on"),
            ("confuses a claim about what ought to be done with a claim about what is the "
             "case",
             "names a move between fact and value that the argument does not make"),
            ("offers an analogy between two cases that are alike in no relevant respect",
             "names a faulty analogy, and no comparison is drawn here"),
            ("mistakes a condition required for a result for one that guarantees it",
             "names a conditional confusion, and no conditional is stated"),
            ("infers a general rule from a single instance",
             "names a hasty generalisation, and no generalisation is drawn"),
            ("infers that a conclusion must itself be false from the observation that the "
             "argument which has been offered in support of it is unsound",
             "names the step from a bad argument to a false conclusion, which is a real "
             "error and not the one here"),
            ("assumes that two parties who disagree about a conclusion must also disagree "
             "about the evidence that bears on whether it is true",
             "describes a misreading of a dispute, and only one party speaks here"),
            ("relies on the claim that a practice must be acceptable because it has long "
             "been followed without anyone raising an objection to it",
             "names an appeal to tradition, which the argument does not make"),
            ("treats a statement that was made about one particular case as though it had "
             "been offered as a principle governing every case of that kind",
             "names an overreach from the particular to the general, and the conclusion "
             "here stays with the single claim"),
        ]
        expl = ("The conclusion rests on the source rather than on the support offered for "
                "the claim, and " + d["why"] + ". Nothing here shows the claim to be false; "
                "what it shows is that the argument has not established it.")
        return self.emit(rng, choices_n, stem, right, wrongs, expl,
                         rng.choice([2, 3, 3, 4]), "v_ac", self.sub)


GENS = [NecSuff(), PartWhole(), SourceFlaw()]


# The necessary condition templates write "The rule says that {req} is needed" and
# "whether {req} was obtained by a means the rule would not recognise", so the
# requirement is a bare subject twice over. One entry read "two independent reviews is
# needed" (INC-0096).
_plural = [d["req"] for d in NECSUFF if plural_head(d["req"])]
if _plural:
    raise SystemExit(
        "g_flaw: a necessary condition goes straight in front of 'is needed', so it has "
        "to be singular. Rename: " + ", ".join(_plural))
