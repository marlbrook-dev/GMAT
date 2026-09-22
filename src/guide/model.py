"""The shape of a guide topic, and the checks that keep one honest.

A topic page is four things a student needs and one thing only we can give them:

  idea     what the topic actually is, in a sentence, before any notation
  facts    the formulas, each with the plain English of what it says
  worked   examples worked all the way through, with the reasoning named
  traps    the specific wrong turns this topic invites
  ladder   what the question looks like at each difficulty the engine serves

The ladder is the part a static guide cannot do. The exam is adaptive, so "know
this topic" is not one thing: at level 1 a percent question asks you to take 20
percent of 80, and at level 5 it asks what happens to a quantity after a 20 percent
rise and a 20 percent fall. The ladder says that out loud, and build_guide pulls a
real item from our own bank at each level so the student sees it rather than reads
about it.
"""


class Topic:
    __slots__ = ("slug", "title", "area", "skill", "idea", "why",
                 "facts", "worked", "traps", "ladder")

    def __init__(self, slug, title, area, skill, idea, why,
                 facts=(), worked=(), traps=(), ladder=None):
        self.slug = slug
        self.title = title
        self.area = area
        self.skill = skill          # the trainer skill this maps to, so practice links work
        self.idea = idea
        self.why = why
        self.facts = list(facts)    # (name, expression, what it says in words)
        self.worked = list(worked)  # dicts: ask, steps, answer, why
        self.traps = list(traps)
        self.ladder = dict(ladder or {})

    def check(self):
        """Fail the build on a topic that is not finished.

        A half written page is worse than no page: a student who finds a heading with
        nothing under it stops trusting the rest of the guide. So a topic ships whole
        or not at all, and this says which part is missing rather than which topic.
        """
        bad = []
        if len(self.idea.split()) < 8:
            bad.append("idea is too short to be one")
        if len(self.why.split()) < 8:
            bad.append("why is too short to be one")
        if not self.facts:
            bad.append("no formulas")
        for name, expr, says in self.facts:
            if not (name and expr and says):
                bad.append("formula %r is missing a part" % (name or expr))
            if says and len(says.split()) < 4:
                bad.append("formula %r says nothing in words" % name)
        if not self.worked:
            bad.append("no worked example")
        for w in self.worked:
            if not w.get("ask") or not w.get("steps") or not w.get("answer"):
                bad.append("a worked example is missing its ask, steps or answer")
        if len(self.traps) < 2:
            bad.append("fewer than two traps named")
        missing = [d for d in (1, 2, 3, 4, 5) if not self.ladder.get(d)]
        if missing:
            bad.append("ladder has no rung at level %s" % ", ".join(map(str, missing)))
        return ["%s: %s" % (self.slug, b) for b in bad]


def check_all(topics):
    """Every topic finished, every slug unique, every skill one the engine knows."""
    bad = []
    seen = {}
    for t in topics:
        bad.extend(t.check())
        if t.slug in seen:
            bad.append("%s: two topics share this slug" % t.slug)
        seen[t.slug] = True
    return bad
