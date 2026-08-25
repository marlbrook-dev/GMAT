// bank_di7.js - Original GMAT Focus Data Insights items D269-D289: MSR set 4, TA, GI, GT, TPA, DS
const MSR_RAIL1 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Fare rules (Harborview Regional Rail)</h4><ul>'+
 '<li>Off-peak tickets are valid on weekdays from 9:30 to 15:30 and after 19:00, and all day on weekends.</li>'+
 '<li>A SaverPass gives 30 percent off off-peak fares only. SaverPass fares are nonrefundable.</li>'+
 '<li>Children under 5 travel free with a fare-paying adult, at most 2 free children per adult; each additional child under 5 pays half the adult fare.</li>'+
 '<li>Bicycles require a bicycle reservation on InterCity trains. Bicycles are not carried on Commuter trains at any time.</li>'+
 '<li>Unused non-SaverPass tickets are refundable within 30 days of purchase, minus a 5 dollar processing fee.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: One-way fares (dollars)</h4><table class="dtable"><thead><tr><th>Route</th><th>Commuter</th><th>InterCity</th></tr></thead><tbody>'+
 '<tr><td>Harborview to Milldale</td><td>8.50</td><td>14.00</td></tr>'+
 '<tr><td>Harborview to Kings Cross</td><td>not served</td><td>22.00</td></tr>'+
 '<tr><td>Milldale to Northgate</td><td>6.00</td><td>10.50</td></tr>'+
 '<tr><td>Harborview to Northgate</td><td>12.00</td><td>18.00</td></tr>'+
 '</tbody></table></div>'+
 '<div class="msrtab"><h4>Tab 3: Email to the fare desk</h4><p>I am traveling this Wednesday from Harborview to a 14:00 meeting in Milldale, and I will bring my bicycle. I hold a SaverPass. What is the least I can pay for the one-way trip, assuming I depart after 9:30?</p></div></div>';
const TA_TRUCKS1 = '<table class="dtable"><thead><tr><th>Truck</th><th>Cuisine</th><th>Days on site per week</th><th>Average daily customers</th><th>Average ticket ($)</th></tr></thead><tbody>'+
 '<tr><td>Aroma</td><td>Thai</td><td>5</td><td>140</td><td>12</td></tr>'+
 '<tr><td>Brava</td><td>Tacos</td><td>6</td><td>180</td><td>9</td></tr>'+
 '<tr><td>Cinder</td><td>Barbecue</td><td>4</td><td>110</td><td>15</td></tr>'+
 '<tr><td>Dosa Bar</td><td>Indian</td><td>5</td><td>150</td><td>11</td></tr>'+
 '<tr><td>Ember</td><td>Burgers</td><td>6</td><td>160</td><td>10</td></tr>'+
 '</tbody></table><p class="dnote">Food trucks operating at a corporate campus. Daily revenue = average daily customers x average ticket; weekly revenue = daily revenue x days on site.</p>';
const GT_LIBRARY1 = '<table class="dtable"><thead><tr><th>Branch</th><th>Weekly visitors</th><th>Items loaned weekly</th><th>E-loans (% of items loaned)</th></tr></thead><tbody>'+
 '<tr><td>Askern</td><td>2,400</td><td>3,600</td><td>25</td></tr>'+
 '<tr><td>Belford</td><td>3,200</td><td>4,000</td><td>30</td></tr>'+
 '<tr><td>Crane</td><td>1,800</td><td>2,880</td><td>40</td></tr>'+
 '<tr><td>Derwent</td><td>2,600</td><td>3,380</td><td>20</td></tr>'+
 '<tr><td>Elmswell</td><td>3,000</td><td>4,200</td><td>35</td></tr>'+
 '</tbody></table><p class="dnote">Five branches of a county library system, weekly averages. E-loans are included in items loaned.</p>';
