"""Generate the item banks from the schemas in src/gen/.

The generators are the source of truth; the emitted .js files are build output and
are gitignored, exactly like /app/ and /blog/. The run is seeded with crc32 of the
exam and category name, so the same commit always produces the same bank. It must
not use Python's hash(), which is randomised per process and quietly made every
build produce a different bank.

Run directly to see the per category report:  python3 src/build_banks.py
"""
import math
import pathlib
import random
import re
import sys
import zlib
from collections import Counter

D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D / "gen"))

import framework as F          # noqa: E402
import mapping as M            # noqa: E402
import g_sat_alg, g_sat_adv, g_sat_psda, g_sat_geo   # noqa: E402,F401
import g_sat_rw, g_gmat_ds, g_act_kol                # noqa: E402,F401
import g_gmat_gt, g_gmat_tpa, g_gmat_msr             # noqa: E402,F401
import g_act_sci, g_gre_verb, g_gmat_cr, g_act_nq    # noqa: E402,F401
import g_rc, g_flaw                                  # noqa: E402,F401

OUT = D / "generated"

# Per category, set to what the schemas can actually produce rather than to a round
# number. 42 categories across the five generated exams, plus 1,852 hand written items.
# Both figures were wrong here until they were counted: this said 34 categories and 1,073
# hand written items "including all 65 LSAT ones, which have no generator", when the LSAT
# had 372 hand written items and now has a generator too.
#
# Five categories exhaust their parameter space below this and ship at their own ceiling
# instead. That is reported, not silent: build_banks prints "categories under target" and
# names the schemas that ran out.
#
#   gmat/v_pc        833   cr_plan_assume, cr_plan_eval, cr_plan_weaken
#   gmat/v_ac      1,422   cr_cause_assume, cr_cause_weaken, cr_necessary, cr_percent,
#                          cr_sample
#   gmat/q_vof     1,967   the five sat_adv_* schemas, remapped
#   sat/rw_sec     2,489   sat_rw_apostrophe, sat_rw_boundary, sat_rw_pronoun, sat_rw_sva
#   act/act_e_cse  2,507   the same four, remapped
#
# The three LSAT Logical Reasoning categories all reach the target, on the same CR
# schemas that fall short under the GMAT taxonomy, because the LSAT groups them
# differently: five schemas feed lsat_lr_evid where the GMAT splits the same five across
# v_ac and v_pc. Its three Reading categories do not, and neither do the two GMAT reading
# ones, for the reason given against v_st below: the count there is gated on how many
# passages are written and no generator cleverness changes that.
#
# The generated bank is 122,380 items and the build counts a published total of 124,232
# with the hand written banks. Both figures are printed by the build rather than taken
# from here; a number in a comment is a number nobody regenerates.
#
# sat/rw_eoi and act/act_e_pow were on this list at 971 and 974 until sat_rw_synthesis
# was written. Both are now at target, and the fix was a second schema rather than a
# wider one: the category held one template, and Expression of Ideas holds two published
# skills, so half the domain had no items at all.
#
# On why 3300 and not more. The ceilings were measured by running at 4000: 24 categories
# still had room there and the total came to 118,447, so the parameter space is not the
# binding constraint. Size is. The deferred remainder grows roughly linearly with this
# number while the blocking download does not, because the starter is strided at
# STARTER_PER_SKILL per skill and is the same size whatever this is set to. 3300 is the
# smallest round value that clears one hundred thousand items, which keeps the deferred
# download as small as that goal allows.
#
# The older caution still stands and is worth re-reading before raising it again: a
# category built on a single schema becomes variations on one template at scale, so past
# a point a new schema is worth far more than a larger number. That is what closed
# sat/rw_eoi and act/act_e_pow. gre/gre_se and gre/gre_tc are the two still on one
# schema each, and are the next places a second schema would pay.
TARGET = 3300

# How many items per skill ship in the blocking starter file. Eighty is several rounds
# per skill, so a student reaches the deferred remainder long after it has arrived, while
# keeping the blocking download around a tenth of the full bank.
STARTER_PER_SKILL = 80

# The SAT modules are the shared quantitative and writing pool every exam remaps from.
# g_gmat_cr and g_flaw join it because the LSAT map draws on the Critical Reasoning and
# flaw schemas; they still reach the GMAT through EXAM_EXTRA, which is where a schema
# authored against one exam's own taxonomy belongs.
POOL_MODS = [g_sat_alg, g_sat_adv, g_sat_psda, g_sat_geo, g_sat_rw, g_gmat_cr, g_flaw]
# The LSAT reading map names the _long variants, which live in GENS_LONG rather than
# GENS, so that list is added to the pool by hand.
POOL_EXTRA = list(g_rc.GENS_LONG)

# SAT categories are authored directly against SAT taxonomy; the other exams remap.
SAT_PLAN = {
    "m_alg": g_sat_alg.GENS,
    "m_adv": g_sat_adv.GENS,
    "m_psda": g_sat_psda.GENS,
    "m_geo": g_sat_geo.GENS,
    "rw_sec": [g for g in g_sat_rw.GENS if g.skill == "rw_sec"],
    "rw_eoi": [g for g in g_sat_rw.GENS if g.skill == "rw_eoi"],
}

