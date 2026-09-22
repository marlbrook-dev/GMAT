# -*- coding: utf-8 -*-
"""Emit src/bank_lsat_rc2.js.

Run: python3 src/mk_bank_lsat_rc2.py src/bank_lsat_rc2.js

Kept in the repository rather than thrown away because the two passes at the bottom are
the content decisions, not scaffolding: which distractor was extended and with what
clause is the record of how the length tell was brought from 66 percent to 6, and the
next person to edit an item here needs to see it.

Written as a generator rather than by hand for one reason: every string goes through
json.dumps, so an apostrophe inside a passage cannot break the file. Unescaped quotes in
a generated JS string once took the whole trainer down (INC-0001), and passages are
full of apostrophes.
"""
import io, json, os, re, sys

P6 = (
"In negligence law the central question is what care a defendant owed, and for most of "
"the doctrine's history the answer was given by a standard rather than a rule: the care "
"a reasonable person would have taken in the circumstances. The standard has the virtue "
"of flexibility and the vice of vagueness, and in 1947 Judge Learned Hand proposed a "
"formulation that promised to remove the vagueness without sacrificing the flexibility. "
"A defendant is negligent, he wrote, if the burden of taking a precaution is less than "
"the probability of the harm multiplied by its gravity. Stated as an inequality, the test "
"looked like a calculation, and generations of scholars have treated it as one.\n\n"
"The appeal is obvious. A standard that tells a jury to consult its sense of "
"reasonableness gives no account of why one verdict follows and another does not. The "
"Hand formulation appears to supply that account, and it does so in a vocabulary the law "
"shares with economics, which is part of why the law and economics movement adopted it so "
"readily. On this reading, negligence liability is a device for inducing efficient levels "
"of precaution: a party who could have avoided a large expected loss at a small cost and "
"failed to do so has wasted resources, and the law makes that party pay.\n\n"
"The difficulty is that the three terms are not the same kind of quantity. Burden is "
"ordinarily a cost in money or forgone activity. Probability is a number, though rarely a "
"knowable one at the moment of decision. Gravity is a harm to a person, and harms to "
"persons are not denominated in the units that burdens are. To multiply the second by the "
"third and compare the product to the first is to assume that a broken leg and the price "
"of a guard rail can be placed on one scale. Courts do this routinely, but they do it "
"under a description that conceals it, and the concealment matters: the Hand formulation "
"presents as arithmetic a judgement that is in fact evaluative.\n\n"
"Defenders of the formulation reply that the objection proves too much. Any allocation of "
"resources to safety implies a rate at which money is traded against risk to persons, and "
"a legal system that refuses to name the rate does not thereby avoid choosing one. It "
"merely chooses it silently, and silence is not neutrality. On this view the Hand test is "
"valuable precisely because it forces the comparison into the open, where it can be "
"argued about, rather than leaving it to an unarticulated sense of what is reasonable.\n\n"
"Both positions have force, and the disagreement between them is not really about "
"arithmetic. It is about whether the discipline of making a tradeoff explicit is worth "
"the risk that the explicit form will be mistaken for an objective one."
)

P7 = (
"When a leaf is chewed, the plant it belongs to releases a mixture of volatile organic "
"compounds into the air around it. Neighbouring plants of the same species, exposed to "
"that mixture and to nothing else, subsequently mount a faster defensive response when "
"they are themselves attacked: they produce protective compounds sooner and in greater "
"quantity than unexposed controls. The effect has now been demonstrated in sagebrush, in "
"lima beans, in maize and in poplar, under field conditions as well as in the laboratory, "
"and it is not seriously disputed.\n\n"
"What the effect should be called is disputed, and the dispute is not merely verbal. The "
"early literature described it as plant communication, and the term has proved durable. "
"Communication, however, ordinarily implies a signal produced because it affects a "
"receiver, and selection acts on the emitter only if the emitter gains. A plant that warns "
"its neighbours has helped its competitors. Unless those neighbours are close relatives, "
"or unless the emitter derives some separate advantage, the trait is difficult to account "
"for.\n\n"
"Three explanations are on offer. The first is kin selection: sagebrush populations are "
"often clonal or closely related, and a warning that reaches relatives can be favoured. "
"The second treats the volatiles as within-plant signalling that neighbours merely "
"intercept. A plant with a branching architecture faces a real problem of internal "
"coordination, since vascular connections between branches are often poor, and a volatile "
"released into the air travels between branches faster than any signal through the stem. "
"On this account the neighbour is an eavesdropper and the emitter gains nothing from being "
"overheard. The third denies that the compounds are signals at all: they may be metabolic "
"byproducts of wounding, informative to whoever detects them in the way that smoke is "
"informative without having been sent.\n\n"
"The experimental work has begun to separate these. Cutting a sagebrush and preventing air "
"movement between its own branches reduces its own subsequent resistance, which is what "
"the within-plant account predicts and what the byproduct account does not. Relatedness "
"between emitter and receiver improves the response in some species and not in others, "
"which is awkward for a pure kin-selection story. The most likely conclusion is that the "
"phenomenon is not one phenomenon, and that the same physical mechanism has been recruited "
"differently in different lineages.\n\n"
"This is an unsatisfying result if what was wanted was a single answer, and a useful one "
"if what was wanted was an accurate description. The vocabulary of communication carried "
"an implicit claim about function, and the claim turned out to be doing work that the "
"evidence did not support."
)

P8A = (
"Passage A\n\n"
"The restorer's obligation is to the painting as its maker left it. Everything that has "
"happened since, the yellowing of varnish, the darkening of a sky, the accumulated "
"repaintings of earlier hands, is damage, and the fact that damage is old does not make it "
"part of the work. A viewer standing before a cleaned picture sees what the painter saw on "
"the day the picture was finished, which is the only state in which the artist's decisions "
"about colour and light are recoverable at all.\n\n"
"The objection that cleaning destroys a patina the artist intended rests on a claim about "
"intention that is almost never supported. Painters worked in varnish because varnish "
"saturates colour and protects a surface, not because they anticipated the amber film it "
"becomes in two centuries. Where a document records an intention to the contrary, the "
"restorer should follow it. Where none exists, the presumption should run toward the "
"painter's visible practice elsewhere, and that practice is overwhelmingly one of bright, "
"legible colour."
)

