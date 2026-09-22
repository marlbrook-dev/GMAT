#!/usr/bin/env python3
"""Emit src/bank_gre_rc3.js.

Run: python3 src/mk_bank_gre_rc3.py src/bank_gre_rc3.js

The last skill on any exam that is still well below its neighbours. GRE Reading
Comprehension holds 40 items against 91 to 95 for the other six GRE skills. These 54
take it to 94.

Sixteen passages in the two shapes the GRE uses: twelve short passages of one dense
paragraph carrying three questions each, and four longer ones carrying four or five.
Subtypes are the five the existing GRE banks use.

Machinery is in src/bank_emit.py; the length tell is corrected by LIFT and check_lift
fails the run if a clause was too short to move the item it names.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

P = {}

P['A'] = ("The claim that a market price aggregates the information held by its "
"participants is usually defended by pointing at prediction markets, where a price does "
"track the probability of an event more closely than most individual forecasts. The "
"defence proves less than it appears to. A prediction market has a settlement date and an "
"unambiguous resolution, which means a trader who is wrong finds out and pays. Markets in "
"which the question never resolves, or resolves decades later, have neither feature, and "
"the mechanism that is supposed to aggregate has nothing to work on.")

P['B'] = ("Readers who encounter the sonnets in the order in which they were printed take "
"that order to be authorial. There is no evidence that it is. The 1609 volume was "
"published, so far as anyone can establish, without the poet's involvement, and the "
"sequence it presents has the shape a publisher would give a manuscript found loose: the "
"poems that clearly belong together are together, and the rest are where they happened to "
"lie. A reader arguing from the sequence to the poet's intention is arguing from the only "
"artefact that survives to a fact it was never in a position to record.")

P['C'] = ("Ecologists distinguish between a species that is rare because it occupies a small "
"range and one that is rare because it occurs thinly across a large one. The distinction "
"is not academic: the first is vulnerable to a single event and the second is not, while "
"the second is vulnerable to a change in conditions across a whole region and the first "
"may not be. A conservation strategy written for one kind of rarity will protect the other "
"badly, and the word rare in a designation does not say which is meant.")

P['D'] = ("Historians of technology have long treated the water frame and the spinning jenny "
"as competing solutions to the same problem. They were not. The jenny multiplied what one "
"person could do by hand and could be worked in a cottage; the water frame required a "
"power source, and a power source required a building, a site on a river and a workforce "
"that came to the machine rather than the reverse. What looks in retrospect like a "
"technical contest was a choice between two arrangements of work, and the second won for "
"reasons that had as much to do with supervision as with output per spindle.")

P['E'] = ("The rise in measured intelligence test scores over the twentieth century, of "
"roughly three points a decade in every country with the data to check, is not disputed. "
"What it means is. The scores did not rise on every subtest: gains were largest on items "
"calling for abstract classification and smallest on those calling for arithmetic or "
"general knowledge. An account of the rise as a change in general ability has to explain "
"why it left the parts of the test most closely tied to schooling nearly untouched.")

P['F'] = ("The Roman census counted citizens, and historians have used its figures to "
"estimate the population of Italy. Two readings are possible. On one, the figures count "
"adult men, and the population of Italy in the first century was around four million. On "
"the other, they count men, women and children, and the population was around one million. "
"The difference is not a matter of precision but of what the word counted meant to the "
"people doing the counting, and the same figures support either reading without strain.")

P['G'] = ("A drug is approved on the strength of trials in the population that will "
"eventually take it, and the population that eventually takes it is rarely the population "
"in the trials. Trial participants are younger, take fewer other medicines, and have the "
"condition being treated and nothing else. The gap is well known and is usually described "
"as a limitation on how far the results generalise. It is better described as a limitation "
"on what the results are about: the trial establishes an effect in a population that, as a "
"population, does not receive the drug.")

P['H'] = ("It is often said that photography freed painting from the obligation to "
"represent. The chronology is against it. The turn away from representation began in "
"European painting decades before photography could record a moving subject or a colour, "
"and the painters most often cited as responding to the camera were working in genres, "
"landscape and portraiture, where the camera was for many years technically incapable of "
"competing. What the camera did quickly was to take over the commercial portrait trade, "
"which is a fact about the market for painters rather than about the theory of painting.")

I = []
def q(iid, pk, sub, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'V', 'type': 'RC', '_p': pk, 'passageId': 'GR3' + pk,
              'sub': sub, 'skill': 'gre_rc', 'diff': diff, 'stem': stem,
              'choices': choices, 'answer': 0, 'expl': expl, 'wrong': wrong})

q('GR101','A','Main idea',3,
 'The primary purpose of the passage is to',
 ['limit the reach of an argument by identifying the conditions its evidence depends on',
  'argue that prediction markets forecast events more accurately than individuals do',
  'establish that market prices never aggregate the information participants hold',
  'describe the settlement procedures used in prediction markets',
  'recommend that markets be designed with unambiguous resolution dates'],
 "The passage grants the prediction market evidence and then names the two features it depends on, which other markets lack.",
 "The accuracy claim is conceded, the passage does not say never, the procedures are the evidence, and no design recommendation is made.")
q('GR102','A','Inference',4,
 'The passage suggests that the aggregating mechanism it describes depends on',
 ['traders learning that they were wrong and bearing a cost for it',
  'the number of participants in the market being sufficiently large',
  'the question being one on which experts already agree',
  'prices being published continuously rather than at intervals',
  'participants having access to the same information'],
 "The passage names a settlement date and an unambiguous resolution, and explains their force as a trader who is wrong finding out and paying.",
 "Participant numbers, expert agreement, publication frequency and equal information are not what the passage identifies.")
q('GR103','A','Function of a sentence',3,
 'The reference to markets in which the question resolves decades later serves to',
 ['identify a case in which the proposed mechanism has nothing to operate on',
  'suggest that long-dated markets are more accurate than short-dated ones',
  'establish that most markets have no settlement date at all',
  'explain why prediction markets attract relatively few traders',
  'introduce an exception that the rest of the passage sets aside'],
 "It is one of the two cases named in the last sentence as lacking the features the mechanism requires.",
 "No accuracy claim, no prevalence claim, no explanation of participation and no set-aside exception appears.")

q('GR104','B','Main idea',3,
 'The passage is primarily concerned with',
 ['questioning an inference readers draw from the only surviving arrangement of a text',
  'establishing the date on which a volume of sonnets was first printed',
  'arguing that the sonnets were written in a different order from the one printed',
  'describing the practices of early seventeenth-century publishers',
  'identifying which of the sonnets clearly belong together'],
 "The last sentence names the error: arguing from the surviving artefact to a fact it could not record.",
 "The date and the publishing practices are premises, no alternative order is proposed, and the groupings are an example.")
q('GR105','B','Inference',4,
 "The passage implies that the printed sequence would be evidence of the poet's intention only if",
 ['the poet had some part in how the volume was arranged',
  'the manuscript had survived alongside the printed volume',
  'the poems that belong together had been separated in printing',
  "the volume had been printed during the poet's lifetime",
  'the publisher had recorded the order in which he received the poems'],
 "The passage says the volume was published without the poet's involvement, which is what removes the sequence as evidence of intention.",
 "A surviving manuscript, a different grouping, the date of printing and a publisher's record would not by themselves supply authorial arrangement.")
q('GR106','B','Function of a sentence',3,
 'The description of the sequence as having the shape a publisher would give a manuscript found loose functions to',
 ['offer an account of the order that requires no authorial decision',
  'suggest that the manuscript was damaged before it reached the printer',
  'establish that the publisher was working without any instructions',
  'question whether the poems in the volume are all by the same author',
  'explain why some of the sonnets are shorter than others'],
 "The clause supplies an alternative origin for the order, which is what undercuts reading it as intentional.",
 "Damage, instructions, authorship and length are not what the description asserts.")

q('GR107','C','Main idea',3,
 'The primary purpose of the passage is to',
 ['distinguish two conditions a single term covers and note the practical consequence',
  'argue that species with small ranges deserve greater conservation attention',
  'establish that most rare species occur thinly across large ranges',
  'describe the events that threaten species with restricted distributions',
  'propose a new term to replace rare in conservation designations'],
 "The passage sets out the two kinds of rarity, says a strategy for one protects the other badly, and notes that the designation does not distinguish them.",
 "Neither kind is given priority, no prevalence claim is made, the events are an illustration, and no new term is proposed.")
q('GR108','C','Inference',4,
 'Based on the passage, a species that occurs thinly across a continent is most vulnerable to',
 ['a change in conditions affecting the whole of its range at once',
  'the loss of the single site at which it breeds',
  'competition from a species with a more restricted range',
  'a reduction in the total area over which it is distributed',
  'an event that destroys a large fraction of one habitat'],
 "The passage says the second kind is vulnerable to a change in conditions across a whole region.",
 "A single site, competition and a localised event are the vulnerabilities of the other kind, and area reduction is not what the passage names.")
q('GR109','C','Detail',2,
 'According to the passage, the two kinds of rarity differ in that one species has',
 ['a small range while the other is thinly distributed across a large one',
  'a declining population while the other has a stable one',
  'few individuals while the other has many',
  'specialised habitat requirements while the other does not',
  'been recently designated while the other has not'],
 "The first sentence of the passage draws exactly this distinction.",
 "Trend, absolute numbers, specialisation and designation history are not the distinction given.")

q('GR110','D','Main idea',4,
 'The passage is primarily concerned with',
 ['reinterpreting a supposed technical contest as a choice between ways of organising work',
  'establishing that the water frame produced more yarn per spindle than the jenny',
  'describing the mechanical differences between two eighteenth-century machines',
  'arguing that the spinning jenny was the superior of the two inventions',
  'explaining why cottage production persisted longer than is usually supposed'],
 "The last sentence states it: the contest was a choice between two arrangements of work, decided partly by supervision.",
 "Output per spindle is what the passage says the outcome did not turn on, the mechanics are material, neither machine is preferred, and cottage persistence is not discussed.")
q('GR111','D','Inference',4,
 'The passage suggests that the water frame prevailed partly because it',
 ['brought workers to a single site where their work could be overseen',
  'produced yarn of a quality the jenny could not match',
  'could be operated by workers with less training',
  'required less capital to install than the jenny did',
  'was protected by a patent the jenny infringed'],
 "The passage says a power source required a building, a site and a workforce that came to the machine, and that supervision mattered as much as output.",
 "Quality, training, capital and patents are not among the reasons given.")
q('GR112','D','Function of a sentence',3,
 'The statement that the jenny could be worked in a cottage serves primarily to',
 ['mark the difference in organisation that the passage goes on to treat as decisive',
  'establish that the jenny was the cheaper of the two machines',
  'suggest that cottage workers resisted moving into factories',
  'explain why the jenny was invented before the water frame',
  'indicate that the jenny required no source of power at all'],
 "It is the first half of the contrast the passage builds between two arrangements of work.",
 "Cost, resistance, chronology and the power question are not what the clause is doing.")

q('GR113','E','Main idea',3,
 'The primary purpose of the passage is to',
 ['point to a pattern within a well established finding that any explanation of it must accommodate',
  'dispute the evidence that intelligence test scores rose during the twentieth century',
  'argue that intelligence tests measure schooling rather than ability',
  'establish that the rise in scores has now ceased in most countries',
  'compare the rate of the rise between countries with different school systems'],
 "The passage grants the rise, reports the uneven subtest pattern, and says an account as general ability must explain it.",
 "The rise is not disputed, the schooling claim is not made, and cessation and cross-country comparison are not discussed.")
q('GR114','E','Inference',4,
 'The passage implies that an explanation of the rise in terms of improved schooling would face the difficulty that',
 ['the gains were smallest on the subtests most closely tied to what schools teach',
  'the rise occurred at the same rate in countries with very different school systems',
  'the rise has been measured only in countries with universal schooling',
  'abstract classification is not taught in most school curricula',
  'arithmetic scores fell over the period in question'],
 "The passage says gains were smallest on arithmetic and general knowledge, which are the school-linked items.",
 "Cross-country rates, measurement coverage, the curriculum point and a fall in arithmetic are not what the passage reports.")
q('GR115','E','Detail',2,
 'According to the passage, the gains over the twentieth century were largest on items calling for',
 ['abstract classification', 'arithmetic', 'general knowledge', 'vocabulary', 'spatial rotation'],
 "The passage names abstract classification as the subtest with the largest gains.",
 "Arithmetic and general knowledge are named as the smallest, and vocabulary and spatial rotation are not mentioned.")

q('GR116','F','Main idea',3,
 'The passage is primarily concerned with',
 ['a disagreement about what a historical source was counting rather than about its accuracy',
  'the difficulty of estimating ancient populations from any surviving evidence',
  'establishing that the population of Italy in the first century was around four million',
  'the administrative procedures by which the Roman census was conducted',
  'the reasons historians have preferred one reading of the census figures'],
 "The last sentence says the difference is about what counted meant to the people doing the counting, and that the figures support either reading.",
 "The passage is about one source rather than the general problem, settles on no figure, and does not describe procedures or preferences.")
q('GR117','F','Inference',4,
 'The passage implies that the two readings of the census figures differ by a factor of roughly',
 ['four', 'two', 'ten', 'one and a half', 'twenty'],
 "Four million against one million is a factor of four.",
 "The other factors do not match the two figures the passage gives.")
q('GR118','F','Function of a sentence',4,
 'The final sentence serves primarily to',
 ['locate the disagreement in the meaning of the record rather than in its reliability',
  'concede that neither reading can be supported by the surviving evidence',
  'suggest that the census figures were recorded inaccurately at the time',
  'recommend that historians abandon the census as a source',
  'introduce a third reading that the passage goes on to develop'],
 "It says the difference is not a matter of precision but of what counted meant, which relocates the dispute.",
 "Both readings are said to be supportable, accuracy is not questioned, no abandonment is urged, and no third reading follows.")

q('GR119','G','Main idea',4,
 'The primary purpose of the passage is to',
 ['restate a known limitation as a claim about what a trial establishes rather than about how far it extends',
  'argue that drug trials should enrol participants who resemble the eventual patients',
  'describe the criteria by which participants are selected for drug trials',
  'establish that most approved drugs are less effective than their trials indicated',
  'question whether regulators should approve drugs on the basis of trial evidence'],
 "The last sentence says the gap is better described as a limitation on what the results are about.",
 "No recommendation about enrolment or approval is made, the criteria are material, and no claim about effectiveness is advanced.")
q('GR120','G','Inference',4,
 "The passage suggests that the population in which a drug's effect has been established is",
 ['one that, taken as a population, does not go on to receive the drug',
  'smaller than the population that eventually receives the drug',
  'selected at random from those with the condition being treated',
  'representative of the eventual patients in every respect but age',
  'the population regulators intend the approval to cover'],
 "The last clause of the passage states this directly.",
 "Size, randomisation, representativeness and regulatory intent are not what the passage asserts.")
q('GR121','G','Detail',2,
 'According to the passage, trial participants differ from eventual patients in that participants',
 ['are younger and take fewer other medicines',
  'are more likely to have been treated previously',
  'report their symptoms more accurately',
  'are drawn from a wider range of countries',
  'have more severe forms of the condition'],
 "The second sentence names younger, fewer other medicines, and the condition and nothing else.",
 "Previous treatment, reporting accuracy, geography and severity are not the differences given.")

q('GR122','H','Main idea',3,
 'The passage is primarily concerned with',
 ['arguing that the chronology does not support a familiar explanation of a change in painting',
  'establishing when photography became capable of recording colour and movement',
  'describing the effect of photography on the market for commercial portraits',
  'arguing that painting turned away from representation for purely internal reasons',
  'comparing the genres in which photographers and painters competed'],
 "The passage states the familiar claim, says the chronology is against it, and gives two reasons.",
 "The technical dates and the portrait market are the evidence, no internal explanation is offered, and no genre comparison is drawn.")
q('GR123','H','Inference',4,
 'The passage suggests that the effect of photography on painting was felt most directly in',
 ['the livelihoods of painters rather than in their aims',
  'landscape painting rather than in portraiture',
  'the technical methods painters used to prepare a canvas',
  'the training offered by academies of art',
  'the prices that collectors would pay for representational work'],
 "The last sentence says the camera took over the commercial portrait trade, which is a fact about the market for painters rather than about the theory of painting.",
 "Landscape is named as a genre the camera could not compete in, and methods, training and collector prices are not discussed.")
q('GR124','H','Strengthen and weaken',4,
 'Which of the following, if true, would most weaken the argument of the passage?',
 ['Painters in the genres named wrote at the time about abandoning representation because the camera had made it redundant',
  'Photography became capable of recording colour several decades later than the passage implies',
  'The turn away from representation accelerated after photography became widely available',
  'Commercial portrait painters in several cities went out of business within a decade',
  'Landscape photography became technically feasible earlier in some countries than in others'],
 "The passage rests on chronology and on technical incapacity. Contemporary statements by painters in those genres would make the influence direct despite both.",
 "Later colour and regional variation strengthen the passage, acceleration is consistent with other causes, and the portrait trade is the passage's own point.")

P['I'] = ("Two accounts of why cities grew in the nineteenth century compete in the "
"literature, and the disagreement has proved durable because each explains what the other "
"finds awkward. On the first, people moved to cities because wages there were higher, and "
"the evidence is that they were: a labourer in Manchester earned more than a labourer in "
"the county he came from, by a margin that survives most attempts to adjust it.\n\n"
"On the second, the wage gap is not a cause but a price. City life in the period was "
"shorter: mortality in the industrial towns exceeded mortality in the countryside by a "
"wide margin, and a wage that did not compensate for that would have attracted nobody. On "
"this reading the cities grew because the countryside was emptying for reasons of its own, "
"chiefly the consolidation of landholding, and the wage gap is what the cities had to "
"offer to absorb the people the land had released.\n\n"
"The two accounts predict different things about the moments when the flow slowed. The "
"first predicts a slowing when the gap narrowed; the second predicts one when the "
"consolidation paused. Both events occurred, at different times in different counties, "
"and the records are good enough to tell which the flow followed. Nobody has done the "
"work, and the reason is that the parish registers that would show it have never been "
"linked to the estate records that would date the consolidation.")

q('GR125','I','Main idea',4,
 'The primary purpose of the passage is to',
 ['describe two rival explanations and identify the comparison that would decide between them',
  'argue that rural consolidation rather than urban wages drove nineteenth-century migration',
  'establish that mortality in industrial towns exceeded mortality in the countryside',
  'explain why wages in industrial cities were higher than wages in the counties',
  'criticise historians for failing to link parish registers to estate records'],
 "The passage sets out both accounts and then names the test that distinguishes them and the reason it has not been run.",
 "Neither account is endorsed, the mortality and wage facts are evidence, and the closing remark explains rather than criticises.")
q('GR126','I','Inference',4,
 'On the second account described in the passage, the wage gap between city and countryside is best understood as',
 ['compensation for a cost that city life imposed',
  'evidence that urban employers competed for scarce labour',
  'a consequence of higher productivity in urban industry',
  'a measurement artefact produced by differences in the cost of living',
  'the reason that landholding in the counties was consolidated'],
 "The second paragraph calls the gap a price rather than a cause and explains it by the mortality difference.",
 "Competition, productivity, measurement and the direction of causation in the last option are not the second account.")
q('GR127','I','Function of a sentence',3,
 'The final sentence of the passage functions to',
 ['explain why a decisive comparison has not been carried out',
  'suggest that the parish registers are unreliable for this period',
  'recommend a change in how archives are catalogued',
  'establish that the estate records do not survive in most counties',
  'concede that the two accounts cannot in principle be distinguished'],
 "It gives the reason nobody has done the work: the two record sets have never been linked.",
 "Reliability, cataloguing policy and survival are not what it says, and the preceding sentence affirms that the records could settle it.")
q('GR128','I','Strengthen and weaken',4,
 'Which of the following findings would most support the first account described in the passage?',
 ['In counties where the wage gap narrowed while consolidation continued, migration to the cities slowed',
  'In counties where consolidation paused while the wage gap held, migration to the cities slowed',
  'Mortality in the industrial towns fell over the second half of the century',
  'Labourers who moved to the cities earned more than those who stayed',
  'Consolidation of landholding proceeded at different rates in different counties'],
 "The first account predicts that the flow follows the gap. A county where only the gap moved, and the flow followed, is the discriminating case.",
 "The second option supports the rival, falling mortality and the wage comparison are already granted, and varying rates are the premise of the test.")
q('GR129','I','Detail',2,
 'According to the passage, the second account attributes the emptying of the countryside chiefly to',
 ['the consolidation of landholding', 'a fall in agricultural wages',
  'the mortality of the industrial towns', 'the growth of the railway network',
  'the enclosure of common pasture'],
 "The second paragraph names the consolidation of landholding.",
 "Agricultural wages, urban mortality, railways and enclosure are not what the passage names as the chief reason.")

P['J'] = ("A proof assistant checks a mathematical argument step by step against a formal "
"system, and a proof it accepts contains no gap. Mathematicians have been slow to adopt "
"them, and the usual explanation is inertia. A better one is that a proof serves two "
"purposes, and the assistant addresses only the first. A proof establishes that a theorem "
"is true, and it explains why. Formalisation preserves the first perfectly and can destroy "
"the second: a hundred lines of case analysis that a reader would summarise in a sentence "
"is, to the machine, the proof.")

P['K'] = ("Attempts to date the arrival of dogs in the Americas have produced two answers. "
"Archaeological remains put it at around ten thousand years ago; genetic estimates based "
"on mutation rates put it several thousand years earlier. The discrepancy has been treated "
"as a problem for one method or the other. It may instead be a fact: a founding population "
"can enter a continent long before it becomes numerous enough to leave remains that "
"survive and are found, and the two methods are dating different events.")

P['L'] = ("The standard objection to citizen science is that volunteers make errors trained "
"observers would not. The data bear this out at the level of the individual record and not "
"at the level of the dataset. A volunteer network reporting a hundred thousand bird "
"sightings contains more misidentifications than a professional survey reporting two "
"thousand, and it also contains the two thousand, along with coverage of places and hours "
"that no professional survey has ever reached. Which dataset is better depends entirely on "
"the question, and the objection is usually made as though it did not.")

P['M'] = ("Adam Smith is read as the theorist of self-interest on the strength of a sentence "
"about the butcher and the brewer. The sentence is in the Wealth of Nations, and so is a "
"great deal about the conditions under which self-interest produces a good outcome: "
"competition among sellers, buyers who can judge what they are buying, and a legal order "
"that makes contracts enforceable and fraud punishable. Smith devoted more pages to what "
"happens when those conditions fail than to the butcher, and the selective reading has "
"made a conditional claim look like an unconditional one.")

q('GR130','J','Main idea',4,
 'The primary purpose of the passage is to',
 ["offer an explanation of a profession's reluctance that is not a charge of inertia",
  'argue that proof assistants should be adopted more widely by mathematicians',
  'establish that formalised proofs contain no logical gaps',
  'describe the formal systems against which proof assistants check arguments',
  'question whether a proof can establish that a theorem is true'],
 "The passage names the usual explanation, calls a better one available, and sets out the two purposes a proof serves.",
 "No adoption is urged, the absence of gaps is granted, the systems are background, and the first purpose is not in doubt.")
q('GR131','J','Inference',4,
 'The passage suggests that a formalised proof may be inferior to an informal one at',
 ['showing a reader why the theorem holds',
  'establishing that the theorem is true',
  'covering every case the theorem requires',
  'being checked by other mathematicians',
  'identifying the assumptions the theorem depends on'],
 "The passage says formalisation preserves the first purpose perfectly and can destroy the second, which is explanation.",
 "Truth, case coverage and assumption tracking are what formalisation does well, and checkability is not raised.")
q('GR132','J','Function of a sentence',3,
 'The reference to a hundred lines of case analysis serves to',
 ['illustrate how a formal proof can obscure the reason a theorem holds',
  'establish that case analysis is the most common method of proof',
  'suggest that proof assistants are slow to check long arguments',
  'show that mathematicians summarise proofs inaccurately',
  'explain why formal systems require so many axioms'],
 "It is the example of the second purpose being destroyed: what a reader would summarise in a sentence is, to the machine, the proof.",
 "Prevalence, speed, summary accuracy and axioms are not what the example shows.")

q('GR133','K','Main idea',3,
 'The passage is primarily concerned with',
 ['proposing that a discrepancy between two methods reflects a real difference in what they date',
  'arguing that genetic estimates of arrival dates are more reliable than archaeological ones',
  'establishing when dogs first arrived in the Americas',
  'describing the mutation rate methods used to date population movements',
  'questioning whether archaeological remains can be dated accurately'],
 "The last sentence says the discrepancy may be a fact and that the two methods are dating different events.",
 "Neither method is preferred, no date is settled, the methods are named rather than described, and dating accuracy is not questioned.")
q('GR134','K','Inference',4,
 'The passage implies that archaeological remains record the arrival of a population only once it has',
 ['become numerous enough to leave traces that survive and are found',
  'spread across the whole of the continent it entered',
  'begun to bury its animals in a recognisable way',
  'developed the material culture that archaeologists study',
  'ceased to move between regions'],
 "The last sentence states exactly this condition.",
 "Geographic spread, burial practice, material culture and settlement are not the condition named.")
q('GR135','K','Strengthen and weaken',4,
 'Which of the following would most strengthen the account the passage proposes?',
 ['A founding population entering another continent is shown to have left no surviving remains for several thousand years',
  'Mutation rate estimates are shown to be accurate to within a century',
  'Archaeological remains of dogs are found at a second site of similar age',
  'Genetic and archaeological dates agree for a species that arrived more recently',
  'The earliest known dog remains in the Americas are redated to a later period'],
 "A documented lag between entry and the first surviving remains is direct support for the two methods dating different events.",
 "Estimate precision, a second site of the same age, agreement elsewhere and a later redating do not establish the lag.")

q('GR136','L','Main idea',3,
 'The primary purpose of the passage is to',
 ['show that an objection holds at one level of analysis and is applied at another',
  'argue that volunteer networks produce more accurate data than professional surveys',
  'establish that professional bird surveys cover fewer places than volunteer networks',
  'describe the kinds of error that volunteer observers most often make',
  'recommend that professional surveys recruit volunteers to extend their coverage'],
 "The passage grants the objection at the level of the individual record and says it fails at the level of the dataset, then notes it is made as though the distinction did not exist.",
 "No accuracy ranking is asserted, the coverage point is evidence, the errors are not described, and no recommendation is made.")
q('GR137','L','Inference',4,
 'The passage suggests that whether a volunteer dataset is preferable to a professional one depends on',
 ['what the dataset is being used to find out',
  'the ratio of misidentifications to correct records',
  'whether the volunteers received training beforehand',
  'the number of professional observers available',
  'how recently the records were collected'],
 "The last sentence says which dataset is better depends entirely on the question.",
 "Error ratio, training, observer numbers and recency are not what the passage makes decisive.")
q('GR138','L','Function of a sentence',3,
 'The observation that the volunteer dataset also contains the two thousand serves to',
 ['indicate that the larger dataset loses nothing the smaller one has',
  'suggest that the professional records were collected by volunteers',
  'establish that the two datasets were gathered in the same places',
  'question whether the professional survey was large enough',
  'explain why misidentifications are more common in larger datasets'],
 "The clause makes the point that the volunteer set includes the professional set's worth of correct records and adds coverage besides.",
 "Provenance, overlap of location, survey size and error rates are not what the clause asserts.")

q('GR139','M','Main idea',4,
 'The passage is primarily concerned with',
 ['arguing that a selective reading has turned a conditional claim into an unconditional one',
  'establishing that Adam Smith did not believe self-interest produces good outcomes',
  'describing the conditions under which competition among sellers benefits buyers',
  'comparing the Wealth of Nations with other economic writing of its period',
  'questioning whether the passage about the butcher and the brewer is authentic'],
 "The last sentence states it directly.",
 "Smith is said to have set out conditions rather than to have denied the conclusion, the conditions are evidence, and no comparison or authenticity question arises.")
q('GR140','M','Detail',2,
 'According to the passage, the conditions Smith named include all of the following EXCEPT',
 ['a limit on the size of the firms competing in a market',
  'competition among sellers',
  'buyers who can judge what they are buying',
  'enforceable contracts',
  'punishable fraud'],
 "The passage lists competition, informed buyers, and a legal order making contracts enforceable and fraud punishable. Firm size is not among them.",
 "The other four are named in the same sentence.")
q('GR141','M','Inference',4,
 'The passage implies that a reader who cites the butcher and the brewer without the conditions is',
 ['reporting one half of an argument as though it were the whole',
  'misquoting a sentence that does not appear in the Wealth of Nations',
  'confusing Smith with a later writer in the same tradition',
  'applying to modern markets a claim Smith made only about eighteenth-century ones',
  "relying on a translation that alters Smith's meaning"],
 "The passage says the selective reading makes a conditional claim look unconditional, which is taking the consequent without the antecedent.",
 "The sentence is granted as Smith's, no confusion, no period restriction and no translation issue is raised.")

P['N'] = ("That a language has many words for something is routinely read as evidence "
"that its speakers care about it. The inference is weak in a way that is easy to state: a "
"count of words measures how a language divides a domain, not how much attention its "
"speakers give the domain. English carries a large vocabulary for the colours of horses, "
"inherited from a period in which the distinctions were worth making, and the speakers "
"who still have the words mostly do not ride.\n\n"
"The inference can be repaired, but only by doing the work it was meant to avoid. A count "
"restricted to words in current use, weighted by how often speakers actually produce "
"them, would track attention rather than inheritance. Such a count requires a corpus of "
"recorded speech, and the languages the argument is usually made about are the ones for "
"which no corpus has been assembled. The claim therefore survives in the places where it "
"cannot be checked and is quietly dropped in the places where it can.")

q('GR142','N','Main idea',4,
 'The primary purpose of the passage is to',
 ['identify a weakness in a common inference and explain why it persists where it does',
  'argue that vocabulary size is unrelated to the concerns of a speech community',
  'recommend that corpora be assembled for languages that currently lack them',
  'describe the historical process by which English acquired its vocabulary for horses',
  'compare two methods of counting the words available to speakers of a language'],
 "The first paragraph states the weakness and the second explains why the claim is made about languages for which the corrective evidence does not exist.",
 "The passage allows a repaired count to track attention, makes no recommendation, uses the horses as an illustration, and does not compare methods as its purpose.")
q('GR143','N','Function of a sentence',3,
 'The reference to the colours of horses serves to',
 ['supply a case in which a vocabulary outlasted the interest that produced it',
  'show that English divides some domains more finely than other languages do',
  'illustrate the difficulty of counting the words a language contains',
  'suggest that speakers retain words whose meanings they no longer know',
  'establish that inherited vocabulary is larger than vocabulary in current use'],
 "The words survive from a period when the distinctions mattered, among speakers for whom they no longer do, which is exactly the gap between division and attention.",
 "No cross-language comparison, counting difficulty, loss of meaning or claim about relative size is made.")
q('GR144','N','Inference',4,
 'The passage implies that the inference it criticises is made most often about languages that',
 ['offer no record against which it could be tested',
  'divide a greater number of domains than English does',
  'have been studied chiefly by non-native speakers',
  'are spoken by communities whose concerns are poorly documented',
  'have acquired most of their vocabulary recently'],
 "The last sentence pairs the survival of the claim with the absence of a corpus and its abandonment with the presence of one.",
 "Number of domains, who studied them, documentation of concerns generally and the age of the vocabulary are not what the passage identifies.")
q('GR145','N','Strengthen and weaken',4,
 "Which of the following, if true, would most undermine the author's objection?",
 ['For every language with a weighted corpus, raw and weighted counts rank domains alike',
  'Some languages with large corpora have never been the subject of the inference',
  'Speakers can often report which domains their language divides most finely',
  'Vocabulary inherited from an earlier period is usually smaller than vocabulary in use',
  'A few communities have retained words for practices they abandoned long ago'],
 "The objection is that a raw count measures division rather than attention. If the two counts agree wherever both can be taken, the raw count is a serviceable proxy and the objection loses its force.",
 "Which languages have been studied, what speakers can report, the relative size of inherited vocabulary and further cases of retention leave the objection standing.")

P['Q'] = ("When a conservator lifts the varnish from an old master, the colours that "
"emerge are brighter than the ones the painting had the day before, and whether they are "
"the ones it had when it left the studio is a harder question than it sounds. Varnish "
"yellows, so removing it recovers something. But painters knew varnish yellows, and "
"several are documented as having chosen their colours against the tone the surface would "
"acquire rather than the tone it had wet.\n\n"
"That documentation is thin and uneven. Where it exists the conservator has a target and "
"the question is one of fact. Where it does not, the choice falls between two defaults: "
"recover what the pigments can be shown to have been, or preserve the surface as it has "
"come down. Neither is neutral. The first treats the painting as the studio released it, "
"the second as the intervening centuries made it, and in practice the matter is decided "
"by whichever of the two the holding institution has written into its charter, which is "
"to say it is not decided at all.")

q('GR146','Q','Main idea',4,
 'The primary purpose of the passage is to',
 ['show that a technical procedure rests on a question the procedure cannot settle',
  'argue that varnish should be left in place on paintings whose painters are undocumented',
  'establish that the colours revealed by cleaning are not the colours the painter mixed',
  'describe the chemical process by which a varnish layer yellows over time',
  'criticise institutions for adopting conservation policies without consulting conservators'],
 "The passage sets out the cleaning decision and shows that the standard it should answer to is undetermined wherever the documentation is missing.",
 "No default is endorsed, the colour claim holds only for some painters, the chemistry is assumed rather than described, and the charters are described rather than blamed on a failure to consult.")
q('GR147','Q','Detail',2,
 'According to the passage, several painters are documented as having',
 ['selected colours for how they would look once the surface had yellowed',
  'applied varnish to their paintings before the paint had fully dried',
  'objected to the varnishing of their work by later owners',
  'left written instructions for the eventual cleaning of their paintings',
  'mixed pigments that resist the yellowing of the varnish above them'],
 "The first paragraph says several painters are documented as having chosen their colours against the tone the surface would acquire.",
 "Timing of varnishing, objections, instructions and pigment chemistry are not in the passage.")
q('GR148','Q','Inference',4,
 'The passage suggests that where the documentation exists, the conservator',
 ['is answering a question about the painting rather than a question of policy',
  'has no reason to remove the varnish that has accumulated on the surface',
  'will arrive at the same result as a conservator following either default',
  'must still defer to the policy written into the institution charter',
  'can establish what the pigments were without chemical analysis'],
 "The second paragraph says that where the documentation exists the conservator has a target and the question is one of fact, as against the two defaults that apply elsewhere.",
 "Removal, agreement with the defaults, deference to the charter and the dispensability of analysis do not follow.")
q('GR149','Q','Function of a sentence',3,
 'The closing phrase, that the matter is not decided at all, serves to',
 ['deny that an institutional convention amounts to an answer to the question',
  'suggest that charters are revised too often to guide conservation practice',
  'indicate that conservators disregard the policies their institutions adopt',
  'concede that the question of the original colours can never be resolved',
  'propose that the two defaults be combined into a single standard'],
 "The phrase distinguishes settling the question from having a rule that produces an outcome, and says the charters do only the second.",
 "Revision, disregard, the impossibility of resolution and a combined standard are not what the phrase asserts.")

P['R'] = ("The standard model of a common resource predicts its exhaustion. Each user "
"gains the whole of what he takes and bears only a fraction of the cost of the depletion, "
"so each takes more than the group would choose, and the resource fails. The model is "
"clean, and it fits the cases from which it was built.\n\n"
"It fits fewer cases than its reach suggests. Fisheries, pastures and irrigation systems "
"held in common have been worked for centuries in many places without failing, and the "
"field studies that documented them turned up the same features again and again. The "
"users could tell who else was drawing on the resource. They could observe how much was "
"being taken. The boundary of the resource, and of the group entitled to it, was known to "
"everyone inside it. And a user who took too much met a penalty that stopped well short "
"of the courts.\n\n"
"What the studies did not turn up is any rule saying which arrangement a given community "
"will reach. The features recur; the institutions do not. A commons that works has "
"boundaries, monitoring and graduated penalties, and knowing this tells an outsider who "
"proposes to build one very little about what to build. Attempts to transplant a working "
"arrangement have failed about as often as attempts to impose the remedy the model "
"recommends, which is private title.")

q('GR150','R','Main idea',4,
 'The passage is primarily concerned with',
 ['marking the limits of a model and of the evidence that qualifies it',
  'arguing that common ownership manages resources better than private title does',
  'establishing that the standard model of a common resource is mistaken',
  'describing the features shared by commons that have lasted for centuries',
  'recommending that outsiders stop proposing institutions for communities they do not belong to'],
 "The first paragraph grants the model its cases, the second limits them, and the third says the qualifying evidence does not yield a design rule either.",
 "No ranking of ownership is offered, the model is limited rather than refuted, the shared features are evidence, and no recommendation is made.")
q('GR151','R','Detail',2,
 'The passage states that users of the durable commons could do all of the following EXCEPT',
 ['hold legal title to the resource they were drawing on',
  'identify the others who were drawing on the resource',
  'observe how much was being taken from it',
  'recognise the boundary of the group entitled to use it',
  'penalise a user without recourse to the courts'],
 "The second paragraph names the other four. Title is what the model recommends in the third paragraph, and is not among the features the studies found.",
 "Identification, observation, the known boundary and the penalty short of the courts are each stated.")
q('GR152','R','Inference',4,
 'The passage implies that the recurring features identified by the field studies',
 ['describe the arrangements that work without amounting to instructions for building one',
  'are present in every community that holds a resource in common',
  'were absent from the cases on which the standard model was built',
  'matter less to a commons than the particular institutions a community adopts',
  'have been reproduced successfully by outsiders in a majority of attempts'],
 "The third paragraph says the features recur, the institutions do not, and that knowing the features tells a would-be builder very little.",
 "Universality, absence from the model cases, relative importance and a success rate are not claimed.")
q('GR153','R','Function of a sentence',3,
 'The reference to private title at the end of the passage serves to',
 ['note that the remedy the model recommends has no better record',
  'identify the arrangement most of the durable commons eventually adopted',
  'explain why transplanted arrangements fail as often as they do',
  'suggest that the standard model was built on cases of private ownership',
  'concede that no arrangement of any kind reliably preserves a common resource'],
 "It is set beside the transplanted arrangements to say that both approaches fail at about the same rate.",
 "The durable commons did not adopt it, it does not explain the transplant failures, it is the model's remedy rather than its evidence, and the passage does not deny that the durable commons preserved their resources.")
q('GR154','R','Strengthen and weaken',4,
 'Which of the following findings would most support the claim made in the third paragraph?',
 ['Communities alike in resource, size and recurring features settled on arrangements differing in their particulars',
  'A commons lacking any one of the recurring features failed within a generation',
  'Several communities that had worked a commons for centuries abandoned it after title was granted',
  'Outsiders who spent a year in a community before proposing an institution succeeded more often',
  'The recurring features were present in the fisheries as well as in the pastures'],
 "The claim is that the features recur while the institutions do not, so holding the features and the circumstances constant and finding the institutions still differ is the case that supports it.",
 "Necessity of the features, the effect of title, the outsiders' success rate and the breadth of the features are all about something else.")

HEADER = '''// bank_gre_rc3.js - Original GRE Reading Comprehension items GR101-GR154.
//
// Generated by src/mk_bank_gre_rc3.py. Edit that file, not this one.
//
// The last skill on any exam still well below its neighbours. GRE Reading Comprehension
// held 40 items against 91 to 95 for the other six GRE skills. These 54 take it to 94.
//
// Sixteen passages in the two shapes the GRE uses: twelve short passages of one dense
// paragraph carrying three questions each, and four longer ones carrying four or five.
// Subtypes are the five the existing GRE banks use: main idea, inference, function of a
// sentence, strengthen and weaken, and detail.
//
// The passage text is a named constant shared by the items that use it, as in the LSAT
// and ACT banks, so a paragraph is not stored three times in one file.
//
// The corrections every hand written bank needs are in src/bank_emit.py (INC-0001,
// INC-0003, INC-0039, INC-0059, INC-0062, INC-0066, INC-0068).
'''

E.permute(I)

# Distractors lifted past the key, by item. A list entry says how many to lift, and that
# number sets the key's rank, which is the difference between spreading the pile and
# moving it one place over (INC-0062). check_lift fails the run if a clause was too short
# to do what the table says it does (INC-0066).
LIFT = {
 'GR101': [('more accurately than individuals do', ' acting alone'),
           ('never aggregate the information participants hold', ' about anything'),
           ('unambiguous resolution dates', ' wherever that can be arranged')],
 'GR103': [('more accurate than short-dated ones', ' about the same question'),
           ('the rest of the passage sets aside', ' as a special case'),
           ('attract relatively few traders', ' despite their accuracy'),
           ('no settlement date at all', ' and no unambiguous resolution')],
 'GR104': ('a different order from the one printed', ' in 1609'),
 'GR107': [('deserve greater conservation attention', ' than they now receive'),
           ('threaten species with restricted distributions', ' most directly'),
           ('occur thinly across large ranges', ' rather than in small ones')],
 'GR108': [('total area over which it is distributed', ' at present'),
           ('a more restricted range', ' in the same habitat'),
           ('large fraction of one habitat', ' in a single season')],
 'GR110': [('more yarn per spindle than the jenny', ' in the same time'),
           ('two eighteenth-century machines', ' used to spin yarn'),
           ('persisted longer than is usually supposed', ' in some districts')],
 'GR116': [('was around four million', ' at the time of the census'),
           ('from any surviving evidence', ' of the ancient world')],
 'GR118': [('supported by the surviving evidence', ' one way or the other'),
           ('recorded inaccurately at the time', ' they were first collected')],
 'GR120': [('in every respect but age', ' and general health'),
           ('with the condition being treated', ' at the trial sites'),
           ('smaller than the population', ' once it is approved'),
           ('regulators intend the approval to cover', ' when they grant it')],
 'GR122': [('representation for purely internal reasons', ' having to do with its own history'),
           ('capable of recording colour and movement', ' in ordinary conditions'),
           ('the market for commercial portraits', ' in the later nineteenth century')],
 'GR125': [('drove nineteenth-century migration', ' to the industrial towns'),
           ('exceeded mortality in the countryside', ' throughout the period'),
           ('higher than wages in the counties', ' the migrants had left'),
           ('parish registers to estate records', ' for the counties in question')],
 'GR128': ('consolidation paused while the wage gap held', ' in the same decade'),
 'GR130': [('adopted more widely by mathematicians', ' than they now are'),
           ('proof assistants check arguments', ' step by step')],
 'GR132': [('the most common method of proof', ' in modern mathematics'),
           ('slow to check long arguments', ' of the kind described'),
           ('summarise proofs inaccurately', ' when they report them to one another')],
 'GR133': ('more reliable than archaeological ones', ' in every case'),
 'GR134': [('the material culture that archaeologists study', ' at such sites'),
           ('the whole of the continent it entered', ' from north to south')],
 'GR138': [('collected by volunteers', ' with no training'),
           ('more common in larger datasets', ' than in smaller ones'),
           ('gathered in the same places', ' over the same years'),
           ('survey was large enough', ' to be worth extending')],
 'GR139': [('did not believe self-interest produces good outcomes', ' of any kind'),
           ('competition among sellers benefits buyers', ' in a given market'),
           ('the butcher and the brewer is authentic', ' as it is usually quoted')],
 'GR142': [('acquired its vocabulary for horses', ' and their colours'),
           ('concerns of a speech community', ' at any period'),
           ('words available to speakers of a language', ' in a domain'),
           ('corpora be assembled', ' as a matter of priority')],
 'GR148': [('following either default', ' in the absence of documentation'),
           ('accumulated on the surface', ' over the centuries'),
           ('written into the institution charter', ' whatever the evidence shows'),
           ('without chemical analysis', ' of the paint layers')],
 'GR152': [('the particular institutions a community adopts', ' in a given case'),
           ('by outsiders in a majority of attempts', ' to build a new commons')],
}
E.extend(I, LIFT, 'LIFT')
E.check_lift(I, E.lift_counts(LIFT))

E.measure(I)
PV = dict((k, 'GR3_P' + k) for k in P)
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_gre_rc3.js',
        HEADER, [('GR3_P' + k, P[k]) for k in sorted(P)], I, 'BANK_GRE_RC3',
        passage_var=PV, group_key='passageId')
