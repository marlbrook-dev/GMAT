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

  Inferred idea asks what follows. Each passage states two rules of the form "every X
  that showed A also had B", and the question supplies a case that lacks B. Modus tollens
  gives a key that must be true, and the distractors are the converse and inverse errors,
  which are the mistakes this question type is actually testing for.

  "States" means printed. The rules used to be held beside the prose as data, used to
  compute the key and quoted by the explanation, and never printed, so half the keys
  followed from nothing the reader could see (INC-0114). text() now prints both, and
  check_premises fails the build if either is missing from the rendered passage.

Nothing here asserts a key. What the passage states is data; what follows from it is
derived by the same rule every time.
"""
import re

from framework import Gen, ItemError, ListsQuestions, balance, buildable_ranks

# --- the corpus --------------------------------------------------------------------
# Each entry is one passage. Fields are written sentences, not templates:
#   old        the received view, as a full sentence
#   old_why    the reasoning that supported it
#   problem    what it could not account for
#   ev1/ev2    a finding: who, where, what (the finding), detail (a methodological fact).
#              ev2who is stored lower case, the form the middle of a sentence needs,
#              because the stated-idea stem quotes it there; the passage capitalises it
#              where it opens a sentence, which cannot damage a proper noun (INC-0115)
#   revision   the account the evidence supports
#   caveat     a limit the author acknowledges
#   cond1/2    (universal, case, conclusion, subject, scope, near): every X with A had B; this
#              case lacks B; therefore it is not an X with A. The universal is printed
#              in the passage and the case is printed in the stem.
#              scope is the phrase that limits whom the rule covers ("the Canadian
#              survey"), and it matters when the conclusion is an outcome, "the Kivalliq
#              site did not show the reversal": a rule about the eleven surveyed sites
#              says nothing about a site outside them, so the case has to put the subject
#              inside, and the check requires the scope in both. A conclusion that denies
#              membership instead ("is not among", "is not in") holds whether or not the
#              subject was ever in the study, and takes an empty scope.
#              near is two wrong conclusions about the same subject, each claiming
#              something neither premise establishes and at least one worded in the
#              negative, so the key is neither the only choice naming the case nor the
#              only negative one about it (INC-0117).
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
  ev2who="a later survey", ev2where="eleven sites across northern Canada",
  ev2what="the same winter reversal appeared wherever the snowpack exceeded forty centimetres",
  ev2detail="deep snow insulates the soil well enough for microbes to stay active beneath it",
  revision="whether the tundra is a sink depends on the season in which it is measured and on how much snow falls",
  caveat="None of the sites studied lies south of the treeline, where soils are warmer and the snowpack thinner.",
  cond1=("every site in the Canadian survey that showed the winter reversal had a snowpack deeper than forty centimetres",
         "the Kivalliq site, one of the eleven in the Canadian survey, recorded a snowpack of twenty-two centimetres",
         "the Kivalliq site did not show the winter reversal",
         "the Kivalliq site",
         "the Canadian survey",
         ("the Kivalliq site released no carbon at all between October and April",
          "the Kivalliq site stayed too cold in winter for microbes to remain active")),
  cond2=("every reading that captured the reversal was taken by an instrument running through the winter",
         "the Barrow readings were taken only in July and August",
         "the Barrow readings are not among those that captured the reversal",
         "the Barrow readings",
         "",
         ("the Barrow readings show that no winter reversal occurs near Barrow",
          "the Barrow readings show the tundra near Barrow to be a carbon sink")),
  about="revising a settled account of Arctic carbon by showing that it rested on measurements taken in one season only",
  implies="the revised account has not been tested in the warmer conditions south of the treeline"),

 dict(key="guilds", topic="English craft guilds",
  old="Historians long explained the decline of the English craft guilds as a consequence of industrial machinery.",
  old_why="Machinery is assumed to have made the guild workshop uneconomic almost as soon as it arrived.",
  problem="The chronology has never fit, because most guilds lost their membership decades before machinery reached their trades.",
  ev1who="Halloway", ev1where="the admission books of the Sheffield cutlers",
  ev1what="membership fell by half between 1790 and 1820, a generation before mechanised grinding entered the trade",
  ev1detail="the books record every admission with a date and a named sponsor",
  ev2who="a study of apprenticeship indentures", ev2where="four other Sheffield trades",
  ev2what="the same early fall appeared wherever the guild had lost its power to prosecute unlicensed work",
  ev2detail="that power was removed by statute at different dates in different trades",
  revision="the guilds were undone by the loss of their legal monopoly, and machinery arrived to find them already weakened",
  caveat="The Sheffield records are unusually complete, and no comparable series survives for the textile towns.",
  cond1=("every trade in the indenture study that showed the early fall had already lost its power to prosecute unlicensed work",
         "the farriers, one of the trades in the indenture study, kept their power to prosecute unlicensed work until 1835",
         "the farriers did not show the early fall before 1835",
         "the farriers",
         "the indenture study",
         ("the farriers' membership did not fall until mechanised work reached their trade",
          "the farriers lost members to the cutlers after 1835")),
  cond2=("every source Halloway used records a sponsor for each admission",
         "the cutlers' journeyman register records no sponsors",
         "the journeyman register is not among the sources Halloway used",
         "the journeyman register",
         "",
         ("the journeyman register does not record the fall in the cutlers' membership",
          "the journeyman register overstates the fall in membership that Halloway reports")),
  about="reordering the causes of an institutional decline by showing that the usual explanation arrives too late to account for it",
  implies="the argument may not extend to trades whose records have not survived"),

 dict(key="reefs", topic="coral colour",
  old="For most of the twentieth century, marine biologists attributed the bright colour of shallow water corals to the pigments of the algae living inside them.",
  old_why="The algae are the obvious source, since they are abundant, pigmented, and present in every healthy colony.",
  problem="The explanation cannot account for corals that stay vividly coloured after the algae have been expelled.",
  ev1who="Takeda", ev1where="a reef flat in the Ryukyu Islands",
  ev1what="bleached colonies went on fluorescing for up to nine weeks, long after any algal pigment would have degraded",
  ev1detail="the colonies were photographed each week under light of identical intensity",
  ev2who="a later laboratory study", ev2where="colonies raised without algae from the larval stage",
  ev2what="the coral itself produces the fluorescent proteins, in every colony kept under strong light",
  ev2detail="colonies held in shade produced almost none of the proteins",
  revision="the colour belongs to the coral, and the algae contribute to it only indirectly",
  caveat="Whether the proteins shield the coral from light, as is often suggested, remains untested.",
  cond1=("every colony in the laboratory study that produced the fluorescent proteins in quantity was kept under strong light",
         "the colonies in the fourth tank of the laboratory study were held in shade throughout",
         "the colonies in the fourth tank did not produce the fluorescent proteins in quantity",
         "the colonies in the fourth tank",
         "the laboratory study",
         ("the colonies in the fourth tank did not survive the laboratory study",
          "the colonies in the fourth tank took their colour from algal pigment instead")),
  cond2=("every colony Takeda photographed was recorded under light of identical intensity",
         "the colonies at the reef margin were photographed under daylight that varied from week to week",
         "the colonies at the reef margin were not among those Takeda photographed",
         "the colonies at the reef margin",
         "",
         ("the colonies at the reef margin did not fluoresce after bleaching",
          "the colonies at the reef margin fluoresced for longer than nine weeks")),
  about="relocating the source of a familiar phenomenon from an organism's partner to the organism itself",
  implies="the function of the proteins remains an open question even though their source is now settled"),

 dict(key="roads", topic="road widening",
  old="Transport planners have generally assumed that widening a congested road reduces the time drivers spend on it.",
  old_why="The same traffic spread across more lanes should move faster, which is true of any fixed quantity of vehicles.",
  problem="The assumption treats the number of drivers as fixed, and it is not.",
  ev1who="Duranton and Turner", ev1where="the interstate network of 228 American cities",
  ev1what="vehicle miles travelled rose almost exactly in proportion to the lane miles added, leaving average speeds unchanged",
  ev1detail="their comparison covers the two decades to 2003",
  ev2who="a narrower study", ev2where="six corridors widened in the same period",
  ev2what="the new traffic appeared within five years wherever the corridor joined two growing suburbs",
  ev2detail="corridors between districts of stable population kept their improved speeds",
  revision="added capacity is taken up by drivers who did not previously make the trip, so widening relieves congestion only where surrounding demand is not growing",
  caveat="Every corridor studied is urban, and nothing here settles the case for rural routes.",
  cond1=("every corridor in the narrower study where new traffic appeared within five years joined two growing suburbs",
         "the Elkford corridor, one of the six in the narrower study, runs between districts whose population has been stable for thirty years",
         "new traffic did not appear within five years on the Elkford corridor",
         "the Elkford corridor",
         "the narrower study",
         ("the Elkford corridor did not need widening in the first place",
          "the Elkford corridor carried less traffic after it was widened than before")),
  cond2=("every figure Duranton and Turner report is drawn from the two decades to 2003",
         "the Pearson expansion was begun and completed between 2008 and 2011",
         "the Pearson expansion is not among the cases Duranton and Turner's figures cover",
         "the Pearson expansion",
         "",
         ("the Pearson expansion did not change average speeds on its route",
          "the Pearson expansion drew drivers who had not previously made the trip")),
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
  ev2who="a regional comparison",
  ev2where="nineteen estuaries in eastern England",
  ev2what="marshes fed by rivers carrying suspended sediment gained height and those behind flood defences lost it",
  ev2detail="the defences had been built for reasons unrelated to the marshes, which let the comparison work as a natural experiment",
  revision="whether a marsh survives depends less on the rate of sea level rise than on whether sediment still reaches it",
  caveat="Every estuary in the comparison drains farmland, and the sediment loads there are far higher than a forested catchment would supply.",
  cond1=("every marsh in the regional comparison that gained height was fed by a river carrying suspended sediment",
         "the Blakeney marsh, one of those in the regional comparison, sits behind a closed sluice that lets no river water through",
         "the Blakeney marsh did not gain height",
         "the Blakeney marsh",
         "the regional comparison",
         ("the Blakeney marsh did not lose height either",
          "the Blakeney marsh was drowned by the rising sea")),
  cond2=("every elevation figure Ravenna and Ostrowski report was measured against a buried horizon marker",
         "the 1974 survey measured elevation only against a benchmark on shore",
         "the 1974 survey's figures are not among those Ravenna and Ostrowski report",
         "the 1974 survey",
         "",
         ("the 1974 survey did not register any marsh as drowning",
          "the 1974 survey recorded the Norfolk marsh as holding its height")),
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
  ev2who="a second study",
  ev2where="parchment offcuts reused in later bindings",
  ev2what="offcuts datable to the supposed gap are as common as those from the centuries around it",
  ev2detail="binders drew on whatever discarded material lay nearest, so the offcuts sample production rather than preservation",
  revision="the apparent collapse is a gap in what survived rather than a gap in what was made",
  caveat="Both lines of evidence come from houses in the south, and the northern foundations were dispersed under conditions the catalogues do not record.",
  cond1=("every house whose catalogue Marchetti used still held its library at the dissolution",
         "the house at Ramsey held no library at the dissolution, having dispersed its books a century before",
         "Ramsey is not among the houses whose catalogue Marchetti used",
         "the house at Ramsey",
         "",
         ("Ramsey did not produce books during the supposed gap",
          "Ramsey's books were dispersed at the dissolution")),
  cond2=("every offcut in the second study came from a binding made after 1400",
         "the Winchester fragment survives only in a binding made in 1260",
         "the Winchester fragment is not in the second study",
         "the Winchester fragment",
         "",
         ("the Winchester fragment does not date from the supposed gap",
          "the Winchester fragment was cut from a book made in the ninth century")),
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
  ev2who="a modelling study",
  ev2where="the same site",
  ev2what="cycles of thirteen and seventeen years minimise overlap between broods rather than with predators",
  ev2detail="the model was fitted to emergence records collected before the hypothesis was formulated",
  revision="the prime cycles are better explained as keeping broods from hybridising than as starving a predator",
  caveat="The model treats hybridisation as uniformly costly, and the cost has been measured in only one pairing of broods.",
  cond1=("every cycle length that minimised overlap in the modelling study was thirteen or seventeen years",
         "the modelling study also tested a cycle length of fifteen years",
         "a cycle length of fifteen years did not minimise overlap in the modelling study",
         "a cycle length of fifteen years",
         "the modelling study",
         ("a cycle length of fifteen years did not protect broods in the modelling study from predators",
          "a cycle length of fifteen years produced more hybrid broods in the modelling study than seventeen")),
  cond2=("every count Duchamp and Reyes report was taken across a span covering two full emergences",
         "the Kentucky counts ran for eleven years",
         "the Kentucky counts are not among those Duchamp and Reyes report",
         "the Kentucky counts",
         "",
         ("the Kentucky counts showed no rise in birds in emergence years",
          "the Kentucky counts showed birds tracking the cicadas over several years")),
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
  ev2who="a later reanalysis",
  ev2where="ward-level records in two of those cities",
  ev2what="the fall appeared first in wards on the new mains, whatever the housing stock",
  ev2detail="ward boundaries did not change across the period, so the comparison follows the same populations",
  revision="the fall in mortality followed the water supply rather than the housing codes",
  caveat="Deaths were recorded by ward of residence, and the poorest households moved between wards more often than the records can track.",
  cond1=("every city in Abara's comparison adopted the building codes and filtration in different years",
         "Providence adopted the building codes and filtration in the same year",
         "Providence is not in Abara's comparison",
         "Providence",
         "",
         ("mortality in Providence did not fall after filtration was installed",
          "mortality in Providence fell with the building codes alone")),
  cond2=("every ward in the reanalysis that showed the early fall was connected to the new mains",
         "the Sixth Ward, one of those in the reanalysis, remained on the old supply until 1902",
         "the Sixth Ward did not show the early fall before 1902",
         "the Sixth Ward",
         "the reanalysis",
         ("the Sixth Ward's mortality did not fall after it joined the new mains",
          "the Sixth Ward had worse housing than the wards on the new mains before 1902")),
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
  ev2who="a corpus study",
  ev2where="two Pacific creoles with no Atlantic contact",
  ev2what="the remaining features track the substrate languages rather than appearing independently",
  ev2detail="the substrate languages are well documented from before contact, so the inheritance can be traced",
  revision="the convergence is partly an artefact of how the grammars were written and partly inheritance from substrates",
  caveat="The Pacific corpus covers two creoles, and the Atlantic pattern it is compared against rests on six.",
  cond1=("every feature Oyelaran found in speech is also attested in at least one substrate language",
         "the preverbal marker in Saramaccan is attested in no substrate language",
         "the preverbal marker in Saramaccan is not among the features Oyelaran found in speech",
         "the preverbal marker in Saramaccan",
         "",
         ("the preverbal marker in Saramaccan does not appear in the written grammars",
          "the preverbal marker in Saramaccan reflects an innate template rather than a substrate language")),
  cond2=("every recording Oyelaran used was made with a speaker who had no schooling in the lexifier",
         "the Krio recording was made with a speaker who had completed secondary school in English, the lexifier of Krio",
         "the Krio recording is not among those Oyelaran used",
         "the Krio recording",
         "",
         ("the Krio recording contains none of the shared features",
          "the Krio recording reproduces features found only in the written grammars of Krio")),
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
  ev1detail="their dates come from zircon crystals, which retain their lead when later heated and so record the eruption rather than any later event",
  ev2who="a second team's study",
  ev2where="carbon isotope records from three continents",
  ev2what="the earliest disturbance coincides with the intrusion of magma into coal beds rather than with the eruptions at the surface",
  ev2detail="the intrusions release carbon from the coal without producing lava at the surface, so they leave no basalt to date",
  revision="the extinction began with gases released by magma intruding into coal, before the surface eruptions that were long blamed for it",
  caveat="The coal beds are documented in one basin, and whether comparable beds underlie the rest of the province is unknown.",
  cond1=("every date Kyerematen and Feld report comes from a zircon crystal",
         "the Meishan figure was obtained from a whole-rock sample",
         "the Meishan figure is not among the dates Kyerematen and Feld report",
         "the Meishan figure",
         "",
         ("the Meishan figure does not come from an ash bed",
          "the Meishan figure places the extinction after the eruptions reached their peak")),
  cond2=("every isotope record in the second team's study that showed the earliest disturbance was taken from a section spanning the boundary",
         "the Karoo section, which supplied one of the records in the second team's study, stops short of the boundary",
         "the isotope record from the Karoo section does not show the earliest disturbance",
         "the Karoo section",
         "the second team's study",
         ("the Karoo section contains no coal beds intruded by magma",
          "the Karoo section records the surface eruptions rather than the intrusions")),
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
  ev2who="a study of governors' minutes",
  ev2where="seven foundations in the same counties",
  ev2what="places were commonly filled by nomination from a subscribing family rather than by application",
  ev2detail="the minutes record the nominator by name, which the registers do not",
  revision="almshouse places went as often to the respectable poor with connections as to the destitute",
  caveat="Both counties lie in the wool-producing south, where subscribing families were unusually numerous.",
  cond1=("every occupant Vestergaard matched to an inventory was buried in the parish of the foundation",
         "Agnes Thorne was buried in a parish other than that of the foundation where she lived",
         "Agnes Thorne is not among the occupants Vestergaard matched to an inventory",
         "Agnes Thorne",
         "",
         ("Agnes Thorne held no property when she entered the almshouse",
          "Agnes Thorne was admitted on the nomination of a subscribing family")),
  cond2=("every place recorded in the governors' minutes names the nominator",
         "the 1683 admissions are recorded without any nominator",
         "the 1683 admissions are not among the places recorded in the minutes",
         "the 1683 admissions",
         "",
         ("the 1683 admissions were not filled by nomination",
          "the 1683 admissions went to applicants with no property")),
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
  ev2who="a playback study",
  ev2where="the same population",
  ev2what="a song heard rarely was copied when it came from the direction the bird later settled in",
  ev2detail="the speakers were moved between seasons, so direction could be varied independently of the song itself",
  revision="song learning is guided by where a bird will settle rather than by how often it hears a song",
  caveat="The island population is unusually dense, and settlement there happens closer to the natal territory than on the mainland.",
  cond1=("every male in the island study had been colour-ringed as a fledgling",
         "the male known as B12 was first ringed as an adult",
         "B12 is not among the males in the island study",
         "the male known as B12",
         "",
         ("B12 did not settle beside the neighbour whose song he copied",
          "B12 copied the adult he heard most often in his first summer")),
  cond2=("every trial in the playback study used a speaker placed in a new position that season",
         "the pilot trials used a speaker left where it had stood the year before",
         "the pilot trials are not among those in the playback study",
         "the pilot trials",
         "",
         ("the pilot trials did not lead any bird to copy a rarely heard song",
          "the pilot trials showed that where a speaker stood has no effect on which song is copied")),
  about="replacing an account of song learning based on frequency of exposure with one based on where a young bird will settle",
  implies="the pattern was found where birds settle unusually close to home and may not hold elsewhere"),
 dict( key="bees",
  topic="honeybee foraging",
  old="Behavioural ecologists long treated the waggle dance as the key to the foraging success of honeybee colonies.",
  old_why="A dancer encodes the direction and distance of a food source in her movements, and recruits who follow her dance reach the source far more often than bees searching alone.",
  problem="The comparison measured what the dance allows a recruit to do, not how much the colony as a whole gains from it.",
  ev1who="Marwick and Solis",
  ev1where="hives whose dancers had been disoriented by diffuse lighting",
  ev1what="colonies unable to read the dance gathered as much food as normal colonies through most of the season",
  ev1detail="the hives were paired by size and placed side by side, so both members of a pair drew on the same flowers",
  ev2who="a follow-up study",
  ev2where="the same hives in a year of patchy bloom",
  ev2what="the colonies that could read the dance gathered more only when food was concentrated in a few rich and distant patches",
  ev2detail="the bloom was mapped each week, so the patchiness of the forage was measured rather than assumed",
  revision="the dance pays off only where forage is scarce and clustered, and elsewhere it adds little to what independent searching finds",
  caveat="Both studies used one strain of bee in temperate farmland, where the flowering calendar is unusually predictable.",
  cond1=("every week in the follow-up study in which the dance-reading colonies gathered more was a week of concentrated bloom",
         "in the week of 14 June the bloom in the follow-up study was spread evenly across the fields",
         "the dance-reading colonies did not gather more in the week of 14 June",
         "the week of 14 June",
         "the follow-up study",
         ("the dance-reading colonies did not forage at all in the week of 14 June",
          "the dance-reading colonies gathered less than the others in the week of 14 June")),
  cond2=("every hive in either study was paired with a hive of the same size",
         "the Ferndale hive had no partner of its size",
         "the Ferndale hive is not among the hives in either study",
         "the Ferndale hive",
         "",
         ("the Ferndale hive could not read the dance",
          "the Ferndale hive gathered more food than the paired hives")),
  about="reassessing the value of a celebrated behaviour by asking how much a group gains from it rather than what it lets an individual do",
  implies="the payoff of the dance has not been measured where flowering is less predictable than on temperate farmland"),
 dict( key="ledgers",
  topic="Victorian postal reform",
  old="Historians of communication long credited cheap uniform postage with turning letter writing into a habit of ordinary households.",
  old_why="Letter volumes multiplied within a few years of the reform, and the reformers themselves had argued that high charges were what kept the poor from writing.",
  problem="A national count of letters cannot say who was writing them, and the reform lowered the cost of business correspondence as much as that of personal letters.",
  ev1who="Ashworth",
  ev1where="the sorting ledgers of two northern towns",
  ev1what="most of the growth in the decade after the reform came from firms rather than from households",
  ev1detail="the ledgers record the sender's address, which can be matched against trade directories",
  ev2who="a study of family papers",
  ev2where="working households in the same towns",
  ev2what="personal letters became common only a generation later, once schooling had spread",
  ev2detail="the papers were deposited by descendants rather than chosen by historians, so no one selected them to fit an argument",
  revision="cheap postage made personal correspondence possible for ordinary households but did not make it common, which waited on literacy",
  caveat="Both towns were centres of manufacturing, where firms wrote far more letters than they did in market towns.",
  cond1=("every sender whose letters Ashworth counted as business mail was listed in a trade directory",
         "the Pellow household appears in no trade directory",
         "the Pellow household is not among the senders whose letters Ashworth counted as business mail",
         "the Pellow household",
         "",
         ("the Pellow household did not send any letters in the decade after the reform",
          "the Pellow household wrote mainly to relatives who had moved away")),
  cond2=("every household in the study of family papers whose papers include personal letters from the decade after the reform had a member who had attended school",
         "the Brierley household, one of those in the study of family papers, had no member who had ever attended school",
         "the Brierley household's papers include no personal letters from the decade after the reform",
         "the Brierley household",
         "the study of family papers",
         ("the Brierley household received no letters from firms in the decade after the reform",
          "the Brierley household relied on a neighbour to write its letters")),
  about="separating what a reform made possible from what it caused, by asking who used it and when",
  implies="the share of the growth that came from firms may have been smaller in towns with less manufacturing"),
 dict( key="seedvariety",
  topic="crop adoption",
  old="Development economists long explained which farmers adopted new seed varieties by the yield advantage the seed offered them.",
  old_why="Adoption was highest where trials showed the largest gains, and farmers asked why they had switched most often named the harvest.",
  problem="The regions with the largest gains were also those with the most rural lenders, and a farmer's own account of a decision is not evidence of what made it possible.",
  ev1who="Achterberg and Nwosu",
  ev1where="neighbouring villages that differed in access to a lender but not in soil or rainfall",
  ev1what="adoption was three times higher in the villages with a lender, although trials had shown the same yield gain in both",
  ev1detail="the villages were chosen from a survey completed before the seed was released, so the comparison was fixed in advance",
  ev2who="a later study",
  ev2where="farmers offered the seed on credit at random",
  ev2what="those offered credit adopted at the rate of the villages with a lender, whatever their soil",
  ev2detail="the offer was assigned by lottery, so the farmers who received it did not differ from the rest in any way that could explain the result",
  revision="access to credit rather than the yield advantage decides who adopts, and the yield advantage matters only once the seed can be paid for",
  caveat="Both studies concern a single seed sold at a single price, and a cheaper variety might not need credit at all.",
  cond1=("every farmer in the later study who adopted the seed in its first season had been offered credit or already had a lender",
         "the farmer on plot 212, one of those in the later study, had neither an offer of credit nor a lender",
         "the farmer on plot 212 did not adopt the seed in its first season",
         "the farmer on plot 212",
         "the later study",
         ("the farmer on plot 212 did not plant any new variety that year",
          "the farmer on plot 212 had the poorest soil in the later study")),
  cond2=("every village in Achterberg and Nwosu's comparison had been surveyed before the seed was released",
         "the village of Kanta was first surveyed a year after the seed was released",
         "the village of Kanta is not among the villages in Achterberg and Nwosu's comparison",
         "the village of Kanta",
         "",
         ("the village of Kanta did not have a lender when the seed was released",
          "the village of Kanta adopted the seed faster than the villages with a lender")),
  about="showing that a decision explained by its benefits was governed by the means to act on them",
  implies="the role of credit may be smaller for a seed that costs less"),
 dict(key="glacier", topic="mountain glacier retreat",
  old="Glaciologists long attributed the retreat of the Hallin glacier to rising summer temperatures.",
  old_why="The glacier's front withdrew fastest in the decades when summers were warmest at the valley weather station.",
  problem="The weather station stands two thousand metres below the ice, and no one had measured how much snow fell on the glacier itself.",
  ev1who="Ferreira and Haldane", ev1where="snow cores drilled at twelve points across the upper glacier",
  ev1what="winter snowfall on the glacier had halved since the 1950s while summer melt had changed little",
  ev1detail="the cores were dated by layers of ash from eruptions whose years are known",
  ev2who="a later study", ev2where="the Varre glacier on the far side of the range",
  ev2what="the Varre glacier, whose snowfall has not declined, has held its front steady over the same decades although its summers warmed as much",
  ev2detail="the two glaciers lie at the same height and face the same way",
  revision="the Hallin glacier is shrinking mainly because less snow reaches it rather than because more of it melts",
  caveat="The cores record only the last seventy years, and the glacier's earlier retreats cannot be tested this way.",
  cond1=("every core in the Ferreira and Haldane study was drilled above three thousand metres",
         "the Sella core was drilled at two thousand four hundred metres",
         "the Sella core is not in the Ferreira and Haldane study",
         "the Sella core",
         "",
         ("the Sella core shows no fall in winter snowfall",
          "the Sella core was never dated by its layers of ash")),
  cond2=("every season in the later study in which the Varre front advanced followed a winter of heavy snow",
         "the 1987 season, one of those in the later study, followed a winter of light snow",
         "the Varre front did not advance in the 1987 season",
         "the 1987 season",
         "the later study",
         ("the Varre glacier lost no ice at all in the 1987 season",
          "the summer of 1987 was not warmer than the summers around it")),
  about="arguing that a glacier's retreat reflects falling snowfall rather than warming, by measuring what reaches the ice instead of relying on a distant weather station",
  implies="the snowfall explanation has not been tested for the glacier's retreats before the last seventy years"),

 dict(key="orchards", topic="orchard pollination",
  old="Growers long assumed that the valley's orchards set fruit only when rented honeybee hives were brought in at blossom.",
  old_why="Yields rose in the seasons when hives were rented and fell in the seasons when they were not.",
  problem="The seasons without rented hives were also the coldest springs, when few insects of any kind fly and blossom is often damaged by frost.",
  ev1who="Maddox", ev1where="forty orchards in which hives were withheld from alternate rows during mild springs",
  ev1what="rows without hives set as much fruit as the rows beside them wherever a hedgerow lay within two hundred metres",
  ev1detail="the rows were assigned by lot, so no grower chose which trees went without hives",
  ev2who="a later survey", ev2where="the bees visiting the same orchards",
  ev2what="solitary bees nesting in the hedgerows made most of the visits to blossom in the rows without hives",
  ev2detail="the visits were counted by observers who did not know which rows had hives",
  revision="in mild springs wild bees from nearby hedgerows can pollinate the orchards without rented hives",
  caveat="All forty orchards lie in the lower part of the valley, where hedgerows are more common than on the upper slopes.",
  cond1=("every orchard in Maddox's trial was planted with a single variety of apple",
         "the Linden orchard grows three varieties of apple in alternating rows",
         "the Linden orchard is not in Maddox's trial",
         "the Linden orchard",
         "",
         ("the Linden orchard sets no fruit without rented hives",
          "the Linden orchard has never been visited by solitary bees")),
  cond2=("every row in the survey that received most of its visits from solitary bees lay within two hundred metres of a hedgerow",
         "the north row of the Ashby orchard, one of those in the survey, lies four hundred metres from any hedgerow",
         "the north row of the Ashby orchard did not receive most of its visits from solitary bees",
         "the north row of the Ashby orchard",
         "the survey",
         ("the north row of the Ashby orchard set no fruit in the mild springs",
          "the north row of the Ashby orchard received no visits from bees of any kind")),
  about="showing that wild bees can do the work credited to rented hives, by separating the hives from the cold springs that coincided with their absence",
  implies="the finding may not hold for orchards on the upper slopes, where hedgerows are scarcer"),

 dict(key="hymnals", topic="parish hymn singing",
  old="Musicologists long held that the harmonised hymn spread through rural parishes from the cathedral choirs that first sang it.",
  old_why="Parish books containing harmonised hymns appear only after the cathedrals adopted them, and in order of distance from each cathedral.",
  problem="The dates come from the books that survive, and parish books were kept and reused far longer in some dioceses than in others.",
  ev1who="Okonjo", ev1where="the payments recorded in parish accounts for the copying of music",
  ev1what="parishes paid copyists for harmonised hymns up to thirty years before the nearest cathedral adopted them",
  ev1detail="the accounts name the copyist and the number of pages in each payment",
  ev2who="a later study", ev2where="the licences issued to travelling singing teachers in four dioceses",
  ev2what="the teachers who carried the new hymns moved between market towns rather than outward from the cathedral cities",
  ev2detail="each licence records the towns in which its holder was permitted to teach",
  revision="the harmonised hymn reached the parishes through teachers working the market towns, often before the cathedrals took it up",
  caveat="Accounts survive for only a minority of parishes, and those that kept them may not have been typical.",
  cond1=("every parish in Okonjo's sample kept accounts that name the copyist for each payment",
         "the accounts of Stow Green record payments for music without naming any copyist",
         "Stow Green is not in Okonjo's sample",
         "Stow Green",
         "",
         ("Stow Green never paid for copies of harmonised hymns",
          "Stow Green adopted the hymns only after the nearest cathedral did")),
  cond2=("every teacher in the licence study who carried the new hymns was licensed to teach in at least three market towns",
         "Thomas Reave, one of the teachers in the licence study, was licensed to teach in a single town",
         "Thomas Reave did not carry the new hymns",
         "Thomas Reave",
         "the licence study",
         ("Thomas Reave never taught singing in a cathedral city",
          "Thomas Reave was not paid for copying any music")),
  about="tracing a musical practice to the teachers who carried it between market towns rather than to the cathedrals credited with spreading it",
  implies="the parishes whose accounts survive may not represent the parishes whose accounts are lost"),
]


# The same structure at LSAT length. Measured as the reader sees them, with both rules
# printed, P runs 202 to 280 words, which is GMAT length, and these run 283 to 442.
# Length is most of what distinguishes LSAT reading, so the two corpora are kept apart and
# the LSAT draws only from this one. The GMAT draws from both, because a real GMAT section
# mixes short passages with longer ones.
P_LONG = [
 dict( key="riparian",
  topic="water rights doctrine",
  old="Legal historians long treated the shift from riparian rights to prior appropriation in the western United States as a straightforward response to aridity, arguing that a doctrine tying water use to ownership of the adjoining bank could not survive in country where the rain did not fall reliably and the rivers ran far from the land that needed them.",
  old_why="The doctrine of prior appropriation, which awards water to whoever first puts it to beneficial use regardless of where their land lies, appears purpose-built for such conditions, and the territories that adopted it earliest were among the driest, so the correlation between climate and doctrine seemed to require no further explanation.",
  problem="The account cannot explain why several equally arid territories retained riparian rules for decades, nor why some comparatively wet jurisdictions adopted appropriation early, and it treats a body of law made by particular legislatures and courts as though it were a precipitation map.",
  ev1who="Ferreira and Lindgren",
  ev1where="the territorial statutes and court records of nine western jurisdictions",
  ev1what="the doctrine adopted tracked the dominant early industry far more closely than it tracked rainfall, with placer mining districts adopting appropriation within a decade of settlement and ranching districts retaining riparian rules well beyond it",
  ev1detail="they coded each jurisdiction by the industry that first organised its water claims, using the claims registers themselves rather than later economic summaries written after the doctrine was settled",
  ev2who="a subsequent study of litigation",
  ev2where="three of those same jurisdictions across forty years",
  ev2what="the timing of doctrinal change followed the arrival of capital that needed secure title to water at a distance from the stream, not any measurable change in the water available",
  ev2detail="the investment records survive because the ventures were incorporated, which means the dates can be fixed independently of the court records they are being compared against",
  revision="the doctrine followed the pattern of industrial demand for transportable, securable water rights rather than the physical scarcity of water itself",
  caveat="All nine jurisdictions were organised under territorial rather than state legislatures, whose members were appointed and whose statutes were subject to congressional revision.",
  cond1=("every jurisdiction in Ferreira and Lindgren's study that adopted appropriation within a decade had an organised placer mining district",
         "the Sweetwater jurisdiction, one of the nine in Ferreira and Lindgren's study, had no mining district of any kind",
         "the Sweetwater jurisdiction did not adopt appropriation within a decade",
         "the Sweetwater jurisdiction",
         "Ferreira and Lindgren's study",
         ("the Sweetwater jurisdiction never adopted appropriation",
          "the Sweetwater jurisdiction received more rain than those that adopted appropriation")),
  cond2=("every jurisdiction Ferreira and Lindgren coded had surviving claims registers",
         "no claims register survives for the Bitterroot jurisdiction",
         "the Bitterroot jurisdiction is not among those Ferreira and Lindgren coded",
         "the Bitterroot jurisdiction",
         "",
         ("the Bitterroot jurisdiction did not organise its water claims around mining",
          "the Bitterroot jurisdiction retained riparian rules for decades")),
  about="displacing a climatic explanation of a legal change with one that turns on who needed the water and on what terms",
  implies="the pattern was established under territorial legislatures whose lawmaking differed from that of the states which succeeded them"),
 dict( key="lichen",
  topic="lichen symbiosis",
  old="For more than a century after Simon Schwendener proposed it in 1867, the standard account of lichens held that each one is a partnership of exactly two organisms, a fungus that provides the structure and an alga or cyanobacterium that provides the sugars, and that the fungal partner alone determines which species a given lichen belongs to.",
  old_why="The two-partner account was established by separating lichens into their components and growing each in isolation, which reliably yielded one fungus and one photosynthetic partner, and by the observation that lichen taxonomy built on fungal characters produced a classification that was stable and predictive.",
  problem="It could not explain why two lichens with identical fungal and algal partners sometimes differ markedly in form, chemistry and habitat, a discrepancy that was recorded repeatedly and set aside as an effect of local conditions.",
  ev1who="Nkemelu and Oberti",
  ev1where="paired collections of two such lichens from the same rock faces",
  ev1what="a basidiomycete yeast is embedded in the outer layer of one form and absent from the other, in every pair examined",
  ev1detail="they searched for it with sequencing rather than by culture, which matters because the yeast does not grow in isolation and a century of separation experiments would therefore have missed it",
  ev2who="a survey of herbarium material",
  ev2where="collections from six continents",
  ev2what="the same yeast lineage occurs across lichens that are otherwise unrelated, and its presence predicts the chemical differences that had been attributed to habitat",
  ev2detail="the herbarium specimens predate the hypothesis by decades, so the sampling cannot have been shaped by what the investigators expected to find",
  revision="a lichen is a community whose members are not fully enumerated by separating and culturing its parts, and some of its characters belong to partners the classical method could not see",
  caveat="The yeast has been shown to be present rather than shown to be necessary, and no lichen has yet been assembled from its components with and without it.",
  cond1=("every pair Nkemelu and Oberti examined was collected from a single rock face",
         "the Patagonian pair was assembled from two localities",
         "the Patagonian pair is not among those Nkemelu and Oberti examined",
         "the Patagonian pair",
         "",
         ("the Patagonian pair does not contain the basidiomycete yeast",
          "the Patagonian pair differs in form only because of local conditions")),
  cond2=("every specimen in the herbarium survey was collected before the hypothesis was proposed",
         "the Tasmanian material was collected after the hypothesis was proposed",
         "the Tasmanian material is not in the herbarium survey",
         "the Tasmanian material",
         "",
         ("the Tasmanian material contains none of the yeast lineage",
          "the Tasmanian material was collected to confirm the hypothesis")),
  about="showing that a long-standing account of an organism was limited by the method used to establish it rather than by the evidence available",
  implies="the revised account establishes that a third partner is present without yet establishing what it does"),
 dict( key="assize",
  topic="medieval grain prices",
  old="Economic historians of medieval England long read the assize of bread, the regulation fixing the weight of a loaf against the price of grain, as evidence that town authorities were able to control the cost of food, and they used the surviving assize records as a direct index of what bread actually cost.",
  old_why="The assize tables are unusually complete, they were revised whenever grain prices moved, and the penalties for selling underweight loaves were recorded and enforced, so the records appeared to describe a functioning price mechanism rather than an aspiration.",
  problem="The records show what the authorities ordered and what they punished, and a series built from enforcement actions cannot distinguish a market in which the rule was generally obeyed from one in which it was generally ignored and occasionally prosecuted.",
  ev1who="Duarte",
  ev1where="the borough court rolls of four towns alongside their assize tables",
  ev1what="prosecutions cluster in the weeks following each revision of the table and fall away afterwards, a pattern that fits intermittent enforcement rather than steady compliance",
  ev1detail="she counted prosecutions per baker rather than in total, which separates a rise caused by more bakers from one caused by more enforcement",
  ev2who="a comparison with institutional accounts",
  ev2where="two monastic houses in the same towns",
  ev2what="the prices those houses actually paid diverge from the assize price by margins that widen in years of poor harvest",
  ev2detail="the houses bought in bulk and recorded what they paid, so their accounts are evidence of transactions rather than of regulation",
  revision="the assize describes what authorities attempted rather than what buyers paid, and the divergence between the two is itself the more informative series",
  caveat="Both monastic houses bought at a scale no household could match, and their prices need not resemble those paid in the market by the week.",
  cond1=("every town in Duarte's comparison kept borough court rolls for the whole period she studied",
         "Hedingham's rolls break off in 1348, midway through the period Duarte studied",
         "Hedingham is not among the towns in Duarte's comparison",
         "Hedingham",
         "",
         ("Hedingham's bakers were not prosecuted after 1348",
          "Hedingham's bakers generally obeyed the assize")),
  cond2=("every price used from the institutional accounts records an actual purchase",
         "the 1361 figure is an estimate entered by the cellarer",
         "the 1361 figure is not among the prices used from the institutional accounts",
         "the 1361 figure",
         "",
         ("the 1361 figure does not differ from the assize price for that year",
          "the 1361 figure records what a household paid for bread")),
  about="distinguishing a record of what was ordered from a record of what was paid, and showing that the gap between them carries the information",
  implies="the transaction evidence comes from buyers whose scale was unlike that of ordinary purchasers"),
 dict( key="wayfinding",
  topic="animal navigation",
  old="It was long held that migratory songbirds navigate principally by a magnetic compass, an account that grew out of orientation cage experiments in which birds deprived of any view of the sky still oriented in their seasonally appropriate direction and reversed when the surrounding field was reversed.",
  old_why="The cage results were replicated across species and decades, the effect was large, and the discovery of magnetically sensitive proteins in the avian retina supplied a mechanism that made the behavioural finding seem settled.",
  problem="An orientation cage measures which way a bird attempts to go, not whether it can reach anywhere in particular, and a compass alone cannot explain how a displaced bird corrects toward a goal it has never approached from that direction.",
  ev1who="Abad and Tsuruoka",
  ev1where="a displacement experiment on adult and first-year birds of one species",
  ev1what="adults displaced a thousand kilometres corrected toward the original goal while first-year birds continued on the original heading",
  ev1detail="both groups were displaced in the same aircraft on the same day, so the difference cannot be attributed to the conditions of transport",
  ev2who="a tracking study",
  ev2where="the same population over three seasons",
  ev2what="the correction appears only after a bird has completed one full migration, and its accuracy improves with each subsequent one",
  ev2detail="the tags recorded position continuously rather than at capture points, which is what allows a correction to be distinguished from a lucky arrival",
  revision="the compass is one component of a system whose map is learned, and the learning rather than the sensing is what distinguishes an experienced migrant",
  caveat="Both studies concern a single species that migrates along a coastline, where landmarks are unusually continuous.",
  cond1=("every bird in the tracking study that corrected toward the goal had completed at least one full migration",
         "the bird tagged A19, one of those in the tracking study, was on its first migration",
         "A19 did not correct toward the goal on that migration",
         "the bird tagged A19",
         "the tracking study",
         ("A19 did not use a magnetic compass on that migration",
          "A19 continued on its original heading because it had been displaced")),
  cond2=("every position used in the tracking study came from a continuously recording tag",
         "the 2021 positions were taken at capture points only",
         "the 2021 positions are not among those used in the tracking study",
         "the 2021 positions",
         "",
         ("the 2021 positions do not show any bird correcting toward the goal",
          "the 2021 positions show birds arriving at the goal by chance")),
  about="separating a sensory mechanism from the learned knowledge that makes it useful, and locating the difference between novice and experienced migrants in the latter",
  implies="the finding rests on a species whose route offers landmarks that most migratory routes do not"),
 dict( key="perspective",
  topic="linear perspective in painting",
  old="Art historians long explained the appearance of linear perspective in fifteenth-century Florence as the consequence of a mathematical discovery, treating Brunelleschi's demonstration and Alberti's treatise as the moment a technique became available and was thereafter adopted because it was correct.",
  old_why="The chronology appears to support it: the demonstration precedes the treatise, the treatise precedes the wide adoption, and painters who worked after it produced constructions that are geometrically consistent in a way that earlier work is not.",
  problem="The account explains adoption by correctness, which cannot distinguish a technique taken up because it solved a problem painters had from one taken up because patrons began to ask for it, and the workshop records that might settle the question were not consulted.",
  ev1who="Mancuso",
  ev1where="the surviving contracts of eleven Florentine workshops",
  ev1what="clauses specifying the depicted setting and the viewer's position enter the contracts before the constructions appear in the paintings, not after",
  ev1detail="she dated the contracts by the notarial registers rather than by the paintings they commissioned, which keeps the two chronologies independent",
  ev2who="a technical examination",
  ev2where="underdrawings in nine panels from those workshops",
  ev2what="the earliest geometrically consistent constructions were laid out over drawings that had already fixed the architecture, so the geometry was fitted to a scheme rather than generating it",
  ev2detail="the underdrawings were recorded by infrared reflectography, which shows the sequence of layers and not merely their presence",
  revision="the technique spread because patrons specified the effect it produced, and the geometry was recruited to deliver a result that had already been asked for",
  caveat="The eleven workshops are all Florentine, and the contract practice of other centres in the same decades is not documented to the same standard.",
  cond1=("every contract Mancuso dated was entered in a surviving notarial register",
         "the Strozzi commission is known only from a later inventory",
         "the Strozzi commission is not among the contracts Mancuso dated",
         "the Strozzi commission",
         "",
         ("the Strozzi commission did not specify the viewer's position",
          "the Strozzi commission was painted before Alberti's treatise")),
  cond2=("every panel in the technical examination was recorded by infrared reflectography",
         "the Arezzo panel was examined by raking light alone",
         "the Arezzo panel is not in the technical examination",
         "the Arezzo panel",
         "",
         ("the Arezzo panel has no underdrawing beneath its architecture",
          "the Arezzo panel's geometry was laid out before its architecture was drawn")),
  about="reversing the assumed order between a technique and the demand for what it produces, using records that fix the two chronologies independently",
  implies="the conclusion describes the practice of one city and is not established for the others"),
 dict( key="antibiotic",
  topic="resistance in soil bacteria",
  old="Resistance to antibiotics was for decades understood as a consequence of clinical use, on the view that exposure in hospitals and on farms selects for resistant strains and that the genes conferring resistance are therefore recent in origin.",
  old_why="The timing fits: resistance to each compound was detected in clinical isolates within a few years of its introduction, and the genes could be traced spreading between species on plasmids in exactly the settings where the drugs were used most heavily.",
  problem="Detection in the clinic records where resistance was looked for, and the reasoning moves from the place a gene was first noticed to the place it arose, which is a step the evidence does not support.",
  ev1who="Iwasaki and Boateng",
  ev1where="permafrost cores from two Arctic sites",
  ev1what="genes conferring resistance to three modern compounds are present in sediment sealed for thirty thousand years",
  ev1detail="they authenticated the sequences by the damage patterns characteristic of ancient DNA, which distinguishes genuinely old material from modern contamination",
  ev2who="a survey of soil isolates",
  ev2where="four sites with no recorded agricultural or clinical exposure",
  ev2what="resistance is common and its genetic architecture is more varied than anything found in clinical isolates",
  ev2detail="the sites were chosen from land-use records compiled for other purposes, so the selection cannot have been made to favour the result",
  revision="resistance genes are ancient features of soil communities, and clinical use selects and concentrates them rather than creating them",
  caveat="That a gene is ancient in soil says nothing about how it reached the clinical strains that now carry it, which remains unexplained for most compounds.",
  cond1=("every sequence Iwasaki and Boateng report showed the damage patterns characteristic of ancient DNA",
         "the Yukon sequence showed none of the damage patterns characteristic of ancient DNA",
         "the Yukon sequence is not among those Iwasaki and Boateng report",
         "the Yukon sequence",
         "",
         ("the Yukon sequence does not confer resistance to any modern compound",
          "the Yukon sequence arose through clinical use of the drug it resists")),
  cond2=("every site in the soil survey was selected from land-use records compiled for other purposes",
         "the Cairngorm site was chosen because of a preliminary result there, not from any land-use record",
         "the Cairngorm site is not in the soil survey",
         "the Cairngorm site",
         "",
         ("the Cairngorm site has no resistant bacteria in its soil",
          "the Cairngorm site has a history of agricultural exposure")),
  about="relocating the origin of a trait from the setting where it was first observed to one where nobody had looked",
  implies="the revised account leaves the route between the ancient reservoir and present clinical strains undescribed"),
 dict( key="enclosure",
  topic="common field agriculture",
  old="The open field system of medieval and early modern England was long described as inefficient, on the grounds that scattered strips wasted labour in movement, that common grazing invited overstocking, and that collective decisions about rotation prevented any individual from improving.",
  old_why="The description follows from the standard model of common property, it was endorsed by the eighteenth-century improvers whose writings supply much of the surviving commentary, and the yields recorded after enclosure are generally higher than those recorded before it.",
  problem="The improvers were arguing for enclosure and their accounts are advocacy, and the yield comparison sets post-enclosure records against pre-enclosure records collected by different means for different purposes.",
  ev1who="Okoro",
  ev1where="manorial accounts from twenty-two villages, matched before and after enclosure",
  ev1what="where the same measurement method spans the change, the yield gain is a third of what the standard comparison reports",
  ev1detail="she restricted the comparison to villages where the same steward kept accounts across the transition, which holds the measurement constant",
  ev2who="a study of strip allocation",
  ev2where="eight of those villages",
  ev2what="the scattering of strips distributes each household's holdings across soil types in a pattern that closely tracks local variation in drainage",
  ev2detail="the soil mapping was done independently of the strip records and the two were matched afterwards, so the pattern was not read into the allocation",
  revision="the open field system traded some efficiency for insurance against local failure, and the scattering that looks wasteful is the mechanism by which it did so",
  caveat="The insurance account explains the pattern of holdings and does not establish that the households involved chose it for that reason.",
  cond1=("every village in Okoro's matched comparison had one steward across the transition",
         "Thornbury changed stewards partway through its enclosure",
         "Thornbury is not in Okoro's matched comparison",
         "Thornbury",
         "",
         ("Thornbury's yields did not rise after enclosure",
          "Thornbury's accounts overstate the gain from enclosure")),
  cond2=("every soil map used in the allocation study was produced independently of the strip records",
         "the Wendle map was drawn from the strip records themselves",
         "the Wendle map is not among those used in the allocation study",
         "the Wendle map",
         "",
         ("the Wendle map does not track local variation in drainage",
          "the Wendle map shows strips scattered across soil types")),
  about="reinterpreting an apparently wasteful practice as a response to risk, after correcting a comparison that had been made with mismatched measurements",
  implies="the account explains why the pattern would be advantageous without showing that it was adopted for that advantage"),
 dict( key="phonotactic",
  topic="infant speech perception",
  old="Infants were long held to learn the sound categories of their language by hearing the words of that language, on a model in which repeated exposure to a word establishes the contrasts it depends on.",
  old_why="Infants do discriminate non-native contrasts early and lose that ability across the first year, and the loss is faster for contrasts absent from the words they hear most often, which fits the exposure account closely.",
  problem="The frequency of a contrast in speech and the frequency of the words carrying it are almost perfectly correlated in natural language, so no observational study can separate them.",
  ev1who="Kirchner and Adeyemi",
  ev1where="an experiment using an artificial language",
  ev1what="infants acquired a contrast presented only in nonsense sequences, as reliably as one presented in words with referents",
  ev1detail="the two conditions used the same acoustic contrast and the same total exposure, differing only in whether the sequences were paired with objects",
  ev2who="a follow-up",
  ev2where="the same infants four months later",
  ev2what="the contrast acquired from nonsense sequences persisted and transferred to sequences the infants had not heard",
  ev2detail="the transfer items were constructed after the first session, so they cannot have been present in the original exposure",
  revision="the statistical distribution of sounds is sufficient for category formation, and the words are the usual carrier of that distribution rather than its source",
  caveat="The artificial language used a contrast that does not occur in the infants' ambient language, and whether the same holds for a contrast they hear daily is untested.",
  cond1=("every infant in the experiment who acquired the contrast heard the full exposure schedule",
         "infant 14, one of those in the experiment, missed the third session",
         "infant 14 did not acquire the contrast",
         "infant 14",
         "the experiment",
         ("infant 14 did not return for the follow-up four months later",
          "infant 14 heard the contrast only in words with referents")),
  cond2=("every transfer item was constructed after the first session",
         "the falling-tone item was in the original stimulus set",
         "the falling-tone item is not among the transfer items",
         "the falling-tone item",
         "",
         ("the falling-tone item was not paired with an object in the first session",
          "the falling-tone item carried a contrast the infants hear every day")),
  about="separating two explanations that natural language confounds, by building a language in which they come apart",
  implies="the result is established for a contrast the infants do not otherwise hear and may not extend to one they do"),
 dict( key="juries",
  topic="civil jury awards",
  old="Legal scholars long attributed the size of damages awarded by civil juries to sympathy for injured plaintiffs, arguing that jurors who identify with a person harmed by a corporation will award more than the harm can justify, and that the variability of awards reflects the variability of that sympathy from one jury to the next.",
  old_why="Awards against corporate defendants are on average larger than awards against individuals for injuries described in similar terms, and interviews with jurors after trial frequently record expressions of anger toward the defendant, so the pattern of verdicts and the jurors' own accounts seemed to point to the same cause.",
  problem="The comparison between corporate and individual defendants does not hold the evidence constant, since cases against corporations more often involve documented injuries and expert testimony, and interviews conducted after a verdict record how jurors explain a decision already made rather than what produced it.",
  ev1who="Castellanos and Whitfield",
  ev1where="mock juries shown identical trial recordings in which only the identity of the defendant was varied",
  ev1what="awards against the corporate defendant were no larger than those against the individual, but the spread of awards was wide under both conditions and narrowed sharply when jurors were given a figure from which to begin",
  ev1detail="the jurors were drawn from the same county jury pools as real trials and deliberated for as long as they chose, which keeps the setting close to the one whose verdicts it is meant to explain",
  ev2who="an analysis",
  ev2where="actual verdicts in seven states that differ in whether attorneys may suggest a figure to the jury",
  ev2what="awards were least variable where attorneys may suggest a figure and most variable where they may not, while the gap between corporate and individual defendants disappeared once the severity of the injury was taken into account",
  ev2detail="the severity of each injury was coded by physicians who did not know the amount awarded, so the measure of harm cannot have been shaped by the verdict it is compared with",
  revision="the variability of awards comes from the absence of any anchor for translating harm into money rather than from sympathy, and the apparent penalty on corporations reflects the severity of the cases brought against them",
  caveat="Both studies concern awards for injuries that can be described medically, and awards for harms such as damage to reputation, where no comparable measure of severity exists, were not examined.",
  cond1=("every case in the analysis of actual verdicts that produced an award above a million dollars involved an injury coded as severe",
         "the Harlan case, one of those in the analysis of actual verdicts, involved an injury coded as minor",
         "the Harlan case did not produce an award above a million dollars",
         "the Harlan case",
         "the analysis of actual verdicts",
         ("the Harlan case did not involve a corporate defendant",
          "the Harlan case was tried in a state that forbids attorneys to suggest a figure")),
  cond2=("every juror in the mock trials was drawn from a county jury pool",
         "the volunteers recruited through a university were not drawn from any jury pool",
         "the volunteers recruited through a university are not among the jurors in the mock trials",
         "the volunteers recruited through a university",
         "",
         ("the volunteers recruited through a university did not deliberate before giving an award",
          "the volunteers recruited through a university awarded more against the corporation")),
  about="replacing an explanation that located the cause of a pattern in jurors' feelings with one that locates it in the information jurors are given",
  implies="the account has not been tested on harms that cannot be graded by a medical measure"),
 dict( key="smoke",
  topic="fire and seed germination",
  old="Plant ecologists long regarded fire as a purely destructive event for the seeds lying in the soil of shrublands, assuming that the heat of a burn kills most of the seed bank and that the flush of seedlings seen after a fire comes from the few seeds buried deep enough to survive it, together with seed blown in from unburned ground.",
  old_why="Soil heated in the laboratory to the temperatures recorded at the surface during a burn yields far fewer seedlings than unheated soil, and the seedlings that appear after a fire are often densest near its unburned margins, which is where wind-blown seed would be expected to land first.",
  problem="Heating soil in an oven reproduces the temperature of a fire and nothing else about it, and the account cannot explain why several species whose seed survives heating perfectly well almost never germinate in unburned ground.",
  ev1who="Okafor and Lindqvist",
  ev1where="seed of eleven shrubland species exposed either to heat alone or to heat followed by smoke drawn through water",
  ev1what="seven of the species germinated in large numbers only after exposure to smoke, and heat alone produced no more seedlings than untreated seed",
  ev1detail="each species was tested with seed collected in a single season and stored under the same conditions, so differences in the age or handling of the seed cannot explain the result",
  ev2who="a field study",
  ev2where="plots burned in a controlled fire and paired plots left unburned but sprayed with smoke water",
  ev2what="the sprayed plots produced seedlings of those seven species in numbers close to those on the burned plots",
  ev2detail="the soil in both kinds of plot had been fenced and netted against incoming seed, which rules out seed blown in from elsewhere as the source of the seedlings",
  revision="for many shrubland species fire acts as a signal, carried in smoke, that releases dormant seed, and the destruction caused by heat is only part of its effect",
  caveat="The eleven species were chosen because they are common after fires, and shrubland species that are rare after fire were not tested.",
  cond1=("every sample in Okafor and Lindqvist's tests that produced a large number of seedlings had been exposed to smoke",
         "sample 31, one of those in Okafor and Lindqvist's tests, was exposed to heat alone",
         "sample 31 did not produce a large number of seedlings",
         "sample 31",
         "Okafor and Lindqvist's tests",
         ("sample 31 did not survive the heat treatment",
          "sample 31 came from one of the seven species that respond to smoke")),
  cond2=("every plot in the field study was fenced and netted against incoming seed",
         "the Rosehill plot was left open to seed carried by the wind",
         "the Rosehill plot is not among those in the field study",
         "the Rosehill plot",
         "",
         ("the Rosehill plot produced no seedlings of the seven species",
          "the Rosehill plot was burned in a controlled fire")),
  about="showing that an event understood as destructive also acts as a trigger, once it is reproduced in more than one of its aspects",
  implies="the response to smoke has been shown in species already known to flourish after fire and may be less common among the rest"),
 dict( key="ballads",
  topic="oral transmission of ballads",
  old="Folklorists long treated the variation among recorded versions of a traditional ballad as the product of faulty memory, on the view that each singer learned a fixed text from an older singer and that the differences between versions accumulate as small errors do when a message is passed along a chain.",
  old_why="Versions collected from singers who learned from one another differ more the more links separate them, and the commonest differences, dropped stanzas and substituted words, are the kinds of change that forgetting produces.",
  problem="The chain model predicts that variation should be random with respect to meaning, and it cannot explain why singers in the same district so often changed the same stanza in the same direction.",
  ev1who="Carrick",
  ev1where="field recordings of a single ballad made in one valley over forty years",
  ev1what="the changes fall entirely in the stanzas that name a place or a family, which singers altered to fit their own locality, while the stanzas carrying the story were reproduced unchanged",
  ev1detail="each recording is accompanied by the singer's own account of where the song was learned, so the line of transmission can be traced for every version",
  ev2who="a study of broadside printings",
  ev2where="the same ballad sold in towns around the valley",
  ev2what="the printed texts reproduce several of the local changes within a few years of their first appearance in the recordings, which is not how accidental errors spread",
  ev2detail="each printing carries the printer's name and address, which dates it from trade directories independently of the recordings",
  revision="much of the variation is deliberate adaptation to a local audience, and memory accounts for less of it than the chain model supposed",
  caveat="The valley had an unusually active trade in printed ballads, and in districts without printers the local changes might have spread in some other way or not at all.",
  cond1=("every stanza in Carrick's recordings that changed from one version to the next named a place or a family",
         "the parting stanza, one of those in Carrick's recordings, names neither a place nor a family",
         "the parting stanza did not change from one version to the next",
         "the parting stanza",
         "Carrick's recordings",
         ("the parting stanza was not printed in any broadside",
          "the parting stanza was dropped by singers who had forgotten it")),
  cond2=("every printing in the broadside study carries a printer's name and address",
         "the Tollbridge sheet carries no printer's name",
         "the Tollbridge sheet is not among the printings in the broadside study",
         "the Tollbridge sheet",
         "",
         ("the Tollbridge sheet does not reproduce any of the local changes",
          "the Tollbridge sheet was printed before the local changes appeared in the recordings")),
  about="reinterpreting variation in an oral tradition as adaptation rather than decay, by tracing where the changes occur and how they spread",
  implies="the link between local change and print may depend on a trade that most districts lacked"),
 dict( key="dialect",
  topic="dialect decline",
  old="Sociolinguists long attributed the decline of rural dialects to broadcasting, reasoning that once radio and television carried a standard form of the language into every home, children would model their speech on it rather than on the speech of their parents and neighbours.",
  old_why="The steepest declines in dialect use were recorded in the decades when broadcasting reached rural districts, and speakers themselves often named the radio as the source of the standard forms they had adopted.",
  problem="Broadcasting arrived in rural districts at the same time as the roads, schools and factory jobs that brought their inhabitants into daily contact with speakers from elsewhere, and a speaker's account of where a form came from is a belief about influence rather than a measure of it.",
  ev1who="Ferrand and Oduya",
  ev1where="two villages that received broadcasting in the same year but were joined to the regional road network twenty years apart",
  ev1what="the dialect forms declined in each village only after its road opened, and the village that waited for its road kept them for two decades while hearing the same broadcasts",
  ev1detail="both series come from recordings made by the same regional survey at the same intervals, so the two villages were measured by the same method",
  ev2who="a study of individual speakers",
  ev2where="a third village over the years in which its factory opened",
  ev2what="the speakers who abandoned dialect forms first were those who took factory jobs alongside workers from other districts, not those whose households owned radios",
  ev2detail="radio ownership was taken from the licence registers rather than from what speakers remembered",
  revision="dialects declined through daily contact with speakers of other varieties, and broadcasting, which offered a standard form without any need to speak it, did little on its own",
  caveat="All three villages lay within a day's travel of a single industrial town, and districts drawn into contact by other means, such as military service, were not studied.",
  cond1=("every speaker in the study of individual speakers who abandoned dialect forms in the first decade after the factory opened had taken a factory job",
         "the speaker recorded as F7, one of those in the study of individual speakers, never worked at the factory",
         "the speaker recorded as F7 did not abandon dialect forms in the first decade after the factory opened",
         "the speaker recorded as F7",
         "the study of individual speakers",
         ("the speaker recorded as F7 did not own a radio in the first decade after the factory opened",
          "the speaker recorded as F7 learned the standard forms from broadcasts")),
  cond2=("every household the study of individual speakers counted as owning a radio appears in the licence registers",
         "the Marston household kept a receiver without ever taking out a licence",
         "the Marston household is not among those the study of individual speakers counted as owning a radio",
         "the Marston household",
         "",
         ("the Marston household did not listen to broadcasts",
          "the Marston household abandoned dialect forms before its neighbours")),
  about="separating two changes that arrived together in order to show which of them altered how people speak",
  implies="the role of contact has been established for one kind of contact and may work differently for others"),
 dict( key="ferries",
  topic="island depopulation",
  old="Planners in the northern archipelago long treated the loss of population from its smaller islands as a consequence of the collapse of inshore fishing, which had employed most of the islands' working men until the 1970s and whose decline coincided with the first large departures.",
  old_why="The census showed that the islands most dependent on fishing lost their people fastest, and the people who left most often named the end of fishing work as their reason for going when they were asked.",
  problem="The account could not explain why two islands with almost identical fishing histories, Vell and Oster, diverged so sharply, Vell keeping most of its people while Oster lost two thirds of them in a single generation.",
  ev1who="Brandvik",
  ev1where="the ferry timetables and school registers of twenty islands over forty years",
  ev1what="islands whose ferries allowed a return to the mainland within a single school day kept their families with children, while islands whose ferries were cut to alternate days lost them within a decade of the cut",
  ev1detail="the timetables were set by the ferry company to spread its fleet across the whole archipelago rather than in response to any island's population, so the cause cannot run from the departures to the timetable",
  ev2who="a later study",
  ev2where="the household registers of Oster and Vell",
  ev2what="the families that left Oster did so in the two years after its ferry was cut to alternate days, whatever their connection to fishing, while fishing families on Vell, whose daily ferry was never cut, mostly stayed",
  ev2detail="the registers record every move with a date and an occupation, so each departure can be matched to the timetable month by month",
  revision="the population of the smaller islands followed the ferry timetable more closely than the fortunes of fishing, and the end of fishing drove people away mainly where the daily ferry had already gone",
  caveat="All twenty islands lie within two hours of the mainland by sea, and the pattern has not been examined on the outer islands, where no timetable allows a return within the day.",
  cond1=("every island in Brandvik's study had a school of its own",
         "the island of Holm has never had a school of its own",
         "the island of Holm is not in Brandvik's study",
         "the island of Holm",
         "",
         ("the island of Holm never had a daily ferry service",
          "the island of Holm lost no families with children after its ferry was cut")),
  cond2=("every family in the later study that left Oster after the cut had children of school age",
         "the Lund family, one of those in the later study, had no children of school age",
         "the Lund family did not leave Oster after the cut",
         "the Lund family",
         "the later study",
         ("the Lund family never depended on fishing work",
          "the Lund family did not use the ferry at all")),
  about="arguing that a loss of population credited to the collapse of an industry followed the loss of daily transport instead",
  implies="the ferry explanation may not hold for islands too far out for a return within the day"),
 dict( key="bridgepiers",
  topic="bridge pier failures",
  old="Engineers responsible for the county's stone bridges long attributed the collapse of their piers to the weight of modern traffic, which by the 1960s had grown to many times the loads the bridges were built to carry, and they strengthened decks and restricted heavy vehicles accordingly.",
  old_why="The bridges that failed stood mostly on the busiest roads, and the failures clustered in the decades when the number of lorries on those roads grew fastest.",
  problem="Strengthening the decks did not stop the failures, and several bridges on lightly used lanes lost piers in the same years while carrying almost no heavy traffic at all.",
  ev1who="Ostrowski",
  ev1where="the surveys of the river bed taken beneath thirty bridges since the 1920s",
  ev1what="every pier that failed, whatever the traffic above it, stood on a bed that had been lowered by at least a metre since the river upstream was straightened",
  ev1detail="the rivers were straightened for drainage in the 1930s, well before the traffic grew, so the lowering of the beds cannot be mistaken for an effect of traffic",
  ev2who="a later study",
  ev2where="sixty piers that the county's inspectors either fitted with concrete aprons or left unprotected",
  ev2what="not one pier fitted with an apron failed in the following forty years, while unprotected piers carrying the same traffic went on failing",
  ev2detail="the aprons were fitted in the order the inspectors reached the piers on their route rather than by the condition of each pier, so the protected piers were not simply the sound ones",
  revision="the piers failed because the straightened rivers scoured the beds beneath them rather than because of the growth in traffic",
  caveat="All thirty bridges cross rivers that were straightened, and no one has examined whether heavy traffic weakens piers that stand on stable beds.",
  cond1=("every bridge in Ostrowski's study had its river bed measured before 1930",
         "the bed beneath the Mell bridge was first measured in 1971",
         "the Mell bridge is not in Ostrowski's study",
         "the Mell bridge",
         "",
         ("the Mell bridge has never lost a pier",
          "the Mell bridge stands on a bed that was never lowered")),
  cond2=("every pier in the later study that was fitted with an apron was reached by the inspectors before 1975",
         "the east pier of the Ardle bridge, one of those in the later study, was first reached by the inspectors in 1981",
         "the east pier of the Ardle bridge was not fitted with an apron",
         "the east pier of the Ardle bridge",
         "the later study",
         ("the east pier of the Ardle bridge did not stand on a lowered bed",
          "the east pier of the Ardle bridge carried no heavy traffic after 1981")),
  about="attributing the failure of bridge piers to the straightening of the rivers beneath them rather than to the growth in traffic",
  implies="traffic may still play a part in the failure of piers whose river beds have not been lowered"),
 dict( key="loanwords",
  topic="borrowed vocabulary",
  old="Historians of the Vesk dialects long held that the Taran words in their vocabulary arrived through trade, carried by merchants who needed a shared stock of terms for goods, weights and prices at the coastal fairs where the two languages met.",
  old_why="The borrowed words cluster in the vocabulary of commerce, and the earliest written examples come from the account books of the fair towns, where they appear a generation before they are found anywhere inland.",
  problem="The account could not explain why so many of the borrowed words name ordinary household things, such as kin, cooking and the parts of a house, that no merchant would have needed a word for at a fair.",
  ev1who="Oduya",
  ev1where="the marriage registers of forty parishes along the old frontier",
  ev1what="the parishes where Taran and Vesk families intermarried most often took up the household words two generations ahead of the fair towns",
  ev1detail="the registers name the parish each spouse came from, so a mixed marriage can be identified without relying on surnames, which families often changed",
  ev2who="a later study",
  ev2where="the letters written by the children of mixed marriages",
  ev2what="the household words appeared first in letters from children raised in homes where both languages were spoken, and only years later in letters from their neighbours",
  ev2detail="the letters are dated and signed, so each use can be placed within a family and within a decade",
  revision="the household vocabulary spread through mixed families rather than through the fairs, and trade accounts for the commercial words alone",
  caveat="The registers survive only for the frontier parishes, where mixed marriages were far more common than in the interior.",
  cond1=("every parish in Oduya's study kept its marriage registers without a break from 1700",
         "the registers of the parish of Harrowby are missing for the years 1741 to 1760",
         "the parish of Harrowby is not among those in Oduya's study",
         "the parish of Harrowby",
         "",
         ("the parish of Harrowby saw no marriages between Taran and Vesk families",
          "the parish of Harrowby never took up the household words")),
  cond2=("every set of letters in the later study that used a household word before 1790 was written by a child of a mixed marriage",
         "the Pell letters, a set in the later study, were written by children of two Vesk parents",
         "the Pell letters did not use a household word before 1790",
         "the Pell letters",
         "the later study",
         ("the Pell letters did not use any Taran word at all",
          "the Pell letters were not written before 1790")),
  about="tracing borrowed words to the families that spoke both languages rather than to the fairs credited with carrying them",
  implies="the family route may matter less in the interior, where mixed marriages were far rarer"),
 dict( key="glassworks",
  topic="pressed glass manufacture",
  old="Historians of the Merrow valley glass industry long credited its move from blown to pressed glass to a single engineer, Tomas Arle, whose patented press appeared in the valley the year before the first pressed tumblers were sold.",
  old_why="The earliest pressed pieces carry marks left by a press of Arle's design, and the firms that bought his press were the first to advertise pressed ware.",
  problem="The account could not explain why firms that never bought the press began selling pressed ware in the same decade, or why several firms that did buy it went on blowing glass for years.",
  ev1who="Castellan",
  ev1where="the wage books of eleven glassworks in the valley",
  ev1what="whether or not a firm owned an Arle press, it began making pressed ware only after hiring mould makers trained at the Lisle foundry",
  ev1detail="the wage books record each worker's trade and the date of hire, so the arrival of the mould makers can be dated independently of the sales records",
  ev2who="a later study",
  ev2where="the moulds recovered from the sites of six glassworks",
  ev2what="the oldest moulds were cut in the Lisle manner and fitted a hand press older than any of Arle's",
  ev2detail="the moulds were dated by the layers in which they were buried, which also held dated coins and bottles",
  revision="pressed glass spread with the mould makers who could cut the moulds rather than with the press credited with it",
  caveat="Wage books survive for only eleven of the valley's thirty works, all of them small firms that could not afford to train mould makers of their own.",
  cond1=("every glassworks in Castellan's study stood within a mile of the river",
         "the Ormond works stood on the ridge four miles from the river",
         "the Ormond works is not in Castellan's study",
         "the Ormond works",
         "",
         ("the Ormond works never employed a mould maker from the Lisle foundry",
          "the Ormond works did not sell pressed ware before 1840")),
  cond2=("every mould in the later study that fitted a hand press was cut in the Lisle manner",
         "mould 31, one of those in the later study, was not cut in the Lisle manner",
         "mould 31 did not fit a hand press",
         "mould 31",
         "the later study",
         ("mould 31 was never used to make pressed ware",
          "mould 31 did not come from the oldest layers")),
  about="crediting a change in manufacture to the craftsmen who carried a skill between firms rather than to the machine it was credited to",
  implies="larger firms that trained their own mould makers may have come to pressing by a different route"),
 dict( key="dyeroot",
  topic="the dye root trade",
  old="Economic historians long attributed the collapse of the Carrow trade in tessel root, a red dye, to the arrival of a cheaper synthetic substitute, which undercut the root on price and was taken up by the large mills within a few years of its first sale.",
  old_why="Exports of the root fell by half in the decade after the substitute appeared, and the mills that bought the substitute had been among the root growers' largest customers.",
  problem="The account could not explain why exports had already begun to fall several years before the substitute was sold, or why growers in the neighbouring province, who faced the same substitute, kept most of their trade.",
  ev1who="Varga",
  ev1where="the customs ledgers of the three ports that shipped the root",
  ev1what="exports fell first and furthest from the port where a new duty on dried root was imposed, and least from the one port exempt from the duty",
  ev1detail="the duty was set by a treasury seeking revenue for a war, and its rate did not change with the price of the root or of the substitute",
  ev2who="a later study",
  ev2where="the account books of twenty growers on either side of the provincial border",
  ev2what="growers who paid the duty cut their plantings within two seasons of its introduction, while growers across the border, who did not pay it, kept planting until the substitute was cheaper than the root",
  ev2detail="the account books record the acreage planted each season, so each cut can be dated to the season in which it was made",
  revision="the trade was lost to the duty before it was lost to the substitute, which completed a decline that the tax had begun",
  caveat="Customs ledgers record only the root that was shipped abroad, and none of the root sold to mills within the province.",
  cond1=("every port in Varga's study kept its ledgers in the treasury's standard form",
         "the ledgers of the port of Selk were kept in a merchant's private form",
         "the port of Selk is not among those in Varga's study",
         "the port of Selk",
         "",
         ("the port of Selk never shipped tessel root",
          "the port of Selk was not subject to the duty")),
  cond2=("every grower in the later study who cut plantings before the substitute was sold had paid the duty",
         "the Ambry farm, one of the growers in the later study, never paid the duty",
         "the Ambry farm did not cut its plantings before the substitute was sold",
         "the Ambry farm",
         "the later study",
         ("the Ambry farm did not grow tessel root after the substitute was sold",
          "the Ambry farm never sold root to the large mills")),
  about="arguing that a trade credited to a new product's competition had already been weakened by a tax before the product arrived",
  implies="the part of the trade that supplied mills within the province is not measured by the evidence"),
 dict( key="gales",
  topic="coastal storm records",
  old="Climate historians long read the rising count of shipwrecks on the Harlan coast in the nineteenth century as evidence that the coast's winter gales had grown more frequent and more violent over those decades.",
  old_why="The wreck registers show three times as many losses in the 1880s as in the 1820s, and the survivors' accounts in those registers blame gales for most of them.",
  problem="The account could not explain why the number of wrecks rose fastest in the years when new ports opened on the coast and the number of vessels passing it rose with them.",
  ev1who="Lindqvist",
  ev1where="the daily logs of nine lighthouses kept from 1820 to 1890",
  ev1what="the number of days with a full gale changed little over the seventy years, while the number of wrecks for each gale rose with the traffic passing each light",
  ev1detail="the keepers recorded the wind on the same scale throughout, and they kept their logs whether or not any ship was in sight",
  ev2who="a later study",
  ev2where="the insurance claims for vessels lost on the coast",
  ev2what="the vessels lost in the later decades were mostly small coasting craft that had begun working the new ports, not the larger ships that had always used the coast",
  ev2detail="the claims give each vessel's tonnage and home port, so the losses can be sorted by the trade each vessel served",
  revision="the rise in wrecks followed the growth of traffic along the coast rather than any change in its gales",
  caveat="The lighthouses stand on the southern half of the coast, and the northern half, where the new ports were fewer, has no comparable record.",
  cond1=("every lighthouse in Lindqvist's study kept its log without a gap of more than a week",
         "the log of the Tarn Head light has a gap of three months in 1851",
         "the Tarn Head light is not among those in Lindqvist's study",
         "the Tarn Head light",
         "",
         ("the Tarn Head light recorded no full gales in 1851",
          "the Tarn Head light never saw a vessel wrecked within its range")),
  cond2=("every vessel in the later study that was lost after 1870 was a coasting craft of under two hundred tons",
         "the Maren Holt, one of the vessels in the later study, was a barque of six hundred tons",
         "the Maren Holt was not lost after 1870",
         "the Maren Holt",
         "the later study",
         ("the Maren Holt was never caught in a full gale",
          "the Maren Holt did not work the new ports")),
  about="arguing that a rise in losses read as a change in the weather followed the growth of the traffic exposed to it instead",
  implies="the northern half of the coast, with fewer new ports, may show a different pattern"),
 dict( key="terraces",
  topic="hillside terracing",
  old="Archaeologists working in the Oruna highlands long dated the building of its stone terraces to a single period of rapid population growth, when, they argued, the valley floors could no longer feed the people living on them.",
  old_why="Settlements in the highlands multiplied in the same centuries in which the first terraces appear, and terraced slopes lie closest to the largest of those settlements.",
  problem="The account could not explain why many terraces were built on slopes far from any settlement, or why some of the largest settlements had no terraces near them at all.",
  ev1who="Kowal",
  ev1where="soil cores taken from behind the walls of sixty terraces",
  ev1what="the terraces were built in several separate episodes, each following a run of years in which the valley floors were buried by flood silt",
  ev1detail="the cores were dated by the pollen and charcoal in each layer, which record the same floods found in the sediments of the valley floor",
  ev2who="a later study",
  ev2where="the layout of terraces on either side of the Oruna river",
  ev2what="terraces were built on the bank of the river that flooded more often, whatever the number of people living there",
  ev2detail="the river's course has changed little, so which bank flooded more can be read from the silt on each side",
  revision="the terraces were built to escape floods on the valley floor rather than to feed a growing population",
  caveat="Cores were taken only from terraces that still stand, and terraces that collapsed early may have been built for other reasons.",
  cond1=("every terrace in Kowal's study faces the river",
         "the terrace at Kest faces away from the river, toward the ridge",
         "the terrace at Kest is not in Kowal's study",
         "the terrace at Kest",
         "",
         ("the terrace at Kest was not built after a flood",
          "the terrace at Kest was never farmed")),
  cond2=("every terrace in the later study that was built before 1200 lies on the bank that flooded more often",
         "the Sarn terraces, among those in the later study, lie on the bank that flooded less often",
         "the Sarn terraces were not built before 1200",
         "the Sarn terraces",
         "the later study",
         ("the Sarn terraces were never flooded",
          "the Sarn terraces did not feed a large settlement")),
  about="tracing a building programme credited to population pressure to a response to floods instead",
  implies="terraces that collapsed early may not share the flood pattern, since none of them was sampled"),
 dict( key="beacons",
  topic="hilltop beacons",
  old="Historians of the Tallow uplands long read the chain of stone beacon platforms along its ridges as a military warning system, built so that a fire lit at the coast could carry news of an invasion inland within a few hours.",
  old_why="The platforms stand within sight of one another along the routes an invader from the coast would have taken, and the oldest written mention of them comes from a year of war.",
  problem="The account could not explain why the platforms were rebuilt and repaired most often in decades of peace, or why several stand where no one travelling from the coast would ever have passed.",
  ev1who="Ansel",
  ev1where="the fuel accounts of the parishes that kept the platforms",
  ev1what="the purchases of wood and pitch for the beacons fell in the weeks before the great autumn fairs far more often than in years of war",
  ev1detail="the accounts record the date of each purchase and the parish that paid for it, so the fires can be placed in the calendar without relying on chronicles written long afterwards",
  ev2who="a later study",
  ev2where="the fair charters of the market towns below the ridges",
  ev2what="every town whose charter granted an autumn fair lay within sight of at least one platform, while towns without a fair mostly did not",
  ev2detail="the charters give the date and the place of each fair, so they can be matched against the sight lines of the platforms",
  revision="the beacons served mainly to announce the opening of the autumn fairs, and their use as a warning in war was an occasional addition to that ordinary purpose",
  caveat="The fuel accounts survive only from the later centuries of the beacons' use, and the purpose for which the first platforms were built cannot be read from them.",
  cond1=("every parish in Ansel's study kept its fuel accounts in the parish chest",
         "the fuel accounts of the parish of Wyke were kept by the lord of the manor rather than in the parish chest",
         "the parish of Wyke is not among those in Ansel's study",
         "the parish of Wyke",
         "",
         ("the parish of Wyke never bought fuel for a beacon",
          "the parish of Wyke did not hold an autumn fair")),
  cond2=("every fair in the later study that was held before 1400 was held within a day's walk of a platform",
         "the fair at Hesket, one of those in the later study, was held three days' walk from any platform",
         "the fair at Hesket was not held before 1400",
         "the fair at Hesket",
         "the later study",
         ("the fair at Hesket was never announced by a beacon",
          "the fair at Hesket did not last more than a day")),
  about="arguing that a network credited to defence served mainly a commercial purpose, by matching the dates of its use to the calendar of fairs",
  implies="the first platforms may have been built for a purpose the surviving accounts cannot show"),

 dict( key="silkworms",
  topic="the silk trade",
  old="Economic historians long blamed the collapse of silk rearing in the Varenne hills on a disease of the silkworm that swept the region in the 1850s, killing whole rearing houses within days and ruining the families who depended on them.",
  old_why="Reports of the disease appear in the same years as the collapse, and the rearing houses that reported it were among the first to close.",
  problem="The account could not explain why rearing fell just as far in villages that never reported the disease, or why it failed to recover once a resistant strain of worm was brought in.",
  ev1who="Morel",
  ev1where="the tithe maps of thirty villages drawn before and after the collapse",
  ev1what="whether or not the disease had been reported there, rearing ended first in the villages where the mulberry groves that fed the worms had been cleared for vines",
  ev1detail="the maps mark every mulberry grove and every vineyard, so the loss of groves can be dated from one survey to the next without relying on the growers' own accounts",
  ev2who="a later study",
  ev2where="the leaf markets of the valley towns",
  ev2what="the price of mulberry leaf doubled in the decade before the collapse, while the price of cocoons barely moved",
  ev2detail="the market books record every sale of leaf by weight and price, so a shortage of leaf shows up as a rise in price before any rearing house closed",
  revision="silk rearing failed because the leaf that fed the worms became scarce and dear, and the disease hastened a decline that the loss of the groves had already begun",
  caveat="The tithe maps cover only the villages of the lower valley, where vines grew well, and the upland villages may have lost their groves for other reasons or not at all.",
  cond1=("every village in Morel's study was mapped for the tithe in both surveys",
         "the village of Sorgue was mapped only in the later survey",
         "the village of Sorgue is not among those in Morel's study",
         "the village of Sorgue",
         "",
         ("the village of Sorgue never kept silkworms",
          "the village of Sorgue did not clear its mulberry groves")),
  cond2=("every leaf market in the later study that recorded a doubling of price kept its books by weight",
         "the leaf market at Aurel, one of those in the later study, kept its books by the basket rather than by weight",
         "the leaf market at Aurel did not record a doubling of price",
         "the leaf market at Aurel",
         "the later study",
         ("the leaf market at Aurel never sold mulberry leaf to rearing houses",
          "the leaf market at Aurel did not trade in cocoons")),
  about="tracing the collapse of a rural industry to the loss of the crop it fed on rather than to the disease blamed for it",
  implies="upland villages may have kept their groves, so the leaf explanation may not reach them"),
 dict( key="printers",
  topic="early printing",
  old="Historians of the book long held that the first printing shops in the Lindmark provinces opened in university towns, drawn there by scholars who wanted texts and had the money to pay for them.",
  old_why="The earliest surviving printed books from the provinces are mostly academic texts, and several of the first shops stood within sight of a university.",
  problem="The account could not explain why a number of university towns had no printer for decades, while several small river towns without a university had one within a few years of the first press.",
  ev1who="Brenner",
  ev1where="the guild records of forty towns that gained a printing shop before 1550",
  ev1what="a printing shop opened within five years of a paper mill starting work nearby far more often than within five years of a university's founding",
  ev1detail="the guild records date each printer's admission, and the mills can be dated from the water rights they were granted, so the two sequences are recorded independently",
  ev2who="a later study",
  ev2where="the paper in books printed in the provinces before 1550",
  ev2what="most of the paper carried watermarks of mills within a day's carriage of the shop that used it",
  ev2detail="each mill marked its paper with its own watermark, so a sheet can be traced to the mill that made it",
  revision="printing spread along the supply of paper rather than following the demand of the universities",
  caveat="The books that survive from the period are mostly those that libraries chose to keep, and cheap printing that went unkept may have followed a different pattern.",
  cond1=("every town in Brenner's study admitted its first printer to a guild",
         "the first printer in the town of Harrow Cross worked without ever joining a guild",
         "the town of Harrow Cross is not among those in Brenner's study",
         "the town of Harrow Cross",
         "",
         ("the town of Harrow Cross had no paper mill nearby",
          "the town of Harrow Cross never printed an academic text")),
  cond2=("every book in the later study that was printed on paper from a distant mill was printed after 1500",
         "the Ostrand psalter, one of the books in the later study, was printed in 1487",
         "the Ostrand psalter was not printed on paper from a distant mill",
         "the Ostrand psalter",
         "the later study",
         ("the Ostrand psalter was not printed in a university town",
          "the Ostrand psalter carried no watermark at all")),
  about="arguing that a technology spread along the supply of its raw material rather than toward the customers credited with drawing it",
  implies="the cheap printing that libraries did not keep may not have followed the paper mills"),
 dict( key="watermills",
  topic="the decline of water mills",
  old="Historians of the Carran valley long attributed the closing of its water mills in the nineteenth century to competition from steam mills in the towns, which could grind all year and were not stopped by drought or ice.",
  old_why="The water mills closed in the decades when the steam mills opened, and the millers who sold up often named the town mills as the reason.",
  problem="The account could not explain why mills on some streams closed before any steam mill opened, while mills on the main river kept working long after the steam mills arrived.",
  ev1who="Tavish",
  ev1where="the gauging records of the valley's streams and the mill leases that depended on them",
  ev1what="whatever the distance to the nearest steam mill, mills closed first on the streams whose summer flow had fallen",
  ev1detail="the streams were gauged by the river board for drainage, not for the mills, so the records do not bend toward any account of why the mills closed",
  ev2who="a later study",
  ev2where="the estate papers of the hill farms above the mill streams and the same gauging records",
  ev2what="the summer flow of each stream fell within a few years of the woods above it being cleared for sheep",
  ev2detail="the estate papers date each clearing and the number of sheep put on the cleared ground",
  revision="the water mills failed mainly because clearing the hills took the summer water from their streams, and the steam mills took trade from mills that were already failing",
  caveat="The gauging records begin only in 1840, after some clearings had already been made, and the earliest closures cannot be tested against them.",
  cond1=("every stream in Tavish's study was gauged at least once each summer from 1840",
         "the Lorn burn was gauged only in the years of flood",
         "the Lorn burn is not among the streams in Tavish's study",
         "the Lorn burn",
         "",
         ("the Lorn burn never drove a mill",
          "the Lorn burn did not lose its summer flow")),
  cond2=("every farm in the later study that cleared its woods before 1850 put more than a thousand sheep on the cleared ground",
         "the Dalmore farm, one of those in the later study, never kept more than four hundred sheep",
         "the Dalmore farm did not clear its woods before 1850",
         "the Dalmore farm",
         "the later study",
         ("the Dalmore farm never cleared any woods",
          "the Dalmore farm did not lie above a mill stream")),
  about="arguing that a rural industry credited to competition was undone first by a change in the land that fed it",
  implies="the earliest closures happened before the records begin and cannot be tested against them"),
 dict( key="mussels",
  topic="freshwater mussels",
  old="Ecologists long attributed the disappearance of the pearl mussel from the rivers of the Brede basin to pollution from the tanneries and dye works that lined its banks through the last century.",
  old_why="The mussel vanished first from the stretches below the largest works, and water drawn near the works carried the dyes and salts most harmful to shellfish.",
  problem="The account could not explain why the mussel failed to return once the works closed and the water was clean again, or why old mussels survived for decades in stretches where no young ones appeared.",
  ev1who="Ferro",
  ev1where="shell growth rings of mussels collected at sixty sites along the basin",
  ev1what="whether or not the water there was polluted, young mussels stopped settling at each site within a few years of a weir being built downstream",
  ev1detail="the rings give the year each mussel settled, so the last year of successful settling can be read at every site",
  ev2who="a later study",
  ev2where="the fish counts taken at the weirs",
  ev2what="the migrating trout on which the mussel's larvae depend stopped passing each weir in the year it was built",
  ev2detail="the counts were made by the fishery board at every weir, so the year each run of trout ended is recorded at the weir that ended it",
  revision="the mussel failed to breed because the weirs cut it off from the fish its young must ride, and the pollution killed adults in stretches where breeding had already stopped",
  caveat="All sixty sites lie on the main river and its larger tributaries, and small streams without weirs were not sampled.",
  cond1=("every site in Ferro's study held living mussels when it was first sampled",
         "the site at Kell Pool held only empty shells when it was first sampled",
         "the site at Kell Pool is not among those in Ferro's study",
         "the site at Kell Pool",
         "",
         ("the site at Kell Pool lay below no weir",
          "the site at Kell Pool was never polluted")),
  cond2=("every weir in the later study built before 1900 was built of stone",
         "the weir at Arden Mill, one of those in the later study, was built of timber",
         "the weir at Arden Mill was not built before 1900",
         "the weir at Arden Mill",
         "the later study",
         ("the weir at Arden Mill did not stop the run of trout",
          "the weir at Arden Mill was not counted by the fishery board")),
  about="arguing that a species credited as a casualty of pollution was lost mainly through a barrier to the host it depends on",
  implies="the weir explanation has not been tested on small streams without weirs"),
 dict( key="moths",
  topic="a downland moth",
  old="Naturalists long attributed the decline of the pale clouded moth across the Wendle downs to the spread of street lighting in the villages, which draws the moths away from their feeding grounds and leaves them exposed to bats.",
  old_why="The moth grew scarce first around the villages that were lit earliest, and light traps set beside the lamps caught fewer of them year by year.",
  problem="The account could not explain why the moth vanished from open downland far from any lamp, while it held on in several lit village gardens.",
  ev1who="Ashdown",
  ev1where="the county's hay-cutting records and the moth counts kept by the downland wardens",
  ev1what="whatever the distance to the nearest lamp, the moth disappeared from each down within a few years of its hay being cut in June rather than August",
  ev1detail="the wardens counted the moth at the same fixed points every summer, so each disappearance is dated by the first year it went unrecorded at a point",
  ev2who="a later study",
  ev2where="the seed heads of the downland scabious and the caterpillars that feed on them",
  ev2what="the caterpillars feed only on scabious seed heads, which a June cut removes before the caterpillars have finished growing",
  ev2detail="the study reared caterpillars from eggs on seed heads cut at each date, so the effect of the cut was measured rather than inferred",
  revision="the moth declined mainly because an earlier hay cut took the seed heads its caterpillars need, and the lamps drew off moths on downs where the caterpillars were already failing",
  caveat="The hay-cutting records cover only the downs the county owns, and privately farmed downs were not included.",
  cond1=("every down in Ashdown's study had been cut for hay in every year since 1950",
         "the down at Sallow Hill had been left uncut for hay since 1962",
         "the down at Sallow Hill is not among those in Ashdown's study",
         "the down at Sallow Hill",
         "",
         ("the down at Sallow Hill never held the moth",
          "the down at Sallow Hill was not lit by any lamp")),
  cond2=("every caterpillar in the later study that completed its growth fed on seed heads left standing into July",
         "the caterpillar from Brook Down, one of those in the later study, fed only on seed heads cut in June",
         "the caterpillar from Brook Down did not complete its growth",
         "the caterpillar from Brook Down",
         "the later study",
         ("the caterpillar from Brook Down was not reared from an egg",
          "the caterpillar from Brook Down came from a lit down")),
  about="arguing that an insect's decline blamed on artificial light was driven mainly by a change in how its food plant was cut",
  implies="the hay-cut explanation has not been tested on privately farmed downs"),
 dict( key="tidetables",
  topic="a port's tide predictions",
  old="Engineers at the port of Haverock long blamed the growing error in its tide predictions on the old tide gauge at the harbour mouth, which they believed had been sinking with the quay it stood on.",
  old_why="The error grew year by year in the way a slowly sinking gauge would produce, and a survey had found the quay settling at one of its corners.",
  problem="The account could not explain why a new gauge set on bedrock showed the same error, or why the error was largest at spring tides and almost absent at neaps.",
  ev1who="Morrow",
  ev1where="the dredging logs of the harbour and the predicted and observed times of high water",
  ev1what="each time the approach channel was deepened, the gap between predicted and observed high water widened, and it widened most at spring tides",
  ev1detail="the logs give the date and depth of every dredge, so each change in the error can be matched to a change in the channel",
  ev2who="a model study",
  ev2where="the harbour basin built at one hundredth of its size",
  ev2what="a deeper channel lets the tide fill the basin faster, so high water arrives earlier and stands higher than the predictions allow",
  ev2detail="the model was run with the channel at each depth recorded in the logs, so the effect of each dredge was measured on its own",
  revision="the predictions failed mainly because dredging changed how the tide filled the basin, and the settling of the quay added only a small part of the error",
  caveat="The model reproduces the basin as it was surveyed in 1970, and changes made to the quays since then were not built into it.",
  cond1=("every high water in Morrow's comparison was recorded by the gauge at the harbour mouth",
         "the high water of 3 March 1968 was recorded only at the inner basin",
         "the high water of 3 March 1968 is not among those in Morrow's comparison",
         "the high water of 3 March 1968",
         "",
         ("the high water of 3 March 1968 was not a spring tide",
          "the high water of 3 March 1968 arrived early")),
  cond2=("every run in the model study that raised high water by more than a centimetre had the channel deeper than eight metres",
         "the run for 1962, one of those in the model study, had the channel at seven metres",
         "the run for 1962 did not raise high water by more than a centimetre",
         "the run for 1962",
         "the model study",
         ("the run for 1962 did not change the time of high water",
          "the run for 1962 was not taken from the dredging logs")),
  about="arguing that an error blamed on a faulty instrument came mainly from a change in the harbour it was measuring",
  implies="the dredging explanation has not been tested against changes made to the quays since 1970"),
 dict( key="drovefairs",
  topic="upland cattle fairs",
  old="Economic historians long credited the railways with ending the great cattle fairs of the Aldon uplands, since cattle sent by rail could reach the southern markets without being sold at a fair on the way.",
  old_why="The largest fairs shrank in the years the lines reached the uplands, and dealers who had bought at the fairs began to buy at the railheads.",
  problem="The account could not explain why several fairs far from any line closed in the same years, while two fairs beside the new stations kept trading for decades.",
  ev1who="Cadell",
  ev1where="the tolls paid at the fair grounds and the licences issued for moving cattle on the drove roads",
  ev1what="whether or not a railway was near, each fair shrank in the year the drove roads that fed it were closed to cattle under the disease orders",
  ev1detail="the licences were issued road by road, so the year each road closed to cattle is known for every fair",
  ev2who="a later study",
  ev2where="the court records of the disease orders and the drovers' own account books",
  ev2what="the orders closed the drove roads first where cattle plague had been reported, and the drovers moved their herds to the few roads left open",
  ev2detail="the account books record the route of every drove, so the move from one road to another is dated by the herds themselves",
  revision="the fairs declined mainly because the disease orders closed the roads that brought cattle to them, and the railways took trade from fairs that had already lost their roads",
  caveat="The drovers' account books survive for only four of the eleven fairs, and the other seven are dated from the tolls alone.",
  cond1=("every fair in Cadell's study charged tolls at the gate of its ground",
         "the fair at Rennet Bridge was held on common land where no toll was charged",
         "the fair at Rennet Bridge is not among those in Cadell's study",
         "the fair at Rennet Bridge",
         "",
         ("the fair at Rennet Bridge did not shrink",
          "the fair at Rennet Bridge lay beside a railway")),
  cond2=("every drove in the later study that reached a fair after 1866 used a road the disease orders had left open",
         "the drove led by Ewan Garth, one of those in the later study, used only roads the orders had closed",
         "the drove led by Ewan Garth did not reach a fair after 1866",
         "the drove led by Ewan Garth",
         "the later study",
         ("the drove led by Ewan Garth did not reach a railhead",
          "the drove led by Ewan Garth carried cattle plague")),
  about="arguing that a trade said to have been ended by the railways was undone first by rules that closed its roads",
  implies="the dating of seven of the fairs rests on tolls alone and is less secure than that of the four with account books"),
 dict( key="placenames",
  topic="how village names were said",
  old="Dialect scholars long attributed the loss of the old pronunciations of village names in the Hollin vale to the village schools, where teachers were said to correct the local forms toward the spelling.",
  old_why="The old forms faded first among children, and the school logbooks record teachers correcting their pupils' speech.",
  problem="The account could not explain why the old forms survived in villages with the strictest schools, while they vanished from several villages that had no school at all.",
  ev1who="Brightwell",
  ev1where="recordings of village speech made in each decade from the 1930s",
  ev1what="whatever kind of school a village had, the old form of its name gave way within a generation of a railway halt opening there",
  ev1detail="the recordings were made for a survey of vowels rather than of names, so the speakers were not asked to say the names with any care",
  ev2who="a later study",
  ev2where="the railway timetables and the station signs of the vale",
  ev2what="each halt was named on its sign and in the timetables in the spelled form, which porters called out and passengers repeated at every stop",
  ev2detail="the timetables survive for every year the halts were open, so the year each spelled name began to be called out is known",
  revision="the old forms were lost mainly because the railway put the spelled names into daily speech, and the schools taught the spelling to children who already heard it at the halt",
  caveat="The recordings cover only villages on the valley floor, and the hill villages that no railway reached were not recorded.",
  cond1=("every speaker in Brightwell's recordings was born in the village where the recording was made",
         "Ada Pell was born in a town outside the vale",
         "Ada Pell is not among the speakers in Brightwell's recordings",
         "Ada Pell",
         "",
         ("Ada Pell did not use the old form of her village's name",
          "Ada Pell never travelled by rail")),
  cond2=("every halt in the later study that opened before 1880 had its name painted on a board rather than cast in iron",
         "the halt at Mickle Ford, one of those in the later study, had its name cast in iron",
         "the halt at Mickle Ford did not open before 1880",
         "the halt at Mickle Ford",
         "the later study",
         ("the halt at Mickle Ford was not named in the timetables",
          "the halt at Mickle Ford did not change how its village's name was said")),
  about="arguing that a change in speech blamed on the schools came mainly from the names a railway called aloud",
  implies="the railway explanation has not been tested in the hill villages the railway never reached"),
 dict( key="potteries",
  topic="a change in pottery",
  old="Archaeologists long read the change from red to grey pottery at the Tarrow settlements as the mark of newcomers from the coast, who were thought to have brought their own potters and their own taste.",
  old_why="Grey wares of similar shapes were common on the coast, and the change came quickly, within a few generations.",
  problem="The account could not explain why the grey pots kept the old local shapes and decoration, or why no other trace of newcomers, in burials or in buildings, appeared with them.",
  ev1who="Havard",
  ev1where="the clay of pots from nine settlements, examined under the microscope",
  ev1what="at every settlement, the grey pots were made from clay dug from a different bed than the red pots before them",
  ev1detail="the grains in each bed differ in shape and mineral, so a pot's clay can be matched to its bed without knowing who made it",
  ev2who="a later study",
  ev2where="the old channels of the river that crosses the settlements, dated from its buried gravels",
  ev2what="the river shifted its course in the century of the change, cutting off the red clay beds and exposing a grey-firing clay in its new banks",
  ev2detail="the gravels hold charcoal that can be dated, so the shift of the river can be placed within a few decades",
  revision="the pottery turned grey mainly because the river moved and the local potters had to dig a different clay, and trade with the coast played at most a small part",
  caveat="Only nine settlements have been sampled, and all of them lie within a day's walk of the river.",
  cond1=("every pot in Havard's sample was found in a house floor that could be dated",
         "the grey jar from the Tolly mound was found in a spoil heap with no dated floor",
         "the grey jar from the Tolly mound is not among the pots in Havard's sample",
         "the grey jar from the Tolly mound",
         "",
         ("the grey jar from the Tolly mound was not made from grey-firing clay",
          "the grey jar from the Tolly mound came from the coast")),
  cond2=("every channel in the later study that cut off a red clay bed was active after the change began",
         "the old channel at Sallen Bend, one of those in the later study, had silted up before the change began",
         "the old channel at Sallen Bend did not cut off a red clay bed",
         "the old channel at Sallen Bend",
         "the later study",
         ("the old channel at Sallen Bend held no charcoal",
          "the old channel at Sallen Bend did not expose any clay")),
  about="arguing that a change in pottery read as the arrival of newcomers came from a change in the local clay",
  implies="the river explanation may not hold for settlements farther from the river, which have not been sampled"),
 dict( key="observatory",
  topic="a star catalogue's errors",
  old="Historians of astronomy long blamed the errors in the Hesketh Observatory's great star catalogue on its night assistants, who were said to have read the divided circle of the transit instrument in haste to finish their long watches.",
  old_why="The errors were largest in the hours before dawn, when the assistants were most tired, and the director's letters complain more than once of their carelessness.",
  problem="The account could not explain why the same errors appeared in stars the director observed himself, or why they were larger on summer nights than on winter ones, when the watches were longest.",
  ev1who="Aubert",
  ev1where="the catalogue's original observing books",
  ev1what="the size of each error followed the temperature of the night on which it was made rather than the observer who made it",
  ev1detail="the books record the reading of a thermometer beside every observation, so each error can be set against the warmth of its night",
  ev2who="a later study",
  ev2where="the iron piers that carried the transit instrument",
  ev2what="the piers leaned toward the south as they warmed, turning the instrument off the meridian by enough to shift every reading it gave",
  ev2detail="the piers still stand in the old dome, so their lean can be measured at any temperature the building reaches",
  revision="the errors came mainly from iron piers that bent with the warmth of the night, and the haste of the assistants added at most a small part",
  caveat="The piers have been repainted and partly rebuilt since the catalogue was made, so their lean today may differ from the lean they had then.",
  cond1=("every star in Aubert's check was observed on a night whose temperature the books record",
         "the star listed as Hesketh 412 was observed on a night for which the books record no temperature",
         "the star listed as Hesketh 412 is not among those in Aubert's check",
         "the star listed as Hesketh 412",
         "",
         ("the star listed as Hesketh 412 was not observed by an assistant",
          "the star listed as Hesketh 412 was observed in summer")),
  cond2=("every measurement in the later study that was made above twelve degrees showed the piers leaning toward the south",
         "the measurement taken on the third of March, one of those in the later study, showed no lean toward the south",
         "the measurement taken on the third of March was not made above twelve degrees",
         "the measurement taken on the third of March",
         "the later study",
         ("the measurement taken on the third of March was not made at night",
          "the measurement taken on the third of March was made after the piers were rebuilt")),
  about="arguing that errors blamed on tired assistants came mainly from an instrument that moved with the heat of the night",
  implies="the lean measured in the piers today may not match the lean they had when the catalogue was made"),
 dict( key="cathedralglass",
  topic="cracked cathedral windows",
  old="Architects long blamed the cracking of the medieval glass in the windows of Saint Aldric's Cathedral on the settling of its foundations, which were thought to have strained the stone frames and broken the panes within them.",
  old_why="The cracks were worst in the windows of the south aisle, where the ground is softest, and a survey made in 1890 found the wall of that aisle slightly out of true.",
  problem="The account could not explain why panes cracked in windows whose frames showed no movement at all, or why the cracking began only after the windows were releaded in the 1850s.",
  ev1who="Osgood",
  ev1where="every cracked pane recorded in the cathedral's repair books since 1850",
  ev1what="the cracks began at the iron bars that brace the windows, and they appeared in the same years that rust was first noted on those bars",
  ev1detail="the repair books describe the state of the bars at each inspection, so the first rust on every window can be dated",
  ev2who="a later study",
  ev2where="the iron bars taken out of the windows during repairs",
  ev2what="the bars fitted at the releading were of a cheaper iron that swelled as it rusted, pressing on the glass around them until the panes broke",
  ev2detail="bars fitted before 1850 survive in two windows, so the older iron can be compared with the newer in the same building",
  revision="the glass cracked mainly because the iron fitted in the 1850s swelled as it rusted, and the settling of the south aisle added at most a small part",
  caveat="Only bars removed during repairs could be cut open, and the windows whose glass has never cracked have not been opened.",
  cond1=("every pane in Osgood's survey was repaired after the cathedral's repair books began",
         "the pane with the lily in the north transept has never been repaired",
         "the pane with the lily in the north transept is not among those in Osgood's survey",
         "the pane with the lily in the north transept",
         "",
         ("the pane with the lily in the north transept has not cracked",
          "the pane with the lily in the north transept is braced by bars of the older iron")),
  cond2=("every bar in the later study that had rusted through its surface had swollen by at least a millimetre",
         "the bar from the Jesse window, one of those in the later study, had swollen by less than a millimetre",
         "the bar from the Jesse window had not rusted through its surface",
         "the bar from the Jesse window",
         "the later study",
         ("the bar from the Jesse window was not fitted in the 1850s",
          "the bar from the Jesse window never pressed on the glass")),
  about="arguing that cracks blamed on a sinking wall came mainly from the iron put in to brace the glass",
  implies="the iron in the windows whose glass has never cracked has not been examined"),
 dict( key="portfever",
  topic="fever in a port town",
  old="Physicians of the day blamed the summer fevers of the port of Caddon on the vapours of the salt marsh to its east, which they believed the wind carried into the lower town on warm evenings.",
  old_why="The fevers came in the hottest months, when the marsh smelled worst, and they struck the lower town, nearest the marsh, far more often than the houses on the hill.",
  problem="The account could not explain why some streets right beside the marsh were spared in every outbreak, while a few houses on the hill, far from it, were struck again and again.",
  ev1who="Linnell",
  ev1where="the burial registers of the town's three parishes",
  ev1what="the deaths clustered around the public cisterns that stored rainwater from the roofs of the lower town, not around the marsh",
  ev1detail="the registers give the street and house of each burial, so every death can be placed on the town plan",
  ev2who="a later study",
  ev2where="the water company's records of which houses drew from which cistern",
  ev2what="the houses on the hill that fell ill again and again all drew their water from the cistern at the fish market, while the spared streets by the marsh had wells of their own",
  ev2detail="the company billed each house by the cistern it drew from, so the supply of every household is known for the years of the outbreaks",
  revision="the fevers spread mainly through water drawn from the public cisterns, and the air from the marsh played at most a small part",
  caveat="The water company's records begin only in 1849, so the outbreaks before that year cannot be traced to a supply.",
  cond1=("every death in Linnell's count was entered in one of the three parish registers",
         "the death of the sailor Tobias Ware was entered only in a ship's log",
         "the death of the sailor Tobias Ware is not among those in Linnell's count",
         "the death of the sailor Tobias Ware",
         "",
         ("the death of the sailor Tobias Ware was not caused by the fever",
          "the death of the sailor Tobias Ware took place on the hill")),
  cond2=("every house in the later study that drew from the fish market cistern had a death in the outbreak of 1853",
         "the house of the Pryor family, one of those in the later study, had no death in the outbreak of 1853",
         "the house of the Pryor family did not draw from the fish market cistern",
         "the house of the Pryor family",
         "the later study",
         ("the house of the Pryor family did not stand by the marsh",
          "the house of the Pryor family had a well of its own")),
  about="arguing that fevers blamed on the air of a marsh were spread mainly by the water the town stored",
  implies="the outbreaks before 1849 cannot be tested against the water supply and may have had another cause"),
 dict( key="fiddletunes",
  topic="a region's fiddle tunes",
  old="Folklorists long explained the change in the fiddle tunes of the Aske dales, which moved from the old minor modes into bright major keys within a generation, as a taste for the music of the dance halls in the towns.",
  old_why="The change came as young people began travelling to the towns for work, and the new keys matched those of the popular songs they heard there.",
  problem="The account could not explain why the tunes kept their old melodies and only moved to new keys, or why the change reached remote farms before it reached the villages nearest the towns.",
  ev1who="Garside",
  ev1where="the manuscript tune books kept by fiddlers in the dales",
  ev1what="each dale's tunes moved into the new keys in the years a concertina player first joined its dances, not in the years its young people began travelling to the towns",
  ev1detail="the fiddlers dated their entries and often noted who played with them, so each change of key can be set against the arrival of a new partner",
  ev2who="a later study",
  ev2where="the order books of the one workshop that sold concertinas in the dales",
  ev2what="the workshop sold its concertinas, each built to play in only two major keys, to the very farms and villages where the tunes changed",
  ev2detail="the workshop recorded the farm or village of every buyer, so the spread of the concertina can be dated across the dales",
  revision="the tunes moved into the new keys mainly so that fiddlers could play with the concertina, which could not play the old ones, and the dance halls played at most a small part",
  caveat="The tune books survive for only sixteen fiddlers, most of them from the upper dales.",
  cond1=("every tune book in Garside's study was dated by the fiddler who kept it",
         "the tune book found at Gill Head carries no dates",
         "the tune book found at Gill Head is not among those in Garside's study",
         "the tune book found at Gill Head",
         "",
         ("the tune book found at Gill Head does not contain any tunes in the new keys",
          "the tune book found at Gill Head belonged to a concertina player")),
  cond2=("every farm in the later study that bought a concertina before 1880 played its dance tunes only in the new keys in 1885",
         "the farm at Low Skell, one of those in the later study, still played some of its dance tunes in the old keys in 1885",
         "the farm at Low Skell did not buy a concertina before 1880",
         "the farm at Low Skell",
         "the later study",
         ("the farm at Low Skell did not have a fiddler",
          "the farm at Low Skell sent its young people to work in the towns")),
  about="arguing that a change in folk music credited to the towns came mainly from the instrument the tunes were played with",
  implies="the account rests mostly on the fiddlers of the upper dales and may not hold for the lower dales"),
 dict( key="fleece",
  topic="the fineness of a flock's wool",
  old="Wool merchants long believed that the fleeces of the Brenlow Down flocks grew coarser in the late eighteenth century because farmers had crossed their fine-woolled ewes with heavier rams bred for meat.",
  old_why="The coarsening followed a rise in the price of mutton, and the farmers' own letters speak of buying rams from the lowland breeders.",
  problem="The account could not explain why fleeces grew coarse on farms that never bought a lowland ram, or why on some farms the coarsening came decades after any change of breed.",
  ev1who="Trevenna",
  ev1where="the locks of wool pinned into the merchants' order books",
  ev1what="the fleeces on every farm grew coarse within a few years of its down being ploughed and sown with clover, whatever rams the farm kept",
  ev1detail="the merchants pinned a lock of each farm's wool beside every order, so the fineness of each year's clip can be measured",
  ev2who="a later study",
  ev2where="the enclosure maps and farm leases of the downs",
  ev2what="the leases required tenants to plough the downs and sow clover, a far richer feed than the old thin turf, on which the sheep grew a coarser fibre",
  ev2detail="the leases survive for most of the farms, so the year in which each down was first ploughed is known",
  revision="the wool grew coarse mainly because the sheep were moved onto the richer grazing of the ploughed downs, and the heavier rams played at most a small part",
  caveat="The merchants bought only the better clips, so the wool of the poorest farms is missing from the order books.",
  cond1=("every sample in Trevenna's study was pinned beside an order that names its farm",
         "the lock of wool found loose in the order book of 1791 was not pinned beside any order",
         "the lock of wool found loose in the order book of 1791 is not among the samples in Trevenna's study",
         "the lock of wool found loose in the order book of 1791",
         "",
         ("the lock of wool found loose in the order book of 1791 is not coarse",
          "the lock of wool found loose in the order book of 1791 came from a lowland ram")),
  cond2=("every farm in the later study whose down was ploughed before 1790 sold only coarse wool in 1800",
         "the farm at Coombe Lacey, one of those in the later study, sold fine wool in 1800",
         "the farm at Coombe Lacey did not have its down ploughed before 1790",
         "the farm at Coombe Lacey",
         "the later study",
         ("the farm at Coombe Lacey did not buy a lowland ram",
          "the farm at Coombe Lacey sold its wool to the merchants")),
  about="arguing that a coarsening of wool blamed on new breeding came mainly from a change in what the sheep ate",
  implies="the pattern is known only for the better farms, since the wool of the poorest farms was never sampled"),
 dict( key="leadmine",
  topic="flooding in a lead mine",
  old="Mining engineers long blamed the flooding of the Greyscar lead mine, whose lower levels had to be abandoned within twenty years, on the heavy rains of the district, which were said to soak down through the hill faster than the pumps could lift the water.",
  old_why="The floods were worst in wet winters, and the mine's pumps were known to be too small for a working so deep.",
  problem="The account could not explain why the flooding went on through a run of dry summers, or why the water rose fastest in the levels nearest the mine's eastern boundary.",
  ev1who="Rasmussen",
  ev1where="the mine captain's daily logs of the water pumped from each level",
  ev1what="the inflow to the lower levels jumped each time the engines at the old Brankholm workings beyond the eastern boundary were stopped, and it followed the rainfall hardly at all",
  ev1detail="the captain recorded the rainfall and the hours his neighbours' engines ran beside each day's water, so the inflow can be set against both",
  ev2who="a later study",
  ev2where="the old plans of the two mines",
  ev2what="a Brankholm level had been driven to within a few yards of the Greyscar workings, leaving a thin wall of rock through which the water held in the old mine could seep",
  ev2detail="both companies filed their plans with the county, so the levels of the two mines can be drawn together on one sheet",
  revision="the lower levels flooded mainly from water held in the workings next door, which seeped through the thin rock between the mines, and the rain played at most a small part",
  caveat="The plans of the Brankholm workings end in 1861, so any levels driven after that year are not shown on them.",
  cond1=("every day in Rasmussen's series has an entry for the water pumped from the lower levels",
         "the fourteenth of June 1866 has no entry for the water pumped from the lower levels",
         "the fourteenth of June 1866 is not among the days in Rasmussen's series",
         "the fourteenth of June 1866",
         "",
         ("no water was pumped from the lower levels on the fourteenth of June 1866",
          "the fourteenth of June 1866 was a day of heavy rain")),
  cond2=("every level in the later study that lay within ten yards of the Brankholm workings took in water through its eastern wall",
         "the level called Deep Adit, one of those in the later study, took in no water through its eastern wall",
         "the level called Deep Adit did not lie within ten yards of the Brankholm workings",
         "the level called Deep Adit",
         "the later study",
         ("the level called Deep Adit was not flooded",
          "the level called Deep Adit was driven after 1861")),
  about="arguing that flooding blamed on the rain came mainly from water held in the workings of the neighbouring mine",
  implies="the plans may not show every level near the boundary, since any driven after 1861 are missing from them"),
 dict( key="coinhoards",
  topic="buried coin hoards",
  old="Archaeologists long read the coin hoards found across the Cobbold uplands as savings buried in haste by families fleeing raiders, who died or never returned to dig them up.",
  old_why="Many of the hoards date from decades in which chronicles record raids on the coast, and a hoard left in the ground seemed to mark an owner who could not come back for it.",
  problem="The account could not explain why so many hoards lay beside springs and boundary stones rather than under houses, or why hoards went on being buried in decades when no raid is recorded at all.",
  ev1who="Halloran",
  ev1where="the reports of every hoard found in the uplands since 1850",
  ev1what="most of the hoards had been placed at springs, boundary stones and old burial mounds, and few had been hidden under the floors of houses",
  ev1detail="the finders' reports give the place of each discovery, so every hoard can be set on the map beside the features around it",
  ev2who="a later study",
  ev2where="the coins themselves",
  ev2what="the hoards placed at springs had been built up over many years, their coins spanning several reigns, while a hoard hidden in a single emergency held coins from a few years only",
  ev2detail="each coin names the ruler who issued it, so the span of years in every hoard can be read from its coins alone",
  revision="most of the hoards were offerings placed at springs and boundaries over many years, and flight from raiders explains at most a small part of them",
  caveat="Hoards found before 1850 were mostly melted down without any record, so where the earliest of them lay is unknown.",
  cond1=("every hoard in Halloran's survey was reported with a note of the place where it was found",
         "the hoard sold at the fair in Hobsley was reported with no note of where it was found",
         "the hoard sold at the fair in Hobsley is not among those in Halloran's survey",
         "the hoard sold at the fair in Hobsley",
         "",
         ("the hoard sold at the fair in Hobsley was not placed at a spring",
          "the hoard sold at the fair in Hobsley was hidden from raiders")),
  cond2=("every hoard in the later study that was built up over many years held coins of at least three rulers",
         "the hoard from the mound at Kilbride, one of those in the later study, held coins of a single ruler",
         "the hoard from the mound at Kilbride was not built up over many years",
         "the hoard from the mound at Kilbride",
         "the later study",
         ("the hoard from the mound at Kilbride was not an offering",
          "the hoard from the mound at Kilbride was buried during a raid")),
  about="arguing that hoards read as savings hidden from raiders were mostly offerings placed over many years",
  implies="the hoards found before 1850 cannot be tested against the pattern, since where they lay was never recorded"),
 dict( key="quakedamage",
  topic="earthquake damage in a market town",
  old="Engineers long blamed the damage that the earthquake of 1884 did to the market town of Cullingham on the poor masonry of its older houses, whose rubble walls were said to have shaken apart where newer brick would have held.",
  old_why="Most of the ruined houses were old ones, and the surveyors sent after the earthquake reported walls laid with little mortar and no bonding stones.",
  problem="The account could not explain why new brick houses in some streets fell while old rubble houses a few streets away stood with hardly a crack.",
  ev1who="Szabo",
  ev1where="the survey of damage made street by street in the weeks after the earthquake",
  ev1what="the ruined houses, old and new alike, lay along a narrow band running through the town, and outside that band even the oldest walls had mostly stood",
  ev1detail="the surveyors graded the damage to every building and noted its age and walling, so the effect of each can be separated on the town plan",
  ev2who="a later study",
  ev2where="boreholes sunk along the line of the band",
  ev2what="the band followed an old river channel filled with soft silt, which shook far more strongly than the rock under the rest of the town",
  ev2detail="the boreholes brought the ground up in cores, so the depth of silt under each street could be measured",
  revision="the damage followed mainly the soft ground of the buried channel, which shook more than the rock around it, and the poor masonry of the old houses played at most a small part",
  caveat="The surveyors graded only the buildings standing within the old borough, so the damage to the farms around the town was never recorded.",
  cond1=("every building in Szabo's count was graded by the surveyors",
         "the tithe barn at Cullingham Grange was never graded by the surveyors",
         "the tithe barn at Cullingham Grange is not among those in Szabo's count",
         "the tithe barn at Cullingham Grange",
         "",
         ("the tithe barn at Cullingham Grange was not damaged in the earthquake",
          "the tithe barn at Cullingham Grange stood on the soft ground of the old channel")),
  cond2=("every street in the later study that lay above more than ten feet of silt lost at least half its houses",
         "Friars Row, one of the streets in the later study, lost fewer than half its houses",
         "Friars Row did not lie above more than ten feet of silt",
         "Friars Row",
         "the later study",
         ("Friars Row was not built of rubble",
          "Friars Row lay on the rock beneath the town")),
  about="arguing that earthquake damage blamed on old masonry followed mainly the soft ground of a buried river channel",
  implies="the farms around the town cannot be checked against the pattern, since their damage was never recorded"),
 dict( key="valleysong",
  topic="a valley's changing birdsong",
  old="Ornithologists long put down the change in the song of the wrens of the Rookwood valley, whose males came to sing higher and shorter phrases within a few decades, to wrens from the lowlands moving in and breeding with them.",
  old_why="The change began soon after lowland wrens were first seen in the valley, and the new song resembled the higher song of the lowland birds.",
  problem="The account could not explain why the birds on the valley floor changed their song first, while those on the upper slopes, where the lowland wrens settled, kept the old song longest.",
  ev1who="Oyelaran",
  ev1where="recordings of the valley's wrens made at intervals since 1950",
  ev1what="the song rose first along the road and the railway that follow the valley floor, and it rose in step with the traffic they carried",
  ev1detail="every recording is logged with the place and year it was made, so the pitch of each territory's song can be followed over time",
  ev2who="a later study",
  ev2where="the noise of the valley measured at the wrens' territories",
  ev2what="the low hum of engines drowned the lower notes of the old song, and females heard males that sang higher at greater distances",
  ev2detail="females were played recordings of both songs under the valley's noise, so the distance at which each song could be heard was measured directly",
  revision="the song rose mainly because the noise of the road and the railway drowned its lower notes, and breeding with lowland wrens played at most a small part",
  caveat="The recordings made before 1970 used equipment that could not capture the highest notes, so the earliest songs may have been higher than they now seem.",
  cond1=("every recording in Oyelaran's series was logged with the place where it was made",
         "the recording on the tape marked C19 was logged with no place",
         "the recording on the tape marked C19 is not among those in Oyelaran's series",
         "the recording on the tape marked C19",
         "",
         ("the recording on the tape marked C19 was not made before 1970",
          "the recording on the tape marked C19 is the song of a lowland wren")),
  cond2=("every territory in the later study that lay within earshot of the road had males singing above the old pitch",
         "the territory by the chapel at Brackenrigg, one of those in the later study, had no males singing above the old pitch",
         "the territory by the chapel at Brackenrigg did not lie within earshot of the road",
         "the territory by the chapel at Brackenrigg",
         "the later study",
         ("the territory by the chapel at Brackenrigg was not held by a lowland wren",
          "the territory by the chapel at Brackenrigg lay on the upper slopes")),
  about="arguing that a change of song blamed on newcomer birds came mainly from the noise of traffic in the valley",
  implies="the earliest recordings may understate the pitch of the old song, so the size of the rise is uncertain"),
 dict( key="bindings",
  topic="crumbling book bindings",
  old="Librarians long blamed the crumbling of the leather bindings in the Wrexley Library on the damp of its old reading rooms, which was said to rot the leather of books shelved against the outer walls.",
  old_why="The worst bindings were found on the shelves along the north wall, which was often wet in winter, and the library's surveyors had complained of its damp for a century.",
  problem="The account could not explain why books bound before 1830 stayed sound on the same wet shelves, or why bindings crumbled just as badly in the dry gallery added in 1900.",
  ev1who="Winstanley",
  ev1where="the binders' invoices kept with the library's accounts",
  ev1what="the crumbling bindings had all been made after the binders changed their supplier of leather, whatever shelf the books had stood on",
  ev1detail="each invoice names the binder, the supplier of the leather and the books bound, so the leather on almost every volume can be traced to its maker",
  ev2who="a later study",
  ev2where="samples of leather cut from damaged and sound bindings",
  ev2what="the newer leather had been tanned by a quicker process that left acid in the skin, and the acid slowly broke the leather down wherever the books were kept",
  ev2detail="the samples were cut from bindings already due to be replaced, so the leather could be tested without harming a sound book",
  revision="the bindings crumbled mainly because of the acid left in leather tanned by the quicker process, and the damp of the reading rooms played at most a small part",
  caveat="Only bindings already due to be replaced could be sampled, so the leather of sound books was tested far less often than that of damaged ones.",
  cond1=("every volume in Winstanley's study was bound by a binder named in the invoices",
         "the prayer book given by the Marchant family was bound by a binder named in none of the invoices",
         "the prayer book given by the Marchant family is not among those in Winstanley's study",
         "the prayer book given by the Marchant family",
         "",
         ("the prayer book given by the Marchant family has not crumbled",
          "the prayer book given by the Marchant family was bound before 1830")),
  cond2=("every sample in the later study that was cut from leather of the quicker process held acid",
         "the sample from the spine of the county atlas, one of those in the later study, held no acid",
         "the sample from the spine of the county atlas was not cut from leather of the quicker process",
         "the sample from the spine of the county atlas",
         "the later study",
         ("the sample from the spine of the county atlas was not taken from a damaged binding",
          "the sample from the spine of the county atlas came from a book shelved on the north wall")),
  about="arguing that bindings blamed on a damp building crumbled mainly because of how their leather was tanned",
  implies="less is known about the leather of the sound books, because few of them could be sampled"),
 dict( key="cheese",
  topic="the rise of a regional cheese",
  old="Food historians long credited the fame of Ardley cheese to the recipe of the abbey at Ardley, whose monks were said to have perfected the cheese and taught it to the farms around them.",
  old_why="The abbey's records describe the making of a hard cheese, and the farms that later sold Ardley cheese in the cities lay within a day's walk of the abbey.",
  problem="The account could not explain why sales in the cities stayed small for two centuries after the abbey closed and then rose within a few years of 1860, or why farms far from the abbey sold as much as those beside it.",
  ev1who="Quillan",
  ev1where="the freight ledgers of the county's railway",
  ev1what="each district's sales rose in the year its farms could first send cheese from a station of their own, whether or not the district lay near the abbey",
  ev1detail="the ledgers record every consignment with the station it left from, the farm that sent it and its weight",
  ev2who="a later study",
  ev2where="letters from the dealers who bought the cheese",
  ev2what="the dealers in London ordered by rail and bought from whichever farms could deliver within two days, since the cheese spoiled on longer journeys by road",
  ev2detail="the letters were kept by the railway's agents, who filed each order with the station that filled it",
  revision="the fame of Ardley cheese came mainly from the railway, which let the farms reach the city markets quickly, and the abbey's recipe played at most a small part",
  caveat="Only letters kept by the railway's agents survive, so dealers who ordered by other means are hardly represented.",
  cond1=("every farm in Quillan's study sent its cheese from a station named in the freight ledgers",
         "the Coldharbour farm sent its cheese from a station named in none of the freight ledgers",
         "the Coldharbour farm is not among those in Quillan's study",
         "the Coldharbour farm",
         "",
         ("the Coldharbour farm sold no cheese in the cities",
          "the Coldharbour farm made its cheese by the abbey's recipe")),
  cond2=("every letter in the later study that was written by a London dealer named a railway station",
         "the letter signed by Amos Venn, one of those in the later study, named no railway station",
         "the letter signed by Amos Venn was not written by a London dealer",
         "the letter signed by Amos Venn",
         "the later study",
         ("the letter signed by Amos Venn ordered no cheese",
          "the letter signed by Amos Venn was written before 1860")),
  about="arguing that a cheese credited to an abbey's recipe grew famous mainly because the railway reached its farms",
  implies="less is known about dealers who ordered by other means, because few of their letters survive"),
 dict( key="millfires",
  topic="fires in cotton mills",
  old="Fires in the cotton mills of Harrowdale were long blamed on the carelessness of the workers, who were said to smoke among the bales and to leave lamps burning when they went home.",
  old_why="The owners' reports after each fire named a careless hand, and the magistrates fined workers found smoking in the mills.",
  problem="The account could not explain why fires grew more frequent after smoking was banned outright in 1852, or why most of them broke out at night, when the mills stood empty.",
  ev1who="Kilbey",
  ev1where="the surveys made by the mills' fire insurers",
  ev1what="most fires began in the carding rooms of mills that had put in the faster carding engines, and few began where workers smoked or lamps were kept",
  ev1detail="each survey records the room in which a fire began and lists the machines that stood in it",
  ev2who="a later study",
  ev2where="the logbooks of the town's fire brigade",
  ev2what="the fibre that gathered on the faster engines grew hot in their bearings and smouldered for hours before flames appeared, which is why the fires were so often found at night",
  ev2detail="the brigade logged the hour at which each fire was reported and the state of the building when it arrived",
  revision="most fires in the mills were started by fibre heated in the bearings of the faster carding engines, and the workers' carelessness played at most a small part",
  caveat="The brigade logged only the fires it was called to, so small fires that workers put out themselves are missing from the study.",
  cond1=("every mill in Kilbey's study was surveyed by one of the insurers",
         "the Ferncliff mill was surveyed by none of the insurers",
         "the Ferncliff mill is not among those in Kilbey's study",
         "the Ferncliff mill",
         "",
         ("the Ferncliff mill never had a fire",
          "the Ferncliff mill ran the faster carding engines")),
  cond2=("every fire in the later study that began in a carding room broke out in a mill running the faster engines",
         "the fire at the Brook Lane mill, one of those in the later study, broke out in a mill running none of the faster engines",
         "the fire at the Brook Lane mill did not begin in a carding room",
         "the fire at the Brook Lane mill",
         "the later study",
         ("the fire at the Brook Lane mill was not reported at night",
          "the fire at the Brook Lane mill was started by a careless worker")),
  about="arguing that mill fires blamed on careless workers were started mainly by the machines",
  implies="less is known about small fires, because those the workers put out were never logged"),
 dict( key="wolves",
  topic="wolves returning to a mountain range",
  old="The return of wolves to the Skarn mountains was long credited to the end of the bounty on wolves in 1971, which was said to have stopped the hunting that had kept them out of the range.",
  old_why="Bounty claims had fallen to nothing by then, and wardens began to report wolves in the range within twenty years of the bounty's end.",
  problem="The account could not explain why wolves came back first to valleys where hunting went on longest, or why they were slow to reach the national park, where it had stopped earliest.",
  ev1who="Brekke",
  ev1where="the land registers of the parishes in the old diocese",
  ev1what="wolves settled first in the valleys where farms had been given up and the fields had grown back into forest, whatever the local rules on hunting",
  ev1detail="the registers record for each parish the year in which each field was given up",
  ev2who="a later study",
  ev2where="the wardens' winter counts of deer",
  ev2what="the young forest held far more deer than the open pastures it replaced, and wolves settled where the deer were most numerous",
  ev2detail="the counts were made each winter by the same wardens along the same routes, so the numbers can be compared from year to year",
  revision="wolves returned to the Skarn mountains mainly because abandoned farmland grew into forest full of deer, and the end of the bounty played at most a small part",
  caveat="The deer counts began only after wolves had come back to some valleys, so the earliest years of their return are not covered.",
  cond1=("every valley in Brekke's study lay within the old diocese",
         "the Kelda valley lay outside the old diocese",
         "the Kelda valley is not among those in Brekke's study",
         "the Kelda valley",
         "",
         ("the Kelda valley has not been resettled by wolves",
          "the Kelda valley was farmed until recently")),
  cond2=("every count in the later study that was made on a forest route found deer",
         "the count on the Scaur ridge, one of those in the later study, found no deer",
         "the count on the Scaur ridge was not made on a forest route",
         "the count on the Scaur ridge",
         "the later study",
         ("the count on the Scaur ridge was not made in winter",
          "the count on the Scaur ridge was made by a new warden")),
  about="arguing that the return of wolves credited to the end of a bounty followed mainly from the regrowth of forest",
  implies="less is known about the first years of the wolves' return, because the deer counts began after them"),
 dict( key="lakebloom",
  topic="green blooms on a lake",
  old="The green blooms that spread across Lake Ellery each summer were long blamed on fertiliser washed from the farms around the lake, which was said to feed the algae.",
  old_why="The blooms were worst after wet springs, when the most water ran off the fields, and the farms' use of fertiliser had doubled since the war.",
  problem="The account could not explain why the blooms kept spreading after the farms cut their use of fertiliser, or why each summer they appeared first in the north bay, far from any farmland.",
  ev1who="Nyberg",
  ev1where="water sampled at fixed points around the shore",
  ev1what="most of the phosphorus that fed the algae entered the lake along the north shore, beside the sewage main that served the lakeside towns",
  ev1detail="the points were chosen so that every stream and pipe entering the lake had one close by",
  ev2who="a later study",
  ev2where="cores of mud drilled from the lake bed",
  ev2what="the blooms began in the year the main was laid, long before the farms' use of fertiliser rose, and grew as the towns it served grew",
  ev2detail="each year's settling mud forms its own layer, so the remains of algae can be dated to the year",
  revision="the blooms were fed mainly by phosphorus from the sewage main, and fertiliser from the farms played at most a small part",
  caveat="All the cores were drilled in the north bay, so the mud off the southern shore has not been dated.",
  cond1=("every sample in Nyberg's study was taken at one of the fixed points",
         "the sample from the ferry landing was taken at none of the fixed points",
         "the sample from the ferry landing is not among those in Nyberg's study",
         "the sample from the ferry landing",
         "",
         ("the sample from the ferry landing held no phosphorus",
          "the sample from the ferry landing was taken after a wet spring")),
  cond2=("every layer in the later study that formed after the main was laid held the remains of blooms",
         "the layer from the Heron Point core, one of those in the later study, held no remains of blooms",
         "the layer from the Heron Point core did not form after the main was laid",
         "the layer from the Heron Point core",
         "the later study",
         ("the layer from the Heron Point core was not drilled in the north bay",
          "the layer from the Heron Point core formed after a wet spring")),
  about="arguing that blooms blamed on farm fertiliser were fed mainly by a sewage main",
  implies="less is known about the southern shore, because no core was drilled there"),
 dict( key="registers",
  topic="gaps in parish registers",
  old="Gaps of a year or more in the baptism registers of the parishes of Eskwith were long put down to the plague of the 1660s, which was said to have killed or scattered the clergy who kept them.",
  old_why="The gaps cluster in the years when the plague was reported in the county, and several of the parishes that lost clergy to it have no entries for those years.",
  problem="The account could not explain why parishes the plague never reached show the same gaps, or why several parishes where it killed dozens kept their registers without a break.",
  ev1who="Ackroyd",
  ev1where="the records of the bishops' visitations",
  ev1what="the gaps fell in the years when a parish had lost its clerk and named no successor, whether or not the plague had reached it",
  ev1detail="each visitation record names the clerk of every parish and the date on which he took office",
  ev2who="a later study",
  ev2where="the payrolls of the customs houses at the county's ports",
  ev2what="many clerks left their parishes to work as writers at the ports, which paid far more, and the parishes that raised the clerk's fee kept their registers without a break",
  ev2detail="the payrolls give each writer's name and the parish he came from",
  revision="the gaps opened mainly because parishes lost their clerks to better-paid work at the ports, and the plague played at most a small part",
  caveat="The bishops visited only every few years, so a clerk who left and was replaced between two visits would not appear in the records.",
  cond1=("every parish in Ackroyd's study was visited by the bishop at least twice",
         "the parish of Low Mardle was visited by the bishop only once",
         "the parish of Low Mardle is not among those in Ackroyd's study",
         "the parish of Low Mardle",
         "",
         ("the parish of Low Mardle was not reached by the plague",
          "the parish of Low Mardle raised its clerk's fee")),
  cond2=("every writer in the later study who came from a parish with a gap had been that parish's clerk",
         "Thomas Garrow, one of the writers in the later study, had never been a parish clerk",
         "Thomas Garrow did not come from a parish with a gap",
         "Thomas Garrow",
         "the later study",
         ("Thomas Garrow was not paid more than a clerk",
          "Thomas Garrow came from a parish the plague reached")),
  about="arguing that gaps in parish registers blamed on the plague opened mainly because clerks left for better pay",
  implies="short vacancies may have been missed, because a clerk replaced between two visits left no trace in the records"),
 dict( key="bells",
  topic="cracked church bells",
  old="The cracking of church bells in the county of Brannock was long blamed on the hard winters of the 1840s, when frost was said to have made the bronze brittle as the bells were rung.",
  old_why="Most of the cracks were reported in the winter months, and the ringers' books note heavy frosts in several of the years when bells cracked.",
  problem="The account could not explain why bells cast before 1830 came through the same winters whole, or why bells cast after 1830 cracked just as often in mild years.",
  ev1who="Pentreath",
  ev1where="the account books of the foundry that cast the county's bells",
  ev1what="nearly all the bells that cracked had been cast after the foundry began buying its tin from a new supplier in 1830, whatever the winters they were rung in",
  ev1detail="the books record for each bell the date it was cast and the merchant who sold the tin for it",
  ev2who="a later study",
  ev2where="assays of fragments from the cracked bells",
  ev2what="the new supplier's tin carried enough lead to weaken the bronze, and bells cast from it cracked under ordinary ringing in any season",
  ev2detail="the churches kept the fragments when the bells were recast, each labelled with the bell it came from",
  revision="most of the bells cracked because the new supplier's tin weakened the bronze, and the hard winters played at most a small part",
  caveat="Only fragments that the churches chose to keep could be assayed, so bells whose pieces were sold or melted down are missing from the study.",
  cond1=("every bell in Pentreath's study was cast by the county's foundry",
         "the tenor bell at Wenlow church was cast by a foundry outside the county",
         "the tenor bell at Wenlow church is not among those in Pentreath's study",
         "the tenor bell at Wenlow church",
         "",
         ("the tenor bell at Wenlow church never cracked",
          "the tenor bell at Wenlow church was cast from the new supplier's tin")),
  cond2=("every fragment in the later study that came from a bell cast after 1830 held more lead than the older bronze",
         "the fragment from the bell at St Kenna's, one of those in the later study, held no more lead than the older bronze",
         "the fragment from the bell at St Kenna's did not come from a bell cast after 1830",
         "the fragment from the bell at St Kenna's",
         "the later study",
         ("the fragment from the bell at St Kenna's did not come from a bell cast by the county's foundry",
          "the fragment from the bell at St Kenna's came from a bell rung in a hard winter")),
  about="arguing that church bells whose cracking was blamed on hard winters cracked mainly because of impure tin",
  implies="less is known about bells whose fragments were not kept, because only kept fragments could be assayed"),
 dict( key="saltwells",
  topic="wells turning salty",
  old="The salt that crept into the town wells of Fennerby was long blamed on the sea floods of 1897, which were said to have soaked salt water into the ground beneath the streets.",
  old_why="The first wells to turn salty stood in streets the floods had reached, and the town's doctors reported the change in the months after the water went down.",
  problem="The account could not explain why wells went on turning salty for thirty years after the floods, or why wells in streets the floods never reached turned salty as well.",
  ev1who="Varley",
  ev1where="the records of the diggers who deepened the town's wells",
  ev1what="the wells turned salty in rings spreading out from the brewery on the quay, the nearest first, whether or not the floods had reached them",
  ev1detail="the diggers noted for each well the depth at which they found water and whether it tasted of salt",
  ev2who="a later study",
  ev2where="the brewery's pumping accounts",
  ev2what="the brewery drew more water from its own wells every year, and the salt reached each ring of wells a few years after the brewery's pumping rose",
  ev2detail="the accounts give the gallons the brewery pumped each week, because it paid its engine men by the gallon",
  revision="the wells turned salty mainly because the brewery's pumping drew sea water into the ground beneath the town, and the floods played at most a small part",
  caveat="The diggers recorded only the wells they were paid to deepen, so wells that were never deepened are missing from the study.",
  cond1=("every well in Varley's study was deepened by the town's diggers",
         "the well in Tanner's Row was never deepened by the town's diggers",
         "the well in Tanner's Row is not among those in Varley's study",
         "the well in Tanner's Row",
         "",
         ("the well in Tanner's Row did not turn salty",
          "the well in Tanner's Row stood in a street the floods reached")),
  cond2=("every well in the later study that stood within a mile of the brewery turned salty after the brewery's pumping rose",
         "the well at the Old Mint, one of those in the later study, never turned salty",
         "the well at the Old Mint did not stand within a mile of the brewery",
         "the well at the Old Mint",
         "the later study",
         ("the well at the Old Mint was not reached by the floods",
          "the well at the Old Mint was deepened by the town's diggers")),
  about="arguing that wells whose salt was blamed on sea floods turned salty mainly because a brewery's pumping drew in sea water",
  implies="less is known about wells that were never deepened, because the diggers recorded only the wells they worked on"),
 dict( key="schooldays",
  topic="absences from village schools",
  old="Absences from the village schools of Fellbeck were long blamed on farmers, who were said to keep their children at home to help with the harvest.",
  old_why="Teachers' letters to the school board complained that harvest work kept children away, and the district was known for its small family farms, where every hand was needed in late summer.",
  problem="The account could not explain why absences were highest in the winter months, long after the harvest was in, or why the children of shopkeepers and miners stayed away as often as farm children.",
  ev1who="Merriman",
  ev1where="the attendance registers of the district's schools",
  ev1what="the absences came mostly from children in the hamlets across the river, and they were clustered in the weeks of winter flood rather than at harvest",
  ev1detail="each register gives the hamlet every child walked from and marks attendance morning and afternoon",
  ev2who="a later study",
  ev2where="the road accounts of the parish vestry",
  ev2what="the absences of those children fell by half in the years after the vestry built footbridges over the fords, though farming in the district went on as before",
  ev2detail="the accounts record what each footbridge cost, the ford it replaced and the month in which it was opened",
  revision="children stayed away mainly because flooded fords cut them off from school, and harvest work played at most a small part",
  caveat="The registers of two schools were lost, so the hamlets that sent their children there are not covered.",
  cond1=("every school in Merriman's study kept a register that gave each child's hamlet",
         "the school at Nettlebeck kept a register that gave no child's hamlet",
         "the school at Nettlebeck is not among those in Merriman's study",
         "the school at Nettlebeck",
         "",
         ("the school at Nettlebeck had no pupils from across the river",
          "the school at Nettlebeck closed at harvest time")),
  cond2=("every child in the later study who crossed a ford on the way to school was absent more often before the footbridges were built",
         "Ellen Tapp, one of the children in the later study, was absent no more often before the footbridges were built",
         "Ellen Tapp did not cross a ford on the way to school",
         "Ellen Tapp",
         "the later study",
         ("Ellen Tapp did not live on a farm",
          "Ellen Tapp was kept at home to help with the harvest")),
  about="arguing that school absences blamed on harvest work came mainly from flooded fords",
  implies="less is known about the hamlets two of the schools served, because those schools' registers were lost"),
 dict( key="wrecks",
  topic="shipwrecks off a sandy coast",
  old="The wrecks along the coast of Otterby were long blamed on wreckers, who were said to light false lamps on the cliffs to lure ships onto the sands.",
  old_why="Local tales named families who plundered the wrecks, and several captains swore they had seen lights on shore before they ran aground.",
  problem="The account could not explain why ships ran aground by day as often as by night, or why the wrecks fell away after 1870, when the plundering went on as before.",
  ev1who="Treloar",
  ev1where="the reports of the inquiries held after each wreck",
  ev1what="most ships struck the same sandbank, at a point the chart then in use placed a mile further out to sea, whether they ran aground by night or by day",
  ev1detail="each report records where the ship struck and which chart its master had used",
  ev2who="a later study",
  ev2where="the notebooks of the survey that corrected the chart in 1870",
  ev2what="the bank had moved toward the shore since the old chart was drawn, which put its true line where the inquiries found the ships had struck",
  ev2detail="the surveyors recorded each sounding with its position, so the line of the bank can be laid over the old chart",
  revision="most ships were wrecked because the chart placed the sandbank too far out to sea, and the wreckers played at most a small part",
  caveat="Inquiries were held only when a ship was lost, so ships that struck the bank and got off again are missing from the study.",
  cond1=("every wreck in Treloar's study was the subject of an inquiry",
         "the loss of the brig Kittiwake was the subject of no inquiry",
         "the loss of the brig Kittiwake is not among those in Treloar's study",
         "the loss of the brig Kittiwake",
         "",
         ("the loss of the brig Kittiwake did not happen at night",
          "the loss of the brig Kittiwake was caused by wreckers")),
  cond2=("every sounding in the later study that was taken on the bank lay closer to shore than the old chart showed",
         "the sounding taken off Penhallow Head, one of those in the later study, lay no closer to shore than the old chart showed",
         "the sounding taken off Penhallow Head was not taken on the bank",
         "the sounding taken off Penhallow Head",
         "the later study",
         ("the sounding taken off Penhallow Head was not recorded with its position",
          "the sounding taken off Penhallow Head was made before 1870")),
  about="arguing that shipwrecks blamed on wreckers came mainly from a chart that placed a sandbank too far out",
  implies="less is known about ships that struck the bank and got off, because inquiries were held only for ships that were lost"),
 dict( key="canal",
  topic="a canal's falling trade",
  old="The fall in traffic on the Shelvock canal was long blamed on the railway that opened beside it in 1847, which was said to have taken the canal's cargoes by charging lower rates.",
  old_why="The railway company boasted of the freight it had won from the boatmen, and the canal's tolls fell in the decade after the line opened.",
  problem="The account could not explain why the tonnage carried on the canal had begun to fall five years before the railway opened, or why cargoes the railway did not carry, such as lime and stone, fell away just as fast.",
  ev1who="Beddoe",
  ev1where="the tonnage books kept by the lock keepers",
  ev1what="the loads fell in the years when the water at the summit ran low, and boats that crossed the summit carried less than boats that did not, whatever their cargo",
  ev1detail="the keepers weighed every boat that passed and noted the depth of water in their locks",
  ev2who="a later study",
  ev2where="the gauge book of the reservoir that fed the summit",
  ev2what="the reservoir had been losing water through a leaking dam since the early 1840s, and in most summers it was too low to keep the summit deep enough for full loads",
  ev2detail="the reservoir keeper read the gauge every morning and entered the level in the book",
  revision="traffic fell mainly because a leaking reservoir left the summit too shallow for loaded boats, and the railway played at most a small part",
  caveat="The tonnage books survive for only half of the locks, so boats that traded between the other locks are not counted.",
  cond1=("every lock in Beddoe's study had a keeper who noted the depth of water",
         "the lock at Scarrow Bridge had a keeper who never noted the depth of water",
         "the lock at Scarrow Bridge is not among those in Beddoe's study",
         "the lock at Scarrow Bridge",
         "",
         ("the lock at Scarrow Bridge was not on the summit",
          "the lock at Scarrow Bridge lost its trade to the railway")),
  cond2=("every summer in the later study in which the reservoir fell below its mark left the summit too shallow for full loads",
         "the summer of 1844, one of those in the later study, left the summit deep enough for full loads",
         "the summer of 1844 did not see the reservoir fall below its mark",
         "the summer of 1844",
         "the later study",
         ("the summer of 1844 was not a summer of heavy rain",
          "the summer of 1844 came before the railway opened")),
  about="arguing that falling traffic on a canal blamed on the railway came mainly from a leaking reservoir",
  implies="less is known about boats that traded between the other locks, because their tonnage books do not survive"),
]


# A conclusion that denies membership. It follows from the rule whether or not the case
# was ever inside the study, which is why a conditional written this way needs no scope.
MEMBER = re.compile(r"\b(?:is|are|was|were) not (?:among|in)\b")
# Every key here is negative, because modus tollens concludes that something is not the
# case. A choice worded that way is therefore a tell unless another choice about the same
# case is worded that way too.
# In any case: the builder capitalises a near miss before testing it, since it becomes a
# sentence, and "No water was pumped" matched nothing while the corpus check, testing the
# stored "no water", passed it (INC-0169).
NEGATIVE = re.compile(r"\b(?:not|no|none|never)\b", re.I)


# The sentences sentences() offers as choices, which the stated-idea schemas print with
# their first letter lowered.
LOWERED = ("old", "old_why", "problem", "ev1what", "ev2what", "ev1detail", "ev2detail",
           "revision", "caveat")


def _strings(p):
    """Every stored string of a passage, the rules' parts included."""
    out = []
    for v in p.values():
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, (list, tuple)):
            for x in v:
                if isinstance(x, str):
                    out.append(x)
                elif isinstance(x, (list, tuple)):
                    out += [y for y in x if isinstance(y, str)]
    return out


