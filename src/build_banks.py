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
# So the generated bank is 29 x 3300 + 9,218 = 104,918, and with the hand written banks
# the build counts a published total of 106,770.
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
    short = [k for k, v in report.items() if v[0] < target]
    if short:
        print("  categories under target: %s"
              % ", ".join("%s/%s" % k for k in sorted(short)))
    return report


if __name__ == "__main__":
    main()
