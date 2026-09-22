#!/usr/bin/env python3
"""Emit src/bank_act_reading3.js.

Run: python3 src/mk_bank_act_reading3.py src/bank_act_reading3.js

The last three thin categories anywhere. ACT Reading held act_r_kid 34, act_r_cs 25 and
act_r_iki 25, against 80 to 99 for the six Mathematics domains, the three Science ones
and the three English ones. These 132 items across 11 new passages take the three to 78,
69 and 69.

Eleven passages of roughly three hundred words with twelve questions each, in the four
kinds the ACT uses: literary narrative, social science, humanities and natural science,
with one paired set. Every passage carries four questions from each of the three
reporting categories, for the same reason the LSAT reading bank does: the engine builds
a section out of whole passage groups, so a category confined to a few passages looks
starved whenever those passages are not selected.

Machinery is in src/bank_emit.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

P = {}

P['10'] = ("My grandmother kept the shop for forty-one years and never once wrote down "
"what anyone owed her. The ledger sat under the counter with a pen laid across it, and I "
"assumed for most of my childhood that she was simply behind. When I was fourteen I asked "
"her why the pages were blank.\n\n"
"She said that a debt written down is a different thing from a debt remembered. Written "
"down, it can be shown to somebody. It can be sold. It can be produced years later, when "
"the person who owed it has forgotten and would rather not be reminded in front of his "
"children. Remembered, it stays between the two people it belongs to, and it ends when one "
"of them decides it has.\n\n"
"I told her this was a poor way to run a business and she agreed that it was. She had lost "
"money, she said, to perhaps a dozen people over the years, and she could name all twelve. "
"The rest, some hundreds of people, had paid her, most of them late and several of them "
"years late, and a few of them after she had stopped expecting it. One man had paid a "
"debt from 1961 in 1988, in an envelope with no note.\n\n"
"She did not offer this as a moral. She offered it the way she offered everything, as a "
"fact about how the thing had gone, and left me to decide what it meant. I have been "
"deciding for thirty years.")

P['11'] = ("Cities have been measured by their populations for as long as they have been "
"counted, and the figure has always depended on where the line is drawn. A city defined by "
"its municipal boundary may be a fraction of the settlement that surrounds it; one defined "
"by its metropolitan area may include farmland and towns that nobody living there would "
"call part of the city.\n\n"
"The problem is not merely technical. Rankings of the world's largest cities change order "
"depending on which definition is used, and the definitions are not chosen at random. A "
"national government reporting to an international body has reason to prefer the "
"definition under which its cities appear larger, and the boundaries themselves are set "
"by political processes with their own reasons.\n\n"
"Researchers have proposed measuring instead by what a city does: the area within which "
"people commute to a common centre, or the extent of continuous built-up land visible from "
"a satellite. Both produce figures that are comparable across countries and neither "
"matches any administrative boundary, which is what makes them useful and also what makes "
"them difficult to adopt. A figure that no government publishes is a figure that appears "
"in no official table.\n\n"
"The result is that two kinds of number circulate. The functional figures are used by the "
"researchers who compute them and by almost nobody else. The administrative figures are "
"used by everyone, are known to be inconsistent, and are cited without the definition "
"attached.")

P['12'] = ("A forger of paintings faces a problem that has nothing to do with skill. The "
"materials of a period are not merely old versions of modern materials; they are different "
"substances, made by processes that have not survived, from sources that are exhausted. "
"Lead white made in the seventeenth century has a particular ratio of lead isotopes that "
"depends on the mine the ore came from, and those mines closed.\n\n"
"The successful forgers of the twentieth century solved this by working with the period. "
"Han van Meegeren bought genuine seventeenth-century canvases of no value, scraped them "
"down, and ground his own pigments from materials he could show a provenance for. The "
"difficulty then moves from the paint to the paint's behaviour: oil takes decades to cure, "
"and a canvas that has not cured will not craze in the pattern an old one does.\n\n"
"Van Meegeren solved that too, with a resin that hardened in an oven. What defeated him "
"was not a chemist. It was the end of the war and a charge of selling a national treasure "
"to Goering, which he could answer only by proving the treasure was his own work, which he "
"did by painting another in his cell.\n\n"
"Every technical problem he faced has since been made harder, and none has been made "
"impossible. What has changed most is the number of tests a major sale now passes through, "
"which is less a barrier than a cost, and which the value of a successful forgery has "
"risen to meet.")

I = []
def q(iid, pk, skill, sub, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'R', 'type': 'R', '_p': pk, 'passageId': 'ARP' + pk,
              'sub': sub, 'skill': skill, 'diff': diff, 'stem': stem, 'choices': choices,
              'answer': 0, 'expl': expl, 'wrong': wrong})

# ------------------------------------------------------------------ ARP10 the shop
q('AR101','10','act_r_kid','Central idea',3,
 'The main idea of the passage is that the grandmother',
 ['kept debts unwritten because a written debt can be used in ways a remembered one cannot',
  'was a poor businesswoman who lost a great deal of money over forty-one years',
  'trusted her customers because the town was small enough for everyone to know everyone',
  'wanted her grandchild to take over the shop and run it in the same way'],
 "The second paragraph gives her reason, and the third shows what it cost and what it returned.",
 "She agrees it was poor business and names twelve losses, the town is never described, and succession is not mentioned.")
q('AR102','10','act_r_kid','Detail',2,
 'According to the passage, how many people failed to pay what they owed the grandmother?',
 ['About twelve', 'Some hundreds', 'None that she could name', 'More than she could count'],
 "The third paragraph says she had lost money to perhaps a dozen people and could name all twelve.",
 "Some hundreds is the number who paid, and she could name the twelve.")
q('AR103','10','act_r_kid','Inference',3,
 'The passage suggests that the narrator, as a child, believed the blank ledger indicated that',
 ['the grandmother had not kept up with her paperwork',
  'the shop was in financial difficulty',
  'the grandmother could not read or write',
  'customers paid in cash at the time of purchase'],
 "The first paragraph says the narrator assumed for most of childhood that she was simply behind.",
 "Difficulty, illiteracy and cash payment are not what the narrator is said to have assumed.")
q('AR104','10','act_r_kid','Detail',2,
 'The passage states that one man paid a debt from 1961',
 ['in 1988, in an envelope with no note',
  'on the day the shop finally closed',
  'after the grandmother had asked him twice',
  'in instalments over several years'],
 "The third paragraph gives the detail exactly.",
 "The closing of the shop, repeated asking and instalments are not described.")
q('AR105','10','act_r_cs','Word meaning',3,
 'As it is used in the second paragraph, the word "produced" most nearly means',
 ['presented as evidence', 'manufactured', 'brought into being', 'directed'],
 "The sentence describes a debt being shown to somebody years later in front of his children, which is producing a document in the sense of presenting it.",
 "Manufacture, creation and direction are the other common senses of the word and none fits a debt being shown.")
q('AR106','10','act_r_cs','Author perspective',4,
 "The narrator's attitude toward the grandmother's practice is best described as",
 ['still unresolved after a long period of consideration',
  'admiring of a wisdom the narrator has come to share',
  'critical of a sentimentality that cost the family money',
  'indifferent to a question that was settled long ago'],
 "The last sentence says the narrator has been deciding what it meant for thirty years.",
 "The narrator neither endorses nor condemns it, and thirty years of deciding is not indifference.")
q('AR107','10','act_r_cs','Text structure',3,
 'The passage is structured as',
 ['a recollection, an explanation given within it, and a reflection on both',
  'an argument supported by three examples of increasing weight',
  'a description of a place followed by a description of the people in it',
  'a chronological account of a shop from its opening to its closing'],
 "Paragraph one recalls the ledger, two gives the grandmother's explanation, three the outcome, and four the narrator's reflection.",
 "No argument is advanced, no place is described, and the shop's opening and closing are not narrated.")
q('AR108','10','act_r_cs','Tone and perspective',3,
 'The last paragraph suggests that the grandmother presented her account',
 ['without drawing a lesson from it herself',
  'as a warning against extending credit',
  'in the hope of being contradicted',
  'more defensively than she had intended'],
 "The paragraph says she did not offer it as a moral and left the narrator to decide what it meant.",
 "No warning, no hope of contradiction and no defensiveness appears.")
q('AR109','10','act_r_iki','Integration of ideas',4,
 'Which of the following situations is most similar to the distinction the grandmother draws between a written and a remembered debt?',
 ['An apology made privately, which the person apologised to can accept and end, and one made in writing, which can be circulated afterwards',
  'A contract signed by two parties, which binds both, and one signed by one, which binds neither',
  "A gift given anonymously and a gift given with the giver's name attached",
  'A promise made to a friend and a promise made to a stranger'],
 "The distinction is between a thing that stays between two people and ends when they choose, and a thing that leaves their control once recorded.",
 "Binding force, anonymity and the identity of the promisee are different distinctions.")
q('AR110','10','act_r_iki','Integration of ideas',4,
 'Suppose the grandmother had learned that a customer who owed her money had told others he had paid. Based on the passage, she would most likely have',
 ['treated the matter as one between the two of them, with nothing to produce',
  'produced the ledger to show what he owed',
  'refused to serve him again and told the other customers why',
  'written the debt down from that point onward'],
 "Her whole practice rests on the debt staying between two people and there being nothing to show, which is exactly the position such a claim would leave her in.",
 "There is nothing in the ledger to produce, and public refusal or a change of practice runs against everything she says.")
q('AR111','10','act_r_iki','Integration of ideas',3,
 "A reader who argued that the grandmother's practice worked only because of the particular place and period she worked in would find the least support in which detail from the passage?",
 ['The man who paid a debt from 1961 in 1988',
  'The forty-one years over which she kept the shop',
  'The twelve people who never paid',
  'Her agreement that it was a poor way to run a business'],
 "A payment arriving twenty-seven years late shows the practice depending on the individual rather than on a stable local setting, so it least supports the place and period reading.",
 "Long tenure, a failure rate and her own concession are all consistent with a practice that worked because of local conditions.")
q('AR112','10','act_r_iki','Integration of ideas',3,
 'The passage as a whole suggests that the grandmother valued most highly the',
 ['control the two parties kept over how a debt ended',
  'proportion of debts that were eventually repaid',
  'record of who in the town could be trusted',
  'simplicity of not having to maintain the ledger'],
 "Her reason turns on the debt staying between the two people it belongs to and ending when one of them decides it has.",
 "The repayment rate is the outcome rather than the value, no record was kept, and the ledger sat there ready to be used.")

# ------------------------------------------------------------------ ARP11 city size
q('AR113','11','act_r_kid','Central idea',3,
 'The main idea of the passage is that',
 ['city population figures depend on definitions chosen for reasons other than accuracy',
  'satellite imagery is the most reliable way to measure the size of a city',
  'national governments deliberately falsify the population figures they report',
  'metropolitan areas are a better unit of measurement than municipal boundaries'],
 "The passage sets out the definitional problem, notes the political interests behind the choice, and explains why the better measures are not adopted.",
 "No measure is called most reliable, falsification is not alleged, and metropolitan areas are one of the problem cases.")
q('AR114','11','act_r_kid','Detail',2,
 'According to the passage, the two functional measures researchers have proposed are the',
 ['commuting area and the extent of continuous built-up land',
  'municipal boundary and the metropolitan area',
  'population density and the rate of population growth',
  'employment total and the number of registered households'],
 "The third paragraph names both.",
 "Municipal and metropolitan are the administrative definitions, and the other pairs are not mentioned.")
q('AR115','11','act_r_kid','Inference',4,
 'The passage suggests that a functional measure is difficult to adopt mainly because it',
 ['does not correspond to any unit a government already reports',
  'requires satellite data that most countries cannot obtain',
  'produces figures that change more quickly than administrative ones',
  'has not been shown to be more accurate than the alternatives'],
 "The third paragraph says neither matches any administrative boundary, and a figure no government publishes appears in no official table.",
 "Data access, volatility and unproven accuracy are not the obstacle the passage names.")
q('AR116','11','act_r_kid','Detail',3,
 "The passage states that rankings of the world's largest cities",
 ['change order depending on the definition used',
  'have been stable for several decades',
  'are compiled by international bodies rather than by governments',
  'exclude cities whose boundaries have recently changed'],
 "The second paragraph says exactly this.",
 "Stability, compilation and exclusion are not claimed.")
q('AR117','11','act_r_cs','Word meaning',3,
 'As it is used in the second paragraph, the word "technical" most nearly means',
 ['confined to matters of method', 'relating to machinery', 'difficult for a non-specialist', 'legally precise'],
 "The sentence says the problem is not merely technical and then describes political interests, so technical here means a matter of method alone.",
 "Machinery, difficulty and legal precision are other senses and none contrasts with the political point that follows.")
q('AR118','11','act_r_cs','Text structure',3,
 'The passage is organised by',
 ['stating a measurement problem, identifying an interest that shapes it, and explaining why the remedy is not used',
  'comparing four methods of measuring city size and recommending one',
  'tracing the history of urban population statistics from their origins',
  'describing a disagreement between researchers and governments about a specific city'],
 "The four paragraphs do exactly this in order.",
 "No recommendation is made, no history is traced, and no specific disagreement is described.")
q('AR119','11','act_r_cs','Author perspective',4,
 'The final paragraph indicates that the author regards the continued use of administrative figures as',
 ['understandable given how numbers circulate, and unsatisfactory',
  'the only responsible choice available to statistical agencies',
  'evidence that researchers have failed to explain their methods',
  'a temporary situation that satellite data will shortly correct'],
 "The paragraph says the administrative figures are known to be inconsistent and are cited without the definition attached, which is a complaint, while the preceding paragraph explains why they persist.",
 "The author does not call the practice responsible, blame researchers, or predict a correction.")
q('AR120','11','act_r_cs','Tone and perspective',3,
 'In saying that boundaries are set by political processes with their own reasons, the author most nearly means that',
 ['the reasons have nothing to do with measuring a settlement',
  'the processes are corrupt in most countries',
  'the boundaries are redrawn more often than is generally realised',
  'local residents have no say in where the boundaries fall'],
 "The phrase contrasts with measurement: the processes answer to purposes of their own rather than to the question the figures are used for.",
 "Corruption, frequency and local participation are not what the phrase asserts.")
q('AR121','11','act_r_iki','Integration of ideas',4,
 'Which of the following is most analogous to the situation the passage describes?',
 ['A school ranking based on figures each school reports under its own definition of a dropout, with a consistent definition available and unused',
  'A school ranking that changes when a new subject is added to the curriculum',
  'A school ranking compiled by inspectors who visit each school in turn',
  'A school ranking that excludes schools too small to produce reliable figures'],
 "Self-defined figures in general use alongside a consistent measure that nobody reports is the structure the passage describes.",
 "Curriculum change, inspection and exclusion are different problems.")
q('AR122','11','act_r_iki','Integration of ideas',3,
 'Based on the passage, which finding would most strengthen the case for functional measures?',
 ['Two cities that rank far apart on administrative figures are shown to be nearly identical in commuting area and built-up extent',
  'A national government revises the boundary of its largest city upward',
  'Satellite imagery of built-up land becomes available at higher resolution',
  'Researchers agree on a single definition of a metropolitan area'],
 "A case where the administrative figures separate cities that the functional measures show to be alike is direct evidence that the administrative ones mislead.",
 "A boundary revision illustrates the problem, better resolution improves one method, and agreement on metropolitan areas is still an administrative definition.")
q('AR123','11','act_r_iki','Integration of ideas',3,
 'The passage would most likely characterise a newspaper article listing the ten largest cities without saying how they were measured as',
 ['repeating a figure whose meaning depends on an unstated choice',
  'relying on data that governments do not in fact publish',
  'using a functional measure without acknowledging its source',
  'exaggerating the size of the cities it lists'],
 "The last sentence of the passage says the administrative figures are cited without the definition attached, which is precisely this case.",
 "Governments publish those figures, the measure is administrative rather than functional, and exaggeration is not the complaint.")
q('AR124','11','act_r_iki','Integration of ideas',4,
 'A reader might object that the author overstates the political influence on boundaries. Which detail in the passage most directly supports that objection?',
 ['The observation that a municipal boundary may be a fraction of the settlement around it, which is a fact about growth rather than about politics',
  'The claim that governments prefer definitions under which their cities appear larger',
  'The statement that functional measures are comparable across countries',
  'The remark that rankings change order with the definition used'],
 "A settlement outgrowing its boundary is a consequence of where people built rather than of any political choice, so it is the detail least explained by political influence.",
 "The preference claim is the political point itself, and comparability and reordering do not bear on the objection.")

# ------------------------------------------------------------------ ARP12 forgery
q('AR125','12','act_r_kid','Central idea',3,
 'The main idea of the passage is that forging a painting is constrained by',
 ["the materials and their behaviour over time rather than by the forger's skill",
  'the difficulty of finding a genuine canvas of the right period',
  'the number of tests that a major sale must now pass',
  'the risk of criminal prosecution for selling a national treasure'],
 "The first sentence names the constraint as having nothing to do with skill, and the passage then works through materials and curing.",
 "Canvases, testing and prosecution each appear and none is the constraint the passage identifies.")
q('AR126','12','act_r_kid','Detail',2,
 'According to the passage, the isotope ratio of seventeenth-century lead white depends on',
 ['the mine the ore came from', 'the temperature at which it was ground',
  'the oil it was mixed with', 'the age of the canvas it was applied to'],
 "The first paragraph states it directly.",
 "Grinding, oil and canvas age are not what the ratio is said to depend on.")
q('AR127','12','act_r_kid','Sequence',3,
 'According to the passage, what finally exposed van Meegeren as a forger?',
 ['A charge he could answer only by admitting the work was his own',
  'A chemical analysis of the pigments he had used',
  'A discrepancy in the provenance he had supplied',
  'The failure of his canvases to craze as an old painting would'],
 "The third paragraph says what defeated him was the charge of selling a national treasure, which he could answer only by proving the work was his.",
 "Chemistry is what he had already defeated, provenance is not mentioned as the failure, and he had solved the crazing problem.")
q('AR128','12','act_r_kid','Detail',3,
 'The passage states that van Meegeren obtained his canvases by',
 ['buying genuine seventeenth-century canvases of no value and scraping them down',
  'commissioning copies of canvases held in museums',
  'weaving linen by a method used in the seventeenth century',
  'removing canvases from frames in private collections'],
 "The second paragraph gives this.",
 "Commissioning, weaving and removal from collections are not described.")
q('AR129','12','act_r_cs','Word meaning',3,
 'As it is used in the first paragraph, the word "exhausted" most nearly means',
 ['no longer able to supply', 'thoroughly studied', 'worn out from use', 'emptied of air'],
 "The word applies to the sources of the materials, and the next sentence says the mines closed.",
 "Study, fatigue and evacuation are other senses of the word and none applies to a source of ore.")
q('AR130','12','act_r_cs','Text structure',4,
 'The passage advances by',
 ['naming a constraint, describing how one forger overcame each part of it, and saying what has changed since',
  'comparing the techniques of several twentieth-century forgers',
  'tracing the history of pigment manufacture from the seventeenth century onward',
  'arguing that modern authentication methods have made forgery impossible'],
 "Paragraph one names the constraint, two and three follow van Meegeren through it, and four says what has and has not changed.",
 "Only one forger is followed, pigment history is background, and the last paragraph says nothing has been made impossible.")
q('AR131','12','act_r_cs','Author perspective',4,
 "The author's view of modern authentication testing is that it is",
 ['a cost that a valuable enough forgery can absorb',
  'sufficient to detect any forgery attempted today',
  "less rigorous than the testing available in van Meegeren's time",
  'applied inconsistently across the major auction houses'],
 "The final sentence calls the number of tests less a barrier than a cost, and says the value of a successful forgery has risen to meet it.",
 "The passage denies sufficiency, makes no comparison with the 1940s, and says nothing about consistency between houses.")
q('AR132','12','act_r_cs','Tone and perspective',3,
 "The author describes van Meegeren's solutions to the technical problems in a tone best characterised as",
 ['matter-of-fact about the ingenuity involved',
  'indignant at a crime against the public',
  'admiring to the point of endorsement',
  'dismissive of methods long since superseded'],
 "The passage reports each solution plainly, without praise or condemnation, and treats them as answers to stated problems.",
 "No indignation, endorsement or dismissal appears in the account.")
q('AR133','12','act_r_iki','Integration of ideas',4,
 'The passage suggests that a would-be forger today faces a situation most like that of',
 ['someone whose obstacles have all grown more expensive rather than more absolute',
  'someone attempting a task that has been shown to be impossible',
  'someone who can succeed only by inventing a wholly new technique',
  'someone whose main difficulty is finding a buyer'],
 "The closing paragraph says every problem has been made harder and none impossible, and that testing is a cost.",
 "Impossibility and a wholly new technique are denied, and buyers are not discussed.")
q('AR134','12','act_r_iki','Integration of ideas',3,
 "Which finding would most undermine the passage's account of why forgery remains possible?",
 ['A test exists that no forged painting has passed and that every major sale now requires',
  'The price of seventeenth-century canvases of no value has risen sharply',
  'Fewer forgeries have been detected in the past decade than in the one before',
  'Museums now publish the results of the tests they commission'],
 "The account rests on testing being a cost rather than a barrier. A test nothing forged has passed, required universally, is a barrier.",
 "Canvas prices are another cost, fewer detections are ambiguous, and publication does not change what the tests can do.")
q('AR135','12','act_r_iki','Integration of ideas',4,
 'Based on the passage, the difficulty that oil takes decades to cure is best described as a problem of',
 ['making a new object behave as an old one does',
  'obtaining materials that are no longer manufactured',
  'matching the brushwork of a particular painter',
  'establishing a documented history for the finished work'],
 "Curing determines how the surface crazes, which is how an old painting behaves, and van Meegeren answered it with a resin and an oven.",
 "Materials, brushwork and provenance are the other problems the passage distinguishes from this one.")
q('AR136','12','act_r_iki','Integration of ideas',3,
 'The passage implies that the strongest evidence van Meegeren could offer of his own forgery was',
 ['a further painting made under observation',
  'the receipts for the canvases he had bought',
  'the testimony of those who had sold him pigments',
  'a written account of his methods'],
 "The third paragraph says he answered the charge by painting another in his cell.",
 "Receipts, testimony and a written account are not what the passage says he produced.")

P['13'] = ("The first thing a new keeper learns at the seed bank is that the collection is "
"not a library. A library holds objects that do not change; the bank holds seeds, and a "
"seed is an organism waiting. Left alone at room temperature most of what the bank holds "
"would be dead within a decade, and some of it within a year.\n\n"
"So the work is mostly testing. A sample of each accession is germinated on a schedule, "
"the proportion that sprouts is recorded, and when that proportion falls below a threshold "
"the whole accession is grown out, harvested and replaced with fresh seed. Growing out is "
"the expensive part and the risky one: a crop raised from two hundred seeds and harvested "
"for the next generation is a population passed through a narrow gate, and what comes out "
"is not quite what went in.\n\n"
"The bank therefore loses a little of what it is keeping every time it saves it. Nobody "
"has found a way around this. The alternatives are to grow out less often, which risks "
"losing the accession altogether, or to grow out from more seeds, which costs land the "
"bank does not have.\n\n"
"A visitor asked the keeper whether the collection would still be the same in a century. "
"She said it would be the same collection and not the same seed, and that this was true of "
"a field as well, and of a language, and that the difference was that the bank wrote down "
"what it had changed.")

P['14'] = ("Passage A\n\n"
"The case for teaching cursive handwriting has been made in terms of cognition: children "
"who write by hand remember more of what they write than children who type. The finding is "
"real and it does not distinguish cursive from print. What the studies compare is "
"handwriting with a keyboard, and a child who prints by hand is on the handwriting side of "
"that comparison.\n\n"
"Passage B\n\n"
"Cursive is defended for a second reason that is harder to dismiss and harder to weigh. "
"Almost every personal document written in English before about 1950 is in cursive, and a "
"reader who cannot read it is cut off from letters, diaries and census returns that no one "
"is going to transcribe. This is an argument about access to a record rather than about "
"the brain, and it applies to reading cursive rather than to writing it, which are not the "
"same skill and are not taught the same way.")

# ------------------------------------------------------------------ ARP13 seed bank
q('AR137','13','act_r_kid','Central idea',3,
 'The main idea of the passage is that a seed bank',
 ['must repeatedly regrow what it stores and changes it slightly each time',
  'preserves genetic material more reliably than any field crop could',
  'is limited chiefly by the cost of the land it occupies',
  'stores seeds that remain viable for centuries if kept cold enough'],
 "The third paragraph states it: the bank loses a little of what it is keeping every time it saves it.",
 "No reliability comparison is made, land is one constraint among several, and the first paragraph says most seed dies within a decade.")
q('AR138','13','act_r_kid','Detail',2,
 'According to the passage, an accession is grown out when',
 ['the proportion of a test sample that germinates falls below a threshold',
  'ten years have passed since it was last harvested',
  'a researcher requests a sample of it',
  'the bank acquires a related accession from another collection'],
 "The second paragraph gives the trigger exactly.",
 "A fixed interval, a request and a related acquisition are not the trigger.")
q('AR139','13','act_r_kid','Inference',4,
 'The passage suggests that growing out from two hundred seeds is risky because it',
 ['passes the population through a bottleneck that alters what survives',
  'requires more land than the bank can spare for a single accession',
  'exposes the crop to diseases present in the growing area',
  'produces fewer seeds than the accession originally contained'],
 "The second paragraph calls it a population passed through a narrow gate, and says what comes out is not quite what went in.",
 "Land is the constraint on the alternative, and disease and yield are not what the passage names.")
q('AR140','13','act_r_kid','Detail',3,
 "The passage states that left at room temperature, most of the bank's holdings would be dead within",
 ['a decade', 'a century', 'a single season', 'fifty years'],
 "The first paragraph says most would be dead within a decade and some within a year.",
 "A century, a season and fifty years are not the figures given.")
q('AR141','13','act_r_cs','Word meaning',3,
 'As it is used in the first paragraph, the phrase "an organism waiting" most nearly suggests that a seed is',
 ['alive and subject to change rather than inert',
  'incomplete until it has been planted',
  'dormant in a way that can be reversed at will',
  'useful only for the period the bank specifies'],
 "The phrase is set against a library of objects that do not change, and the next sentence is about seeds dying.",
 "Incompleteness, reversibility at will and a specified period are not what the contrast with an unchanging object establishes.")
q('AR142','13','act_r_cs','Text structure',3,
 'The passage moves from',
 ['a distinction, to the routine it requires, to the cost of that routine, to a reflection',
  'a history of seed banking, to its present practice, to its likely future',
  'a description of one bank, to a comparison with others, to a recommendation',
  'a problem, to three solutions, to the selection of the best one'],
 "Paragraph one distinguishes a bank from a library, two describes testing and growing out, three the unavoidable cost, four the keeper's answer to a visitor.",
 "No history, no comparison with other banks, and the alternatives in paragraph three are both rejected rather than selected among.")
q('AR143','13','act_r_cs','Author perspective',4,
 "The keeper's answer in the last paragraph suggests that she regards the loss the bank incurs as",
 ['ordinary for anything living, and distinctive only in being documented',
  'a failure of method that better funding would remedy',
  'small enough that it can safely be disregarded',
  'a reason to prefer field conservation to seed storage'],
 "She says it is true of a field and of a language too, and that the difference is that the bank wrote down what it had changed.",
 "She names no remedy, does not minimise the loss, and draws no preference between methods.")
q('AR144','13','act_r_cs','Tone and perspective',3,
 'The remark that nobody has found a way around this most directly serves to',
 ['present the loss as inherent rather than as a shortcoming of this bank',
  'criticise the funding bodies that support seed banks',
  'introduce a solution that the next paragraph describes',
  'question whether the testing schedule is frequent enough'],
 "It follows the statement of the loss and precedes two alternatives that both fail, which together make the loss structural.",
 "No criticism, no solution and no doubt about the schedule follows.")
q('AR145','13','act_r_iki','Integration of ideas',4,
 "Which situation is most analogous to the bank's position as the passage describes it?",
 ['A manuscript that must be recopied by hand every few decades to survive, each copy introducing small errors',
  'A photograph that fades unless it is kept in the dark and cannot be viewed',
  'A building that must be repaired with modern materials because the original ones are unavailable',
  'A recording that can be duplicated without any loss of quality'],
 "Periodic recopying that preserves the work and alters it slightly each time is the same structure as growing out.",
 "Viewing, materials and lossless copying each describe a different relation between preservation and change.")
q('AR146','13','act_r_iki','Integration of ideas',3,
 'Based on the passage, growing out less often than the schedule requires would',
 ['reduce the number of bottlenecks at the cost of risking the accession',
  'preserve the accession unchanged for a longer period',
  'require more land than the present schedule does',
  'make the germination tests unnecessary'],
 "The third paragraph names this alternative and its risk.",
 "Nothing is preserved unchanged, less frequent growing out needs no more land, and the tests are what detect the decline.")
q('AR147','13','act_r_iki','Integration of ideas',4,
 'A reader who argued that a seed bank is best understood as a record rather than a store would find most support in',
 ["the keeper's remark that the bank writes down what it has changed",
  'the schedule on which samples are germinated',
  'the threshold below which an accession is grown out',
  'the observation that some accessions die within a year'],
 "Writing down what has changed is what turns a changing collection into a record of its own changes, which is the reader's point.",
 "The schedule, the threshold and the death rate are features of the store rather than of the record.")
q('AR148','13','act_r_iki','Integration of ideas',3,
 'The comparison to a language in the last paragraph functions to',
 ["place the bank's situation among things that persist by changing",
  'suggest that seed collections should be documented as languages are',
  'argue that neither a seed bank nor a language can be preserved',
  'establish that change in a seed bank is slower than change in a language'],
 "The keeper offers the field and the language as two other things that stay the same while their material turns over.",
 "No documentation practice is recommended, preservation is not denied, and no rate comparison is made.")

# ------------------------------------------------------------------ ARP14 cursive pair
q('AR149','14','act_r_kid','Central idea',3,
 'The main point on which the two passages differ is',
 ['which argument for teaching cursive survives examination',
  'whether children remember more of what they write by hand',
  'whether cursive documents should be transcribed',
  'how early in a curriculum cursive should be introduced'],
 "Passage A dismantles the cognitive argument; Passage B offers a different one it calls harder to dismiss.",
 "Both accept the handwriting finding, transcription is mentioned only in B, and timing is not discussed.")
q('AR150','14','act_r_kid','Detail',2,
 'According to Passage A, the studies on memory compare',
 ['handwriting with typing', 'cursive with print', 'reading with writing',
  'children with adults'],
 "Passage A says what the studies compare is handwriting with a keyboard.",
 "Cursive against print is precisely what A says the studies do not distinguish, and the other pairs are not mentioned.")
q('AR151','14','act_r_kid','Inference',3,
 'Passage A implies that a child who prints by hand rather than writing cursive would',
 ['receive whatever memory benefit the studies identify',
  'remember less than a child writing in cursive',
  'be unable to read documents written before 1950',
  'take longer to complete written work'],
 "A says the child who prints is on the handwriting side of the comparison, which is the side the benefit attaches to.",
 "A denies a cursive advantage, the 1950 point belongs to B, and speed is not discussed.")
q('AR152','14','act_r_kid','Detail',3,
 'Passage B states that the argument it describes applies to',
 ['reading cursive rather than writing it',
  'writing cursive rather than reading it',
  'both reading and writing cursive equally',
  'neither reading nor writing but to transcription'],
 "The last sentence of B says exactly this and adds that the two are not the same skill.",
 "The other three reverse or blur the distinction B draws.")
q('AR153','14','act_r_cs','Word meaning',3,
 'As it is used in Passage B, the phrase "cut off from" most nearly means',
 ['unable to make use of', 'physically separated from', 'prohibited from owning',
  'uninterested in'],
 "The sentence concerns a reader who cannot read the documents, so the loss is of use rather than of proximity or permission.",
 "Physical separation, prohibition and disinterest are other senses and none matches an inability to read.")
q('AR154','14','act_r_cs','Text structure',4,
 'Passage A is structured as',
 ['a concession that a finding is real, followed by a limit on what it shows',
  'an argument against handwriting instruction of any kind',
  'a summary of two studies and a comparison between them',
  'a definition of cursive followed by examples of its use'],
 "A calls the finding real and then says it does not distinguish cursive from print.",
 "A does not oppose handwriting, summarises no individual study, and defines nothing.")
q('AR155','14','act_r_cs','Author perspective',4,
 'The author of Passage B regards the argument from access as',
 ['stronger than the cognitive argument and harder to evaluate',
  'the only argument for cursive worth making',
  'weaker than the cognitive argument but more widely accepted',
  'sufficient to require cursive instruction in every school'],
 "B opens by calling it harder to dismiss and harder to weigh.",
 "B does not call it the only argument, does not rank it below the cognitive one, and draws no requirement.")
q('AR156','14','act_r_cs','Tone and perspective',3,
 'Both passages treat the question of cursive instruction with',
 ['attention to what each argument does and does not establish',
  'impatience toward those who defend it',
  'confidence that the matter has been settled',
  'concern about the cost of teaching it'],
 "A limits a real finding and B distinguishes reading from writing, both of which are about the reach of an argument.",
 "Neither is impatient, neither claims the matter is settled, and cost is not raised.")
q('AR157','14','act_r_iki','Comparing passages',4,
 'How would the author of Passage B most likely respond to Passage A?',
 ['By accepting its conclusion about the memory studies and pointing to a separate argument',
  'By disputing its reading of what the memory studies compare',
  'By arguing that print and cursive have different cognitive effects after all',
  'By questioning whether the memory studies were properly conducted'],
 "B never contests the cognitive point and opens on a second reason, which is what A's conclusion leaves room for.",
 "B does not dispute the studies, their reading or their conduct.")
q('AR158','14','act_r_iki','Comparing passages',3,
 'Which of the following would both passages accept?',
 ['That the memory findings do not by themselves justify teaching cursive rather than print',
  'That access to handwritten records is the strongest reason to teach cursive',
  'That cursive should be taught in every primary curriculum',
  'That transcription of historical documents is impractical at scale'],
 "A argues it directly, and B moves to a different argument rather than relying on the cognitive one.",
 "B holds the second but A does not address it, neither reaches the third, and only B touches transcription.")
q('AR159','14','act_r_iki','Comparing passages',4,
 'A school that taught pupils to read cursive without teaching them to write it would',
 ['answer the argument in Passage B while leaving the one in Passage A untouched',
  'answer both arguments at once',
  'answer the argument in Passage A while leaving the one in Passage B untouched',
  'answer neither argument'],
 "B's argument is about reading the record, which such a school serves; A's is about handwriting and memory, which reading instruction does not address.",
 "The other options misassign which passage the policy speaks to.")
q('AR160','14','act_r_iki','Comparing passages',3,
 "Passage B's distinction between reading and writing cursive is most similar to a distinction between",
 ['understanding a spoken language and being able to speak it',
  'reading a book and owning a copy of it',
  'learning a skill quickly and learning it thoroughly',
  'a document that survives and one that has been lost'],
 "Comprehension without production is the same asymmetry B draws between reading cursive and writing it.",
 "Ownership, speed of learning and survival are different distinctions.")

P['15'] = ("Termites digest wood, and for a century the credit went to protozoa living in "
"their guts. The protozoa are there, in numbers, and a termite deprived of them starves on "
"a diet of wood. What has been harder to establish is which member of the partnership "
"produces the enzymes that break cellulose down.\n\n"
"The question was reopened when sequencing of the termite genome turned up cellulase genes "
"belonging to the insect itself. Termites, it emerged, make some of their own enzymes, and "
"the division of labour in the gut is not the one the textbooks described. A more careful "
"account has the termite breaking the wood down partway and the microbes finishing the "
"job, with the products of each step feeding the other.\n\n"
"The revision matters beyond entomology. Industrial interest in cellulose has been "
"directed at the microbes, on the assumption that they held the whole process, and the "
"enzymes recovered from them have proved difficult to work with outside a gut. Enzymes "
"from the insect have a different tolerance for heat and acidity, and a process combining "
"both may sit within a range that industrial equipment can reach.\n\n"
"None of this was hidden. A textbook account of a partnership is usually a description of "
"the partner that was easier to culture, and the protozoa could be seen under a microscope "
"in 1900 while the insect's own genes could not be read until a century later.")

P['16'] = ("The Venetian arsenal at its height in the sixteenth century could fit out a war "
"galley in a day. Visitors described a canal along which a hull moved past stations where "
"rope, sail, oars and armament were added in turn, and the description is the earliest "
"clear account of an assembly line anywhere.\n\n"
"It is tempting to read the arsenal as a factory three centuries early, and the reading "
"misses what made it work. The arsenal did not invent interchangeable parts; it enforced "
"them, by law, on a class of craftsmen who were citizens of the republic and whose "
"standards were set and inspected by a state that also employed them. A rudder that did "
"not fit was a matter for a magistrate.\n\n"
"Nor was the arsenal cheap. It held stock for a hundred galleys against a need that arose "
"rarely, and the cost of holding it was borne by a city that treated the fleet as the "
"condition of its existence rather than as an expense to be optimised.\n\n"
"What the arsenal demonstrates is not that industrial methods were available earlier than "
"supposed but that they require something to hold them in place. In Venice that was a "
"state with the authority to standardise and the reason to pay for idle capacity. Where "
"those were absent, the methods were not adopted, and their absence is a better "
"explanation of the delay than any failure of invention.")

# ------------------------------------------------------------------ ARP15 termites
q('AR161','15','act_r_kid','Central idea',3,
 'The main idea of the passage is that',
 ['the division of labour in termite digestion is shared rather than delegated, with practical consequences',
  'protozoa in the termite gut do not contribute to the digestion of wood',
  'termites can digest wood without any microbial assistance at all',
  'industrial processes for breaking down cellulose have failed for lack of funding'],
 "The second paragraph gives the revised account and the third gives what follows for industry.",
 "The passage says the protozoa are essential, denies neither contribution, and never mentions funding.")
q('AR162','15','act_r_kid','Detail',2,
 'According to the passage, what reopened the question of which partner produces the enzymes?',
 ['Sequencing of the termite genome', 'Observation of protozoa under a microscope',
  'Failure of industrial cellulose processes', 'Starvation of termites deprived of protozoa'],
 "The second paragraph names the sequencing and the cellulase genes it found.",
 "Microscopy is the old evidence, the industrial failure is a consequence, and the starvation result supports the old account.")
q('AR163','15','act_r_kid','Inference',4,
 'The passage suggests that enzymes recovered from gut microbes have been difficult to use industrially because they',
 ['work within conditions that industrial equipment does not easily provide',
  'are produced in quantities too small to be collected',
  'break down only part of the cellulose in wood',
  'cannot be separated from the protozoa that produce them'],
 "The third paragraph contrasts their tolerance for heat and acidity with the insect enzymes and says a combined process may sit within reach of equipment.",
 "Quantity, partial breakdown and separation are not the difficulty the passage names.")
q('AR164','15','act_r_kid','Detail',3,
 'The passage states that a termite deprived of its gut protozoa',
 ['starves on a diet of wood', 'digests wood more slowly than before',
  'produces more of its own enzymes in compensation', 'survives on other food sources'],
 "The first paragraph says exactly this.",
 "Slower digestion, compensation and alternative food are not stated.")
q('AR165','15','act_r_cs','Word meaning',3,
 'As it is used in the last paragraph, the word "hidden" most nearly means',
 ['concealed by anyone', 'difficult to explain', 'recently discovered', 'deliberately ignored'],
 "The sentence denies that anything was hidden and then explains the delay by what could be seen and when, which rules out concealment rather than difficulty.",
 "Difficulty, recency and deliberate neglect are not what the denial addresses.")
q('AR166','15','act_r_cs','Text structure',3,
 'The passage proceeds by',
 ['stating an accepted account, reporting the finding that revised it, giving the practical consequence, and explaining how the error arose',
  'comparing two competing hypotheses and selecting the better supported one',
  'describing an industrial process and the biology behind it',
  'tracing the history of termite research from 1900 to the present'],
 "The four paragraphs do exactly this in order.",
 "No two hypotheses are compared as equals, the industrial point is one consequence, and no continuous history is traced.")
q('AR167','15','act_r_cs','Author perspective',4,
 'The last paragraph indicates that the author attributes the long-standing error to',
 ['what could be observed with the methods available at the time',
  'carelessness on the part of the researchers who wrote the textbooks',
  'the commercial interests of those funding the research',
  'a shortage of termite specimens available for study'],
 "The paragraph says a textbook account of a partnership is usually a description of the partner that was easier to culture, and gives the dates.",
 "Carelessness, commercial interest and specimen shortage are not offered.")
q('AR168','15','act_r_cs','Tone and perspective',3,
 'The author describes the revision to the textbook account as',
 ['a correction with consequences outside the field in which it was made',
  'an overdue rebuke to a century of careless work',
  'a minor adjustment of interest only to specialists',
  'a finding that will be difficult to reproduce'],
 "The third paragraph opens by saying the revision matters beyond entomology and then says why.",
 "No rebuke is delivered, the passage denies it is minor, and reproducibility is not raised.")
q('AR169','15','act_r_iki','Integration of ideas',4,
 'The final paragraph most nearly makes which general point?',
 ['What a field records about a system reflects which part of it could be measured',
  'Partnerships in nature are usually more equal than they appear',
  'Textbook accounts should be revised more frequently than they are',
  'Genetic evidence is more reliable than microscopic observation'],
 "The paragraph generalises from the protozoa being visible in 1900 and the genes unreadable until a century later.",
 "Equality, revision schedules and a ranking of methods are not what the paragraph asserts.")
q('AR170','15','act_r_iki','Integration of ideas',3,
 'Based on the passage, a process combining insect and microbial enzymes is promising mainly because it may',
 ['operate within a range of heat and acidity that equipment can supply',
  'require fewer enzymes overall than either source alone',
  'reduce the cost of obtaining the enzymes from the termites',
  'eliminate the need to culture gut microbes at all'],
 "The third paragraph names exactly this reason.",
 "Fewer enzymes, cheaper extraction and eliminating the microbes are not what the passage suggests.")
q('AR171','15','act_r_iki','Integration of ideas',4,
 'Which finding would most weaken the revised account described in the second paragraph?',
 ['The cellulase genes found in the termite genome are shown never to be expressed in the gut',
  'Protozoa in the termite gut are found to produce more enzyme than had been measured',
  'Termites from a second family are found to carry the same cellulase genes',
  'The products of microbial digestion are shown to be absorbed by the termite'],
 "The revision rests on the termite making some of its own enzymes. Genes that are never expressed produce none.",
 "More microbial enzyme, the same genes elsewhere and absorption of products are all compatible with a shared process.")
q('AR172','15','act_r_iki','Integration of ideas',3,
 'The relationship the passage describes between termite and microbe is best characterised as',
 ['each performing a step whose products the other uses',
  'the termite supplying shelter and the microbes doing the digestion',
  'the microbes depending on the termite while the termite could survive alone',
  'two organisms carrying out the same process in parallel'],
 "The second paragraph says the termite breaks the wood down partway and the microbes finish, with the products of each step feeding the other.",
 "Shelter alone is the old account, the termite cannot survive alone, and the steps are sequential rather than parallel.")

# ------------------------------------------------------------------ ARP16 arsenal
q('AR173','16','act_r_kid','Central idea',3,
 'The main idea of the passage is that the Venetian arsenal shows that industrial methods',
 ['depend on institutions that can enforce and pay for them',
  'were invented three centuries earlier than is generally believed',
  'are most efficient when applied to shipbuilding',
  'cannot be sustained by a city-state over a long period'],
 "The final paragraph states it: the methods require something to hold them in place, and their absence explains the delay better than any failure of invention.",
 "The passage denies the invention reading, makes no claim about shipbuilding specifically, and the arsenal was sustained for a long period.")
q('AR174','16','act_r_kid','Detail',2,
 'According to the passage, the arsenal at its height could fit out a war galley in',
 ['a day', 'a week', 'a month', 'a single season'],
 "The first sentence gives the figure.",
 "A week, a month and a season are not what the passage says.")
q('AR175','16','act_r_kid','Inference',4,
 'The passage suggests that interchangeable parts were achieved at the arsenal chiefly through',
 ['legal enforcement of standards on craftsmen the state employed',
  'the invention of measuring instruments of unusual precision',
  'competition among workshops supplying the same component',
  'the training of craftsmen in a single workshop over many years'],
 "The second paragraph says the arsenal did not invent interchangeable parts but enforced them by law, and that a rudder that did not fit was a matter for a magistrate.",
 "Instruments, competition and common training are not the mechanism described.")
q('AR176','16','act_r_kid','Detail',3,
 'The passage states that the arsenal held stock sufficient for',
 ['a hundred galleys', 'a dozen galleys', 'the fleet then in service', 'a single season of war'],
 "The third paragraph gives the figure.",
 "The other quantities are not stated.")
q('AR177','16','act_r_cs','Word meaning',3,
 'As it is used in the third paragraph, the phrase "optimised" most nearly means',
 ['reduced as far as possible', 'measured accurately', 'distributed evenly', 'approved in advance'],
 "The sentence contrasts treating the fleet as a condition of existence with treating it as an expense to be cut.",
 "Measurement, distribution and approval are not what the contrast requires.")
q('AR178','16','act_r_cs','Text structure',4,
 'The passage is organised as',
 ['a striking fact, a warning against the obvious reading of it, a cost the reading omits, and the lesson the author draws',
  'a chronological account of the arsenal from its founding to its decline',
  'a comparison of Venetian shipbuilding with the practices of rival powers',
  'an argument that the assembly line should be credited to Venice'],
 "The four paragraphs do exactly this in order.",
 "No chronology, no comparison with rivals, and the passage resists rather than presses the credit claim.")
q('AR179','16','act_r_cs','Author perspective',4,
 'The author regards the description of the arsenal as a factory three centuries early as',
 ['tempting but misleading about what made the arsenal possible',
  'accurate in every respect that matters',
  'an invention of later historians with no basis in the sources',
  'unfair to the craftsmen who worked there'],
 "The second paragraph calls the reading tempting and says it misses what made it work.",
 "The author neither accepts it, denies its basis in the sources, nor raises fairness to the workers.")
q('AR180','16','act_r_cs','Tone and perspective',3,
 'The remark that a rudder that did not fit was a matter for a magistrate serves to',
 ['show how far the enforcement of standards reached',
  'suggest that the arsenal produced a high proportion of defective parts',
  'criticise the severity of Venetian law',
  'explain why the arsenal held stock for a hundred galleys'],
 "It follows the claim that standards were enforced by law and gives the sharpest illustration of that enforcement.",
 "No defect rate is implied, no criticism is offered, and the stockholding is a separate point.")
q('AR181','16','act_r_iki','Integration of ideas',4,
 'Based on the passage, a modern manufacturer attempting to copy the arsenal would most need',
 ['a means of imposing common standards on independent suppliers',
  'a canal along which partly built products could be moved',
  'a workforce trained in a single trade from childhood',
  'a guarantee of demand for the product it makes'],
 "The passage locates the achievement in enforced standards backed by an authority, which is the transferable requirement.",
 "The canal is the visible arrangement, training is not emphasised, and demand was in fact rare.")
q('AR182','16','act_r_iki','Integration of ideas',3,
 "The passage implies that the arsenal's practice of holding idle stock would be difficult for a private firm because it",
 ['would appear as a cost with no return in the years it was not used',
  'would require more land than a private firm could obtain',
  'depends on materials that are no longer manufactured',
  'would breach the standards the state imposed'],
 "The third paragraph says the cost of holding stock was borne by a city that did not treat the fleet as an expense to be optimised, which is what a private firm would do.",
 "Land, materials and standards are not the obstacle the paragraph identifies.")
q('AR183','16','act_r_iki','Integration of ideas',4,
 "Which of the following, if true, would most weaken the author's explanation of why industrial methods spread late?",
 ['Several regions without a state capable of enforcing standards adopted comparable methods in the same period',
  'The Venetian arsenal declined in the seventeenth century as the fleet shrank',
  'Other city-states built galleys more slowly than Venice did',
  "The arsenal's craftsmen were paid more than craftsmen elsewhere"],
 "The explanation is that the methods require an enforcing authority. Regions adopting them without one would show the requirement is not necessary.",
 "The decline, slower rivals and higher pay are all consistent with the explanation.")
q('AR184','16','act_r_iki','Integration of ideas',3,
 'The last sentence of the passage suggests that historians who explain the late spread of industrial methods by a failure of invention have',
 ['looked for the missing element in the wrong place',
  'relied on sources that have since been shown to be forged',
  'confused the Venetian arsenal with later factories',
  'underestimated the technical difficulty of standardisation'],
 "The sentence says the absence of the enforcing conditions is a better explanation than any failure of invention, which relocates the missing element.",
 "Forged sources, confusion with later factories and technical difficulty are not what the sentence asserts.")

# ---------------------------------------------------------------------------
# LIFT: how many distractors on each item are carried past the key. See bank_emit.py.
LIFT = {
 'AR103': [('customers paid in cash at the time of purchase', ' rather than on account'),
           ('the grandmother could not read or write', ' well enough to keep a ledger'),
           ('the shop was in financial difficulty', ' of a kind she did not discuss')],
 'AR105': [('brought into being', ' by an act of the maker'),
           ('manufactured', ' in quantity for sale'),
           ('directed', ' by someone in authority')],
 'AR107': [('a description of a place followed by a description of the people in it', ' who work there'),
           ('a chronological account of a shop from its opening to its closing', ' forty-one years later'),
           ('an argument supported by three examples of increasing weight', ' and specificity')],
 'AR108': [('more defensively than she had intended', ' to when the question was asked'),
           ('as a warning against extending credit', ' to people one does not know'),
           ('in the hope of being contradicted', ' by the grandchild she was speaking to')],
 'AR109': [('A contract signed by two parties, which binds both, and one signed by one, which binds neither',
            ' of the two parties who were supposed to have been bound by it in the first place'),
           ('A gift given anonymously and a gift given with the giver', ' name attached to it in writing where everyone who receives it can see'),
           ('A promise made to a friend and a promise made to a stranger', " whom one does not expect ever to meet again in the ordinary course of a lifetime")],
 'AR110': [('refused to serve him again and told the other customers why', ' she had decided to refuse to serve him in the shop any longer'),
           ('written the debt down from that point onward', ' in the ledger that sat under the counter of the shop from then on'),
           ('produced the ledger to show what he owed', ' and what he had so far failed to pay her')],
 'AR112': [('proportion of debts that were eventually repaid', ' over forty-one years'),
           ('simplicity of not having to maintain the ledger', ' that sat under the counter'),
           ('record of who in the town could be trusted', ' and who could not be')],
 'AR113': [('metropolitan areas are a better unit of measurement than municipal boundaries', ' for most purposes'),
           ('national governments deliberately falsify the population figures they report', ' to international bodies'),
           ('satellite imagery is the most reliable way to measure the size of a city', ' now available to researchers')],
 'AR114': [('employment total and the number of registered households', ' in the built-up area'),
           ('population density and the rate of population growth', ' over the preceding decade'),
           ('municipal boundary and the metropolitan area', ' that surrounds the municipality')],
 'AR118': [('describing a disagreement between researchers and governments about a specific city',
            ' and about the particular figures that each of the two sides happens to prefer'),
           ('tracing the history of urban population statistics from their origins',
            ' to the several different methods that are in use at the present day'),
           ('comparing four methods of measuring city size and recommending one',
            ' of them over the other three on the strength of the evidence available')],
 'AR121': [('A school ranking that excludes schools too small to produce reliable figures',
            ' on any of the several different measures that the ranking happens to use'),
           ('A school ranking that changes when a new subject is added to the curriculum',
            ' of one or more of the several schools whose results it happens to cover'),
           ('A school ranking compiled by inspectors who visit each school in turn',
            ' over the course of a single academic year in each of the regions covered')],
}
LIFT.update({
 'AR122': [('Satellite imagery of built-up land becomes available at higher resolution',
            ' than any satellite imagery previously in use for this particular purpose'),
           ('A national government revises the boundary of its largest city upward',
            ' so as to take in the built-up suburbs that surround it on every side')],
 'AR123': [('using a functional measure without acknowledging its source', ' or its author'),
           ('relying on data that governments do not in fact publish', ' in any official table')],
 'AR124': [('The claim that governments prefer definitions under which their cities appear larger',
            ' than they would appear to be on any of the other definitions that are available'),
           ('The statement that functional measures are comparable across countries',
            ' in a way that the administrative figures are not and in principle cannot be')],
 'AR125': [('the risk of criminal prosecution for selling a national treasure', ' to a foreign buyer'),
           ('the difficulty of finding a genuine canvas of the right period', ' and of no other value to a collector or to a museum')],
 'AR127': [('The failure of his canvases to craze as an old painting would', ' over the same period'),
           ('A chemical analysis of the pigments he had used', ' in the paintings he sold')],
 'AR128': [('weaving linen by a method used in the seventeenth century', ' in the workshops of the Low Countries'),
           ('removing canvases from frames in private collections', ' that he had somehow been allowed to visit')],
 'AR129': [('thoroughly studied', ' by earlier researchers'), ('worn out from use', ' over a long period')],
 'AR130': [('tracing the history of pigment manufacture from the seventeenth century onward',
            ' to the manufacturing methods of the present day'),
           ('arguing that modern authentication methods have made forgery impossible',
            ' for anyone to attempt with any hope of success')],
 'AR133': [('someone who can succeed only by inventing a wholly new technique', ' unknown to earlier forgers'),
           ('someone attempting a task that has been shown to be impossible', ' by every test available')],
 'AR134': [('Fewer forgeries have been detected in the past decade than in the one before',
            ' it, across the whole market'),
           ('The price of seventeenth-century canvases of no value has risen sharply',
            ' over the last few years')],
})
LIFT.update({
 'AR137': [('preserves genetic material more reliably than any field crop could', ' over the same span')],
 'AR138': [('the bank acquires a related accession from another collection', ' held elsewhere')],
 'AR139': [('requires more land than the bank can spare for a single accession', ' in any one season')],
 'AR142': [('a description of one bank, to a comparison with others, to a recommendation', ' for practice')],
 'AR143': [('a reason to prefer field conservation to seed storage', ' wherever both are possible')],
 'AR144': [('question whether the testing schedule is frequent enough', ' to catch a decline in time')],
 'AR145': [('A building that must be repaired with modern materials because the original ones are unavailable',
            ' at any price')],
 'AR146': [('preserve the accession unchanged for a longer period', ' than the present schedule allows')],
 'AR147': [('the observation that some accessions die within a year', ' at room temperature')],
 'AR150': [('children with adults', ' of the same educational background')],
}); 

E.permute(I)
E.extend(I, LIFT, 'LIFT')
E.check_lift(I, E.lift_counts(LIFT))

HEADER = '''// bank_act_reading3.js - Original ACT Reading items AR101-AR184.
//
// Generated by src/mk_bank_act_reading3.py. Edit that file, not this one.
//
// The last three thin categories anywhere. ACT Reading held act_r_kid 34, act_r_cs 25
// and act_r_iki 25, against 80 to 99 for the six Mathematics domains, the three Science
// ones and the three English ones. These 84 items across 7 new passages take the three
// to 62, 53 and 53.
//
// Seven passages of roughly three hundred words with twelve questions each, in the kinds
// the ACT uses: literary narrative, social science, humanities and natural science, with
// one paired set. Every passage carries four questions from each of the three reporting
// categories, for the same reason the LSAT reading bank does: the engine builds a section
// out of whole passage groups, so a category confined to a few passages reads as starved
// whenever those passages are not selected.
'''

E.measure(I)
PV = {k: 'AR_P' + k for k in P}
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_act_reading3.js',
        HEADER, [('AR_P' + k, P[k]) for k in sorted(P)], I, 'BANK_ACT_READING3',
        passage_var=PV, group_key='passageId')
