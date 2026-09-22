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
    ("The folder", "The folders", "of planning applications"),
    ("The carton", "The cartons", "of glass slides"),
    ("The album", "The albums", "of pressed flowers"),
    ("The ledger", "The ledgers", "of quarterly accounts"),
    ("The catalogue", "The catalogues", "of donated instruments"),
    ("The report", "The reports", "of the inspection visits"),
    ("The index", "The indexes", "of parish surnames"),
    ("The tray", "The trays", "of seedlings"),
    ("The reel", "The reels", "of survey film"),
    ("The drawer", "The drawers", "of type"),
    ("The chart", "The charts", "of tidal readings"),
    ("The file", "The files", "of correspondence"),
    ("The sample", "The samples", "of river sediment"),
    ("The batch", "The batches", "of test castings"),
    ("The roll", "The rolls", "of drawings"),
    ("The packet", "The packets", "of seed"),
    ("The case", "The cases", "of mounted specimens"),
    ("The portfolio", "The portfolios", "of student drawings"),
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
    "catalogued by the previous assistant",
    "left in the basement since the move",
    "listed in the appendix",
    "returned by the lending library",
    "prepared for the inspection",
    "marked for disposal last year",
    "drawn up before the boundary changed",
    "kept under the counter",
    "sent on from the county office",
    "checked against the original",
    "withdrawn from display in June",
    "copied for the planning committee",
    "gathered during the first season",
    "annotated by an unknown hand",
    "shelved beside the map cabinet",
    "found folded inside another volume",
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
    ("shows", "show", "a gap of several years."),
    ("appears", "appear", "in the 1931 inventory."),
    ("names", "name", "three people not listed elsewhere."),
    ("covers", "cover", "only the first two seasons."),
    ("requires", "require", "attention from a conservator."),
    ("records", "record", "the weather on each day."),
    ("belongs", "belong", "to the founding collection."),
    ("needs", "need", "rehousing before the winter."),
    ("carries", "carry", "a note in the same hand."),
    ("contradicts", "contradict", "the published account."),
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
    ("Each of the applicants", "his or her", True),
    ("Every researcher", "his or her", True),
    ("Neither of the two surveyors", "his or her", True),
    ("Each of the trustees", "his or her", True),
    ("Every candidate", "his or her", True),
    ("Neither of the two editors", "his or her", True),
    ("Each of the apprentices", "his or her", True),
    ("Every contributor", "his or her", True),
    ("Each of the delegates", "his or her", True),
    ("The society", "its", False),
    ("The panel", "its", False),
    ("The foundation", "its", False),
    ("The consortium", "its", False),
    ("The tribunal", "its", False),
    ("Neither of the two agencies", "its", False),
    ("Each of the archives", "its", False),
    ("The partnership", "its", False),
    ("Neither of the two reports", "its", False),
]
# Each tail says which antecedent it fits: any, a person, or a body. The schema used to
# carry one hand written exception, "if human and album in tail", which is the shape of
# rule that only covers the case its author had in front of them: the next incompatible
# tail needs a new exception and the person adding it has no way to know that. A tag on
# the data cannot be forgotten in the same way.
PRONOUN_TAILS = [
    ("submitted ______ findings before the deadline.", "any"),
    ("published ______ recommendations in March.", "any"),
    ("revised ______ position after the hearing.", "any"),
    ("recorded ______ first album in a converted church.", "body"),
    ("must list ______ previous affiliations.", "any"),
    ("defended ______ conclusions at the symposium.", "any"),
    ("withdrew ______ application in the spring.", "any"),
    ("circulated ______ draft to the other members.", "any"),
    ("entered ______ objection in the minutes.", "any"),
    ("filed ______ accounts a month late.", "any"),
    ("named ______ successor at the meeting.", "any"),
    ("presented ______ evidence to the inquiry.", "any"),
    ("kept ______ records in the same format throughout.", "any"),
    ("declared ______ interest before the vote.", "any"),
    ("set out ______ reasoning in an appendix.", "any"),
    ("withheld ______ support until the second reading.", "any"),
    ("moved ______ collection into storage.", "body"),
    ("amended ______ constitution that year.", "body"),
    ("opened ______ reading room to the public.", "body"),
    ("published ______ first catalogue in 1958.", "body"),
    ("signed ______ name at the foot of the page.", "person"),
    ("left ______ notebooks to the institution.", "person"),
    ("gave ______ address without notes.", "person"),
    ("completed ______ training in under a year.", "person"),
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
        want = "person" if human else "body"
        pool = [t for t, fits in PRONOUN_TAILS if fits in ("any", want)]
        tail = rng.choice(pool)
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


# (singular, plural, kind). kind is person or body, and the tails below say which they
# fit, for the same reason the pronoun tails do: a tail written for one and drawn for the
# other reads as a mistake the student has to stop and rule out.
#
# The second group are nouns whose plural is not the singular plus one character. With
# regular nouns only, the five forms this schema can offer are ordered by length by
# construction, so the key sits at the same rank on every item and 861 shipped items were
# answerable at 100 percent by picking the third shortest without reading (INC-0079).
APOS_NOUNS = [
    ("student", "students", "person"), ("scientist", "scientists", "person"),
    ("architect", "architects", "person"), ("author", "authors", "person"),
    ("engineer", "engineers", "person"), ("curator", "curators", "person"),
    ("botanist", "botanists", "person"), ("historian", "historians", "person"),
    ("translator", "translators", "person"), ("surveyor", "surveyors", "person"),
    ("composer", "composers", "person"), ("printer", "printers", "person"),
    ("conservator", "conservators", "person"), ("editor", "editors", "person"),
    ("geologist", "geologists", "person"), ("archivist", "archivists", "person"),
    ("cartographer", "cartographers", "person"), ("naturalist", "naturalists", "person"),
    ("photographer", "photographers", "person"), ("librarian", "librarians", "person"),
    ("chemist", "chemists", "person"), ("sculptor", "sculptors", "person"),
    ("weaver", "weavers", "person"), ("binder", "binders", "person"),
    ("physician", "physicians", "person"), ("inspector", "inspectors", "person"),
    ("registrar", "registrars", "person"), ("astronomer", "astronomers", "person"),
    ("apprentice", "apprentices", "person"), ("collector", "collectors", "person"),
    ("lecturer", "lecturers", "person"),
    ("secretary", "secretaries", "person"), ("apothecary", "apothecaries", "person"),
    ("notary", "notaries", "person"), ("witness", "witnesses", "person"),
    ("company", "companies", "body"), ("laboratory", "laboratories", "body"),
    ("factory", "factories", "body"), ("registry", "registries", "body"),
    ("foundry", "foundries", "body"), ("society", "societies", "body"),
    ("academy", "academies", "body"), ("agency", "agencies", "body"),
    ("parish", "parishes", "body"), ("press", "presses", "body"),
    ("church", "churches", "body"),
]
APOS_TAILS = [
    ("notes were later published.", "any"),
    ("conclusions drew wide attention.", "any"),
    ("designs were exhibited that autumn.", "any"),
    ("records remain in the archive.", "any"),
    ("drafts were bound in a single volume.", "any"),
    ("objections were entered into the minutes.", "any"),
    ("instruments were sold at auction.", "any"),
    ("correspondence filled four boxes.", "any"),
    ("letters were catalogued in 1962.", "any"),
    ("measurements were checked twice.", "any"),
    ("reports were bound for the library.", "any"),
    ("specimens were relabelled that year.", "any"),
    ("photographs were printed from the originals.", "any"),
    ("accounts were audited in the spring.", "any"),
    ("plans were approved without amendment.", "any"),
    ("proofs were returned uncorrected.", "any"),
    ("tools were given to the workshop.", "any"),
    ("maps were redrawn for the second edition.", "any"),
    ("papers were deposited with the county archive.", "any"),
    ("findings were disputed at the time.", "any"),
    ("sketchbooks were left to the college.", "person"),
    ("lecture notes survive in two copies.", "person"),
    ("observations were published posthumously.", "person"),
    ("testimony was read into the record.", "person"),
]
# A blank that wants the plain plural, not a possessive. Mixing these in is better as an
# item, because telling a plural from a possessive is the distinction the domain is about
# and asking only "which possessive" never tests it. It is also the only thing that moves
# the key off one length rank: the possessive is the second longest of the five forms by
# construction, so an item that wants it can never put the key near the bottom.
# The same idea for a singular subject. With all four modes the schema tests the whole
# plural and possessive contrast rather than only "which possessive", and the key lands
# at a different length rank in each, which is what takes it off one rank.
APOS_SING_TAILS = [
    ("was listed among the founders.", "any"),
    ("had occupied the same site since 1890.", "any"),
    ("published the findings the following year.", "any"),
    ("signed the register on the way in.", "person"),
    ("worked from a set of drawings supplied by the architect.", "person"),
    ("met the inspector at the gate.", "person"),
    ("arrived before the building was open.", "person"),
    ("shared an office on the top floor.", "person"),
    ("was founded a decade before the others.", "body"),
    ("operated from an industrial estate outside the town.", "body"),
]
APOS_PLAIN_TAILS = [
    ("were listed in the order they joined.", "any"),
    ("disagreed about where the boundary ran.", "any"),
    ("had occupied the same site since 1890.", "any"),
    ("published their findings in the same year.", "any"),
    ("met in the long room every Tuesday.", "person"),
    ("arrived before the building was open.", "person"),
    ("worked from the same set of drawings.", "person"),
    ("signed the register on the way in.", "person"),
    ("had been trained at the same institution.", "person"),
    ("shared an office on the top floor.", "person"),
    ("were founded within a decade of each other.", "body"),
    ("operate from the same industrial estate.", "body"),
]


class ApostropheUse(Gen):
    id = "sat_rw_apostrophe"
    skill = "rw_sec"
    section = "RW"
    sub = "Boundaries"
    diff = 2
    fmt = staticmethod(str)

    def build(self, rng):
        # The family is drawn first so the two are evenly represented. Within a family
        # the gaps between the five forms are fixed, so the key's length rank is fixed
        # too; drawing the noun straight from one list let whichever family was larger
        # decide the rank for most of the bank (INC-0079).
        regular = [n for n in APOS_NOUNS if n[1] == n[0] + "s"]
        other = [n for n in APOS_NOUNS if n[1] != n[0] + "s"]
        sg, pl, kind = rng.choice(rng.choice([regular, other]))
        mode = rng.choice(["sg_poss", "pl_poss", "plain_pl", "plain_sg"])
        if mode == "plain_sg":
            tail = rng.choice([t for t, f in APOS_SING_TAILS if f in ("any", kind)])
            right = sg
            wrongs = [
                (pl, "a plural, where the verb calls for a singular subject."),
                (sg + "'s", "a singular possessive, where nothing in the sentence is owned."),
                (pl + "'", "a plural possessive, which is wrong in both number and kind."),
                (pl + "'s", "a plural s followed by a singular possessive, which is not a "
                            "form in English."),
                (sg + "'", "a singular with the apostrophe after it, which is not a form "
                           "of this word at all."),
            ]
            expl = ("The verb is singular and nothing in the sentence belongs to the %s, "
                    "so the subject is the bare singular, \"%s\"." % (sg, right))
        elif mode == "plain_pl":
            tail = rng.choice([t for t, f in APOS_PLAIN_TAILS if f in ("any", kind)])
            right = pl
            wrongs = [
                (sg + "'s", "a singular possessive, where the sentence needs a plain plural."),
                (pl + "'", "a plural possessive, where nothing in the sentence is owned."),
                (sg, "a bare singular, where the verb calls for a plural subject."),
                (pl + "'s", "a plural s followed by a singular possessive, which is not a "
                            "form in English."),
                (sg + "'", "a singular with the apostrophe after it, which is not a form "
                           "of this word at all."),
            ]
            expl = ("Nothing in the sentence belongs to the %s, so no apostrophe is "
                    "wanted: the subject is simply the plural, \"%s\"." % (sg, right))
        else:
            plural = mode == "pl_poss"
            tail = rng.choice([t for t, f in APOS_TAILS if f in ("any", kind)])
            right = pl + "'" if plural else sg + "'s"
            wrongs = [
                (pl, "a plural with no apostrophe, which cannot show possession."),
                (sg + "'s" if plural else pl + "'",
                 "the possessive of the wrong number, which changes how many owners "
                 "there are."),
                (sg, "a bare singular, which shows neither possession nor number."),
                (pl + "'s", "a plural s followed by a singular possessive, which is not a "
                            "form in English."),
                (sg + "'", "a singular with the apostrophe after it, which is the plural "
                           "possessive form of a different word."),
            ]
            expl = ("The sentence needs a possessive, and the possessor is %s, so the form "
                    "is \"%s\": the apostrophe goes %s the s."
                    % ("plural" if plural else "singular", right,
                       "after" if plural else "before"))
        return {
            "stem": "Which choice completes the text so that it conforms to the conventions "
                    "of Standard English?\n\nThe ______ %s" % tail,
            "answer": right,
            "distractors": wrongs,
            "expl": expl,
        }


# Two clauses drawn from two flat lists gave items like "The lease expired at the end of
# the quarter. The glaze began to fuse.", which is punctuated correctly and about nothing.
# The punctuation is what is being tested, so an incoherent pair is not wrong, but a
# student reading it has to decide whether they have misunderstood the sentence, and that
# is not the skill. Grouping by subject costs nothing and multiplies the same way: twelve
# sets of five and five is three hundred coherent pairs where two flat lists of ten gave
# a hundred incoherent ones.
CLAUSE_SETS = [
    (["The tide receded well past the usual mark",
      "The ferry ran only twice a day that winter",
      "A gale had been blowing since the small hours",
      "The harbour master closed the north quay",
      "The channel had silted badly over the summer"],
     ["the boats settled into the mud",
      "the crossing had to be booked a week ahead",
      "no vessel left the harbour for three days",
      "cargo was landed on the south side instead",
      "the dredger was brought back into service"]),
    (["The kiln reached temperature just after dawn",
      "The clay had been left to weather for a year",
      "The glaze was mixed to an old recipe",
      "A crack opened in the kiln floor",
      "The firing ran six hours longer than planned"],
     ["the glaze began to fuse",
      "the weathered clay threw more easily than fresh",
      "the colour came out darker than expected",
      "the next firing had to be postponed",
      "the fuel bill for the month doubled"]),
    (["The archive opened to the public in 1974",
      "The catalogue was compiled by a single volunteer",
      "A water pipe burst above the store room",
      "The reading room was rewired that summer",
      "The collection arrived in eighty unlabelled boxes"],
     ["the catalogue remained incomplete for years",
      "cataloguing took the better part of a decade",
      "several boxes of correspondence were lost",
      "readers were sent to the annexe for a term",
      "sorting the boxes took three seasons of work"]),
    (["The bridge was closed for inspection",
      "Rain had softened the ground overnight",
      "The old surface was lifted in a single day",
      "A water main was found under the verge",
      "The diversion added four miles to the route"],
     ["traffic was diverted through the old town",
      "the excavation resumed at first light",
      "the new layer went down before the frost",
      "the work stopped for a fortnight",
      "the bus timetable was rewritten for the duration"]),
    (["The survey stakes had been moved",
      "Snow fell steadily through the afternoon",
      "The theodolite had not been calibrated since spring",
      "Fog closed in before the second reading",
      "The landowner withdrew permission at short notice"],
     ["the boundary had to be walked again",
      "the survey crew turned back",
      "every angle was taken twice as a check",
      "the team returned the following week",
      "the eastern field was left unmapped"]),
    (["The press was installed on the ground floor",
      "The type had been cast for an earlier edition",
      "The paper arrived damp from the mill",
      "A single compositor set the whole volume",
      "The binder was working two streets away"],
     ["deliveries came through the side entrance",
      "several sorts were missing from the case",
      "the sheets were hung to dry for two days",
      "composition took the better part of a year",
      "finished sheets were carried across by hand"]),
    (["The lease expired at the end of the quarter",
      "The roof had been patched rather than replaced",
      "The building was listed the following year",
      "Damp had reached the first floor",
      "The freeholder refused to renew"],
     ["the tenants moved to a building two streets away",
      "water came through at the first heavy rain",
      "no further alterations were permitted",
      "the lower rooms were taken out of use",
      "the shop closed after forty years"]),
    (["The frost came three weeks early that year",
      "The orchard had not been pruned in a decade",
      "A hedge was taken out to widen the field",
      "The well ran dry in August",
      "The herd was sold at the autumn market"],
     ["the blossom was lost across the whole valley",
      "the trees carried far more wood than fruit",
      "the yield rose but the soil began to blow",
      "water had to be carted from the village",
      "the pasture was ploughed the following spring"]),
    (["The school took its first pupils in 1908",
      "The hall was requisitioned for two years",
      "A second teacher was appointed that term",
      "The roll fell below thirty",
      "The playground was resurfaced over the summer"],
     ["the logbook survives from the first day",
      "lessons were held in the chapel instead",
      "the older children were taught separately",
      "the authority proposed closing the school",
      "the children used the village green for a month"]),
    (["The museum acquired the collection in 1953",
      "A single case held the whole of the bequest",
      "The lighting was replaced with fibre optics",
      "The gallery was closed for six months",
      "The founder left no record of provenance"],
     ["much of the collection has never been displayed",
      "the remainder went into the reserve store",
      "the watercolours could be shown at last",
      "the touring exhibition went ahead regardless",
      "several attributions remain uncertain"]),
    (["The branch line closed in 1964",
      "The signal box was manned until the end",
      "Frost lifted the ballast that winter",
      "A landslip blocked the cutting",
      "The station buildings were sold at auction"],
     ["the track was lifted the following spring",
      "the levers are now in a museum",
      "speed was restricted for most of the season",
      "services terminated at the junction for a month",
      "one of the station buildings is now a private house"]),
    (["The samples were collected before the thaw",
      "The balance had drifted since its last service",
      "A power cut stopped the centrifuge",
      "The reagent was two years past its date",
      "The freezer failed over the holiday"],
     ["the samples were analysed within the week",
      "every weight was taken three times",
      "the run had to be started again",
      "the results were discarded as unreliable",
      "the whole series was lost"]),
]


class CommaSplice(Gen):
    id = "sat_rw_boundary"
    skill = "rw_sec"
    section = "RW"
    sub = "Boundaries"
    diff = 3
    fmt = staticmethod(str)

    def build(self, rng):
        ca, cb = rng.choice(CLAUSE_SETS)
        a = rng.choice(ca)
        b = rng.choice(cb)
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
