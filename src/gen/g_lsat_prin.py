"""Applying a principle, with the answer proved rather than asserted (lsat_lr_prin).

LSAC lists identifying and applying principles among the skills Logical Reasoning
measures. This question states a principle and asks which of five judgments most closely
conforms to it. A judgment conforms when the principle, together with what the judgment
says about its case, establishes the judgment's conclusion.

Each principle is a rule about the members of a group, in one of three forms: every
member who P should A; every member who P and Q should A; no member who P should A. Each
judgment names a member, says which of the principle's conditions they meet, sometimes
leaving one unsaid or citing a fact the principle does not mention, and concludes that
they should A, should not A, or need not A.

Whether a judgment is established is not asserted. entailed() treats what should happen
to a member as one of three statuses, required, forbidden or neither; the principle fixes
the status only for a member who meets all its conditions. It tries every status and
every value of each condition the judgment leaves unsaid, and a judgment is established
only when its conclusion holds in every case the principle allows. Each item is checked
to have exactly one established choice, and check_principles() confirms at build time
that every labelled wrong-answer kind is unestablished and every key established.

"Should not" and "need not" are different claims, and the difference is where these
questions are won. A principle that forbids something establishes both for a member it
covers, so the forbidding form never offers "need not" beside its key: that would be a
second correct answer, which the checker would refuse.

The category also carries identifying principles and reasoning by analogy, which the
hand written items cover and nothing here generates, so this schema stops at CAP items
rather than filling the category's target with one kind of question.
"""
import itertools

from framework import ItemError
from g_gmat_cr import CRBase
from g_lsat_concl import SCENES

CAP = 150

# For each scene: the group as a principle names it, and six members. Every name is
# invented; nothing here is a claim about a real person, building, firm or species. The
# three actions are what a principle can say should happen to a member, written to follow
# "should", "should not" and "need not".
CAST = {
    "At Verdant Logistics": dict(
        group="employee of Verdant Logistics",
        names=["Mara Quist", "Tobin Hale", "Ines Brandt", "Olu Kade", "Petra Voss", "Samir Lund"],
        acts=["be offered a place on the safety course", "receive the winter bonus",
              "be consulted about the new shift pattern"]),
    "At Fenmore College": dict(
        group="student at Fenmore College",
        names=["Ines Varga", "Olu Adebayo", "Kit Marlow", "Dana Reyes", "Yusuf Amari", "Lena Holt"],
        acts=["be given priority for campus housing", "receive the travel grant",
              "be invited to the careers fair"]),
    "In the Aldine collection": dict(
        group="painting in the Aldine collection",
        names=["the Hartwell portrait", "the harbour view", "the Lisle altarpiece",
               "the Merrin still life", "the river landscape", "the Tamsin study"],
        acts=["be lent to other museums", "be moved to the climate controlled gallery",
              "be photographed for the new catalogue"]),
    "At the Bellweather food bank": dict(
        group="volunteer at the Bellweather food bank",
        names=["Dev Rana", "Ruth Amsel", "Cato Brisk", "Nia Okafor", "Hal Pruett", "Suki Mori"],
        acts=["be offered driver training", "be asked to lead a shift",
              "receive a letter of thanks"]),
    "On Wren Lane": dict(
        group="house on Wren Lane",
        names=["the house at number 12", "the corner house", "the house at number 3",
               "the old forge", "the house at number 27", "the white cottage"],
        acts=["be inspected for damp", "receive the insulation grant",
              "be included in the conservation survey"]),
    "In the Delmore business park": dict(
        group="firm in the Delmore business park",
        names=["Corvel", "Stanfield Instruments", "Halden Print", "Mirrow Foods",
               "Ostrand Labs", "Pell and Tate"],
        acts=["be offered the reduced rent", "be invited onto the tenants' board",
              "receive the recycling subsidy"]),
    "At the Harwick Rowing Club": dict(
        group="member of the Harwick Rowing Club",
        names=["Lena Okoro", "Piet Janssen", "Ada Morrell", "Theo Brandt", "Rosa Keel", "Idris Vane"],
        acts=["be given a key to the boathouse", "pay the reduced fee",
              "be picked for the first crew"]),
    "In the Larch Street building": dict(
        group="tenant in the Larch Street building",
        names=["Amos Adeyemi", "Clare Whitlow", "Jonah Pike", "Mei Tanaka", "Otto Sand", "Vera Lind"],
        acts=["be offered a parking space", "receive the rent rebate",
              "be consulted about the renovation"]),
    "Among the bird species recorded on Selby Island": dict(
        group="bird species recorded on Selby Island",
        names=["species K", "species M", "species P", "species R", "species T", "species W"],
        acts=["be listed as a priority for protection", "be counted every spring",
              "be included in the visitor guide"]),
    "In the Castell Orchestra": dict(
        group="musician in the Castell Orchestra",
        names=["Anya Morrow", "Felix Brandt", "Iris Calder", "Nico Salas", "Maud Frey", "Emil Rask"],
        acts=["be offered a solo", "receive the travel allowance",
              "be invited on the summer tour"]),
}