P8B = (
"Passage B\n\n"
"A painting is not a text of which earlier states can be recovered by stripping away "
"later ones. It is an object that has existed in time, and its history is not a layer on "
"top of it but a part of what it now is. The argument for cleaning treats the centuries "
"between the artist and us as interference in a transmission. They are better understood "
"as the thing that has been transmitted.\n\n"
"This is not an argument for leaving every accretion in place. A crude overpainting that "
"obscures a face is worth removing, and nobody seriously proposes otherwise. It is an "
"argument against the assumption that there exists an original state, uniquely correct, "
"which the restorer's work uncovers. The surface a restorer stops at is chosen, and the "
"choice is made on grounds that are aesthetic and contestable rather than technical and "
"determinate. Presenting that choice as the recovery of a fact conceals the most "
"interesting thing about it."
)

P9 = (
"For most of the twentieth century, economists who wanted to estimate a causal effect "
"looked for a natural experiment: some accident of policy or geography that had assigned "
"people to different conditions in a way that was, for the purposes at hand, as good as "
"random. A change in the minimum wage in one state and not its neighbour, a lottery that "
"allocated school places, a border that split an otherwise similar population. The method "
"was ingenious and it was cheap, and it produced a generation of results that overturned "
"conclusions previously reached by comparing groups that differed in every respect at "
"once.\n\n"
"It also had a structural weakness. The researcher did not choose the treatment, and so "
"the treatment was whatever history had happened to supply. A minimum wage rose by the "
"amount the legislature chose, in the year it chose, in a state whose economy differed "
"from its neighbour's in ways the researcher could not fully enumerate. The estimate was "
"credible for that change, in that place, at that time, and the profession spent "
"considerable effort arguing about how far it travelled.\n\n"
"Field experiments removed the constraint. If the researcher assigns the treatment, the "
"treatment can be the one the theory is about rather than the one the legislature "
"happened to pass, and it can be varied deliberately across arms to trace out a response "
"rather than establish a single contrast. The approach has produced findings that natural "
"experiments could not have produced, and it has done so with an internal validity that is "
"a matter of design rather than of argument.\n\n"
"What has been lost is less often discussed. A treatment a researcher can assign is a "
"treatment small enough for a researcher to afford, and small enough that no general "
"equilibrium effects follow from it. A programme that raises the wages of forty workers in "
"a labour market does not change the market; a programme that raises the wages of all of "
"them might, and the second is usually the question of interest. The natural experiment, "
"for all its imprecision, was often measuring the policy, whereas the field experiment is "
"measuring a scale model of it and inferring upward.\n\n"
"The reasonable conclusion is not that one design is better, but that the profession "
"traded one uncertainty for another and has been slower to name the second than it was to "
"name the first."
)

P10 = (
"Alfred Wegener proposed in 1912 that the continents had once been joined and had since "
"moved apart. He assembled the fit of the coastlines, the continuity of rock formations "
"across the Atlantic, the distribution of fossil species that could not have crossed an "
"ocean, and the traces of glaciation in what are now tropical latitudes. The hypothesis "
"explained a great deal that was otherwise unexplained, and it was rejected by most "
"geologists for roughly half a century.\n\n"
"The rejection is often told as a parable about the conservatism of established science, "
"with Wegener as an outsider whose evidence was ignored because he was a meteorologist. "
"The story is satisfying and it is incomplete. The evidence was not ignored; much of it "
"was accepted, and the correspondences Wegener assembled were widely agreed to require an "
"explanation. What was rejected was the mechanism, and the rejection was, on the "
"information then available, reasonable.\n\n"
"Wegener proposed that continents plough through oceanic crust, driven by tidal forces and "
"by a poleward drift. Geophysicists calculated the forces required and found them orders "
"of magnitude larger than the forces available, and calculated the strength of oceanic "
"crust and found it far too great to be ploughed through. Both calculations were correct. "
"A hypothesis whose only proposed mechanism has been shown to be physically impossible is "
"in serious trouble, and treating it so is not prejudice.\n\n"
"What changed was not the continental evidence, which was much the same in 1960 as in "
"1920. It was the ocean floor. Mapping revealed a ridge system running through every "
"ocean basin; magnetic surveys revealed symmetrical bands of reversed polarity on either "
"side of the ridges; dating revealed that the floor was young everywhere and youngest at "
"the ridges. The continents were not ploughing through the crust. The crust was being "
"made at the ridges and carrying the continents with it, and the mechanism that had been "
"shown to be impossible had never been the right one.\n\n"
"The episode is worth being careful about, because both available morals are wrong. It is "
"not a case of evidence defeating dogma, since the evidence that mattered did not exist "
"until the 1950s. Nor is it a case of science working smoothly, since Wegener was treated "
"with a contempt his argument did not deserve. It is a case of a correct conclusion "
"supported by an incorrect mechanism, which is a position the evidence of the day could "
"not distinguish from a wrong conclusion."
)

def item(iid, pid, passage, skill, diff, stem, choices, answer, expl, wrong):
    return {"id": iid, "section": "RC", "type": "RC", "passageId": pid, "_p": passage,
            "skill": skill, "diff": diff, "stem": stem, "choices": choices,
            "answer": answer, "expl": expl, "wrong": wrong}

ITEMS = []
PASSVAR = {}