def check_corpus():
    """A malformed passage would produce a question with no defensible key, so the shape
    is checked at import rather than trusted.

    Both corpora. This used to walk P alone, so the eight long passages were never
    checked at all."""
    seen = set()
    need = ("old old_why problem ev1who ev1where ev1what ev1detail ev2who ev2where "
            "ev2what ev2detail revision caveat about implies").split()
    for p in P + P_LONG:
        if p["key"] in seen:
            raise ItemError("duplicate passage key %r" % p["key"])
        seen.add(p["key"])
        for f in need:
            if not p.get(f) or not str(p[f]).strip():
                raise ItemError("passage %s is missing %s" % (p["key"], f))
        # Stored for the middle of a sentence, where the stated-idea stem quotes it
        # (INC-0115). A capitalised article here printed "According to the passage, A
        # later survey" in every one of those stems.
        if p["ev2who"].split()[0] in ("A", "An", "The", "Later", "Another", "Subsequent"):
            raise ItemError("passage %s stores ev2who as a sentence opener: %r"
                            % (p["key"], p["ev2who"]))
        for c in ("cond1", "cond2"):
            if len(p[c]) != 6 or not all(str(x).strip() for x in p[c][:4]):
                raise ItemError("passage %s has a malformed %s" % (p["key"], c))
            near = p[c][5]
            if len(near) != 2 or not all(str(x).strip() for x in near):
                raise ItemError("passage %s %s needs two near misses" % (p["key"], c))
            # The builder tests a near miss as it prints it, capitalised, so the corpus has
            # to count it the same way (INC-0169).
            for n in near:
                if bool(NEGATIVE.search(n)) != bool(NEGATIVE.search(n[:1].upper() + n[1:])):
                    raise ItemError("passage %s %s: near miss %r counts as negative only in "
                                    "lower case" % (p["key"], c, n[:60]))
            if not p[c][0].startswith("every "):
                raise ItemError("passage %s %s: the rule must open 'every', because text() "
                                "prints it as a sentence of that form" % (p["key"], c))
        # A stated-idea choice prints each of these with its first letter lowered, which is
        # safe for "The" and wrong for a proper noun: a revision opening "Ardley cheese" was
        # offered as "ardley cheese grew famous" (INC-0179). A word the passage writes
        # capitalised in the middle of a sentence is a proper noun, and no lowered field may
        # open with one.
        mid = set()
        for s_ in _strings(p):
            mid |= set(re.findall(r"(?<=[a-z0-9,;:'] )([A-Z][A-Za-z'-]*)", s_))
        for f in LOWERED:
            w = re.match(r"[A-Za-z'-]+", p[f])
            if w and w.group(0)[0].isupper() and w.group(0) in mid:
                raise ItemError("passage %s %s opens with %r, a name this passage capitalises "
                                "mid-sentence, and the stated-idea choices lower its first "
                                "letter: open the sentence with a common word" % (p["key"], f, w.group(0)))


