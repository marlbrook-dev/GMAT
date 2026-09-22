"""GMAT Verbal Reasoning, topic by topic.

Verbal is the section people assume cannot be studied, because there is no formula
sheet and the answer feels like a matter of opinion. It is not. Every question here
has a mechanical structure: a thing the question is actually asking, a small number of
ways the right answer can be built, and a much smaller number of ways the wrong ones
are. Learning those is the whole job, and it is as learnable as a quadratic.

What replaces the formula card on these pages is the QUESTION FORM: the skeleton of
each kind of question, and what it is really asking underneath the wording. The exam
rewrites the wording constantly and changes the skeleton almost never.

The IP position is the same as the quant guide's. Logic belongs to nobody, the
structure of an argument is a fact about arguments, and no other author's explanations
are in here. The passages and arguments in the worked examples are written for this
file.
"""
from .model import Topic

# Two question types, four scored skills. The skill ids are the engine's own, so the
# difficulty ladder on each page pulls real items from the bank the trainer serves.
RC, CR, LOGIC = "Reading Comprehension", "Critical Reasoning", "The Logic Underneath"

TOPICS = [

    Topic(
        slug="rc-how-to-read",
        title="How to Read a GMAT Passage",
        area=RC,
        skill="v_st",
        idea="Read for the shape of the argument and the author's position, not for the "
             "details, because the details are searchable and the shape is not.",
        why="Most people lose Verbal time in the passage rather than the questions. They "
            "read every clause at equal weight, understand all of it for about forty "
            "seconds, then read most of it again per question. Reading for structure "
            "costs less and answers more.",
        facts=[
            ("What a passage is doing", "setup, then a tension, then the author's move",
             "Almost every GMAT passage introduces a view or a finding, complicates it, "
             "and then positions the author relative to that complication."),
            ("The map", "one phrase per paragraph, about its job not its content",
             "Paragraph two is not about migratory patterns, it is the objection to "
             "paragraph one. The job is what questions ask about."),
            ("The author's voice", "look for evaluative words, not factual ones",
             "However, surprisingly, only, failed to, it is worth noting: these are "
             "where the author stops reporting and starts arguing."),
            ("What to skip on the first pass", "lists, dates, names, numbers",
             "These are the things you can find again in ten seconds. Note where they "
             "are, not what they are."),
            ("What never to skip", "any sentence that turns",
             "But, yet, although, nevertheless, on the other hand. A turn is where the "
             "passage changes direction, which is where the questions live."),
            ("Time to spend", "roughly two to three minutes reading, then answer",
             "Reading faster than this to save time costs more time in re-reads than it "
             "saves, which is the most common self-inflicted wound in the section."),
        ],
        worked=[
            dict(ask="A three paragraph passage opens by describing a long-accepted "
                     "explanation for why a particular seabird colony declined. The "
                     "second paragraph presents survey data that the explanation does "
                     "not fit. The third paragraph offers a competing explanation and "
                     "notes it has not yet been tested. What is the map?",
                 steps=[
                     "Paragraph 1: the old explanation. Its job is setup, not argument.",
                     "Paragraph 2: the problem with it. The word that matters is whatever "
                     "introduced the data, because that is the turn.",
                     "Paragraph 3: a replacement, offered but not established. The phrase "
                     "'has not yet been tested' is the author's hedge, and it is the "
                     "author's actual position.",
                     "So the map is: old view, evidence against it, tentative replacement.",
                 ],
                 answer="Old view, evidence against it, tentative replacement",
                 why="Three questions are now answerable without rereading: the primary "
                     "purpose (to present evidence complicating an accepted explanation "
                     "and offer an alternative), the author's attitude to the new "
                     "explanation (interested but not committed), and the function of "
                     "paragraph two (to undermine the view in paragraph one)."),
            dict(ask="Where in that passage would you expect the hardest inference "
                     "question to be anchored?",
                 steps=[
                     "Inference questions need a sentence with more content than it "
                     "states outright.",
                     "Setup sentences state things flatly, so they are poor anchors.",
                     "The hedge in paragraph three says the new explanation is untested. "
                     "That licenses an inference about what is NOT yet known.",
                 ],
                 answer="The hedge in paragraph three",
                 why="A hedge is a claim about the limits of the evidence, and a claim "
                     "about limits supports inferences that a flat factual claim does "
                     "not. Hedges are where the author is most careful, so they are "
                     "where the exam can be most precise."),
        ],
        traps=[
            "Reading for retention rather than for structure. You are not going to be "
            "asked to recall the passage later; you are going to be asked where things "
            "are and what they are doing.",
            "Highlighting or noting the interesting parts. Interesting is not the same "
            "as load bearing, and the parts that feel interesting are usually the "
            "concrete details, which are exactly the searchable ones.",
            "Deciding the topic is boring and disengaging. Disengaged reading of a dull "
            "passage takes longer than engaged reading of one, because you do it twice.",
            "Building an opinion about the subject. The only opinion that is ever "
            "correct is the author's, and confusing yours for theirs is the single "
            "largest source of wrong answers in RC.",
        ],
        ladder={
            1: "A short passage, one clear argument, and the question points at a "
               "sentence that answers it almost verbatim.",
            2: "The passage runs longer and the answer is a paraphrase rather than a "
               "restatement, so matching words no longer works.",
            3: "Two views appear and you have to track which is which. The wrong answers "
               "attach the right claim to the wrong holder.",
            4: "The author's position is stated only through hedges and qualifiers, and "
               "the question asks what they would agree with.",
            5: "The passage concedes a point to the opposing view before rejecting it, "
               "and a wrong answer quotes the concession as though it were the author's "
               "conclusion.",
        },
    ),

    Topic(
        slug="rc-main-idea",
        title="Main Idea and Primary Purpose",
        area=RC,
        skill="v_st",
        idea="The main idea is what the whole passage is for, which means it has to "
             "cover every paragraph and overstate none of them.",
        why="This is usually the first question on a passage and it is the one that "
            "rewards the structural read directly. It is also the cheapest question in "
            "the section if you built a map, and one of the most expensive if you did "
            "not.",
        facts=[
            ("Primary purpose", "to [verb] [what], in order to [why]",
             "The answer is a description of the author's job, so it starts with a verb: "
             "to argue, to describe, to reconcile, to qualify, to refute."),
            ("The coverage test", "does the answer account for every paragraph",
             "An answer that perfectly describes paragraph one and ignores paragraphs "
             "two and three is describing a part, not the whole."),
            ("The scope test", "is the answer as broad as the passage, no broader",
             "Too narrow describes one section; too broad describes the field the "
             "passage sits in. Both are wrong in the same way, by the same amount."),
            ("Verb strength", "the verb has to match how hard the author pushed",
             "If the author raised a possibility, the answer cannot say prove. If the "
             "author demolished a view, the answer cannot say discuss."),
            ("Main idea versus topic", "the topic is the subject, the idea is the claim",
             "Seabird decline is a topic. That the accepted explanation for seabird "
             "decline does not fit the survey data is an idea."),
        ],
        worked=[
            dict(ask="A passage argues that a well-known study overstated the effect of "
                     "a teaching method, gives two methodological reasons, and closes by "
                     "saying the method may still help in smaller classes. Which primary "
                     "purpose fits: (A) to describe a teaching method, (B) to argue that "
                     "a study's conclusion was overstated while allowing a narrower "
                     "version of it, (C) to prove a teaching method does not work, "
                     "(D) to compare two teaching methods?",
                 steps=[
                     "Apply coverage. (A) ignores the entire argument, which is most of "
                     "the passage. Out.",
                     "(D) describes a passage that was never written: there is only one "
                     "method here. Out.",
                     "(C) fails verb strength twice: prove is too strong, and the passage "
                     "explicitly allows the method may still help. Out.",
                     "(B) covers the argument, the reasons and the closing concession.",
                 ],
                 answer="(B)",
                 why="The closing concession is what separates (B) from (C), and it is "
                     "the sort of sentence people skim because it sounds like a "
                     "throwaway. On main idea questions the last sentence is rarely "
                     "throwaway: it is usually where the author sets the final scope."),
        ],
        traps=[
            "Picking the answer that describes the first paragraph. It is the paragraph "
            "you read most carefully, so its content is the most available when you "
            "reach the answer choices.",
            "Picking the most impressive sounding answer. Sweeping answers feel like "
            "main ideas, but a passage that qualified everything cannot have a sweeping "
            "main idea.",
            "Ignoring the verb. Two answers can name the same content and differ only in "
            "whether the author argued it or mentioned it, and only one of those is what "
            "happened.",
            "Answering from the title-like opening sentence. Passages often open with "
            "the view the author is about to complicate, so the opening sentence is "
            "frequently the opposite of the main idea.",
        ],
        ladder={
            1: "One clear argument, and the correct answer restates the author's "
               "conclusion in slightly different words.",
            2: "One wrong answer is true but covers only a single paragraph, so the "
               "coverage test is what decides it.",
            3: "Two answers describe the content correctly and differ in the strength of "
               "their verb.",
            4: "The passage balances two views without endorsing either, and the correct "
               "answer has to be neutral where three tempting answers pick a side.",
            5: "The author's purpose is to qualify a view they largely accept, and the "
               "wrong answers split it into either full agreement or refutation.",
        },
    ),

    Topic(
        slug="rc-detail",
        title="Stated Detail Questions",
        area=RC,
        skill="v_st",
        idea="The answer is in the passage, stated, and your only job is to find the "
             "right lines and refuse to go one inch beyond them.",
        why="These are the most reliably winnable questions in Verbal, and people lose "
            "them by answering from memory of the passage instead of from the passage. "
            "Every one of them is a lookup.",
        facts=[
            ("The question form", "according to the passage, which of the following",
             "The phrase according to the passage is an instruction: the support has to "
             "be findable, not merely reasonable."),
            ("Where to look", "use the map, not the memory",
             "Find the paragraph whose job matches the question, then read the two or "
             "three sentences around the match."),
            ("The proof standard", "you should be able to point at a line",
             "If you cannot underline the support, you are inferring, and this is not an "
             "inference question."),
            ("Paraphrase is expected", "the right answer rarely reuses the passage words",
             "Words that match the passage exactly are more often bait than answer, "
             "because the test writer knows you will search for them."),
            ("EXCEPT and NOT", "four of these are supported, find the one that is not",
             "Reverse the job: you are hunting for the unsupported answer, which means "
             "checking four rather than finding one."),
        ],
        worked=[
            dict(ask="A passage says: 'Although the settlement's granaries could hold "
                     "roughly two years of surplus, excavation has recovered no storage "
                     "vessels of the type used elsewhere in the region.' Which is "
                     "supported: (A) the settlement stored less grain than its neighbours, "
                     "(B) no storage vessels of a regionally common type have been found "
                     "at the settlement, (C) the granaries were never used?",
                 steps=[
                     "Find the line. It is quoted, so the work is comparison, not search.",
                     "(A) compares quantities stored. The passage compares vessel TYPES "
                     "found, not grain stored. That is a different claim.",
                     "(C) goes far beyond the text: absence of one vessel type is not "
                     "absence of use, and the granaries' capacity is stated as fact.",
                     "(B) restates the second clause with nothing added.",
                 ],
                 answer="(B)",
                 why="(A) and (C) are both things a reasonable person might conclude, and "
                     "both are exactly what a stated detail question is testing you to "
                     "refuse. The question did not ask what follows; it asked what the "
                     "passage says."),
        ],
        traps=[
            "Answering from memory because you just read it. The passage is on screen; "
            "confidence is not evidence.",
            "Choosing the answer whose words match the passage most closely. Word overlap "
            "is the cheapest thing for a test writer to fake and the most reliable way to "
            "pull a hurried reader.",
            "Completing the thought. The passage says a vessel type is absent and you "
            "conclude the granaries went unused, which is a small step and still a step.",
            "Missing the EXCEPT. Reading the question too fast inverts your entire job "
            "and you will confirm a correct answer four times without noticing.",
        ],
        ladder={
            1: "One short paragraph and the answer restates a single sentence.",
            2: "The detail is in a longer passage and the answer paraphrases rather than "
               "quotes.",
            3: "Two answers are both in the passage, and only one answers the question "
               "that was asked.",
            4: "The support is split across two sentences, so an answer matching either "
               "half alone is incomplete.",
            5: "An EXCEPT question where the four supported answers are spread across "
               "every paragraph and the unsupported one reads most naturally.",
        },
    ),

    Topic(
        slug="rc-inference",
        title="Inference Questions",
        area=RC,
        skill="v_inf",
        idea="An inference here is something that must be true given the passage, not "
             "something that probably follows from it, which is a much smaller set than "
             "it sounds.",
        why="This is where the everyday meaning of a word costs people points. In "
            "conversation, inferring means making a reasonable leap. On this exam it "
            "means taking a step so small it is almost a restatement.",
        facts=[
            ("The question form", "the passage suggests / implies / it can be inferred",
             "All three phrasings ask the same thing: what is guaranteed by what is "
             "written."),
            ("The standard", "must be true, not could be true",
             "If you can describe any situation consistent with the passage where the "
             "answer is false, the answer is wrong."),
            ("Where inferences come from", "hedges, comparatives, and negations",
             "Only, not all, more than, failed to, unlike. These carry logical content "
             "beyond what they literally assert."),
            ("Small steps win", "the right answer is usually almost boring",
             "A dramatic inference is a wrong inference: the exam does not hide the "
             "answer in a clever leap, it hides it in a dull one."),
            ("Combining two sentences", "the step is allowed, the leap is not",
             "Putting two stated facts together is legitimate inference. Adding a third "
             "fact from your own knowledge is not."),
            ("Negation as a test", "assume the answer is false, does the passage break",
             "If the passage can still be entirely true while the answer is false, that "
             "answer is not an inference."),
        ],
        worked=[
            dict(ask="The passage states: 'Only after the tariff was lifted did exports "
                     "from the province exceed those from its neighbour.' Which must be "
                     "true: (A) the tariff caused the province's exports to be lower, "
                     "(B) before the tariff was lifted, the province's exports did not "
                     "exceed its neighbour's, (C) the neighbour had no tariff?",
                 steps=[
                     "Read 'only after X did Y' as: Y did not happen before X.",
                     "(B) is exactly that restatement. Check it with negation: if the "
                     "province's exports HAD exceeded the neighbour's beforehand, the "
                     "sentence would be false. So it must be true.",
                     "(A) adds causation. The sentence orders two events; it does not say "
                     "one produced the other.",
                     "(C) is about the neighbour's tariffs, which the sentence never "
                     "mentions at all.",
                 ],
                 answer="(B)",
                 why="(B) feels too small to be the answer, and that feeling is the thing "
                     "to train away. 'Only after' is a negation about everything before, "
                     "and turning it into that negation is the whole inference."),
            dict(ask="Same passage adds: 'Not every mill in the province returned to "
                     "full output.' What follows?",
                 steps=[
                     "Not every X did Y means at least one X did not do Y.",
                     "It does NOT mean most did not, or that few did.",
                     "So the guaranteed statement is: at least one mill did not return to "
                     "full output.",
                 ],
                 answer="At least one mill did not return to full output",
                 why="Not every is one of the highest yield phrases in the section "
                     "because everyday speech uses it to imply many did not, while "
                     "logically it guarantees only one. The gap between those two is "
                     "where the wrong answers sit."),
        ],
        traps=[
            "Picking the answer that is most likely true in the real world. Real world "
            "plausibility is not support, and the exam builds wrong answers out of it "
            "deliberately.",
            "Turning sequence into cause. After, following, and once are time words, and "
            "the passage has to say more than sequence before cause is available.",
            "Strengthening the claim. The passage says some and the answer says most; "
            "the passage says suggests and the answer says shows.",
            "Rejecting the correct answer for being obvious. Must be true answers are "
            "supposed to be obvious once found; that is what must be true means.",
        ],
        ladder={
            1: "A single sentence with one clear logical word and an answer that "
               "restates it.",
            2: "The inference combines two adjacent sentences.",
            3: "A quantifier such as not all or only some, where the everyday reading and "
               "the logical reading differ.",
            4: "The support is spread across paragraphs and one wrong answer is true of "
               "the real world but unsupported here.",
            5: "The inference rests on a hedge about what the evidence does not yet show, "
               "and the wrong answers all treat the hedge as a claim.",
        },
    ),

    Topic(
        slug="rc-structure",
        title="Structure and Function Questions",
        area=RC,
        skill="v_ac",
        idea="These ask what a sentence or paragraph is doing, not what it says, and "
             "those are different questions with different answers.",
        why="Function questions are pure structural reading, so they are nearly free if "
            "you mapped the passage and nearly impossible if you did not. They are also "
            "where the map pays for itself a second time.",
        facts=[
            ("The question form", "the author mentions X primarily in order to",
             "The answer is a job, not a summary: to illustrate, to concede, to rebut, "
             "to qualify, to introduce."),
            ("Read around, not at", "the answer is in the sentences either side",
             "A detail's function is set by what it was brought in to serve, which is "
             "almost never in the detail itself."),
            ("Examples serve claims", "an example is evidence for the nearest claim",
             "When a passage names a specific case, look immediately before it for the "
             "general statement it supports."),
            ("Concessions", "although X, Y means X is conceded and Y is the point",
             "The conceded half is frequently what a wrong answer quotes as the author's "
             "view."),
            ("Paragraph function", "each paragraph does one job for the whole",
             "Introduce, complicate, support, qualify, conclude. If you cannot name a "
             "paragraph's job in one verb, you have not finished reading it."),
        ],
        worked=[
            dict(ask="A passage claims early printers standardised spelling more slowly "
                     "than usually supposed. It then says: 'One Antwerp shop, whose "
                     "output survives nearly complete, used three spellings of the same "
                     "common word within a single year.' Why is the shop mentioned?",
                 steps=[
                     "Do not summarise the sentence; ask what it is doing there.",
                     "Look at the sentence before it: the claim about slow "
                     "standardisation.",
                     "A specific named case immediately after a general claim is evidence "
                     "for that claim.",
                     "The parenthetical about surviving output tells you why THIS shop: "
                     "it is unusually good evidence.",
                 ],
                 answer="To give concrete evidence for the claim that standardisation was "
                        "slower than supposed",
                 why="The wrong answer here is almost always a faithful summary of the "
                     "sentence, something like 'to describe the practices of an Antwerp "
                     "printing shop'. That is what the sentence says. The question asked "
                     "what it is for."),
        ],
        traps=[
            "Answering with a summary of the sentence instead of its purpose. This is the "
            "single most common function-question error and the summary answer is always "
            "on offer.",
            "Attaching the example to the wrong claim, usually the one that is nearer in "
            "your memory rather than nearer on the page.",
            "Treating a concession as the author's position. Although and while introduce "
            "the part the author is giving away.",
            "Reading only the cited line. The function of a line is defined entirely by "
            "its neighbours, so the cited line is the one place the answer is not.",
        ],
        ladder={
            1: "A clearly signposted example directly after the claim it supports.",
            2: "The claim is one sentence further away and a nearer claim is on offer as "
               "a wrong answer.",
            3: "The detail serves a concession, so its function is to give ground rather "
               "than to support.",
            4: "The question asks the function of a whole paragraph relative to the "
               "passage's argument.",
            5: "The cited detail supports a claim the author goes on to reject, so its "
               "function is to set up a rebuttal rather than to argue for anything.",
        },
    ),

    Topic(
        slug="rc-tone",
        title="Tone and the Author's Attitude",
        area=RC,
        skill="v_inf",
        idea="The author's attitude is almost always measured and qualified, so the "
             "answer is almost never a strong feeling in either direction.",
        why="Academic prose is written to hedge. The exam draws its passages from that "
            "register and then offers answers with the emotional range of an argument, "
            "which is a range the passage never had.",
        facts=[
            ("Where tone lives", "in adjectives, adverbs and hedges",
             "Surprisingly, merely, only, convincing, overstated, has yet to establish. "
             "Nouns and verbs carry content; the evaluation rides on the modifiers."),
            ("The usual answer", "qualified approval or qualified scepticism",
             "Cautiously optimistic, measured scepticism, qualified endorsement. Passages "
             "that pick a side without qualification are rare."),
            ("What is almost never right", "contempt, indifference, outrage, dismissal",
             "An author indifferent to the subject would not have written about it, and "
             "the exam's sources do not express contempt."),
            ("Two objects, two attitudes", "attitude to the finding is not attitude to "
             "the method",
             "An author can find a result important and its evidence weak, and questions "
             "are built precisely on that split."),
            ("Strength matching", "match the intensity, not just the direction",
             "Getting positive versus negative right and then choosing the extreme "
             "version of it is the most common way to lose these."),
        ],
        worked=[
            dict(ask="An author writes that a new model 'accounts for the anomaly more "
                     "economically than its predecessors, though its central parameter "
                     "has so far resisted independent measurement.' What is the "
                     "attitude: (A) enthusiastic endorsement, (B) qualified approval, "
                     "(C) scepticism, (D) dismissal?",
                 steps=[
                     "Find the evaluative words. 'More economically' is praise. 'Has so "
                     "far resisted independent measurement' is a reservation.",
                     "Both are present, so the answer must contain both.",
                     "(A) drops the reservation. (C) and (D) drop the praise and "
                     "overstate the reservation.",
                     "(B) keeps both, in the right proportion: approval is the main "
                     "clause, the reservation is the subordinate one.",
                 ],
                 answer="(B)",
                 why="The grammar carries the proportion. The praise is in the main "
                     "clause and the reservation is introduced by 'though', which marks "
                     "it as real but secondary. Sentence structure is evidence about "
                     "attitude, not just about meaning."),
        ],
        traps=[
            "Importing your own reaction to the subject matter. The question is about the "
            "author, and the author is often more neutral than the topic deserves.",
            "Reading a single strong word as the whole tone. One sharp adjective in four "
            "paragraphs of hedging does not make an author hostile.",
            "Collapsing two attitudes into one when the author holds different views of "
            "the claim and of the evidence for it.",
            "Choosing the extreme version of the right direction, which is how most tone "
            "questions are actually lost.",
        ],
        ladder={
            1: "One clearly evaluative sentence and an answer that matches its direction.",
            2: "The evaluation is spread over a paragraph and needs summing.",
            3: "Praise and reservation both appear and the answer must hold both.",
            4: "The author's attitude to the finding differs from their attitude to the "
               "method used to get it.",
            5: "The attitude is conveyed only through what the author declines to say, "
               "such as reporting a claim without ever endorsing it.",
        },
    ),
    Topic(
        slug="cr-anatomy",
        title="The Anatomy of an Argument",
        area=CR,
        skill="v_pc",
        idea="Every Critical Reasoning argument is premises plus a conclusion, and "
             "finding which sentence is which is most of the work on every question "
             "type in the section.",
        why="You cannot weaken, strengthen, or find the assumption of an argument whose "
            "conclusion you have misidentified, and misidentifying it is easy because "
            "the conclusion is often not the last sentence.",
        facts=[
            ("The structure", "premises -> conclusion",
             "Premises are offered as true. The conclusion is what they are offered in "
             "support of, and it is the only part that can be attacked."),
            ("Finding the conclusion", "ask which sentence the others are there to "
             "support",
             "Work backwards: pick a candidate and ask whether the rest of the argument "
             "is evidence for it. Only one sentence passes."),
            ("Conclusion signals", "therefore, thus, hence, so, clearly, it follows that",
             "Useful when present, and frequently absent, so the support test matters "
             "more than the signal words."),
            ("Premise signals", "because, since, given that, after all, as shown by",
             "These mark support being offered rather than a claim being made."),
            ("Background", "context that neither supports nor is supported",
             "Often the first sentence. Removing it changes nothing about the argument's "
             "validity, which is the test for whether it is background."),
            ("The gap", "the distance between what is proven and what is claimed",
             "Every CR argument leaves one. The gap is what every question type asks "
             "about, from a different angle."),
        ],
        worked=[
            dict(ask="'Sales of the new model rose 14 percent last quarter. The "
                     "advertising campaign launched at the start of that quarter was "
                     "therefore effective. The campaign ran only in the northeast.' "
                     "What is the conclusion, and what is the gap?",
                 steps=[
                     "Candidate 1: sales rose 14 percent. Is the rest evidence for it? "
                     "No, it is a measured fact.",
                     "Candidate 2: the campaign was effective. Is the sales rise evidence "
                     "for it? Yes. And 'therefore' marks it.",
                     "Candidate 3: the campaign ran only in the northeast. Nothing "
                     "supports it, and it supports nothing directly. It is background, "
                     "and a hint.",
                     "The gap: from 'sales rose after the campaign' to 'the campaign "
                     "caused the rise'.",
                 ],
                 answer="Conclusion: the campaign was effective. Gap: a rise after is "
                        "being read as a rise because of.",
                 why="Notice the conclusion is the middle sentence. People reach for the "
                     "last sentence out of habit, and here the last sentence is the "
                     "detail that makes the argument attackable rather than the claim "
                     "being made."),
            dict(ask="Using that argument, what would weaken it most?",
                 steps=[
                     "The gap is causal, so attack the cause.",
                     "Anything giving an alternative explanation for the 14 percent will "
                     "do it.",
                     "The background sentence hands you one: the campaign ran only in the "
                     "northeast.",
                     "So: sales rose 14 percent nationally, with no larger rise in the "
                     "northeast than elsewhere.",
                 ],
                 answer="Evidence that the rise was not concentrated where the campaign "
                        "ran",
                 why="The weakener came out of the sentence that looked like background. "
                     "Background in CR is rarely decorative: it is usually where the "
                     "test writer has quietly placed the argument's weak point."),
        ],
        traps=[
            "Assuming the conclusion is the last sentence. It is frequently the middle "
            "one, with the final sentence supplying the detail that makes it vulnerable.",
            "Attacking a premise. Premises are given as true, and an answer choice that "
            "disputes one is almost always wrong regardless of how reasonable it sounds.",
            "Reading the background as part of the argument, which makes the argument "
            "look better supported than it is.",
            "Summarising the argument instead of locating its gap. You can restate an "
            "argument perfectly and still have no idea where it is weak.",
        ],
        ladder={
            1: "Two sentences, one signal word, and the conclusion is explicit.",
            2: "No signal word, so the support test is what identifies the conclusion.",
            3: "The conclusion sits mid-paragraph with background on both sides.",
            4: "Two claims are made and only one is the conclusion; the other is an "
               "intermediate step supporting it.",
            5: "The argument states someone else's conclusion and then the author's own, "
               "and the question turns on which is being evaluated.",
        },
    ),

    Topic(
        slug="cr-assumption",
        title="Assumption Questions",
        area=CR,
        skill="v_pc",
        idea="An assumption is something the argument needs to be true but never says, "
             "which means it lives exactly in the gap between the premises and the "
             "conclusion.",
        why="Assumption is the load-bearing question type: strengthen, weaken and flaw "
            "are all built on the same gap. Learning to find the assumption teaches you "
            "most of the section at once.",
        facts=[
            ("The question form", "the argument depends on assuming which of the "
             "following",
             "Depends on is the key phrase: without it the argument collapses, not "
             "merely weakens."),
            ("The negation test", "negate the answer; if the argument breaks, it is "
             "the assumption",
             "This is the only mechanical test in Critical Reasoning and it decides "
             "nearly every assumption question."),
            ("Necessary versus sufficient", "necessary is needed, sufficient would "
             "prove",
             "Assumption questions want necessary. An answer strong enough to prove the "
             "conclusion is usually too strong to be required by it."),
            ("The no-alternative assumption", "nothing else explains the evidence",
             "Any causal argument assumes the absence of other causes, which is why it "
             "is the most common right answer on causal stems."),
            ("The representativeness assumption", "the sample stands for the whole",
             "Any argument from a study, a survey or a subset assumes the subset is "
             "typical."),
            ("The no-change assumption", "what held before still holds",
             "Arguments projecting forward assume conditions do not shift, which is "
             "where predictions are attacked."),
        ],
        worked=[
            dict(ask="'The clinic reduced average waiting time by adding two receptionists. "
                     "The hospital across town, which has similar patient volume, should "
                     "therefore add receptionists to reduce its waiting time.' Which is "
                     "assumed: (A) the hospital has the budget for two receptionists, "
                     "(B) the hospital's waiting time has a similar cause to the clinic's, "
                     "(C) the clinic's waiting time is now the lowest in the region?",
                 steps=[
                     "Gap: what worked THERE will work HERE. So the assumption concerns "
                     "comparability.",
                     "Negate (B): the hospital's waiting time has a different cause, say "
                     "a shortage of examination rooms. Then adding receptionists would "
                     "not help and the argument collapses. So (B) is required.",
                     "Negate (A): the hospital lacks budget. The argument says it should, "
                     "not that it can; recommendation arguments survive this. Weaker "
                     "than it looks.",
                     "Negate (C): the clinic is not the lowest. Irrelevant; the argument "
                     "never claimed it was.",
                 ],
                 answer="(B)",
                 why="The negation test did all the work and it did it without any "
                     "judgement about which answer felt most relevant. That is the point "
                     "of having a mechanical test: relevance is exactly the intuition the "
                     "wrong answers are built to exploit."),
        ],
        traps=[
            "Choosing something that would strengthen the argument rather than something "
            "it requires. Helpful is not the same as necessary, and assumption questions "
            "want necessary.",
            "Choosing an answer that is too strong. If the answer says always or none, "
            "negate it: the negation is usually easy to accept, which shows the argument "
            "never needed it.",
            "Bringing in real world knowledge about what such an argument would obviously "
            "need. The argument only needs what closes ITS gap.",
            "Skipping the negation test because the answer feels right. Feeling right is "
            "what the second-best answer is engineered to do.",
        ],
        ladder={
            1: "A one-step gap and an answer that names it almost directly.",
            2: "Two answers are relevant and only one fails under negation.",
            3: "A causal argument where the assumption is the absence of an alternative "
               "cause.",
            4: "The tempting answer is sufficient rather than necessary, and negating it "
               "leaves the argument standing.",
            5: "The assumption concerns the comparability of two cases that the argument "
               "treats as equivalent without saying so.",
        },
    ),

    Topic(
        slug="cr-weaken",
        title="Weaken Questions",
        area=CR,
        skill="v_ac",
        idea="You are making the conclusion harder to believe, not proving it false, and "
             "the difference between those two is where most wrong answers live.",
        why="Weaken is the most common Critical Reasoning form and the one where the "
            "everyday instinct, to argue with the evidence, is exactly wrong. You attack "
            "the link, not the facts.",
        facts=[
            ("The question form", "which most seriously weakens / calls into question",
             "Most seriously: you are ranking answers by damage, not sorting them into "
             "damaging and not."),
            ("What you attack", "the gap, never the premises",
             "Premises are given as true. An answer denying one is out of bounds however "
             "plausible it reads."),
            ("Alternative cause", "something else explains the evidence",
             "The standard weakener for any argument that reads a correlation as a "
             "cause."),
            ("Reversed cause", "the effect could be producing the cause",
             "Sales rose and advertising rose; perhaps the budget rose because sales did."),
            ("Unrepresentative sample", "the group studied is not like the group "
             "concluded about",
             "Attacks any argument that generalises from a subset."),
            ("The plan will not work", "the proposal fails on its own terms",
             "For recommendation arguments: show the mechanism the plan relies on is "
             "absent or already saturated."),
        ],
        worked=[
            dict(ask="'Employees who use the new scheduling software complete 20 percent "
                     "more tasks per week than those who do not. The company should "
                     "require all employees to use it.' Which weakens most: (A) the "
                     "software costs more than expected, (B) employees chose whether to "
                     "adopt the software, and the earliest adopters were the most "
                     "productive employees already, (C) some employees find the interface "
                     "difficult?",
                 steps=[
                     "Conclusion: everyone should be required to use it. Evidence: users "
                     "complete more tasks.",
                     "Gap: the software is causing the difference, rather than the "
                     "difference existing beforehand.",
                     "(B) attacks exactly that: self-selection means the 20 percent may "
                     "measure who adopted, not what adopting did.",
                     "(A) is about cost, which the argument never traded against output. "
                     "(C) is a difficulty, not evidence the gain is illusory.",
                 ],
                 answer="(B)",
                 why="(B) does not dispute the 20 percent at all: it accepts the number "
                     "and removes its meaning. That is what attacking the link looks "
                     "like, and it is strictly stronger than arguing with the data."),
        ],
        traps=[
            "Attacking a premise. The answer that says the 20 percent figure was measured "
            "badly is out of bounds, and it will be on offer.",
            "Choosing a mildly negative fact. Costs more, is unpopular, has drawbacks: "
            "these are bad news about the subject, not damage to the reasoning.",
            "Weakening a conclusion the argument did not draw, usually a broader one you "
            "supplied yourself.",
            "Forgetting that the conclusion may be a recommendation. You weaken a "
            "recommendation by showing it will not achieve its aim, not by showing the "
            "aim is expensive.",
        ],
        ladder={
            1: "A direct causal claim and an answer supplying an obvious alternative "
               "cause.",
            2: "Two answers are negative and only one touches the reasoning.",
            3: "The weakener works by attacking the sample rather than the cause.",
            4: "The conclusion is a recommendation, so the weakener must show the plan "
               "fails rather than that the situation is bad.",
            5: "The strongest weakener requires combining it with a premise before its "
               "effect is visible, and a flashier answer damages nothing.",
        },
    ),

    Topic(
        slug="cr-strengthen",
        title="Strengthen Questions",
        area=CR,
        skill="v_ac",
        idea="You are closing the same gap a weaken question would attack, usually by "
             "ruling out the alternative explanation rather than by adding more of the "
             "same evidence.",
        why="Strengthen and weaken are one skill, and people who treat them as two end up "
            "choosing answers that repeat the premise, which adds nothing because the "
            "premise was already granted.",
        facts=[
            ("The question form", "which most strengthens / provides the most support",
             "Again a ranking: several answers may help, and one helps most."),
            ("Ruling out alternatives", "no other cause was present",
             "The mirror of the standard weakener, and the most common right answer on "
             "causal stems."),
            ("Closing the comparison", "the two cases really are alike",
             "For analogy and recommendation arguments, evidence of comparability is "
             "what the argument was missing."),
            ("More of the premise is not support", "restating evidence adds nothing",
             "If the argument says users completed more tasks, an answer saying they "
             "completed many more tasks does not close the gap."),
            ("Strength is relative", "a small closure of the real gap beats a large "
             "irrelevance",
             "Answers that sound dramatic often address something the argument did not "
             "depend on."),
        ],
        worked=[
            dict(ask="'Towns that introduced a bottle deposit saw litter fall by a third. "
                     "The deposit reduced litter.' Which most strengthens: (A) the "
                     "deposit was set at a level residents considered meaningful, "
                     "(B) neighbouring towns without a deposit saw no change in litter "
                     "over the same period, (C) litter had been rising in those towns "
                     "before the deposit?",
                 steps=[
                     "Gap: litter fell after the deposit; was the deposit the cause?",
                     "(B) supplies a control group: the same period, no deposit, no "
                     "change. That removes period-wide causes such as weather or a "
                     "national campaign.",
                     "(C) helps a little by removing a pre-existing downward trend, but a "
                     "rising trend reversing is weaker than a matched control.",
                     "(A) explains WHY the deposit might work, which is a mechanism, not "
                     "evidence that it did.",
                 ],
                 answer="(B)",
                 why="A control group is the strongest strengthener available to a causal "
                     "argument, because it eliminates an entire family of alternative "
                     "explanations at once rather than one at a time."),
        ],
        traps=[
            "Choosing an answer that restates the evidence more emphatically. The "
            "premises were already accepted, so repeating them changes nothing.",
            "Choosing a plausible mechanism instead of evidence. Explaining how something "
            "could work is not evidence that it did.",
            "Strengthening a different conclusion, usually a more general one than the "
            "argument actually drew.",
            "Stopping at the first answer that helps. The question asks which helps most, "
            "so a partially helpful answer is a trap when a control group is on offer.",
        ],
        ladder={
            1: "The answer directly rules out the one obvious alternative cause.",
            2: "Two answers help and one helps more, so ranking is required.",
            3: "The strongest answer is a control group rather than extra evidence about "
               "the treated group.",
            4: "One answer provides a mechanism and another provides evidence, and the "
               "mechanism reads more convincingly.",
            5: "The argument depends on an unstated comparison, and the strengthener "
               "works by establishing the two cases are alike in the relevant respect.",
        },
    ),

    Topic(
        slug="cr-flaw",
        title="Flaw and Reasoning Error",
        area=CR,
        skill="v_ac",
        idea="The argument is already broken and your job is to name the break, which "
             "means these questions reward recognising a small number of recurring "
             "patterns.",
        why="Flaws repeat. The same half dozen errors account for most of what the exam "
            "asks you to spot, so this is the highest leverage memorisation in Verbal, "
            "and one of the few places memorisation helps at all.",
        facts=[
            ("Correlation taken as causation", "A and B occur together, so A causes B",
             "The most common flaw on the exam and the one with the most disguises."),
            ("Unrepresentative sample", "this group behaved so, therefore all do",
             "Watch for volunteers, subscribers, respondents, and anyone who opted in."),
            ("Necessary treated as sufficient", "X is needed, so X is enough",
             "You need a ticket to board, which does not mean a ticket gets you on."),
            ("Percent and number confused", "a share moved, so a count moved",
             "A rising share of a shrinking total can be a falling count."),
            ("Attacking the source", "the claimant is biased, so the claim is false",
             "A motive to lie is not evidence of lying."),
            ("Absence of evidence", "not shown to be true, so false",
             "An untested claim is untested, not refuted."),
            ("Equivocation", "one word used in two senses",
             "The argument slides between two meanings and draws a conclusion that needs "
             "only one of them."),
        ],
        worked=[
            dict(ask="'Every executive we surveyed who reads industry newsletters "
                     "reported above-average awareness of competitors. Reading "
                     "newsletters clearly raises competitive awareness.' Name the flaw.",
                 steps=[
                     "Evidence: newsletter readers report high awareness. Conclusion: "
                     "reading raises awareness.",
                     "Check causation: the evidence is co-occurrence, the conclusion is "
                     "cause. Flaw candidate one.",
                     "Check direction: executives already attentive to competitors are "
                     "likelier to read newsletters. The cause may run the other way.",
                     "Also note 'reported', which is self-assessment, and 'we surveyed', "
                     "which may not be representative. The primary flaw remains the "
                     "causal leap.",
                 ],
                 answer="It treats a correlation as a cause, ignoring that the awareness "
                        "may produce the reading rather than the other way round",
                 why="Several flaws are present at once, which is normal at higher "
                     "difficulty. The right answer names the one the conclusion actually "
                     "rests on, so identify the conclusion first and ask what it needed "
                     "that it did not get."),
        ],
        traps=[
            "Naming a flaw that is real but not the one the conclusion depends on. Hard "
            "arguments contain several, and only one is load bearing.",
            "Choosing an answer describing a flaw the argument did not commit, stated in "
            "impressive logical vocabulary.",
            "Objecting to the conclusion rather than the reasoning. You may think the "
            "conclusion is false; the question asks how the argument fails to establish "
            "it.",
            "Missing that a survey of a self-selected group is unrepresentative by "
            "construction, because the sampling is usually mentioned in passing.",
        ],
        ladder={
            1: "A bare correlation-to-causation leap with the answer naming it plainly.",
            2: "The flaw is a sampling problem signalled by one word such as volunteers.",
            3: "Necessary and sufficient are confused, and the answer must say which way.",
            4: "Several flaws are present and the answer names the one the conclusion "
               "rests on.",
            5: "The flaw is an equivocation, where a single word carries one meaning in "
               "the premise and another in the conclusion.",
        },
    ),

    Topic(
        slug="cr-evaluate",
        title="Evaluate the Argument",
        area=CR,
        skill="v_ac",
        idea="You are looking for the question whose two possible answers pull the "
             "argument in opposite directions, which is a sharper test than asking what "
             "would be useful to know.",
        why="These look open ended and are not. There is a mechanical test, the variance "
            "test, that decides them, and without it the answers all look relevant "
            "because they are all about the topic.",
        facts=[
            ("The question form", "most useful to know / most relevant in evaluating",
             "The answer is a question or a quantity to determine, not a fact."),
            ("The variance test", "answer it yes, then no; does the argument move both "
             "ways",
             "If both answers leave the argument where it was, the option is irrelevant "
             "however on-topic it sounds."),
            ("It is weaken and strengthen together", "one answer helps, the other hurts",
             "A correct evaluate option is a weakener and a strengthener bundled into a "
             "single question."),
            ("Targets the gap", "the question probes the assumption",
             "Find the assumption first, then look for the answer that asks whether it "
             "holds."),
            ("On-topic is not the test", "relevance to the subject is not relevance to "
             "the reasoning",
             "Most wrong answers are unmistakably about the same subject and touch "
             "nothing the conclusion depends on."),
        ],
        worked=[
            dict(ask="'The museum extended opening hours into the evening and monthly "
                     "attendance rose 12 percent. The extension should be made "
                     "permanent.' Which is most useful to determine: (A) whether the "
                     "evening staff cost more per hour, (B) whether daytime attendance "
                     "fell during the same months, (C) how many museums in the region "
                     "open in the evening?",
                 steps=[
                     "Assumption: the 12 percent is new attendance, not attendance moved "
                     "from daytime.",
                     "Apply variance to (B). If daytime attendance fell sharply, the rise "
                     "is largely redistribution and the case weakens. If daytime held "
                     "steady, the rise is genuinely new and the case strengthens. It "
                     "swings both ways.",
                     "Apply variance to (A). Higher cost is a consideration the argument "
                     "never weighed, and either answer leaves the attendance claim "
                     "intact.",
                     "(C) tells you about other museums and nothing about this one.",
                 ],
                 answer="(B)",
                 why="The variance test converts a vague judgement about usefulness into "
                     "two concrete checks. Do them out loud: say the yes answer and the "
                     "no answer and watch whether the argument actually moves."),
        ],
        traps=[
            "Choosing an answer that is interesting but leaves the argument unchanged "
            "either way, which describes most of the wrong answers here.",
            "Skipping the variance test and picking by topical relevance, which is the "
            "exact intuition these answers are built to catch.",
            "Testing only one direction. An option can look damaging on the yes answer "
            "and do nothing on the no answer, which means it is not the strongest.",
            "Forgetting the conclusion is often a recommendation, so the useful question "
            "usually concerns whether the plan achieves its aim.",
        ],
        ladder={
            1: "One answer obviously swings the argument and the rest are off topic.",
            2: "Two answers are on topic and only one varies the argument.",
            3: "The option probes an alternative cause rather than the stated evidence.",
            4: "The correct option tests whether a measured gain is new or merely moved "
               "from somewhere else.",
            5: "Several options vary the argument slightly and one varies it most, so the "
               "test has to be applied to each rather than stopped at the first hit.",
        },
    ),

    Topic(
        slug="cr-inference",
        title="Inference and Must Be True",
        area=CR,
        skill="v_inf",
        idea="There is no argument to evaluate here: you are given facts and asked what "
             "they guarantee, which makes this the one Critical Reasoning type with no "
             "gap to find.",
        why="People bring weaken-and-strengthen habits to these questions and start "
            "hunting for flaws in a passage that is making no argument at all. "
            "Recognising the type is half the battle.",
        facts=[
            ("The question form", "which must be true / which is most strongly supported",
             "No conclusion is offered, so there is nothing to attack; you are "
             "constructing, not critiquing."),
            ("The standard", "guaranteed by the statements, not merely consistent",
             "Could be true is not the test. Many wrong answers are perfectly possible."),
            ("Combine, do not extend", "two given facts may be joined",
             "Joining what you were given is inference. Adding what you know is not."),
            ("Watch the quantifiers", "some, most, all, none, only",
             "Most of the difficulty in this type is quantifier logic. Some means at "
             "least one; most means more than half; only reverses a conditional."),
            ("Conditionals", "if A then B gives you: not B, therefore not A",
             "It does not give you: not A, therefore not B, which is the most commonly "
             "offered wrong answer."),
            ("Overlap", "most of X are Y and most of X are Z guarantees an overlap",
             "Two majorities of the same group must share at least one member."),
        ],
        worked=[
            dict(ask="'Every technician certified before 2019 completed the field course. "
                     "Some technicians who completed the field course have never worked "
                     "offshore.' What must be true: (A) some technicians certified before "
                     "2019 have never worked offshore, (B) some who completed the field "
                     "course were certified before 2019, (C) not every technician who "
                     "completed the field course was certified before 2019?",
                 steps=[
                     "Fact 1: certified-before-2019 is a subset of completed-the-course.",
                     "Fact 2: at least one course-completer has never worked offshore.",
                     "(A) places that person inside the pre-2019 subset. Nothing requires "
                     "that; they could be a later certifier. Not guaranteed.",
                     "(B) claims the pre-2019 group is non-empty. The statements never "
                     "say anyone was certified before 2019. Not guaranteed.",
                     "(C) claims the course group is strictly larger. Also not "
                     "guaranteed: every completer could be pre-2019.",
                 ],
                 answer="None of the three is guaranteed",
                 why="This is the shape of a level five inference question: three answers "
                     "that each require one extra step, and the extra step is always "
                     "either assuming a group is non-empty or assuming a subset is "
                     "proper. Both feel automatic and neither is given."),
        ],
        traps=[
            "Reversing a conditional. If A then B does not give you if B then A, and the "
            "reversed form is offered on nearly every conditional question.",
            "Assuming a group has members. All X are Y says nothing about whether any X "
            "exists, and higher difficulty questions turn on exactly that.",
            "Reading some as some but not all. Some means at least one, and is fully "
            "compatible with all.",
            "Choosing the answer that sounds like a sensible conclusion. There is no "
            "conclusion here, and sensible is the wrong standard.",
        ],
        ladder={
            1: "Two facts that combine in one obvious step.",
            2: "A conditional where the correct answer is its contrapositive.",
            3: "A quantifier question turning on the difference between some and most.",
            4: "The wrong answers reverse a conditional or assume a group is non-empty.",
            5: "Several statements must be chained, and every wrong answer needs exactly "
               "one unstated step.",
        },
    ),

    Topic(
        slug="cr-paradox",
        title="Explain the Discrepancy",
        area=CR,
        skill="v_pc",
        idea="Two facts are both true and appear to conflict, and the right answer "
             "supplies the missing circumstance under which both hold at once.",
        why="These are among the fastest questions in the section once you state the "
            "conflict precisely, and among the slowest when you do not, because every "
            "answer sounds like it might explain something.",
        facts=[
            ("The question form", "which best explains / resolves the discrepancy",
             "Nothing is being argued. Both facts stand and you are reconciling them."),
            ("State the conflict first", "X happened, yet Y, which seems to rule X out",
             "Say it in one sentence before reading the answers. Vague conflicts produce "
             "vague answer selection."),
            ("The answer explains both", "not just one side",
             "An answer accounting for only one of the two facts leaves the discrepancy "
             "exactly where it was."),
            ("Usual resolutions", "a hidden third group, a changed denominator, a "
             "different measure",
             "Most discrepancies dissolve when you notice the two facts are counting "
             "different things or different populations."),
            ("Percent versus count", "a rate and a total can move in opposite directions",
             "A falling rate on a growing base can mean a rising count, which resolves a "
             "great many of these."),
        ],
        worked=[
            dict(ask="'The share of commuters cycling to the centre rose from 6 to 11 "
                     "percent after the new lanes opened, yet the number of bicycles "
                     "counted at the centre's racks fell.' What explains this?",
                 steps=[
                     "State the conflict: cycling share up, bicycle count down.",
                     "A share and a count differ by the size of the base. If total "
                     "commuters fell enough, 11 percent of a smaller number can be fewer "
                     "than 6 percent of a larger one.",
                     "Alternatively the measure differs: the racks count parked bicycles, "
                     "not cyclists, so cyclists may now park elsewhere.",
                     "Either resolves both facts without disputing either.",
                 ],
                 answer="Total commuting to the centre fell sharply over the same period, "
                        "so a larger share of a much smaller total is a smaller number",
                 why="The shape here is the most common one in the whole question type: "
                     "one fact is a rate and the other is a count. When you see a percent "
                     "beside a number, check the denominator before reading any answer."),
        ],
        traps=[
            "Choosing an answer that explains only one of the two facts. It will feel "
            "explanatory because it is genuinely about the situation.",
            "Choosing an answer that denies one of the facts. Both are given as true and "
            "the job is to reconcile, not adjudicate.",
            "Failing to state the conflict precisely, which leaves you grading answers on "
            "general plausibility.",
            "Missing a percent-versus-count shape, which is the resolution often enough "
            "to be worth checking first.",
        ],
        ladder={
            1: "A plain conflict and one answer that obviously reconciles it.",
            2: "Two answers are relevant and only one addresses both facts.",
            3: "The resolution is a change in the denominator rather than in behaviour.",
            4: "The two facts measure different populations, and noticing that is the "
               "whole question.",
            5: "The resolution requires a third group that neither fact mentions, and "
               "every wrong answer explains one side convincingly.",
        },
    ),

    Topic(
        slug="cr-boldface",
        title="Boldface and the Role of a Statement",
        area=CR,
        skill="v_pc",
        idea="Two portions are marked and you are asked what each is doing, so the "
             "answer depends entirely on the argument's structure and not at all on its "
             "content.",
        why="These look intimidating and are mechanical. Once you label each boldface as "
            "premise, conclusion, opposing view or concession, most answer choices "
            "eliminate themselves on the first half.",
        facts=[
            ("The question form", "the two portions play which roles",
             "Answers come in pairs, so a wrong first half kills the whole answer "
             "regardless of the second."),
            ("Label before reading answers", "premise, conclusion, opposing claim, "
             "concession",
             "Decide independently, then find the answer that matches. Reading answers "
             "first is how the plausible wrong pair gets in."),
            ("Whose conclusion", "the author's or someone else's",
             "Many of these contain two conclusions and the distinction between them is "
             "usually the whole question."),
            ("Support direction", "does it support the author or the view being rebutted",
             "The most common answer-choice difference is not what a portion is but "
             "which side it serves."),
            ("Eliminate on half one", "check the first role across all five answers first",
             "This usually leaves two, and only then is the second half worth reading."),
        ],
        worked=[
            dict(ask="'It has long been held that the canal was built for irrigation. "
                     "[BOLD 1: Sediment cores show the channel carried water only in "
                     "months when no crops were grown.] Some argue the timing reflects "
                     "later reuse. [BOLD 2: But the channel's lining is contemporaneous "
                     "with its construction.] The canal was therefore not built for "
                     "irrigation.' What roles do the two portions play?",
                 steps=[
                     "Find the author's conclusion: the last sentence, the canal was not "
                     "built for irrigation.",
                     "BOLD 1 is evidence for that conclusion. It is a premise supporting "
                     "the author.",
                     "The sentence after BOLD 1 is an objection to it, not the author's "
                     "view.",
                     "BOLD 2 answers that objection, so it is a premise that defends the "
                     "author's evidence against a counter-argument.",
                 ],
                 answer="The first is evidence supporting the author's conclusion; the "
                        "second is evidence answering an objection to that evidence",
                 why="Neither boldface is the conclusion, which is the most common "
                     "structure and the one people expect least. Locating the "
                     "conclusion separately, before looking at either boldface, is what "
                     "keeps you from forcing one of them into that role."),
        ],
        traps=[
            "Assuming one of the boldface portions must be the conclusion. Frequently "
            "neither is.",
            "Mixing up the author's conclusion with the view the author is arguing "
            "against, which is usually stated first and at length.",
            "Reading the answer choices before labelling. The vocabulary in the answers "
            "is designed to make several labels sound defensible.",
            "Checking both halves of every answer. Eliminating on the first half is "
            "faster and less error prone.",
        ],
        ladder={
            1: "One boldface is the conclusion and the other is a premise supporting it.",
            2: "One boldface belongs to an opposing view, clearly signposted.",
            3: "Neither boldface is the conclusion and both are evidence on opposite "
               "sides.",
            4: "One boldface is a concession the author makes before rejecting the view "
               "it belongs to.",
            5: "The argument contains two conclusions, one the author's and one an "
               "opponent's, and the boldface roles differ only in whose they serve.",
        },
    ),

    Topic(
        slug="cr-plan",
        title="Plans, Proposals and Predictions",
        area=CR,
        skill="v_pc",
        idea="A plan argument concludes that doing something will achieve an aim, so "
             "every question about it turns on whether the mechanism connecting action "
             "to aim actually holds.",
        why="Recommendation stems are extremely common and they change what counts as a "
            "good answer. Facts that are merely bad news about the plan are not "
            "objections; facts that break the mechanism are.",
        facts=[
            ("The structure", "do X, in order to achieve Y",
             "Two things to check: does X produce the intended effect, and does that "
             "effect deliver Y."),
            ("The mechanism assumption", "the lever works as described",
             "Weaken by showing the lever is already at its limit, or that it moves "
             "something other than the target."),
            ("The no-offset assumption", "nothing cancels the gain",
             "Plans fail when the gain is offset elsewhere: demand shifts, people "
             "substitute, a bottleneck moves rather than clears."),
            ("Feasibility is usually not the point", "cost and difficulty are separate",
             "Unless the argument weighed cost, an expensive plan is still a plan that "
             "would work."),
            ("Predictions assume continuity", "conditions that held will keep holding",
             "The standard attack on a forecast is a reason the past pattern will not "
             "continue."),
        ],
        worked=[
            dict(ask="'To cut congestion, the city will convert one traffic lane on the "
                     "bridge to a bus lane, since buses carry more people per lane than "
                     "cars.' Which most seriously questions the plan: (A) the conversion "
                     "will cost more than budgeted, (B) most bridge traffic is freight "
                     "that cannot switch to buses, (C) bus fares will rise next year?",
                 steps=[
                     "Plan: convert a lane. Aim: cut congestion. Mechanism: people move "
                     "from cars to buses, so fewer vehicles.",
                     "(B) attacks the mechanism at its root: if the traffic cannot switch, "
                     "removing a lane reduces capacity without reducing demand, which "
                     "makes congestion worse.",
                     "(A) is cost, which the argument never traded against congestion.",
                     "(C) is a change to buses that might reduce ridership slightly, far "
                     "weaker than showing the target population cannot switch at all.",
                 ],
                 answer="(B)",
                 why="(B) is strong because it does not merely blunt the plan, it "
                     "reverses it: the same fact that removes the benefit also creates a "
                     "harm. On plan questions, always check whether an answer makes the "
                     "plan backfire rather than just underperform."),
        ],
        traps=[
            "Treating cost as an objection when the argument never weighed cost against "
            "the goal.",
            "Accepting a small drawback as the answer when a larger answer breaks the "
            "mechanism entirely.",
            "Missing that a plan can backfire, not merely fail, and that the backfiring "
            "answer is the stronger one when both are present.",
            "Evaluating whether the aim is worth pursuing. The argument's aim is given; "
            "your job is whether the plan achieves it.",
        ],
        ladder={
            1: "The answer plainly states the plan's mechanism does not exist.",
            2: "Two answers are negative and only one touches the mechanism.",
            3: "The plan's gain is offset elsewhere, so the net effect is nil.",
            4: "The correct answer shows the plan backfires rather than merely "
               "underperforms.",
            5: "The conclusion is a forecast resting on continuity, and the answer gives "
               "a specific reason the past pattern will not hold.",
        },
    ),
    Topic(
        slug="logic-causation",
        title="Correlation and Causation",
        area=LOGIC,
        skill="v_ac",
        idea="When two things move together there are five explanations and only one of "
             "them is that the first caused the second, so a causal conclusion needs the "
             "other four ruled out.",
        why="This single pattern accounts for more Critical Reasoning questions than any "
            "other, and it appears in Data Insights too. Knowing the five branches turns "
            "a judgement call into a checklist.",
        facts=[
            ("The five explanations", "cause, reverse cause, third cause, coincidence, "
             "selection",
             "Any observed association is one of these. A causal conclusion is the claim "
             "that it is the first one."),
            ("Reverse causation", "B caused A, not A caused B",
             "Hospitals correlate with illness. Advertising budgets correlate with sales, "
             "and budgets are often set from last quarter's sales."),
            ("Third cause", "C caused both A and B",
             "Ice cream sales and drownings both rise with temperature. Neither touches "
             "the other."),
            ("Coincidence", "with enough comparisons, some will line up",
             "The weakest branch in real arguments and still a legitimate answer when the "
             "sample is small."),
            ("Selection", "the groups differed before anything happened",
             "Anyone who opted in, volunteered, subscribed or adopted early was already "
             "different, and that difference is the rival explanation."),
            ("What a control group does", "removes third cause and coincidence at once",
             "This is why a matched comparison group is the strongest single strengthener "
             "available to a causal argument."),
        ],
        worked=[
            dict(ask="'Students who attend the optional review session score higher on "
                     "the final. The session improves scores.' Walk the five branches.",
                 steps=[
                     "Cause: the session teaches something that helps. Possible.",
                     "Reverse: high scores cause attendance? Not literally, but "
                     "anticipated performance could: students expecting to do well may "
                     "be the conscientious ones who attend.",
                     "Third cause: conscientiousness produces both attendance and "
                     "studying. Strong candidate.",
                     "Coincidence: unlikely with a full cohort.",
                     "Selection: the session is OPTIONAL, so attenders self-selected. "
                     "This is the decisive branch.",
                 ],
                 answer="Selection and third cause are both live, and the word optional "
                        "is what flags them",
                 why="One word, optional, carried the whole weakness. Scan every causal "
                     "argument for the words that reveal how the groups were formed: "
                     "optional, volunteered, chose, signed up, those who responded."),
            dict(ask="What single piece of evidence would most strengthen that argument?",
                 steps=[
                     "The live rivals are selection and third cause.",
                     "A control group removes both: assign students at random rather than "
                     "letting them choose.",
                     "So: in a term when attendance was assigned at random, attenders "
                     "still scored higher.",
                 ],
                 answer="Evidence from random assignment rather than self-selection",
                 why="Randomisation is the one move that closes several branches at "
                     "once, which is why exam answers describing a controlled comparison "
                     "beat answers adding more observational evidence."),
        ],
        traps=[
            "Accepting a causal conclusion because a mechanism is plausible. A believable "
            "story about how A could cause B is not evidence that it did.",
            "Ruling out reverse causation because it sounds odd. Anticipation, "
            "expectation and planning all let a later event shape an earlier behaviour.",
            "Treating a large sample as protection against selection bias. A bigger "
            "self-selected group is a more precisely measured biased group.",
            "Forgetting that ruling out one branch leaves four. An answer eliminating "
            "coincidence does very little if selection is untouched.",
        ],
        ladder={
            1: "A bare association presented as cause, with the alternative named "
               "directly in the answer.",
            2: "The alternative is reverse causation and the answer states it plainly.",
            3: "A third cause is available and must be recognised rather than supplied.",
            4: "Selection bias is signalled by a single word about how the groups formed.",
            5: "Two branches are live at once and the answer closes the one the "
               "conclusion actually rests on.",
        },
    ),

    Topic(
        slug="logic-quantity",
        title="Percents, Numbers and Rates in Arguments",
        area=LOGIC,
        skill="v_ac",
        idea="A share, a count and a rate are three different quantities, and an argument "
             "that starts with one and concludes about another has a gap whether or not "
             "it looks like arithmetic.",
        why="This is the quantitative flaw that shows up in Verbal, and it is also how "
            "most Explain the Discrepancy questions resolve. It is worth being fluent "
            "in because it is mechanical and the exam uses it constantly.",
        facts=[
            ("Share versus count", "percent of what",
             "A rising share of a shrinking total can be a falling count. A falling share "
             "of a growing total can be a rising count."),
            ("The denominator moves too", "both parts of a fraction can change",
             "Most percent flaws come from treating the base as fixed when the argument "
             "gave you no reason to."),
            ("Rate versus total", "per unit is not overall",
             "Accidents per mile driven can fall while total accidents rise, if miles "
             "driven rose more."),
            ("Percent change of a percent", "points and percent are different units",
             "From 4 percent to 6 percent is a rise of 2 percentage points and of 50 "
             "percent, and arguments trade on the ambiguity."),
            ("Bigger share of a smaller pie", "the classic discrepancy resolution",
             "When a rate and a count move opposite ways, look at the base before "
             "anything else."),
            ("Comparing two percents", "of different bases they are not comparable",
             "Thirty percent of the small division and ten percent of the large one may "
             "be the same number of people."),
        ],
        worked=[
            dict(ask="'The proportion of our revenue from Europe fell from 30 percent to "
                     "22 percent. Our European business is shrinking.' What is wrong?",
                 steps=[
                     "The premise is about a share of total revenue. The conclusion is "
                     "about the size of the European business, a count.",
                     "Share = European revenue / total revenue. The share can fall "
                     "because the numerator fell OR because the denominator rose.",
                     "If total revenue doubled while European revenue rose by 45 percent, "
                     "the share falls and Europe grew.",
                     "So the conclusion does not follow.",
                 ],
                 answer="A falling share is consistent with a growing European business "
                        "if the rest of the business grew faster",
                 why="The test is always the same: name the numerator and the "
                     "denominator out loud. Almost every percent flaw becomes visible the "
                     "moment the denominator is said aloud, because arguments rely on you "
                     "never asking percent of what."),
        ],
        traps=[
            "Reading a percent as a count. Share language and count language look alike "
            "in prose and the argument depends on that.",
            "Assuming the base is constant. Nothing in the argument usually says so, and "
            "the gap is exactly there.",
            "Confusing percentage points with percent. A change from 4 to 6 is both 2 "
            "points and 50 percent, and answers exploit the larger-sounding one.",
            "Comparing percentages from different bases as though they were comparable "
            "quantities.",
        ],
        ladder={
            1: "A share is stated and the conclusion is about the same share.",
            2: "A share moves and the conclusion is about a count, with the base "
               "explicitly variable.",
            3: "The base change is implied rather than stated and has to be recognised.",
            4: "A rate and a total move in opposite directions and both facts are true.",
            5: "The argument compares two percentages of different bases and concludes "
               "about the underlying numbers.",
        },
    ),

    Topic(
        slug="logic-wrong-answers",
        title="How Wrong Answers Are Built",
        area=LOGIC,
        skill="v_st",
        idea="Wrong answers are manufactured to a small number of patterns, and "
             "recognising the pattern is often faster and more reliable than arguing your "
             "way to the right answer.",
        why="Under time pressure you will not always be certain which answer is right. "
            "You can almost always be certain that three of them are wrong, and "
            "elimination by pattern is the skill that converts partial understanding "
            "into a correct answer.",
        facts=[
            ("Out of scope", "true, relevant sounding, about something not at issue",
             "The most common wrong answer. It discusses the topic without touching what "
             "the question asked."),
            ("Too strong", "all, never, must, only, impossible",
             "Extreme language is rarely supportable by a hedged passage, and the exam "
             "hedges almost everything."),
            ("Half right", "one clause correct, the next clause wrong",
             "You confirm the first half and stop reading. Read every clause of every "
             "answer you are about to choose."),
            ("Reversed", "the right relationship pointing the wrong way",
             "Cause and effect swapped, or the claim attached to the wrong holder."),
            ("Word match", "reuses the passage's exact words to say something else",
             "Verbatim overlap is the cheapest bait available and it works best on a "
             "hurried reader."),
            ("Real world true", "correct about the world, unsupported by the text",
             "Especially dangerous on inference questions, where your own knowledge feels "
             "like evidence."),
            ("Right answer, wrong question", "answers a question the stem did not ask",
             "A perfect main idea offered on a function question, or a true detail on an "
             "inference question."),
        ],
        worked=[
            dict(ask="An inference question on a passage about medieval canal building "
                     "offers: (A) canals were the most important infrastructure of the "
                     "period, (B) the Antwerp shop's records are incomplete, (C) at "
                     "least one canal was lined at the time of its construction, (D) "
                     "canal building always required central authority. Name each "
                     "pattern.",
                 steps=[
                     "(A) 'most important' is a superlative the passage cannot have "
                     "supported. Too strong, and probably out of scope.",
                     "(B) belongs to a different passage entirely: it word-matches a "
                     "detail you remember. Out of scope.",
                     "(D) 'always' is too strong, and 'required' converts a common "
                     "feature into a necessity. Two patterns at once.",
                     "(C) is modest, guaranteed by a single stated fact, and says nothing "
                     "beyond it.",
                 ],
                 answer="(C)",
                 why="Notice the correct answer is the least impressive of the four. On "
                     "inference questions the quiet answer wins so often that being "
                     "unimpressed by an answer is mild evidence in its favour."),
        ],
        traps=[
            "Choosing the answer you understand best. Clarity is not support, and the "
            "clearest answer is often the one making the boldest unsupported claim.",
            "Stopping at the first correct-looking clause. Half right answers are built "
            "for exactly that reading habit.",
            "Rejecting the right answer for being too obvious or too small, which is the "
            "single most expensive habit in Verbal.",
            "Eliminating by gut rather than by pattern. Naming the pattern out loud is "
            "what makes elimination reliable when you are tired.",
        ],
        ladder={
            1: "One clearly supported answer and four that are plainly off topic.",
            2: "One wrong answer is too strong and the rest are out of scope.",
            3: "A half right answer whose first clause matches the passage exactly.",
            4: "Two answers are supported and one answers a different question than the "
               "stem asked.",
            5: "The best wrong answer is true in the real world, uses the passage's own "
               "words, and is unsupported by the text.",
        },
    ),
]