# ---- Set 6: the Hand formulation ----------------------------------------------------
S = 'LP6'
ITEMS += [
 item('LC036',S,'P6','lsat_rc_main',3,
  'Which one of the following most accurately expresses the main point of the passage?',
  ['A formulation that presents a negligence judgement as a calculation has both a real advantage and a real cost, and the disagreement about it concerns which matters more.',
   'The Hand formulation should be abandoned because its three terms cannot be measured in the same units and the comparison it demands is therefore incoherent.',
   'Courts applying the reasonable person standard reached inconsistent verdicts until the Hand formulation gave them a method for reaching consistent ones.',
   'The law and economics movement adopted the Hand formulation because it shared a vocabulary with economics rather than because it was legally sound.',
   'Negligence liability is best understood as a device for inducing parties to take efficient levels of precaution against foreseeable harm.'],
  0,
  'The passage sets out the appeal, then the incommensurability objection, then the reply that silence is not neutrality, and closes by saying the disagreement is about whether explicitness is worth the risk of false objectivity. That is a characterisation of a live dispute, not a verdict.',
  'The passage does not conclude that the formulation should be abandoned, and the final paragraph says both positions have force. The claim about inconsistent verdicts is not made. The vocabulary point and the efficiency account are each one step in the argument, not its point.'),
 item('LC037',S,'P6','lsat_rc_stated',2,
  'According to the passage, Judge Hand stated that a defendant is negligent when',
  ['the burden of a precaution is less than the probability of the harm multiplied by its gravity',
   'the gravity of the harm exceeds the burden of the precaution that would have prevented it',
   'a reasonable person in the same circumstances would have taken the precaution at issue',
   'the expected loss avoided by a precaution can be stated in the same units as its cost',
   'the party who could most cheaply have avoided the loss failed to take steps to avoid it'],
  0,
  'The second paragraph of the passage states the inequality in exactly these terms: burden less than probability multiplied by gravity.',
  'The second option drops probability from the comparison. The third restates the older standard the formulation was meant to sharpen. The fourth is an assumption the passage says the formulation conceals rather than states. The fifth is the cheapest cost avoider idea, which the passage does not attribute to Hand.'),
 item('LC038',S,'P6','lsat_rc_inf',4,
  'The passage suggests that the author would be most likely to agree with which one of the following statements about the reasonable person standard?',
  ['It also embodies a tradeoff between money and risk to persons, but does not present that tradeoff as a calculation.',
   'It produces more accurate outcomes than the Hand formulation because it does not require quantities that cannot be known.',
   'It was abandoned by most courts once the Hand formulation supplied a more determinate alternative to it.',
   'It is preferable to the Hand formulation because it does not require harms to persons to be priced at all.',
   'Its vagueness is a defect that the law and economics movement was right to try to remove.'],
  0,
  'The defenders argue that any allocation to safety implies a rate at which money trades against risk, and that a system refusing to name the rate still chooses one silently. Applied to the reasonable person standard, that is precisely the claim: the tradeoff is present and unstated.',
  'The passage never says the older standard is more accurate or preferable, and it does not say courts abandoned it. It calls vagueness a vice but does not endorse the movement\'s project.'),
 item('LC039',S,'P6','lsat_rc_struct',4,
  'The fourth paragraph of the passage functions primarily to',
  ['present a response to the objection raised in the paragraph before it',
   'introduce a second objection that is independent of the first',
   'qualify the account of the Hand formulation given in the first two paragraphs',
   'supply the empirical support that the preceding argument had left open',
   'restate the central claim in terms drawn from economics rather than law'],
  0,
  'The third paragraph raises incommensurability; the fourth opens with defenders replying that the objection proves too much. It is a response.',
  'It is not a second objection, and it does not qualify the earlier exposition or supply data. It uses no more economic vocabulary than the paragraphs around it.'),
 item('LC040',S,'P6','lsat_rc_app',5,
  'Which one of the following situations is most closely analogous to the concealment the author describes in the third paragraph?',
  ['A hospital ranks patients for a scarce organ using a formula whose inputs include a judgement about quality of life, and reports the ranking as a medical calculation.',
   'An engineer computes the load a bridge can carry and reports a figure that turns out to be mistaken because a measurement was taken wrongly.',
   'A committee votes on a contested question and announces the result without releasing the tally of individual votes.',
   'A regulator sets an emissions limit and declines to explain the reasoning that produced the particular number chosen.',
   'A firm advertises a product using a statistic that is accurate but drawn from an unrepresentative sample of users.'],
  0,
  'The concealment at issue is an evaluative judgement wearing the dress of arithmetic. A quality of life judgement embedded in a formula and reported as a medical calculation has exactly that structure.',
  'A mismeasured load is an error, not a concealed evaluation. A withheld tally and an unexplained limit are failures to disclose reasoning, not evaluations presented as computations. An unrepresentative statistic is a sampling problem.'),
 item('LC041',S,'P6','lsat_rc_inf',4,
  'It can be inferred from the passage that the author regards the probability term in the Hand formulation as',
  ['a quantity that is genuinely numerical but is seldom available to the party at the time of the decision',
   'the least troubling of the three terms because probabilities are objective in a way that burdens and harms are not',
   'a term whose inclusion is what makes the whole formulation incoherent as a comparison',
   'an element that courts have in practice ignored when applying the test to particular facts',
   'the only term that the law and economics movement was able to supply an account of'],
  0,
  'The third paragraph grants that probability is a number, then immediately adds that it is rarely a knowable one at the moment of decision. Both halves are the author\'s view.',
  'The passage does not rank the terms by how troubling they are, and locates the incoherence in the multiplication of gravity rather than in probability. It does not say courts ignore it or that only the movement accounted for it.'),
 item('LC042',S,'P6','lsat_rc_struct',3,
  'Which one of the following most accurately describes the author\'s attitude toward the Hand formulation?',
  ['Appreciative of what it makes visible while unconvinced that its form matches what it actually does',
   'Persuaded that it improves on the standard it replaced and untroubled by the objections to it',
   'Dismissive of it as a borrowing from economics that obscures more than it reveals',
   'Neutral, in that the passage reports the debate without indicating any view of its own',
   'Critical of the courts that apply it without acknowledging that they are doing so'],
  0,
  'The author calls the concealment a thing that matters and says the formulation presents as arithmetic a judgement that is evaluative, yet grants the reply real force and ends by framing the question as a genuine tradeoff. That is appreciation with a reservation about form.',
  'The author is neither untroubled nor dismissive. The passage is not neutral, since it says the concealment matters. The criticism is of the formulation\'s form rather than of the courts.'),
]

