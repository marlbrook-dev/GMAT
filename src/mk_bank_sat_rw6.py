#!/usr/bin/env python3
"""Emit src/bank_sat_rw6.js.

Run: python3 src/mk_bank_sat_rw6.py src/bank_sat_rw6.js

The last thin pair on the SAT. Craft and Structure held 46 items and Information and
Ideas 48, against 113 to 127 for the four Math domains and the two other Reading and
Writing ones. These 120 items, sixty of each, take them to 106 and 108.

Shape follows the College Board specification: a passage of roughly 25 to 150 words
followed by one multiple choice question with four answer choices, drawn from literature,
history and social studies, the humanities, and science. Subtypes are the six the
existing SAT banks use, in the proportions the specification gives for an operational
form: Words in Context and Central Ideas and Details are the most numerous, Cross-Text
Connections the least, because a cross-text item costs two passages.

Machinery is in src/bank_emit.py. The length tell is corrected by LIFT and check_lift
fails the run if a clause was too short to move the item it names; the older SAT reading
banks were written before that existed, which is how bank_sat_rw.js came to ship at 88
percent longest is key (INC-0069).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

I = []
def q(iid, skill, sub, diff, passage, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'RW', 'type': 'RW', 'sub': sub, 'skill': skill,
              'diff': diff, 'passage': passage, 'stem': stem, 'choices': choices,
              'answer': 0, 'expl': expl, 'wrong': wrong})

WIC = 'Which choice completes the text with the most logical and precise word or phrase?'
PURPOSE = 'Which choice best states the main purpose of the text?'
FUNCTION = 'Which choice best describes the function of the underlined sentence in the text as a whole?'
MAIN = 'Which choice best states the main idea of the text?'
INFER = 'Which choice most logically completes the text?'
EVID = 'Which finding, if true, would most directly support the researchers claim?'

# ============================================================ Words in Context
q('SR201','rw_cs','Words in Context',2,
 "The first photographs of the deep sea floor, taken in the 1940s, showed a landscape "
 "that oceanographers had expected to be featureless. Instead the images revealed tracks, "
 "burrows and mounds across every frame. The sea floor was not barren but ______, worked "
 "over continuously by animals too small to appear in the photographs themselves.",
 WIC,
 ['inhabited', 'illuminated', 'unstable', 'compressed'],
 "The sentence contrasts barren with what the tracks and burrows show, which is that animals live there. Inhabited is the contrast the evidence supports.",
 "Illuminated describes the photograph rather than the floor. Unstable and compressed are properties of sediment that the tracks do not establish.")
q('SR202','rw_cs','Words in Context',3,
 "Jacob Lawrence painted the sixty panels of The Migration Series simultaneously rather "
 "than one at a time, mixing a colour and applying it to every panel that needed it before "
 "moving on. The method was practical, since his paints were expensive, and it had a "
 "consequence he may not have intended: the series is ______ across its whole length, held "
 "together by a palette that could not drift.",
 WIC,
 ['uniform', 'chronological', 'unfinished', 'abstract'],
 "A single mixed colour applied across every panel produces consistency of palette, which the last clause names as a palette that could not drift.",
 "Chronological describes the subject matter rather than the palette. Unfinished contradicts the description, and abstract is not what the method produces.")
q('SR203','rw_cs','Words in Context',3,
 "Reviewers of the first edition complained that the dictionary was ______: it recorded how "
 "people actually spoke, including usages the reviewers regarded as errors, instead of "
 "ruling on what they ought to say. The editors replied that a record of use was the only "
 "kind of dictionary they had set out to make.",
 WIC,
 ['permissive', 'incomplete', 'derivative', 'antiquated'],
 "The complaint is that the dictionary describes rather than prescribes, which from the reviewers' side reads as allowing what should be forbidden.",
 "Incomplete, derivative and antiquated are other complaints a reviewer might make and none matches the objection the colon then explains.")
q('SR204','rw_cs','Words in Context',2,
 "Sea otters eat sea urchins, and sea urchins eat kelp. Where otters were hunted out, urchin "
 "populations grew until the kelp forests were stripped to bare rock. The otter is therefore "
 "described as a ______ species: its numbers are small, but the structure of the whole system "
 "depends on them.",
 WIC,
 ['keystone', 'migratory', 'sentinel', 'pioneer'],
 "The last clause defines the term needed: small numbers, large structural effect. That is what keystone names in ecology.",
 "Migratory, sentinel and pioneer each describe something real about some species and none of them means what the clause after the colon defines.")
q('SR205','rw_cs','Words in Context',3,
 "The composer left the tempo of the second movement unmarked. Performers have read the "
 "omission as ______, taking it to invite a choice rather than to record an oversight, and "
 "recordings of the movement vary in length by more than four minutes.",
 WIC,
 ['deliberate', 'careless', 'conventional', 'illegible'],
 "Reading the blank against the rest of the sentence: taking it to invite a choice rather than an oversight means reading it as intended.",
 "Careless is the reading the sentence explicitly sets aside. Conventional and illegible do not explain why performers vary so widely.")
q('SR206','rw_cs','Words in Context',4,
 "Early accounts of the Silk Road describe a single route carrying goods from China to the "
 "Mediterranean. Archaeological work has made that picture look ______: goods moved in short "
 "relays between neighbouring markets, and few traders travelled more than a fraction of the "
 "distance their cargo did.",
 WIC,
 ['oversimplified', 'implausible', 'unsubstantiated', 'unverifiable'],
 "The evidence does not deny that goods crossed the distance; it shows the mechanism was many short transfers rather than one journey. That makes the earlier picture too simple rather than false.",
 "Implausible and unsubstantiated overstate what the evidence shows, and unverifiable is a claim about the evidence rather than about the picture.")
q('SR207','rw_cs','Words in Context',3,
 "The building's concrete frame was left exposed, its formwork marks and pour lines visible "
 "from the street. What another architect would have covered, this one treated as ______, "
 "arguing that a building should be legible as the thing it is.",
 WIC,
 ['ornament', 'error', 'necessity', 'precedent'],
 "The sentence contrasts covering with treating as something worth showing, and the argument that follows is about legibility, so the marks are made a positive feature.",
 "Error is what the other architect would see. Necessity and precedent do not oppose covering.")
q('SR208','rw_cs','Words in Context',2,
 "For decades the fossil was catalogued as a juvenile of a known species. A recent study of "
 "its bone microstructure found growth rings indicating an adult animal, which makes the "
 "small size ______ rather than a stage: the creature was simply a small species, and a new "
 "one.",
 WIC,
 ['permanent', 'misleading', 'typical', 'unmeasured'],
 "The contrast is between a size that is a phase of growth and one that is final. Growth rings showing an adult make the small size the animal's settled condition.",
 "Misleading describes the catalogue rather than the size. Typical and unmeasured do not complete the contrast with a stage.")
q('SR209','rw_cs','Words in Context',4,
 "Zora Neale Hurston collected folklore in the towns where she had grown up, and her training "
 "as an anthropologist sat oddly with that fact. The discipline of the 1930s prized distance "
 "from the community studied; Hurston's ______ with hers was the thing that let her hear "
 "what a stranger would not.",
 WIC,
 ['familiarity', 'dissatisfaction', 'preoccupation', 'impatience'],
 "The clause contrasts the discipline's prizing of distance with what Hurston had instead, and closeness is what lets her hear what a stranger cannot.",
 "Dissatisfaction, preoccupation and impatience are all attitudes rather than the relation to the community that the contrast with distance requires.")
q('SR210','rw_cs','Words in Context',3,
 "The treaty's language on fishing rights is ______: each side signed a text it read as "
 "confirming its own position, and the disagreement that followed was not about whether the "
 "treaty had been broken but about what it had said.",
 WIC,
 ['ambiguous', 'obsolete', 'unenforceable', 'verbose'],
 "Two parties reading the same text as supporting opposite positions is the definition of language that admits more than one reading.",
 "Obsolete, unenforceable and verbose are other defects a treaty text can have and none of them produces the specific disagreement described.")
q('SR211','rw_cs','Words in Context',2,
 "Dust from the Sahara crosses the Atlantic every summer and falls on the Amazon basin. The "
 "quantity is small by the standards of a desert and ______ by the standards of a rainforest: "
 "the phosphorus it carries is roughly what the basin loses to its rivers each year.",
 WIC,
 ['substantial', 'negligible', 'seasonal', 'unpredictable'],
 "The sentence sets small against a second standard, and the colon says the amount matches the basin's annual loss, which makes it large in that frame.",
 "Negligible repeats rather than contrasts with small. Seasonal and unpredictable describe timing rather than quantity.")
q('SR212','rw_cs','Words in Context',3,
 "Marie Tharp drew the first map of the Atlantic floor from soundings taken by ships she was "
 "not permitted to sail on. Her plotting revealed a rift running the length of the "
 "mid-ocean ridge, a feature her collaborator initially dismissed as ______ before the "
 "earthquake records were overlaid and the two lines matched.",
 WIC,
 ['spurious', 'familiar', 'minor', 'inevitable'],
 "The dismissal is reversed by evidence that the feature is real, so what he thought was that it was not really there.",
 "Familiar, minor and inevitable are all ways of discounting something that is granted to exist, which the overlay would not have corrected.")

q('SR213','rw_cs','Words in Context',3,
 "A stradivarius and a well made modern violin are, in blind listening tests, largely "
 "______: players and audiences asked to identify which is which do no better than chance. "
 "The tests have not changed what the instruments sell for.",
 WIC,
 ['indistinguishable', 'incompatible', 'functionally identical', 'unremarkable'],
 "The colon explains the blank: listeners cannot tell them apart, which is what indistinguishable means.",
 "Functionally identical is close but is about use rather than perception, and the tests measure perception. Incompatible and unremarkable do not fit at all.")
q('SR214','rw_cs','Words in Context',4,
 "The novel is narrated by a character who was not present at most of the events he relates. "
 "Readers have called this a flaw and the author called it the point: an account assembled "
 "from what others said is ______ by construction, and the book is about how a town settles "
 "on a version of itself.",
 WIC,
 ['secondhand', 'fictional', 'unreliable', 'fragmentary'],
 "Assembled from what others said is precisely an account received at one remove, which is what secondhand names, and the clause says the book is about how such an account forms.",
 "Unreliable is the flaw readers allege rather than the neutral fact of construction. Fictional applies to any novel, and fragmentary is not what the construction entails.")
q('SR215','rw_cs','Words in Context',2,
 "Before refrigeration, ice was cut from northern ponds in winter, packed in sawdust and "
 "shipped south, where much of it survived the voyage. The trade looks ______ now, but it "
 "supplied Calcutta and Havana for decades and made a fortune for the Boston merchants who "
 "ran it.",
 WIC,
 ['improbable', 'unaccountable', 'primitive', 'impractical'],
 "The contrast with what follows, a trade that worked and made money, calls for a word about how it strikes a modern reader rather than a defect.",
 "Unaccountable and primitive are judgments the rest of the sentence argues against. Impractical is contradicted by a trade that worked.")
q('SR216','rw_cs','Words in Context',3,
 "The city's grid was laid out in 1811 across farmland, hills and a marsh, none of which the "
 "surveyors proposed to accommodate. The plan was ______ in the literal sense: it described a "
 "city that did not exist and left the ground to be brought into line with it.",
 WIC,
 ['prescriptive', 'unprecedented', 'theoretical', 'premature'],
 "The explanation after the colon is that the plan said what the ground should become rather than recording what it was, which is what prescriptive means.",
 "Unprecedented, theoretical and premature are all plausible descriptions and none of them is the one the colon defines.")
q('SR217','rw_cs','Words in Context',3,
 "Octavia Butler kept notebooks in which she wrote down sales figures she had not yet "
 "achieved and prizes she had not yet won, in the present tense. Read now, the entries look "
 "______ rather than boastful: almost everything in them came true.",
 WIC,
 ['prophetic', 'methodical', 'defensive', 'ironic'],
 "The sentence contrasts boastful with how the entries read given that they came true, and a record written in advance that turns out accurate reads as foretelling.",
 "Methodical describes the practice rather than how it reads. Defensive and ironic do not follow from the entries having come true.")
q('SR218','rw_cs','Words in Context',4,
 "Standard accounts credit the assembly line with the fall in the price of the Model T. The "
 "line certainly cut the hours per car, but the price fell for a second reason the accounts "
 "usually ______: Ford paid for the line out of a volume of sales that a lower price had "
 "itself produced, and each cut in price funded the next.",
 WIC,
 ['omit', 'dispute', 'overstate', 'qualify'],
 "The sentence says the second reason is usually not mentioned, and the colon then supplies it.",
 "Dispute and overstate require the accounts to address the reason at all, and qualify implies they mention it with reservations.")
q('SR219','rw_cs','Words in Context',2,
 "A cuckoo chick hatches before its nestmates, pushes the other eggs out of the nest, and is "
 "raised alone by birds of another species. The behaviour is ______: the chick has never seen "
 "an adult cuckoo and cannot have learned it.",
 WIC,
 ['innate', 'cooperative', 'reciprocal', 'acquired'],
 "The colon gives the reason: no opportunity to learn, so the behaviour must be present from the start.",
 "Acquired is the opposite of what the reason establishes. Cooperative and reciprocal describe relations rather than origins.")
q('SR220','rw_cs','Words in Context',3,
 "The archive holds the correspondence of a firm that traded for two centuries, and almost "
 "none of it concerns the decisions historians would most like to understand. Letters were "
 "written between offices; the partners who made the decisions sat in one room, and their "
 "reasoning is ______ from the record for exactly that reason.",
 WIC,
 ['absent', 'recoverable', 'obscured', 'protected'],
 "Discussion in a single room produces no letters, so nothing about it entered the archive at all.",
 "Obscured and protected imply the reasoning is in the record but hidden. Recoverable is the opposite of what the sentence says.")
q('SR221','rw_cs','Words in Context',3,
 "Publishers of nineteenth century serial fiction paid by the word, and critics have long "
 "treated the length of Victorian novels as a ______ of that arrangement. The account is "
 "tidy and the evidence is mixed: several of the longest novels of the period were sold "
 "outright for a fixed sum.",
 WIC,
 ['consequence', 'justification', 'measure', 'refutation'],
 "Critics treat length as produced by payment by the word, which is a causal claim, and the next sentence supplies counterevidence to it.",
 "Justification, measure and refutation each describe a different relation between the length and the arrangement.")
q('SR222','rw_cs','Words in Context',4,
 "The two paintings were long held to be by different hands. Infrared imaging of the "
 "underdrawing has now shown the same habits in both: the same shorthand for a hand, the "
 "same way of correcting a shoulder. What survives on the surface is ______; what lies "
 "beneath it is not.",
 WIC,
 ['divergent', 'damaged', 'later', 'characteristic'],
 "The contrast is between surface and underdrawing, and the underdrawings match. So the surfaces must be what differ, which is why the attributions differed.",
 "Damaged and later make claims about condition and date that the imaging does not support, and characteristic would make the surfaces agree too.")
q('SR223','rw_cs','Words in Context',2,
 "Mangrove roots slow the water that passes between them, and sediment carried by that water "
 "drops out and settles. Over decades the forest therefore ______ the ground it stands on, "
 "rising with the sea rather than drowning under it.",
 WIC,
 ['builds', 'stabilises', 'colonises', 'drains'],
 "Sediment dropping out and settling adds material, and the second clause says the ground rises, so the forest is making new land.",
 "Stabilises describes holding what is there. Colonises and drains do not account for the rise.")
q('SR224','rw_cs','Words in Context',3,
 "A radio telescope does not resolve fine detail unless its dish is very large. Linking "
 "several dishes across a continent and combining their signals produces the resolution of a "
 "single instrument of that span, so the array is ______ rather than literally enormous.",
 WIC,
 ['synthetic', 'portable', 'inexpensive', 'temporary'],
 "The array achieves by combination what one huge dish would achieve by size, so its aperture is assembled rather than built.",
 "Portable, inexpensive and temporary may all be true of an array and none of them is the contrast with literally enormous.")

q('SR225','rw_cs','Words in Context',3,
 "Vera Rubin measured the rotation of spiral galaxies and found the outer stars moving as "
 "fast as the inner ones, which the visible mass could not explain. The result was "
 "published without much notice for a decade, which makes the later account of it as a "
 "turning point look ______: the field turned, but not when the measurement appeared.",
 WIC,
 ['retrospective', 'overdetermined', 'premature', 'partisan'],
 "The colon says the turn happened later than the measurement, so calling the measurement the turning point is a judgment made after the fact.",
 "Overdetermined and partisan dispute the account rather than dating it, and premature would mean the turn came too early.")
q('SR226','rw_cs','Words in Context',2,
 "A tuning fork struck alone is quiet. Pressed against a table it is loud, and it stops "
 "sounding sooner. The table has not added energy; it has made the transfer of energy to the "
 "air more ______, and the same store is spent faster.",
 WIC,
 ['efficient', 'predictable', 'audible', 'reversible'],
 "The same energy leaves faster and louder, which means the coupling to the air has improved rather than that energy was added.",
 "Predictable and audible describe the effect rather than the transfer, and reversible says nothing about rate.")
q('SR227','rw_cs','Words in Context',3,
 "The manuscript's marginal notes are in three hands from three centuries, each responding "
 "to the last. The book is therefore ______ as well as a text: a record of readers arguing "
 "with one another across the page over three hundred years.",
 WIC,
 ['a conversation', 'a forgery', 'a compilation of extracts', 'a fragment'],
 "Three hands each responding to the last, arguing across the page, is an exchange, which is what the colon then spells out.",
 "Forgery, compilation and fragment describe other things a manuscript can be and none matches the exchange described.")
q('SR228','rw_cs','Words in Context',4,
 "Economists studying minimum wages disagree less than the public argument suggests, and the "
 "disagreement that remains is ______ rather than general: it concerns how large an increase, "
 "applied how quickly, in a labour market of what kind, and almost nobody now holds the "
 "position that any increase at all costs jobs in proportion.",
 WIC,
 ['conditional', 'theoretical', 'longstanding', 'technical'],
 "The colon lists the conditions the remaining disagreement depends on, which is what conditional names.",
 "Technical is close but describes the vocabulary rather than the structure. Theoretical and longstanding do not match the list of conditions.")
q('SR229','rw_cs','Words in Context',2,
 "Chimney swifts cannot perch. Their feet grip vertical surfaces and nothing else, so the "
 "birds spend almost the whole day in the air and roost by ______ to the inside of a chimney "
 "or a hollow tree.",
 WIC,
 ['clinging', 'descending', 'returning', 'signalling'],
 "Feet that grip vertical surfaces and cannot perch means holding on to a wall, which is what clinging names.",
 "Descending, returning and signalling describe movement or behaviour rather than the way the bird rests.")
q('SR230','rw_cs','Words in Context',3,
 "The court's opinion runs to ninety pages and its holding to two sentences. Lawyers reading "
 "it for guidance have found the length ______: the reasoning is set out at such width that "
 "almost any later case can be argued to fall inside some part of it.",
 WIC,
 ['unhelpful', 'intimidating', 'persuasive', 'unusual'],
 "The colon explains that breadth of reasoning makes the opinion usable to argue almost anything, which frustrates someone reading it for guidance.",
 "Intimidating and unusual are reactions to length rather than to what the colon explains, and persuasive is the opposite of the complaint.")
q('SR231','rw_cs','Words in Context',3,
 "Bamboo of a given species flowers everywhere at once, once in a century, and then dies. "
 "Plants raised from seed and grown on another continent flower in the same year as their "
 "relatives at home, which makes the timing ______ rather than a response to local "
 "conditions.",
 WIC,
 ['internal', 'irregular', 'observable', 'recent'],
 "Plants in a different climate flowering in the same year rules out local cues and leaves a clock carried by the plant itself.",
 "Irregular contradicts the once in a century regularity, and observable and recent are not alternatives to a response to conditions.")
q('SR232','rw_cs','Words in Context',4,
 "Translations of the Odyssey into English number in the dozens, and the differences between "
 "them are not mainly about accuracy. Every translator faces the same known words and the "
 "same known grammar; what varies is a set of choices about register, pace and how much "
 "strangeness to keep, which makes the tradition ______ rather than cumulative.",
 WIC,
 ['interpretive', 'contested', 'irreconcilable', 'redundant'],
 "If the words and grammar are settled and the differences lie in choices about rendering, the tradition consists of readings rather than of progress toward one correct version.",
 "Contested overstates a disagreement the passage says is not about accuracy. Irreconcilable and redundant are dismissals rather than descriptions.")

# ============================================================ Text Structure and Purpose
q('SR233','rw_cs','Text Structure and Purpose',3,
 "The Antikythera mechanism, recovered from a shipwreck in 1901, is a geared bronze device "
 "that models the motions of the sun, moon and planets. Nothing of comparable complexity "
 "survives from the next fourteen hundred years. The gap is usually read as a loss of "
 "knowledge, though it may instead reflect what happens to bronze: an obsolete instrument is "
 "worth melting down, and a device that survives at all is one that sank.",
 PURPOSE,
 ['To offer an alternative explanation of an apparent gap in the record',
  'To describe the construction and purpose of an ancient instrument',
  'To argue that ancient engineering was more advanced than is recognised',
  'To explain why bronze objects rarely survive from antiquity'],
 "The first two sentences set up the gap and the last offers a second reading of it that does not require knowledge to have been lost.",
 "The description and the point about bronze are the materials of the argument rather than its purpose, and no general claim about ancient engineering is made.")
q('SR234','rw_cs','Text Structure and Purpose',3,
 "Hokusai produced the Thirty-six Views of Mount Fuji in his seventies, having changed his "
 "artist's name more than thirty times over his career. Each change marked a shift in manner "
 "and each was public. The habit is often treated as eccentricity; it reads better as a "
 "working method, a way of marking off one body of work from the next so that neither had to "
 "answer for the other.",
 PURPOSE,
 ['To reinterpret a biographical habit as a deliberate professional practice',
  'To trace the development of an artist through the names he adopted',
  "To establish that the Fuji series was produced late in the artist's life",
  'To argue that changing names was common among artists of the period'],
 "The text names the habit, reports the usual reading, and replaces it with a reading of the habit as method.",
 "The development, the dating and the prevalence of the practice are either background or not claimed at all.")
q('SR235','rw_cs','Text Structure and Purpose',4,
 "Studies of handwashing among hospital staff report compliance of around forty percent when "
 "measured by hidden observers and around eighty when staff know they are being watched. "
 "Both figures are accurate measurements of something. The first measures behaviour and the "
 "second measures behaviour under observation, and a programme evaluated with the second "
 "will report success whether or not the first has moved.",
 PURPOSE,
 ['To explain how a choice of measurement can make an intervention appear effective',
  'To report that hospital handwashing compliance is lower than is generally believed',
  'To recommend that hospitals use hidden observers to measure compliance',
  'To question whether observed compliance figures are accurately recorded'],
 "The last sentence states the point: the two figures measure different things and the second will show success regardless.",
 "The compliance figure is the evidence, no recommendation is made, and the text calls both figures accurate.")
q('SR236','rw_cs','Text Structure and Purpose',3,
 "Rachel Carson wrote Silent Spring for a general readership and documented it for a hostile "
 "one. The book carries fifty-five pages of references. Carson expected to be attacked on "
 "the facts rather than on the argument, and the apparatus was built so that every claim "
 "could be followed to a source before the attack arrived.",
 PURPOSE,
 ['To explain why a book written for general readers was documented so heavily',
  'To summarise the argument that Silent Spring advanced about pesticides',
  'To describe the response the book received from the chemical industry',
  'To argue that popular science writing should include full references'],
 "The first sentence names the oddity and the last explains it as a defence prepared in advance.",
 "The argument of the book, the response it received and any general recommendation are not what the text is doing.")
q('SR237','rw_cs','Text Structure and Purpose',4,
 "A single tree ring is a poor thermometer. Its width depends on temperature, on rainfall, "
 "on the tree's age, on whether a neighbour fell that year and let light in. What makes tree "
 "rings usable is that the last three of those vary from tree to tree and the first does "
 "not, so averaging many trees leaves the shared signal and cancels the rest.",
 FUNCTION,
 ['It lists the influences that averaging is later said to remove',
  'It establishes that tree rings cannot be used to reconstruct past climate',
  'It introduces the method by which dendrochronology dates a piece of wood',
  'It concedes a limitation that the rest of the text does not address'],
 "The list of four influences is what the final sentence sorts into one shared and three that cancel.",
 "The text says rings are usable, dating is not discussed, and the limitation is addressed rather than conceded.")
q('SR238','rw_cs','Text Structure and Purpose',3,
 "The Erie Canal opened in 1825 and cut the cost of moving a ton of freight from Buffalo to "
 "New York from around a hundred dollars to around ten. Historians cite the figure often. "
 "It understates the change, because at a hundred dollars a ton most of the freight that "
 "later moved was not shipped at all, and the saving on goods that never travelled does not "
 "appear in it.",
 PURPOSE,
 ['To argue that a widely cited figure understates the effect it is used to measure',
  'To describe the engineering achievement that the Erie Canal represented',
  'To establish when the Erie Canal opened and what it cost to build',
  'To compare freight costs before and after the canal was completed'],
 "The text gives the figure, says historians cite it, and then explains what it leaves out.",
 "The engineering, the dates and the comparison are all material for that point rather than the point.")
q('SR239','rw_cs','Text Structure and Purpose',3,
 "Wikipedia's article on a contested subject is often more measured than the sources it cites. "
 "The reason is procedural rather than editorial: a sentence that one group of editors will "
 "not accept is removed, and what survives is what nobody removes. The result is not "
 "neutrality as a policy achieves it but neutrality as an equilibrium produces it.",
 PURPOSE,
 ["To explain a feature of a text by the process that produced it rather than by anyone's intention",
  'To praise the neutrality of an online encyclopedia on contested subjects',
  'To criticise the sources that contested Wikipedia articles rely on',
  'To describe the rules that Wikipedia editors are required to follow'],
 "The middle sentence says the reason is procedural rather than editorial and the last contrasts policy with equilibrium.",
 "The text neither praises nor criticises, and the rules are not what it describes.")

q('SR240','rw_cs','Text Structure and Purpose',3,
 "Bees are said to dance to tell hivemates where flowers are. The dance does carry direction "
 "and distance, and bees that watch it do fly out. But most watchers do not reach the "
 "advertised patch, and hives in which the dance is disrupted forage nearly as well as hives "
 "in which it is not. The signal is real; what it accomplishes is less settled than the "
 "textbook account allows.",
 PURPOSE,
 ['To grant a familiar claim while narrowing what the evidence establishes about it',
  'To argue that the waggle dance does not carry information about food sources',
  'To describe the experiments by which the meaning of the dance was determined',
  'To explain how bees locate flowers in the absence of a communicative signal'],
 "The text affirms that the dance carries information and then reports two findings that limit what follows from it.",
 "The first sentence of the text grants what B denies, the experiments are summarised rather than described, and no alternative mechanism is offered.")
q('SR241','rw_cs','Text Structure and Purpose',4,
 "The Domesday Book records the value of almost every manor in England in 1086 and in 1066. "
 "Historians use the pair of figures to measure the damage of the conquest. The measurement "
 "is only as good as the earlier number, which nobody recorded at the time and which the "
 "1086 commissioners obtained by asking people to remember.",
 FUNCTION,
 ['It identifies the weakness in a source that the preceding sentence relies on',
  'It explains how the Domesday commissioners gathered information in 1086',
  'It establishes that the Domesday Book is the most complete survey of its period',
  'It questions whether the conquest caused any measurable economic damage'],
 "The preceding sentence describes the use historians make of the two figures, and this one shows that one of the two is a recollection rather than a record.",
 "The method is mentioned in service of the weakness, no claim of completeness is made, and the damage itself is not disputed.")
q('SR242','rw_cs','Text Structure and Purpose',3,
 "Gothic cathedrals are often described as the work of anonymous craftsmen. The anonymity is "
 "partly an artefact of what was worth writing down: masons signed their work in marks cut "
 "into the stone, hundreds of which survive, and building accounts name individuals and "
 "their wages. What was not written was a narrative connecting a name to a design.",
 PURPOSE,
 ['To qualify a familiar description by distinguishing what is missing from what was never recorded',
  'To argue that the designers of Gothic cathedrals can now be identified by name',
  'To describe the system by which medieval masons were paid for their work',
  "To establish that masons' marks are the most reliable evidence about medieval building"],
 "The text takes the word anonymous, shows that names and marks survive, and locates the gap in the connecting narrative.",
 "No identification is claimed, the wages are one piece of evidence, and no source is ranked most reliable.")
q('SR243','rw_cs','Text Structure and Purpose',3,
 "A drug that works in mice fails in people about nine times in ten. The usual explanations "
 "are biological: mice are not small people. A second explanation is statistical and less "
 "often raised. Mouse studies are small, and a small study that reaches significance has, on "
 "average, overstated the effect it found, so the result that justifies a human trial is "
 "systematically the most flattering one available.",
 PURPOSE,
 ['To introduce a second account of a known failure rate and explain the mechanism behind it',
  'To argue that mouse models should no longer be used in drug development',
  'To describe the biological differences between mice and human beings',
  'To report the proportion of drugs that fail when tested in human trials'],
 "The text names the usual explanation, says a second is less often raised, and then sets out how it works.",
 "No recommendation about mouse models is made, the biology is named rather than described, and the failure rate is the starting point rather than the purpose.")
q('SR244','rw_cs','Text Structure and Purpose',4,
 "Maps of the Roman road network show a system radiating from Rome. Almost every road on "
 "such a map was built by the army and paid for by the treasury. Roads built by towns for "
 "their own traffic were not recorded centrally and have mostly been found by accident, in "
 "the course of digging for something else. The pattern the maps show is therefore partly a "
 "pattern in who kept records.",
 PURPOSE,
 ['To explain how the way evidence was created shapes the pattern a map appears to reveal',
  'To describe the methods by which the Roman army constructed military roads',
  'To argue that local Roman roads were more extensive than military ones',
  'To recommend that archaeologists search systematically for unrecorded roads'],
 "The last sentence states it: the radiating pattern partly reflects which roads generated records.",
 "Construction methods are not described, no claim about relative extent is made, and no recommendation is offered.")
q('SR245','rw_cs','Text Structure and Purpose',3,
 "Nella Larsen published two novels in two years and then nothing for the remaining thirty "
 "years of her life. Accounts of the silence reach for a plagiarism accusation, a divorce, "
 "a return to nursing. Each is documented and none explains the others away. What the "
 "record supports is that several things happened at once, which is how most careers end "
 "and is harder to narrate than a single cause.",
 PURPOSE,
 ['To resist a single-cause explanation of a biographical fact and say why one is sought',
  'To establish the sequence of events in the later life of a novelist',
  "To argue that the plagiarism accusation was the decisive factor in Larsen's silence",
  "To compare Larsen's career with those of her contemporaries"],
 "The text lists the candidate causes, says none disposes of the others, and closes on why a single cause is attractive to tell.",
 "The sequence is material, a single cause is what the text argues against, and no comparison is drawn.")

# ============================================================ Cross-Text Connections
q('SR246','rw_cs','Cross-Text Connections',4,
 "Text 1: Standardized testing at least applies the same instrument to every student. "
 "Teacher assessment does not, and the variation it introduces falls hardest on students "
 "whose teachers expect least of them. Whatever a test measures badly, it measures badly "
 "for everyone.\n\n"
 "Text 2: A single instrument applied to everyone is not the same as a fair one. A test "
 "written in the register of one group asks that group to recognise its own speech and asks "
 "the others to translate first. The uniformity is in the paper, not in what the paper "
 "demands of the person holding it.",
 'Based on the texts, how would the author of Text 2 most likely respond to the claim in the last sentence of Text 1?',
 ['By arguing that a uniform instrument can still make uneven demands of those who take it',
  'By agreeing that tests measure badly and proposing that they be improved',
  'By denying that teacher assessment varies with what teachers expect',
  'By pointing out that standardized tests are more expensive than teacher assessment'],
 "Text 2's whole point is that sameness of paper is not sameness of demand, which is a direct answer to measuring badly for everyone.",
 "Text 2 does not propose improvement, does not address teacher expectations, and says nothing about cost.")
q('SR247','rw_cs','Cross-Text Connections',3,
 "Text 1: Remote work removes the commute, and the commute is the part of the day that "
 "workers report disliking most. Surveys since 2020 find large majorities preferring at "
 "least some days at home, and productivity measured by output per hour has not fallen.\n\n"
 "Text 2: Output per hour captures the work that was already specified. It does not capture "
 "the work nobody assigned, which in most organisations begins in a conversation that was "
 "not scheduled. Measuring remote work by output is measuring the half of the job that is "
 "easiest to see.",
 'Which choice best describes the relationship between the two texts?',
 ['Text 2 questions whether the measure Text 1 relies on captures what matters',
  'Text 2 disputes the survey findings that Text 1 reports',
  'Text 2 agrees with Text 1 and offers an additional reason for the same conclusion',
  'Text 2 argues that commuting is less disliked than Text 1 claims'],
 "Text 1 rests on output per hour; Text 2 says that measure misses unassigned work.",
 "The surveys and the commute are not disputed, and Text 2 does not reach Text 1's conclusion.")
q('SR248','rw_cs','Cross-Text Connections',4,
 "Text 1: Museums that return contested objects to their countries of origin act rightly. "
 "An object taken under an occupation was not bought, and no length of possession converts a "
 "taking into a title.\n\n"
 "Text 2: The occupation argument is sound and it settles fewer cases than its users "
 "suppose. Most contested objects left their place of origin through a sale, often to a "
 "dealer, often at a price the seller accepted. Deciding those cases needs an account of "
 "when a sale under unequal conditions binds, and the taking argument does not supply one.",
 'Based on the texts, the author of Text 2 would most likely characterise the argument in Text 1 as',
 ['correct as far as it goes but inapplicable to the majority of disputed objects',
  'mistaken, because long possession does convert a taking into a valid title',
  'unnecessary, since museums have already returned the objects it concerns',
  'inconsistent with the practice of the museums that have adopted it'],
 "Text 2 opens by calling the argument sound and then says most objects left by sale, which the argument does not reach.",
 "Text 2 grants the taking argument rather than denying it, and says nothing about what museums have already done.")
q('SR249','rw_cs','Cross-Text Connections',3,
 "Text 1: The case for a four-day week rests on evidence from trials in which firms kept pay "
 "constant and cut hours by a fifth. Output held steady in most of them, and reported "
 "wellbeing rose sharply.\n\n"
 "Text 2: Firms that volunteer for a trial are firms whose managers already believe the "
 "thing will work, in industries where the work is measured in finished pieces rather than "
 "in hours of presence. The trials show what happens in those firms. Whether they show what "
 "would happen elsewhere is a separate question nobody has answered.",
 'Which choice best describes how Text 2 responds to Text 1?',
 ['By granting the results and questioning how far they extend beyond the firms that produced them',
  'By arguing that output in fact fell in most of the trials Text 1 describes',
  'By claiming that reported wellbeing is too subjective to be evidence',
  'By proposing a different length of working week than Text 1 considers'],
 "Text 2 does not contest the results; it says the firms were self selected and asks whether the findings generalise.",
 "Text 2 disputes neither the output figures nor the wellbeing measure, and proposes nothing.")
q('SR250','rw_cs','Cross-Text Connections',4,
 "Text 1: Dictionaries should record use. A dictionary that refuses to enter a word because "
 "its compilers dislike it is not describing the language; it is editing it, and readers who "
 "consult it to learn what a word means will be misled about what it means to everyone "
 "else.\n\n"
 "Text 2: No dictionary records all use, and none pretends to. Every entry rests on "
 "decisions about how many citations are enough, from which sources, over what span. Those "
 "decisions are judgments about which uses count, which is the thing the descriptive "
 "position says it does not do.",
 'Based on the texts, the author of Text 2 would most likely argue that the position described in Text 1 is',
 ['already committed to judgments of the kind it claims to avoid',
  'correct in principle but impossible to apply to a living language',
  'preferable to the alternative it rejects, though for a different reason',
  'inconsistent with how readers actually consult dictionaries'],
 "Text 2's closing sentence says the inclusion decisions are judgments about which uses count, which is what the descriptive position denies doing.",
 "Text 2 does not call the position impossible or preferable, and does not discuss how readers consult a dictionary.")
q('SR251','rw_cs','Cross-Text Connections',3,
 "Text 1: The introduction of a sugar tax in several cities was followed by falls of a fifth "
 "or more in the volume of sugary drinks sold within the city limits.\n\n"
 "Text 2: In two of those cities, sales in the ring of stores just outside the boundary rose "
 "by roughly the volume the city lost. In a third, with no adjacent jurisdiction within "
 "driving distance, they did not.",
 'Based on the texts, the evidence in Text 2 most directly bears on whether the fall reported in Text 1 reflects',
 ['a reduction in consumption or a change in where purchases were made',
  'a change in the price of sugary drinks or a change in their availability',
  'the effect of the tax or the effect of publicity surrounding it',
  'consumption by residents or consumption by visitors to the city'],
 "Sales rising just outside the boundary by the amount lost inside it is the signature of purchases moving rather than stopping.",
 "Price, publicity and visitors are other things that could matter and are not what the cross-boundary figures speak to.")
q('SR252','rw_cs','Cross-Text Connections',4,
 "Text 1: A biography should stay with what its subject did. Speculation about motive is "
 "the biographer writing about himself, and a reader can tell.\n\n"
 "Text 2: Selecting which deeds to report is already an account of what mattered about the "
 "person, and what mattered is a question about motive whether or not the word appears. The "
 "restraint Text 1 recommends does not remove the biographer from the book; it conceals "
 "where he is.",
 'Which choice best states the main point of disagreement between the two texts?',
 ['Whether a biography that avoids discussing motive thereby avoids interpreting its subject',
  'Whether biographers are capable of knowing what their subjects intended',
  'Whether readers prefer biographies that discuss motive to those that do not',
  'Whether the deeds of a subject can be established with certainty'],
 "Text 1 treats restraint as removing the biographer; Text 2 says selection is already interpretation, so restraint only hides it.",
 "Capability, reader preference and certainty about deeds are not what either text turns on.")

q('SR253','rw_cs','Cross-Text Connections',3,
 "Text 1: Charter schools in the city outperform district schools on the state test by "
 "roughly a third of a standard deviation, a gap that has held for six years.\n\n"
 "Text 2: Admission to the oversubscribed charters is by lottery, and the losers of those "
 "lotteries can be followed. Compared with lottery losers rather than with the district "
 "average, charter students gain about a tenth of a standard deviation.",
 'Which choice best describes the function of Text 2 in relation to Text 1?',
 ['It supplies a comparison group that reduces the size of the effect Text 1 reports',
  'It disputes the accuracy of the test scores on which Text 1 relies',
  'It explains why charter schools are oversubscribed in the city',
  'It argues that the gap Text 1 reports has not held for six years'],
 "Lottery losers are the right comparison, and against them the gap shrinks from a third to a tenth.",
 "Text 2 uses the same scores, does not explain oversubscription, and does not dispute the six years.")
q('SR254','rw_cs','Cross-Text Connections',4,
 "Text 1: The best evidence that a painting is by the master is the quality of the painting. "
 "Documents can be forged and provenances invented; the hand cannot be.\n\n"
 "Text 2: Judgments of quality are made by people who know what is at stake, and the same "
 "connoisseurs who could not be fooled have attributed and then withdrawn attributions from "
 "the same canvas within a decade. That the hand cannot be forged does not establish that "
 "the eye cannot be mistaken.",
 'Based on the texts, the author of Text 2 would most likely say that the argument in Text 1 confuses',
 ['the reliability of the evidence with the reliability of those who read it',
  'the quality of a painting with the fame of the painter who made it',
  'documentary evidence with the physical evidence of the canvas',
  'attribution as a scholarly question with attribution as a commercial one'],
 "Text 2's last sentence separates the forgeability of the hand from the fallibility of the eye, which is exactly this distinction.",
 "Fame, documents and commerce all figure in the surrounding discussion and are not what the closing sentence separates.")
q('SR255','rw_cs','Cross-Text Connections',3,
 "Text 1: Reintroducing wolves to the park restored the willows along the streams. Elk, no "
 "longer able to browse in the open without risk, stopped stripping the banks, and the "
 "willows returned within a decade.\n\n"
 "Text 2: Beaver numbers rose over the same decade, from one colony to nine. Beaver dams "
 "raise the water table, and willow grows where the water table is high. Which of the two "
 "changes came first is not recorded, and the park began no measurement of either until "
 "several years in.",
 'Which choice best describes how Text 2 relates to the explanation given in Text 1?',
 ['It identifies a second change that could produce the same outcome and notes that the order is unknown',
  'It denies that willows recovered along the streams during the decade in question',
  'It argues that beaver colonies were the cause of the decline in elk browsing',
  'It reports a measurement programme that settled the question Text 1 raises'],
 "Text 2 supplies a mechanism, high water table, that would also return the willows, and says the sequence was not recorded.",
 "Text 2 accepts the recovery, makes no claim about elk, and says measurement began late.")

q('SR256','rw_cs','Text Structure and Purpose',3,
 "The word robot entered English in 1921, in the translation of a Czech play about "
 "manufactured workers who rebel. The play was a commercial success and its coinage outlived "
 "it. What did not survive is the plot: the manufactured workers of the play are organic, "
 "grown rather than built, and nothing in the text resembles a machine.",
 PURPOSE,
 ['To note that a word has kept a currency its source did not, and has changed its sense in the process',
  'To summarise the plot and reception of an influential Czech play of the 1920s',
  'To argue that the modern conception of robots is mistaken about their origins',
  'To describe the process by which foreign words enter the English language'],
 "The text traces the word from the play, says the coinage outlived the play, and reports that the thing it named was not a machine.",
 "The plot is the evidence, no modern conception is called mistaken, and no general process is described.")
q('SR257','rw_cs','Text Structure and Purpose',4,
 "Hospitals report their surgical mortality rates, and the public can compare them. A "
 "surgeon who declines the hardest cases will report a better rate than one who takes them. "
 "Several states now adjust the published figures for the risk profile of the patients "
 "treated. The adjustment uses the information recorded at admission, which is the "
 "information the hospital enters.",
 FUNCTION,
 ['It identifies a limitation in the correction described immediately before it',
  'It explains how states calculate adjusted surgical mortality rates',
  'It establishes that risk adjustment has made published rates more accurate',
  'It argues that hospitals should not be required to publish mortality rates'],
 "The sentence about who enters the data follows the sentence about adjustment and says the correction depends on a figure the corrected party supplies.",
 "The calculation is named rather than explained, no improvement is established, and no recommendation is made.")
q('SR258','rw_cs','Text Structure and Purpose',3,
 "Hedy Lamarr and George Antheil patented a system for steering a torpedo by switching its "
 "control signal across frequencies in a sequence the sender and receiver both knew. The "
 "navy filed the patent and built nothing. The idea reappeared in the 1960s in a different "
 "field, and the technique is now in every mobile telephone, having reached that position "
 "without anyone consulting the patent.",
 PURPOSE,
 ['To trace an idea that became important through a route that did not run through its first statement',
  'To argue that the navy was mistaken not to build the system described in the patent',
  'To describe the technical operation of frequency hopping in modern telephones',
  'To establish who should be credited with inventing frequency hopping'],
 "The last clause is the point: the technique arrived where it is without anyone consulting the patent.",
 "The navy's decision, the technical operation and the question of credit are all raised in passing rather than argued.")
q('SR259','rw_cs','Text Structure and Purpose',4,
 "Nineteenth century asylum records are the richest surviving source on mental illness in "
 "the period, and they describe only those admitted. Admission depended on a family unable "
 "or unwilling to keep a person at home, which depended on the household's money, on how "
 "many people were in it, and on whether any of them could stay out of work. The records "
 "describe illness filtered through the resources of a household.",
 PURPOSE,
 ['To explain what a rich source can and cannot be used to measure',
  'To argue that nineteenth century asylums admitted patients who were not ill',
  'To describe the conditions under which asylum patients of the period lived',
  'To recommend that historians rely on sources other than asylum records'],
 "The text calls the source rich, names the filter that governed admission, and states what the records are therefore a record of.",
 "No claim is made that patients were not ill, conditions inside are not described, and no alternative source is recommended.")
q('SR260','rw_cs','Text Structure and Purpose',3,
 "A cookbook from 1390 gives quantities as handfuls and cooking times as the length of "
 "prayers. Historians have sometimes read the vagueness as a sign that medieval cooking was "
 "imprecise. A different reading is available: the book was written for people who already "
 "cooked, and a measure stated in the reader's own hand is precise for that reader and "
 "meaningless to anyone else.",
 PURPOSE,
 ['To offer a reading of a feature of a source that reverses the usual inference from it',
  'To describe the methods by which medieval cooks measured ingredients',
  'To argue that medieval cooking was more precise than modern cooking',
  'To establish the audience for which a fourteenth century cookbook was written'],
 "The text names the usual inference from the vagueness and supplies a reading on which the same feature indicates precision for its intended reader.",
 "The methods are the evidence, no comparison with modern cooking is made, and the audience is a premise of the alternative reading.")

# ============================================================ Central Ideas and Details
q('SR261','rw_ii','Central Ideas and Details',3,
 "Coral polyps build their skeletons from calcium carbonate and get most of their energy "
 "from algae living inside their tissue. When water warms beyond a threshold the algae "
 "produce compounds the polyp cannot tolerate, and the polyp expels them. The coral is then "
 "white and alive, living on what it can catch, and it will recover if the water cools "
 "within a few weeks.",
 MAIN,
 ["Bleaching is the expulsion of a coral's algae under heat stress, and is survivable if the stress is brief",
  'Coral polyps are unable to survive without the algae that live inside their tissue',
  'Warming water destroys the calcium carbonate skeletons that coral polyps build',
  'Corals catch most of the food they need from the water around them'],
 "The text describes what bleaching is, why it happens, and that recovery follows if cooling comes soon enough.",
 "The text says a bleached coral is alive, says nothing about the skeleton dissolving, and says catching food is what the coral falls back on.")
q('SR262','rw_ii','Central Ideas and Details',2,
 "The Grand Banks cod fishery supported fishing fleets for four centuries. Catches peaked in "
 "1968 at eight hundred thousand tonnes and collapsed over the next twenty years. A "
 "moratorium in 1992 put thirty thousand people out of work at once. Thirty years later the "
 "stock has not returned to a level that would support a commercial fishery.",
 MAIN,
 ['A long-established fishery collapsed and has not recovered in the decades since it closed',
  'The 1992 moratorium was the cause of the collapse of the Grand Banks cod stock',
  'Catches on the Grand Banks have risen steadily since the moratorium took effect',
  'Fishing fleets worked the Grand Banks for four centuries without affecting the stock'],
 "The text gives the peak, the collapse, the moratorium and the failure to recover.",
 "The moratorium followed the collapse, catches have not risen, and the collapse shows the stock was affected.")
q('SR263','rw_ii','Central Ideas and Details',3,
 "Mary Anning found and prepared the first complete ichthyosaur skeleton, the first two "
 "plesiosaurs, and the first British pterosaur. She sold them to collectors and museums to "
 "support her family. The scientific papers describing them were written by the men who "
 "bought them, and her name does not appear in most of the papers that made the specimens "
 "famous.",
 MAIN,
 ['A collector who found and prepared major fossils was largely left out of the literature describing them',
  'Ichthyosaurs and plesiosaurs were the most significant fossil discoveries of the period',
  'Museums of the period acquired their fossil collections mainly by purchase',
  'Scientific papers of the period were written only by men who owned the specimens described'],
 "The text pairs what Anning did with where her name is absent.",
 "The significance of the species, museum acquisition practice and a universal claim about authorship all go beyond the text.")
q('SR264','rw_ii','Central Ideas and Details',3,
 "A sourdough starter is a stable community of wild yeast and lactic acid bacteria. Neither "
 "organism could hold the flour on its own: the bacteria produce acid that suppresses most "
 "competitors, and the yeast tolerates that acid and produces sugars the bacteria use. A "
 "starter kept for years is the same community, not the same individuals.",
 MAIN,
 ['A starter is a self-sustaining partnership in which each organism makes the other possible',
  'Wild yeast is the organism responsible for the rise of a sourdough loaf',
  'Lactic acid bacteria prevent other microorganisms from growing in flour',
  'A starter maintained for many years contains the original organisms it began with'],
 "The text explains that neither organism could persist alone and that each supplies what the other needs.",
 "The yeast and the bacteria each do part of the work, and the last sentence denies that the individuals persist.")
q('SR265','rw_ii','Central Ideas and Details',4,
 "The Voyager probes carry a gold-plated record of sounds and images, selected in 1977 by a "
 "committee working in six weeks. The committee could not obtain permission to include a "
 "Beatles recording. It could include Bach, Chuck Berry and a Navajo night chant, whose "
 "rights holders agreed or held no rights the committee recognised. What left the solar "
 "system is a selection shaped by copyright as much as by curation.",
 MAIN,
 ['The contents of the Voyager record reflect what could be cleared as well as what was chosen',
  'The committee that assembled the Voyager record worked under an unreasonable deadline',
  "The Voyager record contains music from a wide range of the world's cultures",
  'Copyright law prevented the Voyager record from including any popular music'],
 "The last sentence states it: the selection was shaped by copyright as much as by curation.",
 "The deadline is mentioned, the range is an example, and Chuck Berry is popular music that was included.")
q('SR266','rw_ii','Central Ideas and Details',2,
 "The passenger pigeon was once the most numerous bird in North America, and flocks were "
 "described as darkening the sky for hours. The species nested in enormous colonies and "
 "seems to have required them: birds in small groups bred poorly. Commercial hunting reduced "
 "the colonies below the size at which breeding worked, and the population fell faster than "
 "the hunting alone can explain.",
 MAIN,
 ['A species that depended on very large colonies collapsed once hunting reduced them below a threshold',
  'Commercial hunting was responsible for the entire decline of the passenger pigeon',
  'Passenger pigeons were the most numerous bird species in North America',
  'Birds that nest in colonies are more vulnerable to hunting than solitary birds'],
 "The last sentence says the fall outran the hunting, which the colony requirement explains.",
 "The text expressly says hunting alone does not explain the rate, the abundance is background, and no general claim about colonial birds is made.")
q('SR267','rw_ii','Central Ideas and Details',3,
 "Aluminium was once more valuable than gold. It is the most common metal in the crust, but "
 "it occurs bound to oxygen in a compound that resists every method of separation known "
 "before electricity was cheap. Napoleon III is said to have served his most honoured guests "
 "on aluminium while the rest used silver. The price fell by a factor of two hundred within "
 "five years of the Hall-Heroult process.",
 MAIN,
 ['The value of aluminium reflected the difficulty of extracting it rather than its scarcity',
  "Aluminium is the most abundant metal in the earth's crust",
  'Napoleon III preferred aluminium tableware to silver for reasons of prestige',
  'The Hall-Heroult process was the first method capable of isolating aluminium'],
 "The text pairs abundance with an extraction problem and then reports the collapse in price when extraction became easy.",
 "The abundance and the anecdote are evidence, and the text says earlier methods existed but were not cheap.")
q('SR268','rw_ii','Central Ideas and Details',3,
 "Longitude at sea could not be found without knowing the time at a fixed reference. A clock "
 "that kept time on a rolling ship through changes of temperature and humidity did not "
 "exist. John Harrison spent forty years building four, each smaller than the last, and the "
 "fourth kept time on a voyage to Jamaica to within five seconds. The Board of Longitude "
 "paid him in instalments and never awarded the full prize.",
 MAIN,
 ['A clockmaker solved the longitude problem over four decades and was not fully rewarded for it',
  'Longitude at sea cannot be determined without an accurate reference clock',
  'The Board of Longitude was established to encourage solutions to a navigational problem',
  "Harrison's fourth clock was substantially smaller than the three that preceded it"],
 "The text traces the problem, Harrison's forty years, the successful trial and the withheld prize.",
 "The principle, the Board and the size are details in service of that account.")
q('SR269','rw_ii','Central Ideas and Details',4,
 "The Mercator projection preserves angles, which is why it was drawn: a straight line on the "
 "chart is a course of constant compass bearing, and a navigator can steer it without "
 "recalculation. Preserving angles requires distorting area, and the distortion grows with "
 "latitude. Criticism of the projection as a map of the world is fair. Criticism of it as a "
 "chart mistakes what it was for.",
 MAIN,
 ['A projection criticised for distorting area was designed for a purpose that requires the distortion',
  'The Mercator projection should no longer be used to represent the world',
  'Navigators require charts on which a constant bearing appears as a straight line',
  'All map projections distort either area or angle and none preserves both'],
 "The text explains why the distortion is necessary given the purpose, and distinguishes fair criticism of it as a world map from criticism of it as a chart.",
 "The text calls the world map criticism fair rather than urging abandonment, and the navigation point and the general rule are premises.")
q('SR270','rw_ii','Central Ideas and Details',3,
 "Bird song in cities is higher pitched than the song of the same species in the country. "
 "Traffic noise is concentrated at low frequencies, and a song that overlaps it is not "
 "heard. Recordings made in the same city parks before and after a reduction in traffic "
 "found the pitch falling again within two breeding seasons, which suggests the shift is "
 "adjustment rather than the evolution of a distinct urban population.",
 MAIN,
 ['The pitch of urban bird song is a reversible adjustment to noise rather than an evolved difference',
  'Traffic noise in cities prevents birds of many species from breeding successfully',
  'Birds in cities sing at a higher pitch than birds of the same species elsewhere',
  'Reducing traffic in city parks restores the bird populations that noise displaced'],
 "The before and after recordings and the two-season reversal are what the text uses to distinguish adjustment from evolution.",
 "Breeding failure is not claimed, the pitch difference is the observation rather than the point, and populations are not discussed.")
q('SR271','rw_ii','Central Ideas and Details',2,
 "Saffron is the stigma of a crocus, three per flower, picked by hand at dawn before the sun "
 "opens the bloom. A kilogram takes roughly a hundred and fifty thousand flowers and about "
 "forty hours of picking. No machine has been built that can do it, because the stigma must "
 "be separated from the style without bruising.",
 MAIN,
 ['The cost of saffron follows from a harvest that has resisted mechanisation',
  'Saffron crocuses must be picked at dawn because sunlight damages the stigma',
  'A kilogram of saffron requires approximately a hundred and fifty thousand flowers',
  'Machines have replaced hand labour in most branches of spice production'],
 "The text gives the labour, the quantity and the reason no machine does it, which together account for the cost.",
 "The dawn picking and the flower count are the details, and no claim about spice production generally is made.")
q('SR272','rw_ii','Central Ideas and Details',3,
 "A placebo is not an absence of treatment. Patients given a placebo in a trial are also "
 "given an appointment, an explanation, a schedule and someone who asks how they are, and "
 "trials that add a third arm receiving none of those find that the untreated arm does worse "
 "than the placebo arm on most reported outcomes. What the placebo arm measures is the "
 "effect of everything a trial provides except the drug.",
 MAIN,
 ['A placebo arm measures the effect of the care surrounding a treatment, not the effect of nothing',
  'Patients given a placebo recover as fully as patients given an active drug',
  'Three-arm trials are more informative than trials with two arms',
  'The attention patients receive in a trial is the principal cause of their recovery'],
 "The text lists what a placebo arm receives and closes by naming what it measures.",
 "No equivalence with an active drug is claimed, the three-arm design is evidence, and the last option overstates.")

# ============================================================ Command of Evidence
q('SR273','rw_ii','Command of Evidence',3,
 "Researchers proposed that the songs of humpback whales spread between populations rather "
 "than arising independently in each. They recorded the song sung off eastern Australia in "
 "one year and compared it with songs recorded further east in the years that followed.",
 EVID,
 ['The song recorded off eastern Australia in one year appeared, almost unchanged, in populations progressively further east over the following three years',
  'Humpback whales in every ocean sing songs that share a common structure of themes and phrases',
  'Whales in a single population all sing the same song at the same time in a breeding season',
  'The song sung by an eastern Australian population changed substantially from one year to the next'],
 "A song appearing later and further east, in sequence, is transmission rather than independent invention.",
 "Shared structure could be inherited, within-population agreement is consistent with either account, and year to year change says nothing about spread.")
q('SR274','rw_ii','Command of Evidence',3,
 "A team argued that the stone tools at the site were made by a group that had arrived from "
 "the coast rather than by the people who had occupied the valley for the preceding "
 "millennium.",
 EVID,
 ['The stone the tools are made from outcrops only within a day of the coast and nowhere in the valley',
  'The tools are of a type found at sites across the region throughout the period in question',
  'The site contains hearths and animal bone in the same layer as the tools',
  'Tools of the same type continued to be made in the valley for several centuries afterwards'],
 "Raw material available only near the coast places the makers, or at least the material, outside the valley.",
 "A widespread type, domestic debris and later continuity are each consistent with local manufacture.")
q('SR275','rw_ii','Command of Evidence',4,
 "A study reported that employees who used the company's mentoring programme were promoted "
 "sooner than those who did not. The authors concluded that the programme accelerated "
 "promotion.",
 'Which finding, if true, would most seriously weaken the authors conclusion?',
 ['Employees whose managers had already marked them for promotion were the ones most often referred to the programme',
  'The programme paired each participant with a mentor from a different department',
  'Participants reported higher job satisfaction than non-participants at the end of the programme',
  'The programme has been offered by the company for more than a decade'],
 "If referral followed a prior judgment that the employee would be promoted, the promotions explain the participation rather than the reverse.",
 "The pairing rule, the satisfaction finding and the programme's age leave the causal claim untouched.")
q('SR276','rw_ii','Command of Evidence',3,
 "Archaeologists proposed that a ring of postholes at the site held a roofed structure rather "
 "than an open enclosure.",
 EVID,
 ['The postholes are deep enough to have carried a load and are spaced at intervals a roof of the period would require',
  'The ring encloses an area comparable to that of other enclosures known from the region',
  'Pottery of the same period was recovered from the fill of several of the postholes',
  'The postholes were cut into a natural clay that holds an impression well'],
 "Depth sufficient for load bearing and spacing consistent with a roof are the two structural facts a roof requires.",
 "Comparable area, dated fill and good preservation bear on other questions.")
q('SR277','rw_ii','Command of Evidence',4,
 "A city reported that collisions at intersections fell by a third in the year after it "
 "repainted the crossings and added countdown timers. Officials attributed the fall to the "
 "changes.",
 'Which finding, if true, would most strengthen the officials attribution?',
 ['Collisions at comparable intersections in the same city that were not altered held steady over the same year',
  'Pedestrian volumes at the altered intersections were similar before and after the changes',
  'Drivers surveyed after the changes said the countdown timers were easy to understand',
  'The repainting and the timers were installed at the same time as one another'],
 "A control set of intersections holding steady removes the possibility that something citywide produced the fall.",
 "Stable volumes help but are weaker, driver comprehension is self-report, and simultaneous installation makes the two changes harder to separate.")
q('SR278','rw_ii','Command of Evidence',3,
 "A historian argued that the printed pamphlets of the 1640s reached readers well below the "
 "class that bought books, on the grounds that the pamphlets were cheap.",
 'Which finding, if true, would most directly support the historian claim?',
 ['Inventories of the period record pamphlets among the possessions of labourers and servants',
  'The number of pamphlets printed in the 1640s exceeded the number printed in the previous decade',
  'Pamphlets of the period were printed on lower quality paper than bound books were',
  'Booksellers in London stocked pamphlets alongside bound volumes'],
 "Pamphlets appearing in the inventories of labourers and servants is direct evidence of who owned them.",
 "Volume, paper quality and shop stocking all bear on supply rather than on who read them.")
q('SR279','rw_ii','Command of Evidence',3,
 "Ecologists proposed that the decline of a bee species in the region followed the loss of a "
 "single plant it depends on for early spring forage, rather than pesticide use.",
 EVID,
 ['In the two districts where the plant remains common, the bee has declined far less than elsewhere in the region',
  'Pesticide use in the region has risen over the period in which the bee declined',
  'The bee visits several plant species over the course of a season',
  'The plant in question has declined across the whole of the region'],
 "A gradient in the bee's decline that follows the plant's presence, within the same region, separates the two candidate causes.",
 "Rising pesticide use supports the rival, seasonal breadth weakens the dependence claim, and a uniform decline in the plant leaves nothing to compare.")
q('SR280','rw_ii','Command of Evidence',4,
 "A company reported that customers who downloaded its mobile application spent 40 percent "
 "more per year than customers who did not, and concluded that the application increases "
 "spending.",
 'Which finding, if true, would most seriously weaken the conclusion?',
 ['Customers who already spent the most were the most likely to download the application when it launched',
  'The application allows customers to track a delivery and to reorder a previous purchase',
  'Downloads of the application rose steadily over the year the comparison covers',
  'Customers who downloaded the application contacted customer service less often'],
 "If the heaviest spenders were the ones who downloaded, the spending gap predates the application and is not produced by it.",
 "Features, download growth and service contacts are consistent with the conclusion being true or false.")
q('SR281','rw_ii','Command of Evidence',3,
 "A conservator proposed that the varnish on the painting was applied long after the paint "
 "itself, rather than by the artist as a final layer.",
 EVID,
 ['The varnish lies over a layer of surface dirt that could only have accumulated over years of display',
  'The varnish has yellowed to a degree typical of resins of the period',
  'The painting was in a private collection for most of the nineteenth century',
  'Varnishing a finished painting was standard studio practice at the time'],
 "Dirt between the paint and the varnish places the varnish after a period of exposure, which is exactly the claim.",
 "Yellowing dates the resin, collection history is context, and standard practice supports the rival account.")
q('SR282','rw_ii','Command of Evidence',3,
 "Researchers argued that the people buried in the cemetery came from several different "
 "regions rather than from a single local community.",
 EVID,
 ['Oxygen isotope ratios in the tooth enamel of the individuals fall into three groups matching three separate water sources',
  'The graves contain objects made in several different styles',
  'The cemetery was in use over a period of at least two hundred years',
  'The individuals show a range of ages at death from infancy to old age'],
 "Tooth enamel records the water drunk in childhood, so three isotope groups means three childhood locations.",
 "Object styles travel by trade, long use and a normal age range are expected of any cemetery.")
q('SR283','rw_ii','Command of Evidence',4,
 "A study of a reading programme reported that participating schools improved more than "
 "non-participating schools over two years. A reviewer questioned whether the programme "
 "caused the difference.",
 'Which finding, if true, would most directly address the reviewer question?',
 ['Schools were assigned to participate by lottery from among those that applied',
  'The programme was delivered by teachers already employed at each school',
  'Participating schools reported that the programme was straightforward to run',
  'The two groups of schools were similar in size and in the subjects they offered'],
 "A lottery among applicants makes the two groups alike in everything including the unmeasured things, which is what the reviewer is asking about.",
 "Delivery, ease of use and similarity on two measured characteristics leave selection on unmeasured ones open.")
q('SR284','rw_ii','Command of Evidence',3,
 "A geologist argued that the boulders scattered across the plain were carried there by ice "
 "rather than by a flood.",
 EVID,
 ['The boulders bear parallel scratches of the kind produced by being dragged beneath a moving ice sheet',
  'The boulders are composed of a rock type that outcrops several hundred kilometres away',
  'The plain lies at a lower elevation than the terrain to the north of it',
  'Deposits of fine sediment overlie the boulders across much of the plain'],
 "Glacial striations are a signature of transport beneath ice and not of transport by water.",
 "Distant origin, low elevation and overlying sediment are consistent with either mechanism.")

# ============================================================ Inferences
q('SR285','rw_ii','Inferences',3,
 "Penguins have no external ears and cannot see a chick in a crowd of thousands. A returning "
 "adult calls from the edge of the colony and waits. Chicks respond to the call of their own "
 "parent and to no other, and playback experiments show that a chick answers a recording of "
 "its parent made before it hatched. The recognition therefore cannot ______",
 INFER,
 ['depend on having heard the call after hatching.',
  'involve any sound the parent makes on returning.',
  'be shared by any other species of seabird.',
  'operate reliably in a colony of several thousand.'],
 "A chick answering a recording made before it hatched cannot have learned that call after hatching.",
 "The call is the cue, no other species is discussed, and the colony size is where recognition is said to work.")
q('SR286','rw_ii','Inferences',4,
 "Restoration of a historic building must choose a moment to restore it to. A cathedral "
 "altered in every century of its existence has no original state, only states. A restorer "
 "who removes the eighteenth century work to expose the medieval fabric is not recovering "
 "the building as it was; she is ______",
 INFER,
 ['selecting one of its states and discarding another.',
  'reversing damage that occurred after the building was completed.',
  'returning the building to the condition its builders intended.',
  'preserving the fabric that has survived longest without alteration.'],
 "If there is no original state but a series of states, removing one layer to show another is a choice among them.",
 "The text denies that later work is damage or that an intended condition exists, and the medieval fabric has itself been altered.")
q('SR287','rw_ii','Inferences',3,
 "A firm's quarterly report shows revenue rising and cash falling. The two can move apart "
 "because revenue is recorded when a sale is agreed and cash arrives when the customer pays. "
 "A firm growing quickly by selling on credit will therefore show ______",
 INFER,
 ['healthy revenue while its cash position deteriorates.',
  'falling revenue alongside an improving cash position.',
  'revenue and cash moving together over the same quarter.',
  'no reported revenue until its customers have paid.'],
 "Selling on credit records revenue at once and receives cash later, so growth widens the gap in exactly this direction.",
 "The other options reverse the mechanism or deny the accounting rule the text states.")
q('SR288','rw_ii','Inferences',3,
 "Antibiotic resistance genes have been recovered from bacteria in permafrost sealed for "
 "thirty thousand years, long before any clinical use of antibiotics. Antibiotics are "
 "produced by soil organisms competing with one another, and resistance to them is "
 "correspondingly old. Clinical use did not create resistance; it ______",
 INFER,
 ['selected for genes that were already present in the population.',
  'introduced resistance genes into species that had never carried them.',
  'reduced the number of resistant organisms in soil environments.',
  'made resistance genes detectable for the first time.'],
 "If the genes predate clinical use by thirty thousand years, use can only have favoured what was already there.",
 "Introduction is ruled out by the ancient genes, reduction reverses the effect, and detectability is not what clinical use changed.")
q('SR289','rw_ii','Inferences',4,
 "An index that ranks universities by the salaries of their graduates will rank highest the "
 "institutions that admit the students most likely to earn well. Since admission is "
 "competitive and correlated with family income, an institution could add nothing to its "
 "students and still top the ranking. To measure what an institution contributes, a ranking "
 "would have to ______",
 INFER,
 ['compare outcomes with what the same students would have earned elsewhere.',
  'exclude graduates who enter the highest-paying professions.',
  "weight salaries by the cost of living in the graduate's region.",
  'restrict the comparison to institutions of a similar size.'],
 "Contribution is the difference the institution makes, which requires a counterfactual for the same students.",
 "Excluding professions, adjusting for cost of living and matching on size all leave selection in place.")
q('SR290','rw_ii','Inferences',3,
 "Bicycle helmet laws are followed by fewer head injuries among cyclists and by fewer "
 "cyclists. Where the number of riders falls, the number of injuries falls whether or not "
 "any individual is safer. A study reporting only the total number of head injuries before "
 "and after such a law therefore cannot distinguish ______",
 INFER,
 ['a change in risk per rider from a change in the number of riders.',
  'injuries sustained by cyclists from injuries sustained by pedestrians.',
  'the effect of the law from the effect of improvements in helmet design.',
  'head injuries from injuries to other parts of the body.'],
 "A total with no denominator moves with either the rate or the exposure, and the text names both.",
 "Pedestrians, helmet design and injury site are other confusions and are not what a missing denominator produces.")
q('SR291','rw_ii','Inferences',3,
 "Wind turbines are placed where the wind is strong, and the strongest winds in many "
 "countries are offshore or on high ground far from cities. Electricity loses a fraction of "
 "its energy in every kilometre of transmission. A country choosing turbine sites is "
 "therefore trading ______",
 INFER,
 ['generation at the windiest site against losses in reaching the demand.',
  'the cost of turbines against the cost of the land they stand on.',
  'onshore construction against the difficulty of offshore maintenance.',
  'peak output against the reliability of output over a whole year.'],
 "The text names two facts: the best wind is far away, and distance costs energy. The tradeoff follows from those two.",
 "Land cost, maintenance and reliability are all real considerations the text does not raise.")
q('SR292','rw_ii','Inferences',4,
 "A museum that displays only objects in good condition will show a past that looks better "
 "made than it was. Objects survive in good condition partly because they were made well and "
 "partly because they were used little, and an object used little was often one that was "
 "kept rather than worked. A visitor drawing conclusions about ordinary life from such a "
 "display is therefore likely to ______",
 INFER,
 ['generalise from objects that were not typical of daily use.',
  'underestimate the skill of the craftsmen who made the objects.',
  'assume that the objects were more numerous than they actually were.',
  'conclude that the objects on display were recently manufactured.'],
 "The text says the surviving objects were often kept rather than used, so generalising from them generalises from the unrepresentative.",
 "Skill is overestimated rather than under, and numbers and dating are not what the selection distorts.")
q('SR293','rw_ii','Inferences',3,
 "Every account of the siege comes from the besiegers. The defenders left no written record, "
 "and the accounts that survive describe their conduct at second hand, from outside the "
 "walls, by people with a reason to describe it in a particular way. A historian using these "
 "accounts to establish what the defenders believed is ______",
 INFER,
 ['relying on inference from a source with an interest in the answer.',
  'using the only contemporary evidence that historians regard as reliable.',
  'departing from the accepted chronology of the siege.',
  'assuming that the defenders were literate.'],
 "The sources are external and interested, so any statement about the defenders' beliefs is an inference drawn from them.",
 "Reliability is what the passage questions, chronology is not raised, and literacy is what the defenders are said to lack.")
q('SR294','rw_ii','Inferences',3,
 "Species counts in tropical forests rise with the area surveyed and keep rising: a plot ten "
 "times larger yields more species, and one a hundred times larger more again, with no sign "
 "of a plateau at any area yet sampled. A published figure for the number of species in such "
 "a forest is therefore best read as ______",
 INFER,
 ['a statement about the area that was surveyed.',
  'an overestimate produced by counting the same species twice.',
  'a figure that will fall as identification improves.',
  'a count that is accurate for the forest as a whole.'],
 "If the count keeps rising with area and never plateaus, the figure reported is a property of the plot rather than of the forest.",
 "Double counting, improved identification and accuracy for the whole are each ruled out or unsupported by the rising curve.")
q('SR295','rw_ii','Inferences',4,
 "The recipe for Roman concrete was recovered by analysing surviving structures. Those "
 "structures are the ones still standing after two thousand years, which is a sample "
 "selected on the outcome the analysis is trying to explain. Roman builders who used a worse "
 "mix left buildings that ______",
 INFER,
 ['are not available to be analysed.',
  'were repaired with a better mix at a later date.',
  'have been analysed and found to differ little.',
  'were built for less demanding purposes.'],
 "Selecting on survival means the failures are absent from the sample, which is the point the middle sentence makes.",
 "Repair, analysis and purpose are possibilities the passage does not assert and none of them follows from selection on survival.")
q('SR296','rw_ii','Inferences',3,
 "A language with no written tradition changes without leaving a record of the change. "
 "Reconstructing its earlier form depends on comparing it with related languages and working "
 "backwards from the differences. The reconstruction is therefore ______",
 INFER,
 ['a hypothesis constrained by the languages that survive.',
  'a transcription of a form that was once written down.',
  'more reliable than reconstructions based on written sources.',
  'impossible for any language without a writing system.'],
 "Working backwards from surviving relatives yields a proposal shaped by what those relatives preserve.",
 "Nothing was written, no reliability comparison is made, and the passage describes a method rather than declaring the task impossible.")

q('SR297','rw_ii','Central Ideas and Details',3,
 "Kintsugi repairs broken pottery with lacquer mixed with powdered gold, so that the breaks "
 "are the most visible thing about the finished piece. The technique is often described as "
 "celebrating imperfection. It is better described as refusing to pretend: the bowl was "
 "broken, the break is part of what the bowl now is, and concealing it would make the object "
 "a claim about its own history.",
 MAIN,
 ['A repair technique is better understood as declining to hide a history than as celebrating flaws',
  'Kintsugi produces objects that are more valuable than unbroken pottery of the same kind',
  'Lacquer mixed with powdered gold is the strongest available material for repairing ceramics',
  'Japanese craft traditions generally place a high value on imperfection'],
 "The text sets the usual description against its own, which is about not pretending rather than about celebrating.",
 "Value, material strength and a general claim about Japanese craft are not what the text argues.")
q('SR298','rw_ii','Central Ideas and Details',4,
 "The standard against which a clock is measured has changed four times. A day was once "
 "defined by the sun, then by the earth's rotation measured against the stars, then by the "
 "earth's orbit, and since 1967 by the frequency of a transition in a caesium atom. Each "
 "change was made because the previous standard was found to vary against something more "
 "regular, and the regularity was discovered using the clock the standard defined.",
 MAIN,
 ['Each standard of time was replaced after a clock built to it revealed its own irregularity',
  'The caesium standard adopted in 1967 is the most accurate ever devised',
  'The rotation of the earth is not regular enough to serve as a standard of time',
  'Standards of measurement are revised whenever a more convenient one becomes available'],
 "The last sentence states the pattern: the irregularity was found using the clock the standard itself defined.",
 "Accuracy, the earth's rotation and convenience are each part of the account rather than the account.")
q('SR299','rw_ii','Inferences',3,
 "Insurance works by pooling risks that are independent of one another: one house burning "
 "down tells you nothing about the next. Flood risk is not independent, because a flood "
 "affects every house on the same plain at once. A private insurer covering flood in one "
 "region therefore faces ______",
 INFER,
 ['the possibility that every policy it holds pays out in the same year.',
  'claims that are smaller on average than those from fire.',
  'a lower cost of capital than an insurer covering fire.',
  'customers who are less likely to renew their policies.'],
 "Correlated risk means the claims arrive together, which is exactly what pooling is meant to prevent.",
 "Claim size, cost of capital and renewal are not what correlation implies.")
q('SR300','rw_ii','Inferences',4,
 "An algorithm trained on the hiring decisions a company made in the past will reproduce the "
 "pattern of those decisions, including any part of the pattern the company would not "
 "defend. Removing the applicant's name and photograph does not remove the pattern, because "
 "other fields in the application correlate with the same characteristics. Auditing such a "
 "system for fairness therefore requires ______",
 INFER,
 ['examining the outcomes it produces rather than the fields it was given.',
  'retraining the system on decisions made by a different company.',
  'removing every field that could correlate with a protected characteristic.',
  'confirming that the training decisions were made by more than one person.'],
 "If the pattern survives the removal of the obvious fields, only the outputs can show whether it is still there.",
 "Retraining elsewhere imports another pattern, removing every correlated field is what the text says is not achievable, and the number of deciders is beside the point.")
q('SR301','rw_ii','Command of Evidence',3,
 "A team proposed that the settlement was abandoned because of drought rather than conflict.",
 EVID,
 ['Tree ring records from the valley show fifteen consecutive dry years ending in the decade the settlement was abandoned',
  'The settlement contains no defensive wall or ditch of any period',
  'Pottery at the site is of types found across the region at the same date',
  'The settlement was rebuilt on the same spot two centuries later'],
 "A documented drought coinciding with abandonment supplies the mechanism and the timing the claim needs.",
 "Absent defences are weak negative evidence, and the pottery and the later rebuilding do not bear on why it was left.")
q('SR302','rw_ii','Command of Evidence',3,
 "Researchers argued that the increase in reported food allergies over two decades reflects "
 "a real increase rather than better recognition.",
 EVID,
 ['Rates of anaphylaxis requiring hospital admission, which are recorded in the same way throughout, rose by a comparable proportion',
  'General practitioners now receive more training in the recognition of food allergy than they did',
  'Parents report food allergy in their children more often than clinical testing confirms it',
  'Public awareness of food allergy has risen sharply over the same period'],
 "Hospital anaphylaxis is recorded consistently and does not depend on recognition, so a parallel rise in it supports a real increase.",
 "Training, over-reporting and awareness all support the rival account that recognition changed.")
q('SR303','rw_ii','Central Ideas and Details',2,
 "A cochlear implant does not amplify sound. It converts sound into electrical pulses "
 "delivered directly to the auditory nerve, bypassing the hair cells that a hearing aid "
 "relies on. People who receive one describe the first weeks as learning to interpret a "
 "signal that resembles speech without being the sound they remember.",
 MAIN,
 ['An implant substitutes a new signal for hearing rather than making existing hearing louder',
  'Cochlear implants are more effective than hearing aids for most forms of hearing loss',
  'The hair cells of the inner ear are responsible for converting sound into nerve signals',
  'Most recipients of a cochlear implant recover their original hearing within weeks'],
 "The text says the implant bypasses the hair cells and delivers a signal recipients must learn to read.",
 "No comparison of effectiveness is made, the hair cells are background, and the text says the signal is not the remembered sound.")
q('SR304','rw_ii','Inferences',3,
 "A bridge is designed to carry a load several times the heaviest it will meet. The margin "
 "covers uncertainty in the load, in the material and in the workmanship. An engineer who "
 "learns the material is stronger than assumed has not gained capacity to spend; the margin "
 "was never an estimate of strength but ______",
 INFER,
 ['an allowance for what is not known about the structure.',
  'a requirement imposed by the authority that approved the design.',
  'a measure of how much heavier the traffic is expected to become.',
  'the difference between the design load and the collapse load.'],
 "The text lists three uncertainties the margin covers, so it is an allowance for ignorance rather than a store of strength.",
 "Regulation, traffic growth and the arithmetic definition each describe something else about the margin.")
q('SR305','rw_ii','Command of Evidence',4,
 "A study reported that neighbourhoods with more street trees have lower rates of "
 "prescription for antidepressants, and the authors suggested that trees improve mental "
 "health.",
 'Which finding, if true, would most seriously weaken the suggestion?',
 ['Street trees are planted and maintained at a rate that rises with the average income of a neighbourhood',
  'Residents of neighbourhoods with more street trees report spending more time outdoors',
  'The species planted vary considerably between the neighbourhoods studied',
  'Antidepressant prescription rates have risen across the whole city over the study period'],
 "Income predicts both tree planting and prescribing, so a common cause would produce the association without trees doing anything.",
 "Time outdoors is a possible mechanism, species vary harmlessly, and a citywide rise affects both groups.")
q('SR306','rw_ii','Central Ideas and Details',3,
 "A fungus growing in the Oregon forest covers nearly ten square kilometres and is a single "
 "organism by the test biologists apply: every part of it is genetically identical and "
 "connected. Whether that test is the right one is disputed, since the connections are "
 "threads a metre underground and severing them would leave the parts alive and unchanged.",
 MAIN,
 ['A very large fungus counts as one organism on the accepted test, and the test itself is contested',
  'The fungus growing in the Oregon forest is the largest organism yet discovered',
  'Genetic identity is not a reliable way of distinguishing one organism from another',
  'Severing the underground threads of a fungus would kill the parts it connects'],
 "The text states the test, reports that the fungus meets it, and says the test is disputed for a stated reason.",
 "Size ranking is not claimed, the text reports rather than endorses the objection, and it says the parts would survive.")
q('SR307','rw_ii','Inferences',4,
 "A drug trial that stops early because an interim analysis shows benefit reports a larger "
 "effect than the same trial run to completion would have. The rule for stopping is a "
 "threshold on the observed difference, and a difference crosses it soonest when random "
 "variation happens to be running in the drug's favour. Published effect sizes from trials "
 "stopped early are therefore ______",
 INFER,
 ['biased upward by the condition that caused the trial to stop.',
  'less precise than those from trials that ran to completion.',
  'unrelated to the true effect of the treatment studied.',
  'the most useful available guide to how a drug will perform.'],
 "Stopping when the observed difference is largest selects on a fluctuation, which inflates the reported effect.",
 "Precision is a separate property, the effect is not unrelated to the truth, and the last option reverses the conclusion.")
q('SR308','rw_ii','Command of Evidence',3,
 "A curator argued that the manuscript was copied in a scriptorium that produced books for "
 "sale rather than for a monastic library.",
 EVID,
 ['The parchment is ruled for a fixed number of lines per page and the hand is uniform throughout, both signs of work produced to a specification',
  'The manuscript contains the text of a work that was widely read in the period',
  'The binding was replaced in the eighteenth century and is of no help in dating it',
  'The initials are decorated in a style found in several surviving books of the region'],
 "Ruling to a fixed specification and a uniform hand are marks of production to order rather than of a house copying for itself.",
 "Popularity, a replaced binding and a regional decorative style say nothing about the purpose of production.")

q('SR309','rw_ii','Inferences',3,
 "A recipe scaled from four servings to forty does not work by multiplying every quantity by "
 "ten. Heat reaches the centre of a large pan more slowly, liquid evaporates from a wide "
 "surface faster, and salt distributes through a larger mass less evenly. A cook scaling up "
 "is therefore adjusting for ______",
 INFER,
 ['effects that depend on the size of the vessel rather than on the ratio of ingredients.',
  'differences in the quality of ingredients bought in larger quantities.',
  'the preferences of a larger and more varied group of diners.',
  'the additional time required to prepare a greater number of servings.'],
 "All three examples are consequences of the pan's dimensions rather than of the proportions, which is what the cook must correct for.",
 "Ingredient quality, diner preference and preparation time are real issues the text does not raise.")
q('SR310','rw_ii','Central Ideas and Details',3,
 "The Antarctic ozone hole recovered because the Montreal Protocol was negotiated when three "
 "conditions happened to hold at once: the chemistry was understood, a substitute for the "
 "banned compounds already existed, and the compounds were made by a small number of firms "
 "in a small number of countries. Agreements on other pollutants have had none of those "
 "advantages.",
 MAIN,
 ['An environmental agreement succeeded under conditions that later problems have not shared',
  'The Montreal Protocol is the most effective environmental treaty ever negotiated',
  'Understanding the chemistry of a pollutant is the key to regulating it successfully',
  'Substitutes for harmful compounds are usually available before they are banned'],
 "The text lists three favourable conditions and says other agreements have had none of them.",
 "No ranking is offered, chemistry is one of three conditions, and the availability of substitutes is presented as fortunate rather than usual.")
q('SR311','rw_ii','Command of Evidence',3,
 "Researchers proposed that the pigment on the figurines was applied after firing rather "
 "than before.",
 EVID,
 ['The pigment survives only in recesses and is absent from the raised surfaces that a fired coating would have kept',
  'The pigment is a mineral available within a few kilometres of the site',
  'Figurines of the same type from other sites carry no pigment at all',
  'The clay body of the figurines was fired at a temperature typical of the period'],
 "A coating applied before firing would bond across the whole surface; one applied after sits loose and survives only where it is sheltered.",
 "Local pigment, unpigmented examples elsewhere and firing temperature do not distinguish the two sequences.")
q('SR312','rw_ii','Inferences',4,
 "Two firms bidding for the same contract each know their own costs and not the other's. A "
 "firm that bids its true cost wins nothing, since a rival with the same costs and a smaller "
 "margin will undercut it; a firm that bids far below its cost wins and loses money. The "
 "bid a firm submits is therefore ______",
 INFER,
 ['a guess about the rival as much as a statement about its own costs.',
  'the lowest price at which it could complete the work without loss.',
  'determined mainly by the size of the contract on offer.',
  'identical to the bid the rival will submit under the same conditions.'],
 "Both failure modes described depend on where the rival bids, so the submitted number has to incorporate an estimate of that.",
 "The break-even price is what bidding truthfully means, contract size is not discussed, and identical bids are not implied.")
q('SR313','rw_ii','Central Ideas and Details',2,
 "Guide dogs are trained to disobey. A dog led toward a kerb by a handler who has "
 "misjudged the traffic is expected to stop and to resist the command, a behaviour trainers "
 "call intelligent disobedience. Teaching it takes longer than teaching any single command, "
 "because the dog must learn when a rule it has been taught does not apply.",
 MAIN,
 ['Guide dogs are taught to override a command when following it would be dangerous',
  'Guide dogs are trained more slowly than other kinds of working dog',
  'Handlers of guide dogs frequently misjudge the traffic at a kerb',
  'Dogs are capable of learning a larger number of commands than is generally supposed'],
 "The text names the behaviour, gives the example and explains why it is hard to teach.",
 "No comparison with other working dogs is made, handler error is the example, and the number of commands is not the subject.")
q('SR314','rw_ii','Inferences',3,
 "A river that has been straightened moves water downstream faster. Faster water reaches the "
 "next town sooner and arrives in a narrower peak rather than spread over a day. "
 "Straightening a channel to protect one settlement therefore ______",
 INFER,
 ['transfers part of the problem to the settlements below it.',
  'reduces the total volume of water the river carries in a flood.',
  'lowers the peak flow at every point along the channel.',
  'has no effect on the timing of a flood further downstream.'],
 "Faster water in a narrower peak arriving downstream is a worse flood for the places downstream.",
 "Volume is unchanged, the peak downstream rises rather than falls, and the timing plainly changes.")
q('SR315','rw_ii','Command of Evidence',4,
 "A city reported that a programme placing social workers alongside police on mental health "
 "calls reduced arrests on such calls by half. A council member asked whether the programme "
 "or the selection of calls produced the result.",
 'Which finding, if true, would most directly address the council member question?',
 ['Calls were routed to a paired team or to police alone according to which team was free, not according to the nature of the call',
  'Social workers on the programme had at least five years of experience before joining it',
  'The number of mental health calls the city received did not change over the period',
  'Arrests on other kinds of call fell slightly over the same period'],
 "Assignment by availability rather than by the nature of the call removes the possibility that easier calls went to the paired teams.",
 "Experience, call volume and a small general fall do not settle how calls were assigned.")
q('SR316','rw_ii','Central Ideas and Details',3,
 "The Dewey Decimal system assigns a number to every subject, and the numbers are nested: a "
 "subject that is a subdivision of another gets a longer number beginning with the same "
 "digits. The scheme therefore encodes a claim about how knowledge is organised, and a "
 "subject that does not sit under any existing heading has to be given a number under one "
 "that does not fit.",
 MAIN,
 ['A classification scheme built on nesting commits itself to a structure that later subjects may not fit',
  'The Dewey Decimal system is no longer used by most large research libraries',
  'Numbers in the Dewey system are assigned in the order in which subjects were recognised',
  'Library users find nested classification numbers difficult to interpret'],
 "The text explains the nesting, says it encodes a claim about structure, and gives the consequence for a subject that does not fit.",
 "Usage, order of assignment and user difficulty are not claims the text makes.")
q('SR317','rw_ii','Inferences',3,
 "A photograph of a crowd taken with a long exposure shows the people who stood still and "
 "not the people who moved. Nineteenth century street photographs, which required exposures "
 "of several minutes, show empty boulevards with the occasional figure: a man having his "
 "boots polished, a woman waiting. The streets were not empty; the photographs record ______",
 INFER,
 ['only those who held still long enough to register.',
  'a time of day when few people were about.',
  'the parts of the street that were best lit.',
  'scenes that the photographers had arranged in advance.'],
 "A long exposure registers the stationary and loses the moving, which the examples of a boot polish and a wait illustrate.",
 "Time of day, lighting and staging are alternative explanations the text does not support.")
q('SR318','rw_ii','Command of Evidence',3,
 "A linguist argued that the two dialects diverged before the region was settled from the "
 "north rather than after.",
 EVID,
 ['Both dialects preserve a sound change that the northern speech had already completed before the settlement',
  'Speakers of the two dialects can understand one another without difficulty',
  'The two dialects share most of their vocabulary for farming and weather',
  'Written records of the region begin two centuries after the settlement'],
 "A change completed in the north before settlement, and present in both, would have to have arrived with the settlers or earlier, which dates the divergence relative to it.",
 "Mutual intelligibility, shared vocabulary and the start of the written record do not fix the order.")
q('SR319','rw_ii','Central Ideas and Details',4,
 "Standard accounts of the Industrial Revolution begin with cotton, because cotton is where "
 "the machinery was. Wool was the larger industry throughout, and it mechanised slowly, for "
 "a reason that has more to do with fibre than with invention: wool fibres are irregular and "
 "break under the tension a power loom applies, and the machines that worked on cotton did "
 "not work on wool until they were substantially redesigned.",
 MAIN,
 ['A familiar account begins with cotton because the technology did, not because cotton was the larger trade',
  'Wool was more important than cotton to the British economy of the nineteenth century',
  'Power looms were incapable of weaving wool under any conditions',
  'Mechanisation in the textile industry depended on advances in metalworking'],
 "The text says accounts begin with cotton because the machinery was there, notes that wool was larger, and explains the delay by the fibre.",
 "The text says wool was larger throughout without ranking economic importance, says the looms were redesigned rather than incapable, and does not mention metalworking.")
q('SR320','rw_ii','Inferences',3,
 "An index fund holds every company in a market in proportion to its size, and charges "
 "almost nothing to do so. An active fund selects, and charges for the selection. Across any "
 "period, the holdings of all investors together are the market, so the average actively "
 "managed dollar earns the market return before costs and ______",
 INFER,
 ['less than the market return after them.',
  'more than the index fund after costs in most periods.',
  'the same as the index fund once costs are included.',
  'a return that cannot be compared with the index.'],
 "If the average active dollar earns the market return before costs, subtracting higher costs leaves it below the market.",
 "The other options contradict the arithmetic the passage sets out.")


# ---------------------------------------------------------------------------
# LIFT: how many distractors on each item are carried past the key. See the note in
# bank_emit.py for why one per item is not the fix, and INC-0069 for what a bank that
# was never corrected at all looks like from the student's side.
LIFT = {
 'SR234': [('the Fuji series was produced late in the artist', ' working life, after he had changed his name many times'),
           ('changing names was common among artists of the period', ' and of the generation before it'),
           ('trace the development of an artist through the names he adopted', ' over the course of his career')],
 'SR236': [('summarise the argument that Silent Spring advanced about pesticides', ' and their effect on birds'),
           ('describe the response the book received from the chemical industry', ' in the year it appeared'),
           ('argue that popular science writing should include full references', ' to its sources as a matter of course')],
 'SR238': [('describe the engineering achievement that the Erie Canal represented', ' for its period'),
           ('compare freight costs before and after the canal was completed', ' between Buffalo and New York'),
           ('establish when the Erie Canal opened and what it cost to build', ' in the years before 1825')],
 'SR239': [('praise the neutrality of an online encyclopedia on contested subjects', ' of every kind that it covers'),
           ('describe the rules that Wikipedia editors are required to follow', ' whenever two of them disagree about an edit'),
           ('criticise the sources that contested Wikipedia articles rely on', ' for their claims about the subject under discussion')],
 'SR240': [('argue that the waggle dance does not carry information about food sources', ' at all'),
           ('describe the experiments by which the meaning of the dance was determined', ' in the first place'),
           ('explain how bees locate flowers in the absence of a communicative signal', ' from the hive')],
 'SR242': [('marks are the most reliable evidence about medieval building', ' that has come down to us from the period'),
           ('argue that the designers of Gothic cathedrals can now be identified by name', ' from the surviving records'),
           ('describe the system by which medieval masons were paid for their work', ' during the years they worked on a cathedral site')],
 'SR243': [('argue that mouse models should no longer be used in drug development', ' at any stage of it'),
           ('report the proportion of drugs that fail when tested in human trials', ' after succeeding in mice'),
           ('describe the biological differences between mice and human beings', ' that bear on drug response')],
 'SR244': [('recommend that archaeologists search systematically for unrecorded roads', ' rather than finding them by accident'),
           ('describe the methods by which the Roman army constructed military roads', ' across the provinces'),
           ('argue that local Roman roads were more extensive than military ones', ' in the provinces where both are known')],
 'SR245': [('the plagiarism accusation was the decisive factor in Larsen', ' long silence after her second novel'),
           ('establish the sequence of events in the later life of a novelist', ' who stopped publishing'),
           ('compare Larsen', ' own career with the careers of the novelists who were her contemporaries')],
 'SR246': [('standardized tests are more expensive than teacher assessment', ' to administer at scale'),
           ('agreeing that tests measure badly and proposing that they be improved', ' before they are used again'),
           ('denying that teacher assessment varies with what teachers expect', ' of the students in front of them')],
 'SR248': [('mistaken, because long possession does convert a taking into a valid title', ' in the end'),
           ('unnecessary, since museums have already returned the objects it concerns', ' to their places of origin'),
           ('inconsistent with the practice of the museums that have adopted it', ' as a matter of policy')],
 'SR249': [('arguing that output in fact fell in most of the trials Text 1 describes', ' rather than holding steady'),
           ('proposing a different length of working week than Text 1 considers', ' for the firms in the trials'),
           ('claiming that reported wellbeing is too subjective to be evidence', ' of anything a firm should act on')],
 'SR252': [('Whether readers prefer biographies that discuss motive to those that do not', ' discuss it at all'),
           ('Whether biographers are capable of knowing what their subjects intended', ' at the time they acted'),
           ('Whether the deeds of a subject can be established with certainty', ' from the surviving record')],
 'SR253': [('disputes the accuracy of the test scores on which Text 1 relies', ' for its comparison'),
           ('argues that the gap Text 1 reports has not held for six years', ' as Text 1 claims it has'),
           ('explains why charter schools are oversubscribed in the city', ' that Text 1 describes')],
 'SR254': [('attribution as a scholarly question with attribution as a commercial one', ' of the same canvas'),
           ('the quality of a painting with the fame of the painter who made it', ' in the first place'),
           ('documentary evidence with the physical evidence of the canvas', ' and the paint on it')],
 'SR255': [('denies that willows recovered along the streams during the decade in question', ' at all during the decade'),
           ('argues that beaver colonies were the cause of the decline in elk browsing', ' along the stream banks of the park'),
           ('reports a measurement programme that settled the question Text 1 raises', ' about the willows and the elk')],
}
LIFT.update({
 'SR256': [('argue that the modern conception of robots is mistaken about their origins', ' in a Czech play of the 1920s'),
           ('summarise the plot and reception of an influential Czech play of the 1920s', ' and the coinage it left behind in English')],
 'SR257': [('argues that hospitals should not be required to publish mortality rates', ' at all'),
           ('establishes that risk adjustment has made published rates more accurate', ' than they were')],
 'SR258': [('argue that the navy was mistaken not to build the system described in the patent', ' at the time it was filed'),
           ('describe the technical operation of frequency hopping in modern telephones', ' and in other wireless devices')],
 'SR260': [('establish the audience for which a fourteenth century cookbook was written', ' and how it was used'),
           ('describe the methods by which medieval cooks measured ingredients', ' and timed their cooking')],
 'SR261': [('Coral polyps are unable to survive without the algae that live inside their tissue', ' for any appreciable length of time'),
           ('Warming water destroys the calcium carbonate skeletons that coral polyps build', ' over a period of many years')],
 'SR262': [('Fishing fleets worked the Grand Banks for four centuries without affecting the stock', ' they depended on'),
           ('Catches on the Grand Banks have risen steadily since the moratorium took effect', ' in the year 1992')],
 'SR263': [('Scientific papers of the period were written only by men who owned the specimens described', ' in the papers themselves'),
           ('Ichthyosaurs and plesiosaurs were the most significant fossil discoveries of the period', ' made anywhere in Britain')],
 'SR264': [('A starter maintained for many years contains the original organisms it began with', ' when it was made'),
           ('Lactic acid bacteria prevent other microorganisms from growing in flour', ' of any kind at all')],
 'SR265': [('The committee that assembled the Voyager record worked under an unreasonable deadline', ' of six weeks'),
           ('Copyright law prevented the Voyager record from including any popular music', ' of the period at all')],
 'SR266': [('Commercial hunting was responsible for the entire decline of the passenger pigeon', ' across the whole of North America'),
           ('Birds that nest in colonies are more vulnerable to hunting than solitary birds', ' of about the same size')],
 'SR267': [('Napoleon III preferred aluminium tableware to silver for reasons of prestige', ' rather than of cost'),
           ('The Hall-Heroult process was the first method capable of isolating aluminium', ' from its compounds')],
 'SR268': [('The Board of Longitude was established to encourage solutions to a navigational problem', ' of long standing'),
           ('fourth clock was substantially smaller than the three that preceded it', ' in his workshop')],
 'SR269': [('Navigators require charts on which a constant bearing appears as a straight line', ' across the whole width of the chart'),
           ('All map projections distort either area or angle and none preserves both', ' at the same time as one another')],
 'SR270': [('Reducing traffic in city parks restores the bird populations that noise displaced', ' from them in earlier years'),
           ('Traffic noise in cities prevents birds of many species from breeding successfully', ' in urban parks of any size')],
})
LIFT.update({
 'SR272': [('Patients given a placebo recover as fully as patients given an active drug', ' in most trials of this kind')],
 'SR273': [('The song sung by an eastern Australian population changed substantially from one year to the next',
            ', both in its themes and in the order in which they were sung by the whales')],
 'SR274': [('The tools are of a type found at sites across the region throughout the period in question', ' and afterwards')],
 'SR275': [('Participants reported higher job satisfaction than non-participants at the end of the programme', ' that they had chosen to join')],
 'SR276': [('The ring encloses an area comparable to that of other enclosures known from the region', ' and from the same period of occupation')],
 'SR277': [('Pedestrian volumes at the altered intersections were similar before and after the changes', ' to the crossings were carried out')],
 'SR279': [('Pesticide use in the region has risen over the period in which the bee declined', ' across the whole of it, on every crop')],
 'SR280': [('The application allows customers to track a delivery and to reorder a previous purchase', ' in a single step')],
})
E.permute(I)
E.extend(I, LIFT, 'LIFT')
E.check_lift(I, E.lift_counts(LIFT))

HEADER = '''// bank_sat_rw6.js - Original digital SAT Reading and Writing items SR201-SR320.
//
// Generated by src/mk_bank_sat_rw6.py. Edit that file, not this one.
//
// The last thin pair on the SAT. Craft and Structure held 46 items and Information and
// Ideas 48, against 113 to 127 for the four Math domains and the two other Reading and
// Writing ones. These 120, sixty of each, take them to 106 and 108.
//
// Shape follows the College Board specification: a passage of roughly 25 to 150 words
// followed by one question with four choices, drawn from literature, history and social
// studies, the humanities, and science. Subtypes are the six the existing SAT banks use,
// with Words in Context and Central Ideas and Details the most numerous and Cross-Text
// Connections the fewest, since a cross-text item costs two passages.
//
// On the length tell: the key was the longest option on 68 of the 120 as written. Eight
// of those are vocabulary items, where a clause cannot be appended to a single word and
// the fix is a longer distractor of the same register; the rest are corrected by LIFT,
// which carries a chosen number of distractors past the key item by item. See INC-0069
// for what a reading bank written before any of this existed looks like from the
// student's side: bank_sat_rw.js shipped at 88 percent longest is key.
'''

E.measure(I)
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_sat_rw6.js',
        HEADER, [], I, 'BANK_SAT_RW6', group_key='sub')
