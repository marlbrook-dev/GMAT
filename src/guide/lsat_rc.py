"""LSAT Reading Comprehension, topic by topic.

Four passage sets per section, one of which is Comparative Reading: two shorter
passages by different authors, asked about together. That format is unique to this exam
among the ones we cover and it is why a whole topic here is about relating two texts.

LSAT passages are longer and denser than the GMAT's and far longer than the digital
SAT's, where every question carries its own paragraph. The consequence is that the
reading strategy genuinely differs: here there IS something to map and come back to,
and the map is what makes the questions cheap.

The section also rewards a particular discipline. LSAT answer choices are written to be
defensible on a loose reading and wrong on a close one, more so than on any other exam,
so the margin between the credited answer and the best wrong one is often a single
qualifier.

Same IP position as the rest of the guide: reading and reasoning belong to nobody, no
other author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

METHOD, QUESTIONS = "Reading the Passage", "The Question Types"

TOPICS = [

    Topic(
        slug="lsat-rc-main-idea",
        title="Main Idea and Primary Purpose",
        area=QUESTIONS,
        skill="lsat_rc_main",
        idea="The main point has to cover every paragraph and overstate none of them, "
             "which is a stricter test than it sounds when the passage spends three "
             "paragraphs on a view the author rejects.",
        why="Nearly every passage set opens with one of these, and the structural read "
            "answers it directly. It is also the question most often lost by choosing an "
            "answer that describes the passage's subject rather than its claim.",
        facts=[
            ("Main point", "the claim the whole passage exists to make",
             "Not the topic, and not the most interesting thing said."),
            ("Primary purpose", "the author's job, stated as a verb",
             "To argue, to describe, to reconcile, to qualify, to challenge."),
            ("The coverage test", "does the answer account for every paragraph",
             "An answer describing two of four paragraphs is describing a part."),
            ("The scope test", "as broad as the passage, no broader",
             "Too narrow describes a section; too broad describes the field."),
            ("Verb strength", "match how hard the author pushed",
             "A passage that raises a possibility cannot have a main point that "
             "establishes it."),
            ("Whose view", "the passage may spend most of its length on someone else's",
             "Length is not endorsement, and the author's own position may occupy two "
             "sentences."),
        ],
        worked=[
            dict(ask="A passage devotes three paragraphs to a widely held account of why "
                     "a legal doctrine emerged, then a final paragraph arguing the "
                     "account cannot explain two early cases and proposing that the "
                     "doctrine arose from procedural convenience instead. Which is the "
                     "main point?",
                 steps=[
                     "Identify whose view each paragraph carries. Paragraphs 1 to 3: the "
                     "widely held account, reported not endorsed.",
                     "Paragraph 4: the author's objection and their alternative.",
                     "Coverage: the answer must account for the exposition AND the "
                     "objection, so 'the doctrine arose from procedural convenience' "
                     "alone is too narrow.",
                     "The main point is that the accepted account fails to explain "
                     "certain early cases, and a procedural explanation fits better.",
                 ],
                 answer="The accepted account is inadequate and a procedural explanation "
                        "fits the early cases better",
                 why="Three quarters of the passage is the view being rejected, and an "
                     "answer summarising that view will be offered and will feel "
                     "well-supported because so much text backs it. Length is the trap "
                     "here: the author's position is one paragraph and it is still the "
                     "main point."),
        ],
        traps=[
            "Choosing the answer that describes the view the passage spends most of its "
            "length on, when the author rejects it.",
            "Choosing the author's alternative alone, dropping the critique that occupied "
            "most of the passage.",
            "Choosing an answer that states the topic rather than a claim about it.",
            "Matching content correctly and getting the verb wrong, which is what "
            "separates two otherwise identical answers.",
        ],
        ladder={
            1: "A short passage with one argument and the main point near the end.",
            2: "The correct answer paraphrases rather than restates.",
            3: "One wrong answer covers only part of the passage and is otherwise "
               "accurate.",
            4: "Most of the passage carries a view the author does not hold.",
            5: "Two answers both cover the passage and differ only in the strength of "
               "their verb or the breadth of their scope.",
        },
    ),

    Topic(
        slug="lsat-rc-stated",
        title="Explicitly Stated Information",
        area=QUESTIONS,
        skill="lsat_rc_stated",
        idea="The answer is written in the passage, and the discipline is refusing to go "
             "one word beyond what is there.",
        why="These should be the cheapest questions in the section and they are lost "
            "constantly, because the credited answer paraphrases heavily while a wrong "
            "answer reuses the passage's own words to say something else.",
        facts=[
            ("The stem", "according to the passage, the author states that",
             "The support has to be findable, not merely reasonable."),
            ("Use the map", "go to the paragraph whose job matches the question",
             "Then read the sentences around it rather than searching the whole passage."),
            ("The proof standard", "you should be able to underline it",
             "If you are reasoning rather than locating, you have drifted into "
             "inference."),
            ("Paraphrase is the norm", "the credited answer rarely reuses the wording",
             "Heavy word overlap is more often bait than answer."),
            ("EXCEPT questions", "four are supported, find the one that is not",
             "The job inverts: you are checking four rather than finding one."),
            ("Watch the qualifier", "some, certain, in some cases, primarily",
             "An answer that drops a qualifier is no longer what the passage stated."),
        ],
        worked=[
            dict(ask="The passage states: 'Although the guild's charter permitted members "
                     "to train apprentices, surviving records show that in the first "
                     "decade only master weavers did so.' Which is supported: (A) the "
                     "charter restricted apprentice training to master weavers, (B) in "
                     "the charter's first decade, apprentice training was in practice "
                     "carried out only by master weavers, (C) non-master members were "
                     "prohibited from training apprentices?",
                 steps=[
                     "Locate it. The sentence is quoted, so the work is comparison.",
                     "(A) says the CHARTER restricted it. The passage says the charter "
                     "PERMITTED members generally, and practice differed. Reversed.",
                     "(C) says prohibited. The passage says only masters did so, which is "
                     "a fact about behaviour, not about permission.",
                     "(B) restates the second clause with the qualifier 'in practice' "
                     "preserved.",
                 ],
                 answer="(B)",
                 why="The whole sentence turns on 'although': the rule allowed one thing "
                     "and practice was another. Both wrong answers collapse that "
                     "distinction, in opposite directions. On stated-information "
                     "questions the concession word is usually doing the work."),
        ],
        traps=[
            "Answering from memory of the passage rather than from the passage, which is "
            "on screen.",
            "Choosing the answer with the most word overlap. That is the cheapest trap to "
            "build and it works on a hurried reader.",
            "Completing the thought, so a fact about what happened becomes a claim about "
            "what was permitted.",
            "Missing an EXCEPT, which inverts the task and lets you confirm a supported "
            "answer four times without noticing.",
        ],
        ladder={
            1: "One paragraph and the answer restates a single sentence.",
            2: "The credited answer paraphrases and a decoy reuses the passage's words.",
            3: "Two answers are in the passage and only one answers the question asked.",
            4: "The support is split across two sentences, so a half match is incomplete.",
            5: "An EXCEPT question whose four supported answers are spread across the "
               "whole passage.",
        },
    ),

    Topic(
        slug="lsat-rc-inference",
        title="Inference and Implication",
        area=QUESTIONS,
        skill="lsat_rc_inf",
        idea="An inference must be true given the passage, which is a far smaller set "
             "than what the passage makes likely.",
        why="This is where the LSAT's precision bites hardest. The credited answer is "
            "often almost a restatement, and the best wrong answer is something any "
            "reasonable person would conclude and the passage does not guarantee.",
        facts=[
            ("The stems", "the passage suggests, implies, it can be inferred, most "
             "likely agrees",
             "All ask what is guaranteed by what is written."),
            ("The standard", "must be true, not could be true",
             "If you can describe a situation consistent with the passage where the "
             "answer is false, it is wrong."),
            ("Where inferences live", "hedges, comparatives, negations, concessions",
             "Only, not all, more than, failed to, although. These carry logical content."),
            ("Small steps win", "the credited answer is usually unspectacular",
             "A striking inference is almost always the wrong one."),
            ("Combining is allowed", "two stated facts may be joined",
             "Adding a third from your own knowledge is not."),
            ("Author agreement questions", "what would the author endorse",
             "Anchored to the author's own stated commitments, not to the views they "
             "report."),
            ("The negation check", "assume the answer is false; does the passage break",
             "If the passage survives, the answer was never guaranteed."),
        ],
        worked=[
            dict(ask="The passage says: 'No account of the migration that relies solely "
                     "on climatic data can explain the timing of the eastern "
                     "settlements.' Which must be true: (A) climatic data is irrelevant "
                     "to the migration, (B) any successful account of the eastern "
                     "settlements' timing draws on something besides climatic data, "
                     "(C) the eastern settlements were founded later than the western "
                     "ones?",
                 steps=[
                     "Translate: relies solely on climate -> cannot explain eastern "
                     "timing.",
                     "Contrapositive: explains eastern timing -> does not rely solely on "
                     "climate. That is (B).",
                     "(A) turns 'not sufficient alone' into 'irrelevant', which is a much "
                     "stronger claim the sentence does not make.",
                     "(C) is about relative dates, which the sentence never addresses.",
                 ],
                 answer="(B)",
                 why="The sentence is a conditional in ordinary prose, and the credited "
                     "answer is its contrapositive. That is the most common construction "
                     "in LSAT reading inference, which is why the conditional work from "
                     "Logical Reasoning pays here too. (A) is the trap for anyone reading "
                     "'solely' as 'at all'."),
        ],
        traps=[
            "Choosing the most plausible real-world statement rather than the guaranteed "
            "one.",
            "Strengthening a qualifier: 'not sufficient on its own' becoming 'irrelevant', "
            "or 'suggests' becoming 'shows'.",
            "Attributing a reported view to the author on an author-agreement question.",
            "Rejecting the credited answer for being too obvious. Must be true means it "
            "should look obvious once found.",
        ],
        ladder={
            1: "One sentence with a clear logical word and an answer that restates it.",
            2: "The inference joins two adjacent sentences.",
            3: "A conditional in prose whose contrapositive is the credited answer.",
            4: "A quantifier where the everyday reading and the logical one differ.",
            5: "The inference rests on a hedge about the limits of the evidence, and "
               "every wrong answer treats the hedge as a positive claim.",
        },
    ),

    Topic(
        slug="lsat-rc-structure",
        title="Meaning, Structure and Tone",
        area=QUESTIONS,
        skill="lsat_rc_struct",
        idea="These ask what a word means here, what a sentence is doing, or how the "
             "author feels, and all three are answered from the surrounding text rather "
             "than from the cited line.",
        why="Function and tone questions are pure structural reading, so they are nearly "
            "free with a map and expensive without one. They are also where the "
            "measured-academic-register rule pays: the tone is almost never strong.",
        facts=[
            ("Function stems", "the author mentions X primarily in order to",
             "The answer is a job: to illustrate, to concede, to rebut, to qualify."),
            ("Read around, not at", "a line's function is set by its neighbours",
             "The cited line is the one place the answer is not."),
            ("Meaning in context", "the word may not carry its usual sense",
             "Substitute your own word first, then match."),
            ("Tone lives in modifiers", "adjectives, adverbs and hedges",
             "Surprisingly, merely, only, has yet to establish."),
            ("The usual tone", "qualified approval or measured scepticism",
             "Contempt, outrage and indifference are almost never credited."),
            ("Two objects, two attitudes", "a finding and its evidence can be judged "
             "differently",
             "An author may find a result important and its support weak."),
            ("Match the intensity", "direction is half the answer",
             "Getting positive versus negative right and then choosing the extreme "
             "version is the common loss."),
        ],
        worked=[
            dict(ask="After arguing that early cartographers systematically exaggerated "
                     "coastlines, the passage says: 'One 1587 chart, whose surveyor's "
                     "notes survive in full, records soundings that its engraved version "
                     "silently doubles.' Why is the chart mentioned?",
                 steps=[
                     "Ask what it is doing, not what it says.",
                     "The sentence before it is the general claim about systematic "
                     "exaggeration.",
                     "A specific documented case following a general claim is evidence "
                     "for it.",
                     "The clause about surviving notes explains why THIS chart: it is "
                     "unusually good evidence, because both versions can be compared.",
                 ],
                 answer="To provide documented evidence for the claim that early charts "
                        "exaggerated",
                 why="The wrong answer will be a faithful summary, something like 'to "
                     "describe a discrepancy in a sixteenth century chart'. That is what "
                     "the sentence says. The question asked what it is for, and on the "
                     "LSAT the summary answer is offered on essentially every function "
                     "question."),
        ],
        traps=[
            "Answering a function question with a summary of the cited line.",
            "Attaching an example to the wrong claim, usually the nearer one in memory.",
            "Treating a concession as the author's own position.",
            "Choosing the extreme version of the correct tone direction.",
        ],
        ladder={
            1: "A signposted example directly after the claim it supports.",
            2: "The question asks the function of a whole paragraph.",
            3: "The detail serves a concession rather than the main argument.",
            4: "A tone question where praise and reservation both appear and both must "
               "be held.",
            5: "The cited line supports a view the author later rejects, so its function "
               "is to set up a rebuttal.",
        },
    ),

    Topic(
        slug="lsat-rc-application",
        title="Application and Comparative Reading",
        area=QUESTIONS,
        skill="lsat_rc_app",
        idea="Application questions take the passage's principle to a new case, and "
             "comparative reading asks how two authors relate, which is the format unique "
             "to this exam.",
        why="These are the hardest questions in the section. Application requires "
            "extracting a rule the passage never states as a rule, and comparative "
            "reading requires holding two positions precisely enough to locate a narrow "
            "disagreement.",
        facts=[
            ("Application stems", "which of the following is most analogous",
             "Or: the author would most likely agree that, applied to a new case."),
            ("Extract the principle first", "state the rule in your own words",
             "Then test each answer against the rule, not against the passage's subject."),
            ("Ignore the subject matter", "an analogy about law can match one about "
             "farming",
             "The exam reliably offers an answer sharing the passage's topic and not its "
             "structure."),
            ("Comparative reading", "two shorter passages, different authors",
             "One set of questions asked about both."),
            ("Find the agreement first", "it is usually larger than the disagreement",
             "Naming what both accept is the fastest route to what they do not."),
            ("The point of contact", "they rarely disagree about everything",
             "Usually they share the evidence and differ on interpretation or weight."),
            ("Agreement is a possible answer", "passage B may support or extend A",
             "Do not assume conflict because two texts were given."),
            ("Whose view is asked", "the stem names an author",
             "Answering from the wrong one is the most common error in the format."),
        ],
        worked=[
            dict(ask="Passage A argues a city's decline in street crime followed its "
                     "expanded lighting programme. Passage B reports that crime fell by "
                     "comparable amounts over the same years in four cities that changed "
                     "no lighting. How does B relate to A?",
                 steps=[
                     "A's claim: the lighting produced the decline.",
                     "B's evidence: comparable declines without any lighting change.",
                     "What they AGREE on: crime declined. B does not dispute the figures.",
                     "Point of contact: whether the lighting explains it. B supplies a "
                     "control that points to a cause common to all five cities.",
                 ],
                 answer="B challenges A's causal explanation without disputing A's data",
                 why="An answer saying B contradicts A's crime figures will be offered and "
                     "is wrong: both authors accept the decline. Locating the agreement "
                     "first is what makes the disagreement precise, and precision is what "
                     "these answers are graded on."),
        ],
        traps=[
            "On comparative reading, answering from the wrong author's position.",
            "Assuming the two passages disagree when one supports or extends the other.",
            "On application questions, matching subject matter instead of the underlying "
            "principle.",
            "Overstating a disagreement as flat contradiction when the text supports only "
            "a qualification.",
        ],
        ladder={
            1: "The two passages plainly agree or plainly disagree.",
            2: "An application question where the principle is stated almost outright.",
            3: "The disagreement concerns interpretation of shared evidence.",
            4: "The principle must be extracted from an argument that never states it as "
               "a rule.",
            5: "The stem asks how one author would respond to a specific detail in the "
               "other, rather than to the passage as a whole.",
        },
    ),
]