# ---- Set 7: plant volatiles ---------------------------------------------------------
S = 'LP7'
ITEMS += [
 item('LC043',S,'P7','lsat_rc_main',3,
  'Which one of the following most accurately states the main point of the passage?',
  ['A well established effect was given a name that implied a function, and the evidence now suggests the function varies by lineage rather than being one thing.',
   'The claim that plants communicate with one another has been shown to be false, and the effect is better explained as a metabolic byproduct of wounding.',
   'Kin selection accounts for the release of volatile compounds by damaged plants in every species in which the effect has been observed.',
   'Experimental work under field conditions has failed to reproduce results obtained for volatile signalling in the laboratory.',
   'Plants with poor vascular connections between branches have evolved airborne signalling as a substitute for internal transport.'],
  0,
  'The passage opens by saying the effect is not disputed, says the name is, canvasses three explanations, and concludes that the phenomenon is not one phenomenon and that the vocabulary carried an unsupported functional claim.',
  'The passage does not say communication has been shown false or endorse the byproduct account. Kin selection is said to be awkward for some species. Field results are said to hold. The within-plant account is one of three, not the conclusion.'),
 item('LC044',S,'P7','lsat_rc_stated',2,
  'The passage states that the defensive response in exposed plants differs from that in unexposed controls in that the exposed plants',
  ['produce protective compounds both sooner and in greater quantity',
   'produce protective compounds in greater quantity but on the same timescale',
   'release volatile compounds of their own before any attack occurs',
   'sustain less damage from herbivores over the course of a season',
   'require a shorter period of exposure before the response can be detected'],
  0,
  'The first paragraph says exposed plants produce protective compounds sooner and in greater quantity than unexposed controls.',
  'The second option drops the timing, which the passage gives. The remaining three describe effects the passage does not report.'),
 item('LC045',S,'P7','lsat_rc_inf',5,
  'The passage suggests that the within-plant signalling account is supported by the sagebrush result primarily because that result',
  ['shows an effect on the emitter itself, which an account treating the compounds as mere byproducts does not predict',
   'demonstrates that relatedness between emitter and receiver improves the strength of the response',
   'establishes that volatile compounds travel between branches faster than signals through the stem',
   'rules out the possibility that neighbouring plants detect the compounds at all',
   'shows that the compounds are produced in larger quantities by plants with branching architecture'],
  0,
  'Preventing air movement between a plant\'s own branches reduced its own later resistance. That is a cost to the emitter of losing its own signal, which is what the within-plant account predicts and the byproduct account does not.',
  'Relatedness is raised against kin selection, not here. The speed claim is the account\'s premise rather than what the experiment showed. Nothing rules out detection by neighbours, and quantity by architecture is not reported.'),
 item('LC046',S,'P7','lsat_rc_struct',4,
  'The author\'s reference to smoke serves primarily to',
  ['illustrate how something can be informative to a detector without having been produced in order to inform',
   'suggest that the volatile compounds are harmful to the plants that detect them',
   'concede that the byproduct account cannot explain the experimental results',
   'draw an analogy between chemical detection in plants and sensory perception in animals',
   'emphasise that the compounds are released only when tissue is damaged'],
  0,
  'Smoke appears in the statement of the third explanation, which denies the compounds are signals: they may be informative to whoever detects them the way smoke is informative without having been sent.',
  'No harm is suggested, no concession is made at that point, and the analogy is about sending rather than about sensory modality. The damage point is made elsewhere and is not what the image carries.'),
 item('LC047',S,'P7','lsat_rc_app',5,
  'Which one of the following research findings, if accurate, would most weaken the kin selection explanation as the passage presents it?',
  ['In a species where the response is strong, emitters and receivers in natural stands are no more related to one another than randomly chosen individuals.',
   'In a species where the response is strong, preventing air movement between an emitter\'s own branches reduces its later resistance.',
   'The volatile mixture released after chewing differs in composition from the mixture released after mechanical wounding.',
   'Receivers mount the faster response only when the emitter belongs to the same species.',
   'The protective compounds produced by receivers are metabolically costly to manufacture.'],
  0,
  'Kin selection requires that the warning reach relatives. An emitter whose neighbours are no more related than strangers, in a species where the effect is strong, removes the benefit the account depends on.',
  'The air movement result supports the within-plant account without bearing on relatedness. Mixture composition, species specificity and metabolic cost are all consistent with kin selection.'),
 item('LC048',S,'P7','lsat_rc_inf',4,
  'It can be inferred that the author regards the term plant communication as',
  ['problematic because it asserts something about why the compounds are released rather than only what they do',
   'acceptable provided that the compounds are shown to travel between separate individuals',
   'accurate for sagebrush and inaccurate for the other species in which the effect has been observed',
   'a harmless simplification that has had no effect on the direction of research',
   'preferable to the alternatives on offer because it has generated testable predictions'],
  0,
  'The closing sentence says the vocabulary carried an implicit claim about function that the evidence did not support. The objection is to the functional implication, not to the description of the effect.',
  'Travel between individuals is not the author\'s condition. No per-species verdict on the term is given. The author says the claim was doing work the evidence did not support, so not harmless, and does not defend the term on predictive grounds.'),
 item('LC049',S,'P7','lsat_rc_main',3,
  'The author would most likely describe the conclusion reached in the fourth paragraph as',
  ['unsatisfying to anyone seeking a single explanation but preferable because it fits the evidence',
   'provisional, in that further experiments are expected to identify one mechanism common to all species',
   'surprising, given that the underlying physical mechanism differs between lineages',
   'inconsistent with the field results reported at the start of the passage',
   'the strongest available argument for retaining the vocabulary of communication'],
  0,
  'The final paragraph says exactly this: unsatisfying if a single answer was wanted, useful if an accurate description was.',
  'No single common mechanism is anticipated. The passage says the same physical mechanism was recruited differently, so the difference is in recruitment. Nothing conflicts with the field results, and the conclusion tells against the vocabulary.'),
]