check_corpus()


def cap(s):
    """Capitalise a stored phrase where it opens a sentence. This is the safe direction:
    it cannot damage a proper noun, which lowercasing can, and the file has already
    been fixed twice for doing that."""
    return s[:1].upper() + s[1:]


def text(p):
    """The passage as the reader sees it: two paragraphs of the authored sentences.

    The two rules the inference questions turn on are printed before the synthesis, as
    one sentence. They are part of what the passage says, and the explanation of every
    inference item opens by quoting one of them as such (INC-0114)."""
    one = " ".join([p["old"], p["old_why"], p["problem"]])
    two = ("%s examined %s and found that %s; %s. %s of %s found that %s, and %s. "
           "%s, and %s. Taken together the two results suggest that %s. %s") % (
        p["ev1who"], p["ev1where"], p["ev1what"], p["ev1detail"],
        cap(p["ev2who"]), p["ev2where"], p["ev2what"], p["ev2detail"],
        cap(p["cond1"][0]), p["cond2"][0],
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


class RCBase(ListsQuestions, Gen):
    section = "V"
    type = "RC"
    domain = "nonmath"
    corpus = None
    # How a passage is shown and what its passage id is. The GRE variants in g_gre_rc.py
    # show the same passages as one paragraph, which is a different passage to a reader
    # and so carries a different id.
    render = staticmethod(lambda p: text(p))
    pid = "GP_"
    # What the wrong choices are, which the app prints under "Watch for". Each schema
    # says its own: this note was once written for stated idea in the shared emit() and
    # inherited by three schemas whose wrong choices it described falsely (INC-0117).
    wrong = None

    def __init__(self, corpus=None, suffix=""):
        """A schema over one corpus of passages.

        Two corpora exist because two exams want different passages, not because the
        questions differ: P is GMAT length and P_LONG is LSAT length. The id carries the
        suffix so the two variants are separate schemas to the bias check and the debt
        table, which they have to be: they draw from different prose and can skew
        differently.
        """
        if corpus is not None:
            self.corpus = corpus
        if suffix:
            self.id = self.id + suffix

    # A schema that asks one fixed question of each passage ships one item per passage, so
    # how its keys spread over the length ranks is decided by a handful of draws: 7 of the
    # 14 LSAT caveat keys once landed on the middle rank (INC-0122). Those schemas set
    # this and say their options through options(), and each passage's rank is assigned
    # rather than drawn. k is how many of the passage's own wrong answers are forced.
    once_per_passage = False
    k = 0

    def target_for(self, p, need):
        """The key's length rank to aim for, or None to draw it (see framework.balance)."""
        if not self.once_per_passage:
            return None
        return self.assigned(need)[p["key"]]

    def options(self, p):
        """(key, pool, own wrong answers) for one passage; a schema asked once per passage
        says its options here so its ranks can be assigned before anything is drawn."""
        raise NotImplementedError(self.id)

    def slate(self, right, pool, near):
        """The wrong answers emit() hands to balance(), as (text, note) pairs: the pool and
        the passage's own, neither repeating the key. The rank assignment reads the same
        lists, so it plans with exactly what the draw will have."""
        near = [w for w in near if w != right]
        return ([(w, "") for w in pool if w != right and w not in near],
                [(w, "") for w in near])

    def buildable(self, p, need):
        """The length ranks this passage's key can be given (framework.buildable_ranks)."""
        right, pool, near = self.options(p)
        cands, own = self.slate(right, pool, near)
        return buildable_ranks(right, cands, need, own, self.k)

    def assigned(self, need):
        """{passage key: rank} for this schema's corpus, worked out once."""
        cache = self.__dict__.setdefault("_assigned", {})
        if need not in cache:
            cache[need] = assign_ranks(
                [(p["key"], self.buildable(p, need)) for p in self.corpus], need)
        return cache[need]

    # Each schema lists the questions it asks of a passage in asks(), which make() draws
    # from, so the runner knows when it has made them all (framework.ListsQuestions).
    def units(self):
        return [(p, self.pid + p["key"]) for p in self.corpus]

    def emit(self, rng, choices_n, p, stem, right, pool, expl, diff, skill, sub,
             near=(), k=0, target=None):
        """`near` are wrong answers about the same thing as the key, and at least `k` of
        them are offered. Without them every wrong answer could come from another passage,
        and a wrong answer about a different subject is eliminated without reading
        (INC-0117). Which of them is offered is left to the length balance, because
        forcing particular ones pins where the key can rank by length."""
        cands, own = self.slate(right, pool, near)
        if len(cands) + len(own) < choices_n - 1:
            raise ItemError("%s has only %d distractors" % (self.id, len(cands) + len(own)))
        opts = [right] + [w for w, _ in balance(rng, right, cands, choices_n - 1,
                                                own=own, k=k, target=target)]
        if len(set(opts)) != choices_n:
            raise ItemError("%s drew a repeated option" % self.id)
        rng.shuffle(opts)
        item = {
            "id": None, "section": "V", "type": "RC", "sub": sub, "skill": skill,
            "diff": diff, "passage": self.render(p), "passageId": self.pid + p["key"],
            "stem": stem, "choices": opts, "answer": opts.index(right),
            "expl": expl, "gen": self.id, "domain": "nonmath",
            # Identity is the passage plus the question asked of it, never which other
            # sentences of the same passage were offered as distractors.
            "canon_ignores_choices": True,
            "wrong": self.wrong,
        }
        self.verify(item, right, choices_n, fmt=str)
        return item


class StatedIdea(RCBase):
    """What the passage says. Six askable sentences per passage, each its own question."""
    id = "rc_stated"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 2
    wrong = ("Every other choice states something the passage also says. They are true, and "
             "none of them answers the question that was asked, which is what makes them "
             "tempting.")

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

    def asks(self, p):
        return [(stem(p), field) for field, stem in self.ASKS]

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        stem, field = rng.choice(self.asks(p))
        s = sentences(p)
        right = lower1(s[field])
        pool = [lower1(v) for k, v in s.items() if k != field]
        expl = ("The passage says exactly this, and the question asks only what it says. "
                "Each of the other choices is also drawn from the passage, so each is true; "
                "none of them is what the stem asked about.")
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([1, 2, 2, 3]), "v_st", self.sub)