# A principle: how many conditions it has, the status it fixes for a member who meets
# them all, and the judgment that is its key. A judgment is (facts, conclusion): facts
# maps a condition to True or False, or leaves it unsaid; the key "r" is a fact the
# principle does not mention.
FORMS = {
    "every":  dict(conds=1, status="required", key=({0: True}, "should")),
    "every2": dict(conds=2, status="required", key=({0: True, 1: True}, "should")),
    "no":     dict(conds=1, status="forbidden", key=({0: True}, "should not")),
}

# The wrong answers each form offers, each with what it gets wrong. Every one of them is
# confirmed unestablished by check_principles(); they are written down rather than
# searched for so that each carries its own explanation.
WRONG = {
    "every": [
        (({0: False}, "need not"), "treats the principle as if it also said what happens to cases it does not cover"),
        (({0: False}, "should"), "applies the principle to a case that does not meet its condition"),
        (({0: True}, "need not"), "reaches the opposite of what the principle requires for a case it covers"),
        (({0: True}, "should not"), "rules out what the principle requires for a case it covers"),
        (({"r": True}, "should"), "rests on a fact the principle does not mention, without establishing its condition"),
    ],
    "every2": [
        (({0: True, 1: False}, "should"), "applies the principle to a case that meets only one of its two conditions"),
        (({0: False, 1: True}, "should"), "applies the principle to a case that meets only one of its two conditions"),
        (({0: True}, "should"), "applies the principle without establishing its second condition"),
        (({0: True, 1: True}, "need not"), "reaches the opposite of what the principle requires for a case it covers"),
        (({0: False, 1: False}, "need not"), "treats the principle as if it also said what happens to cases it does not cover"),
    ],
    "no": [
        (({0: False}, "should"), "treats the principle as if it required something for cases it does not cover"),
        (({0: False}, "should not"), "applies the principle's prohibition to a case that does not meet its condition"),
        (({0: True}, "should"), "requires what the principle rules out for a case it covers"),
        (({"r": True}, "should not"), "rests on a fact the principle does not mention, without establishing its condition"),
    ],
}

STATUSES = ("required", "forbidden", "neither")
HOLDS = {"should": lambda s: s == "required",
         "should not": lambda s: s == "forbidden",
         "need not": lambda s: s != "required"}


def entailed(form, facts, concl):
    """Whether the principle and the facts establish the conclusion.

    Tries every value of each condition the facts leave unsaid and every status the
    principle leaves open. The principle fixes the status only when all its conditions
    hold; otherwise any status is possible, because a principle says nothing about the
    cases it does not cover.
    """
    F = FORMS[form]
    unsaid = [i for i in range(F["conds"]) if facts.get(i) is None]
    for vals in itertools.product((True, False), repeat=len(unsaid)):
        known = dict((i, v) for i, v in facts.items() if isinstance(i, int))
        known.update(zip(unsaid, vals))
        covered = all(known[i] for i in range(F["conds"]))
        for status in STATUSES:
            if covered and status != F["status"]:
                continue
            if not HOLDS[concl](status):
                return False
    return True


def check_principles():
    """Every key established and every labelled wrong answer not, for every form."""
    bad = []
    for name, F in FORMS.items():
        if not entailed(name, *F["key"]):
            bad.append("%s: its key is not established" % name)
        for (facts, concl), _ in WRONG[name]:
            if entailed(name, facts, concl):
                bad.append("%s: the wrong answer %r / %r is established" % (name, facts, concl))
        if len(WRONG[name]) < 4:
            bad.append("%s: fewer than four wrong answers" % name)
    return bad


def _article(noun):
    return "an" if noun[:1] in "aeiou" else "a"


