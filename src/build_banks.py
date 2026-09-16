"""Generate the item banks from the schemas in src/gen/.

The generators are the source of truth; the emitted .js files are build output and
are gitignored, exactly like /app/ and /blog/. The run is seeded, so the same
commit always produces the same bank and a rebuild is a no-op rather than a diff.

Run directly to see the per category report:  python3 src/build_banks.py
"""
import pathlib
import sys

D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D / "gen"))

import framework as F          # noqa: E402
import mapping as M            # noqa: E402
import g_sat_alg, g_sat_adv, g_sat_psda, g_sat_geo   # noqa: E402,F401

OUT = D / "generated"
TARGET = 500

POOL_MODS = [g_sat_alg, g_sat_adv, g_sat_psda, g_sat_geo]

# SAT categories are authored directly against SAT taxonomy; the other exams remap.
SAT_PLAN = {
    "m_alg": g_sat_alg.GENS,
    "m_adv": g_sat_adv.GENS,
    "m_psda": g_sat_psda.GENS,
    "m_geo": g_sat_geo.GENS,
}

PREFIX = {"sat": "ZS", "gre": "ZG", "gmat": "ZM"}

HEADER = """// GENERATED FILE. Do not edit.
// Written by src/build_banks.py from the schemas in src/gen/. Every answer key here
// is computed, never asserted, and every distractor is a named misconception that
// the item's own explanation names. Edit the schema, not this file.
"""


def plan_for(exam, pool):
    if exam == "sat":
        return SAT_PLAN
    return M.build_for(exam, pool)


def main(target=TARGET, verbose=True):
    OUT.mkdir(exist_ok=True)
    pool = M.by_id(POOL_MODS)
    report = {}
    for exam, choices in (("sat", 4), ("gre", 5), ("gmat", 5)):
        plan = plan_for(exam, pool)
        items = []
        seen = set()
        n = 1
        for skill in sorted(plan):
            gens = plan[skill]
            got, dropped, errs, made = F.run(
                gens, target, choices, PREFIX[exam],
                seed=20260916 + (abs(hash(exam + skill)) % 99991),
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
