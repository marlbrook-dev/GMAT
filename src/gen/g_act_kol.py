"""ACT Knowledge of Language (act_e_kol): concision, redundancy, and tone.

ACT names three things under this heading: precise and concise word choice,
consistency of style and tone, and cutting redundancy. All three are decidable by
rule rather than by taste, which is what makes them generatable: a phrase that says
the same thing twice is redundant whoever reads it, and "due to the fact that" is
longer than "because" in every sentence either one appears in.

Each distractor here is a named fault, not a near miss: one repeats the idea, one
inflates the phrasing, one breaks the register the sentence has already set.
"""
from framework import Gen, ItemError


# Each redundancy carries its own sentence. A generic frame does not work here:
# "annual yearly" modifies a report, "past history" does not modify a design, and
# slotting them interchangeably produced sentences like "the past history designs".
# (sentence with {X}, redundant phrase, concise replacement, what is doubled)
REDUNDANT = [
    ("The committee published its {X} report on water quality in the district.",
     "annual yearly", "annual", "annual and yearly mean the same thing"),
    ("The archivist summarised the {X} of the building in two pages.",
     "past history", "history", "history is already an account of the past"),
    ("The society set out its {X} for the coming season.",
     "future plans", "plans", "a plan is already about the future"),
    ("Every visitor received a {X} at the door.",
     "free gift", "gift", "a gift is already free"),
    ("The two rivers are {X} below the weir.",
     "joined together", "joined", "joining is already a bringing together"),
    ("The course begins with the {X} of surveying.",
     "basic fundamentals", "fundamentals", "fundamentals are already basic"),
    ("The inquiry reported its {X} in November.",
     "final outcome", "outcome", "an outcome is already the end of the matter"),
    ("The cottage stands in {X} to the mill.",
     "close proximity", "proximity", "proximity is already nearness"),
    ("Residents were given {X} of the closure.",
     "advance warning", "warning", "a warning already comes in advance"),
    ("The discovery came as an {X} to the excavators.",
     "unexpected surprise", "surprise", "a surprise is already unexpected"),
    ("The clerk read a {X} of the previous meeting.",
     "brief summary", "summary", "a summary is already brief"),
    ("The lecturer had to {X} the final point.",
     "repeat again", "repeat", "repeating is already doing it a second time"),
    ("The two departments {X} on the survey.",
     "collaborate together", "collaborate", "collaboration is already joint"),
    ("The treaty depended on {X} between the ports.",
     "mutual cooperation", "cooperation", "cooperation is already mutual"),
    ("The trial produced the same {X} each time.",
     "end result", "result", "a result already comes at the end"),
    ("The firm patented a {X} in glass moulding.",
     "new innovation", "innovation", "an innovation is already new"),
    ("The engineer produced a {X} of the mechanism.",
     "rough estimate approximation", "rough estimate", "an estimate is already an approximation"),
    ("The society keeps the {X} in a locked case.",
     "original prototype", "prototype", "a prototype is already the original"),
    ("The warden gave the {X} instructions to the crew.",
     "necessary essential", "essential", "essential and necessary say the same thing"),
    ("The vote produced a {X} in the committee.",
     "consensus of opinion", "consensus", "a consensus is already an agreement of opinion"),
    ("The surveyor noted the {X} of the boundary.",
     "exact same", "exact", "exact and same are doing one job between them"),
    ("The report set out the {X} of the accident.",
     "true facts", "facts", "a fact is already true"),
    ("The mill kept a {X} of every delivery.",
     "written record", "record", "a record of this kind is already written"),
    ("The plan was abandoned as {X}.",
     "completely unanimous", "unanimous", "unanimous is already complete"),
    ("The clerk filed a {X} of the agreement.",
     "duplicate copy", "copy", "a duplicate is already a copy"),
    ("The society issued a {X} to its members.",
     "personal opinion", "opinion", "an opinion is already personal"),
]

