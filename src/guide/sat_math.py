"""Digital SAT Math, topic by topic.

Organised by College Board's own four content domains, which is also how our engine
scores the section, so every topic here maps to a skill the trainer adapts on and the
difficulty ladder pulls real items from the bank.

One thing shapes almost every strategy note below: the Desmos graphing calculator is
built into Bluebook and allowed on the whole Math section. That is a sourced fact in
data/exams.json, not a recollection. It changes what "solve" means. A question that
wants the intersection of two graphs is a question you can look at rather than solve,
and the students who lose time here are the ones doing algebra the tool would have
done, or reaching for the tool on a question that was one step of arithmetic.

Same IP position as the rest of the guide: the mathematics belongs to nobody, no other
author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

ALG, ADV, PSDA, GEO = ("Algebra", "Advanced Math",
                       "Problem-Solving and Data Analysis",
                       "Geometry and Trigonometry")

TOPICS = [

    Topic(
        slug="sat-linear-equations",
        title="Linear Equations and Their Solutions",
        area=ALG,
        skill="m_alg",
        idea="A linear equation in one variable has exactly one solution unless the "
             "variable cancels, and the two cases where it cancels are worth recognising "
             "on sight.",
        why="Linear work is the largest single slice of the Math section and the part "
            "where speed compounds. Every later topic, systems, functions, word problems, "
            "is built on being able to do this without thinking about it.",
        facts=[
            ("Standard form", "ax + b = c",
             "One unknown, one solution, provided a is not zero."),
            ("No solution", "the variable cancels and the constants disagree",
             "2x + 3 = 2x + 5 becomes 3 = 5, which is false, so nothing works."),
            ("Infinitely many solutions", "the variable cancels and the constants agree",
             "2x + 3 = 2x + 3 becomes 3 = 3, which is true for every x."),
            ("The condition for no solution", "same slope, different intercept",
             "Written as two sides of an equation or as two lines, it is the same idea."),
            ("Clearing fractions", "multiply every term by the common denominator",
             "Every term, including the ones with no fraction, or the equation changes."),
            ("Solving for a variable in terms of others", "isolate it the same way",
             "Literal equations follow identical steps; the letters just look worse."),
        ],
        worked=[
            dict(ask="For what value of k does 3(2x + k) = 6x + 15 have infinitely many "
                     "solutions?",
                 steps=[
                     "Expand the left: 6x + 3k = 6x + 15.",
                     "Subtract 6x from both sides: 3k = 15. The variable has cancelled, "
                     "which is the signal that this is one of the two special cases.",
                     "Infinitely many solutions means the leftover constants must agree, "
                     "so 3k = 15.",
                     "k = 5.",
                 ],
                 answer="k = 5",
                 why="The question is not asking you to solve for x; it is asking you to "
                     "force the cancellation case. Recognising that from the phrase "
                     "'infinitely many solutions' is the whole question, and it takes two "
                     "lines once you do."),
            dict(ask="Solve 2(x - 4) / 3 + 1 = (x + 2) / 2 for x.",
                 steps=[
                     "Common denominator of 3 and 2 is 6. Multiply every term by 6.",
                     "4(x - 4) + 6 = 3(x + 2). Note the standalone 1 became 6.",
                     "4x - 16 + 6 = 3x + 6, so 4x - 10 = 3x + 6.",
                     "x = 16.",
                 ],
                 answer="x = 16",
                 why="Multiplying the standalone term is the step people drop, because it "
                     "has no visible denominator. Every term means every term, and the "
                     "error is silent: you get a clean-looking answer that is wrong."),
        ],
        traps=[
            "Forgetting to multiply a term with no denominator when clearing fractions. "
            "The result still looks tidy, which is why it survives to the answer sheet.",
            "Distributing a negative across only the first term: -(x - 3) is -x + 3, not "
            "-x - 3.",
            "Treating no solution and infinitely many solutions as the same special case. "
            "They are opposite outcomes of the same cancellation.",
            "Solving for x when the question asked for 2x or for x + 1. The SAT asks for "
            "the transformed value often enough that it is worth rereading the question "
            "after you solve.",
        ],
        ladder={
            1: "One or two steps, integer coefficients, solve for x.",
            2: "Fractions or parentheses appear and the steps are the same.",
            3: "The question asks for an expression in x rather than x itself.",
            4: "A parameter is present and the question asks what value makes the "
               "equation have no solution or infinitely many.",
            5: "The equation is embedded in a word problem, so translating it is most of "
               "the work and the algebra is short.",
        },
    ),

    Topic(
        slug="sat-linear-functions",
        title="Linear Functions and Their Graphs",
        area=ALG,
        skill="m_alg",
        idea="Slope is a rate of change and the intercept is a starting value, and "
             "reading a word problem into those two quantities answers most linear "
             "modelling questions immediately.",
        why="The SAT asks about linear models constantly and usually in words: a fee plus "
            "a rate, a starting population plus growth, a tank draining. The questions "
            "are short once you know which number is the slope.",
        facts=[
            ("Slope intercept form", "y = mx + b",
             "m is the rate of change per unit of x, b is the value when x is zero."),
            ("Slope from two points", "m = (y2 - y1) / (x2 - x1)",
             "Rise over run, and the order must match in both numerator and denominator."),
            ("Point slope form", "y - y1 = m(x - x1)",
             "Fastest when you have one point and the slope, which is the usual case."),
            ("Standard form", "Ax + By = C",
             "Slope is -A/B, which is worth knowing rather than rearranging each time."),
            ("What the slope means in words", "the change in y per one unit of x",
             "If x is hours and y is dollars, the slope is dollars per hour."),
            ("What the intercept means in words", "the value before anything happens",
             "The flat fee, the starting amount, the initial population."),
            ("Parallel and perpendicular", "equal slopes; slopes multiplying to -1",
             "Perpendicular means the negative reciprocal, so 3/4 pairs with -4/3."),
        ],
        worked=[
            dict(ask="A technician charges a call-out fee plus an hourly rate. A 3-hour "
                     "job costs $255 and a 7-hour job costs $455. What does a 5-hour job "
                     "cost?",
                 steps=[
                     "Two points: (3, 255) and (7, 455). The model is linear, so find the "
                     "slope.",
                     "m = (455 - 255) / (7 - 3) = 200 / 4 = 50. The hourly rate is $50.",
                     "Find b: 255 = 50(3) + b, so b = 105. The call-out fee is $105.",
                     "At x = 5: 50(5) + 105 = 355.",
                 ],
                 answer="$355",
                 why="You could also notice 5 is halfway between 3 and 7, so the cost is "
                     "halfway between 255 and 455, which is 355, with no algebra at all. "
                     "That shortcut works because the model is linear, and spotting it is "
                     "worth a minute on a section where minutes are the constraint."),
        ],
        traps=[
            "Computing slope with the x and y differences in opposite orders, which flips "
            "the sign.",
            "Reading the intercept as the answer when the question asked for the rate, or "
            "the reverse. The words fee and per hour are what distinguish them.",
            "Using the reciprocal instead of the negative reciprocal for a perpendicular "
            "slope.",
            "Graphing on Desmos when two points and one subtraction would have been "
            "faster. The tool is free to use and not free in time.",
        ],
        ladder={
            1: "Read the slope or intercept straight off an equation or a graph.",
            2: "Find the equation of a line through two given points.",
            3: "A word problem where you must decide which quantity is the slope.",
            4: "The question asks what the slope means in the context, and the wrong "
               "answers all describe the intercept or reverse the units.",
            5: "Two linear models are compared, and the question asks when one overtakes "
               "the other or what their difference represents.",
        },
    ),

    Topic(
        slug="sat-systems",
        title="Systems of Linear Equations",
        area=ALG,
        skill="m_alg",
        idea="Two lines meet at one point, never, or everywhere, and which of those "
             "happens is decided entirely by comparing their slopes and intercepts.",
        why="Systems appear both as pure algebra and as the skeleton of most two-quantity "
            "word problems. With a graphing tool available, the special cases are the "
            "part that still has to be reasoned about.",
        facts=[
            ("One solution", "the lines have different slopes",
             "They cross exactly once, wherever that is."),
            ("No solution", "same slope, different intercept",
             "Parallel and distinct, so they never meet."),
            ("Infinitely many", "same slope, same intercept",
             "The two equations describe the same line."),
            ("Substitution", "solve one equation for a variable, put it in the other",
             "Best when a coefficient is already 1."),
            ("Elimination", "scale one or both, then add to cancel a variable",
             "Best when neither coefficient is 1 and the numbers are friendly."),
            ("Graphing it", "the solution is the intersection point",
             "With Desmos available this is often the fastest route, and it is exact "
             "enough because the answers are separated."),
            ("The parallel condition in coefficients", "a1/a2 = b1/b2",
             "For a1x + b1y = c1 and a2x + b2y = c2, matching ratios means same slope."),
        ],
        worked=[
            dict(ask="For what value of c does the system 3x - 2y = 8 and 9x + cy = 5 "
                     "have no solution?",
                 steps=[
                     "No solution means the lines are parallel and distinct, so the "
                     "slopes must match.",
                     "Slope of the first: -A/B = -3/(-2) = 3/2.",
                     "Slope of the second: -9/c. Set them equal: -9/c = 3/2.",
                     "Cross multiply: -18 = 3c, so c = -6. Check the intercepts differ: "
                     "3x - 2y = 8 and 9x - 6y = 5 are 3 times the first equation on the "
                     "left but 24 against 5 on the right, so distinct. Confirmed.",
                 ],
                 answer="c = -6",
                 why="The check at the end matters. Matching slopes gives either no "
                     "solution or infinitely many, and only comparing the constants tells "
                     "you which. Skipping it gets the right answer here and the wrong one "
                     "on the version of this question that asks for infinitely many."),
        ],
        traps=[
            "Stopping at matching slopes without checking the constants, which cannot "
            "distinguish no solution from infinitely many.",
            "Adding equations without first scaling them, so nothing cancels and the "
            "result is a third equation no simpler than the first two.",
            "Solving for x and reporting it when the question asked for y, or for x + y.",
            "Reading an intersection off a graph when the coordinates are not integers "
            "and the answer choices are close together.",
        ],
        ladder={
            1: "A system solvable by one substitution with small integers.",
            2: "Elimination is needed and one equation must be scaled.",
            3: "A word problem that has to be translated into two equations first.",
            4: "A parameter is present and the question asks for no solution or "
               "infinitely many.",
            5: "The system is given in a form that hides the slopes, and comparing "
               "coefficient ratios is faster than rearranging.",
        },
    ),

    Topic(
        slug="sat-inequalities",
        title="Linear Inequalities and Systems of Them",
        area=ALG,
        skill="m_alg",
        idea="Inequalities behave exactly like equations except for one rule, and that "
             "one rule is where nearly every mistake in the topic comes from.",
        why="Inequality questions often arrive as constraints in a word problem: at most, "
            "at least, no more than. Translating those phrases correctly is most of the "
            "work, and the translation is where the exam sets its traps.",
        facts=[
            ("The one rule", "multiplying or dividing by a negative flips the sign",
             "Adding and subtracting never flip it, whatever the sign."),
            ("At least", "greater than or equal to",
             "At least 20 means 20 or more, so the boundary is included."),
            ("At most", "less than or equal to",
             "At most 20 means 20 or fewer, and the boundary is included."),
            ("More than and fewer than", "strict, boundary excluded",
             "The difference between strict and inclusive changes which endpoint counts."),
            ("Compound inequalities", "a < x < b means both at once",
             "Operate on all three parts together, and flip all of them if you multiply "
             "by a negative."),
            ("Graphing a system", "the solution is the overlap of the shaded regions",
             "A point satisfies the system only if it satisfies every inequality."),
            ("Testing a point", "substitute and see if the statement is true",
             "The fastest way to check which region or which answer choice works."),
        ],
        worked=[
            dict(ask="A crew can load at most 40 boxes per trip. Small boxes weigh 12 kg "
                     "and large boxes 30 kg, and the van carries at most 900 kg. If s is "
                     "the number of small and l the number of large boxes, write the "
                     "system.",
                 steps=[
                     "At most 40 boxes per trip: s + l <= 40. At most means the boundary "
                     "counts.",
                     "Weight: 12s + 30l <= 900.",
                     "Counts cannot be negative, so s >= 0 and l >= 0.",
                     "That is the full system; the first two are what the question is "
                     "about.",
                 ],
                 answer="s + l <= 40, 12s + 30l <= 900, with s and l at least 0",
                 why="Both constraints use at most and both therefore include the "
                     "boundary. The SAT often makes one constraint strict and one "
                     "inclusive in the same question, so read each phrase separately "
                     "rather than assuming they match."),
        ],
        traps=[
            "Not flipping the sign after dividing by a negative. This is the single most "
            "common error in the topic and it produces an answer that is on the list.",
            "Reading at most as strictly less than, which excludes a boundary value that "
            "is frequently the answer.",
            "Flipping the sign when subtracting a negative, which does not flip it.",
            "Shading the wrong side of a boundary line. Testing the origin settles it in "
            "one substitution whenever the line does not pass through it.",
        ],
        ladder={
            1: "Solve a one-step inequality with positive coefficients.",
            2: "A negative coefficient requires the flip.",
            3: "Translate at most or at least from a word problem into a constraint.",
            4: "A system of two inequalities where the question asks which point "
               "satisfies both.",
            5: "The question asks for the greatest or least value of some expression "
               "subject to the constraints, so the answer sits at a boundary.",
        },
    ),

    Topic(
        slug="sat-quadratics",
        title="Quadratic Equations and Parabolas",
        area=ADV,
        skill="m_adv",
        idea="A quadratic has three useful written forms and each one hands you a "
             "different fact for free, so the real skill is choosing the form the "
             "question is asking about.",
        why="Quadratics are the backbone of Advanced Math. Almost every question is "
            "answerable in one step from the right form and in five steps from the wrong "
            "one, and the form is usually named in the question.",
        facts=[
            ("Standard form", "y = ax^2 + bx + c",
             "c is the y-intercept, and a tells you which way it opens."),
            ("Factored form", "y = a(x - r)(x - s)",
             "r and s are the x-intercepts, read straight off."),
            ("Vertex form", "y = a(x - h)^2 + k",
             "The vertex is at (h, k), and note the sign flip on h."),
            ("The quadratic formula", "x = (-b +/- sqrt(b^2 - 4ac)) / (2a)",
             "Works always, and is slower than factoring when factoring is available."),
            ("The discriminant", "b^2 - 4ac",
             "Positive means two real solutions, zero means one, negative means none."),
            ("Axis of symmetry", "x = -b / (2a)",
             "Also the x-coordinate of the vertex, which is often what is wanted."),
            ("Sum and product of roots", "sum = -b/a, product = c/a",
             "Answers many questions without solving for either root."),
            ("Which way it opens", "a positive opens up, a negative opens down",
             "So a positive a means the vertex is a minimum."),
        ],
        worked=[
            dict(ask="The function f(x) = x^2 - 6x + 11 has its minimum at what value of "
                     "x, and what is that minimum?",
                 steps=[
                     "a is positive, so the parabola opens up and the vertex is the "
                     "minimum.",
                     "Axis of symmetry: x = -b/(2a) = 6/2 = 3.",
                     "Minimum value: f(3) = 9 - 18 + 11 = 2.",
                     "Or complete the square: x^2 - 6x + 9 + 2 = (x - 3)^2 + 2, which "
                     "gives the vertex (3, 2) directly.",
                 ],
                 answer="Minimum of 2 at x = 3",
                 why="Both routes are short here. Completing the square is worth having "
                     "because the SAT sometimes asks for the vertex form itself rather "
                     "than the vertex, and then the formula for the axis does not finish "
                     "the job."),
            dict(ask="For what values of k does x^2 + kx + 9 = 0 have exactly one real "
                     "solution?",
                 steps=[
                     "Exactly one real solution means the discriminant is zero.",
                     "b^2 - 4ac = k^2 - 4(1)(9) = k^2 - 36.",
                     "Set it to zero: k^2 = 36.",
                     "k = 6 or k = -6. Both, because squaring lost the sign.",
                 ],
                 answer="k = 6 or k = -6",
                 why="Missing the negative root is the usual loss here. Any time a square "
                     "is undone, there are two answers unless something in the question "
                     "rules one out."),
        ],
        traps=[
            "Reading the vertex of a(x - h)^2 + k as (-h, k). The form subtracts h, so "
            "y = (x - 4)^2 has its vertex at x = 4.",
            "Taking only the positive square root when solving, which silently discards "
            "half the answer.",
            "Using the quadratic formula on something that factors in five seconds, which "
            "is slower and offers more places to slip a sign.",
            "Confusing the number of real solutions with the number of x-intercepts of a "
            "shifted graph. They are the same thing, and the question sometimes asks it "
            "in the less familiar way.",
        ],
        ladder={
            1: "Factor a simple quadratic and read its roots.",
            2: "Identify the vertex from vertex form, or the intercepts from factored "
               "form.",
            3: "Complete the square, or use the axis of symmetry to find a maximum or "
               "minimum.",
            4: "A discriminant question asking for the parameter that gives a given "
               "number of solutions.",
            5: "A quadratic model in a word problem where the vertex answers a question "
               "about maximum height, revenue or area.",
        },
    ),

    Topic(
        slug="sat-polynomials",
        title="Polynomials, Factoring and Zeros",
        area=ADV,
        skill="m_adv",
        idea="A zero of a polynomial and a factor of it are the same information written "
             "two ways, and moving between them is what these questions ask you to do.",
        why="Higher degree polynomials look intimidating and are tested shallowly: the "
            "factor and remainder relationships, and reading a graph's behaviour off its "
            "factors. Knowing those two things covers nearly all of it.",
        facts=[
            ("The factor relationship", "(x - r) is a factor exactly when f(r) = 0",
             "A root and a factor are the same fact in two notations."),
            ("The remainder relationship", "dividing f(x) by (x - r) leaves f(r)",
             "So a remainder of zero means (x - r) divides it exactly."),
            ("Difference of squares", "a^2 - b^2 = (a - b)(a + b)",
             "The most useful factoring pattern on the exam by a distance."),
            ("Perfect square trinomials", "a^2 +/- 2ab + b^2 = (a +/- b)^2",
             "Recognising these saves the quadratic formula."),
            ("Sum and difference of cubes", "a^3 +/- b^3 = (a +/- b)(a^2 -/+ ab + b^2)",
             "The middle sign is opposite the first, and the last term is always plus."),
            ("Multiplicity", "a repeated factor touches the axis rather than crossing",
             "An even multiplicity bounces off, an odd one passes through."),
            ("End behaviour", "the leading term decides both ends",
             "Even degree sends both ends the same way, odd degree opposite ways."),
        ],
        worked=[
            dict(ask="If f(x) = x^3 - 4x^2 + x + 6 and f(3) = 0, factor f completely.",
                 steps=[
                     "f(3) = 0 means (x - 3) is a factor.",
                     "Divide: x^3 - 4x^2 + x + 6 by (x - 3) gives x^2 - x - 2.",
                     "Factor the quadratic: x^2 - x - 2 = (x - 2)(x + 1).",
                     "So f(x) = (x - 3)(x - 2)(x + 1), with zeros at 3, 2 and -1.",
                 ],
                 answer="(x - 3)(x - 2)(x + 1)",
                 why="The given f(3) = 0 is not decoration: it is the factor handed to "
                     "you so the cubic becomes a quadratic. When an SAT question tells you "
                     "one value of a polynomial, that value is almost always the way in."),
        ],
        traps=[
            "Reading a zero at x = 3 as the factor (x + 3). The factor that vanishes at 3 "
            "is (x - 3).",
            "Assuming every polynomial question needs long division. A given root, or a "
            "recognised pattern, usually shortcuts it.",
            "Getting the middle sign wrong in the sum or difference of cubes.",
            "Treating a repeated root as two separate x-intercepts on a graph. It is one "
            "point where the curve touches.",
        ],
        ladder={
            1: "Factor a quadratic or spot a difference of squares.",
            2: "Use a given root to find a remaining factor.",
            3: "Connect the zeros of a polynomial to the x-intercepts of its graph.",
            4: "Multiplicity determines whether the graph crosses or touches, and the "
               "question turns on that.",
            5: "The polynomial is given in an unexpanded or parameterised form and the "
               "question asks about a coefficient or a remainder without solving.",
        },
    ),

    Topic(
        slug="sat-exponentials",
        title="Exponential Functions and Growth",
        area=ADV,
        skill="m_adv",
        idea="Exponential change multiplies by a fixed factor each period, which is what "
             "separates it from linear change, and the exam tests whether you can tell "
             "them apart from a description.",
        why="Growth and decay questions are common and usually arrive in words. Deciding "
            "whether a situation is linear or exponential, and then reading the rate into "
            "the base, is most of the work.",
        facts=[
            ("General form", "y = a * b^x",
             "a is the starting amount, b is the factor per period."),
            ("Growth", "b greater than 1",
             "A 7 percent rise per period means b is 1.07."),
            ("Decay", "b between 0 and 1",
             "A 7 percent fall per period means b is 0.93, not -1.07."),
            ("From a percent rate", "b = 1 + r, with r as a decimal",
             "r is negative for decay, which gives b less than 1 automatically."),
            ("Changing the period", "y = a * b^(x/n) stretches one factor over n steps",
             "Halving every 6 years is a * (1/2)^(t/6) with t in years."),
            ("Linear versus exponential", "equal differences versus equal ratios",
             "A table growing by +5 each row is linear; one growing by times 1.5 is "
             "exponential."),
            ("Exponent rules", "b^m * b^n = b^(m+n), (b^m)^n = b^(mn), b^-n = 1/b^n",
             "The same three rules answer nearly every algebraic exponent question."),
        ],
        worked=[
            dict(ask="A culture of 500 bacteria grows by 20 percent per hour. Write the "
                     "model and find the population after 4 hours.",
                 steps=[
                     "Starting amount a = 500. A 20 percent rise gives b = 1.20.",
                     "Model: P(t) = 500 * 1.2^t, with t in hours.",
                     "After 4 hours: 500 * 1.2^4.",
                     "1.2^4 = 2.0736, so P(4) = 1036.8, about 1037 bacteria.",
                 ],
                 answer="P(t) = 500 * 1.2^t, giving about 1037 after 4 hours",
                 why="Notice 20 percent per hour for 4 hours is not 80 percent. Adding "
                     "the rate gives 900 and multiplying gives about 1037, and the "
                     "difference is exactly what makes the growth exponential. The wrong "
                     "answer of 900 will be on the list."),
        ],
        traps=[
            "Adding a percent rate over several periods instead of multiplying. This is "
            "the defining mistake of the topic.",
            "Writing decay as a negative base. A 7 percent fall is a base of 0.93; a "
            "negative base is not an exponential model at all.",
            "Missing a period conversion, such as an annual rate applied to a model "
            "measured in months.",
            "Reading a table as linear because the values rise steadily. Steady is not "
            "the test; equal differences versus equal ratios is.",
        ],
        ladder={
            1: "Evaluate an exponential expression at a given input.",
            2: "Build the model from a starting amount and a percent rate.",
            3: "Decide from a table or description whether a relationship is linear or "
               "exponential.",
            4: "The period of the model differs from the units in the question.",
            5: "Two models are compared and the question asks when one exceeds the other, "
               "which is a graph intersection rather than an algebraic solve.",
        },
    ),

    Topic(
        slug="sat-radicals-rational",
        title="Radicals and Rational Expressions",
        area=ADV,
        skill="m_adv",
        idea="Both topics are about operations that are only legal sometimes, so the real "
             "content is knowing when the operation breaks and checking whether it did.",
        why="These questions are short and carry a specific trap the SAT uses repeatedly: "
            "an answer that satisfies the transformed equation but not the original one. "
            "Checking is part of the method, not an optional extra.",
        facts=[
            ("Squaring can invent solutions", "always substitute back",
             "Squaring both sides is not reversible, so the result can satisfy more than "
             "the original did."),
            ("Extraneous solution", "a value the algebra produced that fails the original",
             "Discard it. It is not a near miss, it is not a solution."),
            ("Radicals in exponent form", "sqrt(x) = x^(1/2), cbrt(x) = x^(1/3)",
             "Turning a root into an exponent lets the exponent rules do the work."),
            ("Undefined rational expression", "the denominator cannot be zero",
             "Any value making a denominator zero is excluded from the domain."),
            ("Adding rational expressions", "common denominator first",
             "Exactly like fractions, because they are fractions."),
            ("Simplifying", "factor, then cancel common factors",
             "You may cancel factors and never terms: (x + 2)/(x + 3) cancels nothing."),
        ],
        worked=[
            dict(ask="Solve sqrt(2x + 7) = x - 4.",
                 steps=[
                     "Square both sides: 2x + 7 = x^2 - 8x + 16.",
                     "Rearrange: x^2 - 10x + 9 = 0, which factors as (x - 9)(x - 1) = 0.",
                     "Candidates x = 9 and x = 1. Now check both in the ORIGINAL.",
                     "x = 9: sqrt(25) = 5 and 9 - 4 = 5. Valid. x = 1: sqrt(9) = 3 but "
                     "1 - 4 = -3. Invalid, since the square root symbol means the "
                     "non-negative root.",
                 ],
                 answer="x = 9 only",
                 why="x = 1 is not an arithmetic slip; it is produced correctly by "
                     "squaring, which destroyed the sign information on the right side. "
                     "That is why the check is part of the method. The SAT puts x = 1, "
                     "and 'x = 1 and x = 9', among the answer choices."),
        ],
        traps=[
            "Not substituting back after squaring, which leaves an extraneous solution in "
            "the answer.",
            "Cancelling terms rather than factors in a rational expression.",
            "Forgetting that the radical symbol denotes the non-negative root, so a "
            "negative right-hand side means no solution.",
            "Ignoring excluded values when the question asks for the domain, where the "
            "excluded value is the answer.",
        ],
        ladder={
            1: "Simplify a radical or a rational expression.",
            2: "Solve a radical equation whose candidates both check out.",
            3: "One candidate is extraneous and the check is what finds it.",
            4: "The question asks for the domain or for the value that makes an "
               "expression undefined.",
            5: "A rational equation where clearing denominators introduces an excluded "
               "value that is also one of the solutions found.",
        },
    ),

    Topic(
        slug="sat-functions",
        title="Function Notation and Transformations",
        area=ADV,
        skill="m_adv",
        idea="f(x) is a rule applied to an input, and every transformation of a graph is "
             "a change to either the input or the output, which is what decides whether "
             "it moves the way you expect.",
        why="Function notation is used to make ordinary substitution look unfamiliar, and "
            "transformations are a small fixed list that is tested the same way every "
            "time. Both are cheap points once the notation stops being in the way.",
        facts=[
            ("Notation", "f(3) means put 3 everywhere x appears",
             "It is not f multiplied by 3."),
            ("Composition", "f(g(x)) means do g first, then f",
             "Work from the inside out, which is the opposite of reading order."),
            ("Vertical shift", "f(x) + k moves the graph up by k",
             "Output change, and it behaves the way it reads."),
            ("Horizontal shift", "f(x - h) moves the graph RIGHT by h",
             "Input change, and it moves opposite to the sign, which is the surprise."),
            ("Vertical stretch", "a * f(x) scales outputs by a",
             "a greater than 1 stretches, between 0 and 1 compresses."),
            ("Reflection in the x-axis", "-f(x) flips outputs",
             "Every y becomes its negative."),
            ("Reflection in the y-axis", "f(-x) flips inputs",
             "Left and right swap."),
            ("Reading a graph", "f(a) = b means the point (a, b) is on the graph",
             "Most graph questions are this fact used in one direction or the other."),
        ],
        worked=[
            dict(ask="The graph of y = f(x) passes through (2, 5). Through what point "
                     "must y = f(x + 3) - 4 pass?",
                 steps=[
                     "f(x + 3) is an input change: it shifts the graph LEFT by 3, opposite "
                     "to the sign.",
                     "So the x-coordinate 2 becomes 2 - 3 = -1.",
                     "The -4 is an output change: it shifts down by 4, so 5 becomes 1.",
                     "The point is (-1, 1). Check: at x = -1, f(-1 + 3) - 4 = f(2) - 4 = "
                     "5 - 4 = 1.",
                 ],
                 answer="(-1, 1)",
                 why="The check is the reliable part. Rather than remembering which way "
                     "the horizontal shift goes, ask what input makes the inside equal 2, "
                     "since 2 is the input you know something about. That reasoning never "
                     "goes the wrong way round."),
        ],
        traps=[
            "Shifting f(x + 3) to the right. Input changes move opposite to their sign, "
            "and this is the most reliably tested confusion in the topic.",
            "Reading f(x) as f times x, which turns a substitution question into "
            "nonsense.",
            "Doing composition in reading order rather than inside out.",
            "Applying a vertical stretch to the x-coordinates. a * f(x) scales outputs "
            "only.",
        ],
        ladder={
            1: "Evaluate f at a number, from an equation or a table.",
            2: "Read a value off a graph, or compose two simple functions.",
            3: "Apply a single transformation and identify the new graph or point.",
            4: "Two transformations at once, one of them horizontal.",
            5: "The question gives the transformed function and asks about the original, "
               "so every step runs backwards.",
        },
    ),
    Topic(
        slug="sat-ratios-rates",
        title="Ratios, Rates, Proportions and Units",
        area=PSDA,
        skill="m_psda",
        idea="A proportion is two ratios set equal, and most of these questions are won "
             "by writing the units down and checking they cancel to what was asked for.",
        why="Unit conversion and rate work run through the whole data analysis domain, "
            "and the errors are almost never arithmetic. They are setting the ratio up "
            "the wrong way round, which unit tracking catches every time.",
        facts=[
            ("Ratio", "a to b, written a:b or a/b",
             "A comparison of two quantities, not a count of either."),
            ("Part to whole", "if a:b is the ratio, the whole is a + b parts",
             "A 3:5 ratio means 3/8 and 5/8 of the total, not 3/5."),
            ("Proportion", "a/b = c/d, so ad = bc",
             "Cross multiplying is legal because both sides were equal to begin with."),
            ("Unit rate", "the amount per one unit",
             "Miles per hour, dollars per item, people per square kilometre."),
            ("Conversion factors", "multiply by a fraction equal to 1",
             "60 minutes / 1 hour equals 1, so multiplying by it changes units and not "
             "the quantity."),
            ("Track the units", "cancel them like algebra",
             "If the units do not cancel to what the question wants, the setup is upside "
             "down."),
            ("Scaling a ratio", "multiply every part by the same number",
             "A 3:5 ratio at 40 total means 3k + 5k = 40, so k = 5."),
            ("Density and similar rates", "quantity per unit of something else",
             "Same structure as speed: total equals rate times the other quantity."),
        ],
        worked=[
            dict(ask="A machine fills 250 bottles in 8 minutes. At that rate, how many "
                     "bottles does it fill in 3 hours?",
                 steps=[
                     "Rate: 250 bottles / 8 minutes.",
                     "Convert 3 hours to minutes: 3 * 60 = 180 minutes.",
                     "Multiply, tracking units: (250 bottles / 8 min) * 180 min. Minutes "
                     "cancel and bottles remain, which is what was asked for.",
                     "250 * 180 / 8 = 45000 / 8 = 5625.",
                 ],
                 answer="5625 bottles",
                 why="The unit check is the whole safeguard. Had the setup been 8/250 "
                     "times 180, the units would have come out as minutes squared per "
                     "bottle, which is visibly not a number of bottles. You do not need "
                     "to reason about whether to multiply or divide if you write the "
                     "units."),
        ],
        traps=[
            "Reading a 3:5 ratio as 3/5 of the total. It is 3/8.",
            "Mixing units in one calculation, such as a rate per minute against a time in "
            "hours.",
            "Inverting the rate, which unit tracking catches and mental arithmetic does "
            "not.",
            "Answering with the number of parts rather than the quantity, when the "
            "question asked how many rather than what fraction.",
        ],
        ladder={
            1: "A single proportion with one unknown.",
            2: "One unit conversion is needed before the proportion.",
            3: "A part to whole ratio where the total must be split into parts.",
            4: "Two conversions chained, or a rate expressed per unusual units.",
            5: "A ratio changes when a quantity is added to one side, and the new ratio "
               "gives a second equation.",
        },
    ),

    Topic(
        slug="sat-percent",
        title="Percents and Percent Change",
        area=PSDA,
        skill="m_psda",
        idea="Every percent question is a question about what the denominator is, and "
             "naming it out loud settles nearly all of them.",
        why="Percent appears throughout the section and inside other topics, and the "
            "traps are consistent: a moved base, successive changes added instead of "
            "multiplied, and points confused with percent.",
        facts=[
            ("Percent of", "percent times the whole, with percent as a decimal",
             "30 percent of 80 is 0.30 times 80."),
            ("Percent change", "(new - old) / old",
             "The denominator is the ORIGINAL value, always."),
            ("Increase by r percent", "multiply by (1 + r)",
             "A 15 percent rise is times 1.15, which is one step rather than two."),
            ("Decrease by r percent", "multiply by (1 - r)",
             "A 15 percent fall is times 0.85."),
            ("Successive changes multiply", "up 20 then down 20 is times 1.2 times 0.8",
             "Which is 0.96, a net fall of 4 percent, not a return to the start."),
            ("Reversing a change", "divide by the factor, do not subtract the percent",
             "To undo a 25 percent rise, divide by 1.25, which is a 20 percent cut."),
            ("Percentage points", "the difference between two percents",
             "4 percent to 6 percent is 2 points and a 50 percent increase."),
            ("What percent of", "part / whole, then times 100",
             "Read carefully which quantity is the whole; the wording decides it."),
        ],
        worked=[
            dict(ask="A jacket is marked down 30 percent, then a further 20 percent off "
                     "the sale price. What single percent discount is that equivalent to?",
                 steps=[
                     "First markdown: multiply by 0.70.",
                     "Second markdown applies to the SALE price: multiply by 0.80.",
                     "Combined factor: 0.70 * 0.80 = 0.56.",
                     "Paying 56 percent means a 44 percent discount.",
                 ],
                 answer="44 percent",
                 why="50 percent is the answer the question is built to produce, by "
                     "adding 30 and 20. The reason it is wrong is that the second "
                     "discount is taken on a smaller base, and that is the entire content "
                     "of the question."),
        ],
        traps=[
            "Adding successive percent changes. The wrong answer is always offered.",
            "Using the new value as the denominator in percent change.",
            "Undoing a percent increase by subtracting the same percent, which "
            "overshoots.",
            "Treating percentage points as percent, which misstates the change by "
            "whatever the base was.",
        ],
        ladder={
            1: "Take a percent of a number, or find what percent one number is of "
               "another.",
            2: "A single percent increase or decrease.",
            3: "Two successive changes that must be multiplied.",
            4: "The question gives the final value and asks for the original, so the "
               "factor must be divided out.",
            5: "A percent question embedded in a rate or a data display, where the base "
               "changes between the two figures being compared.",
        },
    ),

    Topic(
        slug="sat-statistics",
        title="Mean, Median, Spread and Outliers",
        area=PSDA,
        skill="m_psda",
        idea="Mean, median and range answer different questions about a data set, and the "
             "exam mostly tests which of them a change to the data actually moves.",
        why="These questions are quick and conceptual rather than computational. The "
            "recurring one asks what happens to each measure when a value is added or "
            "changed, and that is decided by reasoning, not by recomputing.",
        facts=[
            ("Mean", "sum divided by count",
             "Every value affects it, so an outlier drags it."),
            ("The sum trick", "sum = mean times count",
             "Most mean questions are easier as a question about the total."),
            ("Median", "the middle value when ordered",
             "With an even count, the mean of the two middle values."),
            ("Median resists outliers", "an extreme value barely moves it",
             "Which is why income and house prices are reported as medians."),
            ("Mode", "the most frequent value",
             "A set can have more than one, or none worth naming."),
            ("Range", "maximum minus minimum",
             "Only the two extremes matter, so nothing in the middle changes it."),
            ("Standard deviation", "how far values sit from the mean on average",
             "Not calculated on this exam; compared. More clustered means smaller."),
            ("Adding a constant to every value", "mean shifts, spread does not",
             "Range and standard deviation are unchanged by a shift."),
        ],
        worked=[
            dict(ask="A set of 9 numbers has a mean of 12. One value, 4, is replaced by "
                     "40. What is the new mean, and what happens to the median?",
                 steps=[
                     "Original sum: 12 * 9 = 108.",
                     "Replacing 4 with 40 adds 36 to the sum: 108 - 4 + 40 = 144.",
                     "New mean: 144 / 9 = 16.",
                     "The median: the count is unchanged at 9, and one value moved from "
                     "below the middle to above it. The middle position is now occupied "
                     "by the next value up, so the median rises slightly or stays put, "
                     "but it cannot jump to 16 the way the mean did.",
                 ],
                 answer="Mean 16; the median moves by at most one position",
                 why="This is the standard shape: one extreme change, and the question is "
                     "whether you know which measure absorbs it. The mean moved 4 points "
                     "on a single replacement; the median is anchored by position rather "
                     "than by value."),
        ],
        traps=[
            "Finding the median without ordering the values first.",
            "Assuming a change that moves the mean moves the median by a similar amount.",
            "Thinking adding a constant to every value increases the spread. It shifts "
            "the centre and leaves spread alone.",
            "Comparing standard deviations by eyeballing the range. Range uses two "
            "points; standard deviation uses all of them.",
        ],
        ladder={
            1: "Compute a mean or a median from a short list.",
            2: "Use the sum relationship to find a missing value given the mean.",
            3: "Decide which measure changes when a value is added or removed.",
            4: "Compare the spread of two data sets from a display without computing.",
            5: "A shift or a scaling is applied to every value and the question asks "
               "which measures move and by how much.",
        },
    ),

    Topic(
        slug="sat-data-inference",
        title="Samples, Margin of Error and What a Study Supports",
        area=PSDA,
        skill="m_psda",
        idea="A study supports a conclusion only about the population it sampled, and "
             "only if the sample was selected at random, which is the fact nearly every "
             "one of these questions turns on.",
        why="This is the most conceptual part of the Math section and the least like "
            "maths. The answers are about what an experiment can and cannot show, and "
            "the wrong answers are all statements that go one step too far.",
        facts=[
            ("Random selection", "lets you generalise to the population sampled",
             "Without it, the sample describes only itself."),
            ("Random assignment", "lets you claim cause",
             "Selection supports generalising; assignment supports causing. Different "
             "words, different licences."),
            ("The population is the sampled one", "not a wider one that resembles it",
             "A random sample of one school's students supports claims about that "
             "school."),
            ("Margin of error", "a range around the estimate, not a mistake",
             "An estimate of 42 percent with a 3 point margin means plausibly 39 to 45."),
            ("Larger samples narrow the interval", "more data, less uncertainty",
             "It does not fix a biased sampling method, only an imprecise one."),
            ("Bias is not cured by size", "a big biased sample is precisely wrong",
             "Voluntary response and convenience samples stay biased at any size."),
            ("Observational study", "shows association only",
             "No assignment means an alternative explanation is always available."),
        ],
        worked=[
            dict(ask="Researchers randomly selected 200 members of a gym and found those "
                     "using the new class booking app attended 20 percent more sessions. "
                     "Which conclusion is supported: (A) the app causes more attendance, "
                     "(B) among members of this gym, app users attend more sessions, "
                     "(C) app users everywhere attend more?",
                 steps=[
                     "Check selection: random, and from this gym's members. So "
                     "generalising to this gym's members is supported.",
                     "Check assignment: members chose whether to use the app. No random "
                     "assignment, so no causal claim.",
                     "(A) claims cause. Not supported.",
                     "(C) generalises beyond the sampled population. Not supported.",
                 ],
                 answer="(B)",
                 why="(B) sounds weak, and weak is what a well designed study of this "
                     "kind actually supports. The two ideas are separate: random "
                     "SELECTION buys you the population, random ASSIGNMENT buys you the "
                     "cause, and this study had only the first."),
        ],
        traps=[
            "Reading a margin of error as an error someone made rather than an interval "
            "around the estimate.",
            "Concluding cause from a study with no random assignment, which is the most "
            "common wrong answer in the topic.",
            "Generalising past the sampled population, usually to everyone.",
            "Believing a larger sample fixes a biased sampling method.",
        ],
        ladder={
            1: "Identify the population a study sampled.",
            2: "Interpret a margin of error as an interval.",
            3: "Distinguish a supported conclusion from one that generalises too far.",
            4: "Separate random selection from random assignment and say what each "
               "licenses.",
            5: "Every answer is nearly right and differs only in the strength of its "
               "claim or the breadth of its population.",
        },
    ),

    Topic(
        slug="sat-scatterplots",
        title="Scatterplots, Models and Reading Data Displays",
        area=PSDA,
        skill="m_psda",
        idea="A line or curve of best fit is a summary of the data, not the data, and "
             "every question is either about the summary or about a point, never "
             "casually about both.",
        why="Data displays carry a lot of these questions and they are fast if you check "
            "the axes first. The errors are visual: a truncated axis, a misread scale, "
            "or answering from a data point when the question asked about the model.",
        facts=[
            ("Line of best fit", "the model, not the observations",
             "Predictions come from the line; actual values come from the points."),
            ("Slope in context", "the predicted change in y per one unit of x",
             "Carries units, and the units are usually the answer."),
            ("Intercept in context", "the predicted y when x is zero",
             "Sometimes meaningless in context, which can itself be the point."),
            ("Residual", "actual minus predicted",
             "Positive means the point sits above the line."),
            ("Positive and negative association", "the direction of the trend",
             "Not a claim about cause, ever."),
            ("Check the axes first", "start value, units and scale",
             "A vertical axis starting well above zero exaggerates every difference."),
            ("Interpolation and extrapolation", "inside the data, or beyond it",
             "Predicting far outside the observed range is the unreliable case."),
        ],
        worked=[
            dict(ask="A scatterplot of study hours against test score has a line of best "
                     "fit with slope 4.2 and intercept 51. A student who studied 6 hours "
                     "scored 82. What is the residual, and what does the slope mean?",
                 steps=[
                     "Predicted score at 6 hours: 4.2(6) + 51 = 25.2 + 51 = 76.2.",
                     "Residual: actual minus predicted = 82 - 76.2 = 5.8.",
                     "Positive, so this student scored above what the model predicted.",
                     "Slope meaning: each additional hour of study is associated with a "
                     "predicted increase of 4.2 points.",
                 ],
                 answer="Residual 5.8; the slope is 4.2 predicted points per hour",
                 why="Note the wording on the slope: associated with a predicted "
                     "increase, not causes an increase. A scatterplot supports "
                     "association, and answer choices that say causes are wrong for that "
                     "reason alone, whatever the numbers."),
        ],
        traps=[
            "Reading a data point when the question asked for the predicted value, or the "
            "reverse. Residual questions need both, in the right roles.",
            "Missing a truncated or non-linear axis, which is the commonest visual trap.",
            "Describing a slope as causing rather than being associated with a change.",
            "Extrapolating far beyond the data and treating the prediction as reliable.",
        ],
        ladder={
            1: "Read a value off a graph or a table.",
            2: "Use a line of best fit to predict a value.",
            3: "Interpret the slope or intercept in the context's units.",
            4: "Compute a residual, which requires both actual and predicted.",
            5: "The display has a truncated axis or a non-linear scale, and a plausible "
               "answer assumes otherwise.",
        },
    ),

    Topic(
        slug="sat-lines-angles",
        title="Lines, Angles and Triangles",
        area=GEO,
        skill="m_geo",
        idea="Almost every geometry question on this exam reduces to angles that must sum "
             "to something, or triangles that are similar, and spotting which one it is "
             "takes seconds.",
        why="Geometry is the smallest domain on the Math section and the most rule-driven. "
            "A short list of facts covers nearly all of it, and the questions reward "
            "recognising a configuration rather than deriving anything.",
        facts=[
            ("Angles on a straight line", "sum to 180 degrees",
             "Supplementary angles, and the most used fact in the topic."),
            ("Angles around a point", "sum to 360 degrees",
             "Useful whenever several angles meet at one vertex."),
            ("Vertical angles", "opposite angles at a crossing are equal",
             "Two intersecting lines give two pairs of equal angles."),
            ("Parallel lines cut by a transversal", "corresponding and alternate angles "
             "are equal",
             "Every angle formed is one of just two values, which is the quick way to see "
             "it."),
            ("Triangle angle sum", "180 degrees",
             "Holds for every triangle without exception."),
            ("Exterior angle", "equals the sum of the two opposite interior angles",
             "Saves a step over computing the third angle first."),
            ("Isosceles triangle", "equal sides face equal angles",
             "Works in both directions, which is often the way in."),
            ("Similar triangles", "equal angles, so sides in proportion",
             "Set up a proportion of matching sides; the scale factor is the same for "
             "all of them."),
        ],
        worked=[
            dict(ask="In a triangle, two sides are equal and the angle between them is 40 "
                     "degrees. What are the other two angles?",
                 steps=[
                     "Equal sides mean the triangle is isosceles, so the two angles facing "
                     "those sides are equal.",
                     "The 40 degree angle is between the equal sides, so it is the one "
                     "that is not part of the equal pair.",
                     "The remaining two angles sum to 180 - 40 = 140 and are equal.",
                     "Each is 70 degrees.",
                 ],
                 answer="70 degrees each",
                 why="The phrase 'between them' is doing the work: it tells you which "
                     "angle is the odd one out. Had the 40 degrees been one of the base "
                     "angles instead, the answer would be 40 and 100, and the question "
                     "would look almost identical."),
        ],
        traps=[
            "Assuming a figure is drawn to scale. The SAT says when it is not, and "
            "measuring a figure that is not to scale gives a confident wrong answer.",
            "Matching the wrong sides when setting up a similar triangle proportion. "
            "Corresponding sides face corresponding angles.",
            "Missing that a triangle is isosceles because the equal sides are given as "
            "equal expressions rather than marked on the figure.",
            "Using the exterior angle rule with the adjacent interior angle instead of "
            "the two opposite ones.",
        ],
        ladder={
            1: "One angle relationship, such as a straight line or a triangle sum.",
            2: "Two relationships chained, such as parallel lines then a triangle.",
            3: "An isosceles triangle where recognising the equal angles is the step.",
            4: "Similar triangles requiring a correctly matched proportion.",
            5: "A figure where the needed relationship is not drawn, and an auxiliary "
               "observation, such as a shared angle, is what connects the two triangles.",
        },
    ),

    Topic(
        slug="sat-circles",
        title="Circles, Arcs and the Circle Equation",
        area=GEO,
        skill="m_geo",
        idea="A circle question is either about a proportion of the whole circle or about "
             "completing the square to find a centre and a radius.",
        why="Circles carry a small number of formulas that appear reliably, and the "
            "equation of a circle is the one piece of coordinate geometry here that needs "
            "an algebraic technique rather than a lookup.",
        facts=[
            ("Circumference", "C = 2 * pi * r",
             "Also pi times the diameter, which is sometimes what is given."),
            ("Area", "A = pi * r^2",
             "Radius squared, so doubling the radius quadruples the area."),
            ("Arc length", "the same fraction of the circumference as the angle is of 360",
             "A 90 degree arc is a quarter of the way round."),
            ("Sector area", "the same fraction of the area",
             "Same proportion logic as arc length, applied to area."),
            ("Radians", "a full turn is 2 * pi radians",
             "So 180 degrees is pi radians, and converting is one multiplication."),
            ("Arc length in radians", "s = r * theta",
             "Only valid with theta in radians, which is why radians exist."),
            ("Equation of a circle", "(x - h)^2 + (y - k)^2 = r^2",
             "Centre (h, k), radius r, and note the signs flip on h and k."),
            ("Completing the square", "turns the expanded form back into centre-radius "
             "form",
             "Halve the coefficient of x, square it, and add it to both sides."),
        ],
        worked=[
            dict(ask="Find the centre and radius of x^2 + y^2 - 6x + 8y = 0.",
                 steps=[
                     "Group: (x^2 - 6x) + (y^2 + 8y) = 0.",
                     "Complete the square in x: half of -6 is -3, squared is 9. Add 9 to "
                     "both sides.",
                     "Complete the square in y: half of 8 is 4, squared is 16. Add 16 to "
                     "both sides.",
                     "(x - 3)^2 + (y + 4)^2 = 25. Centre (3, -4), radius 5.",
                 ],
                 answer="Centre (3, -4), radius 5",
                 why="Both signs flip relative to what the expanded equation showed: -6x "
                     "gave centre x = 3, and +8y gave centre y = -4. And the right side "
                     "is r squared, so the radius is 5 rather than 25. Those are the two "
                     "places this question is lost."),
        ],
        traps=[
            "Reading the radius as r^2 straight off the equation instead of taking the "
            "square root.",
            "Getting the sign of the centre backwards. (x - 3)^2 means the centre is at "
            "+3.",
            "Forgetting to add the completing-the-square constants to BOTH sides.",
            "Using s = r * theta with theta in degrees, which gives a meaningless number.",
        ],
        ladder={
            1: "Apply the area or circumference formula directly.",
            2: "Find an arc length or sector area as a fraction of the whole.",
            3: "Read centre and radius from an equation already in centre-radius form.",
            4: "Complete the square to get there from the expanded form.",
            5: "A circle combined with a line or a triangle, where a radius is also a "
               "side of the other figure.",
        },
    ),

    Topic(
        slug="sat-right-triangles",
        title="Right Triangles and Trigonometry",
        area=GEO,
        skill="m_geo",
        idea="Two special triangles and three ratios cover essentially all of the "
             "trigonometry on this exam, and recognising a special triangle removes the "
             "need for any of the ratios.",
        why="Trig on the SAT is narrow and predictable. The special right triangles turn "
            "multi-step problems into one-step ones, and the sine and cosine relationship "
            "between complementary angles is tested nearly every form.",
        facts=[
            ("Pythagoras", "a^2 + b^2 = c^2",
             "c is the hypotenuse, which is always the side opposite the right angle."),
            ("Common triples", "3-4-5, 5-12-13, 8-15-17, and their multiples",
             "Recognising 6-8-10 as a scaled 3-4-5 saves the arithmetic."),
            ("The 45-45-90 triangle", "sides in ratio 1 : 1 : sqrt(2)",
             "The hypotenuse is a leg times root two."),
            ("The 30-60-90 triangle", "sides in ratio 1 : sqrt(3) : 2",
             "The short leg faces 30 degrees, and the hypotenuse is twice it."),
            ("SOH CAH TOA", "sin = opp/hyp, cos = adj/hyp, tan = opp/adj",
             "Defined from the angle you are standing at."),
            ("Complementary relationship", "sin(x) = cos(90 - x)",
             "The sine of an angle equals the cosine of its complement, which the SAT "
             "tests directly."),
            ("Similar right triangles", "the ratios depend only on the angle",
             "Which is why the trig ratios are well defined at all."),
        ],
        worked=[
            dict(ask="In a right triangle, sin(A) = 3/5. What is cos(90 - A), and what is "
                     "cos(A)?",
                 steps=[
                     "cos(90 - A) = sin(A) by the complementary relationship, so it is "
                     "3/5 with no work.",
                     "For cos(A): sin(A) = 3/5 means opposite 3, hypotenuse 5.",
                     "Recognise the 3-4-5 triple, so the adjacent side is 4.",
                     "cos(A) = adjacent / hypotenuse = 4/5.",
                 ],
                 answer="cos(90 - A) = 3/5 and cos(A) = 4/5",
                 why="The first part needs no triangle at all, only the identity, and the "
                     "SAT asks that exact question often. The second is where the triples "
                     "pay: spotting 3-4-5 replaced a Pythagoras computation."),
        ],
        traps=[
            "Assigning the hypotenuse to a leg. The hypotenuse is always opposite the "
            "right angle and always the longest side.",
            "Mixing up the short and long legs of a 30-60-90 triangle. The short leg "
            "faces the 30 degree angle.",
            "Confusing sin(x) = cos(90 - x) with sin(x) = cos(x), which is true at only "
            "one angle.",
            "Using a trig ratio in a triangle that has no right angle.",
        ],
        ladder={
            1: "Apply Pythagoras with two sides given.",
            2: "Recognise a common triple and skip the computation.",
            3: "Use a special right triangle ratio to find a missing side.",
            4: "Apply a trig ratio, or the complementary relationship, to find a value.",
            5: "The right triangle is embedded in a larger figure and has to be found "
               "before any of this applies.",
        },
    ),
    Topic(
        slug="sat-area-volume",
        title="Area, Surface Area and Volume",
        area=GEO,
        skill="m_geo",
        idea="The volume formulas are given to you on the exam, so what is actually being "
             "tested is whether you can pick the right one and handle what happens to a "
             "solid when a dimension changes.",
        why="Because the reference formulas are provided, these questions never reward "
            "memorisation. They reward reading the solid correctly and knowing how "
            "scaling works, which is the part no reference sheet gives you.",
        facts=[
            ("Rectangle and triangle", "A = lw and A = (1/2)bh",
             "The height of a triangle is perpendicular to the base, not a slanted side."),
            ("Circle", "A = pi * r^2",
             "Radius, not diameter, and the question often gives the diameter."),
            ("Prism or cylinder", "V = base area times height",
             "One rule covering both, whatever the base shape is."),
            ("Pyramid or cone", "V = (1/3) times base area times height",
             "One third of the prism with the same base and height."),
            ("Sphere", "V = (4/3) * pi * r^3",
             "Provided on the exam, like the rest of these."),
            ("Scaling a length by k", "area scales by k^2, volume by k^3",
             "Doubling every dimension multiplies volume by 8, not by 2."),
            ("Composite solids", "add or subtract whole pieces",
             "A shape with a hole is the outer volume minus the inner one."),
            ("Units", "area in square units, volume in cubic units",
             "A units mismatch in the answer choices is often the intended trap."),
        ],
        worked=[
            dict(ask="A cylindrical tank has radius 3 m and height 10 m. A second tank "
                     "has twice the radius and the same height. How many times the volume "
                     "of the first is the second?",
                 steps=[
                     "Volume of a cylinder is pi * r^2 * h.",
                     "Only the radius changed, and volume depends on r squared.",
                     "Doubling r multiplies r^2 by 4, and h is unchanged.",
                     "So the second tank holds 4 times the first. No need to compute "
                     "either volume.",
                 ],
                 answer="4 times",
                 why="8 is the tempting wrong answer, from applying the k cubed rule. "
                     "That rule is for scaling EVERY dimension. Here only one changed, "
                     "so only the exponent on that one matters, which is why it pays to "
                     "read which dimensions moved."),
        ],
        traps=[
            "Using the diameter where the formula wants the radius, which is off by a "
            "factor of 4 in area and 8 in volume.",
            "Applying the cube rule when only one dimension was scaled.",
            "Using a slant height as the perpendicular height of a triangle, cone or "
            "pyramid.",
            "Answering in the wrong units, especially when the question mixes centimetres "
            "and metres.",
        ],
        ladder={
            1: "Apply a given formula to a single solid.",
            2: "The diameter is given and the formula wants the radius.",
            3: "A composite solid formed by adding or removing a piece.",
            4: "A dimension is scaled and the question asks about the effect on volume.",
            5: "The solid is described in words with a unit change, so the setup and the "
               "conversion both have to be right.",
        },
    ),
]