const GI_APPUSERS1 = '<div class="dchart"><svg viewBox="0 0 420 220" width="100%" style="max-width:520px"><g font-family="Manrope,Inter,Arial" font-size="12">'+
 '<line x1="50" y1="180" x2="400" y2="180" stroke="#888"/><line x1="50" y1="20" x2="50" y2="180" stroke="#888"/>'+
 '<line x1="50" y1="140" x2="400" y2="140" stroke="#eee"/><line x1="50" y1="100" x2="400" y2="100" stroke="#eee"/><line x1="50" y1="60" x2="400" y2="60" stroke="#eee"/><line x1="50" y1="20" x2="400" y2="20" stroke="#eee"/>'+
 '<text x="44" y="184" text-anchor="end" fill="#666">0</text><text x="44" y="144" text-anchor="end" fill="#666">20</text><text x="44" y="104" text-anchor="end" fill="#666">40</text><text x="44" y="64" text-anchor="end" fill="#666">60</text><text x="44" y="24" text-anchor="end" fill="#666">80</text>'+
 '<rect x="62" y="96" width="38" height="84" fill="#2563EB"/><text x="81" y="198" text-anchor="middle">Mar</text><text x="81" y="90" text-anchor="middle" fill="#333">42</text>'+
 '<rect x="118" y="84" width="38" height="96" fill="#2563EB"/><text x="137" y="198" text-anchor="middle">Apr</text><text x="137" y="78" text-anchor="middle" fill="#333">48</text>'+
 '<rect x="174" y="90" width="38" height="90" fill="#2563EB"/><text x="193" y="198" text-anchor="middle">May</text><text x="193" y="84" text-anchor="middle" fill="#333">45</text>'+
 '<rect x="230" y="60" width="38" height="120" fill="#2563EB"/><text x="249" y="198" text-anchor="middle">Jun</text><text x="249" y="54" text-anchor="middle" fill="#333">60</text>'+
 '<rect x="286" y="66" width="38" height="114" fill="#2563EB"/><text x="305" y="198" text-anchor="middle">Jul</text><text x="305" y="60" text-anchor="middle" fill="#333">57</text>'+
 '<rect x="342" y="48" width="38" height="132" fill="#2563EB"/><text x="361" y="198" text-anchor="middle">Aug</text><text x="361" y="42" text-anchor="middle" fill="#333">66</text>'+
 '</g></svg><p class="dnote">Monthly active users of a study app, in thousands.</p></div>';