# Categories authored directly against an exam's own taxonomy rather than remapped.
# Data Sufficiency has no SAT counterpart, so it lives here.
EXAM_EXTRA = {"gre": {"gre_tc": [g for g in g_gre_verb.GENS if g.skill == "gre_tc"],
                      "gre_se": [g for g in g_gre_verb.GENS if g.skill == "gre_se"]},
              "gmat": {"di_ds": g_gmat_ds.GENS,
                       # Analysis / Critique, including the flaw schemas. g_flaw adds
                       # three named patterns beside cr_sample, which was the only one
                       # this category had and the reason lsat_lr_flaw could not be
                       # generated honestly at all.
                       "v_ac": [g for g in g_gmat_cr.GENS if g.skill == "v_ac"]
                                + g_flaw.GENS,
                       "v_pc": [g for g in g_gmat_cr.GENS if g.skill == "v_pc"],
                       "di_gt": g_gmat_gt.GENS,
                       "di_tpa": g_gmat_tpa.GENS,
                       "di_msr": g_gmat_msr.GENS,
                       # Reading comprehension. These two were the only GMAT categories
                       # with no generated items, because g_rc.py was written and never
                       # imported (INC-0086). The count is gated on how many passages
                       # exist, not on generator cleverness: a question worded the same
                       # way over two passages is two items, and the same question over
                       # one passage is one. Twelve passages is the corpus today.
                       #
                       # These draw on both corpora. The LSAT reading categories draw
                       # only on the long one, mapped in mapping.py: the short passages
                       # average 192 words, which sits inside the GMAT range, while the
                       # hand written LSAT passages here run 289 to 330, and length is
                       # most of what distinguishes LSAT reading.
                       "v_st": [g for g in g_rc.GENS if g.skill == "v_st"],
                       "v_inf": [g for g in g_rc.GENS if g.skill == "v_inf"]},
              "act": {"act_e_kol": g_act_kol.GENS,
                      # ACT files exponents, radicals, sequences, matrices, complex
                      # numbers and proportional reasoning here. The SAT pool only
                      # covers the first two, so the rest are written directly.
                      "act_m_nq": M.build_for("act", M.by_id(POOL_MODS))["act_m_nq"]
                                  + g_act_nq.GENS,
                      # ACT reports Science under three categories, so each one is its
                      # own bank filled from the schemas that target it. One shared draw
                      # of a study supports all three, which is why they share a module.
                      "act_s_iod": [g for g in g_act_sci.GENS if g.skill == "act_s_iod"],
                      "act_s_si": [g for g in g_act_sci.GENS if g.skill == "act_s_si"],
                      "act_s_esa": [g for g in g_act_sci.GENS if g.skill == "act_s_esa"]}}

PREFIX = {"sat": "ZS", "gre": "ZG", "gmat": "ZM", "act": "ZA", "lsat": "ZL"}

HEADER = """// GENERATED FILE. Do not edit.
// Written by src/build_banks.py from the schemas in src/gen/. Every answer key here
// is computed, never asserted, and every distractor is a named misconception that
// the item's own explanation names. Edit the schema, not this file.
"""


def plan_for(exam, pool):
    plan = dict(SAT_PLAN) if exam == "sat" else M.build_for(exam, pool)
    plan.update(EXAM_EXTRA.get(exam, {}))
    return plan



# INC-0079. The length bias check in test.js runs per hand written source file, because
# INC-0069 found a file playable at 88 percent hidden inside a section figure. Generated
# items were still only measured at the section level, and on the population the test
# harness loads, which is the hand written banks plus the strided starter slice. A schema
# contributing a few dozen items to a figure covering hundreds is invisible in it, and
# sat_rw_apostrophe shipped 861 items that a student answers correctly, all of them, by
# picking the third shortest option: its four choices are the four forms of one noun, and
# for a regular noun those forms are ordered by length by construction.
#
# So the measurement is per schema, per exam, over every item the schema produced rather
# than over a sample taken for another purpose. Three figures, because correcting one
# moves the tell to another: the two extremes, and the share of items whose key sits at
# the single most common length rank, which is what INC-0062 is about.
#
# SCHEMA_DEBT holds MEASURED values for schemas still over the cap, never guesses. Lower
# an entry as a schema is fixed; the check insists an entry be deleted once the schema is
# inside tolerance, so the table cannot quietly outlive the problem.
# Data Sufficiency offers the same five statements on every item, so a length rank there
# is the answer position wearing a different name, and the answer position already has its
# own check. Measuring it twice under two names would mean carrying a permanent debt entry
# for something that is not a length tell at all.
FIXED_CHOICE = {"gmat_ds_linear", "gmat_ds_percent", "gmat_ds_rectangle",
                "gmat_ds_average", "gmat_ds_ratio"}

