"""GRE Reading Comprehension from the reading corpus, shown as one paragraph (gre_rc).

GRE reading had only its 94 hand written items, although it is roughly half of the Verbal
questions, because the passages in g_rc.py are two paragraphs of 202 to 442 words and ETS
says of the GRE that "Most passages are one paragraph long, and one or two are several
paragraphs long" (ETS, GRE General Test Verbal Reasoning,
https://www.ets.org/gre/test-takers/general-test/prepare/content/verbal-reasoning.html,
read September 26, 2026). Thousands of two paragraph passages would have turned the GRE
mix upside down.

So the same passages are shown here as ONE paragraph of six sentences: the earlier view,
what it cannot account for, the two findings, what they suggest together, and the limit.
The supporting detail and the two conditional rules the GMAT inference questions turn on
are left out, and so are those questions. What is asked is what the paragraph carries:

  what it states         a stated idea, with the other five sentences as wrong answers
  what it is about       the main idea schema, unchanged but for the rendering
  what its limit implies the caveat schema, likewise
  what a sentence does   new here: each of the six sentences has a fixed job, set by where
                         the rendering puts it, so the answer is decided by the structure
                         rather than by anyone's reading; asked of the four sentences that
                         have to be read to be told apart

All four ask for a single answer from five choices, the format ETS calls Select One Answer.
The ETS skills these reach are summarizing a passage, distinguishing major from minor
points, reasoning from incomplete data, and understanding the structure of a text.
"""
import re

from framework import ItemError
import mapping
from g_rc import (P, P_LONG, RCBase, MainIdea, CaveatImplication, StatedIdea,
                  cap, lower1)


def gre_text(p):
    """The passage as one paragraph of exactly six sentences, in a fixed order."""
    return " ".join([
        p["old"],
        p["problem"],
        "%s examined %s and found that %s." % (cap(p["ev1who"]), p["ev1where"], p["ev1what"]),
        "%s of %s found that %s." % (cap(p["ev2who"]), p["ev2where"], p["ev2what"]),
        "Taken together, the two results suggest that %s." % p["revision"],
        p["caveat"],
    ])


def gre_sentences(p):
    """What the paragraph states, as answer choices: only sentences it actually shows."""
    return {
        "old": p["old"].rstrip("."),
        "problem": p["problem"].rstrip("."),
        "ev1what": p["ev1what"],
        "ev2what": p["ev2what"],
        "revision": p["revision"],
        "caveat": p["caveat"].rstrip("."),
    }


class GreRender:
    render = staticmethod(gre_text)
    pid = "GRP_"


class GreStated(GreRender, StatedIdea):
    """What the paragraph says. Its other sentences are the wrong answers, true and beside
    the point, which is the trap a stated idea question sets."""
    sub = "Stated idea"
    ASKS = [
        ("ev1what", lambda p: "According to the passage, %s found that" % p["ev1who"]),
        ("ev2what", lambda p: "According to the passage, %s of %s found that"
                              % (p["ev2who"], p["ev2where"])),
        ("problem", lambda p: "According to the passage, the earlier account failed to "
                              "address the fact that"),
        ("revision", lambda p: "According to the passage, the two results taken together "
                               "suggest that"),
    ]

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        field, stem = rng.choice(self.ASKS)
        s = gre_sentences(p)
        right = lower1(s[field])
        pool = [lower1(v) for k, v in s.items() if k != field]
        expl = ("The passage says exactly this, and the question asks only what it says. "
                "Each of the other choices is also a sentence of the passage, so each is "
                "true; none of them is what the stem asked about.")
        return self.emit(rng, choices_n, p, stem(p), right, pool, expl,
                         rng.choice([1, 2, 2, 3]), "gre_rc", self.sub)


class GreMainIdea(GreRender, MainIdea):
    sub = "Main idea"


class GreCaveat(GreRender, CaveatImplication):
    sub = "Inference"


