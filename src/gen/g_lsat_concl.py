"""Must be true, from statements about who has which property (lsat_lr_concl).

LSAC lists drawing well-supported conclusions among the skills Logical Reasoning measures,
and the category that carries it here had 31 hand written items and no generator: the
mapping in mapping.py found nothing in the critical reasoning pool that asks it. One kind
of that question can be generated honestly, because its answer can be PROVED rather than
judged: a handful of statements using every, no, some and most, and a question asking what
must also be true. Reading those quantity words exactly as written is one of the points the
category promises.

So every item here is checked by brute force, not by the author's reading. A statement
about three properties is true or false of a group of people depending only on how many of
them fall into each of the eight combinations of the three, so the checker enumerates
every group with up to MAXC people in each combination and keeps, as a truth table, which
of the 36 possible statements hold in each. The key must hold in every group where the
premises hold; each wrong answer must fail in at least one of them, which is a
counterexample, so it could be false. Nothing is asserted by hand.

Semantics follow the test's own conventions, and are the ones that make these questions
hard: "some" means at least one and possibly all; "most" means more than half; "every"
does not say that there is anyone of the kind at all.

Each pattern is a pair of premises whose combination licenses one conclusion that neither
premise gives alone, with the explanation of why written for that pattern. The
combination is the question; a key that restates one premise would test nothing, and the
checker refuses one. A third premise is sometimes added that bears on the same people and
licenses nothing new about the pair the key is about, which is what a real stimulus does
to a reader who has not worked out which statements matter.
"""
import itertools
import zlib

from framework import ItemError
from g_gmat_cr import CRBase

FORMS = ("all", "no", "some", "somenot", "most", "mostnot")
# Up to this many people of each of the eight kinds. Three is enough for every
# counterexample these patterns need, and check_logic confirms it against four.
MAXC = 3


def _tables(maxc):
    """Truth table of every statement (form, a, b) over every group, as bitsets.

    A group is numbered by its eight counts read as the digits of a base maxc+1 number,
    and bit m of a statement's table says whether the statement holds in group m. The
    tables are built from D[kind][v], the groups with exactly v people of that kind, so a
    statement's table is a union of intersections rather than a loop over every group:
    building them group by group made the bound check take 23 seconds, and this takes
    well under one.
    """
    base = maxc + 1
    n = base ** 8
    D = [[int((("0" * (v * base ** t) + "1" * base ** t + "0" * ((base - 1 - v) * base ** t))
               * base ** (7 - t))[::-1], 2) for v in range(base)] for t in range(8)]
    atoms = [(f, a, b) for f in FORMS for a in range(3) for b in range(3) if a != b]
    bits = {}
    for a in range(3):
        for b in range(3):
            if a == b:
                continue
            yes = [t for t in range(8) if t >> a & 1 and t >> b & 1]
            no = [t for t in range(8) if t >> a & 1 and not t >> b & 1]
            by = {}
            for c1 in range(base):
                for c2 in range(base):
                    s12 = D[yes[0]][c1] & D[yes[1]][c2]
                    for c3 in range(base):
                        s123 = s12 & D[no[0]][c3]
                        for c4 in range(base):
                            k = (c1 + c2, c3 + c4)
                            by[k] = by.get(k, 0) | (s123 & D[no[1]][c4])
            rule = {"all": lambda y, x: x == 0, "no": lambda y, x: y == 0,
                    "some": lambda y, x: y > 0, "somenot": lambda y, x: x > 0,
                    "most": lambda y, x: y > x, "mostnot": lambda y, x: x > y}
            for f in FORMS:
                acc = 0
                for (y, x), m in by.items():
                    if rule[f](y, x):
                        acc |= m
                bits[(f, a, b)] = acc
    return atoms, bits, (1 << n) - 1


ATOMS, BITS, FULL = _tables(MAXC)


def holds_where(premises, bits=None, full=None):
    bits, full = bits or BITS, full or FULL
    s = full
    for p in premises:
        s &= bits[p]
    return s


def valid(premises, stmt, bits=None, full=None):
    """True when stmt holds in every group in which all the premises hold."""
    bits = bits or BITS
    s = holds_where(premises, bits, full)
    return s != 0 and s & ~bits[stmt] == 0


# The groups in which there is at least one person with property a. "Some" and "most"
# say that there is; "every" and "no" do not, which is the trap in a wrong answer that
# would follow if only anyone of the kind existed.
EXISTS = [BITS[("some", a, (a + 1) % 3)] | BITS[("somenot", a, (a + 1) % 3)] for a in range(3)]


