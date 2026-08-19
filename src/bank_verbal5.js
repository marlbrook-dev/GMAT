// bank_verbal5.js - Start From Nowhere trainer, Verbal batch 5 (V241-V260, RC passage P8)
const RC_P8 = 'The standard account of the late twentieth century\'s expansion in world trade gives a starring role to the shipping container. Before containerization, general cargo was loaded and unloaded piece by piece by gangs of longshoremen, a process so slow and expensive that handling charges at the dock could amount to a substantial fraction of a good\'s delivered price. Standardized steel boxes allowed cargo to travel from a factory floor to a ship\'s hold with minimal handling, cutting the time a vessel spent in port from days to hours and sharply reducing theft, breakage, and the insurance premiums that reflected them. On this view, the container made distance cheap, and trade followed.\n\nSkeptics have questioned how much of the boom the container can rightly claim. Its adoption was gradual, spreading across major ports over two decades, while the steepest growth in trade coincided with successive rounds of tariff reduction, making the two influences difficult to separate. Published series of ocean freight rates, moreover, show no steep decline in the decades after the container\'s introduction, partly because savings at the dock were offset by the enormous capital costs of specialized ships, cranes, and chassis. For some economists, the container\'s principal contribution was therefore not lower cost but reliability: once sailing schedules became predictable, firms could confidently divide production among plants in different countries, timing shipments of components to arrive precisely when needed.\n\nRecent quantitative work has tried to settle the question by exploiting the staggered dates at which countries\' ports began handling containers. These studies generally find that containerization is associated with increases in trade between country pairs larger than those attributable to tariff cuts, though the gains emerge only after long lags and are concentrated where inland transportation and customs procedures were also modernized. That pattern suggests the original question was framed too narrowly. What mattered was not the box alone but the complementary investments and institutional adjustments the box invited.';

