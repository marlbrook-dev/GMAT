"""Generate the item banks from the schemas in src/gen/.

The generators are the source of truth; the emitted .js files are build output and
are gitignored, exactly like /app/ and /blog/. The run is seeded with crc32 of the
exam and category name, so the same commit always produces the same bank. It must
not use Python's hash(), which is randomised per process and quietly made every
build produce a different bank.

Run directly to see the per category report:  python3 src/build_banks.py
"""
import pathlib
import sys
import zlib

D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D / "gen"))

import framework as F          # noqa: E402
import mapping as M            # noqa: E402
import g_sat_alg, g_sat_adv, g_sat_psda, g_sat_geo   # noqa: E402,F401
import g_sat_rw, g_gmat_ds, g_act_kol                # noqa: E402,F401
import g_gmat_gt, g_gmat_tpa, g_gmat_msr             # noqa: E402,F401
import g_act_sci, g_gre_verb, g_gmat_cr, g_act_nq    # noqa: E402,F401

OUT = D / "generated"

# Per category, set to what the schemas can actually produce rather than to a round
# number. 34 categories across the four generated exams, plus 1,073 hand written items
# (including all 65 LSAT ones, which have no generator).
#
# Three categories exhaust their parameter space below this and ship at their own ceiling
# instead. That is reported, not silent: build_banks prints "categories under target" and
# names the schemas that ran out.
#
#   gmat/v_pc      833   cr_plan_assume, cr_plan_eval, cr_plan_weaken
#   sat/rw_eoi     971   sat_rw_transition
#   act/act_e_pow  974   sat_rw_transition remapped
#
# So the published bank is 31 x 1200 + 833 + 971 + 974 + 1,073 = 41,051.
#
# Raising this further is possible: nothing else was exhausted at 1200, so the other 31
# ceilings are somewhere above it and untested. Two reasons to think twice before doing
# it. Bank files grow roughly linearly and the wire cost with them, which
# src/smoke_load.js measures on every run against a 4 second budget to first question.
# And the categories built on a single schema (sat/rw_eoi, gre/gre_se, gre/gre_tc,
# act/act_e_pow) become variations on one template at scale, so past a point a new schema
# is worth far more than a larger number.
TARGET = 1200

# How many items per skill ship in the blocking starter file. Eighty is several rounds
# per skill, so a student reaches the deferred remainder long after it has arrived, while
# keeping the blocking download around a tenth of the full bank.
STARTER_PER_SKILL = 80

POOL_MODS = [g_sat_alg, g_sat_adv, g_sat_psda, g_sat_geo, g_sat_rw]

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
                       "v_ac": [g for g in g_gmat_cr.GENS if g.skill == "v_ac"],
                       "v_pc": [g for g in g_gmat_cr.GENS if g.skill == "v_pc"],
                       "di_gt": g_gmat_gt.GENS,
                       "di_tpa": g_gmat_tpa.GENS,
                       "di_msr": g_gmat_msr.GENS},
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


def main(target=TARGET, verbose=True):
    OUT.mkdir(exist_ok=True)
    pool = M.by_id(POOL_MODS)
    report = {}
    for exam, choices in (("sat", 4), ("gre", 5), ("gmat", 5), ("act", 4)):
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
            n += len(got)
            items.extend(got)
            by_skill[skill] = list(got)
            report[(exam, skill)] = (len(got), dropped, errs)
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

        const = "BANK_GEN_" + exam.upper()
        js = F.to_js(starter, const, HEADER)
        (OUT / ("bank_gen_%s.js" % exam)).write_text(js, encoding="utf-8")
        js_rest = F.to_js(rest, const + "_REST", HEADER)
        (OUT / ("bank_gen_%s_rest.js" % exam)).write_text(js_rest, encoding="utf-8")
        if verbose:
            print("  wrote generated/bank_gen_%s.js: %d starter + %d deferred = %d items, "
                  "%d + %d bytes"
                  % (exam, len(starter), len(rest), len(items), len(js), len(js_rest)))
    short = [k for k, v in report.items() if v[0] < target]
    if short:
        print("  categories under target: %s"
              % ", ".join("%s/%s" % k for k in sorted(short)))
    return report


if __name__ == "__main__":
    main()
