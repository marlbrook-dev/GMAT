// Start From Nowhere trainer - GMAT Focus Data Insights bank 5 (D241-D260), original items.

const DS_CHOICES5 = [
  'Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.',
  'Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.',
  'BOTH statements TOGETHER are sufficient, but NEITHER statement alone is sufficient.',
  'EACH statement ALONE is sufficient.',
  'Statements (1) and (2) TOGETHER are NOT sufficient.'
];

const GT_TABLE9 = '<table class="dtable"><thead><tr><th>Airline</th><th>Scheduled Flights</th><th>On-Time Arrivals</th><th>Cancelled Flights</th><th>Average Delay (min)</th></tr></thead><tbody>'+
  '<tr><td>Arrow Air</td><td>500</td><td>425</td><td>10</td><td>18</td></tr>'+
  '<tr><td>BlueJet</td><td>400</td><td>348</td><td>12</td><td>24</td></tr>'+
  '<tr><td>CloudLine</td><td>250</td><td>205</td><td>5</td><td>30</td></tr>'+
  '<tr><td>DriftAir</td><td>600</td><td>510</td><td>15</td><td>15</td></tr>'+
  '<tr><td>EastPeak</td><td>350</td><td>287</td><td>14</td><td>21</td></tr>'+
  '</tbody></table><p class="dnote">March operations for five regional airlines; every scheduled flight either operated or was cancelled, and the average delay covers only operated flights that arrived late.</p>';

const GT_TABLE10 = '<table class="dtable"><thead><tr><th>Solar Farm</th><th>Capacity (MW)</th><th>First Half Output (MWh)</th><th>Second Half Output (MWh)</th><th>Operating Cost per MWh ($)</th></tr></thead><tbody>'+
  '<tr><td>Brightfield</td><td>20</td><td>16,000</td><td>20,000</td><td>30</td></tr>'+
  '<tr><td>Copper Mesa</td><td>50</td><td>45,000</td><td>43,200</td><td>25</td></tr>'+
  '<tr><td>Duneview</td><td>10</td><td>9,000</td><td>10,800</td><td>40</td></tr>'+
  '<tr><td>Larkspur</td><td>40</td><td>30,000</td><td>36,000</td><td>32</td></tr>'+
  '<tr><td>Saltgrass</td><td>25</td><td>20,000</td><td>25,000</td><td>28</td></tr>'+
  '</tbody></table><p class="dnote">Nameplate capacity, half-year electricity output, and operating cost per megawatt hour for five solar farms last year.</p>';

