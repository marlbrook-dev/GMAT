"""GMAT Data Insights: Two-Part Analysis.

A TPA item gives one scenario and asks for two related values, one selected in each
column of a shared option list. That shape is what makes it a distinct skill: the two
answers are coupled, so a candidate who solves for one and guesses the other gets no
credit, and the wrong value for column A is usually the RIGHT value for column B.

The framework's multiple choice machinery does not apply here, because the answer is a
pair of indexes into one shared list rather than a single choice. So TwoPart builds the
option list itself, under three rules:

  The two keyed values are different, so a pair like (45, 45) cannot be read as one
  selection made twice.
  Every option is a value some plausible method actually produces, named in the
  explanation. A padding number nobody would compute teaches nothing.
  The keys land at random positions in a sorted list, so order carries no signal.

Everything is still computed. The scenarios are small linear systems whose solutions
are drawn first and whose totals are derived from them, which is why the arithmetic
always comes out whole.
"""
from framework import Gen, ItemError


def money(x):
    return "{:,}".format(int(round(x)))


class TwoPart(Gen):
    section = "DI"
    type = "TPA"
    skill = "di_tpa"
    sub = "Two-part"
    domain = "math"
    qskill = "q_alg"
    diff = 3

    def parts(self, rng):
        """Return (stem, columns, keyA, keyB, [(value, why), ...], expl)."""
        raise NotImplementedError

    def make(self, rng, choices_n):
        stem, columns, ka, kb, cands, expl = self.parts(rng)
        if ka == kb:
            raise ItemError("%s drew the same value twice" % self.id)
        keys = {money(ka), money(kb)}
        if len(keys) != 2:
            raise ItemError("%s keys collide once rendered" % self.id)
        opts, why = [], {}
        for v, w in cands:
            if v is None or v <= 0 or v != int(v):
                continue
            t = money(v)
            if t in keys or t in why:
                continue
            why[t] = w
            opts.append(t)
        need = 6 - 2
        if len(opts) < need:
            raise ItemError("%s has only %d usable decoys" % (self.id, len(opts)))
        pool = sorted(set(opts[:need]) | keys, key=lambda t: int(t.replace(",", "")))
        if len(pool) != 6:
            raise ItemError("%s built %d options, expected six" % (self.id, len(pool)))
        item = {
            "id": None, "section": "DI", "type": "TPA", "sub": "Two-part",
            "skill": "di_tpa", "diff": self.diff, "answerType": "tpa",
            "stem": stem + "\n\nIn the table, select " + columns[0].lower()
                    + " and select " + columns[1].lower()
                    + " consistent with the information given. Make only two selections, "
                      "one in each column.",
            "columns": list(columns), "choices": pool,
            "answer": [pool.index(money(ka)), pool.index(money(kb))],
            "expl": expl, "gen": self.id, "domain": "math", "qskill": "q_alg",
            "wrong": self._decoy_line(pool, keys, why),
        }
        self.verify_tpa(item, ka, kb)
        return item

    def _decoy_line(self, pool, keys, why):
        for t in pool:
            if t not in keys and t in why:
                return "The option " + t + " comes from " + why[t] + "."
        return ""

    def verify_tpa(self, item, ka, kb):
        c = item["choices"]
        if len(c) != 6 or len(set(c)) != 6:
            raise ItemError("%s option list is not six distinct values" % self.id)
        a, b = item["answer"]
        if a == b:
            raise ItemError("%s keys landed on one option" % self.id)
        if c[a] != money(ka) or c[b] != money(kb):
            raise ItemError("%s keys do not match the computed values" % self.id)
        self.verify_common(item)

    def verify_common(self, item):
        import json
        from framework import DASH
        if DASH.search(json.dumps(item)):
            raise ItemError("%s contains an em or en dash" % self.id)
        for k in ("stem", "expl"):
            if not item[k] or not str(item[k]).strip():
                raise ItemError("%s missing %s" % (self.id, k))
        if item["diff"] not in (1, 2, 3, 4, 5):
            raise ItemError("%s difficulty %r" % (self.id, item["diff"]))


# --- fixed fee plus a rate --------------------------------------------------------
JOBS = [("Brightwater Plumbing", "call-out fee", "hourly rate", "hours of labour", "job", 1),
        ("Calder Copy Centre", "setup charge", "price per copy", "copies", "order", 50),
        ("Merrow Van Hire", "base charge", "charge per mile", "miles", "rental", 20),
        ("Ferris Catering", "booking fee", "price per guest", "guests", "event", 10),
        ("Oakley Storage", "joining fee", "monthly charge", "months", "contract", 1)]