const BANK_VERBAL5 = [
  {
    id: 'V241', section: 'V', type: 'CR', skill: 'v_ac', diff: 2,
    stem: 'The Brightleaf chain of garden supply stores began keeping all of its locations open two hours later into the evening starting in March. Over the following quarter, the chain\'s revenue was 14 percent higher than in the same quarter of the previous year. The chain\'s management concluded that the extended evening hours were responsible for the increase in revenue.\n\nWhich of the following, if true, most seriously weakens the management\'s conclusion?',
    choices: [
      'Brightleaf\'s spending on staff wages increased when the stores began staying open later.',
      'Sales of garden supplies are subject to strong seasonal fluctuations over the course of a year.',
      'A regional competitor with stores near most Brightleaf locations went out of business in February.',
      'Several Brightleaf locations carry specialty products that no nearby retailer offers.',
      'Customer satisfaction surveys at Brightleaf showed no change after the extended hours were introduced.'
    ],
    answer: 2,
    expl: 'The argument attributes the revenue gain to the extended hours, but the closure of a nearby competitor supplies a compelling alternative explanation. If customers displaced by that closure shifted their purchases to Brightleaf, revenue could have risen 14 percent even if the hours had never changed. An alternative cause directly undermines the causal conclusion.',
    wrong: 'The other choices concern costs, product mix, satisfaction scores, or seasonal patterns that the year-over-year comparison already controls for. None offers a rival explanation for the revenue increase.'
  },
  {
    id: 'V242', section: 'V', type: 'CR', skill: 'v_ac', diff: 3,
    stem: 'Meridian Bottling currently makes its beverage bottles from a petroleum-based resin. A newly available plant-based resin costs 8 percent less per kilogram than the petroleum-based resin. Meridian therefore projects that switching to the plant-based resin will lower its total spending on bottle material.\n\nThe projection relies on which of the following assumptions?',
    choices: [
      'The plant-based resin is less harmful to the environment than the petroleum-based resin.',
      'Producing a bottle of acceptable quality from the plant-based resin does not require enough additional resin by weight to offset the lower price per kilogram.',
      'The price of the petroleum-based resin will rise over the next several years.',
      'Meridian\'s competitors have not yet begun using the plant-based resin in their own bottles.',
      'Consumers will be unable to detect any difference between bottles made from the two resins.'
    ],
    answer: 1,
    expl: 'The projection moves from a lower price per kilogram to lower total spending on material, which holds only if the amount of resin needed per bottle does not rise enough to cancel the savings. If each bottle required, say, 15 percent more of the cheaper resin, total spending would actually increase. The argument therefore depends on this assumption.',
    wrong: 'Environmental merit, future petroleum prices, competitors\' choices, and consumer perceptions bear on other business questions but are not required for the cost projection to follow.'
  },
  {
    id: 'V243', section: 'V', type: 'CR', skill: 'v_ac', diff: 3,
    stem: 'The city of Alder Grove plans to install solar panels on the roofs of its administrative buildings in order to reduce the amount it spends on electricity. The city will not install batteries, so any electricity the panels generate must be used at the moment it is produced or else be surrendered to the regional grid without compensation.\n\nWhich of the following, if true, provides the strongest support for the prediction that the plan will reduce the city\'s spending on electricity?',
    choices: [
      'Several nearby cities have installed solar panels on the roofs of schools and firehouses.',
      'Residents of Alder Grove have expressed strong support for renewable energy initiatives.',
      'The manufacturer of the panels offers an extended warranty at no additional charge.',
      'The administrative buildings consume the great majority of their electricity during daytime working hours, when the panels will be generating power.',
      'The panels can be installed without closing the administrative buildings to the public.'
    ],
    answer: 3,
    expl: 'Because unstored power is surrendered without payment, the plan saves money only if the buildings can use the electricity when it is generated. Establishing that consumption is concentrated in daylight hours shows that the solar output will displace electricity the city would otherwise purchase, which directly supports the prediction of lower spending.',
    wrong: 'Precedent in other cities, public support, a free warranty, and convenient installation say nothing about whether the generated power will actually offset the city\'s electricity purchases.'
  },
  {
    id: 'V244', section: 'V', type: 'CR', skill: 'v_ac', diff: 4,
    stem: 'A study of employees at a large insurance firm found that those who regularly used the stairs rather than the elevator missed 30 percent fewer workdays because of illness than those who rarely used the stairs. The study\'s authors concluded that regular stair use improves employees\' health and thereby reduces illness-related absences.\n\nWhich of the following, if true, most seriously weakens the authors\' conclusion?',
    choices: [
      'The firm\'s headquarters has only four floors, so climbing the stairs takes employees little time.',
      'Employees with chronic health conditions that cause frequent absences are often advised by their physicians to avoid climbing stairs.',
      'Some employees who regularly use the stairs do so mainly to avoid waiting for crowded elevators.',
      'Illness-related absence rates at the firm are lower overall than the national average for office workers.',
      'The study was conducted during a winter in which influenza was unusually widespread in the region.'
    ],
    answer: 1,
    expl: 'The argument infers that stair use causes better health, but the correct choice reverses the direction of causation. If employees already prone to illness-related absence avoid the stairs on medical advice, the frequently absent would cluster in the elevator group, producing the observed correlation without any health benefit from stair climbing.',
    wrong: 'Building height, employees\' motives for taking the stairs, the firm\'s overall absence rate, and the severity of the flu season do not bear on which way the causal arrow runs.'
  },
  {
    id: 'V245', section: 'V', type: 'CR', skill: 'v_ac', diff: 3,
    stem: 'Grain prices in the Redfield region are typically lowest at harvest, when supply peaks, and highest in late winter. The Redfield farmers\' cooperative plans to build storage silos so that its members can hold their grain after harvest and sell it in late winter instead. The cooperative predicts that the plan will increase members\' net income from grain sales.\n\nThe prediction depends on which of the following assumptions?',
    choices: [
      'Late-winter grain prices will be higher next year than they were last year.',
      'Every member of the cooperative will choose to store grain in the new silos.',
      'No other cooperative in the Redfield region currently operates storage silos.',
      'Storing grain over the winter will improve the quality of the grain.',
      'The cost of storing grain until late winter, including any losses from spoilage, will not equal or exceed the seasonal price premium members can expect to receive.'
    ],
    answer: 4,
    expl: 'Holding grain to capture the late-winter premium raises net income only if capturing that premium costs less than the premium itself. If storage fees and spoilage losses matched or exceeded the seasonal price difference, members would gain nothing or lose money, so the prediction cannot stand without this assumption.',
    wrong: 'Universal participation, year-over-year price levels, the absence of rival silos, and quality improvements are all stronger claims than, or different claims from, what the prediction requires.'
  },
  {
    id: 'V246', section: 'V', type: 'CR', skill: 'v_ac', diff: 5,
    stem: 'At Corven Bank, mortgage applications submitted through the bank\'s mobile app are approved at a rate of 74 percent, while applications submitted in person at branches are approved at a rate of 55 percent. Bank executives concluded that the app\'s automated document check, which flags incomplete or inconsistent paperwork before submission, causes app-based applications to be stronger than branch applications.\n\nWhich of the following, if true, most seriously undermines the executives\' conclusion?',
    choices: [
      'The automated document check occasionally flags paperwork that is in fact complete and consistent.',
      'Approval rates for both application channels have risen since the mobile app was introduced.',
      'Branch employees, whose performance is evaluated partly on application volume, routinely encourage customers to apply even when the customers\' finances make approval unlikely.',
      'Most customers who apply through the app are younger than most customers who apply at branches.',
      'The app allows applicants to save a partially completed application and finish it at a later time.'
    ],
    answer: 2,
    expl: 'The executives treat the approval gap as evidence that the document check strengthens applications, but the correct choice shows the two channels draw from different applicant pools. If branch staff solicit applications from customers with weak finances, the branch approval rate would be lower even if the document check had no effect whatsoever. The comparison therefore cannot establish the claimed cause.',
    wrong: 'Occasional false flags, a shared upward trend, an age difference with no stated link to creditworthiness, and a convenience feature all leave the selection problem untouched.'
  },
  {
    id: 'V247', section: 'V', type: 'CR', skill: 'v_pc', diff: 2,
    stem: 'Five years ago, the state widened Route 9 from four lanes to six in order to reduce rush-hour congestion. Today, average rush-hour travel times on Route 9 are longer than they were before the widening, even though the region\'s population has grown only slightly.\n\nWhich of the following, if true, most helps to explain the increase in travel times?',
    choices: [
      'The added capacity led many commuters who had previously used trains or parallel roads to begin driving on Route 9 instead.',
      'The widening project was completed on schedule and within its original budget.',
      'Speed limits on Route 9 were left unchanged after the widening was completed.',
      'Most drivers who use Route 9 during rush hour commute to jobs within the same metropolitan area.',
      'Several other highways in the state have also experienced increased congestion over the past five years.'
    ],
    answer: 0,
    expl: 'The puzzle is that added capacity coincided with slower trips despite little population growth. If the wider road drew drivers away from trains and parallel routes, traffic on Route 9 could have grown far faster than the population did, more than absorbing the two new lanes and lengthening travel times.',
    wrong: 'Budget performance, unchanged speed limits, commuting destinations, and congestion elsewhere supply no source of additional traffic on Route 9 itself.'
  },
  {
    id: 'V248', section: 'V', type: 'CR', skill: 'v_pc', diff: 3,
    stem: 'Over the past two years, the chemical plant on the Kestrel River has reduced its discharge of nitrates into the river by 40 percent, and no other facility discharges nitrates into the river. Yet monitoring stations downstream of the plant now record higher nitrate concentrations than they did two years ago.\n\nWhich of the following, if true, most helps to resolve the apparent discrepancy?',
    choices: [
      'The plant achieved its reduction in discharge by installing new filtration equipment.',
      'Nitrate concentrations upstream of the plant have remained at historically low levels.',
      'The plant now operates fewer hours per week than it did two years ago.',
      'A prolonged regional drought has reduced the river\'s flow to a small fraction of its former volume.',
      'Several species of fish have recently returned to stretches of the river upstream of the plant.'
    ],
    answer: 3,
    expl: 'Concentration depends on the amount of nitrate discharged and on the volume of water available to dilute it. If drought sharply reduced the river\'s flow, downstream concentrations could rise even though the total quantity discharged fell by 40 percent.',
    wrong: 'The other choices describe how the reduction was achieved or conditions that make the puzzle harder to explain, not a mechanism that reconciles lower discharge with higher readings.'
  },
  {
    id: 'V249', section: 'V', type: 'CR', skill: 'v_pc', diff: 4,
    stem: 'Two years ago, Halbrook Medical Center required its surgical teams to adopt a standardized safety checklist that controlled trials have shown to reduce surgical complications. Since the requirement took effect, the rate of complications recorded at Halbrook has risen by 20 percent.\n\nWhich of the following, if true, does most to explain the rise in Halbrook\'s recorded complication rate?',
    choices: [
      'Many of Halbrook\'s surgeons initially regarded the checklist as an unnecessary administrative burden.',
      'The checklist requires surgical teams to document minor complications that, before the requirement, went almost entirely unrecorded.',
      'The controlled trials of the checklist were conducted at hospitals considerably larger than Halbrook.',
      'Since adopting the checklist, Halbrook has performed a growing share of routine operations that carry the lowest risk of complications.',
      'Most complications recorded at Halbrook arise during patients\' recovery rather than during surgery itself.'
    ],
    answer: 1,
    expl: 'A recorded rate can climb because documentation improves even while actual outcomes hold steady or improve. If the checklist forces teams to log minor complications that previously went unrecorded, the 20 percent rise reflects a change in measurement rather than a decline in surgical safety, dissolving the apparent conflict with the trial evidence.',
    wrong: 'Initial resistance, differences in trial settings, a shift toward lower-risk operations, and the timing of complications might explain a failure to improve, but none accounts for an increase in what gets recorded.'
  },
  {
    id: 'V250', section: 'V', type: 'CR', skill: 'v_pc', diff: 4,
    stem: 'In the nation of Veldana, the average hourly wage paid in every individual industry rose last year. Nevertheless, the average hourly wage across the nation\'s economy as a whole was lower at the end of the year than at the beginning.\n\nWhich of the following, if true, most helps to explain how both of these statements could be true?',
    choices: [
      'Consumer prices in Veldana rose faster than wages did last year.',
      'Several Veldanan industries recorded their largest wage gains in more than a decade.',
      'Veldana\'s government raised the national minimum wage midway through the year.',
      'Union membership declined in several Veldanan industries last year.',
      'Employment expanded rapidly in low-wage industries while remaining flat in high-wage industries, shifting a larger share of the workforce into low-wage work.'
    ],
    answer: 4,
    expl: 'The economy-wide average is a weighted average of industry wages, with the weights set by each industry\'s share of total employment. If the workforce shifted toward low-wage industries, the overall average could fall even though every industry\'s own average rose. This composition effect reconciles the two statements.',
    wrong: 'Price inflation concerns purchasing power rather than the nominal average, and the remaining choices would tend to raise, not lower, the economy-wide figure.'
  },
  {
    id: 'V251', section: 'V', type: 'CR', skill: 'v_inf', diff: 1,
    stem: 'At Dunmore Community College, every student enrolled in the evening welding certificate program holds a full-time job. Some students enrolled in that program receive tuition reimbursement from their employers.\n\nIf the statements above are true, which of the following must also be true?',
    choices: [
      'Every student at Dunmore who holds a full-time job is enrolled in the evening welding certificate program.',
      'Most employers in the Dunmore area offer tuition reimbursement to their employees.',
      'Some students enrolled in the evening welding certificate program do not receive tuition reimbursement.',
      'At least some students who hold full-time jobs receive tuition reimbursement from their employers.',
      'Students who do not hold full-time jobs are prohibited from enrolling in the evening welding certificate program.'
    ],
    answer: 3,
    expl: 'Some students in the program receive tuition reimbursement, and every student in the program holds a full-time job. Those particular students are therefore full-time jobholders who receive reimbursement, so the conclusion follows directly from combining the two statements.',
    wrong: 'The other options reverse the stated relationship, generalize beyond the evidence, or treat a description of current enrollees as if it were an admission requirement.'
  },
  {
    id: 'V252', section: 'V', type: 'CR', skill: 'v_inf', diff: 3,
    stem: 'In Marston County, the total amount of electricity consumed by households declined between 2020 and 2025. Over the same period, the number of households in the county increased.\n\nIf the statements above are true, which of the following must also be true on the basis of them?',
    choices: [
      'Households in Marston County adopted more energy-efficient appliances between 2020 and 2025.',
      'The total amount of electricity consumed by businesses in Marston County also declined over the period.',
      'Average electricity consumption per household in Marston County was lower in 2025 than in 2020.',
      'Electricity prices in Marston County rose between 2020 and 2025.',
      'No individual household in Marston County consumed more electricity in 2025 than it did in 2020.'
    ],
    answer: 2,
    expl: 'Average consumption per household equals total household consumption divided by the number of households. With the numerator falling and the denominator rising, the average in 2025 must be lower than in 2020.',
    wrong: 'Explanations involving appliances or prices go beyond the stated figures, and the claims about businesses and about every individual household are not entailed by county-level totals.'
  },
  {
    id: 'V253', section: 'V', type: 'CR', skill: 'v_inf', diff: 4,
    stem: 'At Torvald Manufacturing, 20 percent of job applicants were invited to interview in 2023. In 2025, only 10 percent of job applicants were invited to interview, yet the number of applicants invited to interview was greater in 2025 than it was in 2023.\n\nWhich of the following conclusions is most strongly supported by the statements above?',
    choices: [
      'Torvald received more than twice as many job applications in 2025 as it did in 2023.',
      'Torvald hired more new employees in 2025 than it did in 2023.',
      'The overall quality of Torvald\'s applicant pool declined between 2023 and 2025.',
      'Torvald applied stricter standards when reviewing applications in 2025 than in 2023.',
      'Fewer invited applicants declined their interview invitations in 2025 than in 2023.'
    ],
    answer: 0,
    expl: 'Invitations equaled 20 percent of applications in 2023 and 10 percent of applications in 2025. For 10 percent of the 2025 total to exceed 20 percent of the 2023 total, the 2025 application count must be more than double the 2023 count. This follows arithmetically from the stated figures.',
    wrong: 'Hiring totals, applicant quality, review standards, and declination behavior all involve matters the statements never address.'
  },
  {
    id: 'V254', section: 'V', type: 'CR', skill: 'v_inf', diff: 3,
    stem: 'Novena Kitchenware repairs or replaces, free of charge, any of its products that is returned within two years of purchase. Last month, several Novena products were returned within two years of purchase, but Novena did not replace any products last month.\n\nIf the statements above are true, which of the following must be true?',
    choices: [
      'Novena\'s spending on repairs was unusually high last month.',
      'None of the Novena products returned last month was more than two years old.',
      'Novena has replaced at least some returned products in previous months.',
      'Most of the products returned to Novena last month required only minor repairs.',
      'Every Novena product returned within two years of purchase last month was repaired free of charge.'
    ],
    answer: 4,
    expl: 'The policy guarantees that any product returned within two years is either repaired or replaced. Several such products were returned last month and none was replaced, so each of them must have been repaired, and the policy specifies that the service is provided free of charge.',
    wrong: 'Repair spending, prior months\' replacements, the age of other returned items, and the severity of the repairs all lie outside what the two statements establish.'
  },
  {
    id: 'V255', section: 'V', type: 'RC', passageId: 'P8', passage: RC_P8, skill: 'v_st', diff: 3,
    stem: 'The primary purpose of the passage is to',
    choices: [
      'defend the standard account of containerization against criticism from skeptical economists',
      'trace a scholarly debate over the container\'s role in trade growth and identify what that debate reveals about how technologies produce economic effects',
      'argue that tariff reductions, rather than containerization, were the principal cause of the growth in world trade',
      'describe the technical innovations that transformed cargo handling during the twentieth century',
      'recommend policies for ports that are seeking to modernize their infrastructure'
    ],
    answer: 1,
    expl: 'The passage presents the standard account, the skeptics\' objections, and recent quantitative findings, then closes by reframing the issue: the container\'s power lay in the complementary investments and adjustments it invited. Choice B captures both the survey of the debate and the concluding lesson about technological change.',
    wrong: 'The passage neither defends one side outright nor credits tariffs over the container, and it is organized around a debate, not a technical history or a set of policy recommendations.'
  },
  {
    id: 'V256', section: 'V', type: 'RC', passageId: 'P8', passage: RC_P8, skill: 'v_st', diff: 3,
    stem: 'According to the passage, containerization reduced each of the following EXCEPT',
    choices: [
      'theft of cargo',
      'breakage of cargo',
      'the time vessels spent in port',
      'the amount of fuel consumed by cargo ships',
      'insurance premiums associated with shipping'
    ],
    answer: 3,
    expl: 'The first paragraph states that containers cut the time a vessel spent in port from days to hours and sharply reduced theft, breakage, and the insurance premiums that reflected them. Fuel consumption is never mentioned anywhere in the passage.',
    wrong: 'Each of the other four items appears explicitly in the first paragraph\'s list of the container\'s benefits.'
  },
  {
    id: 'V257', section: 'V', type: 'RC', passageId: 'P8', passage: RC_P8, skill: 'v_st', diff: 3,
    stem: 'According to the passage, some economists contend that the container\'s principal contribution to trade lay in',
    choices: [
      'a reduction in the capital costs of operating modern ports',
      'a decline in the insurance premiums charged to shippers',
      'the predictability of sailing schedules, which allowed firms to divide production across countries',
      'the elimination of the need for successive rounds of tariff reduction',
      'expanded employment opportunities for longshoremen at major ports'
    ],
    answer: 2,
    expl: 'The second paragraph reports that for some economists the container\'s principal contribution was not lower cost but reliability: predictable schedules let firms divide production among plants in different countries and time component shipments precisely. Choice C restates this position.',
    wrong: 'The passage says capital costs offset dock savings rather than falling, attributes insurance savings to the standard account rather than to the skeptics, and never links the container to tariff policy or to dockworker employment gains.'
  },
  {
    id: 'V258', section: 'V', type: 'RC', passageId: 'P8', passage: RC_P8, skill: 'v_inf', diff: 4,
    stem: 'The passage suggests that the trade gains identified by recent quantitative work would most likely have been smallest in a country that',
    choices: [
      'equipped its ports to handle containers but did not modernize its inland transportation or customs procedures',
      'reduced its tariffs during the same period in which its ports adopted containers',
      'began handling containers earlier than its major trading partners did',
      'conducted most of its trade with countries located nearby',
      'possessed unusually deep natural harbors before containerization began'
    ],
    answer: 0,
    expl: 'The third paragraph states that the gains from containerization are concentrated where inland transportation and customs procedures were also modernized, and the final sentence attributes the container\'s power to complementary investments and institutional adjustments. A country that adopted containers without those complements would therefore be expected to see the smallest gains.',
    wrong: 'Tariff timing, early adoption, trading partners\' proximity, and harbor depth are never identified as conditions that limited the container\'s measured effects.'
  },
  {
    id: 'V259', section: 'V', type: 'RC', passageId: 'P8', passage: RC_P8, skill: 'v_st', diff: 4,
    stem: 'The author mentions published series of ocean freight rates in the second paragraph primarily in order to',
    choices: [
      'show that the container was adopted more slowly than is commonly believed',
      'support the claim that trade agreements had little effect on the growth of trade',
      'challenge the idea that the container\'s benefits arrived chiefly through cheaper ocean transport',
      'demonstrate that ports failed to recover their investments in specialized ships and cranes',
      'establish that theft and breakage remained common even after containerization'
    ],
    answer: 2,
    expl: 'The freight-rate evidence appears amid the skeptics\' case: rates show no steep decline after the container\'s introduction, partly because dock savings were offset by capital costs. This detail undercuts the standard account\'s premise that the container made transport dramatically cheaper, which is exactly what choice C describes.',
    wrong: 'The pace of adoption is addressed by a different sentence, and the passage nowhere claims that trade agreements were ineffective, that port investments went unrecovered, or that theft and breakage persisted.'
  },
  {
    id: 'V260', section: 'V', type: 'RC', passageId: 'P8', passage: RC_P8, skill: 'v_inf', diff: 5,
    stem: 'It can be inferred that the author of the passage would be most likely to agree with which of the following statements about technological change?',
    choices: [
      'New transport technologies typically harm the economies that adopt them first.',
      'Quantitative estimates of a technology\'s economic effects are inherently unreliable.',
      'The container\'s effect on trade was ultimately smaller than that of tariff liberalization.',
      'The economic impact of a transport technology depends substantially on investments and institutional adjustments beyond the technology itself.',
      'Scholarly debates about economic causation rarely yield conclusions of practical value.'
    ],
    answer: 3,
    expl: 'The author concludes that the original question was framed too narrowly and that what mattered was not the box alone but the complementary investments and institutional adjustments it invited. This generalizes directly to the statement in choice D about technologies requiring complements to produce economic effects.',
    wrong: 'The author cites the quantitative work approvingly, reports that containerization\'s association with trade exceeded that of tariff cuts, and treats the scholarly debate as illuminating rather than futile.'
  }
];
