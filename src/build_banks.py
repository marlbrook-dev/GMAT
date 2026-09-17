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
import g_act_sci, g_gre_verb                         # noqa: E402,F401

OUT = D / "generated"
TARGET = 500

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
                       "di_gt": g_gmat_gt.GENS,
                       "di_tpa": g_gmat_tpa.GENS,
                       "di_msr": g_gmat_msr.GENS},
              "act": {"act_e_kol": g_act_kol.GENS,
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
            report[(exam, skill)] = (len(got), dropped, errs)
            if verbose:
                flag = "" if len(got) >= target else "   SHORT"
                print("  %-5s %-10s %4d items from %2d schemas%s"
                      % (exam, skill, len(got), len(gens), flag))
                if len(got) < target and errs:
                    print("        %s" % errs[-1])
        const = "BANK_GEN_" + exam.upper()
        js = F.to_js(items, const, HEADER)
        (OUT / ("bank_gen_%s.js" % exam)).write_text(js, encoding="utf-8")
        if verbose:
            print("  wrote generated/bank_gen_%s.js: %d items, %d bytes"
                  % (exam, len(items), len(js)))
    short = [k for k, v in report.items() if v[0] < target]
    if short:
        print("  categories under target: %s"
              % ", ".join("%s/%s" % k for k in sorted(short)))
    return report


if __name__ == "__main__":
    main()