class FeePlusRate(TwoPart):
    id = "tpa_fee_rate"

    def parts(self, rng):
        firm, feename, ratename, unit, job, scale = rng.choice(JOBS)
        rate = (rng.choice([8, 12, 15, 18, 20, 24, 25, 30, 35, 40, 45, 50]) if scale == 1
                else rng.choice([1, 2, 3, 4, 5, 6, 8]))
        fee = rng.choice([20, 25, 30, 35, 40, 45, 50, 60, 65, 75, 80, 90])
        u1 = rng.randint(2, 6) * scale
        u2 = u1 + rng.randint(2, 5) * scale
        t1, t2 = fee + rate * u1, fee + rate * u2
        stem = (firm + " charges every customer a fixed " + feename + " plus a "
                + ratename + ". One " + job + " involving " + str(u1) + " " + unit
                + " came to a total of $" + money(t1) + ", and another involving "
                + str(u2) + " " + unit + " came to a total of $" + money(t2) + ".")
        cands = [
            (t1 // u1, "dividing the first total by its " + unit
             + ", which charges the fixed " + feename + " to every unit"),
            (t2 // u2, "dividing the second total by its " + unit + " in the same way"),
            (t2 - t1, "the difference between the two totals, which is the cost of the "
             "extra " + unit + " rather than either quantity asked for"),
            (rate * u1, "the labour portion of the first " + job
             + " rather than the " + ratename),
            (fee + rate, "adding one unit's charge to the " + feename),
            (rate * 2, "doubling the " + ratename + " for no stated reason"),
            (fee * 2, "doubling the " + feename),
            (t1 - rate, "subtracting a single unit's charge from the first total"),
        ]
        expl = ("Let f be the " + feename + " and r the " + ratename + ". Then f + "
                + str(u1) + "r = " + money(t1) + " and f + " + str(u2) + "r = "
                + money(t2) + ". Subtracting gives " + str(u2 - u1) + "r = "
                + money(t2 - t1) + ", so r = " + money(rate) + ". Substituting back, f = "
                + money(t1) + " - " + str(u1) + " x " + money(rate) + " = " + money(fee) + ".")
        return stem, (ratename.capitalize() + " (dollars)", feename.capitalize() + " (dollars)"), \
            rate, fee, cands, expl


# --- two products, two constraints -------------------------------------------------
MIXES = [("Harlow Bakery", "sourdough loaves", "rye loaves", "loaves"),
         ("Pinecrest Nursery", "maple saplings", "birch saplings", "saplings"),
         ("Ardell Press", "hardcover copies", "paperback copies", "copies"),
         ("Granby Cycles", "road frames", "touring frames", "frames"),
         ("Selby Ceramics", "glazed tiles", "matte tiles", "tiles")]


class TwoGoods(TwoPart):
    id = "tpa_two_goods"

    def parts(self, rng):
        firm, ga, gb, noun = rng.choice(MIXES)
        pa = rng.choice([4, 5, 6, 8, 9, 10, 12, 15])
        pb = rng.choice([3, 7, 11, 13, 14, 16, 18, 20])
        if pa == pb:
            raise ItemError("prices must differ")
        na = rng.randint(12, 90)
        nb = rng.randint(12, 90)
        if na == nb:
            raise ItemError("counts must differ")
        count = na + nb
        rev = pa * na + pb * nb
        stem = (firm + " sold " + money(count) + " " + noun + " in a single day, some of "
                "them " + ga + " at $" + money(pa) + " each and the rest " + gb + " at $"
                + money(pb) + " each. The day's takings from these " + noun + " were $"
                + money(rev) + ".")
        cands = [
            (count - na - 1, "an off by one count of the " + gb),
            (rev // (pa + pb), "dividing the takings by the two prices added together"),
            (count // 2, "splitting the " + noun + " evenly between the two kinds"),
            (rev // pa, "pricing every one of the " + noun + " as " + ga),
            (rev // pb, "pricing every one of the " + noun + " as " + gb),
            (count - na + 2, "a miscount of the " + gb + " by two"),
            (abs(na - nb), "the difference between the two counts rather than either count"),
            (count, "the combined count rather than either kind on its own"),
        ]
        # Neither kind can outnumber the whole day's sales, so a decoy above the total
        # is spotted without doing any work.
        cands = [(v, w) for v, w in cands if v is not None and v <= count]
        lo, hi = min(pa, pb), max(pa, pb)
        hiname, hin = (ga, na) if pa > pb else (gb, nb)
        expl = ("Let a be the number of " + ga + " and b the number of " + gb + ". Then a + b = "
                + money(count) + " and " + money(pa) + "a + " + money(pb) + "b = " + money(rev)
                + ". Multiplying the count equation by " + money(lo) + " gives " + money(lo)
                + "a + " + money(lo) + "b = " + money(lo * count) + ". Subtracting that from the "
                "takings equation leaves " + money(hi - lo) + " times the number of " + hiname
                + ", so " + money(rev) + " - " + money(lo * count) + " = " + money(rev - lo * count)
                + " and the number of " + hiname + " is " + money(hin) + ". The other kind makes "
                "up the rest: " + money(count) + " - " + money(hin) + " = " + money(count - hin) + ".")
        return stem, ("Number of " + ga, "Number of " + gb), na, nb, cands, expl


# --- a rate and a time from two legs ------------------------------------------------
TRIPS = [("a delivery van", "the depot", "the distribution centre"),
         ("a survey launch", "the harbour", "the offshore platform"),
         ("a shuttle bus", "the terminal", "the long stay car park"),
         ("a freight train", "the yard", "the river crossing")]


class SpeedAndTime(TwoPart):
    id = "tpa_speed_time"

    def parts(self, rng):
        what, start, end = rng.choice(TRIPS)
        back = rng.choice([24, 30, 32, 36, 40, 42, 45, 48, 50, 54, 60])
        backh = rng.choice([3, 4, 5, 6, 8])
        dist = back * backh
        faster = [d for d in range(back + 5, back * 2 + 1)
                  if dist % d == 0 and dist // d < backh and d - back in (6, 8, 10, 12, 15, 20, 24)]
        if not faster:
            raise ItemError("no outbound speed gives whole hours both ways")
        speed = rng.choice(faster)
        slower = speed - back
        hours = dist // speed
        stem = (what.capitalize() + " travels from " + start + " to " + end + " at a steady "
                + money(speed) + " kilometres per hour, taking " + money(hours)
                + " hours. It returns along the same route at a steady speed "
                + money(slower) + " kilometres per hour slower than it went out.")
        cands = [
            (hours, "the outbound time, which the question does not ask for"),
            (speed, "the outbound speed rather than the return speed"),
            (dist, "the distance, which is neither quantity asked for"),
            (speed + slower, "adding the difference in speed rather than subtracting it"),
            (backh + 1, "an off by one on the return time"),
            (dist // speed + slower, "adding the speed difference to the outbound time"),
            (2 * hours, "doubling the outbound time instead of computing the slower leg"),
            (slower, "the difference in speed rather than the return speed"),
            (hours + backh, "the round trip time rather than the return leg alone"),
            (backh - 1, "an off by one on the return time in the other direction"),
        ]
        expl = ("The outbound leg covers " + money(speed) + " x " + money(hours) + " = "
                + money(dist) + " kilometres. The return speed is " + money(speed) + " - "
                + money(slower) + " = " + money(back) + " kilometres per hour, so the return "
                "takes " + money(dist) + "/" + money(back) + " = " + money(backh) + " hours.")
        return stem, ("Return speed (km per hour)", "Return time (hours)"), back, backh, cands, expl


# --- percent of a base --------------------------------------------------------------
BUDGETS = [("Hollis District Council", "the roads budget", "the parks budget"),
           ("Trenton Labs", "the equipment budget", "the training budget"),
           ("Caraway Foods", "the packaging budget", "the haulage budget"),
           ("Vale Academy", "the library budget", "the sports budget")]


class SplitBudget(TwoPart):
    id = "tpa_budget"

    def parts(self, rng):
        org, ba, bb = rng.choice(BUDGETS)
        total = rng.choice([40, 50, 60, 80, 100, 120, 150, 200]) * 1000
        share = rng.choice([15, 20, 25, 30, 35, 40, 45])
        a = total * share // 100
        rest = total - a
        pctb = rng.choice([20, 25, 40, 50, 60, 75])
        b = rest * pctb // 100
        if b == a or b <= 0:
            raise ItemError("the two amounts must differ")
        stem = (org + " divides a budget of $" + money(total) + " among several lines. "
                + ba.capitalize() + " takes " + money(share) + " percent of the whole "
                "budget, and " + bb + " takes " + money(pctb) + " percent of what is left "
                "after " + ba + " is funded.")
        cands = [
            (total * pctb // 100, "taking " + money(pctb) + " percent of the whole budget "
             "rather than of what remains"),
            (rest, "what is left after " + ba + ", before " + bb + " takes its share"),
            (total - a - b, "what remains after both lines are funded"),
            (total * (share + pctb) // 100, "adding the two percentages and applying them "
             "to the whole budget"),
            (a + b, "the two lines added together"),
            (total // 2, "splitting the budget evenly"),
            (abs(a - b), "the gap between the two lines rather than either line"),
        ]
        expl = (ba.capitalize() + " takes " + money(share) + " percent of $" + money(total)
                + " = $" + money(a) + ". That leaves $" + money(total) + " - $" + money(a)
                + " = $" + money(rest) + ", and " + bb + " takes " + money(pctb)
                + " percent of that: $" + money(b) + ".")
        return stem, (ba.capitalize() + " (dollars)", bb.capitalize() + " (dollars)"), \
            a, b, cands, expl


GENS = [FeePlusRate(), TwoGoods(), SpeedAndTime(), SplitBudget()]