# Inflated phrasings, each with the sentence it actually fits. Mixing them was a
# real bug: the frames need a subordinating conjunction, so dropping a verb phrase
# into one produced "The survey was postponed concluded that the ground had frozen".
# Grouping by what the phrase is grammatically keeps every draw a sentence.
# (sentence with {X}, inflated phrasing, plain replacement, another inflated phrase
#  of the SAME grammatical kind, so the wrong choices are still sentences)
WORDY = [
    ("The survey was postponed {X} the ground had frozen solid overnight.",
     "due to the fact that", "because", "in spite of the fact that"),
    ("The archive will close {X} the building can be rewired.",
     "for the purpose of ensuring that", "so that", "due to the fact that"),
    ("The society reprinted the map {X} members had asked for copies.",
     "due to the fact that", "because", "in the event that"),
    ("The kiln was relit {X} the glaze tests could be finished.",
     "in order that", "so that", "in spite of the fact that"),
    ("The ferry stopped running {X} the harbour silted up.",
     "as a consequence of the fact that", "because", "in the event that"),
    ("The lecture will go ahead {X} the speaker recovers in time.",
     "in the event that", "if", "due to the fact that"),
    ("The bridge remained open {X} the flooding was severe.",
     "in spite of the fact that", "although", "due to the fact that"),
    ("The society met {X} the second Tuesday of every month.",
     "on a regular basis on", "on", "for the purpose of"),
    ("The trustees {X} sell the west field.",
     "made the decision to", "decided to", "came to the conclusion that they should"),
    ("The inspector {X} the repairs had never been carried out.",
     "came to the conclusion that", "concluded that", "made the determination that"),
    ("{X} the excavation, three wells were uncovered.",
     "During the course of", "During", "For the duration of"),
    ("The mill employed {X} weavers from the surrounding villages.",
     "a large number of", "many", "a considerable quantity of"),
    ("The lighthouse was automated {X} the last keeper retired.",
     "at the point in time when", "when", "due to the fact that"),
    ("The harvest failed {X} the rains came too late.",
     "owing to the fact that", "because", "in the event that"),
    ("The tram line closed {X} the council could not fund the repairs.",
     "for the reason that", "because", "in spite of the fact that"),
    ("The society keeps the ledgers {X} anyone should wish to consult them.",
     "in the event that", "in case", "due to the fact that"),
    ("The quarry reopened {X} demand for stone recovered.",
     "at such time as", "when", "in spite of the fact that"),
    ("The record survives {X} the fire destroyed most of the archive.",
     "in spite of the fact that", "although", "due to the fact that"),
    ("The surveyors worked {X} the whole of the summer.",
     "throughout the entirety of", "throughout", "for the duration of"),
    ("The map was redrawn {X} the boundary moved.",
     "each and every time that", "whenever", "in the event that"),
    ("The engine ran {X} the fuel lasted.",
     "for as long a period as", "as long as", "in spite of the fact that"),
    ("The vote was delayed {X} more members could attend.",
     "in order that", "so that", "for the purpose of"),
    ("The kiln reached temperature {X} an hour.",
     "in the space of approximately", "in about", "for a period of roughly"),
    ("The society published the findings {X} the excavation ended.",
     "subsequent to the time that", "after", "prior to the start of"),
    ("The collection was moved {X} the roof began to leak.",
     "as a result of the fact that", "because", "in the event that"),
    ("The apprentice worked {X} the master permitted.",
     "to whatever extent that", "as far as", "in spite of the fact that"),
    ("The gate stays locked {X} the warden opens it at dawn.",
     "up until such time as", "until", "due to the fact that"),
    ("The society meets {X} the hall is available.",
     "provided that the condition holds that", "provided that", "in the event that"),
    ("The bell was recast {X} it cracked in the frost.",
     "by reason of the fact that", "because", "in spite of the fact that"),
    ("The ledger records payments {X} 1804 and 1829.",
     "in the period between", "between", "during the course of"),
]

