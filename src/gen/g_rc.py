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

from framework import Gen, ItemError, balance

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
]


# A conclusion that denies membership. It follows from the rule whether or not the case
# was ever inside the study, which is why a conditional written this way needs no scope.
MEMBER = re.compile(r"\b(?:is|are|was|were) not (?:among|in)\b")
# Every key here is negative, because modus tollens concludes that something is not the
# case. A choice worded that way is therefore a tell unless another choice about the same
# case is worded that way too.
NEGATIVE = re.compile(r"\b(?:not|no|none|never)\b")


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
            if not p[c][0].startswith("every "):
                raise ItemError("passage %s %s: the rule must open 'every', because text() "
                                "prints it as a sentence of that form" % (p["key"], c))


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


class RCBase(Gen):
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

    def target_for(self, p, need):
        """The key's length rank to aim for, or None to draw it (see framework.balance)."""
        return None

    def emit(self, rng, choices_n, p, stem, right, pool, expl, diff, skill, sub,
             near=(), k=0, target=None):
        """`near` are wrong answers about the same thing as the key, and at least `k` of
        them are offered. Without them every wrong answer could come from another passage,
        and a wrong answer about a different subject is eliminated without reading
        (INC-0117). Which of them is offered is left to the length balance, because
        forcing particular ones pins where the key can rank by length."""
        near = [w for w in near if w != right]
        cands = [(w, "") for w in pool if w != right and w not in near]
        if len(cands) + len(near) < choices_n - 1:
            raise ItemError("%s has only %d distractors" % (self.id, len(cands) + len(near)))
        opts = [right] + [w for w, _ in balance(rng, right, cands, choices_n - 1,
                                                own=[(w, "") for w in near], k=k,
                                                target=target)]
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

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
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
    """Primary concern, worded in this passage's own terms so it is a distinct item.

    The wrong answers are the ones a main idea question is built to test: a part of the
    passage offered as the whole (either finding, or the limit it closes on), a claim
    broader than anything it argues, and the reverse of what it argues. Two of them are
    always this passage's own, so the key is not the only choice about its subject. Other
    passages' summaries stay in the pool for variety and can fill the remaining slots.
    """
    id = "rc_main"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 3
    wrong = ("The wrong choices are the usual traps for this question: one part of the "
             "passage offered as if it were the whole, a claim broader than anything the "
             "passage argues, the reverse of what it argues, or a description of a "
             "different passage.")

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
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
        expl = ("The passage opens with the received view, shows what it cannot account "
                "for, presents two findings, and states what they support. That is the "
                "shape of the whole passage, and the correct choice describes it. The other "
                "choices describe one part of the passage as if it were the whole, claim "
                "more than the passage argues, reverse it, or describe a different passage.")
        return self.emit(rng, choices_n, p, "The passage is primarily concerned with",
                         right, pool, expl, rng.choice([2, 3, 3]), "v_st", self.sub,
                         near=findings, k=1, target=self.target_for(p, choices_n - 1))


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

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        cond = rng.choice([p["cond1"], p["cond2"]])
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
        stem = ("If %s, which of the following can be properly inferred from the passage?"
                % case)
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([3, 4, 4, 5]), "v_inf", self.sub, near=own, k=1)


class CaveatImplication(RCBase):
    """What the author's qualification implies, worded per passage.

    Two wrong answers are always this passage's own misreadings of the closing sentence:
    that the first finding is unreliable, that the old account still holds wherever the
    studies did not look, or that the revision has been shown everywhere. Each is the
    mistake of turning a stated limit into a verdict. Other passages' implications can
    fill the remaining slots.
    """
    id = "rc_caveat"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 3
    wrong = ("The wrong choices misread the closing sentence: as a verdict against the "
             "evidence, as settling what was never tested, or as a limit that belongs to a "
             "different passage.")

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
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
        expl = ("The closing sentence names a limit on what the evidence shows rather than a "
                "doubt about the evidence itself, and the correct choice states that limit "
                "in this passage's own terms. The wrong choices treat the limit as a verdict "
                "against the findings, treat what was never tested as settled one way or "
                "the other, or state a limit that belongs to a different passage.")
        stem = "The author's closing observation most strongly suggests that"
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([2, 3, 3, 4]), "v_inf", self.sub, near=own, k=1,
                         target=self.target_for(p, choices_n - 1))


# The GMAT draws on both corpora, because a real section mixes passage lengths. The LSAT
# variants draw only on the long one and carry a suffix, so the bias check and the debt
# table treat them as the separate schemas they are: different prose can skew differently,
# and a figure recorded against one corpus says nothing about the other.
GENS = [StatedIdea(P + P_LONG), MainIdea(P + P_LONG),
        Inference(P + P_LONG), CaveatImplication(P + P_LONG)]
GENS_LONG = [StatedIdea(P_LONG, "_long"), MainIdea(P_LONG, "_long"),
             Inference(P_LONG, "_long"), CaveatImplication(P_LONG, "_long")]


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