# Each entry is (longest or largest, shortest or smallest, one rank holds, one answer
# value holds), MEASURED
# on the day the check was written, never a guess. They are what the bank is, not
# what it should be: a schema is allowed to sit at its recorded number and nowhere
# worse. Lower an entry when a schema is improved; the check refuses an entry that
# is no longer needed, so the table cannot outlive the problem it records.
#
# The fourth number is the first figure here about what the answer IS rather than where
# it sits among the choices. Three place based checks share a blind spot the size of
# everything else, and msr_count answered 1 on 98 percent of its items while passing all
# three (INC-0081).
#
# The three worst were fixed rather than recorded. sat_rw_apostrophe was answerable
# at 100 percent by picking the third shortest option and is at 41; cr_plan_eval put
# the key shortest on 98 percent of 1,117 items and is at 19; cr_plan_weaken put it
# longest on 65 percent of 1,106 and is at 15.
# Why an entry is expected to stay. The table records what a schema measures; this
# records the cases where the measurement is a property of the question type rather than
# a defect to grind down, so the next person does not spend an hour on one I already spent
# an hour on. A schema not named here has no excuse and should come down.
SCHEMA_NOTES = {
    ("act", "act_kol_concision"):
        "as act_kol_redundancy, and for the same reason: the key is the concise option "
        "and no shorter one preserves the meaning. Both were written in the same module "
        "and only redundancy was ever recorded, because concision ships 28 items and the "
        "check did not look below fifty until INC-0088.",
    ("act", "act_s_claim"):
        "Half fixed. It had three possible correct answers in the whole schema and two "
        "of them opened with Yes, so answering Yes was right on 70 percent of items "
        "without reading the table. Each study now also carries the mirror claim it "
        "does not support, which balances the verdict at 50 percent, takes the distinct "
        "answers from three to six and the most common one from 70 percent to 35, and "
        "doubles the schema to 60 items along the way. What remains is a length rank "
        "holding on 55 percent: the correct reason names the specific comparison and "
        "the two wrong ones are generic, so the key sits at a predictable place in the "
        "ordered options. That wants distractors as specific as the key, which is a "
        "rewrite of the reason clauses rather than an addition to them.",
    ("act", "act_kol_redundancy"):
        "the key is the concise option, which is the shortest by the nature of the "
        "skill, and no shorter option can preserve the meaning. Picking the shortest "
        "is also what the real exam rewards on this question type, so the tell is the "
        "thing being taught. Measured for the odd one out as well: 96 percent, which "
        "is the same fact and not a second one.",
    ("gmat", "gmat_ds_rectangle"):
        "small, and its mode is the combined answer, which is the one its parameters "
        "reach most easily. Worth the same work gmat_ds_linear got if it grows.",
    ("gmat", "gmat_ds_percent"): "as gmat_ds_rectangle.",
}

SCHEMA_DEBT = {
    ('act', 'act_kol_concision'): (0, 100, 100, 23),
    ('act', 'act_kol_redundancy'): (0, 100, 100, 4),
    ('act', 'act_nq_proportion'): (24, 3, 48, 5),
    ('act', 'act_nq_scinot'): (6, 10, 50, 1),
    ('act', 'act_s_claim'): (41, 2, 55, 35),
    ('act', 'act_s_support'): (0, 0, 48, 3),
    ('act', 'act_s_why2'): (1, 19, 52, 4),
    ('act', 'sat_adv_radical>act_m_nq'): (52, 3, 52, 3),
    ('act', 'sat_alg_word>act_m_alg'): (8, 0, 48, 2),
    ('act', 'sat_rw_apostrophe>act_e_cse'): (14, 17, 47, 1),
    ('act', 'sat_rw_boundary>act_e_cse'): (34, 0, 50, 0),
    ('gmat', 'gmat_ds_percent'): (41, 3, 41, 41),
    ('gmat', 'gmat_ds_rectangle'): (42, 4, 42, 42),
    ('gmat', 'gt_avg'): (0, 8, 53, 2),
    ('gmat', 'gt_count'): (0, 6, 45, 44),
    ('gmat', 'gt_gap'): (0, 19, 43, 3),
    ('gmat', 'gt_ratio'): (9, 0, 45, 10),
    ('gmat', 'msr_count'): (0, 3, 45, 42),
    ('gmat', 'sat_adv_exponential>q_rrp'): (39, 0, 46, 8),
    ('gmat', 'sat_adv_exprules>q_vof'): (19, 6, 44, 8),
    ('gmat', 'sat_adv_radical>q_vof'): (47, 2, 47, 2),
    ('gmat', 'sat_alg_distribute>q_alg'): (40, 42, 42, 3),
    ('gmat', 'sat_psda_percent>q_rrp'): (0, 45, 45, 5),
    ('gre', 'sat_adv_exponential>gre_arith'): (40, 0, 45, 10),
    ('gre', 'sat_adv_exprules>gre_arith'): (17, 6, 45, 9),
    ('gre', 'sat_adv_radical>gre_alg'): (52, 2, 52, 3),
    ('gre', 'sat_alg_distribute>gre_alg'): (37, 41, 41, 4),
    ('gre', 'sat_geo_parallel>gre_geo'): (0, 22, 44, 2),
    ('gre', 'sat_psda_percent>gre_arith'): (0, 45, 45, 6),
    ('sat', 'sat_adv_radical'): (52, 3, 52, 2),
    ('sat', 'sat_alg_word'): (6, 0, 53, 3),
    ('sat', 'sat_psda_percent'): (0, 38, 49, 5),
    ('sat', 'sat_rw_boundary'): (34, 0, 50, 0),
}

