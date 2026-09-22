"""Reading comprehension: generated questions over authored passages.

The honest position on this category, established by measurement rather than assumed:
a reading question worded the same way across two different passages is ONE item under
the dedup key, because the stem and the choices are identical. So item count here is
gated on how many PASSAGES exist, and no amount of generator cleverness changes that.
What the generator can do is extract the largest honest number of distinct questions from
each passage, which is what this module is built to do.

The passages are written, not generated. Each one is stored as complete sentences under
named roles, and the module assembles them and derives the questions. That keeps the prose
at the standard of the hand written passages, because a person wrote every sentence, while
the questions stay computable from the structure.

Every passage follows the revision narrative, which is what most academic reading passages
actually are: a received view, the reason it was held, the thing it could not explain, two
findings with specifics, the revised account, and a qualification.

Two question families come out of that, and they are the two the GMAT reports separately:

  Stated idea asks what the passage says. The key is a sentence the passage contains, and
  the distractors are other sentences it also contains, which are true but do not answer
  the stem. That is the real trap on this question type, and it is decidable.

  Inferred idea asks what follows. Each passage carries two conditionals of the form
  "every X that showed A also had B", paired with a case that lacks B. Modus tollens gives
  a key that must be true, and the distractors are the converse and inverse errors, which
  are the mistakes this question type is actually testing for.

Nothing here asserts a key. What the passage states is data; what follows from it is
derived by the same rule every time.
"""
from framework import Gen, ItemError, balance

