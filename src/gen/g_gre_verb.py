"""GRE Verbal: Text Completion and Sentence Equivalence.

These are vocabulary in context items, so there is no arithmetic to compute a key from.
What makes them generatable anyway is that the semantics can be held as data rather than
as judgement:

  A GROUP is a set of words that are freely interchangeable in ordinary prose. Its members
  are synonyms of each other, which is what Sentence Equivalence needs, since that question
  asks for two words producing sentences alike in meaning.
  An AXIS is the dimension a group sits on. Each axis holds exactly two groups, opposites
  of one another.
  A FRAME is a sentence with one blank plus the clause that forces the blank's meaning. It
  names the group it requires.

From that, correctness follows by construction rather than by assertion. The key is drawn
from the frame's own group. Every distractor is drawn from a group on a DIFFERENT axis,
which is a meaning the frame's justifying clause rules out, and no two distractors come
from the same group, so no unintended synonym pair can form. One distractor may be drawn
from the frame's opposite group, which is the polarity trap: it fits the grammar and the
topic, and reverses the sense.

The discipline this needs is in the lexicon, not the code. A group whose members are only
loosely similar would produce a Sentence Equivalence item with no defensible pair, so the
groups here are deliberately small and tight, and a word that is close but not
interchangeable (laconic for terse, parsimonious for frugal) is left out.
"""
from framework import Gen, ItemError

# axis: the dimension; two groups per axis, opposed. gloss: what the group means.
GROUPS = {
    "brief":     dict(axis="length", pos="adj", gloss="short and to the point",
                      words=["concise", "succinct", "terse", "compact"]),
    "lengthy":   dict(axis="length", pos="adj", gloss="using far more words than needed",
                      words=["verbose", "prolix", "rambling", "long winded"]),
    "obscure":   dict(axis="clarity", pos="adj", gloss="hard to understand",
                      words=["abstruse", "recondite", "arcane", "impenetrable"]),
    "clear":     dict(axis="clarity", pos="adj", gloss="easy to understand",
                      words=["lucid", "transparent", "intelligible", "straightforward"]),
    "plentiful": dict(axis="supply", pos="adj", gloss="present in large quantity",
                      words=["abundant", "copious", "plentiful", "ample"]),
    "scarce":    dict(axis="supply", pos="adj", gloss="present in too small a quantity",
                      words=["scant", "meagre", "sparse", "scanty"]),
    "fickle":    dict(axis="constancy", pos="adj", gloss="liable to change without warning",
                      words=["capricious", "mercurial", "fickle", "volatile"]),
    "steady":    dict(axis="constancy", pos="adj", gloss="unchanging and dependable",
                      words=["constant", "steadfast", "unwavering", "unswerving"]),
    "friendly":  dict(axis="temper", pos="adj", gloss="warm and pleasant towards others",
                      words=["affable", "genial", "amiable", "cordial"]),
    "hostile":   dict(axis="temper", pos="adj", gloss="eager to quarrel or attack",
                      words=["truculent", "belligerent", "pugnacious", "combative"]),
    "thrifty":   dict(axis="spending", pos="adj", gloss="careful not to spend more than needed",
                      words=["frugal", "thrifty", "economical", "sparing"]),
    "lavish":    dict(axis="spending", pos="adj", gloss="spending wastefully and without limit",
                      words=["profligate", "extravagant", "prodigal", "spendthrift"]),
    "bold":      dict(axis="nerve", pos="adj", gloss="willing to face danger or objection",
                      words=["intrepid", "dauntless", "audacious", "fearless"]),
    "timid":     dict(axis="nerve", pos="adj", gloss="lacking confidence and holding back",
                      words=["timorous", "diffident", "hesitant", "tentative"]),
    "fake":      dict(axis="authenticity", pos="adj", gloss="not what it is presented as",
                      words=["spurious", "bogus", "counterfeit", "fraudulent"]),
    "genuine":   dict(axis="authenticity", pos="adj", gloss="exactly what it is presented as",
                      words=["authentic", "genuine", "legitimate", "unfeigned"]),
    "stubborn":  dict(axis="flexibility", pos="adj", gloss="refusing to be moved from a position",
                      words=["obdurate", "intransigent", "adamant", "unyielding"]),
    "yielding":  dict(axis="flexibility", pos="adj", gloss="readily giving way to others",
                      words=["pliant", "accommodating", "malleable", "tractable"]),
    "novel":     dict(axis="freshness", pos="adj", gloss="new and not seen before",
                      words=["novel", "unprecedented", "original", "innovative"]),
    "stale":     dict(axis="freshness", pos="adj", gloss="worn out by repetition",
                      words=["hackneyed", "trite", "banal", "stale"]),
    "praise":    dict(axis="regard", pos="verb", gloss="to speak highly of",
                      words=["laud", "extol", "commend", "applaud"]),
    "disparage": dict(axis="regard", pos="verb", gloss="to speak of as worthless",
                      words=["deride", "belittle", "denigrate", "disparage"]),
    "shorten":   dict(axis="extent", pos="verb", gloss="to cut back or make shorter",
                      words=["curtail", "abridge", "truncate", "pare"]),
    "enlarge":   dict(axis="extent", pos="verb", gloss="to make larger or greater",
                      words=["amplify", "augment", "enlarge", "expand"]),
    "reveal":    dict(axis="disclosure", pos="verb", gloss="to make known what was hidden",
                      words=["divulge", "disclose", "reveal", "impart"]),
    "conceal":   dict(axis="disclosure", pos="verb", gloss="to keep from being known",
                      words=["conceal", "withhold", "suppress", "hide"]),
    "bolster":   dict(axis="strength", pos="verb", gloss="to make stronger or better supported",
                      words=["bolster", "buttress", "reinforce", "strengthen"]),
    "undermine": dict(axis="strength", pos="verb", gloss="to weaken gradually from beneath",
                      words=["undermine", "weaken", "erode", "sap"]),
    "begin":     dict(axis="onset", pos="verb", gloss="to set something going",
                      words=["initiate", "inaugurate", "launch", "commence"]),
    "end":       dict(axis="onset", pos="verb", gloss="to bring something to a stop",
                      words=["terminate", "discontinue", "halt", "cease"]),
    "allow":     dict(axis="permission", pos="verb", gloss="to give official leave for",
                      words=["permit", "sanction", "authorise", "license"]),
    "forbid":    dict(axis="permission", pos="verb", gloss="to rule officially against",
                      words=["prohibit", "proscribe", "forbid", "ban"]),
}

