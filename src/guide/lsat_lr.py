"""LSAT Logical Reasoning, topic by topic.

Logical Reasoning is the LSAT, in the sense that it is most of the scored section time
and the skill the rest of the exam leans on. The arguments are shorter than the GMAT's
and considerably tighter: the gap between premise and conclusion is usually one precise
logical step, and the wrong answers are built by taking a different precise step.

Two things separate this section from every other verbal section we cover, and they are
why this is its own guide rather than a relabelled one.

First, conditional logic is explicit and load bearing. Sufficient and necessary
conditions, contrapositives, and the difference between them are tested directly and
often, and the exam expects you to handle chains of them.

Second, there are question types with no counterpart elsewhere: principle questions,
which ask you to match a rule to a case or extract a rule from one, and parallel
reasoning, which asks you to find the argument with the same STRUCTURE regardless of
subject matter.

Same IP position as the rest of the guide: logic belongs to nobody, no other author's
explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

CORE, CONDITIONAL, FAMILIES = ("Reading an Argument", "Conditional Logic",
                               "The Question Families")

TOPICS = [

    Topic(
        slug="lsat-argument-structure",
        title="Argument Parts and Structure",
        area=CORE,
        skill="lsat_lr_struct",
        idea="Every stimulus is premises, possibly an intermediate conclusion, and a main "
             "conclusion, and mistaking which is which makes every downstream question "
             "unanswerable.",
        why="The LSAT puts conclusions in the middle, attributes them to other people, "
            "and stacks one on another more often than any other exam. Finding the main "
            "conclusion reliably is the foundational skill of the section.",
        facts=[
            ("Main conclusion", "the claim everything else supports",
             "Nothing in the stimulus supports anything above it."),
            ("Intermediate conclusion", "supported by premises AND supporting the main one",
             "It sits in the middle of the chain and is the most common wrong answer on "
             "main conclusion questions."),
            ("The why test", "ask why the author believes each candidate",
             "If the answer is elsewhere in the stimulus, the candidate is not the main "
             "conclusion."),
            ("Someone else's claim", "many stimuli open with a view the author rejects",
             "Watch for: some argue, it is widely held, critics contend."),
            ("Conclusion indicators", "therefore, thus, hence, so, clearly, it follows",
             "Present often enough to help and absent often enough not to rely on."),
            ("Premise indicators", "because, since, for, given that, after all",
             "These mark support being offered."),
            ("Counterpremise indicators", "although, while, admittedly, granted",
             "These mark a concession, which is neither premise nor conclusion of the "
             "author's own case."),
        ],
        worked=[
            dict(ask="'Many people assume that longer prison sentences deter crime. But "
                     "sentence length has risen steadily in this region for two decades "
                     "while reported offences have held constant. Deterrence, then, "
                     "cannot be the main driver of sentencing policy, since policy has "
                     "continued to lengthen sentences regardless.' What is the main "
                     "conclusion?",
                 steps=[
                     "Sentence 1 is a view attributed to 'many people'. Not the author's.",
                     "Sentence 2 is evidence: sentences up, offences flat.",
                     "Sentence 3 contains 'then' and also 'since'. The part before 'since' "
                     "is the claim; the part after is its support.",
                     "Apply the why test: why does the author believe deterrence is not "
                     "the driver? Because policy lengthens sentences regardless. So the "
                     "main conclusion is that deterrence cannot be the main driver of "
                     "SENTENCING POLICY.",
                 ],
                 answer="Deterrence cannot be the main driver of sentencing policy",
                 why="Note what the conclusion is NOT: it is not that longer sentences "
                     "fail to deter. The evidence would support that, and the exam offers "
                     "it, but the author drew a narrower conclusion about what motivates "
                     "policy. Answering with the claim the evidence supports, rather than "
                     "the claim the author made, is the standard error."),
        ],
        traps=[
            "Choosing the intermediate conclusion. It has support under it, which makes it "
            "feel like a conclusion, and it also supports something else.",
            "Choosing the view the author is arguing against, usually stated first and at "
            "length.",
            "Choosing the claim the evidence would support rather than the one the author "
            "actually drew.",
            "Relying on indicator words. A stimulus can contain 'therefore' in a "
            "subordinate clause and state its real conclusion without any marker.",
        ],
        ladder={
            1: "Two premises and a clearly marked conclusion.",
            2: "No indicator word, so the why test locates it.",
            3: "The stimulus opens with an opposing view that must be set aside.",
            4: "An intermediate conclusion is present and is offered as an answer.",
            5: "The stimulus contains two authors' conclusions and the question asks for "
               "one of them specifically.",
        },
    ),

    Topic(
        slug="lsat-conditionals",
        title="Conditional Logic: Sufficient and Necessary",
        area=CONDITIONAL,
        skill="lsat_lr_struct",
        idea="If A then B says A guarantees B, and it says nothing whatever about what "
             "happens without A, which is the source of most wrong answers in the "
             "section.",
        why="Conditional reasoning is explicit on the LSAT in a way it is not on the "
            "other exams. Being fluent in it, including chains and the contrapositive, "
            "converts a family of hard questions into mechanical ones.",
        facts=[
            ("Notation", "A -> B, read as if A then B",
             "A is sufficient for B; B is necessary for A."),
            ("Sufficient", "enough to guarantee",
             "If A happens, B must. A is a trigger."),
            ("Necessary", "required, but not enough on its own",
             "Without B, A cannot happen."),
            ("The contrapositive", "A -> B gives not-B -> not-A",
             "Negate both and reverse them. Always valid, and the exam relies on it."),
            ("The two invalid moves", "not-A -> not-B, and B -> A",
             "The inverse and the converse. Both appear as answer choices constantly."),
            ("Necessary condition indicators", "only, only if, requires, must, unless, "
             "depends on",
             "The word 'only' introduces the NECESSARY condition, not the sufficient "
             "one."),
            ("Unless", "translate as if not",
             "X unless Y becomes not-Y -> X."),
            ("Chaining", "A -> B and B -> C give A -> C",
             "And the contrapositive of the chain: not-C -> not-A."),
            ("Quantifiers", "some means at least one; most means more than half",
             "Two 'most' statements about the same group must overlap."),
        ],
        worked=[
            dict(ask="'Only applicants who submitted a portfolio were interviewed.' What "
                     "follows, and what does not?",
                 steps=[
                     "'Only' introduces the necessary condition. Being interviewed "
                     "requires having submitted a portfolio.",
                     "So: interviewed -> submitted a portfolio.",
                     "Contrapositive: did not submit -> was not interviewed. Valid.",
                     "What does NOT follow: submitted -> interviewed. That is the "
                     "converse, and the sentence says nothing about portfolio submitters "
                     "who were not interviewed.",
                 ],
                 answer="Interviewed -> submitted; equivalently, not submitted -> not "
                        "interviewed",
                 why="The English word 'only' points at the necessary condition, and "
                     "everyday speech uses it loosely enough that the reversal feels "
                     "right. Translating to arrow notation before reasoning removes the "
                     "temptation entirely, which is why it is worth doing on paper."),
            dict(ask="'No proposal is funded unless it is endorsed by two reviewers. "
                     "Every endorsed proposal is logged.' If a proposal was funded, what "
                     "must be true?",
                 steps=[
                     "Unless means if not: not endorsed -> not funded. Contrapositive: "
                     "funded -> endorsed.",
                     "Second statement: endorsed -> logged.",
                     "Chain: funded -> endorsed -> logged.",
                     "So a funded proposal was logged.",
                 ],
                 answer="It was logged",
                 why="Two translations and one chain, all mechanical. The tempting wrong "
                     "answer is that a logged proposal was funded, which reverses the "
                     "chain. Once the arrows are written down, reversing one is visibly "
                     "not a step you are allowed to take."),
        ],
        traps=[
            "Reversing a conditional, which is the most frequently offered wrong answer "
            "in the section.",
            "Negating both sides without reversing, which is the inverse and equally "
            "invalid.",
            "Reading 'only' as introducing the sufficient condition. It introduces the "
            "necessary one.",
            "Treating 'some' as 'some but not all'. Some means at least one and is "
            "compatible with all.",
        ],
        ladder={
            1: "One conditional and its contrapositive.",
            2: "A translation from 'only if' or 'unless'.",
            3: "A two-link chain plus its contrapositive.",
            4: "Several conditionals where only one chain reaches the conclusion.",
            5: "Conditionals mixed with quantifiers, where a 'most' overlap is what "
               "connects two statements.",
        },
    ),

    Topic(
        slug="lsat-assumptions",
        title="Detecting Assumptions",
        area=FAMILIES,
        skill="lsat_lr_assum",
        idea="An assumption is what the argument needs and never states, and the LSAT "
             "splits this into two question types that want different strengths of "
             "answer.",
        why="Necessary and sufficient assumption questions look alike and are graded "
            "differently. Choosing by feel rather than by test is how people who "
            "understand the argument still get these wrong.",
        facts=[
            ("Necessary assumption", "the argument DEPENDS on it",
             "Stems say: depends on, requires, assumes."),
            ("Sufficient assumption", "adding it makes the conclusion FOLLOW",
             "Stems say: if assumed, allows the conclusion to be properly drawn."),
            ("The negation test", "negate a candidate; if the argument collapses it is "
             "necessary",
             "The single most reliable mechanical test in the section."),
            ("Necessary answers are weak", "some, at least one, not always",
             "A strong answer is usually more than the argument required."),
            ("Sufficient answers are strong", "often a conditional linking the gap",
             "They are allowed to do more than needed; they just have to close it."),
            ("Find the gap first", "what appears in the conclusion and not the premises",
             "A new term in the conclusion is nearly always where the assumption lives."),
            ("Bridging terms", "the assumption often links two different concepts",
             "Premise talks about cost, conclusion about value: the link is the "
             "assumption."),
        ],
        worked=[
            dict(ask="'The new alloy is lighter than steel of equivalent strength. It "
                     "will therefore reduce the fuel consumption of vehicles built with "
                     "it.' Name the gap, then give a necessary and a sufficient "
                     "assumption.",
                 steps=[
                     "Premise is about weight. Conclusion is about fuel consumption. The "
                     "gap is between those two concepts.",
                     "Necessary: vehicle weight affects fuel consumption at least to some "
                     "degree. Negate it: weight has no effect on fuel consumption. The "
                     "argument collapses, so it is necessary.",
                     "Also necessary: the alloy replaces steel in enough of the vehicle "
                     "to lower total weight.",
                     "Sufficient: any reduction in vehicle weight reduces fuel "
                     "consumption, and building with the alloy reduces vehicle weight. "
                     "Adding that makes the conclusion follow.",
                 ],
                 answer="Necessary: weight affects fuel use. Sufficient: any weight "
                        "reduction reduces fuel use, and this does reduce weight.",
                 why="Notice how much weaker the necessary answer is. 'At least to some "
                     "degree' is enough to be required and nowhere near enough to prove "
                     "the conclusion. Reading the stem to see which type is being asked "
                     "for is therefore not a formality; it changes which answer is "
                     "correct."),
        ],
        traps=[
            "Choosing a sufficient assumption on a necessary assumption question. It is "
            "usually too strong and survives negation comfortably.",
            "Skipping the negation test because an answer feels central to the argument.",
            "Choosing an answer that strengthens without being required.",
            "Supplying real-world knowledge the argument would obviously need. It needs "
            "only what closes ITS gap.",
        ],
        ladder={
            1: "A one-term gap and an answer that names it directly.",
            2: "Two candidates are relevant and negation separates them.",
            3: "The assumption rules out an alternative explanation.",
            4: "The stem asks for a sufficient assumption and the answer is a conditional.",
            5: "The gap is between two abstractions and the bridging answer is phrased in "
               "terms neither the premise nor the conclusion used.",
        },
    ),

    Topic(
        slug="lsat-flaws",
        title="Identifying Flaws in Arguments",
        area=FAMILIES,
        skill="lsat_lr_flaw",
        idea="The argument is already broken and the answer names the break in abstract "
             "terms, so the skill is matching a concrete error to a general description.",
        why="Flaw answers are written in formal language that is harder to read than the "
            "argument. Knowing the recurring flaws by name means you recognise the "
            "description rather than decoding it under time.",
        facts=[
            ("Confusing necessary and sufficient", "treats a requirement as a guarantee",
             "The most common flaw on this exam, and it is often phrased abstractly."),
            ("Correlation taken as causation", "two things co-occur, so one causes",
             "With the usual branches: reverse cause, third cause, coincidence."),
            ("Unrepresentative sample", "generalises from an atypical group",
             "Watch for volunteers, respondents, and anyone who opted in."),
            ("Equivocation", "one term used in two senses",
             "The argument needs one meaning in the premise and another in the "
             "conclusion."),
            ("Ad hominem", "attacks the arguer instead of the argument",
             "A motive to be wrong is not evidence of being wrong."),
            ("Circular reasoning", "assumes what it sets out to prove",
             "The conclusion restates a premise in different words."),
            ("Part and whole", "true of the parts, so true of the whole",
             "Or the reverse, which is equally invalid."),
            ("Absence of evidence", "not proven, therefore false",
             "An untested claim is untested."),
            ("Percent and number", "a share moved, so a count moved",
             "Appears in formal dress as 'confuses a proportion with an absolute "
             "quantity'."),
        ],
        worked=[
            dict(ask="'Anyone who has mastered the technique can complete the assembly in "
                     "under an hour. Yolanda completed it in fifty minutes, so she has "
                     "mastered the technique.' Name the flaw.",
                 steps=[
                     "Translate: mastered -> under an hour. That is the premise.",
                     "The argument observes: under an hour. And concludes: mastered.",
                     "That is the converse of the stated conditional.",
                     "In flaw-answer language: it treats a necessary condition as though "
                     "it were sufficient. Completing it quickly is required of masters, "
                     "not proof of mastery.",
                 ],
                 answer="It confuses a necessary condition with a sufficient one",
                 why="The abstract phrasing is what makes these hard, not the logic. "
                     "Translating the stimulus into arrows first, and only then reading "
                     "the answers, means you are matching a known shape rather than "
                     "parsing formal language cold."),
        ],
        traps=[
            "Choosing a flaw the argument did not commit, described in impressive "
            "terminology.",
            "Naming a real but secondary flaw when the conclusion rests on a different "
            "one.",
            "Objecting to the conclusion's truth rather than to the reasoning.",
            "Reading the answer choices before understanding the argument, which lets "
            "their vocabulary suggest flaws that are not there.",
        ],
        ladder={
            1: "A bare causal leap with the answer naming it plainly.",
            2: "A conditional is reversed and the answer describes it abstractly.",
            3: "A sampling flaw signalled by one word about how the group formed.",
            4: "Several flaws are present and the answer names the load-bearing one.",
            5: "The flaw is an equivocation or a part-and-whole error, described in terms "
               "that do not reuse the stimulus's vocabulary.",
        },
    ),

    Topic(
        slug="lsat-additional-evidence",
        title="The Effect of Additional Evidence",
        area=FAMILIES,
        skill="lsat_lr_evid",
        idea="Strengthen, weaken, and evaluate all ask the same question from different "
             "angles: what does this new fact do to the gap between the premises and the "
             "conclusion.",
        why="This is the largest question family in the section. Treating the three types "
            "as one skill, applied in different directions, is what makes them fast.",
        facts=[
            ("Weaken", "make the conclusion less likely, not false",
             "You are damaging the link, never disputing a premise."),
            ("Strengthen", "make it more likely, usually by ruling out an alternative",
             "More of the same evidence rarely helps."),
            ("Evaluate", "find the question whose two answers pull opposite ways",
             "The variance test: answer it yes, then no, and see if the argument moves."),
            ("Premises are granted", "an answer disputing one is out of bounds",
             "However reasonable it sounds."),
            ("Causal arguments", "attack or defend by alternative cause",
             "The standard move in both directions."),
            ("Sample arguments", "attack or defend by representativeness",
             "Show the group studied is or is not typical."),
            ("Plan arguments", "attack by showing the mechanism fails",
             "Cost and difficulty are objections only if the argument weighed them."),
            ("Degree matters", "the question asks which MOST strengthens or weakens",
             "Several answers may help; you are ranking, not filtering."),
        ],
        worked=[
            dict(ask="'Residents of the district who use the new cycle lanes report fewer "
                     "sick days than those who do not. The lanes are therefore improving "
                     "residents' health.' Which most weakens?",
                 steps=[
                     "Conclusion: the lanes improve health. Evidence: users report fewer "
                     "sick days.",
                     "Gap: the lanes are causing the difference, rather than the "
                     "difference pre-existing.",
                     "Strongest attack: self-selection. Residents already healthy enough "
                     "to cycle regularly chose to use the lanes.",
                     "Weaker attacks: the lanes cost money, some residents dislike them, "
                     "sick days are self-reported. The last is closest but still concedes "
                     "a real difference.",
                 ],
                 answer="Evidence that lane users were already healthier before the lanes "
                        "opened",
                 why="The self-selection answer does not dispute the sick-day figures at "
                     "all. It accepts them and removes their meaning, which is strictly "
                     "stronger than arguing with the data and is why it outranks the "
                     "self-reporting objection."),
        ],
        traps=[
            "Attacking a premise, which is always available among the answers and always "
            "wrong.",
            "Choosing a merely negative fact about the subject rather than damage to the "
            "reasoning.",
            "Stopping at the first answer that helps on a question asking which helps "
            "most.",
            "On evaluate questions, testing only one direction. An option must move the "
            "argument both ways.",
        ],
        ladder={
            1: "A direct causal claim and an obvious alternative cause.",
            2: "Two answers are negative and only one touches the reasoning.",
            3: "The attack works through the sample rather than the cause.",
            4: "The conclusion is a recommendation and the answer must break the "
               "mechanism.",
            5: "An evaluate question where several options look relevant and only one "
               "varies the argument in both directions.",
        },
    ),

    Topic(
        slug="lsat-conclusions",
        title="Drawing Well-Supported Conclusions",
        area=FAMILIES,
        skill="lsat_lr_concl",
        idea="You are given facts and asked what they guarantee, so there is no argument "
             "to attack and no gap to find, only what follows.",
        why="These are constructive rather than critical, and people bring critical habits "
            "to them and start hunting for flaws in a stimulus that is making no "
            "argument. Recognising the type is half the work.",
        facts=[
            ("Must be true", "guaranteed by the statements",
             "Not merely consistent with them, which describes most wrong answers."),
            ("Most strongly supported", "a slightly lower bar",
             "Still supported by the text, never by plausibility."),
            ("Combine, do not extend", "joining two given facts is allowed",
             "Adding a third from your own knowledge is not."),
            ("Conditionals chain", "A -> B and B -> C give A -> C",
             "And the contrapositive of the whole chain."),
            ("Quantifier overlap", "most X are Y and most X are Z guarantees an overlap",
             "Two majorities of the same group must share a member."),
            ("Some is symmetric", "some X are Y means some Y are X",
             "Unlike conditionals, this one does reverse."),
            ("Watch for the empty set", "all X are Y does not say any X exists",
             "Higher difficulty questions turn on exactly this."),
        ],
        worked=[
            dict(ask="'Every registered surveyor in the county holds a provincial "
                     "licence. Most provincial licence holders in the county also hold a "
                     "federal certificate. Most provincial licence holders in the county "
                     "work in forestry.' What must be true?",
                 steps=[
                     "Two 'most' statements about the same group: provincial licence "
                     "holders in the county.",
                     "Two majorities of one group must overlap, so at least one person "
                     "holds a federal certificate AND works in forestry.",
                     "What does NOT follow: anything about registered surveyors "
                     "specifically. They are a subset of licence holders, and a majority "
                     "of the whole says nothing about any particular subset.",
                     "Also not guaranteed: that any registered surveyor exists at all.",
                 ],
                 answer="At least one provincial licence holder in the county both holds "
                        "a federal certificate and works in forestry",
                 why="The overlap rule is the only inference the two 'most' statements "
                     "license, and it is about the group they were both about. Every "
                     "wrong answer here will apply one of those majorities to the "
                     "surveyors, which is the subset the first sentence introduced "
                     "precisely to tempt you."),
        ],
        traps=[
            "Choosing an answer that is merely possible rather than guaranteed.",
            "Applying a statement about a group to one of its subsets.",
            "Reversing a conditional, which never reverses, while forgetting that 'some' "
            "does.",
            "Assuming a category has members when the statements never said so.",
        ],
        ladder={
            1: "Two facts combining in one step.",
            2: "A conditional and its contrapositive.",
            3: "A quantifier question turning on some against most.",
            4: "Two majorities of one group, where the overlap is the only valid "
               "inference.",
            5: "A subset is introduced and every wrong answer applies a whole-group claim "
               "to it.",
        },
    ),

    Topic(
        slug="lsat-principles",
        title="Principles, Rules and Analogy",
        area=FAMILIES,
        skill="lsat_lr_prin",
        idea="A principle is a general rule, and these questions either apply one to a "
             "case or extract one from a case, so the direction of travel is what the "
             "stem tells you.",
        why="Principle questions have no counterpart on the other exams and they are "
            "mechanically tractable: a principle is usually a conditional, and applying "
            "it is the same work as any other conditional question.",
        facts=[
            ("A principle is a conditional", "if these conditions hold, this follows",
             "Translating it into an arrow makes applying it mechanical."),
            ("Apply the principle", "the stem gives the rule, the answer is the case",
             "The case must satisfy the rule's trigger exactly."),
            ("Identify the principle", "the stem gives the case, the answer is the rule",
             "The rule must cover this case and not overreach it."),
            ("Match the scope", "the rule must not be broader than the case needs",
             "A rule covering far more than the case is a common wrong answer."),
            ("Every condition must be met", "a partially satisfied trigger fires nothing",
             "If the rule needs two conditions, the case must have both."),
            ("Justify versus conform", "does the principle require it, or merely allow it",
             "Stems distinguish these and the answers differ accordingly."),
            ("Watch for the ought", "principles are often normative",
             "Should, ought, is justified in. The conclusion carries the same modality."),
        ],
        worked=[
            dict(ask="Principle: 'A public body should release a document only if "
                     "releasing it serves the public interest and no individual named in "
                     "it would face a specific risk of harm.' A body is deciding about a "
                     "report that serves the public interest and names an informant who "
                     "would face threats if identified. What follows?",
                 steps=[
                     "Translate: release -> (serves public interest AND no named "
                     "individual at specific risk). 'Only if' marks the necessary "
                     "conditions.",
                     "The case: public interest is served. But a named individual would "
                     "face a specific risk.",
                     "One of the two necessary conditions fails.",
                     "Contrapositive: if either condition fails, the body should not "
                     "release it.",
                 ],
                 answer="The body should not release the document",
                 why="'Only if' introduced necessary conditions, so satisfying one of two "
                     "gets you nothing. The tempting wrong answer says the public "
                     "interest justifies release, which treats a necessary condition as "
                     "sufficient: the same flaw as the whole conditional family, dressed "
                     "as an ethics question."),
        ],
        traps=[
            "Applying a principle whose trigger is only partly satisfied.",
            "Choosing a principle broader than the case requires, which would decide "
            "cases the stimulus never raised.",
            "Missing the direction: applying when the stem asked you to identify, or the "
            "reverse.",
            "Dropping the normative force, so a principle saying a body 'should not' "
            "yields a conclusion that it 'cannot'.",
        ],
        ladder={
            1: "A one-condition principle applied to a case that plainly meets it.",
            2: "The principle must be extracted from a described case.",
            3: "A two-condition principle where one condition fails.",
            4: "Two candidate principles both fit and one is broader than the case.",
            5: "The principle is normative and the answer must preserve exactly its "
               "modality and scope.",
        },
    ),

    Topic(
        slug="lsat-explanations-parallel",
        title="Explanations and Parallel Reasoning",
        area=FAMILIES,
        skill="lsat_lr_expl",
        idea="Explanation questions reconcile two facts that seem to conflict; parallel "
             "reasoning questions ask which argument has the same shape, regardless of "
             "what it is about.",
        why="Parallel reasoning is the most time-expensive question type in the section "
            "and the most mechanical once you abstract the structure. Working from the "
            "shape rather than the subject is the whole technique.",
        facts=[
            ("Explain the discrepancy", "both facts are true, find the circumstance",
             "Nothing is being argued; you are reconciling, not adjudicating."),
            ("State the conflict precisely", "before reading any answer",
             "Vague conflicts produce vague answer selection."),
            ("The answer explains both", "an answer covering one side leaves the puzzle",
             "This is what eliminates most choices."),
            ("Parallel reasoning", "match the STRUCTURE, ignore the subject",
             "An argument about birds can parallel one about tax policy."),
            ("Abstract before comparing", "write the shape in letters",
             "All A are B; this is A; therefore this is B."),
            ("Match the conclusion type first", "conditional, causal, comparative, "
             "recommendation",
             "This usually eliminates three answers in one pass."),
            ("Match validity", "a flawed argument parallels a flawed one",
             "Parallel flaw questions require the SAME flaw, not merely any flaw."),
            ("Do not match topic", "similar subject matter is bait",
             "The exam reliably offers one answer about the stimulus's own subject."),
        ],
        worked=[
            dict(ask="'Every technician who handles the reagent wears a respirator. Petra "
                     "wears a respirator, so Petra handles the reagent.' Which has the "
                     "same structure: (A) Every bird in the aviary is banded; this bird "
                     "is banded, so it is in the aviary. (B) Every bird in the aviary is "
                     "banded; this bird is in the aviary, so it is banded. (C) Every "
                     "technician wears a respirator; Petra is a technician, so she wears "
                     "one.",
                 steps=[
                     "Abstract the stimulus: All A are B. X is B. Therefore X is A. That "
                     "is the converse, and it is invalid.",
                     "(A): All A are B. X is B. Therefore X is A. Same shape, same "
                     "invalidity.",
                     "(B): All A are B. X is A. Therefore X is B. Valid, so it does not "
                     "match.",
                     "(C): same valid shape as (B), and it is about the stimulus's own "
                     "subject, which is the bait.",
                 ],
                 answer="(A)",
                 why="(C) shares the topic and not the structure; (A) shares the "
                     "structure and not the topic. That pairing is deliberate on nearly "
                     "every parallel question. Abstracting into letters before looking at "
                     "the answers makes the topic irrelevant, which is exactly what you "
                     "want it to be."),
        ],
        traps=[
            "Matching subject matter instead of structure. There is almost always an "
            "answer about the stimulus's own topic and it is almost always wrong.",
            "On a parallel flaw question, choosing an argument that is flawed in a "
            "different way.",
            "Matching a valid argument to an invalid one, or the reverse.",
            "On explanation questions, choosing an answer that accounts for only one of "
            "the two facts.",
        ],
        ladder={
            1: "A plain discrepancy with one answer that reconciles it.",
            2: "A parallel question where matching the conclusion type settles it.",
            3: "The explanation turns on a changed base or a different population.",
            4: "A parallel flaw question requiring the same specific error.",
            5: "Two answers share the structure and differ in whether the reasoning is "
               "valid, or in the strength of the conclusion drawn.",
        },
    ),
]
