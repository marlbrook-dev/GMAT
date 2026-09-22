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
import re

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


# The same structure at LSAT length. P runs 171 to 224 words, which is GMAT length; these
# run 259 to 358, which is where the hand written LSAT passages in this repository sit.
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
  ev2who="A subsequent study of litigation",
  ev2where="three of those same jurisdictions across forty years",
  ev2what="the timing of doctrinal change followed the arrival of capital that needed secure title to water at a distance from the stream, not any measurable change in the water available",
  ev2detail="the investment records survive because the ventures were incorporated, which means the dates can be fixed independently of the court records they are being compared against",
  revision="the doctrine followed the pattern of industrial demand for transportable, securable water rights rather than the physical scarcity of water itself",
  caveat="All nine jurisdictions were organised under territorial rather than state legislatures, whose members were appointed and whose statutes were subject to congressional revision.",
  cond1=("every jurisdiction in the study that adopted appropriation within a decade had an organised placer mining district",
         "the Sweetwater jurisdiction had no mining district of any kind",
         "the Sweetwater jurisdiction did not adopt appropriation within a decade",
         "the Sweetwater jurisdiction"),
  cond2=("every date Ferreira fixes comes from a claims register kept at the time",
         "the Bitterroot date was reconstructed from a later economic summary",
         "the Bitterroot date is not among those Ferreira fixes",
         "the Bitterroot date"),
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
  ev2who="A survey of herbarium material",
  ev2where="collections from six continents",
  ev2what="the same yeast lineage occurs across lichens that are otherwise unrelated, and its presence predicts the chemical differences that had been attributed to habitat",
  ev2detail="the herbarium specimens predate the hypothesis by decades, so the sampling cannot have been shaped by what the investigators expected to find",
  revision="a lichen is a community whose members are not fully enumerated by separating and culturing its parts, and some of its characters belong to partners the classical method could not see",
  caveat="The yeast has been shown to be present rather than shown to be necessary, and no lichen has yet been assembled from its components with and without it.",
  cond1=("every pair Nkemelu examined was collected from a single rock face",
         "the Patagonian pair was assembled from two localities",
         "Nkemelu did not examine the Patagonian pair",
         "the Patagonian pair"),
  cond2=("every specimen in the herbarium survey was collected before the hypothesis was proposed",
         "the Tasmanian material was collected in 2019",
         "the Tasmanian material is not in the herbarium survey",
         "the Tasmanian material"),
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
  ev2who="A comparison with institutional accounts",
  ev2where="two monastic houses in the same towns",
  ev2what="the prices those houses actually paid diverge from the assize price by margins that widen in years of poor harvest",
  ev2detail="the houses bought in bulk and recorded what they paid, so their accounts are evidence of transactions rather than of regulation",
  revision="the assize describes what authorities attempted rather than what buyers paid, and the divergence between the two is itself the more informative series",
  caveat="Both monastic houses bought at a scale no household could match, and their prices need not resemble those paid in the market by the week.",
  cond1=("every town in Duarte's comparison kept borough court rolls for the whole period",
         "Hedingham's rolls break off in 1348",
         "Hedingham is not among the towns in Duarte's comparison",
         "Hedingham"),
  cond2=("every price used from the institutional accounts records an actual purchase",
         "the 1361 figure is an estimate entered by the cellarer",
         "the 1361 figure is not among the prices used",
         "the 1361 figure"),
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
  ev2who="A tracking study",
  ev2where="the same population over three seasons",
  ev2what="the correction appears only after a bird has completed one full migration, and its accuracy improves with each subsequent one",
  ev2detail="the tags recorded position continuously rather than at capture points, which is what allows a correction to be distinguished from a lucky arrival",
  revision="the compass is one component of a system whose map is learned, and the learning rather than the sensing is what distinguishes an experienced migrant",
  caveat="Both studies concern a single species that migrates along a coastline, where landmarks are unusually continuous.",
  cond1=("every bird that corrected toward the goal had completed at least one full migration",
         "the bird tagged A19 was in its first autumn",
         "A19 did not correct toward the goal",
         "the bird tagged A19"),
  cond2=("every position used in the tracking study came from a continuously recording tag",
         "the 2021 positions were taken at capture points only",
         "the 2021 positions are not used in the tracking study",
         "the 2021 positions"),
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
  ev2who="A technical examination",
  ev2where="underdrawings in nine panels from those workshops",
  ev2what="the earliest geometrically consistent constructions were laid out over drawings that had already fixed the architecture, so the geometry was fitted to a scheme rather than generating it",
  ev2detail="the underdrawings were recorded by infrared reflectography, which shows the sequence of layers and not merely their presence",
  revision="the technique spread because patrons specified the effect it produced, and the geometry was recruited to deliver a result that had already been asked for",
  caveat="The eleven workshops are all Florentine, and the contract practice of other centres in the same decades is not documented to the same standard.",
  cond1=("every contract Mancuso dated was entered in a surviving notarial register",
         "the Strozzi commission is known only from a later inventory",
         "Mancuso did not date the Strozzi commission",
         "the Strozzi commission"),
  cond2=("every panel in the technical examination was recorded by infrared reflectography",
         "the Arezzo panel was examined by raking light alone",
         "the Arezzo panel is not in the technical examination",
         "the Arezzo panel"),
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
  ev2who="A survey of soil isolates",
  ev2where="four sites with no recorded agricultural or clinical exposure",
  ev2what="resistance is common and its genetic architecture is more varied than anything found in clinical isolates",
  ev2detail="the sites were chosen from land-use records compiled for other purposes, so the selection cannot have been made to favour the result",
  revision="resistance genes are ancient features of soil communities, and clinical use selects and concentrates them rather than creating them",
  caveat="That a gene is ancient in soil says nothing about how it reached the clinical strains that now carry it, which remains unexplained for most compounds.",
  cond1=("every sequence Iwasaki reports showed the damage patterns characteristic of ancient DNA",
         "the Yukon sequence showed no such damage",
         "Iwasaki does not report the Yukon sequence",
         "the Yukon sequence"),
  cond2=("every site in the soil survey was selected from land-use records compiled for other purposes",
         "the Cairngorm site was chosen after a preliminary result there",
         "the Cairngorm site is not in the soil survey",
         "the Cairngorm site"),
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
  ev2who="A study of strip allocation",
  ev2where="eight of those villages",
  ev2what="the scattering of strips distributes each household's holdings across soil types in a pattern that closely tracks local variation in drainage",
  ev2detail="the soil mapping was done independently of the strip records and the two were matched afterwards, so the pattern was not read into the allocation",
  revision="the open field system traded some efficiency for insurance against local failure, and the scattering that looks wasteful is the mechanism by which it did so",
  caveat="The insurance account explains the pattern of holdings and does not establish that the households involved chose it for that reason.",
  cond1=("every village in Okoro's matched comparison had one steward across the transition",
         "Thornbury changed stewards in 1761",
         "Thornbury is not in Okoro's matched comparison",
         "Thornbury"),
  cond2=("every soil map used in the allocation study was produced independently of the strip records",
         "the Wendle map was drawn from the strip records themselves",
         "the Wendle map was not used in the allocation study",
         "the Wendle map"),
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
  ev2who="A follow-up",
  ev2where="the same infants four months later",
  ev2what="the contrast acquired from nonsense sequences persisted and transferred to sequences the infants had not heard",
  ev2detail="the transfer items were constructed after the first session, so they cannot have been present in the original exposure",
  revision="the statistical distribution of sounds is sufficient for category formation, and the words are the usual carrier of that distribution rather than its source",
  caveat="The artificial language used a contrast that does not occur in the infants' ambient language, and whether the same holds for a contrast they hear daily is untested.",
  cond1=("every infant who acquired the contrast heard the full exposure schedule",
         "infant 14 missed the third session",
         "infant 14 did not acquire the contrast",
         "infant 14"),
  cond2=("every transfer item was constructed after the first session",
         "the falling-tone item was in the original stimulus set",
         "the falling-tone item is not a transfer item",
         "the falling-tone item"),
  about="separating two explanations that natural language confounds, by building a language in which they come apart",
  implies="the result is established for a contrast the infants do not otherwise hear and may not extend to one they do"),
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
    corpus = None

    def __init__(self, corpus=None, suffix=""):
        """A schema over one corpus of passages.

        Two corpora exist because two exams want different passages, not because the
        questions differ: P runs 171 to 224 words, which is GMAT length, and P_LONG runs
        at LSAT length. The id carries the suffix so the two variants are separate
        schemas to the bias check and the debt table, which they have to be: they draw
        from different prose and can skew differently.
        """
        if corpus is not None:
            self.corpus = corpus
        if suffix:
            self.id = self.id + suffix

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
    """Primary concern, worded in this passage's own terms so it is a distinct item."""
    id = "rc_main"
    skill = "v_st"
    sub = "Identify Stated Idea"
    diff = 3

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        others = [q for q in self.corpus if q["key"] != p["key"]]
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
        p = rng.choice(self.corpus)
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
        # Conclusions belonging to other passages, which are the same shape and length as
        # the key and are safely wrong because the stem names the subject it asks about.
        #
        # Without them the key was the shortest of the five choices on 68 percent of
        # items and the schema was answerable without reading (INC-0088). The key is one
        # clause by the nature of modus tollens, while the converse, the inverse, the
        # revision and the caveat all run long, so the pool had nothing at the key's
        # length but other[2]. Balance can only straddle a key with what it is given.
        for q in self.corpus:
            if q["key"] == p["key"]:
                continue
            for c in (q["cond1"], q["cond2"]):
                pool.append(c[2][0].upper() + c[2][1:] + ".")
        expl = ("The passage establishes that %s. The question adds that %s. If every case "
                "of the one kind has the property, then a case lacking the property is not "
                "a case of that kind, so %s. The two tempting wrong answers reverse that "
                "reasoning: one assumes that having the property makes a case a member, and "
                "the other assumes that a non-member cannot have it. Neither follows."
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
        # "Hedingham's rolls break off in 1348". Four of the forty open with a proper
        # noun, and lowercasing the first letter turned them into "hedingham's rolls" and
        # "thornbury changed stewards". Transforming a stored field to fit a slot is the
        # fault this file has already been fixed for twice; the field goes in as stored.
        stem = ("If %s, which of the following can be properly inferred from the passage?"
                % case)
        return self.emit(rng, choices_n, p, stem, right, pool, expl,
                         rng.choice([3, 4, 4, 5]), "v_inf", self.sub)


class CaveatImplication(RCBase):
    """What the author's qualification implies, worded per passage."""
    id = "rc_caveat"
    skill = "v_inf"
    sub = "Identify Inferred Idea"
    diff = 3

    def make(self, rng, choices_n):
        p = rng.choice(self.corpus)
        others = [q for q in self.corpus if q["key"] != p["key"]]
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
            univ, case, concl, subject = p[which]
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
