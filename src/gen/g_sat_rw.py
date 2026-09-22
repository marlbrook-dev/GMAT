"""SAT Standard English Conventions (rw_sec) and Expression of Ideas (rw_eoi).

Grammar is the part of the verbal section that generates honestly: the rules are
finite and mechanical, so the key follows from the rule rather than from taste, and
each distractor breaks one NAMED rule that the explanation then names.

The volume comes from composition. A sentence is assembled from independent slots
(a subject, the phrase that comes between it and its verb, a predicate), so a few
dozen hand written pieces yield thousands of distinct sentences, the same way a
numeric schema yields thousands of distinct equations. Every slot is written so the
rule under test has exactly one correct resolution; anything arguable is left out,
because an item with two defensible answers is worse than no item.
"""
from framework import Gen, ItemError


# --- shared inventories -------------------------------------------------------
# (singular head, plural head, plural of-phrase) so the head and the nearest noun
# disagree in number, which is the whole difficulty of subject verb agreement.
HEADS = [
    ("The collection", "The collections", "of fossils"),
    ("The list", "The lists", "of committee members"),
    ("The box", "The boxes", "of replacement parts"),
    ("The study", "The studies", "of migratory patterns"),
    ("The bundle", "The bundles", "of letters"),
    ("The set", "The sets", "of instructions"),
    ("The shipment", "The shipments", "of textbooks"),
    ("The recording", "The recordings", "of the interviews"),
    ("The series", "The series", "of experiments"),
    ("The stack", "The stacks", "of survey maps"),
    ("The crate", "The crates", "of glass negatives"),
    ("The register", "The registers", "of parish births"),
]
MODIFIERS = [
    "that the museum acquired last spring",
    "stored behind the workshop",
    "circulated before the vote",
    "compiled over three decades",
    "found in the attic",
    "printed on the back panel",
    "delayed by the storm",
    "recovered from the flooded basement",
    "assembled by the previous curator",
    "kept in the north reading room",
]
# (third person singular, plural or base form, predicate tail)
VERBS = [
    ("was", "were", "catalogued by volunteers."),
    ("has", "have", "been there since the renovation."),
    ("includes", "include", "two entries added last year."),
    ("suggests", "suggest", "a shift in timing."),
    ("seems", "seem", "to assume prior experience."),
    ("arrives", "arrive", "on Thursday."),
    ("remains", "remain", "in the city archive."),
    ("describes", "describe", "a method no longer in use."),
]


class SubjectVerbAgreement(Gen):
    id = "sat_rw_sva"
    skill = "rw_sec"
    section = "RW"
    sub = "Form, structure, and sense"
    diff = 2
    fmt = staticmethod(str)

    def build(self, rng):
        sg, pl, of = rng.choice(HEADS)
        mid = rng.choice(MODIFIERS)
        vsg, vpl, tail = rng.choice(VERBS)
        if sg == pl:
            raise ItemError("head noun has no number contrast")
        plural = rng.choice([True, False])
        subj = "%s %s" % (pl if plural else sg, of)
        right, wrong = (vpl, vsg) if plural else (vsg, vpl)
        # Non finite forms a student reaches for when the intervening phrase makes the
        # number of the head hard to see. Built from the base form so they read as real
        # English rather than as a mangled verb.
        base = {"was": "be", "were": "be", "has": "have", "have": "have"}.get(vpl, vpl)
        return {
            "stem": "Which choice completes the text so that it conforms to the conventions "
                    "of Standard English?\n\n%s %s ______ %s" % (subj, mid, tail),
            "answer": right,
            "distractors": [
                (wrong, "agreeing the verb with \"%s\", the noun nearest to it, instead of "
                        "with \"%s\", the head of the subject. The words between a subject "
                        "and its verb never change the subject's number."
                        % (of.split()[-1], (pl if plural else sg).split()[-1])),
                ("being", "a participle, which cannot serve as the main verb of a sentence."),
                (base, "an unconjugated form that agrees with nothing."),
                ("having been", "a non finite phrase that leaves the sentence without a main verb."),
            ],
            "expl": "The head of the subject is \"%s\", which is %s, so the verb must be "
                    "\"%s\". The phrase \"%s %s\" describes the subject but does not change "
                    "its number."
                    % ((pl if plural else sg).split()[-1], "plural" if plural else "singular",
                       right, of, mid),
        }


