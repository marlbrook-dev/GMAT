#!/usr/bin/env python3
"""Emit src/bank_verbal9.js.

Run: python3 src/mk_bank_gmat_rc.py src/bank_verbal9.js

The flagship exam's thinnest skills. GMAT Focus Verbal has two reading skills in GMAC's
own score report taxonomy, Identify Stated Idea and Identify Inferred Idea, and the bank
held 32 and 39 items against 111 to 127 for every other skill on the exam. Eleven
passages carried all of it. These 144 items across 24 new passages take v_st to 104 and
v_inf to 111, which puts reading in the same band as everything else.

Nothing here is tagged v_ac. Analysis / Critique is already the largest verbal skill at
124, and a reading bank that grew it further would move the imbalance rather than close
it. The two reading skills are wider than they sound: GMAC files main idea, primary
purpose, organisation and stated detail under Identify Stated Idea, and inference,
application and author attitude under Identify Inferred Idea, so six questions on one
passage split three and three without repeating a question shape.

Passages are named constants rather than inlined per item. The existing GMAT verbal banks
store the same paragraph on every question that shares it, which is how bank_verbal.js
came to hold one passage five times.

Machinery is in src/bank_emit.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

P = {}

P['A'] = ("Credit rating agencies are paid by the issuers whose securities they rate, an "
"arrangement that invites the obvious objection: a firm shopping for a rating will buy "
"from whoever offers the highest one. The arrangement was not always the rule. Until the "
"early 1970s the agencies sold their judgments to investors by subscription, and the "
"switch is usually explained by the photocopier, which made it impossible to charge for "
"a document that a single subscriber could reproduce for everyone.\n\n"
"The explanation is incomplete. Subscription revenue was falling, but the agencies also "
"acquired something in the same decade that made issuers willing to pay: regulatory "
"force. Once bank capital rules and pension mandates were written in terms of ratings, a "
"bond without one was unsalable to a large part of the market, and the issuer needed the "
"rating more than any investor did. Photocopying explains why the old business model "
"weakened; it does not explain why a new payer appeared with an inelastic demand.\n\n"
"The distinction matters for reform. If the problem is that information is easy to copy, "
"the remedy lies in how the product is sold. If the problem is that regulation created a "
"captive buyer, then no change in billing arrangements will help, because the conflict "
"survives any fee structure that leaves ratings embedded in the rules. Proposals to "
"rotate agencies among issuers, or to have a public body assign them, address the second "
"diagnosis. Proposals to return to investor subscription address the first, and would "
"reproduce the conflict within a year if the mandates stayed in place.")

P['B'] = ("Coffee was grown under shade trees for most of its commercial history. Beginning "
"in the 1970s, breeding programmes produced varieties that tolerate full sun, and "
"plantations across Central America cleared their canopy to plant them. Yields roughly "
"doubled. The agronomic literature of the period treated the canopy as a constraint that "
"technology had removed.\n\n"
"Two costs surfaced later. The first was chemical: sun grown coffee depletes soil faster "
"and admits more weeds, so fertiliser and herbicide inputs rose to a level that consumed "
"much of the additional revenue on smaller farms. The second was epidemiological. Coffee "
"leaf rust spreads fastest in warm, humid, still air, and a closed canopy is cooler by "
"several degrees than an open field at midday. When the rust epidemic of 2012 moved "
"through the region, losses on sun grown plots ran well ahead of losses on shaded ones "
"at comparable altitudes.\n\n"
"It would be a mistake to read this as vindication of the older practice. Shade suppresses "
"yield, and a farm that keeps its canopy is buying insurance with a premium it pays every "
"year whether the rust arrives or not. What the episode revealed is narrower and more "
"useful: the canopy was performing a function nobody had priced, and the varieties bred to "
"do without it were evaluated on a single output measure over a period that happened to "
"contain no epidemic. The failure was not of the breeding programme but of the trial "
"design, which asked how much coffee a plant yields rather than what the system it sits "
"in was doing.")

P['C'] = ("The Hanseatic League, a confederation of northern European merchant towns that "
"dominated Baltic trade from the thirteenth century, had no standing army, no common "
"treasury and no court with power to compel a member. Historians have long asked how it "
"enforced anything. The usual answer is reputation: a merchant who cheated would not trade "
"again. That answer is inadequate on its own, because reputation works only where the "
"injured party and future counterparties share information, and the League's ports were "
"weeks apart by sail.\n\n"
"The mechanism that did the work appears to have been collective, not individual. When a "
"town's authorities wronged a Hanseatic merchant, the League's response was to embargo the "
"town, and every member was expected to withdraw. The threat was credible because the "
"cost of compliance was low for most members and the cost of defection was expulsion, "
"which carried the loss of trading privileges in every other member port. A merchant "
"deciding whether to honour the embargo was not weighing one lost relationship against a "
"gain but weighing the entire network against it.\n\n"
"This reading has an implication that the reputation account lacks. Collective punishment "
"requires agreement on what counts as a violation, which is why the League's surviving "
"records consist so largely of assembly minutes rather than contracts. The institution "
"whose absence puzzles historians, a court, was in effect replaced by a legislature, and "
"the effort went into defining the offence rather than trying the offender.")

P['D'] = ("Almost every class of antibiotic in clinical use was discovered between 1940 and "
"1962, most of them by screening soil bacteria for compounds that killed other bacteria. "
"The method then stopped producing. Pharmaceutical firms describe the subsequent gap as a "
"market failure, and by their accounting it is one: an antibiotic is taken for ten days "
"rather than for life, and a new one is held in reserve precisely so that it is not sold.\n\n"
"The scientific account is different and less often heard. Soil screening works by growing "
"bacteria in a dish, and roughly ninety nine percent of soil species will not grow in one. "
"The screens of the golden age were sampling the same small culturable fraction over and "
"over, which is why they returned the same compounds with increasing frequency and finally "
"returned nothing new. The pipeline did not dry up because the chemistry was exhausted; it "
"dried up because the sampling method had reached the edge of what it could reach.\n\n"
"The two accounts recommend different interventions. If the barrier is economic, the remedy "
"is a prize, a subscription payment, or an extended exclusivity period, and these have been "
"tried with modest results. If the barrier is methodological, the remedy is a way to culture "
"the uncultured, and the isolation chip, which grows soil organisms in situ inside a "
"diffusion chamber, produced a novel antibiotic class in 2015 after a gap of nearly thirty "
"years. Neither account is wrong. But a market incentive applied to an exhausted method buys "
"more searching in the same place.")

P['E'] = ("The diversified conglomerate is out of fashion, and the case against it is "
"familiar: investors can diversify for themselves at lower cost, so a firm that does it on "
"their behalf destroys value and trades at a discount to the sum of its parts. The empirical "
"literature of the 1990s measured that discount repeatedly and put it at ten to fifteen "
"percent.\n\n"
"A later strand of work questioned what the discount measures. Firms do not become "
"conglomerates at random; they acquire divisions, and the divisions they acquire tend to be "
"ones that were already struggling. Comparing a conglomerate's segments with freestanding "
"firms in the same industries therefore compares a portfolio of rescued businesses with a "
"portfolio of average ones. When researchers tracked segments from before acquisition, much "
"of the discount was present beforehand.\n\n"
"This does not rehabilitate the form. It relocates the question. The interesting comparison "
"is not between a conglomerate and a set of standalone firms but between a conglomerate's "
"internal capital market and the external one it substitutes for. Internal allocation has a "
"real advantage where external lenders cannot verify quality, which is why conglomerates "
"remain common in economies with shallow capital markets and rare in the United States. It "
"has a real disadvantage where divisional managers lobby, since the headquarters that "
"reallocates cash is also the audience for that lobbying. Which effect dominates is an "
"empirical question about a particular economy at a particular time, and the answer has "
"changed at least once within living memory.")

P['F'] = ("When a large whale dies and sinks, its carcass supports a succession of "
"communities on the sea floor for decades. Scavengers strip the soft tissue within months. "
"A second stage, lasting a year or two, is dominated by organisms that colonise the "
"enriched sediment around the bones. The third and longest stage depends on the bones "
"themselves: they are rich in lipids, and bacteria metabolising those lipids produce "
"sulphide, which supports the same chemosynthetic animals found at hydrothermal vents.\n\n"
"The resemblance to vent communities prompted a hypothesis that whale falls serve as "
"stepping stones, allowing vent species to disperse between widely separated vent fields "
"across otherwise uninhabitable abyssal plain. The hypothesis is attractive and has been "
"difficult to test. Genetic work has since shown that most of the chemosynthetic species "
"on whale falls are not the species found at vents but close relatives specialised to "
"bones, which weakens the stepping stone reading considerably.\n\n"
"It also raises a question the original hypothesis obscured. Whale falls are recent in "
"evolutionary terms: large whales appeared perhaps thirty million years ago, and the "
"bone specialists must have come from somewhere. The most likely source is the same "
"sulphide rich habitats that vents represent, which means the dispersal ran the other "
"way. Rather than whale falls carrying vent fauna across the abyss, vents appear to have "
"supplied the ancestors of a fauna that now lives nowhere else.")

P['G'] = ("Between 1935 and 1943 the Federal Writers' Project employed several thousand "
"unemployed writers to produce guidebooks to every state. The programme is usually "
"discussed as relief spending, and the guides as a byproduct. The guides themselves suggest "
"a different emphasis. They were compiled by people with no training in the subjects they "
"covered, working from local interviews and county records, and the result is a body of "
"documentation of ordinary American life in the 1930s that no other source approaches in "
"breadth.\n\n"
"Whether this was intended is disputed. The programme's national director wrote about "
"cultural nationalism and about giving the country a portrait of itself. The regional "
"directors wrote about payrolls. Both were telling the truth about their own positions, and "
"the surviving correspondence shows the two purposes in constant tension over questions such "
"as whether a state office could refuse an unqualified applicant sent by the relief rolls.\n\n"
"What the guides demonstrate is less a matter of intent than of structure. A programme that "
"had to employ whoever was unemployed in a given county could not concentrate its writers "
"where the literary talent was, and the geographic spread that this forced on it is exactly "
"what makes the collection valuable now. The same constraint that made the guides uneven as "
"prose made them comprehensive as record. Patronage designed for quality would have produced "
"a shelf of better books about fewer places.")

P['H'] = ("Groundwater is reported in national accounts, when it is reported at all, as a "
"flow: so many cubic metres pumped in a year. Treating it as a flow is an accounting choice "
"with consequences, because an aquifer is a stock, and a stock that is drawn down faster "
"than it recharges is being liquidated rather than harvested. A farm economy that draws its "
"irrigation from a depleting aquifer records rising output and no offsetting entry.\n\n"
"Attempts to correct this run into a measurement problem that is genuinely hard. The volume "
"of water in an aquifer is not directly observable; it is inferred from well levels, from "
"the rate at which the land surface subsides, and since 2002 from satellite gravimetry, "
"which detects the mass change that depletion causes. The three methods disagree, sometimes "
"by factors rather than percentages, and each is biased in a direction the others are not.\n\n"
"The disagreement is often cited as a reason to wait for better data before revising the "
"accounts. That inference does not follow. The current treatment implicitly assigns the "
"stock a depletion rate of zero, which is not an estimate under uncertainty but a value "
"every method rejects. A figure known only to within a factor of two is more informative "
"than a figure known to be wrong, and the choice between them is not a choice between "
"precision and imprecision but between a wide interval and a point outside it.")

P['I'] = ("The standardisation of railway track gauge in Britain is often presented as a "
"triumph of the better design. Two gauges competed into the 1840s: the narrow gauge that "
"most companies had adopted by inheritance from colliery tramways, and Brunel's broad "
"gauge, which was faster, steadier and allowed larger locomotives. Parliament chose the "
"narrow gauge in 1846, and the broad gauge was gone by 1892.\n\n"
"The engineering merits ran the other way, and the outcome is usually explained by the "
"installed base: by 1846 there were roughly 1900 miles of narrow gauge track and about 270 "
"of broad, so conversion costs decided it. This is true but proves less than it appears to. "
"A network's value to a user grows with the number of points it reaches, so the larger "
"system was more valuable per mile as well as larger, and the gap would have widened at any "
"relative cost of conversion. The installed base was not merely a sunk cost to be weighed "
"against the benefits of switching; it was itself the benefit.\n\n"
"The case is cited in economics as a standard example of lock in to an inferior technology, "
"and it does show that. It is less often noticed that the parliamentary commissioners said "
"so at the time. Their report concedes the broad gauge's superiority in terms that leave no "
"ambiguity, and recommends the narrow gauge anyway on grounds of uniformity. Lock in here "
"was not a market failing to see what an observer could see; it was a decision taken with "
"the tradeoff in full view.")

P['J'] = ("Naked mole rats live in colonies with a single breeding female, sterile workers "
"and a division of labour, a social organisation otherwise found mainly among insects. "
"Explaining eusociality in insects is made easier by their unusual genetics: in bees, ants "
"and wasps, sisters share three quarters of their genes rather than half, so a worker may "
"propagate more of her genome by raising sisters than by breeding. Mole rats are ordinary "
"mammals, and the explanation is unavailable.\n\n"
"Two alternatives have been proposed. The first is ecological: mole rats eat underground "
"tubers that are scattered unpredictably through hard, dry soil, and locating one requires "
"more tunnelling than a lone animal can perform. The second is demographic: dispersal in "
"such soil is close to suicidal, so a young animal's realistic options are to stay or to "
"die, which makes the cost of remaining a helper low rather than the benefit high.\n\n"
"These are usually presented as rivals and are better read as complements operating on "
"different sides of the same ledger. What deserves more attention is that neither requires "
"the genetic asymmetry that the insect literature has treated as central. If eusociality "
"can arise twice in mammals, as it has, from ecology alone, then the haplodiploid "
"explanation may be describing a factor that makes the arrangement easier in insects rather "
"than one that makes it possible.")

P['K'] = ("Newspapers derived a large share of their revenue from classified advertising, "
"and the loss of that revenue to online listing sites is the standard account of their "
"decline. The account is right about the money and misleading about the mechanism. "
"Classified advertising was never profitable in isolation; it was profitable because it "
"shared a printing plant, a delivery fleet and a subscriber list with the news operation. "
"A bundle of that kind is stable only while no component can be supplied separately at "
"lower cost.\n\n"
"What the listing sites did was not to undercut the price of a classified advertisement, "
"though they did that too. It was to demonstrate that the advertisement did not need the "
"newspaper. A seller wanted to reach buyers, not readers, and the newspaper had been "
"selling access to buyers by selling access to readers because no cheaper route existed. "
"Once one did, the bundle came apart in the direction of whichever component had been "
"subsidising the other.\n\n"
"This suggests a general caution about cross subsidy as a business strategy. A firm that "
"funds an unprofitable product from a profitable one is often described as investing in the "
"former, and sometimes it is. But the arrangement also conceals which product the customer "
"is actually paying for, and the concealment is mutual: the firm may not know either. The "
"newspapers that responded to the loss of classifieds by cutting newsroom costs were acting "
"on a theory of their own business that the unbundling had just refuted.")

P['L'] = ("A tree adds one growth ring a year, and the ring is narrow in a bad year. "
"Because trees of the same species in the same region respond to the same weather, their "
"ring sequences match, and overlapping samples from living trees, old timber and buried "
"logs can be chained backwards to build a continuous record thousands of years long. The "
"technique dates a piece of wood to the calendar year.\n\n"
"Its value to archaeology is obvious and has a second application that is less obvious. "
"Large volcanic eruptions inject sulphate into the stratosphere and cool the hemisphere for "
"one to three years, which appears in tree rings as a narrow band across many sites at "
"once. Ice cores record the same eruptions as sulphate layers, but ice core chronologies "
"are built by counting annual layers and accumulate error with depth, running several years "
"adrift by the first millennium.\n\n"
"Matching the two records lets the ice core chronology be corrected against the tree ring "
"one, and the correction has revised the dates of several eruptions that historians had "
"used as fixed points. The awkward part is that some of those historians had dated the "
"eruptions from written accounts of unusual weather, and a few of the written accounts were "
"in turn used to check the ice cores. Untangling which record is independent of which has "
"occupied the field for two decades and is not finished.")

P['M'] = ("Craft guilds controlled apprenticeship in most European cities from the "
"thirteenth century to the eighteenth, and economic historians have long disagreed about "
"what they accomplished. One view holds that guilds were cartels: they restricted entry, "
"raised prices and resisted innovation, and their abolition was a precondition of "
"industrial growth. A second holds that they solved a contracting problem no market could "
"solve, since a master who trains an apprentice creates a competitor and has every reason "
"to teach badly.\n\n"
"The second view has the better of the specific evidence on training. Apprenticeship "
"contracts were enforced by guild courts, and the records show them enforcing obligations "
"in both directions, against masters who withheld instruction as well as apprentices who "
"left early. Cities without guilds do not show comparable institutions, and the skills "
"involved took years to transmit and could not be observed from outside.\n\n"
"The first view has the better of the aggregate evidence. Guild towns did grow more slowly, "
"and the correlation survives most attempts to explain it away. The two findings are "
"compatible if the training function and the cartel function were bundled in the same "
"institution, which is the reading the evidence best supports and the least satisfying one, "
"because it means the question of whether guilds were on balance beneficial cannot be "
"answered without knowing how much the training was worth. That figure is not recoverable "
"from the records that survive.")

P['N'] = ("Tidal power is the most predictable renewable resource: the tides are driven by "
"orbital mechanics and can be forecast for centuries. Wind and solar output cannot be "
"forecast reliably a week ahead. Predictability is worth a great deal to a grid operator, "
"who must hold reserve capacity against forecast error, and tidal generation is often "
"promoted on this basis.\n\n"
"Predictable is not the same as steady. A tidal stream turbine produces nothing at slack "
"water, which occurs four times a day, and its output over a day is a sequence of pulses. "
"Across a month the pulses vary again with the spring and neap cycle, so a tidal plant "
"delivers perhaps twice as much energy in a spring week as in a neap one. None of this is a "
"forecasting problem, and all of it is a matching problem: the generation profile is known "
"in advance and does not resemble the demand profile.\n\n"
"The usual response is that sites with different tidal phases can be combined to smooth the "
"aggregate. This works in principle and is limited in practice by geography, since the "
"phase of the tide is set by the shape of the coast and the high energy sites in any one "
"country tend to share a basin and therefore a phase. The advantage of predictability is "
"real but narrower than the promotional literature suggests: it reduces the reserve a "
"system must hold against surprise without reducing the storage it must hold against "
"a shortfall it can see coming.")

P['O'] = ("Manufacturers hold warranty data that is unusually informative about product "
"quality: a claim records a failure, its date, the unit, and often the component. Firms "
"treat the data as a cost record. Analysts have argued for treating it as a leading "
"indicator, on the reasoning that a rise in claim rates precedes the reputational damage "
"and recall expense that follow.\n\n"
"The reasoning is sound and the data is harder to use than it appears. A claim is filed "
"only if a customer notices a fault, judges it worth the trouble, and is still inside the "
"coverage period, so the claim rate is a product of the failure rate and a reporting rate "
"that varies by market, by channel and by how much the product cost. A model sold mainly "
"through dealers who handle the paperwork will show a higher claim rate than an identical "
"model sold direct, and the difference says nothing about the units.\n\n"
"This is not an argument against using the data but against using it in levels. The "
"reporting rate for a given product in a given market changes slowly, while a genuine "
"manufacturing problem appears as a step. Differencing removes most of the nuisance and "
"leaves the signal, at the cost of detecting only changes rather than states. Firms that "
"have tried to rank products by warranty cost have generally ranked their distribution "
"arrangements instead.")

P['P'] = ("Domesticated animals of unrelated species share a set of traits that wild "
"populations lack: floppy ears, shortened muzzles, patchy coats, smaller brains, reduced "
"reactivity to humans and, in many species, breeding outside the ancestral season. The "
"cluster is old news and the explanation is not. Selective breeding for tameness should "
"produce tameness, and there is no obvious reason it should produce white patches.\n\n"
"A long running experiment on silver foxes, begun in 1959 and selecting on nothing but "
"willingness to approach a human hand, produced most of the cluster within forty "
"generations. Whatever links the traits therefore lies inside the animals rather than in "
"anything the breeders were doing. The leading candidate is the neural crest, a population "
"of embryonic cells that migrates through the developing body and contributes to the "
"adrenal glands, parts of the skull and jaw, the ear cartilage and the pigment cells. A "
"mild deficit in neural crest cell migration would reduce adrenal output, which is what "
"tameness largely consists of, and would produce the rest as side effects.\n\n"
"The hypothesis explains the cluster with one mechanism and is not yet established. Its "
"strongest test would be a domesticated lineage that shows tameness without the "
"accompanying traits, which would require the traits to be separable and would sink the "
"account. No such lineage has been reported, though the search has not been systematic and "
"absence of a report in a literature that is not looking is weak evidence.")

P['Q'] = ("Vernacular building traditions are frequently praised for climatic intelligence: "
"the thick walls and small windows of hot dry regions, the deep eaves and raised floors of "
"hot wet ones, the compact plans of cold ones. The praise is deserved and the usual "
"explanation for it is wrong. Vernacular forms are not the product of accumulated wisdom "
"about thermal performance, because the builders had no way to measure thermal "
"performance and no vocabulary in which to record a finding about it.\n\n"
"What they had was material and a constraint. A tradition that builds in rammed earth "
"produces thick walls because thin ones fall down, and thick earth walls happen to buffer "
"a daily temperature swing. A tradition in a wet climate builds a steep roof to shed water "
"and gets a ventilated cavity as a consequence. The climatic performance is real and is "
"largely a side effect of solving a structural problem with the material at hand, which "
"itself reflects the climate through what grows and what erodes.\n\n"
"The distinction is not pedantic. Architects who read vernacular form as encoded climate "
"knowledge have reproduced the form in new materials, and the performance does not follow: "
"a thin concrete wall with the same window ratio as a thick earth one buffers nothing. "
"Reading the form as a byproduct directs attention to the property that mattered, which "
"was thermal mass, and thermal mass can be supplied in other ways. The tradition is worth "
"studying for what its buildings do, not for what its builders knew.")

P['R'] = ("Flood insurance in the United States is provided largely by a federal programme "
"whose premiums have historically been set below actuarial cost. The subsidy is defended "
"as protecting existing homeowners from a charge they did not anticipate when they bought. "
"Its critics note the obvious perverse consequence: underpriced insurance encourages "
"building in floodplains, which raises the eventual claim.\n\n"
"Both sides of this argument treat the price signal as the mechanism, and the evidence for "
"that mechanism is weaker than either side assumes. Surveys of floodplain residents "
"consistently find that most substantially underestimate their flood risk and many are "
"unaware of the designation, which means the premium is not functioning as information "
"regardless of its level. A household that does not believe it is in a floodplain does not "
"read a low premium as a statement about the floodplain.\n\n"
"If that is right, raising premiums to actuarial levels would transfer money without "
"changing much behaviour, at least in the short run, and the case for doing it rests on "
"fiscal grounds rather than on incentives. The behavioural work points to a different "
"instrument: the risk designation itself, if it were disclosed at the point of sale in a "
"form buyers read, would do what the premium is supposed to do. That is a cheaper reform "
"and a less popular one, because a disclosure that changes behaviour changes property "
"values, and the constituency that resists actuarial pricing resists disclosure for the "
"same underlying reason.")

P['S'] = ("Ecologists conventionally describe a site by what lives there. An alternative "
"measure, introduced in the last two decades, describes it by what does not: the dark "
"diversity of a site is the set of species that belong to its regional pool and could "
"survive its conditions but are absent. A site with high observed richness and high dark "
"diversity is unsaturated; a site with high observed richness and low dark diversity "
"holds most of what it could hold.\n\n"
"The measure is useful because the two sites are indistinguishable on a species count and "
"very different for management. In the first, the limitation is dispersal, and connecting "
"the site to others will add species. In the second, the limitation is the site itself, "
"and connection will add nothing. Conservation budgets are routinely spent on corridors "
"in places where the second description applies.\n\n"
"The difficulty is that dark diversity is not observed but estimated, and the estimate "
"requires deciding which regional species could survive at the site, which is close to "
"the question the measure is meant to answer. Practitioners use species co-occurrence "
"across the region as a proxy: a species that reliably occurs with the ones present is "
"assumed suitable. This works where the region is well surveyed and degrades quickly "
"where it is not, and the places with the thinnest survey data are disproportionately the "
"places where the management question is live.")

P['T'] = ("Clerical work in the United States was performed almost entirely by men until "
"the 1880s and almost entirely by women by 1930. The typewriter is usually credited with "
"the change, on the reasoning that a new machine created a new occupation with no "
"incumbent claim to it. The chronology fits loosely and the mechanism is doubtful, since "
"nothing about the machine favoured either sex and its early operators included many men.\n\n"
"A better account begins with what happened to the office rather than what entered it. "
"Firm size grew sharply in the same decades, and correspondence volume grew faster than "
"firm size. The clerk of 1870 was an apprentice manager who drafted letters, kept accounts "
"and expected promotion. The office of 1910 had divided that role into specialised, "
"repetitive positions with no promotion track attached. The typewriter was an instrument of "
"that division rather than its cause.\n\n"
"Once the position carried no prospect of advancement, it no longer attracted men who had "
"alternatives, and it became available to a large pool of educated women who had very few. "
"Wages fell relative to other work, which is the pattern of a job losing its ladder rather "
"than of a technology raising productivity. The feminisation of clerical work is better "
"read as a consequence of deskilling than as a consequence of mechanisation, and the two "
"are separable: the machine could have been introduced without the reorganisation, and in "
"small firms it was.")

P['U'] = ("Seawater absorbs roughly a quarter of the carbon dioxide released by burning "
"fossil fuels, and the absorbed gas forms carbonic acid, lowering ocean pH. The standard "
"concern is that organisms building shells and skeletons from calcium carbonate will find "
"it harder to do so, since acidification reduces the concentration of the carbonate ion "
"they draw on. Laboratory experiments have repeatedly confirmed the effect on corals, "
"pteropods and some molluscs.\n\n"
"Field results have been more varied, and the variation is instructive. Several species "
"calcify normally or faster at pH levels that impair them in tanks. The usual explanation "
"is that laboratory animals are held without food at a level matching the field, and "
"calcification is energetically expensive: an animal with ample energy can maintain the "
"chemistry at its shell surface against an unfavourable gradient, and an animal without "
"cannot. Acidification in that reading is not a chemical barrier but a metabolic tax.\n\n"
"This reframing does not make the problem smaller and it changes what is at risk. A "
"metabolic tax falls hardest where energy is already limiting, which is not where the "
"chemistry is worst. It also implies that the effect will interact with warming and with "
"the food supply rather than adding to them, so projections built by summing single factor "
"experiments will misstate the total in a direction that cannot be signed in advance.")

P['V'] = ("Microfinance institutions lending to borrowers without collateral often use "
"group liability: five or six borrowers receive individual loans, and if one defaults the "
"others are denied future credit. Repayment rates under this structure have been "
"remarkable, frequently above ninety five percent, and the standard explanation credits "
"peer monitoring. Neighbours know who is diverting a loan and can apply pressure that no "
"loan officer could.\n\n"
"A randomised trial in India that converted group liability loans to individual liability, "
"while holding the group meetings and everything else constant, found no difference in "
"default over the following two years. The result is difficult to reconcile with the "
"monitoring account and easy to reconcile with a simpler one: what sustains repayment is "
"the prospect of a further loan, and the group structure had been doing little beyond "
"assembling borrowers in a room every week.\n\n"
"If the dynamic incentive is the whole mechanism, group liability is not merely "
"unnecessary but costly, since it makes each borrower's credit hostage to others and "
"deters exactly the borrowers with the most productive projects, who have the most to lose "
"from someone else's failure. Several large lenders moved to individual liability after the "
"trial and report no deterioration. The episode is a reminder that a practice with an "
"excellent outcome and a plausible story attached will be explained by that story until "
"someone varies it.")

P['W'] = ("The Homeric poems were composed before writing was in general use in Greece, "
"and the question of how a work of that length was produced without it was settled, in "
"most scholars' view, by fieldwork among South Slavic singers in the 1930s. Those singers "
"performed epics of comparable length and could not read. They did so by assembling "
"formulas, fixed phrases fitted to the metre, which allowed composition during "
"performance rather than recitation from memory. The Homeric text shows the same "
"formulaic density, and the inference was drawn.\n\n"
"The inference is strong and one part of it is regularly overstated. That a technique "
"suffices to produce such a poem does not establish that it produced this one, and the "
"Homeric poems differ from the recorded South Slavic material in ways that the formulaic "
"account does not obviously explain, most notably in a large scale architecture that "
"holds across thousands of lines.\n\n"
"The reasonable position concedes the technique and leaves the architecture open. A "
"tradition of oral composition can produce a long poem; whether it can produce a long "
"poem shaped like this one is a separate question, and the comparative evidence bears on "
"it only if the South Slavic singers were doing the same thing rather than something "
"similar. The fieldwork demonstrated a possibility that had been denied. It did not, and "
"was not designed to, identify which of the possibilities the Greek case represents.")

P['X'] = ("The shipping container reduced the cost of moving manufactured goods by an order "
"of magnitude, and the usual explanation is labour: a break bulk ship required gangs of "
"dockworkers for days, and a container ship requires cranes for hours. Labour cost was "
"indeed the largest single line in the old accounts. It was not the largest saving.\n\n"
"The larger saving was in time, and specifically in the time a ship spent in port. A "
"vessel earns nothing tied up, and break bulk vessels spent more than half their working "
"lives alongside. Cutting port time raised the effective capacity of the world fleet "
"without building a ship. A secondary and larger effect followed from predictability: once "
"a sailing could be scheduled to the day, an importer no longer needed to hold weeks of "
"inventory against a variable transit, and the inventory saving accrued to firms that "
"never appeared in any shipping account.\n\n"
"This explains a pattern that the labour account leaves puzzling, namely that the ports "
"which adopted containers earliest were not those with the most expensive dockworkers but "
"those with the most congested berths. It also explains why the transformation looked "
"modest for its first decade. The inventory saving requires reliable schedules, reliable "
"schedules require a network, and a network requires that the ports at both ends have "
"converted. Until enough of them had, the container was a cheaper way to load a ship and "
"very little else.")

# ---------------------------------------------------------------------------
# Items. Keys are written first and permute() moves them; see bank_emit.py.
I = []
def q(iid, pk, skill, sub, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'V', 'type': 'RC', '_p': pk, 'passageId': 'VRP' + pk,
              'sub': sub, 'skill': skill, 'diff': diff, 'stem': stem,
              'choices': choices, 'answer': 0, 'expl': expl, 'wrong': wrong})

# ---------------------------------------------------------------- A, ratings
q('V601','A','v_st','Main idea',3,
 'The passage is primarily concerned with',
 ['distinguishing two explanations of a change in how an industry is paid, and arguing that they point to different reforms',
  'demonstrating that credit rating agencies systematically inflate the ratings they are paid to issue',
  'tracing the history of credit rating from subscription sales to the issuer pays model',
  'arguing that the photocopier was the decisive cause of a change in an industry business model',
  'proposing that a public body should assign rating agencies to issuers'],
 'The first paragraph gives the photocopier account, the second adds regulatory force, and the third says which reform each diagnosis implies.',
 'Inflation is the objection the passage opens with rather than its subject; the history and the photocopier are material for the argument; the public body appears only as an example of one reform family.')
q('V602','A','v_st','Stated detail',2,
 'According to the passage, the agencies acquired which of the following in the same decade in which subscription revenue was falling?',
 ['A position in regulations that made a rating necessary for a bond to be widely salable',
  'A legal immunity from suits brought by investors who relied on their ratings',
  'The ability to reproduce their reports cheaply for a mass readership',
  'A statutory obligation to disclose the methodology behind each rating',
  'Ownership of the pension funds that were their largest subscribers'],
 'The second paragraph says bank capital rules and pension mandates were written in terms of ratings, so an unrated bond was unsalable to a large part of the market.',
 'Immunity, disclosure obligations and fund ownership are never mentioned; cheap reproduction is what the photocopier gave everyone, and is presented as a loss to the agencies.')
q('V603','A','v_st','Organisation',3,
 'The third paragraph proceeds by',
 ['pairing each of two diagnoses with the class of remedy it implies, and noting that one remedy fails under the other diagnosis',
  'ranking four proposed reforms by how much of the conflict each would eliminate',
  'conceding that neither diagnosis has enough evidence behind it to guide policy',
  'showing that the two diagnoses offered earlier are ultimately the same diagnosis',
  'recommending that ratings be removed from bank capital rules and pension mandates'],
 'Copying implies a change in how the product is sold; a captive buyer implies that billing changes cannot help; subscription would reproduce the conflict if mandates stayed.',
 'No ranking is given, the evidence is not called insufficient, the diagnoses are kept distinct, and the passage stops short of recommending any reform.')
q('V604','A','v_inf','Inference',4,
 'It can be inferred from the passage that a return to investor subscription would',
 ['leave the conflict of interest in place so long as ratings remained embedded in regulation',
  'restore the agencies to the revenue levels they enjoyed before the 1970s',
  'be resisted by investors, who would have to pay for what they now receive free',
  'eliminate the conflict of interest but at an unacceptable cost in coverage',
  'require the agencies to abandon the methodologies they currently use'],
 'The last sentence says subscription addresses the copying diagnosis and would reproduce the conflict within a year if the mandates stayed in place.',
 'Revenue levels, investor resistance, coverage costs and methodology are all outside what the passage claims.')
q('V605','A','v_inf','Author agreement',4,
 'The author would most likely agree that the photocopier account of the switch to issuer pays is',
 ['accurate as far as it goes but silent on why a new payer was willing to appear',
  'a rationalisation offered by the agencies to deflect criticism of their incentives',
  'contradicted by the timing of the regulatory changes of the same decade',
  'adequate as an explanation of the switch but useless as a guide to reform',
  'the only account consistent with the decline in subscription revenue'],
 'The second paragraph calls it incomplete: it explains why the old model weakened but not why an inelastic buyer appeared.',
 'The passage does not question the account\'s good faith or its timing, does not call it adequate, and treats falling subscription revenue as common ground rather than as evidence only it explains.')
q('V606','A','v_inf','Application',5,
 'Which of the following situations is most closely analogous to the relationship the passage describes between issuers and ratings?',
 ['A restaurant that must obtain a municipal hygiene certificate before it may open pays the inspection firm that grades it',
  'A magazine sells advertising space to the companies whose products it reviews',
  'A university pays an accreditation body a fee proportional to its enrolment',
  'A software vendor commissions an independent benchmark of its own product and publishes the result',
  'A charity submits voluntarily to an audit in order to reassure its donors'],
 'The point is a buyer made captive by a rule: the restaurant cannot operate without the grade, so it needs the grader more than any diner does.',
 'The magazine, the vendor and the charity all describe voluntary arrangements; the university fee is compulsory but is not a graded judgment the institution shops for.')

# ---------------------------------------------------------------- B, coffee
q('V607','B','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['identify what an agricultural trial failed to measure, using the consequences of a shift in growing practice',
  'argue that shade grown coffee is superior to sun grown coffee in Central America',
  'describe the course of the coffee leaf rust epidemic of 2012',
  'explain why breeding programmes should not aim at increasing yield',
  'compare the input costs of shaded and unshaded coffee plantations'],
 'The last paragraph names the failure: the trial design asked how much coffee a plant yields rather than what the system it sits in was doing.',
 'The passage expressly declines to declare shade superior, and the epidemic, the breeding aim and the input costs are all evidence rather than the point.')
q('V608','B','v_st','Stated detail',2,
 'According to the passage, a closed coffee canopy differs from an open field at midday in that the canopy is',
 ['several degrees cooler',
  'considerably more humid',
  'less exposed to wind',
  'lower in soil nitrogen',
  'more accessible to the spores that carry rust'],
 'The second paragraph states the temperature difference directly, as the reason rust moved faster on sun grown plots.',
 'Humidity and still air are named as conditions rust likes, not as properties the canopy supplies; nitrogen and spore access are not discussed.')
q('V609','B','v_st','Structure',3,
 'The author mentions that shade suppresses yield primarily in order to',
 ['prevent the epidemic evidence from being read as a general case for returning to shade',
  'explain why breeding programmes sought sun tolerant varieties in the first place',
  'account for the rise in fertiliser and herbicide use on sun grown plots',
  'establish that the 2012 losses were smaller than they first appeared',
  'question whether the yield gains of the 1970s were real'],
 'It opens the sentence that begins "It would be a mistake to read this as vindication of the older practice."',
 'The breeding motive is given earlier and separately; inputs, the size of the losses and the reality of the yield gains are not what the concession is doing.')
q('V610','B','v_inf','Inference',4,
 'The passage suggests that a grower who keeps a canopy is in a position most like that of someone who',
 ['pays a recurring cost for protection against an event that may not occur',
  'delays a profitable investment until its risks are better understood',
  'accepts a lower return in exchange for a shorter payback period',
  'buys an asset whose value is expected to rise with the price of a commodity',
  'diversifies a portfolio in order to reduce its exposure to a single market'],
 'The passage says the grower is buying insurance with a premium paid every year whether the rust arrives or not.',
 'No delay, payback period, commodity exposure or diversification is described; the analogy in the text is specifically insurance.')
q('V611','B','v_inf','Inference',5,
 'It can be inferred from the passage that if the 2012 epidemic had occurred during the period in which the sun tolerant varieties were being evaluated, the evaluations would most likely have',
 ['registered a cost that the trials as conducted did not capture',
  'concluded that the new varieties were more rust resistant than the old ones',
  'been abandoned before the yield comparisons could be completed',
  'attributed the losses to the rise in fertiliser and herbicide inputs',
  'recommended the new varieties only for plantations at higher altitudes'],
 'The complaint is that the trials ran over a period that happened to contain no epidemic, so the canopy function went unpriced. An epidemic inside the window would have priced it.',
 'Nothing suggests the new varieties resist rust better, that trials would stop, that inputs would be blamed, or that altitude was a trial variable.')
q('V612','B','v_inf','Author attitude',4,
 'The author\'s attitude toward the breeding programmes described is best characterised as',
 ['unwilling to fault them for a shortcoming located in how their product was tested',
  'critical of their failure to anticipate the epidemiological consequences of removing shade',
  'approving of their results but sceptical that the varieties will remain viable',
  'dismissive of the agronomic reasoning that produced sun tolerant varieties',
  'undecided as to whether their yield gains were correctly measured'],
 'The closing sentence says in terms that the failure was not of the breeding programme but of the trial design.',
 'The passage declines to blame the breeders, does not question the yield measurements, and says nothing about future viability.')

# ---------------------------------------------------------------- C, Hanse
q('V613','C','v_st','Main idea',3,
 'The passage is primarily concerned with',
 ['arguing that a trading league enforced its rules collectively rather than through individual reputation',
  'explaining why the Hanseatic League never established a court with power to compel its members',
  'describing the geographic obstacles to communication among Baltic ports',
  'assessing the commercial success of the Hanseatic League relative to its rivals',
  'showing that embargoes are generally more effective than legal judgments'],
 'The second paragraph names the mechanism as collective, not individual, and the third draws out what that implies.',
 'The absent court is the puzzle rather than the subject, geography is one premise, and no comparison with rivals or with legal systems generally is offered.')
q('V614','C','v_st','Stated detail',2,
 'According to the passage, a member town that ignored an embargo faced',
 ['expulsion, and with it the loss of trading privileges in every other member port',
  'a fine levied by the assembly and payable to the injured merchant',
  'the seizure of its vessels by the ports that had complied',
  'exclusion from future assemblies without loss of trading rights',
  'a counter embargo organised by the merchant who had been wronged'],
 'The second paragraph states the penalty and why it was credible.',
 'Fines, seizures, mere exclusion from assemblies and private counter embargoes are not mentioned.')
q('V615','C','v_st','Structure',4,
 'The author cites the distance between the League\'s ports primarily in order to',
 ['show why an explanation based on individual reputation cannot by itself account for enforcement',
  'explain why the League could not maintain a standing army',
  'suggest that embargoes were difficult to coordinate across the Baltic',
  'account for the survival of so many assembly records',
  'establish that the League\'s members traded mainly with non members'],
 'Reputation requires that the injured party and future counterparties share information, and the passage says ports were weeks apart by sail.',
 'The army, the difficulty of coordination, the records and the trading partners are all outside what that sentence is doing.')
q('V616','C','v_inf','Inference',4,
 'It can be inferred from the passage that the League\'s surviving records consist so largely of assembly minutes because',
 ['a system of collective punishment had to settle in advance what would count as an offence',
  'the League kept no records of individual transactions between merchants',
  'assemblies met more frequently than any other body the League maintained',
  'written contracts were unenforceable in the absence of a court',
  'minutes were the only documents that member towns were required to preserve'],
 'The last paragraph draws exactly this connection: defining the offence replaced trying the offender.',
 'The passage does not claim transaction records were absent, does not compare meeting frequencies, does not say contracts were unenforceable, and mentions no preservation requirement.')
q('V617','C','v_inf','Inference',5,
 'The passage suggests that the League\'s enforcement mechanism would have been least effective against a town whose merchants',
 ['traded mainly outside the network of member ports',
  'were fewer in number than those of the towns embargoing it',
  'had no representation in the League\'s assemblies',
  'dealt in goods that several member ports also supplied',
  'were frequently accused of violations by other members'],
 'The threat works because defection costs the entire network. A town that barely uses the network loses little by being cut off from it.',
 'Numbers, representation, the goods traded and an accusation record are all irrelevant to whether the network has hold over the town.')
q('V618','C','v_inf','Author agreement',4,
 'The author would most likely agree with which of the following statements about the reputation account of Hanseatic enforcement?',
 ['It identifies a real force but requires an information flow the League did not have',
  'It has been superseded by documentary evidence that was unavailable to earlier historians',
  'It applies to relations among merchants but not to relations among towns',
  'It is circular, since it explains compliance by assuming the compliance it should explain',
  'It was invented to fill the gap left by the absence of a Hanseatic court'],
 'The first paragraph calls it inadequate on its own, specifically because reputation needs shared information and the ports were weeks apart.',
 'No new documents are invoked, no merchant and town distinction is drawn, circularity is not the charge, and the account\'s origin is not discussed.')

# ---------------------------------------------------------------- D, antibiotics
q('V619','D','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['set a methodological explanation of a research drought beside an economic one and show that they recommend different remedies',
  'argue that pharmaceutical firms have misrepresented the reasons for the shortage of new antibiotics',
  'describe the discovery of a new class of antibiotic by means of the isolation chip',
  'urge that public funds replace private investment in antibiotic discovery',
  'explain why antibiotics are less profitable than drugs taken for chronic conditions'],
 'The third paragraph states that the two accounts recommend different interventions and that neither is wrong.',
 'The firms are not accused of misrepresentation, the isolation chip is one example, no funding proposal is made, and the profitability point is one premise of the economic account.')
q('V620','D','v_st','Stated detail',2,
 'According to the passage, the limitation of soil screening as a discovery method is that',
 ['the great majority of soil species cannot be grown in a dish',
  'soil samples from different regions contain largely the same species',
  'compounds active in soil are frequently inactive in the human body',
  'the screens require quantities of soil that are impractical to collect',
  'bacteria grown in a dish lose the ability to produce defensive compounds'],
 'The second paragraph says roughly ninety nine percent of soil species will not grow in a dish, so the screens sampled the same small culturable fraction.',
 'Regional similarity, in vivo inactivity, sample volumes and loss of production in culture are not claimed.')
q('V621','D','v_st','Stated detail',3,
 'The passage states that the isolation chip works by',
 ['growing soil organisms in place within a diffusion chamber',
  'concentrating rare soil species before they are transferred to a dish',
  'sequencing soil DNA and synthesising the compounds it encodes',
  'screening compounds against bacteria that have already acquired resistance',
  'shortening the time required for a screen from months to days'],
 'The third paragraph describes it as growing soil organisms in situ inside a diffusion chamber.',
 'Concentration, sequencing, resistant target screening and speed are all other approaches and none is described here.')
q('V622','D','v_inf','Inference',4,
 'It can be inferred from the passage that the increasing frequency with which the golden age screens returned already known compounds was a sign that',
 ['the accessible fraction of soil species had been substantially exhausted',
  'the compounds in question were the most chemically stable ones available',
  'laboratories were duplicating one another\'s sampling sites',
  'resistance was spreading faster than new compounds could be found',
  'the screening protocols had become less sensitive over time'],
 'Sampling the same small culturable fraction repeatedly is what produces rediscovery, and the passage says the method had reached the edge of what it could reach.',
 'Stability, duplicated sites, resistance and declining sensitivity are alternative stories the passage does not tell.')
q('V623','D','v_inf','Application',5,
 'The passage\'s closing observation about a market incentive applied to an exhausted method most directly implies that',
 ['prize and subscription schemes will yield little unless the range of organisms searched is widened',
  'economic explanations of the antibiotic gap are mistaken',
  'firms have insufficient reason to develop antibiotics at any price',
  'the isolation chip should be funded in preference to any economic reform',
  'the modest results of existing incentive schemes were unforeseeable'],
 'The sentence says such an incentive buys more searching in the same place, and the same place is what has been exhausted.',
 'The passage says neither account is wrong, does not deny that incentives matter at all, stops short of ranking the remedies, and treats the modest results as evidence rather than as a surprise.')
q('V624','D','v_inf','Author agreement',4,
 'The author would most likely agree that the pharmaceutical firms\' account of the antibiotic gap is',
 ['correct on its own terms while leaving out the constraint that ended the discovery era',
  'a defence of inaction dressed up as an analysis of incentives',
  'inconsistent with the record of discovery between 1940 and 1962',
  'adequate for the period before 1962 but not for the period since',
  'unfalsifiable, since any absence of discovery can be attributed to weak incentives'],
 'The passage grants the economics by their accounting and then supplies the scientific account that is less often heard, concluding that neither is wrong.',
 'No accusation of bad faith or unfalsifiability is made, no inconsistency with the record is alleged, and the periods are not divided that way.')

# ---------------------------------------------------------------- E, conglomerates
q('V625','E','v_st','Main idea',4,
 'The passage is primarily concerned with',
 ['showing that a measured discount was misinterpreted and relocating the question it was thought to answer',
  'defending the diversified conglomerate against the criticism that it destroys shareholder value',
  'explaining why conglomerates are more common in economies with shallow capital markets',
  'describing the empirical methods used to estimate the conglomerate discount in the 1990s',
  'arguing that divisional managers exert undue influence over corporate headquarters'],
 'The middle paragraph undermines what the discount measures, and the third says the interesting comparison is a different one.',
 'The passage refuses to rehabilitate the form, and the shallow markets point, the methods and the lobbying are all supporting material.')
q('V626','E','v_st','Stated detail',3,
 'According to the passage, researchers who tracked acquired segments from before their acquisition found that',
 ['much of the conglomerate discount was already present before the segments were acquired',
  'the segments outperformed comparable freestanding firms in the years after acquisition',
  'the discount was concentrated in conglomerates operating in unrelated industries',
  'acquisitions were made at random with respect to the target\'s prior performance',
  'the discount disappeared entirely once industry effects were controlled for'],
 'The second paragraph states this directly as the result that questioned what the discount measures.',
 'No outperformance, no concentration by relatedness, no randomness and no complete disappearance is claimed.')
q('V627','E','v_st','Structure',4,
 'The reference to divisional managers who lobby serves primarily to',
 ['name the cost that offsets the advantage of internal capital allocation',
  'explain why conglomerate headquarters tend to be large relative to their divisions',
  'illustrate the difficulty of comparing a division with a freestanding firm',
  'suggest that the conglomerate discount is caused by internal politics',
  'introduce a reason that acquired divisions tend to have been struggling'],
 'It is the real disadvantage set against the real advantage of internal allocation where lenders cannot verify quality.',
 'Headquarters size, the comparison problem and the selection of targets are handled elsewhere, and the passage stops short of attributing the discount to politics.')
q('V628','E','v_inf','Inference',4,
 'It can be inferred from the passage that the internal capital market of a conglomerate is most likely to be advantageous where',
 ['outside lenders have difficulty telling good projects from bad ones',
  'the conglomerate\'s divisions operate in closely related industries',
  'divisional managers are compensated on the performance of their own units',
  'the firm can raise equity more cheaply than it can raise debt',
  'the discount to the sum of the parts is largest'],
 'The third paragraph says internal allocation has a real advantage where external lenders cannot verify quality.',
 'Relatedness, compensation design, the equity and debt mix and the size of the discount are not the condition named.')
q('V629','E','v_inf','Inference',5,
 'The passage implies that the finding that conglomerates trade at a discount to the sum of their parts is',
 ['consistent with the conglomerate form adding value, if the parts were below average when acquired',
  'an artefact of the accounting conventions used in the 1990s',
  'stronger evidence against the form than its critics have recognised',
  'confined to conglomerates in economies with deep capital markets',
  'the result the later literature set out to reproduce and could not'],
 'If the segments were already discounted before acquisition, the comparison with average standalone firms cannot show that the form destroyed value, and may conceal that it added some.',
 'No accounting artefact is alleged, the passage weakens rather than strengthens the case against, the deep markets point concerns prevalence, and the later work questioned the interpretation rather than failing to reproduce the number.')
q('V630','E','v_inf','Application',4,
 'Which of the following, if true, would most strengthen the reading of the discount that the second paragraph proposes?',
 ['Divisions acquired by conglomerates were trading at a discount to industry peers in the year before acquisition',
  'Conglomerates that divested divisions saw their own share prices rise on the announcement',
  'The discount is larger for conglomerates with more divisions than for those with fewer',
  'Freestanding firms in the same industries grew faster than conglomerate segments',
  'Conglomerate headquarters costs account for a measurable share of the discount'],
 'The paragraph\'s claim is that the acquired businesses were already struggling, so a pre acquisition discount is the direct evidence for it.',
 'Divestiture gains, division counts, growth comparisons and headquarters costs are all consistent with the original interpretation as well.')

# ---------------------------------------------------------------- F, whale falls
q('V631','F','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['report evidence against a hypothesis about deep sea dispersal and describe the reversed account that replaces it',
  'describe the three stages of community succession that follow the death of a large whale',
  'argue that whale fall communities are more diverse than hydrothermal vent communities',
  'explain how bacteria metabolising bone lipids produce sulphide on the sea floor',
  'question whether large whales have existed for long enough to support specialised fauna'],
 'The succession is setup; the second paragraph reports the genetic result against the stepping stone reading, and the third gives the reversed dispersal account.',
 'Succession and the sulphide chemistry are background, no diversity comparison is made, and the age of whales is used as a premise rather than doubted.')
q('V632','F','v_st','Stated detail',2,
 'According to the passage, the third and longest stage of a whale fall community depends on',
 ['sulphide produced by bacteria metabolising lipids in the bones',
  'soft tissue that scavengers have not removed',
  'organic material enriching the sediment around the carcass',
  'the migration of species from nearby hydrothermal vents',
  'currents that carry larvae across the abyssal plain'],
 'The first paragraph states it: the bones are rich in lipids, and bacteria metabolising them produce sulphide.',
 'Soft tissue belongs to the first stage and enriched sediment to the second; vent migration and currents are the hypothesis rather than the stage.')
q('V633','F','v_st','Structure',3,
 'The author mentions that large whales appeared perhaps thirty million years ago primarily in order to',
 ['establish that the bone specialists must have originated in some earlier habitat',
  'indicate that whale fall communities are younger than hydrothermal vent communities',
  'question the reliability of the genetic dating used in the studies described',
  'explain why whale falls are difficult to locate on the sea floor',
  'show that the stepping stone hypothesis was plausible when it was proposed'],
 'The third paragraph says the bone specialists must have come from somewhere, and the recency of whales is what forces that question.',
 'The relative age of vents is implied but is not the purpose, the dating is not questioned, locating falls is not discussed, and the plausibility of the hypothesis is not what the sentence supports.')
q('V634','F','v_inf','Inference',4,
 'It can be inferred from the passage that the stepping stone hypothesis required that the chemosynthetic species found on whale falls be',
 ['the same species that occur at hydrothermal vents',
  'capable of surviving without sulphide for extended periods',
  'more numerous on whale falls than at vents',
  'descended from ancestors that lived on the abyssal plain',
  'present during the first stage of the succession as well as the third'],
 'The hypothesis was that falls let vent species disperse between vent fields, which requires that they be vent species; the genetic finding that they are close relatives is what weakens it.',
 'Sulphide tolerance, abundance, abyssal ancestry and stage of appearance are not what the hypothesis turned on.')
q('V635','F','v_inf','Inference',4,
 'The passage suggests that the bone specialist fauna is best described as',
 ['a group that arose from vent related ancestors and now occupies a habitat of its own',
  'a remnant of a fauna that was once widespread across the abyssal plain',
  'an assemblage whose members are recruited anew from vents at each whale fall',
  'a set of species that can survive equally well at vents and on bones',
  'the ancestral stock from which modern vent communities descend'],
 'The last paragraph says the likely source is the sulphide rich habitats that vents represent, and that the fauna now lives nowhere else.',
 'The passage gives the dispersal direction as vents to bones, not the reverse, and describes bone specialists as distinct from vent species rather than interchangeable or continually recruited.')
q('V636','F','v_inf','Application',5,
 'Which of the following findings would most weaken the account offered in the final paragraph?',
 ['Bone specialist lineages are shown by molecular dating to be substantially older than large whales',
  'A whale fall is found to support fewer chemosynthetic species than a vent of comparable size',
  'Some vent species are found to tolerate the sulphide levels typical of whale falls',
  'Scavenging at whale falls is shown to last longer in cold water than in warm',
  'Bone specialists are found at the carcasses of large fish as well as of whales'],
 'The account assumes the specialists arose after whale falls became available, from vent stock. Lineages older than whales would leave that derivation without a habitat to arise in.',
 'Species counts, tolerance, scavenging duration and other carcass types are compatible with the account as stated.')

# ---------------------------------------------------------------- G, Federal Writers
q('V637','G','v_st','Main idea',3,
 'The passage is primarily concerned with',
 ['arguing that the documentary value of a relief programme followed from a constraint rather than from an intention',
  'establishing that the Federal Writers\' Project was intended from the outset as a cultural undertaking',
  'describing the disagreements between the national and regional directors of a federal programme',
  'evaluating the literary quality of the state guidebooks the programme produced',
  'arguing that public patronage of the arts should be judged by its employment effects'],
 'The final paragraph says what the guides demonstrate is less a matter of intent than of structure, and names the constraint.',
 'The intent question is left disputed, the directors and the prose quality are evidence, and no general standard for arts patronage is proposed.')
q('V638','G','v_st','Stated detail',2,
 'According to the passage, the writers who compiled the guides',
 ['had no training in the subjects they wrote about',
  'were selected by the national director for their literary promise',
  'were drawn mainly from the states in which they had been born',
  'worked from a standard questionnaire issued by the national office',
  'were paid according to the number of entries they completed'],
 'The first paragraph says they were people with no training in the subjects they covered, working from local interviews and county records.',
 'Selection by the national director, birth state, a questionnaire and piece rates are all unmentioned.')
q('V639','G','v_st','Structure',4,
 'The author\'s statement that both the national director and the regional directors were telling the truth about their own positions functions primarily to',
 ['present a dispute about purpose as genuine rather than as a case of one side dissembling',
  'explain why the surviving correspondence is difficult to interpret',
  'suggest that the programme lacked a coherent chain of command',
  'establish that cultural nationalism was the programme\'s official rationale',
  'introduce the question of whether unqualified applicants could be refused'],
 'It keeps both accounts of purpose standing, which is what lets the paragraph describe the two as in constant tension.',
 'The correspondence is cited as evidence rather than called opaque, no failure of command is alleged, no official rationale is settled, and the applicant question is an illustration that follows.')
q('V640','G','v_inf','Inference',4,
 'It can be inferred from the passage that if the Federal Writers\' Project had been free to employ only the most capable writers, the guides would most likely have been',
 ['better written and less comprehensive in their geographic coverage',
  'completed more quickly and at lower cost per volume',
  'more consistent in their treatment of contested local history',
  'less useful to historians but more valuable as literature about the same places',
  'similar in coverage, since the relief rolls included capable writers in every county'],
 'The closing sentence says patronage designed for quality would have produced a shelf of better books about fewer places.',
 'Speed, cost, consistency and an unchanged coverage are not what the passage predicts, and the fourth option keeps the coverage the passage says would have shrunk.')
q('V641','G','v_inf','Inference',4,
 'The passage suggests that the unevenness of the guides as prose is',
 ['inseparable from the feature that makes them valuable as a record',
  'the chief reason they have been neglected by historians',
  'evidence that the regional directors prevailed over the national director',
  'attributable to the speed at which the volumes had to be produced',
  'less pronounced than critics at the time alleged'],
 'The same constraint that made the guides uneven as prose made them comprehensive as record.',
 'Neglect, the outcome of the directors\' dispute, production speed and contemporary criticism are not claims the passage makes.')
q('V642','G','v_inf','Author agreement',4,
 'The author would most likely agree that discussing the Federal Writers\' Project mainly as relief spending',
 ['understates what its output turned out to be worth',
  'misrepresents the intentions of the programme\'s national director',
  'is accurate, since employment was the only purpose the programme achieved',
  'confuses the programme with the other arts projects of the same period',
  'reflects the priorities of the regional rather than the national offices'],
 'The first paragraph says the guides are usually treated as a byproduct and that they suggest a different emphasis, and the passage then makes the case for their value.',
 'The director\'s intentions are reported rather than defended, employment was not the only achievement on this account, no confusion with other projects is raised, and the regional priorities point is about the programme rather than about later commentary.')

# ---------------------------------------------------------------- H, groundwater
q('V643','H','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['argue that an accounting practice should change despite the poor state of the measurements that would inform it',
  'compare three methods of estimating the volume of water remaining in an aquifer',
  'demonstrate that satellite gravimetry is the most reliable measure of groundwater depletion',
  'explain why farm economies that irrigate from aquifers record rising output',
  'propose that groundwater be reported as a stock rather than as a flow in a particular country'],
 'The third paragraph rejects the inference that disagreement among methods is a reason to wait, on the ground that the current treatment is a value every method rejects.',
 'The three methods and the farm output are premises, no method is preferred, and no country specific proposal is made.')
q('V644','H','v_st','Stated detail',2,
 'According to the passage, satellite gravimetry detects groundwater depletion by measuring',
 ['the change in mass that depletion causes',
  'the rate at which the land surface subsides',
  'the level of water standing in observation wells',
  'the volume of water withdrawn by irrigation pumps',
  'the reduction in surface flow of connected rivers'],
 'The second paragraph names it as the method that detects the mass change depletion causes.',
 'Subsidence and well levels are the other two methods; pumping volume is the flow figure already recorded, and river flow is not mentioned.')
q('V645','H','v_st','Structure',4,
 'The author characterises the current treatment of groundwater as implicitly assigning a depletion rate of zero primarily in order to',
 ['show that the existing figure is not a cautious estimate but one the evidence excludes',
  'argue that the three measurement methods should be averaged rather than compared',
  'suggest that national accounts were designed before depletion was understood',
  'explain why the disagreement among methods has persisted',
  'establish that groundwater depletion is more severe than the accounts indicate'],
 'The point of the sentence is that zero is not an estimate under uncertainty but a value every method rejects, which is why waiting for better data does not follow.',
 'Averaging, the history of the accounts and the persistence of disagreement are not what it supports, and the severity of depletion is not the argument.')
q('V646','H','v_inf','Inference',4,
 'It can be inferred from the passage that the author regards a groundwater figure known only to within a factor of two as',
 ['preferable to the figure currently used, because the current one lies outside any plausible range',
  'acceptable only as a temporary measure until the three methods converge',
  'no more useful than the current figure, since both are subject to large error',
  'reliable enough to support the taxation of groundwater withdrawal',
  'the best that gravimetry will be able to achieve'],
 'The closing sentence frames the choice as between a wide interval and a point outside it, and says the interval is more informative.',
 'No temporary status, no equivalence, no tax proposal and no limit on gravimetry is stated.')
q('V647','H','v_inf','Inference',5,
 'The passage suggests that a national account that treats groundwater purely as a flow will',
 ['show a country liquidating an asset as though it were earning income',
  'overstate the volume of water pumped in any given year',
  'understate the cost of irrigation to the farms that rely on it',
  'become accurate again once the aquifer stops being drawn down',
  'record the depletion with a lag of several years'],
 'The first paragraph says an aquifer drawn down faster than it recharges is being liquidated rather than harvested, and the economy records rising output with no offsetting entry.',
 'Pumping volume is what such accounts do record correctly, farm level cost is not the subject, and neither a return to accuracy nor a lag is described.')
q('V648','H','v_inf','Application',4,
 'Which of the following arguments most closely parallels the reasoning of the passage\'s final paragraph?',
 ['A firm should record a rough estimate of an uncertain liability rather than carry it at nothing, since nothing is the one figure known to be false',
  'A firm should defer recognising a liability until its amount can be determined within a narrow range',
  'A firm should report the most conservative of several estimates when experts disagree',
  'A firm should disclose the disagreement among its experts rather than publish any single figure',
  'A firm should adopt whichever estimation method its industry most commonly uses'],
 'The structure is identical: the status quo is not a cautious choice under uncertainty but a value the evidence excludes, so a wide interval beats it.',
 'Deferral is the inference the passage rejects, and conservatism, disclosure of disagreement and industry convention are different principles.')

# ---------------------------------------------------------------- I, gauge
q('V649','I','v_st','Main idea',4,
 'The passage is primarily concerned with',
 ['refining the standard account of a case of technological lock in by identifying what the installed base contributed',
  'arguing that Parliament was mistaken to select the narrow gauge in 1846',
  'describing the engineering advantages of the broad gauge over the narrow gauge',
  'showing that network effects were not understood by nineteenth century engineers',
  'explaining why the broad gauge survived until 1892 despite the parliamentary decision'],
 'The second paragraph says the conversion cost account proves less than it appears to, and the third notes the commissioners saw the tradeoff.',
 'The decision is not called mistaken, the engineering and the survival date are supporting facts, and the passage says the commissioners understood the tradeoff.')
q('V650','I','v_st','Stated detail',2,
 'According to the passage, the mileage of narrow gauge track in Britain in 1846 was approximately',
 ['1900 miles',
  '270 miles',
  '2170 miles',
  '1846 miles',
  '892 miles'],
 'The second paragraph gives roughly 1900 miles of narrow gauge against about 270 of broad.',
 'The 270 figure is the broad gauge; the others are not in the passage.')
q('V651','I','v_st','Structure',4,
 'The author\'s point in observing that a network\'s value to a user grows with the number of points it reaches is that',
 ['the larger system was worth more per mile, so the gap between the two would have widened regardless of conversion costs',
  'the narrow gauge would eventually have prevailed even if it had been the smaller system in 1846',
  'conversion costs had been overstated by the parliamentary commissioners',
  'the broad gauge could not have been extended at an acceptable cost',
  'users of the broad gauge were fewer than the mileage figures suggest'],
 'The sentence concludes that the installed base was not merely a sunk cost to be weighed against switching but was itself the benefit.',
 'No claim is made about a counterfactual in which the narrow gauge is smaller, and nothing is said about overstated costs, extension costs or user counts.')
q('V652','I','v_inf','Inference',4,
 'It can be inferred from the passage that the standard explanation of the outcome by conversion costs is incomplete because it treats the installed base as',
 ['a cost of switching rather than as a source of value in its own right',
  'larger than the surviving records show it to have been',
  'fixed at its 1846 level rather than growing thereafter',
  'the property of individual companies rather than of the network',
  'a consequence of the parliamentary decision rather than a cause of it'],
 'The passage says exactly this: the installed base was not merely a sunk cost to be weighed against the benefits of switching; it was itself the benefit.',
 'Record accuracy, growth after 1846, ownership and the direction of causation are not the gap identified.')
q('V653','I','v_inf','Inference',5,
 'The passage suggests that the parliamentary commissioners\' report is of particular interest because it shows that',
 ['the inferior standard was adopted by a body that acknowledged its inferiority',
  'the commissioners had underestimated how quickly the broad gauge could be extended',
  'uniformity was valued more highly by Parliament than by the railway companies',
  'the engineering case for the broad gauge was contested at the time',
  'lock in can be avoided when a central authority intervenes early enough'],
 'The last paragraph notes that the report concedes the broad gauge\'s superiority without ambiguity and recommends the narrow gauge anyway, so this was a decision taken with the tradeoff in full view.',
 'No underestimate is mentioned, Parliament and the companies are not compared, the engineering case is presented as conceded rather than contested, and the case is an instance of lock in rather than of its avoidance.')
q('V654','I','v_inf','Author agreement',4,
 'The author would most likely agree that the British gauge case is',
 ['a genuine instance of lock in, though not one caused by a failure of foresight',
  'a poor example of lock in, since the better technology was correctly identified',
  'evidence that parliamentary intervention generally worsens technological outcomes',
  'best explained by the political influence of the narrow gauge companies',
  'unusual in that the installed base played no part in the outcome'],
 'The passage says the case does show lock in and that the decision was taken with the tradeoff in full view.',
 'The passage affirms rather than denies that it is lock in, generalises nothing about intervention, alleges no lobbying, and makes the installed base central.')

# ---------------------------------------------------------------- J, mole rats
q('V655','J','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['present two non genetic explanations of a social arrangement and draw out what they imply for a genetic one',
  'establish that naked mole rats are more closely related to insects than previously believed',
  'argue that ecological explanations of eusociality are superior to demographic ones',
  'describe the division of labour within a naked mole rat colony',
  'question whether eusociality in insects depends on unusual genetics at all'],
 'The last paragraph says neither alternative requires the genetic asymmetry the insect literature treats as central, and suggests what that means for the haplodiploid account.',
 'No relatedness claim is made, the two alternatives are called complements rather than ranked, the division of labour is setup, and the passage stops short of denying that genetics matters in insects.')
q('V656','J','v_st','Stated detail',2,
 'According to the passage, sisters in bees, ants and wasps share',
 ['three quarters of their genes',
  'half of their genes',
  'all of their genes',
  'a quarter of their genes',
  'the same proportion of genes that mammalian siblings share'],
 'The first paragraph gives the figure as three quarters rather than half.',
 'Half is the ordinary mammalian case the passage contrasts with; the other figures are not stated.')
q('V657','J','v_st','Stated detail',3,
 'The passage describes the demographic explanation of mole rat eusociality as resting on the claim that',
 ['dispersal through the soil the animals inhabit is close to fatal',
  'colonies grow faster than the available tuber supply can sustain',
  'a single breeding female produces more offspring than can be fed',
  'workers live long enough to inherit the breeding position',
  'the sex ratio in a colony is heavily skewed toward females'],
 'The second paragraph says dispersal in such soil is close to suicidal, so staying is cheap rather than beneficial.',
 'Food supply, offspring numbers, inheritance of breeding status and sex ratio are not the demographic claim as given.')
q('V658','J','v_inf','Inference',4,
 'It can be inferred from the passage that the ecological and demographic explanations differ chiefly in that one emphasises',
 ['the benefit of remaining in the colony while the other emphasises the low cost of doing so',
  'genetic relatedness while the other emphasises environmental constraint',
  'the behaviour of workers while the other emphasises the behaviour of the breeding female',
  'conditions inside the colony while the other emphasises conditions outside it',
  'the origins of eusociality while the other emphasises its persistence'],
 'The passage says they operate on different sides of the same ledger: tunnelling for scattered tubers is a benefit of group living, and lethal dispersal makes helping cheap.',
 'Neither invokes relatedness, neither is about the female specifically, both concern the environment, and neither is confined to origins or persistence.')
q('V659','J','v_inf','Inference',5,
 'The passage suggests that the haplodiploid explanation of insect eusociality may be best understood as identifying a factor that',
 ['lowers the threshold for eusociality rather than one without which it cannot arise',
  'operates in mammals as well as in insects, though less strongly',
  'has been refuted by the mole rat evidence',
  'applies only to species whose females mate more than once',
  'explains the division of labour but not the sterility of workers'],
 'The closing sentence says it may describe a factor that makes the arrangement easier in insects rather than one that makes it possible.',
 'The passage does not extend it to mammals, does not call it refuted, says nothing about mating frequency here, and draws no division of labour distinction.')
q('V660','J','v_inf','Application',4,
 'Which of the following discoveries would most weaken the ecological explanation described in the passage?',
 ['A eusocial mole rat species is found in loose soil where tubers are abundant and evenly distributed',
  'A solitary mole rat species is found to tunnel as extensively as eusocial species do',
  'Tubers are shown to be a smaller part of the mole rat diet than was believed',
  'Eusocial colonies are found to contain more than one breeding female in some seasons',
  'Dispersal is shown to be less dangerous during the wet season than during the dry'],
 'The ecological account makes eusociality a response to scattered food in hard soil. A eusocial species where neither condition holds removes the work the explanation was doing.',
 'Tunnelling by solitary species, diet share, breeding female counts and seasonal dispersal risk all leave the conditions the account names intact.')

# ---------------------------------------------------------------- K, classifieds
q('V661','K','v_st','Main idea',3,
 'The passage is primarily concerned with',
 ['reinterpreting the mechanism by which a revenue source was lost, and drawing a general caution from it',
  'arguing that newspapers were wrong to reduce newsroom costs after losing classified revenue',
  'describing how online listing sites undercut the price of classified advertising',
  'explaining why classified advertising was never profitable on its own terms',
  'proposing a business model that would allow newspapers to recover lost advertising'],
 'The first two paragraphs relocate the mechanism from price to unbundling, and the third generalises about cross subsidy.',
 'The newsroom cuts appear only in the closing sentence, the price cut is expressly not the main mechanism, the profitability point is a premise, and no model is proposed.')
q('V662','K','v_st','Stated detail',2,
 'According to the passage, classified advertising was profitable because it',
 ['shared a printing plant, a delivery fleet and a subscriber list with the news operation',
  'commanded higher rates per column inch than display advertising did',
  'required almost no editorial labour to produce',
  'attracted readers who would not otherwise have bought the paper',
  'was sold on annual contracts rather than by the insertion'],
 'The first paragraph states the shared infrastructure as the reason.',
 'Rates, editorial labour, reader attraction and contract terms are not given as the reason.')
q('V663','K','v_st','Structure',4,
 'The author distinguishes reaching buyers from reaching readers primarily in order to',
 ['show that the newspaper had been selling one thing by means of another that was no longer necessary',
  'argue that newspapers should have charged sellers more than they charged readers',
  'explain why display advertising survived while classified advertising did not',
  'establish that listing sites reached a larger audience than newspapers did',
  'suggest that newspaper readers were rarely the buyers of classified goods'],
 'The seller wanted buyers and the newspaper supplied them by supplying readers because no cheaper route existed; once one did, the bundle came apart.',
 'No pricing recommendation is made, display advertising is not discussed, audience size is not compared, and the passage does not claim readers were not buyers.')
q('V664','K','v_inf','Inference',4,
 'It can be inferred from the passage that the newspapers that responded by cutting newsroom costs were assuming that',
 ['the news operation had been supported by classified revenue rather than the reverse',
  'readers would tolerate a reduction in coverage without cancelling subscriptions',
  'listing sites would eventually raise their prices to newspaper levels',
  'classified advertising could be restored if the paper became cheaper to produce',
  'display advertising would replace the revenue that classifieds had provided'],
 'The last sentence says they were acting on a theory of their own business that the unbundling had just refuted. The unbundling ran in the direction of whichever component had been subsidising the other.',
 'Reader tolerance, future pricing by rivals, restoration of classifieds and display substitution are not the theory identified.')
q('V665','K','v_inf','Inference',5,
 'The passage suggests that a bundle of products is vulnerable when',
 ['one of its components can be supplied on its own more cheaply than within the bundle',
  'the components are sold to different sets of customers',
  'the firm cannot determine which component is more profitable',
  'the bundle depends on physical infrastructure that is expensive to maintain',
  'one component has been in decline for a long period'],
 'The first paragraph states the stability condition: a bundle of that kind is stable only while no component can be supplied separately at lower cost.',
 'Different customer sets, managerial ignorance, infrastructure cost and slow decline are conditions the passage mentions or implies but does not identify as the vulnerability.')
q('V666','K','v_inf','Application',4,
 'The caution the author draws about cross subsidy applies most directly to a firm that',
 ['funds a loss making division from a profitable one without knowing which the customer values',
  'sets prices below cost in order to drive a competitor from the market',
  'holds a portfolio of products whose revenues are uncorrelated with one another',
  'invests in research whose commercial value cannot be estimated in advance',
  'sells a product at a loss in order to profit from the supplies it consumes'],
 'The third paragraph says the arrangement conceals which product the customer is actually paying for, and the concealment is mutual.',
 'Predatory pricing, portfolio correlation, research uncertainty and the razor and blades model are different phenomena, and none turns on the firm\'s own ignorance of what is being bought.')

# ---------------------------------------------------------------- L, tree rings
q('V667','L','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['describe a dating technique, a second use to which it has been put, and a complication that use has produced',
  'argue that ice core chronologies are less reliable than tree ring chronologies',
  'explain how overlapping wood samples are chained into a continuous record',
  'establish the dates of several large volcanic eruptions of the first millennium',
  'question the value of written weather accounts as historical evidence'],
 'The three paragraphs do exactly this: the technique, the volcanic cross dating, and the circularity problem it exposed.',
 'The reliability comparison and the chaining method are parts of the account, no dates are established, and the written accounts are discussed only as part of the complication.')
q('V668','L','v_st','Stated detail',2,
 'According to the passage, a large volcanic eruption appears in tree ring records as',
 ['a narrow band occurring across many sites at the same time',
  'a layer of sulphate deposited between two rings',
  'an abrupt change in the chemistry of the wood',
  'a sequence of unusually wide rings following a single narrow one',
  'a gap in which no ring was formed at all'],
 'The second paragraph says the cooling appears in tree rings as a narrow band across many sites at once.',
 'Sulphate layers belong to ice cores; wood chemistry, wide ring sequences and missing rings are not described.')
q('V669','L','v_st','Stated detail',3,
 'The passage states that ice core chronologies accumulate error because they are built by',
 ['counting annual layers downward through the core',
  'matching sulphate peaks to eruptions of known date',
  'measuring the decay of isotopes trapped in the ice',
  'estimating the rate at which snow compacts into ice',
  'correlating ice thickness with recorded temperatures'],
 'The second paragraph says they are built by counting annual layers and accumulate error with depth.',
 'Matching to known eruptions is the correction rather than the construction; isotopes, compaction rates and temperature correlation are not mentioned.')
q('V670','L','v_inf','Inference',4,
 'It can be inferred from the passage that a tree ring chronology does not accumulate error with depth in the way an ice core chronology does because',
 ['overlapping samples can be matched to one another by their shared response to weather',
  'trees are less affected by the conditions that produce unusual layers in ice',
  'wood samples are available from more locations than ice cores are',
  'each tree ring is thicker than the corresponding annual layer of ice',
  'tree ring records extend over shorter periods than ice core records'],
 'The first paragraph explains that matching sequences across samples is what allows the chain to be extended backwards, so the chain is anchored by pattern matching rather than by counting alone.',
 'Weather sensitivity is what makes the method work rather than something trees lack; sample availability, ring thickness and record length do not bear on cumulative counting error.')
q('V671','L','v_inf','Inference',5,
 'The passage suggests that the difficulty occupying the field for two decades arises because',
 ['records used to check one another may not have been independent to begin with',
  'tree ring and ice core chronologies disagree by more than either method can explain',
  'written accounts of unusual weather have been shown to be unreliable',
  'the revised eruption dates conflict with the archaeological record',
  'few eruptions large enough to cool a hemisphere occurred in the first millennium'],
 'The last paragraph says some historians dated eruptions from written weather accounts, and a few of those accounts were used to check the ice cores, so untangling which record is independent of which is the problem.',
 'The passage does not say the disagreement is inexplicable, does not declare the written accounts unreliable, raises no archaeological conflict, and does not claim eruptions were few.')
q('V672','L','v_inf','Application',4,
 'Which of the following research practices would most directly address the difficulty described in the final paragraph?',
 ['Documenting, for each eruption date in use, which records contributed to it and which did not',
  'Collecting additional ice cores from a second polar region',
  'Extending the tree ring chronology further into the past',
  'Reassessing the written accounts for evidence of copying between chroniclers',
  'Measuring sulphate concentrations in the ice with greater precision'],
 'The problem is not accuracy but provenance: which record is independent of which. A dependency record for each date is what resolves it.',
 'More cores, a longer chronology and better precision improve the measurements without settling independence, and copying among chroniclers is a narrower version of the problem rather than a way to untangle it.')

# ---------------------------------------------------------------- M, guilds
q('V673','M','v_st','Main idea',4,
 'The passage is primarily concerned with',
 ['showing that two opposed views of an institution are compatible, and why that leaves the central question unanswerable',
  'arguing that craft guilds were cartels whose abolition permitted industrial growth',
  'demonstrating that guild courts enforced apprenticeship contracts in both directions',
  'explaining why cities without guilds developed no comparable training institutions',
  'assessing whether guild towns grew more slowly than towns without guilds'],
 'The final paragraph reconciles the two views by bundling and then says the balance cannot be struck without a figure the records do not preserve.',
 'The cartel view is one side, the court records and the absence of substitutes are evidence for the other, and the growth correlation is granted rather than assessed.')
q('V674','M','v_st','Stated detail',2,
 'According to the passage, the contracting problem that guilds are said to have solved arises because a master who trains an apprentice',
 ['creates a competitor and therefore has reason to teach badly',
  'cannot recover the wages he pays during the years of training',
  'must accept whoever the town authorities assign to him',
  'loses the apprentice\'s labour to a rival before the term ends',
  'is liable for the apprentice\'s errors against third parties'],
 'The first paragraph states this as the second view\'s premise.',
 'Wage recovery, assignment, poaching and liability are not the problem named.')
q('V675','M','v_st','Structure',4,
 'The author notes that guild courts enforced obligations against masters as well as apprentices primarily in order to',
 ['support the view that the institution addressed a training problem rather than only restricting entry',
  'show that guild courts were more impartial than municipal courts of the period',
  'explain why apprenticeship terms were as long as they were',
  'question whether guilds restricted entry as severely as the cartel view holds',
  'establish that apprentices frequently left before completing their terms'],
 'Two way enforcement is evidence that the courts were solving the teaching problem, which is the second view.',
 'No comparison with municipal courts is drawn, term length is not explained, entry restriction is granted elsewhere, and early departure is an example rather than the point.')
q('V676','M','v_inf','Inference',4,
 'It can be inferred from the passage that the author regards the bundling reading as unsatisfying because it',
 ['requires a quantity that the surviving records cannot supply',
  'depends on evidence from cities that never had guilds',
  'contradicts the finding that guild towns grew more slowly',
  'assumes that the two functions could not have been separated',
  'rests on correlations rather than on documentary evidence'],
 'The paragraph says it is the least satisfying reading because the net question cannot be answered without knowing how much the training was worth, and that figure is not recoverable.',
 'The guildless cities support the training view, the growth finding is accommodated rather than contradicted, separability is not assumed, and both kinds of evidence are used.')
q('V677','M','v_inf','Inference',5,
 'The passage suggests that evidence showing guild towns grew more slowly than towns without guilds is',
 ['consistent with guilds having performed a valuable training function',
  'the strongest single argument against the training account',
  'likely to be explained away as further research is done',
  'confined to the period after the seventeenth century',
  'difficult to reconcile with the records of the guild courts'],
 'The two findings are said to be compatible if the functions were bundled, so the aggregate result does not tell against the training evidence.',
 'The passage calls the correlation robust rather than likely to dissolve, gives it no period limit, and treats it as compatible with the court records rather than in tension with them.')
q('V678','M','v_inf','Application',4,
 'Which of the following, if it could be established, would most help resolve the question the author says cannot currently be answered?',
 ['A reliable estimate of the value of the skills that guild apprenticeship transmitted',
  'A count of the years for which apprentices in various trades were bound',
  'Evidence that guild courts heard more cases against masters than against apprentices',
  'A demonstration that guild towns and non guild towns were otherwise similar',
  'Records showing how guilds set the prices their members charged'],
 'The closing sentence names precisely this figure as what the balance turns on and what the records do not preserve.',
 'Term lengths, case ratios, comparability and price setting each inform one side without supplying the missing quantity.')

# ---------------------------------------------------------------- N, tidal
q('V679','N','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['distinguish the advantage a resource genuinely offers from a broader one often claimed for it',
  'argue that tidal power is unsuitable for supplying electricity at scale',
  'compare the forecasting accuracy of tidal, wind and solar generation',
  'explain how the spring and neap cycle affects the output of a tidal plant',
  'propose that tidal sites in different basins be developed together'],
 'The closing sentence separates the real benefit, less reserve against surprise, from the claimed one, a steady supply.',
 'The passage does not reject tidal power, the forecasting comparison and the neap cycle are premises, and site combination is examined rather than proposed.')
q('V680','N','v_st','Stated detail',2,
 'According to the passage, a tidal stream turbine produces no output',
 ['at slack water, which occurs four times a day',
  'during neap tides',
  'when the tide is running in the direction opposite to the design flow',
  'for roughly half of each spring and neap cycle',
  'at any time that demand is below a threshold'],
 'The second paragraph states this directly.',
 'Neap tides reduce but do not eliminate output, and the other conditions are not described.')
q('V681','N','v_st','Structure',4,
 'The author\'s statement that none of this is a forecasting problem, and all of it is a matching problem, serves primarily to',
 ['concede the predictability of tidal output while denying that predictability answers the objection',
  'argue that grid operators have misunderstood the nature of tidal generation',
  'introduce the proposal that sites with different tidal phases be combined',
  'suggest that demand could be reshaped to fit the tidal generation profile',
  'establish that tidal output is more variable than wind or solar output'],
 'It grants that the profile is known in advance and locates the difficulty in the fact that it does not resemble demand.',
 'No accusation against operators is made, the combination proposal follows separately, demand reshaping is not raised, and no claim of greater variability appears.')
q('V682','N','v_inf','Inference',4,
 'It can be inferred from the passage that combining tidal sites to smooth aggregate output is limited in practice because',
 ['tidal phase is determined by coastal geometry, so the best sites in one country tend to share it',
  'transmission losses between distant sites exceed the benefit of smoothing',
  'the spring and neap cycle affects all sites in a country simultaneously',
  'sites with differing phases have lower energy densities than sites in one basin',
  'grid operators cannot forecast the combined output of several plants'],
 'The third paragraph says the phase of the tide is set by the shape of the coast and the high energy sites in any one country tend to share a basin and therefore a phase.',
 'Transmission losses, energy density and forecasting are not the limitation; the spring and neap point is a separate variation the passage raises earlier.')
q('V683','N','v_inf','Inference',5,
 'The passage implies that a grid supplied partly by tidal generation would still require',
 ['storage sufficient to cover shortfalls that are known about in advance',
  'reserve capacity against errors in tidal forecasting',
  'a demand profile that varies with the lunar month',
  'turbines capable of generating at slack water',
  'a backup source with the same output profile as the tidal plant'],
 'The closing sentence distinguishes reserve against surprise, which predictability reduces, from storage against a shortfall the operator can see coming, which it does not.',
 'Forecast error is what predictability removes, demand cannot be required to follow the moon, slack water generation is impossible on the passage\'s own account, and a matching backup would reproduce the problem.')
q('V684','N','v_inf','Application',4,
 'Which of the following is most closely analogous to the distinction the passage draws about tidal generation?',
 ['A commuter train that runs exactly on schedule but arrives at times that suit few passengers',
  'A factory that can produce any quantity ordered but cannot predict what will be ordered',
  'A supplier whose deliveries are frequent but whose quality varies without warning',
  'A generator that is cheap to run but expensive to build',
  'A forecast that is accurate in the short term and unreliable beyond a week'],
 'Perfect predictability with a profile that does not match demand is exactly the train that is punctual at the wrong hours.',
 'The factory and the forecast describe uncertainty, the supplier describes unreliability, and the cost profile is a different tradeoff.')

# ---------------------------------------------------------------- O, warranty
q('V685','O','v_st','Main idea',3,
 'The passage is primarily concerned with',
 ['explaining why a promising data source must be used in changes rather than in levels',
  'arguing that manufacturers should treat warranty claims as a cost record rather than an indicator',
  'describing how reporting rates for warranty claims vary between distribution channels',
  'demonstrating that warranty data cannot support useful inferences about product quality',
  'proposing a method for estimating failure rates from customer complaints'],
 'The third paragraph says this is not an argument against using the data but against using it in levels, and explains why differencing works.',
 'The passage supports using the data, the channel variation is evidence, it denies that the data is useless, and no estimation method for failure rates is proposed.')
q('V686','O','v_st','Stated detail',2,
 'According to the passage, a warranty claim is filed only if the customer',
 ['notices a fault, judges it worth the trouble, and is still within the coverage period',
  'purchased the product directly from the manufacturer rather than through a dealer',
  'can demonstrate that the fault was present at the time of sale',
  'has registered the product with the manufacturer',
  'reports the fault before attempting any repair'],
 'The second paragraph lists these three conditions.',
 'Purchase channel, proof of prior defect, registration and repair sequence are not the conditions given.')
q('V687','O','v_st','Structure',4,
 'The author contrasts a model sold through dealers with an identical model sold direct primarily in order to',
 ['show that a difference in claim rates can arise with no difference in the units themselves',
  'argue that dealers file claims that customers would not have troubled to file',
  'suggest that direct sales channels produce more reliable products',
  'explain why warranty coverage periods differ between channels',
  'establish that claim paperwork is the main cost of a warranty programme'],
 'The example isolates the reporting rate: the difference says nothing about the units.',
 'Dealer behaviour is the mechanism rather than the point, no quality difference by channel is claimed, coverage periods are not compared, and paperwork cost is not discussed.')
q('V688','O','v_inf','Inference',4,
 'It can be inferred from the passage that differencing warranty claim data is useful because the reporting rate',
 ['changes slowly, while a manufacturing problem appears as a step',
  'is the same across markets once seasonal effects are removed',
  'can be measured directly for each distribution channel',
  'is proportional to the price of the product in every market',
  'falls as a product ages within its coverage period'],
 'The third paragraph gives exactly this contrast as the reason differencing removes the nuisance and leaves the signal.',
 'Cross market equality, direct measurement, price proportionality and ageing are not what the argument rests on.')
q('V689','O','v_inf','Inference',5,
 'The passage suggests that firms which have ranked their products by warranty cost have produced rankings that primarily reflect',
 ['differences in how their products are distributed',
  'differences in the length of coverage each product carries',
  'the relative complexity of the products compared',
  'changes in manufacturing quality over the period studied',
  'the age profile of the units in service'],
 'The closing sentence says such firms have generally ranked their distribution arrangements instead.',
 'Coverage length, complexity, quality change and age profile are not what the passage says the rankings captured.')
q('V690','O','v_inf','Application',4,
 'Which of the following limitations of the differencing approach is most directly implied by the passage?',
 ['It reveals that a product has changed without indicating how good the product is',
  'It requires a longer observation period than firms typically have',
  'It cannot be applied where products are sold through a single channel',
  'It understates problems that develop slowly over the life of a product',
  'It is sensitive to the price at which the product was sold'],
 'The passage grants the approach works at the cost of detecting only changes rather than states.',
 'Observation length, single channel restriction, slow developing faults and price sensitivity are not the cost the passage names.')

# ---------------------------------------------------------------- P, domestication
q('V691','P','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['present a single mechanism proposed to explain a cluster of traits, and state what would test it',
  'argue that selection for tameness is sufficient to explain all traits of domesticated animals',
  'describe the design and results of a long running experiment on silver foxes',
  'establish that the neural crest is the source of pigment cells in mammals',
  'question whether the traits associated with domestication really co occur'],
 'The passage sets out the puzzle, gives the neural crest hypothesis, and names the observation that would sink it.',
 'The passage does not claim sufficiency, the fox experiment is evidence, the neural crest biology is background, and the cluster is treated as established.')
q('V692','P','v_st','Stated detail',2,
 'According to the passage, the silver fox experiment selected on',
 ['willingness to approach a human hand',
  'coat colour and ear carriage',
  'reduced adrenal output measured directly',
  'breeding outside the ancestral season',
  'tolerance of confinement in groups'],
 'The second paragraph says it selected on nothing but willingness to approach a human hand.',
 'Coat and ears are among the traits that emerged, adrenal output is the proposed mechanism, out of season breeding is another trait, and confinement is not mentioned.')
q('V693','P','v_st','Stated detail',3,
 'The passage states that the neural crest contributes to all of the following EXCEPT',
 ['the length of the ancestral breeding season',
  'the adrenal glands',
  'parts of the skull and jaw',
  'the cartilage of the ear',
  'the pigment cells'],
 'The list in the second paragraph names the adrenal glands, parts of the skull and jaw, ear cartilage and pigment cells. Breeding season is a trait in the cluster, not a structure the crest builds.',
 'The other four are given explicitly.')
q('V694','P','v_inf','Inference',4,
 'It can be inferred from the passage that the fox experiment matters to the argument because it shows that the cluster of traits',
 ['can arise from selection on tameness alone, so the link must lie within the animals',
  'appears more rapidly in foxes than in other domesticated species',
  'is present in wild populations at low frequency',
  'depends on deliberate breeding for appearance as well as behaviour',
  'is confined to species that have been domesticated recently'],
 'The passage draws the inference itself: whatever links the traits lies inside the animals rather than in anything the breeders were doing.',
 'Relative speed, wild frequency, appearance breeding and recency are not what the experiment establishes.')
q('V695','P','v_inf','Inference',5,
 'The passage suggests that a domesticated lineage showing tameness without the other traits would',
 ['undermine the neural crest hypothesis by showing the traits to be separable',
  'confirm that selection for tameness acts on adrenal output',
  'indicate that the lineage had been domesticated more recently than others',
  'show that the cluster arises only under deliberate selection for appearance',
  'require that the neural crest contribute to more structures than is currently believed'],
 'The last paragraph names this as the strongest test: it would require the traits to be separable and would sink the account.',
 'The other options either support the hypothesis or introduce claims the passage does not connect to the test.')
q('V696','P','v_inf','Author attitude',4,
 'The author\'s attitude toward the neural crest hypothesis is best described as',
 ['sympathetic to its economy while noting that the evidence that would test it has not been sought',
  'convinced that it has been established by the silver fox experiment',
  'doubtful that any single mechanism could explain a cluster of this breadth',
  'critical of researchers who have failed to propose an alternative',
  'indifferent as between it and the accounts it competes with'],
 'The closing lines credit it with explaining the cluster with one mechanism, deny that it is established, and observe that absence of a report in a literature that is not looking is weak evidence.',
 'The passage says it is not yet established, does not doubt single mechanism accounts in principle, criticises no one, and is plainly not indifferent.')

# ---------------------------------------------------------------- Q, vernacular
q('V697','Q','v_st','Main idea',4,
 'The passage is primarily concerned with',
 ['correcting an explanation of why vernacular buildings perform well, and showing why the correction matters practically',
  'arguing that vernacular building traditions perform better thermally than modern ones',
  'describing the building materials characteristic of hot dry, hot wet and cold regions',
  'criticising architects who build in concrete rather than in traditional materials',
  'establishing that thermal mass is the most important property of a building envelope'],
 'The first two paragraphs relocate the cause from accumulated knowledge to material and structural constraint, and the third says the distinction is not pedantic.',
 'No general performance comparison is made, the regional survey is setup, concrete is one example, and thermal mass is the property the argument identifies rather than a ranking claim.')
q('V698','Q','v_st','Stated detail',2,
 'According to the passage, a tradition that builds in rammed earth produces thick walls because',
 ['thin walls of that material do not stand up',
  'thick walls were required by local building custom',
  'thick walls buffer the daily temperature swing',
  'the material was cheap enough to use in quantity',
  'thick walls resist erosion during the wet season'],
 'The second paragraph gives the structural reason and treats the thermal buffering as the consequence.',
 'Custom, cost and erosion are not given, and the buffering is the side effect rather than the reason.')
q('V699','Q','v_st','Structure',4,
 'The author refers to a thin concrete wall with the same window ratio as a thick earth one primarily in order to',
 ['show that copying vernacular form without the underlying property fails to reproduce the performance',
  'argue that concrete is unsuitable for buildings in hot dry climates',
  'illustrate the difficulty of measuring thermal performance in existing buildings',
  'suggest that window ratio matters less to performance than wall thickness does',
  'establish that modern materials cannot provide thermal mass'],
 'It is the case in which architects reproduced the form in new materials and the performance did not follow.',
 'No general verdict on concrete is offered, measurement is not the issue, the window ratio is held constant rather than compared, and the passage says mass can be supplied in other ways.')
q('V700','Q','v_inf','Inference',4,
 'It can be inferred from the passage that the author regards the climatic performance of vernacular buildings as',
 ['real, but not the property their builders were trying to achieve',
  'overstated by architects who have studied the buildings',
  'achievable only with the materials the traditions actually used',
  'the result of trial and error carried out over many generations',
  'less important than the structural performance of the same buildings'],
 'The second paragraph calls the performance real and largely a side effect of solving a structural problem with the material at hand.',
 'The passage does not call the performance overstated, expressly says mass can be supplied in other ways, rejects accumulated wisdom, and does not rank the two kinds of performance.')
q('V701','Q','v_inf','Inference',5,
 'The passage suggests that the reason vernacular materials tend to suit their climates is that',
 ['what grows and what erodes in a place is itself determined by that climate',
  'builders selected materials after testing how they performed thermally',
  'materials unsuited to a climate were too expensive to transport',
  'traditions borrowed materials from neighbouring regions with similar weather',
  'the same materials are available in most climates at similar cost'],
 'The second paragraph closes by saying the material at hand itself reflects the climate through what grows and what erodes.',
 'Testing is what the passage says builders could not do; transport cost, borrowing and universal availability are not raised.')
q('V702','Q','v_inf','Application',4,
 'Which of the following would the author most likely regard as the appropriate lesson for a contemporary architect designing in a hot dry climate?',
 ['Identify the physical property the traditional form supplied and provide it by whatever means the new materials allow',
  'Build in the traditional material, since new materials cannot reproduce its behaviour',
  'Reproduce the traditional proportions of wall to window as closely as possible',
  'Treat the traditional form as evidence of knowledge the tradition could not articulate',
  'Measure the performance of existing traditional buildings before designing anything new'],
 'The closing lines say reading the form as a byproduct directs attention to the property that mattered, thermal mass, which can be supplied in other ways.',
 'The passage does not require traditional materials, warns against copying proportions, denies the encoded knowledge reading, and does not make measurement the lesson.')

# ---------------------------------------------------------------- R, flood insurance
q('V703','R','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['question a mechanism both sides of a policy debate assume, and identify the instrument that assumption overlooks',
  'argue that federal flood insurance premiums should be raised to actuarial levels',
  'demonstrate that residents of floodplains are poorly informed about their risk',
  'explain why building in floodplains has continued despite repeated losses',
  'compare the fiscal and behavioural arguments for reforming flood insurance'],
 'The second paragraph attacks the shared price signal assumption, and the third names disclosure as the instrument the behavioural work points to.',
 'The passage does not endorse actuarial pricing on behavioural grounds, the survey finding is evidence, floodplain building is context, and the fiscal point is a consequence rather than the subject.')
q('V704','R','v_st','Stated detail',2,
 'According to the passage, surveys of floodplain residents consistently find that most',
 ['substantially underestimate their flood risk',
  'would accept higher premiums in exchange for faster claim settlement',
  'purchased their homes before the floodplain was designated',
  'believe the federal programme will be discontinued',
  'have experienced at least one flood since purchase'],
 'The second paragraph states the underestimation finding, and adds that many are unaware of the designation.',
 'Premium tradeoffs, purchase timing, programme expectations and flood experience are not reported.')
q('V705','R','v_st','Structure',4,
 'The author observes that a household which does not believe it is in a floodplain does not read a low premium as a statement about the floodplain in order to',
 ['show that the premium cannot be functioning as information at any level',
  'explain why premiums have remained below actuarial cost for so long',
  'argue that the subsidy should be defended on grounds other than fairness',
  'suggest that households would respond to a premium increase by relocating',
  'establish that insurers have failed to communicate risk to their customers'],
 'It completes the argument that the price signal mechanism both sides assume is not operating.',
 'The history of the subsidy, the fairness defence, relocation and insurer communication are not what the sentence supports.')
q('V706','R','v_inf','Inference',4,
 'It can be inferred from the passage that if the author is right, raising premiums to actuarial levels would',
 ['change little about where people build, at least in the short run',
  'reduce the number of households carrying flood insurance at all',
  'increase the accuracy of residents\' beliefs about their own risk',
  'be opposed chiefly by insurers rather than by homeowners',
  'require the risk designations to be redrawn first'],
 'The third paragraph says it would transfer money without changing much behaviour, at least in the short run.',
 'Coverage rates, belief accuracy, insurer opposition and redrawing designations are not consequences the passage draws.')
q('V707','R','v_inf','Inference',5,
 'The passage suggests that disclosure at the point of sale is a less popular reform than actuarial pricing because',
 ['it would move property values, which is what the resistance to pricing is ultimately about',
  'it would impose administrative costs on sellers rather than on the federal programme',
  'buyers would be unable to interpret the information it provided',
  'it would apply to properties that actuarial pricing would leave untouched',
  'the designations on which it depends are frequently inaccurate'],
 'The closing sentence says a disclosure that changes behaviour changes property values, and the constituency that resists actuarial pricing resists disclosure for the same underlying reason.',
 'Administrative cost, buyer comprehension, coverage scope and designation accuracy are not the reason given.')
q('V708','R','v_inf','Application',4,
 'Which of the following findings would most weaken the author\'s argument?',
 ['Households that were informed of their floodplain designation went on to buy at the same rate as those who were not',
  'Premiums under the federal programme are further below actuarial cost than previously estimated',
  'Floodplain residents who have experienced a flood remain in place at high rates',
  'The federal programme pays out more in claims than it collects in premiums',
  'Building in floodplains has slowed in states that recently raised premiums'],
 'The argument is that disclosure would do what the premium cannot. If disclosed households behave identically, the instrument the author recommends does nothing.',
 'The subsidy size and the programme deficit are already granted; staying after a flood concerns existing residents rather than buyers; and the last option would weaken the claim about premiums only, which is a weaker hit than removing the proposed remedy.')

# ---------------------------------------------------------------- S, dark diversity
q('V709','S','v_st','Main idea',3,
 'The passage is primarily concerned with',
 ['describing a measure that distinguishes two situations a species count conflates, and the estimation problem it faces',
  'arguing that conservation budgets have been spent on corridors that add no species',
  'defining the regional species pool and explaining how it is delimited',
  'demonstrating that species co occurrence is an unreliable guide to habitat suitability',
  'comparing observed richness with dark diversity across a range of sites'],
 'The three paragraphs give the measure, why it matters for management, and the circularity in estimating it.',
 'The corridor point is one consequence, the pool and the co occurrence proxy are components, and no cross site comparison is presented.')
q('V710','S','v_st','Stated detail',2,
 'According to the passage, the dark diversity of a site is the set of species that',
 ['belong to the regional pool and could survive there but are absent',
  'were present historically and have since been lost',
  'are present but too rare to be detected by standard survey methods',
  'occur at the site only during part of the year',
  'would arrive if the site were connected to others by a corridor'],
 'The first paragraph defines it in these terms.',
 'Historical loss, undetected rarity, seasonality and corridor arrivals are all different sets.')
q('V711','S','v_st','Structure',4,
 'The author contrasts two sites with equally high observed richness primarily in order to',
 ['show that a species count cannot distinguish a dispersal limit from a site limit',
  'argue that observed richness is a poor measure of conservation value',
  'illustrate how dark diversity is estimated from co occurrence data',
  'establish that unsaturated sites are more common than saturated ones',
  'explain why regional species pools differ between regions'],
 'The two sites are indistinguishable on a species count and very different for management, which is the case for the measure.',
 'The passage does not condemn richness generally, the estimation method comes later, no prevalence claim is made, and regional differences are not discussed.')
q('V712','S','v_inf','Inference',4,
 'It can be inferred from the passage that building a corridor to a site with low dark diversity would',
 ['add few species, because the limitation lies in the site rather than in access to it',
  'reduce the site\'s observed richness by introducing competitors',
  'be justified only if the regional pool were unusually large',
  'raise the site\'s dark diversity by expanding its effective regional pool',
  'be cheaper than the alternatives available to managers'],
 'The second paragraph says that where the limitation is the site itself, connection will add nothing.',
 'Competitive loss, pool size conditions, a raised dark diversity and relative cost are not what follows.')
q('V713','S','v_inf','Inference',5,
 'The passage suggests that the co occurrence proxy is least trustworthy precisely where',
 ['the management question it is meant to inform is most pressing',
  'the regional species pool contains the largest number of species',
  'observed richness is high relative to the regional pool',
  'the site has been surveyed more often than its neighbours',
  'dispersal rather than site conditions is the limiting factor'],
 'The closing sentence says the proxy degrades where the region is poorly surveyed, and the thinnest survey data is disproportionately where the management question is live.',
 'Pool size, relative richness, survey frequency at the site and the nature of the limitation are not what governs the proxy\'s reliability.')
q('V714','S','v_inf','Application',4,
 'The estimation difficulty described in the final paragraph is best characterised as',
 ['requiring an answer to something close to the question the measure was introduced to settle',
  'arising from the impossibility of surveying every species at a site',
  'a consequence of using regional rather than local data',
  'stemming from disagreement among practitioners about how to define a region',
  'the result of applying a measure designed for plants to other taxa'],
 'Deciding which regional species could survive at the site is close to the question the measure is meant to answer, which is the circularity named.',
 'Survey completeness, the regional and local distinction, definitional disagreement and taxonomic scope are not the difficulty stated.')

# ---------------------------------------------------------------- T, clerical work
q('V715','T','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['replace a technological explanation of an occupational change with one based on how the work was reorganised',
  'argue that the typewriter had no effect on the composition of the clerical workforce',
  'describe the growth of firm size and correspondence volume in the late nineteenth century',
  'establish that clerical wages fell relative to other work between 1880 and 1930',
  'explain why educated women had few employment alternatives before 1930'],
 'The passage sets out the typewriter account, calls the mechanism doubtful, and gives deskilling as the better account.',
 'The passage allows the typewriter a role as an instrument, and firm size, wages and women\'s alternatives are components of the argument.')
q('V716','T','v_st','Stated detail',2,
 'According to the passage, the clerk of 1870',
 ['drafted letters, kept accounts and expected promotion',
  'was employed chiefly by firms too small to use a typewriter',
  'was paid more than a manager in the same firm',
  'had usually been trained at a commercial college',
  'worked under a supervisor who had held the same position'],
 'The second paragraph describes the 1870 clerk as an apprentice manager with those duties and that expectation.',
 'Firm size, pay relative to managers, training and supervision are not stated.')
q('V717','T','v_st','Structure',4,
 'The author notes that the typewriter\'s early operators included many men primarily in order to',
 ['cast doubt on the claim that the machine itself favoured one sex',
  'show that the transition to a female workforce took longer than is usually supposed',
  'establish that men left clerical work only when wages fell',
  'suggest that the machine was adopted before the reorganisation of the office',
  'explain why the chronology of the change is difficult to establish'],
 'It supports the sentence that nothing about the machine favoured either sex, which is why the mechanism is doubtful.',
 'Duration, the timing of men\'s departure, adoption sequence and chronological difficulty are not what the detail establishes.')
q('V718','T','v_inf','Inference',4,
 'It can be inferred from the passage that the fall in clerical wages relative to other work is treated by the author as evidence that',
 ['the position had lost its promotion prospects rather than gained in productivity',
  'the supply of educated women exceeded the demand for clerical labour',
  'firms were substituting machines for workers wherever they could',
  'clerical work had become more physically demanding than before',
  'the typewriter reduced the skill required to produce a letter'],
 'The passage says the wage pattern is that of a job losing its ladder rather than of a technology raising productivity.',
 'Labour supply, machine substitution, physical demands and typing skill are not the inference the passage draws from the wages.')
q('V719','T','v_inf','Inference',5,
 'The passage suggests that in small firms the typewriter',
 ['was adopted without the reorganisation of clerical work that accompanied it elsewhere',
  'displaced male clerks more rapidly than in large firms',
  'was introduced later than in large firms and to less effect',
  'increased the volume of correspondence more than it reduced the labour of producing it',
  'made promotion from clerk to manager more common than before'],
 'The closing sentence says the machine could have been introduced without the reorganisation, and in small firms it was.',
 'Displacement speed, timing, correspondence volume and promotion rates are not claimed.')
q('V720','T','v_inf','Application',4,
 'Which of the following, if true, would most strengthen the author\'s account?',
 ['Large firms that divided clerical work into specialised positions before adopting typewriters also became predominantly female',
  'The typewriter was adopted at about the same time in firms of every size',
  'Women who entered clerical work had on average more schooling than the men they replaced',
  'Correspondence volume grew fastest in the industries that adopted typewriters earliest',
  'Clerical wages fell most sharply in the decade after the typewriter was introduced'],
 'The account separates reorganisation from mechanisation. Firms that reorganised first and feminised without the machine isolate the variable the author says did the work.',
 'Uniform adoption, schooling, correspondence growth and a wage fall following the machine are each consistent with the typewriter account the author rejects.')

# ---------------------------------------------------------------- U, acidification
q('V721','U','v_st','Main idea',4,
 'The passage is primarily concerned with',
 ['reinterpreting a threat as a metabolic cost rather than a chemical barrier, and saying what that changes',
  'arguing that laboratory experiments on ocean acidification have been poorly designed',
  'establishing that ocean acidification poses a smaller threat than is commonly supposed',
  'describing the chemistry by which dissolved carbon dioxide lowers the pH of seawater',
  'comparing the effects of acidification on corals, pteropods and molluscs'],
 'The second paragraph offers the energetic reading of the field results and the third says the reframing does not make the problem smaller but changes what is at risk.',
 'The laboratory work is reinterpreted rather than faulted, the threat is not minimised, and the chemistry and the taxa are background.')
q('V722','U','v_st','Stated detail',2,
 'According to the passage, acidification reduces the concentration of',
 ['the carbonate ion that shell building organisms draw on',
  'the dissolved oxygen available to organisms at depth',
  'the calcium available in surface seawater',
  'the carbon dioxide that seawater is able to absorb',
  'the organic matter on which filter feeders depend'],
 'The first paragraph states this as the standard concern.',
 'Oxygen, calcium, absorptive capacity and organic matter are not what the passage says is reduced.')
q('V723','U','v_st','Structure',4,
 'The author mentions that laboratory animals are held without food at a level matching the field primarily in order to',
 ['explain why tank results and field results diverge',
  'argue that laboratory experiments should be abandoned in favour of field observation',
  'show that calcification is more energetically expensive than was believed',
  'establish that the species studied in tanks were not representative',
  'suggest that the pH levels used in tanks were unrealistically low'],
 'It is the usual explanation for why several species calcify normally in the field at pH levels that impair them in tanks.',
 'No abandonment is urged, the energetic cost is the mechanism rather than the finding, representativeness is not questioned, and the pH levels are said to match.')
q('V724','U','v_inf','Inference',4,
 'It can be inferred from the passage that an organism with ample energy can calcify at an unfavourable pH because it can',
 ['maintain the chemistry immediately around its shell against the surrounding water',
  'switch to a shell material other than calcium carbonate',
  'delay calcification until conditions improve',
  'absorb carbonate ions directly from its food',
  'reduce the surface area over which dissolution occurs'],
 'The second paragraph says an animal with ample energy can maintain the chemistry at its shell surface against an unfavourable gradient.',
 'Material substitution, delay, dietary carbonate and surface area are not mechanisms the passage names.')
q('V725','U','v_inf','Inference',5,
 'The passage suggests that the metabolic reading implies that the greatest harm from acidification will occur where',
 ['energy is already scarce, which need not be where the water chemistry is worst',
  'pH has fallen furthest below preindustrial levels',
  'calcifying species are most abundant',
  'warming has been slowest and food supply most stable',
  'laboratory and field results agree most closely'],
 'A metabolic tax falls hardest where energy is already limiting, which the passage says is not where the chemistry is worst.',
 'The remaining options either restate the chemical reading or name conditions the passage does not connect to harm.')
q('V726','U','v_inf','Application',4,
 'The final paragraph implies that projections of acidification\'s effects built by adding together the results of single factor experiments will',
 ['be wrong by an amount whose direction cannot be determined beforehand',
  'understate the total harm, since interactions compound the separate effects',
  'be reliable for corals but not for pteropods',
  'improve as more single factor experiments are conducted',
  'overstate the harm, since organisms compensate for stresses they face together'],
 'The closing sentence says such projections will misstate the total in a direction that cannot be signed in advance.',
 'The passage refuses to sign the error, makes no taxon specific claim, and does not suggest more of the same experiments would fix it.')

# ---------------------------------------------------------------- V, microfinance
q('V727','V','v_st','Main idea',3,
 'The primary purpose of the passage is to',
 ['report an experimental result that undercuts the accepted explanation of a lending practice, and draw out its consequences',
  'argue that microfinance institutions should abandon group meetings as well as group liability',
  'establish that repayment rates under group liability have been overstated',
  'describe the design of a randomised trial conducted in India',
  'explain why borrowers without collateral are difficult to lend to'],
 'The trial removes group liability with no effect on default, and the third paragraph says what follows if the dynamic incentive is the whole mechanism.',
 'Meetings were held constant rather than condemned, the repayment rates are granted, the design is evidence, and the collateral problem is setup.')
q('V728','V','v_st','Stated detail',2,
 'According to the passage, under group liability a borrower whose fellow group member defaults',
 ['is denied future credit',
  'must repay the defaulter\'s balance',
  'forfeits a deposit held by the lender',
  'is transferred to a different group',
  'pays a higher interest rate on subsequent loans'],
 'The first paragraph says that if one defaults the others are denied future credit.',
 'Repaying the balance, forfeiting a deposit, transfer and a rate increase are not the terms described.')
q('V729','V','v_st','Stated detail',3,
 'The passage states that the Indian trial held constant',
 ['the group meetings and everything else apart from the liability structure',
  'the size of the loans and the interest rate charged',
  'the identity of the loan officer assigned to each group',
  'the length of the repayment period',
  'the number of borrowers in each group'],
 'The second paragraph says it converted group liability loans to individual liability while holding the group meetings and everything else constant.',
 'Loan size, officer, term and group size may follow from everything else but are not what the passage names.')
q('V730','V','v_inf','Inference',4,
 'It can be inferred from the passage that the peer monitoring account predicts that converting to individual liability would',
 ['raise default rates, since the pressure neighbours apply would be removed',
  'reduce the number of borrowers willing to take loans',
  'have no effect so long as weekly meetings continued',
  'increase the average size of the loans requested',
  'make loan officers more important to repayment than borrowers'],
 'The account credits repayment to pressure that group liability makes rational. Removing the liability should remove the pressure and raise default, which is why the null result is hard to reconcile with it.',
 'Borrower numbers, meeting effects, loan size and officer importance are not what the account predicts about the conversion.')
q('V731','V','v_inf','Inference',5,
 'The passage suggests that group liability deters borrowers with the most productive projects because those borrowers',
 ['stand to lose the most if another member of the group fails',
  'are the least likely to need further loans from the same lender',
  'can obtain credit from other sources on better terms',
  'are least willing to attend weekly meetings',
  'face the highest probability of failure themselves'],
 'The third paragraph says group liability makes each borrower\'s credit hostage to others and deters exactly those with the most to lose from someone else\'s failure.',
 'Outside options, meeting attendance and own failure risk are not the reason given, and the passage does not claim such borrowers stop needing credit.')
q('V732','V','v_inf','Author agreement',4,
 'The author would most likely agree that the peer monitoring account persisted as long as it did because',
 ['it was a plausible story attached to an excellent outcome that no one had varied',
  'the institutions using group liability had an interest in defending it',
  'no data on individual liability lending was available before the trial',
  'randomised trials were not used in development economics until recently',
  'the outcome it predicted was indistinguishable from the outcome of any rival account'],
 'The closing sentence makes exactly this point about a practice with an excellent outcome and a plausible story attached.',
 'Institutional interest, data availability, the history of trials and observational equivalence are not the explanation offered.')

# ---------------------------------------------------------------- W, oral composition
q('V733','W','v_st','Main idea',4,
 'The passage is primarily concerned with',
 ['granting what a body of comparative evidence established while limiting the conclusion drawn from it',
  'arguing that the Homeric poems were composed in writing rather than orally',
  'describing the fieldwork conducted among South Slavic singers in the 1930s',
  'establishing that formulaic density is the defining feature of oral poetry',
  'questioning whether writing was genuinely unavailable in Greece at the relevant period'],
 'The passage accepts the technique and holds the large scale architecture open, saying the fieldwork demonstrated a possibility rather than identifying which possibility the Greek case represents.',
 'It does not argue for written composition, the fieldwork is evidence, formulaic density is a feature rather than a definition, and the availability of writing is a premise.')
q('V734','W','v_st','Stated detail',2,
 'According to the passage, the South Slavic singers composed their epics by',
 ['assembling fixed phrases fitted to the metre during performance',
  'memorising a text that had been dictated to them',
  'improvising freely without regard to metrical constraint',
  'adapting written versions they had heard read aloud',
  'dividing long poems among several performers'],
 'The first paragraph describes composition by formula during performance rather than recitation from memory.',
 'Memorisation, free improvisation, written sources and divided performance are all excluded or unmentioned.')
q('V735','W','v_st','Structure',4,
 'The author\'s statement that a technique sufficing to produce such a poem does not establish that it produced this one serves primarily to',
 ['separate what the comparative evidence proves from what it has been taken to prove',
  'question the accuracy of the transcriptions made during the fieldwork',
  'suggest that the Homeric poems are longer than the South Slavic epics',
  'introduce the claim that writing was available in Greece earlier than supposed',
  'argue that formulaic density can be produced by written composition as well'],
 'It is the hinge of the paragraph that says one part of the inference is regularly overstated.',
 'Transcription accuracy, relative length, the availability of writing and written formulas are not what the sentence does.')
q('V736','W','v_inf','Inference',4,
 'It can be inferred from the passage that the feature of the Homeric poems the author regards as unexplained by the formulaic account is',
 ['their organisation across thousands of lines',
  'the density of fixed phrases in their metre',
  'the length of individual performances',
  'the absence of written sources behind them',
  'their survival in a period without writing'],
 'The second paragraph names a large scale architecture that holds across thousands of lines as what the account does not obviously explain.',
 'Formulaic density is what the account does explain, and performance length, sources and survival are not raised as puzzles.')
q('V737','W','v_inf','Inference',5,
 'The passage suggests that the comparative evidence bears on the question of large scale architecture only if',
 ['the South Slavic singers were doing the same thing as the Homeric composers rather than something similar',
  'the recorded South Slavic epics are as long as the Homeric poems',
  'the fieldwork was conducted before the singers had heard written versions',
  'formulaic density can be measured on a common scale in both traditions',
  'the Greek and South Slavic traditions descend from a common source'],
 'The third paragraph states this condition directly.',
 'Length, contamination, measurement and common descent are not the condition named.')
q('V738','W','v_inf','Author attitude',4,
 'The author\'s position on the significance of the 1930s fieldwork is best described as',
 ['accepting its central demonstration while declining to extend it beyond what it was designed to show',
  'sceptical that singers who could not read composed the epics attributed to them',
  'persuaded that it settles the question of how the Homeric poems were composed',
  'critical of the scholars who conducted it for generalising from a single tradition',
  'undecided as to whether oral composition of long poems is possible at all'],
 'The closing lines say the fieldwork demonstrated a possibility that had been denied and did not, and was not designed to, identify which possibility the Greek case represents.',
 'The passage does not doubt the singers, does not treat the question as settled, criticises no one, and grants the possibility explicitly.')

# ---------------------------------------------------------------- X, containers
q('V739','X','v_st','Main idea',3,
 'The passage is primarily concerned with',
 ['identifying the saving that mattered most in a transport innovation, and using it to explain two otherwise puzzling patterns',
  'arguing that dockworkers were displaced more slowly than is usually claimed',
  'describing the inventory practices of importers before containerisation',
  'explaining why the cost of moving manufactured goods fell by an order of magnitude',
  'comparing the congestion of major ports before and after containers were adopted'],
 'The second paragraph names time and inventory as the larger savings, and the third says this explains the adoption pattern and the slow first decade.',
 'Displacement, inventory practice and congestion are components; the order of magnitude fall is the fact being explained rather than the explanation.')
q('V740','X','v_st','Stated detail',2,
 'According to the passage, break bulk vessels spent',
 ['more than half of their working lives alongside in port',
  'roughly a third of each voyage waiting for a berth',
  'longer in port than container vessels spend at sea',
  'most of their time in ports with the most expensive labour',
  'several days loading for every day they spent unloading'],
 'The second paragraph states the figure.',
 'The other proportions and comparisons are not given.')
q('V741','X','v_st','Structure',4,
 'The author mentions that the inventory saving accrued to firms that never appeared in any shipping account primarily in order to',
 ['indicate that the largest benefit fell outside the industry whose costs were being measured',
  'suggest that shipping companies underinvested in containerisation as a result',
  'explain why importers resisted the shift to container transport',
  'establish that shipping accounts of the period were inaccurate',
  'argue that the inventory saving has never been reliably estimated'],
 'It follows the claim that predictability produced a secondary and larger effect, and locates that effect off the shipping ledger.',
 'Underinvestment, importer resistance, inaccuracy and estimation difficulty are not what the remark establishes.')
q('V742','X','v_inf','Inference',4,
 'It can be inferred from the passage that ports with the most congested berths adopted containers earliest because containerisation',
 ['relieved the constraint that berth time placed on their throughput',
  'required less quayside space than break bulk handling',
  'allowed them to reduce their dockside workforces fastest',
  'attracted the shipping lines with the newest vessels',
  'reduced the depth of water their berths needed'],
 'The saving the passage identifies is in port time, so the ports where berth time bound hardest had the most to gain.',
 'Space, labour reduction, fleet age and draught are not the mechanism the passage supplies.')
q('V743','X','v_inf','Inference',5,
 'The passage suggests that the container\'s effect looked modest for its first decade because',
 ['the inventory saving depended on a network that had not yet been built',
  'early containers were smaller than those in use later',
  'shipping lines were reluctant to retire serviceable break bulk vessels',
  'dockworkers in most ports resisted the new handling methods',
  'importers had not yet learned to schedule shipments to the day'],
 'The closing sentences say the inventory saving requires reliable schedules, which require a network, which requires conversion at both ends.',
 'Container size, vessel retirement, labour resistance and importer learning are not the reason given.')
q('V744','X','v_inf','Application',4,
 'Which of the following business situations most closely parallels the pattern described in the final paragraph?',
 ['A payment system whose value to any merchant depends on how many other merchants accept it',
  'A factory whose unit costs fall as its output rises',
  'A product that sells slowly until its price falls below a threshold',
  'A service whose quality improves as its staff gain experience',
  'A supplier that wins customers by offering longer credit terms'],
 'The container\'s main benefit arrives only once enough ports have converted, which is the structure of a network whose value to each user depends on adoption by others.',
 'Scale economies, price thresholds, learning curves and credit terms are all mechanisms internal to one firm rather than dependent on adoption by others.')

E.permute(I)

# ---------------------------------------------------------------------------
# LIFT: how many distractors on each item are carried past the key.
#
# 94 of the 144 items had the key as the longest option, which a student can play at
# 65 percent against a chance rate of 20. Extending one distractor on each of them, the
# correction the first three reading banks used, would have produced 94 items whose key
# was second longest: the pile relocates rather than spreads, which is INC-0062. The
# number of distractors lifted past the key is what sets the key's rank, so the entries
# below carry four, three, two, one or none, chosen to fill the ranks that the bank as
# written left empty. Every clause is content, not padding: it says something further
# about the wrong answer it is attached to, which is what a distractor of the right
# length should have said in the first place.
LIFT = {
 # four, so the key becomes the shortest option
 'V601': [('systematically inflate', ' in order to keep the business of the issuers who pay them'),
          ('photocopier was the decisive', ' and that no other development of the period contributed'),
          ('tracing the history of credit rating', ' and identifying the decade in which the change took place'),
          ('public body should assign', ' in place of the arrangement under which issuers choose their own')],
 'V613': [('never established a court', ' of its own'),
          ('commercial success of the Hanseatic League', ' in the Baltic and the North Sea over three centuries'),
          ('embargoes are generally more effective', ' at securing compliance from a distant party'),
          ('geographic obstacles to communication', ' during the centuries before steam navigation')],
 'V624': [('unfalsifiable, since any absence', ' after the fact'),
          ('adequate for the period before 1962', ' when the golden age of screening ended'),
          ('inconsistent with the record of discovery', ' by a method that was then still productive'),
          ('defence of inaction dressed up', ' by the firms whose incentives it describes')],
 'V629': [('stronger evidence against the form', ' in the three decades since it was first measured'),
          ('later literature set out to reproduce', ' using data on segments from before acquisition'),
          ('confined to conglomerates in economies with deep', ' where external lenders can verify quality for themselves'),
          ('artefact of the accounting conventions', ' that governed segment reporting at the time')],
 'V639': [("cultural nationalism was the programme's official", ' from the beginning'),
          ('unqualified applicants could be refused', ' by a state office'),
          ('surviving correspondence is difficult to interpret', ' at this distance in time'),
          ('lacked a coherent chain of command', ' between Washington and the state offices')],
 'V649': [('broad gauge survived until 1892', ' in the face of a parliamentary decision taken forty six years earlier'),
          ('network effects were not understood', ' by any of the engineers who gave evidence to the commissioners'),
          ('engineering advantages of the broad gauge', ' in speed, steadiness and the size of locomotive it permitted'),
          ('Parliament was mistaken to select', ' on the evidence that was before it at the time')],
 'V657': [('single breeding female produces more offspring', ' than the colony can support'),
          ('colonies grow faster than the available tuber supply', ' in any given season'),
          ('sex ratio in a colony is heavily skewed', ' from the first generation onward'),
          ('workers live long enough to inherit', ' should she die')],
 'V664': [('classified advertising could be restored', ' at a lower rate per line'),
          ('readers would tolerate a reduction in coverage', ' of the kind the cuts produced'),
          ('display advertising would replace the revenue', ' within a few years'),
          ('listing sites would eventually raise their prices', ' once the classifieds had gone')],
 'V673': [('guild courts enforced apprenticeship contracts', ' for the full length of the agreed term of years'),
          ('craft guilds were cartels whose abolition', ' cleared the way for the factory system that replaced them'),
          ('cities without guilds developed no comparable', ' for transmitting a craft from one generation to the next'),
          ('guild towns grew more slowly', ' over the whole period for which records survive')],
 'V679': [('spring and neap cycle affects the output', ' of a plant over the course of a single lunar month'),
          ('tidal power is unsuitable for supplying electricity', ' to a grid of any appreciable size'),
          ('forecasting accuracy of tidal, wind and solar', ' over horizons of a week or more in ordinary operation'),
          ('tidal sites in different basins be developed', ' as a single portfolio under one operator')],
 'V688': [('same across markets once seasonal effects', ' have been taken out of the series'),
          ('proportional to the price of the product', ' at the point of sale'),
          ('measured directly for each distribution channel', ' from the claims already filed'),
          ('falls as a product ages within its coverage', ' whatever its failure rate')],
 'V697': [('perform better thermally than modern ones', ' built to the same plan in the same climate'),
          ('building materials characteristic of hot dry', ' and the forms that each of those materials permits'),
          ('thermal mass is the most important property', ' a designer working in any material can specify'),
          ('architects who build in concrete', ' in places where an older material was available')],
 'V703': [('premiums should be raised to actuarial levels', ' over a period of years rather than at once'),
          ('residents of floodplains are poorly informed', ' about the designation that applies to the property they bought'),
          ('fiscal and behavioural arguments for reforming', ' as they are usually put by each side of the debate'),
          ('building in floodplains has continued', ' through decades of losses on the public record')],
 'V712': [("raise the site's dark diversity by expanding", ' beyond its present limits'),
          ("reduce the site's observed richness by introducing", ' for the same resources'),
          ('justified only if the regional pool were unusually large', ' for the habitat type in question'),
          ('cheaper than the alternatives available to managers', ' working to a fixed annual budget')],
 'V722': [('dissolved oxygen available to organisms at depth', ' below the mixed layer'),
          ('carbon dioxide that seawater is able to absorb', ' from the atmosphere'),
          ('organic matter on which filter feeders depend', ' in the surface waters'),
          ('calcium available in surface seawater', ' for building shells and skeletons')],
 'V727': [('should abandon group meetings as well', ' and lend to individual borrowers directly rather than through groups at all'),
          ('repayment rates under group liability have been overstated', ' by the institutions that collect and publish the repayment figures themselves'),
          ('borrowers without collateral are difficult to lend to', ' at interest rates that they would be able to afford to pay back'),
          ('design of a randomised trial conducted in India', ' and the two full years of repayment data that the trial went on to produce')],
 'V737': [('fieldwork was conducted before the singers had heard', ' of any of the epic material that they themselves went on to perform'),
          ('formulaic density can be measured on a common scale', ' across languages, metres and quite separate performance traditions'),
          ('Greek and South Slavic traditions descend from a common', ' rather than merely resembling one another in their outward form'),
          ('recorded South Slavic epics are as long as the Homeric', ' and are organised on very much the same scale')],
 'V744': [('sells slowly until its price falls below a threshold', ' that buyers set for themselves'),
          ('wins customers by offering longer credit terms', ' than its competitors will match'),
          ('quality improves as its staff gain experience', ' with the work over several years'),
          ('unit costs fall as its output rises', ' toward the designed capacity of the plant')],
}
E.extend(I, LIFT, 'LIFT4')

LIFT3 = {
 # three, so the key becomes the second shortest
 'V602': [('legal immunity from suits', ' brought after a default'),
          ('statutory obligation to disclose the methodology', ' at the time the rating is published'),
          ('reproduce their reports cheaply', ' without the consent of a subscriber')],
 'V606': [('software vendor commissions an independent benchmark', ' before releasing the next version of the product'),
          ('magazine sells advertising space to the companies', ' whose editors have no say in which products are reviewed'),
          ('university pays an accreditation body a fee', ' on a schedule that is published in advance each year and reviewed by the trustees of both bodies')],
 'V615': [('embargoes were difficult to coordinate', ' within a single sailing season'),
          ("League's members traded mainly with non members", ' rather than with one another in the Baltic'),
          ('League could not maintain a standing army', ' of the kind territorial states of the period fielded')],
 'V623': [('isolation chip should be funded in preference', ' that has so far been proposed by anyone'),
          ('modest results of existing incentive schemes were unforeseeable', ' at the time they were designed and could not have been read off the record then available'),
          ('insufficient reason to develop antibiotics at any price', ' a public purchaser could realistically offer for a drug held in reserve')],
 'V630': [('divested divisions saw their own share prices rise', ' rather than on completion'),
          ('larger for conglomerates with more divisions', ' in the same set of industries'),
          ('same industries grew faster than conglomerate segments', ' over the decade the studies covered')],
 'V635': [('recruited anew from vents at each whale fall', ' as the bones begin to yield sulphide'),
          ('once widespread across the abyssal plain', ' before large whales appeared'),
          ('survive equally well at vents and on bones', ' of the same chemistry')],
 'V645': [('three measurement methods should be averaged', ' before any figure is published'),
          ('groundwater depletion is more severe than the accounts indicate', ' in most farm economies'),
          ('national accounts were designed before depletion', ' had been observed anywhere')],
 'V648': [('defer recognising a liability until its amount', ' by a method the profession has accepted for that class of liability'),
          ('disclose the disagreement among its experts', ' in a note to the accounts rather than in the accounts themselves'),
          ('most conservative of several estimates when experts disagree', ' about the amount at stake and about the method of arriving at it')],
 'V658': [('behaviour of workers while the other emphasises the behaviour', ' who does not forage'),
          ('conditions inside the colony while the other emphasises', ' in the surrounding soil'),
          ('genetic relatedness while the other emphasises environmental', ' of a kind mammals do not share')],
 'V661': [('newspapers were wrong to reduce newsroom costs', ' in the years that followed'),
          ('business model that would allow newspapers to recover', ' the revenue the listing sites took'),
          ('online listing sites undercut the price of classified', ' in every market they entered')],
 'V666': [('portfolio of products whose revenues are uncorrelated', ' across the business cycle'),
          ('sells a product at a loss in order to profit from the supplies', ' over the life of the product'),
          ('invests in research whose commercial value cannot be estimated', ' by anyone inside the firm')],
 'V672': [('Reassessing the written accounts for evidence of copying', ' from one chronicle to another during the same decades'),
          ('Measuring sulphate concentrations in the ice with greater', ' at every depth in the core and across several cores'),
          ('Collecting additional ice cores from a second polar region', ' for comparison with the cores already in hand, at the same depths')],
 'V681': [('grid operators have misunderstood the nature of tidal', ' and the reserve capacity it calls for'),
          ('sites with different tidal phases be combined', ' into a single smoother supply for the grid'),
          ('demand could be reshaped to fit the tidal generation', ' by moving load into the hours when the tide is running')],
 'V684': [('produce any quantity ordered but cannot predict', ' from one week to the next'),
          ('deliveries are frequent but whose quality varies', ' from one consignment to another'),
          ('accurate in the short term and unreliable beyond a week', ' at any time of year')],
 'V691': [('selection for tameness is sufficient to explain all traits', ' that domesticated species are observed to display'),
          ('design and results of a long running experiment on silver foxes', ' begun in 1959 and continued for forty generations'),
          ('neural crest is the source of pigment cells in mammals', ' as well as of several other tissues named here')],
 'V696': [('doubtful that any single mechanism could explain a cluster', ' spanning behaviour, anatomy and pigmentation'),
          ('convinced that it has been established by the silver fox', ' and the forty generations of selection it ran for'),
          ('critical of researchers who have failed to propose an alternative', ' account of the cluster in the decades since it was described')],
 'V706': [("increase the accuracy of residents' beliefs", ' within a season or two'),
          ('reduce the number of households carrying flood insurance', ' in designated areas'),
          ('be opposed chiefly by insurers rather than by homeowners', ' who bear the premium')],
 'V709': [('species co occurrence is an unreliable guide', ' in any region that has been surveyed to a reasonable standard'),
          ('conservation budgets have been spent on corridors', ' that the species in question would never have used'),
          ('comparing observed richness with dark diversity across a range', ' of habitat types, survey intensities and regional pools')],
 'V715': [('growth of firm size and correspondence volume', ' and the reorganisation of clerical work that followed in the larger firms'),
          ('typewriter had no effect on the composition of the clerical', ' at any point during the decades in question'),
          ('clerical wages fell relative to other work between 1880 and 1930', ' in every region for which figures survive')],
 'V721': [('ocean acidification poses a smaller threat', ' to calcifying organisms than to other marine life'),
          ('laboratory experiments on ocean acidification have been poorly', ' from the outset of the research programme'),
          ('chemistry by which dissolved carbon dioxide lowers the pH', ' of the surface ocean over the industrial period')],
 'V729': [('identity of the loan officer assigned to each group', ' throughout the two years the trial ran'),
          ('size of the loans and the interest rate charged', ' on each of the loans that were made'),
          ('number of borrowers in each group', ' and the frequency with which the groups met')],
 'V734': [('improvising freely without regard to metrical constraint', ' of any kind at all'),
          ('adapting written versions they had heard read aloud', ' by another person who was able to read'),
          ('memorising a text that had been dictated to them', ' line by line over many sittings')],
 'V739': [('dockworkers were displaced more slowly than is usually claimed', ' in the ports that were the first to convert to containers'),
          ('congestion of major ports before and after containers', ' had come into general use on the main routes'),
          ('inventory practices of importers before containerisation', ' and the weeks of buffer stock that they had to hold against delay')],
 'V743': [('shipping lines were reluctant to retire serviceable break bulk', ' while they still earned'),
          ('importers had not yet learned to schedule shipments', ' against a reliable sailing'),
          ('dockworkers in most ports resisted the new handling', ' for as long as they could')],
}
E.extend(I, LIFT3, 'LIFT3')

LIFT2 = {
 # two, so the key becomes the middle option
 'V604': [('resisted by investors, who would have to pay', ' out of returns that are already thin'),
          ('eliminate the conflict of interest but at an unacceptable cost', ' to the breadth of market coverage')],
 'V616': [('minutes were the only documents that member towns were required', ' in their own archives'),
          ('assemblies met more frequently than any other body', ' over the course of its history')],
 'V632': [('organic material enriching the sediment', ' in the first year or two'),
          ('migration of species from nearby hydrothermal vents', ' across the abyssal plain')],
 'V646': [('no more useful than the current figure, since both', ' of unknown size in either direction'),
          ('acceptable only as a temporary measure until the three methods', ' on a single figure for the stock remaining')],
 'V660': [('solitary mole rat species is found to tunnel as extensively', ' in the same soil conditions'),
          ('colonies are found to contain more than one breeding female', ' when food is plentiful')],
 'V667': [('dates of several large volcanic eruptions', ' from two records that are independent of one another'),
          ('ice core chronologies are less reliable than tree ring', ' at every depth below the surface of the core')],
 'V683': [('backup source with the same output profile', ' running alongside it'),
          ('reserve capacity against errors in tidal forecasting', ' of the kind wind requires')],
 'V693': [('parts of the skull and jaw', ' of the developing animal'),
          ('the cartilage of the ear', ' that gives it its carriage')],
 'V708': [('Premiums under the federal programme are further below actuarial', ' than the programme itself has reported in any of its filings'),
          ('Floodplain residents who have experienced a flood remain in place', ' for years afterwards rather than relocating')],
 'V718': [('supply of educated women exceeded the demand for clerical labour', ' in the cities where the offices were'),
          ('firms were substituting machines for workers wherever they could', ' do so without disrupting the work')],
 'V733': [('writing was genuinely unavailable in Greece', ' when the poems took their present shape'),
          ('Homeric poems were composed in writing rather than orally', ' by a single author working with a written text')],
 'V741': [('shipping companies underinvested in containerisation', ' for most of a decade'),
          ('inventory saving has never been reliably estimated', ' by anyone in the industry')],
}
E.extend(I, LIFT2, 'LIFT2')

LIFT1 = {
 # one, so the key becomes the second longest
 'V607': ('shade grown coffee is superior to sun grown', ' wherever altitude and rainfall permit either'),
 'V626': ('segments outperformed comparable freestanding firms', ' on every measure'),
 'V636': ('support fewer chemosynthetic species than a vent', ' at the same depth'),
 'V655': ('naked mole rats are more closely related to insects', ' than to other rodents'),
 'V662': ('commanded higher rates per column inch than display', ' in most markets and in most years of the period'),
 'V677': ('difficult to reconcile with the records of the guild courts', ' that survive'),
 'V686': ('purchased the product directly from the manufacturer', ' and registered it'),
 'V702': ('Measure the performance of existing traditional buildings', ' in the same climate before committing to a design'),
 'V710': ('present but too rare to be detected by standard survey', ' in a single season'),
 'V725': ('warming has been slowest and food supply most stable', ' through the year in the regions concerned'),
 'V735': ('introduce the claim that writing was available in Greece', ' before the poems were fixed'),
}
E.extend(I, LIFT1, 'LIFT1')

# Every id the four tables name, with the number of distractors carried past its key.
# check_lift turns a clause that was too short into a named failure rather than a
# distribution that improved less than the tables claim (INC-0066).
INTENT = {}
for _tbl, _n in ((LIFT, 4), (LIFT3, 3), (LIFT2, 2), (LIFT1, 1)):
    for _id in _tbl:
        if _id in INTENT:
            sys.exit('%s appears in two lift tables' % _id)
        INTENT[_id] = _n
E.check_lift(I, INTENT)

HEADER = '''// bank_verbal9.js - Original GMAT Focus Reading Comprehension items V601-V744.
//
// Generated by src/mk_bank_gmat_rc.py. Edit that file, not this one.
//
// The flagship exam's thinnest skills. Identify Stated Idea held 32 items and Identify
// Inferred Idea 39, against 111 to 127 for every other skill on the exam, and eleven
// passages carried all of it. These 144 items across 24 new passages take the two to
// 104 and 111.
//
// Nothing here is tagged v_ac. Analysis / Critique was already the largest verbal skill
// at 124, and growing it further would move the imbalance rather than close it.
//
// Passages are named constants. The existing GMAT verbal banks inline the same paragraph
// on every question that shares it.
//
// On the length tell: the key was the longest option on 94 of these 144 items as
// written, playable at 65 percent against a chance rate of 20. It is corrected by
// carrying four, three, two, one or no distractors past the key, item by item, rather
// than one everywhere, which would have moved the pile to second longest and left it
// just as findable. See LIFT in the generator.
'''

E.measure(I)
PV = {k: 'V_P' + k for k in P}
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_verbal9.js',
        HEADER, [('V_P' + k, P[k]) for k in sorted(P)], I, 'BANK_VERBAL9',
        passage_var=PV, group_key='passageId')