const BANK_DI5 = [
  {
    id: 'D241', section: 'DI', type: 'DS', domain: 'algebra', skill: 'di_ds', qskill: 'linear_equations', diff: 2,
    stem: 'What is the value of x?\n\n(1) 3x + 6 = 21\n\n(2) 4x - 9 = 11',
    choices: DS_CHOICES5, answer: 3,
    expl: 'Statement (1): 3x + 6 = 21 gives 3x = 15, so x = 5. Sufficient. Statement (2): 4x - 9 = 11 gives 4x = 20, so x = 5. Sufficient. Each statement alone pins down a single value, so the answer is D.',
    wrong: 'Choosing C by assuming both linear equations are needed; each one alone already yields exactly one value of x.'
  },
  {
    id: 'D242', section: 'DI', type: 'DS', domain: 'arithmetic', skill: 'di_ds', qskill: 'ratios', diff: 3,
    stem: 'A jar contains only red marbles and green marbles. What fraction of the marbles in the jar are red?\n\n(1) The ratio of red marbles to green marbles in the jar is 3 to 5.\n\n(2) The jar contains 12 more green marbles than red marbles.',
    choices: DS_CHOICES5, answer: 0,
    expl: 'Statement (1): if red to green is 3 to 5, red marbles are 3 parts out of 8 total parts, so the fraction is 3/8 no matter how many marbles there are. Sufficient. Statement (2): green = red + 12 gives fraction red/(2 x red + 12), which is 1/4 when red = 6 but 1/3 when red = 12. Not sufficient. Answer A.',
    wrong: 'Picking C or E on the belief that a ratio cannot fix a fraction without actual counts; a part-to-part ratio fully determines the part-to-whole fraction.'
  },
  {
    id: 'D243', section: 'DI', type: 'DS', domain: 'arithmetic', skill: 'di_ds', qskill: 'word_problems', diff: 3,
    stem: 'The total cost of a restaurant meal was split evenly among the members of a dinner group, with each member paying a whole number of dollars. How many members were in the group?\n\n(1) Each member paid exactly 15 dollars.\n\n(2) The total cost of the meal was less than 100 dollars.',
    choices: DS_CHOICES5, answer: 4,
    expl: 'Statement (1): the total is 15 x n, but n itself is unknown. Not sufficient. Statement (2): a cap on the total says nothing about the number of members. Not sufficient. Together: 15 x n < 100 allows n = 2, 3, 4, 5, or 6, so several group sizes remain possible. Answer E.',
    wrong: 'Choosing C because combining gives a bound; a bound that still allows n from 2 through 6 is not a unique value.'
  },
  {
    id: 'D244', section: 'DI', type: 'DS', domain: 'arithmetic', skill: 'di_ds', qskill: 'overlapping_sets', diff: 3,
    stem: 'How many students in a certain music program play both piano and violin?\n\n(1) In the program, 18 students play piano and 14 students play violin.\n\n(2) In the program, exactly 25 students play piano, violin, or both.',
    choices: DS_CHOICES5, answer: 2,
    expl: 'Statement (1) gives the two group sizes but no link between them, so the overlap could be anything from 0 to 14. Not sufficient. Statement (2) gives only the union. Not sufficient. Together: both = 18 + 14 - 25 = 7. Sufficient, so the answer is C.',
    wrong: 'Picking E because total program enrollment is never given; the union count in statement (2) is all that the overlap formula needs.'
  },
  {
    id: 'D245', section: 'DI', type: 'DS', domain: 'rates', skill: 'di_ds', qskill: 'work_rate', diff: 4,
    stem: 'Machines X and Y, working together at their constant rates, filled a production order. How many hours would machine Y take to fill the order working alone at its constant rate?\n\n(1) Working alone at its constant rate, machine X would take 6 hours to fill the order.\n\n(2) Working together, the two machines filled the order in 2 hours, and the rate of machine Y is twice the rate of machine X.',
    choices: DS_CHOICES5, answer: 1,
    expl: 'Statement (1) describes only machine X. Not sufficient. Statement (2): let the rate of X be r orders per hour, so the rate of Y is 2r and r + 2r = 1/2, giving r = 1/6 and the Y rate 1/3; machine Y alone takes 3 hours. Sufficient. Answer B.',
    wrong: 'Choosing C from the habit that work problems need both statements; statement (2) already contains a complete two-equation system.'
  },
  {
    id: 'D246', section: 'DI', type: 'DS', domain: 'logic', skill: 'di_ds', diff: 4,
    stem: 'A city ordinance states that a food truck may park overnight in the market square only if the truck holds both a current vending permit and a current fire safety certificate. Is food truck T permitted to park overnight in the market square?\n\n(1) Truck T holds a current vending permit but has never applied for a fire safety certificate.\n\n(2) Truck T holds a current fire safety certificate.',
    choices: DS_CHOICES5, answer: 0,
    expl: 'Statement (1): a truck that never applied for a fire safety certificate cannot hold one, so truck T fails a required condition and is definitely not permitted. A definite No answers the question, so (1) is sufficient. Statement (2): the certificate is only one of the two requirements, and the permit status is unknown, so the answer could be Yes or No. Not sufficient. Answer A.',
    wrong: 'Rejecting statement (1) because it leads to a No; sufficiency requires a definite answer, not a Yes.'
  },
  {
    id: 'D247', section: 'DI', type: 'DS', domain: 'number properties', skill: 'di_ds', qskill: 'number_properties', diff: 5,
    stem: 'Is the positive integer n a perfect square?\n\n(1) n is divisible by 4.\n\n(2) n has an odd number of positive divisors.',
    choices: DS_CHOICES5, answer: 1,
    expl: 'Statement (1): n = 4 is a perfect square but n = 8 is not, and both are divisible by 4. Not sufficient. Statement (2): divisors pair up as d with n/d, and the pairing leaves an unmatched divisor exactly when some d equals n/d, that is, when n = d^2. So an odd divisor count occurs only for perfect squares, giving a definite Yes. Sufficient. Answer B.',
    wrong: 'Choosing C or E by not recalling that a positive integer has an odd number of divisors exactly when it is a perfect square.'
  },
  {
    id: 'D248', section: 'DI', type: 'DS', domain: 'logic', skill: 'di_ds', diff: 4,
    stem: 'Five consultants, including Baker, Chen, and Ortiz, each gave exactly one presentation last week, on five different days, Monday through Friday. Did Ortiz present on an earlier day than Chen?\n\n(1) Ortiz presented on an earlier day than Baker.\n\n(2) Baker presented on an earlier day than Chen.',
    choices: DS_CHOICES5, answer: 2,
    expl: 'Statement (1) alone: Chen is unrestricted, so Chen could fall before or after Ortiz. Not sufficient. Statement (2) alone: Ortiz is unrestricted. Not sufficient. Together: Ortiz was earlier than Baker and Baker was earlier than Chen, so Ortiz was earlier than Chen, a definite Yes. Answer C.',
    wrong: 'Picking E because the exact days are never fixed; the question asks only for the order of two people, which the combined chain settles.'
  },
  {
    id: 'D249', section: 'DI', type: 'GT', domain: 'data analysis', skill: 'di_gt', qskill: 'percent', diff: 2,
    stem: GT_TABLE9 + '\n\nBased on the table, which airline had the highest percentage of its scheduled flights arrive on time in March?',
    choices: ['Arrow Air', 'BlueJet', 'CloudLine', 'DriftAir', 'EastPeak'],
    answer: 1,
    expl: 'On-time rates: Arrow Air 425/500 = 85 percent, BlueJet 348/400 = 87 percent, CloudLine 205/250 = 82 percent, DriftAir 510/600 = 85 percent, EastPeak 287/350 = 82 percent. BlueJet is highest at 87 percent.',
    wrong: 'Choosing DriftAir for having the most on-time arrivals in absolute terms; the question asks for a percentage of scheduled flights.'
  },
  {
    id: 'D250', section: 'DI', type: 'GT', domain: 'data analysis', skill: 'di_gt', qskill: 'arithmetic', diff: 3,
    stem: GT_TABLE9 + '\n\nAccording to the table, how many DriftAir flights operated in March but did not arrive on time?',
    choices: ['60', '75', '85', '90', '105'],
    answer: 1,
    expl: 'Every scheduled flight either operated or was cancelled, so DriftAir operated 600 - 15 = 585 flights. Of those, 510 arrived on time, leaving 585 - 510 = 75 operated flights that were late.',
    wrong: '90 comes from 600 - 510, which forgets to remove the 15 cancelled flights that never operated at all.'
  },
  {
    id: 'D251', section: 'DI', type: 'GT', domain: 'data analysis', skill: 'di_gt', qskill: 'arithmetic', diff: 4,
    stem: GT_TABLE9 + '\n\nFor each airline, define total delay minutes as the number of operated flights that arrived late multiplied by that airline\'s average delay. Which airline had the greatest total delay minutes in March?',
    choices: ['Arrow Air', 'BlueJet', 'CloudLine', 'DriftAir', 'EastPeak'],
    answer: 2,
    expl: 'Late operated flights are scheduled minus on-time minus cancelled. Arrow Air: 65 x 18 = 1170. BlueJet: 40 x 24 = 960. CloudLine: 40 x 30 = 1200. DriftAir: 75 x 15 = 1125. EastPeak: 49 x 21 = 1029. CloudLine has the greatest total, 1200 minutes.',
    wrong: 'Choosing DriftAir for having the most late flights (75) or BlueJet for a long average delay; the product, not either factor alone, decides it.'
  },
  {
    id: 'D252', section: 'DI', type: 'GT', domain: 'data analysis', skill: 'di_gt', qskill: 'arithmetic', diff: 1,
    stem: GT_TABLE10 + '\n\nAccording to the table, which solar farm produced less electricity in the second half of the year than in the first half?',
    choices: ['Brightfield', 'Copper Mesa', 'Duneview', 'Larkspur', 'Saltgrass'],
    answer: 1,
    expl: 'Only Copper Mesa declined: 43,200 MWh in the second half versus 45,000 MWh in the first half. The other four farms all increased their output.',
    wrong: 'Misreading the two output columns and comparing a farm against a different row.'
  },
  {
    id: 'D253', section: 'DI', type: 'GT', domain: 'data analysis', skill: 'di_gt', qskill: 'ratios', diff: 3,
    stem: GT_TABLE10 + '\n\nBased on the table, the full-year output of Larkspur, in MWh per MW of capacity, was closest to which of the following?',
    choices: ['1,500', '1,600', '1,650', '1,750', '1,800'],
    answer: 2,
    expl: 'Larkspur produced 30,000 + 36,000 = 66,000 MWh over the year, with 40 MW of capacity. 66,000 / 40 = 1,650 MWh per MW.',
    wrong: '1,500 comes from using only the first-half output twice, and 1,800 from using only the second-half output twice.'
  },
  {
    id: 'D254', section: 'DI', type: 'GT', domain: 'data analysis', skill: 'di_gt', qskill: 'arithmetic', diff: 4,
    stem: GT_TABLE10 + '\n\nDefine second-half operating cost as second-half output multiplied by operating cost per MWh. According to the table, which farm had the greatest second-half operating cost?',
    choices: ['Brightfield', 'Copper Mesa', 'Duneview', 'Larkspur', 'Saltgrass'],
    answer: 3,
    expl: 'Brightfield: 20,000 x 30 = 600,000. Copper Mesa: 43,200 x 25 = 1,080,000. Duneview: 10,800 x 40 = 432,000. Larkspur: 36,000 x 32 = 1,152,000. Saltgrass: 25,000 x 28 = 700,000. Larkspur is greatest at 1,152,000 dollars.',
    wrong: 'Choosing Copper Mesa for the largest output or Duneview for the highest per-MWh cost; the totals must actually be multiplied out.'
  },
  {
    id: 'D255', section: 'DI', type: 'TPA', domain: 'algebra', skill: 'di_tpa', qskill: 'linear_equations', diff: 2,
    stem: 'A harbor ferry sells adult tickets for 8 dollars each and child tickets for 5 dollars each. One afternoon a tour group bought 10 tickets for a total of 62 dollars.\n\nSelect the number of adult tickets and the number of child tickets the group bought. Make only two selections, one in each column.',
    answerType: 'tpa',
    columns: ['Adult tickets', 'Child tickets'],
    choices: ['2', '3', '4', '5', '6', '7'],
    answer: [2, 4],
    expl: 'With a adult tickets, 8a + 5(10 - a) = 62, so 3a + 50 = 62 and a = 4, leaving 6 child tickets. Check: 4 x 8 + 6 x 5 = 32 + 30 = 62 dollars.',
    wrong: 'Swapping the columns to 6 adults and 4 children gives 48 + 20 = 68 dollars, which is too much.'
  },
  {
    id: 'D256', section: 'DI', type: 'TPA', domain: 'arithmetic', skill: 'di_tpa', qskill: 'ratios', diff: 3,
    stem: 'A landscaping crew ordered a total of 90 shrubs, each either a holly or a juniper. After the crew planted 15 of the holly shrubs and 15 of the juniper shrubs, the ratio of unplanted holly shrubs to unplanted juniper shrubs was 2 to 3.\n\nSelect the number of holly shrubs ordered and the number of juniper shrubs ordered. Make only two selections, one in each column.',
    answerType: 'tpa',
    columns: ['Holly shrubs ordered', 'Juniper shrubs ordered'],
    choices: ['24', '36', '39', '45', '51', '54'],
    answer: [2, 4],
    expl: 'Let h and j be the ordered counts, h + j = 90 and 3(h - 15) = 2(j - 15). The second gives 3h - 2j = 15; substituting j = 90 - h gives 5h = 195, so h = 39 and j = 51. Check: unplanted counts are 24 and 36, and 24 to 36 is 2 to 3.',
    wrong: '24 and 36 are the unplanted counts, not the ordered counts; the question asks for the original order.'
  },
  {
    id: 'D257', section: 'DI', type: 'TPA', domain: 'critical reasoning', skill: 'di_tpa', diff: 3,
    stem: 'A city plans to replace the always-on fixed lights in its parking garage with motion sensor lights and predicts that the change will lower the electricity cost of lighting the garage, because the new lights will run only when a person or vehicle is present.\n\nSelect for Strengthen the statement that, if true, most strengthens the prediction, and select for Weaken the statement that, if true, most weakens it. Make only two selections, one in each column.',
    answerType: 'tpa',
    columns: ['Strengthen', 'Weaken'],
    choices: [
      'Overnight security recordings show that on most nights no one enters the garage between 1 a.m. and 5 a.m.',
      'The new lights produce the same brightness as the fixed lights they replace.',
      'Several nearby cities use motion sensor lights in their public libraries.',
      'The upfront cost of installing the new lights will be paid from a federal grant.',
      'Each time a sensor light switches on it draws a surge of power that cancels the savings from any off period shorter than an hour, and vehicles enter the garage every few minutes around the clock.',
      'Electricity rates in the region are expected to remain unchanged for the next decade.'
    ],
    answer: [0, 4],
    expl: 'The prediction depends on the lights actually being off for meaningful stretches. Long empty periods every night (choice 0) mean real off time and real savings, strengthening the prediction. Constant traffic plus a surge that wipes out savings for short off periods (choice 4) means the new lights could cost as much or more, weakening it. The other choices concern brightness, other cities, installation funding, and rate stability, none of which bears on whether usage-based lighting cuts this electricity cost.',
    wrong: 'Choice 3 tempts as a strengthener, but it addresses installation funding, not the electricity cost the prediction is about.'
  },
  {
    id: 'D258', section: 'DI', type: 'TPA', domain: 'rates', skill: 'di_tpa', qskill: 'rates', diff: 3,
    stem: 'Two cyclists start at the same time from towns 84 miles apart and ride toward each other along the same road, each at a constant speed. The faster cyclist rides 3 miles per hour faster than the slower cyclist, and they meet after exactly 4 hours.\n\nSelect the speed, in miles per hour, of the slower cyclist and of the faster cyclist. Make only two selections, one in each column.',
    answerType: 'tpa',
    columns: ['Slower cyclist (mph)', 'Faster cyclist (mph)'],
    choices: ['6', '8', '9', '12', '14', '15'],
    answer: [2, 3],
    expl: 'They close 84 miles in 4 hours, so their combined speed is 84 / 4 = 21 mph. With slower speed s, s + (s + 3) = 21 gives s = 9, and the faster cyclist rides 12 mph. Check: 4 x (9 + 12) = 84 miles.',
    wrong: 'Pairs like 9 and 15 or 6 and 9 either break the 3 mph gap or fail to sum to the required 21 mph combined speed.'
  },
  {
    id: 'D259', section: 'DI', type: 'TPA', domain: 'number properties', skill: 'di_tpa', qskill: 'number_properties', diff: 5,
    stem: 'At a charity auction, every painting sold for exactly 250 dollars and every sculpture sold for exactly 400 dollars. The paintings and sculptures together brought in exactly 4300 dollars, at least one of each type was sold, and more paintings than sculptures were sold.\n\nSelect the number of paintings sold and the number of sculptures sold. Make only two selections, one in each column.',
    answerType: 'tpa',
    columns: ['Paintings', 'Sculptures'],
    choices: ['2', '6', '7', '10', '14', '16'],
    answer: [4, 0],
    expl: 'The revenue equation 250p + 400s = 4300 reduces to 5p + 8s = 86. Then 8s must leave remainder 1 when 86 - 8s is checked against 5, which forces s = 2 or s = 7 in range: s = 2 gives p = 14, and s = 7 gives p = 6. Only p = 14, s = 2 satisfies more paintings than sculptures. Check: 14 x 250 + 2 x 400 = 3500 + 800 = 4300 dollars.',
    wrong: 'p = 6 and s = 7 also matches the revenue exactly but violates the condition that more paintings than sculptures were sold.'
  },
  {
    id: 'D260', section: 'DI', type: 'TPA', domain: 'rates', skill: 'di_tpa', qskill: 'work_rate', diff: 4,
    stem: 'Working alone at a constant rate of 25 pages per hour, editor A can proofread a certain manuscript in 12 hours. When editor A and editor B work on the manuscript together, each at a constant rate, they finish it in exactly 4 hours.\n\nSelect the number of hours editor B would need to proofread the manuscript alone and the rate of editor B in pages per hour. Make only two selections, one in each column.',
    answerType: 'tpa',
    columns: ['Hours for editor B alone', 'Editor B pages per hour'],
    choices: ['5', '6', '8', '40', '50', '60'],
    answer: [1, 4],
    expl: 'The manuscript has 25 x 12 = 300 pages. Finishing together in 4 hours means a combined rate of 300 / 4 = 75 pages per hour, so the rate of editor B is 75 - 25 = 50 pages per hour, and alone editor B needs 300 / 50 = 6 hours. Check: 1/12 + 1/6 = 1/4 of the job per hour.',
    wrong: '8 hours comes from subtracting 4 from 12, and 60 pages per hour from dividing 300 by 5; both skip the combined-rate step.'
  }
];