PRONOUN_SUBJECTS = [
    ("Each of the researchers", "his or her", True),
    ("Every applicant", "his or her", True),
    ("Neither of the two candidates", "his or her", True),
    ("Each of the volunteers", "his or her", True),
    ("The committee", "its", False),
    ("The orchestra", "its", False),
    ("The board of trustees", "its", False),
    ("The research team", "its", False),
    ("Neither of the two proposals", "its", False),
    ("Each of the museums", "its", False),
]
PRONOUN_TAILS = [
    "submitted ______ findings before the deadline.",
    "published ______ recommendations in March.",
    "revised ______ position after the hearing.",
    "recorded ______ first album in a converted church.",
    "must list ______ previous affiliations.",
    "defended ______ conclusions at the symposium.",
    "withdrew ______ application in the spring.",
]


class PronounAgreement(Gen):
    id = "sat_rw_pronoun"
    skill = "rw_sec"
    section = "RW"
    sub = "Form, structure, and sense"
    diff = 2
    fmt = staticmethod(str)

    def build(self, rng):
        subj, right, human = rng.choice(PRONOUN_SUBJECTS)
        tail = rng.choice(PRONOUN_TAILS)
        if human and "album" in tail:
            raise ItemError("predicate does not fit a personal antecedent")
        other = "its" if human else "his or her"
        return {
            "stem": "Which choice completes the text so that it conforms to the conventions "
                    "of Standard English?\n\n%s %s" % (subj, tail),
            "answer": right,
            "distractors": [
                ("their", "matching the pronoun to the plural noun inside the subject phrase "
                          "rather than to \"%s\", which is singular." % subj.split()[0]),
                (other, "a pronoun of the wrong kind for this antecedent."),
                ("they're", "a contraction of \"they are\", which is not a possessive at all."),
                ("it's", "a contraction of \"it is\", which is not a possessive at all."),
                ("theirs", "a possessive that stands alone and cannot precede a noun."),
            ],
            "expl": "\"%s\" is singular, so the possessive pronoun must be singular: \"%s\". "
                    "A plural noun inside the subject phrase does not make the subject plural."
                    % (subj, right),
        }


APOS_NOUNS = [("student", "students"), ("scientist", "scientists"), ("architect", "architects"),
              ("author", "authors"), ("engineer", "engineers"), ("curator", "curators"),
              ("botanist", "botanists"), ("historian", "historians"),
              ("translator", "translators"), ("surveyor", "surveyors"),
              ("composer", "composers"), ("printer", "printers")]
APOS_TAILS = ["notes were later published.", "conclusions drew wide attention.",
              "designs were exhibited that autumn.", "records remain in the archive.",
              "drafts were bound in a single volume.", "objections were entered into the minutes.",
              "instruments were sold at auction.", "correspondence filled four boxes."]


class ApostropheUse(Gen):
    id = "sat_rw_apostrophe"
    skill = "rw_sec"
    section = "RW"
    sub = "Boundaries"
    diff = 2
    fmt = staticmethod(str)

    def build(self, rng):
        sg, pl = rng.choice(APOS_NOUNS)
        tail = rng.choice(APOS_TAILS)
        plural = rng.choice([True, False])
        right = pl + "'" if plural else sg + "'s"
        return {
            "stem": "Which choice completes the text so that it conforms to the conventions "
                    "of Standard English?\n\nThe ______ %s" % tail,
            "answer": right,
            "distractors": [
                (pl, "a plural with no apostrophe, which cannot show possession."),
                (sg + "'s" if plural else pl + "'",
                 "the possessive of the wrong number, which changes how many owners there are."),
                (sg, "a bare singular, which shows neither possession nor number."),
                (pl + "'s", "a plural s followed by a singular possessive, which is not a form "
                            "in English."),
            ],
            "expl": "The sentence needs a possessive, and the possessor is %s, so the form is "
                    "\"%s\": the apostrophe goes %s the s."
                    % ("plural" if plural else "singular", right,
                       "after" if plural else "before"),
        }