# --- the corpus --------------------------------------------------------------------
# Each entry is one passage. Fields are written sentences, not templates:
#   old        the received view, as a full sentence
#   old_why    the reasoning that supported it
#   problem    what it could not account for
#   ev1/ev2    a finding: who, where, what (the finding), detail (a methodological fact)
#   revision   the account the evidence supports
#   caveat     a limit the author acknowledges
#   cond1/2    (universal, case, conclusion): every X with A had B; this case lacks B;
#              therefore it is not an X with A. Written so all three read naturally.
#   about      what the passage is primarily concerned with, in this passage's own terms
#   implies    what the caveat implies, in this passage's own terms
P = [
 dict(key="tundra", topic="Arctic carbon",
  old="Until the late 1980s, ecologists treated the Arctic tundra as a permanent carbon sink.",
  old_why="Cold soils decompose organic matter far more slowly than plants deposit it, so the balance seemed certain to run one way.",
  problem="The account rested entirely on measurements taken during the brief summer, when photosynthesis is at its peak.",
  ev1who="Oechsner and colleagues", ev1where="a monitoring station on the Alaskan North Slope",
  ev1what="the soil released more carbon between October and April than the vegetation had taken up across the whole of the preceding summer",
  ev1detail="their instruments ran continuously for three years rather than being read seasonally",
  ev2who="A later survey", ev2where="eleven sites across northern Canada",
  ev2what="the same winter reversal appeared wherever the snowpack exceeded forty centimetres",
  ev2detail="deep snow insulates the soil well enough for microbes to stay active beneath it",
  revision="whether the tundra is a sink depends on the season in which it is measured and on how much snow falls",
  caveat="None of the sites studied lies south of the treeline, where soils are warmer and the snowpack thinner.",
  cond1=("every site in the Canadian survey that showed the winter reversal had a snowpack deeper than forty centimetres",
         "the Kivalliq site recorded a snowpack of twenty-two centimetres",
         "the Kivalliq site did not show the winter reversal", "the Kivalliq site"),
  cond2=("every reading that captured the reversal was taken by an instrument running through the winter",
         "the Barrow readings were taken only in July and August",
         "the Barrow readings did not capture the reversal", "the Barrow readings"),
  about="revising a settled account of Arctic carbon by showing that it rested on measurements taken in one season only",
  implies="the revised account has not been tested in the warmer conditions south of the treeline"),

 dict(key="guilds", topic="English craft guilds",
  old="Historians long explained the decline of the English craft guilds as a consequence of industrial machinery.",
  old_why="Machinery is assumed to have made the guild workshop uneconomic almost as soon as it arrived.",
  problem="The chronology has never fit, because most guilds lost their membership decades before machinery reached their trades.",
  ev1who="Halloway", ev1where="the admission books of the Sheffield cutlers",
  ev1what="membership fell by half between 1790 and 1820, a generation before mechanised grinding entered the trade",
  ev1detail="the books record every admission with a date and a named sponsor",
  ev2who="A study of apprenticeship indentures", ev2where="four other Sheffield trades",
  ev2what="the same early fall appeared wherever the guild had lost its power to prosecute unlicensed work",
  ev2detail="that power was removed by statute at different dates in different trades",
  revision="the guilds were undone by the loss of their legal monopoly, and machinery arrived to find them already weakened",
  caveat="The Sheffield records are unusually complete, and no comparable series survives for the textile towns.",
  cond1=("every trade in the study that showed the early fall had already lost its power to prosecute unlicensed work",
         "the farriers retained that power until 1835",
         "the farriers did not show the early fall before 1835", "the farriers"),
  cond2=("every figure Halloway reports comes from a book that records a sponsor for each admission",
         "the cutlers' journeyman register records no sponsors",
         "Halloway's figures do not come from the journeyman register", "the journeyman register"),
  about="reordering the causes of an institutional decline by showing that the usual explanation arrives too late to account for it",
  implies="the argument may not extend to trades whose records have not survived"),

 dict(key="reefs", topic="coral colour",
  old="For most of the twentieth century, marine biologists attributed the bright colour of shallow water corals to the pigments of the algae living inside them.",
  old_why="The algae are the obvious source, since they are abundant, pigmented, and present in every healthy colony.",
  problem="The explanation cannot account for corals that stay vividly coloured after the algae have been expelled.",
  ev1who="Takeda", ev1where="a reef flat in the Ryukyu Islands",
  ev1what="bleached colonies went on fluorescing for up to nine weeks, long after any algal pigment would have degraded",
  ev1detail="the colonies were photographed each week under light of identical intensity",
  ev2who="Later laboratory work", ev2where="colonies raised without algae from the larval stage",
  ev2what="the coral itself produces the fluorescent proteins, in every colony kept under strong light",
  ev2detail="colonies held in shade produced almost none of the proteins",
  revision="the colour belongs to the coral, and the algae contribute to it only indirectly",
  caveat="Whether the proteins shield the coral from light, as is often suggested, remains untested.",
  cond1=("every colony in the laboratory work that produced the fluorescent proteins was kept under strong light",
         "the colonies in the fourth tank were held in shade throughout",
         "the colonies in the fourth tank did not produce the fluorescent proteins", "the colonies in the fourth tank"),
  cond2=("every colony Takeda photographed was recorded under light of identical intensity",
         "the colonies at the reef margin were photographed under whatever light the day provided",
         "the colonies at the reef margin were not among those Takeda photographed", "the colonies at the reef margin"),
  about="relocating the source of a familiar phenomenon from an organism's partner to the organism itself",
  implies="the function of the proteins remains an open question even though their source is now settled"),

 dict(key="roads", topic="road widening",
  old="Transport planners have generally assumed that widening a congested road reduces the time drivers spend on it.",
  old_why="The same traffic spread across more lanes should move faster, which is true of any fixed quantity of vehicles.",
  problem="The assumption treats the number of drivers as fixed, and it is not.",
  ev1who="Duranton and Turner", ev1where="the interstate network of 228 American cities",
  ev1what="vehicle miles travelled rose almost exactly in proportion to the lane miles added, leaving average speeds unchanged",
  ev1detail="their comparison covers the two decades to 2003",
  ev2who="A narrower study", ev2where="six corridors widened in the same period",
  ev2what="the new traffic appeared within five years wherever the corridor joined two growing suburbs",
  ev2detail="corridors between districts of stable population kept their improved speeds",
  revision="added capacity is taken up by drivers who did not previously make the trip, so widening relieves congestion only where surrounding demand is not growing",
  caveat="Every corridor studied is urban, and nothing here settles the case for rural routes.",
  cond1=("every corridor in the narrower study where new traffic appeared within five years joined two growing suburbs",
         "the Elkford corridor runs between districts whose population has been stable for thirty years",
         "new traffic did not appear within five years on the Elkford corridor", "the Elkford corridor"),
  cond2=("every figure Duranton and Turner report is drawn from the two decades to 2003",
         "the Pearson expansion was completed in 2011",
         "the Pearson expansion is not among the cases their figures cover", "the Pearson expansion"),
  about="explaining why a measure fails to produce its expected effect by identifying a quantity the usual reasoning treats as fixed",
  implies="the conclusion is drawn entirely from urban cases and may not hold elsewhere"),
# Eight more passages. Two of the four schemas here build their distractors from
# OTHER passages, so with four passages they raised ItemError on every draw and
# contributed nothing; five is the minimum for five choices and twelve gives the
# balance room to work (INC-0086).
 dict( key="saltmarsh",
  topic="salt marsh sediment",
  old="For most of the twentieth century, coastal engineers treated salt marshes as a fixed line that either held against the sea or was lost to it.",
  old_why="Marsh elevation was surveyed against a benchmark on land, so a marsh that kept its height was recorded as holding and one that lost height was recorded as drowning.",
  problem="The surveys had no way to register sediment arriving from upstream, which raises a marsh at the same time as the sea rises beneath it.",
  ev1who="Ravenna and Ostrowski",
  ev1where="a tidal creek system on the Norfolk coast",
  ev1what="the marsh surface rose by four millimetres a year while the local sea level rose by three",
  ev1detail="they measured against horizon markers buried in the peat rather than against a benchmark on shore",
  ev2who="A regional comparison",
  ev2where="nineteen estuaries in eastern England",
  ev2what="marshes fed by rivers carrying suspended sediment gained height and those behind flood defences lost it",
  ev2detail="the defences had been built for reasons unrelated to the marshes, which let the comparison work as a natural experiment",
  revision="whether a marsh survives depends less on the rate of sea level rise than on whether sediment still reaches it",
  caveat="Every estuary in the comparison drains farmland, and the sediment loads there are far higher than a forested catchment would supply.",
  cond1=("every marsh in the comparison that gained height was fed by a river carrying suspended sediment",
         "the Blakeney marsh sits behind a closed sluice",
         "the Blakeney marsh did not gain height",
         "the Blakeney marsh"),
  cond2=("every elevation figure Ravenna reports was measured against a buried horizon marker",
         "the 1974 survey used a benchmark on shore",
         "the 1974 survey is not among the figures Ravenna reports",
         "the 1974 survey"),
  about="replacing an account of coastal marsh loss that measured the wrong thing with one that turns on sediment supply",
  implies="the revised account may not hold where catchments deliver much less sediment than farmland does"),
 dict( key="scriptoria",
  topic="monastic book production",
  old="Historians of the medieval book long held that production collapsed in England between the ninth and the eleventh centuries.",
  old_why="The count of surviving manuscripts from those years is a small fraction of the count from the centuries on either side, and survival was treated as a proxy for output.",
  problem="Survival depends on what happened to a book after it was made, and the dissolution of the monasteries fell unevenly across the collections that held those years.",
  ev1who="Marchetti",
  ev1where="the surviving library catalogues of four southern houses",
  ev1what="the catalogues list three times as many ninth-century volumes as now survive from those houses",
  ev1detail="the catalogues were drawn up before the dissolution and record shelfmarks rather than titles alone",
  ev2who="A second study",
  ev2where="parchment offcuts reused in later bindings",
  ev2what="offcuts datable to the supposed gap are as common as those from the centuries around it",
  ev2detail="binders drew on whatever discarded material lay nearest, so the offcuts sample production rather than preservation",
  revision="the apparent collapse is a gap in what survived rather than a gap in what was made",
  caveat="Both lines of evidence come from houses in the south, and the northern foundations were dispersed under conditions the catalogues do not record.",
  cond1=("every house whose catalogue Marchetti used still held its library at the dissolution",
         "the house at Ramsey had dispersed its books a century earlier",
         "Ramsey is not among the houses whose catalogue Marchetti used",
         "the house at Ramsey"),
  cond2=("every offcut in the second study came from a binding made after 1400",
         "the Winchester fragment was bound in 1260",
         "the Winchester fragment is not in the second study",
         "the Winchester fragment"),
  about="arguing that an apparent decline in medieval book production is an artefact of how books survived rather than of how many were made",
  implies="the conclusion rests on southern collections and may not describe the northern houses at all"),
 dict( key="cicadas",
  topic="periodical cicada emergence",
  old="Entomologists once explained the long prime-numbered life cycles of periodical cicadas as a defence that starves their predators.",
  old_why="A predator whose own cycle is two or three years cannot synchronise with a prey that appears every thirteen or seventeen, so the prey escapes by arithmetic.",
  problem="The account assumes a specialist predator tracking the cicadas, and no predator in the range feeds on them exclusively.",
  ev1who="Duchamp and Reyes",
  ev1where="a long-running site in southern Illinois",
  ev1what="bird populations rose in emergence years and returned to baseline within two seasons, showing no multi-year tracking at all",
  ev1detail="their counts covered thirty-one years, which spans two full emergences of the local brood",
  ev2who="A modelling study",
  ev2where="the same site",
  ev2what="cycles of thirteen and seventeen years minimise overlap between broods rather than with predators",
  ev2detail="the model was fitted to emergence records collected before the hypothesis was formulated",
  revision="the prime cycles are better explained as keeping broods from hybridising than as starving a predator",
  caveat="The model treats hybridisation as uniformly costly, and the cost has been measured in only one pairing of broods.",
  cond1=("every brood in the Illinois record that avoided overlap had a cycle length of thirteen or seventeen years",
         "the Ozark brood runs on a nine-year cycle",
         "the Ozark brood did not avoid overlap",
         "the Ozark brood"),
  cond2=("every count Duchamp reports was taken across a span covering two full emergences",
         "the Kentucky counts ran for eleven years",
         "the Kentucky counts are not among those Duchamp reports",
         "the Kentucky counts"),
  about="replacing a predator-based explanation of cicada life cycles with one that turns on avoiding overlap between broods",
  implies="the replacement depends on a cost that has been measured for only one pair of broods"),
 dict( key="tenements",
  topic="nineteenth-century housing reform",
  old="Urban historians long credited the fall in tenement mortality after 1890 to the building codes passed in that decade.",
  old_why="The codes mandated windows, ventilation shafts and running water, and mortality fell in the years following their passage in city after city.",
  problem="Water filtration was installed across the same cities in the same years, and no study had separated the two.",
  ev1who="Abara",
  ev1where="eleven cities that adopted the codes and filtration at different dates",
  ev1what="mortality fell with filtration wherever the two were separated by more than three years, and did not fall with the codes alone",
  ev1detail="the staggered dates arose from municipal borrowing limits rather than from any judgement about health",
  ev2who="A later reanalysis",
  ev2where="ward-level records in two of those cities",
  ev2what="the fall appeared first in wards on the new mains, whatever the housing stock",
  ev2detail="ward boundaries did not change across the period, so the comparison follows the same populations",
  revision="the fall in mortality followed the water supply rather than the housing codes",
  caveat="Deaths were recorded by ward of residence, and the poorest households moved between wards more often than the records can track.",
  cond1=("every city in Abara's comparison separated the two reforms by more than three years",
         "Providence adopted both in the same year",
         "Providence is not in Abara's comparison",
         "Providence"),
  cond2=("every ward that showed the early fall was connected to the new mains",
         "the Sixth Ward remained on the old supply until 1902",
         "the Sixth Ward did not show the early fall before 1902",
         "the Sixth Ward"),
  about="attributing a fall in urban mortality to water filtration rather than to the housing codes passed at the same time",
  implies="the ward-level result may be weakened by movement between wards that the records cannot follow"),
 dict( key="pidgin",
  topic="creole grammar",
  old="Linguists once treated the shared grammatical features of unrelated creoles as evidence of an innate template surfacing where transmission breaks down.",
  old_why="Creoles that arose thousands of miles apart, from different source languages, converge on the same handling of tense and negation, which chance seemed unlikely to produce.",
  problem="The comparison set was assembled from grammars written by observers trained in the same European tradition.",
  ev1who="Oyelaran",
  ev1where="field recordings from six Atlantic creoles",
  ev1what="three of the shared features are absent in speech and present only in the written grammars",
  ev1detail="the recordings were made with speakers who had no schooling in the lexifier language",
  ev2who="A corpus study",
  ev2where="two Pacific creoles with no Atlantic contact",
  ev2what="the remaining features track the substrate languages rather than appearing independently",
  ev2detail="the substrate languages are well documented from before contact, so the inheritance can be traced",
  revision="the convergence is partly an artefact of how the grammars were written and partly inheritance from substrates",
  caveat="The Pacific corpus covers two creoles, and the Atlantic pattern it is compared against rests on six.",
  cond1=("every feature Oyelaran found in speech is also attested in at least one substrate language",
         "the preverbal marker in Saramaccan is attested in no substrate language",
         "Oyelaran did not find the preverbal marker in Saramaccan in speech",
         "the preverbal marker in Saramaccan"),
  cond2=("every recording in the study was made with a speaker who had no schooling in the lexifier",
         "the Krio speaker had completed secondary school in English",
         "the Krio recording is not in the study",
         "the Krio recording"),
  about="questioning whether the grammatical convergence of unrelated creoles reflects an innate template or the methods used to describe them",
  implies="the Pacific evidence rests on a much smaller sample than the Atlantic pattern it is set against"),
 dict( key="basalt",
  topic="mass extinction timing",
  old="The extinction at the end of the Permian was for decades attributed to the Siberian basalt eruptions alone.",
  old_why="The eruptions are the largest in the rock record and fall within the same interval as the extinction, and no other candidate of that scale was known.",
  problem="The interval could only be dated to within half a million years, which is long enough to contain several distinct causes.",
  ev1who="Kyerematen and Feld",
  ev1where="ash beds bracketing the boundary in southern China",
  ev1what="the main pulse of extinction begins sixty thousand years before the eruptions reach their peak",
  ev1detail="their dates come from zircon crystals, which close to argon loss and so record the eruption rather than later heating",
  ev2who="A second team",
  ev2where="carbon isotope records from three continents",
  ev2what="the earliest disturbance coincides with the intrusion of magma into coal beds rather than with the eruptions at the surface",
  ev2detail="the intrusions release carbon from the coal without producing lava at the surface, so they leave no basalt to date",
  revision="the extinction began with gases released by magma intruding into coal, before the surface eruptions that were long blamed for it",
  caveat="The coal beds are documented in one basin, and whether comparable beds underlie the rest of the province is unknown.",
  cond1=("every date Kyerematen reports comes from a zircon crystal",
         "the Meishan figure was obtained from a whole-rock sample",
         "the Meishan figure is not among the dates Kyerematen reports",
         "the Meishan figure"),
  cond2=("every isotope record showing the earliest disturbance was taken from a section spanning the boundary",
         "the Karoo section stops short of the boundary",
         "the Karoo section does not show the earliest disturbance",
         "the Karoo section"),
  about="moving the cause of an extinction from surface eruptions to the intrusions that preceded them by dating the two separately",
  implies="the mechanism has been documented in one basin and may not extend across the whole province"),
 dict( key="almshouse",
  topic="early modern poor relief",
  old="Social historians long described early modern almshouses as institutions of last resort for the destitute.",
  old_why="Their founding statutes speak of the poor, and the surviving admission registers record occupants with no property to their name.",
  problem="Property was recorded at admission, and an applicant had reason to appear poorer than they were.",
  ev1who="Vestergaard",
  ev1where="probate inventories matched to almshouse registers in two counties",
  ev1what="a third of occupants had held moveable goods worth more than a labourer's annual wage within five years of entry",
  ev1detail="the match was made on parish, name and burial date rather than on name alone",
  ev2who="A study of governors' minutes",
  ev2where="seven foundations in the same counties",
  ev2what="places were commonly filled by nomination from a subscribing family rather than by application",
  ev2detail="the minutes record the nominator by name, which the registers do not",
  revision="almshouse places went as often to the respectable poor with connections as to the destitute",
  caveat="Both counties lie in the wool-producing south, where subscribing families were unusually numerous.",
  cond1=("every occupant Vestergaard matched to an inventory was buried in the parish of the foundation",
         "Agnes Thorne was buried in the next parish",
         "Vestergaard did not match Agnes Thorne to an inventory",
         "Agnes Thorne"),
  cond2=("every place recorded in the governors' minutes names the nominator",
         "the 1683 admissions are recorded without any nominator",
         "the 1683 admissions are not among the places recorded in the minutes",
         "the 1683 admissions"),
  about="revising the view that almshouses served the destitute by showing how places were actually filled",
  implies="the finding comes from a region with unusually many subscribing families and may not generalise"),
 dict( key="birdsong",
  topic="song learning in sparrows",
  old="It was long held that a young sparrow learns its song by copying whichever adult male it hears most often in its first summer.",
  old_why="Birds raised in isolation with a single recorded tutor reproduce that tutor's song, and birds raised in silence never develop a normal song at all.",
  problem="The tutoring experiments offered one song at a time, which cannot show how a bird chooses among the several it hears in the wild.",
  ev1who="Nakamura and Hollings",
  ev1where="an island population colour-ringed since fledging",
  ev1what="young males copied the neighbour they later settled beside, not the adult they had heard most",
  ev1detail="the ringing allowed every bird's territory and every song heard in its first summer to be reconstructed",
  ev2who="A playback experiment",
  ev2where="the same population",
  ev2what="a song heard rarely was copied when it came from the direction the bird later settled in",
  ev2detail="the speakers were moved between seasons, so direction could be varied independently of the song itself",
  revision="song learning is guided by where a bird will settle rather than by how often it hears a song",
  caveat="The island population is unusually dense, and settlement there happens closer to the natal territory than on the mainland.",
  cond1=("every male in the island study copied a song he heard in his first summer",
         "the male ringed as B12 sang a pattern absent from the island that year",
         "B12 did not copy a song he heard in his first summer",
         "the male ringed as B12"),
  cond2=("every playback result came from a season in which the speakers had been moved",
         "the first season used fixed speakers",
         "the first season is not among the playback results",
         "the first season"),
  about="replacing an account of song learning based on frequency of exposure with one based on where a young bird will settle",
  implies="the pattern was found where birds settle unusually close to home and may not hold elsewhere"),
]


