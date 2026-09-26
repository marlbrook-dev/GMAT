"""Parallel reasoning, with the pattern of every argument fixed and proved (lsat_lr_expl).

LSAC lists recognizing similarities and differences between patterns of reasoning among the
skills Logical Reasoning measures, and it sits in the category that also carries
explanations. The question gives an argument and asks which of five others reasons in the
most similar way, or, when the argument is flawed, which commits the most similar flaw.

What makes two arguments parallel is their form, and form can be fixed when an argument is
written. So each argument here is built from one of eight forms over the vocabulary of
g_lsat_concl.py: a rule about a group (every, no, or some of its members who have one
property have another), a named member of the group, and a conclusion about that member.
The key is the one choice built on the stimulus's form; the other four are built on
different forms, each in a different setting from the stimulus and from each other, so no
choice can be picked by its subject matter.

Whether each form is valid is not asserted. check_forms() evaluates every form against
every small group with one named member, and the build fails if a form marked valid has a
counterexample or one marked flawed has none. The label decides the question's wording:
"most similar in its reasoning" for a valid argument, "most similar flawed reasoning" for
a flawed one.

The category also carries explanations, which the hand written items cover and nothing
here generates, so this schema stops at CAP items rather than filling the category's
target with one kind of question.
"""
import itertools

from framework import ItemError
from g_gmat_cr import CRBase
from g_lsat_concl import SCENES

CAP = 150

# One named member of each scene's group, with the phrase that places them in it. Every
# name is invented; nothing here is a claim about a real person, building or species.
MEMBERS = {
    "At Verdant Logistics": ("an employee of Verdant Logistics", ["Mara Quist", "Tobin Hale"]),
    "At Fenmore College": ("a student at Fenmore College", ["Ines Varga", "Olu Adebayo"]),
    "In the Aldine collection": ("a painting in the Aldine collection",
                                 ["the Hartwell portrait", "the harbour view"]),
    "At the Bellweather food bank": ("a volunteer at the Bellweather food bank",
                                     ["Dev Rana", "Ruth Amsel"]),
    "On Wren Lane": ("a house on Wren Lane", ["the house at number 12", "the corner house"]),
    "In the Delmore business park": ("a firm in the Delmore business park",
                                     ["Corvel", "Stanfield Instruments"]),
    "At the Harwick Rowing Club": ("a member of the Harwick Rowing Club",
                                   ["Lena Okoro", "Piet Janssen"]),
    "In the Larch Street building": ("a tenant in the Larch Street building",
                                     ["Amos Adeyemi", "Clare Whitlow"]),
    "Among the bird species recorded on Selby Island": (
        "a bird species recorded on Selby Island", ["species K", "species M"]),
    "In the Castell Orchestra": ("a musician in the Castell Orchestra",
                                 ["Anya Morrow", "Felix Brandt"]),
}

# The group noun as it stands before "who"/"that" in a rule, so a rule names its group.
GROUP = {
    "At Verdant Logistics": "employee of Verdant Logistics",
    "At Fenmore College": "student at Fenmore College",
    "In the Aldine collection": "painting in the Aldine collection",
    "At the Bellweather food bank": "volunteer at the Bellweather food bank",
    "On Wren Lane": "house on Wren Lane",
    "In the Delmore business park": "firm in the Delmore business park",
    "At the Harwick Rowing Club": "member of the Harwick Rowing Club",
    "In the Larch Street building": "tenant in the Larch Street building",
    "Among the bird species recorded on Selby Island": "bird species recorded on Selby Island",
    "In the Castell Orchestra": "musician in the Castell Orchestra",
}
GROUP_PL = {
    "At Verdant Logistics": "employees of Verdant Logistics",
    "At Fenmore College": "students at Fenmore College",
    "In the Aldine collection": "paintings in the Aldine collection",
    "At the Bellweather food bank": "volunteers at the Bellweather food bank",
    "On Wren Lane": "houses on Wren Lane",
    "In the Delmore business park": "firms in the Delmore business park",
    "At the Harwick Rowing Club": "members of the Harwick Rowing Club",
    "In the Larch Street building": "tenants in the Larch Street building",
    "Among the bird species recorded on Selby Island": "bird species recorded on Selby Island",
    "In the Castell Orchestra": "musicians in the Castell Orchestra",
}

# A form is its rule, what is said of the member (True: has the property, False: lacks
# it), and what is concluded of them. P, Q, R are properties 0, 1, 2.
#   rule: ("all"|"no"|"some", a, b), or a pair of "all" rules for the chain
#   fact: (property, has)       conclusion: (property, has)
FORMS = {
    "mp":      dict(rules=[("all", 0, 1)], fact=(0, True), concl=(1, True), valid=True,
                    family="mp", say="applies a rule to a case that meets its condition and "
                    "concludes that the case has the feature the rule promises"),
    "mt":      dict(rules=[("all", 0, 1)], fact=(1, False), concl=(0, False), valid=True,
                    family="mt", say="finds a case that lacks what the rule promises and "
                    "concludes that the case does not meet the rule's condition"),
    "ac":      dict(rules=[("all", 0, 1)], fact=(1, True), concl=(0, True), valid=False,
                    family="ac", say="finds a case that has what the rule promises and "
                    "concludes that the case meets the rule's condition, which reverses the rule"),
    "da":      dict(rules=[("all", 0, 1)], fact=(0, False), concl=(1, False), valid=False,
                    family="da", say="finds a case that does not meet the rule's condition and "
                    "concludes that it lacks what the rule promises, although the rule says "
                    "nothing about such cases"),
    "no_mp":   dict(rules=[("no", 0, 1)], fact=(0, True), concl=(1, False), valid=True,
                    family="mp", say="applies a rule that no one meeting a condition has a "
                    "feature to a case that meets the condition"),
    "no_da":   dict(rules=[("no", 0, 1)], fact=(0, False), concl=(1, True), valid=False,
                    family="da", say="concludes that a case outside a rule's condition must "
                    "have the feature the rule denies to those inside it"),
    "some_mp": dict(rules=[("some", 0, 1)], fact=(0, True), concl=(1, True), valid=False,
                    family="some", say="concludes that a particular case has a feature because "
                    "some of those like it do"),
    "chain":   dict(rules=[("all", 0, 1), ("all", 1, 2)], fact=(0, True), concl=(2, True),
                    valid=True, family="chain", say="links two rules and applies the pair to a "
                    "case that meets the first condition"),
}


