"""GMAT Data Insights: Multi-Source Reasoning.

An MSR item presents two or three sources that have to be read together, and the
questions turn on a fact that lives in none of them alone. The reasoning is rule
checking rather than argument, which is exactly what makes it generatable without ever
asserting a key: the rules are data, the cases are data, and compliance is decided by
evaluating one against the other in Python.

The design point that matters is the same one that makes real MSR hard. Each case
violates a deliberately chosen number of rules, so a reader who checks only the first
source, or only the obvious rule, reaches a confident wrong answer. The explanation
walks every case, because a student who got it wrong needs to see which rule they
missed, not just the count.
"""
from framework import Gen, ItemError


def word(n):
    return {0: "None", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}.get(n, str(n))


# Each policy is a set of independent, checkable conditions over a case's fields.
# fields: (label, kind) where kind drives how a value is drawn and rendered.
POLICIES = [
    dict(
        key="rooms", org="Alderton Conference Centre", unit="booking request",
        source_a="Room booking policy", source_b="Pending requests",
        caption=("Requests are approved only if every condition in the booking policy "
                 "is met. Room capacities are fixed and may not be exceeded."),
        rules=[
            ("cap", "The number of attendees may not exceed the capacity of the room booked."),
            ("notice", "A request must be submitted at least {notice} days before the booking date."),
            ("approve", "A booking in the Ridgeway Room requires written approval from a department head."),
            ("weeks", "A recurring booking may run for at most {weeks} consecutive weeks."),
        ],
        rooms=[("Cobb Room", 8), ("Shaw Room", 15), ("Ridgeway Room", 30), ("Turner Room", 45)],
        cols=["Request", "Room", "Attendees", "Days of notice", "Head approval", "Recurring weeks"],
    ),
    dict(
        key="grants", org="the Hartwell Community Fund", unit="grant application",
        source_a="Grant eligibility rules", source_b="Applications received",
        caption=("An application is funded only if it satisfies every eligibility rule. "
                 "Amounts are in thousands of dollars."),
        rules=[
            ("cap", "The amount requested may not exceed the ceiling for the applicant's category."),
            ("notice", "An application must be filed at least {notice} days before the project start date."),
            ("approve", "An application in the Heritage category requires a letter of support from the council."),
            ("weeks", "A project may not run for more than {weeks} weeks."),
        ],
        rooms=[("Youth", 12), ("Heritage", 30), ("Environment", 45), ("Arts", 20)],
        cols=["Application", "Category", "Amount requested", "Days of notice",
              "Council letter", "Project weeks"],
    ),
    dict(
        key="shipments", org="Brightlin Freight", unit="shipment order",
        source_a="Acceptance conditions", source_b="Orders awaiting dispatch",
        caption=("An order is dispatched only if every acceptance condition is met. "
                 "Weights are in kilograms."),
        rules=[
            ("cap", "The weight of a shipment may not exceed the limit for the vehicle assigned."),
            ("notice", "An order must be lodged at least {notice} days before the dispatch date."),
            ("approve", "A shipment assigned to the Long Haul Rig requires a signed customs declaration."),
            ("weeks", "A standing order may repeat for at most {weeks} consecutive weeks."),
        ],
        rooms=[("City Van", 600), ("Box Truck", 2400), ("Long Haul Rig", 9000), ("Flatbed", 4500)],
        cols=["Order", "Vehicle", "Weight", "Days of notice", "Customs declaration",
              "Standing weeks"],
    ),
]


