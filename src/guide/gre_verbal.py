"""GRE Verbal Reasoning, topic by topic.

Three question types and nothing else: text completion, sentence equivalence, and
reading comprehension. The section is short and adaptive between its two modules, so
the questions are dense rather than numerous.

The GRE differs from every other verbal section we cover in one respect that changes
how to study it: vocabulary is load bearing. Two of the three question types put a
blank in a sentence and ask which word belongs there, and no amount of strategy
recovers a word you do not know. What strategy does buy is the ability to work out
which KIND of word belongs there, which is often enough to answer without knowing every
choice.

Same IP position as the rest of the guide: language and logic belong to nobody, no
other author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

VOCAB, RC = "Vocabulary in Context", "Reading Comprehension"

TOPICS = [

    Topic(
        slug="gre-text-completion",
        title="Text Completion",
        area=VOCAB,
        skill="gre_tc",
        idea="One, two or three blanks in a short passage, and each blank is decided by "
             "the rest of the sentence rather than by which word sounds most impressive.",
        why="Text completion is the largest slice of GRE verbal. With multiple blanks "
            "there is no partial credit, so the discipline of predicting each blank "
            "before reading any choice is what separates a reliable score from a "
            "coin flip.",
        facts=[
            ("The format", "one to three blanks, three choices each, no partial credit",
             "A three-blank question with two right is scored the same as none right."),
            ("The method", "cover the choices, predict each blank in your own words",
             "Then match. This is the whole technique and it is not optional at three "
             "blanks."),
            ("Start with the easiest blank", "not necessarily the first",
             "Filling one blank often constrains the others."),
            ("Find the clue", "the sentence contains the answer's meaning somewhere",
             "A definition, a restatement, a contrast, or an example."),
            ("Contrast signals", "but, however, although, despite, far from, rather than",
             "The blank means roughly the opposite of the nearby idea."),
            ("Continuation signals", "and, moreover, indeed, in fact, that is",
             "The blank means roughly the same as the nearby idea."),
            ("Charge first", "positive, negative or neutral",
             "Settling the charge eliminates choices before precise meaning matters."),
            ("Punctuation carries logic", "a colon or a semicolon often signals "
             "restatement",
             "What follows a colon usually explains what came before it."),
        ],
        worked=[
            dict(ask="'Though the committee's report was praised for its candour, its "
                     "recommendations proved so ___ that no department could determine "
                     "what was being asked of it.' Predict the blank.",
                 steps=[
                     "'Though' sets up a contrast with 'praised for its candour'.",
                     "Candour means frankness and clarity, so the blank is the opposite "
                     "of that: unclear.",
                     "The second clause confirms it: no department could determine what "
                     "was asked.",
                     "Predict: vague. Then look for the choice closest to vague, such as "
                     "nebulous or amorphous.",
                 ],
                 answer="A word meaning vague or unclear",
                 why="The prediction was made from two clues pointing the same way, which "
                     "is how these sentences are built. Note that you do not need to know "
                     "every choice: you need to recognise one that means vague, and "
                     "eliminate any that do not."),
        ],
        traps=[
            "Reading the choices before predicting. Every choice is a real word used "
            "correctly somewhere, and reading them first makes several sound plausible.",
            "Filling blanks in order rather than starting with the most constrained one.",
            "Missing a contrast word, which reverses the meaning you need and leaves you "
            "choosing a synonym of the clue.",
            "Choosing the hardest word because the GRE is known for vocabulary. The exam "
            "tests fit, and the hard word is often the wrong one.",
        ],
        ladder={
            1: "One blank with a plain restatement clue.",
            2: "One blank where a contrast word reverses the direction.",
            3: "Two blanks, where filling one constrains the other.",
            4: "Three blanks with clues distributed across the whole passage.",
            5: "The clue is structural rather than lexical: the sentence's logic, not any "
               "one word, tells you what belongs.",
        },
    ),

    Topic(
        slug="gre-sentence-equivalence",
        title="Sentence Equivalence",
        area=VOCAB,
        skill="gre_se",
        idea="Pick TWO of six words that both fit the sentence and produce the same "
             "meaning, which means the answer is a pair rather than two separate "
             "choices.",
        why="This format rewards a specific habit: predicting the meaning first and then "
            "looking for a pair. Hunting for synonyms among the six without a prediction "
            "is how people pick a pair that fits each other and not the sentence.",
        facts=[
            ("The format", "six choices, choose exactly two, no partial credit",
             "Both must be right or the question scores zero."),
            ("The two must fit the sentence", "and produce the same meaning",
             "Two synonyms that do not fit are a trap, and the exam includes them."),
            ("Predict first, then pair", "same method as text completion",
             "Find the meaning the sentence needs, then find two words carrying it."),
            ("Not every synonym pair is the answer", "the exam plants extra pairs",
             "Usually one pair fits and another pair is synonymous but wrong for the "
             "sentence."),
            ("A word with no partner is wrong", "the answer is always a pair",
             "If a choice has no plausible match among the other five, eliminate it."),
            ("Same meaning, not same word", "the resulting sentences must mean the same",
             "Two words can both fit and give different meanings, which fails the test."),
            ("Order does not matter", "it is a set of two",
             "Selecting the same two in either order is the same answer."),
        ],
        worked=[
            dict(ask="'The normally ___ curator surprised the trustees by objecting "
                     "loudly to the acquisition.' Choices: taciturn, voluble, reticent, "
                     "meticulous, garrulous, punctilious.",
                 steps=[
                     "Clue: 'surprised' plus 'objecting loudly' means the behaviour was "
                     "out of character, so normally the curator is quiet.",
                     "Predict: quiet, reserved.",
                     "Scan for a pair meaning quiet: taciturn and reticent. Both fit.",
                     "Check the decoys: voluble and garrulous are a genuine synonym pair "
                     "meaning talkative, and they contradict the sentence. Meticulous and "
                     "punctilious are a third pair meaning careful, which fits nothing in "
                     "the clue.",
                 ],
                 answer="taciturn and reticent",
                 why="Three synonym pairs among six choices, and only one matches the "
                     "prediction. That is the standard construction. Without predicting "
                     "first, all three pairs look equally like answers, which is exactly "
                     "the effect intended."),
        ],
        traps=[
            "Finding a synonym pair and selecting it without checking it against the "
            "sentence.",
            "Selecting two words that both fit but mean different things, which fails the "
            "equivalence requirement.",
            "Choosing only one word you are confident about and guessing the second. Both "
            "must be right, so a confident single is worth nothing on its own.",
            "Missing a contrast or a signal of surprise, which flips the meaning needed.",
        ],
        ladder={
            1: "A plain clue and one obvious synonym pair.",
            2: "Two pairs exist and only one fits the sentence.",
            3: "The clue is a contrast that must be noticed to get the direction right.",
            4: "Three pairs exist and the sentence's logic is what selects between them.",
            5: "The correct two are not close synonyms in isolation and are equivalent "
               "only in this sentence's context.",
        },
    ),

    Topic(
        slug="gre-reading-comp",
        title="Reading Comprehension on the GRE",
        area=RC,
        skill="gre_rc",
        idea="GRE passages are short and dense rather than long and discursive, so the "
             "reading is slower per line and the questions sit closer to the text than "
             "they look.",
        why="People carry SAT reading habits into the GRE and lose time. These passages "
            "pack a full argument into a paragraph or two, and skimming for structure "
            "works less well when every sentence is structural.",
        facts=[
            ("Passage length", "typically one to five paragraphs, often short",
             "A one-paragraph passage may still carry three questions."),
            ("Read for the argument", "what is claimed, and what is offered for it",
             "GRE passages argue more often than they describe."),
            ("Select-in-passage questions", "choose a sentence that does a stated job",
             "You click a sentence rather than a lettered choice, so the answer is exact."),
            ("Multiple-answer questions", "choose all that apply, one to three",
             "Each choice is independently true or false; there is no partial credit."),
            ("Inference standard", "must be supported, not merely plausible",
             "The same standard as every other exam, and the same everyday-usage trap."),
            ("Watch the hedges", "may, suggests, some, tends to",
             "GRE authors qualify heavily, and answers that drop the qualifier are "
             "wrong."),
            ("Vocabulary matters here too", "a word you misread changes the claim",
             "Dense passages give you fewer chances to recover from a misread word."),
        ],
        worked=[
            dict(ask="A passage says: 'While the theory accounts for the observed "
                     "distribution in temperate zones, its extension to tropical systems "
                     "rests on an assumption that has not been independently verified.' "
                     "Which is supported: (A) the theory is wrong about tropical systems, "
                     "(B) the theory's application to tropical systems depends on an "
                     "unverified assumption, (C) the theory has been verified for "
                     "temperate zones?",
                 steps=[
                     "(B) restates the second clause almost exactly. Check it: rests on "
                     "an assumption not independently verified. Supported.",
                     "(A) turns unverified into wrong, which is the everyday-usage trap. "
                     "Unverified means not yet established either way.",
                     "(C) says the temperate case is verified. The passage says the "
                     "theory ACCOUNTS FOR the distribution there, which is not the same "
                     "as independent verification.",
                 ],
                 answer="(B)",
                 why="(C) is the subtler trap because it feels like a fair reading of "
                     "'accounts for'. The passage uses 'independently verified' for one "
                     "half and not the other, and that asymmetry is deliberate. On dense "
                     "passages the exact verb is usually where the question lives."),
        ],
        traps=[
            "Treating unverified, unproven or untested as equivalent to false.",
            "Dropping a hedge, so 'may contribute' becomes 'contributes'.",
            "Answering a select-all question after finding one correct choice. Each one "
            "has to be evaluated.",
            "Skimming a GRE passage the way a longer passage can be skimmed. There is "
            "less redundancy here, so less to skip.",
        ],
        ladder={
            1: "A short passage and an answer that restates one sentence.",
            2: "The answer paraphrases and a hedge must be preserved.",
            3: "A select-all question where two of three choices are supported.",
            4: "The passage distinguishes two claims with different levels of support "
               "and the question turns on that asymmetry.",
            5: "A select-in-passage question where several sentences do something close "
               "to the stated job and only one does it exactly.",
        },
    ),

    Topic(
        slug="gre-rc-arguments",
        title="Argument Questions Inside Reading Comprehension",
        area=RC,
        skill="gre_rc",
        idea="Some GRE reading questions are critical reasoning in disguise: a short "
             "argument, and a question about what would strengthen, weaken or is assumed "
             "by it.",
        why="These are scored as reading comprehension and behave like logic questions, "
            "so recognising which one you are looking at decides whether you go hunting "
            "in the passage or reasoning about a gap.",
        facts=[
            ("Recognising one", "the passage is one short argument, not a description",
             "A premise, a conclusion, and a question about the link between them."),
            ("Find the conclusion first", "the claim the rest supports",
             "Not necessarily the last sentence."),
            ("The gap", "the distance between what is shown and what is claimed",
             "Every one of these questions is about the gap, from some angle."),
            ("Weaken", "make the conclusion harder to believe",
             "Attack the link, not the premises, which are given as true."),
            ("Strengthen", "close the gap, usually by ruling out an alternative",
             "More of the same evidence rarely helps."),
            ("Assumption", "what the argument needs and never says",
             "Negate a candidate: if the argument collapses, that is the assumption."),
            ("Argument evaluation", "which question would be most useful to answer",
             "Test it both ways: does the argument move on yes and on no."),
        ],
        worked=[
            dict(ask="'Since the museum introduced free evening entry, weekday attendance "
                     "has risen by 18 percent. The free evenings are therefore "
                     "responsible for the increase.' Which most weakens this?",
                 steps=[
                     "Conclusion: the free evenings caused the rise. Evidence: attendance "
                     "rose after they began.",
                     "Gap: after is being read as because.",
                     "Weaken by supplying an alternative cause covering the same period.",
                     "For instance: a major exhibition opened the same week and drew "
                     "visitors at all times of day.",
                 ],
                 answer="Evidence of another cause operating over the same period",
                 why="Notice what does NOT weaken it: that the free evenings cost the "
                     "museum money, or that some visitors dislike crowds. Both are "
                     "negative facts about the policy and neither touches whether it "
                     "caused the rise, which is the only thing the conclusion claimed."),
        ],
        traps=[
            "Treating an argument question as a detail question and searching the passage "
            "for a stated answer that is not there.",
            "Attacking a premise rather than the reasoning.",
            "Choosing a fact that is merely bad news about the subject rather than "
            "damaging to the argument.",
            "Strengthening by repeating the evidence, which was already granted.",
        ],
        ladder={
            1: "A plain causal claim and an obvious alternative cause.",
            2: "The correct answer is an assumption the argument needs.",
            3: "Two answers are relevant and only one bears on the conclusion drawn.",
            4: "The conclusion is a recommendation, so weakening means showing the plan "
               "fails.",
            5: "The question asks what would be most useful to determine, so each option "
               "must be tested in both directions.",
        },
    ),
]