def _sentence(scene, props, rule):
    f, a, b = rule
    g, gp, rel = GROUP[scene["intro"]], GROUP_PL[scene["intro"]], scene["rel"]
    if f == "all":
        return "Every %s %s %s %s." % (g, rel, props[a][0], props[b][0])
    if f == "no":
        return "No %s %s %s %s." % (g, rel, props[a][0], props[b][0])
    return "Some %s %s %s %s." % (gp, rel, props[a][1], props[b][1])


def render(form, scene, idx, name):
    """One argument of the given form, in the given scene, about the named member."""
    props = [scene["props"][i] for i in idx]
    F = FORMS[form]
    where, _ = MEMBERS[scene["intro"]]
    rules = " ".join(_sentence(scene, props, r) for r in F["rules"])
    p, has = F["fact"]
    fact = "%s, %s, %s." % (name[0].upper() + name[1:], where,
                            props[p][0] if has else props[p][2])
    c, chas = F["concl"]
    concl = "So %s %s." % (name, props[c][0] if chas else props[c][2])
    return "%s %s %s" % (rules, fact, concl)


STEM_VALID = "Which one of the following arguments is most similar in its pattern of reasoning to the argument above?"
STEM_FLAWED = "The flawed pattern of reasoning in the argument above is most similar to that in which one of the following arguments?"


class ParallelReasoning(CRBase):
    """Which argument shares the stimulus's form, among arguments built on other forms."""
    id = "lsat_parallel"
    skill = "lsat_lr_expl"
    section = "LR"
    type = "LR"
    sub = "Parallel reasoning"
    diff = 4
    item_cap = CAP

    def make(self, rng, choices_n):
        form = rng.choice(sorted(FORMS))
        # Every argument on the page gets a setting of its own.
        scenes = rng.sample(SCENES, len(SCENES))

        def draw(scene):
            idx = rng.sample(range(len(scene["props"])), 3)
            name = rng.choice(MEMBERS[scene["intro"]][1])
            return idx, name

        s0 = scenes[0]
        idx0, name0 = draw(s0)
        stimulus = render(form, s0, idx0, name0)
        valid = FORMS[form]["valid"]
        stem = stimulus + "\n\n" + (STEM_VALID if valid else STEM_FLAWED)
        k_idx, k_name = draw(scenes[1])
        right = render(form, scenes[1], k_idx, k_name)
        # Other forms only, and never one from the key's family: "no one who P has Q"
        # applied to a P is the same move as "everyone who P has Q" applied to a P, and
        # offering it would make a second defensible answer.
        others = [f for f in sorted(FORMS) if FORMS[f]["family"] != FORMS[form]["family"]]
        if len(others) < choices_n - 1:
            raise ItemError("%s: too few other forms" % self.id)
        if len(others) > len(scenes) - 2:
            raise ItemError("%s: more forms than settings" % self.id)
        wrongs = []
        for f, scene in zip(rng.sample(others, len(others)), scenes[2:]):
            idx, name = draw(scene)
            wrongs.append((render(f, scene, idx, name),
                           "%s; the argument above does something else" % FORMS[f]["say"]))
        expl = ("The argument %s. That is %s. The correct choice does the same thing with a "
                "different rule about a different group." % (
                    FORMS[form]["say"],
                    "valid reasoning" if valid else "a flaw, and the question asks for the "
                    "same flaw"))
        item = self.emit(rng, choices_n, stem, right, wrongs, expl,
                         4 if valid else 5, self.skill, self.sub)
        item["section"] = "LR"
        item["type"] = "LR"
        return item


GENS = [ParallelReasoning()]


def check_forms():
    """Every form's valid flag, confirmed against every small group with one named member.

    A group is counts of the eight kinds of member (0 to 2 of each) plus the named member's
    own kind. A rule is read over the whole group including the named member, since they
    belong to it. A form is valid when every group that makes its rules and its fact true
    also makes its conclusion true.
    """
    bad = []
    for name, F in FORMS.items():
        counter = False
        for counts in itertools.product(range(3), repeat=8):
            for me in range(8):
                total = list(counts)
                total[me] += 1

                def holds(rule):
                    f, a, b = rule
                    kinds = [t for t in range(8) if t >> a & 1]
                    yes = sum(total[t] for t in kinds if t >> b & 1)
                    no = sum(total[t] for t in kinds if not t >> b & 1)
                    return {"all": no == 0, "no": yes == 0, "some": yes > 0}[f]

                p, has = F["fact"]
                if not all(holds(r) for r in F["rules"]) or bool(me >> p & 1) != has:
                    continue
                c, chas = F["concl"]
                if bool(me >> c & 1) != chas:
                    counter = True
                    break
            if counter:
                break
        if counter == F["valid"]:
            bad.append("%s is marked %s but %s" % (
                name, "valid" if F["valid"] else "flawed",
                "has a counterexample" if counter else "has none"))
    return bad