def valid_if_any(premises, stmt, who):
    """Valid once it is also given that someone has each property in `who`."""
    s = holds_where(premises)
    for a in who:
        s &= EXISTS[a]
    return s != 0 and s & ~BITS[stmt] == 0


# The same claim written two ways. "No A is B" and "no B is A" say one thing, as do the
# two orders of "some"; offering both would put the same claim on the page twice.
def same_claim(x, y):
    if x == y:
        return True
    return (x[0] == y[0] and x[0] in ("no", "some") and x[1] == y[2] and x[2] == y[1])


# Premises over p=0, q=1, r=2, the conclusion they license, and why. The first premise
# list is the stimulus order.
PATTERNS = [
    dict(key="chain", prem=[("all", 0, 1), ("all", 1, 2)], concl=("all", 0, 2), diff=2),
    dict(key="allno", prem=[("all", 0, 1), ("no", 1, 2)], concl=("no", 0, 2), diff=3),
    dict(key="someall", prem=[("some", 0, 1), ("all", 1, 2)], concl=("some", 0, 2), diff=3),
    dict(key="mostmost", prem=[("most", 0, 1), ("most", 0, 2)], concl=("some", 1, 2), diff=4),
    dict(key="mostall", prem=[("most", 0, 1), ("all", 1, 2)], concl=("most", 0, 2), diff=4),
    dict(key="allsomenot", prem=[("all", 0, 1), ("somenot", 2, 1)], concl=("somenot", 2, 0), diff=4),
    dict(key="nosome", prem=[("no", 0, 1), ("some", 2, 0)], concl=("somenot", 2, 1), diff=3),
    dict(key="allsome", prem=[("all", 0, 1), ("some", 2, 0)], concl=("some", 2, 1), diff=3),
    dict(key="noall", prem=[("no", 0, 1), ("all", 2, 1)], concl=("no", 2, 0), diff=3),
]