OPPOSITE = {}
for _k, _g in GROUPS.items():
    for _k2, _g2 in GROUPS.items():
        if _k2 != _k and _g2["axis"] == _g["axis"]:
            OPPOSITE[_k] = _k2

# Every frame carries the clause that forces its meaning, so the explanation can point at
# the words on the page rather than appeal to taste.
FRAMES = [
    ("brief", "The editor cut every clause that repeated an earlier one, leaving a summary "
     "so ______ that the whole argument fit on a single page.", "every repeated clause was cut and the whole argument fits on one page"),
    ("brief", "Asked to keep her remarks under two minutes, the chair delivered a ______ "
     "account that omitted nothing essential.", "the remarks had to run under two minutes and still omit nothing essential"),
    ("brief", "What had been a forty page proposal became, after three rounds of editing, a "
     "______ statement of the same plan.", "forty pages became a statement of the same plan"),
    ("lengthy", "Reviewers complained that the manuscript was ______, spending nine pages on "
     "a point that its own abstract had made in two sentences.", "nine pages are spent on what the abstract made in two sentences"),
    ("lengthy", "The witness gave a ______ answer that circled the question for several "
     "minutes without ever reaching it.", "the answer circled the question for several minutes without reaching it"),
    ("lengthy", "Her first drafts were famously ______, and the work of revision was mostly "
     "the work of deletion.", "revising the drafts consisted mostly of deleting"),
    ("obscure", "The paper's central proof is so ______ that even specialists in the field "
     "asked the author to restate it in plainer terms.", "even specialists asked for it to be restated in plainer terms"),
    ("obscure", "Written for a handful of colleagues rather than for students, the treatise "
     "remains ______ to anyone outside that circle.", "it was written for a handful of colleagues and not for students"),
    ("obscure", "The ritual's meaning is now ______, the community that once explained it "
     "having long since dispersed.", "the community that could explain it has dispersed"),
    ("clear", "The judge's opinion was praised as ______, laying out each step of the "
     "reasoning in terms a non lawyer could follow.", "each step is laid out in terms a non lawyer could follow"),
    ("clear", "Where the earlier manual buried its instructions in jargon, the replacement is "
     "______ enough to be used without training.", "the replacement can be used without training, unlike the jargon filled original"),
    ("clear", "She had a gift for making a ______ summary of a tangled dispute, so that "
     "readers grasped in a paragraph what had taken years to argue.", "readers grasp in a paragraph what took years to argue"),
    ("plentiful", "Rainfall that season was so ______ that reservoirs filled months ahead of "
     "schedule and the restrictions were lifted.", "reservoirs filled months early and restrictions were lifted"),
    ("plentiful", "The archive holds ______ documentation of the period, far more than any "
     "single scholar could read in a career.", "there is more documentation than one scholar could read in a career"),
    ("plentiful", "Evidence for the migration is ______, drawn from pottery, burials and "
     "three separate written records.", "the evidence is drawn from pottery, burials and three written records"),
    ("scarce", "Funding for the survey was so ______ that the team could visit only two of "
     "the eleven sites it had planned to study.", "the team could visit only two of eleven planned sites"),
    ("scarce", "Written evidence for the settlement is ______, amounting to a single tax roll "
     "and one disputed letter.", "the evidence amounts to one tax roll and one disputed letter"),
    ("scarce", "Rations grew ______ as the winter went on, and the expedition began weighing "
     "each day's flour to the gram.", "the expedition began weighing each day's flour to the gram"),
    ("fickle", "The market for the shares proved ______, rising a third one week and giving "
     "it all back the next.", "the price rose a third in one week and gave it all back the next"),
    ("fickle", "A ______ patron, he funded the orchestra lavishly for two seasons and then "
     "withdrew without explanation.", "he funded the orchestra for two seasons and then withdrew without explanation"),
    ("fickle", "Mountain weather here is notoriously ______, and a clear morning is no "
     "guarantee of a clear afternoon.", "a clear morning is no guarantee of a clear afternoon"),
    ("steady", "Through four changes of government her support for the programme remained "
     "______, which is why both sides came to trust her.", "the support survived four changes of government"),
    ("steady", "The lighthouse keeper's attendance was ______: in thirty years he missed not "
     "one night.", "in thirty years he missed not one night"),
    ("steady", "What the project needed was not brilliance but a ______ effort maintained "
     "over several years.", "what was needed was effort maintained over several years"),
    ("friendly", "Famously ______, the new director learned the name of every member of staff "
     "within a fortnight.", "the director learned every member of staff's name within a fortnight"),
    ("friendly", "The negotiations opened in a ______ atmosphere, with both delegations "
     "visibly relieved to be talking at all.", "both delegations were visibly relieved to be talking"),
    ("friendly", "He was ______ even with those who had opposed him, and the opposition "
     "found it disarming.", "he was warm even towards those who had opposed him"),
    ("hostile", "The tone of the reply was so ______ that the mediator suspended the session "
     "before either side could answer it.", "the mediator suspended the session before either side could answer"),
    ("hostile", "A ______ questioner, he treated every interview as a contest to be won "
     "rather than a conversation.", "every interview was treated as a contest to be won"),
    ("hostile", "Relations between the two departments turned ______ after the budget was "
     "split, and meetings had to be chaired from outside.", "meetings had to be chaired from outside after relations soured"),
    ("thrifty", "Running the charity on a tenth of what its rivals spent, she was ______ "
     "without ever being mean about what mattered.", "the charity ran on a tenth of what rivals spent"),
    ("thrifty", "Wartime households learned to be ______ with everything, saving string, fat "
     "and paper against a shortage that might come.", "households saved string, fat and paper against a possible shortage"),
    ("thrifty", "The design is admired for being ______ of material: it uses a third less "
     "steel than the structure it replaced.", "it uses a third less steel than the structure it replaced"),
    ("lavish", "A ______ heir, he spent in four years an estate that had taken three "
     "generations to build.", "an estate built over three generations was spent in four years"),
    ("lavish", "The banquet was criticised as ______ at a time when the city was asking "
     "residents to ration water.", "the city was asking residents to ration water at the time"),
    ("lavish", "Her ______ habits alarmed the trustees, who watched the fund shrink by a "
     "fifth in a single year.", "the fund shrank by a fifth in a single year"),
    ("bold", "It was a ______ decision to publish the findings before the grant was secure, "
     "and it cost her the grant.", "the findings were published before the grant was secure"),
    ("bold", "The ______ crew put to sea in weather that had kept every other boat in "
     "harbour.", "they put to sea in weather that kept every other boat in harbour"),
    ("bold", "Only a ______ negotiator would have opened with a demand that the other side "
     "had already called impossible.", "the opening demand had already been called impossible"),
    ("timid", "Too ______ to raise her objection in the meeting, she sent it afterwards in a "
     "note that nobody answered.", "the objection was not raised in the meeting but sent afterwards in a note"),
    ("timid", "His ______ manner at the hearing was mistaken for evasion, though it was only "
     "nerves.", "the manner was nerves, mistaken for evasion"),
    ("timid", "The committee's ______ first proposal asked for a pilot in one district rather "
     "than the reform it had been convened to design.", "the proposal asked for a pilot in one district rather than the reform it was convened to design"),
    ("fake", "Three of the letters turned out to be ______, written on paper manufactured "
     "sixty years after their supposed date.", "the paper was manufactured sixty years after the supposed date"),
    ("fake", "The qualification proved ______; the institution named on it had never "
     "existed.", "the institution named on the qualification had never existed"),
    ("fake", "Her claim of an inheritance was ______, resting on a will that the probate "
     "office had no record of.", "the will has no record at the probate office"),
    ("genuine", "Testing confirmed the bowl was ______, its clay matching the local seam and "
     "its glaze the workshop's own recipe.", "the clay matches the local seam and the glaze the workshop's recipe"),
    ("genuine", "What the audience found moving was that the apology was plainly ______ "
     "rather than drafted for them.", "the apology was plainly not drafted for the audience"),
    ("genuine", "Every document in the bundle proved ______, as the archivist's report "
     "confirmed line by line.", "the archivist's report confirmed every document line by line"),
    ("stubborn", "He remained ______ through eleven hours of negotiation, conceding not one "
     "of the points at issue.", "not one point was conceded in eleven hours"),
    ("stubborn", "The board was ______ on the question of the site, and no argument about "
     "cost moved it.", "no argument about cost moved the board"),
    ("stubborn", "Her ______ refusal to withdraw the paper, in the face of two hostile "
     "reviews, was later vindicated.", "the paper was not withdrawn despite two hostile reviews"),
    ("yielding", "A ______ chair, he rearranged the agenda whenever a member asked, and the "
     "meeting ran four hours.", "the agenda was rearranged whenever a member asked"),
    ("yielding", "The union found the new management unexpectedly ______, agreeing within a "
     "week to terms it had refused for a year.", "terms refused for a year were agreed within a week"),
    ("yielding", "Heated to the right temperature the alloy becomes ______, and can be worked "
     "into shapes that would crack it cold.", "heated, the alloy can be worked into shapes that would crack it cold"),
    ("novel", "The technique was ______ when she described it in 1974, and no earlier use of "
     "it has since been found.", "no earlier use has been found than the 1974 description"),
    ("novel", "What the panel wanted was a ______ approach, not another version of the plan "
     "that had failed twice already.", "the panel did not want another version of the plan that had failed twice"),
    ("novel", "The building's roof was ______ in its day, the first of its kind to span so "
     "wide a hall without columns.", "it was the first of its kind to span so wide a hall without columns"),
    ("stale", "The speech was ______, assembling phrases that every delegate had heard at "
     "the previous three conferences.", "the phrases had been heard at the previous three conferences"),
    ("stale", "Critics called the plot ______, noting that the same twist had carried four "
     "films in the same decade.", "the same twist had carried four films in the same decade"),
    ("stale", "Her complaint was that the advice, however sound, had become ______ through "
     "constant repetition.", "the advice had become worn through constant repetition"),
    ("praise", "The committee went out of its way to ______ the junior staff, naming each of "
     "them in the published report.", "each junior staff member was named in the published report"),
    ("praise", "Reviewers who had savaged her first book were quick to ______ the second.",
     "the same reviewers who savaged the first book reversed themselves on the second"),
    ("praise", "It is unusual for a regulator to ______ a company it has just fined, but the "
     "cooperation had been exceptional.", "the regulator had just fined the company, yet the cooperation was exceptional"),
    ("disparage", "He would ______ any proposal he had not written himself, whatever its "
     "merits.", "any proposal he had not written was treated the same way, whatever its merits"),
    ("disparage", "It costs nothing to ______ a plan from the sidelines, and rather more to "
     "offer a better one.", "the contrast is with offering a better plan"),
    ("disparage", "The memoir takes every chance to ______ colleagues who are no longer alive "
     "to reply.", "the colleagues are no longer alive to reply"),
    ("shorten", "Falling revenue forced the museum to ______ its opening hours from ten a day "
     "to six.", "opening hours went from ten a day to six"),
    ("shorten", "The editor asked her to ______ the chapter by a third without losing the "
     "argument.", "the chapter had to lose a third of its length"),
    ("shorten", "Rather than cancel the season the company chose to ______ it, staging four "
     "productions instead of seven.", "four productions were staged instead of seven"),
    ("enlarge", "The grant allowed the clinic to ______ its hours, which rose from twenty a "
     "week to fifty.", "hours rose from twenty a week to fifty"),
    ("enlarge", "Each retelling served to ______ his part in the rescue, until he was its "
     "only hero.", "his part grew with each retelling until he was the only hero"),
    ("enlarge", "The new wing will ______ the collection's display space by roughly half.",
     "display space grows by roughly half"),
    ("reveal", "Ordered by the court to ______ the terms of the settlement, the company "
     "published them in full the same afternoon.", "the terms were published in full after a court order"),
    ("reveal", "She agreed to ______ the source only after he had been dead for twenty "
     "years.", "the source was made known only after his death"),
    ("conceal", "The auditors found that the company had worked for years to ______ the "
     "scale of the losses from its own board.", "the scale of the losses was kept from the board for years"),
    ("conceal", "There was no attempt to ______ the disagreement; both sides described it "
     "in their opening statements.", "the contrast is with describing it openly in the opening statements"),
    ("bolster", "The second trial was designed to ______ a finding that a single small study "
     "had left in doubt.", "a finding left in doubt needed firmer support"),
    ("bolster", "Three new sources ______ the dating, which until then had rested on one "
     "inscription.", "the dating had rested on one inscription and now rests on more"),
    ("undermine", "The discovery of a fourth manuscript did not settle the question so much "
     "as ______ the account everyone had been working from.", "the account everyone worked from was left weaker, not confirmed"),
    ("undermine", "Repeated missed deadlines ______ the confidence that had taken the team "
     "two years to build.", "confidence built over two years was worn away"),
    ("begin", "The trustees voted to ______ a review of every grant awarded since 2019.",
     "a review was set going"),
    ("begin", "Rather than wait for the legislation, the city chose to ______ the scheme in "
     "three districts.", "the scheme was set going in three districts without waiting"),
    ("end", "Falling attendance forced the theatre to ______ the run three weeks early.",
     "the run was stopped three weeks early"),
    ("end", "The agency will ______ the programme in June unless the funding is renewed.",
     "the programme stops in June absent renewal"),
    ("allow", "The council voted to ______ the market to trade on Sundays, reversing a rule "
     "that had stood since 1953.", "the market is given official leave to trade on Sundays"),
    ("allow", "Only the regulator can ______ a trial of this kind, and it did so in "
     "writing.", "the regulator gave official leave, in writing"),
    ("forbid", "The new rules ______ any contact between the two departments while the "
     "inquiry is running.", "contact is ruled against while the inquiry runs"),
    ("forbid", "Her contract did not ______ outside work, which is why the objection came to "
     "nothing.", "the objection failed because outside work was not ruled against"),
]


