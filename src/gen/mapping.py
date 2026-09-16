"""One schema, four exams.

An equation is an equation. What differs between the GMAT, the GRE, the SAT and the ACT is
how the content is bucketed, how many answer choices there are, and how hard the
typical item runs. So the schemas are written once and remapped here, rather than
written three times and drifting apart three ways.

Difficulty is shifted, not copied: the same linear equation that is a warm up on
the SAT sits mid range on the GRE, because the population taking each test is
different. The shift is a deliberate editorial judgement and is recorded per exam
below so it can be argued with.
"""
from framework import Gen


class Remap(Gen):
    """The same problem schema, filed under another exam's taxonomy."""

    def __init__(self, inner, skill, section, bump=0, sub=None):
        self.inner = inner
        self.id = "%s>%s" % (inner.id, skill)
        self.skill = skill
        self.section = section
        self.sub = sub or inner.sub
        self.diff = inner.diff
        self.bump = bump
        self.type = inner.type
        self.fmt = inner.fmt

    def build(self, rng):
        spec = dict(self.inner.build(rng))
        spec["skill"] = self.skill
        spec["section"] = self.section
        if self.sub:
            spec["sub"] = self.sub
        d = spec.get("diff", self.inner.diff) + self.bump
        spec["diff"] = max(1, min(5, d))
        return spec


def by_id(mods):
    out = {}
    for m in mods:
        for g in m.GENS:
            out[g.id] = g
    return out


# Which SAT schema feeds which category on each exam. A schema appears under the
# category whose published framework actually names that content, never under a
# category just because it needs filling.
GRE_MAP = {
    "gre_arith": ["sat_psda_percent", "sat_psda_pctchange", "sat_psda_rate",
                  "sat_psda_units", "sat_adv_exprules", "sat_adv_exponential"],
    "gre_alg": ["sat_alg_linear1", "sat_alg_distribute", "sat_alg_system",
                "sat_alg_inequality", "sat_alg_feval", "sat_alg_abs",
                "sat_adv_quadroots", "sat_adv_radical", "sat_adv_rational",
                "sat_adv_polyfactor", "sat_adv_nonlinsys"],
    "gre_geo": ["sat_geo_angles", "sat_geo_pythag", "sat_geo_circle", "sat_geo_rect",
                "sat_geo_volume", "sat_geo_similar", "sat_geo_trig", "sat_geo_parallel",
                "sat_alg_slope", "sat_alg_parperp"],
    "gre_data": ["sat_psda_center", "sat_psda_prob", "sat_psda_table", "sat_psda_model"],
}

# ACT Mathematics, filed under ACT's own eight reporting categories (ACT publishes the
# percentage of the section each one carries). Every schema sits under the category whose
# published description actually names its content: "Integrating Essential Skills" is ACT's
# own name for rates, percentages, proportional relationships, area and volume, and average
# and median, which is exactly the SAT problem-solving and data-analysis pool, so that is
# where those schemas go rather than under Statistics and Probability.
#
# ACT does not publish a Modeling item count because Modeling is scored across the other
# categories rather than alongside them, so it is not a bucket here.
ACT_MAP = {
    "act_m_nq": ["sat_adv_exprules", "sat_adv_radical"],
    "act_m_alg": ["sat_alg_linear1", "sat_alg_distribute", "sat_alg_system",
                  "sat_alg_inequality", "sat_alg_abs", "sat_alg_word",
                  "sat_adv_quadroots", "sat_adv_polyfactor", "sat_adv_nonlinsys"],
    "act_m_fun": ["sat_alg_feval", "sat_adv_vertex", "sat_adv_exponential",
                  "sat_adv_rational"],
    "act_m_geo": ["sat_geo_angles", "sat_geo_pythag", "sat_geo_circle", "sat_geo_rect",
                  "sat_geo_volume", "sat_geo_similar", "sat_geo_trig", "sat_geo_parallel",
                  "sat_alg_slope", "sat_alg_parperp"],
    "act_m_sp": ["sat_psda_center", "sat_psda_prob", "sat_psda_table", "sat_psda_model"],
    "act_m_ies": ["sat_psda_percent", "sat_psda_pctchange", "sat_psda_rate",
                  "sat_psda_units"],
    # English. Conventions of Standard English is the same body of rules the SAT
    # calls Standard English Conventions, and Production of Writing turns on the
    # same transition logic, so those schemas are reused rather than rewritten.
    # Knowledge of Language has no SAT counterpart and has its own generators in
    # g_act_kol.py.
    "act_e_cse": ["sat_rw_sva", "sat_rw_pronoun", "sat_rw_apostrophe", "sat_rw_boundary"],
    "act_e_pow": ["sat_rw_transition"],
}

# A category's section is not always the exam's default. ACT English and ACT Math
# are both mapped above, so the section is read per skill rather than per exam.
SECTION_OVERRIDE = {"act_e_cse": "E", "act_e_pow": "E", "act_e_kol": "E"}

GMAT_MAP = {
    "q_rrp": ["sat_psda_percent", "sat_psda_pctchange", "sat_psda_rate",
              "sat_psda_units", "sat_adv_exponential"],
    "q_vof": ["sat_adv_exprules", "sat_adv_radical", "sat_adv_quadroots",
              "sat_adv_polyfactor", "sat_adv_rational"],
    "q_alg": ["sat_alg_linear1", "sat_alg_distribute", "sat_alg_system",
              "sat_alg_inequality", "sat_alg_feval", "sat_alg_abs",
              "sat_adv_vertex", "sat_adv_nonlinsys", "sat_alg_slope", "sat_alg_parperp"],
    "q_csp": ["sat_psda_center", "sat_psda_prob", "sat_psda_table"],
}

# The GRE and GMAT quantitative sections run harder than the SAT's, so every
# remapped schema moves up one band. Anything already at the top stays there.
GRE_BUMP = 1
GMAT_BUMP = 1
# The ACT draws on the same school mathematics as the SAT and, like the SAT, gives four answer
# choices, so nothing shifts. What differs is pace, about 60 seconds a question against the
# SAT's 95, and that is a section setting rather than an item property.
ACT_BUMP = 0


def build_for(exam, pool):
    """Return the remapped generator list for one exam, keyed by category."""
    if exam == "gre":
        table, section, bump = GRE_MAP, "Q", GRE_BUMP
    elif exam == "gmat":
        table, section, bump = GMAT_MAP, "Q", GMAT_BUMP
    elif exam == "act":
        table, section, bump = ACT_MAP, "M", ACT_BUMP
    else:
        raise ValueError(exam)
    out = {}
    for skill, ids in table.items():
        gens = []
        for gid in ids:
            g = pool.get(gid)
            if g is None:
                raise KeyError("mapping names a schema that does not exist: %s" % gid)
            gens.append(Remap(g, skill, SECTION_OVERRIDE.get(skill, section), bump))
        out[skill] = gens
    return out
