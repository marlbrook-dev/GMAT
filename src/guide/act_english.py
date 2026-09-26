"""ACT English, topic by topic.

Organised by ACT's own three reporting categories, which is also how our engine scores
the section: Conventions of Standard English, Production of Writing, and Knowledge of
Language.

One number shapes every strategy note here. The section is 50 questions in 35 minutes,
which is about 42 seconds each including reading the passage around them. That is the
tightest per-question budget on any exam we cover, and it is why the section rewards
rules you can apply on sight rather than reasoning you have to construct.

Two habits follow from it. The shortest answer that is grammatically correct and keeps
the meaning is right far more often than not, because the section actively tests
concision. And when a question's stem states a purpose, that purpose decides the answer
and nothing else does, so the stem is worth reading twice even at 42 seconds.

A note on typography. This site does not use em dashes or en dashes anywhere, which is
a house rule. The ACT tests them, so where a dash is the point it is written here as a
double hyphen, the way it is typed in plain text.

Same IP position as the rest of the guide: grammar and rhetoric belong to nobody, no
other author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

CSE, POW, KOL = ("Conventions of Standard English", "Production of Writing",
                 "Knowledge of Language")

TOPICS = [

    Topic(
        slug="act-e-sentence-structure",
        title="Sentence Structure and Boundaries",
        area=CSE,
        skill="act_e_cse",
        idea="Most punctuation questions on this section are one question wearing "
             "different clothes: is each side of the mark a complete sentence, and does "
             "the mark you chose match that answer.",
        why="Boundaries are the largest slice of the conventions category and the fastest "
            "to decide once you run the clause test. At 42 seconds a question, a "
            "mechanical test beats an ear every time.",
        facts=[
            ("Independent clause", "subject plus verb, could stand alone",
             "The test every boundary question runs on."),
            ("Comma splice", "two independent clauses joined by a comma alone",
             "Always wrong, and the most frequently tested error in the category."),
            ("Run-on", "two independent clauses with no punctuation",
             "Equally wrong, and often offered as the shortest choice to tempt you."),
            ("Period and semicolon are equivalent here", "both separate two independent "
             "clauses",
             "So the ACT never offers both as correct answers to one question. If you see "
             "both, neither is right."),
            ("Comma plus FANBOYS", "for, and, nor, but, or, yet, so",
             "A comma before one of these joining two independent clauses is correct."),
            ("Colon", "needs a complete sentence on its LEFT",
             "What follows may be a list, a phrase or a clause; what precedes may not be "
             "a fragment."),
            ("Dash", "written here as -- , does a colon's job, or a pair does commas'",
             "One dash before an explanation, or a matched pair around an interruption."),
            ("Dependent clause markers", "because, although, when, if, since, while",
             "These make a clause unable to stand alone, so the boundary rules change."),
        ],
        worked=[
            dict(ask="'The bridge had been surveyed twice that spring ___ engineers still "
                     "disagreed about the footings.'  (A) NO CHANGE (comma), "
                     "(B) semicolon, (C) comma plus yet, (D) no punctuation.",
                 steps=[
                     "Left: 'The bridge had been surveyed twice that spring'. Independent.",
                     "Right: 'engineers still disagreed about the footings'. Independent.",
                     "Two independent clauses, so (A) is a splice and (D) is a run-on. "
                     "Both out.",
                     "(B) and (C) are both mechanically correct, which cannot happen on a "
                     "real item, so look at meaning: the relationship is contrast, which "
                     "'yet' marks and a semicolon does not. (C).",
                 ],
                 answer="(C)",
                 why="The clause test eliminated half the choices before any judgement "
                     "about meaning. Work in that order: mechanics first, and only when "
                     "two choices survive does the logical relationship decide. It is "
                     "faster and it does not depend on what sounds right."),
        ],
        traps=[
            "Joining two independent clauses with a comma. One rule, tested constantly.",
            "Treating 'however', 'therefore' and 'moreover' as FANBOYS. They are not, so "
            "a comma before one joining two clauses is still a splice.",
            "Putting a colon after a fragment.",
            "Choosing the shortest option when the shortest is a run-on. Concision only "
            "wins among choices that are all correct.",
        ],
        ladder={
            1: "Two short independent clauses with an obvious splice among the choices.",
            2: "One side is a dependent clause, so the rules differ.",
            3: "A colon is offered and the left side must be tested for completeness.",
            4: "'However' appears and is mistaken for a coordinating conjunction.",
            5: "Two choices are mechanically correct and the logical relationship between "
               "the clauses decides.",
        },
    ),

    Topic(
        slug="act-e-usage",
        title="Agreement, Pronouns, Verbs and Modifiers",
        area=CSE,
        skill="act_e_cse",
        idea="The verb agrees with its subject and the pronoun with its antecedent, and "
             "the exam's entire method is putting distance between the two so the nearest "
             "noun is the wrong one.",
        why="These are reliable points once you can find the subject, and finding it is "
            "mechanical: cross out the phrases in between. That beats reading the "
            "sentence aloud, because the sentence was written to sound like the wrong "
            "answer.",
        facts=[
            ("Find the subject", "cross out prepositional phrases and relative clauses",
             "'The row of cabinets IS blocking the door': the subject is row."),
            ("The nearest noun is a decoy", "placed there deliberately",
             "Nearly every agreement item puts a plural noun beside a singular subject."),
            ("Inverted sentences", "there is, there are, here comes",
             "The subject follows the verb, so locate it before choosing."),
            ("Each, every, either, neither", "singular",
             "Even when followed by 'of the' plus a plural."),
            ("As well as, along with, in addition to", "do NOT make a subject plural",
             "Only 'and' does that."),
            ("Pronoun agreement", "singular antecedent takes a singular pronoun",
             "And a pronoun that could refer to two nouns is wrong, however grammatical."),
            ("Who and whom", "who is the subject, whom is the object",
             "Substitute he or him: if him fits, whom is right."),
            ("Dangling modifier", "an opening phrase describes the subject that follows",
             "'Having sealed the deck, the rain caused no damage' says the rain sealed the "
             "deck."),
            ("Verb tense", "match the timeline the passage established",
             "Do not shift without a reason in the text."),
        ],
        worked=[
            dict(ask="'The series of lectures on coastal erosion, delivered by three "
                     "visiting researchers, ___ scheduled for the spring term.'  "
                     "(A) were, (B) was.",
                 steps=[
                     "Cross out the prepositional phrase: 'of lectures on coastal "
                     "erosion'.",
                     "Cross out the participial phrase: 'delivered by three visiting "
                     "researchers'.",
                     "What remains: 'The series ___ scheduled'. Singular.",
                     "So (B) was.",
                 ],
                 answer="(B)",
                 why="Three plural nouns sit between the subject and its verb: lectures, "
                     "researchers, and arguably erosion. That is not an accident, it is "
                     "the item. Crossing out takes three seconds and is more reliable "
                     "than an ear at 42 seconds a question."),
        ],
        traps=[
            "Agreeing with the nearest noun. That is what the item is testing, every "
            "time.",
            "Treating 'as well as' or 'along with' as though they were 'and'.",
            "Fixing a dangling modifier by rewriting the phrase rather than supplying the "
            "right subject.",
            "Leaving a pronoun whose antecedent is ambiguous when a choice naming the noun "
            "is available.",
        ],
        ladder={
            1: "Subject and verb adjacent.",
            2: "One phrase separates them.",
            3: "Several phrases intervene, or the sentence is inverted.",
            4: "The subject is 'each' or 'neither' followed by a plural phrase.",
            5: "A modifier is grammatical in more than one position and placement changes "
               "the meaning.",
        },
    ),

    Topic(
        slug="act-e-punctuation",
        title="Commas, Apostrophes and Internal Punctuation",
        area=CSE,
        skill="act_e_cse",
        idea="Inside a sentence, punctuation marks off material that could be removed, "
             "and the test is whether the sentence still works and still identifies its "
             "subject without it.",
        why="Comma questions are frequent and feel arbitrary until you see that almost all "
            "of them are one idea: is this element essential to identifying what is being "
            "talked about, or is it extra.",
        facts=[
            ("Non-essential elements", "surrounded by a matched pair of commas",
             "Remove it and the sentence still says who or what it is about."),
            ("Essential elements", "no commas at all",
             "Remove it and you no longer know which thing is meant."),
            ("The pair rule", "one comma before means one comma after",
             "A single comma around an interruption is always wrong."),
            ("Matched marks", "commas, dashes or parentheses, but not mixed",
             "A comma at one end and a dash at the other is wrong."),
            ("Never between subject and verb", "however long the subject",
             "A long subject invites a comma the rule forbids."),
            ("Items in a series", "commas between three or more",
             "Two items joined by 'and' take no comma."),
            ("Its and it's", "its is possessive, it's is it is",
             "The possessive pronoun has no apostrophe, the reverse of nouns."),
            ("Singular and plural possessive", "apostrophe s, or s then apostrophe",
             "The student's notebook; the students' notebooks."),
            ("Plain plurals take no apostrophe", "ever",
             "Decades, names and ordinary plurals."),
            ("When in doubt, fewer commas", "the ACT penalises unnecessary ones",
             "A comma needs a reason; length is not one."),
        ],
        worked=[
            dict(ask="Which is correct: (A) 'The surveyor, who mapped the northern "
                     "boundary, later disputed the findings.' (B) 'The surveyor who "
                     "mapped the northern boundary later disputed the findings.' What "
                     "decides it?",
                 steps=[
                     "Apply the removal test to 'who mapped the northern boundary'.",
                     "If the passage has already told you which surveyor, the clause is "
                     "extra: use the pair of commas, (A).",
                     "If there were several surveyors and this clause is what identifies "
                     "this one, it is essential: no commas, (B).",
                     "Context decides, which is why these items always give you the "
                     "surrounding sentences.",
                 ],
                 answer="(A) if the surveyor is already identified, (B) if the clause "
                        "identifies them",
                 why="The commas change the meaning, which is why the rule is not "
                     "arbitrary. With them there is one surveyor; without them there were "
                     "several and this is the one who disputed the findings."),
        ],
        traps=[
            "Using one comma where a matched pair is needed.",
            "Placing a comma between a long subject and its verb.",
            "Writing it's for the possessive. Expanding to 'it is' settles it instantly.",
            "Adding an apostrophe to a plain plural, especially a decade or a surname.",
        ],
        ladder={
            1: "An introductory phrase needing a comma after it.",
            2: "A plain its and it's or possessive choice.",
            3: "A non-essential clause needing a matched pair.",
            4: "The essential and non-essential distinction changes meaning and context "
               "decides.",
            5: "The choices mix commas, dashes and parentheses and the matched pair rule "
               "eliminates most of them.",
        },
    ),

    Topic(
        slug="act-e-organization",
        title="Organization, Transitions and Placement",
        area=POW,
        skill="act_e_pow",
        idea="Transitions are decided by the logical relationship between two sentences, "
             "and placement questions are decided by what the sentence refers to.",
        why="These are fully mechanical once you name the relationship, and they are where "
            "people lose time by reading only the sentence containing the blank. The "
            "relationship needs both halves.",
        facts=[
            ("Name the relationship first", "then match a transition to it",
             "Reading the choices first makes several of them sound plausible."),
            ("Contrast", "however, nevertheless, by contrast, still, on the other hand",
             "The second sentence cuts against the first."),
            ("Continuation", "moreover, furthermore, in addition, similarly, also",
             "The second adds more of the same."),
            ("Cause and effect", "therefore, thus, consequently, as a result",
             "The second follows from the first."),
            ("Example", "for example, for instance, specifically",
             "The second is a case of the first."),
            ("Sequence", "first, next, meanwhile, finally",
             "Only when the passage is genuinely ordering events."),
            ("Sentence placement", "follow the referring words",
             "A sentence beginning 'This method' must come after the method is named."),
            ("Pronouns constrain order", "a pronoun cannot precede its antecedent",
             "The single most reliable clue on placement questions."),
            ("Paragraph placement", "same logic, one level up",
             "Find what the paragraph refers back to and put it after that."),
        ],
        worked=[
            dict(ask="Where should this sentence go: 'Such kilns, however, required "
                     "continuous tending, which few small workshops could afford.'",
                 steps=[
                     "'Such kilns' refers back, so the sentence must follow a place where "
                     "a specific kind of kiln has been described.",
                     "'however' signals contrast, so what precedes should be a point in "
                     "the kilns' favour.",
                     "So: immediately after the sentence describing the advantage of that "
                     "kiln type.",
                     "It cannot go before the kilns are introduced, whatever else is true "
                     "of the paragraph.",
                 ],
                 answer="Directly after the sentence describing that kiln type's advantage",
                 why="Two words did the whole job: 'Such' points backwards and 'however' "
                     "says what it points back to is a positive. Placement questions are "
                     "almost always decided by referring words, which is why scanning for "
                     "them first is faster than reading the paragraph as a whole."),
        ],
        traps=[
            "Reading only the sentence with the blank. The relationship needs the sentence "
            "before it.",
            "Choosing a cause transition because the second sentence contains causal "
            "words internally.",
            "Placing a sentence before the thing its pronoun or demonstrative refers to.",
            "Using a sequence transition when nothing is in sequence.",
        ],
        ladder={
            1: "A plain contrast or continuation between two short sentences.",
            2: "Cause and effect must be told from contrast.",
            3: "A placement question decided by one referring word.",
            4: "One sentence contains internal logic words pointing the other way.",
            5: "Two transitions are in the same family and the passage's structure decides "
               "which degree of contrast fits.",
        },
    ),

    Topic(
        slug="act-e-purpose",
        title="Topic Development and Questions With a Stated Purpose",
        area=POW,
        skill="act_e_pow",
        idea="When the stem states a goal, the goal is the only criterion, and the "
             "best-written choice that does a different job is wrong.",
        why="This is the question type where the stem carries all the information and "
            "gets skimmed at 42 seconds each. Adding or deleting text, and whether a "
            "passage achieved a purpose, are decided entirely by what the stem asked for.",
        facts=[
            ("Read the stem twice", "it names the goal",
             "To emphasise, to introduce, to provide a specific example, to conclude."),
            ("The goal is the only test", "not elegance, not interest, not accuracy",
             "Every choice is usually true; only one does the stated job."),
            ("Add or delete questions", "decide by relevance to the paragraph's point",
             "Then pick the reason that matches, because the reasons are also graded."),
            ("The reason must be right too", "yes-because and no-because",
             "Two choices may share your yes or no and differ in why, and only one is "
             "credited."),
            ("Delete is often correct", "if the material is off point or repeats",
             "The ACT genuinely rewards removing text, more than people expect."),
            ("Whole-essay questions", "at the end, about whether the passage did X",
             "Judge the passage as a whole, not the final paragraph."),
            ("Specificity", "when the stem asks for a specific detail, vague loses",
             "And when it asks to conclude, a new fact loses."),
        ],
        worked=[
            dict(ask="The stem asks for the choice that most effectively emphasises the "
                     "scale of the excavation. Which wins: (A) the excavation was "
                     "significant, (B) the excavation was carried out carefully over "
                     "several seasons, (C) the excavation removed 40,000 cubic metres of "
                     "fill across eleven sites?",
                 steps=[
                     "Goal: emphasise SCALE.",
                     "(A) 'significant' is vague and could mean importance rather than "
                     "size.",
                     "(B) is about care and duration, which is a different quality "
                     "entirely.",
                     "(C) gives magnitude in numbers, which is what scale means.",
                 ],
                 answer="(C)",
                 why="(A) and (B) are both true and well written and do different jobs. "
                     "That is the shape of every stated-purpose question: the wrong "
                     "answers are not wrong about the facts, they are wrong about the "
                     "task. Which is why the stem is worth the extra two seconds."),
        ],
        traps=[
            "Skimming the stem. It is the only thing that distinguishes the choices.",
            "Choosing the most detailed or most elegant option when the stem asked for "
            "something else.",
            "Getting the yes or no right and the reason wrong on an add-or-delete "
            "question.",
            "Keeping text because it is interesting. Interesting is not relevant.",
        ],
        ladder={
            1: "The stem is plain and only one choice attempts the goal.",
            2: "Two choices attempt it and one does it more directly.",
            3: "An add-or-delete question where the reason distinguishes two choices.",
            4: "The goal is to conclude or to introduce, so a new fact disqualifies an "
               "otherwise good choice.",
            5: "A whole-essay question where the final paragraph suggests one answer and "
               "the passage as a whole supports another.",
        },
    ),

    Topic(
        slug="act-e-style",
        title="Concision, Style and Word Choice",
        area=KOL,
        skill="act_e_kol",
        idea="Among choices that are all grammatically correct and all keep the meaning, "
             "the shortest is usually right, because redundancy is what this category "
             "tests.",
        why="Knowledge of Language is the smallest category and the most rule-like. "
            "Recognising redundancy on sight is worth real time on a section where the "
            "budget is 42 seconds a question.",
        facts=[
            ("Shortest correct answer", "usually right",
             "Only among choices that are correct and preserve the meaning. It is a "
             "tiebreak, not a first move."),
            ("Redundancy", "two words doing one job",
             "Past history, unexpected surprise, joined together, annual yearly."),
            ("Wordiness", "a phrase where a word will do",
             "Due to the fact that means because; in order to means to."),
            ("OMIT and DELETE", "real options and often correct",
             "If removing it loses nothing, remove it."),
            ("Consistent register", "match the passage's level",
             "A casual phrase in a formal passage is wrong even when grammatical."),
            ("Word choice", "the precise word, not the impressive one",
             "Affect and effect, fewer and less, among and between."),
            ("Idiom", "the preposition a word takes",
             "Different from, capable of, comply with, preferable to."),
            ("Do not confuse concision with omission", "meaning must survive",
             "The shortest choice is wrong if it drops something the sentence needed."),
        ],
        worked=[
            dict(ask="'The committee reconvened again in order to discuss the matter of "
                     "the budget once more.' Which is best: (A) NO CHANGE, "
                     "(B) reconvened again to discuss the budget, (C) reconvened to "
                     "discuss the budget, (D) reconvened once more in order to discuss "
                     "the budget again?",
                 steps=[
                     "Find the redundancies. 'Reconvened' already means met again, so "
                     "'again' and 'once more' are both redundant.",
                     "'In order to' is wordy for 'to'.",
                     "'The matter of the budget' is wordy for 'the budget'.",
                     "(C) removes all three and keeps the meaning. (B) keeps 'again', "
                     "(D) keeps everything.",
                 ],
                 answer="(C)",
                 why="Three separate redundancies in one sentence, which is typical of "
                     "this category. Note the shortest choice won here because it was "
                     "also correct and complete, not merely because it was shortest. "
                     "That order matters: check correctness first, then length."),
        ],
        traps=[
            "Applying 'shortest is best' before checking that the short choice is correct "
            "and complete.",
            "Missing a redundancy because both words are common, such as 'reconvened "
            "again'.",
            "Choosing a more elaborate phrasing because it sounds more formal. The ACT "
            "does not reward ornament.",
            "Overlooking OMIT as an option when the underlined text adds nothing.",
        ],
        ladder={
            1: "One obvious redundancy among the choices.",
            2: "A wordy phrase has a one-word equivalent.",
            3: "OMIT is correct and must be recognised as a real option.",
            4: "The shortest choice drops necessary meaning and a slightly longer one is "
               "right.",
            5: "Two choices are equally concise and register or idiom decides.",
        },
    ),
]