# A note explains an entry, so it cannot outlive one. The check already deletes an entry
# the moment the schema no longer needs it, and the paragraph beside it used to stay:
# three notes about geometry schemas survived the entries they annotated in this change
# alone, and a note about a debt nobody owes any more is the table outliving the problem
# by the other door.
_orphans = sorted(k for k in SCHEMA_NOTES if k not in SCHEMA_DEBT)
if _orphans:
    raise SystemExit("SCHEMA_NOTES explains entries that no longer exist; delete the "
                     "note with the entry: " + ", ".join("%s/%s" % k for k in _orphans))


# A schema offers a fixed list of wrong answers, and an exam asks for a fixed number of
# choices that all look alike. When two of those wrong answers work out to the same
# value, or too few of them render the way the key does, the whole draw is thrown away.
# The throwing away is silent: a rejected draw is how a schema says "not this one", the
# next draw is a new set of numbers, and the category still fills from its neighbours.
#
# Two different things hide in there. Particular numbers colliding is harmless. A
# collision in the SHAPE of what a schema offers is not: sat_geo_trig lost every tangent
# item at five choices because swapping the legs and inverting the ratio are the same
# arithmetic for a tangent (INC-0090), and sat_adv_exponential lost three draws in four
# on every exam because a starting amount times a fraction raised to a power renders as
# a whole number, a decimal or a fraction depending on the draw (INC-0092). A twentieth
# of a schema's draws is where the second stops looking like the first.
#
# Only AssemblyError counts. A schema raising plain ItemError from its own build() is
# refusing a parameter combination that does not make a question, which is the schema
# doing its job.
DISCARD_CAP = 5

# MEASURED, like SCHEMA_DEBT, and read the same way: a schema may sit at its recorded
# number and nowhere worse, and the check insists an entry be deleted once the schema no
# longer needs it. Unlike SCHEMA_DEBT these figures are exact rather than sampled, since
# the probe draws a fixed number of times from a fixed seed, so a number that moves means
# someone changed the schema. Every one of them is a subspace that never reaches a
# student: the absolute value inequalities whose two bounds are the same distance out,
# the circles whose radius and diameter make two of the wrong answers agree, the slopes
# that come out as fractions while the wrong answers come out whole. They are worth
# fixing one at a time.
DISCARD_DEBT = {
    ('gmat', 'gt_change'): 12,
    ('gmat', 'sat_adv_exprules>q_vof'): 6,
    ('gmat', 'sat_adv_nonlinsys>q_alg'): 9,
    ('gmat', 'sat_alg_slope>q_alg'): 7,
    ('gre', 'sat_adv_exprules>gre_arith'): 6,
    ('gre', 'sat_adv_nonlinsys>gre_alg'): 12,
    ('gre', 'sat_alg_slope>gre_geo'): 7,
    ('gre', 'sat_geo_circle>gre_geo'): 10,
}

NUMERIC = re.compile(r"^\$?-?[\d,]+(\.\d+)?(/\d+)?$")
# A number with a unit word after it, as the percent change schema renders its choices.
# Ranked by value like any other number: the character count there tracks the digits, not
# anything a student could use. The unit has to be the same on every choice, so "5 hours"
# against "5 minutes" is not quietly treated as a tie.
UNIT_NUM = re.compile(r"^(\$?-?[\d,]+(\.\d+)?(/\d+)?) ([a-z][a-z ]*)$")


def _split(c):
    t = str(c).strip()
    m = UNIT_NUM.match(t)
    return (m.group(1), m.group(4)) if m else (t, "")


def _numeric(it):
    parts = [_split(c) for c in it["choices"]]
    if not all(NUMERIC.match(n) for n, _ in parts):
        return False
    return len(set(u for _, u in parts)) == 1


def _value(c):
    t = _split(c)[0].replace("$", "").replace(",", "").strip()
    if "/" in t:
        a, b = t.split("/", 1)
        return float(a) / float(b)
    return float(t)