class ApplyPrinciple(CRBase):
    """Which judgment the stated principle establishes."""
    id = "lsat_principle"
    skill = "lsat_lr_prin"
    section = "LR"
    type = "LR"
    sub = "Apply a principle"
    diff = 3
    item_cap = CAP

    def make(self, rng, choices_n):
        form = rng.choice(sorted(FORMS))
        F = FORMS[form]
        scene = rng.choice(SCENES)
        cast = CAST[scene["intro"]]
        idx = rng.sample(range(len(scene["props"])), 3)
        props = [scene["props"][i] for i in idx]   # conditions 0 and 1, then the unrelated fact
        act = rng.choice(cast["acts"])
        rel = scene["rel"]
        nonrestrictive = "which" if rel == "that" else "who"
        group = cast["group"]

        conds = [props[i][0] for i in range(F["conds"])]
        if form == "no":
            principle = "No %s %s %s should %s." % (group, rel, conds[0], act)
        else:
            principle = "Every %s %s %s should %s." % (group, rel, " and ".join(conds), act)

        def said(facts):
            """What a judgment says of its member: the true facts first, then any that do
            not hold after "but", so "works night shifts but does not hold a licence"."""
            yes, no = [], []
            for k in ["r"] + list(range(F["conds"])):
                if k not in facts:
                    continue
                prop = props[2] if k == "r" else props[k]
                (yes if facts[k] else no).append(prop[0] if facts[k] else prop[2])

            def listed(xs):
                return xs[0] if len(xs) == 1 else "%s and %s" % (", ".join(xs[:-1]), xs[-1])
            if yes and no:
                return "%s but %s" % (listed(yes), " and ".join(no))
            return listed(yes or no)

        # One member per choice: the key takes the first name and each wrong answer one of
        # the rest, so no two choices are ever about the same member.
        names = rng.sample(cast["names"], 1 + len(WRONG[form]))

        def judgment(name, facts, concl):
            return "%s, %s %s, %s %s." % (name[0].upper() + name[1:], nonrestrictive,
                                          said(facts), concl, act)

        kfacts, kconcl = F["key"]
        wrongs = [(facts, concl, why) for (facts, concl), why in WRONG[form]]
        rng.shuffle(wrongs)

        def padded(facts):
            """The same facts, sometimes with the unrelated one added. It changes nothing
            about what the judgment establishes, and it is how the length of the key is
            kept from giving it away."""
            if "r" in facts or rng.random() < 0.5:
                return facts
            out = dict(facts)
            out["r"] = rng.random() < 0.5
            return out

        # The key has no negation in it and most wrong answers do, so left alone the key
        # was the shortest or second shortest choice on three draws in four. A rank for
        # the key is drawn first, and which wrong answers are offered, and which choices
        # also mention the unrelated fact, are redrawn until the key lands on it.
        target = rng.randint(0, choices_n - 1)
        best = None
        for _ in range(80):
            kf = padded(kfacts)
            right = judgment(names[0], kf, kconcl)
            picked = rng.sample(range(len(wrongs)), choices_n - 1)
            offered = []
            for i in picked:
                facts, concl, why = wrongs[i]
                pf = padded(facts)
                offered.append((judgment(names[1 + i], pf, concl), why, pf, concl))
            rank = sum(1 for w in offered if len(w[0]) < len(right))
            if best is None or abs(rank - target) < best[0]:
                best = (abs(rank - target), right, offered, kf)
            if rank == target:
                break
        _, right, offered, kf = best
        # Every choice is checked again exactly as it will be shown, the key established
        # and each wrong answer not, since padding must never change which is which.
        if not entailed(form, kf, kconcl):
            raise ItemError("%s: the key is not established" % self.id)
        for w, why, pf, concl in offered:
            if entailed(form, pf, concl):
                raise ItemError("%s: a wrong answer is established: %s" % (self.id, w))
        pool = [(w, why) for w, why, _, _ in offered]
        stem_q = rng.choice([
            "Which one of the following judgments most closely conforms to the principle above?",
            "The principle above, if valid, most helps to justify which one of the following judgments?",
        ])
        stem = "Principle: %s\n\nEach judgment below concerns %s %s. %s" % (
            principle, _article(group), group, stem_q)
        subject = names[0][0].upper() + names[0][1:]
        if form == "no":
            expl = ("The principle says that no %s %s %s should %s. %s %s, so the "
                    "principle covers this case and establishes that %s should not %s. The "
                    "other judgments are not established: each concerns a case the principle "
                    "does not cover, rests on a fact it does not mention, or requires what it "
                    "rules out." % (group, rel, conds[0], act, subject, said(kfacts),
                                    names[0], act))
        else:
            expl = ("The principle says that every %s %s %s should %s. %s %s, so the "
                    "principle covers this case and establishes that %s should %s. The other "
                    "judgments are not established: each draws a conclusion about a case the "
                    "principle does not cover, leaves one of its conditions unestablished, or "
                    "reaches the opposite of what it requires."
                    % (group, rel, " and ".join(conds), act, subject, said(kfacts),
                       names[0], act))
        item = self.emit(rng, choices_n, stem, right, pool, expl,
                         3 if form == "every" else 4, self.skill, self.sub)
        item["section"] = "LR"
        item["type"] = "LR"
        return item


GENS = [ApplyPrinciple()]