# rel is the relative pronoun the domain's nouns take. Every property is written out in
# all four shapes the sentences need: the derivation of a plural or a negative from a
# singular is where the assumption hides (INC-0087).
SCENES = [
    dict(intro="At Verdant Logistics", sg="employee", pl="employees", rel="who", props=[
        ("works night shifts", "work night shifts", "does not work night shifts", "do not work night shifts"),
        ("holds a forklift licence", "hold a forklift licence", "does not hold a forklift licence", "do not hold a forklift licence"),
        ("is paid by the hour", "are paid by the hour", "is not paid by the hour", "are not paid by the hour"),
        ("belongs to the union", "belong to the union", "does not belong to the union", "do not belong to the union"),
        ("has been with the firm for over five years", "have been with the firm for over five years",
         "has not been with the firm for over five years", "have not been with the firm for over five years"),
    ]),
    dict(intro="At Fenmore College", sg="student", pl="students", rel="who", props=[
        ("lives on campus", "live on campus", "does not live on campus", "do not live on campus"),
        ("receives a scholarship", "receive a scholarship", "does not receive a scholarship", "do not receive a scholarship"),
        ("plays a varsity sport", "play a varsity sport", "does not play a varsity sport", "do not play a varsity sport"),
        ("studies a science", "study a science", "does not study a science", "do not study a science"),
        ("works part time", "work part time", "does not work part time", "do not work part time"),
    ]),
    dict(intro="In the Aldine collection", sg="painting", pl="paintings", rel="that", props=[
        ("dates from before 1800", "date from before 1800", "does not date from before 1800", "do not date from before 1800"),
        ("is on permanent display", "are on permanent display", "is not on permanent display", "are not on permanent display"),
        ("was donated by a private collector", "were donated by a private collector",
         "was not donated by a private collector", "were not donated by a private collector"),
        ("has been restored", "have been restored", "has not been restored", "have not been restored"),
        ("is attributed to a named artist", "are attributed to a named artist",
         "is not attributed to a named artist", "are not attributed to a named artist"),
    ]),
    dict(intro="At the Bellweather food bank", sg="volunteer", pl="volunteers", rel="who", props=[
        ("drives a delivery route", "drive a delivery route", "does not drive a delivery route", "do not drive a delivery route"),
        ("works on weekends", "work on weekends", "does not work on weekends", "do not work on weekends"),
        ("speaks Spanish", "speak Spanish", "does not speak Spanish", "do not speak Spanish"),
        ("is trained in first aid", "are trained in first aid", "is not trained in first aid", "are not trained in first aid"),
        ("joined this year", "joined this year", "did not join this year", "did not join this year"),
    ]),
    dict(intro="On Wren Lane", sg="house", pl="houses", rel="that", props=[
        ("has solar panels", "have solar panels", "does not have solar panels", "do not have solar panels"),
        ("was built before 1950", "were built before 1950", "was not built before 1950", "were not built before 1950"),
        ("has a garage", "have a garage", "does not have a garage", "do not have a garage"),
        ("is rented out", "are rented out", "is not rented out", "are not rented out"),
        ("has a garden facing south", "have a garden facing south", "does not have a garden facing south",
         "do not have a garden facing south"),
    ]),
    dict(intro="In the Delmore business park", sg="firm", pl="firms", rel="that", props=[
        ("exports its products", "export their products", "does not export its products", "do not export their products"),
        ("employs more than fifty people", "employ more than fifty people", "does not employ more than fifty people",
         "do not employ more than fifty people"),
        ("was founded after 2010", "were founded after 2010", "was not founded after 2010", "were not founded after 2010"),
        ("leases its premises", "lease their premises", "does not lease its premises", "do not lease their premises"),
        ("has a research unit", "have a research unit", "does not have a research unit", "do not have a research unit"),
    ]),
    dict(intro="At the Harwick Rowing Club", sg="member", pl="members", rel="who", props=[
        ("rows in a racing crew", "row in a racing crew", "does not row in a racing crew", "do not row in a racing crew"),
        ("coaches the juniors", "coach the juniors", "does not coach the juniors", "do not coach the juniors"),
        ("serves on a committee", "serve on a committee", "does not serve on a committee", "do not serve on a committee"),
        ("lives within walking distance of the boathouse", "live within walking distance of the boathouse",
         "does not live within walking distance of the boathouse", "do not live within walking distance of the boathouse"),
        ("joined before 2020", "joined before 2020", "did not join before 2020", "did not join before 2020"),
    ]),
    dict(intro="In the Larch Street building", sg="tenant", pl="tenants", rel="who", props=[
        ("keeps a pet", "keep a pet", "does not keep a pet", "do not keep a pet"),
        ("pays rent monthly", "pay rent monthly", "does not pay rent monthly", "do not pay rent monthly"),
        ("has lived there for over a decade", "have lived there for over a decade",
         "has not lived there for over a decade", "have not lived there for over a decade"),
        ("sits on the tenants' committee", "sit on the tenants' committee", "does not sit on the tenants' committee",
         "do not sit on the tenants' committee"),
        ("owns a car", "own a car", "does not own a car", "do not own a car"),
    ]),
    dict(intro="Among the bird species recorded on Selby Island", sg="species", pl="species", rel="that", props=[
        ("nests on the cliffs", "nest on the cliffs", "does not nest on the cliffs", "do not nest on the cliffs"),
        ("migrates in winter", "migrate in winter", "does not migrate in winter", "do not migrate in winter"),
        ("feeds mainly on fish", "feed mainly on fish", "does not feed mainly on fish", "do not feed mainly on fish"),
        ("is protected by law", "are protected by law", "is not protected by law", "are not protected by law"),
        ("was recorded in the last survey", "were recorded in the last survey", "was not recorded in the last survey",
         "were not recorded in the last survey"),
    ]),
    dict(intro="In the Castell Orchestra", sg="musician", pl="musicians", rel="who", props=[
        ("plays a string instrument", "play a string instrument", "does not play a string instrument",
         "do not play a string instrument"),
        ("teaches privately", "teach privately", "does not teach privately", "do not teach privately"),
        ("has a permanent contract", "have a permanent contract", "does not have a permanent contract",
         "do not have a permanent contract"),
        ("composes music", "compose music", "does not compose music", "do not compose music"),
        ("lives outside the city", "live outside the city", "does not live outside the city", "do not live outside the city"),
    ]),
]

STEMS = ("If the statements above are true, which one of the following must also be true?",
         "If all of the statements above are true, which one of the following must be true?")


class Words:
    """One draw's vocabulary: a scene and three of its properties, as p, q and r."""

    def __init__(self, scene, idx):
        self.s = scene
        self.p = [scene["props"][i] for i in idx]

    def who_sg(self, a):
        return "%s %s %s" % (self.s["sg"], self.s["rel"], self.p[a][0])

    def who_pl(self, a):
        return "%s %s %s" % (self.s["pl"], self.s["rel"], self.p[a][1])

    def say(self, st):
        """A statement as a sentence without its full stop, starting in lower case."""
        f, a, b = st
        sg, pl, nsg, npl = self.p[b]
        if f == "all":
            return "every %s %s" % (self.who_sg(a), sg)
        if f == "no":
            return "no %s %s" % (self.who_sg(a), sg)
        if f == "some":
            return "some %s %s" % (self.who_pl(a), pl)
        if f == "somenot":
            return "some %s %s" % (self.who_pl(a), npl)
        if f == "most":
            return "most %s %s" % (self.who_pl(a), pl)
        return "most %s %s" % (self.who_pl(a), npl)

    def sentence(self, st):
        t = self.say(st)
        return t[0].upper() + t[1:] + "."