def check_corpus():
    """A malformed passage would produce a question with no defensible key, so the shape
    is checked at import rather than trusted."""
    seen = set()
    need = ("old old_why problem ev1who ev1where ev1what ev1detail ev2who ev2where "
            "ev2what ev2detail revision caveat about implies").split()
    for p in P:
        if p["key"] in seen:
            raise ItemError("duplicate passage key %r" % p["key"])
        seen.add(p["key"])
        for f in need:
            if not p.get(f) or not str(p[f]).strip():
                raise ItemError("passage %s is missing %s" % (p["key"], f))
        for c in ("cond1", "cond2"):
            if len(p[c]) != 4 or not all(str(x).strip() for x in p[c]):
                raise ItemError("passage %s has a malformed %s" % (p["key"], c))


check_corpus()


def text(p):
    """The passage as the reader sees it: two paragraphs of the authored sentences."""
    one = " ".join([p["old"], p["old_why"], p["problem"]])
    two = ("%s examined %s and found that %s; %s. %s of %s found that %s, and %s. "
           "Taken together the two results suggest that %s. %s") % (
        p["ev1who"], p["ev1where"], p["ev1what"], p["ev1detail"],
        p["ev2who"], p["ev2where"], p["ev2what"], p["ev2detail"],
        p["revision"], p["caveat"])
    return one + "\n\n" + two


