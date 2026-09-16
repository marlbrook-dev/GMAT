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


GENS = [SubjectVerbAgreement(), PronounAgreement(), ApostropheUse(), CommaSplice(), Transitions()]
