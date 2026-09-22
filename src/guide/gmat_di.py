"""GMAT Data Insights, topic by topic.

Data Insights is the section that did not exist before the Focus Edition, which means
it is the section people have the least idea how to study and the one where a guide
earns the most. It is also the only section with an on-screen calculator, and knowing
when not to reach for it is a real skill.

Five question types sit in here and they test one thing between them: whether you can
get a decision out of data without computing everything the data would let you
compute. Almost every trap in the section is an invitation to calculate something you
did not need.

The IP position matches the rest of the guide. Arithmetic and the logic of sufficiency
belong to nobody, no other author's explanations are in here, and every exam figure
comes from data/exams.json with its source attached.
"""
from .model import Topic

DS, GT, MSR_TPA, NUM = ("Data Sufficiency", "Tables and Graphics",
                        "Multi-Source and Two-Part", "The Numeracy Underneath")

TOPICS = [

    Topic(
        slug="ds-format",
        title="Data Sufficiency: The Five Answers",
        area=DS,
        skill="di_ds",
        idea="You are not asked to answer the question, only to decide whether the "
             "statements would let you answer it, and those are different tasks with "
             "different amounts of work.",
        why="Data Sufficiency is the question type most often lost to habit: people solve "
            "it, which takes three times as long and produces the wrong answer whenever "
            "sufficiency and solvability come apart.",
        facts=[
            ("The five answers", "A: 1 alone. B: 2 alone. C: both together. D: either "
             "alone. E: not even together",
             "They are the same five on every question, in the same order, so they are "
             "worth knowing cold rather than rereading."),
            ("A and B are exclusive", "if statement 1 works alone, the answer is A or D",
             "Never C. C means neither alone is enough and together they are."),
            ("D is the easy one to miss", "both work independently",
             "People find statement 1 sufficient, feel finished, and pick A without "
             "testing statement 2."),
            ("C is not a compromise", "together means neither alone was enough",
             "Choosing C because you are unsure is the most expensive habit in the "
             "question type: it is a specific claim, not a hedge."),
            ("Sufficient means one answer", "exactly one value, or a definite yes or no",
             "Two possible values is insufficient even if both are plausible and even if "
             "one is obviously intended."),
            ("You never need the value", "only whether it is pinned down",
             "Recognising that a linear equation in one unknown has one solution is "
             "sufficient; solving it is wasted time."),
        ],
        worked=[
            dict(ask="What is the value of x? (1) 3x + 7 = 22. (2) x is the only even "
                     "prime.",
                 steps=[
                     "Statement 1: a linear equation with one unknown and a nonzero "
                     "coefficient has exactly one solution. Sufficient. Do not solve it.",
                     "So the answer is A or D. Now test statement 2 independently, "
                     "forgetting statement 1 entirely.",
                     "Statement 2: the only even prime is 2, so x = 2. Sufficient.",
                     "Both sufficient alone.",
                 ],
                 answer="D",
                 why="Statement 1 never needed solving: the structure of the equation "
                     "settles sufficiency. Statement 2 contradicts statement 1 on the "
                     "value, which cannot happen on a real GMAT item and is here to make "
                     "the point that you are not reconciling them. You test each alone."),
            dict(ask="Is n greater than 10? (1) n squared is greater than 100. (2) n is "
                     "a positive integer less than 12.",
                 steps=[
                     "This is a yes/no question, so sufficient means always yes or always "
                     "no.",
                     "Statement 1: n squared > 100 means n > 10 OR n < -10. If n = 11, "
                     "yes. If n = -11, no. Two different answers, so insufficient.",
                     "Statement 2 alone: n could be 3 (no) or 11 (yes). Insufficient.",
                     "Together: n is a positive integer under 12, and from statement 1 "
                     "n > 10 or n < -10. Positive rules out the negative branch, so "
                     "n = 11. Always yes. Sufficient together.",
                 ],
                 answer="C",
                 why="Statement 1's negative branch is the entire question. Squaring "
                     "destroys sign information, so any statement involving a square "
                     "should prompt you to check the negative case before anything else."),
        ],
        traps=[
            "Solving instead of deciding. Sufficiency is usually visible from the "
            "structure, and the arithmetic is the part the clock takes.",
            "Letting statement 1 colour your reading of statement 2. Each must be tested "
            "as if the other did not exist, which is harder than it sounds once you have "
            "read both.",
            "Choosing C as a hedge. C is the claim that neither statement alone was "
            "enough, which is a strong claim and often false.",
            "Forgetting negatives, zero and fractions. A statement that pins down a "
            "positive integer may leave a negative or a fraction wide open.",
        ],
        ladder={
            1: "One statement is plainly sufficient and the other plainly is not.",
            2: "Both statements are sufficient alone, so the answer is D and the trap is "
               "stopping at A.",
            3: "A statement looks sufficient until the negative case is checked.",
            4: "Neither statement alone works and the combination pins the value down, "
               "with a tempting reading that makes one alone look enough.",
            5: "Both together still leave two possible values, so the answer is E, and "
               "the combination looks convincing until it is tested with a second case.",
        },
    ),

    Topic(
        slug="ds-method",
        title="Working a Data Sufficiency Question",
        area=DS,
        skill="di_ds",
        idea="There is a fixed order of operations that makes these fast: understand the "
             "question, test statement one alone, test statement two alone, and only "
             "then consider them together.",
        why="Most Data Sufficiency errors are procedural rather than mathematical. People "
            "know the maths and lose the question by contaminating one statement with "
            "the other, or by answering a question they rewrote in their head.",
        facts=[
            ("Step 1", "rephrase the question into what would settle it",
             "Is x positive becomes: do I know the sign of x. That is usually a much "
             "smaller thing to establish than x itself."),
            ("Step 2", "statement 1 alone, covering statement 2",
             "Physically ignore the other statement. Contamination is the single most "
             "common procedural error here."),
            ("Step 3", "statement 2 alone, forgetting statement 1 entirely",
             "Hardest step, because you now know something you are required to unknow."),
            ("Step 4", "only if both failed, combine",
             "If either was sufficient alone, combining is wasted work and cannot change "
             "the answer."),
            ("Testing by cases", "find two cases that give different answers",
             "To prove insufficiency you need exactly two examples that disagree. That is "
             "faster than any general argument."),
            ("Cases worth trying", "0, 1, a negative, a fraction, a large number",
             "These five break most statements that look sufficient, and they break them "
             "quickly."),
        ],
        worked=[
            dict(ask="Is xy greater than 0? (1) x + y is greater than 0. (2) x - y is "
                     "greater than 0.",
                 steps=[
                     "Rephrase: xy > 0 asks whether x and y have the SAME sign. That is "
                     "the whole question.",
                     "Statement 1 alone: x = 3, y = 1 gives sum 4 and same signs, so yes. "
                     "x = 5, y = -1 gives sum 4 and opposite signs, so no. Insufficient.",
                     "Statement 2 alone: x = 3, y = 1 gives difference 2, same signs, "
                     "yes. x = 1, y = -3 gives difference 4, opposite signs, no. "
                     "Insufficient.",
                     "Together: x = 3, y = 1 satisfies both and gives yes. x = 5, y = -1 "
                     "satisfies both and gives no. Still insufficient.",
                 ],
                 answer="E",
                 why="Rephrasing to 'same sign' made every test a matter of picking two "
                     "numbers rather than manipulating inequalities. When the reworded "
                     "question is about sign, parity or whether something is an integer, "
                     "cases beat algebra nearly every time."),
        ],
        traps=[
            "Carrying information from statement 1 into statement 2, which is what makes "
            "a C look like a B.",
            "Answering the question you rephrased into rather than the one asked, "
            "especially when the rephrasing dropped a condition.",
            "Combining before both alone have failed, which costs time and occasionally "
            "produces a C where D was correct.",
            "Testing only integers. Fractions between 0 and 1 behave differently under "
            "squaring and multiplication and break many statements.",
        ],
        ladder={
            1: "The rephrasing is direct and one statement plainly settles it.",
            2: "Insufficiency is shown by two easy integer cases.",
            3: "Only a fraction or a negative reveals the insufficiency.",
            4: "The statements interact, so the combination requires real reasoning "
               "rather than stacking.",
            5: "The rephrasing itself is the question, and reading the stem literally "
               "leads to a defensible wrong answer.",
        },
    ),

    Topic(
        slug="ds-yes-no",
        title="Value Questions and Yes or No Questions",
        area=DS,
        skill="di_ds",
        idea="A value question needs one number and a yes or no question needs one "
             "consistent answer, and a statement can be sufficient for one and useless "
             "for the other.",
        why="This is the distinction that makes Data Sufficiency feel inconsistent to "
            "people who have not named it. Once named, half the confusing questions stop "
            "being confusing.",
        facts=[
            ("Value question", "what is x: sufficient means exactly one value",
             "Two possible values is insufficient, however close together they are."),
            ("Yes or no question", "is x even: sufficient means always yes or always no",
             "A definite no is just as sufficient as a definite yes, which is the part "
             "people forget."),
            ("Always no is sufficient", "proving it cannot happen settles the question",
             "If a statement guarantees x is odd, it has answered is x even, with no."),
            ("Sometimes yes is insufficient", "one case each way kills it",
             "This is why two counterexamples is the whole proof technique for "
             "insufficiency."),
            ("A range can be sufficient", "for yes or no, not for value",
             "Knowing x is between 12 and 20 settles is x greater than 10 and settles "
             "nothing about what x is."),
            ("Spotting the type", "read for a question word or a verb",
             "What, how many and what is the value are value questions. Is, does, are and "
             "can are yes or no."),
        ],
        worked=[
            dict(ask="Is the integer p a prime? (1) p has exactly two distinct positive "
                     "factors. (2) p is between 90 and 96.",
                 steps=[
                     "Yes or no question, so sufficient means always yes or always no.",
                     "Statement 1: exactly two distinct positive factors is the "
                     "definition of prime. Always yes. Sufficient.",
                     "Answer is A or D. Test statement 2 alone.",
                     "Statement 2: integers 91 to 95. 91 is 7 times 13, not prime. 93 is "
                     "3 times 31, not prime. 94 and 95 are not prime. 92 is not prime. "
                     "Every value gives no. Always no, so sufficient.",
                 ],
                 answer="D",
                 why="Statement 2 is sufficient by always answering no, which is the step "
                     "people skip. They check a couple of values, see none are prime, and "
                     "call it insufficient because it did not identify p. Identifying p "
                     "was never the question."),
        ],
        traps=[
            "Treating a definite no as insufficient. It answers the question completely.",
            "Demanding a value on a yes or no question, which makes sufficient statements "
            "look inadequate.",
            "Accepting a range on a value question, where a range is never enough unless "
            "it contains exactly one qualifying value.",
            "Misreading the stem's type in the first three seconds and then working the "
            "wrong standard for two minutes.",
        ],
        ladder={
            1: "A yes or no question where one statement gives a definite yes.",
            2: "Sufficiency comes from a definite no rather than a yes.",
            3: "A range is sufficient for the yes or no question asked and would not be "
               "for a value.",
            4: "The stem looks like a value question and is a yes or no question, or the "
               "reverse.",
            5: "A range contains exactly one integer satisfying a hidden condition, so it "
               "is sufficient for a value question after all.",
        },
    ),

    Topic(
        slug="gt-tables",
        title="Table Analysis",
        area=GT,
        skill="di_gt",
        idea="You are given a sortable table and three true-or-false statements, and the "
             "sort is the tool: most statements that look like work become a single "
             "glance after the right column is sorted.",
        why="Table Analysis rewards deciding what you need before you look, and punishes "
            "reading the table top to bottom. The table is usually larger than anything "
            "you need from it.",
        facts=[
            ("The format", "one table, three statements, each true or false",
             "All three must be right for credit, so the cheap statements matter as much "
             "as the hard one."),
            ("Sort first", "pick the column the statement is about",
             "Highest, lowest, top three, more than half: every one of these is one sort "
             "away from obvious."),
            ("Read the statement twice", "note the exact comparison and the exact group",
             "Statements are written so that a near-miss reading is true and the actual "
             "reading is false."),
            ("Watch the qualifier", "all, none, at least one, more than half",
             "One counterexample kills an all. Finding it is usually a sort and a glance "
             "at one end."),
            ("Column headers carry units", "per capita, thousands, percent",
             "The most common table error is comparing a count column with a rate column "
             "as though they measured the same thing."),
            ("Do not compute the whole column", "you need one comparison, not a total",
             "If the statement is about a maximum, summing the column is pure loss."),
        ],
        worked=[
            dict(ask="A table lists 14 regions with columns for population (thousands), "
                     "clinics, and clinics per 100,000 people. Statement: 'The region "
                     "with the most clinics also has the highest number of clinics per "
                     "100,000 people.' How do you check it?",
                 steps=[
                     "Two different columns, so two sorts, not one computation.",
                     "Sort by clinics descending and note the top region only.",
                     "Sort by clinics per 100,000 descending and note the top region only.",
                     "If they are the same region the statement is true; otherwise false. "
                     "No arithmetic at all.",
                 ],
                 answer="Two sorts and two glances",
                 why="The statement is designed to look like it needs the ratio "
                     "recomputed. It needs two maxima, and the table already holds both "
                     "columns. Before computing anything from a table, check whether the "
                     "quantity is already a column."),
        ],
        traps=[
            "Comparing a count column against a rate column. A large region with many "
            "clinics can have a low rate, and the table gives you both so that you can "
            "confuse them.",
            "Missing the units in the header. Population in thousands against clinics as "
            "a raw count changes every ratio by a factor of a thousand.",
            "Recomputing a column that already exists, which is the most common way to "
            "lose time here.",
            "Getting two of three statements right and moving on. There is no partial "
            "credit, so the last statement is worth the same as the first two combined.",
        ],
        ladder={
            1: "One sort answers the statement directly.",
            2: "Two sorts are needed and the comparison is still a glance.",
            3: "The statement uses a qualifier such as more than half, so counting rows "
               "matters.",
            4: "A count column and a rate column are both present and the statement "
               "trades on the difference.",
            5: "The statement is true of a near reading and false of the exact one, and "
               "the difference is a single word such as among or including.",
        },
    ),

    Topic(
        slug="gt-graphics",
        title="Graphics Interpretation",
        area=GT,
        skill="di_gt",
        idea="You read a chart and complete sentences from dropdown menus, so the answer "
             "set is fixed and usually far coarser than the precision the chart appears "
             "to offer.",
        why="People over-read these charts. The dropdown options are typically spaced "
            "widely enough that an estimate settles them, and reading to the nearest unit "
            "is effort that buys nothing.",
        facts=[
            ("The format", "one graphic, sentences with dropdown blanks",
             "The options tell you the precision required, so read them before reading "
             "the chart."),
            ("Read the options first", "they set the grain of the answer",
             "If the choices are 10, 50 and 200, you need an order of magnitude, not a "
             "value."),
            ("Check both axes", "including the origin and the units",
             "A vertical axis starting at 40 rather than 0 makes a small difference look "
             "like a large one, and that is done on purpose."),
            ("Trend words are comparisons", "increases, decreases, remains roughly "
             "constant",
             "You are comparing two points or a slope, never computing a rate unless "
             "asked."),
            ("Scatter plots", "look for the shape, not the points",
             "Positive, negative or no association, and whether the relationship bends. "
             "Individual points matter only when the question names one."),
            ("Best fit lines", "the line is a summary, not data",
             "A question about the line is about the trend; a question about a point is "
             "about that point."),
        ],
        worked=[
            dict(ask="A scatter plot shows 30 stores by floor area against annual "
                     "revenue, with a rising best fit line. The sentence reads: 'For "
                     "every additional 1,000 square feet, predicted revenue increases by "
                     "approximately [dropdown: $15,000 / $60,000 / $250,000].' How do you "
                     "settle it?",
                 steps=[
                     "The options are far apart, so an estimate of the slope is enough.",
                     "Pick two easy points ON THE LINE, not on the data: where the line "
                     "crosses convenient gridlines.",
                     "Read the rise and the run between them, in the axis units.",
                     "Divide, then match to whichever option is nearest. Nothing needs to "
                     "be exact.",
                 ],
                 answer="The slope read off two gridline crossings on the line",
                 why="Two mistakes are available here and both are avoidable. Reading two "
                     "data points instead of two line points gives the slope between two "
                     "stores rather than the trend. And chasing precision when the "
                     "options differ by a factor of four is time spent buying nothing."),
        ],
        traps=[
            "Reading data points when the question asks about the fitted line, or the "
            "reverse.",
            "Missing a truncated axis, which makes a modest change look dramatic and is "
            "the most common visual trick in the type.",
            "Ignoring a log scale, where equal spacing means equal multiples rather than "
            "equal differences.",
            "Over-reading precision the dropdown does not ask for.",
        ],
        ladder={
            1: "A single value read directly off a labelled axis.",
            2: "A comparison between two clearly separated points.",
            3: "A slope or rate estimated from the fitted line.",
            4: "The axis is truncated or the scale is not linear, and noticing it changes "
               "the answer.",
            5: "The sentence asks about the relationship's shape rather than its "
               "direction, and one plausible option describes a linear fit to data that "
               "bends.",
        },
    ),

    Topic(
        slug="gt-scales",
        title="Axes, Scales and Units",
        area=GT,
        skill="di_gt",
        idea="Most wrong answers on chart questions come from reading the picture "
             "correctly and the axis incorrectly, which is why the axis is the first "
             "thing to read and the last thing people check.",
        why="Every visual in Data Insights is a claim about numbers, and the axis is where "
            "the claim is defined. A truncated baseline, a log scale, or a units label in "
            "thousands changes conclusions without changing the shape of the picture.",
        facts=[
            ("Where does the axis start", "zero or somewhere else",
             "A bar chart starting at 40 exaggerates every difference. Check the baseline "
             "before comparing bar heights."),
            ("What are the units", "thousands, millions, percent, per capita",
             "The header or axis label carries this and it is the most skipped text on "
             "the screen."),
            ("Linear or logarithmic", "equal spacing means equal steps or equal multiples",
             "On a log axis, the gap from 1 to 10 equals the gap from 10 to 100."),
            ("Two axes, two scales", "a dual axis chart has two different rulers",
             "Lines crossing on a dual axis chart means nothing: the crossing point is an "
             "artefact of the two scalings."),
            ("Percent of what", "a stacked chart shows shares, not totals",
             "A shrinking segment of a growing total can be a growing quantity."),
            ("Cumulative or per period", "does the line show the total so far",
             "A cumulative chart never falls, so a flattening line means the periodic "
             "value went to nearly zero, not that the total dropped."),
        ],
        worked=[
            dict(ask="A dual axis chart shows monthly units sold on the left axis (0 to "
                     "500) and average price on the right axis ($18 to $24). The lines "
                     "cross in August. What does the crossing tell you?",
                 steps=[
                     "Ask what the two axes measure. Units on one, dollars on the other: "
                     "different quantities entirely.",
                     "The crossing point is where the two lines happen to occupy the same "
                     "vertical position on the screen.",
                     "That position means 'about 250 units' on one ruler and 'about $21' "
                     "on the other. Those are not equal to each other in any sense.",
                     "Shifting either axis range would move the crossing anywhere.",
                 ],
                 answer="Nothing. The crossing is an artefact of two independent scalings",
                 why="A dual axis crossing is the most confidently misread feature in "
                     "data presentation, in the exam and outside it. The only readings "
                     "that survive are about each line's own direction and each line's "
                     "own values, never about where they sit relative to one another."),
        ],
        traps=[
            "Comparing bar heights without checking the baseline, which turns a 3 percent "
            "difference into a picture of a doubling.",
            "Reading a log axis as linear, which understates every large value by an "
            "order of magnitude.",
            "Attaching meaning to where two lines cross on a dual axis chart.",
            "Missing a units label such as thousands, which is usually set in small type "
            "beside the axis and changes every answer by three orders of magnitude.",
        ],
        ladder={
            1: "A linear axis starting at zero with plain units.",
            2: "The units are in thousands and the answer options are spaced to catch it.",
            3: "The baseline is truncated and the question asks about the size of a "
               "difference.",
            4: "The scale is logarithmic and a plausible option assumes it is linear.",
            5: "A dual axis chart where the intended reading concerns each line "
               "separately and a tempting option concerns their crossing.",
        },
    ),
    Topic(
        slug="msr-format",
        title="Multi-Source Reasoning",
        area=MSR_TPA,
        skill="di_msr",
        idea="Two or three tabs of material feed several questions, and the skill is "
             "finding which tab answers the question rather than understanding all of "
             "them.",
        why="These carry the highest reading load in the section and the lowest reward "
            "for thorough reading. The material is deliberately larger than any one "
            "question needs.",
        facts=[
            ("The format", "two or three tabs, then questions on the set",
             "Tabs hold prose, tables, emails, memos or a mix, and the questions arrive "
             "after you have seen all of them."),
            ("Skim for what each tab is", "one phrase per tab, not a summary",
             "Tab 1 is the proposal, tab 2 is the cost data, tab 3 is the objection. "
             "That map is what the questions are navigated with."),
            ("Read the question, then return", "do not pre-read for detail",
             "Detail read in advance is detail read twice, and most of it is never "
             "asked about."),
            ("Watch for conflict between tabs", "sources may disagree",
             "When two tabs give different figures, the question usually turns on which "
             "source a claim relies on."),
            ("Who is speaking", "an email is a claim, not a fact",
             "A tab written by an interested party asserts things; the question may ask "
             "what is supported rather than what is said."),
            ("Answer from the cited tab only", "support has to be in the source",
             "Combining tabs is legitimate when the question is about the whole set and "
             "wrong when it is about one."),
        ],
        worked=[
            dict(ask="Three tabs: a proposal to consolidate two warehouses, a table of "
                     "shipping costs by route, and an email from the regional manager "
                     "arguing the consolidation will raise delivery times. A question "
                     "asks whether consolidating would reduce total shipping cost. Where "
                     "do you look?",
                 steps=[
                     "The question is about cost, so the cost table is the source.",
                     "The email is about delivery time, which is a different quantity. It "
                     "is also an argument rather than data.",
                     "The proposal may state an expected saving, which is a claim by the "
                     "proposer, not a measurement.",
                     "So: work the table, and treat the proposal's figure as something to "
                     "check against it rather than to accept.",
                 ],
                 answer="The cost table, with the proposal's claim checked against it",
                 why="Two of the three tabs are about the topic and neither answers the "
                     "question. That distribution is typical: the set is built so that "
                     "the wrong tab is always relevant enough to feel right."),
        ],
        traps=[
            "Reading all tabs closely before seeing a single question, which is where "
            "most of the lost time in Data Insights goes.",
            "Treating an assertion in an email or memo as established fact. The writer "
            "usually has a position.",
            "Answering from the wrong tab when two tabs are both about the subject and "
            "only one holds the quantity asked about.",
            "Missing that two sources disagree, which is often the entire point of a "
            "question in the set.",
        ],
        ladder={
            1: "One tab obviously holds the answer and it is stated there.",
            2: "The answer needs one figure from a table and one sentence from prose.",
            3: "Two tabs are relevant and only one contains the quantity asked about.",
            4: "The tabs disagree, and the question turns on which source a claim rests "
               "on.",
            5: "The answer requires combining a table figure with a constraint stated in "
               "a different tab, and a tempting answer uses the table alone.",
        },
    ),

    Topic(
        slug="tpa-format",
        title="Two-Part Analysis",
        area=MSR_TPA,
        skill="di_tpa",
        idea="You choose one option in each of two columns from a shared list, and the "
             "two parts are almost always linked, so solving them together is faster "
             "than solving them apart.",
        why="The shared answer list is what makes these efficient or slow. Used well it "
            "is a constraint that narrows both columns at once; ignored it is just a long "
            "list read twice.",
        facts=[
            ("The format", "two columns, one shared list, one selection per column",
             "Both selections must be right, so this is effectively one question with two "
             "halves."),
            ("The columns are usually linked", "a pair that satisfies a relationship",
             "Larger and smaller, before and after, the two quantities that sum to a "
             "total."),
            ("Work the constraint, not the list", "find the relationship first",
             "Reading the list before understanding what connects the two columns is how "
             "these take four minutes."),
            ("Test candidate pairs", "plug in rather than solve when the list is short",
             "With five or six options, testing a promising pair is often faster than "
             "algebra."),
            ("Order matters", "check which column is which",
             "The most frequent error is a correct pair entered the wrong way round, "
             "which scores zero."),
            ("Same option twice", "sometimes allowed, sometimes not",
             "Read the instruction above the table rather than assuming; it varies by "
             "question."),
        ],
        worked=[
            dict(ask="A question gives a mixture problem and asks you to select the "
                     "number of litres of solution A and of solution B, from a shared "
                     "list of integers, so that the mixture has a stated concentration "
                     "and a stated total volume. How do you approach it?",
                 steps=[
                     "Two constraints are given: total volume and final concentration. "
                     "Two unknowns, two equations.",
                     "Use the easier constraint first: the volumes must sum to the stated "
                     "total. That alone eliminates most pairs on the list.",
                     "Among surviving pairs, test the concentration constraint on the "
                     "most promising one.",
                     "Confirm which column asked for A and which for B before entering.",
                 ],
                 answer="Filter on the sum first, then test the survivors on "
                        "concentration",
                 why="The sum constraint is cheap to apply and usually leaves two or "
                     "three pairs out of a list of six. Applying the expensive constraint "
                     "to everything, rather than to the survivors, is the difference "
                     "between ninety seconds and four minutes."),
        ],
        traps=[
            "Entering the right pair in the wrong order, which is scored as entirely "
            "wrong and is the most common loss in the type.",
            "Solving each column independently when a relationship links them, which "
            "doubles the work.",
            "Applying the harder constraint first when a cheaper one would eliminate most "
            "of the list.",
            "Assuming an option cannot be used in both columns without reading the "
            "instruction.",
        ],
        ladder={
            1: "The two columns are independent and each is a direct lookup.",
            2: "One simple relationship links the columns and the list is short.",
            3: "Two constraints apply and filtering in the right order saves most of the "
               "time.",
            4: "The relationship is stated in words that must be translated before any "
               "option is tested.",
            5: "Several pairs satisfy the obvious constraint and only one satisfies a "
               "condition stated in passing.",
        },
    ),

    Topic(
        slug="di-percent",
        title="Percent Change, Growth and Share in Data",
        area=NUM,
        skill="di_gt",
        idea="The arithmetic in Data Insights is mostly percent change and share, and "
             "almost every trap in it is a question about which number is the "
             "denominator.",
        why="This is the numeracy the section runs on. It is not hard arithmetic, it is "
            "arithmetic done under time on numbers that were chosen so that a careless "
            "denominator gives a wrong answer that appears in the options.",
        facts=[
            ("Percent change", "(new - old) / old",
             "The denominator is always the ORIGINAL value, which is the half people "
             "reverse under time pressure."),
            ("Percent versus percentage point", "4 to 6 is 2 points and 50 percent",
             "Charts and dropdowns exploit the difference constantly."),
            ("Share of total", "part / whole",
             "Both parts can move. A rising share can accompany a falling count."),
            ("Successive changes do not add", "up 20 then down 20 is down 4",
             "Multiply the factors: 1.2 times 0.8 is 0.96. This appears every year in "
             "some form."),
            ("Reversing a change", "to undo a 20 percent rise you cut by 16.7 percent",
             "Because you are dividing by 1.2, not subtracting 20 percent."),
            ("Compound growth", "multiply by (1 + r) each period",
             "Two periods of 10 percent is a factor of 1.21, not 1.20."),
            ("Weighted average sits nearer the bigger group",
             "between the two averages, closer to the larger n",
             "Useful as a sanity check: an answer outside the two component averages is "
             "always wrong."),
        ],
        worked=[
            dict(ask="A table shows a product line's revenue at $4.2m in 2023 and $5.1m "
                     "in 2024, while total company revenue went from $21m to $30m. Did "
                     "the line's share rise or fall?",
                 steps=[
                     "Share in 2023: 4.2 / 21 = 0.20, so 20 percent.",
                     "Share in 2024: 5.1 / 30 = 0.17, so 17 percent.",
                     "The share fell, from 20 to 17 percent.",
                     "Note the line's revenue ROSE by about 21 percent over the same "
                     "period.",
                 ],
                 answer="The share fell from 20 percent to 17 percent even though revenue "
                        "rose",
                 why="Both facts are true and they point opposite ways, which is the "
                     "shape the exam uses most. The line grew and shrank as a share "
                     "because the denominator grew faster. Whenever a question mixes a "
                     "share with an amount, compute both rather than inferring one from "
                     "the other."),
        ],
        traps=[
            "Dividing by the new value when computing percent change. The denominator is "
            "the original.",
            "Adding successive percent changes, which is wrong in a direction that "
            "usually appears among the options.",
            "Confusing a rise in share with a rise in amount, or the reverse.",
            "Treating percentage points as percent, which overstates or understates by "
            "whatever the base happens to be.",
        ],
        ladder={
            1: "A single percent change with both values given.",
            2: "A share computed from a part and a total.",
            3: "Two successive changes that must be multiplied rather than added.",
            4: "A share and an amount move in opposite directions and both are asked "
               "about.",
            5: "A reversal question, where undoing a stated percentage change requires "
               "dividing rather than subtracting.",
        },
    ),

    Topic(
        slug="di-estimation",
        title="Estimating, and When to Use the Calculator",
        area=NUM,
        skill="di_gt",
        idea="Data Insights is the only section with an on-screen calculator, and the "
             "people who use it most are usually the slowest, because most questions are "
             "decided by a comparison rather than a value.",
        why="The section is 20 questions in 45 minutes, so roughly two minutes each "
            "including the reading. Any habit that spends thirty seconds producing a "
            "precise number where a rough one would decide the question costs a quarter "
            "of that budget.",
        facts=[
            ("Calculator availability", "Data Insights only",
             "GMAC states an on-screen calculator is available in this section. The "
             "citation is on our GMAT exam guide page and on the section index above; "
             "the other sections are worked by hand."),
            ("Ask what precision the answer needs", "options set the grain",
             "Widely spaced options need an estimate. Close options need care, and are "
             "rarer than people expect."),
            ("Round before dividing", "4.18 / 20.7 is about 4.2 / 21",
             "Rounding both numbers in the same direction keeps the error small and "
             "predictable."),
            ("Benchmark fractions", "1/3 is 33 percent, 1/6 is about 17, 1/8 is 12.5",
             "Recognising a ratio as near a benchmark settles most share questions "
             "without arithmetic."),
            ("Compare by ratio, not difference", "which is bigger needs no subtraction",
             "To compare 17/48 with 23/70, compare to 1/3: one is above, the other "
             "below. Done."),
            ("Sanity check the magnitude", "does the answer have the right size",
             "A units slip gives an answer wrong by a factor of a thousand, which is "
             "visible without checking the arithmetic."),
        ],
        worked=[
            dict(ask="Which is larger, 17/48 or 23/70? Settle it without dividing "
                     "either.",
                 steps=[
                     "Compare each to the benchmark 1/3.",
                     "17/48: one third of 48 is 16, and 17 is more than 16, so 17/48 is "
                     "above 1/3.",
                     "23/70: one third of 70 is about 23.3, and 23 is less than that, so "
                     "23/70 is below 1/3.",
                     "One is above 1/3 and the other below, so 17/48 is larger.",
                 ],
                 answer="17/48",
                 why="Two divisions became two comparisons against a number you already "
                     "know. This works whenever the two fractions straddle a benchmark, "
                     "which is often, because exam fractions are chosen near familiar "
                     "values rather than at random."),
        ],
        traps=[
            "Reaching for the calculator by reflex. Opening it, typing, and reading back "
            "costs more than most of these questions are worth.",
            "Rounding the numerator and denominator in opposite directions, which "
            "compounds the error instead of cancelling it.",
            "Computing a precise value when the question asked which is larger.",
            "Trusting a calculator result whose magnitude is implausible, which is how a "
            "units error survives to the answer.",
        ],
        ladder={
            1: "A single division where the options are far apart.",
            2: "A comparison settled by rounding both values.",
            3: "A ratio compared against a benchmark fraction rather than computed.",
            4: "The options are close enough that the rounding direction has to be "
               "controlled.",
            5: "The question asks for a comparison that looks like it needs two exact "
               "values and is settled by one structural observation.",
        },
    ),
]