CLAUSE_A = [
    "The tide receded well past the usual mark",
    "The kiln reached temperature just after dawn",
    "Snow fell steadily through the afternoon",
    "The archive opened to the public in 1974",
    "The bridge was closed for inspection",
    "Rain had softened the ground overnight",
    "The ferry ran only twice a day that winter",
    "The survey stakes had been moved",
    "The press was installed on the ground floor",
    "The lease expired at the end of the quarter",
]
CLAUSE_B = [
    "the boats settled into the mud",
    "the glaze began to fuse",
    "the survey crew turned back",
    "its catalogue remained incomplete for years",
    "traffic was diverted through the old town",
    "the excavation resumed at first light",
    "supplies had to be ordered well in advance",
    "the boundary had to be walked again",
    "deliveries came through the side entrance",
    "the tenants moved to a building two streets away",
]


class CommaSplice(Gen):
    id = "sat_rw_boundary"
    skill = "rw_sec"
    section = "RW"
    sub = "Boundaries"
    diff = 3
    fmt = staticmethod(str)

    def build(self, rng):
        a = rng.choice(CLAUSE_A)
        b = rng.choice(CLAUSE_B)
        style = rng.choice(["semicolon", "period", "and"])
        right = {"semicolon": "%s; %s." % (a, b),
                 "period": "%s. %s." % (a, b[0].upper() + b[1:]),
                 "and": "%s, and %s." % (a, b)}[style]
        return {
            "stem": "Which choice completes the text so that it conforms to the conventions "
                    "of Standard English?\n\n______",
            "answer": right,
            "distractors": [
                ("%s, %s." % (a, b),
                 "a comma splice: a comma on its own cannot join two complete sentences."),
                ("%s %s." % (a, b),
                 "a run on: two complete sentences with no punctuation between them."),
                ("%s; and %s." % (a, b),
                 "a semicolon and a coordinating conjunction together, where either alone "
                 "would do the job."),
                ("%s, %s;" % (a, b),
                 "a comma splice that also ends the sentence on a semicolon."),
            ],
            "expl": "\"%s\" and \"%s\" are each complete sentences. Joining two complete "
                    "sentences takes a semicolon, a period, or a comma plus a coordinating "
                    "conjunction. A comma alone is a splice." % (a, b),
        }


