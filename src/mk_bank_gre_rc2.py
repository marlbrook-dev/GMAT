#!/usr/bin/env python3
"""Emit src/bank_gre_rc2.js.

Run: python3 src/mk_bank_gre_rc2.py src/bank_gre_rc2.js

The last flagged reading gap. GRE Reading Comprehension held 14 items spread across three
files, which the review bot reports as the one GRE skill under twenty five. These 26 take
it to 40.

Eight passages in the shape the GRE uses: short passages of one dense paragraph carrying
two or three questions, and two longer ones carrying four. The existing GRE banks inline
the passage text on every item that shares it; these use a named constant instead, which
is how the LSAT and ACT banks do it and which stops the same paragraph being stored three
times.

Machinery is in src/bank_emit.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

P = {}
P['A'] = ("The conventional account of the printing press credits it with the spread of "
"literacy. The causation may run the other way. Presses were capital investments that "
"required a market, and the towns where they were established first were those that "
"already supported scribal workshops, notarial schools and a class of merchants who kept "
"their own accounts. What the press changed was not whether people read but what reading "
"cost, and a fall in cost matters most to those who are already readers.")

P['B'] = ("Reviewers of the manuscript objected that its central claim rested on a single "
"excavated site. The objection is fair as far as it goes, but it mistakes what the claim "
"is. The author does not argue that the practice was widespread; she argues that it "
"existed, which one site can establish, and that its existence is incompatible with the "
"chronology the field has assumed. A counterexample does not need to be typical to do its "
"work.")

P['C'] = ("For decades the sterile male technique was the standard method of suppressing "
"screwworm populations: irradiated males were released in numbers large enough to swamp "
"the wild population, and the females that mated with them produced no offspring. The "
"method worked because female screwworms mate once. Applied to species whose females mate "
"repeatedly, it has largely failed, and the failures were for years attributed to "
"insufficient release numbers rather than to the biology that made the original success "
"possible.")

P['D'] = ("It is often said that the novel form arrived with the eighteenth century. The "
"claim survives because of how the term is defined. Prose narratives of substantial length "
"with invented characters existed in Japan by the eleventh century and in the Hellenistic "
"world well before that. What the eighteenth century produced in England was a market, a "
"critical vocabulary and an audience that read alone and silently, and it is the "
"institution rather than the form that is being dated.")

P['E'] = ("The standard objection to a wealth tax is that it is difficult to administer, "
"since illiquid assets must be valued annually and valuation invites dispute. The "
"objection is sound and it is also not decisive, because every tax base requires "
"valuation of something and the question is comparative. Income is no easier to define at "
"its edges than wealth is, and the fact that a familiar difficulty has been absorbed into "
"routine does not make it a smaller difficulty than an unfamiliar one.")

P['F'] = ("Birds that cache food in autumn and recover it months later show seasonal growth "
"in the hippocampus, and the growth is largest in the species that cache most. The "
"correlation was taken as evidence that caching drives the growth. A complication has "
"since emerged: in several species the enlargement precedes the caching season rather than "
"following it, and in one it occurs in individuals prevented from caching at all. Whatever "
"the hippocampus is responding to, it is not the act of storing food.")

P['G'] = ("The argument that a language shapes the thought of its speakers has had two "
"lives. In its strong form, which held that speakers of a language lacking a distinction "
"cannot make that distinction, it was tested repeatedly through the middle of the "
"twentieth century and abandoned. In its weak form, which holds only that habitual "
"distinctions are made faster and more reliably than unfamiliar ones, it has been "
"confirmed many times and is unsurprising.\n\n"
"The difficulty is that the weak form is often defended with rhetoric belonging to the "
"strong one. A finding that speakers of a language with obligatory evidential marking "
"attend more closely to sources is reported as showing that they inhabit a different "
"world. They do not; they answer a particular class of question faster, which is what was "
"measured and is worth knowing. The inflation is not harmless, because it invites a "
"refutation of the strong claim to be read as a refutation of the weak one, and the weak "
"one is true.")

P['H'] = ("Peer review is defended on two grounds that are usually run together. The first "
"is that it filters: unsound work is stopped before publication. The second is that it "
"improves: reviewers find errors the author missed and the published version is better "
"than the submitted one. The evidence for the second is reasonably good. The evidence for "
"the first is poor, and the studies that exist suggest reviewers agree with one another "
"barely more than chance would predict on whether a given paper should be accepted.\n\n"
"This matters for what reform should aim at. If review is mainly a filter, the reasonable "
"response to its unreliability is to strengthen it, with more reviewers and stricter "
"criteria. If it is mainly an improver, the unreliability of the accept and reject "
"decision is close to irrelevant, and the reasonable response is to decouple the two "
"functions: publish more and review after, which is what several fields have begun to do.")

I = []
def q(iid, pk, sub, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'V', 'type': 'RC', '_p': pk, 'passageId': 'GRP' + pk,
              'sub': sub, 'skill': 'gre_rc', 'diff': diff, 'stem': stem,
              'choices': choices, 'answer': 0, 'expl': expl, 'wrong': wrong})
print('scaffold ready')

q('GR001','A','Main idea',3,
 'The primary purpose of the passage is to',
 ['question the direction of a causal claim about a technology and its social effect',
  'establish that literacy rates were higher before printing',
  'describe the economic conditions under which early presses were financed',
  'argue that the printing press had little effect on the cost of books',
  'compare scribal workshops with the presses that replaced them'],
 'It names the conventional account, says the causation may run the other way, and gives the reason: presses went where readers already were.',
 'No rate is claimed, the financing is a premise rather than the subject, the cost fell on the passage\'s own account, and the workshops appear only as evidence.')
q('GR002','A','Inference',4,
 'The passage suggests that a fall in the cost of reading matter would be of least benefit to',
 ['a population in which few people could already read',
  'merchants who kept their own accounts',
  'towns that supported notarial schools',
  'readers who had previously borrowed rather than bought books',
  'scribes whose livelihoods depended on copying'],
 'The last sentence says a fall in cost matters most to those already reading. Its least effect is therefore where readers are few.',
 'Merchants, notarial towns and previous borrowers are all readers. Scribes are harmed rather than unbenefited, which is a different thing.')
q('GR003','A','Function of a sentence',3,
 'The reference to capital investments serves primarily to',
 ['explain why presses appeared first where a reading public already existed',
  'contrast the expense of printing with the expense of scribal copying',
  'suggest that early printers were motivated chiefly by profit',
  'indicate that presses were beyond the means of most towns',
  'introduce the objection that the rest of the passage answers'],
 'It is the reason presses needed a market, which is the mechanism for the reversed causation.',
 'No cost comparison is drawn, motive is not the point, affordability is not claimed, and no objection follows.')

q('GR004','B','Main idea',3,
 'The passage is primarily concerned with',
 ['explaining why an objection, though accurate, does not tell against the claim it targets',
  'defending the practice of drawing conclusions from single archaeological sites',
  'establishing that the practice described was more widespread',
  'criticising reviewers for failing to read the manuscript carefully',
  'proposing a revised chronology for the period in question'],
 'The objection is called fair as far as it goes and then shown to mistake what the claim is: existence, not prevalence.',
 'No general defence of single sites is offered, prevalence is expressly not claimed, the reviewers are not accused of carelessness, and no chronology is proposed.')
q('GR005','B','Inference',4,
 'The passage implies that the reviewers\' objection would have been telling if the author had argued that',
 ['the practice was common across the region and period',
  'the site had been dated by more than one method',
  'the existing chronology was correct in outline',
  'a counterexample must be typical to be informative',
  'the excavation was more carefully conducted than earlier ones'],
 'The objection is that one site is too little. That bites against a claim of prevalence, which is precisely the claim the author did not make.',
 'Dating method, the chronology and excavation quality are not what the objection concerns, and the fourth is the principle the passage denies.')
q('GR006','B','Function of a sentence',4,
 'The final sentence functions to',
 ['state the general principle on which the passage\'s defence of the author rests',
  'concede a limitation that the author will need to address in later work',
  'introduce a second objection that the reviewers had overlooked',
  'qualify the claim that the practice existed',
  'summarise the reviewers\' position in its strongest form'],
 'A counterexample does not need to be typical to do its work is the principle that makes one site sufficient for an existence claim.',
 'Nothing is conceded or qualified, no second objection appears, and it states the author\'s defence rather than the reviewers\' case.')

q('GR007','C','Main idea',3,
 'The primary purpose of the passage is to',
 ['identify the condition that made a technique work and explain why its failures were misread',
  'argue that the sterile male technique should be abandoned for all species',
  'describe the biological mechanism by which irradiation prevents reproduction',
  'compare the cost of the sterile male technique with that of chemical control',
  'establish that screwworm populations have been permanently suppressed'],
 'The passage names the single mating of female screwworms as the condition, notes the failures elsewhere, and says they were attributed to release numbers rather than to that biology.',
 'No general abandonment is urged, irradiation is not explained, cost is absent, and permanence is not claimed.')
q('GR008','C','Inference',4,
 'It can be inferred from the passage that increasing the number of sterile males released would be least effective in a species whose females',
 ['mate several times over their reproductive lives',
  'produce unusually large numbers of offspring',
  'disperse widely from their site of emergence',
  'are difficult to distinguish from males in the field',
  'survive for a shorter period than males do'],
 'The technique depends on a female\'s single mating being wasted. Repeated mating gives her other chances, so more releases do not rescue it.',
 'Fecundity, dispersal, identification and survival are all relevant to control in general but none is the condition the passage isolates.')
q('GR009','C','Strengthen and weaken',4,
 'Which of the following, if true, most strengthens the passage\'s account of why the technique failed in other species?',
 ['In a species whose females mate twice, doubling the release rate produced no greater suppression than the original rate.',
  'The irradiation dose used in later programmes was lower.',
  'Later programmes were conducted over smaller geographic areas than the screwworm campaign.',
  'Wild males in later programmes were more numerous than had been estimated.',
  'Sterile males released in later programmes survived for fewer days after release.'],
 'The account says the limit is biological rather than numerical. A doubled release rate achieving nothing is exactly that prediction confirmed.',
 'Dose, area, wild numbers and survival are all versions of the numerical explanation the passage is arguing against.')

q('GR010','D','Main idea',3,
 'The passage is chiefly concerned with',
 ['showing that a familiar claim about origins depends on how a term is defined',
  'establishing that the novel originated in Japan rather than in England',
  'describing the reading practices of eighteenth century English audiences',
  'arguing that critical vocabulary is a prerequisite for any literary form',
  'comparing Hellenistic prose narratives with later European ones'],
 'The claim survives because of how the term is defined, and the passage then separates the form from the institution being dated.',
 'No rival origin is asserted, the reading practices are evidence, no prerequisite claim is made, and no comparison is drawn.')
q('GR011','D','Inference',4,
 'The passage implies that a historian who dated the novel to the eighteenth century would be understood by the author to be dating',
 ['the conditions surrounding the form rather than the form itself',
  'the earliest surviving prose narrative of substantial length',
  'the point at which invented characters first appeared in prose',
  'the emergence of silent reading as a private activity',
  'a claim that the author regards as simply mistaken'],
 'The last sentence says it is the institution rather than the form that is being dated, and names the market, the vocabulary and the audience.',
 'The earlier narratives are granted. Silent reading is one of three conditions rather than the whole. The author calls the claim dependent on definition rather than mistaken.')
q('GR012','D','Function of a sentence',3,
 'The reference to Japan and the Hellenistic world serves to',
 ['show that the defining features of the form predate the period usually given',
  'suggest that the English novel was influenced by earlier traditions',
  'establish that prose narrative developed independently in several places',
  'question whether length is a useful criterion for identifying a novel',
  'illustrate the difficulty of dating undated manuscripts'],
 'They are instances of prose narratives of substantial length with invented characters, which is the definition the sentence before supplies.',
 'No influence is claimed, independence is not the point being made, length is used rather than questioned, and dating difficulty is absent.')

q('GR013','E','Main idea',3,
 'The primary purpose of the passage is to',
 ['grant an objection while denying that it settles the question',
  'demonstrate that a wealth tax would be simpler to administer than an income tax',
  'argue that valuation disputes are rare in practice',
  'recommend that wealth be taxed at the same rate as income',
  'establish that income is impossible to define at its edges'],
 'The objection is called sound and also not decisive, and the reason given is that the question is comparative.',
 'Simpler is stronger than the passage claims. Disputes are granted, no rate is recommended, and income is called no easier rather than impossible.')
q('GR014','E','Inference',4,
 'The passage suggests that the familiarity of a difficulty can',
 ['make it seem smaller than a comparable unfamiliar one',
  'reduce the number of disputes that the difficulty generates',
  'indicate that the difficulty has in fact been solved',
  'justify treating the tax base that carries it as preferable',
  'make it harder to measure the cost of administering a tax'],
 'The last clause says absorbing a familiar difficulty into routine does not make it a smaller difficulty than an unfamiliar one, which implies it looks smaller.',
 'Fewer disputes, solution and justification are all things the passage denies follow, and measurement cost is not discussed.')
q('GR015','E','Strengthen and weaken',5,
 'Which of the following, if true, would most weaken the passage\'s argument?',
 ['Valuation disputes over illiquid assets consume several times the administrative resources that income definition disputes do.',
  'Several countries that adopted a wealth tax later repealed it.',
  'Most household wealth in developed economies is held in liquid form.',
  'Income tax codes have grown substantially longer over the past century.',
  'Wealth is distributed more unequally than income in most countries.'],
 'The argument is that the comparison is what matters and that familiarity disguises the income side. A large measured gap in the comparison is what would defeat it.',
 'Repeal has many causes, liquid holdings would help the argument, code length is ambiguous, and distribution is a different question.')

q('GR016','F','Main idea',3,
 'The primary purpose of the passage is to',
 ['report evidence that unsettles an accepted explanation of a correlation',
  'establish that hippocampal growth is unrelated to food caching',
  'describe the seasonal behaviour of birds that store food',
  'argue that correlational evidence is unreliable in behavioural ecology',
  'propose an alternative cause for the enlargement observed'],
 'The correlation and its accepted reading are stated, then the timing and the prevented individuals complicate it, and the passage stops short of an alternative.',
 'Unrelated is stronger than the evidence given. The behaviour is background, no general claim about correlation is made, and no alternative is proposed.')
q('GR017','F','Inference',4,
 'The finding about individuals prevented from caching is significant because it',
 ['separates the enlargement from the behaviour it was thought to result from',
  'shows that the enlargement is larger in species that cache more',
  'confirms that the enlargement is seasonal rather than permanent',
  'establishes that caching is unnecessary for winter survival',
  'suggests that the birds were prevented from caching too late in the season'],
 'If the enlargement occurs without caching, caching cannot be what produces it, which is the passage\'s conclusion.',
 'The species comparison is the original correlation. Seasonality is assumed throughout. Survival is not discussed, and the timing objection would undercut rather than explain the finding.')
q('GR018','F','Function of a sentence',4,
 'The last sentence of the passage functions to',
 ['state what the evidence rules out without asserting what is responsible',
  'identify the environmental cue that triggers the enlargement',
  'summarise the correlation described at the start of the passage',
  'concede that the complication may prove to be an artefact',
  'recommend a particular design for future experiments'],
 'Whatever the hippocampus is responding to, it is not the act of storing food, which excludes a cause without naming one.',
 'No cue is identified, the correlation is not restated, nothing is conceded as artefact, and no design is recommended.')

q('GR019','G','Main idea',4,
 'The primary purpose of the passage is to',
 ['distinguish two versions of a claim and object to how the weaker one is presented',
  'argue that linguistic relativity has been refuted in all its forms',
  'report experimental findings about speakers of languages with evidential marking',
  'establish that habitual distinctions are made faster than unfamiliar ones',
  'trace the history of a hypothesis from its formulation to its abandonment'],
 'The two forms are separated, the weak one is called true, and the objection is that it is defended with rhetoric belonging to the strong one.',
 'The weak form is affirmed rather than refuted. The evidential finding is an example, the speed result is granted rather than established here, and the history is compressed background.')
q('GR020','G','Inference',5,
 'The passage suggests that the inflation it describes is harmful chiefly because it',
 ['allows a refutation of the strong claim to be taken as a refutation of the weak one',
  'exaggerates the speed advantage that the experiments actually measured',
  'discourages researchers from testing the strong form of the claim',
  'implies that speakers of some languages are incapable of certain thoughts',
  'makes the weak form difficult to distinguish from an untestable assertion'],
 'The last sentence says exactly this and adds that the weak one is true.',
 'The speed result is reported accurately; the inflation is in the interpretation. Testing, incapacity and testability are not the stated harm.')
q('GR021','G','Function of a sentence',4,
 'The statement that they answer a particular class of question faster serves to',
 ['restate a reported finding in terms of what was actually measured',
  'concede that the evidential marking result has not been replicated',
  'introduce a distinction between speed and accuracy of response',
  'suggest that the finding is too small to be of interest',
  'establish that evidential marking is unusual among languages'],
 'It follows they do not, and replaces inhabiting a different world with the measurement, then says it is worth knowing.',
 'No replication issue is raised, speed and accuracy are not separated, the finding is called worth knowing, and frequency across languages is not the point.')
q('GR022','G','Strengthen and weaken',5,
 'Which of the following, if true, would most undermine the passage\'s characterisation of the weak form?',
 ['Speakers showed no advantage on distinctions their language marks obligatorily once education was controlled for.',
  'The strong form of the claim was defended by researchers who also endorsed the weak form.',
  'Evidential marking is obligatory in a smaller number of languages than was once believed.',
  'Some experiments on habitual distinctions have used very small samples.',
  'Speakers of languages without evidential marking can be trained to attend to sources.'],
 'The passage calls the weak form confirmed many times. Removing the advantage once education is controlled would remove the confirmation itself.',
 'Who defended what, how many languages mark evidentiality, individual sample sizes and trainability all leave the confirmed effect standing.')

q('GR023','H','Main idea',4,
 'The primary purpose of the passage is to',
 ['separate two functions of a practice and draw out what follows for how it should be changed',
  'argue that peer review should be abolished in favour of publishing everything',
  'establish that reviewers disagree with one another more often than they agree',
  'describe the reforms that several fields have recently adopted',
  'demonstrate that peer review improves the papers it is applied to'],
 'The filter and the improver are separated, the evidence for each is weighed, and the final paragraph says what each account implies for reform.',
 'Abolition is not urged. The agreement statistic is evidence rather than the point. The reforms are an illustration, and the improvement claim is one half of the distinction.')
q('GR024','H','Inference',5,
 'According to the passage, someone who believed peer review functions mainly as a filter would most likely favour',
 ['increasing the number of reviewers and tightening the criteria for acceptance',
  'publishing submissions promptly and collecting reviews afterwards',
  'separating the decision to publish from the effort to improve a paper',
  'abandoning the requirement that reviewers agree with one another',
  'measuring the improvement between submitted and published versions'],
 'The final paragraph states that response directly for the filter account.',
 'The other four belong to the improver account or to measurement rather than to strengthening the filter.')
q('GR025','H','Function of a sentence',4,
 'The observation that reviewers agree barely more than chance would predict is offered as',
 ['evidence bearing on one of the two defences the passage distinguishes',
  'the main conclusion for which the rest of the passage argues',
  'a reason to doubt that peer review improves the papers it is applied to',
  'an explanation of why several fields have begun publishing before review',
  'a concession that weakens the passage\'s own position'],
 'It sits in the paragraph weighing the evidence, and it bears on the filter defence specifically.',
 'The conclusion is about reform. It bears on filtering rather than improving, it is evidence rather than an explanation of the reforms, and the passage has no position it weakens.')
q('GR026','H','Strengthen and weaken',5,
 'Which of the following, if true, would most strengthen the case for the decoupling the passage describes?',
 ['Papers rejected by one journal and published unchanged by another are cited at the same rate as papers accepted first time.',
  'Reviewers spend more time on papers they expect to recommend for acceptance.',
  'Most authors report that reviewer comments improved their manuscripts.',
  'Journals that publish more papers receive more submissions.',
  'The number of papers submitted for review has risen faster than the number of reviewers.'],
 'Decoupling assumes the accept and reject decision carries little information. Equal citation rates for papers that failed it are that assumption confirmed.',
 'Reviewer effort, author satisfaction, submission volume and reviewer supply bear on the practice without testing whether the decision is informative.')

print('%d items drafted' % len(I))

HEADER = '''// bank_gre_rc2.js - Original GRE Reading Comprehension items GR001-GR026.
//
// Generated by src/mk_bank_gre_rc2.py. Edit that file, not this one.
//
// The last flagged reading gap. GRE Reading Comprehension held 14 items spread across
// three files, the one GRE skill the review bot reported under twenty five. These 26
// take it to 40.
//
// Eight passages in the shape the GRE uses: six short passages of one dense paragraph
// carrying three questions each, and two longer ones carrying four. Subtypes are the
// ones the existing GRE banks use: main idea, inference, function of a sentence, and
// strengthen and weaken.
//
// The existing GRE banks inline the passage text on every item that shares it. These use
// a named constant, which is how the LSAT and ACT banks do it and which stops the same
// paragraph being stored three times in one file.
//
// The corrections every hand written bank needs are in src/bank_emit.py (INC-0001,
// INC-0003, INC-0039, INC-0059, INC-0062).
'''

E.permute(I)

EXTEND = {
 'GR001': ('establish that literacy rates were higher before printing', ' than is usually supposed'),
 'GR003': ('contrast the expense of printing with the expense of scribal copying', ' at the same volume'),
 'GR004': ('establishing that the practice described was more widespread', ' than the reviewers were willing to allow'),
 'GR005': ('the site had been dated by more than one method', ' before publication'),
 'GR006': ("summarise the reviewers' position in its strongest form", ' before answering it'),
 'GR007': ('describe the biological mechanism by which irradiation prevents reproduction', ' in released males'),
 'GR009': ('The irradiation dose used in later programmes was lower', ' than that used against screwworms'),
 'GR010': ('describing the reading practices of eighteenth century English audiences', ' in some detail'),
 'GR011': ('the earliest surviving prose narrative of substantial length', ' in any language'),
 'GR012': ('suggest that the English novel was influenced by earlier traditions', ' from outside Europe'),
 'GR014': ('make it harder to measure the cost of administering a tax', ' of either kind'),
 'GR015': ('Several countries that adopted a wealth tax later repealed it', ' within a decade'),
 'GR016': ('argue that correlational evidence is unreliable in behavioural ecology', ' generally'),
 'GR018': ('recommend a particular design for future experiments', ' on the question'),
 'GR019': ('report experimental findings about speakers of languages with evidential marking', ' in particular'),
 'GR020': ('makes the weak form difficult to distinguish from an untestable assertion', ' about experience'),
 'GR022': ('Some experiments on habitual distinctions have used very small samples', ' of speakers'),
 'GR023': ('describe the reforms that several fields have recently adopted', ' in place of review before publication'),
 'GR024': ('measuring the improvement between submitted and published versions', ' of the same paper'),
 'GR026': ('Journals that publish more papers receive more submissions', ' the following year'),
}
E.extend(I, EXTEND)

EXTEND2 = {
 'GR001': ('describe the economic conditions under which early presses were financed', ' and established'),
 'GR004': ('defending the practice of drawing conclusions from single archaeological sites', ' in general'),
 'GR007': ('compare the cost of the sterile male technique with that of chemical control', ' over time'),
 'GR010': ('arguing that critical vocabulary is a prerequisite for any literary form', ' to emerge'),
 'GR013': ('establish that income is impossible to define at its edges', ' in any tax code'),
 'GR016': ('propose an alternative cause for the enlargement observed', ' in the caching species'),
 'GR019': ('trace the history of a hypothesis from its formulation to its abandonment', ' in the strong form'),
 'GR023': ('demonstrate that peer review improves the papers it is applied to', ' before publication'),
 'GR002': ('readers who had previously borrowed rather than bought books', ' from others'),
 'GR005': ('a counterexample must be typical to be informative', ' about the period'),
 'GR008': ('produce unusually large numbers of offspring', ' in a single generation'),
 'GR011': ('the point at which invented characters first appeared in prose', ' narrative'),
 'GR014': ('indicate that the difficulty has in fact been solved', ' by administrators'),
 'GR017': ('confirms that the enlargement is seasonal rather than permanent', ' in those species'),
 'GR020': ('discourages researchers from testing the strong form of the claim', ' experimentally'),
 'GR024': ('abandoning the requirement that reviewers agree with one another', ' before a decision'),

 'GR021': ('establish that evidential marking is unusual among languages', ' of the world'),
 'GR025': ("a concession that weakens the passage's own position", ' on reform'),
}
E.extend(I, EXTEND2, 'EXTEND2')

# Third pass, on HALF the rank two items rather than all of them.
#
# The first attempt extended all thirteen and the best single-rank strategy stayed at 50:
# the pile moved from rank two to rank one intact. That is INC-0062 happening inside the
# correction for INC-0062. Moving every member of a group shifts it; spreading a group
# means moving some of it. Seven of the thirteen are extended here and six are left.
EXTEND3 = {
 'GR001': ('little effect on the cost of books', ' once it was widely adopted'),
 'GR004': ('criticising reviewers for failing to read the manuscript carefully', ' enough'),
 'GR010': ('establishing that the novel originated in Japan rather than in England', ' in the eleventh century'),
 'GR011': ('the emergence of silent reading as a private activity', ' among English audiences'),
 'GR016': ('establish that hippocampal growth is unrelated to food caching', ' in any species'),
 'GR019': ('establish that habitual distinctions are made faster than unfamiliar ones', ' by speakers'),
 'GR024': ('separating the decision to publish from the effort to improve a paper', ' before it appears'),
}
E.extend(I, EXTEND3, 'EXTEND3')

E.measure(I)
PV = {k: 'GR_P' + k for k in P}
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_gre_rc2.js',
        HEADER, [('GR_P' + k, P[k]) for k in sorted(P)], I, 'BANK_GRE_RC2',
        passage_var=PV, group_key='passageId')