def make_cases(rng, pol, n):
    """Draw n cases, each violating a chosen set of rules, and record which."""
    notice = rng.choice([3, 5, 7, 10])
    weeks = rng.choice([6, 8, 10, 12])
    special = pol["rooms"][2][0]            # the option the approval rule attaches to
    cases = []
    # One case must be clean and at least one must fail on the approval rule, or the
    # "which single change" question has nothing to bite on.
    plan = [set()] + [set(rng.sample(["cap", "notice", "approve", "weeks"],
                                     rng.choice([1, 1, 2]))) for _ in range(n - 1)]
    rng.shuffle(plan)
    if not any("approve" in p for p in plan):
        plan[rng.randrange(len(plan))] = {"approve"}
    for i, broken in enumerate(plan):
        if "approve" in broken:
            room, cap = pol["rooms"][2]
        else:
            room, cap = rng.choice([r for r in pol["rooms"] if r[0] != special])
        size = (cap + rng.randrange(1, max(2, cap // 4))) if "cap" in broken \
            else rng.randrange(max(1, cap // 3), cap + 1)
        days = rng.randrange(0, notice) if "notice" in broken \
            else rng.randrange(notice, notice + 12)
        appr = "No" if "approve" in broken else "Yes"
        wk = rng.randrange(weeks + 1, weeks + 8) if "weeks" in broken \
            else rng.randrange(1, weeks + 1)
        cases.append(dict(tag=pol["unit"][0].upper() + str(i + 1), room=room, cap=cap,
                          size=size, days=days, appr=appr, weeks=wk, broken=broken))
    return notice, weeks, cases


def violations(pol, notice, weeks, c):
    """Recompute from the rendered values, so the key cannot drift from the table."""
    special = pol["rooms"][2][0]
    bad = []
    if c["size"] > c["cap"]:
        bad.append("cap")
    if c["days"] < notice:
        bad.append("notice")
    if c["room"] == special and c["appr"] != "Yes":
        bad.append("approve")
    if c["weeks"] > weeks:
        bad.append("weeks")
    return bad


def render(pol, notice, weeks, cases):
    rules = "".join("<li>" + text.format(notice=notice, weeks=weeks) + "</li>"
                    for _, text in pol["rules"])
    caps = ", ".join(n + " " + "{:,}".format(v) for n, v in pol["rooms"])
    head = "".join("<th>" + c + "</th>" for c in pol["cols"])
    rows = "".join(
        "<tr><td>" + c["tag"] + "</td><td>" + c["room"] + "</td><td>"
        + "{:,}".format(c["size"]) + "</td><td>" + str(c["days"]) + "</td><td>"
        + c["appr"] + "</td><td>" + str(c["weeks"]) + "</td></tr>" for c in cases)
    return ("<div class=\"msrc\"><h4>" + pol["source_a"] + "</h4><ul>" + rules
            + "</ul><p class=\"dnote\">Limits by "
            + pol["cols"][1].lower() + ": " + caps + ".</p></div>"
            + "<div class=\"msrc\"><h4>" + pol["source_b"] + "</h4>"
            + "<table class=\"dtable\"><thead><tr>" + head + "</tr></thead><tbody>"
            + rows + "</tbody></table><p class=\"dnote\">" + pol["caption"] + "</p></div>")


class MSRBase(Gen):
    section = "DI"
    type = "MSR"
    skill = "di_msr"
    sub = "Multi-source"
    domain = "nonmath"
    diff = 3

    def sources(self, rng):
        pol = rng.choice(POLICIES)
        notice, weeks = None, None
        n = rng.choice([4, 5])
        notice, weeks, cases = make_cases(rng, pol, n)
        for c in cases:
            c["bad"] = violations(pol, notice, weeks, c)
        return pol, notice, weeks, cases

    def walk(self, pol, notice, weeks, cases):
        names = {"cap": "exceeds the limit", "notice": "gives too little notice",
                 "approve": "lacks the required approval",
                 "weeks": "runs for too many weeks"}
        return " ".join(
            c["tag"] + ": " + ("meets every condition."
                               if not c["bad"] else
                               " and ".join(names[b] for b in c["bad"]) + ".")
            for c in cases)


class CountCompliant(MSRBase):
    id = "msr_count"

    def build(self, rng):
        pol, notice, weeks, cases = self.sources(rng)
        ok = [c for c in cases if not c["bad"]]
        ans = len(ok)
        onlycap = sum(1 for c in cases if c["bad"] == ["cap"] or not c["bad"])
        onlynotice = sum(1 for c in cases if "notice" not in c["bad"])
        onlysize = sum(1 for c in cases if c["size"] <= c["cap"])
        cands = []
        for v, w in [(len(cases) - ans, "counting the " + pol["unit"] + "s that fail rather "
                      "than those that pass"),
                     (onlysize, "checking the limit alone and ignoring the other conditions"),
                     (onlynotice, "checking the notice rule alone"),
                     (onlycap, "treating a failure on any rule other than the limit as acceptable"),
                     (ans + 1, "an off by one count"),
                     (max(0, ans - 1), "an off by one count in the other direction"),
                     (len(cases), "assuming every " + pol["unit"] + " listed is acceptable")]:
            if v != ans and 0 <= v <= len(cases):
                cands.append((float(v), w))
        return dict(
            stem="How many of the " + pol["unit"] + "s listed satisfy every condition "
                 "exactly as submitted, with no change?",
            answer=float(ans), distractors=cands, diff=rng.choice([2, 3]),
            passageHtml=render(pol, notice, weeks, cases), domain="nonmath",
            expl=self.walk(pol, notice, weeks, cases) + " That leaves " + word(ans).lower()
                 + " " + pol["unit"] + ("" if ans == 1 else "s") + " meeting every condition.")


class SingleFix(MSRBase):
    """Choices are the possible single changes, and exactly one of them fixes the case.

    The distractor machinery does not apply, because the options are sentences rather
    than values, so this builds the option set directly and computes which one works by
    applying each change and re-running the rule check.
    """
    id = "msr_fix"
    diff = 4

    def make(self, rng, choices_n):
        pol, notice, weeks, cases = self.sources(rng)
        target = [c for c in cases if len(c["bad"]) == 1]
        if not target:
            raise ItemError("msr_fix needs a case failing exactly one rule")
        c = rng.choice(target)
        rule = c["bad"][0]
        special = pol["rooms"][2][0]
        roomy = [r for r in pol["rooms"] if r[1] >= c["size"] and r[0] != c["room"]]
        if not roomy:
            raise ItemError("msr_fix has nowhere to reassign the case")
        earlier = max(1, notice - c["days"] + 1)
        sizecol = pol["cols"][2].lower()
        # Every option is a concrete change, and every option is applied to a copy of the
        # case so the key is decided by re-running the rule check rather than by assertion.
        fixes = [
            ("cap", "Reassign it to " + roomy[0][0],
             dict(room=roomy[0][0], cap=roomy[0][1])),
            ("notice", "Submit it " + str(earlier) + " day" + ("" if earlier == 1 else "s")
             + " earlier", dict(days=c["days"] + earlier)),
            ("approve", "Obtain the written approval the policy requires", dict(appr="Yes")),
            ("weeks", "Shorten it to " + str(weeks) + " weeks", dict(weeks=weeks)),
            (None, "Reduce the " + sizecol + " by one", dict(size=max(0, c["size"] - 1))),
        ]
        import copy
        works = []
        for tag, label, change in fixes:
            probe = copy.deepcopy(c)
            probe.update(change)
            if not violations(pol, notice, weeks, probe):
                works.append(label)
        if len(works) != 1:
            raise ItemError("msr_fix has %d changes that clear the case" % len(works))
        right = works[0]
        opts = [label for _, label, _ in fixes][:choices_n]
        if right not in opts or len(set(opts)) != len(opts) or len(opts) < choices_n:
            raise ItemError("msr_fix could not build distinct options")
        rng.shuffle(opts)
        names = {"cap": "records a " + pol["cols"][2].lower() + " of "
                        + "{:,}".format(c["size"]) + " against a limit of "
                        + "{:,}".format(c["cap"]) + " for " + c["room"],
                 "notice": "gives only " + str(c["days"]) + " days of notice where "
                           + str(notice) + " are required",
                 "approve": "is in " + special + " without the required approval",
                 "weeks": "runs for " + str(c["weeks"]) + " weeks where " + str(weeks)
                          + " is the maximum"}
        item = {
            "id": None, "section": "DI", "type": "MSR", "sub": "Multi-source",
            "skill": "di_msr", "diff": self.diff,
            "stem": c["tag"] + " would satisfy every condition if which one of the "
                    "following single changes were made?",
            "choices": opts, "answer": opts.index(right),
            "expl": c["tag"] + " fails on exactly one condition: it " + names[rule]
                    + ". Applying each listed change in turn and re-checking every rule, "
                      "only " + right.lower() + " leaves a request that breaches nothing.",
            "wrong": "The other options each change something " + c["tag"]
                     + " already gets right, so the single real violation survives them.",
            "gen": self.id, "passageHtml": render(pol, notice, weeks, cases),
            "domain": "nonmath",
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


class WhichFails(MSRBase):
    """Which case fails on a named rule. Choices are the case tags."""
    id = "msr_which"
    diff = 3

    def make(self, rng, choices_n):
        pol, notice, weeks, cases = self.sources(rng)
        rule = rng.choice(["cap", "notice", "weeks"])
        hits = [c for c in cases if rule in c["bad"]]
        if len(hits) != 1:
            raise ItemError("msr_which needs exactly one case failing that rule")
        win = hits[0]["tag"]
        # The choices are the cases themselves, so a draw with fewer cases than the exam
        # has options would ship a short item. Drop it; the next draw may have five.
        if len(cases) < choices_n:
            raise ItemError("msr_which drew %d cases for a %d choice exam"
                            % (len(cases), choices_n))
        opts = [c["tag"] for c in cases][:choices_n]
        if win not in opts:
            raise ItemError("msr_which lost its key")
        rng.shuffle(opts)
        asked = {"cap": "exceeds the limit that applies to it",
                 "notice": "was submitted with less notice than the rules require",
                 "weeks": "runs for longer than the rules allow"}[rule]
        detail = {"cap": lambda c: "{:,}".format(c["size"]) + " against a limit of "
                                   + "{:,}".format(c["cap"]),
                  "notice": lambda c: str(c["days"]) + " days of notice against "
                                      + str(notice) + " required",
                  "weeks": lambda c: str(c["weeks"]) + " weeks against a maximum of "
                                     + str(weeks)}[rule]
        item = {
            "id": None, "section": "DI", "type": "MSR", "sub": "Multi-source",
            "skill": "di_msr", "diff": self.diff,
            "stem": "Which one of the " + pol["unit"] + "s listed " + asked + "?",
            "choices": opts, "answer": opts.index(win),
            "expl": " ".join(c["tag"] + ": " + detail(c) + "." for c in cases)
                    + " Only " + win + " breaches the rule asked about.",
            "wrong": "The other " + pol["unit"] + "s may fail on a different condition, "
                     "which is not what this question asks.",
            "gen": self.id, "passageHtml": render(pol, notice, weeks, cases),
            "domain": "nonmath",
        }
        self.verify(item, win, len(opts), fmt=str)
        return item


GENS = [CountCompliant(), SingleFix(), WhichFails()]
