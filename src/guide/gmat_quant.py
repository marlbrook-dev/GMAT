"""GMAT Focus Quantitative Reasoning: the whole content scope, taught.

Written for this site. The mathematics here is mathematics, which belongs to nobody
and can be taught by anyone; the explanations, examples and named traps are ours.

Scope was set from two things and nothing else: the arithmetic and algebra the exam
actually asks for, and the sub-topic tags already carried by every item in our own
bank, so a guide page and the practice behind it can never describe different things.
"""
from .model import Topic

ARITHMETIC = "Arithmetic and Number Properties"
ALGEBRA = "Algebra"
WORDS = "Word Problems"
STATS = "Statistics, Sets and Counting"
COORD = "Coordinate Geometry"


TOPICS = [

Topic(
    slug="fractions", title="Fractions", area=ARITHMETIC, skill="q_vof",
    idea="A fraction is a division that has not been carried out yet, which is why it "
         "is usually easier to work with than the decimal it would turn into.",
    why="Fractions turn up inside almost every other quant topic: ratios are fractions, "
        "percents are fractions over 100, rates are fractions with units, and a "
        "probability is a fraction of outcomes. Fluency here buys speed everywhere else.",
    facts=[
        ("Adding with the same denominator", "a/b + c/b = (a + c)/b",
         "When the pieces are the same size, count them."),
        ("Adding with different denominators", "a/b + c/d = (ad + bc)/bd",
         "Rewrite both over the product of the denominators, then count."),
        ("Multiplying", "(a/b) x (c/d) = ac/bd",
         "Multiply across the top and across the bottom. No common denominator needed."),
        ("Dividing", "(a/b) / (c/d) = (a/b) x (d/c) = ad/bc",
         "Dividing by a fraction is multiplying by its reciprocal."),
        ("Reciprocal", "the reciprocal of n is 1/n",
         "The number you multiply by to get 1. Zero has none."),
        ("Comparing two fractions", "a/b > c/d exactly when ad > bc",
         "Cross multiply upward and compare the two products, with positive denominators."),
        ("A fraction squared", "(a/b)^2 = a^2/b^2",
         "The exponent reaches the top and the bottom separately."),
        ("The square root of a fraction", "sqrt(a/b) = sqrt(a)/sqrt(b)",
         "The root reaches the top and the bottom separately."),
        ("Numbers between 0 and 1", "if 0 < x < 1 then x^2 < x < sqrt(x)",
         "Squaring a proper fraction shrinks it and taking its root grows it, which is "
         "the reverse of what happens above 1."),
    ],
    worked=[
        dict(ask="Which is larger, 7/9 or 8/11?",
             steps=["Cross multiply upward: 7 x 11 = 77 sits with 7/9, and 8 x 9 = 72 "
                    "sits with 8/11.",
                    "77 > 72, and both denominators are positive, so the fraction the "
                    "larger product came from is the larger fraction."],
             answer="7/9",
             why="Cross multiplication is only a comparison of the same two fractions "
                 "rewritten over the common denominator 99. It is faster because you "
                 "never have to write the 99 down."),
        dict(ask="A tank is 3/8 full. After 12 more litres it is 5/8 full. What does it hold?",
             steps=["The 12 litres filled 5/8 - 3/8 = 2/8 = 1/4 of the tank.",
                    "If a quarter is 12 litres, the whole is 4 x 12."],
             answer="48 litres",
             why="The question is about a difference of fractions of one unknown total. "
                 "Naming the total as 1 rather than as x keeps the arithmetic in "
                 "fractions, where it is short."),
        dict(ask="If 0 < x < 1, order x, x squared, and the square root of x.",
             steps=["Try a value that is easy to take a root of: x = 1/4.",
                    "Then x squared = 1/16, x = 1/4, and sqrt(x) = 1/2.",
                    "1/16 < 1/4 < 1/2, so x squared < x < sqrt(x)."],
             answer="x squared < x < sqrt(x)",
             why="One well chosen number settles an ordering question faster than "
                 "reasoning about it in the abstract, and 1/4 is chosen because its "
                 "root is exact."),
    ],
    traps=[
        "Adding denominators. 1/2 + 1/3 is not 2/5. The denominator names the size of "
        "the piece, and pieces of different sizes cannot be counted together until they "
        "are rewritten.",
        "Assuming squaring makes a number bigger. Below 1 it makes it smaller, and the "
        "exam builds whole questions on that single fact.",
        "Cancelling across a plus sign. In (a + b)/b the b does not cancel; only a "
        "factor of the whole numerator can.",
    ],
    ladder={
        1: "Arithmetic with two friendly fractions and no context.",
        2: "One step of context in front of the arithmetic, such as a share of a total.",
        3: "Two fractions of different wholes, so you have to notice they are not "
           "comparable until one is rewritten.",
        4: "Fractions of an unknown total, where the answer is a fraction rather than a "
           "number, or a comparison you must resolve without a calculator.",
        5: "The behaviour of fractions as objects: what happens to an expression when a "
           "variable is a proper fraction, with the answer depending on the range.",
    },
),

Topic(
    slug="percents", title="Percents", area=ARITHMETIC, skill="q_rrp",
    idea="A percent is a fraction whose denominator is fixed at 100, which is the only "
         "reason percents can be compared across quantities of different sizes.",
    why="Percent change is the single most common quantitative idea in business, so it "
        "is the most common idea on this exam. It appears on its own, inside rates and "
        "ratios, and behind most of the Data Insights charts.",
    facts=[
        ("Percent to decimal", "n percent = n/100",
         "Divide by 100, or move the decimal point two places left."),
        ("Percent of a value", "n percent of v = (n/100) x v",
         "The word 'of' is a multiplication sign."),
        ("What percent", "a is (a/b) x 100 percent of b",
         "Divide the part by the whole, then scale to 100."),
        ("Percent change", "change = ((final - initial)/initial) x 100",
         "The denominator is always where you started, never where you ended."),
        ("n percent greater", "final = (1 + n/100) x initial",
         "One whole plus the increase, in one multiplication."),
        ("n percent less", "final = (1 - n/100) x initial",
         "One whole minus the decrease, in one multiplication."),
        ("Successive changes", "final = initial x (1 + r1) x (1 + r2)",
         "Percent changes multiply. They do not add."),
    ],
    worked=[
        dict(ask="A price rises 20 percent, then falls 20 percent. What is the net change?",
             steps=["Start at 100 so the arithmetic is readable.",
                    "Up 20 percent: 100 x 1.2 = 120.",
                    "Down 20 percent: 120 x 0.8 = 96.",
                    "96 against a start of 100 is a 4 percent fall."],
             answer="A 4 percent decrease",
             why="The two changes are percentages of different numbers. The rise is 20 "
                 "percent of 100 and the fall is 20 percent of 120, so the fall is "
                 "larger in absolute terms and cannot cancel the rise."),
        dict(ask="After a 15 percent discount an item costs 68 dollars. What was the "
                 "original price?",
             steps=["68 is not the discount, it is what remains: 85 percent of the original.",
                    "0.85 x original = 68.",
                    "original = 68 / 0.85 = 80."],
             answer="80 dollars",
             why="The common error is taking 15 percent of 68 and adding it back, which "
                 "answers a different question: it computes 15 percent of the new price, "
                 "not of the old one."),
        dict(ask="x is 40 percent of y, and y is 25 percent of z. x is what percent of z?",
             steps=["x = 0.4y and y = 0.25z.",
                    "Substitute: x = 0.4 x 0.25 x z = 0.1z."],
             answer="10 percent",
             why="Chained percents multiply. Reading 'of' as multiplication turns the "
                 "whole chain into one product with no equations to solve."),
    ],
    traps=[
        "Using the final value as the base of a percent change. The base is always the "
        "starting value, which is what makes a rise and a fall of the same percentage "
        "not cancel.",
        "Adding successive percentages. Up 10 then up 10 is up 21, not up 20.",
        "Confusing a percent with a percentage point. A rate moving from 4 percent to 6 "
        "percent is up 2 points and up 50 percent, and the exam will offer both numbers.",
    ],
    ladder={
        1: "One percent of one number, stated directly.",
        2: "A single percent change with the base named for you.",
        3: "Working backwards from the result to the original, where the given number is "
           "the remainder rather than the change.",
        4: "Two changes in sequence, or a percent of a percent, where the bases differ.",
        5: "Percent relationships between three quantities with no numbers at all, where "
           "the answer is an expression and every choice is a plausible rearrangement.",
    },
),

Topic(
    slug="ratios", title="Ratios and Proportions", area=ARITHMETIC, skill="q_rrp",
    idea="A ratio compares two quantities by division and deliberately throws away the "
         "actual sizes, which is why a ratio alone can never tell you how many there are.",
    why="Ratio questions are cheap for the exam to make hard: the same setup can ask for "
        "a part, a total, a difference, or what happens after a change, and each needs a "
        "different move from the same starting line.",
    facts=[
        ("Three ways to write one ratio", "a/b, a : b, a to b",
         "Identical meaning, three notations, and the exam moves between them freely."),
        ("Part to total", "if the ratio is a : b then the parts are a/(a+b) and b/(a+b)",
         "A ratio of parts becomes a fraction of the whole by adding the parts first."),
        ("The multiplier", "a : b means the quantities are ak and bk for some k",
         "Every ratio hides one unknown multiplier, and most questions are really "
         "asking you to find it."),
        ("A proportion", "a/b = c/d is the same as ad = bc",
         "Cross multiply to clear the fractions."),
        ("Combining two ratios", "x : y = 3 : 4 and x : z = 7 : 11 gives x : y : z = 21 : 28 : 33",
         "Scale both ratios so the shared term matches its least common multiple."),
        ("What is not a ratio", "(4 + m)/m is not a ratio of anything",
         "A ratio compares two quantities. An expression with a sum on top is a "
         "quantity, not a comparison."),
    ],
    worked=[
        dict(ask="A bag holds red and blue counters in the ratio 3 : 5. There are 24 more "
                 "blue than red. How many counters are there?",
             steps=["Write the counts as 3k and 5k.",
                    "The difference is 5k - 3k = 2k, and that equals 24, so k = 12.",
                    "Total = 8k = 96."],
             answer="96 counters",
             why="Naming the multiplier k turns every ratio question into one linear "
                 "equation. The only decision is which quantity the given number "
                 "describes: here a difference, not a total."),
        dict(ask="x : y = 3 : 4 and y : z = 6 : 7. Find x : y : z.",
             steps=["y appears as 4 in one ratio and 6 in the other. The least common "
                    "multiple of 4 and 6 is 12.",
                    "Scale the first by 3: x : y = 9 : 12.",
                    "Scale the second by 2: y : z = 12 : 14.",
                    "Now y agrees, so x : y : z = 9 : 12 : 14."],
             answer="9 : 12 : 14",
             why="Two ratios only join through the term they share, and they can only "
                 "join once that term is written as the same number in both."),
    ],
    traps=[
        "Treating a ratio as a count. A ratio of 3 : 5 does not mean 8 objects; it means "
        "some multiple of 8, and the question has to give you something else to pin it down.",
        "Adding ratios term by term. 1 : 2 combined with 3 : 4 is not 4 : 6.",
        "Applying the part-to-part ratio where a part-to-total fraction is wanted. In "
        "3 : 5 the red share is 3/8, not 3/5.",
    ],
    ladder={
        1: "A ratio and a total, asking for one part.",
        2: "A ratio and one part, asking for the other or for the total.",
        3: "A ratio and a difference rather than a total.",
        4: "Two ratios sharing a term, or a ratio that changes when a quantity is added "
           "to one side only.",
        5: "A ratio question with no numbers, where the answer is an expression in the "
           "original terms and the trap choices are the plausible rearrangements.",
    },
),

Topic(
    slug="rates-and-work", title="Rates, Distance and Work", area=ARITHMETIC, skill="q_rrp",
    idea="A rate is an amount divided by the time it took, and every question in this "
         "family is the same single relationship read in one of three directions.",
    why="These are the classic word problems, and they reward one habit above all: "
        "writing the units next to the numbers, because the units tell you which of the "
        "three forms of the formula you need.",
    facts=[
        ("Distance", "distance = rate x time",
         "The whole family, in one line."),
        ("Time", "time = distance / rate",
         "The same relationship solved for time."),
        ("Rate", "rate = distance / time",
         "The same relationship solved for rate."),
        ("Average rate", "average rate = total distance / total time",
         "Never the average of the rates, unless the times happen to be equal."),
        ("Work", "work done = rate x time",
         "Identical to distance, with jobs in place of miles."),
        ("Two workers together", "combined rate = rate of one + rate of the other",
         "Rates add when the work is done at the same time. Times do not add."),
        ("Closing a gap", "time to meet = gap / (difference or sum of rates)",
         "Subtract the rates when they move the same way, add them when they approach."),
    ],
    worked=[
        dict(ask="A car covers 60 miles at 30 mph, then 60 miles at 60 mph. What is its "
                 "average speed?",
             steps=["Total distance = 120 miles.",
                    "First leg takes 60/30 = 2 hours, second takes 60/60 = 1 hour, so "
                    "total time is 3 hours.",
                    "Average = 120/3 = 40 mph."],
             answer="40 mph",
             why="Not 45. The car spends twice as long at the slower speed, so the slower "
                 "speed carries more weight. Averaging the two rates would only be right "
                 "if the two times were equal, not the two distances."),
        dict(ask="One pipe fills a tank in 6 hours, another in 3 hours. How long together?",
             steps=["Rates are 1/6 and 1/3 of a tank per hour.",
                    "Combined rate = 1/6 + 1/3 = 1/6 + 2/6 = 3/6 = 1/2 tank per hour.",
                    "Time = 1 tank / (1/2 tank per hour) = 2 hours."],
             answer="2 hours",
             why="Add the rates, then invert at the end. Adding the times, or averaging "
                 "them, answers nothing: the two pipes are running at once, and the "
                 "answer must be shorter than either alone."),
    ],
    traps=[
        "Averaging two speeds. The average of the rates is only the average rate when "
        "the times are equal, and the exam nearly always makes the distances equal instead.",
        "Adding times for simultaneous work. If two machines run together the job takes "
        "less time than either alone, so any answer longer than the faster one is wrong "
        "on sight.",
        "Mismatched units. Minutes against hours, or litres per minute against a tank in "
        "litres, is where most of the lost marks in this family actually go.",
    ],
    ladder={
        1: "One rate, one time, asking for the distance or the work.",
        2: "Solving the same relationship for the rate or the time instead.",
        3: "Two legs at different rates, asking for an average.",
        4: "Two agents working together, or one catching another, with the gap given.",
        5: "Rates that change partway, or a combined-work question where one worker "
           "leaves early and the answer is a fraction of a job.",
    },
),

Topic(
    slug="number-properties", title="Number Properties", area=ARITHMETIC, skill="q_vof",
    idea="Number properties questions ask what must be true about a number from its "
         "form alone, without ever knowing which number it is.",
    why="This is where Data Sufficiency lives most comfortably: a statement about "
        "evenness or sign often settles a question without settling the number, which "
        "is exactly the distinction that question type is testing.",
    facts=[
        ("Odd and even, adding", "odd + odd = even, even + even = even, odd + even = odd",
         "Two of a kind give an even sum; a mismatch gives an odd one."),
        ("Odd and even, multiplying", "even x anything = even, odd x odd = odd",
         "A single even factor makes the whole product even."),
        ("Signs, multiplying", "(+)(+) = +, (-)(-) = +, (+)(-) = -",
         "Like signs give a positive, unlike signs give a negative."),
        ("Signs, dividing", "the same rule as multiplying",
         "Division inherits the sign rule from multiplication."),
        ("Divisible by 2", "the last digit is 0, 2, 4, 6 or 8",
         "Only the ones digit matters."),
        ("Divisible by 3", "the digits add to a multiple of 3",
         "Add the digits and test the total."),
        ("Divisible by 4", "the last two digits form a multiple of 4",
         "Only the last two digits matter."),
        ("Divisible by 5", "the last digit is 0 or 5",
         "Only the ones digit matters."),
        ("Divisible by 6", "divisible by both 2 and 3",
         "Test the two rules separately."),
        ("Divisible by 9", "the digits add to a multiple of 9",
         "The same test as 3, with a stricter total."),
        ("Remainders", "the remainder is a non-negative integer smaller than the divisor",
         "Dividing by 7 can only leave 0 through 6."),
        ("Division written out", "x/y = quotient + remainder/y",
         "Any division splits into a whole part and a leftover fraction."),
        ("Terminating decimals", "1/n terminates exactly when n reduces to only 2s and 5s",
         "1/8 and 1/20 terminate; 1/12 does not, because a 3 survives the reduction."),
        ("Leading zeros", "for integer x with k digits, 1/x has k - 1 leading zeros",
         "Unless x is a power of 10, in which case it has k - 2."),
    ],
    worked=[
        dict(ask="If n is an odd integer, must n squared plus n be even?",
             steps=["n is odd, so n squared is odd x odd = odd.",
                    "Then n squared + n is odd + odd = even."],
             answer="Yes, always",
             why="No value of n was needed. The form of the number settles it, which is "
                 "the whole point of the topic: the answer is about every odd integer "
                 "at once."),
        dict(ask="What is the remainder when 7 to the power 30 is divided by 10?",
             steps=["A remainder on division by 10 is just the units digit.",
                    "Units digits of powers of 7 cycle 7, 9, 3, 1 and then repeat every four.",
                    "30 divided by 4 leaves remainder 2, so it sits at the second place "
                    "in the cycle."],
             answer="9",
             why="Large exponents are never meant to be computed. The units digit of any "
                 "base repeats on a short cycle, so the work is finding the cycle and "
                 "then a remainder on its length."),
    ],
    traps=[
        "Forgetting that zero is even, and that it is neither positive nor negative.",
        "Assuming a variable is an integer. Unless the question says integer, x could be "
        "3/2, and most number property traps are built on exactly that.",
        "Treating a remainder as able to reach the divisor. Dividing by 5 leaves 0 to 4, "
        "never 5.",
    ],
    ladder={
        1: "Apply one divisibility rule to a given number.",
        2: "Classify an expression as odd or even from the parts.",
        3: "A remainder question with small numbers, or factors of a stated integer.",
        4: "A units digit or trailing zero question with an exponent too large to compute.",
        5: "A must-be-true question over all integers of a form, where four choices hold "
           "for the number you tried and only one holds for every number.",
    },
),

Topic(
    slug="factors-and-multiples", title="Factors, Multiples, GCF and LCM",
    area=ARITHMETIC, skill="q_vof",
    idea="Every integer above 1 is a product of primes in exactly one way, and nearly "
         "every question in this topic is that factorisation read differently.",
    why="Prime factorisation is the tool that makes counting factors, finding a greatest "
        "common factor, a least common multiple, or a count of trailing zeros into the "
        "same short piece of work.",
    facts=[
        ("Factor", "y is a factor of x when x divided by y leaves no remainder",
         "It divides in exactly."),
        ("Multiple", "a multiple of n is n times any integer",
         "The multiples of 4 are 4, 8, 12 and so on."),
        ("Counting factors", "add 1 to each prime exponent, then multiply",
         "240 = 2^4 x 3 x 5 gives (4+1)(1+1)(1+1) = 20 factors."),
        ("Greatest common factor", "take each shared prime to its smallest exponent",
         "Only primes present in both contribute."),
        ("Least common multiple", "take every prime to its largest exponent",
         "Every prime present in either contributes."),
        ("The pair rule", "GCF x LCM = the product of the two numbers",
         "Knowing three of the four values gives the fourth."),
        ("Trailing zeros", "count the pairs of 2 and 5 in the prime factorisation",
         "Each pair makes one factor of 10, and one zero on the end."),
        ("Consecutive integers", "two consecutive integers share no factor above 1",
         "Their greatest common factor is always 1."),
    ],
    worked=[
        dict(ask="How many positive factors does 240 have?",
             steps=["Prime factorise: 240 = 2^4 x 3^1 x 5^1.",
                    "Add one to each exponent: 5, 2, 2.",
                    "Multiply: 5 x 2 x 2 = 20."],
             answer="20 factors",
             why="Every factor is built by choosing an exponent for each prime, from zero "
                 "up to the exponent available. The count of choices multiplies, which is "
                 "where the add-one-then-multiply rule comes from."),
        dict(ask="Find the GCF and the LCM of 24 and 60.",
             steps=["24 = 2^3 x 3 and 60 = 2^2 x 3 x 5.",
                    "GCF takes shared primes at the smaller exponent: 2^2 x 3 = 12.",
                    "LCM takes every prime at the larger exponent: 2^3 x 3 x 5 = 120."],
             answer="GCF 12, LCM 120",
             why="A check comes free: 12 x 120 = 1440 and 24 x 60 = 1440, which is the "
                 "pair rule confirming both answers at once."),
    ],
    traps=[
        "Counting only the small factors and forgetting that 1 and the number itself "
        "both count.",
        "Swapping the GCF and LCM rules. The common factor takes the smaller exponent; "
        "the common multiple takes the larger.",
        "Counting trailing zeros by counting fives alone. It is the pairs of 2 and 5 "
        "that matter, though in a factorial the fives are usually the scarcer of the two.",
    ],
    ladder={
        1: "List the factors of a small number.",
        2: "Find the GCF or LCM of two small numbers.",
        3: "Count the factors of a number you must factorise first.",
        4: "Use the pair rule, or find trailing zeros in a product.",
        5: "A question about an unknown integer described only by its factors, where the "
           "answer is a property rather than a value.",
    },
),

Topic(
    slug="exponents", title="Exponents", area=ARITHMETIC, skill="q_vof",
    idea="An exponent counts repeated multiplication, and every exponent rule is that "
         "counting done once and then written down.",
    why="Exponent rules are the most mechanical marks on the quant section, and the "
        "questions that look hardest are usually two rules applied in order rather than "
        "anything new.",
    facts=[
        ("Same base, multiplying", "x^a x x^b = x^(a+b)",
         "Multiplying counts more copies, so the exponents add."),
        ("Same base, dividing", "x^a / x^b = x^(a-b)",
         "Dividing cancels copies, so the exponents subtract."),
        ("Power of a power", "(x^a)^b = x^(ab)",
         "b groups of a copies each, so the exponents multiply."),
        ("Different bases, same exponent", "x^a x y^a = (xy)^a",
         "A shared exponent can be factored out over a product."),
        ("A quotient to a power", "x^a / y^a = (x/y)^a",
         "The same rule, over a division."),
        ("Zero exponent", "x^0 = 1 for any non-zero x",
         "Dividing a power by itself leaves 1."),
        ("Negative exponent", "x^(-n) = 1/(x^n)",
         "A negative exponent flips the base, it does not make it negative."),
        ("Fractional exponent", "x^(1/n) is the nth root of x",
         "Roots and exponents are the same operation written two ways."),
        ("Adding like powers", "2^n + 2^n = 2^(n+1)",
         "Two copies of a power of 2 is the next power of 2."),
        ("Adding unlike powers", "x^a + x^b does not simplify by any exponent rule",
         "Factor out the smaller power instead: 2^10 + 2^11 = 2^10(1 + 2)."),
    ],
    worked=[
        dict(ask="Simplify (3^5 x 3^2) / 3^4.",
             steps=["Top: 3^5 x 3^2 = 3^7.",
                    "Divide: 3^7 / 3^4 = 3^3.",
                    "3^3 = 27."],
             answer="27",
             why="Each step is one rule. Working the powers out to numbers first would "
                 "mean multiplying 243 by 9 and dividing by 81, which is the same answer "
                 "by a much longer road."),
        dict(ask="If 2^x + 2^x + 2^x + 2^x = 2^12, what is x?",
             steps=["Four copies of 2^x is 4 x 2^x.",
                    "4 is 2^2, so this is 2^2 x 2^x = 2^(x+2).",
                    "2^(x+2) = 2^12, and with equal bases the exponents must match.",
                    "x + 2 = 12."],
             answer="x = 10",
             why="Addition of like powers is turned into multiplication first, because "
                 "there is no rule for adding exponents but there is one for multiplying "
                 "them. Rewriting 4 as a power of the same base is what joins the two sides."),
    ],
    traps=[
        "Reading a negative exponent as a negative number. 2^(-3) is 1/8, a positive number.",
        "Adding exponents when the bases differ. 2^3 x 3^3 is 6^3, not 6^6 and not 2^6.",
        "Trying to simplify a sum of powers with a product rule. x^a + x^b needs "
        "factoring, not an exponent law.",
    ],
    ladder={
        1: "One rule applied to numbers.",
        2: "Two rules in sequence, still with numeric bases.",
        3: "Negative or zero exponents, or a base that must be rewritten to match.",
        4: "An equation where both sides must be written as powers of the same base.",
        5: "A sum of powers that has to be factored, or an inequality where the answer "
           "depends on whether the base is above or below 1.",
    },
),

Topic(
    slug="roots", title="Roots and Radicals", area=ARITHMETIC, skill="q_vof",
    idea="A root is an exponent written differently, so every root rule is an exponent "
         "rule you already know, with one extra rule about signs.",
    why="Roots reward recognition rather than calculation: the exam expects you to know "
        "the perfect squares on sight and to simplify rather than approximate.",
    facts=[
        ("Multiplying roots", "sqrt(a) x sqrt(b) = sqrt(ab)",
         "Roots of the same index multiply under one sign."),
        ("Dividing roots", "sqrt(a) / sqrt(b) = sqrt(a/b)",
         "The same rule, over a division."),
        ("Adding roots", "sqrt(a) + sqrt(b) is not sqrt(a + b)",
         "There is no addition rule. sqrt(9) + sqrt(16) is 7, while sqrt(25) is 5."),
        ("Like radicals", "3 sqrt(5) + 2 sqrt(5) = 5 sqrt(5)",
         "Identical radicals are collected like identical variables."),
        ("Root as an exponent", "sqrt(x) = x^(1/2), and the nth root of x is x^(1/n)",
         "Which lets every exponent rule apply to roots."),
        ("The square root of a square", "sqrt(x^2) = the absolute value of x",
         "The radical sign means the non-negative root, so the sign information is lost."),
        ("Perfect squares to know", "1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225",
         "Recognising these on sight is most of the speed in this topic."),
        ("Approximations to know", "sqrt(2) is about 1.4, sqrt(3) about 1.7, sqrt(5) about 2.2",
         "Enough to place an answer between two choices without a calculator."),
    ],
    worked=[
        dict(ask="Simplify sqrt(72).",
             steps=["Find the largest perfect square that divides 72: 36.",
                    "72 = 36 x 2, so sqrt(72) = sqrt(36) x sqrt(2).",
                    "sqrt(36) = 6."],
             answer="6 sqrt(2)",
             why="Pulling out the largest perfect square is the whole technique. Pulling "
                 "out a smaller one, like 4, still works but leaves another step: "
                 "2 sqrt(18) has to be simplified again."),
        dict(ask="Simplify sqrt(54) / sqrt(6).",
             steps=["Combine under one radical: sqrt(54/6).",
                    "54/6 = 9.",
                    "sqrt(9) = 3."],
             answer="3",
             why="Dividing first keeps the numbers small. Simplifying each root "
                 "separately gives 3 sqrt(6) over sqrt(6), which is the same answer with "
                 "more chances to slip."),
    ],
    traps=[
        "Splitting a root across addition. sqrt(a + b) is not sqrt(a) + sqrt(b), and the "
        "exam offers that as a choice on purpose.",
        "Forgetting the absolute value. sqrt(x^2) is the size of x, not x, which matters "
        "whenever x could be negative.",
        "Leaving an answer unsimplified and not finding it among the choices, then "
        "assuming the work was wrong.",
    ],
    ladder={
        1: "Take the root of a perfect square.",
        2: "Simplify one radical by pulling out a perfect square.",
        3: "Combine radicals under multiplication or division before simplifying.",
        4: "Collect like radicals in an expression, or handle a fractional exponent.",
        5: "A question turning on the sign, where sqrt(x^2) forces a case split, or "
           "nested roots rewritten as exponents.",
    },
),

Topic(
    slug="quadratics", title="Quadratics and Factoring", area=ALGEBRA, skill="q_alg",
    idea="A quadratic is an equation whose highest power is two, and nearly every one "
         "you meet is solved by turning it into a product that equals zero.",
    why="Factoring is the workhorse of the algebra section. The exam rarely wants the "
        "quadratic formula; it wants you to see the factor pair, and it builds the "
        "numbers so that you can.",
    facts=[
        ("General form", "ax^2 + bx + c = 0",
         "A quadratic must be written this way before it can be factored."),
        ("Zero product property", "if A x B = 0 then A = 0 or B = 0",
         "A product is zero only when a factor is zero. This is why factoring solves."),
        ("Factoring when a = 1", "x^2 + bx + c = (x + p)(x + q) where pq = c and p + q = b",
         "Find the pair that multiplies to c and adds to b."),
        ("FOIL", "(x + p)(x + q) = x^2 + (p + q)x + pq",
         "First, Outside, Inside, Last: the expansion that factoring reverses."),
        ("Square of a sum", "(x + y)^2 = x^2 + 2xy + y^2",
         "The middle term is twice the product, and it is the term people forget."),
        ("Square of a difference", "(x - y)^2 = x^2 - 2xy + y^2",
         "The same identity with the middle term negative."),
        ("Difference of squares", "(x + y)(x - y) = x^2 - y^2",
         "The middle terms cancel. Worth spotting on sight."),
        ("Common factor first", "ab + ac = a(b + c)",
         "Always pull out a shared factor before anything else."),
        ("A variable can be zero", "x(x + 100) = 0 gives x = 0 or x = -100",
         "Zero is a legitimate solution, and dividing both sides by x would lose it."),
    ],
    worked=[
        dict(ask="Solve x^2 - 3x - 28 = 0.",
             steps=["Look for two numbers multiplying to -28 and adding to -3.",
                    "-7 and 4: their product is -28 and their sum is -3.",
                    "So (x - 7)(x + 4) = 0.",
                    "By the zero product property, x = 7 or x = -4."],
             answer="x = 7 or x = -4",
             why="The sign pattern does the searching for you. A negative product means "
                 "the pair has opposite signs, and a small negative sum means the larger "
                 "of the two is the negative one."),
        dict(ask="If x^2 - y^2 = 40 and x + y = 10, what is x - y?",
             steps=["x^2 - y^2 factors as (x + y)(x - y).",
                    "So 10 x (x - y) = 40.",
                    "x - y = 4."],
             answer="4",
             why="Recognising the difference of squares turns a two variable system into "
                 "one division. Solving for x and y separately reaches the same answer "
                 "and takes five times as long."),
        dict(ask="Solve 4x^2 = 12x.",
             steps=["Move everything to one side: 4x^2 - 12x = 0.",
                    "Factor out the common 4x: 4x(x - 3) = 0.",
                    "So x = 0 or x = 3."],
             answer="x = 0 or x = 3",
             why="Dividing both sides by 4x at the start looks quicker and throws away "
                 "x = 0, because you cannot divide by something that might be zero. "
                 "Moving to one side and factoring never loses a root."),
    ],
    traps=[
        "Dividing both sides by a variable. That discards the root where the variable is "
        "zero, and the exam includes that root in the answer choices.",
        "Forgetting the middle term when squaring. (x + y)^2 is not x^2 + y^2, and the "
        "difference between them is exactly 2xy.",
        "Factoring before the equation equals zero. x^2 + 5x = 6 does not factor usefully "
        "until it is written as x^2 + 5x - 6 = 0.",
    ],
    ladder={
        1: "Expand a product of two binomials.",
        2: "Factor a quadratic with a = 1 and small whole roots.",
        3: "Factor after rearranging into general form, or after pulling out a common factor.",
        4: "Recognise an identity to shortcut a system, or handle a leading coefficient "
           "other than 1.",
        5: "A quadratic in disguise, where the variable is an expression, or a question "
           "about the number of real roots rather than their values.",
    },
),

Topic(
    slug="inequalities", title="Inequalities", area=ALGEBRA, skill="q_alg",
    idea="An inequality is solved exactly like an equation with one exception, and that "
         "exception is the whole topic.",
    why="Inequalities are where Data Sufficiency does its best work, because a range of "
        "possible values often fails to answer a question that a single value would settle.",
    facts=[
        ("Adding or subtracting", "if a < b then a + c < b + c",
         "Shifting both sides by the same amount keeps the direction."),
        ("Multiplying by a positive", "if a < b and c > 0 then ac < bc",
         "A positive scaling keeps the direction."),
        ("Multiplying by a negative", "if a < b and c < 0 then ac > bc",
         "A negative scaling flips the sign. This is the exception the topic is about."),
        ("Combining two inequalities", "if a < b and b < c then a < c",
         "Inequalities chain in the same direction."),
        ("Adding two inequalities", "if a < b and c < d then a + c < b + d",
         "Same direction inequalities can be added. They cannot be subtracted."),
        ("Squaring is not safe", "a < b does not give a^2 < b^2",
         "Try -3 < 2. Squaring gives 9 > 4, and the direction reverses."),
        ("Reciprocals flip for same signs", "if 0 < a < b then 1/a > 1/b",
         "Taking reciprocals reverses the order, provided both are on the same side of zero."),
    ],
    worked=[
        dict(ask="Solve -3x + 7 > 19.",
             steps=["Subtract 7 from both sides: -3x > 12.",
                    "Divide both sides by -3, and flip the sign: x < -4."],
             answer="x < -4",
             why="The flip happens once, at the moment of dividing by a negative. "
                 "Checking one value settles it: x = -5 gives 15 + 7 = 22, which is "
                 "greater than 19, so the solution set is correct."),
        dict(ask="If 2 < x < 5 and -3 < y < 1, what is the range of x - y?",
             steps=["x - y is largest when x is largest and y is smallest: 5 - (-3) = 8.",
                    "It is smallest when x is smallest and y is largest: 2 - 1 = 1.",
                    "So 1 < x - y < 8."],
             answer="1 < x - y < 8",
             why="Subtraction means the extremes pair up crosswise. Subtracting the "
                 "inequalities term by term is not a valid move and would give the wrong "
                 "range here."),
    ],
    traps=[
        "Forgetting to flip when multiplying or dividing by a negative. This is the most "
        "common single error in the algebra section.",
        "Multiplying both sides by a variable of unknown sign. You do not know whether to "
        "flip, so the move is not available until the sign is settled.",
        "Subtracting one inequality from another. Only addition in the same direction is "
        "valid; for subtraction you have to pair the extremes crosswise.",
    ],
    ladder={
        1: "One step, with a positive coefficient.",
        2: "Two steps, including a division by a negative.",
        3: "A compound inequality solved for a range.",
        4: "Combining ranges for two variables under an operation.",
        5: "An inequality with a variable coefficient, where the answer splits into cases "
           "on the sign.",
    },
),

Topic(
    slug="absolute-value", title="Absolute Value", area=ALGEBRA, skill="q_alg",
    idea="Absolute value is distance from zero, which is why it is never negative and "
         "why an equation containing it usually has two answers rather than one.",
    why="The exam likes absolute value precisely because it produces two cases. A "
        "question that looks like it has one answer has two, and one of them is in the "
        "answer choices as a trap.",
    facts=[
        ("Definition", "the absolute value of a is a when a is at least 0, and -a when a < 0",
         "Distance from zero, so the result is never negative."),
        ("An equation splits", "if the absolute value of X is k then X = k or X = -k",
         "Two cases, always, provided k is positive."),
        ("No solution", "the absolute value of X cannot equal a negative number",
         "Distance is never negative, so such an equation has no solution at all."),
        ("Two absolute values equal", "if |A| = |B| then A = B or A = -B",
         "The insides are equal or they are opposites."),
        ("Triangle inequality", "|a + b| is at most |a| + |b|",
         "Equality holds when a and b have the same sign, or one is zero."),
        ("Subtracting", "|a - b| is at least |a| - |b|",
         "The mirror of the rule above."),
        ("Square root connection", "sqrt(x^2) = |x|",
         "Which is why a square root introduces an absolute value rather than a sign."),
    ],
    worked=[
        dict(ask="Solve |2x + 4| = 12.",
             steps=["Case one: 2x + 4 = 12, so 2x = 8 and x = 4.",
                    "Case two: 2x + 4 = -12, so 2x = -16 and x = -8."],
             answer="x = 4 or x = -8",
             why="Both must be checked against the original: |12| = 12 and |-12| = 12, "
                 "so both survive. Some absolute value equations produce a case that "
                 "fails the check, which is why checking is part of the method."),
        dict(ask="Solve |16x + 14| = |8x + 6|.",
             steps=["Case one, insides equal: 16x + 14 = 8x + 6, so 8x = -8 and x = -1.",
                    "Case two, insides opposite: 16x + 14 = -(8x + 6) = -8x - 6.",
                    "That gives 24x = -20, so x = -5/6."],
             answer="x = -1 or x = -5/6",
             why="Two absolute values give two cases, not four. Setting each side "
                 "positive and negative separately would produce four equations, of "
                 "which two are duplicates of the other two."),
    ],
    traps=[
        "Solving only the positive case. Every absolute value equation has a second case, "
        "and the exam puts the missing root among the choices.",
        "Treating |a + b| as |a| + |b|. Those are equal only when a and b share a sign.",
        "Forgetting that sqrt(x^2) is |x| rather than x, which matters the moment x could "
        "be negative.",
    ],
    ladder={
        1: "Evaluate an absolute value expression at a given number.",
        2: "Solve a single absolute value equation.",
        3: "Solve one where a case has to be rejected after checking.",
        4: "Two absolute values set equal, or an absolute value inside an inequality.",
        5: "A question about the sign or range of a variable where the absolute value is "
           "the only clue, typical of Data Sufficiency.",
    },
),

Topic(
    slug="functions", title="Functions", area=ALGEBRA, skill="q_alg",
    idea="A function is a rule that turns each input into exactly one output, and most "
         "exam questions are that rule applied carefully rather than understood deeply.",
    why="Function notation is used to make ordinary substitution look unfamiliar. Once "
        "you read f(x) as a set of instructions, most of these questions become arithmetic.",
    facts=[
        ("Notation", "f(x) means the rule f applied to the input x",
         "It is not f multiplied by x."),
        ("Evaluating", "f(3) means replace every x in the rule with 3",
         "Substitute the number everywhere x appears, then simplify."),
        ("Domain", "the set of inputs the rule can legally take",
         "Excludes anything that divides by zero or takes the root of a negative."),
        ("Range", "the set of outputs the rule can produce",
         "What comes out, across every legal input."),
        ("Composition", "f(g(x)) means apply g first, then f",
         "Work from the inside out. Order matters."),
        ("A function of an expression", "f(x + 1) means substitute the whole expression",
         "Every x in the rule becomes (x + 1), brackets included."),
    ],
    worked=[
        dict(ask="If f(x) = 2x^2 - 3x, what is f(-2)?",
             steps=["Replace each x with -2: 2(-2)^2 - 3(-2).",
                    "(-2)^2 = 4, so the first term is 2 x 4 = 8.",
                    "The second term is -3 x -2 = +6.",
                    "8 + 6 = 14."],
             answer="14",
             why="The brackets matter twice: (-2)^2 is 4, not -4, and subtracting a "
                 "negative adds. Both are where this question is designed to catch people."),
        dict(ask="If f(x) = x + 3 and g(x) = x^2, what is f(g(2)) minus g(f(2))?",
             steps=["g(2) = 4, so f(g(2)) = 4 + 3 = 7.",
                    "f(2) = 5, so g(f(2)) = 25.",
                    "7 - 25 = -18."],
             answer="-18",
             why="Composition is not commutative, and this question exists to show that. "
                 "Working inside out each time keeps the order straight."),
    ],
    traps=[
        "Reading f(x) as multiplication. f(a + b) is not f(a) + f(b) for most rules.",
        "Composing in the wrong order. f(g(x)) applies g first, and the two orders usually "
        "give different answers.",
        "Dropping brackets when the input is an expression. In f(x) = x^2, f(x + 1) is "
        "(x + 1)^2, not x^2 + 1.",
    ],
    ladder={
        1: "Evaluate a function at a number.",
        2: "Evaluate with a negative input, where sign handling matters.",
        3: "Compose two functions, or evaluate at an expression.",
        4: "Solve for an input given the output, or work with the domain.",
        5: "A defined operation with an unfamiliar symbol, where the rule is given in the "
           "question and nothing is memorised.",
    },
),

Topic(
    slug="word-translations", title="Word Problems and Translations", area=WORDS,
    skill="q_alg",
    idea="A word problem is an equation written in English, and translating it is a "
         "mechanical job once you know which English word maps to which symbol.",
    why="Most lost marks in this family are lost in the translation, not the algebra. "
        "The arithmetic is usually easy; deciding what to call x is what takes the time.",
    facts=[
        ("is, was, has been", "=",
         "Any form of the verb to be is an equals sign."),
        ("more than, greater than, older than", "+",
         "Addition, and the order of the two quantities does not matter."),
        ("less than, fewer than, younger than", "-",
         "Subtraction, and here the order DOES matter: 5 less than x is x - 5."),
        ("of", "x",
         "Multiplication, especially after a fraction or a percent."),
        ("times, factor, product", "x",
         "All three of these words mean multiply the two quantities."),
        ("per, for each, ratio of", "/",
         "Each of these words puts the quantity that follows underneath."),
        ("Price per item", "price per item = total cost / number of items",
         "The word per is the division bar."),
        ("Profit", "profit = total revenue - total cost",
         "Or revenue minus fixed costs minus variable costs."),
        ("Consecutive integers", "x, x + 1, x + 2, and so on",
         "Each is one more than the last."),
        ("Consecutive even or odd", "x, x + 2, x + 4, and so on",
         "Both families step by two; only the starting parity differs."),
        ("Consecutive multiples of n", "x, x + n, x + 2n, and so on",
         "Step by the multiple."),
    ],
    worked=[
        dict(ask="Five less than three times a number is 22. What is the number?",
             steps=["Call the number x. Three times it is 3x.",
                    "Five less than that is 3x - 5, not 5 - 3x.",
                    "3x - 5 = 22, so 3x = 27 and x = 9."],
             answer="9",
             why="'Less than' reverses the order of what you read. This is the single "
                 "most common translation error, and the exam offers 5 - 3x = 22 as a "
                 "path to a wrong answer that is in the choices."),
        dict(ask="The sum of three consecutive even integers is 48. What is the largest?",
             steps=["Call them x, x + 2 and x + 4.",
                    "Their sum is 3x + 6 = 48, so 3x = 42 and x = 14.",
                    "The largest is x + 4 = 18."],
             answer="18",
             why="Naming the smallest as x is a habit worth keeping: it makes every other "
                 "term an addition. The final step matters too, since the question asks "
                 "for the largest rather than for x."),
    ],
    traps=[
        "Reversing 'less than'. Five less than x is x - 5. Reading left to right gives "
        "5 - x, which is a different number and usually an answer choice.",
        "Answering for x when the question asked for something built from x, such as the "
        "largest of three integers or the total rather than the part.",
        "Using one variable where the problem has two independent quantities, which forces "
        "a guess rather than a solve.",
    ],
    ladder={
        1: "One sentence, one operation.",
        2: "Two operations in one sentence, with order mattering.",
        3: "Two quantities related to each other, solved as a small system.",
        4: "A setup where the question asks for a combination rather than for the variable.",
        5: "A translation with no numbers, where the answer is an expression and every "
           "choice is a plausible misreading of the same sentence.",
    },
),

Topic(
    slug="interest-and-growth", title="Interest and Growth", area=WORDS, skill="q_rrp",
    idea="Simple interest adds the same amount each period; compound interest multiplies "
         "by the same factor each period, and that single difference is the topic.",
    why="Compound growth is the business idea the exam cares most about, and it is the "
        "same mathematics as population growth, depreciation and any repeated percent change.",
    facts=[
        ("Simple interest", "interest = principal x rate x time",
         "The interest is computed on the original amount every period."),
        ("Compound interest", "A = P(1 + r/n)^(nt)",
         "P is the principal, r the annual rate, n the compoundings per year, t the years."),
        ("Annual compounding", "A = P(1 + r)^t",
         "The same formula with n = 1."),
        ("Linear growth", "final = kn + p",
         "A constant amount k added for each of n periods, starting from p."),
        ("Growth as repeated percent change", "A = P x (1 + r)^t",
         "Compound growth is just the same percent change applied over and over."),
        ("Decay", "A = P(1 - r)^t",
         "The same formula with the rate subtracted instead of added."),
    ],
    worked=[
        dict(ask="1,000 dollars at 10 percent annual simple interest for 3 years. What "
                 "is the interest?",
             steps=["Simple interest = 1000 x 0.10 x 3.",
                    "= 300."],
             answer="300 dollars",
             why="Each year earns 100, computed on the original 1,000 every time. Nothing "
                 "is ever earned on the interest, which is exactly what makes it simple."),
        dict(ask="1,000 dollars at 10 percent compounded annually for 3 years. What is "
                 "the balance?",
             steps=["A = 1000 x (1.1)^3.",
                    "1.1^2 = 1.21, and 1.21 x 1.1 = 1.331.",
                    "A = 1,331."],
             answer="1,331 dollars",
             why="331 of interest against 300 for simple interest. The extra 31 is the "
                 "interest earned on interest, and it is the whole point of the "
                 "distinction the question is testing."),
    ],
    traps=[
        "Using the compound formula with the number of years where the number of "
        "compounding periods is wanted. Quarterly for 2 years is 8 periods at a quarter "
        "of the annual rate.",
        "Adding the rate rather than multiplying by one plus the rate. Growth of 10 "
        "percent multiplies by 1.1, it does not add 1.1.",
        "Treating compound interest as simple interest times a fudge factor. Over a few "
        "periods the gap is small, and the exam picks numbers where the difference is "
        "exactly one answer choice apart.",
    ],
    ladder={
        1: "One period of simple interest.",
        2: "Several periods of simple interest, or one of compound.",
        3: "Compound interest over two or three periods, computed by hand.",
        4: "Compounding more often than annually, so the rate and the period both change.",
        5: "Comparing two growth schemes, where the answer is which is larger rather than "
           "by how much.",
    },
),

Topic(
    slug="statistics", title="Statistics", area=STATS, skill="q_csp",
    idea="Every statistic on this exam is a single number summarising a set, and the "
         "questions are about what that number does and does not tell you.",
    why="Statistics appears in Quant and again behind most of Data Insights. Knowing how "
        "the mean reacts to an added value, and how the standard deviation does not react "
        "to a shift, answers a surprising number of questions on its own.",
    facts=[
        ("Average", "average = sum of terms / number of terms",
         "Which rearranges to sum = average x count, the form most questions need."),
        ("Evenly spaced sets", "in an evenly spaced set the mean equals the median",
         "True of consecutive integers, evens, odds and any arithmetic sequence."),
        ("Average of a consecutive set", "average = (first + last) / 2",
         "Because the set is symmetric about its centre."),
        ("Counting a consecutive set", "count = last - first + 1",
         "The plus one is for the endpoint you would otherwise drop."),
        ("Counting multiples in a range", "count = (last multiple - first multiple)/n + 1",
         "The same idea, stepping by n."),
        ("Weighted average", "weighted average = sum of (value x weight) / sum of weights",
         "Ordinary averaging is the special case where the weights are equal."),
        ("Weighted average boundaries", "the result lies between the two values, nearer "
         "the heavier one",
         "Which often settles a question without any arithmetic."),
        ("Median, odd count", "the middle value once ordered",
         "At position (n + 1)/2."),
        ("Median, even count", "the average of the two middle values",
         "At positions n/2 and n/2 + 1."),
        ("Mode", "the value that appears most often",
         "A set can have several modes, or none worth naming."),
        ("Range", "range = largest - smallest",
         "It uses only two members and ignores everything between them."),
        ("Standard deviation", "a measure of how far the values sit from the mean",
         "Larger when the values are spread out, zero when they are all identical."),
        ("Shifting a set", "adding a constant to every term leaves the standard deviation "
         "unchanged",
         "Every value moves together, so the spread is untouched."),
        ("Scaling a set", "multiplying every term by k multiplies the standard deviation by |k|",
         "Stretching the set stretches the spread."),
    ],
    worked=[
        dict(ask="A set of 5 numbers averages 12. A sixth number is added and the average "
                 "becomes 13. What was it?",
             steps=["The first five sum to 5 x 12 = 60.",
                    "The six together sum to 6 x 13 = 78.",
                    "The new number is 78 - 60 = 18."],
             answer="18",
             why="Averages are converted to sums immediately. Sums add; averages do not, "
                 "and almost every average question becomes easy at the moment you write "
                 "sum = average x count."),
        dict(ask="A class of 10 averages 70 and a class of 30 averages 90. What is the "
                 "combined average?",
             steps=["Total = 10 x 70 + 30 x 90 = 700 + 2700 = 3400.",
                    "Count = 40.",
                    "Average = 3400/40 = 85."],
             answer="85",
             why="Not 80. The larger class pulls the result toward 90, and the answer must "
                 "land between 70 and 90 nearer the heavier side. That check alone "
                 "eliminates the average-of-the-averages trap answer."),
    ],
    traps=[
        "Averaging two averages. That is only correct when the two groups are the same "
        "size, and the exam almost always makes them different sizes.",
        "Assuming the mean equals the median. That holds for evenly spaced sets, not in "
        "general, and a single outlier separates them.",
        "Thinking a shift changes the standard deviation. Adding 10 to every value moves "
        "the mean by 10 and leaves the spread exactly as it was.",
    ],
    ladder={
        1: "Compute an average from a short list.",
        2: "Work backwards from an average to a missing value.",
        3: "Combine two groups with a weighted average, or find a median from an ordered set.",
        4: "Reason about how a statistic reacts to a change in the set.",
        5: "Compare the spread of two sets, or determine what must be true about a set "
           "from partial information, typical of Data Sufficiency.",
    },
),

Topic(
    slug="sets", title="Overlapping Sets", area=STATS, skill="q_csp",
    idea="An overlapping sets question is about double counting: anything in two groups "
         "gets counted twice unless you take it back out once.",
    why="Two and three circle problems look like puzzles and are really one formula. The "
        "difficulty is almost always in reading which region a given number describes.",
    facts=[
        ("Two sets", "total in A or B = A + B - (A and B)",
         "Add the two groups, then subtract the overlap you counted twice."),
        ("Two sets with a neither", "total = A + B - (A and B) + neither",
         "Everything outside both groups still belongs to the total."),
        ("Three sets", "A or B or C = A + B + C - (AB) - (AC) - (BC) + (ABC)",
         "Subtract each pairwise overlap, then add back the middle, which was removed "
         "three times and added three times."),
        ("Exactly two", "members in exactly two groups = (AB) + (AC) + (BC) - 3(ABC)",
         "Each pairwise count includes the triple overlap, so remove it three times."),
        ("From a table", "for two attributes, a two by two table is faster than a diagram",
         "Rows and columns each sum to their totals, which fills the table in."),
    ],
    worked=[
        dict(ask="In a group of 100, 60 play football, 45 play tennis, and 20 play both. "
                 "How many play neither?",
             steps=["Playing at least one = 60 + 45 - 20 = 85.",
                    "Neither = 100 - 85 = 15."],
             answer="15",
             why="The 20 who play both were counted once inside the 60 and once inside "
                 "the 45. Subtracting them once leaves each person counted exactly once, "
                 "which is what 'at least one' means."),
        dict(ask="Of 50 people, 30 like coffee, 25 like tea, and 5 like neither. How many "
                 "like both?",
             steps=["At least one = 50 - 5 = 45.",
                    "45 = 30 + 25 - both, so 45 = 55 - both.",
                    "both = 10."],
             answer="10",
             why="The same formula read backwards. Building the table or the diagram is "
                 "optional here; what is not optional is noticing that 30 + 25 exceeds "
                 "45, and the excess is exactly the overlap."),
    ],
    traps=[
        "Confusing 'both' with 'only'. If 20 play both, the number who play only football "
        "is 60 - 20 = 40, and the exam offers both numbers.",
        "Forgetting the neither group. The two circles do not have to fill the total.",
        "In three set problems, subtracting the triple overlap once instead of handling it "
        "properly. It is removed three times by the pairwise terms and has to come back.",
    ],
    ladder={
        1: "Two sets with the overlap given, asking for the union.",
        2: "Two sets working backwards to the overlap.",
        3: "Two sets with a neither group included.",
        4: "A two by two table with one cell missing.",
        5: "Three sets, or a question distinguishing exactly two from at least two.",
    },
),

Topic(
    slug="counting", title="Combinations and Permutations", area=STATS, skill="q_csp",
    idea="Counting questions come down to one decision: does the order of what you chose "
         "matter, or not.",
    why="Getting the order question right is worth more than knowing either formula, "
        "because the two formulas differ by exactly the factor that order introduces.",
    facts=[
        ("Order does not matter", "combinations",
         "A committee, a handshake, a selection of flavours."),
        ("Order does matter", "permutations",
         "A ranking, a password, seats in a row, first and second place."),
        ("Combination formula", "nCk = n! / ((n - k)! x k!)",
         "Choose k from n, ignoring order."),
        ("Permutation formula", "nPk = n! / (n - k)!",
         "Arrange k out of n, where order counts."),
        ("The relationship", "nPk = nCk x k!",
         "A permutation is a combination whose k chosen items are then arranged."),
        ("Repeated items", "n! / (r1! x r2! x ...)",
         "Divide by the factorial of each repeat count. AABB arranges in 4!/(2!2!) = 6 ways."),
        ("Circular arrangements", "(k - 1)!",
         "One seat is fixed to kill the rotations that are the same arrangement."),
        ("The counting principle", "independent choices multiply",
         "3 shirts and 4 ties give 12 outfits."),
    ],
    worked=[
        dict(ask="How many ways can a committee of 3 be chosen from 8 people?",
             steps=["A committee has no order, so this is a combination.",
                    "8C3 = 8! / (5! x 3!) = (8 x 7 x 6) / (3 x 2 x 1).",
                    "= 336/6 = 56."],
             answer="56",
             why="Cancelling before multiplying keeps the numbers small. Writing out 8! is "
                 "never necessary: only the top few factors survive the division."),
        dict(ask="How many arrangements of the letters in the word LEVEL?",
             steps=["5 letters, with L appearing twice and E appearing twice.",
                    "5! / (2! x 2!) = 120/4.",
                    "= 30."],
             answer="30",
             why="Without the division, swapping the two Ls would count as a new "
                 "arrangement, and it is not: the word looks identical. Each repeated "
                 "letter divides out its own factorial."),
    ],
    traps=[
        "Using a permutation where order does not matter. That overcounts by k!, and the "
        "overcounted number is in the answer choices.",
        "Forgetting to divide by repeats. Arrangements of a word with a doubled letter "
        "are half what they first appear.",
        "Adding when the choices are independent. Independent stages multiply; addition is "
        "for cases that cannot both happen.",
    ],
    ladder={
        1: "A direct application of the counting principle.",
        2: "One combination or one permutation, clearly signalled.",
        3: "Deciding which of the two applies from the wording.",
        4: "Arrangements with repeated items, or a restriction on one position.",
        5: "A count split into cases that are added, each case a product, with a "
           "restriction that removes some of them.",
    },
),

Topic(
    slug="probability", title="Probability", area=STATS, skill="q_csp",
    idea="A probability is a count of favourable outcomes over a count of possible ones, "
         "which makes most probability questions counting questions in disguise.",
    why="The exam keeps the arithmetic small and puts the difficulty in deciding what to "
        "count, and in choosing between the and rule, the or rule and the complement.",
    facts=[
        ("Basic probability", "P = favourable outcomes / total outcomes",
         "Both counts must describe the same sample space."),
        ("A sample space", "the probabilities of all outcomes sum to 1",
         "Which is the check that a set of probabilities is coherent."),
        ("Complement", "P(not A) = 1 - P(A)",
         "Often far easier than counting A directly."),
        ("At least one", "P(at least one) = 1 - P(none)",
         "The single most useful shortcut in the topic."),
        ("Independent events", "P(A and B) = P(A) x P(B)",
         "When one happening does not change the other."),
        ("Dependent events", "P(A and B) = P(A) x P(B given A)",
         "Drawing without replacement changes the second probability."),
        ("Mutually exclusive", "P(A or B) = P(A) + P(B)",
         "When they cannot both happen."),
        ("Not mutually exclusive", "P(A or B) = P(A) + P(B) - P(A and B)",
         "The same double counting correction as overlapping sets."),
    ],
    worked=[
        dict(ask="A fair coin is flipped 4 times. What is the probability of at least one head?",
             steps=["Counting 'at least one' directly means one, two, three or four heads.",
                    "The complement is simpler: no heads at all.",
                    "P(no heads) = (1/2)^4 = 1/16.",
                    "P(at least one) = 1 - 1/16 = 15/16."],
             answer="15/16",
             why="Whenever a question says 'at least one', the complement is a single "
                 "case while the direct count is several. That is the reason the phrase "
                 "is a signal rather than a description."),
        dict(ask="A bag holds 5 red and 3 blue. Two are drawn without replacement. What "
                 "is the probability both are red?",
             steps=["First draw: 5 red out of 8, so 5/8.",
                    "Second draw: 4 red remain out of 7, so 4/7.",
                    "Multiply: 5/8 x 4/7 = 20/56 = 5/14."],
             answer="5/14",
             why="Without replacement the second probability depends on the first, so "
                 "both the numerator and the denominator drop by one. Using 5/8 twice "
                 "would answer a question about drawing with replacement."),
    ],
    traps=[
        "Multiplying unchanged probabilities for draws without replacement. The pool "
        "shrinks, and both parts of the fraction change.",
        "Adding probabilities of events that can both happen, which double counts the "
        "overlap.",
        "Counting 'at least one' case by case when the complement is a single "
        "calculation.",
    ],
    ladder={
        1: "One event, one step.",
        2: "Two independent events multiplied.",
        3: "Drawing without replacement, or a complement.",
        4: "The or rule where the events overlap, or a probability built from a "
           "combination count.",
        5: "A multi stage problem where the cases must be enumerated and added, each case "
           "a product.",
    },
),

Topic(
    slug="sequences", title="Sequences", area=ALGEBRA, skill="q_alg",
    idea="A sequence is a list with a rule, and the exam only uses two rules: add the "
         "same amount each time, or multiply by the same amount each time.",
    why="Sequence questions look intimidating because of the notation and are usually one "
        "substitution. Identifying which of the two rules is in play is most of the work.",
    facts=[
        ("Arithmetic sequence", "each term is the previous one plus a constant d",
         "The common difference d can be negative."),
        ("nth term, arithmetic", "a(n) = a(1) + (n - 1)d",
         "The minus one is because the first term takes no steps."),
        ("Sum of an arithmetic sequence", "S(n) = (n/2)(a(1) + a(n))",
         "The count times the average of the first and last terms."),
        ("Geometric sequence", "each term is the previous one times a constant r",
         "The common ratio r can be a fraction, which makes the sequence shrink."),
        ("nth term, geometric", "a(n) = a(1) x r^(n - 1)",
         "Again minus one, for the same reason."),
        ("Recognising which", "check differences, then check ratios",
         "Constant difference means arithmetic; constant ratio means geometric."),
    ],
    worked=[
        dict(ask="The sequence 5, 10, 15, 20 continues. What is the 4th term by formula, "
                 "and what is the sum of the first four?",
             steps=["Differences are 5 each time, so d = 5 and a(1) = 5.",
                    "a(4) = 5 + (4 - 1) x 5 = 5 + 15 = 20, which matches the list.",
                    "S(4) = (4/2)(5 + 20) = 2 x 25 = 50."],
             answer="a(4) = 20 and the sum is 50",
             why="Checking the formula against a term you can see is worth the two "
                 "seconds: it catches an off by one in the exponent or the (n - 1) "
                 "before it costs you the question."),
        dict(ask="A sequence starts at 5 and doubles each time. What is the 4th term?",
             steps=["Constant ratio, so geometric with a(1) = 5 and r = 2.",
                    "a(4) = 5 x 2^(4 - 1) = 5 x 8 = 40."],
             answer="40",
             why="The exponent is 3, not 4, because the first term has been doubled three "
                 "times to reach the fourth. Writing the list out, 5, 10, 20, 40, "
                 "confirms it and takes no longer."),
    ],
    traps=[
        "Using n instead of n - 1 in the exponent or the multiplier. The first term takes "
        "no steps, and that off by one is the most common error here.",
        "Assuming a sequence is arithmetic without checking. If the differences are not "
        "constant, check the ratios before assuming anything.",
        "Summing a geometric sequence with the arithmetic sum formula, which only works "
        "when the terms are evenly spaced.",
    ],
    ladder={
        1: "Continue a sequence by spotting the pattern.",
        2: "Apply the nth term formula for an arithmetic sequence.",
        3: "Sum an arithmetic sequence, or find a term of a geometric one.",
        4: "Work backwards from a known term to the first term or the common difference.",
        5: "A sequence defined recursively, where each term refers to the one before and "
           "there is no closed formula to substitute into.",
    },
),

Topic(
    slug="coordinate-geometry", title="Coordinate Geometry", area=COORD, skill="q_alg",
    idea="Coordinate geometry turns pictures into algebra: a line becomes an equation, "
         "and a distance becomes the Pythagorean theorem.",
    why="This is the geometry the GMAT Focus quant section does ask about, and nearly all "
        "of it is the slope formula and the slope intercept equation used carefully.",
    facts=[
        ("The quadrants", "I is (+,+), II is (-,+), III is (-,-), IV is (+,-)",
         "Numbered anticlockwise from the top right."),
        ("Slope", "m = (y2 - y1) / (x2 - x1), the rise over the run",
         "Subtract in the same order on the top and the bottom."),
        ("Slope intercept form", "y = mx + b",
         "m is the slope and b is where the line crosses the y axis."),
        ("Positive slope", "the line rises left to right",
         "As x increases, y increases."),
        ("Negative slope", "the line falls left to right",
         "As x increases, y decreases."),
        ("Zero slope", "a horizontal line, y = b",
         "No rise, so the slope is 0."),
        ("Undefined slope", "a vertical line, x = a",
         "No run, so the division is undefined. Vertical is not slope zero."),
        ("Parallel lines", "equal slopes, different intercepts",
         "Same steepness, so the two lines never meet."),
        ("Perpendicular lines", "slopes multiply to -1, so each is the negative reciprocal",
         "A slope of 2/3 is perpendicular to -3/2."),
        ("Distance", "distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)",
         "The Pythagorean theorem with the horizontal and vertical gaps as the legs."),
        ("Midpoint", "midpoint = ((x1 + x2)/2, (y1 + y2)/2)",
         "The average of the x values and the average of the y values."),
        ("Reflections", "over the x axis (x,y) becomes (x,-y); over the y axis it becomes "
         "(-x,y); over the origin it becomes (-x,-y)",
         "Flip the coordinate belonging to the axis you are crossing."),
    ],
    worked=[
        dict(ask="Find the equation of the line through (2, 3) and (6, 11).",
             steps=["Slope = (11 - 3)/(6 - 2) = 8/4 = 2.",
                    "Use y = mx + b with one point: 3 = 2(2) + b, so b = -1.",
                    "The line is y = 2x - 1."],
             answer="y = 2x - 1",
             why="Either point gives the same b, and checking with the other is a free "
                 "verification: 2(6) - 1 = 11, which matches."),
        dict(ask="A line is perpendicular to y = (3/4)x + 2 and passes through (0, 5). "
                 "What is its equation?",
             steps=["The negative reciprocal of 3/4 is -4/3.",
                    "It passes through (0, 5), which is the y intercept, so b = 5.",
                    "The line is y = (-4/3)x + 5."],
             answer="y = (-4/3)x + 5",
             why="Negative reciprocal means both operations: flip the fraction AND change "
                 "the sign. Doing only one of the two is the trap, and both half answers "
                 "appear among the choices."),
    ],
    traps=[
        "Subtracting the coordinates in opposite orders on the top and the bottom, which "
        "gives the slope the wrong sign.",
        "Calling a vertical line slope zero. Zero slope is horizontal; vertical is "
        "undefined, and the exam tests that they are different.",
        "Taking the reciprocal without the negative when finding a perpendicular slope.",
    ],
    ladder={
        1: "Read a slope or an intercept from an equation.",
        2: "Find a slope from two points.",
        3: "Build the full equation from two points, or from a point and a slope.",
        4: "Parallel or perpendicular conditions, or a distance between two points.",
        5: "A question about where two lines meet, or which quadrant a line passes "
           "through, answered without drawing anything.",
    },
),

]