# Being on a different axis is usually enough to guarantee a distractor cannot fit, but
# not always: some axes overlap in ordinary use. "Falling attendance forced the theatre to
# ______ the run three weeks early" takes halt from the onset axis and curtail from the
# extent axis equally well, which is fatal for a Text Completion item with one key. These
# pairs may not supply distractors to each other. Listed as a set of unordered pairs and
# checked for symmetry below.
CONFUSABLE = [
    ("extent", "onset"),          # curtail / halt, abridge / discontinue
    ("supply", "spending"),       # scant / sparing
    ("constancy", "flexibility"), # unwavering / unyielding
    ("regard", "strength"),       # denigrate / undermine
    ("permission", "onset"),      # sanction / launch
]
BLOCKED = {}
for _a, _b in CONFUSABLE:
    BLOCKED.setdefault(_a, set()).add(_b)
    BLOCKED.setdefault(_b, set()).add(_a)


def check_lexicon():
    """The lexicon is the only place this category can go wrong, so it is checked."""
    seen = {}
    for name, g in GROUPS.items():
        if name not in OPPOSITE:
            raise ItemError("group %s has no opposite on axis %s" % (name, g["axis"]))
        if len(g["words"]) < 4:
            raise ItemError("group %s is too small for a pair plus variety" % name)
        for w in g["words"]:
            if w in seen:
                raise ItemError("word %r is in both %s and %s" % (w, seen[w], name))
            seen[w] = name
    for grp, text, why in FRAMES:
        if grp not in GROUPS:
            raise ItemError("frame names unknown group %r" % grp)
        if text.count("______") != 1:
            raise ItemError("frame for %s does not have exactly one blank" % grp)
    for a, bs in BLOCKED.items():
        for b in bs:
            if a not in BLOCKED.get(b, set()):
                raise ItemError("blocked axis pair %s/%s is not symmetric" % (a, b))
    # Every group must still have four usable distractor groups after blocking, or its
    # frames can never produce an item and the lexicon has quietly lost them.
    for name, g in GROUPS.items():
        usable = [k for k, o in GROUPS.items()
                  if o["axis"] != g["axis"] and o["axis"] not in BLOCKED.get(g["axis"], set())
                  and o["pos"] == g["pos"]]
        if len(usable) < 4:
            raise ItemError("group %s has only %d usable distractor groups after blocking"
                            % (name, len(usable)))