class MainIdea(RCBase):
    """Primary concern, worded in this passage's own terms so it is a distinct item.

    The wrong answers are the ones a main idea question is built to test: a part of the
    passage offered as the whole (either finding, or the limit it closes on), a claim
    broader than anything it argues, and the reverse of what it argues. Two of them are
    always this passage's own, so the key is not the only choice about its subject. Other
    passages' summaries stay in the pool for variety and can fill the remaining slots.

    One question per passage, so the key's length rank is assigned (INC-0122).
    """
    id = "rc_main"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 3
    wrong = ("The wrong choices are the usual traps for this question: one part of the "
             "passage offered as if it were the whole, a claim broader than anything the "
             "passage argues, the reverse of what it argues, or a description of a "
             "different passage.")

    once_per_passage = True
    k = 1

    def options(self, p):
        others = [q for q in self.corpus if q["key"] != p["key"]]
        right = p["about"]
        # At least one finding is always offered, because a finding is the part most
        # easily mistaken for the whole and it shares the passage's own words, which is
        # what stops the key being the only choice about this passage. The other own
        # options join the pool, where the length balance can use them.
        findings = ["reporting the finding of %s that %s" % (p["ev1who"], p["ev1what"]),
                    "reporting the finding of %s that %s" % (p["ev2who"], p["ev2what"]),
                    "reporting a finding about %s" % p["ev1where"],
                    "reporting a finding about %s" % p["ev2where"]]
        pool = (["arguing that most established accounts of %s are unreliable" % p["topic"],
                 "acknowledging that %s" % p["implies"],
                 "defending the account the passage opens with against the evidence "
                 "raised against it"]
                + [q["about"] for q in others])
        return right, pool, findings

    def asks(self, p):
        return [("The passage is primarily concerned with", None)]

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        (stem, _), = self.asks(p)
        right, pool, findings = self.options(p)
        expl = ("The passage opens with the received view, shows what it cannot account "
                "for, presents two findings, and states what they support. That is the "
                "shape of the whole passage, and the correct choice describes it. The other "
                "choices describe one part of the passage as if it were the whole, claim "
                "more than the passage argues, reverse it, or describe a different passage.")
        return self.emit(rng, choices_n, p, stem,
                         right, pool, expl, rng.choice([2, 3, 3]), "v_st", self.sub,
                         near=findings, k=self.k, target=self.target_for(p, choices_n - 1))


