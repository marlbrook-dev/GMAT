"""ACT Reading, topic by topic.

Organised by ACT's own three reporting categories, which is also how our engine scores
the section: Key Ideas and Details, Craft and Structure, and Integration of Knowledge
and Ideas.

The section's defining constraint is time. Four passage sets in 35 to 40 minutes means
roughly eight or nine minutes each including the reading, which is less per passage
than any other exam here gives. Everything below is shaped by that: read for structure,
answer from the text, and do not reread.

One passage set is Paired Passages, two shorter texts by different authors asked about
together, which is where the Integration of Knowledge and Ideas questions concentrate.

Same IP position as the rest of the guide: reading belongs to nobody, no other author's
explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

KID, CS, IKI = ("Key Ideas and Details", "Craft and Structure",
                "Integration of Knowledge and Ideas")

TOPICS = [

    Topic(
        slug="act-r-method",
        title="How to Read an ACT Passage",
        area=KID,
        skill="act_r_kid",
        idea="Read for the shape and the author's position, not for the details, because "
             "the details are findable in ten seconds and the shape is not.",
        why="Eight or nine minutes per passage set is the tightest reading budget of any "
            "exam here. The time is lost in rereading, and the fix is a first pass that "
            "makes rereading unnecessary.",
        facts=[
            ("The budget", "about 3 minutes reading, then 5 to 6 answering",
             "Reading faster to save time costs more in rereads than it saves."),
            ("Map, do not memorise", "one phrase per paragraph about its JOB",
             "Paragraph two is not about the harvest, it is the objection to paragraph "
             "one."),
            ("Find the author's voice", "evaluative words, not factual ones",
             "However, surprisingly, only, failed to. These are where reporting stops and "
             "arguing starts."),
            ("Skip on the first pass", "lists, dates, names, numbers",
             "Note where they are, not what they are."),
            ("Never skip a turn", "but, yet, although, nevertheless",
             "A turn is where the passage changes direction, which is where questions "
             "live."),
            ("Line references are gifts", "they tell you exactly where to look",
             "Read the lines around the reference, not just the cited line."),
            ("Answer order", "do the line-reference questions first",
             "They are fastest and they build your map of the passage for the rest."),
            ("Prose fiction differs", "read for relationships and motive",
             "Who wants what, and how do they feel about each other."),
        ],
        worked=[
            dict(ask="A social science passage opens describing a long-accepted account of "
                     "why a town's mills closed, then presents shipping records that do "
                     "not fit, then offers a different explanation and notes it has not "
                     "been tested. What is the map, and what does it buy you?",
                 steps=[
                     "Paragraph 1: the old account. Job: setup, not argument.",
                     "Paragraph 2: evidence against it. Job: the turn.",
                     "Paragraph 3: a replacement, offered but hedged. Job: the author's "
                     "actual position.",
                     "That map answers the main idea question, the author's attitude "
                     "question, and any function question about paragraph two, without "
                     "returning to the text.",
                 ],
                 answer="Old account, evidence against, tentative replacement",
                 why="Three questions answered from a three-phrase map. That is where the "
                     "time budget comes from: the questions that need the whole passage "
                     "get answered from the map, leaving your minutes for the ones that "
                     "need a specific line."),
        ],
        traps=[
            "Reading for retention. You will not be asked to recall the passage, you will "
            "be asked where things are and what they are doing.",
            "Reading the cited line only on a line-reference question. The answer is "
            "usually in the sentence before or after.",
            "Disengaging from a dull passage, which makes you read it twice.",
            "Forming your own opinion about the subject. The only opinion ever correct is "
            "the author's.",
        ],
        ladder={
            1: "A short passage and a question answered almost verbatim.",
            2: "The answer paraphrases, so matching words no longer works.",
            3: "Two views appear and you must track which is which.",
            4: "The author's position is carried only by hedges and qualifiers.",
            5: "The passage concedes a point before rejecting it, and a wrong answer "
               "quotes the concession as the author's view.",
        },
    ),

    Topic(
        slug="act-r-details",
        title="Key Ideas, Details and Sequence",
        area=KID,
        skill="act_r_kid",
        idea="Main idea questions need an answer covering the whole passage, and detail "
             "questions need one you can point at, and confusing the two standards is how "
             "both are lost.",
        why="This is the largest reporting category in the section. Detail questions are "
            "the cheapest points on the ACT if you go back to the text, and among the most "
            "expensive if you answer from memory.",
        facts=[
            ("Main idea", "covers every paragraph, overstates none",
             "An answer describing one paragraph is describing a detail."),
            ("Detail questions", "the support is findable",
             "According to the passage means you can underline it."),
            ("Go back", "always, even when you are sure",
             "The passage is on screen and confidence is not evidence."),
            ("Paraphrase is expected", "the answer rarely reuses the wording",
             "Word overlap is the cheapest bait to build."),
            ("Sequence questions", "what happened first, next, last",
             "Common in prose fiction and narrative passages; track order on your map."),
            ("Cause and effect", "the passage must state the link",
             "Two events described in order is not a stated cause."),
            ("EXCEPT and NOT", "four are supported, find the one that is not",
             "The job inverts, and missing it means confirming a correct answer four "
             "times."),
        ],
        worked=[
            dict(ask="A passage says: 'Although the cooperative's charter allowed any "
                     "member to call a general meeting, the minutes record that in its "
                     "first eight years only the two founding families ever did so.' "
                     "Which is supported: (A) the charter restricted who could call "
                     "meetings, (B) in the cooperative's first eight years, only members "
                     "of two families in fact called general meetings, (C) other members "
                     "were unaware of their right?",
                 steps=[
                     "Locate it. The sentence is quoted, so this is comparison.",
                     "(A) says the CHARTER restricted it. The passage says the charter "
                     "ALLOWED any member, and practice differed. Reversed.",
                     "(C) offers a reason, which the passage never gives. It explains "
                     "rather than reports.",
                     "(B) restates the second clause with nothing added.",
                 ],
                 answer="(B)",
                 why="'Although' is doing the work: the rule permitted one thing and "
                     "practice was another. Both wrong answers collapse that distinction, "
                     "one by changing the rule and one by explaining the practice. On "
                     "detail questions, the concession word is usually the hinge."),
        ],
        traps=[
            "Answering from memory because you read it a minute ago.",
            "Choosing the answer with the most word overlap with the passage.",
            "Supplying a reason the passage did not give.",
            "Choosing a true detail on a main idea question, which is what every wrong "
            "answer there is built from.",
        ],
        ladder={
            1: "A detail stated almost verbatim in the answer.",
            2: "The answer paraphrases and a decoy reuses the passage's words.",
            3: "A main idea question where one wrong answer covers a single paragraph.",
            4: "A sequence or cause question where order is stated and causation is not.",
            5: "An EXCEPT question whose four supported answers span the whole passage.",
        },
    ),

    Topic(
        slug="act-r-craft",
        title="Craft and Structure: Words, Function and Voice",
        area=CS,
        skill="act_r_cs",
        idea="These ask what a word means here, what a passage element is doing, or how "
             "the author sounds, and all three are answered from the surrounding text "
             "rather than from general knowledge.",
        why="Vocabulary in context questions are frequent and nearly free with the right "
            "method, and function questions are pure structural reading, so both are "
            "cheap if you built a map.",
        facts=[
            ("Words in context", "cover the choices and predict your own word",
             "The passage's use decides it, not the word's usual meaning."),
            ("Secondary meanings", "common words in uncommon senses",
             "Check, novel, qualify, arrest, register, grave."),
            ("Function stems", "the author includes X primarily to",
             "The answer is a job: to illustrate, to concede, to contrast, to introduce."),
            ("Read around, not at", "a line's function is set by its neighbours",
             "The cited line is the one place the answer is not."),
            ("Point of view", "who is narrating and how much they know",
             "First person, third limited, third omniscient. Common in prose fiction."),
            ("Tone lives in modifiers", "adjectives, adverbs and hedges",
             "And is usually more measured than the answer choices suggest."),
            ("Match the intensity", "direction is only half",
             "Getting positive versus negative right and then choosing the extreme is the "
             "common loss."),
        ],
        worked=[
            dict(ask="'The report's conclusions were qualified at every turn.' What does "
                     "'qualified' mean here: (A) certified as competent, (B) limited by "
                     "conditions, (C) eligible, (D) skilled?",
                 steps=[
                     "Cover the choices. Predict from the sentence: 'at every turn' "
                     "suggests hedging throughout.",
                     "Predict: hedged, limited.",
                     "(A), (C) and (D) are all the 'having the necessary skill or "
                     "eligibility' sense of the word, which is its most common meaning.",
                     "(B) is the secondary sense and the one this sentence uses.",
                 ],
                 answer="(B)",
                 why="Three of the four choices cluster around the word's everyday "
                     "meaning, which is the construction that makes these items work. "
                     "Predicting before reading the choices is what keeps that cluster "
                     "from looking like the right neighbourhood."),
        ],
        traps=[
            "Choosing a word's most common meaning when the passage uses a secondary one.",
            "Answering a function question with a summary of the cited line.",
            "Choosing the extreme version of the correct tone direction.",
            "Reading only the cited line on a function question.",
        ],
        ladder={
            1: "A word with a clear contextual clue.",
            2: "A function question about a plainly signposted example.",
            3: "A common word used in a secondary sense.",
            4: "A tone question where praise and reservation both appear.",
            5: "The cited element supports a view the author later rejects, so its "
               "function is to set up a rebuttal.",
        },
    ),

    Topic(
        slug="act-r-integration",
        title="Integration of Knowledge and Ideas, and Paired Passages",
        area=IKI,
        skill="act_r_iki",
        idea="These ask you to compare two texts, judge how well a claim is supported, or "
             "apply the passage to a new case, and all three need the author's position "
             "held precisely.",
        why="One set per section is Paired Passages, and this is where those questions "
            "concentrate. They are the most time-expensive in the section, which is why "
            "the technique is to read each passage separately and answer the "
            "single-passage questions first.",
        facts=[
            ("Paired passages", "two shorter texts, different authors",
             "With questions about A, about B, and about both."),
            ("Read A, answer A's questions, then B", "do not read both first",
             "Holding two passages at once is what makes these expensive."),
            ("Answer the both-questions last", "when each is fresh in its own right",
             "By then you have a position for each author."),
            ("Find the agreement first", "usually larger than the disagreement",
             "Naming what both accept locates the narrow thing they do not."),
            ("Agreement is a possible answer", "B may support or extend A",
             "Do not assume conflict because two texts were given."),
            ("Whose view is asked", "the stem names an author",
             "Answering from the wrong one is the most common error in the format."),
            ("Evidence questions", "which detail best supports a claim",
             "The support must bear on THIS claim, not merely be true."),
            ("Match the strength", "would disagree, would qualify, would note",
             "A mild reservation and a flat rejection are different answers."),
        ],
        worked=[
            dict(ask="Passage A argues a river's fish population recovered because of a "
                     "fishing ban. Passage B reports that populations recovered by similar "
                     "amounts in three neighbouring rivers with no ban. How would B's "
                     "author most likely respond to A?",
                 steps=[
                     "A's claim: the ban caused the recovery.",
                     "B's evidence: comparable recoveries without any ban.",
                     "What they AGREE on: the population recovered. B does not dispute "
                     "that.",
                     "Point of contact: whether the ban explains it. B points to a cause "
                     "common to all four rivers.",
                 ],
                 answer="By questioning A's causal explanation without disputing the "
                        "recovery itself",
                 why="An answer saying B disputes A's population figures will be offered "
                     "and is wrong, because both authors accept the recovery. Naming the "
                     "agreement first is what makes the disagreement precise, and "
                     "precision is what separates the credited answer from the "
                     "second-best one."),
        ],
        traps=[
            "Answering from the wrong author's position.",
            "Assuming the two passages disagree when one supports or extends the other.",
            "Reading both passages before answering anything, which doubles what you are "
            "holding in mind.",
            "Choosing evidence that is true but does not bear on the specific claim.",
        ],
        ladder={
            1: "The two passages plainly agree or plainly disagree.",
            2: "An evidence question with one obviously matching detail.",
            3: "The disagreement concerns interpretation of shared evidence.",
            4: "The correct answer is a qualification rather than a rejection.",
            5: "The stem asks how one author would respond to a specific detail in the "
               "other rather than to the passage as a whole.",
        },
    ),
]
