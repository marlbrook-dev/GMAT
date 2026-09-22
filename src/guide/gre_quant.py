"""GRE Quantitative Reasoning, topic by topic.

Four content areas, matching ETS's own division and our engine's scoring: arithmetic,
algebra, geometry, and data analysis. On top of those sits a question FORMAT that is
unique to this exam and worth a topic of its own, because the strategy for it has
nothing to do with the mathematics: quantitative comparison.

An on-screen calculator is available throughout the section. As on every exam that
provides one, the students who lose time are the ones who reach for it on questions
that were one comparison, or who compute a value when the question asked which of two
things is larger.

Same IP position as the rest of the guide: the mathematics belongs to nobody, no other
author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

FORMAT, ARITH, ALG, GEO, DATA = ("The Formats", "Arithmetic", "Algebra", "Geometry",
                                 "Data Analysis")

TOPICS = [

    Topic(
        slug="gre-quantitative-comparison",
        title="Quantitative Comparison",
        area=FORMAT,
        skill="gre_arith",
        idea="You are given two quantities and asked which is larger, which is a question "
             "you can often answer without computing either of them.",
        why="This format is unique to the GRE and it is where the most time is wasted. "
            "The four answer choices never change, and the fourth one, that the "
            "relationship cannot be determined, is what most of the difficulty is built "
            "around.",
        facts=[
            ("The four choices", "A larger, B larger, equal, or cannot be determined",
             "Identical on every question, so they are worth knowing rather than reading."),
            ("You are comparing, not solving", "the value is rarely needed",
             "If both quantities share a term, remove it from both and compare what is "
             "left."),
            ("Legal operations", "add or subtract anything from both sides",
             "Also multiply or divide both by a POSITIVE quantity."),
            ("Illegal operation", "multiplying or dividing by something that could be "
             "negative",
             "It can flip the comparison, which is the same rule as inequalities."),
            ("Test cases", "try 0, 1, a negative, and a fraction between 0 and 1",
             "These four break most comparisons that look settled."),
            ("Two different results means D", "if one case gives A and another gives B",
             "You are done immediately; no further work is needed."),
            ("D is impossible with only numbers", "if both quantities are pure numbers, "
             "one relationship holds",
             "So D can only be right when a variable is involved."),
            ("Geometry figures may mislead", "not necessarily drawn to scale",
             "A figure that looks like a right angle is not one unless it says so."),
        ],
        worked=[
            dict(ask="x is a nonzero number. Quantity A: x^2. Quantity B: x^3. Which is "
                     "larger?",
                 steps=[
                     "Try x = 2: A is 4, B is 8. B is larger.",
                     "Try x = 1/2: A is 1/4, B is 1/8. A is larger.",
                     "Two cases give opposite results, so the relationship is not "
                     "determined.",
                     "Stop here. Trying more values cannot change the answer.",
                 ],
                 answer="D, cannot be determined",
                 why="Two cases settled it in about ten seconds, and no algebra was "
                     "needed. The fraction between 0 and 1 is the case that does the "
                     "work, because raising it to a higher power makes it SMALLER, which "
                     "is the behaviour people forget."),
            dict(ask="Quantity A: 37 * 43. Quantity B: 38 * 42. Which is larger?",
                 steps=[
                     "Both are products of two numbers summing to 80.",
                     "For a fixed sum, the product is largest when the numbers are closest "
                     "together.",
                     "38 and 42 are closer than 37 and 43.",
                     "So Quantity B is larger, with no multiplication at all.",
                 ],
                 answer="B",
                 why="Both products are computable and computing them is slower and more "
                     "error prone than the structural observation. On this format, "
                     "looking for the structure first is the habit worth building, "
                     "because the questions are written to have one."),
        ],
        traps=[
            "Computing both quantities when a comparison would settle it, which costs "
            "time on a section that is short.",
            "Multiplying both sides by a variable that could be negative or zero.",
            "Choosing D whenever a variable appears. A variable makes D possible, not "
            "likely.",
            "Choosing D when both quantities are pure numbers, where D is never correct.",
        ],
        ladder={
            1: "Both quantities are numbers and one arithmetic step decides it.",
            2: "A shared term can be removed from both sides.",
            3: "A variable is present and two test cases give the same result.",
            4: "The fraction or negative case reverses what the integer case suggested.",
            5: "A structural relationship, such as a fixed sum or a symmetry, decides it "
               "and computing is impractical.",
        },
    ),

    Topic(
        slug="gre-arithmetic",
        title="Arithmetic and Number Properties",
        area=ARITH,
        skill="gre_arith",
        idea="Integers, factors, remainders, ratios and percents, which underpin every "
             "other quant topic and are where the fast structural observations live.",
        why="Arithmetic questions on the GRE are rarely about computing. They are about "
            "recognising a property, which turns a long calculation into a one-line "
            "observation.",
        facts=[
            ("Prime factorisation", "every integer above 1 factors uniquely into primes",
             "The basis of most factor, multiple and divisibility questions."),
            ("Counting factors", "add 1 to each prime exponent and multiply",
             "36 is 2^2 * 3^2, so (2+1)(2+1) = 9 factors."),
            ("Even and odd", "even times anything is even; odd times odd is odd",
             "Addition: same parity gives even, different gives odd."),
            ("Remainders", "dividend = divisor * quotient + remainder",
             "The remainder is always less than the divisor."),
            ("Percent change", "(new - old) / old",
             "Denominator is the original value, always."),
            ("Successive percents multiply", "up 20 then down 20 is times 0.96",
             "A net fall of 4 percent, not a return to the start."),
            ("Ratios are parts", "a 3:5 ratio means 3/8 and 5/8 of the whole",
             "Not 3/5, which is the standard misreading."),
            ("Absolute value", "distance from zero, never negative",
             "|x| = 5 has two solutions, which is where most of its difficulty comes "
             "from."),
        ],
        worked=[
            dict(ask="When the positive integer n is divided by 7, the remainder is 4. "
                     "What is the remainder when 3n is divided by 7?",
                 steps=[
                     "n = 7k + 4 for some integer k.",
                     "3n = 21k + 12.",
                     "21k is divisible by 7, so it contributes no remainder. The remainder "
                     "comes from 12.",
                     "12 divided by 7 leaves 5.",
                 ],
                 answer="5",
                 why="You can also just pick a number: n = 4 works, 3n = 12, remainder 5. "
                     "Picking a specific value is legitimate whenever the question's "
                     "answer does not depend on which value you chose, and remainder "
                     "questions are the clearest case of that."),
        ],
        traps=[
            "Reading a ratio as a fraction of the whole when it is a fraction of the "
            "other part.",
            "Adding successive percent changes.",
            "Taking only the positive solution to an absolute value equation.",
            "Forgetting that a remainder must be smaller than the divisor, which makes "
            "some answer choices impossible on sight.",
        ],
        ladder={
            1: "A direct computation with a percent or a ratio.",
            2: "A factor or multiple question needing prime factorisation.",
            3: "A remainder question solvable by picking a number.",
            4: "Parity or sign reasoning where the general case must be argued.",
            5: "Two properties combine, such as a remainder condition together with a "
               "divisibility one.",
        },
    ),

    Topic(
        slug="gre-algebra",
        title="Algebra, Equations and Inequalities",
        area=ALG,
        skill="gre_alg",
        idea="Linear and quadratic work, inequalities, and functions, with the recurring "
             "GRE twist that you are often asked for an expression rather than for a "
             "variable.",
        why="Algebra questions here reward noticing what is actually asked. A system you "
            "cannot solve individually may still give you x + y directly, and spotting "
            "that saves most of the work.",
        facts=[
            ("Linear equations", "isolate the variable",
             "One equation, one unknown, one solution unless the variable cancels."),
            ("Systems", "substitution or elimination",
             "Two equations, two unknowns, usually one solution."),
            ("Asked for an expression", "solve for what is asked, not for each variable",
             "Adding two equations often gives x + y in one step."),
            ("Quadratics", "factor, or use x = (-b +/- sqrt(b^2 - 4ac)) / (2a)",
             "Factoring is faster when it is available."),
            ("Difference of squares", "a^2 - b^2 = (a - b)(a + b)",
             "The most useful factoring identity on this exam."),
            ("Inequalities", "flip the sign when multiplying or dividing by a negative",
             "The one rule that behaves differently from equations."),
            ("Exponent rules", "b^m * b^n = b^(m+n), (b^m)^n = b^(mn), b^-n = 1/b^n",
             "These three cover nearly every exponent question."),
            ("Function notation", "f(3) means substitute 3 for every x",
             "Not f multiplied by 3."),
        ],
        worked=[
            dict(ask="If 3x + 2y = 17 and x + 4y = 19, what is x + y?",
                 steps=[
                     "The question asks for x + y, not for x and y separately, so look "
                     "for a shortcut before solving.",
                     "Add the two equations: 4x + 6y = 36.",
                     "Divide by 2: 2x + 3y = 18. Not directly x + y, so solve properly.",
                     "From the second equation x = 19 - 4y. Substitute: 3(19 - 4y) + 2y = "
                     "17, so 57 - 12y + 2y = 17, giving 10y = 40 and y = 4. Then x = 3, "
                     "so x + y = 7.",
                 ],
                 answer="7",
                 why="Checking for the shortcut cost five seconds and did not pay here, "
                     "which is worth showing: the habit is to look, not to assume the "
                     "shortcut exists. On the GRE it often does, and adding the equations "
                     "is the first thing to try when x + y is what is wanted."),
        ],
        traps=[
            "Solving for x and reporting it when the question asked for x + y, 2x, or "
            "1/x.",
            "Not flipping the inequality sign after dividing by a negative.",
            "Taking only the positive square root, which halves the solution set.",
            "Expanding a difference of squares the long way when the identity would have "
            "been one line.",
        ],
        ladder={
            1: "A single linear equation in one variable.",
            2: "A two-equation system solved by substitution.",
            3: "The question asks for an expression and a shortcut exists.",
            4: "A quadratic where recognising a factoring identity is what makes it "
               "quick.",
            5: "An inequality with a variable coefficient, so the sign of that variable "
               "has to be reasoned about before dividing.",
        },
    ),

    Topic(
        slug="gre-geometry",
        title="Geometry",
        area=GEO,
        skill="gre_geo",
        idea="Lines, triangles, circles and coordinate geometry, with one rule that "
             "overrides visual intuition: the figures are not necessarily drawn to scale.",
        why="Geometry on the GRE is a modest list of facts applied to figures you cannot "
            "trust. Most errors come from measuring rather than reasoning, especially on "
            "quantitative comparison questions where a figure is supplied.",
        facts=[
            ("Figures are not to scale", "unless the question says so",
             "Never measure, never assume a right angle, never assume two sides are "
             "equal."),
            ("Triangle angle sum", "180 degrees",
             "With the exterior angle equal to the sum of the two opposite interior "
             "angles."),
            ("Triangle inequality", "any two sides sum to more than the third",
             "Which bounds an unknown side between a difference and a sum."),
            ("Pythagoras", "a^2 + b^2 = c^2",
             "With the common triples 3-4-5 and 5-12-13 worth recognising."),
            ("Special right triangles", "1 : 1 : sqrt(2) and 1 : sqrt(3) : 2",
             "The 45-45-90 and the 30-60-90."),
            ("Circle", "C = 2 * pi * r and A = pi * r^2",
             "Arcs and sectors are the same fraction of each as the angle is of 360."),
            ("Similar figures", "equal angles, sides in proportion",
             "Areas scale by the square of the ratio, volumes by the cube."),
            ("Coordinate geometry", "slope, distance and midpoint formulas",
             "Distance is Pythagoras applied to the horizontal and vertical gaps."),
        ],
        worked=[
            dict(ask="Two sides of a triangle are 7 and 12. What is the range of possible "
                     "lengths for the third side?",
                 steps=[
                     "The triangle inequality: any two sides must sum to more than the "
                     "third.",
                     "Upper bound: the third side is less than 7 + 12 = 19.",
                     "Lower bound: the third side is more than 12 - 7 = 5.",
                     "So the third side is strictly between 5 and 19.",
                 ],
                 answer="Greater than 5 and less than 19",
                 why="Both bounds are strict. At exactly 5 or exactly 19 the three points "
                     "are collinear and there is no triangle. Answer choices frequently "
                     "include the endpoints for exactly that reason."),
        ],
        traps=[
            "Measuring a figure or assuming it is to scale. This is the single largest "
            "source of geometry errors on this exam.",
            "Including the endpoints in a triangle inequality range.",
            "Assuming a triangle is isosceles or right because it looks that way.",
            "Scaling an area by the length ratio instead of its square.",
        ],
        ladder={
            1: "One formula applied directly.",
            2: "Two angle relationships chained.",
            3: "A special right triangle or a common triple shortens the work.",
            4: "A figure is supplied and the answer depends on not trusting it.",
            5: "Similar figures where the question asks about area or volume, so the "
               "ratio must be squared or cubed.",
        },
    ),

    Topic(
        slug="gre-data-analysis",
        title="Data Analysis, Statistics and Probability",
        area=DATA,
        skill="gre_data",
        idea="Reading data displays, plus the statistics and counting that the GRE tests "
             "more heavily than any other exam we cover.",
        why="This is the largest single content area in GRE quant and the one with the "
            "most distinctive content: standard deviation, normal distribution and "
            "counting all appear here and mostly do not appear on the other exams.",
        facts=[
            ("Mean", "sum divided by count; sum = mean times count",
             "The second form solves most mean questions faster than the first."),
            ("Median", "the middle value when ordered",
             "Resistant to outliers, which is usually why it is being asked about."),
            ("Range and quartiles", "max minus min; the interquartile range is Q3 - Q1",
             "Boxplots on this exam are read in quartiles."),
            ("Standard deviation", "typical distance from the mean",
             "More clustered means smaller; adding a constant to every value leaves it "
             "unchanged."),
            ("Normal distribution", "about 68 percent within one standard deviation",
             "About 95 percent within two, which is the figure most questions use."),
            ("Probability", "favourable outcomes over total outcomes",
             "For equally likely outcomes."),
            ("At least one", "1 minus the probability of none",
             "Almost always faster than adding the cases."),
            ("Combinations and permutations", "order does not matter, or it does",
             "Committees are combinations; rankings and seatings are permutations."),
            ("Overlapping sets", "total = A + B minus both plus neither",
             "The two-set formula, which most set questions reduce to."),
        ],
        worked=[
            dict(ask="A bag holds 5 red and 3 blue marbles. Two are drawn without "
                     "replacement. What is the probability that at least one is blue?",
                 steps=[
                     "At least one is the complement of none, so compute the probability "
                     "that both are red.",
                     "First red: 5/8. Second red, without replacement: 4/7.",
                     "Both red: (5/8)(4/7) = 20/56 = 5/14.",
                     "At least one blue: 1 - 5/14 = 9/14.",
                 ],
                 answer="9/14",
                 why="The direct route means adding three cases: exactly one blue in two "
                     "orders, plus both blue. The complement is one multiplication and "
                     "one subtraction. Whenever a probability question says at least one, "
                     "compute the opposite first."),
        ],
        traps=[
            "Adding cases for an at-least-one question instead of using the complement.",
            "Using combinations where order matters, or permutations where it does not.",
            "Treating standard deviation as something to compute. On this exam it is "
            "compared and reasoned about, not calculated.",
            "Forgetting to subtract the overlap in a two-set problem, which double counts "
            "everyone in both.",
        ],
        ladder={
            1: "Read a value off a chart, or compute a simple mean.",
            2: "A probability with equally likely outcomes.",
            3: "An at-least-one question where the complement is the fast route.",
            4: "A counting question where deciding between combinations and permutations "
               "is the whole difficulty.",
            5: "Standard deviation or a normal distribution question answered by "
               "reasoning about spread rather than by computation.",
        },
    ),
]
