#!/usr/bin/env python3
"""Emit src/bank_lsat_rc3.js.

Run: python3 src/mk_bank_lsat_rc3.py src/bank_lsat_rc3.js

The last starved corpus on any exam. After bank_lsat_lr3.js took Logical Reasoning to 29
to 31 per skill, the review bot's remaining LSAT warning was the five reading skills at
10, 10, 12, 18 and 20. These 84 items across 12 new passage sets take all five to 30 or
more, which clears the last category under 25 on any of the five exams.

Twelve sets of seven, the shape LSAC publishes for the section: single passages of
roughly four hundred words and two comparative pairs, across law, natural science,
humanities, social science and the history of science.

Every set covers all five tracked skills. That is not decoration: the engine builds a
section out of whole passage groups, so a skill confined to one passage is dropped
whenever that passage is not selected, and the skill then looks starved to the bot even
when the bank holds enough of it. The two remaining question slots per set are spread so
that the totals land where they are needed rather than evenly.

Machinery is in src/bank_emit.py. The length tell is corrected by LIFT, and check_lift
fails the run if any clause was too short to move the item it names.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

P = {}

P['11'] = ("The exclusionary rule bars evidence obtained in violation of the Fourth "
"Amendment from being used against a defendant at trial. Its usual justification is "
"deterrence: an officer who knows an unlawful search will produce nothing usable has less "
"reason to conduct one. The rule is therefore defended not as a right of the defendant but "
"as a cost imposed on the state to discipline its own agents.\n\n"
"Critics have pressed two objections. The first is empirical. If deterrence is the point, "
"the rule should be evaluated by whether it deters, and the studies attempting to measure "
"that have produced results too weak and too contested to sustain the doctrine on their "
"own. The second is distributive. The rule benefits only defendants against whom unlawful "
"searches produced evidence, which is to say the guilty; a person searched unlawfully who "
"turns out to have nothing incriminating receives no remedy from it at all.\n\n"
"Defenders answer the second objection by observing that it mistakes a side effect for a "
"purpose. The rule is not a compensation scheme, and it was never claimed that its "
"benefits would fall on those most wronged. The answer is sound as far as it goes, and it "
"has an awkward consequence. Once the rule is understood purely as a deterrent, the "
"empirical objection becomes the whole of the case, and a deterrent that cannot be shown "
"to deter is difficult to defend against a proposal to replace it with something cheaper.\n\n"
"A third position, less often argued, holds that a court which admits unlawfully obtained "
"evidence makes itself a party to the violation, and that the rule protects the integrity "
"of the proceeding rather than the interests of anyone in it. This reading is immune to "
"both objections, since it neither promises deterrence nor claims to compensate. It is "
"also the reading the Supreme Court has moved furthest away from, which suggests that its "
"immunity has been purchased at the price of anything the Court is willing to call a "
"reason.")

P['12'] = ("Most land plants form partnerships with fungi at their roots. The fungus takes "
"sugars from the plant and supplies it with phosphorus and nitrogen drawn from a volume of "
"soil far larger than the roots can reach. The relationship is ancient and close to "
"universal, and in the last two decades a further claim has attached itself to it: that "
"the fungal threads link neighbouring plants into a network through which they exchange "
"resources and even warnings of attack.\n\n"
"The evidence for linkage is good. Radioactive carbon supplied to one tree turns up in a "
"neighbour, and the fungal connections are visible under a microscope. The evidence for "
"what the linkage does is much weaker. Carbon moving from one plant to another may be "
"moving because the fungus takes it and later releases it, which makes the fungus the "
"agent rather than a conduit between plants. The quantities are small and their direction "
"is not consistently from the well supplied to the needy.\n\n"
"The gap between the two bodies of evidence has been filled by a metaphor. Describing the "
"network as a system through which trees feed their offspring or warn their neighbours "
"supplies an intention that nothing in the data requires, and once supplied it organises "
"further observation: a finding that fits is reported as confirmation and a finding that "
"does not is reported as a complication.\n\n"
"None of this shows the cooperative reading to be false. It shows that the reading has run "
"ahead of what has been measured, and that the measurement needed to settle it has a "
"specific shape. What is required is not more demonstrations that carbon moves but "
"experiments in which the fungus and the plants can be given conflicting interests, so "
"that the direction of any transfer identifies which party the transfer serves. Such "
"experiments are difficult and few have been attempted.")

P['13'] = ("Copyright law protects works fixed in a tangible medium. A song that exists only "
"as a performance, passed from one musician to another and altered at every pass, is not "
"fixed in that sense until somebody writes it down or records it. The rule was written for "
"printed works and it has a consequence its drafters did not consider: whoever first "
"records an oral tradition acquires a copyright in it.\n\n"
"In the early twentieth century collectors travelled through the American South recording "
"blues and work songs. Several of them registered copyrights in the results. The songs had "
"circulated for decades and in some cases for generations; the collector added a "
"transcription and a title. Courts asked to consider the resulting claims applied the "
"fixation rule as written and upheld most of them, with the result that royalties from the "
"later commercial recordings flowed to the collectors' estates rather than to the "
"communities the songs came from.\n\n"
"The obvious response is to say the collectors contributed nothing original. That response "
"is weaker than it sounds. Transcription of an oral performance requires choices about "
"which of several versions to fix, which repetitions to preserve and how to render pitch "
"and rhythm that notation handles badly. Those choices are the sort of thing copyright "
"ordinarily treats as authorship, and a rule that denied protection to them would also "
"deny it to a good deal of editorial work nobody wishes to strip of protection.\n\n"
"The difficulty is not that the collectors did nothing but that what they did was small "
"and what they acquired was large. Copyright has no mechanism for matching the scope of a "
"right to the size of the contribution that earned it, and in the ordinary case it does "
"not need one, because the contribution is the whole work. Oral traditions are the case "
"where the ordinary assumption fails, and the law has continued to apply a rule whose "
"justification depends on that assumption holding.")

I = []
def q(iid, pk, skill, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'RC', 'type': 'RC', '_p': pk,
              'passageId': 'LP' + pk, 'skill': skill, 'diff': diff, 'stem': stem,
              'choices': choices, 'answer': 0, 'expl': expl, 'wrong': wrong})

# ------------------------------------------------------------------ LP11 exclusionary
q('LC101','11','lsat_rc_main',3,
 'Which one of the following most accurately expresses the main point of the passage?',
 ['The deterrence rationale leaves the exclusionary rule exposed to an empirical objection, and the reading that would answer it is the one the Court has abandoned',
  'The exclusionary rule should be replaced by a remedy that compensates those subjected to unlawful searches',
  'Studies of whether the exclusionary rule deters unlawful searches have been too weak to settle the question',
  'The exclusionary rule protects the integrity of judicial proceedings rather than the interests of defendants',
  'Critics of the exclusionary rule have misunderstood the purpose the rule was adopted to serve'],
 'The passage sets out the deterrence defence, two objections, the answer to one of them and the awkward consequence of that answer, and closes on the third position and its fate.',
 'B is never recommended, C is one objection, D is the third position rather than the point, and the passage grants one of the criticisms.')
q('LC102','11','lsat_rc_stated',2,
 'According to the passage, the distributive objection to the exclusionary rule is that the rule',
 ['benefits only those against whom an unlawful search produced evidence',
  'imposes costs on the state that are ultimately borne by taxpayers',
  'applies unevenly across jurisdictions with different police practices',
  'protects defendants at the expense of the victims of their crimes',
  'is invoked more often by wealthy defendants than by poor ones'],
 'The second paragraph states it: a person searched unlawfully who turns out to have nothing incriminating receives no remedy at all.',
 'Costs, uneven application, victims and wealth are not the objection as the passage gives it.')
q('LC103','11','lsat_rc_stated',3,
 'The passage states that defenders of the rule respond to the distributive objection by arguing that it',
 ['mistakes a side effect of the rule for the purpose of the rule',
  'relies on studies whose results are too weak to be decisive',
  'would apply equally to any remedy for unlawful searches',
  'undervalues the interest defendants have in a fair trial',
  'assumes that the rule was adopted to compensate those searched'],
 'The third paragraph gives exactly this answer, adding that the rule is not a compensation scheme.',
 'B is the other objection, and C, D and E are not the response described.')
q('LC104','11','lsat_rc_inf',4,
 "It can be inferred from the passage that the author regards the defenders' answer to the distributive objection as",
 ['correct, and as narrowing the ground on which the rule can be defended',
  'incorrect, because the rule does in fact compensate those it benefits',
  'irrelevant, since the empirical objection is the more serious of the two',
  'persuasive only to those who already accept the deterrence rationale',
  'the strongest of the three positions the passage describes'],
 'The passage calls the answer sound as far as it goes and then says it has an awkward consequence: the empirical objection becomes the whole of the case.',
 'The answer is not called incorrect or irrelevant, its persuasiveness is not made conditional, and the third position is the one treated as immune.')
q('LC105','11','lsat_rc_struct',4,
 'The author mentions that the Supreme Court has moved furthest away from the third position primarily in order to',
 ['note that the position least vulnerable to the objections is also the one least available in practice',
  'establish that the third position is unsound as a matter of constitutional law',
  'explain why the deterrence rationale became the dominant justification',
  'suggest that the Court has been persuaded by the empirical objection',
  'indicate that the third position is a recent invention of commentators'],
 'The closing sentence pairs the position\'s immunity with the Court\'s retreat from it, and says the immunity was bought at the price of anything the Court will call a reason.',
 'No unsoundness is asserted, the rise of deterrence is not explained, the Court\'s motive is not given, and nothing suggests the position is new.')
q('LC106','11','lsat_rc_app',4,
 'Which one of the following situations is most analogous to the position of a person who is searched unlawfully but has nothing incriminating, as the passage describes it?',
 ['A safety regulation that penalises firms only when an unsafe practice has already caused an injury, leaving those exposed to the same practice without recourse',
  'A tax credit available only to firms that can document the expenditure it is meant to encourage',
  'A warranty that covers a product only during the first year after purchase',
  'A licensing rule that bars a firm from operating until it has passed an inspection',
  'A fine calculated as a proportion of the profit an offending firm made'],
 'The structure is a remedy that attaches only where the wrong produced a particular downstream result, leaving equally wronged parties with nothing.',
 'Documentation, time limits, prior approval and proportionate fines are different structures.')
q('LC107','11','lsat_rc_app',3,
 'The author would be most likely to agree with which one of the following statements?',
 ['A justification that rests entirely on an effect must be abandoned or replaced if the effect cannot be demonstrated',
  'A rule that benefits the guilty more than the innocent is for that reason unjust',
  'Empirical studies are a poor basis on which to settle questions of constitutional doctrine',
  'Courts should adopt whichever justification for a rule is least vulnerable to objection',
  'The exclusionary rule should be retained in its present form'],
 'The third paragraph draws exactly this consequence: once the rule is purely a deterrent, a deterrent that cannot be shown to deter is hard to defend.',
 'B is the objection the passage says is answered, C contradicts the treatment of the empirical objection, D is a procedural recommendation never made, and E is a verdict the passage withholds.')

# ------------------------------------------------------------------ LP12 mycorrhizal
q('LC108','12','lsat_rc_main',3,
 'Which one of the following most accurately states the main point of the passage?',
 ['A well supported claim about fungal connections has been extended into a claim about cooperation that the evidence does not yet support',
  'Plants exchange resources and warnings through fungal networks connecting their roots',
  'Mycorrhizal fungi take sugars from plants and supply them with phosphorus and nitrogen',
  'Metaphors have no legitimate place in the description of biological systems',
  'Experiments giving plants and fungi conflicting interests have shown the cooperative account to be false'],
 'The passage grants the linkage evidence, finds the functional evidence weak, identifies the metaphor filling the gap, and says what measurement would settle it.',
 'B is the claim under examination, C is background, D is stronger than anything said, and E describes experiments the passage says have rarely been attempted.')
q('LC109','12','lsat_rc_stated',2,
 'According to the passage, the evidence that fungal threads link neighbouring plants includes',
 ['radioactive carbon given to one tree appearing in a neighbour',
  'measurements showing that resources move from well supplied plants to needy ones',
  'observations of plants responding to attacks on their neighbours',
  'the universality of the plant and fungus partnership among land plants',
  'the greater volume of soil a fungus can reach than a root system can'],
 'The second paragraph names the labelled carbon result and the microscope observations as the good evidence for linkage.',
 'B is expressly denied, C is part of the claim rather than the evidence, and D and E are background about the partnership.')
q('LC110','12','lsat_rc_stated',3,
 'The passage states that carbon moving from one plant to another may be doing so because',
 ['the fungus takes the carbon and later releases it, making the fungus the agent',
  'the receiving plant is short of carbon and signals its need',
  'the two plants belong to the same species and are closely related',
  'the measurement technique cannot distinguish carbon from other elements',
  'soil water carries dissolved carbon between root systems'],
 'The second paragraph offers this as the reading that makes the fungus the agent rather than a conduit between plants.',
 'Signalling, relatedness, measurement error and soil water are not the alternative given.')
q('LC111','12','lsat_rc_inf',4,
 'It can be inferred from the passage that an experiment giving the fungus and the plants conflicting interests would be valuable because it would',
 ['allow the direction of any transfer to show which party the transfer serves',
  'establish for the first time that carbon moves between connected plants',
  'demonstrate that the fungal network is more extensive than has been measured',
  'settle whether plants can respond to attacks on their neighbours',
  'show that the cooperative reading of the network is mistaken'],
 'The final paragraph names this design and says exactly what it would identify.',
 'B is already established, C and D are different questions, and E presupposes the answer the experiment is meant to find.')
q('LC112','12','lsat_rc_struct',4,
 'The author refers to a finding that fits being reported as confirmation and a finding that does not as a complication primarily in order to',
 ['describe how a metaphor accepted in advance shapes the interpretation of later evidence',
  'accuse researchers in the field of deliberately suppressing unfavourable results',
  'argue that the cooperative account has been refuted by the findings that do not fit',
  'explain why the quantities of carbon transferred are small',
  'illustrate the difficulty of measuring transfers under field conditions'],
 'It follows directly from the claim that the metaphor supplies an intention the data does not require and then organises further observation.',
 'No accusation of suppression is made, no refutation is claimed, and the quantities and field difficulties are separate points.')
q('LC113','12','lsat_rc_app',4,
 "The author's criticism of the cooperative reading is most similar to which one of the following criticisms?",
 ['A study establishes that two markets move together and is then described as showing that one market responds to the other, which the data does not distinguish',
  'A study uses a sample too small to support the conclusion drawn from it',
  'A study reports a result that later teams have been unable to reproduce',
  'A study measures an outcome that is only loosely related to the one of interest',
  'A study is funded by a party with an interest in its conclusion'],
 'Co movement established, direction and agency assumed: that is the same structure as linkage established and cooperation assumed.',
 'Sample size, reproducibility, proxy outcomes and funding are different criticisms.')
q('LC114','12','lsat_rc_app',3,
 'Which one of the following, if true, would most support the cooperative reading of the fungal network as the passage describes it?',
 ['Carbon is found to move consistently from plants with ample reserves to plants that are shaded and short of them',
  'Fungal connections are found to be more numerous between plants of the same species than between plants of different species',
  'The fungal threads are shown to extend further from the root than had been measured',
  'Plants grown without fungal partners are found to grow more slowly',
  'The same fungal species is found on every continent where the host plants occur'],
 'The passage says the direction of transfer is not consistently from the well supplied to the needy. A consistent direction is what the reading needs and lacks.',
 'Connection counts, extent, dependence and distribution all bear on the partnership rather than on whether transfer serves the plants.')

# ------------------------------------------------------------------ LP13 copyright
q('LC115','13','lsat_rc_main',3,
 'Which one of the following most accurately expresses the main point of the passage?',
 ['A copyright rule that works where the contribution is the whole work misallocates rights when applied to oral traditions',
  'The collectors who recorded blues and work songs contributed nothing that deserved copyright protection',
  'Copyright law should be amended to protect works that exist only as performances',
  'Courts applying the fixation rule to recorded oral traditions decided those cases wrongly',
  'Transcribing an oral performance requires choices that copyright ordinarily treats as authorship'],
 'The final paragraph states it: copyright cannot match the scope of a right to the size of the contribution, and oral traditions are where the assumption that makes this acceptable fails.',
 'B is the response the passage calls weaker than it sounds, C and D are remedies and verdicts never offered, and E is a supporting premise.')
q('LC116','13','lsat_rc_stated',2,
 'According to the passage, a work is protected by copyright only if it is',
 ['fixed in a tangible medium',
  'original to the person claiming protection',
  'registered with a public authority',
  'published for commercial sale',
  'attributable to an identifiable author'],
 'The opening sentence states the fixation requirement, and the passage turns on it.',
 'Originality, registration, publication and attribution figure in the discussion but are not the rule stated.')
q('LC117','13','lsat_rc_stated',3,
 'The passage states that transcription of an oral performance requires choices about all of the following EXCEPT',
 ['whether the performer intended the version to be definitive',
  'which of several versions to fix',
  'which repetitions to preserve',
  'how to render pitch',
  'how to render rhythm'],
 'The third paragraph lists version, repetitions, pitch and rhythm. The performer\'s intention is not among them.',
 'The other four are named in the same sentence.')
q('LC118','13','lsat_rc_inf',4,
 "It can be inferred from the passage that a rule denying copyright protection to the collectors' transcriptions would",
 ['also withdraw protection from editorial work that few would wish to leave unprotected',
  'return the royalties from later commercial recordings to the communities the songs came from',
  'be inconsistent with the requirement that a work be fixed in a tangible medium',
  'apply only to works whose origins lie in an oral tradition',
  "have been rejected by the courts that considered the collectors' claims"],
 'The third paragraph says the choices transcription requires are the sort of thing copyright treats as authorship, and a rule denying them protection would also deny it to editorial work.',
 'B, C, D and E each assert consequences the passage does not draw.')
q('LC119','13','lsat_rc_struct',4,
 'The author characterises the response that the collectors contributed nothing original as weaker than it sounds primarily in order to',
 ['show that the difficulty cannot be resolved by denying that the collectors did anything',
  "defend the courts that upheld the collectors' copyright claims",
  'argue that transcription is a more demanding skill than is generally recognised',
  'establish that the collectors acted in good faith when they registered their copyrights',
  'introduce the proposal that royalties be divided between collectors and communities'],
 'The paragraph blocks the easy answer so that the last paragraph can locate the real problem in the mismatch between contribution and right.',
 'The courts are not defended, the skill point is instrumental, good faith is not discussed, and no proposal is made.')
q('LC120','13','lsat_rc_app',4,
 'Which one of the following is most analogous to the mismatch the author identifies in the final paragraph?',
 ['A finder who adds a frame to an unattributed painting and thereby acquires title to the painting',
  'An editor who corrects the proofs of a novel and is paid a fee rather than a royalty',
  'A translator who receives a copyright in the translation but not in the original work',
  'A photographer who is refused copyright in a photograph of a public building',
  'An archivist who catalogues a collection and is credited in the published guide'],
 'A small addition producing a right over the whole is exactly the structure the passage describes.',
 'B, C and E match contribution to reward, and D is a denial of protection rather than a mismatch.')
q('LC121','13','lsat_rc_app',3,
 'The passage suggests that copyright law manages without a mechanism for matching a right to the size of a contribution because',
 ['in the ordinary case the contribution being protected is the entire work',
  'courts can adjust royalties when the contribution is unusually small',
  'most works protected by copyright have a single identifiable author',
  'the fixation requirement excludes contributions that are too slight',
  'registration allows competing claims to be resolved before they reach a court'],
 'The last paragraph says the ordinary case does not need the mechanism because the contribution is the whole work.',
 'Judicial adjustment, single authorship, a slightness threshold and registration are not what the passage gives as the reason.')

P['14'] = ("Development economics has spent two decades absorbing the randomised controlled "
"trial. The method addresses a real problem. A programme that hands out bed nets and is "
"followed by a fall in malaria may have caused the fall or may have been placed where the "
"fall was coming anyway, and no amount of statistical adjustment can separate the two if "
"the placement was not random. Randomising the placement does separate them, and the "
"result is a causal estimate that does not depend on a model of how placement was decided.\n\n"
"The gains have been substantial and they have a boundary that is easy to lose sight of. "
"A trial estimates the effect of a particular programme, run by a particular organisation, "
"in a particular place, at a particular scale. Each of those qualifications can matter. A "
"programme that works when delivered by a well supervised research team may not work when "
"delivered by a ministry; a programme that raises the incomes of its participants at small "
"scale may not do so at large scale if the gains came from taking work that would "
"otherwise have gone to a neighbour.\n\n"
"Advocates of the method are aware of these limits and have responded by running trials in "
"more places and at larger scales, which is the right response and an expensive one. "
"Critics argue that the limits are not a matter of coverage but of kind: what a policy "
"maker needs is a judgment about a mechanism, and a mechanism cannot be established by "
"accumulating estimates of effects, however many places they come from.\n\n"
"The disagreement is less sharp than it appears. Both sides accept that a mechanism is "
"what transfers and that a trial does not deliver one directly. What separates them is a "
"judgment about the second best: whether a well founded estimate from somewhere else is a "
"better guide to a decision than an unverified mechanism, or worse. That is a question "
"about the reliability of the alternatives, and neither side has produced much evidence "
"about it, which is an odd position for a field that made its reputation by demanding "
"evidence.")

P['15'] = ("Passage A\n\n"
"Constitutional interpretation should be governed by the original public meaning of the "
"text: what an ordinary reader at the time of ratification would have understood the words "
"to say. The alternative is not a different method but the absence of one. A judge who "
"consults contemporary values is consulting something that has no determinate content and "
"that he will inevitably read as agreeing with him. Originalism constrains because the "
"historical record is external to the judge and can show him to be wrong.\n\n"
"The familiar objection is that the record is indeterminate and that historians disagree. "
"They do, but the disagreement has edges. There are propositions about eighteenth century "
"usage that the evidence forecloses, and a method that can be shown to be wrong about some "
"things is doing more work than one that cannot be shown to be wrong about anything.\n\n"
"Passage B\n\n"
"The case for originalism rests on constraint, and constraint is an empirical claim. It is "
"testable and it has not been tested. What we observe is that judges who describe "
"themselves as originalists reach conclusions that track their prior commitments about as "
"closely as anyone else's do, and that where the historical record cuts against those "
"conclusions it is characterised as indeterminate rather than as controlling.\n\n"
"This is not an accusation of bad faith. The historical record for any contested provision "
"is large, fragmentary and written by people who disagreed with one another, and a "
"conscientious reader working through it has a great deal of room without ever knowingly "
"choosing an answer. The point is that a method whose discipline depends on a record of "
"that character supplies less discipline than its defenders claim, and that the "
"comparison they invite, between a constrained method and an unconstrained one, is not the "
"comparison that the evidence supports.")

P['16'] = ("Alfred Wegener proposed in 1912 that the continents had once formed a single mass "
"and had since moved apart. He assembled the fit of the coastlines, matching rock "
"formations on opposite sides of the Atlantic, and fossil species distributed in ways that "
"no ocean crossing could explain. The proposal was rejected by the geological establishment "
"for half a century, and the usual account of the rejection treats it as a failure of "
"imagination.\n\n"
"That account is too comfortable. Wegener's critics had a specific objection and it was a "
"good one: he could name no mechanism capable of moving a continent. His own suggestions, "
"that the continents were driven by tidal forces and by a drift toward the equator, were "
"calculated by physicists to be too weak by several orders of magnitude, and Wegener "
"conceded as much. A theory with strong circumstantial evidence and no possible cause is in "
"an awkward position, and the geologists who declined to accept it were applying a standard "
"they applied elsewhere.\n\n"
"What broke the impasse was not new argument about the old evidence but a new kind of "
"evidence from a place nobody had been looking. Surveys of the sea floor after 1950 found "
"mid ocean ridges, magnetic striping symmetrical about them, and ocean crust nowhere older "
"than a small fraction of the age of the continents. These findings supplied the mechanism, "
"and within a decade the profession had changed its mind.\n\n"
"The episode is often taught as a lesson about resistance to new ideas. It teaches "
"something narrower and more useful. The demand for a mechanism was reasonable and the "
"absence of one was a real defect, which the circumstantial evidence could not repair "
"however much of it accumulated. What the case shows is not that the establishment was "
"closed but that a certain kind of gap in a theory cannot be filled from the direction the "
"theory came from.")

# ------------------------------------------------------------------ LP14 trials
q('LC122','14','lsat_rc_main',4,
 'Which one of the following most accurately expresses the main point of the passage?',
 ["A dispute about the reach of randomised trials turns on a comparison neither side has investigated",
  "Randomised controlled trials have solved the problem of separating a programme's effect from the conditions in which it was placed",
  "Randomised trials should be run in more places and at larger scales before their results are used",
  "Policy makers need judgments about mechanisms, which randomised trials cannot supply",
  "Development economics has become less rigorous since it adopted the randomised trial"],
 "The final paragraph narrows the disagreement to a judgment about the second best and notes that neither side has produced evidence about it.",
 "B is the method's achievement, C is the advocates' response, D is the critics' claim, and E is never said.")
q('LC123','14','lsat_rc_stated',2,
 'According to the passage, randomising the placement of a programme addresses the problem that',
 ["a programme may have been placed where the outcome it aims at was already improving",
  "programmes are often delivered by organisations with an interest in their success",
  "the same programme may have different effects at different scales",
  "participants may change their behaviour because they know they are being studied",
  "outcomes are frequently measured by the organisation that ran the programme"],
 "The first paragraph gives exactly this: a fall that may have been coming anyway, which no adjustment can separate if placement was not random.",
 "Delivery, scale, behaviour change and self measurement are other issues, two of them raised later as limits rather than as the problem randomisation solves.")
q('LC124','14','lsat_rc_stated',3,
 "The passage states that a programme raising participants' incomes at small scale may fail to do so at large scale because",
 ["the gains may have come from work that would otherwise have gone to someone else",
  "large programmes attract participants who are less motivated than early ones",
  "the organisations that run large programmes are less well supervised",
  "the cost per participant rises as a programme expands",
  "measurement becomes less accurate as the number of participants grows"],
 "The second paragraph names displacement as the reason a small scale income gain need not survive expansion.",
 "Motivation, supervision, cost and measurement are not the mechanism given for the scale limit.")
q('LC125','14','lsat_rc_inf',4,
 "It can be inferred from the passage that the author regards the advocates' response of running more and larger trials as",
 ["appropriate, though it does not meet the objection the critics actually make",
  "misguided, because the limits of the method are a matter of coverage",
  "sufficient to establish the mechanisms policy makers require",
  "less expensive than the critics have suggested",
  "an admission that the method cannot support policy decisions"],
 "The third paragraph calls it the right response and an expensive one, and then states that the critics' objection is about kind rather than coverage.",
 "B reverses the critics' position, C contradicts the fourth paragraph, D reverses the cost remark, and E is not conceded.")
q('LC126','14','lsat_rc_struct',4,
 'The final paragraph functions primarily to',
 ["identify the question on which the two positions actually differ and note that it is unexamined",
  "adjudicate between the advocates and the critics in favour of the critics",
  "propose a research programme that would combine the strengths of both approaches",
  "concede that the criticisms of the randomised trial have been overstated",
  "explain why mechanisms are what transfer from one setting to another"],
 "It says both sides agree that mechanisms transfer and that trials do not deliver them, locates the disagreement in a judgment about the second best, and observes that neither side has evidence about it.",
 "No side is preferred, no programme is proposed, no concession of overstatement is made, and the transfer point is common ground rather than the paragraph's work.")
q('LC127','14','lsat_rc_app',4,
 'Which one of the following best illustrates the kind of question the author says neither side has produced evidence about?',
 ["Whether decisions guided by a trial result from another country turn out better than decisions guided by an untested account of how the programme works",
  "Whether randomised trials can be conducted at the scale at which programmes are actually run",
  "Whether ministries deliver programmes as reliably as research teams do",
  "Whether the participants in a trial are representative of the wider population",
  "Whether displacement effects are large enough to matter at national scale"],
 "The unexamined question is the comparison between a well founded estimate from elsewhere and an unverified mechanism, judged by which is the better guide to a decision.",
 "Scale, delivery, representativeness and displacement are limits the passage discusses rather than the comparison it says is unexamined.")
q('LC128','14','lsat_rc_app',3,
 'The author would be most likely to agree with which one of the following statements?',
 ["A field that requires evidence for its conclusions should require it also for its claims about its own methods",
  "Randomised trials should be abandoned in favour of judgments about mechanisms",
  "The limits of the randomised trial can be overcome by running trials in enough settings",
  "Statistical adjustment is an adequate substitute for randomisation where randomisation is impossible",
  "Mechanisms established in one setting can be relied on in any other"],
 "The closing clause calls the absence of evidence about the comparison an odd position for a field that made its reputation by demanding evidence.",
 "B, C, D and E are positions the passage either attributes to one side or contradicts outright.")

# ------------------------------------------------------------------ LP15 originalism
q('LC129','15','lsat_rc_main',4,
 'Which one of the following most accurately describes the relationship between the two passages?',
 ["Passage B accepts the standard by which passage A defends its method and argues that the method has not been shown to meet it",
  "Passage B denies the premise on which passage A's argument rests and offers an alternative method",
  "Passage B agrees with passage A's conclusion but reaches it by a different route",
  "Passage B attributes to defenders of the method a motive that passage A does not address",
  "Passage B argues that the historical record is more determinate than passage A allows"],
 "A rests the case on constraint; B says constraint is an empirical claim, testable, untested, and not borne out by what is observed.",
 "B offers no alternative method, reaches the opposite conclusion, expressly disclaims an accusation of bad faith, and treats the record as less determinate rather than more.")
q('LC130','15','lsat_rc_stated',2,
 'According to passage A, the alternative to interpreting the text by its original public meaning is',
 ["the absence of any method at all",
  "a method that gives greater weight to precedent",
  "a method that defers to the judgment of legislatures",
  "a method that treats the historical record as indeterminate",
  "a method that asks what the drafters privately intended"],
 "The first paragraph of A states this: the alternative is not a different method but the absence of one.",
 "Precedent, deference, indeterminacy and drafters' intentions are not what A names.")
q('LC131','15','lsat_rc_stated',3,
 "Passage B states that where the historical record cuts against a self described originalist judge's conclusion, the record is",
 ["characterised as indeterminate rather than as controlling",
  "supplemented with evidence of the drafters' private intentions",
  "set aside in favour of contemporary values",
  "read as supporting the opposite conclusion",
  "referred to historians for further study"],
 "The first paragraph of B says exactly this.",
 "The other four describe moves B does not attribute to such judges.")
q('LC132','15','lsat_rc_inf',4,
 "It can be inferred that the author of passage B would respond to passage A's claim that a method which can be shown to be wrong about some things is doing more work than one that cannot by",
 ["granting it while denying that the showing happens often enough to constrain outcomes",
  "denying that any method can be shown to be wrong about matters of interpretation",
  "arguing that the claim assumes what it sets out to prove about contemporary values",
  "pointing out that historians disagree about eighteenth century usage",
  "accepting it as decisive in favour of the method passage A defends"],
 "B concedes that the record is large and fragmentary rather than empty, and argues that a conscientious reader has room without ever knowingly choosing, which is a claim about frequency rather than possibility.",
 "B does not deny that any method can be checked, makes no circularity charge, treats historians' disagreement as A's objection rather than B's, and reaches the opposite verdict.")
q('LC133','15','lsat_rc_struct',4,
 'The second paragraph of passage B serves primarily to',
 ["forestall a misreading of the criticism it has just made",
  "supply the evidence for the claim made in the first paragraph",
  "concede a point to passage A before rejecting its conclusion",
  "describe the method by which the historical record should be read",
  "explain why the historical record for contested provisions is fragmentary"],
 "It opens by saying this is not an accusation of bad faith and then explains how a conscientious reader could reach the observed pattern.",
 "It supplies an explanation rather than evidence, concedes nothing to A's conclusion, prescribes no method, and the character of the record is a premise rather than the point.")
q('LC134','15','lsat_rc_app',4,
 'Both passages would agree with which one of the following statements?',
 ["Whether a method of interpretation constrains the judges who use it is a question that matters to its defence",
  "Judges who describe themselves as originalists reach conclusions that track their prior commitments",
  "The historical record forecloses some propositions about eighteenth century usage",
  "A method of interpretation that cannot be shown to be wrong is for that reason unacceptable",
  "Contemporary values have no determinate content that a judge could consult"],
 "A rests its case on constraint and B tests the same claim, so both treat constraint as the standard that matters.",
 "B asserts the second and A would deny it; A asserts the third and fifth; and the fourth is A's argument rather than shared ground.")
q('LC135','15','lsat_rc_app',3,
 "Which one of the following, if true, would most strengthen passage B's argument?",
 ["A study finds that originalist and non originalist judges are equally likely to reach the outcome their prior writings favour",
  "Historians agree about the original public meaning of most constitutional provisions",
  "Self described originalists cite historical sources more often than other judges do",
  "Courts have overturned several originalist decisions on historical grounds",
  "The historical record for contested provisions has grown larger as more archives are digitised"],
 "B's central observation is that originalists track their prior commitments about as closely as anyone else. A study measuring exactly that is direct support.",
 "B is weakened by agreement among historians and by decisions overturned on historical grounds, citation frequency is not the claim, and archive growth is neutral.")

# ------------------------------------------------------------------ LP16 Wegener
q('LC136','16','lsat_rc_main',3,
 'Which one of the following most accurately expresses the main point of the passage?',
 ["The rejection of continental drift reflected a reasonable demand that the evidence available at the time could not satisfy",
  "Wegener's critics rejected continental drift because they were unwilling to consider an unfamiliar idea",
  "Sea floor surveys after 1950 established that the continents had once formed a single mass",
  "A theory supported by circumstantial evidence should be accepted even where no mechanism is known",
  "Geologists apply a stricter standard to theories proposed by outsiders than to those proposed by colleagues"],
 "The final paragraph states it: the demand for a mechanism was reasonable, the absence was a real defect, and the gap could not be filled from the direction the theory came from.",
 "B is the account the passage calls too comfortable, C is the evidence rather than the point, D is contradicted, and E is never suggested.")
q('LC137','16','lsat_rc_stated',2,
 'According to the passage, the evidence Wegener assembled included all of the following EXCEPT',
 ["magnetic striping symmetrical about mid ocean ridges",
  "the fit of the coastlines on opposite sides of the Atlantic",
  "matching rock formations on opposite sides of the Atlantic",
  "fossil species distributed in ways no ocean crossing could explain",
  "the single mass from which he held the continents to have separated"],
 "The magnetic striping came from sea floor surveys after 1950, decades after Wegener's proposal.",
 "The coastline fit, the rock formations and the fossil distributions are named in the first paragraph, and the single mass is the proposal itself.")
q('LC138','16','lsat_rc_stated',3,
 "The passage states that Wegener's own suggested mechanisms were",
 ["calculated by physicists to be too weak by several orders of magnitude",
  "rejected by geologists before they had been calculated",
  "withdrawn by Wegener before the theory was published",
  "based on processes occurring at mid ocean ridges",
  "accepted as plausible even by those who rejected the theory"],
 "The second paragraph says tidal forces and equatorial drift were calculated to be too weak by several orders of magnitude, and that Wegener conceded it.",
 "The other four misstate the sequence or the verdict.")
q('LC139','16','lsat_rc_inf',4,
 'It can be inferred from the passage that additional evidence of the kind Wegener assembled would have',
 ["left the theory in the same position, because it could not supply the missing mechanism",
  "eventually persuaded the geological establishment to accept the theory",
  "been rejected by physicists on the same grounds as his proposed mechanisms",
  "made the sea floor surveys of the 1950s unnecessary",
  "shown the demand for a mechanism to be unreasonable"],
 "The closing paragraph says the circumstantial evidence could not repair the defect however much of it accumulated.",
 "B contradicts that sentence, C misapplies the physicists' objection, D reverses the role of the surveys, and E contradicts the passage's verdict on the demand.")
q('LC140','16','lsat_rc_struct',4,
 'The author describes the usual account of the rejection as too comfortable primarily in order to',
 ["signal that the passage will defend the critics on grounds the usual account ignores",
  "argue that the geological establishment was in fact more receptive than is supposed",
  "question whether the rejection lasted as long as is generally claimed",
  "introduce the sea floor evidence that eventually settled the matter",
  "suggest that Wegener himself was responsible for the delay in acceptance"],
 "The phrase closes the first paragraph and the second opens with the critics' specific objection, called a good one.",
 "Receptiveness, duration and Wegener's responsibility are not claimed, and the sea floor evidence arrives two paragraphs later.")
q('LC141','16','lsat_rc_app',4,
 'Which one of the following situations is most analogous to the position of continental drift before 1950, as the passage describes it?',
 ["A medical hypothesis with consistent clinical correlations and no known pathway by which the agent could cause the disease",
  "A medical hypothesis supported by a single trial that other teams have not reproduced",
  "A medical hypothesis rejected because the researcher proposing it lacked formal training",
  "A medical hypothesis that predicts an outcome no instrument of the period could measure",
  "A medical hypothesis abandoned after its author withdrew the data supporting it"],
 "Strong circumstantial evidence with no available cause is exactly the shape the passage gives the theory.",
 "Reproducibility, credentials, unmeasurable predictions and withdrawn data are different defects.")
q('LC142','16','lsat_rc_app',3,
 'The passage suggests that the lesson usually drawn from the Wegener episode is mistaken chiefly because it',
 ["treats as closed mindedness what was the application of a standard applied elsewhere",
  "overstates how long the geological establishment resisted the theory",
  "credits the sea floor surveys with more than they established",
  "assumes that Wegener had no mechanism to offer",
  "ignores the role played by physicists in the dispute"],
 "The second paragraph says the geologists were applying a standard they applied elsewhere, which is the answer to the failure of imagination reading.",
 "Duration, the surveys, Wegener's suggestions and the physicists are all handled accurately by the passage rather than misstated by the usual lesson.")

P['17'] = ("The class action allows one plaintiff to sue on behalf of everyone similarly "
"harmed. Its usual justification is access: a claim worth two hundred dollars is not worth "
"bringing alone, and a defendant who inflicts a small loss on a million people is "
"effectively immune unless the claims can be combined. Aggregation converts a set of "
"claims that nobody would pursue into one that somebody will.\n\n"
"The mechanism has a feature that its justification does not mention. Once aggregated, the "
"claim is controlled not by the people whose it is but by a lawyer whose fee depends on a "
"settlement and who is chosen, in practice, by whoever files first. The absent members are "
"represented in the sense that their interests are asserted and in no other sense: they do "
"not instruct counsel, they usually do not know the case exists, and the notice they "
"receive is designed by the parties who want them not to object.\n\n"
"Courts have responded with review. A settlement must be approved as fair, and the judge "
"approving it is asked to protect people who are not present against a bargain struck by "
"two parties who both want it approved. Nobody in the room has an interest in identifying "
"its defects, and the record the judge reads is assembled by the people who made it. That "
"the approval standard is demanding on paper does not supply the adversarial testing the "
"rest of the system depends on.\n\n"
"The objection is often taken to be an argument against class actions. It is better read "
"as an argument about what they are. A class action is not a lawsuit brought by a million "
"people; it is a regulatory proceeding conducted by a private party and reviewed by a "
"judge, and the standards appropriate to it are the standards appropriate to regulation "
"rather than those appropriate to litigation between parties who can look after "
"themselves. Framed that way the absence of adversarial testing is a design question with "
"known answers, rather than an embarrassment to be managed by insisting that the members "
"are really the clients.")

P['18'] = ("New Caledonian crows make tools. They cut hooks from twigs and barbed strips from "
"pandanus leaves, carry favoured tools between sites, and in captivity have solved "
"problems requiring a tool to be used on another tool. The behaviour was for a time "
"treated as evidence of a general reasoning capacity, and the inference was encouraged by "
"the crows' performance on tasks designed for primates.\n\n"
"Two findings have complicated the picture. The first is that hand raised crows with no "
"opportunity to observe an adult still produce recognisable tools, which indicates a strong "
"inherited component to the behaviour and weakens the analogy with a general capacity "
"applied to a new problem. The second is that the crows fail at tasks only slightly "
"different from those they solve. A crow that will bend a wire into a hook to lift a bucket "
"may not push the same bucket over when lifting is impossible.\n\n"
"The natural conclusion is that the tool behaviour is specialised rather than general, and "
"that conclusion is probably right. It should be drawn carefully, because the same pattern "
"of failure on near neighbours of solved tasks is found in every species that has been "
"tested carefully, including our own. Human subjects are famously bad at transferring a "
"solution across a change of surface detail, and nobody concludes from this that human "
"reasoning is a bundle of narrow specialisations, although some have argued exactly "
"that.\n\n"
"What the crow work has actually established is that a species with no recent common "
"ancestry with primates, and a brain organised on a different plan, arrives at behaviour "
"that meets any reasonable behavioural definition of tool use and manufacture. Whether it "
"arrives by the route primates take is a separate question and a harder one, and the "
"temptation to answer it by ranking species on a single scale is the same temptation the "
"field has failed to resist for a century.")

P['19'] = ("A translator faces a choice that has no neutral option. A translation may bring "
"the text toward the reader, replacing what is unfamiliar with something the reader will "
"recognise, or bring the reader toward the text, preserving what is strange at the cost of "
"fluency. The terms usually used are domestication and foreignisation, and the debate "
"between them is old.\n\n"
"The case for domestication is that a translation is a text in its own language and should "
"work as one. A reader who stumbles over a construction that no English writer would use "
"has been given an obstacle the original readers never faced, which is a departure from the "
"original rather than a fidelity to it. The case for foreignisation is that the strangeness "
"is often the point: a work written against the conventions of its own literature becomes, "
"when smoothed into the target language, a work that observes them.\n\n"
"Both cases are strong and they are not symmetrical. Domestication has the better argument "
"about the ordinary sentence, where a literal rendering is simply worse English and "
"communicates less. Foreignisation has the better argument about the passages that matter "
"most, where an author's departures from ordinary usage are doing the work the reader came "
"for. A policy applied uniformly will therefore be wrong in one direction or the other, and "
"the interesting question is not which policy to adopt but how a translator decides which "
"sentences are which.\n\n"
"That question is rarely addressed, and the reason may be that answering it would expose "
"how much of translation is criticism. Deciding that a departure from usage is doing work "
"is a judgment about what the text is for, arrived at by reading it closely, and a "
"translator who makes that judgment well is doing what a critic does and then acting on it "
"in a medium where the reasoning cannot be shown.")

P['20'] = ("Between a quarter and a half of employment in many countries is informal: "
"unregistered, untaxed, and invisible to the statistics that describe the economy. The "
"figure is usually presented as a measurement problem to be solved, and considerable "
"effort has gone into solving it, through household surveys, satellite imagery of "
"night time light, and estimates derived from currency in circulation.\n\n"
"These methods disagree with one another, which is expected, and they disagree in a "
"patterned way, which is more informative. Currency based estimates are highest, survey "
"based estimates lowest, and the gap is widest in countries where enforcement is most "
"aggressive. The obvious reading is that respondents in those countries conceal more, and "
"it is probably correct. It also implies something the measurement literature is slow to "
"say: the size of the informal sector is not a fact about the economy waiting to be "
"measured accurately, but partly a fact about the relationship between people and the "
"state, which the act of measuring is part of.\n\n"
"This is not a counsel of despair. It is a reason to be specific about what a particular "
"number is for. A figure used to estimate lost tax revenue and a figure used to estimate "
"how many households lack social protection are answering different questions, and the "
"same activity may belong in one and not the other: a subsistence trader owes little tax "
"and lacks all protection.\n\n"
"Treating informality as a single quantity has consequences in policy as well as "
"measurement. Programmes to formalise employment are evaluated by whether registrations "
"rise, which they can do without any change in the conditions under which people work, and "
"which they routinely do where registration is made a condition of something people already "
"needed. A programme that improves a number it was designed to improve, by a route that "
"leaves the underlying situation where it was, is the ordinary outcome of measuring one "
"thing and caring about another.")

# ------------------------------------------------------------------ LP17 class actions
q('LC143','17','lsat_rc_main',4,
 'Which one of the following most accurately expresses the main point of the passage?',
 ["An objection usually taken as an argument against class actions is better understood as identifying what kind of proceeding a class action is",
  "Class actions should be abolished because absent members cannot control the claims brought on their behalf",
  "Judicial review of class settlements is inadequate because the parties who assemble the record both want approval",
  "The access justification for class actions is the only one that withstands examination",
  "Absent class members should be given a greater role in instructing counsel"],
 "The final paragraph reframes the objection: a class action is a regulatory proceeding conducted privately, and the standards appropriate to it are regulatory ones.",
 "B is expressly rejected as the reading, C is a step in the argument, D is not claimed, and E is the insistence the passage says should be abandoned.")
q('LC144','17','lsat_rc_stated',2,
 'According to the passage, the usual justification for the class action is that it',
 ["makes it worth bringing claims that would be too small to bring alone",
  "allows courts to impose penalties larger than any individual could obtain",
  "reduces the number of separate proceedings a court must hear",
  "gives claimants access to lawyers they could not otherwise afford",
  "prevents defendants from settling with claimants one at a time"],
 "The first paragraph gives access in exactly these terms.",
 "Penalties, docket efficiency, affordability and sequential settlement are not the justification stated.")
q('LC145','17','lsat_rc_stated',3,
 'The passage states that the notice absent class members receive is',
 ["designed by parties who want them not to object",
  "required by statute to explain the terms of any settlement",
  "sent only to members whose claims exceed a threshold",
  "prepared by the judge who will review the settlement",
  "the principal means by which members instruct counsel"],
 "The second paragraph says this directly.",
 "Statutory content, thresholds, judicial authorship and instruction are not what the passage says about notice.")
q('LC146','17','lsat_rc_inf',4,
 'It can be inferred from the passage that the author regards the requirement of judicial approval as',
 ["a real safeguard that cannot supply what adversarial testing supplies",
  "sufficient protection for absent members in most cases",
  "a formality that courts apply without serious attention",
  "unnecessary once the members have received adequate notice",
  "the feature that distinguishes a class action from a regulatory proceeding"],
 "The third paragraph grants that the standard is demanding on paper and says it does not supply the adversarial testing the rest of the system depends on.",
 "B and D overstate its adequacy, C accuses courts of inattention the passage does not allege, and E reverses the final paragraph.")
q('LC147','17','lsat_rc_struct',4,
 "The author's observation that nobody in the room has an interest in identifying a settlement's defects functions primarily to",
 ["explain why judicial review cannot do the work adversarial process does elsewhere",
  "accuse the lawyers involved of concealing defects from the court",
  "argue that settlements should be reviewed by a second judge",
  "show that the approval standard is less demanding than it appears on paper",
  "establish that most class settlements are unfair to absent members"],
 "It is the reason the demanding standard does not supply adversarial testing, which is the sentence that follows.",
 "No concealment is alleged, no second judge is proposed, the standard is called demanding on paper, and no claim about most settlements is made.")
q('LC148','17','lsat_rc_app',4,
 'The reframing proposed in the final paragraph would most likely lead the author to favour which one of the following?',
 ["Procedures borrowed from administrative agencies, such as a public comment period and a reasoned decision on objections",
  "A rule requiring every absent member to opt in before the claim may proceed",
  "A cap on the fee that class counsel may recover from a settlement",
  "A requirement that class counsel be chosen by the member with the largest claim",
  "Abolition of the class action in favour of individual suits"],
 "If the proceeding is regulatory, the design questions have known answers in regulatory practice, which is what the paragraph says.",
 "Opt in, fee caps and counsel selection all treat it as litigation between clients and counsel, and abolition is the reading the paragraph rejects.")
q('LC149','17','lsat_rc_app',3,
 'Which one of the following best expresses the sense in which the passage says absent members are represented?',
 ["Their interests are asserted on their behalf, and nothing more follows from the relationship",
  "They are bound by the outcome but may withdraw at any point before settlement",
  "They select counsel indirectly through the member who files first",
  "They are consulted about the terms of any settlement before it is approved",
  "They are protected by a judge who acts as their advocate"],
 "The second paragraph says exactly this: asserted, and in no other sense, with three specifics following.",
 "Withdrawal, indirect selection, consultation and judicial advocacy are all things the passage denies or does not claim.")

# ------------------------------------------------------------------ LP18 crows
q('LC150','18','lsat_rc_main',4,
 'Which one of the following most accurately states the main point of the passage?',
 ["The crow findings establish tool use on an independent evolutionary line, and the inference to a general capacity should be drawn cautiously for reasons that apply to every species",
  "Tool use in New Caledonian crows is a narrow specialisation rather than a general reasoning capacity",
  "Hand raised crows produce tools without observing adults, which shows the behaviour is inherited",
  "Human reasoning is better described as a bundle of narrow specialisations than as a general capacity",
  "Species should not be ranked on a single scale of intelligence"],
 "The final paragraph names what has actually been established and separates it from the harder question, and the third paragraph makes the caution symmetrical across species.",
 "B is called probably right but stated more carefully in the passage, C is one finding, D is a position the passage attributes to others, and E is a closing remark rather than the point.")
q('LC151','18','lsat_rc_stated',2,
 'According to the passage, New Caledonian crows in captivity have',
 ["solved problems requiring a tool to be used on another tool",
  "taught tool manufacture to crows raised without adults",
  "outperformed primates on tasks designed for primates",
  "produced tools from materials not found in their natural range",
  "abandoned tool use when food was made freely available"],
 "The first paragraph names this among the behaviours observed.",
 "Teaching, outperforming primates, novel materials and abandonment are not stated.")
q('LC152','18','lsat_rc_stated',3,
 'The passage states that a crow able to bend a wire into a hook to lift a bucket may nonetheless fail to',
 ["push the same bucket over when lifting it is impossible",
  "use a tool it has not previously encountered",
  "select the longer of two available sticks",
  "retrieve a tool it has carried between sites",
  "repeat the solution on a second occasion"],
 "The second paragraph gives this as the example of failure on a near neighbour of a solved task.",
 "Novel tools, length selection, retrieval and repetition are not the failure described.")
q('LC153','18','lsat_rc_inf',4,
 "It can be inferred that the author mentions human subjects' difficulty in transferring solutions across changes of surface detail in order to suggest that",
 ["failure on near neighbours of solved tasks is weaker evidence of narrow specialisation than it first appears",
  "human reasoning and crow tool use rest on the same underlying mechanism",
  "the tasks given to crows have been poorly designed",
  "comparisons between species are of little scientific value",
  "the conclusion that crow tool use is specialised is mistaken"],
 "The paragraph grants that the specialised conclusion is probably right and then notes the same pattern in every species tested, including humans, whom nobody describes that way on that basis.",
 "B, C and D overreach, and E contradicts the concession the paragraph makes.")
q('LC154','18','lsat_rc_struct',4,
 'The third paragraph relates to the second in that it',
 ["accepts the conclusion the second paragraph supports while questioning the strength of one line of support for it",
  "rejects the findings reported in the second paragraph as unreplicated",
  "offers an alternative explanation of the findings reported in the second paragraph",
  "extends the second paragraph's findings to species other than crows",
  "concedes that the second paragraph's findings are inconsistent with the first paragraph"],
 "It says the natural conclusion is probably right, then undercuts the near neighbour failures as evidence by noting they occur everywhere.",
 "Nothing is rejected as unreplicated, no alternative explanation is offered, the extension is to the evidence rather than the findings, and no inconsistency is conceded.")
q('LC155','18','lsat_rc_app',4,
 'Which one of the following research findings would most strengthen the case that crow tool use reflects a general capacity rather than a specialisation?',
 ["Crows transfer a solution learned with one kind of material to a problem requiring a different kind, without further training",
  "Crows in a new population are observed manufacturing hooks of the same design as those described",
  "Crows carry favoured tools over longer distances than had previously been recorded",
  "Hand raised crows improve their tool designs over successive attempts",
  "Crows outperform primates on a task requiring a tool to be used on another tool"],
 "Transfer across a change of material without retraining is precisely the capacity the near neighbour failures are said to argue against.",
 "Design consistency, carrying distance, within task improvement and a single comparative result are all compatible with a specialisation.")
q('LC156','18','lsat_rc_app',3,
 'The author would be most likely to describe the ranking of species on a single scale of intelligence as',
 ["a persistent temptation that substitutes for the harder comparative question",
  "a useful summary of differences that are otherwise hard to state",
  "a methodological error confined to the study of birds",
  "an approach that the field abandoned during the last century",
  "the only available way of comparing distantly related species"],
 "The closing sentence calls it a temptation the field has failed to resist for a century, offered in place of the separate and harder question.",
 "B and E endorse it, C narrows it to birds, and D says it was abandoned when the passage says the opposite.")

# ------------------------------------------------------------------ LP19 translation
q('LC157','19','lsat_rc_main',3,
 'Which one of the following most accurately expresses the main point of the passage?',
 ["Because neither general policy is right everywhere, the real question is how a translator judges which sentences call for which, and that question implicates criticism",
  "Foreignisation preserves what matters most in a literary work and should be preferred",
  "Domestication produces better English and should be preferred for ordinary sentences",
  "The debate between domestication and foreignisation cannot be resolved",
  "Translators should be trained as literary critics before being allowed to translate"],
 "The third paragraph names the interesting question and the fourth says why it is rarely addressed.",
 "B and C are the halves the passage balances, D is more defeatist than the passage, and E is a recommendation never made.")
q('LC158','19','lsat_rc_stated',2,
 'According to the passage, the case for domestication rests on the claim that',
 ["a translation is a text in its own language and should work as one",
  "readers of translations are less patient than readers of original works",
  "the conventions of the target language are more flexible than those of the source",
  "literal renderings misrepresent the meaning of the original",
  "most readers of a translation cannot read the original"],
 "The second paragraph states this as the case for domestication.",
 "Patience, flexibility, misrepresentation and readership are not the argument given.")
q('LC159','19','lsat_rc_stated',3,
 'The passage states that a work written against the conventions of its own literature becomes, when smoothed into the target language,',
 ["a work that observes those conventions",
  "a work whose author is unrecognisable",
  "a work that reads as a period piece",
  "a work of criticism rather than of literature",
  "a work more faithful to the original than a literal rendering"],
 "The second paragraph says exactly this as the case for foreignisation.",
 "The other four are not what the passage says the smoothing produces.")
q('LC160','19','lsat_rc_inf',4,
 'It can be inferred from the passage that the author regards a translator who applies foreignisation uniformly as likely to produce',
 ["renderings of ordinary sentences that are worse English and communicate less",
  "a text that no reader of the target language will finish",
  "a text more faithful to the original than any alternative",
  "the same result as a translator who applies domestication uniformly",
  "a translation that critics will prefer to one produced by any other policy"],
 "The third paragraph says domestication has the better argument about the ordinary sentence, where a literal rendering is simply worse English and communicates less.",
 "B and E overstate, C contradicts the balance struck, and D denies the asymmetry the paragraph insists on.")
q('LC161','19','lsat_rc_struct',4,
 'The author says the two cases are not symmetrical primarily in order to',
 ["show that each has the better argument over a different part of a text, which is why a uniform policy fails",
  "indicate that the case for domestication is the stronger of the two overall",
  "concede that the debate has been conducted unfairly by its participants",
  "explain why translators have avoided addressing how they decide",
  "argue that the two cases are ultimately reconcilable into a single principle"],
 "The sentence introduces the split between ordinary sentences and passages that matter most, from which the failure of uniform policy follows.",
 "Neither case is called stronger overall, no unfairness is alleged, the avoidance is explained in the last paragraph, and no single principle is proposed.")
q('LC162','19','lsat_rc_app',4,
 "Which one of the following situations is most analogous to the translator's position as the final paragraph describes it?",
 ["A restorer who must decide which irregularities in a painting are damage and which are the painter's hand, and whose reasoning survives only in the finished surface",
  "An editor who applies a house style guide consistently across every manuscript",
  "A curator who selects which works from a collection to display and explains the choice in a catalogue",
  "A performer who follows a score exactly as written",
  "A cataloguer who records the provenance of each object in an archive"],
 "A judgment that is criticism, acted on in a medium where the reasoning cannot be shown, is exactly the restorer's position.",
 "The editor applies a rule, the curator can show the reasoning, the performer exercises no such judgment, and the cataloguer records rather than judges.")
q('LC163','19','lsat_rc_app',3,
 'The passage suggests that the question of how a translator decides which sentences are which is rarely addressed because',
 ["addressing it would reveal how much of translation consists of critical judgment",
  "translators disagree too sharply about the answer to discuss it usefully",
  "the answer differs so much between languages that no general account is possible",
  "readers of translations are not interested in the translator's reasoning",
  "the two policies are applied by different schools of translators"],
 "The final paragraph offers exactly this as the likely reason.",
 "Disagreement, language specificity, reader interest and schools are not the explanation given.")

# ------------------------------------------------------------------ LP20 informality
q('LC164','20','lsat_rc_main',4,
 'Which one of the following most accurately expresses the main point of the passage?',
 ["Informality is not a single quantity waiting to be measured, and treating it as one distorts both the statistics and the policies built on them",
  "Currency based estimates of the informal sector are more reliable than survey based ones",
  "Programmes to formalise employment have failed to improve the conditions under which people work",
  "The size of the informal sector cannot be measured by any available method",
  "Aggressive enforcement causes respondents to conceal informal activity from surveys"],
 "The second paragraph denies that it is a fact waiting to be measured, the third says be specific about what a number is for, and the fourth carries the point into policy.",
 "B ranks methods the passage only contrasts, C is one example, D is more defeatist than the passage, and E is a step in the argument.")
q('LC165','20','lsat_rc_stated',2,
 'According to the passage, the gap between currency based and survey based estimates is widest in countries where',
 ["enforcement is most aggressive",
  "the informal sector is largest",
  "household surveys are conducted least often",
  "night time light imagery is least reliable",
  "tax rates on registered employment are highest"],
 "The second paragraph states this as the patterned disagreement.",
 "Sector size, survey frequency, imagery and tax rates are not what the passage connects to the gap.")
q('LC166','20','lsat_rc_stated',3,
 'The passage states that a subsistence trader',
 ["owes little tax and lacks all social protection",
  "is counted in survey based estimates but not in currency based ones",
  "would register if registration were made simpler",
  "is the typical case in countries with aggressive enforcement",
  "appears in night time light imagery but not in household surveys"],
 "The third paragraph uses exactly this case to show that one activity may belong in one figure and not the other.",
 "The other four are claims the passage does not make about the trader.")
q('LC167','20','lsat_rc_inf',4,
 'It can be inferred from the passage that the author would regard a single official figure for the size of the informal sector as',
 ["useful only once it is clear which question the figure is meant to answer",
  "unattainable given the disagreement among estimation methods",
  "preferable to several figures produced by competing methods",
  "a reasonable target for statistical agencies to pursue",
  "the most important input to a programme of formalisation"],
 "The third paragraph says the point is not despair but a reason to be specific about what a particular number is for.",
 "B is the despair the passage disclaims, C and D treat a single figure as the goal, and E inverts the fourth paragraph.")
q('LC168','20','lsat_rc_struct',4,
 'The author describes a programme that raises registrations without changing working conditions primarily in order to',
 ["show that the confusion identified in measurement reappears as a failure in policy",
  "argue that formalisation programmes should be discontinued",
  "explain why registration is often made a condition of something people already needed",
  "establish that registration figures are less accurate than survey figures",
  "suggest that the conditions under which people work are impossible to measure"],
 "The final paragraph opens by saying treating informality as a single quantity has consequences in policy as well as measurement, and this is the example.",
 "No discontinuation is urged, the conditioning is the mechanism rather than the point, accuracy is not compared, and measurability of conditions is not questioned.")
q('LC169','20','lsat_rc_app',4,
 'Which one of the following is most closely analogous to the difficulty the passage identifies in the final paragraph?',
 ["A hospital judged by waiting list length that shortens the list by changing who is allowed to join it",
  "A hospital that reports its waiting list length less often than regulators require",
  "A hospital whose waiting list is longer than those of comparable hospitals",
  "A hospital that treats more patients than it did in the previous year",
  "A hospital that measures waiting times from referral rather than from first contact"],
 "A measure improved by a route that leaves the underlying situation untouched is exactly the structure described.",
 "Reporting frequency, comparison, volume and the definitional choice in E are different problems, and E comes closest only as a measurement definition rather than as improving the number without changing the thing.")
q('LC170','20','lsat_rc_app',3,
 'Which one of the following, if true, would most undermine the claim that respondents in countries with aggressive enforcement conceal more?',
 ["Currency in circulation in those countries is inflated by cross border demand unrelated to informal work",
  "Household surveys in those countries are conducted by the same agencies as elsewhere",
  "Night time light estimates in those countries fall between the survey and currency figures",
  "Enforcement in those countries is directed mainly at large firms",
  "Informal workers in those countries are more likely to work in agriculture"],
 "The gap is between currency and survey estimates. If the currency figure is inflated for an unrelated reason, the gap no longer indicates concealment.",
 "Survey agencies, an intermediate third estimate, enforcement targets and sector composition do not remove the reason for the gap.")

P['21'] = ("Passage A\n\n"
"Research paid for by the public should be readable by the public, and the subscription "
"model fails that test twice over: libraries pay for the same research their own "
"institutions produced, and everyone outside a subscribing institution pays again or goes "
"without. Open access corrects this. The author pays a processing charge, the article is "
"free to read, and the cost falls on the party that already has a grant rather than on "
"every reader who might want the result.\n\n"
"Objections about quality mistake the funding model for the review process. The same "
"reviewers read the same manuscripts under either model, and a journal that lowered its "
"standards to collect more charges would lose the reputation that makes the charges worth "
"paying.\n\n"
"Passage B\n\n"
"The author pays model moves the cost from the reader to the author, and whether that is "
"an improvement depends entirely on who the authors are. A researcher at a well funded "
"institution in a wealthy country has the charge covered by a grant or a library "
"agreement. A researcher without one pays from a personal budget, applies for a waiver "
"that must be requested and justified, or publishes elsewhere.\n\n"
"The reply is that waivers exist and are granted generously. They do exist. Requesting one "
"requires identifying oneself to an editor as unable to pay, before the decision on the "
"manuscript has been made, and there is no way to measure how many authors decline to ask. "
"What can be measured is that the share of published authors from lower income countries "
"has not risen in the journals that converted, and in several has fallen.\n\n"
"None of this defends the subscription model, which had its own and worse exclusions. It "
"is an argument that the exclusion has been relocated rather than removed, and that a "
"reform described as opening access should be assessed by who publishes as well as by who "
"reads.")

P['22'] = ("For most of the twentieth century peptic ulcers were understood as a disease of "
"stress and acid. The treatment was acid suppression, which worked in the sense that "
"symptoms abated, and recurrence was treated as the nature of the condition. In 1982 two "
"Australian researchers proposed that most ulcers were caused by a bacterium, Helicobacter "
"pylori, and could be cured with antibiotics.\n\n"
"The reception was cool, and the usual account attributes this to entrenched interests. "
"The account is not baseless, since acid suppression was among the most profitable classes "
"of drug then sold. But the substantive objection came first and it was serious: the "
"stomach was believed to be sterile, the organism had been seen before and dismissed as a "
"contaminant, and the association between bacterium and ulcer was compatible with the "
"bacterium colonising tissue that was already damaged.\n\n"
"What the researchers supplied, over the following decade, was not more association but "
"the three things the objection required: a method of culturing the organism reliably, so "
"that it could be studied rather than glimpsed; a demonstration that ingesting it produced "
"gastritis in a healthy person, which one of them performed on himself; and trials showing "
"that eradicating it cured the ulcer and prevented recurrence, which acid suppression never "
"did.\n\n"
"The self experiment is the part the story is usually told around, and it is the least "
"important of the three. It established that the organism could cause inflammation in a "
"healthy stomach, which mattered, and a single subject could not have established the "
"rest. The culture method is what allowed everyone else to work on the question, and the "
"eradication trials are what moved the profession. A story that ends at the self experiment "
"teaches that persistence and courage overcome resistance, which is true and is not the "
"lesson. The lesson is that an objection of a particular shape can only be met by evidence "
"of a matching shape, and that assembling it took ten years and a great many people.")

# ------------------------------------------------------------------ LP21 open access
q('LC171','21','lsat_rc_main',4,
 'Which one of the following most accurately describes the relationship between the two passages?',
 ["Passage B accepts that the model passage A criticises was worse and argues that the reform relocates the exclusion rather than removing it",
  "Passage B defends the subscription model against the criticisms passage A makes of it",
  "Passage B argues that open access lowers the quality of peer review",
  "Passage B agrees with passage A about who bears the cost but disagrees about whether the cost is justified",
  "Passage B proposes a third funding model that neither passage A nor the subscription model provides"],
 "B's last paragraph says the subscription model had its own and worse exclusions, and frames the argument as relocation rather than removal.",
 "B does not defend subscriptions, says nothing about review quality, disputes who bears the cost rather than its justification, and proposes no model.")
q('LC172','21','lsat_rc_stated',2,
 'According to passage A, under the open access model the processing charge falls on',
 ["the party that already holds a grant",
  "the library of the author's institution",
  "the reader who wishes to obtain the article",
  "the journal that publishes the article",
  "the agency that funded the underlying research"],
 "The first paragraph of A says the cost falls on the party that already has a grant rather than on every reader.",
 "Libraries, readers, journals and funding agencies each figure in the passages without being what A names here.")
q('LC173','21','lsat_rc_stated',3,
 'Passage B states that what can be measured about journals that converted to open access is that the share of published authors from lower income countries',
 ["has not risen, and in several has fallen",
  "has risen more slowly than in journals that did not convert",
  "has risen only where waivers are granted automatically",
  "cannot be compared with the period before conversion",
  "matches the share of authors requesting waivers"],
 "The second paragraph of B gives exactly this as the measurable point, against the unmeasurable one about who declines to ask.",
 "The other four misstate the finding or the comparison.")
q('LC174','21','lsat_rc_inf',4,
 'It can be inferred that the author of passage B regards the existence of waivers as',
 ["genuine, and insufficient because the cost of requesting one is not captured by counting grants",
  "a formality that journals advertise without ever granting",
  "sufficient to answer the objection about authors who cannot pay",
  "evidence that the open access model is more inclusive than the subscription model",
  "the main reason the share of authors from lower income countries has fallen"],
 "B says they do exist, then names the cost of asking and says there is no way to measure how many decline.",
 "B does not call them a formality, does not find them sufficient, draws the opposite inference about inclusiveness, and names them as insufficient rather than causal.")
q('LC175','21','lsat_rc_struct',4,
 'The second paragraph of passage A serves primarily to',
 ["answer an objection by distinguishing the funding model from the process the objection concerns",
  "supply evidence that open access journals maintain the same standards as subscription journals",
  "concede that some open access journals have lowered their standards",
  "explain why reputation matters more to journals than revenue does",
  "introduce the argument that the public should be able to read publicly funded research"],
 "It says objections about quality mistake the funding model for the review process, and then gives two reasons.",
 "It argues rather than supplies evidence, concedes nothing, does not rank reputation against revenue, and the public access argument is the first paragraph.")
q('LC176','21','lsat_rc_app',4,
 'Which one of the following would passage B most likely regard as the right way to assess an open access reform?',
 ["Comparing the composition of the authors published before and after conversion",
  "Comparing the number of readers before and after conversion",
  "Comparing the rate at which waiver requests are granted with the rate at which they are made",
  "Comparing the processing charge with the subscription price it replaced",
  "Comparing the review standards applied before and after conversion"],
 "B's closing sentence says a reform described as opening access should be assessed by who publishes as well as by who reads.",
 "Readership, grant rates, price and standards are each partial or belong to A's case.")
q('LC177','21','lsat_rc_app',3,
 'Both passages would agree with which one of the following?',
 ["The subscription model excluded people who should have had access to published research",
  "Processing charges are the fairest available way of funding publication",
  "The share of authors from lower income countries is the right measure of a reform",
  "Peer review is unaffected by how a journal is funded",
  "Waivers make the processing charge model accessible to authors without grants"],
 "A argues the subscription model failed readers twice over, and B says it had its own and worse exclusions.",
 "B disputes the second, A never endorses the third, the fourth is A's alone, and B denies the fifth.")

# ------------------------------------------------------------------ LP22 Helicobacter
q('LC178','22','lsat_rc_main',4,
 'Which one of the following most accurately expresses the main point of the passage?',
 ["The ulcer case is better read as showing that an objection of a particular shape requires evidence of a matching shape than as a story about persistence",
  "The reception of the bacterial theory of ulcers was cool because acid suppression was highly profitable",
  "The self experiment was the decisive step in establishing that Helicobacter pylori causes ulcers",
  "Peptic ulcers were misunderstood for most of the twentieth century",
  "Eradicating Helicobacter pylori cures ulcers and prevents their recurrence"],
 "The final paragraph names the usual lesson, calls it true and not the lesson, and states the one the passage draws.",
 "B is called not baseless but secondary, C is called the least important of the three, and D and E are premises.")
q('LC179','22','lsat_rc_stated',2,
 'According to the passage, the substantive objection to the bacterial theory included the belief that',
 ["the stomach was sterile",
  "antibiotics could not reach the stomach lining",
  "ulcers recurred regardless of treatment",
  "stress was the only known cause of gastritis",
  "the organism could not survive outside the body"],
 "The second paragraph lists sterility, the earlier dismissal as a contaminant, and the colonisation alternative.",
 "Drug delivery, recurrence, stress and survival outside the body are not among the objections named.")
q('LC180','22','lsat_rc_stated',3,
 'The passage states that the three things the objection required were a reliable culture method, a demonstration in a healthy person, and',
 ["trials showing that eradication cured the ulcer and prevented recurrence",
  "a mechanism by which the bacterium damages the stomach lining",
  "evidence that the organism was present in every patient with an ulcer",
  "an explanation of why acid suppression relieved symptoms",
  "confirmation that the organism had been seen by earlier researchers"],
 "The third paragraph names the eradication trials as the third, and notes that acid suppression never prevented recurrence.",
 "Mechanism, universality, the acid explanation and prior sightings are not the third item.")
q('LC181','22','lsat_rc_inf',4,
 'It can be inferred from the passage that the association between the bacterium and ulcers was insufficient on its own because it',
 ["was compatible with the bacterium colonising tissue that had already been damaged",
  "had been reported only by the two researchers who proposed the theory",
  "rested on a sample of patients too small to be persuasive",
  "could not be reproduced outside Australia",
  "conflicted with the observation that acid suppression relieved symptoms"],
 "The second paragraph names exactly this alternative reading of the association.",
 "Provenance, sample size, reproducibility and the acid observation are not what the passage says left the association short.")
q('LC182','22','lsat_rc_struct',4,
 'The author calls the self experiment the least important of the three primarily in order to',
 ["redirect attention to the contributions that allowed others to work on the question and changed the profession",
  "question whether the self experiment was conducted as reported",
  "argue that single subject experiments have no evidential value",
  "suggest that the researchers should have obtained ethical approval first",
  "show that the objection about sterility was never fully answered"],
 "The paragraph grants what the self experiment established, then names the culture method and the trials as what did the work.",
 "The conduct is not questioned, single subject work is credited with something, ethics are not discussed, and the sterility objection is treated as met.")
q('LC183','22','lsat_rc_app',4,
 'Which one of the following best illustrates the lesson the author draws in the final paragraph?',
 ["A claim doubted because an association could run either way is settled by an intervention that fixes the direction, not by further associations",
  "A claim doubted by a profession is eventually accepted because its proponent refuses to abandon it",
  "A claim is strengthened by each new study that reports the same association",
  "A claim is accepted once a respected researcher endorses it publicly",
  "A claim is rejected because the researcher proposing it stood to gain from its acceptance"],
 "Matching the shape of the evidence to the shape of the objection is exactly the move A describes.",
 "Persistence, accumulation, endorsement and motive are the readings the passage sets aside.")
q('LC184','22','lsat_rc_app',3,
 'The passage suggests that the usual account attributing the cool reception to entrenched interests is',
 ["partly right and misleading about the order in which the objections arose",
  "entirely mistaken, since no commercial interest was at stake",
  "the most complete explanation available of the delay in acceptance",
  "inconsistent with the profitability of acid suppressing drugs",
  "an invention of writers unfamiliar with the scientific record"],
 "The second paragraph says the account is not baseless, names the profitability, and then says the substantive objection came first and was serious.",
 "B and D deny the profitability the passage grants, C treats it as complete, and E accuses the writers of ignorance the passage does not allege.")

# Six further primary purpose and organisation questions. Main Idea and Primary Purpose
# was the one reading skill that twelve sets of seven would have left at 24, one short of
# the threshold the review bot warns at, so six sets carry an eighth question rather than
# the totals being left to come out where they fell.
q('LC185','11','lsat_rc_main',4,
 'The passage is organised in which one of the following ways?',
 ["A justification is stated, two objections are raised, one is answered at a cost, and a third position is described as immune and unavailable",
  "Three justifications for a rule are stated and compared, and the strongest is identified",
  "An objection is stated, answered, and then restated in a stronger form that the answer does not meet",
  "A rule is described, its history is traced, and its likely future is predicted",
  "Two positions are set out and a compromise between them is proposed"],
 "Deterrence, the empirical and distributive objections, the answer and its awkward consequence, then the integrity reading and the Court's retreat from it.",
 "Only one justification is defended at length, the objection is not restated, no history or prediction is offered, and no compromise is proposed.")
q('LC186','13','lsat_rc_main',3,
 'The primary purpose of the passage is to',
 ["locate the source of a legal difficulty in an assumption that ordinarily holds and fails in one class of case",
  "criticise the collectors who registered copyrights in songs they had recorded",
  "describe the history of blues and work song collecting in the American South",
  "argue that the fixation requirement should be removed from copyright law",
  "defend the courts that applied the fixation rule as written"],
 "The last paragraph identifies the assumption that the contribution is the whole work, and names oral traditions as where it fails.",
 "The collectors are not the target, the history is material, no removal is urged, and the courts are neither defended nor condemned.")
q('LC187','15','lsat_rc_main',4,
 'The two passages are primarily concerned with',
 ["whether a method of interpretation delivers the constraint claimed for it",
  "whether the original public meaning of a constitutional text can be recovered",
  "whether judges should consult contemporary values in interpreting a text",
  "whether historians agree about eighteenth century usage",
  "whether judges are candid about the reasons for their decisions"],
 "A rests the case on constraint and B treats constraint as an empirical claim that has not been tested, so constraint is the shared subject.",
 "Recoverability, contemporary values and historians' agreement are components, and B expressly declines to make the exchange about candour.")
q('LC188','17','lsat_rc_main',4,
 'The passage proceeds by',
 ["stating a justification, identifying what it leaves out, showing that the usual safeguard cannot supply it, and reinterpreting the proceeding",
  "setting out two competing justifications for a procedure and choosing between them",
  "describing a procedure, cataloguing its abuses, and proposing statutory reform",
  "arguing that a procedure should be abolished and answering the objections to abolition",
  "comparing a legal procedure with a regulatory one and finding the comparison inapt"],
 "Access, the control problem, the limits of judicial approval, and the regulatory reframing, in that order.",
 "Only one justification is examined, no catalogue or statute is offered, abolition is rejected, and the regulatory comparison is endorsed rather than found inapt.")
q('LC189','19','lsat_rc_main',3,
 'The primary purpose of the passage is to',
 ["show that a familiar debate is settled in different directions for different parts of a text, and to name the question that follows",
  "argue that foreignisation is the more faithful of the two approaches to translation",
  "describe the history of the debate between domestication and foreignisation",
  "recommend that translators state their policy before beginning a translation",
  "establish that literary translation cannot be evaluated objectively"],
 "The third paragraph splits the verdict and names the interesting question, and the fourth explains why it goes unaddressed.",
 "Neither approach is preferred overall, no history is given, no policy statement is recommended, and objectivity is not the subject.")
q('LC190','21','lsat_rc_main',4,
 'Which one of the following most accurately states a point on which the two passages take opposing positions?',
 ["Whether the shift to author paid publication removes the exclusions of the subscription model",
  "Whether the subscription model excluded readers who should have had access",
  "Whether peer reviewers apply the same standards under either funding model",
  "Whether waivers for processing charges exist in practice",
  "Whether publicly funded research should be readable by the public"],
 "A presents open access as correcting the failure; B argues the exclusion has been relocated rather than removed.",
 "Both grant the second, only A addresses the third, both grant the fourth, and neither disputes the fifth.")

LIFT = {
 'LC101': [("protects the integrity of judicial proceedings rather than", " the interests of any of the parties before the court"),
           ("Studies of whether the exclusionary rule deters unlawful searches", " have been carried out repeatedly and have settled nothing"),
           ("should be replaced by a remedy that compensates those subjected", " to a search of theirs that produced nothing incriminating at all"),
           ("have misunderstood the purpose the rule was adopted", " to serve, and the objections they raise miss it entirely as a result")],
 'LC102': [("applies unevenly across jurisdictions", " with different police practices and different courts"),
           ("imposes costs on the state that are ultimately borne by taxpayers", " rather than by the officers"),
           ("protects defendants at the expense of the victims", " of the crimes they are charged with")],
 'LC103': [("assumes that the rule was adopted to compensate", " those subjected to an unlawful search"),
           ("relies on studies whose results are too weak", " and too contested to be decisive")],
 'LC106': [("A tax credit available only to firms that can document the expenditure", " it is meant to encourage, which the firms least able to spend cannot produce"),
           ("A licensing rule that bars a firm from operating until it has passed", " an inspection conducted at the firm's own expense before it is permitted to trade at all"),
           ("A warranty that covers a product only during the first year after purchase", " and lapses whether or not the fault complained of had been present from the very start")],
 'LC107': [("Empirical studies are a poor basis on which to settle questions", " of constitutional doctrine, whatever their quality"),
           ("Courts should adopt whichever justification for a rule is least vulnerable", " to the objections that have been raised against it")],
 'LC108': [("Experiments giving plants and fungi conflicting interests have shown", " the cooperative account to be false in every case tested")],
 'LC110': [("the measurement technique cannot distinguish carbon", " taken up by the fungus from carbon passed between plants"),
           ("the two plants belong to the same species", " and are closely related to one another"),
           ("the receiving plant is short of carbon", " and signals that shortage to its neighbours"),
           ("soil water carries dissolved carbon between root systems", " without any fungal involvement")],
 'LC112': [("argue that the cooperative account has been refuted", " by the findings that do not fit it"),
           ("accuse researchers in the field of deliberately suppressing", " results that count against the cooperative reading"),
           ("illustrate the difficulty of measuring transfers under field conditions", " rather than in a laboratory")],
 'LC113': [("A study measures an outcome that is only loosely related to the one of interest", " and is then reported as though the two measures had been the same thing all along"),
           ("A study reports a result that later teams have been unable to reproduce", " using the same materials and following the same protocol throughout every attempt they made")],
 'LC117': [("which of several versions to fix", " in writing when the performances differ"),
           ("which repetitions to preserve", " and which to treat as incidental"),
           ("how to render rhythm", " that ordinary musical notation handles badly")],
}
LIFT.update({
 'LC120': [("A translator who receives a copyright in the translation but not in the original", " work that was translated"),
           ("An editor who corrects the proofs of a novel and is paid a fee", " rather than a royalty on the sales")],
 'LC124': [("large programmes attract participants who are less motivated", " than those who joined the earliest trials"),
           ("measurement becomes less accurate as the number of participants grows", " beyond a certain point"),
           ("the organisations that run large programmes are less well supervised", " than a research team is"),
           ("the cost per participant rises as a programme expands", " to cover a whole region rather than a district")],
 'LC125': [("misguided, because the limits of the method are a matter of coverage", " rather than of kind"),
           ("an admission that the method cannot support policy decisions", " of the kind it was adopted to inform"),
           ("sufficient to establish the mechanisms policy makers require", " in order to act on a result")],
 'LC126': [("propose a research programme that would combine the strengths", " of the two approaches the passage has described"),
           ("adjudicate between the advocates and the critics in favour of the critics", " and the objection they have raised")],
 'LC128': [("Statistical adjustment is an adequate substitute for randomisation", " wherever randomisation cannot be arranged"),
           ("The limits of the randomised trial can be overcome by running trials", " in a sufficient number of different settings"),
           ("Randomised trials should be abandoned in favour of judgments", " about the mechanisms that produce an effect")],
 'LC129': [("denies the premise on which passage A's argument rests", " and offers an alternative method of interpretation"),
           ("attributes to defenders of the method a motive that passage A", " does not address anywhere in its argument")],
 'LC134': [("Judges who describe themselves as originalists reach conclusions", " that track their prior commitments closely"),
           ("A method of interpretation that cannot be shown to be wrong", " is for that reason unacceptable in a court"),
           ("The historical record forecloses some propositions about eighteenth century", " usage that were once thought open"),
           ("Contemporary values have no determinate content", " that a judge could consult in deciding a case")],
 'LC135': [("The historical record for contested provisions has grown larger", " as more archives of the period are digitised"),
           ("Historians agree about the original public meaning", " of most of the constitutional provisions that are litigated"),
           ("Self described originalists cite historical sources more often", " in their written opinions than other judges do")],
 'LC136': [("Geologists apply a stricter standard to theories proposed by outsiders", " than to those proposed by colleagues"),
           ("critics rejected continental drift because they were unwilling", " to consider an idea unfamiliar to them")],
 'LC139': [("been rejected by physicists on the same grounds", " as the mechanisms he had proposed himself"),
           ("eventually persuaded the geological establishment to accept the theory", " without any further evidence"),
           ("made the sea floor surveys of the 1950s unnecessary", " to the eventual acceptance of the theory")],
})
LIFT.update({
 'LC140': [("argue that the geological establishment was in fact more receptive", " than it is usually supposed to have been"),
           ("suggest that Wegener himself was responsible for the delay", " in the acceptance of his theory")],
 'LC141': [("A medical hypothesis rejected because the researcher proposing it lacked formal training", " in the discipline the hypothesis belongs to")],
 'LC142': [("overstates how long the geological establishment resisted the theory", " before accepting it"),
           ("credits the sea floor surveys with more than they established", " about the movement of continents"),
           ("ignores the role played by physicists in the dispute", " over the mechanisms that were proposed"),
           ("assumes that Wegener had no mechanism to offer", " when in fact he offered two of them himself")],
 'LC143': [("Judicial review of class settlements is inadequate because the parties", " who assemble the record both want the settlement approved"),
           ("Class actions should be abolished because absent members cannot control", " the claims that are brought on their behalf"),
           ("The access justification for class actions is the only one", " that withstands any serious examination of the procedure")],
 'LC147': [("show that the approval standard is less demanding than it appears", " to be when it is read on paper"),
           ("establish that most class settlements are unfair to absent members", " of the class they bind")],
 'LC149': [("They are bound by the outcome but may withdraw at any point", " before the settlement is approved"),
           ("They are consulted about the terms of any settlement", " before the judge is asked to approve it"),
           ("They select counsel indirectly through the member who files first", " in whichever court hears the claim")],
 'LC150': [("Human reasoning is better described as a bundle of narrow specialisations", " than as a single general capacity that is applied to whatever new problems arise"),
           ("Tool use in New Caledonian crows is a narrow specialisation rather than a general", " reasoning capacity of the kind that primates have usually been held to possess themselves")],
 'LC153': [("human reasoning and crow tool use rest on the same underlying mechanism", " despite the difference in brain organisation"),
           ("the conclusion that crow tool use is specialised is mistaken", " and should be replaced by the general capacity reading"),
           ("comparisons between species are of little scientific value", " where the species being compared are distantly related"),
           ("the tasks given to crows have been poorly designed", " by researchers working from studies that were designed for primates")],
 'LC154': [("concedes that the second paragraph's findings are inconsistent", " with what the first paragraph reported about captive crows"),
           ("offers an alternative explanation of the findings reported", " in the second paragraph about hand raised crows"),
           ("rejects the findings reported in the second paragraph as unreplicated", " by any other research group working on the question")],
 'LC155': [("Crows in a new population are observed manufacturing hooks of the same design", " as those described in the earlier studies"),
           ("Crows carry favoured tools over longer distances than had previously been recorded", " in the course of field observation of wild birds")],
 'LC157': [("Foreignisation preserves what matters most in a literary work and should be preferred", " wherever the two approaches conflict with one another in the course of a single text"),
           ("Domestication produces better English and should be preferred for ordinary sentences", " and for every other kind of sentence that a translator is called on to render as well"),
           ("Translators should be trained as literary critics before being allowed to translate", " a work that has any literary standing at all, however modest that standing might in fact be")],
 'LC160': [("a translation that critics will prefer to one produced by any other policy", " of rendering"),
           ("the same result as a translator who applies domestication uniformly", " across the whole text")],
})
LIFT.update({
 'LC162': [("A curator who selects which works from a collection to display and explains", " the choice in a catalogue that visitors can read alongside the works themselves"),
           ("An editor who applies a house style guide consistently across every manuscript", " that the publishing house sends out to be prepared for the printer in any given week of the working year"),
           ("A cataloguer who records the provenance of each object in an archive", " and sets out in a note the evidence on which each one of the attributions in the collection has been made to rest"),
           ("A performer who follows a score exactly as written", " and adds nothing at all to it that the composer had not already set down in the written notation himself, note for note")],
 'LC164': [("Programmes to formalise employment have failed to improve the conditions", " under which the people they register actually work"),
           ("Currency based estimates of the informal sector are more reliable", " than the survey based estimates that statistical agencies prefer"),
           ("Aggressive enforcement causes respondents to conceal informal activity", " from the household surveys on which the official figures rest")],
 'LC167': [("unattainable given the disagreement among estimation methods", " that are currently in use"),
           ("preferable to several figures produced by competing methods", " that disagree with one another")],
 'LC170': [("Night time light estimates in those countries fall between the survey", " and currency figures rather than outside them"),
           ("Household surveys in those countries are conducted by the same agencies", " that conduct them everywhere else"),
           ("Informal workers in those countries are more likely to work in agriculture", " than in any other sector of the economy")],
 'LC171': [("Passage B agrees with passage A about who bears the cost", " of publication but disagrees about whether that cost is justified")],
 'LC175': [("supply evidence that open access journals maintain the same standards", " as the subscription journals they replaced"),
           ("introduce the argument that the public should be able to read", " the research that public money has paid for"),
           ("concede that some open access journals have lowered their standards", " in order to collect more charges"),
           ("explain why reputation matters more to journals than revenue does", " over any extended period of years")],
 'LC177': [("The share of authors from lower income countries is the right measure", " by which any such reform should be judged"),
           ("Waivers make the processing charge model accessible to authors", " who have no grant to draw the charge from"),
           ("Processing charges are the fairest available way of funding publication", " of research results")],
 'LC181': [("conflicted with the observation that acid suppression relieved symptoms", " in most of the patients who received it"),
           ("had been reported only by the two researchers who proposed the theory", " and by nobody else at the time")],
 'LC184': [("the most complete explanation available of the delay in acceptance", " of the bacterial theory"),
           ("an invention of writers unfamiliar with the scientific record", " of the period in question"),
           ("inconsistent with the profitability of acid suppressing drugs", " in the years the theory was proposed")],
 'LC185': [("An objection is stated, answered, and then restated in a stronger form", " that the answer given earlier does not meet"),
           ("Three justifications for a rule are stated and compared, and the strongest", " of the three is then identified and defended at length")],
 'LC188': [("arguing that a procedure should be abolished and answering the objections", " that have been raised against abolishing it altogether now"),
           ("comparing a legal procedure with a regulatory one and finding the comparison", " inapt in the respects that matter most to the argument being made"),
           ("setting out two competing justifications for a procedure and choosing", " between them on the strength of the evidence that is available")],
 'LC189': [("argue that foreignisation is the more faithful of the two approaches", " to the translation of any literary work at all, of whatever kind"),
           ("recommend that translators state their policy before beginning", " work on a translation of any appreciable length or difficulty")],
}); 

E.permute(I)
E.extend(I, LIFT, 'LIFT')
E.check_lift(I, {k: len(v) for k, v in LIFT.items()})

HEADER = '''// bank_lsat_rc3.js - Original LSAT Reading Comprehension items LC101-LC190.
//
// Generated by src/mk_bank_lsat_rc3.py. Edit that file, not this one.
//
// The last starved corpus on any exam. After bank_lsat_lr3.js took Logical Reasoning to
// 29 to 31 per skill, the review bot's remaining LSAT warning was the five reading
// skills at 10, 10, 12, 18 and 20. These 90 items across 12 new passage sets take all
// five to 30 or more.
//
// Twelve sets, the shape LSAC publishes for the section: single passages of roughly four
// hundred words and two comparative pairs, across law, natural science, humanities,
// social science and the history of science. Six sets carry an eighth question, because
// twelve sets of seven would have left Main Idea and Primary Purpose at 24, one short of
// the threshold the review bot warns at.
//
// Every set covers all five tracked skills. The engine builds a section out of whole
// passage groups, so a skill confined to one passage is dropped whenever that passage is
// not selected, and the skill then reads as starved even when the bank holds enough.
//
// On the length tell: the key was the longest option on 62 of the 90 as written, playable
// at 69 percent against a chance rate of 20. Corrected by LIFT, which carries a chosen
// number of distractors past the key item by item; check_lift fails the run if a clause
// was too short to do it.
'''

E.measure(I)
PV = {k: 'L_RP' + k for k in P}
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_lsat_rc3.js',
        HEADER, [('L_RP' + k, P[k]) for k in sorted(P)], I, 'BANK_LSAT_RC3',
        passage_var=PV, group_key='passageId')