def why_follows(w, pat, prem):
    """The reasoning that licenses the conclusion, written per pattern."""
    k = pat["key"]
    P, Q, R = (w.who_pl(i) for i in range(3))
    rel, pl = w.s["rel"], w.s["pl"]
    (p_sg, p_pl, p_nsg, p_npl), (q_sg, q_pl, q_nsg, q_npl), (r_sg, r_pl, r_nsg, r_npl) = w.p
    if k == "chain":
        return "All %s %s, and all %s %s, so all %s %s." % (P, q_pl, Q, r_pl, P, r_pl)
    if k == "allno":
        return ("All %s %s, and no %s %s, so no %s %s."
                % (P, q_pl, w.who_sg(1), r_sg, w.who_sg(0), r_sg))
    if k == "someall":
        return ("Some %s %s, and all %s %s, so those %s %s too, which means some %s %s."
                % (P, q_pl, Q, r_pl, pl, r_pl, P, r_pl))
    if k == "mostmost":
        return ("More than half of the %s %s, and more than half of them %s. Two groups that "
                "each take in more than half of the same %s must overlap, so at least one of "
                "them does both, which means some %s %s." % (P, q_pl, r_pl, pl, Q, r_pl))
    if k == "mostall":
        return ("More than half of the %s %s, and all %s %s, so more than half of the %s %s."
                % (P, q_pl, Q, r_pl, P, r_pl))
    if k == "allsomenot":
        return ("All %s %s, so none of the %s %s %s can be among them. Some %s %s, so those "
                "%s %s, which means some %s %s." % (P, q_pl, pl, rel, q_npl, R, q_npl, pl,
                                                    p_npl, R, p_npl))
    if k == "nosome":
        return ("Some %s %s, and no %s %s, so those %s %s, which means some %s %s."
                % (R, p_pl, w.who_sg(0), q_sg, pl, q_npl, R, q_npl))
    if k == "allsome":
        return ("Some %s %s, and all %s %s, so those %s %s too, which means some %s %s."
                % (R, p_pl, P, q_pl, pl, q_pl, R, q_pl))
    if k == "noall":
        return ("All %s %s, and no %s %s, so no %s %s."
                % (R, q_pl, w.who_sg(1), p_sg, w.who_sg(2), p_sg))
    raise ValueError(k)


def why_not(w, st, prem, concl):
    """Why a wrong answer is wrong, as specifically as the checker's verdict allows.

    Every reason here is decided by the checker, not asserted: a statement that no group
    satisfying the premises makes true is called impossible, and one that some group
    makes false is called one that could be false.
    """
    f, a, b = st
    if holds_where(list(prem) + [st]) == 0:
        return "cannot be true: it contradicts what the statements say"
    if valid_if_any(prem, st, [a]):
        return ("would follow only if there were any %s %s %s, and the statements never say "
                "there are" % (w.s["pl"], w.s["rel"], w.p[a][1]))
    for pf, pa, pb in prem:
        if pf == "all" and f == "all" and (a, b) == (pb, pa):
            return ("reverses an every statement: that every %s %s does not mean that every "
                    "%s %s" % (w.who_sg(pa), w.p[pb][0], w.who_sg(pb), w.p[pa][0]))
    if f == "somenot" and ("some", a, b) in prem:
        return ("mistakes some for not all: that some of them do leaves open that every one "
                "of them does")
    if {a, b} == {concl[1], concl[2]}:
        return ("may be true, but the statements require only that " + w.say(concl))
    if f in ("most", "mostnot") and not any(p[0] in ("most", "mostnot") and p[1] == a
                                            for p in prem):
        return "reads a majority into statements that give no proportion for this group"
    return "could be false: the statements hold just as well in a case where it fails"