# ---- Set 8: the comparative pair, restoration ---------------------------------------
S = 'LP8'
ITEMS += [
 item('LC050',S,'P8','lsat_rc_main',3,
  'Which one of the following most accurately describes the relationship between the two passages?',
  ['Passage A defends a standard for restoration; passage B argues that the standard presupposes something that does not exist.',
   'Passage A and passage B recommend the same practice for different reasons.',
   'Passage B provides empirical evidence against a claim that passage A makes without support.',
   'Passage A addresses paintings and passage B addresses objects generally, so the two do not conflict.',
   'Passage B accepts passage A\'s account of intention and disputes only its account of varnish.'],
  0,
  'A argues the obligation is to the work as its maker left it. B argues that there is no uniquely correct original state for the restorer to uncover, which attacks the presupposition rather than the application.',
  'They recommend different practices. B offers argument rather than evidence. B is explicitly about paintings. B does not engage A\'s varnish reasoning at all.'),
 item('LC051',S,'P8','lsat_rc_stated',2,
  'Passage A states that painters worked in varnish because varnish',
  ['saturates colour and protects the surface',
   'was expected to acquire an amber tone over time',
   'allowed later restorers to remove accretions safely',
   'was the only medium available for finishing a picture',
   'made the painter\'s decisions about light recoverable'],
  0,
  'Passage A says painters worked in varnish because it saturates colour and protects a surface, not because they anticipated the amber film.',
  'The amber film is what A says they did not anticipate. The other three are not claims A makes about why varnish was used.'),
 item('LC052',S,'P8','lsat_rc_inf',5,
  'Which one of the following would the author of passage B be most likely to say about the documentary exception that passage A allows?',
  ['It concedes that the stopping point is chosen, since a document could only ever settle one of many such choices.',
   'It is unnecessary, because documents recording a painter\'s intentions are almost never authentic.',
   'It should be extended so that documentary evidence governs every decision a restorer makes.',
   'It shows that passage A is really arguing about paintings rather than about restoration in general.',
   'It is the strongest part of passage A\'s argument and should be accepted without qualification.'],
  0,
  'B\'s claim is that no uniquely correct original state exists and that the surface a restorer stops at is chosen. A document settling one intention would not supply the determinate original B denies, so the exception illustrates rather than escapes B\'s point.',
  'B raises no doubt about authenticity and does not ask for the exception to be extended. Both passages are about paintings. B would not accept any part of A without qualification, since its objection is to A\'s presupposition.'),
 item('LC053',S,'P8','lsat_rc_struct',4,
  'The second paragraph of passage B is primarily concerned with',
  ['narrowing the position just stated so that it is not confused with a more extreme one',
   'offering an example that illustrates the principle stated in the first paragraph',
   'conceding the central claim of passage A before restating an objection to it',
   'introducing a distinction between paintings and other kinds of historical object',
   'explaining why crude overpainting is more damaging than discoloured varnish'],
  0,
  'It opens by saying this is not an argument for leaving every accretion in place, grants that crude overpainting should go, and then restates what the argument actually is. That is narrowing to avoid a misreading.',
  'The overpainting case is a disclaimer rather than an illustration of the principle, and no concession to A\'s central claim is made. No object distinction appears, and no comparison of damage is offered.'),
 item('LC054',S,'P8','lsat_rc_app',5,
  'Both authors would most likely agree that',
  ['a restorer who removes a later hand\'s repainting of a face is doing something defensible',
   'the state of a painting when its maker finished it is the state a viewer should be shown',
   'the history of a painting after its completion is part of what the painting now is',
   'documentary evidence of a painter\'s intention should govern a restorer\'s decisions',
   'the choice of a surface to stop at rests on grounds that are aesthetic rather than technical'],
  0,
  'A treats earlier repaintings as damage to be removed. B says a crude overpainting obscuring a face is worth removing and nobody seriously proposes otherwise. They agree on that case.',
  'The second and fourth are A only, the third and fifth are B only.'),
 item('LC055',S,'P8','lsat_rc_inf',4,
  'It can be inferred that the author of passage A regards the claim that artists intended a patina as',
  ['a claim about intention that is usually asserted without the evidence it would require',
   'a claim that is true of some painters and false of others, so that no general rule follows',
   'the strongest objection to cleaning, and one that has not been answered',
   'a confusion between what a painter intended and what a restorer is able to achieve',
   'a position held only by those unfamiliar with the chemistry of varnish'],
  0,
  'Passage A says the objection rests on a claim about intention that is almost never supported, and then sets out what the presumption should be where no document exists.',
  'A does not divide painters into cases, does not call the objection strongest or unanswered, frames the problem as evidence rather than as a confusion of terms, and makes no claim about who holds it.'),
 item('LC056',S,'P8','lsat_rc_struct',3,
  'The phrase describing the intervening centuries as the thing that has been transmitted functions in passage B to',
  ['reverse the metaphor of interference that the opposing argument depends on',
   'establish that the physical condition of a painting cannot be improved',
   'introduce the exception for crude overpainting that follows it',
   'concede that some accretions are more valuable than the original surface',
   'define the technical vocabulary used in the rest of the passage'],
  0,
  'B says the argument for cleaning treats the centuries as interference in a transmission, then answers that they are better understood as the thing transmitted. It turns the opposing image around.',
  'It makes no claim about improvement, does not introduce the exception, ranks nothing above the original surface, and defines no terms.'),
]

# ---- Set 9: field experiments -------------------------------------------------------
S = 'LP9'
ITEMS += [
 item('LC057',S,'P9','lsat_rc_main',3,
  'Which one of the following most accurately expresses the main point of the passage?',
  ['A method that solved a real weakness in its predecessor introduced a different weakness that the field has been slower to acknowledge.',
   'Field experiments are superior to natural experiments because the researcher controls the assignment of the treatment.',
   'Natural experiments should be abandoned because the treatments they study are determined by legislatures rather than by theory.',
   'General equilibrium effects make it impossible to learn anything about policy from experimental evidence.',
   'Economists in the twentieth century reached unsound conclusions by comparing groups that differed in many respects at once.'],
  0,
  'The closing paragraph says the profession traded one uncertainty for another and has been slower to name the second. The body sets out the first weakness and then the second.',
  'The passage declines to rank the designs. It does not call for abandoning natural experiments, does not say nothing can be learned, and treats the pre-1980s comparison problem as background.'),
 item('LC058',S,'P9','lsat_rc_stated',2,
  'According to the passage, the structural weakness of the natural experiment is that',
  ['the treatment studied is whatever history supplied rather than the one the theory concerns',
   'the groups being compared differ from one another in every respect at once',
   'the assignment of people to conditions is rarely close enough to random to be credible',
   'the results obtained are too imprecise to distinguish between competing theories',
   'the method is expensive relative to the precision of the estimates it produces'],
  0,
  'The second paragraph says the researcher did not choose the treatment, so the treatment was whatever history happened to supply.',
  'Differing in every respect describes the older method natural experiments replaced. The passage says the assignment is as good as random for the purpose. Imprecision is mentioned but is not the structural point, and the method is called cheap.'),
 item('LC059',S,'P9','lsat_rc_inf',5,
  'The passage suggests that a field experiment on a programme raising the wages of forty workers would be least informative about',
  ['what would happen if the same programme were applied to an entire labour market',
   'whether the workers who received the higher wages changed their hours of work',
   'how the size of the wage increase affects the response it produces',
   'whether the estimated effect is internally valid for the workers studied',
   'how the programme compares with a second programme tested in the same design'],
  0,
  'The fourth paragraph says a programme too small to move the market produces no general equilibrium effects, and that the market-wide question is usually the one of interest. Scaling up is exactly what the design cannot speak to.',
  'The other four are all within the reach of a well designed small experiment; three of them are named as strengths of the approach.'),
 item('LC060',S,'P9','lsat_rc_struct',4,
  'The passage is organised in which one of the following ways?',
  ['An older method is described and its weakness identified, a newer method is described as removing that weakness, and a cost of the newer method is then set out.',
   'Two methods are described and the evidence for preferring one of them is assembled.',
   'A widely held view is stated, evidence against it is presented, and a revised version of the view is proposed.',
   'A problem is posed, three solutions to it are canvassed, and the most promising is identified.',
   'A historical development is narrated and its consequences for policy are assessed.'],
  0,
  'That is the order exactly: natural experiments, their structural weakness, field experiments removing it, then what has been lost.',
  'The passage assembles no case for preferring one. No widely held view is refuted and no revision offered. There are two methods rather than three solutions, and the assessment is methodological rather than about policy consequences.'),
 item('LC061',S,'P9','lsat_rc_app',5,
  'Which one of the following is most analogous to the tradeoff the passage describes?',
  ['A wind tunnel test of a scale model gives precise measurements of a shape that is not the size of the object that will be built.',
   'A survey with a large sample produces a narrower confidence interval than one with a small sample.',
   'A clinical trial is halted early because an interim analysis shows a clear benefit.',
   'A telescope with a wider field of view resolves less detail than one with a narrower field.',
   'An accountant reconciles two ledgers and finds a discrepancy that neither ledger alone would reveal.'],
  0,
  'The passage says the field experiment measures a scale model of the policy and infers upward, gaining internal validity by design while losing the scale at which the effect of interest operates. The wind tunnel is that structure.',
  'Sample size, early stopping and field of view are tradeoffs of a different kind, and the reconciliation case is not a tradeoff at all.'),
 item('LC062',S,'P9','lsat_rc_inf',4,
  'It can be inferred that the author regards internal validity that is a matter of design rather than of argument as',
  ['a genuine advance, though not one that settles what the estimate applies to',
   'the decisive consideration in choosing between the two methods',
   'less important than the credibility that natural experiments earn through debate',
   'achievable only in laboratory conditions rather than in the field',
   'the reason the profession was slow to notice the limits of field experiments'],
  0,
  'The third paragraph presents it as a real gain. The fourth immediately says what the design cannot reach, and the conclusion declines to rank the methods. So it is an advance that leaves the question of scope open.',
  'The author explicitly declines to make it decisive and does not rank it below debate. It is said to hold in the field. The slowness is noted without being explained this way.'),
 item('LC063',S,'P9','lsat_rc_main',3,
  'The author\'s attitude toward the shift from natural experiments to field experiments is best described as',
  ['recognising the gain while pressing a question the shift has left unanswered',
   'approving, on the ground that internal validity is the paramount methodological virtue',
   'sceptical, on the ground that experimental treatments are too small to be informative',
   'indifferent, since the passage treats the two designs as equally sound',
   'critical of the profession for having adopted a method whose weaknesses were obvious'],
  0,
  'The author credits findings natural experiments could not have produced, then presses the scale question, then says the profession traded one uncertainty for another and named the second more slowly.',
  'Not approving without reservation, and not sceptical that field experiments are uninformative. Not indifferent, since a specific gap is pressed. The criticism is of the slowness to name it, not of the adoption.'),
]