class Inference(RCBase):
    """Modus tollens over a rule the passage states.

    The key MUST be true given the rule, which the passage prints, and the case, which
    the stem prints. Two wrong answers are always about the same case: authored near
    misses that claim something neither premise establishes, one of them worded in the
    negative like the key. The rest come from the classic invalid moves, the converse
    and the inverse, and from conclusions that belong to other cases.
    """
    id = "rc_infer"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 4
    wrong = ("The wrong choices that name the same case are the traps: each says something "
             "about it that neither the rule in the passage nor the premise in the question "
             "establishes. The others run the rule backwards, stretch the passage's "
             "conclusion, or concern a different case.")

    def asks(self, p):
        # The stem STATES the case; the long comment above the return in make() says why.
        return [("If %s, which of the following can be properly inferred from the passage?"
                 % cond[1], cond) for cond in (p["cond1"], p["cond2"])]

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        stem, cond = rng.choice(self.asks(p))
        univ, case, concl, subject, scope, near = cond
        other = p["cond2"] if cond is p["cond1"] else p["cond1"]
        right = concl[0].upper() + concl[1:] + "."
        near = [n[0].upper() + n[1:] + "." for n in near]
        # At least one near miss worded in the negative is always offered, because every
        # key is negative and would otherwise be the only negative choice naming the case.
        # A positive near miss joins the pool with the rest.
        own = [n for n in near if NEGATIVE.search(n)]
        pool = [n for n in near if n not in own] + [
            # The converse: having the property does not make it a member.
            "Any case with the property described in the passage must be one of those the "
            "passage's generalisation covers.",
            # The inverse: denying the antecedent.
            "Cases outside the passage's generalisation cannot have the property it "
            "describes.",
            other[2][0].upper() + other[2][1:] + ".",
        ]
        # Two more used to be built here by gluing " in every case." onto the revision
        # and " for the same reason." onto the caveat, which printed choices such as
        # "...where landmarks are unusually continuous for the same reason." They were
        # filler, wrong because they barely parsed, and the near misses do their job.
        # Conclusions belonging to other passages, which are the same shape and length as
        # the key. They were added because without them the key was the shortest of the
        # five choices on 68 percent of items (INC-0088). On their own they were a subject
        # tell instead: the key was the only choice naming the case, and picking the
        # option that repeated the stem's names found it on 91 percent of draws
        # (INC-0117). The near misses above now hold two slots, so these fill the rest.
        for q in self.corpus:
            if q["key"] == p["key"]:
                continue
            for c in (q["cond1"], q["cond2"]):
                pool.append(c[2][0].upper() + c[2][1:] + ".")
        expl = ("The passage states that %s. The question adds that %s. If every case of "
                "the one kind has the property, then a case lacking the property is not a "
                "case of that kind, so %s. The other choices about the same case claim "
                "things that neither the rule nor the question establishes, and the rest "
                "either run the rule backwards or concern a different case."
                % (univ, case, concl))
        # The stem STATES the case, which is the whole point of a conditional question and
        # is why the corpus keeps the case apart from everything that goes into the prose.
        # It used to only name the subject, so the item asked what could be inferred about
        # the Sweetwater jurisdiction from a passage that never mentions Sweetwater: the
        # premise the question turns on was used to compute the key and to write the
        # explanation and was never shown to the person answering (INC-0097).
        #
        # Stating the case also keeps the two conditionals in a passage apart. The stem
        # used to end by naming the subject for exactly that reason, since otherwise both
        # produced the identical "which of the following can be inferred" and collapsed
        # into one item; the case does the same job and says something while doing it.
        # Not lower1(case). Every case clause is already stored in the form a sentence
        # wants it in the middle: "the Sweetwater jurisdiction had no mining district",
        # "Hedingham's rolls break off in 1348". Some open with a proper noun, and
        # lowercasing the first letter turned them into "hedingham's rolls" and
        # "thornbury changed stewards". Transforming a stored field to fit a slot is the
        # fault this file has already been fixed for twice; the field goes in as stored.
        # asks() builds the stem, so questions() lists exactly what this prints.
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([3, 4, 4, 5]), "v_inf", self.sub, near=own, k=1)


