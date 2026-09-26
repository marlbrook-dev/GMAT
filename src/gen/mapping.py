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


class RemapItem(Gen):
    """The same schema under another exam's taxonomy, for a generator that builds the
    whole item itself.

    Remap above rewrites the SPEC before the framework assembles an item from it, which
    works for every schema that implements build(). The Critical Reasoning schemas
    implement make() instead, assembling the item directly and hardcoding its section, so
    Remap could only reach them after the fact. This rewrites the finished item.

    Which wrapper applies is decided per generator by whether its class overrides make(),
    not per exam, so mapping an item-level schema onto some third exam needs no change
    here.
    """

    def __init__(self, inner, skill, section, bump=0, sub=None):
        self.inner = inner
        self.id = "%s>%s" % (inner.id, skill)
        self.skill = skill
        self.section = section
        self.sub = sub or getattr(inner, "sub", None)
        self.diff = max(1, min(5, getattr(inner, "diff", 2) + bump))
        self.bump = bump
        self.type = getattr(inner, "type", "MC")
        self.fmt = getattr(inner, "fmt", None)
        self.domain = getattr(inner, "domain", None)

    def make(self, rng, choices_n):
        it = dict(self.inner.make(rng, choices_n))
        it["skill"] = self.skill
        it["section"] = self.section
        it["gen"] = self.id
        if self.sub:
            it["sub"] = self.sub
        it["diff"] = max(1, min(5, it.get("diff", self.inner.diff) + self.bump))
        return it


def wrap(inner, skill, section, bump):
    """Remap or RemapItem, whichever the inner generator needs."""
    own_make = type(inner).make is not Gen.make
    cls = RemapItem if own_make else Remap
    return cls(inner, skill, section, bump)


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
    # Rhetorical Synthesis sits here on ACT's own description of the category, not on a
    # resemblance: Production of Writing "requires you to apply your understanding of the
    # purpose and focus of a piece of writing", and its Topic Development strand asks the
    # student to "determine whether a text or part of a text has met its intended goal,
    # and evaluate the relevance of material in terms of a text's focus" (Preparing for
    # the ACT, ACT, 2026,
    # https://www.act.org/content/dam/act/unsecured/documents/Preparing-for-the-ACT.pdf).
    # A synthesis item states the goal and asks which sentence meets it using relevant
    # material from the notes, which is that sentence read as an instruction.
    "act_e_pow": ["sat_rw_transition", "sat_rw_synthesis"],
}

# A category's section is not always the exam's default. ACT English and ACT Math
# are both mapped above, so the section is read per skill rather than per exam.
SECTION_OVERRIDE = {"act_e_cse": "E", "act_e_pow": "E", "act_e_kol": "E",
                    "lsat_rc_stated": "RC", "lsat_rc_main": "RC", "lsat_rc_inf": "RC"}

# The LSAT had no generated bank at all: 372 hand written items against 20,000 to 40,000
# on the other four. Its Logical Reasoning section is the same genre as GMAT Critical
# Reasoning, five choices and all, so the CR schemas serve it.
#
# Mapped by what each item ASKS, not by what its schema is called, because the two come
# apart. cr_necessary is named for necessary-condition reasoning and its stem reads
# "most seriously undermines", which makes it an evidence question and not an assumption
# one. Checking the rendered stem rather than the id moved it a category.
#
# LSAC's own descriptions, carried as the points arrays in LSAT_SKILLS, are the test of
# whether a schema belongs:
#   lsat_lr_assum  "Detecting assumptions made by particular arguments"
#   lsat_lr_evid   "Determining how additional evidence affects an argument",
#                  "Strengthening and weakening", "Ruling out an alternative explanation"
#
# lsat_lr_flaw was held back when cr_sample was the only flaw schema in the pool, because
# every generated flaw item would then have been an unrepresentative sample, and a
# category whose label promises the common patterns of bad reasoning and delivers one of
# them teaches the wrong model of it. g_flaw.py adds three more patterns, so the category
# now draws on four distinct errors: an unrepresentative sample, a requirement read as a
# guarantee, a property carried between a whole and its parts, and a claim settled by its
# source. All four are errors LSAC and GMAC both name.
#
# Structure, principle and explanation have no counterpart in the pool and stay hand
# written. Conclusion has none here either; it is generated by g_lsat_concl.py, which is
# written against the LSAT's own category and so is wired in build_banks.EXAM_EXTRA.
LSAT_MAP = {
    "lsat_lr_assum": ["cr_cause_assume", "cr_plan_assume"],
    "lsat_lr_evid": ["cr_cause_weaken", "cr_plan_weaken", "cr_plan_eval",
                     "cr_percent", "cr_necessary"],
    "lsat_lr_flaw": ["cr_sample", "cr_necsuff", "cr_partwhole", "cr_authority"],
    # Reading Comprehension, from the long passage corpus only. The short corpus is GMAT
    # length and serving it under an LSAT label would misdescribe the format, which is why
    # these are the _long variants rather than the schemas the GMAT uses. These categories
    # ship well under target and say so: the count is gated on how many passages exist,
    # and eight is what is written.
    "lsat_rc_stated": ["rc_stated_long"],
    "lsat_rc_main": ["rc_main_long"],
    # Both of these ask what follows from the passage rather than what it states, which is
    # LSAC's "information or ideas that can be inferred".
    "lsat_rc_inf": ["rc_infer_long", "rc_caveat_long"],
}

# An editorial judgement, recorded so it can be argued with, like the other two. The CR
# schemas are authored at GMAT difficulty, and the LSAT is sat by a population that has
# already self-selected into graduate admissions, so the same argument runs easier there
# than it does on the GMAT. One band, and anything already at the top stays there.
LSAT_BUMP = 1

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
    elif exam == "lsat":
        table, section, bump = LSAT_MAP, "LR", LSAT_BUMP
    else:
        raise ValueError(exam)
    out = {}
    for skill, ids in table.items():
        gens = []
        for gid in ids:
            g = pool.get(gid)
            if g is None:
                raise KeyError("mapping names a schema that does not exist: %s" % gid)
            gens.append(wrap(g, skill, SECTION_OVERRIDE.get(skill, section), bump))
        out[skill] = gens
    return out