class Transitions(Gen):
    id = "sat_rw_transition"
    skill = "rw_eoi"
    section = "RW"
    sub = "Transitions"
    diff = 3
    fmt = staticmethod(str)

    # Each case is written so that exactly one relation fits the pair. The subject
    # matter varies independently of the relation, which is where the volume comes from.
    CASES = [
        ("contrast",
         ["The survey found that most residents supported the proposal.|turnout at the public meeting was the lowest in a decade.",
          "The alloy resists corrosion better than any earlier formulation.|it becomes brittle below freezing.",
          "Early reviews praised the novel's structure.|it sold fewer than four hundred copies.",
          "The instrument was calibrated the previous week.|its readings drifted throughout the trial.",
          "The colony expanded rapidly in its first decade.|almost none of its original buildings survive.",
          "The method is widely taught in introductory courses.|few working laboratories still rely on it."],
         ["However,", "Nevertheless,", "By contrast,", "Even so,"]),
        ("result",
         ["The river had been rerouted a century earlier to power the mills.|the original channel is now visible only as a shallow depression.",
          "Funding for the observatory was withdrawn in 1931.|the survey was never completed.",
          "The pigment was ground far more finely than was usual.|the surface reflects light unevenly.",
          "The archive was stored in an unheated outbuilding.|many of the bindings have warped.",
          "The species has no natural predator on the island.|its population has doubled every four years.",
          "The road was built along the old drove route.|it follows the ridge rather than the valley floor."],
         ["Consequently,", "As a result,", "Therefore,"]),
        ("example",
         ["Several species in the region have adapted to the shorter growing season.|the alpine poppy now flowers three weeks earlier than it did in 1950.",
          "The workshop produced objects for a range of buyers.|a single ledger page lists a bishop, a brewer, and a ship's captain.",
          "Some of the letters were written in haste.|one breaks off in the middle of a sentence.",
          "The technique appears across the whole of the period.|a bowl from the earliest layer already shows it.",
          "Several instruments in the collection were altered by later owners.|the 1690 viol has a nineteenth century neck."],
         ["For example,", "For instance,"]),
        ("addition",
         ["The new catalogue lists every manuscript held by the library.|it records the provenance of each one.",
          "The survey mapped the field boundaries in detail.|it identified three previously unrecorded wells.",
          "The process uses less water than the older method.|it produces no sulphur dioxide.",
          "The edition restores the original punctuation.|it prints the cancelled passages in an appendix.",
          "The programme trains apprentices in the workshop.|it places them with practising binders for a year."],
         ["In addition,", "Moreover,", "Furthermore,"]),
        ("concession",
         ["The technique produces unusually durable pigments.|it requires equipment that few studios can afford.",
          "The dataset is the largest of its kind.|it covers only a single decade.",
          "The translation reads fluently.|it smooths away much of the original's difficulty.",
          "The design won the competition outright.|it was never built."],
         ["Admittedly,", "To be sure,"]),
        ("sequence",
         ["The samples were washed and dried in the field.|they were sorted by grain size in the laboratory.",
          "The timber was left to season for two winters.|it was cut to length and planed.",
          "The plates were exposed at the telescope.|they were developed in a darkroom on the same site.",
          "The text was set in type and proofed.|the corrected sheets went to the press."],
         ["Afterward,", "Subsequently,"]),
    ]
    WRONG = {
        "contrast": "signals that the second sentence follows from the first, when it cuts against it.",
        "result": "signals a contrast, when the second sentence is a consequence of the first.",
        "example": "signals a contrast or a consequence, when the second sentence is an instance of the first.",
        "addition": "signals a contrast, when the second sentence adds to the first rather than qualifying it.",
        "concession": "signals agreement or consequence, when the second sentence concedes a drawback.",
        "sequence": "signals contrast or cause, when the two sentences are simply steps in order.",
    }
    POOL = {
        "contrast": ["Consequently,", "For example,", "In addition,", "Similarly,", "Afterward,", "Therefore,"],
        "result": ["However,", "Nevertheless,", "By contrast,", "For example,", "Admittedly,", "Even so,"],
        "example": ["However,", "Consequently,", "Nevertheless,", "In addition,", "Afterward,", "Therefore,"],
        "addition": ["However,", "By contrast,", "Nevertheless,", "For example,", "Admittedly,", "Even so,"],
        "concession": ["Consequently,", "Similarly,", "In addition,", "For example,", "Therefore,", "Afterward,"],
        "sequence": ["However,", "By contrast,", "Consequently,", "Admittedly,", "Nevertheless,", "Even so,"],
    }

    def build(self, rng):
        rel, pairs, rights = rng.choice(self.CASES)
        pair = rng.choice(pairs)
        s1, s2 = pair.split("|")
        right = rng.choice(rights)
        pool = [w for w in self.POOL[rel] if w != right]
        rng.shuffle(pool)
        return {
            "stem": "Which choice completes the text with the most logical transition?\n\n"
                    "%s ______ %s" % (s1, s2),
            "answer": right,
            "distractors": [(w, "a transition that %s" % self.WRONG[rel]) for w in pool],
            "expl": "The second sentence stands in a relationship of %s to the first, so the "
                    "transition has to signal %s, which \"%s\" does."
                    % (rel, rel, right.rstrip(",")),
        }