class CaveatImplication(RCBase):
    """What the author's qualification implies, worded per passage.

    Two wrong answers are always this passage's own misreadings of the closing sentence:
    that the first finding is unreliable, that the old account still holds wherever the
    studies did not look, or that the revision has been shown everywhere. Each is the
    mistake of turning a stated limit into a verdict. Other passages' implications can
    fill the remaining slots.

    One question per passage, so the key's length rank is assigned (INC-0122).
    """
    id = "rc_caveat"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 3
    wrong = ("The wrong choices misread the closing sentence: as a verdict against the "
             "evidence, as settling what was never tested, or as a limit that belongs to a "
             "different passage.")

    once_per_passage = True
    k = 1

    def options(self, p):
        others = [q for q in self.corpus if q["key"] != p["key"]]
        right = p["implies"]
        # At least one of the two misreadings that quote the passage is always offered,
        # because a choice that repeats the passage's words is what a reader who is
        # matching rather than reading reaches for. The third misreading, and the other
        # passages' limits, fill the rest.
        own = ["the finding of %s that %s is unreliable" % (p["ev1who"], p["ev1what"]),
               "it has been shown everywhere that %s" % p["revision"],
               "the evidence from %s is unreliable" % p["ev1where"],
               "the evidence from %s is unreliable" % p["ev2where"]]
        pool = (["the account of %s that the passage opens with still holds wherever the "
                 "studies did not look" % p["topic"]]
                + [q["implies"] for q in others])
        return right, pool, own

    def asks(self, p):
        return [("The author's closing observation most strongly suggests that", None)]

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        (stem, _), = self.asks(p)
        right, pool, own = self.options(p)
        expl = ("The closing sentence names a limit on what the evidence shows rather than a "
                "doubt about the evidence itself, and the correct choice states that limit "
                "in this passage's own terms. The wrong choices treat the limit as a verdict "
                "against the findings, treat what was never tested as settled one way or "
                "the other, or state a limit that belongs to a different passage.")
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([2, 3, 3, 4]), "v_inf", self.sub, near=own, k=self.k,
                         target=self.target_for(p, choices_n - 1))


