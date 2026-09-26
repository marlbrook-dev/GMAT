"""ACT Mathematics, topic by topic.

Organised by ACT's own six reporting categories, which is also how our engine scores
the section: Number and Quantity, Algebra, Functions, Geometry, Statistics and
Probability, and Integrating Essential Skills.

Two facts about this section shape everything below.

It is the broadest maths section of any exam here. Where the SAT concentrates on
algebra and data and the GMAT excludes geometry entirely, the ACT asks about
trigonometry, logarithms, matrices, complex numbers, sequences and conic sections,
mostly one question each. Breadth beats depth: a topic you have never seen costs a
point, and no topic goes very deep.

And the questions are roughly in increasing difficulty, 60 questions in 60 minutes on
the older form and 45 in 50 on the enhanced one. Either way the early questions are
worth the same as the late ones, which makes finishing the easy ones accurately more
valuable than solving the hard ones.

Same IP position as the rest of the guide: the mathematics belongs to nobody, no other
author's explanations are in here, and every exam figure carries its source.
"""
from .model import Topic

NQ, ALG, FUN, GEO, SP, IES = ("Number and Quantity", "Algebra", "Functions", "Geometry",
                              "Statistics and Probability",
                              "Integrating Essential Skills")

TOPICS = [

    Topic(
        slug="act-m-number",
        title="Number and Quantity",
        area=NQ,
        skill="act_m_nq",
        idea="Integers, exponents, roots, absolute value and the handful of exotic "
             "objects the ACT asks about once each: matrices, complex numbers and "
             "vectors.",
        why="This category is where the ACT's breadth shows most. Each exotic topic is "
            "usually one question tested shallowly, so recognising what is being asked is "
            "worth more than depth in any of them.",
        facts=[
            ("Exponent rules", "b^m * b^n = b^(m+n), (b^m)^n = b^(mn), b^-n = 1/b^n",
             "Three rules covering nearly every exponent question."),
            ("Fractional exponents", "b^(m/n) is the nth root of b to the m",
             "So x^(1/2) is the square root and x^(2/3) is the cube root squared."),
            ("Absolute value", "distance from zero, never negative",
             "|x| = 5 has two solutions, which is where its difficulty comes from."),
            ("Prime factorisation", "every integer above 1 factors uniquely",
             "The basis of factor, multiple, GCF and LCM questions."),
            ("Complex numbers", "i^2 = -1, and i cycles i, -1, -i, 1",
             "Divide the exponent by 4 and use the remainder."),
            ("Matrix addition", "add entry by entry, same dimensions only",
             "Scalar multiplication multiplies every entry."),
            ("Matrix multiplication", "row times column, inner dimensions must match",
             "An m by n times an n by p gives an m by p."),
            ("Vectors", "add component by component",
             "Magnitude is Pythagoras on the components."),
            ("Scientific notation", "one digit before the point, times a power of ten",
             "Multiply the leading numbers and add the exponents."),
        ],
        worked=[
            dict(ask="What is i^47?",
                 steps=[
                     "Powers of i cycle with period 4: i, -1, -i, 1 for exponents 1, 2, "
                     "3, 4.",
                     "Divide 47 by 4: 11 remainder 3.",
                     "A remainder of 3 corresponds to i^3.",
                     "i^3 = -i.",
                 ],
                 answer="-i",
                 why="The cycle turns an impossible-looking exponent into a division with "
                     "remainder. Every ACT complex number question of this shape is the "
                     "same three seconds of work, which is why recognising the type "
                     "matters more than understanding complex numbers deeply."),
        ],
        traps=[
            "Taking only the positive solution to an absolute value equation.",
            "Adding exponents when multiplying different bases, or multiplying them when "
            "the bases are the same.",
            "Multiplying matrices entry by entry. That is addition; multiplication is row "
            "times column.",
            "Treating i^2 as 1. It is -1, and the sign error propagates through "
            "everything after it.",
        ],
        ladder={
            1: "A direct exponent or absolute value computation.",
            2: "Fractional or negative exponents.",
            3: "A prime factorisation question, or a power of i.",
            4: "Matrix multiplication where the dimensions must be checked first.",
            5: "Two number properties combine, such as a factor condition together with a "
               "remainder one.",
        },
    ),

    Topic(
        slug="act-m-algebra",
        title="Algebra, Equations and Inequalities",
        area=ALG,
        skill="act_m_alg",
        idea="Linear and quadratic work, systems, inequalities and expressions, which "
             "underpins most of the rest of the section.",
        why="Algebra is the largest reporting category and it feeds Functions and "
            "Integrating Essential Skills as well. Speed here creates time for the "
            "breadth elsewhere.",
        facts=[
            ("Linear equations", "isolate the variable",
             "One unknown, one solution, unless the variable cancels."),
            ("Systems", "substitution when a coefficient is 1, else elimination",
             "Two equations, two unknowns."),
            ("Quadratics", "factor first, formula second",
             "x = (-b +/- sqrt(b^2 - 4ac)) / (2a) when factoring does not present itself."),
            ("Difference of squares", "a^2 - b^2 = (a - b)(a + b)",
             "The most useful factoring identity on the section."),
            ("The discriminant", "b^2 - 4ac",
             "Positive gives two real roots, zero gives one, negative gives none."),
            ("Inequalities", "flip the sign when multiplying or dividing by a negative",
             "The one rule that differs from equations."),
            ("Absolute value equations", "split into two cases",
             "|x - 3| = 7 gives x - 3 = 7 and x - 3 = -7."),
            ("Logarithms", "log base b of x equals y means b^y = x",
             "Nearly every ACT log question is that translation."),
            ("Log rules", "log(mn) = log m + log n, log(m/n) = log m - log n",
             "And log(m^k) = k log m."),
        ],
        worked=[
            dict(ask="If log base 3 of (x + 1) = 4, what is x?",
                 steps=[
                     "Translate the logarithm into exponential form: 3^4 = x + 1.",
                     "3^4 = 81.",
                     "So x + 1 = 81.",
                     "x = 80.",
                 ],
                 answer="80",
                 why="The translation is the entire question. ACT logarithm items almost "
                     "never require the log rules; they require knowing that a log IS an "
                     "exponent, so writing the exponential form first turns them into "
                     "arithmetic."),
        ],
        traps=[
            "Not flipping the inequality sign after dividing by a negative.",
            "Solving an absolute value equation as one case instead of two.",
            "Solving for x when the question asked for 2x, x + 1, or an expression.",
            "Using the quadratic formula on something that factors in five seconds.",
        ],
        ladder={
            1: "A one or two step linear equation.",
            2: "A system solved by substitution.",
            3: "A quadratic that factors, or a logarithm to translate.",
            4: "An absolute value or inequality needing case analysis.",
            5: "The question asks for an expression rather than a variable and a shortcut "
               "exists.",
        },
    ),

    Topic(
        slug="act-m-functions",
        title="Functions, Graphs and Sequences",
        area=FUN,
        skill="act_m_fun",
        idea="Function notation, transformations, and the small set of function families "
             "the ACT asks you to recognise from an equation or a graph.",
        why="Transformations and graph reading are tested every form in nearly the same "
            "way, so this is one of the most predictable categories on the section.",
        facts=[
            ("Notation", "f(3) means substitute 3 for every x",
             "Not f multiplied by 3."),
            ("Composition", "f(g(x)) means do g first",
             "Work inside out, which is the opposite of reading order."),
            ("Vertical shift", "f(x) + k moves up by k",
             "Output change, behaves as it reads."),
            ("Horizontal shift", "f(x - h) moves RIGHT by h",
             "Input change, moves opposite to the sign."),
            ("Reflections", "-f(x) flips vertically, f(-x) flips horizontally",
             "Output negated, or input negated."),
            ("Domain restrictions", "no dividing by zero, no even root of a negative",
             "These two account for nearly every domain question."),
            ("Arithmetic sequence", "a_n = a_1 + (n - 1)d",
             "Add a fixed amount each term."),
            ("Geometric sequence", "a_n = a_1 * r^(n - 1)",
             "Multiply by a fixed ratio each term."),
            ("Recognising families", "linear, quadratic, exponential, absolute value",
             "A parabola, a V shape, a curve that flattens: the graph names the family."),
            ("Period and amplitude", "y = a sin(bx) has amplitude |a| and period 2pi/b",
             "The two facts ACT trigonometry graphs ask for."),
        ],
        worked=[
            dict(ask="The graph of y = f(x) passes through (4, -2). Through what point "
                     "does y = f(x + 1) + 5 pass?",
                 steps=[
                     "Rather than recalling which way the horizontal shift goes, ask what "
                     "input makes the inside equal 4, since 4 is the input you know "
                     "about.",
                     "x + 1 = 4 gives x = 3.",
                     "At x = 3: f(3 + 1) + 5 = f(4) + 5 = -2 + 5 = 3.",
                     "So the point is (3, 3).",
                 ],
                 answer="(3, 3)",
                 why="Solving for the input rather than remembering a rule never goes the "
                     "wrong way round. The horizontal shift direction is the single most "
                     "commonly reversed fact in this category, and this method sidesteps "
                     "it entirely."),
        ],
        traps=[
            "Shifting f(x + 1) to the right. Input changes move opposite to their sign.",
            "Reading f(x) as f times x.",
            "Doing composition in reading order rather than inside out.",
            "Using the arithmetic sequence formula on a geometric sequence, which is a "
            "sign the difference rather than the ratio was checked.",
        ],
        ladder={
            1: "Evaluate a function at a number.",
            2: "Read a value off a graph, or compose two functions.",
            3: "A single transformation.",
            4: "Two transformations, one of them horizontal.",
            5: "A sequence question where the type must be identified before a formula "
               "applies.",
        },
    ),

    Topic(
        slug="act-m-geometry",
        title="Geometry and Trigonometry",
        area=GEO,
        skill="act_m_geo",
        idea="Lines, triangles, circles, solids and right triangle trigonometry, which is "
             "the widest geometry of any exam here and the shallowest per topic.",
        why="Unlike the SAT, the ACT gives you no formula sheet, so the formulas have to "
            "be known. The compensation is that each is applied directly rather than "
            "buried in a multi-step problem.",
        facts=[
            ("Triangle angle sum", "180 degrees",
             "With the exterior angle equal to the sum of the two opposite interior "
             "angles."),
            ("Pythagoras", "a^2 + b^2 = c^2",
             "With triples 3-4-5, 5-12-13 and 8-15-17 worth recognising on sight."),
            ("Special right triangles", "1 : 1 : sqrt(2) and 1 : sqrt(3) : 2",
             "The 45-45-90 and the 30-60-90."),
            ("SOH CAH TOA", "sin = opp/hyp, cos = adj/hyp, tan = opp/adj",
             "Defined from the angle you are standing at."),
            ("Law of sines", "a/sin A = b/sin B = c/sin C",
             "For triangles with no right angle, which the ACT does ask about."),
            ("Law of cosines", "c^2 = a^2 + b^2 - 2ab cos C",
             "Pythagoras with a correction term for the angle."),
            ("Circle area and circumference", "A = pi r^2, C = 2 pi r",
             "Arcs and sectors are the same fraction of each as the angle is of 360."),
            ("Circle equation", "(x - h)^2 + (y - k)^2 = r^2",
             "Centre (h, k), radius r, and the signs flip."),
            ("Volume", "prism or cylinder is base area times height",
             "Pyramid or cone is one third of that."),
            ("Slope and distance", "m = rise/run, distance is Pythagoras on the gaps",
             "Parallel lines share a slope; perpendicular slopes multiply to -1."),
            ("Scaling", "lengths by k means areas by k^2 and volumes by k^3",
             "Tested directly and reliably."),
        ],
        worked=[
            dict(ask="A cone and a cylinder have the same radius and the same height. The "
                     "cylinder holds 54 cubic cm. How much does the cone hold?",
                 steps=[
                     "Cylinder volume is base area times height.",
                     "Cone volume is one third of base area times height.",
                     "Same radius and same height means the same base area and the same "
                     "height.",
                     "So the cone is one third of 54, which is 18.",
                 ],
                 answer="18 cubic cm",
                 why="Neither volume needed computing and the radius was never used. The "
                     "relationship between the two formulas answered it. ACT geometry "
                     "rewards spotting that kind of structure, because the arithmetic is "
                     "usually the slow part."),
        ],
        traps=[
            "Assuming a figure is drawn to scale when the question does not say so.",
            "Using the diameter where the formula wants the radius.",
            "Mixing up the short and long legs of a 30-60-90 triangle. The short leg faces "
            "the 30 degree angle.",
            "Scaling an area by the length ratio instead of its square.",
        ],
        ladder={
            1: "One formula applied directly.",
            2: "Two angle relationships chained.",
            3: "A special right triangle or a recognised triple shortens the work.",
            4: "Law of sines or cosines on a non-right triangle.",
            5: "A scaling question, or a solid where a relationship between two formulas "
               "replaces the computation.",
        },
    ),

    Topic(
        slug="act-m-statistics",
        title="Statistics and Probability",
        area=SP,
        skill="act_m_sp",
        idea="Averages, spread, counting and probability, with the recurring ACT twist "
             "that the mean is usually easier handled as a question about the total.",
        why="This category is consistently winnable and consistently rushed, because it "
            "sits late in the section where time is shortest. The shortcuts here are "
            "worth knowing precisely for that reason.",
        facts=[
            ("Mean", "sum divided by count",
             "So sum equals mean times count, which is the more useful form."),
            ("Median", "middle value when ordered",
             "Order first. With an even count, average the two middle values."),
            ("Mode and range", "most frequent; maximum minus minimum",
             "Range uses only the two extremes."),
            ("Weighted average", "weight each value by how many there are",
             "Sits nearer the larger group, which is a useful sanity check."),
            ("Probability", "favourable over total",
             "For equally likely outcomes."),
            ("At least one", "1 minus the probability of none",
             "Almost always faster than adding cases."),
            ("Independent events", "multiply the probabilities",
             "For A and B when one does not affect the other."),
            ("Without replacement", "the denominator shrinks",
             "Second draw is out of one fewer."),
            ("Counting principle", "multiply the choices at each stage",
             "Four shirts and three ties gives twelve outfits."),
            ("Combinations and permutations", "order does not matter, or it does",
             "Committees are combinations; rankings and seatings are permutations."),
        ],
        worked=[
            dict(ask="A student's five test scores average 82. What must the sixth score "
                     "be to raise the average to 84?",
                 steps=[
                     "Current total: 82 * 5 = 410.",
                     "Required total for six tests at 84: 84 * 6 = 504.",
                     "The sixth score is the difference: 504 - 410 = 94.",
                     "Check: 504 / 6 = 84. Correct.",
                 ],
                 answer="94",
                 why="Working in totals rather than averages turns this into two "
                     "multiplications and a subtraction. Almost every ACT mean question "
                     "becomes simpler the moment you convert the averages into sums, "
                     "which is why the sum form of the formula is the one worth "
                     "remembering."),
        ],
        traps=[
            "Finding the median without ordering the values first.",
            "Adding cases for an at-least-one probability instead of using the "
            "complement.",
            "Forgetting the denominator shrinks on a draw without replacement.",
            "Using combinations where order matters, or permutations where it does not.",
        ],
        ladder={
            1: "Compute a mean, median or simple probability.",
            2: "Use the sum relationship to find a missing value.",
            3: "A weighted average, or a probability without replacement.",
            4: "An at-least-one question where the complement is the fast route.",
            5: "A counting question where deciding between combinations and permutations "
               "is the whole difficulty.",
        },
    ),

    Topic(
        slug="act-m-essential-skills",
        title="Integrating Essential Skills",
        area=IES,
        skill="act_m_ies",
        idea="Rates, proportions, percents, area and volume applied in multi-step word "
             "problems, which is the category that combines the others rather than "
             "adding new content.",
        why="This is the largest reporting category on the section and it contains no new "
            "mathematics. What it tests is whether you can hold a two or three step "
            "problem together without losing track of units.",
        facts=[
            ("Track the units", "cancel them like algebra",
             "If the units do not come out as what was asked for, the setup is upside "
             "down."),
            ("Rate", "distance = rate times time",
             "And the same structure for work, cost and density."),
            ("Average rate", "total distance over total time",
             "NOT the average of the two rates, which is the standard trap."),
            ("Proportion", "a/b = c/d, so ad = bc",
             "Set up with matching quantities in matching positions."),
            ("Percent change", "(new - old) / old",
             "Denominator is the original."),
            ("Successive percents multiply", "up 20 then down 20 is times 0.96",
             "A net fall of 4 percent."),
            ("Read the last line twice", "the question often asks for something derived",
             "Not x, but the total, the difference, or the amount remaining."),
            ("Estimate to check", "does the answer have a plausible size",
             "A units slip is visible without redoing the arithmetic."),
        ],
        worked=[
            dict(ask="A cyclist rides 30 km at 15 km/h and returns the same 30 km at 10 "
                     "km/h. What is the average speed for the whole trip?",
                 steps=[
                     "Average speed is total distance over total time, never the average "
                     "of the two speeds.",
                     "Out: 30 / 15 = 2 hours. Back: 30 / 10 = 3 hours.",
                     "Total distance 60 km, total time 5 hours.",
                     "60 / 5 = 12 km/h.",
                 ],
                 answer="12 km/h",
                 why="12.5 is the average of 15 and 10 and it will be among the choices. "
                     "It is wrong because more time is spent at the slower speed, so the "
                     "slow leg gets more weight. Any time two rates are averaged over the "
                     "same distance, the answer is below the arithmetic mean."),
        ],
        traps=[
            "Averaging two rates directly. The wrong answer is always offered.",
            "Mixing units, such as a rate per minute against a time in hours.",
            "Solving correctly and answering the wrong question, which is what the last "
            "line is there to catch.",
            "Adding successive percent changes.",
        ],
        ladder={
            1: "A single rate or proportion.",
            2: "One unit conversion before the computation.",
            3: "A two step word problem where an intermediate value is needed.",
            4: "An average rate question, or two successive percent changes.",
            5: "Three steps with a derived final quantity, where the last line asks for "
               "something other than the variable you solved for.",
        },
    ),
]