# ---- Set 10: continental drift ------------------------------------------------------
S = 'LP10'
ITEMS += [
 item('LC064',S,'P10','lsat_rc_main',4,
  'Which one of the following most accurately expresses the main point of the passage?',
  ['The long rejection of continental drift is misdescribed by both of the usual morals, because the conclusion was right and the mechanism offered for it was impossible.',
   'Wegener\'s hypothesis was rejected because he was a meteorologist rather than a geologist, and the rejection was therefore a failure of scientific openness.',
   'The discovery of seafloor spreading in the 1950s vindicated the mechanism Wegener had proposed four decades earlier.',
   'Geophysicists who calculated the forces required to move continents made errors that went undetected for half a century.',
   'Scientific communities accept new hypotheses only when the evidence for them becomes overwhelming.'],
  0,
  'The last paragraph says both available morals are wrong and states the position: a correct conclusion supported by an incorrect mechanism, which the evidence of the day could not distinguish from a wrong conclusion.',
  'The passage calls the outsider story incomplete rather than correct. The new evidence replaced Wegener\'s mechanism rather than vindicating it. The calculations are said to have been correct. The final option is a generality the passage does not endorse.'),
 item('LC065',S,'P10','lsat_rc_stated',2,
  'The passage states that the geophysicists\' calculations showed that',
  ['the available forces were far smaller than those required and oceanic crust was far too strong to be ploughed through',
   'the continents had not been joined at any point in the geological past',
   'tidal forces vary too little over geological time to produce a poleward drift',
   'the fit of the coastlines could be accounted for by erosion rather than by separation',
   'the fossil distributions Wegener assembled were consistent with land bridges'],
  0,
  'The third paragraph reports both calculations in these terms and adds that both were correct.',
  'The calculations addressed the mechanism, not whether the continents had been joined, and the passage says the correspondences were widely agreed to require explanation. The remaining options are not in the passage.'),
 item('LC066',S,'P10','lsat_rc_inf',5,
  'Which one of the following can be inferred from the passage about the evidence Wegener assembled?',
  ['It was largely accepted at the time and was not what changed when the hypothesis was finally accepted.',
   'It was dismissed by geologists who had not examined the fossil and glacial records themselves.',
   'It was superseded by the magnetic surveys, which explained the same observations more economically.',
   'It was insufficient on its own to show that the continents had once been joined.',
   'It was reinterpreted in the 1950s as evidence for a mechanism Wegener had not considered.'],
  0,
  'The passage says the evidence was not ignored, that much of it was accepted, and that the continental evidence was much the same in 1960 as in 1920. What changed was the ocean floor.',
  'The passage denies it was ignored. The surveys explained different observations. The passage does not say the continental evidence was insufficient for the conclusion, only that the mechanism failed. The fifth misstates what the new evidence did.'),
 item('LC067',S,'P10','lsat_rc_struct',4,
  'The second paragraph of the passage functions primarily to',
  ['identify a common account of the episode and state what is missing from it',
   'supply the biographical background needed to understand the rejection',
   'concede a point to Wegener\'s critics before rejecting their conclusion',
   'introduce the geophysical calculations that the following paragraph describes',
   'contrast the reception of the hypothesis in geology with its reception in meteorology'],
  0,
  'It names the parable about conservatism, calls it satisfying and incomplete, and says what the parable leaves out: the evidence was not ignored and the mechanism was what failed.',
  'It supplies no biography beyond the discipline point, concedes nothing to critics, and does not contrast disciplines. It sets up the third paragraph without being about the calculations.'),
 item('LC068',S,'P10','lsat_rc_app',5,
  'The author\'s analysis of the drift episode most strongly supports which one of the following principles?',
  ['A hypothesis may be reasonably resisted when its only proposed mechanism is demonstrably impossible, even if its conclusion is correct.',
   'A hypothesis supported by evidence from several independent domains should be accepted even where no mechanism for it is known.',
   'Scientific disputes are resolved by the accumulation of evidence rather than by the discovery of new kinds of evidence.',
   'The disciplinary background of a hypothesis\'s proponent should play no part in how the hypothesis is assessed.',
   'A correct conclusion reached by faulty reasoning is of no more value to a field than an incorrect one.'],
  0,
  'That is the passage\'s own summary: a hypothesis whose only mechanism has been shown impossible is in serious trouble, and treating it so is not prejudice, even though the conclusion turned out correct.',
  'The second is the position the passage says was reasonably resisted. The third is contradicted by the role of the ocean floor data. The fourth is a fair principle but not what the analysis supports. The fifth is stronger than anything the passage says.'),
 item('LC069',S,'P10','lsat_rc_inf',4,
  'The passage suggests that the author regards the contempt shown toward Wegener as',
  ['unwarranted, even though the resistance to his mechanism was not',
   'the principal reason the hypothesis took half a century to be accepted',
   'understandable given that his training was in a different discipline',
   'evidence that the parable about scientific conservatism is essentially correct',
   'a consequence of his failure to publish the fossil and glacial evidence in full'],
  0,
  'The final paragraph says the smooth-working moral is wrong because Wegener was treated with a contempt his argument did not deserve, while the paragraph before defends the resistance to the mechanism as reasonable.',
  'The passage attributes the delay to the missing ocean floor evidence. It does not excuse the contempt by discipline, says the parable is incomplete, and never suggests he withheld evidence.'),
 item('LC070',S,'P10','lsat_rc_struct',4,
  'Which one of the following best describes the role of the fourth paragraph in the passage?',
  ['It explains what new evidence resolved the dispute and why it did so without vindicating the original mechanism.',
   'It presents the strongest version of the argument the second paragraph had criticised.',
   'It supplies the biographical detail that the earlier paragraphs had deferred.',
   'It concedes that the geophysical calculations reported earlier were mistaken.',
   'It generalises from the drift episode to the behaviour of scientific communities.'],
  0,
  'The fourth paragraph gives the ridges, the magnetic bands and the dating, and then says the continents were not ploughing through the crust at all, so the impossible mechanism had never been the right one.',
  'It does not restate the parable, adds no biography, affirms rather than retracts the calculations, and the generalising is left to the fifth paragraph.'),
]

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# Distractor extension.
#
# Measured on the first pass: the longest option was the key on 66 percent of items,
# against a chance rate of 20 and a recorded cap of 36. That is the INC-0044 length tell
# reappearing in hand written content, and a student who picks the longest option without
# reading would have scored two in three on this bank.
#
# The cause is real rather than careless. A correct LSAT answer is usually the most fully
# qualified statement on offer, so writing the key first and the distractors after
# produces short wrong answers. The fix is the one INC-0044 used: lengthen distractors so
# the key's length rank is uniform, with each added clause chosen to leave the option
# wrong for the reason it was already wrong. Every clause below either states the
# omission that makes the option wrong or carries its error one step further. None of
# them is filler, and none makes a wrong option defensible.
EXTEND = {
 'LC036': ('therefore incoherent', ', and no reformulation of it could repair that defect'),
 'LC037': ('that would have prevented it', ', whatever the probability of its occurring'),
 'LC040': ('a measurement was taken wrongly', ' and the error went unnoticed until the structure was built'),
 'LC043': ('metabolic byproduct of wounding', ' that is informative only to whoever happens to detect it'),
 'LC045': ('faster than signals through the stem', ', which is the premise the account begins from'),
 'LC046': ('sensory perception in animals', ', where a stimulus is received and then acted upon'),
 'LC047': ('reduces its later resistance', ', which bears on where the signal is directed'),
 'LC048': ('in which the effect has been observed', ', so that no single verdict on the term is possible'),
 'LC050': ('so the two do not conflict', ' and can both be accepted without qualification'),
 'LC052': ('rather than about restoration in general', ', which narrows its scope considerably'),
 'LC053': ('other kinds of historical object', ', a distinction the first paragraph had not drawn'),
 'LC056': ('more valuable than the original surface', ' that lies beneath them'),
 'LC057': ('rather than by theory', ', a limitation that no amount of care in the analysis can remedy'),
 'LC058': ('close enough to random to be credible', ' for the particular comparison being drawn'),
 'LC059': ('changed their hours of work', ' in response to the programme'),
 'LC060': ('a revised version of the view is proposed', ' that accommodates the evidence while preserving what was correct in the original'),
 'LC061': ('neither ledger alone would reveal', ', and corrects both of them accordingly'),
 'LC064': ('a failure of scientific openness', ' rather than a judgement about the evidence available'),
 'LC065': ('by erosion rather than by separation', ' of the landmasses over geological time'),
 'LC066': ('explained the same observations more economically', ' than his own account had'),
 'LC068': ('no mechanism for it is known', ' or can presently be imagined'),
}