ORDINAL = ("first", "second", "third", "fourth", "fifth", "sixth")
# The job each sentence does, by position in gre_text. Two wordings of each, so the
# length of the key is not fixed by the position asked about.
JOB = [
    ("set out the account that the rest of the passage revises",
     "introduce a view that the passage goes on to call into question"),
    ("point to a weakness in the account described in the first sentence",
     "identify something that the earlier account cannot explain or rests on too narrowly"),
    ("present a finding that tells against the earlier account",
     "report the first of the two results that the author relies on"),
    ("present a second finding that extends the first",
     "report further evidence that points the same way as the result described before it"),
    ("state the conclusion that the author draws from the two findings",
     "draw together the evidence into a revised account"),
    ("acknowledge a limit on how far the evidence has been shown to hold",
     "note a qualification of the conclusion the passage has just drawn"),
]
# Jobs no sentence in these passages does.
NO_JOB = [
    "concede that the earlier account was correct after all",
    "offer an example of a general principle stated earlier in the passage",
    "predict how the question the passage raises will finally be settled",
    "cast doubt on the reliability of the second finding",
]
WHY = [
    "The passage opens with the received view, and everything after it tests that view.",
    "The second sentence gives the reason the received view is in doubt.",
    "The third sentence is the first of the two findings the passage reports.",
    "The fourth sentence adds a second finding that points the same way as the first.",
    "The fifth sentence says what the two findings suggest together, which is the "
    "passage's conclusion.",
    "The last sentence limits that conclusion rather than adding to it.",
]


# Which sentences are asked about. Every passage has the same six part shape, so the
# first sentence (the received view) and the fifth (it opens "Taken together") would be
# answered by position alone once a student has seen a few; the weakness, the two
# findings and the limit have to be read to be told apart.
ASKED = (1, 2, 3, 5)


class FunctionOfSentence(GreRender, RCBase):
    """What one sentence does in the paragraph. The rendering fixes each sentence's job, so
    the answer is decided by where the sentence sits and not by anyone's judgement."""
    id = "rc_function"
    skill = "gre_rc"
    sub = "Function of a sentence"
    diff = 3
    wrong = ("The wrong choices describe what a different sentence of the passage does, or "
             "a job that no sentence in it does.")

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        i = rng.choice(ASKED)
        right = rng.choice(JOB[i])
        pool = [rng.choice(JOB[j]) for j in range(len(JOB)) if j != i] + rng.sample(NO_JOB, 2)
        stem = ("In the context of the passage as a whole, the %s sentence serves primarily to"
                % ORDINAL[i])
        expl = ("Read in order, the passage sets out an account, points to a weakness in it, "
                "reports two findings, says what they suggest together and closes on a "
                "limit. " + WHY[i])
        item = self.emit(rng, choices_n, p, stem, right, pool, expl,
                         [2, 3, 3, 3, 3, 3][i], "gre_rc", self.sub)
        # Two wordings of one job would be one answer twice, and a second key if the job
        # were the asked one.
        jobs = [j for c in item["choices"] for j, texts in enumerate(JOB) if c in texts]
        if len(jobs) != len(set(jobs)) or jobs.count(i) != 1:
            raise ItemError("%s offered one sentence's job twice" % self.id)
        return item


_CORPUS = P + P_LONG
INNER = [GreStated(_CORPUS, "_gre"), GreMainIdea(_CORPUS, "_gre"),
         GreCaveat(_CORPUS, "_gre"), FunctionOfSentence(_CORPUS, "_gre")]
GENS = [mapping.wrap(g, "gre_rc", "V", 0) for g in INNER]


_BREAK = re.compile(r"[.!?]\s+[A-Z]")


def check_corpus():
    """Every passage renders as exactly six sentences, in the order the jobs assume.

    The function questions name a sentence by its position, so a field that holds two
    sentences, or one that is missing, would shift every position after it and make the
    key describe a different sentence from the one the student counts to.
    """
    bad = []
    for p in _CORPUS:
        for k in ("old", "problem", "ev1what", "ev2what", "revision", "caveat",
                  "ev1who", "ev1where", "ev2who", "ev2where"):
            v = p.get(k) or ""
            if not v:
                bad.append("%s: %s is empty" % (p["key"], k))
            elif _BREAK.search(v.rstrip(".")):
                bad.append("%s: %s holds more than one sentence" % (p["key"], k))
        for k in ("old", "problem", "caveat"):
            if not (p.get(k) or "").endswith("."):
                bad.append("%s: %s does not end with a full stop" % (p["key"], k))
        n = len(_BREAK.findall(gre_text(p))) + 1
        if n != len(JOB):
            bad.append("%s renders as %d sentences, not %d" % (p["key"], n, len(JOB)))
    return bad