# The GMAT draws on both corpora, because a real section mixes passage lengths. The LSAT
# variants draw only on the long one and carry a suffix, so the bias check and the debt
# table treat them as the separate schemas they are: different prose can skew differently,
# and a figure recorded against one corpus says nothing about the other.
GENS = [StatedIdea(P + P_LONG), MainIdea(P + P_LONG),
        Inference(P + P_LONG), CaveatImplication(P + P_LONG)]
GENS_LONG = [StatedIdea(P_LONG, "_long"), MainIdea(P_LONG, "_long"),
             Inference(P_LONG, "_long"), CaveatImplication(P_LONG, "_long")]


def assign_ranks(can, need):
    """Each passage's key length rank, as evenly spread as the ranks each can build allow.

    `can` is (passage key, buildable ranks) in corpus order. The most constrained passages
    are placed first, each on the least used rank it can build, and a tie goes to the next
    rank in rotation, so a corpus in which every passage can build every rank comes out as
    a plain rotation. Returns {passage key: rank}.
    """
    ranks = need + 1
    load = [0] * ranks
    out = {}
    order = sorted(range(len(can)), key=lambda i: len(can[i][1]))
    for n, i in enumerate(order):
        key, ok = can[i]
        if not ok:
            raise ItemError("passage %s can build no length rank at all" % key)
        t = min(ok, key=lambda r: (load[r], (r - n) % ranks))
        out[key] = t
        load[t] += 1
    return out