for it in ITEMS:
    ext = EXTEND.get(it['id'])
    if not ext:
        continue
    needle, clause = ext
    hits = [i for i, c in enumerate(it['choices']) if needle in c]
    if len(hits) != 1:
        sys.exit('%s: needle %r matched %d choices, not 1' % (it['id'], needle, len(hits)))
    i = hits[0]
    if i == it['answer']:
        sys.exit('%s: the extension targets the key, which would make the tell worse' % it['id'])
    c = it['choices'][i]
    trailing = c.endswith('.')
    if trailing:
        c = c[:-1]
    it['choices'][i] = c + clause + ('.' if trailing else '')

# A second clause on thirteen items, for a tell the recorded ratchet does not measure.
#
# After the first pass the two extremes were clean, 0 percent longest and 6 percent
# shortest against a cap of 36. The length RANK was not: 25 of 35 keys sat second
# longest, so a student who always picked the second longest option would have scored
# 71 percent. That is the same exploit one position over, and the reason it appeared is
# mechanical. Extending exactly one distractor past the key moves every key from rank 5
# to rank 4.
#
# These clauses push a second distractor past the key on a subset, spreading the rank.
# Same rule as the first pass: each addition states the omission that makes the option
# wrong or carries its error one step further, and none makes a wrong option defensible.
EXTEND2 = {
 'LC036': ('reached inconsistent verdicts', ' from one jurisdiction to the next'),
 'LC037': ('failed to take steps to avoid it', ', whatever the burden of doing so would have been'),
 'LC038': ('does not require harms to persons to be priced at all', ', and so avoids the comparison entirely'),
 'LC040': ('declines to explain the reasoning', ' that produced the particular number it chose, leaving the tradeoff unstated'),
 'LC041': ('ignored when applying the test', ' to the particular facts in front of them'),
 'LC043': ('in every species in which the effect has', ' been observed, whatever the relatedness of the plants involved'),
 'LC045': ('relatedness between emitter and receiver improves', ' the strength of the response in every species tested'),
 'LC046': ('harmful to the plants that detect them', ', rather than merely detectable by them'),
 'LC047': ('differs in composition from the mixture released after mechanical wounding', ', which bears on what triggers release'),
 'LC048': ('shown to travel between separate individuals', ' rather than only between the branches of one'),
 'LC049': ('underlying physical mechanism differs between lineages', ' rather than having been recruited differently'),
 'LC050': ("accepts passage A's account of intention", ' and disputes only its account of what varnish was for'),
 'LC052': ('almost never authentic', ' and cannot be relied on where they survive'),
}