class MustBeTrue(CRBase):
    """What must also be true, given statements quantified by every, no, some and most."""
    id = "lsat_concl_quant"
    skill = "lsat_lr_concl"
    section = "LR"
    type = "LR"
    sub = "Must be true"
    diff = 3

    def make(self, rng, choices_n):
        pat = rng.choice(PATTERNS)
        scene = rng.choice(SCENES)
        idx = rng.sample(range(len(scene["props"])), 3)
        w = Words(scene, idx)
        prem = list(pat["prem"])
        concl = pat["concl"]
        diff = pat["diff"]
        # A third premise, half the time. It must be consistent with the others, must say
        # something they do not say even once every group is taken to have members (so
        # never "no X is Y" beside "most X are not Y"), and must tell the reader nothing
        # new about the pair the key is about.
        if rng.random() < 0.5:
            spare = [at for at in ATOMS
                     if not same_claim(at, concl) and at not in prem
                     and {at[1], at[2]} != {concl[1], concl[2]}
                     and holds_where(prem + [at]) != 0
                     and not valid(prem, at)
                     and not valid_if_any(prem, at, [0, 1, 2])
                     and not any(valid(prem + [at], x) and not valid(prem, x)
                                 for x in ATOMS if {x[1], x[2]} == {concl[1], concl[2]})]
            if spare:
                prem.append(rng.choice(spare))
                diff = min(5, diff + 1)
        if holds_where(prem) == 0:
            raise ItemError("%s: premises cannot all be true" % self.id)
        if not valid(prem, concl):
            raise ItemError("%s: the key does not follow" % self.id)
        # The combination is the question. A key one premise gives alone tests nothing.
        if any(valid([x], concl) for x in prem):
            raise ItemError("%s: one premise alone gives the key" % self.id)
        # "No A is B" and "no B is A" are one claim, as are the two orders of "some", so
        # the key is written either way round. Always writing it one way made those keys
        # the shortest option far more often than chance, and the longest far less.
        shown = concl
        if concl[0] in ("no", "some") and rng.random() < 0.5:
            shown = (concl[0], concl[2], concl[1])
        sentences = [w.sentence(x) for x in prem]
        first = scene["intro"] + ", " + sentences[0][0].lower() + sentences[0][1:]
        stim = " ".join([first] + sentences[1:])
        stem = stim + "\n\n" + STEMS[zlib.crc32(stim.encode()) % len(STEMS)]
        right = w.sentence(shown)
        wrongs, used = [], [concl]
        # Shuffled, so which way round a symmetric wrong answer is written is left to
        # chance for the same reason as the key's.
        for at in rng.sample(ATOMS, len(ATOMS)):
            if at in prem or any(same_claim(at, u) for u in used) or valid(prem, at):
                continue
            used.append(at)
            wrongs.append((w.sentence(at), why_not(w, at, prem, shown)))
        # Nearest first: a wrong answer about the key's own pair, or the converse of a
        # premise, is the one a careless reader picks, so those are what get offered.
        def pull(item):
            text = item[0]
            st = next(a for a in ATOMS if w.sentence(a) == text)
            near = {st[1], st[2]} == {concl[1], concl[2]}
            conv = any(p[0] == "all" and st == ("all", p[2], p[1]) for p in prem)
            return (0 if near or conv else 1, rng.random())
        wrongs.sort(key=pull)
        wrongs = wrongs[:max(choices_n + 15, 20)]
        expl = why_follows(w, pat, prem)
        if shown != concl:
            expl += " Put the other way round, " + w.say(shown) + "."
        item = self.emit(rng, choices_n, stem, right, wrongs, expl, diff, self.skill, self.sub)
        item["section"] = "LR"
        item["type"] = "LR"
        # Identity is the argument, not which of its wrong answers were offered: a student
        # who has worked out what must be true of one stimulus has answered it.
        item["canon_ignores_choices"] = True
        for c in item["choices"]:
            st = next(a for a in ATOMS if w.sentence(a) == c)
            if (c == right) != valid(prem, st) or (c == right) != same_claim(st, concl):
                raise ItemError("%s: the checker disagrees with the key on %r" % (self.id, c))
        return item


GENS = [MustBeTrue()]


def check_logic():
    """Every pattern's key follows and needs both premises, confirmed with a bigger bound.

    MAXC bounds the groups the checker tries. A bound too small could miss the only
    counterexample to a wrong answer and so certify it as a second correct one. This
    recomputes validity for every pattern and every statement with one more person per
    kind and returns what disagrees, which should be nothing.
    """
    atoms4, bits4, full4 = _tables(MAXC + 1)
    bad = []
    for pat in PATTERNS:
        prem = pat["prem"]
        if not valid(prem, pat["concl"], bits4, full4):
            bad.append("%s: key does not follow" % pat["key"])
        for x in prem:
            if valid([x], pat["concl"], bits4, full4):
                bad.append("%s: one premise gives the key" % pat["key"])
        for extra in [None] + ATOMS:
            ps = prem + ([extra] if extra else [])
            if holds_where(ps) == 0:
                continue
            for at in ATOMS:
                if valid(ps, at) != valid(ps, at, bits4, full4):
                    bad.append("%s + %s: %s differs between bounds" % (pat["key"], extra, at))
    return bad
