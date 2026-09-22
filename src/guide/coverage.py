"""What the quant guide still owes, measured against a real reference.

The owner's standing objection to generated study material is the right one: it is
easy to write something that reads like a syllabus and quietly omits a third of the
exam, and the omission is invisible because the page looks finished. So the scope of
this guide is not decided by what got written. It is decided here, against a list of
every quant heading in the reference the owner supplied, and the build prints what is
still missing.

The list below is the CHECKLIST, not the content: headings and formula names, which
are facts about what the exam tests. What each one means, how it works, where it goes
wrong and what it looks like at each difficulty is written from scratch in the topic
files. A checklist tells you what to teach. It does not teach it.
"""

# Every quant heading in the GMAT Focus reference guide supplied 2026-09-22, in the
# order the document presents them, mapped to the topic slug that covers it.
# None means nothing covers it yet, which is what the build reports.
REFERENCE = [
    # Fractions
    ("Adding and subtracting fractions", "fractions"),
    ("Multiplying and dividing fractions", "fractions"),
    ("Reciprocals", "fractions"),
    ("Comparing fraction size by cross multiplication", "fractions"),
    ("Squares and square roots of fractions", "fractions"),
    ("Properties of a number between 0 and 1", "fractions"),
    ("The distributive property", "fractions"),
    ("Converting a fraction to a percent", "percents"),

    # Linear and quadratic equations
    ("Factoring out common factors", "quadratics"),
    ("The zero product property", "quadratics"),
    ("General form of a quadratic", "quadratics"),
    ("Factoring a quadratic", "quadratics"),
    ("FOIL", "quadratics"),
    ("The three quadratic identities", "quadratics"),
    ("Difference of squares", "quadratics"),
    ("PEMDAS and order of operations", "exponents"),

    # Properties of numbers
    ("Even and odd rules for addition and subtraction", "number-properties"),
    ("Even and odd rules for multiplication and division", "number-properties"),
    ("Sign rules for multiplication and division", "number-properties"),
    ("Factors", "factors-and-multiples"),
    ("Multiples", "factors-and-multiples"),
    ("A formula for division with remainder", "number-properties"),
    ("Divisibility rules", "number-properties"),
    ("The range of possible remainders", "number-properties"),
    ("Prime numbers below 100", "factors-and-multiples"),
    ("Counting the factors of a number", "factors-and-multiples"),
    ("Finding the LCM", "factors-and-multiples"),
    ("Finding the GCF", "factors-and-multiples"),
    ("LCM times GCF", "factors-and-multiples"),
    ("Factorials and trailing zeros", "factors-and-multiples"),
    ("Trailing zeros", "factors-and-multiples"),
    ("Leading zeros in a decimal", "number-properties"),
    ("Terminating decimals", "number-properties"),
    ("Patterns in units digits", "number-properties"),

    # Roots and exponents
    ("Perfect squares and perfect cubes", "roots"),
    ("Non-perfect square roots to memorise", "roots"),
    ("Two consecutive integers share no factor", "factors-and-multiples"),
    ("Multiplying and dividing radicals", "roots"),
    ("Adding and subtracting radicals", "roots"),
    ("Square root of a square or binomial", "roots"),
    ("Exponents to memorise", "exponents"),
    ("Multiplication and division of like bases", "exponents"),
    ("Power to a power", "exponents"),
    ("Different bases with like exponents", "exponents"),
    ("Radicals in exponential form", "roots"),
    ("Multiple square roots", "roots"),
    ("Nonzero base to the zero power", "exponents"),
    ("Negative exponents", "exponents"),
    ("Special addition rule with exponents", "exponents"),
    ("Number properties of exponents by base and exponent range", "exponents"),
    ("Square roots of large and small perfect squares", "roots"),
    ("Cube roots of large and small perfect cubes", "roots"),

    # Inequalities and absolute value
    ("Absolute value definition", "absolute-value"),
    ("Equations with one absolute value", "absolute-value"),
    ("When two absolute values are equal", "absolute-value"),
    ("Adding and subtracting absolute values", "absolute-value"),
    ("Inequalities", "inequalities"),

    # Word problems
    ("Basic word translations", "word-translations"),
    ("Price per item", "word-translations"),
    ("The profit equation", "word-translations"),
    ("Simple interest", "interest-and-growth"),
    ("Compound interest", "interest-and-growth"),
    ("Linear growth", "interest-and-growth"),
    ("Consecutive integers", "word-translations"),
    ("Consecutive even or odd integers", "word-translations"),
    ("Consecutive multiples", "word-translations"),

    # Rates and work
    ("Rate, time and distance", "rates-and-work"),
    ("Average rate", "rates-and-work"),
    ("Converging and diverging rates", "rates-and-work"),
    ("Round trip rates", "rates-and-work"),
    ("Catch up rate", "rates-and-work"),
    ("Catch up and pass", "rates-and-work"),
    ("Rate, time and work", "rates-and-work"),
    ("An object's work rate", "rates-and-work"),
    ("Combined worker formula", "rates-and-work"),

    # Ratios
    ("Three ways to express a ratio", "ratios"),
    ("What constitutes a useful ratio", "ratios"),
    ("Ratio of part to total", "ratios"),
    ("Multipart ratios and the LCM", "ratios"),

    # Percents
    ("Converting to and from a percent", "percents"),
    ("Percent of translations", "percents"),
    ("What percent translation", "percents"),
    ("Percent less than and greater than", "percents"),
    ("Variable percent translations", "percents"),
    ("Percent change", "percents"),

    # Statistics
    ("Average", "statistics"),
    ("Evenly spaced sets", "statistics"),
    ("Counting integers in a consecutive set", "statistics"),
    ("Counting multiples in a consecutive set", "statistics"),
    ("Average of a consecutive set", "statistics"),
    ("Weighted average", "statistics"),
    ("Boundaries of a weighted average", "statistics"),
    ("Median", "statistics"),
    ("Mode", "statistics"),
    ("Range", "statistics"),
    ("Standard deviation range", "statistics"),
    ("Standard deviation under a shift or a scaling", "statistics"),

    # Sets
    ("Members in either set", "sets"),
    ("Three circle Venn equations", "sets"),

    # Counting
    ("Combinations", "counting"),
    ("Permutations", "counting"),
    ("Permutations with indistinguishable items", "counting"),
    ("Circular arrangements", "counting"),

    # Probability
    ("Basic probability", "probability"),
    ("Probability of a sample space", "probability"),
    ("Complementary events", "probability"),
    ("Probability of A and B", "probability"),
    ("The addition rule", "probability"),
    ("Probability of at least one", "probability"),

    # Coordinate geometry
    ("The coordinate plane and quadrants", "coordinate-geometry"),
    ("Slope of a line", "coordinate-geometry"),
    ("Slope intercept form", "coordinate-geometry"),
    ("Positive, negative, zero and undefined slope", "coordinate-geometry"),
    ("Parallel lines", "coordinate-geometry"),
    ("Perpendicular lines", "coordinate-geometry"),
    ("Reflections", "coordinate-geometry"),
    ("The distance formula", "coordinate-geometry"),
    ("The midpoint formula", "coordinate-geometry"),

    # Functions and sequences
    ("Domain and range", "functions"),
    ("Arithmetic sequences", "sequences"),
    ("Sum of an arithmetic sequence", "sequences"),
    ("Geometric sequences", "sequences"),
]


def report(topics):
    """What is covered, what is planned but unwritten, and what nothing claims yet."""
    have = {t.slug for t in topics}
    covered, planned, orphan = [], {}, []
    for heading, slug in REFERENCE:
        if slug is None:
            orphan.append(heading)
        elif slug in have:
            covered.append(heading)
        else:
            planned.setdefault(slug, []).append(heading)
    return dict(total=len(REFERENCE), covered=covered, planned=planned, orphan=orphan)