for it in ITEMS:
    ext = EXTEND2.get(it['id'])
    if not ext:
        continue
    needle, clause = ext
    hits = [i for i, c in enumerate(it['choices']) if needle in c]
    if len(hits) != 1:
        sys.exit('%s: EXTEND2 needle %r matched %d choices, not 1' % (it['id'], needle, len(hits)))
    i = hits[0]
    if i == it['answer']:
        sys.exit('%s: EXTEND2 targets the key' % it['id'])
    c = it['choices'][i]
    trailing = c.endswith('.')
    if trailing:
        c = c[:-1]
    it['choices'][i] = c + clause + ('.' if trailing else '')


# Emit.
#
# Every item above was written with its key first, because that is how a person writes
# one. Shipping it that way would reproduce INC-0039 exactly: 225 of 302 correct answers
# sitting at position A, a bank a test-wise student can beat without reading. So the
# choices are permuted here and the answer index is COMPUTED from where the key landed,
# never asserted.
#
# The seed is zlib.crc32 of the item id, not Python's hash(), because hash() is randomised
# per process and the bank would differ on every build (INC-0003).
import zlib, random

def permute(it):
    key = it['choices'][it['answer']]
    rnd = random.Random(zlib.crc32(it['id'].encode('ascii')))
    ch = list(it['choices'])
    rnd.shuffle(ch)
    it['choices'] = ch
    it['answer'] = ch.index(key)
    return it

for it in ITEMS:
    permute(it)

PASS_SRC = {'P6': P6, 'P7': P7, 'P8': P8A + '\n\n' + P8B, 'P9': P9, 'P10': P10}
PVAR = {'P6': 'LC_P6', 'P7': 'LC_P7', 'P8': 'LC_P8', 'P9': 'LC_P9', 'P10': 'LC_P10'}

HEADER = '''// bank_lsat_rc2.js - Original LSAT Reading Comprehension items LC036-LC070.
//
// The second Reading Comprehension bank. HANDOFF.md names the reading corpus as the
// biggest real gap in the product: every thin category across every exam is passage
// based, because passages are hand written and no generator makes them, and no increase
// to the generated TARGET can change that. LSAT was the thinnest of all at 65 items
// across twelve categories. These five sets of seven take Reading Comprehension from 35
// items to 70.
//
// Five sets, matching the shape LSAC publishes for the section: four single passages and
// one comparative pair, each followed by five to eight questions. Subjects are spread as
// the real section spreads them, across law, natural science, humanities, social science
// and the history of science.
//
// Every set covers all five tracked Reading Comprehension skills, for the same reason the
// first bank does: the engine builds a section out of whole passage groups, so a skill
// confined to one passage would be dropped whenever that passage is not selected.
//
// TWO THINGS ABOUT HOW THIS FILE WAS PRODUCED, both of which are ledger entries.
//
// The strings are JSON escaped rather than hand quoted. An unescaped apostrophe inside a
// single quoted JS string once took the entire trainer down at parse time (INC-0001), and
// passages are made of apostrophes.
//
// The answer positions are permuted and the index computed from where the key landed. The
// items were written with the correct choice first, because that is how a person writes
// one, and shipping them that way would have reproduced INC-0039: a bank whose key sits at
// position A, beatable without reading the question. The permutation is seeded from
// zlib.crc32 of the item id, not from hash(), which Python randomises per process and
// which once made every build produce a different bank (INC-0003).
'''

out = [HEADER]
for k in ['P6', 'P7', 'P8', 'P9', 'P10']:
    out.append('const %s = %s;' % (PVAR[k], json.dumps(PASS_SRC[k])))
out.append('')
out.append('const BANK_LSAT_RC2 = [')
cur = None
for it in ITEMS:
    if it['passageId'] != cur:
        cur = it['passageId']
        out.append('// ---------- Set %s ----------' % cur)
    fields = [
        # Single quoted, matching every other bank file. The id is plain ASCII with
        # nothing to escape, and the build's item counter reads ids by pattern: a file
        # that quotes them differently counted as zero items (INC-0059).
        "id:'%s'" % it['id'],
        'section:%s' % json.dumps(it['section']),
        'type:%s' % json.dumps(it['type']),
        'passageId:%s' % json.dumps(it['passageId']),
        'passage:%s' % PVAR[it['_p']],
        'skill:%s' % json.dumps(it['skill']),
        'diff:%d' % it['diff'],
    ]
    out.append('{' + ','.join(fields) + ',')
    out.append(' stem:%s,' % json.dumps(it['stem']))
    out.append(' choices:[' + ','.join(json.dumps(c) for c in it['choices']) + '],answer:%d,' % it['answer'])
    out.append(' expl:%s,' % json.dumps(it['expl']))
    out.append(' wrong:%s},' % json.dumps(it['wrong']))
out.append('];')
out.append('')
out.append('')

js = '\n'.join(out)

# House rules, checked here rather than discovered by the build.
for ch, name in ((chr(0x2014), 'em dash'), (chr(0x2013), 'en dash')):
    if ch in js:
        sys.exit('%s in the bank' % name)
bad = sorted(set(c for c in js if ord(c) > 127))
if bad:
    sys.exit('non-ascii in the bank: %r' % bad)

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'x')
dest = sys.argv[1] if len(sys.argv) > 1 else 'src/bank_lsat_rc2.js'
io.open(dest, 'w', encoding='utf-8').write(js)

# Report the two distributions that matter, measured rather than assumed.
from collections import Counter
pos = Counter(it['answer'] for it in ITEMS)
longest_is_key = sum(1 for it in ITEMS
                     if len(it['choices'][it['answer']]) == max(len(c) for c in it['choices']))
skills = Counter(it['skill'] for it in ITEMS)
print('wrote %s: %d items, %d passages' % (dest, len(ITEMS), len(PASS_SRC)))
print('  key position   ', dict(sorted(pos.items())), ' (chance is %.1f each)' % (len(ITEMS) / 5.0))
print('  longest is key %d of %d = %d%% (chance 20%%)'
      % (longest_is_key, len(ITEMS), round(longest_is_key * 100.0 / len(ITEMS))))
print('  per skill      ', dict(sorted(skills.items())))
print('  choices per item', sorted(set(len(it['choices']) for it in ITEMS)))