def sentences(p):
    """Everything the passage states, as candidate answers. A distractor drawn from here
    is TRUE of the passage and simply does not answer the stem, which is the trap this
    question type is really about."""
    return {
        "old": p["old"].rstrip("."),
        "old_why": p["old_why"].rstrip("."),
        "problem": p["problem"].rstrip("."),
        "ev1what": p["ev1what"],
        "ev2what": p["ev2what"],
        "ev1detail": p["ev1detail"],
        "ev2detail": p["ev2detail"],
        "revision": p["revision"],
        "caveat": p["caveat"].rstrip("."),
    }


def lower1(s):
    return s[0].lower() + s[1:] if s else s


class RCBase(Gen):
    section = "V"
    type = "RC"
    domain = "nonmath"

    def emit(self, rng, choices_n, p, stem, right, pool, expl, diff, skill, sub):
        cands = [(w, "") for w in pool if w != right]
        if len(cands) < choices_n - 1:
            raise ItemError("%s has only %d distractors" % (self.id, len(cands)))
        opts = [right] + [w for w, _ in balance(rng, right, cands, choices_n - 1)]
        if len(set(opts)) != choices_n:
            raise ItemError("%s drew a repeated option" % self.id)
        rng.shuffle(opts)
        item = {
            "id": None, "section": "V", "type": "RC", "sub": sub, "skill": skill,
            "diff": diff, "passage": text(p), "passageId": "GP_" + p["key"],
            "stem": stem, "choices": opts, "answer": opts.index(right),
            "expl": expl, "gen": self.id, "domain": "nonmath",
            # Identity is the passage plus the question asked of it, never which other
            # sentences of the same passage were offered as distractors.
            "canon_ignores_choices": True,
            "wrong": "Every other choice states something the passage also says. They are "
                     "true, and none of them answers the question that was asked, which is "
                     "what makes them tempting.",
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


class StatedIdea(RCBase):
    """What the passage says. Six askable sentences per passage, each its own question."""
    id = "rc_stated"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 2

    ASKS = [
        ("ev1what", lambda p: "According to the passage, %s found that" % p["ev1who"]),
        ("ev2what", lambda p: "According to the passage, %s of %s found that"
                              % (p["ev2who"], p["ev2where"])),
        ("old_why", lambda p: "The passage indicates that the earlier view was held on the "
                              "grounds that"),
        ("problem", lambda p: "According to the passage, the earlier account failed to "
                              "address the fact that"),
        ("ev1detail", lambda p: "The passage states that, in the work of %s," % p["ev1who"]),
        ("ev2detail", lambda p: "According to the passage, the second set of results also "
                                "established that"),
    ]

    def make(self, rng, choices_n):
        p = rng.choice(P)
        field, stem = rng.choice(self.ASKS)
        s = sentences(p)
        right = lower1(s[field])
        pool = [lower1(v) for k, v in s.items() if k != field]
        expl = ("The passage says exactly this, and the question asks only what it says. "
                "Each of the other choices is also drawn from the passage, so each is true; "
                "none of them is what the stem asked about.")
        return self.emit(rng, choices_n, p, stem(p), right, pool, expl,
                         rng.choice([1, 2, 2, 3]), "v_st", self.sub)


class MainIdea(RCBase):
    """Primary concern, worded in this passage's own terms so it is a distinct item."""
    id = "rc_main"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 3

    def make(self, rng, choices_n):
        p = rng.choice(P)
        others = [q for q in P if q["key"] != p["key"]]
        if len(others) < choices_n - 1:
            raise ItemError("rc_main needs more passages for distractors")
        right = p["about"]
        pool = [q["about"] for q in others]
        expl = ("The passage opens with the received view, shows what it cannot account "
                "for, presents two findings, and states what they support. That is the "
                "shape of the whole passage, and the correct choice describes it. The other "
                "choices describe what a different passage on a different subject does.")
        return self.emit(rng, choices_n, p, "The passage is primarily concerned with",
                         right, pool, expl, rng.choice([2, 3, 3]), "v_st", self.sub)


class Inference(RCBase):
    """Modus tollens over a conditional the passage states.

    The key MUST be true given two things the passage says. The distractors are the two
    classic invalid moves, the converse and the inverse, plus statements the passage does
    not license at all. That is what this question type tests, so the distractors are the
    misconceptions rather than decoration.
    """
    id = "rc_infer"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 4

    def make(self, rng, choices_n):
        p = rng.choice(P)
        cond = rng.choice([p["cond1"], p["cond2"]])
        univ, case, concl, subject = cond
        other = p["cond2"] if cond is p["cond1"] else p["cond1"]
        right = concl[0].upper() + concl[1:] + "."
        pool = [
            # The converse: having the property does not make it a member.
            "Any case with the property described in the passage must be one of those the "
            "passage's generalisation covers.",
            # The inverse: denying the antecedent.
            "Cases outside the passage's generalisation cannot have the property it "
            "describes.",
            other[2][0].upper() + other[2][1:] + ".",
            lower1(p["revision"])[0].upper() + lower1(p["revision"])[1:] + " in every case.",
            p["caveat"].rstrip(".") + " for the same reason.",
        ]
        expl = ("The passage states that %s. It also states that %s. If every case of the "
                "one kind has the property, then a case lacking the property is not a case "
                "of that kind, so %s. The two tempting wrong answers reverse that reasoning: "
                "one assumes that having the property makes a case a member, and the other "
                "assumes that a non-member cannot have it. Neither follows."
                % (univ, case, concl))
        # The stem names the case it asks about. Both conditionals in a passage otherwise
        # produce the identical stem "which of the following can be inferred", so the two
        # collapse into one item and half the inference questions in the corpus vanish.
        stem = ("Which of the following can be properly inferred from the passage about %s?"
                % subject)
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([3, 4, 4, 5]), "v_inf", self.sub)


class CaveatImplication(RCBase):
    """What the author's qualification implies, worded per passage."""
    id = "rc_caveat"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 3

    def make(self, rng, choices_n):
        p = rng.choice(P)
        others = [q for q in P if q["key"] != p["key"]]
        if len(others) < choices_n - 1:
            raise ItemError("rc_caveat needs more passages for distractors")
        right = p["implies"]
        pool = [q["implies"] for q in others]
        expl = ("The closing sentence names a limit on the evidence rather than a doubt "
                "about it, so what it implies is that the revised account has not been "
                "tested outside the range the studies covered. The other choices state "
                "limits that belong to a different passage.")
        stem = "The author's closing observation most strongly suggests that"
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([2, 3, 3, 4]), "v_inf", self.sub)


GENS = [StatedIdea(), MainIdea(), Inference(), CaveatImplication()]
