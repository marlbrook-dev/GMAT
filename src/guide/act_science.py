"""ACT Science, topic by topic.

Organised by ACT's own three reporting categories, which is also how our engine scores
the section: Interpretation of Data, Scientific Investigation, and Evaluation of
Scientific Arguments and Models.

The single most useful thing to know about this section is what it is not. It is not a
test of science knowledge. It is a reading and data-interpretation section that happens
to use scientific material, and the outside knowledge it assumes is roughly a year of
introductory science. Students who try to understand the underlying science lose the
section on time; students who treat the figures as a lookup table finish it.

Three passage formats recur: Data Representation, which is graphs and tables with
little prose; Research Summaries, which describe two or more experiments; and
Conflicting Viewpoints, which gives two or more scientists disagreeing and is the one
set that is genuinely a reading task.

One structural note, sourced in data/exams.json: on the enhanced ACT this section is
optional and is not part of the Composite score.

Same IP position as the rest of the guide: reading data belongs to nobody, no other
author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

IOD, SI, ESA = ("Interpretation of Data", "Scientific Investigation",
                "Evaluation of Scientific Arguments and Models")

TOPICS = [

    Topic(
        slug="act-s-method",
        title="How to Work an ACT Science Passage",
        area=IOD,
        skill="act_s_iod",
        idea="Read the axes and the variables, not the prose, because most questions are "
             "lookups and the prose is mostly there to slow you down.",
        why="Forty questions in forty minutes over six or seven passages is about a "
            "minute each. The time is lost reading explanatory text that no question ever "
            "asks about.",
        facts=[
            ("What the section actually tests", "reading figures, not knowing science",
             "Outside knowledge is rare and shallow when it appears at all."),
            ("Read the figures first", "axis labels, units, and what varies",
             "Thirty seconds on the axes saves minutes on the questions."),
            ("Skip the prose on the first pass", "return only when a question sends you",
             "Except on Conflicting Viewpoints, which is genuinely a reading set."),
            ("Note the direction of each relationship", "as X rises, Y does what",
             "Most Interpretation of Data questions are that one observation."),
            ("Watch the units", "and any multiplier in the header",
             "Thousands, per kilogram, times ten to the minus three."),
            ("Check the axis start", "zero or somewhere else",
             "A truncated axis exaggerates every difference."),
            ("Trends questions", "increasing, decreasing, or neither",
             "And whether the relationship is consistent across the whole range."),
            ("Interpolation and extrapolation", "between the data, or beyond it",
             "Beyond the measured range is the unreliable case and the exam asks about "
             "it."),
            ("Two figures", "questions often need one value from each",
             "Find the shared variable; that is the bridge between them."),
        ],
        worked=[
            dict(ask="A figure plots enzyme activity against temperature for three pH "
                     "values. A question asks at which pH activity peaks at the lowest "
                     "temperature. How do you work it?",
                 steps=[
                     "Do not think about enzymes. Identify the axes: temperature "
                     "horizontal, activity vertical, three curves labelled by pH.",
                     "The question asks about the location of each curve's peak along the "
                     "horizontal axis.",
                     "Find each curve's highest point and read its temperature.",
                     "Report the pH whose peak sits furthest left. No biology used.",
                 ],
                 answer="The pH whose curve peaks furthest left on the temperature axis",
                 why="The question sounds like biochemistry and is a reading task about "
                     "three maxima. That is the section in one example: whatever the "
                     "subject, the work is locating something on a figure, and knowing "
                     "what enzymes do would not have helped."),
        ],
        traps=[
            "Reading the prose thoroughly before the questions. Most of it is never "
            "asked about.",
            "Trying to understand the science. The section does not reward it and the "
            "clock punishes it.",
            "Missing a unit multiplier in a table header, which changes every answer by "
            "orders of magnitude.",
            "Missing a truncated axis, so a small difference looks decisive.",
        ],
        ladder={
            1: "Read a single value off one figure.",
            2: "Identify the direction of a relationship.",
            3: "Combine a value from one figure with a value from another.",
            4: "Extrapolate beyond the measured range, or interpolate between points.",
            5: "The figure has a non-linear scale or a truncated axis and a plausible "
               "answer assumes otherwise.",
        },
    ),

    Topic(
        slug="act-s-investigation",
        title="Scientific Investigation: Reading an Experiment",
        area=SI,
        skill="act_s_si",
        idea="Research Summaries questions turn on what was changed, what was measured, "
             "and what was held constant, so identifying those three answers most of "
             "them.",
        why="Once you can name the independent variable, the dependent variable and the "
            "controls, questions about purpose, design and what a further experiment "
            "should do become nearly automatic.",
        facts=[
            ("Independent variable", "what the experimenter changed on purpose",
             "Usually what differs between the experiments or across the rows."),
            ("Dependent variable", "what was measured",
             "Usually the column or the vertical axis."),
            ("Controlled variables", "what was deliberately held the same",
             "These are what make the comparison meaningful."),
            ("Control group", "the condition with no treatment",
             "Its job is to show what happens without the thing being tested."),
            ("Why two experiments", "usually one variable differs between them",
             "Find that difference; it is what the second experiment was for."),
            ("Purpose questions", "what was this step FOR",
             "Answered by what it holds constant or what it rules out."),
            ("Design a further experiment", "change one variable, hold the rest",
             "Answers changing two variables at once are wrong by construction."),
            ("Replication", "repeated trials reduce the effect of chance",
             "Not the same as a control, and the exam distinguishes them."),
        ],
        worked=[
            dict(ask="Experiment 1 measures corrosion of a metal strip in salt solutions "
                     "at five concentrations, at 20 degrees. Experiment 2 repeats it at "
                     "40 degrees. A question asks why Experiment 2 was performed. What is "
                     "the answer?",
                 steps=[
                     "Name the variables in Experiment 1: independent is concentration, "
                     "dependent is corrosion, temperature is held at 20.",
                     "Compare with Experiment 2: the only change is temperature.",
                     "A variable held constant in one experiment and changed in the next "
                     "is the thing the second experiment exists to test.",
                     "So: to determine whether temperature affects the relationship "
                     "between concentration and corrosion.",
                 ],
                 answer="To test whether temperature affects the result found in "
                        "Experiment 1",
                 why="The method is entirely mechanical: list what is held constant in "
                     "one experiment, find which of those the next one changes, and that "
                     "is its purpose. It works on essentially every Research Summaries "
                     "purpose question and requires no science at all."),
        ],
        traps=[
            "Confusing the independent and dependent variables, which reverses every "
            "design question.",
            "Choosing a proposed experiment that changes two variables at once.",
            "Treating repeated trials as a control group. Replication addresses chance; a "
            "control addresses the treatment.",
            "Answering a purpose question from the passage's introduction rather than from "
            "what the experiment actually varies.",
        ],
        ladder={
            1: "Identify what was measured in a single experiment.",
            2: "Name the variable that differs between two experiments.",
            3: "Explain the purpose of a step or of a control.",
            4: "Choose the further experiment that isolates one variable.",
            5: "Several variables differ between experiments and the question turns on "
               "which one the comparison actually isolates.",
        },
    ),

    Topic(
        slug="act-s-arguments",
        title="Evaluating Models, Hypotheses and Conflicting Viewpoints",
        area=ESA,
        skill="act_s_esa",
        idea="You are asked whether data supports or weakens a stated position, which "
             "means holding each position precisely enough to see what would count "
             "against it.",
        why="Conflicting Viewpoints is the one set in this section that is genuinely a "
            "reading task, and it carries the questions people most often run out of time "
            "for. Reading each viewpoint for its claim, not its detail, is what makes it "
            "quick.",
        facts=[
            ("Read each viewpoint for its claim", "one sentence each, in your own words",
             "The details are lookups; the claim is what questions compare."),
            ("Find the point of disagreement", "they usually share most of the facts",
             "They differ on mechanism, cause, or which evidence matters."),
            ("Support means consistent with", "the finding fits the claim's prediction",
             "Ask what each scientist would EXPECT to see, then check the data."),
            ("Weaken means inconsistent", "the finding is what the claim rules out",
             "Not merely unhelpful, but contrary."),
            ("Whose view is asked", "the stem names a scientist or a student",
             "Answering from the wrong one is the most common error in the format."),
            ("Agreement questions", "what would BOTH accept",
             "Usually a shared observation rather than an interpretation."),
            ("Match the claim's scope", "a claim about one case is not about all cases",
             "Evidence about a different scale or population may not bear."),
            ("New information questions", "if this were true, who is helped",
             "Test it against each viewpoint's prediction in turn."),
        ],
        worked=[
            dict(ask="Scientist 1 says a lake's algal blooms are driven by farm runoff. "
                     "Scientist 2 says they are driven by rising water temperature. A new "
                     "finding shows blooms occurred in years with high runoff regardless "
                     "of temperature. Who is supported?",
                 steps=[
                     "Scientist 1 predicts: blooms track runoff.",
                     "Scientist 2 predicts: blooms track temperature.",
                     "The finding: blooms happened with high runoff even when temperature "
                     "was not high.",
                     "That is what Scientist 1 predicts and what Scientist 2's claim "
                     "cannot account for. Supports 1, weakens 2.",
                 ],
                 answer="Scientist 1 is supported and Scientist 2 is weakened",
                 why="The phrase 'regardless of temperature' is the whole question: it "
                     "removes the variable Scientist 2 depends on and the effect persists. "
                     "Writing down what each side PREDICTS, before looking at the finding, "
                     "is what makes that visible in a few seconds."),
        ],
        traps=[
            "Answering from the wrong scientist's position.",
            "Treating a finding as weakening a view when it is merely unrelated to it.",
            "Bringing in real-world knowledge about which explanation is actually correct. "
            "The question is about the stated positions.",
            "Reading the viewpoints in full detail. The claims are what get compared; the "
            "details are lookups.",
        ],
        ladder={
            1: "One viewpoint and a finding that plainly fits or does not.",
            2: "Two viewpoints with an obvious disagreement.",
            3: "A question about what both would accept.",
            4: "New information must be tested against each viewpoint's prediction.",
            5: "The finding bears on a detail one viewpoint depends on and the other never "
               "mentions, so it supports one without touching the other.",
        },
    ),
]
