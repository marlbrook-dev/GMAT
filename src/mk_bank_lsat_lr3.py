#!/usr/bin/env python3
"""Emit src/bank_lsat_lr3.js.

Run: python3 src/mk_bank_lsat_lr3.py src/bank_lsat_lr3.js

The LSAT is the one exam the review bot still fails. Its bank holds 142 items against
594 to 1392 for the other four, every one of its twelve skills sits under 21, and the
run reports 232 avoidable repeats in 3500 items served. Logical Reasoning is two thirds
of the real exam and was seven skills at 9 to 11 items each.

These 140 items take each of the seven to 29 or 31. They are grouped by skill rather
than interleaved, because the skill is what the shortfall is measured in and a file
ordered that way can be counted by eye.

Subtypes are the ones the existing LSAT banks use. Difficulty runs 2 to 4, weighted to
3, matching the distribution already in bank_lsat_lr.js and bank_lsat_lr2.js.

Machinery is in src/bank_emit.py. The length tell is corrected by LIFT, which carries a
chosen number of distractors past the key on each listed item; see the note there for
why one per item is not enough.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

I = []
def q(iid, skill, sub, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'LR', 'type': 'LR', 'sub': sub, 'skill': skill,
              'diff': diff, 'stem': stem, 'choices': choices, 'answer': 0,
              'expl': expl, 'wrong': wrong})

# ===================================================================== assumptions
q('LL101','lsat_lr_assum','Necessary assumption',3,
 "Publisher: Readers who finish a novel are far more likely to buy the author's next one "
 "than readers who abandon it. Our new series will therefore keep its first chapters "
 "short, since short opening chapters reduce the rate at which readers abandon a novel.\n\n"
 "Which one of the following is an assumption required by the publisher's argument?",
 ['Shortening the opening chapters of the new series will not reduce the rate at which readers finish it for some other reason',
  'Most readers who abandon a novel do so during its opening chapters',
  'Readers who finish a novel recommend it to others more often than readers who abandon it',
  'The new series will attract readers who have not previously bought books',
  'Novels with short opening chapters sell more copies in their first month'],
 'The plan works only if the change does not cost as much completion as it buys. If short openings also drove readers away later, the rate of finishing could fall despite fewer early abandonments.',
 'Where abandonment happens, recommendations, new readers and first month sales are all consistent with the argument failing.')
q('LL102','lsat_lr_assum','Necessary assumption',3,
 "A city council proposes to reduce traffic deaths by lowering the speed limit on arterial "
 "roads from 40 to 30 kilometres per hour. Opponents note that most drivers already exceed "
 "the posted limit. The council replies that lowering the limit will still reduce deaths, "
 "because enforcement cameras are triggered by the posted limit.\n\n"
 "The council's reply assumes which one of the following?",
 ['The cameras will issue enough citations at the lower limit to change how fast at least some drivers travel',
  'Drivers who exceed the speed limit are responsible for the majority of traffic deaths on arterial roads',
  'The cost of operating the enforcement cameras will be recovered from the citations they generate',
  'No arterial road in the city is currently without an enforcement camera',
  'Lowering the speed limit will not increase the number of collisions at intersections'],
 'The reply concedes that drivers exceed the limit and rests entirely on the cameras. If citations at the new threshold changed nobody\'s speed, the reply would give no reason to expect fewer deaths.',
 'Who causes deaths, cost recovery, complete camera coverage and intersection collisions are all compatible with the reply being sound or unsound.')
q('LL103','lsat_lr_assum','Sufficient assumption',4,
 "Archaeologist: The pottery at the lower site is decorated in a style that appears at the "
 "upper site only in its latest layers. So the lower site was occupied after the upper site "
 "was abandoned.\n\n"
 "The archaeologist's conclusion follows logically if which one of the following is assumed?",
 ['A decorative style appears at a site only after it has ceased to be used at every site where it appeared earlier',
  'The upper site was abandoned before any pottery in the latest style was produced there',
  'No decorative style found at the lower site appears in the earliest layers of the upper site',
  'The lower site was occupied for a shorter period than the upper site was',
  'Pottery styles spread from one settlement to another more slowly than other crafts do'],
 'With that premise, a style present at the lower site cannot have been in use anywhere earlier, so the upper site occupation using it had ended. That forces the conclusion.',
 'B contradicts the evidence, C and D do not bear on order, and E is about rate rather than sequence.')
q('LL104','lsat_lr_assum','Necessary assumption',2,
 "Nutritionist: The participants who followed our meal plan lost more weight over six months "
 "than those who did not. The plan is therefore effective.\n\n"
 "Which one of the following is an assumption on which the nutritionist's argument depends?",
 ['The two groups did not differ in some other respect that would account for the difference in weight loss',
  'Participants who followed the plan will keep the weight off for at least a further six months',
  'The plan is less expensive to follow than the diets the other participants chose',
  'Weight loss is the only health outcome the meal plan was designed to improve',
  'Every participant who followed the plan lost weight during the six months'],
 'The inference from a group difference to the plan working requires that the plan is what differed. Any other systematic difference between the groups would explain the result instead.',
 'Durability, cost, other outcomes and universal success are all things the argument can do without.')
q('LL105','lsat_lr_assum','Sufficient assumption',4,
 "Editor: A newspaper should print a correction whenever it publishes a false statement of "
 "fact. Our weather forecast said the storm would arrive on Tuesday and it arrived on "
 "Wednesday. So we should print a correction.\n\n"
 "The editor's conclusion follows logically if which one of the following is assumed?",
 ['A forecast that does not come true is a false statement of fact',
  'A newspaper is responsible for the accuracy of the forecasts it publishes',
  'Readers rely on the newspaper for information about approaching storms',
  'The newspaper has printed corrections for inaccurate forecasts in the past',
  'A forecast that is wrong about the day of an event is wrong about the event itself'],
 'The rule applies to false statements of fact. Calling an unfulfilled forecast one brings the case under the rule, which is what the conclusion needs.',
 'Responsibility, reliance and past practice do not connect the forecast to the rule, and E restates the error without classifying it.')
q('LL106','lsat_lr_assum','Necessary assumption',3,
 "Economist: Firms that grant their workers a share of profits report higher productivity "
 "than comparable firms that do not. Profit sharing therefore raises productivity, and "
 "should be encouraged by tax policy.\n\n"
 "The economist's argument requires the assumption that",
 ['higher productivity is not itself among the reasons a firm adopts profit sharing',
  'workers value a share of profits more highly than an equivalent increase in wages',
  'tax policy is capable of influencing whether a firm adopts profit sharing',
  'firms that adopt profit sharing do not also adopt other productivity measures',
  'the productivity gains from profit sharing exceed the cost of the profits shared'],
 'The causal claim reverses if productive firms are the ones that can afford to share profits. Ruling that out is what the inference from correlation to cause needs.',
 'Worker preferences, the reach of tax policy, other measures and net cost all bear on the recommendation rather than on the causal claim it rests on.')
q('LL107','lsat_lr_assum','Necessary assumption',3,
 "Veterinarian: The vaccine protects dogs against the virus for at least three years. Owners "
 "are nonetheless told to revaccinate annually. Since annual revaccination carries a small "
 "risk of adverse reaction, the recommendation does more harm than good.\n\n"
 "Which one of the following is an assumption required by the veterinarian's argument?",
 ['Annual revaccination provides no benefit beyond the protection the vaccine already gives for three years',
  'The adverse reactions caused by revaccination are more serious than the illness the virus causes',
  'Most owners follow the recommendation to revaccinate their dogs every year',
  'No dog loses protection against the virus in less than three years',
  'Veterinarians recommend annual revaccination because it increases their revenue'],
 'The argument weighs a small risk against nothing. If the annual dose added protection, whether by covering the minority whose immunity lapses or by improving coverage, the balance is not established.',
 'Severity, compliance and motive are beside the point, and D is stronger than the argument needs and is not required.')
q('LL108','lsat_lr_assum','Sufficient assumption',4,
 "Critic: Any film that depicts a historical figure has a duty to the record. This film "
 "invents a meeting between two people who never met. It therefore fails in its duty.\n\n"
 "The critic's conclusion follows logically if which one of the following is assumed?",
 ['A film that invents an event involving a historical figure fails in any duty it has to the record',
  'The two people the film depicts as meeting are both historical figures',
  'Audiences cannot distinguish invented scenes from documented ones',
  'A film with a duty to the record should state at the outset which of its scenes are invented',
  'Inventing a meeting is a more serious departure from the record than inventing dialogue'],
 'The premise establishes a duty and an invention. The gap is whether inventing breaches the duty, and the assumption closes it.',
 'B is nearly given by the first premise, C and D add obligations without linking invention to breach, and E compares breaches rather than establishing one.')
q('LL109','lsat_lr_assum','Necessary assumption',3,
 "Airline executive: Passengers say they want more legroom, but when we offer seats with more "
 "legroom at a higher fare, most passengers buy the cheaper seat. Their stated preference is "
 "therefore not their real one.\n\n"
 "The executive's argument depends on assuming which one of the following?",
 ['Passengers who buy the cheaper seat could have afforded the seat with more legroom',
  'The additional legroom offered is enough to make a noticeable difference on a long flight',
  'Passengers are aware of the difference in legroom between the two kinds of seat',
  'No airline offers more legroom without charging a higher fare for it',
  'Passengers would pay more for other improvements to the cabin as well'],
 'A choice reveals a preference only where both options were available. If the higher fare was out of reach, buying the cheaper seat says nothing about wanting legroom.',
 'Noticeability and awareness bear on whether the choice was informed rather than whether it was free, and D and E are irrelevant to this airline\'s passengers.')
q('LL110','lsat_lr_assum','Necessary assumption',3,
 "Historian: The invention of double entry bookkeeping is often credited with enabling the "
 "growth of large commercial partnerships. But merchants in several cities ran partnerships "
 "of comparable size for a century before the method spread. The credit is therefore "
 "misplaced.\n\n"
 "Which one of the following is an assumption required by the historian's argument?",
 ['The partnerships that predated the method were not using some other technique that served the same purpose',
  'Double entry bookkeeping was invented in one of the cities where the earlier partnerships operated',
  'The earlier partnerships kept records that survive in sufficient detail to be compared',
  'Large partnerships became more common after double entry bookkeeping spread than before',
  'No merchant who used double entry bookkeeping operated a partnership of comparable size'],
 'The argument infers from earlier large partnerships that the method was not what enabled them. That holds only if those merchants were not doing by other means what the method later did.',
 'Place of invention, record survival, later prevalence and E all leave the inference untouched or contradict the premises.')
q('LL111','lsat_lr_assum','Sufficient assumption',3,
 "Gardener: Plants in the shaded bed flowered two weeks later than those in the sunny bed. "
 "Since the two beds were planted on the same day with seed from the same packet, the "
 "difference in flowering time was caused by the difference in light.\n\n"
 "The gardener's conclusion follows logically if which one of the following is assumed?",
 ['Light was the only condition that differed between the two beds',
  'Plants grown from a single packet of seed are genetically identical',
  'Shade delays flowering in most species of flowering plant',
  'The shaded bed received at least some direct sunlight each day',
  'Flowering time is a reliable indicator of a plant\'s overall health'],
 'Same day, same seed and light as the sole remaining difference leaves light as the only available cause, which makes the conclusion follow.',
 'Genetic identity is close to given, B and C support the claim without forcing it, and E is beside the point.')
q('LL112','lsat_lr_assum','Necessary assumption',4,
 "Sociologist: Neighbourhoods with more community organisations report less crime. Some argue "
 "that the organisations deter crime. In fact the causation runs the other way: where crime "
 "is low, residents are willing to spend evenings at meetings.\n\n"
 "The sociologist's argument assumes which one of the following?",
 ['The willingness to attend evening meetings is affected by the level of crime in a neighbourhood',
  'Community organisations have no effect at all on the level of crime',
  'Residents of high crime neighbourhoods would form organisations if it were safe to do so',
  'Crime statistics are reported with equal accuracy in all neighbourhoods',
  'Most community organisations hold their meetings in the evening rather than during the day'],
 'The reversed account works through willingness to attend. If crime levels did not affect that willingness, the mechanism the sociologist proposes would not exist.',
 'B is stronger than the argument needs, and C, D and E are not required for the reversed direction to hold.')
q('LL113','lsat_lr_assum','Necessary assumption',3,
 "Manufacturer: Our competitor claims its batteries last longer than ours. But its test ran "
 "the batteries continuously, while ours are designed for intermittent use. The comparison "
 "is therefore worthless.\n\n"
 "The manufacturer's argument requires which one of the following assumptions?",
 ['A battery designed for intermittent use may perform differently under continuous drain than under the use it was designed for',
  'The competitor conducted the test knowing that it would disadvantage',
  'Most purchasers use batteries of this kind intermittently',
  'The manufacturer\'s batteries would outlast the competitor\'s in a test of intermittent use',
  'No standard test protocol exists for comparing batteries of this kind'],
 'Calling the comparison worthless requires that the test condition matters to the result. If design for intermittent use made no difference under continuous drain, the objection would collapse.',
 'Motive, usage patterns, the outcome of a fairer test and the absence of a standard are all things the objection can do without.')
q('LL114','lsat_lr_assum','Sufficient assumption',4,
 "Ethicist: A promise may be broken only when keeping it would cause serious harm. Refusing "
 "to testify would cause serious harm to the defendant. So the witness may break her promise "
 "of confidentiality and testify.\n\n"
 "The ethicist's conclusion follows logically if which one of the following is assumed?",
 ['Keeping the promise of confidentiality would require the witness to refuse to testify',
  'Serious harm to a defendant is worse than the harm caused by breaking a promise',
  'A witness who promises confidentiality is under an obligation to keep the promise',
  'The defendant is not responsible for the situation in which the witness finds herself',
  'Testimony from the witness would change the outcome of the proceeding'],
 'The rule is about the harm keeping the promise would cause. The premise gives the harm of refusing to testify. Linking the two requires that keeping the promise is refusing to testify.',
 'B, C, D and E are about weight, obligation, fault and effect, none of which bridges the rule to the stated harm.')
q('LL115','lsat_lr_assum','Necessary assumption',3,
 "Programme director: Students who took our summer course scored higher on the entrance "
 "examination than students who did not. The course therefore prepares students well for the "
 "examination.\n\n"
 "The argument depends on the assumption that",
 ['the students who took the course were not already better prepared than those who did not',
  'the entrance examination measures the skills the course is designed to teach',
  'students who take the course spend less time studying on their own',
  'the course covers every topic that appears on the entrance examination',
  'no other summer course produces a comparable difference in scores'],
 'Self selection is the obvious rival explanation. If the stronger students were the ones who enrolled, the score difference is not evidence about the course.',
 'What the examination measures, private study, coverage and rival courses all leave the selection problem untouched.')
q('LL116','lsat_lr_assum','Necessary assumption',3,
 "Curator: The painting cannot be by the master, because it is painted on oak, and the master "
 "used only poplar panels.\n\n"
 "Which one of the following is an assumption on which the curator's argument relies?",
 ['The panel the painting is on is the one the painter originally used',
  'The master had access to poplar throughout the period in which he worked',
  'Oak panels were more expensive than poplar panels at the time',
  'No other painter of the period is known to have used oak panels',
  'The painting has not been attributed to the master by any other expert'],
 'The inference runs from the present support to the master\'s practice. A panel transferred or replaced at any point after painting would break it.',
 'Availability, cost, other painters and other attributions do not bear on whether the present panel is the original one.')
q('LL117','lsat_lr_assum','Sufficient assumption',3,
 "Coach: Any player who misses three consecutive training sessions is dropped from the squad. "
 "Reyes missed the sessions on Monday and Wednesday. So Reyes will be dropped.\n\n"
 "The coach's conclusion follows logically if which one of the following is assumed?",
 ['The only training sessions in the relevant period were Monday, Tuesday and Wednesday, and Reyes missed Tuesday as well',
  'Reyes has been warned about attendance on a previous occasion',
  'No player has ever been retained after missing three consecutive',
  'Training sessions are held on Monday, Wednesday and Friday',
  'Reyes had no acceptable reason for missing the two sessions'],
 'The rule needs three consecutive misses and the premises give two. Only an assumption supplying the third, and making the three consecutive, closes the gap.',
 'Warnings, past practice and reasons do not supply the missing session, and D makes Monday and Wednesday non consecutive.')
q('LL118','lsat_lr_assum','Necessary assumption',4,
 "Analyst: The company should not enter the South American market. Its two previous foreign "
 "ventures both failed within three years, and each cost more to unwind than it earned.\n\n"
 "The analyst's argument requires assuming which one of the following?",
 ['Something about the way the company approaches foreign markets, rather than the particular markets it chose, contributed to the earlier failures',
  'The South American market is more competitive than the markets in which the company previously failed',
  'The company has no more capital available now than it had at the time',
  'A venture that is unwound at a loss is worse for the company than not entering the market at all',
  'No competitor has succeeded in the South American market after failing'],
 'Two failures predict a third only if something transferable caused them. If both failures were specific to those markets, the record says nothing about this one.',
 'Relative competitiveness, capital, the comparison in D and competitors\' records do not license the projection from past to future.')
q('LL119','lsat_lr_assum','Necessary assumption',3,
 "Librarian: Circulation of physical books has fallen every year for a decade, while use of "
 "our digital collection has risen. We should therefore shift acquisition funds from print to "
 "digital.\n\n"
 "The librarian's argument assumes which one of the following?",
 ['The decline in print circulation is not caused chiefly by the condition or age of the print collection',
  'Digital titles cost the library less per loan than print titles do',
  'Patrons who borrow digital titles would not borrow the same titles in print if digital were unavailable',
  'The digital collection can be expanded without renegotiating the library\'s existing licences',
  'No patron relies exclusively on the print collection'],
 'Shifting funds away from print assumes print is declining for reasons a better print collection would not fix. If the collection is old because it is underfunded, the recommendation deepens the cause.',
 'Cost per loan, substitution, licensing and exclusive reliance bear on the merits without being required by the inference.')
q('LL120','lsat_lr_assum','Sufficient assumption',4,
 "Regulator: A drug may be approved only if its benefits outweigh its risks for the population "
 "that will take it. This drug's benefits outweigh its risks for patients over sixty. It "
 "should therefore be approved.\n\n"
 "The regulator's conclusion follows logically if which one of the following is assumed?",
 ['The population that will take the drug consists of patients over sixty',
  'The drug carries fewer risks for patients over sixty than for younger patients',
  'No drug has been approved on the basis of benefits to a single age group',
  'Patients under sixty have alternative treatments available to them',
  'The benefits of the drug increase with the age of the patient'],
 'The rule quantifies over the population that will take the drug. The premise is about patients over sixty. Identifying the two makes the conclusion follow.',
 'Comparative risk, precedent, alternatives and an age trend all leave the populations unmatched.')

# ===================================================================== flaws
q('LL121','lsat_lr_flaw','Flaw',3,
 "Columnist: The mayor says the new stadium will create two thousand jobs. But the mayor's "
 "brother owns a construction firm that is bidding on the work. We should therefore reject "
 "the claim that the stadium will create two thousand jobs.\n\n"
 "The reasoning in the columnist's argument is flawed in that it",
 ['rejects a claim on the basis of the interests of the person making it rather than on the evidence for it',
  'treats a necessary condition for the stadium\'s approval as though it were a sufficient one',
  'assumes without warrant that the construction firm will win the contract it is bidding on',
  'draws a conclusion about the total number of jobs from evidence about construction jobs only',
  'fails to consider that the stadium might create jobs indirectly as well as directly'],
 'The interest may be a reason for scrutiny. It is not a reason the figure is wrong, and the columnist offers nothing else.',
 'No necessary and sufficient confusion, no assumption about the bid, and the argument makes no claim about job types or indirect effects.')
q('LL122','lsat_lr_flaw','Flaw',3,
 "Researcher: Countries with higher rates of tea drinking have lower rates of heart disease. "
 "Tea must therefore protect the heart.\n\n"
 "The researcher's reasoning is most vulnerable to criticism on the grounds that it",
 ['infers a causal relationship from a correlation without ruling out other differences between the countries',
  'relies on a sample of countries too small to support a general conclusion',
  'assumes that what is true of a country as a whole is true of each of its citizens',
  'confuses the rate of a disease with the number of people who have it',
  'treats the absence of evidence against a hypothesis as evidence for it'],
 'Countries differ in diet, income, health care and much else, any of which could produce the pattern. The argument does not address them.',
 'Sample size is not raised, no division fallacy is committed, rates are used consistently, and evidence is offered rather than absent.')
q('LL123','lsat_lr_flaw','Flaw',4,
 "Manager: Our best salespeople all make more than forty calls a week. If the rest of the "
 "team made forty calls a week, they would sell as much as our best people do.\n\n"
 "The manager's argument is flawed because it",
 ['treats a feature shared by successful salespeople as though it were what makes them successful',
  'assumes that the rest of the team is capable of making forty calls a week',
  'overlooks the possibility that some salespeople make more than forty calls',
  'relies on a definition of best salespeople that is not stated',
  'generalises from the sales team to the company as a whole'],
 'High call volume may be a consequence of skill, or a correlate of it. That the best all do it does not make it the cause of their results.',
 'Capability, the possibility in C, definitional vagueness and scope are not what the inference turns on.')
q('LL124','lsat_lr_flaw','Flaw',3,
 "Council member: Either we raise the transit fare or we cut service. Riders have made clear "
 "they will not accept a service cut. So we must raise the fare.\n\n"
 "The council member's reasoning is flawed in that it",
 ['presents two options as exhaustive without establishing that no others exist',
  'infers what riders will accept from what they have said they want',
  'assumes that a fare increase will produce the revenue the system needs',
  'fails to specify the size of the fare increase being proposed',
  'treats the preferences of riders as decisive on a question of policy'],
 'The argument runs on a disjunction it never defends. Subsidy, cost reduction and deferral are not addressed.',
 'The other options identify gaps that would matter only after the disjunction were granted.')
q('LL125','lsat_lr_flaw','Flaw',3,
 "Advertisement: More dentists recommend our toothpaste than any other brand. So our "
 "toothpaste is the most effective one available.\n\n"
 "The advertisement's reasoning is most vulnerable to the criticism that it",
 ['assumes that the recommendations of dentists track effectiveness rather than some other consideration',
  'fails to state how many dentists were asked for a recommendation',
  'ignores the possibility that dentists recommend more than one brand',
  'treats a claim about a plurality as though it were a claim about a majority',
  'provides no evidence that the dentists surveyed were selected at random'],
 'Dentists might recommend on price, availability, familiarity or a manufacturer relationship. The inference needs them to be recommending on effectiveness, which is not established.',
 'Sample size, multiple recommendations, plurality and selection all bear on the strength of the survey rather than on what a recommendation means.')
q('LL126','lsat_lr_flaw','Flaw',4,
 "Philosopher: Nothing that is truly beautiful requires explanation. This painting has been "
 "the subject of a hundred scholarly explanations. It is therefore not truly beautiful.\n\n"
 "The philosopher's argument is flawed in that it",
 ['confuses what a thing requires with what people have in fact produced concerning it',
  'relies on a notion of beauty that admits of degrees while treating it as absolute',
  'assumes that the scholarly explanations of the painting are correct',
  'draws a conclusion about a particular work from a claim about works in general',
  'fails to consider that a painting might be beautiful to some viewers and not to others'],
 'A hundred explanations show that people explained it, not that it required explaining. The premise is about necessity and the evidence is about occurrence.',
 'Degrees, correctness, the general to particular move and subjectivity are all real issues elsewhere and not the gap here.')
q('LL127','lsat_lr_flaw','Flaw',3,
 "Official: Critics say our inspection programme is ineffective because violations have not "
 "declined since it began. But violations would have risen sharply without the programme. "
 "The critics have no evidence that this is false.\n\n"
 "The official's reasoning is flawed because it",
 ['treats the absence of evidence against a claim as though it supported the claim',
  'attacks the critics rather than the substance of their objection',
  'assumes that the inspection programme was designed to reduce violations',
  'draws a conclusion about the future from evidence about the past',
  'confuses the number of violations with the number of inspections'],
 'That nobody has disproved the counterfactual is not a reason to believe it. The official offers no positive evidence at all.',
 'No personal attack, the design is common ground, no projection forward, and the counts are not conflated.')
q('LL128','lsat_lr_flaw','Parallel flaw',4,
 "Every member of the committee who voted against the proposal is a lawyer. Ruiz is a lawyer. "
 "So Ruiz voted against the proposal.\n\n"
 "Which one of the following arguments contains flawed reasoning most similar to that in the "
 "argument above?",
 ['Every building on the square that survived the fire is made of stone. The library is made of stone. So the library survived the fire.',
  'Every building on the square that survived the fire is made of stone. The library did not survive the fire. So the library is not made of stone.',
  'No building on the square that survived the fire is made of wood. The library is made of wood. So the library did not survive the fire.',
  'Every building made of stone on the square survived the fire. The library survived the fire. So the library is made of stone.',
  'Most buildings on the square that survived the fire are made of stone. The library is made of stone. So the library probably survived the fire.'],
 'The original affirms the consequent: all A are B, x is B, therefore x is A. A reproduces that exactly.',
 'B is a valid contrapositive, C is valid, D affirms the consequent in the other direction and is not the same form, and E is probabilistic rather than flawed in this way.')
q('LL129','lsat_lr_flaw','Flaw',3,
 "Developer: Residents object that the new tower will block their light. But the same "
 "residents objected to the last three buildings approved in the district, and none of those "
 "has caused the problems they predicted.\n\n"
 "The developer's reasoning is flawed in that it",
 ['treats the record of a group\'s past predictions as settling the merits of its present one',
  'assumes that the residents who object now are the same as those who objected before',
  'fails to establish that the previous buildings were of comparable height',
  'ignores the possibility that the earlier objections led to changes in those buildings',
  'concludes that a prediction is false merely because it has not yet been verified'],
 'Whether this tower blocks light is a question about this tower. A poor forecasting record gives reason for scepticism and is not an answer.',
 'B, C and D are all specific ways the analogy might fail, each of which matters only once the general move is granted; E misdescribes what the developer does.')
q('LL130','lsat_lr_flaw','Flaw',3,
 "Nutritional supplement label: In a study, participants who took our supplement reported "
 "more energy than participants who took nothing at all. The supplement therefore increases "
 "energy.\n\n"
 "The reasoning is most vulnerable to criticism on the grounds that it",
 ['fails to rule out that the reported difference was produced by the participants\' expectations',
  'relies on self reported energy rather than on a physiological measurement',
  'does not say how long the participants took the supplement',
  'assumes that all participants took the supplement as directed',
  'generalises from participants in a study to the population at large'],
 'A comparison against nothing rather than against a placebo leaves expectation as an untested explanation of a self reported outcome.',
 'B is close but is a feature of the outcome measure rather than the design gap; C, D and E are secondary.')
q('LL131','lsat_lr_flaw','Flaw',4,
 "Scientist: Either the sample was contaminated or the instrument was miscalibrated. We have "
 "confirmed that the instrument was miscalibrated. So the sample was not contaminated.\n\n"
 "The scientist's argument is flawed in that it",
 ['treats an or claim as though it excluded the possibility that both alternatives hold',
  'accepts the calibration record without independent verification',
  'assumes that a miscalibrated instrument produces results that are always wrong',
  'fails to consider explanations other than the two it names',
  'draws a conclusion about this sample from evidence about the instrument'],
 'Inclusive disjunction permits both. Confirming one disjunct does not rule the other out.',
 'Verification, the effect of miscalibration, further explanations and the subject of the evidence are not the error committed.')
q('LL132','lsat_lr_flaw','Flaw',3,
 "Principal: Our students' average mathematics score rose this year. The new curriculum is "
 "working.\n\n"
 "The principal's reasoning is most vulnerable to the criticism that it",
 ['overlooks the possibility that the composition of the student body changed between the two years',
  'assumes that mathematics is the subject in which improvement matters most',
  'treats an average as though it described every student',
  'fails to compare the school\'s results with those of other schools',
  'ignores the cost of introducing the new curriculum'],
 'An average over a different set of students can move without any student improving. That alone breaks the inference.',
 'Subject priority, the average as a description, comparisons and cost bear on the decision rather than on the causal claim.')
q('LL133','lsat_lr_flaw','Flaw',3,
 "Commentator: The minister claims the reforms will reduce waiting times. But the minister "
 "could not say last week how long the current waiting times are. The reforms will therefore "
 "not reduce waiting times.\n\n"
 "The commentator's reasoning is flawed because it",
 ['infers the falsity of a claim from a shortcoming in the person who made it',
  'assumes that the minister was being deliberately evasive',
  'treats current waiting times as the only measure of the system\'s performance',
  'concludes that a reform will fail without considering its details',
  'relies on a single occasion to establish a general pattern'],
 'Ignorance of the baseline is a reason to doubt the minister\'s command of the brief. It is not evidence about what the reforms will do.',
 'Evasion, the measure, the details and the single occasion each name a further weakness without identifying the move the argument makes.')
q('LL134','lsat_lr_flaw','Flaw',4,
 "Anthropologist: Societies that practise elaborate burial rites believe in an afterlife. The "
 "people of this valley buried their dead with grave goods and built substantial tombs. They "
 "therefore believed in an afterlife.\n\n"
 "A questionable aspect of the anthropologist's reasoning is that it",
 ['assumes that grave goods and substantial tombs constitute elaborate burial rites as the generalisation uses that term',
  'infers a belief held by individuals from a practice observed at the level of a society',
  'relies on archaeological evidence where written evidence would be more reliable',
  'does not establish that the tombs and the grave goods date from the same period',
  'takes for granted that every society with such a belief practises elaborate rites'],
 'The generalisation is about elaborate rites and the evidence is about two specific practices. Whether those amount to elaborate rites in the relevant sense is assumed.',
 'B is a real worry but is weaker here, C and D are evidentiary, and E reverses the conditional without being what the argument does.')
q('LL135','lsat_lr_flaw','Flaw',3,
 "Union representative: Management says it cannot afford the raise. But last year management "
 "said the same thing, and the company reported record profits. So the company can afford "
 "the raise this year.\n\n"
 "The representative's reasoning is flawed in that it",
 ['assumes that the company\'s position this year resembles its position last year',
  'confuses profit with the cash available to pay wages',
  'attacks management rather than the case management has made',
  'treats record profits as though they were unusually large profits',
  'fails to specify the size of the raise being sought'],
 'One year\'s record profits establish that the claim was wrong then. The argument needs this year to be relevantly like last year, which it does not show.',
 'B and D are quibbles about the financial terms, C misdescribes the move, and E is beside the point.')
q('LL136','lsat_lr_flaw','Parallel flaw',4,
 "If the shipment had arrived on time, the shelves would be full. The shelves are not full. "
 "So the shipment did not arrive on time. And since the shipment did not arrive on time, the "
 "driver must have taken the wrong route.\n\n"
 "The argument's reasoning is flawed in that it",
 ['establishes one possible cause of a delay and treats it as the only one',
  'infers a cause from an effect that could have been produced by that cause',
  'reverses a conditional in the course of drawing its first conclusion',
  'relies on a premise that contradicts one of its own conclusions',
  'treats a sufficient condition for full shelves as a necessary one'],
 'The first step is a valid contrapositive. The second jumps from a delay to one particular explanation of it without excluding any other.',
 'B describes the second step too weakly to be a flaw, and C, D and E misdescribe the first step, which is sound.')
q('LL137','lsat_lr_flaw','Flaw',3,
 "Journalist: The bridge inspection found no structural defects. The engineers who conducted "
 "it are employed by the authority that owns the bridge. The inspection is therefore "
 "worthless.\n\n"
 "The journalist's argument is flawed because it",
 ['moves from a reason to scrutinise a finding to the conclusion that the finding carries no weight',
  'assumes that the engineers were instructed to report no defects',
  'fails to consider that an independent inspection might reach the same finding',
  'treats the authority\'s ownership of the bridge as evidence of negligence',
  'generalises from one inspection to the authority\'s inspections as a whole'],
 'An interested inspector is a reason for a second opinion. Worthless is a much stronger claim and nothing supports it.',
 'B, C and D each assert something the journalist does not say, and E misstates the scope.')
q('LL138','lsat_lr_flaw','Flaw',3,
 "Buyer: This vineyard's wine won a gold medal in each of the last four years. Its wine is "
 "therefore better than that of the neighbouring vineyard, which has never won a medal.\n\n"
 "The buyer's reasoning is most vulnerable to criticism on the grounds that it",
 ['assumes that the neighbouring vineyard entered the competition',
  'treats the judgments of a competition as though they were unanimous',
  'relies on results from four years to draw a conclusion about the present',
  'fails to consider the price at which each vineyard sells its wine',
  'ignores the possibility that the two vineyards make different varieties'],
 'A vineyard that never entered cannot have won. The absence of a medal is then no evidence at all about its wine.',
 'Unanimity, recency, price and variety are secondary once the participation gap is seen.')
q('LL139','lsat_lr_flaw','Flaw',4,
 "Planner: Widening the motorway will not reduce congestion. Every previous widening in this "
 "region was followed within five years by traffic volumes as high as before.\n\n"
 "Which one of the following most accurately describes a flaw in the planner's reasoning?",
 ['It does not consider that congestion might have been worse still had the earlier widenings not taken place',
  'It assumes that the earlier widenings were of comparable scale to the one proposed',
  'It relies on a period of five years that is not shown to be the relevant one',
  'It treats traffic volume as equivalent to congestion',
  'It draws a conclusion about one region from evidence about several'],
 'Volumes returning to their previous level is consistent with the widening having prevented a much larger increase. The counterfactual is never addressed.',
 'B, C and D name assumptions worth examining, and E misdescribes the evidence, which is from this region.')
q('LL140','lsat_lr_flaw','Flaw',3,
 "Teacher: Students who read for pleasure write better essays. Requiring students to read a "
 "novel each month will therefore improve their essays.\n\n"
 "The teacher's reasoning is flawed in that it",
 ['overlooks the difference between reading chosen freely and reading that is required',
  'assumes that essay quality can be measured reliably',
  'fails to specify how long the novels should be',
  'generalises from students who read to students in general',
  'treats writing well as the only purpose of reading'],
 'The evidence is about reading for pleasure. A requirement produces reading, and whether it produces the thing the evidence is about is exactly what is skipped.',
 'Measurement, length, scope and purpose are all beside the substitution the argument makes.')

# ===================================================================== evidence
q('LL141','lsat_lr_evid','Weaken',3,
 "Hotel manager: Guests who book directly with us stay longer on average than guests who book "
 "through travel sites. We should therefore close our travel site listings and push all "
 "bookings to our own site.\n\n"
 "Which one of the following, if true, most weakens the manager's argument?",
 ['Guests who find the hotel on a travel site and then book directly are recorded as direct bookings',
  'The commission the hotel pays to travel sites has risen',
  'Some guests who book directly are members of the hotel\'s loyalty programme',
  'The hotel\'s own site is easier to use on a telephone',
  'Occupancy at the hotel is highest during the months'],
 'If travel sites are how long staying guests find the hotel, closing the listings removes the source of the very bookings the manager wants more of.',
 'Commission, loyalty membership, usability and seasonality leave the mechanism the plan relies on intact.')
q('LL142','lsat_lr_evid','Strengthen',3,
 "Botanist: The tree rings from this stand are unusually narrow for the years 1815 to 1817. "
 "The eruption of a large volcano in 1815 is the likely cause, since the ash it injected "
 "would have cooled the region.\n\n"
 "Which one of the following, if true, most strengthens the botanist's argument?",
 ['Stands of the same species several hundred kilometres away show narrow rings for the same three years',
  'The stand has produced narrow rings in several other years since 1817',
  'The trees in the stand were between forty and sixty years old in 1815',
  'Volcanic ash from large eruptions can remain in the stratosphere for more than a year',
  'Narrow rings in this species are usually caused by drought rather than by cold'],
 'A regional signal is what a hemispheric cooling would produce and a local cause would not. Independent stands showing the same three years is the strongest available confirmation.',
 'B weakens by showing the pattern is not special, C is background, D is already assumed by the argument, and E weakens it.')
q('LL143','lsat_lr_evid','Weaken',4,
 "Economist: Raising the minimum wage in this city did not reduce employment: the number of "
 "restaurant jobs in the city was the same a year after the increase as it was before.\n\n"
 "Which one of the following, if true, most weakens the economist's argument?",
 ['Restaurant employment in neighbouring cities without an increase rose by eight percent over the same year',
  'Some restaurants in the city raised their prices after the increase took effect',
  'The increase was phased in over eighteen months rather than applied at once',
  'Restaurant workers in the city had been paid above the old minimum on average',
  'The city\'s population grew slightly over the year in question'],
 'Flat against a rising counterfactual is a loss. The comparison the economist makes is with the city\'s own past rather than with what would otherwise have happened.',
 'Prices, phasing, prior wages and population growth are each consistent with the economist being right.')
q('LL144','lsat_lr_evid','Strengthen',3,
 "Physician: Patients given the new anaesthetic reported less nausea after surgery than "
 "patients given the standard one. The new anaesthetic therefore causes less nausea.\n\n"
 "Which one of the following, if true, most strengthens the physician's argument?",
 ['Patients were assigned to the two anaesthetics at random and neither they nor the recovery staff knew which was given',
  'The new anaesthetic has been in use in other countries for several years',
  'Nausea after surgery is among the complications patients most wish to avoid',
  'The standard anaesthetic is less expensive than the new one',
  'Some patients given the new anaesthetic reported no nausea at all'],
 'Randomisation removes selection and blinding removes expectation and reporting bias, which are the two ways the comparison could mislead.',
 'Prior use, patient preference, cost and the existence of nausea free patients do not bear on whether the comparison is sound.')
q('LL145','lsat_lr_evid','Weaken',3,
 "Publisher: Our audiobooks are narrated by the authors themselves. Listeners rate author "
 "narrated books more highly than books read by professional narrators, so we will continue "
 "the practice.\n\n"
 "Which one of the following, if true, most weakens the publisher's reasoning?",
 ['Authors narrate their own books mainly when they are already well known to readers',
  'Professional narrators can record a book in fewer sessions than most authors require',
  'Some listeners say they prefer a narrator whose voice they do not associate with the text',
  'Ratings of audiobooks have risen across the industry over the past five years',
  'The publisher\'s author narrated books are longer on average than its other titles'],
 'If fame selects which books get author narration, the ratings track the author\'s standing rather than the narration, and the practice is not what is being measured.',
 'Recording time, minority preferences, an industry trend and length do not touch the selection problem.')
q('LL146','lsat_lr_evid','Evaluate',4,
 "Farmer: Since we switched to no till planting, our soil holds more water and our yields "
 "have risen. Every farm in the district should switch.\n\n"
 "Which one of the following would be most useful to know in evaluating the farmer's "
 "recommendation?",
 ['Whether the soils on other farms in the district resemble those on this farm in the respects that make no till effective',
  'Whether the farmer received a subsidy for switching to no till planting',
  'How many years the farmer has been using the no till method',
  'Whether yields on this farm were rising before the switch',
  'What equipment is required to plant without tilling'],
 'The recommendation generalises from one farm to a district. Whether the relevant soil conditions carry over is what decides whether it should.',
 'D is a good question about the causal claim, but the recommendation to others turns on transferability; subsidy, duration and equipment bear on cost and confidence rather than on the generalisation.')
q('LL147','lsat_lr_evid','Strengthen',3,
 "Curator: This manuscript was probably copied in the northern scriptorium. Its parchment was "
 "prepared by a method used there and rarely elsewhere.\n\n"
 "Which one of the following, if true, most strengthens the curator's conclusion?",
 ['The ink used in the manuscript contains a mineral found only in the region of the northern scriptorium',
  'The northern scriptorium produced more manuscripts in this period than any other',
  'Parchment prepared by that method was traded over long distances during this period',
  'The manuscript\'s script resembles that of manuscripts from several scriptoria',
  'The northern scriptorium kept records of the manuscripts it produced'],
 'A second independent indicator pointing to the same place is what an argument from one indicator most needs.',
 'B is weak base rate support, C weakens the inference, D is neutral, and E matters only if the records were consulted.')
q('LL148','lsat_lr_evid','Weaken',3,
 "Safety officer: Since the warning signs were installed at the crossing, the number of "
 "collisions there has fallen by half. The signs are therefore working.\n\n"
 "Which one of the following, if true, most weakens the safety officer's argument?",
 ['A new bypass opened at the same time as the signs and carries most of the traffic that formerly used the crossing',
  'Two of the collisions that occurred after the signs were installed involved drivers from outside the area',
  'The signs are illuminated only between dusk and dawn',
  'Collisions at other crossings in the region have not fallen over the same period',
  'The signs cost more to install than the safety officer had estimated'],
 'Half the collisions with a fraction of the traffic is not an improvement in safety per crossing. The bypass supplies the whole of the change.',
 'B and C are details, D would strengthen, and cost is beside the point.')
q('LL149','lsat_lr_evid','Strengthen',4,
 "Zoologist: The birds on the island have shorter wings than those on the mainland. Since "
 "long wings are a disadvantage where strong winds can carry a bird out to sea, the "
 "difference is the result of selection rather than of diet or climate.\n\n"
 "Which one of the following, if true, most strengthens the zoologist's argument?",
 ['Island birds raised from eggs on the mainland grow wings as short as those of birds raised on the island',
  'The island is subject to strong winds during the season in which the birds breed',
  'Mainland birds occasionally fly to the island and back',
  'Wing length in this species varies more on the island than on the mainland',
  'The diet available on the island is similar to that available on the mainland'],
 'Short wings in birds raised in mainland conditions shows the trait is inherited rather than produced by the island environment, which is exactly what selection requires and diet or climate would not give.',
 'B supports the selective pressure without addressing heritability, C weakens by allowing gene flow, D is neutral, and E removes one rival explanation but not the climate one.')
q('LL150','lsat_lr_evid','Weaken',3,
 "Consultant: Firms that hold weekly all staff meetings report higher employee satisfaction "
 "than firms that do not. Your firm should institute weekly all staff meetings.\n\n"
 "Which one of the following, if true, most weakens the consultant's recommendation?",
 ['Firms adopt weekly all staff meetings only after satisfaction has already reached a level at which staff are willing to attend them',
  'Weekly meetings take an hour of each employee\'s time',
  'Some employees at firms with weekly meetings say they find them repetitive',
  'Employee satisfaction is measured by survey rather than by retention',
  'Your firm is smaller than most of the firms'],
 'If satisfaction is what makes the meetings possible rather than the reverse, instituting them in a firm without it does not import the result.',
 'Time cost, repetitiveness, the measure and firm size are each reasons for caution that leave the causal claim standing.')
q('LL151','lsat_lr_evid','Strengthen',3,
 "Detective: The intruder must have known the house. Nothing was disturbed except the drawer "
 "in which the jewellery was kept, and that drawer is not visible from the doorway.\n\n"
 "Which one of the following, if true, most strengthens the detective's conclusion?",
 ['The jewellery had been moved to that drawer from another room the week before',
  'The lock on the front door showed no sign of having been forced',
  'The drawer was the only one in the room that was unlocked',
  'Several other valuable items were kept in plain view elsewhere',
  'The intruder entered through a window at the back of the house'],
 'A recent move means the location was known only to people with current knowledge of the household, which is stronger than knowing the layout.',
 'B and E concern entry, C offers an innocent explanation for the choice of drawer, and D supports the conclusion only weakly.')
q('LL152','lsat_lr_evid','Weaken',4,
 "Historian: The plague cannot have caused the collapse of the city, because the population "
 "had already fallen by a third in the two decades before the plague arrived.\n\n"
 "Which one of the following, if true, most weakens the historian's argument?",
 ['A city weakened by a long decline is far less able to withstand a sudden loss of population than a stable one',
  'The plague reached the city later than it reached several neighbouring settlements',
  'Estimates of the city\'s population in the earlier period vary by as much as a fifth',
  'The city\'s decline in the earlier period was caused chiefly by emigration',
  'Some smaller towns in the region survived the plague without collapsing'],
 'The argument assumes a prior decline leaves no causal work for the plague. If decline is what makes a shock fatal, the two are complements rather than rivals.',
 'Timing, estimate uncertainty, the cause of the earlier decline and other towns do not address that assumption.')
q('LL153','lsat_lr_evid','Strengthen',3,
 "Engineer: The crack in the beam was caused by fatigue rather than by the impact. Fatigue "
 "cracks spread slowly and leave characteristic bands, and bands are visible on this "
 "fracture surface.\n\n"
 "Which one of the following, if true, most strengthens the engineer's conclusion?",
 ['Impacts of the kind that struck the beam do not produce bands on a fracture surface',
  'The beam was in service for eleven years before the crack was discovered',
  'Fatigue is the most common cause of failure in beams of this type',
  'The impact occurred within hours of the crack being discovered',
  'Bands on a fracture surface can sometimes be obscured by corrosion'],
 'The bands are evidence for fatigue only if the rival cause would not produce them. Ruling that out converts the sign into a discriminating one.',
 'Service life and base rates are weak support, D is neutral or slightly adverse, and E concerns the reliability of the sign\'s absence.')
q('LL154','lsat_lr_evid','Weaken',3,
 "School board member: The reading programme should be discontinued. Test scores at the three "
 "schools that adopted it have not risen since it began.\n\n"
 "Which one of the following, if true, most weakens the board member's argument?",
 ['The three schools that adopted the programme were the ones whose scores had been falling fastest',
  'The programme costs less per student than the materials it replaced',
  'Teachers at the three schools report that students enjoy the programme',
  'Scores at schools that did not adopt the programme also failed to rise',
  'The programme was designed for students in the earliest grades only'],
 'Selecting the fastest falling schools means holding steady is an improvement. The flat result is consistent with the programme working.',
 'Cost and enjoyment are other considerations, D strengthens rather than weakens, and E narrows the claim without rescuing it.')
q('LL155','lsat_lr_evid','Strengthen',3,
 "Archaeologist: The settlement was abandoned suddenly. Cooking pots were left on hearths and "
 "tools were left in the workshops.\n\n"
 "Which one of the following, if true, most strengthens the archaeologist's conclusion?",
 ['The pots and tools are of kinds that were valuable and difficult to replace',
  'The settlement was occupied for at least two centuries before it was abandoned',
  'Similar settlements in the region were abandoned within the same fifty year period',
  'The hearths show signs of having been used regularly over many years',
  'No human remains have been found within the settlement'],
 'People leaving in an orderly way take what is worth taking. Value is what makes abandonment of the objects evidence of haste.',
 'Duration of occupation, regional timing, hearth use and the absence of remains do not bear on whether the departure was sudden.')
q('LL156','lsat_lr_evid','Weaken',4,
 "Marketing director: Our television advertisements are working. Sales rose twelve percent in "
 "the four weeks after the campaign began.\n\n"
 "Which one of the following, if true, most weakens the director's argument?",
 ['The campaign began in the week the product was first stocked by the largest national retailer',
  'The campaign cost more than the gross margin on the additional units sold',
  'Sales in the four weeks before the campaign were lower than in the same period a year earlier',
  'Competing products were advertised on television during the same four weeks',
  'The advertisements were shown mainly during programmes watched by existing customers'],
 'A distribution change of that size explains the increase on its own, and it coincides exactly with the campaign.',
 'B concerns profitability rather than effect, C is weakly favourable to the director, and D and E raise doubts without supplying a rival cause.')
q('LL157','lsat_lr_evid','Strengthen',3,
 "Ecologist: Removing the deer from the island allowed the understorey to recover. Seedlings "
 "of five tree species reappeared within three years of the removal.\n\n"
 "Which one of the following, if true, most strengthens the ecologist's conclusion?",
 ['On a neighbouring island where the deer were not removed, no seedlings of those species appeared over the same three years',
  'The deer had been present on the island for more than fifty years',
  'The five species are among the most common trees in the region',
  'Rainfall over the three years was close to the long term average',
  'Seedlings of two other species did not reappear after the removal'],
 'A control island isolates the removal from anything else the three years brought. That is what the inference needs.',
 'Duration, commonness and average rainfall are background, and E is mildly adverse.')
q('LL158','lsat_lr_evid','Weaken',3,
 "Insurer: Drivers who install our monitoring device have fewer accidents than those who do "
 "not. The device makes drivers safer, so we will require it of all policyholders.\n\n"
 "Which one of the following, if true, most weakens the insurer's reasoning?",
 ['Drivers who volunteer to be monitored are those who already consider themselves careful',
  'The device records speed and braking but not the time of day',
  'Some drivers find the device distracting during the first weeks of use',
  'The discount offered to drivers who install the device exceeds its cost',
  'Accident rates have fallen among all drivers over the period studied'],
 'Volunteering selects the careful. Requiring the device of everyone imports the population it was never measured on.',
 'Recording limits, initial distraction, the discount and a general trend are each smaller problems.')
q('LL159','lsat_lr_evid','Evaluate',4,
 "Councillor: Installing solar panels on the town hall will pay for itself in nine years and "
 "the roof has at least twenty years of life left. We should install them.\n\n"
 "The answer to which one of the following would be most useful in evaluating the "
 "councillor's argument?",
 ['Whether the nine year figure assumes that the price the town pays for electricity stays at its present level',
  'Whether other buildings owned by the town have roofs suitable for panels',
  'Whether the panels would be visible from the square in front of the town hall',
  'How many years the town hall roof has been in place already',
  'Whether the town has borrowed money for capital projects in the past'],
 'The payback period is a function of avoided electricity cost. If it assumes a static price, the whole case rests on an assumption the question would expose.',
 'Other buildings, appearance, roof age and borrowing history do not bear on whether the figure is sound.')
q('LL160','lsat_lr_evid','Strengthen',3,
 "Linguist: The two languages are related. Their words for the numbers one through ten "
 "correspond in a regular pattern of sound changes.\n\n"
 "Which one of the following, if true, most strengthens the linguist's conclusion?",
 ['The same pattern of sound changes holds across several hundred words unrelated to counting',
  'Speakers of the two languages have traded with one another for centuries',
  'Numerals are among the words least often borrowed between languages',
  'The two languages share a similar word order in simple sentences',
  'Both languages are spoken in regions that were once part of the same empire'],
 'Regular correspondence across a large and varied vocabulary is the signature of common descent, which borrowing across ten words is not.',
 'C helps but is weaker, and trade, word order and shared political history each supply an alternative to descent or nothing at all.')

# ===================================================================== conclusions
q('LL161','lsat_lr_concl','Must be true',3,
 "Every violinist in the orchestra also plays in a chamber group. No member of a chamber "
 "group teaches at the conservatory. Alvarez teaches at the conservatory.\n\n"
 "If the statements above are true, which one of the following must also be true?",
 ['Alvarez is not a violinist in the orchestra',
  'Alvarez does not play the violin at all',
  'No violinist in the orchestra teaches anywhere',
  'Some members of chamber groups are violinists in the orchestra',
  'Every conservatory teacher is barred from joining a chamber group'],
 'Orchestra violinists are all in chamber groups, and nobody in a chamber group teaches at the conservatory. Alvarez teaches there, so Alvarez is not one of them.',
 'B overreaches from orchestra to instrument, C and E generalise beyond the premises, and D does not follow if the orchestra has no violinists.')
q('LL162','lsat_lr_concl','Must be true',3,
 "The library will extend its hours only if the council approves the budget. The council will "
 "approve the budget only if the audit is completed by June. The audit will not be completed "
 "by June.\n\n"
 "Which one of the following must be true?",
 ['The library will not extend its hours',
  'The council will reject the budget outright',
  'The audit will be completed at some point after June',
  'The library would have extended its hours had the audit been completed',
  'The council would have approved the budget had it wished to'],
 'Two chained necessary conditions fail at the far end, so the near end fails too.',
 'B is stronger than not approving, C adds a fact not given, and D and E reverse the conditionals.')
q('LL163','lsat_lr_concl','Most strongly supported',4,
 "In the decade after the tax on sugary drinks took effect, sales of those drinks in the city "
 "fell by a fifth while sales in the surrounding region were unchanged. Sales of bottled "
 "water in the city rose by about the same volume. Dental treatment rates among city children "
 "have not changed.\n\n"
 "The statements above most strongly support which one of the following?",
 ['The tax changed which drinks city residents bought without producing the health effect it was intended to produce',
  'The tax had no effect on what city residents drank',
  'City residents bought sugary drinks outside the city to avoid the tax',
  'Dental treatment rates are a poor measure of children\'s dental health',
  'Bottled water is as damaging to children\'s teeth as sugary drinks are'],
 'Substitution is established by the two sales figures against a stable regional comparison, and the dental figure shows the intended outcome did not follow.',
 'B contradicts the sales data, C is possible but unsupported, and D and E are speculative explanations rather than what the data supports.')
q('LL164','lsat_lr_concl','Main conclusion',3,
 "Some argue that the museum should return the bronzes because they were taken by force. That "
 "is true, but it is not the strongest reason. The strongest reason is that the objects mean "
 "something in the place they came from that they cannot mean here, and a museum exists to "
 "let objects mean something.\n\n"
 "Which one of the following most accurately expresses the main conclusion of the argument?",
 ['The best reason to return the bronzes is that they can carry their meaning only in their place of origin',
  'The bronzes were taken by force and should be returned',
  'A museum exists in order to let objects mean something to those who see them',
  'Arguments from the circumstances of acquisition are weaker than arguments from meaning',
  'The museum is not a suitable place to display the bronzes'],
 'The passage concedes the force argument and then names the strongest reason, which is the claim everything else supports.',
 'B is the conceded point, C is a premise, D is implied rather than asserted as the conclusion, and E is a consequence the passage does not draw.')
q('LL165','lsat_lr_concl','Must be true',3,
 "Every package that arrived on Tuesday was sent by express. Some packages sent by express "
 "were damaged in transit. No damaged package was accepted by the receiving clerk.\n\n"
 "Which one of the following must be true on the basis of the statements above?",
 ['If a package that arrived on Tuesday was damaged in transit, the receiving clerk did not accept it',
  'Some packages that arrived on Tuesday were damaged in transit',
  'Every package the receiving clerk accepted arrived on a day other than Tuesday',
  'No package sent by express was accepted by the receiving clerk',
  'Some packages sent by express arrived on a day other than Tuesday'],
 'The third premise applies to any damaged package, whenever it arrived.',
 'B, D and E assert existence or universality the premises do not give, and C does not follow at all.')
q('LL166','lsat_lr_concl','Most strongly supported',3,
 "A survey of household energy use found that homes with programmable thermostats used no "
 "less energy on average than homes without them. A separate study found that most owners of "
 "programmable thermostats had never changed the settings the device came with.\n\n"
 "The statements above most strongly support which one of the following?",
 ['The energy saving potential of programmable thermostats depends on their being configured, which most owners do not do',
  'Programmable thermostats are incapable of reducing household energy use',
  'Households that install programmable thermostats use more energy than they otherwise would',
  'Manufacturers set the default settings of programmable thermostats badly',
  'Most households would save energy by removing their programmable thermostats'],
 'The two findings fit together as a configuration problem: the device can save and is not being used in the way that saves.',
 'B and E go further than the data, C reverses it, and D is one explanation among several the data does not choose between.')
q('LL167','lsat_lr_concl','Must be true',4,
 "If the treaty is ratified, the tariffs will fall. If the tariffs fall, either exports will "
 "rise or domestic producers will lose market share. Domestic producers will not lose market "
 "share.\n\n"
 "If the statements above are true and the treaty is ratified, which one of the following "
 "must be true?",
 ['Exports will rise',
  'The tariffs will not fall',
  'Domestic producers will increase their market share',
  'Exports will rise only if the tariffs fall',
  'The treaty will be ratified only if exports rise'],
 'Ratification gives falling tariffs, which gives the disjunction, and the second disjunct is denied.',
 'B contradicts the chain, C is stronger than not losing share, and D and E state conditionals the premises do not support.')
q('LL168','lsat_lr_concl','Main conclusion',3,
 "Critics of the new pension rule say it will reduce saving. They point to the fall in "
 "contributions in the first quarter after the rule took effect. But contributions fall in "
 "the first quarter of every year, and this year's fall was smaller than usual. The critics "
 "have produced no evidence for their claim.\n\n"
 "Which one of the following most accurately states the main conclusion of the argument?",
 ['The critics have offered nothing that supports their claim about the rule',
  'The new pension rule will not reduce saving',
  'Contributions fall in the first quarter of every year',
  'This year\'s fall in contributions was smaller than usual',
  'The critics have misunderstood how the new pension rule works'],
 'The final sentence is what the seasonal facts are offered to establish, and it is a claim about their evidence rather than about the rule.',
 'B is stronger than what is argued, C and D are the premises, and E is never asserted.')
q('LL169','lsat_lr_concl','Most strongly supported',3,
 "Among the plays attributed to the dramatist, those written after 1605 use a vocabulary of "
 "roughly nine thousand distinct words, while those written before 1600 use roughly six "
 "thousand. The later plays are on average no longer than the earlier ones.\n\n"
 "The statements above most strongly support which one of the following?",
 ['The dramatist\'s later plays draw on a wider vocabulary than his earlier ones for works of similar length',
  'The dramatist learned three thousand new words between 1600 and 1605',
  'The later plays are more difficult for modern readers than the earlier ones',
  'Some of the plays attributed to the dramatist were written by someone else',
  'Vocabulary size is the best available test of when a play was written'],
 'Equal length with more distinct words is precisely a wider vocabulary per unit of text, which is what the two figures give.',
 'B is a specific mechanism, C concerns difficulty, D raises attribution, and E makes a methodological claim, none of which the data supports.')
q('LL170','lsat_lr_concl','Must be true',3,
 "No employee who works remotely attends the Monday briefing. Every employee on the product "
 "team attends the Monday briefing. Nakamura works remotely.\n\n"
 "Which one of the following must be true?",
 ['Nakamura is not on the product team',
  'Everyone who attends the Monday briefing is on the product team',
  'No employee on the product team works remotely on any day',
  'Some employees who work remotely are on the product team',
  'Nakamura attends a briefing on a day other than Monday'],
 'Product team members all attend; remote workers never do; Nakamura is remote.',
 'B reverses a conditional, C overstates it, D contradicts the premises, and E adds a fact not given.')
q('LL171','lsat_lr_concl','Most strongly supported',4,
 "Insurance claims for water damage in the district rose sharply in the year after the new "
 "drainage system was completed. The system was designed to handle the heaviest rainfall "
 "recorded in the previous fifty years, and no rainfall in the year in question exceeded half "
 "that level.\n\n"
 "The statements above most strongly support which one of the following?",
 ['The rise in claims was not caused by rainfall exceeding what the system was built for',
  'The drainage system was built to a lower standard than its design specified',
  'The new drainage system caused the increase in water damage',
  'Insurance claims for water damage are a reliable measure of water damage',
  'Rainfall in the district is becoming less predictable than it was'],
 'The two facts about rainfall and design capacity jointly exclude one explanation and say nothing about the others.',
 'B and C name particular explanations the facts do not establish, D is a methodological assumption, and E is unsupported.')
q('LL172','lsat_lr_concl','Main conclusion',3,
 "It is often said that a jury of ordinary citizens cannot understand expert testimony. The "
 "evidence does not bear this out. Studies comparing jury verdicts with the verdicts judges "
 "would have reached in the same cases find agreement in about four cases in five, and the "
 "disagreements are no more common in technical cases than in others.\n\n"
 "The main conclusion of the argument is that",
 ['the claim that juries cannot understand expert testimony is not supported by the evidence',
  'juries and judges agree in about four cases out of five',
  'juries understand expert testimony as well as judges do',
  'technical cases are no harder for juries than other cases',
  'the jury system should be retained in its present form'],
 'The second sentence states the conclusion and the studies are offered in support of it.',
 'B and D are the evidence, C is stronger than a claim about agreement rates, and E is a policy conclusion never drawn.')
q('LL173','lsat_lr_concl','Must be true',3,
 "All of the manuscripts in the collection that are dated were produced in the fifteenth "
 "century. Some manuscripts in the collection are illuminated. No illuminated manuscript in "
 "the collection is undated.\n\n"
 "Which one of the following must be true?",
 ['Some manuscripts in the collection were produced in the fifteenth century',
  'Every manuscript in the collection was produced in the fifteenth century',
  'All dated manuscripts in the collection are illuminated',
  'No undated manuscript in the collection was produced in the fifteenth century',
  'Most manuscripts in the collection are illuminated'],
 'Some are illuminated, none of those is undated, so some are dated, and all dated ones are fifteenth century.',
 'B and D go beyond the dated subset, C reverses the third premise, and E is a quantity claim the premises do not give.')
q('LL174','lsat_lr_concl','Most strongly supported',3,
 "Cities that introduced bicycle sharing schemes saw the number of cycling injuries rise. "
 "They also saw the number of cycling trips rise by a larger proportion than injuries did.\n\n"
 "The statements above most strongly support which one of the following?",
 ['Cycling in those cities became safer per trip even as the total number of injuries rose',
  'Bicycle sharing schemes make cycling more dangerous',
  'Most cycling injuries in those cities involved shared bicycles',
  'The rise in injuries would have been larger without the sharing schemes',
  'Cyclists using shared bicycles are more careful than other cyclists'],
 'Injuries rising more slowly than trips is a fall in injuries per trip, which is the rate that describes safety.',
 'B misreads the totals, C and E make claims about shared bicycles specifically, and D is a counterfactual the data does not support.')
q('LL175','lsat_lr_concl','Must be true',4,
 "If the compound is present, the solution turns blue. The solution turns blue only if the "
 "temperature is above twenty degrees. The temperature is eighteen degrees.\n\n"
 "Which one of the following must be true?",
 ['The compound is not present',
  'The solution is not blue and the compound is present',
  'Raising the temperature would turn the solution blue',
  'The solution turns blue whenever the temperature is above twenty degrees',
  'The compound is present only at temperatures above twenty degrees'],
 'Below twenty the solution cannot be blue, and the compound would make it blue, so the compound is absent.',
 'B is self contradictory given the premises, C and D reverse the second conditional, and E confuses a condition on the colour with one on the compound.')
q('LL176','lsat_lr_concl','Most strongly supported',3,
 "The factory installed sensors that stop a machine when a worker's hand approaches it. In "
 "the year after installation, reported hand injuries fell by two thirds, and reported near "
 "misses rose fourfold.\n\n"
 "Which one of the following is most strongly supported by the statements above?",
 ['The sensors are intervening in situations that previously produced injuries',
  'Workers have become less careful since the sensors were installed',
  'The sensors stop the machines more often than is necessary',
  'Near misses were underreported before the sensors were installed',
  'The factory will eliminate hand injuries entirely within a few years'],
 'A near miss is what an injury becomes when something intervenes, and the two figures move in exactly that pattern.',
 'B, C and D are possible explanations of part of the data, and E is a prediction the data does not license.')
q('LL177','lsat_lr_concl','Main conclusion',3,
 "The proposal would require every new building to include parking. Supporters say this "
 "prevents crowding on the streets. But parking requirements raise construction costs, and "
 "the cost is passed to tenants whether or not they own a car. A requirement that charges "
 "everyone for a service used by some is a poor way to allocate a scarce resource.\n\n"
 "Which one of the following most accurately expresses the main conclusion?",
 ['Requiring parking in every new building allocates a scarce resource poorly',
  'Parking requirements raise the cost of construction',
  'Tenants who do not own cars should not pay for parking',
  'Street crowding is not a serious problem in the district',
  'The proposal will not achieve what its supporters intend'],
 'The last sentence states the general principle as the verdict on the proposal, and the cost facts are what lead to it.',
 'B is a premise, C is implied but narrower, and D and E are not asserted.')
q('LL178','lsat_lr_concl','Must be true',3,
 "Whenever the ferry is cancelled, the road is closed or the sea is rough. The road was open "
 "all week. The ferry was cancelled on Thursday.\n\n"
 "Which one of the following must be true?",
 ['The sea was rough on Thursday',
  'The sea was rough all week',
  'The ferry ran on every day except Thursday',
  'The road is closed whenever the sea is rough',
  'The ferry is cancelled whenever the sea is rough'],
 'Cancellation requires one of two conditions; the road was open, so the other held.',
 'B, C, D and E each assert more than Thursday, or reverse the conditional.')
q('LL179','lsat_lr_concl','Most strongly supported',4,
 "Two groups of readers were given the same article. One group read it in a typeface designed "
 "to be slightly hard to read. That group scored higher on a test of recall a week later, but "
 "took longer to finish reading and reported enjoying the article less.\n\n"
 "The statements above most strongly support which one of the following?",
 ['The typeface that made reading harder improved recall at a cost in time and enjoyment',
  'Difficult typefaces should be used in textbooks',
  'Readers who enjoy an article remember less of it',
  'Recall a week later is the most important measure of reading',
  'The two groups differed in reading ability before the study began'],
 'All three findings are stated and the conclusion does no more than put them together as a tradeoff.',
 'B is a recommendation, C generalises a correlation, D ranks measures, and E contradicts the design as described.')
q('LL180','lsat_lr_concl','Must be true',3,
 "No document in the sealed file has been read by anyone outside the ministry. Some documents "
 "in the sealed file were written by the ambassador. Everything the ambassador wrote in that "
 "year was read by the foreign press.\n\n"
 "Which one of the following must be true?",
 ['Some documents written by the ambassador were not written in that year',
  'The foreign press has read documents in the sealed file',
  'The ambassador wrote nothing in that year',
  'Everything in the sealed file was written by the ambassador',
  'The foreign press is not outside the ministry'],
 'Sealed file documents by the ambassador are unread outside the ministry, so they cannot be among the things read by the foreign press, so they were not written in that year.',
 'B contradicts the first premise, C and D are stronger than the premises allow, and E is an unmotivated escape.')

# ===================================================================== structure
q('LL181','lsat_lr_struct','Role of a claim',3,
 "Planner: The bus route should not be extended to the industrial park. Extending it would "
 "add eleven minutes to every trip on the route. It is true that the park employs four "
 "hundred people. But fewer than thirty of them live along the route, and the eleven minutes "
 "would be borne by two thousand daily riders.\n\n"
 "The claim that the park employs four hundred people plays which one of the following roles "
 "in the planner's argument?",
 ['It is a point granted to the other side, which the planner then argues is outweighed',
  'It is the main conclusion the planner\'s other statements are offered to support',
  'It is evidence that the extension would benefit a substantial number of riders',
  'It is an assumption the planner must make in order to compare the two groups',
  'It is a claim the planner goes on to show is false'],
 'The phrase It is true that marks a concession, and the next sentence gives the reason it does not settle the matter.',
 'B and C misplace it, D calls a stated fact an assumption, and the planner never denies it.')
q('LL182','lsat_lr_struct','Method of argument',3,
 "Physician: You say that because the trial found no benefit, the treatment does not work. "
 "But the trial enrolled forty patients. A trial that size would miss a benefit of the "
 "magnitude this treatment is expected to produce more often than not.\n\n"
 "The physician responds to the objection by",
 ['arguing that the study cited is too small to detect the effect at issue',
  'presenting a study that reached the opposite conclusion',
  'questioning the motives of those who conducted the trial',
  'showing that the treatment has worked for particular patients',
  'pointing out that the objection assumes what it sets out to prove'],
 'The reply is entirely about statistical power: forty patients would miss an effect of this size most of the time.',
 'No second study, no attack on motives, no anecdote, and no charge of circularity.')
q('LL183','lsat_lr_struct','Point at issue',4,
 "Ferrand: Public money should support only art that a broad public wants to see. Otherwise "
 "taxpayers are funding the tastes of a few.\n"
 "Iqbal: Public money supports research whose value no broad public can judge in advance. "
 "Art is no different.\n\n"
 "Ferrand and Iqbal disagree about whether",
 ['popular demand is the right test for what public money should support',
  'taxpayers should have any say in how public money is spent',
  'scientific research is a good use of public money',
  'the public is capable of judging the value of contemporary art',
  'art and research are funded from the same public budgets'],
 'Ferrand proposes broad demand as the criterion and Iqbal offers a case where it plainly does not apply, which is a denial of the criterion.',
 'Neither addresses B or E; Iqbal treats research funding as common ground rather than arguing for it; and D is not what either says.')
q('LL184','lsat_lr_struct','Role of a claim',3,
 "Editor: Our readers complain that the paper covers national politics at the expense of "
 "local news. Circulation is falling. Papers that expanded local coverage in comparable "
 "towns have held their circulation. We should expand local coverage.\n\n"
 "The claim that circulation is falling plays which one of the following roles?",
 ['It states the problem the recommended course of action is meant to address',
  'It is the main conclusion of the argument',
  'It is offered as evidence that readers prefer local news',
  'It is a concession to a view the editor rejects',
  'It explains why comparable towns expanded their local coverage'],
 'The recommendation is a remedy, and the falling circulation is what it is a remedy for.',
 'The recommendation is the conclusion, the complaint is the evidence about preference, nothing is conceded, and the other towns\' motives are not discussed.')
q('LL185','lsat_lr_struct','Argument structure',4,
 "The company's losses are usually blamed on the strike. But the losses began two quarters "
 "before the strike and continued at the same rate throughout it. The strike may have "
 "prevented a recovery, but it did not cause the losses.\n\n"
 "The argument proceeds by",
 ['using the timing of an outcome to rule out a proposed cause while allowing it a lesser role',
  'showing that the proposed cause and the outcome are unrelated',
  'offering an alternative explanation that fits the evidence better',
  'demonstrating that the usual account rests on a confusion of terms',
  'conceding the main point while disputing a subsidiary one'],
 'Onset before the strike is what rules out causation, and the concession about recovery is exactly the lesser role.',
 'B ignores the concession, C offers no alternative, D names no confusion, and E reverses which point is conceded.')
q('LL186','lsat_lr_struct','Role of a claim',3,
 "Geologist: Some say the boulders were carried here by a glacier. The nearest glaciated "
 "terrain is four hundred kilometres away, which is far but not impossible for ice to carry "
 "rock. The decisive point is that the boulders match bedrock exposed two kilometres "
 "upstream.\n\n"
 "The statement that four hundred kilometres is far but not impossible for ice to carry rock "
 "serves to",
 ['set aside an objection that would otherwise do the work the geologist wants done differently',
  'establish that the glacial account is the more likely of the two',
  'introduce the evidence on which the geologist\'s conclusion rests',
  'concede that the boulders may have been carried by a glacier after all',
  'question whether the nearest glaciated terrain has been correctly identified'],
 'The geologist declines to rest on distance, which clears the ground for the decisive point about the bedrock match.',
 'It does not favour the glacial account, the decisive evidence is the next sentence, it concedes possibility rather than the conclusion, and the terrain is not questioned.')
q('LL187','lsat_lr_struct','Method of argument',3,
 "Defence counsel: The prosecution says my client was seen leaving the building at nine. The "
 "witness who says so also testified that the street was unlit and that she was forty metres "
 "away.\n\n"
 "The counsel's argument proceeds by",
 ['drawing on the witness\'s own testimony to cast doubt on what she reported',
  'presenting a second witness whose account conflicts with the first',
  'establishing that the client was elsewhere at the time in question',
  'arguing that the prosecution has misquoted its own witness',
  'showing that the witness has a reason to testify against the client'],
 'Both the darkness and the distance come from the same witness, and they undercut the identification without contradicting her.',
 'No second witness, no alibi, no misquotation and no motive is alleged.')
q('LL188','lsat_lr_struct','Point at issue',3,
 "Okoro: Remote work makes new employees less productive, because they learn the job by "
 "watching colleagues.\n"
 "Baptiste: New employees at our firm learned faster after we moved to remote work, because "
 "we finally wrote the procedures down.\n\n"
 "Okoro and Baptiste disagree over whether",
 ['learning by watching colleagues is necessary for new employees to come up to speed',
  'remote work reduces the productivity of experienced employees',
  'written procedures are useful to new employees',
  'the firm should return its employees to the office',
  'new employees at their firm are productive'],
 'Okoro treats observation as the mechanism of learning, and Baptiste offers a case where a substitute worked, which denies its necessity.',
 'Experienced employees, the usefulness of documents, the return to office and current productivity are each outside what both address.')
q('LL189','lsat_lr_struct','Role of a claim',4,
 "Reviewer: The novel has been praised for its historical accuracy. Accuracy is not nothing. "
 "But a novel that gets every detail right and never makes a reader care about anyone in it "
 "has failed at the thing novels are for.\n\n"
 "The statement that accuracy is not nothing functions in the argument to",
 ['acknowledge a merit of the novel before subordinating it to a standard the reviewer takes to be more important',
  'introduce the criterion by which the reviewer will judge the novel',
  'summarise the praise the novel has received from other critics',
  'suggest that the novel\'s accuracy has been overstated',
  'state the conclusion for which the rest of the passage argues'],
 'It grants the merit and the next sentence sets it below the standard the reviewer applies.',
 'The criterion arrives in the last sentence, the praise is the previous sentence, accuracy is not disputed, and the conclusion is the failure claim.')
q('LL190','lsat_lr_struct','Method of argument',3,
 "Architect: You object that the design is out of keeping with the street. Every building on "
 "this street was out of keeping with it when it was built, including the one you live "
 "in.\n\n"
 "The architect responds to the objection by",
 ['showing that the standard the objection applies would have excluded what the objector values',
  'arguing that the objector has misunderstood the design',
  'denying that the design departs from the character of the street',
  'claiming that the character of a street cannot be defined',
  'appealing to the judgment of professionals rather than residents'],
 'The reply turns the criterion on the objector\'s own house, which is a reductio of the standard rather than a defence of the design.',
 'The design is not defended on its merits, the departure is conceded, no definitional claim is made, and no appeal to expertise appears.')
q('LL191','lsat_lr_struct','Argument structure',3,
 "Few doubt that the vaccine works. The question is whether requiring it is justified. A "
 "requirement is justified when the harm prevented to others is substantial and no lesser "
 "measure would achieve it. Both conditions hold here.\n\n"
 "The argument proceeds by",
 ['setting aside one question, stating a standard for a second, and asserting that the standard is met',
  'establishing that the vaccine works and inferring that a requirement is justified',
  'considering two possible standards and choosing between them',
  'refuting an objection and then offering positive evidence',
  'deriving a general principle from a particular case'],
 'Efficacy is put aside, the two part standard is stated, and the last sentence claims it is satisfied.',
 'B misstates the inference, only one standard is given, nothing is refuted, and the movement is from principle to case.')
q('LL192','lsat_lr_struct','Role of a claim',3,
 "Auditor: The department says the overspend was caused by unexpected fuel prices. Fuel "
 "prices did rise. But fuel is four percent of the department's budget, and the overspend was "
 "nineteen percent.\n\n"
 "The statement that fuel prices did rise plays which one of the following roles?",
 ['It grants the factual basis of an explanation the auditor goes on to show is inadequate',
  'It is the conclusion the auditor draws from the budget figures',
  'It is evidence that the department\'s explanation is correct',
  'It is an assumption the auditor makes for the sake of argument only',
  'It identifies the cause of the overspend the auditor eventually accepts'],
 'The rise is conceded as true and the arithmetic then shows it cannot account for the size of the overspend.',
 'It is not a conclusion, it does not support the department once the arithmetic is in, it is asserted rather than supposed, and no cause is accepted.')
q('LL193','lsat_lr_struct','Method of argument',4,
 "Historian: My colleague argues that the letters are forgeries because they use a word not "
 "otherwise recorded before 1750. The same word appears in a parish register of 1698 that my "
 "colleague has himself cited in print.\n\n"
 "The historian counters the colleague's argument by",
 ['producing a counterexample to the factual premise on which it rests',
  'showing that the colleague\'s conclusion does not follow from his premises',
  'arguing that the standard the colleague applies is too strict',
  'questioning whether the parish register has been correctly dated',
  'suggesting that the colleague has a stake in the letters being forgeries'],
 'The premise is that the word is not recorded before 1750, and the register of 1698 is a direct counterexample to it.',
 'The inference is not challenged, no standard is discussed, the register is relied on rather than doubted, and no motive is raised.')
q('LL194','lsat_lr_struct','Point at issue',3,
 "Delacroix: A biography should tell us what its subject did, not speculate about what he "
 "felt.\n"
 "Whitlock: What a person did is unintelligible without some account of why, and why is a "
 "matter of what he felt.\n\n"
 "The exchange most supports the claim that they disagree about whether",
 ['an account of a subject\'s inner life belongs in a biography of him',
  'biographers are capable of knowing what their subjects felt',
  'the subject of a biography deserves privacy about his feelings',
  'most biographies published today speculate too much',
  'a biography should explain its subject\'s actions at all'],
 'Delacroix excludes the inner life and Whitlock makes it necessary to the task, which is a direct clash.',
 'Capability, privacy and current practice are not addressed, and Delacroix does not deny that actions should be reported.')
q('LL195','lsat_lr_struct','Role of a claim',3,
 "Dietitian: Oat bran was once said to lower cholesterol dramatically. The studies behind "
 "that claim compared oat bran with nothing rather than with other fibre. Oat bran is "
 "perfectly good food. It is not medicine.\n\n"
 "The statement that oat bran is perfectly good food serves to",
 ['prevent the criticism of the studies from being read as an attack on the food itself',
  'provide the evidence for the conclusion that oat bran is not medicine',
  'concede that the original studies reached the right conclusion',
  'introduce a comparison between oat bran and other sources of fibre',
  'state the main conclusion of the dietitian\'s argument'],
 'It is a clarification of scope: the target is the medical claim, not the food, and the sentence marks that boundary.',
 'It is not evidence, it concedes nothing about the studies, the fibre comparison is earlier, and the conclusion is the last sentence.')
q('LL196','lsat_lr_struct','Method of argument',3,
 "Engineer: The report recommends replacing the pumps because two failed last year. Two out "
 "of ninety is within the failure rate the manufacturer publishes and within the rate we have "
 "seen in every year since installation.\n\n"
 "The engineer's argument proceeds by",
 ['placing the cited events in a context that shows them to be unremarkable',
  'denying that the two pumps failed as the report describes',
  'arguing that replacing the pumps would cost more than it saves',
  'identifying an error in the manufacturer\'s published failure rate',
  'proposing an alternative explanation for the two failures'],
 'The failures are granted and the two comparisons, published rate and own history, make the number ordinary rather than alarming.',
 'The failures are not denied, no cost argument appears, the published rate is relied on, and no alternative explanation is offered.')
q('LL197','lsat_lr_struct','Argument structure',4,
 "Two explanations of the decline have been offered: the new predator and the loss of nesting "
 "sites. The predator arrived in 2019 and the decline began in 2014. Nesting sites have been "
 "lost steadily since the 1990s, and the decline tracks that loss closely in every region "
 "where both have been measured.\n\n"
 "The argument proceeds by",
 ['eliminating one candidate explanation on the timing and supporting the other with a fit across regions',
  'showing that the two explanations are compatible and both contribute',
  'establishing that neither explanation accounts for the decline',
  'arguing that the decline began earlier than had been supposed',
  'questioning the measurements on which the predator explanation rests'],
 'The 2019 arrival cannot explain a decline from 2014, and the regional tracking is positive support for the other.',
 'The predator is excluded rather than combined, one explanation is supported, the start date is given rather than argued for, and the measurements are used rather than doubted.')
q('LL198','lsat_lr_struct','Role of a claim',3,
 "Coach: Our opponents have lost four matches in a row. That is the sort of fact that makes a "
 "team dangerous rather than weak: they will be better prepared for us than any side we have "
 "met this season.\n\n"
 "The claim that the opponents have lost four matches in a row functions in the argument as",
 ['a fact whose usual significance the coach argues is the opposite of what it appears to be',
  'the main conclusion the coach draws about the coming match',
  'evidence that the opponents are a weaker side than they were',
  'an assumption the coach makes without supporting it',
  'a concession that the coach immediately withdraws'],
 'The losing run is taken as given and reinterpreted: it is offered as a reason for concern rather than comfort.',
 'It is a premise rather than the conclusion, the coach denies it shows weakness, it is stated as fact, and nothing is withdrawn.')
q('LL199','lsat_lr_struct','Method of argument',3,
 "Legislator: The bill is said to be unenforceable. Every consumer protection statute we have "
 "passed in thirty years was called unenforceable when it was introduced, and each is "
 "enforced today.\n\n"
 "The legislator's response is most vulnerable to the criticism that it",
 ['does not address any feature of this bill that might make it unenforceable',
  'assumes that consumer protection statutes are the only relevant comparison',
  'relies on a period of thirty years without justifying that choice',
  'treats enforcement and enforceability as the same thing',
  'fails to name the people who called the earlier statutes unenforceable'],
 'The track record establishes that the objection has been wrong before, which is not an answer to the objection as made about this bill.',
 'B, C, D and E are narrower complaints about the comparison rather than the reason it does not answer the charge.')
q('LL200','lsat_lr_struct','Role of a claim',4,
 "Curator: Attributing the drawing to the workshop rather than the master would lower its "
 "value considerably. That is a reason to examine the attribution carefully. It is not a "
 "reason to reach one conclusion rather than the other.\n\n"
 "The statement that attributing the drawing to the workshop would lower its value plays "
 "which one of the following roles?",
 ['It is a consideration the curator says bears on how the question should be investigated but not on how it should be answered',
  'It is the main conclusion the curator defends',
  'It is evidence that the drawing is by the master rather than the workshop',
  'It is an objection the curator goes on to refute',
  'It is an assumption the curator accepts only for the sake of argument'],
 'The two following sentences say exactly this: a reason for care, not a reason for a verdict.',
 'It is not the conclusion, it is not evidence for either attribution, no objection is refuted, and it is asserted outright.')

# ===================================================================== principles
q('LL201','lsat_lr_prin','Identify the principle',3,
 "A shop advertised a coat at half price. When a customer arrived, the shop said the sale had "
 "ended that morning but offered the coat at a quarter off. The shop had not updated its "
 "window. The shop should honour the advertised price.\n\n"
 "Which one of the following principles most helps to justify the conclusion?",
 ['A seller who leaves an offer on display is bound by it until the display is withdrawn',
  'A seller must give notice before changing the price of any advertised item',
  'A customer who relies on an advertisement is entitled to compensation for the journey',
  'A sale price must remain available for a reasonable period after it is advertised',
  'A seller may not offer a discount smaller than the one advertised'],
 'The shop\'s failure to remove the display is what the case turns on, and this principle makes the display binding while it stands.',
 'B is about notice, C about compensation, D about duration and E about the size of the offer, none of which matches the facts as given.')
q('LL202','lsat_lr_prin','Apply a principle',3,
 "Principle: A person who benefits from another's mistake should return the benefit if the "
 "mistake was one the person could easily have pointed out at the time.\n\n"
 "Which one of the following judgments most closely conforms to the principle?",
 ['Marchetti, who noticed that the cashier had charged for one book instead of two but said nothing, should pay for the second book',
  'Oyelaran, who was given the wrong change in a currency she does not read, need not return the difference',
  'Petrov, who found a wallet in the street and handed it to the police, should be rewarded',
  'Quinn, whose neighbour built a fence on Quinn\'s land by mistake, should pay for the fence',
  'Sandoval, who was overcharged and did not notice, should be refunded the difference'],
 'Noticing at the time is precisely the condition, and Marchetti did notice and stayed silent.',
 'B is a correct application of the exception rather than the principle, C, D and E concern situations the principle does not govern.')
q('LL203','lsat_lr_prin','Identify the principle',4,
 "The researcher declined to publish the finding because the sample had been collected by a "
 "method she had criticised in print two years earlier. Her colleagues thought this "
 "excessive, since the finding would probably have held under any method. She was right to "
 "decline.\n\n"
 "Which one of the following principles most helps to justify the researcher's decision?",
 ['One should not rely on a method one has publicly argued to be unsound, even where the result would likely survive a sound method',
  'A researcher should publish only findings that have been replicated by an independent team',
  'A finding obtained by an unsound method is more likely to be false than one obtained by a sound method',
  'One should not criticise in print a method one may later need to use',
  'A researcher\'s past publications should not constrain her present choices'],
 'The distinctive fact is the public criticism, and the principle makes consistency binding regardless of how the result would have come out.',
 'B imposes replication, C is a probabilistic claim the colleagues already dispute, D reverses the lesson, and E contradicts the decision.')
q('LL204','lsat_lr_prin','Apply a principle',3,
 "Principle: An institution that solicits donations for a stated purpose must use them for "
 "that purpose or return them.\n\n"
 "Which one of the following judgments most closely conforms to the principle?",
 ['A hospital that raised money for a scanner it then decided not to buy must offer the money back to the donors',
  'A hospital that raised money for a scanner may spend the surplus on staff training',
  'A hospital that raised money without stating a purpose must spend it on patient care',
  'A hospital that bought a scanner from general funds may keep donations raised afterwards',
  'A hospital may solicit donations for a purpose it has not yet decided to pursue'],
 'Abandoning the stated purpose triggers the alternative the principle gives, which is return.',
 'B diverts funds, C adds a duty the principle does not state, D is not addressed, and E concerns solicitation rather than use.')
q('LL205','lsat_lr_prin','Parallel principle',4,
 "A referee should not officiate a match involving a club she once played for, even if she "
 "is confident of her impartiality, because the appearance of partiality damages the game.\n\n"
 "Which one of the following most closely conforms to the principle underlying the argument "
 "above?",
 ['A judge should not hear a case brought by a former law partner, however sure he is of his own neutrality, because public confidence in the courts would suffer',
  'A referee who makes a mistake should acknowledge it after the match rather than during it',
  'A judge should recuse himself from a case in which he holds a financial interest, because he might decide it wrongly',
  'A teacher should not grade the work of a relative, because she would be unable to judge it fairly',
  'A journalist should disclose any payment received from a subject she writes about'],
 'The structure is: appearance matters independently of actual impartiality, and the harm is to confidence in the institution. A reproduces both.',
 'C and D rest the duty on the risk of a wrong decision, which is the reasoning the original expressly sets aside; B and E are different duties.')
q('LL206','lsat_lr_prin','Identify the principle',3,
 "The airline rebooked the passenger on a later flight without telling her and she missed a "
 "connection. The airline says its terms allow it to change bookings. The airline still owes "
 "her the cost of the missed connection.\n\n"
 "Which one of the following principles most helps to justify the conclusion?",
 ['A party entitled to change an arrangement must give notice in time for the other party to adjust',
  'A party may not change an arrangement once the other party has relied on it',
  'Terms of service are unenforceable unless the customer has read them',
  'A party that causes a loss must compensate it regardless of what its terms provide',
  'A customer who books a connection assumes the risk that it will be missed'],
 'The airline\'s right to change is conceded, so the ground of liability must be the failure to notify, which this principle supplies.',
 'B denies the conceded right, C and D are far broader than the case needs, and E contradicts the conclusion.')
q('LL207','lsat_lr_prin','Apply a principle',3,
 "Principle: A person should be praised for an act only if she could have chosen not to do "
 "it.\n\n"
 "The principle, if valid, most helps to justify the reasoning in which one of the following?",
 ['The clerk deserves no praise for reporting the theft, since the law required her to report it and she would have been prosecuted otherwise',
  'The clerk deserves praise for reporting the theft, since reporting it took considerable courage',
  'The clerk deserves no praise for reporting the theft, since she had no evidence that a theft had occurred',
  'The clerk deserves praise for reporting the theft, since the report led to the recovery of the money',
  'The clerk deserves no praise for reporting the theft, since she did not report it promptly'],
 'The principle makes the availability of an alternative necessary, and compulsion under threat of prosecution is what removes it.',
 'B, C, D and E turn on courage, evidence, outcome and timing, none of which the principle addresses.')
q('LL208','lsat_lr_prin','Identify the principle',4,
 "The newspaper published the leaked memorandum. Its editor knew the leak would cost the "
 "source her job. The memorandum showed that a regulator had suppressed a safety report. The "
 "newspaper was right to publish.\n\n"
 "Which one of the following principles most helps to justify the newspaper's decision?",
 ['Publication is warranted where it exposes a serious failure of a body the public depends on, even at a substantial cost to an individual',
  'A newspaper should publish any document that comes into its possession lawfully',
  'A newspaper owes no duty to a source who chooses to leak a document',
  'A newspaper should not publish a leaked document unless it has verified its contents independently',
  'The public interest in safety outweighs every competing consideration'],
 'The case pairs a serious institutional failure with a known personal cost, and the principle weighs exactly those two.',
 'B is too permissive, C dismisses the cost rather than weighing it, D would count against publishing here, and E is too strong to be plausible.')
q('LL209','lsat_lr_prin','Apply a principle',3,
 "Principle: A rule adopted to prevent a particular harm should not be applied where that "
 "harm cannot occur.\n\n"
 "Which one of the following judgments most closely conforms to the principle?",
 ['A prohibition on open flames in the archive, adopted to protect the paper records, need not apply in the digital reading room where no paper is kept',
  'A prohibition on open flames in the archive should be extended to the digital reading room for the sake of consistency',
  'A prohibition on food in the archive should be relaxed because staff find it inconvenient',
  'A prohibition on open flames should be replaced by a requirement that fire extinguishers be provided',
  'A prohibition on open flames in the archive should be enforced more strictly during the winter'],
 'The rule\'s purpose is protecting paper, and a room with no paper is precisely where the harm cannot occur.',
 'B extends rather than limits, C appeals to convenience, D substitutes a different rule, and E varies enforcement.')
q('LL210','lsat_lr_prin','Identify the principle',3,
 "The tenant painted the flat without permission. The landlord says the lease forbids "
 "alterations. The paint improved the flat and the landlord relet it at a higher rent without "
 "repainting. The landlord should not charge the tenant for restoring the original "
 "colour.\n\n"
 "Which one of the following principles most helps to justify the conclusion?",
 ['A party may not recover the cost of undoing a change from which it has instead chosen to benefit',
  'A tenant who improves a property is entitled to a share of the increased rent',
  'A lease term is unenforceable if the landlord does not enforce it immediately',
  'A party may recover only losses that were foreseeable when the agreement was made',
  'A tenant may alter a property where the alteration is an improvement'],
 'The landlord kept the paint and raised the rent, so the restoration cost was never incurred and is not recoverable on this principle.',
 'B claims a share, C is about waiver generally, D is a remoteness rule, and E rewrites the lease.')
q('LL211','lsat_lr_prin','Apply a principle',4,
 "Principle: One may break a minor rule in order to prevent a much greater harm, provided no "
 "lawful means of preventing that harm was available.\n\n"
 "Which one of the following judgments most closely conforms to the principle?",
 ['A driver who crossed a solid line to avoid a child who had run into the road, with no room to stop, acted permissibly',
  'A driver who crossed a solid line to reach a hospital, having decided not to call an ambulance, acted permissibly',
  'A driver who crossed a solid line because the road was empty acted permissibly',
  'A driver who crossed a solid line to avoid a child and was not seen by any other driver acted permissibly',
  'A driver who crossed a solid line and caused no accident acted permissibly'],
 'A greater harm, a minor rule and no alternative are all present: there was no room to stop.',
 'B had a lawful means available, C names no harm, and D and E rest on being unobserved or lucky rather than on the principle.')
q('LL212','lsat_lr_prin','Identify the principle',3,
 "The committee rejected the grant application because the applicant had failed to disclose a "
 "previous award for closely related work. The application was otherwise the strongest "
 "submitted. The committee acted correctly.\n\n"
 "Which one of the following principles most helps to justify the committee's decision?",
 ['An applicant\'s failure to disclose material information is a sufficient ground for rejection whatever the merits of the application',
  'A committee should fund the strongest application it receives',
  'An applicant who has received a previous award should not receive a second one for related work',
  'A committee should reject any application it cannot verify in full',
  'An applicant who fails to disclose information should be given an opportunity to correct the omission'],
 'The decision turns on non disclosure overriding merit, and the principle says exactly that.',
 'B would reverse the decision, C makes the prior award rather than the concealment decisive, D is far broader, and E recommends a different course.')
q('LL213','lsat_lr_prin','Apply a principle',3,
 "Principle: A professional should not accept work she lacks the competence to perform, even "
 "where the client understands the limits of her experience.\n\n"
 "The principle most helps to justify which one of the following judgments?",
 ['The surveyor should have declined the marine survey despite telling the owner she had never surveyed a vessel',
  'The surveyor was entitled to accept the marine survey because the owner knew her experience was limited',
  'The surveyor should have charged less for the marine survey than an experienced surveyor would',
  'The surveyor should have declined the marine survey because the owner was not told her experience was limited',
  'The surveyor was entitled to accept the marine survey because no experienced surveyor was available'],
 'The principle makes the client\'s understanding irrelevant, which is the distinctive feature of the case as stated.',
 'B and E rely on consent and necessity, C is about fees, and D makes disclosure decisive when the principle says it is not.')
q('LL214','lsat_lr_prin','Parallel principle',4,
 "A government should not fund a project whose benefits accrue entirely to those already able "
 "to pay for it, since public money is justified by the provision of what the market will not "
 "provide.\n\n"
 "Which one of the following judgments most closely conforms to the principle above?",
 ['The city should not subsidise a private marina used only by boat owners, since those owners can and do pay commercial rates elsewhere',
  'The city should not subsidise a private marina, since the money would be better spent on schools',
  'The city should subsidise a public swimming pool, since swimming is good for health',
  'The city should not fund a bus route that few residents use, since the cost per passenger is high',
  'The city should fund a museum, since museums attract visitors who spend money locally'],
 'The principle turns on benefits confined to those who can already buy the thing in a market, which is exactly the marina case.',
 'B is a budget priority argument, C and E give positive reasons of a different kind, and D turns on cost per user.')
q('LL215','lsat_lr_prin','Identify the principle',3,
 "The teacher gave the same mark to a student who had plainly worked for weeks and to one who "
 "had written the essay the night before, because the two essays were of equal quality. The "
 "teacher acted correctly.\n\n"
 "Which one of the following principles most helps to justify the teacher's decision?",
 ['Work should be assessed on what it achieves rather than on what it cost its author',
  'Students should not be told how their work is assessed',
  'A teacher should not attempt to determine how long a student spent on an assignment',
  'Effort should be rewarded only where it produces a better result',
  'Two students who receive the same mark should be given the same feedback'],
 'Equal marks for unequal effort at equal quality is precisely an achievement standard.',
 'B and E are about communication, C is about evidence, and D is close but concedes that effort is rewardable when it pays, which the case does not require.')
q('LL216','lsat_lr_prin','Apply a principle',3,
 "Principle: An organisation should disclose a data breach to those affected as soon as it "
 "is confirmed, even if the investigation is not complete.\n\n"
 "Which one of the following judgments most closely conforms to the principle?",
 ['The company should have written to affected customers in March, when it confirmed the breach, rather than in July when it identified the cause',
  'The company should have written to affected customers in January, when it first suspected a breach',
  'The company should have completed its investigation before writing to affected customers',
  'The company should have written only to customers whose accounts were shown to have been accessed',
  'The company should have written to all customers, whether or not they were affected'],
 'Confirmation is the trigger and completion of the investigation is expressly not required.',
 'B moves the trigger to suspicion, C contradicts the principle, and D and E concern who is told rather than when.')
q('LL217','lsat_lr_prin','Identify the principle',4,
 "The publisher withdrew the book after learning that its author had fabricated an interview "
 "in an earlier book. Nothing in the present book had been shown to be false. The publisher "
 "acted correctly.\n\n"
 "Which one of the following principles most helps to justify the publisher's decision?",
 ['A publisher may withdraw a work of nonfiction where it has lost the ability to vouch for the author\'s reporting',
  'A publisher should withdraw any book that contains a false statement',
  'An author who fabricates once will fabricate again',
  'A publisher should verify every factual claim in a work of nonfiction before publishing it',
  'A reader who buys a book of nonfiction is entitled to a refund if any part of it is false'],
 'Nothing in this book was shown false, so the ground has to be the loss of warrant rather than a found error, and the principle supplies it.',
 'B and E require a falsehood the case lacks, C is an empirical claim rather than a principle, and D would make publication impossible.')
q('LL218','lsat_lr_prin','Apply a principle',3,
 "Principle: Where two parties are equally at fault for a loss, each should bear half of "
 "it.\n\n"
 "Which one of the following judgments most closely conforms to the principle?",
 ['The two firms, each of which failed to check the figures it was responsible for, should each bear half the cost of the error',
  'The two firms should each bear half the cost, since neither was at fault',
  'The firm that discovered the error should bear less of the cost than the firm that made it',
  'The larger firm should bear more of the cost, since it can better afford to',
  'The firm whose failure occurred first should bear the whole cost'],
 'Equal fault by both is the condition, and it is satisfied by two firms each failing at its own task.',
 'B denies fault, C rewards discovery, D allocates by capacity, and E allocates by sequence.')
q('LL219','lsat_lr_prin','Identify the principle',3,
 "The conductor programmed a work by a composer whose politics he found repellent. He "
 "explained the composer's history in the programme note. He was right to do both.\n\n"
 "Which one of the following principles most helps to justify the conductor's decision?",
 ['A work may be performed on its merits provided the audience is given what it needs to judge the work in its context',
  'An artist\'s politics are irrelevant to the value of the work',
  'A performer should not impose his own moral judgments on an audience',
  'A programme note should describe the circumstances in which a work was composed',
  'Works by objectionable figures should be performed only rarely'],
 'The decision has two parts and only this principle licenses both: perform on merit, and disclose the context.',
 'B and C justify the performance alone, D justifies the note alone, and E recommends a restriction the conductor did not observe.')
q('LL220','lsat_lr_prin','Apply a principle',4,
 "Principle: A promise extracted by a threat is not binding, but a promise made in exchange "
 "for a favour is binding even if the favour was small.\n\n"
 "Which one of the following judgments most closely conforms to the principle?",
 ['Ferreira, who promised to work a double shift after a colleague covered an hour of hers, is bound by the promise',
  'Ferreira, who promised to work a double shift after being told she would be reported otherwise, is bound by the promise',
  'Ferreira, who promised to work a double shift in exchange for a colleague covering an hour, is not bound because the exchange was unequal',
  'Ferreira, who promised to work a double shift for no reason, is bound by the promise',
  'Ferreira, who promised to work a double shift, may withdraw the promise at any time before the shift begins'],
 'A small favour given in exchange makes the promise binding on the principle\'s second clause.',
 'B is the threat case the first clause releases, C imports a proportionality test the principle rejects, and D and E are not governed by it.')

# ===================================================================== explanations
q('LL221','lsat_lr_expl','Resolve the discrepancy',3,
 "The clinic began offering appointments in the evening, and the number of patients seen per "
 "week rose by a fifth. Yet the number of distinct patients the clinic sees in a year has not "
 "changed.\n\n"
 "Which one of the following, if true, most helps to explain the results described above?",
 ['Patients who previously missed appointments now attend, so the same people are seen more often',
  'The clinic hired an additional nurse when the evening appointments began',
  'Evening appointments are longer on average than daytime appointments',
  'Some patients prefer evening appointments to daytime ones',
  'The clinic\'s catchment area has not grown in population'],
 'More visits from the same people raises weekly volume and leaves the annual head count flat, which is exactly the pattern.',
 'Staffing, appointment length, preference and population each explain one half at most.')
q('LL222','lsat_lr_expl','Explain the discrepancy',3,
 "Since the supermarket moved its bakery to the front of the store, sales of bread have "
 "fallen while sales of pastries have risen by more than bread sales fell.\n\n"
 "Which one of the following, if true, most helps to explain the change?",
 ['Customers who now pass the display buy pastries on impulse and buy fewer loaves as a result',
  'The supermarket reduced the price of pastries in the same week',
  'Bread is baked earlier in the day than pastries are',
  'The bakery occupies less floor space at the front of the store than it did at the back',
  'Some customers visit the supermarket only to buy bread'],
 'A single mechanism, impulse purchase at the new location displacing a planned one, moves both figures in the directions observed.',
 'B explains only the pastry rise, C and D are background, and E explains neither change.')
q('LL223','lsat_lr_expl','Parallel reasoning',4,
 "Whenever the archive is open, at least one archivist is on duty. The archive was open on "
 "Friday. So an archivist was on duty on Friday.\n\n"
 "Which one of the following arguments is most similar in its reasoning to the argument "
 "above?",
 ['Whenever the ferry runs, a pilot is aboard. The ferry ran on Sunday. So a pilot was aboard on Sunday.',
  'Whenever the ferry runs, a pilot is aboard. A pilot was aboard on Sunday. So the ferry ran on Sunday.',
  'Whenever a pilot is aboard, the ferry runs. The ferry did not run on Sunday. So no pilot was aboard.',
  'The ferry usually runs when a pilot is available. A pilot was available on Sunday. So the ferry probably ran.',
  'Whenever the ferry runs, a pilot is aboard. The ferry did not run on Sunday. So no pilot was aboard.'],
 'The original is a straightforward modus ponens on a universal conditional, which A reproduces exactly.',
 'B affirms the consequent, C is a valid contrapositive of a different conditional, D is probabilistic, and E denies the antecedent.')
q('LL224','lsat_lr_expl','Resolve the discrepancy',3,
 "A study found that people who eat breakfast weigh less on average than people who skip it. "
 "A trial that randomly assigned participants to eat or skip breakfast found no difference in "
 "weight after four months.\n\n"
 "Which one of the following, if true, most helps to resolve the apparent conflict?",
 ['People who already keep to a regular routine are both more likely to eat breakfast and more likely to weigh less',
  'Participants in the trial who ate breakfast ate fewer calories at lunch',
  'The trial measured weight rather than body composition',
  'Breakfast eaters in the study were younger on average than breakfast skippers',
  'Four months is long enough for a difference in weight to appear'],
 'A common cause behind both the habit and the weight makes the observed association real and the causal claim false, which is what the trial found.',
 'B and E bear on the trial\'s internal workings, C questions the measure, and D names one confounder without connecting it to weight.')
q('LL225','lsat_lr_expl','Explain the discrepancy',3,
 "The city replaced its street lights with brighter ones. Reported crime on the affected "
 "streets rose in the following year, while residents reported feeling safer.\n\n"
 "Which one of the following, if true, most helps to explain the results?",
 ['Residents who feel safer are more willing to report crimes they witness',
  'The new lights cost more to operate than the ones they replaced',
  'Crime rose across the city over the same period',
  'Brighter lighting makes it easier for offenders to identify targets',
  'The city installed the new lights on its busiest streets first'],
 'Reporting rates and actual crime are different things, and a rise in willingness to report raises the first without the second, alongside the feeling of safety.',
 'B is irrelevant, C removes the local puzzle without explaining the pairing, D explains the rise but contradicts the feeling, and E is background.')
q('LL226','lsat_lr_expl','Resolve the discrepancy',4,
 "The airline reduced the number of flights it cancels, and its on time arrival rate "
 "improved. Passenger complaints about delays nonetheless rose.\n\n"
 "Which one of the following, if true, most helps to explain the increase in complaints?",
 ['Flights that would formerly have been cancelled now operate, and most of those arrive late',
  'The airline carried more passengers in the second year than in the first',
  'Complaints can now be submitted through an application on a telephone',
  'On time arrival is measured against a schedule the airline sets itself',
  'Other airlines also reduced their cancellation rates over the period'],
 'Cancelled flights carry no arriving passengers and generate a different complaint. Operating them adds late arrivals to the count while the published rate still improves.',
 'B and C raise complaint volume without connecting to delays specifically, D questions the metric, and E is beside the point.')
q('LL227','lsat_lr_expl','Parallel reasoning',4,
 "Most of the students who passed the examination attended the review session. So the review "
 "session probably helped students pass.\n\n"
 "Which one of the following arguments is most similar in its reasoning to the argument "
 "above?",
 ['Most of the plants that survived the frost were in the greenhouse. So the greenhouse probably protected them.',
  'All of the plants in the greenhouse survived the frost. So the greenhouse protected them.',
  'Most of the plants in the greenhouse survived the frost. So most plants that survived were in the greenhouse.',
  'No plant outside the greenhouse survived the frost. So the greenhouse was necessary for survival.',
  'Some plants survived the frost outside the greenhouse. So the greenhouse was not necessary for survival.'],
 'Both move from a majority of the successful cases sharing a feature to a tentative causal claim about that feature.',
 'B is universal rather than majority, C reverses the proportion, and D and E are about necessity.')
q('LL228','lsat_lr_expl','Explain the discrepancy',3,
 "Vineyards in the valley have planted a grape that ripens two weeks earlier than the "
 "traditional variety. Harvest dates have not moved.\n\n"
 "Which one of the following, if true, most helps to explain why harvest dates have not "
 "moved?",
 ['Growers now leave the fruit on the vine after ripening to concentrate its sugars',
  'The new grape yields slightly less fruit per vine than the traditional variety',
  'The new grape was first planted five years ago',
  'Harvest dates in neighbouring valleys have moved earlier',
  'The new grape is more resistant to mildew than the traditional variety'],
 'Ripening earlier and picking later by the same interval leaves the date unchanged, and the sugar motive supplies the reason.',
 'Yield, planting date, neighbours and disease resistance say nothing about when the fruit is picked.')
q('LL229','lsat_lr_expl','Resolve the discrepancy',3,
 "The publisher lowered the price of its journal subscription by a third, and total "
 "subscription revenue rose. It lowered the price by a further third the next year, and "
 "revenue fell.\n\n"
 "Which one of the following, if true, most helps to explain the different outcomes?",
 ['Almost every library that would subscribe at any price had already subscribed after the first reduction',
  'The journal published more articles in the second year than in the first',
  'Some libraries subscribe to the journal through a consortium',
  'The publisher raised the price of its other journals in the second year',
  'Production costs per issue fell over the two years'],
 'The first cut recruited new subscribers and the second had almost none left to recruit, so the lower price applied to a nearly fixed base.',
 'Article count, consortia, other journals and costs do not bear on the response to price.')
q('LL230','lsat_lr_expl','Explain the discrepancy',3,
 "Since the factory installed the new filter, emissions measured at the stack have fallen by "
 "half. Air quality monitors in the town nearby show no improvement.\n\n"
 "Which one of the following, if true, most helps to explain these results?",
 ['The pollutant the monitors measure comes mostly from road traffic rather than from the factory',
  'The filter requires cleaning more often than the manufacturer predicted',
  'The monitors were installed in the town before the factory was built',
  'Emissions at the stack are measured hourly and town air quality daily',
  'The factory operates fewer hours in winter than in summer'],
 'If the factory is a small part of the town\'s exposure, halving its output need not register at all.',
 'Cleaning frequency, monitor age, sampling interval and seasonality do not explain the absence of any improvement.')
q('LL231','lsat_lr_expl','Resolve the discrepancy',4,
 "Countries that spend more per pupil on schooling do not on average score higher on "
 "international tests. Within any one country, schools that spend more per pupil do score "
 "higher.\n\n"
 "Which one of the following, if true, most helps to explain this pattern?",
 ['Within a country, additional spending goes disproportionately to schools serving pupils who were already scoring well',
  'International tests are translated into each country\'s language before being administered',
  'Countries differ in the age at which pupils begin formal schooling',
  'Spending per pupil is measured in local currency and converted at market exchange rates',
  'Some countries spend more on teacher salaries and others on buildings'],
 'A within country correlation produced by allocation rather than by effect would vanish at the country level, which is exactly the pattern described.',
 'B, C, D and E identify differences between countries without explaining why the relationship reverses across the two levels.')
q('LL232','lsat_lr_expl','Explain the discrepancy',3,
 "The train operator added carriages to its busiest service. The number of passengers "
 "standing did not fall.\n\n"
 "Which one of the following, if true, most helps to explain the result?",
 ['Passengers who had been travelling on earlier and later services moved to the busiest one once it was less crowded',
  'The additional carriages are of an older design than the rest of the train',
  'The service runs every twenty minutes throughout the day',
  'Season ticket sales have been flat for three years',
  'The platform at the busiest station is long enough for the lengthened train'],
 'Latent demand filling the new space is a standard mechanism and it accounts precisely for capacity rising with no change in standing.',
 'Carriage age, frequency, ticket sales and platform length do not explain why the extra space filled.')
q('LL233','lsat_lr_expl','Parallel reasoning',3,
 "No recording in the archive was made before 1930. Some recordings in the archive are of "
 "folk songs. So some recordings of folk songs were made after 1930.\n\n"
 "Which one of the following arguments is most similar in its reasoning to the argument "
 "above?",
 ['No book in the library was printed before 1800. Some books in the library are atlases. So some atlases were printed after 1800.',
  'No book in the library was printed before 1800. Some atlases were printed after 1800. So some books in the library are atlases.',
  'Every book in the library was printed after 1800. Some atlases are in the library. So every atlas was printed after 1800.',
  'No book printed before 1800 is in the library. Some atlases are not in the library. So some atlases were printed before 1800.',
  'Some books in the library are atlases. Some atlases were printed after 1800. So some books in the library were printed after 1800.'],
 'A universal restriction on a set plus an existential claim about members of that set yields an existential conclusion combining the two, which A copies exactly.',
 'B reverses the direction, C overgeneralises, D draws an invalid conclusion from a negative, and E chains two existentials.')
q('LL234','lsat_lr_expl','Resolve the discrepancy',3,
 "The bookshop moved its fiction section upstairs. Fiction sales fell by a tenth. Total sales "
 "for the shop rose by a tenth.\n\n"
 "Which one of the following, if true, most helps to explain the results?",
 ['The ground floor space freed by the move now holds a cafe and a stationery section that together sell more than the fiction they replaced',
  'Customers who buy fiction spend more per visit than other customers',
  'The staircase to the first floor is at the back of the shop',
  'The shop\'s fiction stock was reduced when the section moved',
  'Nearby shops also reported higher sales over the same period'],
 'The two figures fit if what took the vacated space sells more than the displaced fiction lost, which is what A says.',
 'B and C would deepen the puzzle or explain only the fall, D explains the fall alone, and E explains neither.')
q('LL235','lsat_lr_expl','Explain the discrepancy',4,
 "Hospitals that adopted the checklist reported fewer surgical complications in the first "
 "year. In the third year their complication rates had returned to where they began.\n\n"
 "Which one of the following, if true, most helps to explain the return?",
 ['Staff came to complete the checklist as a formality without performing the checks it lists',
  'The hospitals that adopted the checklist were those with the highest complication rates',
  'Complication rates at hospitals that did not adopt the checklist were unchanged over the three years',
  'The checklist was revised at the end of the first year',
  'Surgical volumes at the adopting hospitals rose over the three years'],
 'A procedure that is recorded rather than performed produces exactly this shape: an early gain that decays as the practice hollows out.',
 'B explains an initial fall by regression, C rules out a general trend, D is a change without a direction, and E is volume rather than rate.')
q('LL236','lsat_lr_expl','Resolve the discrepancy',3,
 "Wolves were reintroduced to the park, and the elk population fell as expected. The number "
 "of elk killed by wolves each year, however, is far too small to account for the "
 "decline.\n\n"
 "Which one of the following, if true, most helps to explain the decline?",
 ['Elk now avoid the valleys where wolves hunt, and those valleys hold the best winter forage',
  'Wolves also prey on deer, which compete with elk for forage',
  'The park has recorded elk numbers by the same method for forty years',
  'Wolf numbers in the park have grown each year since the reintroduction',
  'Elk calves are more vulnerable to predation than adults are'],
 'Behavioural displacement from the best feeding grounds reduces survival and reproduction far beyond the kill count, which is the gap the puzzle names.',
 'B would help elk, C is methodological, D raises kills rather than closing the gap, and E is about which elk are taken.')
q('LL237','lsat_lr_expl','Explain the discrepancy',3,
 "The company introduced an annual bonus for the ten employees with the highest individual "
 "output. Individual output rose in every department. Total output for the company fell.\n\n"
 "Which one of the following, if true, most helps to explain the results?",
 ['Employees stopped helping colleagues with tasks that did not count toward their own output',
  'The bonus was smaller than employees had expected',
  'Individual output is measured in units completed per week',
  'Some departments produce components used by others',
  'The company hired no new employees during the year'],
 'Measured individual output rising while the total falls is what happens when cooperation, which the measure ignores, is withdrawn.',
 'B, C and E are background, and D describes a dependency without saying anything changed.')
q('LL238','lsat_lr_expl','Resolve the discrepancy',4,
 "Since the museum began charging for entry, attendance has fallen by a third while revenue "
 "from the shop and cafe has risen.\n\n"
 "Which one of the following, if true, most helps to explain the rise in shop and cafe "
 "revenue?",
 ['Visitors who have paid to enter stay longer and are more likely to buy something than those who entered free',
  'The shop has extended its opening hours',
  'The cafe raised its prices when the entry charge was introduced',
  'Attendance had been rising for several years before the charge',
  'The museum spends its shop and cafe revenue on conservation'],
 'A charge selects for committed visitors and changes the behaviour of those who come, which is enough to raise spending on a smaller base.',
 'B and C are alternative causes that do not connect to the attendance fall, D is background, and E concerns what the money is used for.')
q('LL239','lsat_lr_expl','Explain the discrepancy',3,
 "A manufacturer improved the fuel efficiency of its delivery vans by a quarter. The fuel its "
 "customers buy for those vans has not fallen.\n\n"
 "Which one of the following, if true, most helps to explain why fuel purchases have not "
 "fallen?",
 ['Customers have extended their delivery routes now that each kilometre costs less to drive',
  'The improved vans cost more to buy than the vans they replaced',
  'Fuel prices have been stable over the period in question',
  'Some customers operate vans from more than one manufacturer',
  'The efficiency improvement was measured under laboratory conditions'],
 'A lower cost per kilometre invites more kilometres, and the extra distance absorbs the saving.',
 'Purchase price, fuel prices and mixed fleets are beside the point, and E questions the figure rather than explaining the outcome.')
q('LL240','lsat_lr_expl','Parallel reasoning',4,
 "The only way to reach the summit before dark is to leave at dawn. The party did not reach "
 "the summit before dark. So the party did not leave at dawn.\n\n"
 "The reasoning in which one of the following is most similar to the flawed reasoning above?",
 ['The only way to qualify for the grant is to submit by March. The laboratory did not qualify for the grant. So the laboratory did not submit by March.',
  'The only way to qualify for the grant is to submit by March. The laboratory did not submit by March. So the laboratory did not qualify for the grant.',
  'Anyone who submits by March qualifies for the grant. The laboratory qualified. So the laboratory submitted by March.',
  'The only way to qualify for the grant is to submit by March. The laboratory submitted by March. So the laboratory qualified for the grant.',
  'Most laboratories that submit by March qualify for the grant. The laboratory submitted by March. So it probably qualified.'],
 'Leaving at dawn is necessary rather than sufficient, so failing to arrive does not show the party slept in. A reproduces that error exactly.',
 'B is a valid use of the necessary condition, C affirms the consequent of a different conditional, D treats a necessary condition as sufficient, and E is probabilistic.')

E.permute(I)

# ---------------------------------------------------------------------------
# LIFT: how many distractors on each item are carried past the key.
#
# Written naturally the key was the longest option on 108 of these 140, playable at 77
# percent against a chance rate of 20. Extending one distractor on each would leave 108
# items whose key is second longest, which is the same tell one position over (INC-0062).
# The number lifted is what sets the key's rank, so these entries carry four, three, two,
# one or none, chosen to fill the ranks the bank as written left empty. check_lift below
# fails the run if a clause was too short to do it (INC-0066).
LIFT = {}
LIFT.update({
 'LL101': [('sell more copies in their first month', ' than they do over the remainder of their first year in print'),
           ('readers who have not previously bought books', ' from any publisher of commercial fiction in the past decade'),
           ('recommend it to others more often than readers who abandon it', ' and recommend it to a wider circle of acquaintances'),
           ('abandon a novel do so during its opening chapters', ' rather than at any later point in the book, whatever its length')],
 'LL102': [('responsible for the majority of traffic deaths on arterial roads', ' recorded in the city'),
           ('recovered from the citations they generate', ' within the first year of operation'),
           ('not increase the number of collisions at intersections', ' where the arterial roads meet local streets')],
 'LL104': [('keep the weight off for at least a further six months', ' after the study has ended'),
           ('less expensive to follow than the diets the other participants chose', ' over the same six month period')],
 'LL107': [('more serious than the illness the virus causes', ' in an unvaccinated dog'),
           ('because it increases their revenue', ' rather than because the evidence supports it'),
           ('follow the recommendation to revaccinate their dogs every year', ' for as long as the animal lives')],
 'LL108': [('state at the outset which of its scenes are invented', ' and which are drawn from the record')],
 'LL112': [('hold their meetings in the evening rather than during the day', ' or at the weekend'),
           ('would form organisations if it were safe to do so', ' after dark'),
           ('have no effect at all on the level of crime', ' in the areas they were formed to serve'),
           ('reported with equal accuracy in all neighbourhoods', ' of the city, whatever their crime rate')],
 'LL113': [('knowing that it would disadvantage', ' the particular batteries it was comparing its own products against'),
           ("would outlast the competitor's in a test of intermittent use", ' conducted under the same laboratory conditions'),
           ('Most purchasers use batteries of this kind intermittently', ' rather than drawing on them without interruption for many hours at a time')],
 'LL115': [('measures the skills the course is designed to teach', ' and nothing else'),
           ('covers every topic that appears on the entrance examination', ' in the year it is taken')],
 'LL117': [('No player has ever been retained after missing three consecutive', ' sessions in the period since the rule was first adopted'),
           ('Training sessions are held on Monday, Wednesday and Friday', ' of each week throughout the whole of the club\'s playing season'),
           ('has been warned about attendance on a previous occasion', ' by the coach, in the presence of the rest of the squad, earlier in the season')],
 'LL118': [('more competitive than the markets in which the company previously failed', ' and has more established local firms operating in it'),
           ('unwound at a loss is worse for the company than not entering the market at all', ' once the damage to its reputation is taken into account'),
           ('no more capital available now than it had at the time', ' of the two earlier ventures that both failed within three years of their launch'),
           ('No competitor has succeeded in the South American market after failing', ' elsewhere in a comparable line of business at any point over the last decade')],
})
LIFT.update({
 'LL122': [('what is true of a country as a whole is true of each of its citizens', ' when considered one at a time')],
 'LL123': [('some salespeople make more than forty calls', ' a week without selling more than their colleagues'),
           ('the rest of the team is capable of making forty calls a week', ' alongside their other duties')],
 'LL124': [('a fare increase will produce the revenue the system needs', ' to maintain the present level of service'),
           ('the preferences of riders as decisive on a question of policy', ' that affects the whole city'),
           ('infers what riders will accept from what they have said they want', ' when they were asked about it'),
           ('fails to specify the size of the fare increase being proposed', ' or the period over which it would apply')],
 'LL125': [('a plurality as though it were a claim about a majority', ' of the dentists who were asked'),
           ('the dentists surveyed were selected at random', ' from the profession as a whole'),
           ('dentists recommend more than one brand', ' of toothpaste to the same patients')],
 'LL129': [('the earlier objections led to changes in those buildings', ' before they were approved'),
           ('the residents who object now are the same as those who objected before', ' to the earlier buildings')],
 'LL130': [('relies on self reported energy rather than on a physiological measurement', ' of any objective kind at all'),
           ('generalises from participants in a study to the population at large', ' without any further qualification'),
           ('assumes that all participants took the supplement as directed', ' for the whole of the study period')],
 'LL131': [('a miscalibrated instrument produces results that are always wrong', ' by a detectable margin')],
 'LL134': [('a belief held by individuals from a practice observed at the level of a society', ' over the course of many generations'),
           ('every society with such a belief practises elaborate rites', ' at the burial of each one of its dead'),
           ('the tombs and the grave goods date from the same period', " of the valley's occupation by those people"),
           ('relies on archaeological evidence where written evidence would be more reliable', ' about a matter of religious belief of this kind')],
 'LL135': [('record profits as though they were unusually large profits', ' for a company of this size'),
           ('attacks management rather than the case management has made', ' about the current year'),
           ('confuses profit with the cash available to pay wages', ' over the coming twelve months')],
 'LL139': [('the earlier widenings were of comparable scale to the one proposed', ' for the motorway now planned'),
           ('a period of five years that is not shown to be the relevant one', ' for measuring the effect of a widening')],
 'LL140': [('generalises from students who read to students in general', ' without allowing for the difference'),
           ('assumes that essay quality can be measured reliably', ' by the person who set the work in the first place'),
           ('treats writing well as the only purpose of reading', ' that a school need concern itself with')],
})
LIFT.update({
 'LL141': [('commission the hotel pays to travel sites has risen', ' in each of the three years that have just passed'),
           ('Occupancy at the hotel is highest during the months', ' in which the city holds its largest conferences'),
           ("hotel's own site is easier to use on a telephone", ' than the sites most travellers book their rooms through'),
           ("members of the hotel's loyalty programme", ' and receive a discount on the published rate')],
 'LL143': [('Some restaurants in the city raised their prices after the increase took effect', ' rather than reducing the hours they offered')],
 'LL144': [('among the complications patients most wish to avoid', ' in the days following any operation of this kind'),
           ('in use in other countries for several years', ' without any comparable difficulty being reported')],
 'LL146': [('received a subsidy for switching to no till planting', ' that other farms in the district would not be offered'),
           ('How many years the farmer has been using the no till method', ' on the particular fields whose yields have risen since the change'),
           ('Whether yields on this farm were rising before the switch', ' for reasons that have nothing to do with the method of planting'),
           ('What equipment is required to plant without tilling', ' and whether it can be hired locally rather than having to be bought outright')],
 'LL147': [('produced more manuscripts in this period than any other', ' scriptorium working in the region'),
           ('traded over long distances during this period', ' and used by scriptoria far from where it was made'),
           ('script resembles that of manuscripts from several scriptoria', ' working in the same decades')],
 'LL149': [('subject to strong winds during the season in which the birds breed', ' and for some weeks afterwards'),
           ('diet available on the island is similar to that available on the mainland', ' at every season of the year')],
 'LL150': [('say they find them repetitive', ' and would prefer them to be held less often than every week'),
           ('measured by survey rather than by retention', ' or by any of the other behavioural indicators the firms collect'),
           ('Your firm is smaller than most of the firms', " whose survey results the consultant's recommendation about weekly meetings has been drawn from")],
 'LL151': [('Several other valuable items were kept in plain view elsewhere', ' in rooms the intruder passed through')],
 'LL153': [('in service for eleven years before the crack was discovered', ' during a routine inspection'),
           ('can sometimes be obscured by corrosion', ' of the kind found on beams exposed to weather'),
           ('most common cause of failure in beams of this type', ' in structures of comparable age'),
           ('impact occurred within hours of the crack being discovered', ' by the engineer who examined the beam')],
 'LL154': [('schools that did not adopt the programme also failed to rise', ' over the same three year period'),
           ('report that students enjoy the programme', ' more than the materials it replaced'),
           ('costs less per student than the materials it replaced', ' in each of the three schools concerned')],
 'LL157': [('Seedlings of two other species did not reappear after the removal', ' of the deer from the island, although they had been present before'),
           ('present on the island for more than fifty years', ' before the decision to remove them from the park was finally taken')],
 'LL158': [('records speed and braking but not the time of day', ' at which a journey is made'),
           ('discount offered to drivers who install the device exceeds its cost', ' over a single policy year'),
           ('find the device distracting during the first weeks of use', ' after it has been fitted')],
})
LIFT.update({
 'LL159': [('panels would be visible from the square in front of the town hall', ' or only from the street behind it'),
           ('other buildings owned by the town have roofs suitable for panels', ' of the same kind, size and orientation'),
           ('the town has borrowed money for capital projects in the past', ' on terms comparable to those now available'),
           ('How many years the town hall roof has been in place already', ' without having needed any substantial repair work')],
 'LL163': [("Bottled water is as damaging to children's teeth as sugary drinks are", ' when it is drunk in the same quantities by children')],
 'LL164': [('circumstances of acquisition are weaker than arguments from meaning', ' in disputes over restitution'),
           ('A museum exists in order to let objects mean something to those who see them', ' rather than merely to preserve them')],
 'LL165': [('Every package the receiving clerk accepted arrived on a day other than Tuesday', ' of the week in question'),
           ('Some packages sent by express arrived on a day other than Tuesday', ' and were accepted by the receiving clerk'),
           ('No package sent by express was accepted by the receiving clerk', ' at any point during the week in question'),
           ('Some packages that arrived on Tuesday were damaged in transit', ' before they reached the receiving clerk')],
 'LL166': [('install programmable thermostats use more energy than they otherwise would', ' over the course of a full year'),
           ('would save energy by removing their programmable thermostats', ' and returning to a simple manual control instead'),
           ('set the default settings of programmable thermostats badly', ' for most of the households that end up buying them')],
 'LL169': [('later plays are more difficult for modern readers than the earlier ones', ' are for those same readers today'),
           ('Some of the plays attributed to the dramatist were written by someone else', ' working in the same period and city')],
 'LL171': [('built to a lower standard than its design specified', ' in at least part of the district'),
           ('a reliable measure of water damage', ' in districts where most properties are insured'),
           ('becoming less predictable than it was', ' when the drainage system was designed')],
 'LL172': [('technical cases are no harder for juries than other cases', ' of comparable length and complexity')],
 'LL176': [('eliminate hand injuries entirely within a few years', ' of the sensors being installed'),
           ('Workers have become less careful since the sensors were installed', ' on the machines they operate'),
           ('Near misses were underreported before the sensors were installed', ' and are now recorded automatically'),
           ('sensors stop the machines more often than is necessary', ' to prevent an injury from occurring')],
 'LL177': [('Street crowding is not a serious problem in the district', ' the proposal would apply to'),
           ('The proposal will not achieve what its supporters intend', ' it to achieve in the district'),
           ('Tenants who do not own cars should not pay for parking', ' they have no occasion to use')],
 'LL180': [('Everything in the sealed file was written by the ambassador', ' during his time in the post'),
           ('The foreign press has read documents in the sealed file', ' held by the ministry')],
 'LL181': [("It is the main conclusion the planner's other statements are offered to support", ' in the passage'),
           ('evidence that the extension would benefit a substantial number of riders', ' on the existing route'),
           ('an assumption the planner must make in order to compare the two groups', ' of people affected')],
})
LIFT.update({
 'LL182': [('the objection assumes what it sets out to prove', ' about the treatment'),
           ('showing that the treatment has worked for particular patients', ' seen in the clinic'),
           ('questioning the motives of those who conducted the trial', ' and reported its result'),
           ('presenting a study that reached the opposite conclusion', ' about the same treatment')],
 'LL184': [('It explains why comparable towns expanded their local coverage', ' when their own circulation fell')],
 'LL185': [('the usual account rests on a confusion of terms', ' that the argument then clears up'),
           ('offering an alternative explanation that fits the evidence better', ' than the one usually given')],
 'LL186': [('the nearest glaciated terrain has been correctly identified', ' by earlier surveys of the region'),
           ('the boulders may have been carried by a glacier after all', ' over the intervening distance'),
           ('the glacial account is the more likely of the two', ' explanations under consideration'),
           ("introduce the evidence on which the geologist's conclusion rests", ' in the sentences that follow')],
 'LL187': [('the witness has a reason to testify against the client', ' that she did not disclose'),
           ('establishing that the client was elsewhere at the time in question', ' on the evening of the incident'),
           ('presenting a second witness whose account conflicts with the first', ' on the question of identification')],
 'LL189': [('introduce the criterion by which the reviewer will judge the novel', ' in the remainder of the paragraphs that follow'),
           ('summarise the praise the novel has received from other critics', ' in the months since it was published earlier in the year')],
 'LL190': [('appealing to the judgment of professionals rather than residents', ' of the street under discussion'),
           ('denying that the design departs from the character of the street', ' as the street stands at present'),
           ('claiming that the character of a street cannot be defined', ' precisely enough to be applied at all')],
 'LL191': [('establishing that the vaccine works and inferring that a requirement is justified', ' on that basis alone')],
 'LL194': [('the subject of a biography deserves privacy about his feelings', ' even after his death'),
           ('biographers are capable of knowing what their subjects felt', ' at any given moment'),
           ("a biography should explain its subject's actions at all", ' rather than simply record them'),
           ('most biographies published today speculate too much', ' about the inner lives of their subjects')],
 'LL195': [('provide the evidence for the conclusion that oat bran is not medicine', ' but ordinary food'),
           ('introduce a comparison between oat bran and other sources of fibre', ' in the ordinary diet'),
           ('concede that the original studies reached the right conclusion', ' about cholesterol after all')],
 'LL197': [('questioning the measurements on which the predator explanation rests', ' in the regions where both were studied'),
           ('the two explanations are compatible and both contribute', ' to the decline that has been observed')],
 'LL198': [('evidence that the opponents are a weaker side than they were', ' at the start of the present season'),
           ('the main conclusion the coach draws about the coming match', ' against that particular opposition'),
           ('an assumption the coach makes without supporting it', ' at any point in the passage that follows')],
})
LIFT.update({
 'LL200': [('evidence that the drawing is by the master rather than the workshop', ' that produced work under the name of the master himself'),
           ('an assumption the curator accepts only for the sake of argument', ' with those who disagree with him about the attribution of the drawing'),
           ('It is an objection the curator goes on to refute', ' in the two sentences that follow, by appealing to the purpose of the examination'),
           ('It is the main conclusion the curator defends', ' in the passage, and the two sentences that follow are both offered in support of it alone')],
 'LL203': [('more likely to be false than one obtained by a sound method', ' of collecting the same sample')],
 'LL204': [('bought a scanner from general funds may keep donations raised afterwards', ' for the same equipment'),
           ('raised money without stating a purpose must spend it on patient care', ' rather than on new equipment')],
 'LL205': [('holds a financial interest, because he might decide it wrongly', ' as a result of that financial interest in the outcome'),
           ('should not grade the work of a relative, because she would be unable to judge it fairly', ' however hard she might try to set the family relationship aside'),
           ('should acknowledge it after the match rather than during it', ' so that play is not disrupted any further than it already has been by the mistake'),
           ('should disclose any payment received from a subject she writes about', ' at the time the article appears rather than at some later date, when it may no longer matter')],
 'LL206': [('must compensate it regardless of what its terms provide', ' about changes to a booking'),
           ('may not change an arrangement once the other party has relied on it', ' in making further plans'),
           ('who books a connection assumes the risk that it will be missed', ' if the first flight is changed')],
 'LL208': [('unless it has verified its contents independently', ' of the source who supplied the document'),
           ('publish any document that comes into its possession lawfully', ' whatever the consequences may be for the person who supplied it')],
 'LL209': [('should be extended to the digital reading room for the sake of consistency', ' across the whole of the building'),
           ('replaced by a requirement that fire extinguishers be provided', ' in every room of the archive and the reading room'),
           ('should be enforced more strictly during the winter', ' when the heating is in use and the building is at its driest')],
 'LL210': [('recover only losses that were foreseeable when the agreement was made', ' by the party now claiming them')],
 'LL212': [('should be given an opportunity to correct the omission', ' before the application is judged'),
           ('received a previous award should not receive a second one for related work', ' from the same committee in consecutive rounds'),
           ('should reject any application it cannot verify in full', ' before the closing date by which its decisions have to be made public'),
           ('should fund the strongest application it receives', ' in any round, whatever else may be said about the applicant who made it')],
 'LL214': [('a bus route that few residents use, since the cost per passenger is high', ' compared with other routes in the city'),
           ('since the money would be better spent on schools', ' and on other services the whole city uses'),
           ('since museums attract visitors who spend money locally', ' in shops and restaurants near the site of the museum')],
 'LL217': [('verify every factual claim in a work of nonfiction before publishing it', ' under its own imprint'),
           ('entitled to a refund if any part of it is false', ' in any material respect')],
 'LL218': [('should bear less of the cost than the firm that made it', ' in proportion to their contributions'),
           ('should bear more of the cost, since it can better afford to', ' out of the reserves that it has accumulated over the years'),
           ('should each bear half the cost, since neither was at fault', ' for the error that occurred in the figures they exchanged')],
})
LIFT.update({
 'LL219': [('A programme note should describe the circumstances in which a work was composed', ' and the life of the person who composed it'),
           ('should not impose his own moral judgments on an audience', ' that has come to the concert hall to hear the music'),
           ('Works by objectionable figures should be performed only rarely', ' and never as the principal item of any concert programme'),
           ("An artist's politics are irrelevant to the value of the work", ' and to the case for performing the work in public at all')],
 'LL222': [('occupies less floor space at the front of the store than it did at the back', ' of the shop')],
 'LL224': [('younger on average than breakfast skippers', ' and were drawn from a different part of the country'),
           ('who ate breakfast ate fewer calories at lunch', ' than those who had been assigned to skip it')],
 'LL225': [('makes it easier for offenders to identify targets', ' worth approaching'),
           ('cost more to operate than the ones they replaced', ' over a full year'),
           ('installed the new lights on its busiest streets first', ' and the quieter ones later'),
           ('Crime rose across the city over the same period', ' and not only on the streets that were relit')],
 'LL226': [('carried more passengers in the second year than in the first', ' on the same set of routes'),
           ('measured against a schedule the airline sets itself', ' and revises from time to time'),
           ('submitted through an application on a telephone', ' rather than only by letter or telephone call')],
 'LL229': [('published more articles in the second year than in the first', ' without increasing its page count'),
           ('raised the price of its other journals in the second year', ' by about the same proportion each time')],
 'LL230': [('requires cleaning more often than the manufacturer predicted', ' when it was first installed'),
           ('measured hourly and town air quality daily', ' by instruments of different sensitivity'),
           ('monitors were installed in the town before the factory was built', ' on the edge of the town itself')],
 'LL231': [("translated into each country's language before being administered", ' to the pupils who go on to sit them')],
 'LL234': [('who buy fiction spend more per visit than other customers', ' do on any single visit to the shop, whichever section of it they buy from'),
           ('Nearby shops also reported higher sales over the same period', ' of the year, both before the fiction section moved and for some months after it'),
           ("The shop's fiction stock was reduced when the section moved", ' upstairs to the first floor, and has not been restored to its former size since'),
           ('staircase to the first floor is at the back of the shop', ' some distance from the main entrance and out of sight of most of the customers')],
 'LL236': [('Wolf numbers in the park have grown each year since the reintroduction', ' was first carried out'),
           ('recorded elk numbers by the same method for forty years', ' before and after the wolves returned'),
           ('Elk calves are more vulnerable to predation than adults are', ' during their first winter in the park')],
 'LL238': [('extended its opening hours', ' at the entrance to the museum building ever since the new charge began'),
           ('cafe raised its prices when the entry charge was introduced', ' at the start of the present financial year for the museum')],
 'LL239': [('improvement was measured under laboratory conditions', ' rather than on the road'),
           ('cost more to buy than the vans they replaced', " in the fleets of the customers who bought them"),
           ('operate vans from more than one manufacturer', ' on the same set of delivery routes')],
})

E.extend(I, LIFT, 'LIFT')
INTENT = E.lift_counts(LIFT)
E.check_lift(I, INTENT)

HEADER = '''// bank_lsat_lr3.js - Original LSAT Logical Reasoning items LL101-LL240.
//
// Generated by src/mk_bank_lsat_lr3.py. Edit that file, not this one.
//
// The LSAT was the one exam the review bot still failed: 142 items against 594 to 1392
// for the other four, every skill under 21, and 232 avoidable repeats in 3500 items
// served. Logical Reasoning is two thirds of the real exam and was seven skills at 9 to
// 11 items each. These 140 take each of the seven to 29 or 31.
//
// Grouped by skill rather than interleaved, because the skill is what the shortfall was
// measured in.
//
// On the length tell: the key was the longest option on 108 of the 140 as written,
// playable at 77 percent against a chance rate of 20. It is corrected by carrying four,
// three, two, one or no distractors past the key, item by item; see LIFT in the
// generator for why one per item would only move the tell.
'''

E.measure(I)
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_lsat_lr3.js',
        HEADER, [], I, 'BANK_LSAT_LR3', group_key='skill')