def check_spread(gens=None, choices_n=5):
    """Every schema asked once per passage can spread its keys evenly over the ranks.

    Each passage's key is given a length rank it can build (INC-0122). A key longer or
    shorter than every option it can be offered with can only be the longest or the
    shortest, and enough of those pile that rank up whatever the assignment does. So this
    fails when the ranks cannot be filled to within one passage of each other, and names
    the passages with the fewest ranks open, which are the ones whose keys to rewrite.
    """
    need = choices_n - 1
    bad = []
    for g in (gens if gens is not None else GENS + GENS_LONG):
        if not g.once_per_passage:
            continue
        got = list(g.assigned(need).values())
        load = [got.count(t) for t in range(need + 1)]
        if max(load) - min(load) > 1:
            tight = sorted((len(g.buildable(p, need)), p["key"], g.buildable(p, need))
                           for p in g.corpus)[:4]
            bad.append("%s: keys per length rank, shortest to longest, %s; the passages "
                       "with the fewest ranks open are %s" % (
                           g.id, load, ", ".join("%s (%s)" % (k, r) for _, k, r in tight)))
    return bad


def check_premises(draws=300, choices_n=5):
    """An inference stem has to state the premise the answer turns on.

    The question is a modus tollens: the passage supplies the universal, the QUESTION
    supplies the particular case, and the key is what follows. The case is stored apart
    from the prose for exactly that reason, and for a long time the stem named the
    subject of the case without stating the case itself, so every item asked what could
    be inferred about a Sweetwater jurisdiction that the passage never mentions and the
    explanation told the student the passage had said so (INC-0097).

    Nothing about either string on its own was wrong, which is why no existing check saw
    it. What has to hold is a relation between the stem and the passage: the stem states
    a premise, and that premise is new, because a case already in the passage would make
    the question trivial rather than unanswerable. Both are checked here.

    The same held for the other premise, the rule, and was not looked for when the case
    was fixed (INC-0114). So the corpus pass also finds each rule in the rendered passage,
    and requires every outcome conclusion to put its case inside the rule's scope.
    """
    import random as _random
    bad = []
    # The corpus pass. Each conditional stores the subject its case is about, which the
    # stem no longer prints now that it prints the whole case; it is checked instead,
    # because the premise the question supplies and the conclusion it licenses have to
    # be about the same thing.
    #
    # Two partial tests rather than one strict one. Requiring the full subject phrase in
    # both clauses was tried and is wrong: the corpus properly writes "the male ringed
    # as B12" once and "B12" after, which is how the sentences want to read. So the
    # subject has to appear in at least one of the two, and the two have to share a
    # token that identifies something, a name or a code or a long word. Neither test
    # proves they are about the same thing; between them they catch a pair that plainly
    # is not.
    stop = set("""the that this which with from into over under about every each some
    their there where when what whose been were have they them then than only also more
    most much many less least other others another same such only not and but for nor
    was had has does did will would could should before after while during within""".split())
    for p in P + P_LONG:
        for which in ("cond1", "cond2"):
            univ, case, concl, subject, scope, near = p[which]
            # The rule has to be printed, because the key is derived from it and the
            # explanation quotes it as something the passage says. For as long as this
            # schema existed it was held beside the prose and never printed (INC-0114).
            if univ.lower() not in text(p).lower():
                bad.append("%s %s: the rule the key turns on is not in the passage: %r"
                           % (p["key"], which, univ[:60]))
            # And the case has to be one the rule covers. An outcome about a case outside
            # the study follows from nothing; a conclusion that denies membership follows
            # either way, which is why only outcomes need a scope.
            if scope:
                if scope not in univ or scope not in case:
                    bad.append("%s %s: the scope %r has to appear in the rule and in the "
                               "case, so the case is inside what the rule covers"
                               % (p["key"], which, scope))
            elif not MEMBER.search(concl):
                bad.append("%s %s: an outcome conclusion needs a declared scope and a "
                           "case placed inside it: %r" % (p["key"], which, concl))
            if subject.lower() not in (case + " " + concl).lower():
                bad.append("%s %s: neither the case nor the conclusion names %r"
                           % (p["key"], which, subject))
            def tokens(t):
                """Words that name something: a code, a name, or a long content word.

                The possessive is stripped, because the corpus writes "Hedingham's rolls"
                in the case and "Hedingham" in the conclusion and they are the same town.
                Capitalisation counts only away from the first word, where it means a
                proper noun rather than the start of a clause.
                """
                out = set()
                for m in re.finditer(r"[A-Za-z0-9]+(?:'s)?", t):
                    w = m.group(0)
                    base = w[:-2].lower() if w.endswith("'s") else w.lower()
                    if any(ch.isdigit() for ch in base):
                        out.add(base)
                    elif w[:1].isupper() and m.start() > 0:
                        out.add(base)
                    elif len(base) >= 6 and base not in stop:
                        out.add(base)
                return out
            for n in near:
                if not (tokens(case) & tokens(n)):
                    bad.append("%s %s: a near miss names nothing the case names, so it is "
                               "not about the same thing: %r" % (p["key"], which, n[:60]))
            if not any(NEGATIVE.search(n) for n in near):
                bad.append("%s %s: no near miss is worded in the negative, so the key would "
                           "be the only negative statement about the case" % (p["key"], which))
            if not (tokens(case) & tokens(concl)):
                bad.append("%s %s: the case and the conclusion share nothing that names "
                           "a thing, so they may not be about the same one" % (p["key"], which))
    for g in GENS + GENS_LONG:
        if not g.id.startswith("rc_infer"):
            continue
        rng = _random.Random(20260922)
        seen = set()
        for _ in range(draws):
            try:
                it = g.make(rng, choices_n)
            except ItemError:
                continue
            stem, key = it["stem"], it["stem"][:60]
            if key in seen:
                continue
            seen.add(key)
            if not stem.startswith("If ") or ", which of the following" not in stem:
                bad.append("%s: stem states no premise: %s" % (g.id, stem[:70]))
                continue
            premise = stem[3:stem.index(", which of the following")].strip()
            if len(premise.split()) < 4:
                bad.append("%s: premise is too thin to be one: %s" % (g.id, premise))
            if premise.lower() in it["passage"].lower():
                bad.append("%s: the premise is already in the passage, so the question "
                           "asks nothing: %s" % (g.id, premise[:60]))
    return bad


def check_tells(draws=400, choices_n=5, ceiling=0.4, gens=None):
    """No reading schema may be answerable by matching words instead of reading.

    Two shortcuts are measured, the ones INC-0117 found working on nine draws in ten.
    For an inference item, pick the choice that repeats the most names from the premise
    in the stem, or, among the choices that name the case at all, the one worded in the
    negative, since every key here is. For a main idea or caveat item, pick the choice
    whose words appear most in the passage. A shortcut that lands on the key and on
    nothing else counts against the schema, because a tie is a guess.

    The ceiling is twice what a blind guess earns among five choices. What was measured
    before the fix was 79 to 95 percent, so the check trips on the defect and not on the
    ordinary variation of a random draw. Stated idea is exempt: all of its choices are
    sentences of the passage by design, which is the whole trap that question sets.
    """
    import random as _random
    stop = set("""that this which with from into have been were their there where when
    what about than more most other only also such these those them they then some over
    under after before because between within without""".split())

    def names(t):
        out = set()
        for m in re.finditer(r"[A-Za-z0-9]+", t):
            w = m.group(0)
            if any(ch.isdigit() for ch in w) or (w[:1].isupper() and m.start() > 0) or len(w) >= 7:
                out.add(w.lower())
        return out

    def words(t):
        return {w.lower() for w in re.findall(r"[A-Za-z]{5,}", t)} - stop

    def unique_key(scores, answer):
        best = max(scores)
        return best > 0 and scores.count(best) == 1 and scores[answer] == best

    bad = []
    for g in (gens if gens is not None else GENS + GENS_LONG):
        if g.id.startswith("rc_stated"):
            continue
        rng = _random.Random(20260926)
        seen, n, hits, neg_hits = set(), 0, 0, 0
        for _ in range(draws):
            try:
                it = g.make(rng, choices_n)
            except ItemError:
                continue
            k = (it["passageId"], it["stem"], tuple(sorted(it["choices"])))
            if k in seen:
                continue
            seen.add(k)
            n += 1
            ch, a = it["choices"], it["answer"]
            if g.id.startswith("rc_infer"):
                ref = names(it["stem"][3:it["stem"].index(", which of the following")])
                overlap = [len(names(c) & ref) for c in ch]
                hits += unique_key(overlap, a)
                negs = [1 if (overlap[i] and NEGATIVE.search(c)) else 0 for i, c in enumerate(ch)]
                neg_hits += unique_key(negs, a)
            else:
                ref = words(it["passage"])
                hits += unique_key([len(words(c) & ref) / max(1, len(words(c))) for c in ch], a)
        for label, h in (("the words it shares with the stem or passage", hits),
                         ("being the only negative choice that names the case", neg_hits)):
            if n and h / n > ceiling:
                bad.append("%s: the key is found by %s on %d of %d draws (%d percent, "
                           "ceiling %d)" % (g.id, label, h, n, round(100 * h / n),
                                            round(100 * ceiling)))
    return bad