# --- Rhetorical Synthesis -----------------------------------------------------
# Expression of Ideas holds two skills, Rhetorical Synthesis and Transitions, together
# 8 to 12 questions (Table 2, The Digital SAT Suite of Assessments Specifications
# Overview, Summer 2022,
# https://satsuite.collegeboard.org/media/pdf/digital-sat-test-spec-overview.pdf).
# Only Transitions had a schema, so half the published domain had no items at all and
# the category shipped at 971 of its 3300 target on one template.
#
# The item format is the College Board's own, read off RW question 12 of Digital SAT
# Sample Questions and Answer Explanations
# (https://satsuite.collegeboard.org/media/pdf/digital-sat-sample-questions.pdf): a set
# of bulleted research notes, a stated rhetorical goal, and the question "Which choice
# most effectively uses relevant information from the notes to accomplish this goal?"
#
# Generating this honestly needs a different trick from the grammar schemas. There is no
# rule to apply, so the key cannot be derived from one. What can be derived is the
# relationship between the notes: the topic is stored as structured facts, each goal
# names one relationship over those facts, and the sentence that expresses exactly that
# relationship is the key. Every distractor is then another goal's sentence, which makes
# it accurate, drawn from the notes, and wrong only in what it accomplishes. That is the
# actual skill, and it means no distractor is a throwaway.
NAMES = [
    "Dalia Renner", "Tomas Ivarsson", "Priya Ganeshan", "Marcus Oyelaran",
    "Freya Lindholm", "Idris Bakare", "Noor Haddad", "Rafael Quintero",
    "Sunniva Aalto", "Jonah Beckett", "Amara Nwosu", "Kiran Mehta",
    "Elsa Brandt", "Toma Kuwahara", "Lucien Faure", "Rosa Delgado",
    "Owen Trevelyan", "Mei Sato", "Anselm Roth", "Hana Vukovic",
    "Ciaran Doyle", "Yara Mansour", "Petra Novak", "Emeka Chukwu",
]
CITIES = [
    "Lisbon", "Halifax", "Dunedin", "Trieste", "Bergen", "Cork",
    "Valparaiso", "Tallinn", "Hobart", "Ghent", "Reykjavik", "Kaunas",
]
# Each topic is one coherent practice. shared_pl is the trait both works have, written
# for a plural subject; shared_noun is the same trait as a noun phrase; works supply the
# particular that distinguishes them. Nothing here is asserted as fact about a real
# person: these are item parameters, the same way the transition pairs above are.
SYN_TOPICS = [
    dict(role="sculptor", thing="sculpture", things="sculptures",
         shared_pl="are assembled from materials salvaged from demolition sites",
         verb="incorporates",
         works=[("Ridgeline", "roof slates and copper flashing"),
                ("Quarter Turn", "window sashes and cast iron door handles"),
                ("Long Shadow", "scaffold boards and sash weights"),
                ("Undercroft", "floor joists and lengths of lead pipe"),
                ("Second Fixing", "plaster cornice and skirting board"),
                ("Party Wall", "brick, lath, and horsehair plaster")]),
    dict(role="printmaker", thing="print series", things="print series",
         shared_pl="are printed from plates the artist leaves out of doors to corrode",
         verb="was printed from",
         works=[("Tideline", "a zinc plate left in an estuary for a winter"),
                ("Saltmarsh", "a copper plate buried in brackish mud"),
                ("Windbreak", "a steel plate fixed to a fence post for a year"),
                ("Rainshadow", "a plate left under a leaking gutter"),
                ("Hoarfrost", "a plate exposed on a roof through three frosts"),
                ("Spoil Heap", "a plate weighted down in colliery waste")]),
    dict(role="composer", thing="piece", things="pieces",
         shared_pl="are built on recordings of machinery made in working buildings",
         verb="is built on",
         works=[("Card Room", "the sound of a cotton carding machine"),
                ("Dry Dock", "the sound of a riveting hammer"),
                ("Lock Keeper", "the sound of canal lock gates"),
                ("Bell Pit", "the sound of a winding engine"),
                ("Flour Mill", "the sound of a stone dressing hammer"),
                ("Tannery", "the sound of a drum of oak bark")]),
    dict(role="photographer", thing="series", things="series",
         shared_pl="record buildings in the month before they were demolished",
         verb="records",
         works=[("Last Term", "a village school closed after ninety years"),
                ("Notice to Quit", "a terrace of railway cottages"),
                ("Closing Time", "a dockside public house"),
                ("Final Shift", "a rope walk still in use the week before"),
                ("Deconsecrated", "a chapel emptied of its fittings"),
                ("Summer Season", "a pier pavilion after its last concert")]),
    dict(role="weaver", thing="hanging", things="hangings",
         shared_pl="use yarn dyed with plants gathered within a mile of the loom",
         verb="uses",
         works=[("Headland", "weld gathered from a field margin"),
                ("Green Lane", "woad grown on an allotment"),
                ("Coppice", "alder bark from a managed wood"),
                ("Verge", "dyer's chamomile from a roadside"),
                ("Dune Slack", "lichen taken from fallen branches"),
                ("Millrace", "madder root from a garden bed")]),
    dict(role="bookbinder", thing="binding", things="bindings",
         shared_pl="reuse boards taken from books too damaged to repair",
         verb="reuses",
         works=[("Interleaved", "boards from a water damaged atlas"),
                ("Recto", "boards from a fire damaged ledger"),
                ("Endpaper", "boards from a mould damaged hymnal"),
                ("Gathering", "boards from a broken parish register"),
                ("Headband", "boards from a split herbal"),
                ("Fore Edge", "boards from a warped account book")]),
    dict(role="furniture maker", thing="cabinet", things="cabinets",
         shared_pl="are made from single trees felled by storms",
         verb="is made from",
         works=[("Windthrow", "an oak brought down in a gale"),
                ("Crown Shy", "a beech split by lightning"),
                ("Root Plate", "an ash uprooted in flood water"),
                ("Standing Dead", "an elm killed by disease"),
                ("Leader Loss", "a pine snapped above the first branch"),
                ("Hedgerow", "a field maple lost to a storm")]),
    dict(role="ceramicist", thing="vessel", things="vessels",
         shared_pl="are glazed with ash from a single species of wood",
         verb="is glazed with",
         works=[("Sessile", "ash from oak offcuts"),
                ("Withy", "ash from willow prunings"),
                ("Stool Shoot", "ash from hazel rods"),
                ("Suckered", "ash from cherry branches"),
                ("Pollard", "ash from lime poles"),
                ("Windfall", "ash from apple wood")]),
]
# Each goal names one relationship over the stored facts and one sentence that expresses
# it. The other three sentences become this goal's distractors, so what makes a choice
# wrong is never that it is false.
SYN_GOALS = ["similarity", "difference", "introduce", "dates"]
# Transitions runs at a single difficulty, so before this schema every item in the
# category sat at 3 and the adaptive model had nothing to move between. The goals differ
# in what they actually ask for: reading one pair of notes off the list, holding two
# notes against each other, or judging what a reader who knows none of it needs first.
SYN_DIFF = {"dates": 2, "similarity": 3, "difference": 3, "introduce": 4}
SYN_WHY = {
    "similarity": "a sentence that emphasizes what the two %s have in common, which is "
                  "not the goal stated in the question",
    "difference": "a sentence that emphasizes how the two %s differ, which is not the "
                  "goal stated in the question",
    "introduce": "a sentence that introduces the %s, which an audience that already "
                 "knows the work does not need",
    "dates": "a sentence that dates the two %s accurately and establishes no "
             "relationship between them",
    "unsupported": "a claim the notes do not support: they say both %s were shown "
                   "outside the city, not that these were the first to be",
    "onesided": "a note repeated accurately about one %s, where the question asks "
                "about both %s",
    "place": "a true but bare fact about where the %s works, which meets no "
             "rhetorical goal at all",
    "kind": "a sentence that names the two %s and says nothing about them that the "
            "notes had not already said",
    "exhibited": "the one note about the two %s that no stated goal asks for",
}