def bias(items, choices):
    """The extremes and the most common rank, ranked by whatever a guesser could use.

    For a worded answer that is the character count. For a numeric one it is the VALUE,
    which is the decision test.js already made and made for a reason: among numbers of the
    same shape the character count just tracks the digit count, so measuring length there
    reports the size of the numbers rather than anything a student could exploit. The
    framework balances numeric distractors on value for the same reason.
    """
    if items and all(_numeric(it) for it in items if isinstance(it["answer"], int)):
        key = lambda it, i: _value(it["choices"][i])
    else:
        key = lambda it, i: len(str(it["choices"][i]))
    rank = [0] * choices
    scored = longest = shortest = 0
    counted = 0
    for it in items:
        # Two part analysis answers a pair of row indices, not one choice, so a length
        # rank over its options means nothing. Skipped rather than coerced.
        if not isinstance(it["answer"], int):
            continue
        counted += 1
        L = [key(it, i) for i in range(len(it["choices"]))]
        order = sorted(range(len(L)), key=lambda i: L[i])
        rank[order.index(it["answer"])] += 1
        mx, mn = max(L), min(L)
        if L.count(mx) != 1 or L.count(mn) != 1:
            continue
        scored += 1
        if L[it["answer"]] == mx:
            longest += 1
        if L[it["answer"]] == mn:
            shortest += 1
    n = max(1, counted)
    numeric = bool(items) and all(_numeric(it) for it in items
                                  if isinstance(it["answer"], int))
    # The fourth figure is about the answer itself rather than where it sat. Every other
    # check here measures the key's place among the choices, and a schema whose parameters
    # produce the same answer over and over passes all of them while a student who always
    # says that answer scores 98 percent (INC-0081).
    vals = Counter(str(it["choices"][it["answer"]]) for it in items
                   if isinstance(it["answer"], int))
    top = int(round(100.0 * max(vals.values()) / max(1, counted))) if vals else 0
    return (int(round(100.0 * longest / max(1, scored))),
            int(round(100.0 * shortest / max(1, scored))),
            int(round(100.0 * max(rank) / n)), scored, counted, numeric,
            top, len(vals))


def se_points(pct, n):
    """One standard error of a proportion at this sample size, in percentage points."""
    p = min(max(pct / 100.0, 0.0), 1.0)
    return math.sqrt(p * (1 - p) / max(1, n)) * 100


# Draws per schema in the discard probe. Enough to see a question form that never builds
# (a form is a third or a half of a schema's draws) without doubling the build.
DISCARD_DRAWS = 400


# A phrase said twice where two pieces of text meet. The pool word problem printed "5
# gallons per minute gallons per minute" in 287 items because its template and the code
# filling it both wrote the unit, and nothing read a generated stem as a sentence
# (INC-0120). A run of single letters, a coin toss sequence such as "H T H T H", is the
# one legitimate repeat and is allowed. Passages are not scanned: prose there can repeat
# itself on purpose ("piece by piece by gangs of longshoremen").
DOUBLED = re.compile(r"\b((?:[A-Za-z']+ )+[A-Za-z']+) \1\b")
SAID_ONCE = ("stem", "prompt", "choices", "statements", "expl", "wrong")


def said_twice(text):
    """The first run of two or more words repeated back to back in `text`, or None."""
    for m in DOUBLED.finditer(text):
        if any(len(w) > 1 for w in m.group(1).split()):
            return m.group(0)
    return None


def check_said_once(items):
    """One line per item whose text says a phrase twice back to back (INC-0120)."""
    out = []
    for it in items:
        for field in SAID_ONCE:
            val = it.get(field)
            for text in (val if isinstance(val, list) else [val]):
                hit = said_twice(text) if isinstance(text, str) else None
                if hit:
                    out.append("%s (%s) %s: %r" % (it["id"], it.get("gen") or "", field, hit))
                    break
            else:
                continue
            break
    return out


def check_discarded(exam, choices, gens):
    """Report schemas whose questions cannot be assembled into items for this exam.

    Measured on its OWN seeded draws rather than on the ones the bank build happened to
    make, because the bank build visits a schema as often as its neighbours leave room
    for and dedups against a shared set, so the same schema reads 8 percent in one build
    and 13 in the next with nothing about it changed. That is the drift INC-0089 is
    about, and here it can be removed rather than tolerated: how often a schema's
    questions fail to assemble is a property of the schema and the choice count and
    nothing else. A fixed count of draws from a fixed seed makes the figure exact, so the
    recorded number moves only when someone changes the schema.

    It counts AssemblyError and nothing else. An earlier version matched on one of the
    two messages make() can raise and missed the other, which was the larger of the two
    by an order of magnitude (INC-0092); counting the exception type rather than its
    wording is what stops the next one hiding behind a message nobody thought of.
    """
    out = []
    for g in gens:
        rng = random.Random(20260922 + zlib.crc32(("%s|%s" % (exam, g.id)).encode()) % 99991)
        lost = 0
        for _ in range(DISCARD_DRAWS):
            try:
                g.make(rng, choices)
            except F.AssemblyError:
                lost += 1
            except (F.ItemError, ArithmeticError):
                pass
        pct = int(round(100.0 * lost / DISCARD_DRAWS))
        rec = DISCARD_DEBT.get((exam, g.id))
        lim = max(DISCARD_CAP, rec or 0)
        if pct > lim:
            out.append("  %s/%-28s cannot assemble %d percent of its questions into %d "
                       "choices, above %d" % (exam, g.id, pct, choices, lim))
        elif rec is not None and pct <= DISCARD_CAP:
            out.append("  %s/%s serves this exam now (%d percent); delete its "
                       "DISCARD_DEBT entry" % (exam, g.id, pct))
    return out


