#!/usr/bin/env python3
"""Emit src/bank_act_reading2.js.

Run: python3 src/mk_bank_act_reading2.py src/bank_act_reading2.js

The second ACT Reading bank. With the LSAT done, ACT Reading was the thinnest passage
based section left: 40 items across three skills, 11 of them in two of the skills. These
40 items take it to 80 and every skill past the review bot's threshold of 25.

Four passages, one in each genre the ACT uses and in the order it uses them: literary
narrative, social science, humanities, natural science. Ten questions each, which is the
real section's shape.

Machinery is in src/bank_emit.py. See that file for why keys are permuted, why the seed
is crc32, and why the strings are JSON escaped.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

P6 = ("LITERARY NARRATIVE: The Tuner\n\n"
"My father tuned pianos for forty one years and never owned one. He said the reason was "
"obvious and I did not understand it until I was thirty. A tuner who keeps a piano at "
"home stops hearing it. The instrument becomes furniture, and furniture is the one thing "
"a tuner cannot afford to make of a piano.\n\n"
"He worked by ear and by a fork he had carried since his apprenticeship, a dull steel "
"thing he struck against his knee. Electronic tuners existed and he did not object to "
"them. He said they were faster and that speed was not what anyone was paying him for. "
"What they were paying him for, he said, was the twenty minutes after the tuning, when he "
"sat and played badly and listened to what the room did to the sound.\n\n"
"I went with him on Saturdays. The houses were mostly unremarkable and the pianos were "
"mostly bad, and he treated each one as though it had been made for someone who loved it, "
"which he pointed out was usually true. A bad piano that is played is worth more attention "
"than a good one that is not, he said, because attention is the only thing that keeps an "
"instrument from becoming a table.\n\n"
"Once, in a house where nobody had touched the piano in a decade, he tuned it for two "
"hours and then refused payment. I asked him about it on the way home. He said the woman "
"had explained that it was her mother's and she could not bring herself to sell it and "
"could not bring herself to play it either. He said he had not tuned a piano that "
"afternoon. He had tuned a piece of furniture, and he did not charge for furniture.\n\n"
"I have a piano now. I play it badly, most evenings, and I hear it every time.")

P7 = ("SOCIAL SCIENCE: What the Queue Knows\n\n"
"When a new road opens, traffic on it is lighter than planners predicted for about a year, "
"and then it is heavier. The pattern is so consistent that it has a name, induced demand, "
"and an explanation that most planners now accept: a faster road changes where people "
"choose to live, work and shop, and those choices take time to register. The road does not "
"absorb existing trips. It creates new ones.\n\n"
"The finding is old. Engineers in the 1930s noticed that widening a congested street "
"relieved it only briefly. What is new is the ability to measure it. Vehicle counts once "
"came from a person with a clipboard at an intersection; they now come from the phones in "
"the cars, which record not only how many vehicles passed but where each began and where "
"it ended. That second piece is what turned an anecdote into a quantity.\n\n"
"The measured elasticity is close to one. A ten percent increase in road capacity in a "
"metropolitan area produces, within a decade, roughly a ten percent increase in vehicle "
"miles travelled. Congestion returns to where it was. The road is not useless: more people "
"are making more trips, and trips have value. But the benefit is not the one the road was "
"sold on, and the difference matters when a city is deciding what to build.\n\n"
"The uncomfortable corollary is that the reverse also holds. Cities that have removed "
"urban motorways have found that the traffic does not reappear on surrounding streets in "
"the volumes predicted. Some of it disappears. Trips that were worth making at one cost "
"are not worth making at another, and a road, like a queue, is partly made of the people "
"who decided to join it.")

P8 = ("HUMANITIES: The Copyist's Hand\n\n"
"Before photography, the way to know a painting you could not visit was to see a copy of "
"it, and copies were made by the thousand. The copyist was a recognised profession with an "
"apprenticeship and a market, and the best of them were paid well. The word we would use "
"now, reproduction, carries an implication the period would not have recognised: that the "
"copy is a lesser kind of thing whose only merit is fidelity.\n\n"
"Read the contracts and a different picture appears. A patron commissioning a copy "
"routinely specified changes. Make the room lighter. Leave out the dog. Put my wife's face "
"where the saint's is. These were not liberties taken by a careless hand; they were the "
"commission. The copyist was understood to be making a new painting that stood in a "
"particular relation to an old one, and the relation was a matter of negotiation rather "
"than of duty.\n\n"
"This is awkward for a way of thinking about art that begins with the single authentic "
"object. It is less awkward if you notice that the period had no such notion. A workshop "
"produced paintings; the master's hand appeared in some passages and not others; a "
"successful composition was repeated because it was successful. The idea that a painting "
"is the trace of one person's unrepeatable act is roughly two centuries old, and we have "
"projected it backwards onto three centuries that did not hold it.\n\n"
"None of this makes the copies masterpieces. Most are dull, as most of anything is. It "
"does mean that judging them as failed originals is judging them by a standard nobody "
"involved in making them had ever heard of.")

P9 = ("NATURAL SCIENCE: The Ice Has a Memory\n\n"
"An ice core is a cylinder of compressed snow, and the snow fell in layers, one for each "
"year. Near the surface the layers are thick enough to count by eye. Deeper down the weight "
"above compresses them, and by two kilometres a layer is a few millimetres, and by three it "
"is thinner than that. Counting stops being possible and dating has to be done another way.\n\n"
"Trapped in the ice are bubbles of the atmosphere as it was when the snow closed over them. "
"This is what makes the cores valuable: they are not a proxy for past air, they are past "
"air. Measure the carbon dioxide in a bubble and you have measured the carbon dioxide in "
"the atmosphere of that year, with no model in between.\n\n"
"There is a complication, and it is not small. Snow does not become ice at the surface. It "
"stays porous for decades, sometimes centuries, and air circulates through it freely until "
"the pores close. So the air in a bubble is younger than the ice around it, by an interval "
"that depends on the temperature and the snowfall rate at the time. In central Antarctica, "
"where snowfall is light, the gap can exceed six thousand years.\n\n"
"This does not make the cores unreliable. It makes them require a correction, and the "
"correction is itself measured rather than assumed: the closure depth can be observed "
"directly in modern snow, and the relationship between climate and closure can be "
"calibrated against periods where an independent date exists. What the ice will not give "
"you is a reading you can take without knowing any of this, and a great deal of "
"misunderstanding about ice cores comes from people who wanted one.")

I = []
def q(iid, pid, pv, sub, skill, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'R', 'type': 'R', 'passageId': pid, '_p': pv,
              'sub': sub, 'skill': skill, 'diff': diff, 'stem': stem,
              'choices': choices, 'answer': 0, 'expl': expl, 'wrong': wrong})
print('scaffold ready')

# ---- ARP6 literary narrative ---------------------------------------------------------
q('AR041','ARP6','P6','Central idea','act_r_kid',3,
 'The main purpose of the passage is to:',
 ['convey what the narrator eventually understood about a father\'s refusal to own a piano.',
  'explain the technical differences between tuning by ear and tuning electronically.',
  'describe the decline of piano tuning as a profession over four decades.',
  'criticise people who keep instruments in their homes without playing them.'],
 'The passage opens with the refusal, says the narrator did not understand it until thirty, and closes with the narrator owning a piano and hearing it every time. The arc is the understanding.',
 'The electronic comparison is one paragraph. No decline is described. The woman with her mother\'s piano is treated with sympathy rather than criticism.')
q('AR042','ARP6','P6','Detail','act_r_kid',2,
 'According to the passage, the father said that what his customers were paying him for was:',
 ['the twenty minutes after the tuning, spent listening to the room.',
  'the speed with which he could complete a tuning.',
  'the steel fork he had carried since his apprenticeship.',
  'his refusal to use electronic tuning equipment.'],
 'He says speed is not what anyone is paying for, and then names the twenty minutes afterwards.',
 'Speed is explicitly ruled out. The fork and the refusal are described but never named as what is paid for.')
q('AR043','ARP6','P6','Word meaning','act_r_cs',3,
 'As it is used in the passage, the word furniture most nearly means something that is:',
 ['present without being attended to.',
  'built to be useful rather than beautiful.',
  'too heavy to be moved easily.',
  'inherited rather than purchased.'],
 'The father says a tuner who keeps a piano stops hearing it and it becomes furniture, and later that attention is what keeps an instrument from becoming a table. Furniture is the unattended thing.',
 'Usefulness, weight and inheritance are all associations the word can carry elsewhere but none is the sense the passage builds.')
q('AR044','ARP6','P6','Text structure','act_r_cs',3,
 'The final one sentence paragraph functions primarily to:',
 ['show that the narrator has come to hold the view the father was describing.',
  'reveal that the narrator has taken up the father\'s profession.',
  'suggest that the narrator regrets not having owned a piano earlier.',
  'contrast the narrator\'s musical ability with the father\'s.'],
 'The father\'s point was that attention is what keeps a piano from being furniture. The narrator plays badly and hears it every time, which is the father\'s position held rather than merely reported.',
 'No profession is taken up. Regret is not expressed, and playing badly echoes the father\'s own description of himself rather than contrasting with it.')
q('AR045','ARP6','P6','Tone and perspective','act_r_cs',3,
 'The narrator\'s attitude toward the father is best described as:',
 ['respectful of a judgement the narrator needed years to share.',
  'amused by convictions the narrator regards as eccentric.',
  'resentful of Saturdays spent in other people\'s houses.',
  'uncertain whether the father\'s methods were effective.'],
 'The narrator says the reason was obvious and that understanding took until thirty, then ends by holding the same view. That is respect arriving late.',
 'Nothing is treated as eccentric or resented, and the father\'s effectiveness is never questioned.')
q('AR046','ARP6','P6','Inference','act_r_kid',4,
 'It can reasonably be inferred that the father refused payment because he believed that:',
 ['the work he had done did not count as tuning a piano in the sense he cared about.',
  'the woman would not have been able to afford his usual fee.',
  'the instrument was too damaged for the tuning to hold.',
  'he had taken longer than he had originally quoted.'],
 'He says directly that he had not tuned a piano, he had tuned a piece of furniture, and that he does not charge for furniture.',
 'Affordability, damage and overrun are never mentioned; the two hours are given without complaint.')
q('AR047','ARP6','P6','Integration of ideas','act_r_iki',4,
 'The father\'s remark that a bad piano that is played is worth more attention than a good one that is not most directly supports the idea that:',
 ['the value he assigns to an instrument depends on its use rather than its quality.',
  'poorly made pianos require more frequent tuning than well made ones.',
  'skilled players are less common among his customers than he would like.',
  'the condition of an instrument can be judged from how often it is tuned.'],
 'The remark ranks a played bad piano above an unplayed good one, which makes use rather than quality the measure.',
 'Frequency of tuning, the skill of players and judging condition are all plausible topics the remark does not address.')
q('AR048','ARP6','P6','Integration of ideas','act_r_iki',4,
 'Which of the following statements would the father most likely agree with, based on the passage?',
 ['A well made instrument left untouched for years has lost something a tuning cannot restore.',
  'An electronic tuner produces a result inferior to one produced by ear.',
  'A tuner should decline work on instruments that are rarely played.',
  'The value of a piano is determined largely by the quality of its manufacture.'],
 'He calls the untouched piano furniture rather than an instrument and will not charge for it, which is exactly this.',
 'He says he does not object to electronic tuners. He took the work rather than declining it. Manufacture is the measure he rejects.')
q('AR049','ARP6','P6','Detail','act_r_kid',2,
 'The passage indicates that the father tuned using:',
 ['his ear together with a tuning fork he had kept since training.',
  'an electronic tuner he had bought late in his career.',
  'a set of forks of different pitches carried in a case.',
  'his ear alone, without any reference pitch.'],
 'The passage says he worked by ear and by a fork carried since his apprenticeship.',
 'He did not use an electronic tuner himself, one fork is described rather than a set, and the fork is a reference pitch.')
q('AR050','ARP6','P6','Integration of ideas','act_r_iki',5,
 'The passage as a whole suggests that the father\'s refusal to own a piano and his refusal to accept payment share which underlying principle?',
 ['An instrument is defined by the attention paid to it rather than by its presence.',
  'A professional should not profit from work performed on a personal acquaintance.',
  'Equipment owned by a tradesperson should be limited to what the trade requires.',
  'Work should be priced by the time it takes rather than by its difficulty.'],
 'He will not own one because ownership would stop him hearing it, and he will not charge for one nobody hears. Both turn on attention constituting the instrument.',
 'The woman is not an acquaintance, the equipment point is not made, and he charges nothing at all rather than by time.')

# ---- ARP7 social science -------------------------------------------------------------
q('AR051','ARP7','P7','Central idea','act_r_kid',3,
 'The main idea of the passage is that:',
 ['added road capacity generates new travel, so congestion returns and the benefit is not the one promised.',
  'measurements of traffic taken from mobile phones are more accurate than counts taken by hand.',
  'cities that remove urban motorways experience less disruption than planners predict.',
  'engineers have understood induced demand since the 1930s but have been ignored by planners.'],
 'The passage defines induced demand, reports the measured elasticity, and draws the conclusion that congestion returns and the benefit is different from the one the road was sold on.',
 'Phone data, motorway removal and the history are each a supporting paragraph rather than the point.')
q('AR052','ARP7','P7','Detail','act_r_kid',2,
 'According to the passage, the measured elasticity of vehicle miles travelled with respect to road capacity is:',
 ['close to one, so a ten percent capacity increase produces roughly ten percent more travel.',
  'well below one, so travel rises more slowly than capacity.',
  'above one, so travel rises faster than capacity.',
  'too variable between cities to be summarised by a single figure.'],
 'The passage states the elasticity is close to one and gives the ten percent example.',
 'Below one, above one and unmeasurable all contradict the stated figure.')
q('AR053','ARP7','P7','Text structure','act_r_cs',3,
 'The second paragraph serves mainly to:',
 ['explain why a long standing observation could recently be turned into a measurement.',
  'establish that engineers in the 1930s were the first to propose induced demand.',
  'argue that clipboard counts were unreliable and should never have been used.',
  'introduce the objection that the rest of the passage answers.'],
 'It contrasts the old clipboard counts with phone data that records origin and destination, and says that second piece turned an anecdote into a quantity.',
 'Priority of discovery is mentioned but is not the function. The old counts are not called unreliable, and no objection is introduced.')
q('AR054','ARP7','P7','Word meaning','act_r_cs',3,
 'As used in the passage, the word absorb most nearly means:',
 ['accommodate without generating more of.',
  'eliminate entirely from the network.',
  'delay until a later period.',
  'redistribute among neighbouring routes.'],
 'The sentence contrasts absorbing existing trips with creating new ones, so absorbing is taking in what is already there without adding to it.',
 'Elimination, delay and redistribution are all things a road might do but none is set against creating new trips.')
q('AR055','ARP7','P7','Author perspective','act_r_cs',4,
 'The author\'s attitude toward new road construction is best described as:',
 ['sceptical of the case usually made for it while allowing that it delivers something.',
  'opposed to it on the ground that congestion always returns to its previous level.',
  'supportive of it because additional trips have value to those who make them.',
  'neutral, in that the passage reports findings without evaluating them.'],
 'The author says the road is not useless and that trips have value, then says the benefit is not the one the road was sold on and that the difference matters.',
 'Not outright opposition, since value is granted; not support, since the case is challenged; not neutral, since a judgement is stated.')
q('AR056','ARP7','P7','Inference','act_r_kid',4,
 'It can reasonably be inferred from the passage that a road opened last month is likely to:',
 ['carry less traffic now than it will carry in several years.',
  'already be as congested as the road it was built to relieve.',
  'reduce vehicle miles travelled across the metropolitan area.',
  'attract traffic mainly from drivers who previously used side streets.'],
 'The passage opens by saying traffic is lighter than predicted for about a year and then heavier, because relocation decisions take time.',
 'Immediate congestion contradicts the first year pattern, area travel rises rather than falls, and the source of the new traffic is described as new trips rather than diverted ones.')
q('AR057','ARP7','P7','Integration of ideas','act_r_iki',4,
 'The final paragraph supports which of the following claims about traffic?',
 ['The number of trips people make depends partly on how easy those trips are.',
  'Removing a motorway reduces the total number of vehicles registered in a city.',
  'Surrounding streets can absorb any volume displaced from a closed motorway.',
  'Predictions about motorway removal have generally proved accurate.'],
 'The paragraph says trips worth making at one cost are not worth making at another, and that a road is partly made of the people who decided to join it.',
 'Registrations are not discussed, the streets do not absorb the traffic because some of it disappears, and the predictions are said to be wrong.')
q('AR058','ARP7','P7','Integration of ideas','act_r_iki',5,
 'The comparison of a road to a queue in the last sentence is used to suggest that:',
 ['both are partly constituted by the choices of the people who join them.',
  'both become less efficient as more people use them.',
  'both require a central authority to manage access.',
  'both are more easily removed than they are built.'],
 'The sentence says trips worth making at one cost are not at another, and that a road, like a queue, is partly made of the people who decided to join it.',
 'Efficiency, management and ease of removal are all true of queues in some sense but none is the point the sentence draws.')
q('AR059','ARP7','P7','Detail','act_r_kid',2,
 'The passage states that vehicle counts now come from:',
 ['phones in the cars, which record where each trip began and ended.',
  'sensors embedded in the road surface at fixed intervals.',
  'cameras that photograph vehicles at intersections.',
  'surveys in which drivers report their journeys.'],
 'The second paragraph says counts now come from the phones in the cars, recording origin and destination.',
 'Sensors, cameras and surveys are not mentioned.')
q('AR060','ARP7','P7','Integration of ideas','act_r_iki',4,
 'Which finding, if reported, would most weaken the passage\'s account of induced demand?',
 ['In a large sample of cities, vehicle miles travelled were unchanged a decade after capacity rose.',
  'Some cities that removed motorways saw traffic increase on parallel routes.',
  'Phone based counts systematically undercount trips shorter than one mile.',
  'Congestion on a new road took eighteen months rather than a year to return.'],
 'The account rests on the elasticity being close to one. Unchanged travel after a decade would put it near zero.',
 'Parallel routes, short trip undercounting and a slightly different timescale each qualify a detail rather than the central claim.')

print('%d items after ARP6 and ARP7' % len(I))

# ---- ARP8 humanities -----------------------------------------------------------------
q('AR061','ARP8','P8','Central idea','act_r_kid',3,
 'The main purpose of the passage is to:',
 ['argue that copies were made under assumptions the modern idea of the original does not capture.',
  'establish that most painted copies produced before photography were of poor quality.',
  'trace the development of the copyist\'s apprenticeship system over three centuries.',
  'demonstrate that patrons of the period had little interest in the paintings they commissioned.'],
 'The passage sets the modern implication of reproduction against the contracts, and concludes that judging copies as failed originals uses a standard nobody involved had heard of.',
 'Dullness is conceded in one line rather than argued. The apprenticeship is mentioned once, and patrons are shown to be highly engaged.')
q('AR062','ARP8','P8','Detail','act_r_kid',2,
 'According to the passage, patrons commissioning a copy routinely:',
 ['specified changes to the painting being copied.',
  'required the copyist to work in the original artist\'s workshop.',
  'paid less than they would have paid for an original composition.',
  'insisted that the copy be indistinguishable from its source.'],
 'The third paragraph says patrons routinely specified changes and gives three examples.',
 'The workshop requirement and the pricing are not mentioned, and indistinguishability is the opposite of what the contracts show.')
q('AR063','ARP8','P8','Word meaning','act_r_cs',3,
 'As used in the passage, the word liberties most nearly refers to:',
 ['departures from the source that a copyist took without being asked.',
  'freedoms granted to copyists by the guilds that licensed them.',
  'choices a patron was entitled to make about a finished work.',
  'privileges enjoyed by workshops that employed a recognised master.'],
 'The sentence says the changes were not liberties taken by a careless hand but the commission itself, so a liberty is an unrequested departure.',
 'Guild freedoms, patron entitlements and workshop privileges are all senses the word could carry but none fits the contrast being drawn.')
q('AR064','ARP8','P8','Text structure','act_r_cs',3,
 'The passage is organised primarily by:',
 ['naming a modern assumption, setting historical evidence against it, and identifying where the assumption came from.',
  'describing a profession, listing its techniques, and assessing the quality of its output.',
  'presenting two competing theories and arguing for one of them.',
  'narrating a change in taste and explaining what caused it.'],
 'The order is exactly that: the implication carried by reproduction, the contracts, the workshop practice, and the observation that the single object idea is two centuries old.',
 'Techniques are not listed, no two theories compete, and no change in taste is narrated.')
q('AR065','ARP8','P8','Author perspective','act_r_cs',4,
 'The author includes the statement that most copies are dull mainly to:',
 ['prevent the argument from being read as a claim about the quality of the copies.',
  'concede that the contracts cannot be taken at face value.',
  'suggest that the copyists lacked the training their masters had.',
  'explain why so few copies survive from the period.'],
 'It is immediately followed by the point that judging them as failed originals is the wrong standard. The concession keeps the argument about standards rather than about merit.',
 'The contracts are relied on rather than doubted. Training and survival are not the subject.')
q('AR066','ARP8','P8','Inference','act_r_kid',4,
 'It can reasonably be inferred that the author regards the idea that a painting is the trace of one person\'s unrepeatable act as:',
 ['a relatively recent notion that is applied to periods it does not fit.',
  'a standard that copyists of the period tried and failed to meet.',
  'an idea invented by workshops to justify repeating successful compositions.',
  'the only defensible basis for valuing a painting today.'],
 'The passage calls it roughly two centuries old and says we have projected it backwards onto three centuries that did not hold it.',
 'The copyists had not heard of it. Workshops repeated compositions for success rather than to justify anything, and the author offers no verdict on its defensibility now.')
q('AR067','ARP8','P8','Integration of ideas','act_r_iki',4,
 'The three examples of patron instructions are included in order to:',
 ['show that changes were part of the commission rather than errors of execution.',
  'illustrate the range of subjects that copyists were asked to paint.',
  'suggest that patrons had poor judgement about composition.',
  'demonstrate how closely copyists were supervised during their work.'],
 'They come immediately before the statement that these were the commission rather than liberties taken by a careless hand.',
 'Subject range, patron judgement and supervision are not what the examples are used to establish.')
q('AR068','ARP8','P8','Integration of ideas','act_r_iki',5,
 'Which situation is most analogous to the relationship the passage describes between a copy and its source?',
 ['A theatre company staging a play with cuts and a changed setting that the commissioning festival requested.',
  'A student copying a drawing in a gallery in order to learn the older artist\'s technique.',
  'A printer producing identical impressions of an engraving from a single plate.',
  'A forger painting in an older style and signing another artist\'s name.'],
 'The staging stands in a negotiated relation to an existing work, with the alterations specified by whoever commissioned it. That is the contract relation the passage describes.',
 'The student copies to learn rather than on commission. The printer produces identical impressions, which is the fidelity model the passage rejects. The forger conceals rather than negotiates.')
q('AR069','ARP8','P8','Detail','act_r_kid',2,
 'The passage states that within a workshop:',
 ['the master\'s hand appeared in some passages of a painting and not others.',
  'every painting was completed by a single identified artist.',
  'copies were produced only after the original had been sold.',
  'apprentices were forbidden to alter a composition in any way.'],
 'The fourth paragraph says a workshop produced paintings and the master\'s hand appeared in some passages and not others.',
 'Single authorship is the idea the passage says did not apply. Timing of sale and a prohibition on alteration are not stated.')
q('AR070','ARP8','P8','Integration of ideas','act_r_iki',4,
 'The passage suggests that the word reproduction is misleading when applied to these paintings because it:',
 ['implies that fidelity to the source was the only thing being judged.',
  'suggests that the copies were produced by mechanical means.',
  'indicates that the copies were made without the source artist\'s permission.',
  'implies that the copies were intended for a wider audience than the originals.'],
 'The first paragraph says the word carries the implication that the copy is a lesser thing whose only merit is fidelity, which the contracts contradict.',
 'Mechanical production, permission and audience are not the implication the passage identifies.')

# ---- ARP9 natural science ------------------------------------------------------------
q('AR071','ARP9','P9','Central idea','act_r_kid',3,
 'The main idea of the passage is that:',
 ['ice cores give a direct record of past air, but reading it requires a correction that must itself be measured.',
  'ice cores cannot be dated accurately below a depth of two kilometres.',
  'the carbon dioxide measured in ice cores is systematically lower than the true past value.',
  'central Antarctica is a poor location for extracting reliable ice cores.'],
 'The passage sets out the direct record, introduces the closure delay as a complication, and says the complication requires a measured correction rather than making the cores unreliable.',
 'Dating below two kilometres changes method rather than becoming impossible. No systematic bias in the measurement is claimed, and central Antarctica is an example rather than a verdict.')
q('AR072','ARP9','P9','Detail','act_r_kid',2,
 'According to the passage, in central Antarctica the difference in age between a bubble and the ice around it can exceed:',
 ['six thousand years.',
  'six hundred years.',
  'sixty thousand years.',
  'two kilometres of accumulated layers.'],
 'The third paragraph gives the figure as exceeding six thousand years where snowfall is light.',
 'Six hundred and sixty thousand misstate the figure, and the last option names a depth rather than an interval.')
q('AR073','ARP9','P9','Word meaning','act_r_cs',3,
 'As used in the passage, the phrase no model in between most nearly emphasises that the measurement:',
 ['is of the past atmosphere itself rather than of something standing in for it.',
  'has not been adjusted for the effects of compression at depth.',
  'can be performed without specialised laboratory equipment.',
  'agrees with predictions made by climate simulations.'],
 'The sentence says the cores are not a proxy for past air, they are past air, and the phrase reinforces that directness.',
 'Compression, equipment and agreement with simulations are all separate matters the phrase does not address.')
q('AR074','ARP9','P9','Text structure','act_r_cs',4,
 'The third paragraph relates to the second paragraph by:',
 ['introducing a complication that qualifies the directness the second paragraph claimed.',
  'providing the experimental evidence for the claim the second paragraph made.',
  'restating the second paragraph\'s point in more technical language.',
  'describing an alternative method that avoids the second paragraph\'s difficulty.'],
 'The second paragraph says the bubble is past air with no model in between. The third opens with a complication and explains that the air is younger than the ice.',
 'It is not evidence, not a restatement, and no alternative method is offered.')
q('AR075','ARP9','P9','Inference','act_r_kid',4,
 'It can reasonably be inferred that the age gap between a bubble and its surrounding ice would be smallest where:',
 ['snowfall is heavy, so pores close sooner.',
  'the ice is thickest, so compression is greatest.',
  'the core is drilled closest to the coast.',
  'temperatures are lowest year round.'],
 'The passage says the gap depends on temperature and snowfall rate and that it is largest where snowfall is light, so heavy snowfall closes pores sooner and shrinks the gap.',
 'Thickness and drilling location are not given as determinants, and low temperature is associated with the light snowfall that widens the gap.')
q('AR076','ARP9','P9','Author perspective','act_r_cs',4,
 'The author\'s tone in the final sentence is best described as:',
 ['pointed, in identifying a misunderstanding and where it comes from.',
  'apologetic, in acknowledging a defect in the method.',
  'uncertain, in leaving open whether the correction is reliable.',
  'enthusiastic, in praising the precision of the technique.'],
 'The sentence says a great deal of misunderstanding comes from people who wanted a reading they could take without knowing any of this. It names the source of the error.',
 'Nothing is apologised for, the correction is called measured rather than doubtful, and the sentence is not praise.')
q('AR077','ARP9','P9','Integration of ideas','act_r_iki',4,
 'The passage indicates that the correction for the age gap is credible because it is:',
 ['measured directly in modern snow and calibrated against independently dated periods.',
  'small enough that it makes no practical difference to the result.',
  'derived from the same climate models the cores are used to test.',
  'applied uniformly to every core regardless of where it was drilled.'],
 'The final paragraph says the closure depth can be observed directly in modern snow and the relationship calibrated against periods with an independent date.',
 'The gap is large, not small. Using the models under test would be circular, and the correction varies with conditions rather than being uniform.')
q('AR078','ARP9','P9','Integration of ideas','act_r_iki',5,
 'Which of the following best captures the relationship between the passage\'s second and fourth paragraphs?',
 ['The fourth preserves the second\'s claim by showing that the obstacle to it is itself measurable.',
  'The fourth withdraws the second\'s claim in light of the difficulty raised between them.',
  'The fourth extends the second\'s claim to a wider range of gases.',
  'The fourth explains why the second\'s claim holds only for shallow cores.'],
 'The second claims a direct record, the third raises the closure gap, and the fourth says this does not make the cores unreliable but requires a correction that is measured rather than assumed.',
 'Nothing is withdrawn or extended, and no depth restriction is introduced.')
q('AR079','ARP9','P9','Detail','act_r_kid',2,
 'The passage states that snow at the surface:',
 ['remains porous for decades or centuries, allowing air to circulate.',
  'seals immediately, trapping air from the year it fell.',
  'contains no measurable carbon dioxide until it is compressed.',
  'must be removed before a usable core can be extracted.'],
 'The third paragraph says snow does not become ice at the surface, stays porous for decades and sometimes centuries, and air circulates freely until pores close.',
 'Immediate sealing is what the paragraph denies, and the other two are not stated.')
q('AR080','ARP9','P9','Integration of ideas','act_r_iki',4,
 'Based on the passage, a researcher who reported a carbon dioxide value from a deep Antarctic core without adjusting for pore closure would most likely have:',
 ['attributed the measurement to a year considerably earlier than the air actually dates from.',
  'overstated the concentration of carbon dioxide in the sample.',
  'produced a value that no independent method could check.',
  'been unable to date the surrounding ice layers at all.'],
 'The air is younger than the ice around it. Dating the air by the ice therefore places it too early, by up to six thousand years in central Antarctica.',
 'The concentration itself is unaffected, independent checks are described as available, and dating the ice is possible by other means.')

print('%d items total' % len(I))

# Four more, two Craft and Structure and two Integration. The existing bank holds 18 Key
# Ideas, 11 Craft and 11 Integration; the forty above would have left the second and
# third at 23, just under the review bot's threshold of 25. The alternative was to
# relabel four inference items as Craft, which would have cleared the number by
# misreporting what the items test. Writing four more is the honest way to move it.
q('AR081','ARP6','P6','Text structure','act_r_cs',3,
 'The passage is told from the point of view of:',
 ['an adult recalling childhood Saturdays and interpreting them in the light of later understanding.',
  'a child describing the father\'s work as it happens.',
  'an observer outside the family who knew the father professionally.',
  'the father himself, addressing a grown child.'],
 'The narrator says the reason was obvious and that understanding came at thirty, and closes in the present tense owning a piano. The recall is retrospective and interpreted.',
 'The Saturdays are recalled rather than narrated as they happen, the narrator is the child rather than an outsider, and the father is quoted rather than speaking.')
q('AR082','ARP7','P7','Word meaning','act_r_cs',3,
 'As used in the passage, the word elasticity most nearly refers to:',
 ['how much one quantity changes in response to a change in another.',
  'the capacity of a road surface to withstand heavy loads.',
  'the willingness of drivers to alter their routes at short notice.',
  'the range of speeds a road is designed to accommodate.'],
 'The passage gives the figure as close to one and then explains it as a ten percent capacity increase producing roughly ten percent more travel, which is a ratio of responses.',
 'Road surface, route flexibility and design speed are all traffic topics the word does not mean here.')
q('AR083','ARP8','P8','Integration of ideas','act_r_iki',4,
 'The passage suggests that a museum label describing a painted copy as a reproduction would be:',
 ['imposing a standard of fidelity that the work was not made to meet.',
  'accurate, since the copy was produced from an existing composition.',
  'misleading only if the copy were of higher quality than its source.',
  'appropriate provided the label also named the original artist.'],
 'The first paragraph says reproduction implies the copy is a lesser thing whose only merit is fidelity, and the contracts show fidelity was negotiable.',
 'Accuracy is what the passage disputes. Quality and attribution are not the grounds of the objection.')
q('AR084','ARP9','P9','Integration of ideas','act_r_iki',4,
 'The passage\'s treatment of the pore closure problem is best described as:',
 ['presenting it as a reason to correct the measurement rather than to distrust it.',
  'presenting it as a flaw that limits how far back cores can be read.',
  'presenting it as a difficulty that only affects cores from central Antarctica.',
  'presenting it as a problem that later drilling techniques have removed.'],
 'The fourth paragraph opens by saying this does not make the cores unreliable, it makes them require a correction, and then explains how the correction is measured.',
 'No depth limit is set, central Antarctica is the extreme case rather than the only one, and no technique is said to have removed it.')

# -------------------------------------------------------------------------------------
HEADER = '''// bank_act_reading2.js - Original ACT Reading items AR041-AR080.
//
// Generated by src/mk_bank_act_reading2.py. Edit that file, not this one.
//
// The second ACT Reading bank. With the LSAT done, ACT Reading was the thinnest passage
// based section left: 40 items across three skills, with two of them holding 11 each.
// These 40 items take it to 80 and every skill past the review bot's threshold of 25.
//
// Four passages, one in each genre the ACT uses and in the order it uses them: literary
// narrative, social science, humanities, natural science. Ten questions each, which is
// the real section's shape, and four choices rather than five.
//
// The corrections every hand written bank needs are in src/bank_emit.py: keys permuted
// off position A and the index computed (INC-0039), seeded from crc32 rather than hash
// (INC-0003), strings JSON escaped (INC-0001), ids single quoted so the build can count
// them (INC-0059). Three extension passes rather than one, because correcting a length
// tell moves it one rank over (INC-0062).
'''

E.permute(I)

# First pass. Same cause as every other hand written bank: the key is the most carefully
# qualified option, so it is long. Each clause states the omission that makes the option
# wrong or carries its error one step further.
EXTEND = {
 'AR041': ('technical differences between tuning by ear and tuning electronically', ' that the father described'),
 'AR042': ('the speed with which he could complete a tuning', ' compared with other tuners'),
 'AR043': ('built to be useful rather than beautiful', ' by whoever made it'),
 'AR044': ("the narrator's musical ability with the father's", ' at the same age'),
 'AR045': ('amused by convictions the narrator regards as eccentric', ' but harmless'),
 'AR046': ('the woman would not have been able to afford his usual fee', ' for two hours of work'),
 'AR047': ('poorly made pianos require more frequent tuning', ' than well made ones do'),
 'AR048': ('An electronic tuner produces a result inferior to one produced by ear', ' in the hands of a skilled tuner'),
 'AR049': ('an electronic tuner he had bought late in his career', ' to save time'),
 'AR050': ('A professional should not profit from work performed on a personal acquaintance', ' or a neighbour'),
 'AR051': ('measurements of traffic taken from mobile phones are more accurate', ' than counts taken by hand at intersections'),
 'AR052': ('well below one, so travel rises more slowly than capacity', ' does'),
 'AR053': ('establish that engineers in the 1930s were the first to propose induced demand', ' as an explanation'),
 'AR054': ('redistribute among neighbouring routes', ' in the same network'),
 'AR055': ('opposed to it on the ground that congestion always returns', ' to its previous level'),
 'AR056': ('already be as congested as the road it was built to relieve', ' was before it opened'),
 'AR057': ('Surrounding streets can absorb any volume displaced from a closed motorway', ' without additional delay'),
 'AR058': ('both become less efficient as more people use them', ' at the same time'),
 'AR059': ('sensors embedded in the road surface at fixed intervals', ' along each route'),
 'AR060': ('Some cities that removed motorways saw traffic increase on parallel routes', ' nearby'),
 'AR061': ('most painted copies produced before photography were of poor quality', ' by any standard'),
 'AR062': ("required the copyist to work in the original artist's workshop", ' while making the copy'),
 'AR063': ('freedoms granted to copyists by the guilds that licensed them', ' to practise'),
 'AR064': ('describing a profession, listing its techniques, and assessing the quality of its output', ' over time'),
 'AR065': ('concede that the contracts cannot be taken at face value', ' as evidence of practice'),
 'AR066': ('a standard that copyists of the period tried and failed to meet', ' in their work'),
 'AR067': ('illustrate the range of subjects that copyists were asked to paint', ' for their patrons'),
 'AR068': ('A student copying a drawing in a gallery in order to learn the older artist\'s technique', ' by imitation'),
 'AR069': ('every painting was completed by a single identified artist', ' from beginning to end'),
 'AR070': ('suggests that the copies were produced by mechanical means', ' rather than by hand'),
 'AR071': ('ice cores cannot be dated accurately below a depth of two kilometres', ' by any method'),
 'AR072': ('six hundred years', ' at most'),
 'AR073': ('has not been adjusted for the effects of compression at depth', ' in the core'),
 'AR074': ('providing the experimental evidence for the claim the second paragraph made', ' about past air'),
 'AR075': ('the ice is thickest, so compression is greatest', ' at that depth'),
 'AR076': ('apologetic, in acknowledging a defect in the method', ' that cannot be corrected'),
 'AR077': ('small enough that it makes no practical difference to the result', ' being reported'),
 'AR078': ("The fourth withdraws the second's claim in light of the difficulty", ' raised between them'),
 'AR079': ('seals immediately, trapping air from the year it fell', ' on the surface'),
 'AR080': ('overstated the concentration of carbon dioxide in the sample', ' that was analysed'),
}
E.extend(I, EXTEND)

# Second pass, on the subset that lands at second longest after the first.
EXTEND2 = {
 'AR041': ('describe the decline of piano tuning as a profession', ' over the four decades the father worked'),
 'AR044': ('suggest that the narrator regrets not having owned a piano', ' earlier in life'),
 'AR046': ('the instrument was too damaged for the tuning to hold', ' for any length of time'),
 'AR048': ('A tuner should decline work on instruments that are rarely played', ' by their owners'),
 'AR050': ('Equipment owned by a tradesperson should be limited to what the trade requires', ' for daily work'),
 'AR051': ('cities that remove urban motorways experience less disruption', ' than planners predict beforehand'),
 'AR053': ('argue that clipboard counts were unreliable', ' and should never have been used for planning'),
 'AR055': ('supportive of it because additional trips have value', ' to the people who make them'),
 'AR057': ('Removing a motorway reduces the total number of vehicles registered', ' in the city concerned'),
 'AR061': ("trace the development of the copyist's apprenticeship system", ' over the three centuries in question'),
 'AR064': ('presenting two competing theories and arguing for one of them', ' at length'),
 'AR066': ('an idea invented by workshops to justify repeating successful compositions', ' for different patrons'),
 'AR068': ('A forger painting in an older style and signing another artist\'s name', ' to the finished work'),
 'AR071': ('the carbon dioxide measured in ice cores is systematically lower', ' than the true value for that year'),
 'AR074': ("restating the second paragraph's point in more technical language", ' for specialists'),
 'AR076': ('uncertain, in leaving open whether the correction is reliable', ' enough to depend on'),
 'AR078': ("The fourth extends the second's claim to a wider range of gases", ' trapped in the same bubbles'),
 'AR080': ('produced a value that no independent method could check', ' against another record'),
}
E.extend(I, EXTEND2, 'EXTEND2')

E.measure(I)
PVAR = {'P6': 'AR_P6', 'P7': 'AR_P7', 'P8': 'AR_P8', 'P9': 'AR_P9'}
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_act_reading2.js',
        HEADER, [('AR_P6', P6), ('AR_P7', P7), ('AR_P8', P8), ('AR_P9', P9)],
        I, 'BANK_ACT_READING2', passage_var=PVAR, group_key='passageId')