class RhetoricalSynthesis(Gen):
    id = "sat_rw_synthesis"
    skill = "rw_eoi"
    section = "RW"
    sub = "Rhetorical Synthesis"
    diff = 3
    fmt = staticmethod(str)

    def build(self, rng):
        t = rng.choice(SYN_TOPICS)
        name = rng.choice(NAMES)
        city = rng.choice(CITIES)
        (an, ad), (bn, bd) = rng.sample(t["works"], 2)
        ya = rng.randint(2004, 2015)
        yb = ya + rng.randint(1, 6)
        last = name.split()[-1]
        gap = "a year" if yb - ya == 1 else (
            "%s years" % ["", "", "two", "three", "four", "five", "six"][yb - ya])
        thing, things, role = t["thing"], t["things"], t["role"]

        notes = [
            "%s is a %s based in %s." % (name, role, city),
            "Most of %s's %s %s." % (last, things, t["shared_pl"]),
            "%s (%d) %s %s." % (an, ya, t["verb"], ad),
            "%s (%d) %s %s." % (bn, yb, t["verb"], bd),
            "Both %s were made for exhibitions outside %s." % (things, city),
        ]
        rng.shuffle(notes)

        sent = {
            "similarity": "%s (%d) and %s (%d) %s, like most of %s's %s."
                          % (an, ya, bn, yb, t["shared_pl"], last, things),
            "difference": "%s (%d) %s %s, whereas %s %s %s."
                          % (an, ya, t["verb"], ad, bn, t["verb"], bd),
            "introduce": "%s is a %s based in %s whose %s %s."
                         % (name, role, city, things, t["shared_pl"]),
            # Drawn from the notes and plausible, but the notes say the two were made
            # for exhibitions outside the city, not that they were the first to be.
            "unsupported": "%s (%d) and %s (%d) were the first of %s's %s to be shown "
                           "outside %s, the city where %s is based."
                           % (an, ya, bn, yb, last, things, city, last),
            # Accurate and specific, but about one work where every goal needs both.
            "onesided": "%s (%d) %s %s." % (an, ya, t["verb"], ad),
            # Two more, accurate and off the goal like the rest, and deliberately one
            # much shorter and one much longer than any key. Without them the pool has
            # nothing on one side of a given key and the framework cannot balance where
            # the key falls by length, so the goal becomes readable off the lengths.
            "place": "%s works in %s." % (last, city),
            "kind": "%s (%d) and %s (%d) are both %s." % (an, ya, bn, yb, things),
            "onesidedlong": "%s (%d) %s %s, and it was made for an exhibition held "
                            "outside %s, where %s is based."
                            % (an, ya, t["verb"], ad, city, last),
            "exhibited": "Both %s (%d) and %s (%d) were made for exhibitions held "
                         "outside %s, which is the city where %s is based."
                         % (an, ya, bn, yb, city, last),
            "dates": "%s completed %s in %d and %s in %d, %s later."
                     % (last, an, ya, bn, yb, gap),
        }
        ask = {
            "similarity": "emphasize a similarity between the two %s" % things,
            "difference": "emphasize a difference between the two %s" % things,
            "introduce": "introduce %s's work to an audience unfamiliar with it" % last,
            "dates": "specify when each of the two %s was completed" % things,
        }
        goal = rng.choice(SYN_GOALS)
        # Four candidates for three slots, so the framework can balance the key's
        # length rank. With exactly three the pool has no slack and the rank is fixed by
        # the goal, which would make the goal readable off the choice lengths.
        wrong = [(sent[g], SYN_WHY[g] % (things if g != "introduce" else role))
                 for g in SYN_GOALS if g != goal]
        wrong.append((sent["unsupported"], SYN_WHY["unsupported"] % things))
        wrong.append((sent["onesided"], SYN_WHY["onesided"] % (thing, things)))
        wrong.append((sent["place"], SYN_WHY["place"] % role))
        wrong.append((sent["exhibited"], SYN_WHY["exhibited"] % things))
        wrong.append((sent["kind"], SYN_WHY["kind"] % things))
        wrong.append((sent["onesidedlong"], SYN_WHY["onesided"] % (thing, things)))
        # Shuffled after every candidate is in, not before. The framework fills each
        # side of the key from the front of this list, so anything appended after the
        # shuffle is systematically last in its side and the key's length rank piles up
        # in one place.
        rng.shuffle(wrong)
        rng.shuffle(wrong)
        return {
            "stem": "While researching a topic, a student has taken the following "
                    "notes:\n\n%s\n\nThe student wants to %s. Which choice most "
                    "effectively uses relevant information from the notes to "
                    "accomplish this goal?"
                    % ("\n".join("- " + n for n in notes), ask[goal]),
            "answer": sent[goal],
            "distractors": wrong,
            "diff": SYN_DIFF[goal],
            "expl": "The goal is to %s, and only this choice does that: %s"
                    % (ask[goal], self.BECAUSE[goal] % things),
        }

    BECAUSE = {
        "similarity": "it names both %s and then the trait the notes give to the whole "
                      "body of work, so the reader sees what the two have in common.",
        "difference": "it sets the two %s side by side on the one point where the notes "
                      "have them differ, and says what each one does.",
        "introduce": "it says who the maker is, where they work, and what the %s have "
                     "in common, which is what a reader meeting the work for the first "
                     "time needs.",
        "dates": "it gives the completion year of each of the two %s and claims nothing "
                 "further about them.",
    }

GENS = [SubjectVerbAgreement(), PronounAgreement(), ApostropheUse(), CommaSplice(),
        Transitions(), RhetoricalSynthesis()]