def check_bias(measured, verbose=True):
    """Fail the build on a schema over its recorded bias, or on a stale recording."""
    problems, stale = [], []
    for (exam, gen, choices), (lo, sh, best, scored, n, num, top, ndist) in \
            sorted(measured.items()):
        # A size threshold that skips is a silent exemption, and it falls on exactly the
        # schemas most likely to carry a structural tell: the ones built from a small
        # authored corpus. rc_infer shipped 40 items whose key was the shortest choice on
        # 68 percent of them and was never measured, because 40 is under 50 (INC-0088).
        #
        # So the cap widens with the sampling error instead of the check switching off.
        # Below ten items nothing is measured, because even a perfect run is thin there.
        # From ten up the tolerance is the ordinary cap or chance plus two and a half
        # standard errors of a proportion at this sample size, whichever is larger: at 40
        # items that is the ordinary 36 percent, and at 8 it would have been 55.
        if n < 10:
            continue
        # A fixed choice schema offers the same five statements on every item, so its
        # length and value ranks are the answer position wearing another name and the
        # position has its own check. Which statement is correct is not: a student who
        # always says the same one is using the fourth figure, so that one still applies.
        fixed = gen in FIXED_CHOICE
        chance = int(round(100.0 / choices))
        # Two ceilings, and they mean different things. The policy line is 1.8 times
        # chance, a number someone chose. The floor is what a schema with no tell at all
        # can reach on a thin draw, which is an error bar already and is why it takes no
        # second one below.
        policy = int(round(1.8 * chance))
        floor = int(round(chance + 2.5 * se_points(100.0 / choices, n)))
        cap = max(policy, floor)
        rec = SCHEMA_DEBT.get((exam, gen))
        limit = tuple(max(cap, r) for r in rec[:3]) if rec else (cap, cap, cap)
        big, small, one = (("largest is key", "smallest is key", "one value rank holds")
                           if num else
                           ("longest is key", "shortest is key", "one length rank holds"))
        # The answer value check has its own chance rate, and it is bounded at both ends. A
        # schema that can only produce two different answers cannot go below fifty, so
        # holding it to 100 over the number of CHOICES asks for something arithmetic
        # forbids. And a schema producing hundreds of different answers has a chance rate
        # near zero, where 1.8 times it is also near zero; always saying the same answer
        # is not a strategy worth having unless it beats guessing, so the limit is never
        # stricter than the ordinary cap either.
        vchance = max(int(round(100.0 / max(1, ndist))), chance)
        vcap = int(round(1.8 * vchance))
        vlimit = max(vcap, rec[3] if rec and len(rec) > 3 else 0)
        # (measured, ceiling, the part of the ceiling that is already an error bar, ...)
        checks = [(top, vlimit, 0, "one answer value holds", vchance)]
        if not fixed:
            checks = [(lo, limit[0], floor, big, chance),
                      (sh, limit[1], floor, small, chance),
                      (best, limit[2], floor, one, chance)] + checks

        # A measurement is not the thing itself, and every ceiling here except the small
        # sample floor is a line rather than an error bar, so the comparison has to carry
        # one. Without it a schema whose true rate sits on its line fails about half the
        # times it is measured, and what moves it is the neighbours: a category stops at
        # TARGET, so growing one schema shrinks the others and changes which items the
        # shared dedup set had already taken by the time they ran. Widening one geometry
        # schema moved six untouched siblings by 1 to 4 points and failed all six
        # (INC-0089). Clearing that by re-measuring and re-recording is a ratchet being
        # rewritten rather than read, and a rewrite for drift is indistinguishable from
        # one that accepts a regression.
        #
        # So a figure fails only when it is over its ceiling by more than the standard
        # error of a proportion at the size it was measured at: about two points on a
        # bank of five hundred, which is the size of the drift and nowhere near the size
        # of a real tell (rc_infer was 32 points over). Against a recorded figure that is
        # if anything generous to the check, since the record is a measurement too and
        # carries an error of its own. Nothing is re-recorded for drift, so the ceiling
        # stays the figure a person chose and cannot walk upward alongside the bank.
        for got, lim, bar, what, ch in checks:
            tol = 0.0 if lim <= bar else se_points(lim, n)
            if got > lim + tol:
                why = SCHEMA_NOTES.get((exam, gen))
                problems.append("  %s/%-30s %s on %d percent of %d, above %d (chance %d)%s"
                                % (exam, gen, what, got, n, lim, ch,
                                   "\n      note: " + why if why else ""))

        # The staleness check mirrors it. An entry is called unnecessary only when the
        # measurement sits clear of the cap by that same margin rather than a point under
        # it; otherwise the drift that can no longer fail the build would delete the
        # record instead, and the figure is lost by the other door.
        def clear(got, ceiling, bar):
            return got <= ceiling - (0.0 if ceiling <= bar else se_points(ceiling, n))

        if rec and clear(top, vcap, 0) and (fixed or (clear(lo, cap, floor)
                                                      and clear(sh, cap, floor)
                                                      and clear(best, cap, floor))):
            stale.append("  %s/%s is inside tolerance now (%d/%d/%d); delete its "
                         "SCHEMA_DEBT entry" % (exam, gen, lo, sh, best))
    if problems or stale:
        print("ERROR: generated schema answer bias (INC-0079)", file=sys.stderr)
        for line in problems + stale:
            print(line, file=sys.stderr)
        sys.exit(1)
    if verbose:
        # Counted at the threshold the check actually uses. It used to say 50 while the
        # check said 50 too, and when the check moved to 10 this line was what would have
        # gone on reporting the old number: adding four schemas left the count unchanged
        # at 188, and noticing that is what found INC-0088 in the first place. A headline
        # that counts something other than what was checked is how the next one hides.
        checked = sum(1 for v in measured.values() if v[4] >= 10)
        small = sum(1 for v in measured.values() if 10 <= v[4] < 50)
        print("  schema answer bias: %d schemas measured, all inside recorded tolerance"
              " (%d of them under 50 items, held to a cap widened for the sample)"
              % (checked, small))