check_lexicon()


def pick_distractor_groups(rng, grp, n, allow_opposite=True):
    """n groups, all on different axes from the frame's, no two the same group.

    A distractor drawn from another axis is a meaning the frame's justifying clause has
    already ruled out, so it cannot accidentally be a second right answer. The frame's own
    opposite may be included once, as the polarity trap.
    """
    axis = GROUPS[grp]["axis"]
    blocked = BLOCKED.get(axis, set())
    pool = [k for k, g in GROUPS.items() if g["axis"] != axis
            and g["axis"] not in blocked
            and g["pos"] == GROUPS[grp]["pos"]]
    if len(pool) < n:
        raise ItemError("not enough groups off the %s axis for %s" % (axis, grp))
    picked = rng.sample(pool, n)
    if allow_opposite and rng.random() < 0.55:
        picked[rng.randrange(n)] = OPPOSITE[grp]
    return picked


class GreVerbBase(Gen):
    section = "V"

    def frame(self, rng):
        grp, text, why = rng.choice(FRAMES)
        return grp, text, why


class TextCompletion(GreVerbBase):
    id = "gre_tc_one"
    skill = "gre_tc"
    type = "TC"
    sub = "Text Completion, one blank"
    diff = 3

    def make(self, rng, choices_n):
        grp, text, why = self.frame(rng)
        g = GROUPS[grp]
        right = rng.choice(g["words"])
        dgroups = pick_distractor_groups(rng, grp, choices_n - 1)
        opts = [right]
        for dg in dgroups:
            opts.append(rng.choice(GROUPS[dg]["words"]))
        if len(set(opts)) != choices_n:
            raise ItemError("%s drew a repeated word" % self.id)
        rng.shuffle(opts)
        opp = OPPOSITE[grp]
        trap = next((w for w in opts if w in GROUPS[opp]["words"]), None)
        expl = ("The sentence pins the blank down: " + why + ". That calls for a word meaning "
                + g["gloss"] + ", which is what " + right + " means.")
        wrong = ("The other choices name meanings the sentence has already ruled out"
                 + (", and " + trap + " reverses it, meaning " + GROUPS[opp]["gloss"]
                    + " rather than " + g["gloss"] + "." if trap else "."))
        item = {
            "id": None, "section": "V", "type": "TC", "sub": self.sub, "skill": "gre_tc",
            "diff": rng.choice([2, 3, 3, 4]),
            "stem": text, "choices": opts, "answer": opts.index(right),
            "expl": expl, "wrong": wrong, "gen": self.id,
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


class SentenceEquivalence(GreVerbBase):
    """Six options, exactly two of which are synonyms of each other AND both fit.

    choices_n is ignored here on purpose: Sentence Equivalence is always six options and
    always two keys. That is the format, not a parameter, and an item that offered five
    would not be the question the GRE asks.
    """
    id = "gre_se_pair"
    skill = "gre_se"
    type = "SE"
    sub = "Sentence Equivalence"
    diff = 3

    INSTRUCTION = ("Select the TWO answer choices that, when used to complete the sentence, "
                   "fit the meaning as a whole and produce completed sentences alike in "
                   "meaning.")

    def make(self, rng, choices_n):
        grp, text, why = self.frame(rng)
        g = GROUPS[grp]
        pair = rng.sample(g["words"], 2)
        # Four distractors from four DIFFERENT groups, none on this frame's axis. That is
        # what guarantees the pair is the only pair: two distractors from one group would
        # be synonyms of each other and would make a second defensible answer.
        dgroups = pick_distractor_groups(rng, grp, 4)
        opts = list(pair) + [rng.choice(GROUPS[dg]["words"]) for dg in dgroups]
        if len(set(opts)) != 6:
            raise ItemError("%s drew a repeated word" % self.id)
        rng.shuffle(opts)
        key = sorted([opts.index(pair[0]), opts.index(pair[1])])
        # Verify the promise the instruction makes: among the six, exactly one unordered
        # pair is drawn from a single group. Checked rather than trusted, because a lexicon
        # edit that put two synonyms in different groups would otherwise ship silently.
        owner = {}
        for name, grpdef in GROUPS.items():
            for w in grpdef["words"]:
                owner[w] = name
        buckets = {}
        for w in opts:
            buckets.setdefault(owner[w], []).append(w)
        pairs = [ws for ws in buckets.values() if len(ws) >= 2]
        if len(pairs) != 1 or len(pairs[0]) != 2:
            raise ItemError("%s produced %d synonym pairs, expected exactly one"
                            % (self.id, len(pairs)))
        opp = OPPOSITE[grp]
        trap = next((w for w in opts if w in GROUPS[opp]["words"]), None)
        expl = ("The sentence pins the blank down: " + why + ". That calls for a word meaning "
                + g["gloss"] + ". Of the six choices, " + pair[0] + " and " + pair[1]
                + " are the only two that both fit and mean the same thing, so they are the "
                "pair that produce sentences alike in meaning.")
        wrong = ("A word can fit the blank and still be wrong here, because the question "
                 "asks for two choices that produce the SAME sentence. The remaining choices "
                 "each come from a different sense, so no other pair among them means the "
                 "same thing"
                 + (", and " + trap + " reverses the sentence, meaning "
                    + GROUPS[opp]["gloss"] + "." if trap else "."))
        item = {
            "id": None, "section": "V", "type": "SE", "sub": self.sub, "skill": "gre_se",
            "diff": rng.choice([2, 3, 3, 4]), "answerType": "se",
            "stem": self.INSTRUCTION + "\n\n" + text,
            "choices": opts, "answer": key, "expl": expl, "wrong": wrong, "gen": self.id,
        }
        self.verify_se(item, pair)
        return item

    def verify_se(self, item, pair):
        import json
        from framework import DASH
        c = item["choices"]
        if len(c) != 6 or len(set(c)) != 6:
            raise ItemError("%s is not six distinct options" % self.id)
        a, b = item["answer"]
        if a == b or {c[a], c[b]} != set(pair):
            raise ItemError("%s keys do not match the drawn pair" % self.id)
        if DASH.search(json.dumps(item)):
            raise ItemError("%s contains an em or en dash" % self.id)
        if item["diff"] not in (1, 2, 3, 4, 5):
            raise ItemError("%s difficulty %r" % (self.id, item["diff"]))
        for k in ("stem", "expl"):
            if not item[k] or not str(item[k]).strip():
                raise ItemError("%s missing %s" % (self.id, k))


GENS = [TextCompletion(), SentenceEquivalence()]