# (formal sentence with {X}, the formal completion, a casual one, why it breaks)
TONE = [
    ("The committee concluded that the proposal was {X}.",
     "financially unsound", "a total money pit",
     "slang in a sentence whose register is formal throughout"),
    ("The report describes the decline as {X}.",
     "gradual but unmistakable", "kinda slow but pretty obvious",
     "casual usage in an otherwise formal report"),
    ("The curator judged the attribution to be {X}.",
     "unreliable", "pretty sketchy",
     "informal vocabulary against the formal frame of the sentence"),
    ("The board considered the timetable {X}.",
     "unrealistic", "a complete joke",
     "a colloquial idiom inside a formal minute"),
    ("Inspectors found the repairs to be {X}.",
     "inadequate", "a bit rubbish",
     "a casual register the surrounding sentence does not share"),
    ("The tribunal held the evidence to be {X}.",
     "insufficient", "way too thin",
     "a conversational intensifier in a formal finding"),
    ("The auditors described the accounts as {X}.",
     "materially incomplete", "kind of a mess",
     "a casual noun phrase in a formal audit statement"),
    ("The surveyor reported the foundations to be {X}.",
     "structurally sound", "totally fine, no worries",
     "a reassurance addressed to the reader rather than a finding"),
    ("The panel found the methodology {X}.",
     "insufficiently documented", "super vague",
     "an informal intensifier in a formal assessment"),
    ("The trustees judged the endowment {X}.",
     "adequate for the purpose", "good enough, probably",
     "a hedge that no formal minute would record"),
    ("The inspectorate deemed the records {X}.",
     "incomplete in several respects", "all over the place",
     "an idiom that formal prose does not use"),
    ("The review described the translation as {X}.",
     "broadly faithful to the original", "pretty much spot on",
     "colloquial phrasing against a formal review"),
]


class Redundancy(Gen):
    id = "act_kol_redundancy"
    skill = "act_e_kol"
    section = "E"
    sub = "Cutting redundancy"
    diff = 2
    fmt = staticmethod(str)

    def build(self, rng):
        frame, red, concise, why = rng.choice(REDUNDANT)
        wordy = rng.choice(WORDY)[1]
        return {
            "stem": "Which choice best fits the underlined portion of the sentence?\n\n"
                    + frame.replace("{X}", "______"),
            "answer": concise,
            "distractors": [
                (red, "a redundancy: %s, so one of the two words is doing no work." % why),
                ("%s %s" % (rng.choice(["essential", "important", "very"]), red),
                 "the same redundancy with a third word stacked on top of it."),
                ("the aforementioned %s" % concise, "a formal filler that adds length without "
                                                    "adding meaning, which is the fault this "
                                                    "question is about."),
                (wordy + " " + concise, "a plain phrase weighed down by an inflated one."),
            ],
            "expl": "\"%s\" says the same thing twice, because %s. \"%s\" carries the whole "
                    "meaning on its own." % (red, why, concise),
        }


class Concision(Gen):
    id = "act_kol_concision"
    skill = "act_e_kol"
    section = "E"
    sub = "Precise and concise word choice"
    diff = 2
    fmt = staticmethod(str)

    def build(self, rng):
        frame, long_form, short_form, other_long = rng.choice(WORDY)
        return {
            "stem": "Which choice best fits the underlined portion of the sentence?\n\n"
                    + frame.replace("{X}", "______"),
            "answer": short_form,
            "distractors": [
                (long_form, "a phrase of several words doing the work of one, with nothing gained."),
                (other_long, "an inflated phrase that also names the wrong relationship "
                             "between the two halves of the sentence."),
                ("%s the fact that" % short_form, "the concise word with the inflated tail "
                                                  "still attached to it."),
                ("%s, and" % short_form, "a conjunction that joins the clauses without naming "
                                         "the relationship between them."),
            ],
            "expl": "\"%s\" says in one word what \"%s\" takes several to say. On the ACT the "
                    "shortest choice that keeps the meaning and stays grammatical is normally "
                    "the right one." % (short_form, long_form),
        }


class ToneConsistency(Gen):
    id = "act_kol_tone"
    skill = "act_e_kol"
    section = "E"
    sub = "Consistency in style and tone"
    diff = 3
    fmt = staticmethod(str)

    def build(self, rng):
        frame, formal, casual, why = rng.choice(TONE)
        other = rng.choice([t for t in TONE if t[1] != formal])
        return {
            "stem": "The sentence below appears in a formal report. Which choice keeps the "
                    "style and tone consistent?\n\n" + frame.replace("{X}", "______"),
            "answer": formal,
            "distractors": [
                (casual, "%s." % why),
                (other[2], "a casual phrase, and one borrowed from a sentence about something "
                           "else entirely."),
                (formal + ", honestly", "an aside addressed to the reader, which formal prose "
                                        "does not use."),
                (formal.upper(), "capitals used for emphasis, which formal prose does not do."),
            ],
            "expl": "The sentence is formal throughout, so the completion must be too. "
                    "\"%s\" matches it; the alternatives break the register, which is exactly "
                    "what this question tests." % formal,
        }


GENS = [Redundancy(), Concision(), ToneConsistency()]
