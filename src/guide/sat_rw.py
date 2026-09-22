"""Digital SAT Reading and Writing, topic by topic.

Organised by College Board's own four domains, matching how our engine scores the
section: Information and Ideas, Craft and Structure, Expression of Ideas, and Standard
English Conventions.

One structural fact runs through all of it and is worth stating once. On the digital
SAT every Reading and Writing question has its OWN short passage, usually one
paragraph, and the questions are grouped by domain in roughly increasing difficulty.
There is no long passage with ten questions hanging off it. That changes the strategy
completely: there is nothing to skim and come back to, and no reason to read ahead.

A note on typography. This site does not use em dashes or en dashes anywhere, which is
a house rule. The SAT does test them, so where a dash is the point it is written here
as a double hyphen, the way it is typed in plain text.

Same IP position as the rest of the guide: grammar and rhetoric belong to nobody, no
other author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

II, CS, EOI, SEC = ("Information and Ideas", "Craft and Structure",
                    "Expression of Ideas", "Standard English Conventions")

TOPICS = [

    Topic(
        slug="sat-rw-central-ideas",
        title="Central Ideas and Details",
        area=II,
        skill="rw_ii",
        idea="The passage is one paragraph, so its main idea is usually one sentence in "
             "it, and the job is telling that sentence apart from the ones supporting it.",
        why="These are the most answerable questions in the section and people lose them "
            "by choosing a detail that is true. True is not the test; being the point of "
            "the paragraph is.",
        facts=[
            ("What is being asked", "which choice best states the main idea",
             "The whole paragraph, not the most interesting sentence in it."),
            ("The coverage test", "does the answer account for the whole paragraph",
             "An answer describing one sentence is describing a detail."),
            ("Find the claim sentence", "the one the others explain or support",
             "Often first or last, and frequently the one after a turn word."),
            ("Turn words relocate the point", "however, but, yet, although",
             "What follows a turn is usually the paragraph's actual position."),
            ("Detail questions are lookups", "the support has to be findable",
             "According to the text means you can point at the line."),
            ("Paraphrase is expected", "the answer rarely reuses the passage's words",
             "Heavy word overlap is more often bait than answer."),
        ],
        worked=[
            dict(ask="A paragraph describes how a 19th century engineer's bridge design "
                     "was dismissed for decades, then notes that modern analysis shows it "
                     "used less material than any contemporary alternative. Which is the "
                     "main idea: (A) the engineer built bridges in the 19th century, "
                     "(B) modern analysis can evaluate historical designs, (C) a design "
                     "long dismissed turns out to have been unusually efficient?",
                 steps=[
                     "Find the turn. The word 'then' marks it: the paragraph changes "
                     "direction from dismissal to vindication.",
                     "(A) is true and is setup. It accounts for the first half only.",
                     "(B) is true and is the method, not the finding. The paragraph is "
                     "about this design, not about analysis in general.",
                     "(C) covers both halves: dismissed, and actually efficient.",
                 ],
                 answer="(C)",
                 why="(A) and (B) are both supported by the text, which is exactly what "
                     "makes them good wrong answers. The main idea question is not asking "
                     "what is true, it is asking what the paragraph was written to say."),
        ],
        traps=[
            "Choosing a true detail. Every wrong answer here is usually supportable; only "
            "one is the point.",
            "Choosing the first sentence by default. On a passage with a turn, the "
            "opening is often the view being complicated.",
            "Choosing the broadest answer. A paragraph about one bridge does not have a "
            "main idea about engineering history.",
            "Answering from memory after one read, when the passage is four lines long "
            "and still on the screen.",
        ],
        ladder={
            1: "A short paragraph with the main idea in its final sentence.",
            2: "The answer paraphrases rather than restates.",
            3: "A true detail is offered as a distractor and the coverage test decides.",
            4: "The paragraph turns, and the wrong answer quotes the half before the "
               "turn.",
            5: "Two answers both cover the paragraph and differ only in scope or in how "
               "strongly they state the claim.",
        },
    ),

    Topic(
        slug="sat-rw-evidence",
        title="Command of Evidence, Textual and Quantitative",
        area=II,
        skill="rw_ii",
        idea="You are given a claim and asked which piece of evidence, from a text or "
             "from a graph, would most directly support or undermine it.",
        why="The quantitative version catches people out because it looks like a maths "
            "question and is not: the arithmetic is trivial and the difficulty is entirely "
            "in matching a number to the exact claim being made.",
        facts=[
            ("Read the claim first", "before any data or any choices",
             "The claim names a comparison, a direction and a group. All three matter."),
            ("Most directly", "the evidence has to bear on THIS claim",
             "Several choices are usually true and about the topic."),
            ("Match the variable", "the graph may show several",
             "A claim about growth rate is not supported by a figure about total size."),
            ("Match the direction", "supports or weakens, as asked",
             "Half the plausible answers point the correct way about the wrong thing."),
            ("Match the group", "the claim may be about a subset",
             "Data about all sites does not settle a claim about coastal sites."),
            ("The arithmetic is trivial", "read, compare, done",
             "If you find yourself computing, re-read the claim: you have probably drifted."),
            ("True is not sufficient", "a true statement that does not bear is wrong",
             "This is the same standard as the textual version."),
        ],
        worked=[
            dict(ask="A researcher claims that a fertiliser increases yield more in dry "
                     "years than in wet ones. A bar chart shows yield with and without "
                     "fertiliser in four years, two dry and two wet. What do you check?",
                 steps=[
                     "The claim is about a DIFFERENCE OF DIFFERENCES: the fertiliser "
                     "effect in dry years against the effect in wet years.",
                     "So the quantity is not yield, and not even fertilised yield. It is "
                     "the gap between the two bars in each year.",
                     "Compute that gap for the dry years and for the wet years.",
                     "The claim is supported only if the dry-year gaps are larger.",
                 ],
                 answer="Compare the with-and-without gap in dry years against the same "
                        "gap in wet years",
                 why="Almost every wrong answer here reports a single bar being tallest, "
                     "which is true and irrelevant. The claim compared two effects, so "
                     "the evidence must be about two effects. Naming the exact quantity "
                     "before looking at the chart is what prevents the drift."),
        ],
        traps=[
            "Choosing the most striking number on the graph. Striking is not the same as "
            "relevant to the claim.",
            "Supporting a claim about a rate with data about a total, or the reverse.",
            "Answering about the wrong group when the claim named a subset.",
            "Reading the axis without its units or its starting value, so a small "
            "difference looks large.",
        ],
        ladder={
            1: "One clear claim and one obviously matching figure.",
            2: "Two variables are shown and only one is the claim's.",
            3: "The claim concerns a subset of what the display shows.",
            4: "The claim is a comparison, so two quantities must be compared rather than "
               "one read.",
            5: "The claim is a difference of differences and every wrong answer reports a "
               "single true value.",
        },
    ),

    Topic(
        slug="sat-rw-inferences",
        title="Inferences and Completing the Text",
        area=II,
        skill="rw_ii",
        idea="These ask you to finish a sentence or a logical thought, and the answer has "
             "to follow from the passage, not merely sound like a sensible continuation.",
        why="The everyday meaning of infer costs points here exactly as it does on every "
            "other exam. The correct answer is usually a small, almost dull step that the "
            "text has already licensed.",
        facts=[
            ("The stem", "which most logically completes the text",
             "You are finishing the author's thought, not adding your own."),
            ("Watch the connector", "the blank usually follows a signal word",
             "Therefore points forward to a consequence; however points to a contrast."),
            ("Predict before reading choices", "say the ending in your own words",
             "Then find the closest match, which stops the choices steering you."),
            ("Small steps win", "the answer rarely introduces new information",
             "A dramatic conclusion is usually the wrong one."),
            ("Watch the scope", "some, most, all, always, never",
             "A hedged passage cannot support an absolute ending."),
            ("Two-part logic", "if the text sets up a condition, the ending applies it",
             "Conditional passages want the conclusion, not a restatement."),
        ],
        worked=[
            dict(ask="'Fossil evidence from the site records twelve mammal species, none "
                     "of which is known to have tolerated sustained frost. Researchers "
                     "therefore conclude that during the period of deposition, the region "
                     "___' Complete the thought.",
                 steps=[
                     "The connector is 'therefore', so what follows is a conclusion from "
                     "the evidence.",
                     "Evidence: twelve species, none frost tolerant.",
                     "Predict: the region was not subject to sustained frost, so it was "
                     "warmer than that.",
                     "Reject anything stronger, such as a specific temperature, or "
                     "anything about a different period.",
                 ],
                 answer="did not experience sustained frost",
                 why="The prediction is almost a restatement of the evidence, and that is "
                     "correct. Wrong answers here typically name a cause for the warmth, "
                     "or give a numeric temperature, both of which go past what twelve "
                     "species can establish."),
        ],
        traps=[
            "Choosing the most interesting completion rather than the supported one.",
            "Ignoring the connector, which frequently reverses which direction the ending "
            "must go.",
            "Strengthening the claim: the passage says suggests and the answer says "
            "proves.",
            "Importing outside knowledge about the subject, which feels like evidence and "
            "is not in the text.",
        ],
        ladder={
            1: "A one-step conclusion signalled plainly.",
            2: "The connector is a contrast, so the ending must oppose what came before.",
            3: "A quantifier in the passage limits how strong the ending can be.",
            4: "Two answers both follow and one goes further than the evidence allows.",
            5: "The passage sets up a condition and the ending must apply it rather than "
               "restate it.",
        },
    ),

    Topic(
        slug="sat-rw-words-in-context",
        title="Words in Context",
        area=CS,
        skill="rw_cs",
        idea="The question is never what the word usually means; it is which word fits "
             "the specific job this sentence needs doing.",
        why="This is the most common question type in Craft and Structure, and it is "
            "winnable without a large vocabulary because the sentence tells you what it "
            "needs if you cover the choices and ask.",
        facts=[
            ("The method", "cover the choices and predict your own word",
             "Then match. Reading the choices first lets them define the sentence for "
             "you."),
            ("Look for the clue", "the sentence almost always contains one",
             "A definition, a contrast, an example, or a restatement after a colon."),
            ("Contrast clues", "but, however, although, unlike, rather than",
             "These tell you the blank means roughly the OPPOSITE of something nearby."),
            ("Continuation clues", "and, moreover, indeed, that is",
             "These tell you it means roughly the SAME as something nearby."),
            ("Charge", "is the word positive, negative, or neutral",
             "Getting the charge right eliminates two choices before meaning matters."),
            ("Secondary meanings", "a common word used in an uncommon sense",
             "Words like qualify, arrest, novel and check are tested this way."),
            ("It must fit the grammar too", "part of speech and the words it takes",
             "A verb that needs a preposition has to have it available."),
        ],
        worked=[
            dict(ask="'Far from being ___, the committee's recommendations were hedged at "
                     "every point and left the central question open.' Which fits: "
                     "(A) tentative, (B) decisive, (C) lengthy, (D) unpopular?",
                 steps=[
                     "'Far from being' is a contrast marker: the blank is the OPPOSITE of "
                     "what follows.",
                     "What follows: hedged at every point, left the question open.",
                     "So the blank means something like firm or conclusive.",
                     "(B) decisive. (A) tentative is a synonym for hedged, which is the "
                     "trap for anyone who missed the contrast.",
                 ],
                 answer="(B)",
                 why="(A) is the answer to the same sentence with the contrast removed, "
                     "which is why it is there. Two words in the stem, 'far from', decide "
                     "the entire question, and they are easy to read past."),
        ],
        traps=[
            "Missing a contrast marker and choosing the synonym of the nearby phrase, "
            "which is the single most common error here.",
            "Choosing the hardest-looking word on the assumption the exam wants "
            "difficulty. It wants fit.",
            "Using a word's most common meaning when the sentence is using a secondary "
            "one.",
            "Picking a word with the right meaning and the wrong charge, such as a "
            "negative word in an approving sentence.",
        ],
        ladder={
            1: "A straightforward clue and a common word.",
            2: "The clue is a contrast that must be noticed.",
            3: "Two choices share a meaning and differ in charge or formality.",
            4: "The tested word is a common one used in a secondary sense.",
            5: "Two choices both fit the meaning and only one fits the grammar of what "
               "follows.",
        },
    ),

    Topic(
        slug="sat-rw-purpose",
        title="Text Structure and Purpose",
        area=CS,
        skill="rw_cs",
        idea="These ask what a sentence or a passage is doing rather than what it says, "
             "and those are different questions with different answers.",
        why="Function questions reward reading for structure. They are quick if you can "
            "name each sentence's job in one verb, and slow if you try to answer by "
            "summarising the content.",
        facts=[
            ("The stem", "the main purpose of the text, or of the underlined sentence",
             "The answer is a job: to introduce, to illustrate, to qualify, to refute."),
            ("Answers start with a verb", "and the verb is what distinguishes them",
             "Two answers may name the same content and differ only in the verb."),
            ("Read around the sentence", "its neighbours define its job",
             "A sentence's function is set by what it was brought in to serve."),
            ("Examples serve claims", "look immediately before a specific case",
             "The general statement it supports is almost always the previous sentence."),
            ("Concessions", "although X, Y gives away X and asserts Y",
             "The conceded half is what wrong answers quote as the author's view."),
            ("Match the strength", "the verb must match how hard the author pushed",
             "If the author raised a possibility, the answer cannot say demonstrates."),
        ],
        worked=[
            dict(ask="A paragraph argues that urban beekeeping has been overstated as a "
                     "conservation measure. It then says: 'A 2019 census of one European "
                     "city recorded more hives per square kilometre than local forage "
                     "could sustain.' What is that sentence doing?",
                 steps=[
                     "Do not summarise it; ask what it is for.",
                     "The sentence before it is the claim: the benefit is overstated.",
                     "A specific measured case following a general claim is evidence for "
                     "that claim.",
                     "So its purpose is to provide evidence that hive density can exceed "
                     "what the environment supports.",
                 ],
                 answer="To give specific evidence for the claim that the practice has "
                        "been overstated",
                 why="The wrong answer on offer will be a faithful summary, something "
                     "like 'to describe a census conducted in a European city'. That is "
                     "what the sentence says. The question asked what it is for."),
        ],
        traps=[
            "Answering with a summary instead of a purpose. The summary answer is always "
            "available and always wrong on these.",
            "Attaching an example to the wrong claim, usually the nearer one in memory "
            "rather than on the page.",
            "Treating a concession as the author's own position.",
            "Choosing a verb stronger than the passage earned.",
        ],
        ladder={
            1: "A clearly signposted example right after the claim it supports.",
            2: "The question asks the purpose of the whole paragraph.",
            3: "The sentence serves a concession rather than the main claim.",
            4: "Two answers name the content correctly and differ in their verb.",
            5: "The cited sentence supports a view the author goes on to reject, so its "
               "function is to set up a rebuttal.",
        },
    ),

    Topic(
        slug="sat-rw-cross-text",
        title="Cross-Text Connections",
        area=CS,
        skill="rw_cs",
        idea="Two short texts are given and you are asked how the second author would "
             "respond to the first, which means finding the precise point they disagree "
             "about.",
        why="These are the hardest questions in Craft and Structure because both texts "
            "are usually reasonable and the disagreement is narrow. Locating it exactly "
            "is the entire question.",
        facts=[
            ("Read text 1 for its claim", "one sentence, in your own words",
             "Then do the same for text 2 before looking at any choice."),
            ("Find the exact point of contact", "they rarely disagree about everything",
             "Usually they share the facts and differ on interpretation or significance."),
            ("Agreement is possible", "the answer may be that text 2 supports text 1",
             "Do not assume a disagreement just because two texts were given."),
            ("Whose view is being asked about", "the stem names one author",
             "Answering from the wrong author's position is the most common error."),
            ("Match the strength", "would disagree, would qualify, would note",
             "A mild reservation and a flat rejection are different answers."),
            ("The answer must be supported by both", "it describes a relation",
             "An answer true of one text and unsupported by the other is wrong."),
        ],
        worked=[
            dict(ask="Text 1 argues a city's transit ridership rose because of a new fare "
                     "cap. Text 2 reports that ridership rose by similar amounts in three "
                     "comparable cities that introduced no fare change. How would the "
                     "author of Text 2 most likely respond?",
                 steps=[
                     "Text 1's claim: the fare cap caused the rise.",
                     "Text 2's evidence: similar rises without a fare cap elsewhere.",
                     "Point of contact: not whether ridership rose, which both accept, "
                     "but whether the cap explains it.",
                     "So Text 2 would say the rise may have a cause common to all four "
                     "cities, so the cap is not established as the reason.",
                 ],
                 answer="By questioning the causal claim, not the ridership figures",
                 why="Both authors agree ridership rose. An answer saying Text 2 disputes "
                     "the increase misreads the disagreement entirely, and it will be on "
                     "the list. Naming what the two texts AGREE about is often the fastest "
                     "route to what they do not."),
        ],
        traps=[
            "Answering from the wrong author's perspective. Read the stem twice.",
            "Assuming disagreement. Some of these are one author supporting or extending "
            "the other.",
            "Overstating the disagreement, such as flat contradiction where the text "
            "supports only a qualification.",
            "Choosing an answer true of one text but not describing the relationship "
            "between them.",
        ],
        ladder={
            1: "The two texts plainly agree or plainly disagree.",
            2: "The disagreement is about interpretation rather than fact.",
            3: "The two share their evidence and differ on what it shows.",
            4: "The correct answer is a qualification rather than a rejection.",
            5: "The stem asks how one author would respond to a specific detail in the "
               "other, not to the text as a whole.",
        },
    ),
    Topic(
        slug="sat-rw-transitions",
        title="Transitions",
        area=EOI,
        skill="rw_eoi",
        idea="The right transition is decided by the logical relationship between the two "
             "sentences, so the method is to name that relationship before looking at any "
             "choice.",
        why="Transitions are among the most frequent questions in the section and they "
            "are fully mechanical. Once you can sort transitions into four or five "
            "families, the choices sort themselves.",
        facts=[
            ("The method", "cover the choices, name the relationship, then match",
             "Reading the choices first makes several of them sound plausible."),
            ("Contrast", "however, nevertheless, by contrast, on the other hand, still",
             "The second sentence cuts against the first."),
            ("Continuation", "moreover, furthermore, in addition, similarly, likewise",
             "The second sentence adds more of the same."),
            ("Cause and effect", "therefore, thus, consequently, as a result, hence",
             "The second sentence follows from the first."),
            ("Example", "for example, for instance, specifically, notably",
             "The second sentence is a case of the first."),
            ("Concession", "admittedly, granted, to be sure, of course",
             "The writer gives ground before pushing back."),
            ("Sequence", "first, next, subsequently, finally, meanwhile",
             "Only correct when the passage is actually ordering events."),
            ("Read both sentences fully", "the relationship needs both halves",
             "Reading only the sentence with the blank is how the wrong family gets "
             "chosen."),
        ],
        worked=[
            dict(ask="'The alloy resists corrosion better than steel and costs less to "
                     "produce. ___, it has not been adopted for marine use, because it "
                     "loses strength above 60 degrees.' Which transition: (A) Therefore, "
                     "(B) Similarly, (C) Nevertheless, (D) For example?",
                 steps=[
                     "Sentence 1: two advantages of the alloy.",
                     "Sentence 2: it has not been adopted, for a stated reason.",
                     "The relationship is contrast: despite the advantages, it is not "
                     "used.",
                     "(C) Nevertheless. (A) reverses the logic, (B) claims addition, "
                     "(D) claims the second is an example of the first.",
                 ],
                 answer="(C)",
                 why="(A) Therefore is the trap, because the sentence contains 'because' "
                     "and reads as if causal reasoning is going on. It is, but within "
                     "sentence 2. The relationship BETWEEN the two sentences is the "
                     "contrast, and that is what the transition marks."),
        ],
        traps=[
            "Reading only the sentence containing the blank. The relationship needs the "
            "sentence before it too.",
            "Choosing a cause transition because the second sentence contains causal "
            "words internally.",
            "Using a sequence transition when nothing is actually in sequence.",
            "Picking between two transitions in the same family, when the exam almost "
            "never offers two correct ones. If two seem right, the relationship has been "
            "misnamed.",
        ],
        ladder={
            1: "A plain contrast or continuation between two short sentences.",
            2: "The relationship is cause and effect and must be told from contrast.",
            3: "One sentence contains internal logic words that point the wrong way.",
            4: "The correct transition is a concession, which is a contrast with a "
               "particular shape.",
            5: "Two choices are in the same family and the passage's structure decides "
               "which degree of contrast is right.",
        },
    ),

    Topic(
        slug="sat-rw-synthesis",
        title="Rhetorical Synthesis",
        area=EOI,
        skill="rw_eoi",
        idea="You are given notes and a stated goal, and the answer is whichever sentence "
             "accomplishes THAT goal, which is usually not the sentence that uses the "
             "most notes.",
        why="This question type is unique to the digital SAT and is entirely a reading "
            "task disguised as a writing one. The goal sentence in the stem is the whole "
            "question, and it is the part people skim.",
        facts=[
            ("The stem states the goal", "read it twice before the notes",
             "To emphasise a similarity, to introduce X to an unfamiliar audience, to "
             "explain why."),
            ("The goal is the only criterion", "not elegance, not completeness",
             "A well written sentence that does a different job is wrong."),
            ("Every choice is factually true", "they all come from the notes",
             "So accuracy never distinguishes them and checking it wastes time."),
            ("Emphasise a similarity", "the sentence must compare and say they are alike",
             "Mentioning both things is not comparing them."),
            ("Emphasise a difference", "the sentence must contrast them explicitly",
             "Listing both facts side by side is not a contrast."),
            ("Introduce to an unfamiliar audience", "define, do not assume",
             "The answer usually explains what something is."),
            ("Using more notes is not better", "the goal decides, not coverage",
             "The longest choice is frequently the wrong one."),
        ],
        worked=[
            dict(ask="Notes give: Lake A is 40 m deep and holds 12 fish species; Lake B "
                     "is 38 m deep and holds 11 fish species. The goal is to emphasise a "
                     "similarity between the lakes. Which is best: (A) Lake A is 40 m "
                     "deep and holds 12 species, while Lake B is 38 m deep and holds 11, "
                     "(B) Lake A, at 40 m, is deeper than Lake B, at 38 m, (C) The two "
                     "lakes are comparable in both depth and species count, at about 40 m "
                     "and roughly a dozen species each?",
                 steps=[
                     "Goal: emphasise a SIMILARITY.",
                     "(A) states both sets of facts and the word 'while' sets up a "
                     "contrast. It lists rather than compares.",
                     "(B) explicitly contrasts, which is the opposite of the goal.",
                     "(C) states that they are alike and gives the shared values.",
                 ],
                 answer="(C)",
                 why="(A) is true, complete, uses every note, and does not do the job. "
                     "That is the shape of the whole question type: the wrong answers are "
                     "not wrong about the facts, they are wrong about the task."),
        ],
        traps=[
            "Skimming the goal sentence. It is the only thing that distinguishes the "
            "choices, and it is one line.",
            "Choosing the sentence that uses the most notes. Coverage is not the goal "
            "unless the goal says so.",
            "Confusing listing two facts with comparing or contrasting them.",
            "Checking the notes for factual accuracy. They are all accurate; that is not "
            "where the answer is.",
        ],
        ladder={
            1: "The goal is plain and only one choice attempts it.",
            2: "Two choices attempt the goal and one does it more directly.",
            3: "The goal is to emphasise a similarity or difference and a listing answer "
               "is offered.",
            4: "The goal names an audience, so the answer must define rather than assume.",
            5: "Two choices both meet the goal and differ in which detail they "
               "foreground, with the stem naming which one matters.",
        },
    ),

    Topic(
        slug="sat-rw-boundaries",
        title="Sentence Boundaries and End Punctuation",
        area=SEC,
        skill="rw_sec",
        idea="Most punctuation questions on this exam are really one question: is each "
             "side of the punctuation a complete sentence, and does the mark you chose "
             "match that answer.",
        why="Standard English Conventions is the most learnable domain in the section "
            "because the rules are finite. Sentence boundaries are the largest slice of "
            "it and the errors are a short list.",
        facts=[
            ("Independent clause", "has a subject and a verb and could stand alone",
             "This is the test every boundary question runs on."),
            ("Comma splice", "two independent clauses joined by a comma alone",
             "Always wrong, and it is the most frequently tested error in the domain."),
            ("Period or semicolon", "both correctly separate two independent clauses",
             "So the exam never offers both as choices for the same blank."),
            ("Comma plus FANBOYS", "for, and, nor, but, or, yet, so",
             "A comma is correct before one of these joining two independent clauses."),
            ("Colon", "needs a complete sentence BEFORE it",
             "What follows can be a list, a phrase or a sentence; what precedes cannot be "
             "a fragment."),
            ("Dash", "written here as -- , can do a colon's job or a pair can do commas'",
             "A single dash before an explanation, or a matched pair around an "
             "interruption."),
            ("Dependent clause", "starts with because, although, when, if, since, while",
             "It cannot stand alone, so joining it with a comma is fine and with a "
             "semicolon is not."),
            ("The no-punctuation option", "sometimes correct",
             "When the two parts are not both independent and nothing needs separating."),
        ],
        worked=[
            dict(ask="Choose the punctuation: 'The engine had been rebuilt twice ___ it "
                     "still failed inspection.'  (A) comma, (B) semicolon, (C) comma plus "
                     "but, (D) no punctuation.",
                 steps=[
                     "Left side: 'The engine had been rebuilt twice'. Subject and verb, "
                     "stands alone. Independent.",
                     "Right side: 'it still failed inspection'. Subject and verb, stands "
                     "alone. Independent.",
                     "Two independent clauses, so a comma alone is a splice. (A) out. "
                     "(D) is a run-on. Out.",
                     "(B) and (C) are both grammatically correct, so the exam would not "
                     "offer both. Here the relationship is contrast, which 'but' marks, "
                     "so (C).",
                 ],
                 answer="(C)",
                 why="The clause test eliminated two choices before any judgement about "
                     "meaning. That is the order to work in: mechanics first, and only "
                     "then, if two choices survive, the logical relationship."),
        ],
        traps=[
            "Joining two independent clauses with a comma. If you learn one rule in this "
            "domain, this is it.",
            "Using a colon after a fragment. The colon needs a complete sentence on its "
            "left, always.",
            "Treating 'however' as a FANBOYS word. It is not, so a comma before it "
            "joining two clauses is still a splice.",
            "Adding punctuation because the sentence feels long. Length is not a reason; "
            "structure is.",
        ],
        ladder={
            1: "Two short independent clauses and an obvious splice among the choices.",
            2: "One side is a dependent clause, so the rules differ.",
            3: "A colon is offered and the left side must be tested for completeness.",
            4: "'However' or 'therefore' appears and is mistaken for a coordinating "
               "conjunction.",
            5: "Two choices are mechanically correct and the logical relationship decides.",
        },
    ),

    Topic(
        slug="sat-rw-commas",
        title="Commas and Other Internal Punctuation",
        area=SEC,
        skill="rw_sec",
        idea="Within a sentence, punctuation marks off information that could be removed, "
             "and the test is whether the sentence still works without it.",
        why="Commas are tested constantly and the rules feel arbitrary until you see that "
            "nearly all of them are the same idea: is this element essential to "
            "identifying what is being talked about, or is it extra.",
        facts=[
            ("Non-essential elements", "surrounded by a pair of commas",
             "Remove it and the sentence still says who or what it is about."),
            ("Essential elements", "no commas",
             "Remove it and you no longer know which thing is meant."),
            ("The pair rule", "one comma before means one comma after",
             "A single comma around a non-essential phrase is always wrong."),
            ("Items in a list", "commas between them",
             "Three or more items; two items joined by and take no comma."),
            ("Introductory element", "comma after it",
             "After a phrase or dependent clause that opens the sentence."),
            ("Never between subject and verb", "no comma, however long the subject",
             "A long subject invites a comma that the rule forbids."),
            ("Pairs of dashes and parentheses", "same job as a pair of commas",
             "Written here as -- ; the two marks in a pair must match each other."),
            ("The removal test", "read the sentence without the element",
             "If it still identifies its subject, the element is non-essential."),
        ],
        worked=[
            dict(ask="Which is correct: (A) 'The violinist, who premiered the concerto in "
                     "1897, later destroyed the manuscript.' (B) 'The violinist who "
                     "premiered the concerto in 1897 later destroyed the manuscript.' "
                     "Both can be right. What decides it?",
                 steps=[
                     "Apply the removal test to the clause 'who premiered the concerto in "
                     "1897'.",
                     "If the passage has already identified which violinist, the clause "
                     "is extra information: use the pair of commas, so (A).",
                     "If there are several violinists and this clause is what tells you "
                     "which one, it is essential: no commas, so (B).",
                     "Context decides, which is why these questions always give you the "
                     "surrounding sentence.",
                 ],
                 answer="(A) if the violinist is already identified, (B) if the clause is "
                        "what identifies them",
                 why="This is the clearest case of the essential and non-essential "
                     "distinction, and it shows why the rule is not arbitrary: the commas "
                     "change the meaning. With them, there is one violinist. Without "
                     "them, there were several and this is the one who did it."),
        ],
        traps=[
            "Using one comma where a pair is needed, which is the most common comma error "
            "the exam tests.",
            "Placing a comma between a long subject and its verb.",
            "Mixing a comma at one end of an interruption with a dash at the other. The "
            "pair must match.",
            "Adding a comma before 'and' when it joins only two items rather than "
            "separating three.",
        ],
        ladder={
            1: "An introductory phrase needing a comma after it.",
            2: "A list of three or more items.",
            3: "A non-essential clause needing a matched pair.",
            4: "The essential and non-essential distinction changes the meaning and "
               "context decides.",
            5: "The choices mix commas, dashes and parentheses, and the matched pair rule "
               "is what eliminates most of them.",
        },
    ),

    Topic(
        slug="sat-rw-agreement",
        title="Subject Verb and Pronoun Agreement",
        area=SEC,
        skill="rw_sec",
        idea="The verb agrees with its subject and the pronoun agrees with what it stands "
             "for, and the exam's whole strategy is to put distance between the two.",
        why="These are reliable points once you can find the subject. The exam separates "
            "subject from verb with prepositional phrases and clauses precisely because "
            "the nearest noun is usually the wrong one.",
        facts=[
            ("Find the subject", "cross out the prepositional phrases",
             "'The box of old photographs IS heavy': the subject is box, not photographs."),
            ("The nearest noun is a decoy", "it is placed there on purpose",
             "Nearly every agreement question puts a plural noun beside a singular "
             "subject."),
            ("Inverted sentences", "there is, there are, here comes",
             "The subject follows the verb, so find it before choosing."),
            ("Each, every, either, neither", "singular",
             "Even when followed by 'of the students'."),
            ("Compound subjects with and", "plural",
             "But 'along with', 'as well as' and 'in addition to' do NOT make it plural."),
            ("Collective nouns", "usually singular on this exam",
             "The team is, the committee has."),
            ("Pronoun agreement", "singular antecedent takes a singular pronoun",
             "Each participant submitted THEIR form is accepted; a plural antecedent "
             "never takes a singular pronoun."),
            ("Ambiguous pronouns", "if it could refer to two things, it is wrong",
             "The exam offers a version naming the noun instead."),
        ],
        worked=[
            dict(ask="Choose the verb: 'The collection of manuscripts that survived the "
                     "fire ___ now held in three separate archives.'  (A) is, (B) are.",
                 steps=[
                     "Cross out the prepositional phrase: 'of manuscripts'.",
                     "Cross out the relative clause: 'that survived the fire'.",
                     "What remains: 'The collection ___ now held'. The subject is "
                     "collection, singular.",
                     "So (A) is.",
                 ],
                 answer="(A)",
                 why="Both 'manuscripts' and 'archives' are plural and both sit between "
                     "or beside the subject and its verb. Crossing out the phrases is "
                     "mechanical and takes three seconds, and it is more reliable than "
                     "reading the sentence aloud, because the sentence was written to "
                     "sound plural."),
        ],
        traps=[
            "Agreeing with the nearest noun instead of the subject. This is what the "
            "question is testing every single time.",
            "Treating 'as well as' or 'along with' as though they were 'and'.",
            "Missing that 'each' and 'neither' are singular when followed by a plural "
            "phrase.",
            "Leaving a pronoun whose antecedent is ambiguous, when a choice naming the "
            "noun is available.",
        ],
        ladder={
            1: "Subject and verb adjacent, agreement plain.",
            2: "One prepositional phrase separates them.",
            3: "A relative clause and a phrase both intervene.",
            4: "The sentence is inverted, or the subject is 'each' or 'neither' plus a "
               "plural phrase.",
            5: "A pronoun question where the grammatically fine option is ambiguous and "
               "the correct answer names the noun.",
        },
    ),

    Topic(
        slug="sat-rw-modifiers-verbs",
        title="Modifiers, Verb Forms and Possessives",
        area=SEC,
        skill="rw_sec",
        idea="A modifier attaches to whatever it sits next to, verb tense has to match the "
             "timeline the passage set, and an apostrophe marks possession rather than a "
             "plural.",
        why="These three are the rest of the conventions domain and each has a single "
            "reliable test. Together with agreement and boundaries they account for "
            "essentially every question in it.",
        facts=[
            ("Dangling modifier", "an opening phrase modifies the subject that follows",
             "'Having finished the survey, the data were analysed' says the data finished "
             "the survey."),
            ("The fix", "make the subject the thing the phrase describes",
             "Having finished the survey, the TEAM analysed the data."),
            ("Misplaced modifier", "put the describing phrase beside what it describes",
             "Only, almost and nearly change meaning depending on where they sit."),
            ("Tense consistency", "match the timeline the passage established",
             "Do not shift tense without a reason in the text."),
            ("Its and it's", "its is possessive, it's is it is",
             "The possessive pronoun has no apostrophe, which is the reverse of nouns."),
            ("Singular possessive", "add apostrophe s",
             "The student's notebook, one student."),
            ("Plural possessive", "add the apostrophe after the s",
             "The students' notebooks, several students."),
            ("Plural, not possessive", "no apostrophe at all",
             "Decades, names and plain plurals never take one."),
            ("Their, there and they're", "possessive, place, and they are",
             "Tested directly and easy to check by expanding the contraction."),
        ],
        worked=[
            dict(ask="Fix: 'Walking through the abandoned factory, the machinery appeared "
                     "untouched for decades.'",
                 steps=[
                     "The opening phrase 'Walking through the abandoned factory' has to "
                     "describe the subject that follows.",
                     "The subject is 'the machinery', so the sentence says the machinery "
                     "was walking.",
                     "Fix by supplying the real subject: someone walking.",
                     "'Walking through the abandoned factory, we found the machinery "
                     "untouched for decades.'",
                 ],
                 answer="Make the walker the subject of the main clause",
                 why="The test is entirely mechanical: read the opening phrase, then read "
                     "the first noun after the comma, and ask whether that noun did the "
                     "thing. If not, the modifier dangles, and the fix is always to "
                     "change the subject rather than the phrase."),
        ],
        traps=[
            "Fixing a dangling modifier by rewriting the phrase instead of supplying the "
            "right subject.",
            "Adding an apostrophe to a plain plural, especially to a decade or a name.",
            "Writing it's for the possessive. Expanding it to 'it is' settles it every "
            "time.",
            "Shifting tense mid-passage because a sentence sounds better that way.",
        ],
        ladder={
            1: "A plain its and it's or their and there choice.",
            2: "Singular against plural possessive.",
            3: "A dangling modifier with a clearly wrong subject.",
            4: "Tense must match a timeline stated earlier in the passage.",
            5: "A modifier is grammatical in more than one position and the placement "
               "changes the meaning.",
        },
    ),
]