const BANK_DI7 = [
{id:'D269',section:'DI',type:'MSR',domain:'math',skill:'di_msr',qskill:'q_rrp',diff:3,passageHtml:MSR_RAIL1,
 stem:'What is the least the emailer in Tab 3 can pay for the one-way trip described?',
 choices:['5.95 dollars','8.50 dollars','9.80 dollars','12.60 dollars','14.00 dollars'],answer:2,
 expl:'The bicycle rules out Commuter trains entirely, so the emailer needs the InterCity fare of 14.00 with a bicycle reservation. Departing after 9:30 on a weekday is off-peak, so the SaverPass applies: 14.00 x 0.7 = 9.80.',
 wrong:'5.95 applies the discount to the Commuter fare, but no bicycle may board a Commuter train; 12.60 uses a 10 percent discount instead of 30.'},
{id:'D270',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:3,passageHtml:MSR_RAIL1,
 stem:'A traveler bought an off-peak SaverPass ticket last week but no longer needs it. Under the rules, what refund is the traveler entitled to?',
 choices:['Nothing','The fare minus a 5 dollar fee','The full fare','5 dollars','The fare minus 30 percent'],answer:0,
 expl:'SaverPass fares are nonrefundable, so the refund is nothing. The 30-day, minus-5-dollars rule applies only to non-SaverPass tickets.',
 wrong:'Applying the general refund rule to a SaverPass fare is the intended trap; the SaverPass clause overrides it.'},
{id:'D271',section:'DI',type:'MSR',domain:'math',skill:'di_msr',qskill:'q_rrp',diff:4,passageHtml:MSR_RAIL1,
 stem:'On a Saturday, one adult without a SaverPass travels from Milldale to Northgate on a Commuter train with three children, all under 5. What total fare does the group pay?',
 choices:['6.00 dollars','7.50 dollars','9.00 dollars','12.00 dollars','4.20 dollars'],answer:2,
 expl:'The adult pays the 6.00 Commuter fare. Two children ride free with the fare-paying adult; the third pays half the adult fare, 3.00. Total 9.00.',
 wrong:'Forgetting the two-free-children cap gives 6.00; charging all three children half fare gives 15.00, not offered, while 12.00 treats one child as full fare.'},
{id:'D272',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_RAIL1,
 stem:'Which of the following trips is NOT permitted under the rules?',
 choices:['An InterCity trip from Harborview to Milldale with a reserved bicycle','A Commuter trip from Milldale to Northgate with a bicycle','A weekend Commuter trip from Harborview to Northgate on a SaverPass off-peak fare','An InterCity trip from Harborview to Kings Cross without a bicycle','A weekday 10:00 off-peak Commuter trip from Harborview to Milldale'],answer:1,
 expl:'Bicycles are not carried on Commuter trains at any time, so the Milldale to Northgate Commuter trip with a bicycle is not permitted. Each other trip satisfies the rules: reserved bicycles ride InterCity, weekends are off-peak all day, and 10:00 falls inside the weekday off-peak window.',
 wrong:'Kings Cross is unreachable by Commuter train, but choice D uses InterCity, which serves it.'},
{id:'D273',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:TA_TRUCKS1,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'The median of the five trucks\' average daily customers is 150.',answer:true},
  {text:'The truck with the highest average ticket is on site the fewest days per week.',answer:true},
  {text:'Brava has the highest daily revenue of the five trucks.',answer:false}],
 expl:'Customers sorted: 110, 140, 150, 160, 180; the median is 150 (Yes). Cinder has the highest ticket, 15 dollars, and the fewest days, 4 (Yes). Daily revenues: Aroma 1680, Brava 1620, Cinder 1650, Dosa Bar 1650, Ember 1600; Aroma leads, not Brava (No).',
 wrong:'Brava has the most customers, but revenue multiplies customers by ticket, and its 9 dollar ticket drags it below Aroma.'},
{id:'D274',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,passageHtml:TA_TRUCKS1,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'Ember\'s weekly revenue exceeds Cinder\'s weekly revenue.',answer:true},
  {text:'Exactly two trucks have weekly revenue above 9,000 dollars.',answer:true},
  {text:'If Cinder added a fifth day on site at its current daily averages, its weekly revenue would exceed Dosa Bar\'s.',answer:false}],
 expl:'Weekly revenues: Aroma 8400, Brava 9720, Cinder 6600, Dosa Bar 8250, Ember 9600. Ember 9600 beats Cinder 6600 (Yes). Above 9000: Brava and Ember only (Yes). Cinder at five days would earn 5 x 1650 = 8250, equal to Dosa Bar, not more (No).',
 wrong:'Equal is not exceeds; statement 3 turns on that edge.'},
{id:'D275',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:GI_APPUSERS1,answerType:'gi',
 stem:'The bar chart shows monthly active users of a study app, in thousands, for March through August. Complete each statement using the drop-down options.',
 statements:[
  {text:'Compared with the preceding month, the largest increase in active users occurred in ____.',options:['April','June','July','August'],answer:1},
  {text:'The median of the six monthly values is ____ thousand.',options:['48','52.5','54','57'],answer:1}],
 expl:'Month-over-month changes: April +6, May -3, June +15, July -3, August +9; the largest increase is June. Sorted values 42, 45, 48, 57, 60, 66; the median is (48 + 57) / 2 = 52.5.',
 wrong:'August has the highest bar but not the largest rise; the median of an even count averages the two middle values rather than picking either one.'},
{id:'D276',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,passageHtml:GI_APPUSERS1,answerType:'gi',
 stem:'Using the bar chart of monthly active users, complete each statement.',
 statements:[
  {text:'From March to August, active users increased by approximately ____.',options:['24%','36%','57%','66%'],answer:2},
  {text:'The number of months showing a decline from the preceding month is ____.',options:['1','2','3','4'],answer:1}],
 expl:'The rise is 66 - 42 = 24 thousand on a base of 42, and 24 / 42 is about 57 percent. Declines occurred in May and July, two months.',
 wrong:'24 percent reads the absolute change as the percentage; using August as the base gives about 36 percent.'},
{id:'D277',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:2,passageHtml:GT_LIBRARY1,
 stem:'Which branch has the highest number of items loaned per weekly visitor?',
 choices:['Askern','Belford','Crane','Derwent','Elmswell'],answer:2,
 expl:'Loans per visitor: Askern 1.5, Belford 1.25, Crane 2880 / 1800 = 1.6, Derwent 1.3, Elmswell 1.4. Crane is highest.',
 wrong:'Elmswell loans the most items in total, but the question asks for the per-visitor rate.'},
{id:'D278',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:GT_LIBRARY1,
 stem:'Approximately how many e-loans does Elmswell make weekly?',
 choices:['1,050','1,260','1,470','1,680','1,890'],answer:2,
 expl:'E-loans are 35 percent of Elmswell\'s 4,200 weekly loans: 0.35 x 4200 = 1,470.',
 wrong:'1,050 applies 25 percent (Askern\'s share) and 1,260 applies 30 percent (Belford\'s share) to Elmswell\'s loans.'},
{id:'D279',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:GT_LIBRARY1,
 stem:'Which branch makes the greatest number of physical (non-electronic) loans weekly?',
 choices:['Askern','Belford','Crane','Derwent','Elmswell'],answer:1,
 expl:'Physical loans: Askern 3600 x 0.75 = 2700, Belford 4000 x 0.70 = 2800, Crane 2880 x 0.60 = 1728, Derwent 3380 x 0.80 = 2704, Elmswell 4200 x 0.65 = 2730. Belford leads.',
 wrong:'Derwent has the lowest e-share but a smaller loan base; the answer needs the product, not the percentage alone.'},
{id:'D280',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,passageHtml:GT_LIBRARY1,
 stem:'If Crane\'s weekly visitors increased by 25 percent while its items loaned per visitor stayed the same, approximately how many items would Crane loan weekly?',
 choices:['3,150','3,300','3,456','3,600','3,750'],answer:3,
 expl:'Crane loans 1.6 items per visitor. New visitors: 1800 x 1.25 = 2250. New loans: 2250 x 1.6 = 3,600.',
 wrong:'Raising loans by 25 percent of the visitor increase only, or applying 25 percent to loans and visitors both, produces the nearby traps.'},
{id:'D281',section:'DI',type:'TPA',domain:'arithmetic',skill:'di_tpa',qskill:'q_rrp',diff:3,
 stem:'A cyclist rides 24 kilometers to a lake at 16 kilometers per hour and returns along the same 24-kilometer route at 12 kilometers per hour.\n\nSelect the number of minutes the outbound ride takes, and the number of minutes the return ride takes. Make only two selections, one in each column.',
 answerType:'tpa',columns:['Outbound minutes','Return minutes'],
 choices:['60','75','90','105','120','150'],answer:[2,4],
 expl:'Outbound: 24 / 16 = 1.5 hours = 90 minutes. Return: 24 / 12 = 2 hours = 120 minutes.',
 wrong:'Averaging the two speeds to 14 km/h and splitting the time evenly misses that the slower leg takes longer.'},
{id:'D282',section:'DI',type:'TPA',domain:'arithmetic',skill:'di_tpa',qskill:'q_rrp',diff:4,
 stem:'A retailer buys a lamp for 80 dollars and sets its list price 25 percent above cost. During a sale, the lamp sells at 15 percent below list price.\n\nSelect the list price, in dollars, and the retailer\'s profit on the sale, in dollars. Make only two selections, one in each column.',
 answerType:'tpa',columns:['List price','Profit at sale'],
 choices:['5','15','20','85','95','100'],answer:[5,0],
 expl:'List price: 80 x 1.25 = 100. Sale price: 100 x 0.85 = 85, so profit is 85 - 80 = 5 dollars.',
 wrong:'Treating the two percentages as canceling (25 up then 15 down leaves 10 percent profit, or 8 dollars) ignores that the discount applies to the larger list price.'},
{id:'D283',section:'DI',type:'TPA',domain:'statistics',skill:'di_tpa',qskill:'q_csp',diff:3,
 stem:'A quiz team of 5 members has an average score of 82. Two new members join, and their scores average 68.\n\nSelect the total of the original five scores, and the new seven-member average. Make only two selections, one in each column.',
 answerType:'tpa',columns:['Total of original five','Seven-member average'],
 choices:['390','410','546','76','78','80'],answer:[1,4],
 expl:'Original total: 5 x 82 = 410. New total: 410 + 2 x 68 = 546, and 546 / 7 = 78.',
 wrong:'Averaging 82 and 68 to get 75 weights the two groups equally even though five members carry the higher average.'},
{id:'D284',section:'DI',type:'TPA',domain:'combinatorics',skill:'di_tpa',qskill:'q_csp',diff:5,
 stem:'A club with 6 members must choose a president and a treasurer, with no member holding both offices. Separately, the club must also choose an unordered pair of members to audit the budget.\n\nSelect the number of ways to choose the president and treasurer, and the number of possible auditor pairs. Make only two selections, one in each column.',
 answerType:'tpa',columns:['President and treasurer','Auditor pairs'],
 choices:['11','15','21','30','36','25'],answer:[3,1],
 expl:'Ordered offices: 6 x 5 = 30. Unordered pairs: 30 / 2 = 15, which is C(6,2).',
 wrong:'Using 6 x 6 = 36 lets one member hold both offices; forgetting to halve for the unordered pair gives 30 twice.'},
{id:'D285',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:2,
 stem:'What is the value of x?\n\n(1) 3x + 2y = 16\n(2) y = 2',choices:DS_CHOICES,answer:2,
 expl:'(1) One equation, two unknowns: not sufficient. (2) Says nothing about x: not sufficient. Together: 3x + 4 = 16, so x = 4. Sufficient. C.',
 wrong:'Trap: statement (1) looks solvable because the numbers are small, but any y still shifts x.'},
{id:'D286',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_vof',diff:3,
 stem:'Is the positive integer n divisible by 6?\n\n(1) n is divisible by 12\n(2) n is divisible by 9',choices:DS_CHOICES,answer:0,
 expl:'(1) Every multiple of 12 is a multiple of 6: sufficient, answer yes. (2) n = 9 gives no, n = 18 gives yes: not sufficient. A.',
 wrong:'Trap: 9 shares the factor 3 with 6, which tempts a yes, but divisibility by 6 also needs the factor 2.'},
{id:'D287',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_rrp',diff:4,
 stem:'A jar contains only red marbles and blue marbles. What fraction of the marbles are red?\n\n(1) The ratio of red to blue marbles is 3 to 5\n(2) The jar contains 24 blue marbles',choices:DS_CHOICES,answer:0,
 expl:'(1) With only two colors, red is 3 of every 8 marbles: the fraction is 3/8. Sufficient. (2) A count of blue alone fixes neither the total nor the fraction. A.',
 wrong:'Trap: assuming a fraction question needs actual counts; a complete ratio already determines it.'},
{id:'D288',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:4,
 stem:'Is a > b?\n\n(1) a - b > -2\n(2) 2a > 2b + 1',choices:DS_CHOICES,answer:1,
 expl:'(1) a - b could be -1 (no) or 3 (yes): not sufficient. (2) Dividing by 2: a > b + 0.5, which forces a > b. Sufficient. B.',
 wrong:'Trap: reading a - b > -2 as a - b > 2; the negative bound allows both outcomes.'},
{id:'D289',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_csp',diff:5,
 stem:'Set S consists of 5 distinct positive integers. Is the median of S greater than 10?\n\n(1) Three of the integers in S are greater than 10\n(2) The average (arithmetic mean) of S is 12',choices:DS_CHOICES,answer:0,
 expl:'(1) In a sorted list of 5, the median is the 3rd value. If three integers exceed 10, they occupy at latest positions 3, 4, and 5, so the 3rd value exceeds 10. Sufficient, yes. (2) The set {1, 2, 5, 25, 27} has mean 12 and median 5, while {10, 11, 12, 13, 14} has mean 12 and median 12: not sufficient. A.',
 wrong:'Trap: the mean feels informative, but it says nothing about where the middle value sits.'},
];
