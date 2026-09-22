#!/usr/bin/env python3
"""Emit src/bank_lsat_lr2.js.

Run: python3 src/mk_bank_lsat_lr2.py src/bank_lsat_lr2.js

The second Logical Reasoning bank. After PR 65 doubled Reading Comprehension, Logical
Reasoning was the only starved section left on the LSAT: seven skills holding 3 to 5
items each, which the review bot reports as twelve skills under twenty five. These 42
items take LR from 30 to 72 and every skill from 3-5 to 9-11.

All the emitting, permuting, extending and measuring is in src/bank_emit.py, which holds
the three corrections a hand written bank always needs. What is here is the content and
the extension clauses, which are the content too: which distractor was lengthened and
with what is the record of how the length tell was brought down.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit as E

I = []
def q(iid, sub, skill, diff, stem, choices, expl, wrong):
    I.append({'id': iid, 'section': 'LR', 'type': 'LR', 'sub': sub, 'skill': skill,
              'diff': diff, 'stem': stem, 'choices': choices, 'answer': 0,
              'expl': expl, 'wrong': wrong})

# ---- Argument Parts and Structure ---------------------------------------------------
q('LL031','Role of a claim','lsat_lr_struct',3,
 'Economist: Raising the tax on sugared drinks is often defended on the ground that it will improve public health. Consumption of the taxed drinks does fall. But in every jurisdiction that has adopted such a tax, purchases of untaxed sweetened products have risen by a comparable amount, and total sugar intake has not measurably changed. The tax should be defended, if at all, as a source of revenue.\n\nThe claim that consumption of the taxed drinks does fall plays which one of the following roles in the economist\'s argument?',
 ['It is a concession to the opposing view, granted so that the argument can turn on what that fact fails to establish.',
  'It is the main conclusion, supported by the observation about purchases of untaxed sweetened products.',
  'It is evidence offered in direct support of the recommendation stated in the final sentence.',
  'It is an assumption without which the claim about total sugar intake could not be evaluated.',
  'It is a counterexample to the claim that such taxes are defended on public health grounds.'],
 'The economist grants the fact the other side relies on, then shows it does not carry the conclusion because substitution offsets it. That is a concession.',
 'The main conclusion is the recommendation in the final sentence. The falling consumption supports the opposing view rather than the recommendation, is stated as an observation rather than assumed, and is not a counterexample to anything.')

q('LL032','Method of argument','lsat_lr_struct',3,
 'Critic: The gallery defends its new hanging by saying that visitors spend longer in the reorganised rooms. Longer viewing is not the same as better viewing. A room whose labels are hard to read also holds visitors longer, and nobody would call that an improvement.\n\nThe critic responds to the gallery by',
 ['offering a case in which the gallery\'s measure of success is satisfied without the success it is meant to indicate',
  'questioning whether the gallery has measured the time visitors spend accurately',
  'arguing that the gallery has confused a cause with one of its effects',
  'showing that the gallery\'s conclusion contradicts a claim it makes elsewhere',
  'pointing out that the gallery has no evidence about visitors who left early'],
 'The illegible label case satisfies the proxy, longer time in the room, while plainly not being better viewing. That shows the proxy does not track what it is standing in for.',
 'The critic does not dispute the measurement itself, allege a causal confusion, find an internal contradiction, or raise the visitors who left.')

q('LL033','Role of a claim','lsat_lr_struct',4,
 'Historian: The standard account holds that the city declined because its harbour silted up. Silting certainly occurred. But the tax rolls show the merchant population falling for two decades before the earliest sediment layer that could have obstructed shipping. Whatever the harbour did to the city afterwards, it cannot explain a decline already underway.\n\nThe statement that silting certainly occurred functions in the argument to',
 ['acknowledge a fact the standard account relies on while denying it the explanatory role that account assigns it',
  'establish that the standard account is based on evidence that has since been shown to be unreliable',
  'introduce the tax roll evidence that the rest of the argument develops',
  'state the conclusion for which the dating of the sediment layer is offered as support',
  'concede that the historian\'s own explanation of the decline is incomplete'],
 'The historian grants the silting and then removes its explanatory work by dating it after the decline began. Granting the fact and denying its role is the function.',
 'Nothing is said to be unreliable. The sentence does not introduce the tax rolls or state the conclusion, and the historian offers no explanation of his own to concede anything about.')

q('LL034','Method of argument','lsat_lr_struct',3,
 'Administrator: Our department should not adopt the new grading software. It was written for institutions with a single academic calendar, and we run three. Every workaround proposed so far requires an administrator to re-enter dates by hand each term, which is the task the software was bought to eliminate.\n\nThe administrator argues against adoption by',
 ['showing that the proposed remedies for a mismatch reintroduce the very cost the purchase was meant to avoid',
  'arguing that the software would fail entirely under the conditions the department operates in',
  'questioning whether the department genuinely runs three academic calendars',
  'comparing the software unfavourably with an alternative product',
  'claiming that the cost of the software exceeds the savings it would produce'],
 'The argument turns on the workarounds: each restores the manual date entry the purchase was supposed to remove, so adoption buys nothing.',
 'The administrator does not say it would fail entirely, doubts nothing about the calendars, names no alternative, and makes no claim about price against savings.')

q('LL035','Role of a claim','lsat_lr_struct',4,
 'Biologist: It is tempting to conclude from the recovery of the wolf population that the reintroduction programme succeeded. The population has indeed recovered. But it recovered at the same rate in the adjacent valley, where no animals were released and where the same restrictions on hunting took effect in the same year. The restrictions, not the releases, are the likely cause.\n\nThe assertion that the population has indeed recovered serves primarily to',
 ['grant the observation on which the tempting conclusion rests before showing that a different cause accounts for it',
  'provide the evidence from which the biologist infers that the hunting restrictions were effective',
  'identify the conclusion that the comparison with the adjacent valley is intended to support',
  'rule out the possibility that the reintroduced animals failed to survive',
  'establish that the reintroduction programme was carried out as designed'],
 'The recovery is granted, and the valley comparison then reassigns its cause. Granting the shared observation is what makes the comparison the decisive move.',
 'The evidence for the restrictions is the valley, not the recovery alone. The conclusion is about cause. Nothing is said about survival or about fidelity to the design.')

q('LL036','Method of argument','lsat_lr_struct',4,
 'Editor: A reviewer objects that our style guide forbids the passive voice. It does not. It advises against the passive where an agent is known and relevant, and gives four cases in which the passive is preferred. The reviewer has read a preference as a prohibition, and then criticised us for a rule we do not have.\n\nThe editor\'s argument proceeds by',
 ['correcting a misstatement of the editor\'s own position and noting that the objection depends on it',
  'conceding that the style guide is ambiguous and proposing a clearer formulation',
  'arguing that the reviewer\'s objection would apply equally to any style guide',
  'showing that the reviewer has applied a standard inconsistently across cases',
  'defending the prohibition on the passive voice by citing the four exceptions'],
 'The editor states what the guide actually says, shows the objection targets something else, and identifies the misreading. That is correcting a misstated position.',
 'No ambiguity is conceded, no generalisation to all guides is offered, no inconsistency is alleged, and the editor denies the prohibition rather than defending it.')

# ---- Drawing Well-Supported Conclusions ---------------------------------------------
q('LL037','Most strongly supported','lsat_lr_concl',3,
 'Every building on the older campus was fitted with the same boiler model in 1978. Boilers of that model have a service life of forty years under continuous use and somewhat longer under intermittent use. The three buildings that are heated year round have all had their boilers replaced. The library, which is closed for four months each year, has not.\n\nWhich one of the following is most strongly supported by the information above?',
 ['The library\'s boiler has been in service longer than any boiler currently operating on the older campus.',
  'The library\'s boiler will fail before the end of the current year.',
  'Intermittent use extends a boiler\'s service life by at least four months per year of reduced operation.',
  'The three year round buildings replaced their boilers because the boilers had reached the end of their service life.',
  'No boiler on the older campus has ever been replaced before reaching forty years of age.'],
 'All were fitted in 1978, the year round buildings have replaced theirs, and the library has not. So the library\'s is the only original one still running, and therefore the longest in service.',
 'Nothing dates the failure. The extension from intermittent use is described only as somewhat longer. The reason for the replacements is not given, and nothing rules out an early replacement.')

q('LL038','Must be true','lsat_lr_concl',3,
 'The archive accepts a manuscript only if it is either older than 1600 or written by an author already represented in the collection. It accepted the Warren manuscript. The Warren manuscript was written in 1742.\n\nIf the statements above are true, which one of the following must also be true?',
 ['Its author is already represented in the archive\'s collection.',
  'It is the most recent manuscript the archive has accepted.',
  'The archive accepts every manuscript by an author it already holds.',
  'The archive has accepted other manuscripts written after 1600.',
  'Its author wrote at least one other manuscript that survives.'],
 'Acceptance requires one of the two conditions. The date rules out the first, so the second must hold.',
 'Nothing about recency, about accepting every manuscript by a held author, about other post-1600 acceptances, or about survival of other works follows.')

q('LL039','Most strongly supported','lsat_lr_concl',4,
 'Among the plots sown in April, yield rose with rainfall up to sixty millimetres and fell above it. Among the plots sown in May, yield rose with rainfall across the whole range recorded. Total rainfall in the region exceeded sixty millimetres in each of the last six seasons.\n\nThe statements above most strongly support which one of the following?',
 ['In each of the last six seasons, the April plots would have yielded more had rainfall been lower.',
  'The May plots outyielded the April plots in each of the last six seasons.',
  'Rainfall above sixty millimetres damages seed sown in April but not seed sown in May.',
  'Sowing in May is preferable to sowing in April in any region with high rainfall.',
  'Yield in the April plots has fallen in each of the last six seasons.'],
 'Above sixty millimetres, April yield falls as rainfall rises. Rainfall exceeded sixty in each of the six seasons, so in each of them less rain would have meant more yield.',
 'No comparison of the two groups\' levels is given, only their responses. The mechanism, the general recommendation and the trend over seasons all go beyond what is stated.')

q('LL040','Must be true','lsat_lr_concl',3,
 'No member of the drafting committee voted against the proposal. Every member who attended the March meeting voted on the proposal. Two members of the committee did not vote at all.\n\nIf the statements above are true, which one of the following must be true?',
 ['At least two members of the committee did not attend the March meeting.',
  'Every member who attended the March meeting voted in favour of the proposal.',
  'The proposal was adopted by the drafting committee.',
  'Exactly two members of the committee were absent from the March meeting.',
  'Some member of the committee abstained rather than voting against.'],
 'Attending the March meeting entails voting. Two members did not vote, so those two did not attend.',
 'The second is true of attendees but the question asks what must follow, and it does: attendees voted and nobody voted against. Adoption does not follow from an absence of opposing votes, exactly two absentees is not entailed, and abstaining is not the same as not voting at all.')

q('LL041','Most strongly supported','lsat_lr_concl',4,
 'The clinic sees patients by appointment and by walk in. Walk in patients wait longer on average than patients with appointments. Last month the clinic reduced the number of appointment slots and the average wait for walk in patients fell.\n\nWhich one of the following is most strongly supported by the information above?',
 ['Some of the time freed by the reduction in appointment slots was used to see walk in patients.',
  'The clinic saw fewer patients in total last month than in the month before.',
  'Walk in patients now wait less time on average than patients with appointments.',
  'Reducing appointment slots is the most effective way to shorten waits for walk in patients.',
  'The number of walk in patients fell last month.'],
 'Fewer appointment slots and a shorter walk in wait together suggest the freed capacity went to walk ins; otherwise the reduction would not have shortened their wait.',
 'Total volume, a reversal of the two groups\' relative waits, a claim about the best method, and a fall in walk in numbers are all unsupported and the last would be an alternative explanation rather than something supported.')

q('LL042','Must be true','lsat_lr_concl',4,
 'Any grant application scored above eighty by both reviewers is funded. Any application scored below sixty by either reviewer is rejected. The Halloran application was scored seventy four by the first reviewer.\n\nIf the statements above are true, which one of the following must be true of the Halloran application?',
 ['It was not funded on the basis of scoring above eighty with both reviewers.',
  'It was rejected.',
  'It was funded.',
  'The second reviewer scored it below sixty.',
  'It was neither funded nor rejected.'],
 'Seventy four is not above eighty, so the funding rule cannot have been satisfied. Whether it was funded some other way is not stated, and the question asks only what must be true.',
 'Rejection requires a score below sixty from someone, which is not established. Funding is not established. The second reviewer\'s score is unknown, and nothing says these are the only two outcomes.')

# ---- Detecting Assumptions ----------------------------------------------------------
q('LL043','Necessary assumption','lsat_lr_assum',3,
 'Newspaper column: The council should reject the proposed stadium. Cities that have built comparable stadiums in the past decade have seen no lasting increase in employment, and the public share of the cost has in every case exceeded the original estimate.\n\nThe argument depends on assuming which one of the following?',
 ['The reasons the council might have for approving the stadium are not ones the column\'s evidence leaves untouched.',
  'No city that built a comparable stadium experienced any economic benefit whatever.',
  'The public share of the cost of the proposed stadium will exceed the original estimate by more than it did elsewhere.',
  'Employment is the only measure by which a public investment should be judged.',
  'The council has been presented with an alternative use for the same funds.'],
 'The column moves from two findings to a recommendation. That step needs the findings to bear on the actual case for approval; if the council\'s reasons lie elsewhere, the evidence does not reach them.',
 'No benefit whatever is far stronger than needed. A larger overrun, a sole measure and an alternative use are none of them required for the argument to go through.')

q('LL044','Sufficient assumption','lsat_lr_assum',4,
 'Curator: This panel cannot be by Vasari. Every authenticated Vasari panel uses a ground of gesso over linen, and this panel\'s ground is gesso applied directly to the board.\n\nThe curator\'s conclusion follows logically if which one of the following is assumed?',
 ['Vasari never used a ground other than gesso over linen on a panel.',
  'Panels with gesso applied directly to the board were unusual in Vasari\'s workshop.',
  'Every panel with a ground of gesso over linen is by Vasari.',
  'Authentication of a panel depends primarily on the preparation of its ground.',
  'No painter other than Vasari used a ground of gesso over linen.'],
 'The evidence covers authenticated panels only. To reach a conclusion about every Vasari panel, the curator needs the practice to hold without exception, which is what this supplies.',
 'Unusual is not never. The third and fifth reverse the conditional. The fourth is about method rather than about the inference.')

q('LL045','Necessary assumption','lsat_lr_assum',3,
 'Manufacturer: Our new packaging uses thirty percent less plastic by weight than the packaging it replaces, so switching to it will reduce the amount of plastic waste our products generate.\n\nThe argument depends on assuming which one of the following?',
 ['The number of packages the company produces will not rise enough to offset the saving per package.',
  'The new packaging can be recycled by the same facilities that handle the old packaging.',
  'Consumers will not prefer the old packaging strongly enough to reduce sales.',
  'No competitor has adopted packaging that uses less plastic still.',
  'The thirty percent reduction was measured under conditions representative of ordinary use.'],
 'A saving per package becomes a saving in total only if volume does not rise to cancel it. Deny this and the conclusion fails.',
 'Recyclability, consumer preference and competitors are all beside the total weight claim. Measurement conditions bear on the premise rather than on the step from it.')

q('LL046','Sufficient assumption','lsat_lr_assum',4,
 'Policy analyst: The programme cannot be judged a failure. Its stated aim was to reduce waiting times, and waiting times fell in every region where it operated.\n\nThe analyst\'s conclusion follows logically if which one of the following is assumed?',
 ['A programme that achieves its stated aim everywhere it operates is not a failure.',
  'Waiting times would not have fallen in those regions without the programme.',
  'Reducing waiting times was the programme\'s most important aim.',
  'No programme that reduces waiting times has ever been judged a failure.',
  'The programme operated in every region where waiting times fell.'],
 'The premise is that the stated aim was met everywhere it operated. This principle carries that straight to the conclusion.',
 'Counterfactual causation, relative importance and the historical generalisation are none of them enough to license the step. The fifth reverses the relation.')

q('LL047','Necessary assumption','lsat_lr_assum',4,
 'Researcher: Students who took notes by hand recalled more of the lecture a week later than students who typed. Handwriting must therefore engage memory more deeply than typing does.\n\nWhich one of the following is an assumption required by the researcher\'s argument?',
 ['The difference in recall is not explained by some other difference between the two groups.',
  'Students who took notes by hand wrote down fewer words than those who typed.',
  'Recall a week later is a better measure of learning than recall immediately afterwards.',
  'The students were assigned to the two conditions rather than choosing between them.',
  'Typing produces notes that are less useful for revision than handwritten notes.'],
 'The inference from a difference in outcome to a claim about mechanism requires that nothing else distinguishing the groups produced it. Deny it and the conclusion collapses.',
 'Word count is a possible mechanism rather than a requirement. The value of delayed recall, the assignment procedure and the usefulness of the notes are each too specific to be necessary.')

q('LL048','Necessary assumption','lsat_lr_assum',3,
 'Chef: Diners say they want smaller portions, but the dishes we serve in half sizes sell poorly. What diners actually want is not smaller portions but the feeling of having been offered them.\n\nThe chef\'s argument depends on assuming which one of the following?',
 ['Diners who want smaller portions would order the half sizes if that were what they wanted.',
  'The half size dishes are priced proportionately to the full size dishes.',
  'Most diners are aware that half sizes are available.',
  'The full size portions are larger than most diners can finish.',
  'No restaurant has succeeded by offering only smaller portions.'],
 'The chef reads poor sales as showing the stated preference is not the real one. That reading requires that wanting smaller portions would show up as ordering them.',
 'Pricing and awareness are ways the assumption could fail rather than the assumption itself, and are narrower than it. Portion size and other restaurants are not required.')

# ---- Identifying Flaws in Arguments -------------------------------------------------
q('LL049','Flaw','lsat_lr_flaw',3,
 'Columnist: The mayor claims the new bus lanes have improved traffic. But the mayor proposed the lanes, campaigned for them and would be embarrassed if they failed. Her assessment can safely be disregarded.\n\nThe reasoning in the columnist\'s argument is flawed in that it',
 ['rejects a claim on the basis of the claimant\'s interest in it rather than on any evidence about the claim itself',
  'treats the absence of evidence for a conclusion as evidence that the conclusion is false',
  'draws a general conclusion from an unrepresentative sample of cases',
  'confuses a condition sufficient for a result with one necessary for it',
  'relies on the testimony of a source whose expertise has not been established'],
 'Everything offered concerns the mayor\'s stake in the outcome. None of it bears on whether traffic improved, which is the question.',
 'No absence of evidence is treated as disproof, no sample is generalised from, no conditional is reversed, and the columnist relies on no testimony.')

q('LL050','Flaw','lsat_lr_flaw',3,
 'Manager: Our most productive engineers all use the new development tool. If the remaining engineers adopted it, their productivity would rise to the same level.\n\nThe manager\'s reasoning is questionable because it',
 ['overlooks the possibility that the most productive engineers adopted the tool because they were already the most productive',
  'assumes without warrant that the remaining engineers are willing to change the tools they use',
  'fails to consider whether the new tool is more expensive than the tools it would replace',
  'treats a claim about a group as though it were a claim about each of its members',
  'relies on a measure of productivity that has not been shown to be accurate'],
 'The association is equally consistent with the causation running the other way, or with a common cause. The argument assumes the tool made them productive.',
 'Willingness and cost are practical objections rather than flaws in the inference. No group to member slide occurs, and the measure is not the issue.')

q('LL051','Flaw','lsat_lr_flaw',4,
 'Official: Critics say our inspection regime is too lax because only two percent of inspections find a violation. But a high violation rate would mean the regime was failing to deter. A low rate is exactly what a successful regime produces.\n\nThe official\'s reply is most vulnerable to the criticism that it',
 ['offers an interpretation of the low rate that is consistent with the critics\' explanation as well as the official\'s',
  'assumes that deterrence is the only purpose an inspection regime can serve',
  'relies on statistics whose source and method have not been disclosed',
  'attacks the critics\' motives rather than the substance of their objection',
  'concludes that the regime is successful merely because no alternative has been proposed'],
 'A low rate is what successful deterrence produces and also what lax inspection produces. Since the evidence fits both stories, it cannot favour one.',
 'The official does not claim deterrence is the only purpose, question the statistics, attack motives, or argue from the absence of alternatives.')

q('LL052','Flaw','lsat_lr_flaw',4,
 'Advocate: Opponents of the housing bill say it will not solve the shortage. That is true, but it is not an objection. No single measure will solve the shortage. The bill should therefore be passed.\n\nThe advocate\'s argument is flawed in that it',
 ['treats the failure of an objection to be decisive as though it established the case in favour',
  'misrepresents the opponents as claiming that the bill would make the shortage worse',
  'assumes that the housing shortage can be solved by legislation of some kind',
  'appeals to the number of people who support the bill rather than to its merits',
  'takes a claim about all measures to establish a claim about this measure in particular'],
 'Showing that one objection does not defeat the bill leaves the bill unsupported. The advocate moves from that to a recommendation with nothing positive offered.',
 'The opponents are not misrepresented, the solvability assumption is not what the argument turns on, no appeal to numbers is made, and the generalisation about measures is used correctly.')

q('LL053','Flaw','lsat_lr_flaw',4,
 'Nutritionist: A study found that people who eat breakfast weigh less than those who skip it. Skipping breakfast therefore causes weight gain, and anyone trying to lose weight should eat in the morning.\n\nThe nutritionist\'s reasoning is flawed because it',
 ['infers a causal relation and a direction for it from an association that is consistent with neither',
  'generalises from a study whose sample was too small to support any conclusion',
  'assumes that everyone who eats breakfast eats the same kind of food',
  'ignores evidence that some people who skip breakfast are underweight',
  'confuses the average weight of a group with the weight of each of its members'],
 'The association supports neither that skipping causes gain nor that the effect runs that way rather than the reverse or from a third factor. Two steps are taken at once.',
 'Sample size is not given, the composition of breakfast is beside the point, no such evidence is ignored in the argument, and no average to individual slide occurs.')

q('LL054','Flaw','lsat_lr_flaw',3,
 'Developer: Residents object that the tower will block their light. But the same residents objected to the terrace development ten years ago, and that development is now considered an asset to the street. Their objection can be set aside.\n\nThe developer\'s argument is most vulnerable to criticism on the ground that it',
 ['assumes that an objection is unfounded because objections from the same source proved unfounded before',
  'fails to establish that the terrace development is in fact considered an asset',
  'overlooks the possibility that the residents have other objections to the tower',
  'treats the residents as a single group with a single view',
  'draws a conclusion about light from evidence concerning the appearance of a street'],
 'Being wrong once does not make a different objection wrong. Nothing here addresses whether the tower will block light.',
 'The terrace verdict is granted for argument. Other objections, the unity of the group and the subject matter of the earlier case are all secondary to the inference itself.')

# ---- Effect of Additional Evidence ---------------------------------------------------
q('LL055','Strengthen','lsat_lr_evid',3,
 'Archaeologist: The settlement was abandoned suddenly rather than gradually. Cooking vessels were left on hearths, and stores of grain were left sealed in pits.\n\nWhich one of the following, if true, most strengthens the archaeologist\'s argument?',
 ['At nearby settlements known to have been abandoned gradually, vessels and stored grain were removed before departure.',
  'The grain in the sealed pits was of a variety grown widely in the region at the time.',
  'The hearths show signs of having been used over many years.',
  'Cooking vessels of the kind found were costly to replace.',
  'The settlement was occupied for at least two centuries before it was abandoned.'],
 'The inference needs leaving goods behind to distinguish sudden from gradual abandonment. The comparison supplies exactly that contrast.',
 'The grain variety, the age of the hearths and the length of occupation are silent on the manner of departure. The cost of the vessels helps a little but says nothing about what gradual departures look like.')

q('LL056','Weaken','lsat_lr_evid',3,
 'Hospital director: Our new triage protocol works. Since it was introduced, the average time from arrival to treatment has fallen by eighteen minutes.\n\nWhich one of the following, if true, most weakens the director\'s argument?',
 ['Over the same period the hospital began diverting the most complex cases to a regional centre.',
  'Some staff found the new protocol harder to follow than the one it replaced.',
  'The average time from arrival to treatment remains longer than at comparable hospitals.',
  'The eighteen minute figure is an average across all departments rather than a figure for each.',
  'The protocol was introduced at the same time in every department of the hospital.'],
 'Diverting the most complex cases would shorten the average without the protocol doing anything, which supplies the whole effect from another source.',
 'Difficulty of use, a comparison with other hospitals, the averaging across departments and simultaneous rollout leave the causal claim largely intact.')

q('LL057','Strengthen','lsat_lr_evid',4,
 'Engineer: The bridge deck is deteriorating faster than expected, and the cause must be the de-icing salt. Decks on the two neighbouring spans, which carry similar traffic and were built to the same design, are not salted and show no comparable deterioration.\n\nWhich one of the following, if true, most strengthens the engineer\'s argument?',
 ['The three spans were built in the same year, by the same contractor, from the same batch of concrete.',
  'De-icing salt is known to accelerate the corrosion of reinforcing steel in concrete.',
  'The deteriorating span carries slightly more heavy goods traffic than the neighbouring spans.',
  'Salting of the deteriorating span began within a year of its opening.',
  'The neighbouring spans are inspected on the same schedule as the deteriorating span.'],
 'The comparison is only as good as the similarity of the spans. Same year, contractor and concrete batch closes the remaining ways they could differ.',
 'The known mechanism supports plausibility without improving the comparison. More heavy traffic weakens it. The timing and the inspection schedule add little.')

q('LL058','Weaken','lsat_lr_evid',4,
 'Publisher: Our decision to drop the paywall was correct. Readership tripled in the year that followed, and subscription revenue fell by only four percent.\n\nWhich one of the following, if true, most weakens the publisher\'s argument?',
 ['Most of the subscriptions that would have lapsed that year were on multi-year terms that had not yet come up for renewal.',
  'Several competing publications dropped their paywalls during the same year.',
  'The tripled readership included a large number of readers outside the publication\'s home market.',
  'Advertising rates in the sector fell during the year in question.',
  'The paywall had been in place for only two years before it was removed.'],
 'If the lapses were deferred by multi-year terms, the four percent understates the loss and the year is too early to judge. That attacks the one figure holding the argument up.',
 'Competitors, the location of new readers, ad rates and the age of the paywall do not undercut the revenue figure on which the claim rests.')

q('LL059','Strengthen','lsat_lr_evid',3,
 'Teacher: The reading scheme is responsible for the improvement. Pupils who joined the scheme in September scored higher in June than pupils who did not join.\n\nWhich one of the following, if true, most strengthens the teacher\'s argument?',
 ['Pupils were assigned to the scheme by lot rather than by teacher recommendation.',
  'The pupils who joined the scheme enjoyed it more than they expected to.',
  'The June assessment was marked by teachers who did not know which pupils had joined.',
  'The scheme has produced similar results at a school in a neighbouring district.',
  'Pupils who joined the scheme attended more sessions than the scheme required.'],
 'The obvious rival explanation is that stronger readers joined. Assignment by lot removes it, which is the weakest link in the argument.',
 'Enjoyment is irrelevant. Blind marking removes a smaller bias. Another school and attendance both help slightly without addressing selection.')

q('LL060','Weaken','lsat_lr_evid',4,
 'Consultant: Remote work has not reduced productivity. Output per employee at the firms we surveyed was unchanged after they moved to remote work.\n\nWhich one of the following, if true, most weakens the consultant\'s argument?',
 ['The firms that agreed to be surveyed were those that had already reported satisfaction with remote work.',
  'Output per employee is measured differently in some of the surveyed industries than in others.',
  'Some employees at the surveyed firms returned to the office part of the week.',
  'The survey covered a period of eighteen months rather than a full business cycle.',
  'Output per employee rose slightly at a minority of the firms surveyed.'],
 'A sample drawn from firms already satisfied with remote work cannot support a general claim, because the firms where it went badly are the ones missing.',
 'Measurement differences, hybrid attendance and the survey window are weaker objections, and a minority improving is consistent with the claim.')

# ---- Principles, Rules and Analogy ---------------------------------------------------
q('LL061','Principle applied','lsat_lr_prin',3,
 'A reviewer should disclose any relationship with an author that a reader would want to know about when weighing the review, whether or not the relationship affected the reviewer\'s judgement.\n\nThe principle above most helps to justify which one of the following?',
 ['Ferris should have disclosed that the author had been her doctoral supervisor, even though she believes it made no difference to her assessment.',
  'Ferris should have declined to review the book, because the author had been her doctoral supervisor.',
  'Ferris need not have disclosed her acquaintance with the author, because the review was favourable.',
  'Ferris should disclose the relationship only if a reader complains about the review.',
  'Ferris should have disclosed her view of the author\'s earlier work before reviewing the new book.'],
 'The principle requires disclosure regardless of effect on judgement. A supervisor is plainly a relationship a reader would want to know about.',
 'The principle requires disclosure, not recusal. It does not turn on the review being favourable or on a complaint, and a view of earlier work is not a relationship.')

q('LL062','Principle applied','lsat_lr_prin',3,
 'It is wrong to make a promise that one does not intend to keep, and equally wrong to make one that one knows one will be unable to keep.\n\nThe principle above is violated in which one of the following situations?',
 ['Ibarra promises to deliver the report by Friday although the data it requires will not be released until the following week.',
  'Ibarra promises to deliver the report by Friday and is prevented from doing so by an illness nobody anticipated.',
  'Ibarra promises to deliver the report by Friday, intending to do so, and finds the task harder than expected.',
  'Ibarra declines to promise a delivery date because she is not certain she can meet one.',
  'Ibarra promises to deliver the report by Friday and delivers it on Thursday.'],
 'Knowing the data will not exist until afterwards is knowing the promise cannot be kept, which the principle forbids.',
 'Unforeseen illness and unexpected difficulty involve no such knowledge. Declining to promise and delivering early violate nothing.')

q('LL063','Principle identified','lsat_lr_prin',4,
 'The council refused the licence because the applicant had twice failed to file the returns required of an existing licence holder. The applicant objected that the returns were a formality and that no harm had come of the omissions.\n\nWhich one of the following principles, if valid, most helps to justify the council\'s refusal?',
 ['A regulator may treat a record of ignoring requirements as evidence about how an applicant would behave in future, whatever harm those omissions caused.',
  'A regulator should refuse a licence whenever an applicant has broken any rule, however minor.',
  'A regulator should give greater weight to an applicant\'s conduct than to the applicant\'s stated intentions.',
  'A requirement that causes no harm when ignored should be removed rather than enforced.',
  'An applicant who objects to a refusal bears the burden of showing that the refusal was unreasonable.'],
 'The applicant\'s defence is that the omissions were harmless. This principle makes the record itself the relevant evidence, which answers that defence directly.',
 'The second is far stronger than the council needs. The third does not engage the harmlessness point, the fourth argues against the council, and the fifth is procedural.')

q('LL064','Parallel principle','lsat_lr_prin',4,
 'A guide who leads a party into terrain beyond its ability is at fault even if the party returns unharmed.\n\nThe principle above is most closely paralleled by which one of the following?',
 ['A pharmacist who dispenses the wrong dose is at fault even if the patient suffers no ill effect.',
  'A pharmacist who dispenses the right dose is not at fault if the patient suffers an ill effect.',
  'A guide who refuses to lead a party into difficult terrain has not thereby failed the party.',
  'A pharmacist is at fault for an error only when the patient is harmed by it.',
  'A party that insists on entering terrain beyond its ability shares the fault with its guide.'],
 'Both make fault turn on the conduct rather than on the outcome: wrong dose, harmless outcome, still at fault.',
 'The second and fourth reverse or restrict the principle. The third and fifth concern different questions, refusal and shared responsibility.')

q('LL065','Principle applied','lsat_lr_prin',3,
 'An institution that benefits from a practice it knows to be unjust has an obligation to act, and the obligation is not discharged by the institution\'s having inherited the practice rather than established it.\n\nThe principle above most strongly supports which one of the following?',
 ['The university cannot rely on the fact that the endowment was created long before its current officers took office.',
  'The university should return the endowment to the descendants of those who were wronged.',
  'The university is obliged to act only if it established the practice from which it benefits.',
  'The university bears no obligation because its current officers did not know of the practice.',
  'The university should establish whether other institutions face comparable obligations.'],
 'The principle expressly refuses inheritance as a discharge, which is exactly what reliance on the endowment\'s age would amount to.',
 'The principle requires action without specifying return. The third and fourth contradict it, and comparison with others is beside it.')

q('LL066','Principle identified','lsat_lr_prin',4,
 'The editor removed the photograph from the archive listing at the family\'s request, but kept the original in the archive and noted in the catalogue that an image had been withdrawn from public display.\n\nWhich one of the following principles most closely conforms to the editor\'s handling of the request?',
 ['A custodian may limit access to material out of regard for those affected, provided the record of what exists is not altered.',
  'A custodian should comply with any request from a family concerning material that depicts them.',
  'A custodian should never remove material from public view once it has been catalogued.',
  'A custodian should preserve material only where doing so serves a research purpose.',
  'A custodian should make public the reasons for any decision to restrict access.'],
 'Access was limited and the record was preserved and annotated. That is the shape of the principle exactly.',
 'The second and third are absolutes the editor did not follow. The fourth is about preservation criteria, and the editor noted the withdrawal without giving reasons.')

# ---- Explanations and Parallel Reasoning --------------------------------------------
q('LL067','Resolve the discrepancy','lsat_lr_expl',3,
 'The library extended its opening hours by twelve hours a week. Over the following term, the total number of hours the building was occupied by readers rose only slightly, while the number of individual visits rose sharply.\n\nWhich one of the following, if true, most helps to explain the results?',
 ['The added hours were early in the morning, when readers tend to come in briefly and leave.',
  'The library publicised the extended hours widely among students and staff.',
  'Seating in the reading rooms was not increased when the hours were extended.',
  'The number of books borrowed rose in proportion to the number of visits.',
  'Other libraries in the city reduced their opening hours during the same term.'],
 'Many short visits explain a sharp rise in visits with little rise in total occupied hours. The timing of the added hours supplies that.',
 'Publicity and neighbouring closures explain more visits without explaining why total hours barely moved. Seating would cap both, and borrowing is beside the point.')

q('LL068','Resolve the discrepancy','lsat_lr_expl',3,
 'A vineyard switched from hand harvesting to machine harvesting. The cost per tonne harvested fell by a third, yet the vineyard\'s total harvesting cost for the season rose.\n\nWhich one of the following, if true, most helps to explain the apparent discrepancy?',
 ['The machine allowed the vineyard to bring in a far larger crop than it could previously have harvested in time.',
  'The machine required an operator with a licence that the vineyard\'s existing staff did not hold.',
  'Machine harvested fruit sold for slightly less per tonne than hand harvested fruit.',
  'The vineyard hired fewer seasonal workers than it had in previous years.',
  'The machine was bought outright rather than leased for the season.'],
 'A lower cost per tonne with a much larger tonnage gives a higher total. The volume increase reconciles both figures directly.',
 'The licence and the purchase are costs that would raise the total without explaining the per tonne fall. Price per tonne is revenue, and fewer workers cuts cost.')

q('LL069','Parallel reasoning','lsat_lr_expl',4,
 'Every apprentice who completed the programme was offered a post. Yates completed the programme. So Yates was offered a post.\n\nThe reasoning above is most similar to that in which one of the following?',
 ['Every ticket drawn in the first round won a prize. The green ticket was drawn in the first round. So the green ticket won a prize.',
  'Every ticket that won a prize was drawn in the first round. The green ticket won a prize. So the green ticket was drawn in the first round.',
  'Most apprentices who completed the programme were offered a post. Yates completed the programme. So Yates was probably offered a post.',
  'No ticket drawn after the first round won a prize. The green ticket won a prize. So the green ticket was drawn in the first round.',
  'Every apprentice offered a post had completed the programme. Yates was offered a post. So Yates completed the programme.'],
 'The original applies a universal to an instance of its antecedent. The first option has exactly that form.',
 'The second and fifth reason from the consequent. The third weakens the premise to most. The fourth reasons from a negative universal.')

q('LL070','Resolve the discrepancy','lsat_lr_expl',4,
 'A city introduced a fee for single use bags. Bag use in supermarkets fell by eighty percent. The total weight of plastic in the city\'s household waste stream did not fall.\n\nWhich one of the following, if true, most helps to explain the results?',
 ['Households had reused the free bags as bin liners and now buy heavier purpose made liners instead.',
  'Some shoppers bought reusable bags made from thicker plastic than the bags they replaced.',
  'The fee applied only to supermarkets and not to smaller retailers.',
  'Plastic packaging on grocery items increased slightly over the same period.',
  'Households were slower to change their habits than the council had expected.'],
 'A substitution that is heavier than what it replaces holds the total steady even as bag use collapses, and reuse as bin liners is the known channel.',
 'Reusable bags are bought once. Smaller retailers and packaging would add to the total rather than hold it level, and slow habit change conflicts with the eighty percent fall.')

q('LL071','Parallel flaw','lsat_lr_expl',4,
 'The restaurants with the longest queues serve the best food. If we improve our food, our queues will lengthen.\n\nWhich one of the following exhibits a flaw in reasoning most similar to that in the argument above?',
 ['The firms with the largest research budgets hold the most patents. If we increase our research budget, we will hold more patents.',
  'The firms with the largest research budgets hold the most patents. Our research budget is small, so we hold few patents.',
  'Every firm that holds many patents has a large research budget. We hold many patents, so our budget must be large.',
  'Firms with large research budgets tend to be older. Our firm is new, so our budget is probably small.',
  'The firms with the most patents are the most profitable. We should therefore seek patents in order to become profitable.'],
 'Both take an association and assume that moving the associated variable will move the other, with the direction of causation simply assumed.',
 'The second applies the association to a case. The third reasons from the consequent of a universal. The fourth is a different inference, and the fifth is a recommendation rather than a prediction.')

q('LL072','Resolve the discrepancy','lsat_lr_expl',3,
 'Two clinics use the same surgical technique for the same condition. The first reports a complication rate twice that of the second, yet independent review found the surgery at both to be of equally high quality.\n\nWhich one of the following, if true, most helps to explain the difference in reported rates?',
 ['The first clinic accepts referrals of patients whose other conditions make complications more likely.',
  'The first clinic performs the operation more often than the second.',
  'Surgeons at the second clinic have on average more years of experience.',
  'The second clinic follows up with patients for a longer period after surgery.',
  'The first clinic publishes its complication rate annually and the second does not.'],
 'Different patient mixes produce different complication rates from identical surgery. The referral pattern supplies exactly that.',
 'Volume alone does not change a rate. Greater experience and longer follow up at the second clinic would cut against the review\'s finding or raise its reported rate. Publication does not change the rate.')

print('%d items drafted' % len(I))

# -------------------------------------------------------------------------------------
HEADER = '''// bank_lsat_lr2.js - Original LSAT Logical Reasoning items LL031-LL072.
//
// Generated by src/mk_bank_lsat_lr2.py. Edit that file, not this one.
//
// The second Logical Reasoning bank. After the reading corpus doubled, Logical Reasoning
// was the only starved section left on the LSAT: seven skills holding 3 to 5 items each,
// which the review bot reports as skills under twenty five. These 42 items take LR from
// 30 to 72, six per skill.
//
// Six per skill rather than a flat total, because the engine selects per skill and a
// section that averages well can still starve a single skill. The seven subtypes inside
// each skill are the ones LSAC describes for the section.
//
// The three corrections every hand written bank needs live in src/bank_emit.py: keys
// permuted off position A and the index computed (INC-0039), seeded from crc32 rather
// than hash (INC-0003), strings JSON escaped (INC-0001), ids single quoted so the build
// can count them (INC-0059).
'''

E.permute(I)

# Measured before extension: the longest option was the key far more often than chance,
# for the same reason it was in the reading bank. A correct LSAT answer is the most
# carefully qualified statement on offer, so writing the key first and the distractors
# after produces short wrong answers. Each clause below states the omission that makes
# the option wrong or carries its error one step further. None is filler and none makes a
# wrong option defensible.
EXTEND = {
 'LL031': ('supported by the observation about purchases', ' of untaxed sweetened products in those jurisdictions'),
 'LL032': ('measured the time visitors spend accurately', ' across the reorganised and unreorganised rooms'),
 'LL033': ('based on evidence that has since been shown to be unreliable', ' by later work on the sediment record'),
 'LL034': ('would fail entirely under the conditions', ' the department operates in, whatever workaround was adopted'),
 'LL035': ('infers that the hunting restrictions were effective', ' across both the release area and the adjacent valley'),
 'LL036': ('the style guide is ambiguous', ' on the point the reviewer raised'),
 'LL037': ('will fail before the end of the current year', ', having passed the service life stated for its model'),
 'LL038': ('the most recent manuscript the archive has accepted', ', since nothing later than 1742 is mentioned'),
 'LL039': ('outyielded the April plots in each of the last six seasons', ', given that their yield rose across the whole range'),
 'LL040': ('voted in favour of the proposal', ', since no member of the committee voted against it'),
 'LL041': ('saw fewer patients in total last month', ' than in the month before the change was made'),
 'LL042': ('was rejected', ' on the strength of the first reviewer\'s score alone'),
 'LL043': ('experienced any economic benefit whatever', ' from building a comparable stadium'),
 'LL044': ('unusual in Vasari\'s workshop', ' during the period the panel is thought to date from'),
 'LL045': ('recycled by the same facilities', ' that handle the packaging it replaces'),
 'LL046': ('would not have fallen in those regions', ' had the programme never operated there'),
 'LL047': ('wrote down fewer words than those who typed', ' during the lecture itself'),
 'LL048': ('priced proportionately to the full size dishes', ' rather than at more than half the price'),
 'LL049': ('treats the absence of evidence for a conclusion', ' as evidence that the conclusion is false'),
 'LL050': ('willing to change the tools they use', ' in the way the manager\'s proposal would require'),
 'LL051': ('assumes that deterrence is the only purpose', ' an inspection regime can be designed to serve'),
 'LL052': ('misrepresents the opponents', ' as claiming that the bill would make the shortage worse'),
 'LL053': ('sample was too small to support any conclusion', ' about the population the study was drawn from'),
 'LL054': ('fails to establish that the terrace development', ' is in fact considered an asset to the street'),
 'LL055': ('grown widely in the region at the time', ' the settlement is thought to have been abandoned'),
 'LL056': ('harder to follow than the one it replaced', ' during the first weeks after it was introduced'),
 'LL057': ('accelerate the corrosion of reinforcing steel', ' in concrete decks of the kind used on all three spans'),
 'LL058': ('dropped their paywalls during the same year', ', competing for the same readers'),
 'LL059': ('similar results at a school in a neighbouring district', ' with a comparable intake'),
 'LL060': ('measured differently in some of the surveyed industries', ' than in others covered by the same survey'),
 'LL061': ('declined to review the book', ', because the author had been her doctoral supervisor'),
 'LL062': ('prevented from doing so by an illness', ' that nobody involved could have anticipated'),
 'LL063': ('refuse a licence whenever an applicant has broken any rule', ', however minor the breach and whatever its consequences'),
 'LL064': ('is not at fault if the patient suffers an ill effect', ' that the correct dose could not have prevented'),
 'LL065': ('return the endowment to the descendants', ' of those who were wronged by the practice'),
 'LL066': ('comply with any request from a family', ' concerning material in which they are depicted'),
 'LL067': ('publicised the extended hours widely', ' among students and staff before the term began'),
 'LL068': ('required an operator with a licence', ' that none of the vineyard\'s existing staff held'),
 'LL069': ('Most apprentices who completed the programme were offered a post', '. Yates completed it, so Yates was probably offered one'),
 'LL070': ('bought reusable bags made from thicker plastic', ' than the single use bags they replaced'),
 'LL071': ('Our research budget is small, so we hold few patents', ' relative to the firms with the largest budgets'),
 'LL072': ('performs the operation more often than the second', ' over the course of a year'),
}
E.extend(I, EXTEND)

# A second clause on twenty two items, for the tell that appears one position over.
#
# After the first pass the extremes were clean, 10 percent longest and 0 shortest against
# a cap of 36. The rank was not: 30 of 42 keys sat second longest, so a student picking
# the second longest option would have scored 71 percent. This is mechanical rather than
# careless, and it is the second time it has happened: extending exactly one distractor
# per item moves every key from rank 5 to rank 4. bank_emit.measure reports the whole
# rank for that reason.
EXTEND2 = {
 'LL031': ('the claim about total sugar intake could not be evaluated', ' against the evidence the economist gives'),
 'LL032': ("gallery's conclusion contradicts a claim it makes elsewhere", ' about the purpose of the reorganisation'),
 'LL033': ('the dating of the sediment layer is offered as support', ' by the rest of the argument'),
 'LL034': ('the cost of the software exceeds the savings', ' it would produce over its working life'),
 'LL035': ('the comparison with the adjacent valley is intended to support', ' in the final sentence'),
 'LL036': ('citing the four exceptions', ' the guide sets out to it'),
 'LL039': ('damages seed sown in April but not seed sown in May', ', whatever the total for the season'),
 'LL041': ('the most effective way to shorten waits', ' for patients who arrive without an appointment'),
 'LL045': ('measured under conditions representative of ordinary use', ' rather than under laboratory conditions'),
 'LL046': ('has ever been judged a failure', ' by those who evaluated it'),
 'LL047': ('better measure of learning than recall immediately afterwards', ' at the end of the lecture'),
 'LL048': ('offering only smaller portions', ' to the exclusion of full size dishes'),
 'LL049': ('a source whose expertise has not been established', ' by anything the columnist offers'),
 'LL050': ('more expensive than the tools it would replace', ' across the whole engineering team'),
 'LL051': ('merely because no alternative has been proposed', ' by the critics who object to it'),
 'LL052': ('a claim about this measure in particular', ' without further support'),
 'LL053': ('the weight of each of its members', ' taken individually'),
 'LL054': ('evidence concerning the appearance of a street', ' ten years after the fact'),
 'LL055': ('occupied for at least two centuries', ' before the date of its abandonment'),
 'LL057': ('slightly more heavy goods traffic than the neighbouring spans', ' over the same period'),
 'LL060': ('a period of eighteen months rather than a full business cycle', ' in the industries concerned'),
 'LL061': ('because the review was favourable', ' to the book under discussion'),
}
E.extend(I, EXTEND2, 'EXTEND2')

# A third clause on sixteen items. Two passes took the best single-rank strategy from 71
# to 57; this takes it to the low forties, which is where the reading bank landed. The
# residual concentration is recorded in the header rather than chased further: ranking
# five options by character count is not something a reader does by eye, and the two
# tells that are visible, longest and shortest, are at 10 and 0 percent against a cap of
# 36.
EXTEND3 = {
 'LL031': ('the recommendation stated in the final sentence', ' about how the tax should be defended'),
 'LL032': ('no evidence about visitors who left early', ' or about where they went afterwards'),
 'LL033': ("the historian's own explanation of the decline", ' is incomplete in the same way'),
 'LL034': ('genuinely runs three academic calendars', ' rather than one with variations'),
 'LL036': ('applied a standard inconsistently across cases', ' covered by the style guide'),
 'LL037': ("Intermittent use extends a boiler's service life", ' by at least four months for every year of reduced operation'),
 'LL038': ('accepted other manuscripts written after 1600', ' by authors it already held'),
 'LL039': ('in any region with high rainfall', ', whatever the pattern of that rainfall'),
 'LL040': ('abstained rather than voting against', ' when the proposal was put'),
 'LL041': ('wait less time on average than patients with appointments', ' at the same clinic'),
 'LL043': ('the only measure by which a public investment should be judged', ' by a council'),
 'LL044': ('No painter other than Vasari used a ground of gesso over linen', ' on a panel of this kind'),
 'LL045': ('prefer the old packaging strongly enough to reduce sales', ' of the products it holds'),
 'LL046': ('operated in every region where waiting times fell', ' during the period studied'),
 'LL047': ('assigned to the two conditions rather than choosing between them', ' themselves'),
 'LL048': ('larger than most diners can finish', ' at a single sitting'),
}
E.extend(I, EXTEND3, 'EXTEND3')

E.measure(I)
E.write(sys.argv[1] if len(sys.argv) > 1 else 'src/bank_lsat_lr2.js',
        HEADER, [], I, 'BANK_LSAT_LR2', group_key='skill')