def main(target=TARGET, verbose=True):
    OUT.mkdir(exist_ok=True)
    # Before anything is generated, because this one is about the words rather than the
    # numbers and there is no point measuring a bank whose sentences do not agree with
    # themselves (INC-0093).
    wording = (g_act_sci.check_names() + g_act_sci.check_readings()
               + g_gmat_gt.check_directions())
    if wording:
        print("ERROR: ACT science wording, against its own table (INC-0093, INC-0098)",
              file=sys.stderr)
        for line in wording:
            print("  " + line, file=sys.stderr)
        sys.exit(1)
    premises = g_rc.check_premises()
    if premises:
        print("ERROR: reading inference stems and the premises they turn on (INC-0097)",
              file=sys.stderr)
        for line in premises:
            print("  " + line, file=sys.stderr)
        sys.exit(1)
    tells = g_rc.check_tells()
    if tells:
        print("ERROR: reading schemas answerable by matching words (INC-0117)",
              file=sys.stderr)
        for line in tells:
            print("  " + line, file=sys.stderr)
        sys.exit(1)
    pool = M.by_id(POOL_MODS)
    pool.update({g.id: g for g in POOL_EXTRA})
    report = {}
    by_gen = {}
    # LSAT gives five choices, confirmed against LSAC sample questions and carried in
    # exam_harness.js, which is the same as the GMAT, so the CR schemas need no reshaping.
    starving = []
    for exam, choices in (("sat", 4), ("gre", 5), ("gmat", 5), ("act", 4), ("lsat", 5)):
        plan = plan_for(exam, pool)
        items = []
        by_skill = {}
        seen = set()
        n = 1
        for skill in sorted(plan):
            gens = plan[skill]
            got, dropped, errs, made = F.run(
                gens, target, choices, PREFIX[exam],
                # crc32, not hash(). Python randomises string hashing per process, so
                # the previous seed changed on every build: the bank was different every
                # time, the "seeded and reproducible" promise was not true, and the bias
                # ratchet in test.js drifted a few points between runs for no reason.
                seed=20260916 + (zlib.crc32((exam + skill).encode()) % 99991),
                start=n, existing=seen,
            )
            for it in got:
                seen.add(F.canon(it))
                if it.get("gen") and isinstance(it.get("choices"), list):
                    by_gen.setdefault((exam, it["gen"], len(it["choices"])), []).append(it)
            n += len(got)
            items.extend(got)
            by_skill[skill] = list(got)
            report[(exam, skill)] = (len(got), dropped, errs)
            # A schema that contributes nothing is a failure, not a small number. rc_main
            # and rc_caveat raised ItemError on every draw for want of one more passage,
            # and because ItemError is the ordinary way a schema says this draw did not
            # work, a schema saying it every time looked exactly like a fussy one. Only
            # the category total was reported, so a zero inside it was invisible
            # (INC-0086). Fatal, because there is no honest reason to wire a schema into
            # a plan and ship none of it.
            silent = [g.id for g in gens if made.get(g.id, 0) == 0]
            if silent:
                raise SystemExit(
                    "build_banks: %s/%s wires %d schema(s) that produced no items at all: "
                    "%s. Either they cannot draw, or the plan should not name them."
                    % (exam, skill, len(silent), ", ".join(sorted(silent))))
            # A schema can also produce only PART of itself, which is the same silence
            # one level down. sat_geo_trig listed five wrong answers, but two of them
            # were the same arithmetic for the tangent, so once the duplicate was
            # dropped the tangent form had three where a five choice exam needs four and
            # every tangent item was thrown away. The GRE shipped the schema's sine and
            # cosine forms and nothing else, and the only visible trace was an item
            # count half the SAT's, with no reference to compare it against (INC-0090).
            #
            # A few such rejections are particular parameters colliding and are harmless,
            # since the next draw is a new set of numbers. A twentieth of a schema's
            # draws is not: at that rate the collision is in the shape of what the schema
            # offers rather than in the numbers, and something it was written to ask is
            # not being asked. sat_adv_exponential was losing three quarters of its
            # draws that way, to the other of make()'s two refusals, and the counter
            # that knew was read by nobody (INC-0092).
            starving.extend(check_discarded(exam, choices, gens))
            if verbose:
                flag = "" if len(got) >= target else "   SHORT"
                print("  %-5s %-10s %4d items from %2d schemas%s"
                      % (exam, skill, len(got), len(gens), flag))
                if len(got) < target and errs:
                    print("        %s" % errs[-1])
        # Split into a starter slice and the remainder.
        #
        # The whole bank is a blocking script, so time to first question used to be time
        # to download every item. Measured on regular 3G that was 20 seconds for GMAT and
        # 23 for ACT, which is well past where people leave. Nothing about the items was
        # wrong; the loading was.
        #
        # The starter is strided rather than taken from the front, because items within a
        # skill come out in generation order and the front of that run is not spread
        # across difficulty. Striding gives the engine a representative pool immediately,
        # so a student's first rounds are drawn from the same distribution they would
        # have been anyway.
        starter, rest = [], []
        for skill, group in sorted(by_skill.items()):
            stride = max(1, len(group) // STARTER_PER_SKILL)
            head = group[::stride][:STARTER_PER_SKILL]
            head_ids = {id(x) for x in head}
            starter.extend(head)
            rest.extend([x for x in group if id(x) not in head_ids])

        # A reading item without its passage is an unanswerable question, and the way
        # it happened was a field the emitter never copied: right in memory, right in
        # every test that builds items in process, gone in the file that ships
        # (INC-0099). Checked here, against what the item IS, before anything is
        # written, and checked again in the browser against what reaches the screen.
        mute = ["%s (%s)" % (it["id"], it.get("gen") or "")
                for it in items
                if it.get("type") in ("RC", "R")
                and not (it.get("passage") or it.get("passageHtml"))]
        if mute:
            raise SystemExit(
                "build_banks: %s has %d reading item(s) with nothing to read: %s"
                % (exam, len(mute), ", ".join(mute[:6])))
        twice = check_said_once(items)
        if twice:
            raise SystemExit(
                "build_banks: %s has %d item(s) that say a phrase twice back to back "
                "(INC-0120): %s" % (exam, len(twice), "; ".join(twice[:6])))

        const = "BANK_GEN_" + exam.upper()
        js = F.to_js(starter, const, HEADER)
        (OUT / ("bank_gen_%s.js" % exam)).write_text(js, encoding="utf-8")
        # The deferred remainder ships in chunks, not one file. Cloudflare rejects any
        # static asset over 25 MiB, and at TARGET 3300 the ACT remainder alone is about
        # 30 MiB, so a single file fails the deploy outright rather than degrading. The
        # budget below is well under the limit so the next raise of TARGET does not walk
        # back into it: each chunk defines its own const and pushes itself, so the count
        # is free to grow.
        CHUNK_BYTES = 18 * 1024 * 1024
        chunks, cur, cur_n = [], [], 0
        for it in rest:
            # Cheap size estimate: the real cost is the emitted JSON-ish text, and the
            # stem plus the prompt and choices is almost all of it.
            approx = len(str(it))
            if cur and cur_n + approx > CHUNK_BYTES:
                chunks.append(cur); cur, cur_n = [], 0
            cur.append(it); cur_n += approx
        if cur: chunks.append(cur)
        if not chunks: chunks = [[]]
        rest_bytes = 0
        for ci, part in enumerate(chunks, start=1):
            js_rest = F.to_js(part, "%s_REST%d" % (const, ci), HEADER)
            (OUT / ("bank_gen_%s_rest%d.js" % (exam, ci))).write_text(js_rest, encoding="utf-8")
            rest_bytes += len(js_rest)
        # Remove a single-file remainder left by an older build, so a stale 30 MiB asset
        # cannot be picked up by the glob in build.py and shipped alongside the chunks.
        _legacy = OUT / ("bank_gen_%s_rest.js" % exam)
        if _legacy.exists(): _legacy.unlink()
        js_rest = "x" * rest_bytes  # only its length is used in the report below
        if verbose:
            print("  wrote generated/bank_gen_%s.js: %d starter + %d deferred in %d chunk(s)"
                  " = %d items, %d + %d bytes (largest chunk %.1f MiB)"
                  % (exam, len(starter), len(rest), len(chunks), len(items), len(js),
                     len(js_rest),
                     max((OUT / ("bank_gen_%s_rest%d.js" % (exam, i + 1))).stat().st_size
                         for i in range(len(chunks))) / 1048576.0))
    if starving:
        print("ERROR: schemas whose questions cannot be assembled for an exam (INC-0090, INC-0092)",
              file=sys.stderr)
        for line in starving:
            print(line, file=sys.stderr)
        sys.exit(1)
    check_bias(dict(((e, g, c), bias(v, c)) for (e, g, c), v in by_gen.items()), verbose)
    short = [k for k, v in report.items() if v[0] < target]
    if short:
        print("  categories under target: %s"
              % ", ".join("%s/%s" % k for k in sorted(short)))
    return report


if __name__ == "__main__":
    main()
