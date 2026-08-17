// Data Insights seed bank. Types: DS, GT, MSR, TPA. skill: di_ds, di_gt, di_msr, di_tpa. domain: math | nonmath. qskill: underlying quant skill when math.
const DS_CHOICES = [
 'Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.',
 'Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.',
 'BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.',
 'EACH statement ALONE is sufficient.',
 'Statements (1) and (2) TOGETHER are NOT sufficient.'];

const GT_TABLE1 = '<table class="dtable"><thead><tr><th>Region</th><th>Q1 revenue ($ thousands)</th><th>Q2 revenue ($ thousands)</th><th>Q2 units sold</th></tr></thead><tbody>'+
 '<tr><td>North</td><td>240</td><td>276</td><td>1,200</td></tr>'+
 '<tr><td>South</td><td>180</td><td>171</td><td>950</td></tr>'+
 '<tr><td>East</td><td>300</td><td>345</td><td>1,500</td></tr>'+
 '<tr><td>West</td><td>150</td><td>180</td><td>800</td></tr>'+
 '<tr><td>Central</td><td>210</td><td>210</td><td>1,000</td></tr></tbody></table><p class="dnote">Regional sales for a consumer-goods company, first and second quarters.</p>';

const GT_CHART1 = '<div class="dchart"><svg viewBox="0 0 420 220" width="100%" style="max-width:520px"><g font-family="Inter,Arial" font-size="12">'+
 '<line x1="50" y1="180" x2="400" y2="180" stroke="#888"/><line x1="50" y1="20" x2="50" y2="180" stroke="#888"/>'+
 '<text x="8" y="184" fill="#666">0</text><text x="8" y="104" fill="#666">50</text><text x="8" y="24" fill="#666">100</text>'+
 '<line x1="50" y1="100" x2="400" y2="100" stroke="#eee"/><line x1="50" y1="20" x2="400" y2="20" stroke="#eee"/>'+
 '<rect x="65" y="116" width="40" height="64" fill="#5b6bd6"/><text x="85" y="198" text-anchor="middle">Jan</text><text x="85" y="110" text-anchor="middle" fill="#333">40</text>'+
 '<rect x="120" y="92" width="40" height="88" fill="#5b6bd6"/><text x="140" y="198" text-anchor="middle">Feb</text><text x="140" y="86" text-anchor="middle" fill="#333">55</text>'+
 '<rect x="175" y="100" width="40" height="80" fill="#5b6bd6"/><text x="195" y="198" text-anchor="middle">Mar</text><text x="195" y="94" text-anchor="middle" fill="#333">50</text>'+
 '<rect x="230" y="68" width="40" height="112" fill="#5b6bd6"/><text x="250" y="198" text-anchor="middle">Apr</text><text x="250" y="62" text-anchor="middle" fill="#333">70</text>'+
 '<rect x="285" y="76" width="40" height="104" fill="#5b6bd6"/><text x="305" y="198" text-anchor="middle">May</text><text x="305" y="70" text-anchor="middle" fill="#333">65</text>'+
 '<rect x="340" y="52" width="40" height="128" fill="#5b6bd6"/><text x="360" y="198" text-anchor="middle">Jun</text><text x="360" y="46" text-anchor="middle" fill="#333">80</text>'+
 '<text x="225" y="214" text-anchor="middle" fill="#666">Monthly website visits (thousands), January to June</text></g></svg></div>';

const MSR_SET1 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Room booking policy</h4><ul>'+
 '<li>Rooms: A (capacity 8), B (capacity 15), C (capacity 30).</li>'+
 '<li>All bookings require at least 24 hours\' notice.</li>'+
 '<li>A group larger than a room\'s capacity may not book that room.</li>'+
 '<li>Room C may be booked only with written approval from a department head. Rooms A and B may be booked by any employee.</li>'+
 '<li>Recurring bookings may run for at most 8 consecutive weeks.</li>'+
 '<li>Catering is available only in Rooms B and C and must be requested at least 48 hours before the booking.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: Pending requests</h4><table class="dtable"><thead><tr><th>Request</th><th>Group size</th><th>Room</th><th>Notice given</th><th>Other details</th></tr></thead><tbody>'+
 '<tr><td>R1</td><td>12</td><td>B</td><td>3 days</td><td>Catering requested 3 days ahead</td></tr>'+
 '<tr><td>R2</td><td>25</td><td>C</td><td>3 days</td><td>No department head approval attached</td></tr>'+
 '<tr><td>R3</td><td>6</td><td>A</td><td>12 hours</td><td>None</td></tr>'+
 '<tr><td>R4</td><td>20</td><td>B</td><td>1 week</td><td>None</td></tr>'+
 '<tr><td>R5</td><td>10</td><td>B</td><td>2 weeks</td><td>Recurring weekly for 10 weeks</td></tr></tbody></table></div></div>';

const BANK_DI = [
// Data Sufficiency
{id:'D001',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:2,
 stem:'Is x > 5?\n\n(1) x^2 > 25\n(2) x > 4',choices:DS_CHOICES,answer:2,
 expl:'(1) x > 5 or x < -5: not sufficient. (2) x could be 4.5 or 6: not sufficient. Together: x > 4 and (x > 5 or x < -5) forces x > 5. Sufficient. C.',
 wrong:'Trap: treating x^2 > 25 as x > 5. Squares hide negatives.'},
{id:'D002',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_rrp',diff:3,
 stem:'What is the ratio of the number of boys to the number of girls in a certain class?\n\n(1) 40 percent of the students in the class are boys.\n(2) There are 12 boys in the class.',choices:DS_CHOICES,answer:0,
 expl:'(1) Boys 40%, girls 60%, ratio 2:3. Sufficient. (2) 12 boys, unknown girls. Not sufficient. A.',
 wrong:'A ratio question needs relative sizes, not counts. Percent gives the ratio directly.'},
{id:'D003',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_vof',diff:3,
 stem:'Is the positive integer n divisible by 6?\n\n(1) n is divisible by 3.\n(2) n is divisible by 4.',choices:DS_CHOICES,answer:2,
 expl:'(1) n = 3 (no) or 6 (yes): not sufficient. (2) n = 4 (no) or 12 (yes): not sufficient. Together: divisible by 3 and 4, so by 12, so by 6. Sufficient. C.'},
{id:'D004',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:4,
 stem:'What is the value of x?\n\n(1) 3x + 2y = 12\n(2) 6x + 4y = 24',choices:DS_CHOICES,answer:4,
 expl:'Statement (2) is exactly twice statement (1): the same line. One equation in two unknowns, even taken together. Not sufficient. E.',
 wrong:'Two equations do not guarantee a solution; check whether they are independent.'},
{id:'D005',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_rrp',diff:3,
 stem:'A car traveled from Town P to Town Q without stopping. What was the car\'s average speed for the trip?\n\n(1) The distance from P to Q is 120 miles.\n(2) The trip took 2 hours 30 minutes.',choices:DS_CHOICES,answer:2,
 expl:'Average speed = distance / time. Each statement gives one of the two. Together: 120 / 2.5 = 48 mph. C.'},
{id:'D006',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:4,
 stem:'If xy is not 0, is x/y > 1?\n\n(1) x > y > 0\n(2) x - y = 3',choices:DS_CHOICES,answer:0,
 expl:'(1) Both positive and x larger, so x/y > 1. Sufficient. (2) x = 4, y = 1 gives 4 (yes); x = 1, y = -2 gives -1/2 (no). Not sufficient. A.',
 wrong:'Never cross-multiply an inequality by a variable whose sign you do not know.'},
{id:'D007',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_csp',diff:3,
 stem:'A company has 200 employees. How many of the company\'s managers work remotely?\n\n(1) 30 percent of the employees are managers.\n(2) 24 of the managers, which is 40 percent of all managers, work remotely.',choices:DS_CHOICES,answer:1,
 expl:'(1) 60 managers, but no remote information. Not sufficient. (2) States directly that 24 managers work remotely. Sufficient. B.',
 wrong:'Do not be lured into combining; read (2) literally, it answers the question by itself.'},
{id:'D008',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:3,
 stem:'If x is positive, what is the value of x?\n\n(1) x^2 = 49\n(2) x^3 = 343',choices:DS_CHOICES,answer:3,
 expl:'(1) x = 7 or -7, but x is positive, so x = 7. Sufficient. (2) x = 7 (cube roots are unique). Sufficient. D.',
 wrong:'Use the stem\'s constraint (x positive) when evaluating (1).'},
// Graphs and Tables
{id:'D009',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:2,passageHtml:GT_TABLE1,
 stem:'Which region had the greatest percent increase in revenue from Q1 to Q2?',
 choices:['North','South','East','West','Central'],answer:3,
 expl:'North 36/240 = 15%; South negative; East 45/300 = 15%; West 30/150 = 20%; Central 0%. West.',
 wrong:'East has the largest dollar increase (45), a trap for a percent question.'},
{id:'D010',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:GT_TABLE1,
 stem:'What was the East region\'s Q2 revenue per unit sold?',
 choices:['$200','$220','$230','$250','$300'],answer:2,
 expl:'$345,000 / 1,500 units = $230.'},
{id:'D011',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_csp',diff:3,passageHtml:GT_TABLE1,
 stem:'What is the median Q2 revenue across the five regions, in thousands of dollars?',
 choices:['171','180','210','236.4','276'],answer:2,
 expl:'Sort Q2: 171, 180, 210, 276, 345. Middle value 210.',
 wrong:'D (236.4) is the mean.'},
{id:'D012',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,passageHtml:GT_TABLE1,
 stem:'Total Q2 revenue was approximately what percent greater than total Q1 revenue?',
 choices:['8.5%','9.4%','10.2%','11.0%','12.5%'],answer:1,
 expl:'Q1 total 1,080; Q2 total 1,182. Increase 102/1,080 = 9.4%.'},
{id:'D013',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:GT_TABLE1,
 stem:'Which region\'s Q2 revenue per unit was closest to $200?',
 choices:['North','South','East','West','Central'],answer:4,
 expl:'North 230, South 180, East 230, West 225, Central 210. Central (10 away) is closest.',
 wrong:'South (180) is 20 away; the trap is assuming the lowest value is closest.'},
{id:'D014',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_csp',diff:3,passageHtml:GT_CHART1,
 stem:'What was the average (arithmetic mean) number of monthly visits, in thousands, over the six months shown?',
 choices:['55','58','60','62','65'],answer:2,
 expl:'40 + 55 + 50 + 70 + 65 + 80 = 360. 360/6 = 60.'},
{id:'D015',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_csp',diff:3,passageHtml:GT_CHART1,
 stem:'In how many of the six months did visits exceed the six-month average?',
 choices:['2','3','4','5','6'],answer:1,
 expl:'Average is 60. Months above 60: April (70), May (65), June (80). Three.'},
// Two-Part Analysis
{id:'D016',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_alg',diff:4,answerType:'tpa',
 stem:'A gym charges a one-time joining fee plus a fixed monthly fee. A member who stays for 6 months pays $390 in total, and a member who stays for 10 months pays $610 in total.\n\nIn the table, select the monthly fee and the joining fee, in dollars. Make only two selections, one in each column.',
 columns:['Monthly fee','Joining fee'],choices:['45','50','55','60','65','70'],answer:[2,3],
 expl:'6m + j = 390 and 10m + j = 610. Subtract: 4m = 220, m = 55. Then j = 390 - 330 = 60.',
 wrong:'Two-part items with linked unknowns are just a system of equations; solve once, then place both answers.'},
{id:'D017',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_csp',diff:4,answerType:'tpa',
 stem:'A student\'s average score on 4 tests is 82. If the lowest score is dropped, the average of the remaining 3 tests is 86.\n\nSelect the lowest score and the sum of the remaining three scores. Make only two selections, one in each column.',
 columns:['Lowest score','Sum of remaining three'],choices:['70','72','76','246','258','264'],answer:[0,4],
 expl:'Total of 4 = 328. Total of 3 = 258. Lowest = 328 - 258 = 70.'},
{id:'D018',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_rrp',diff:5,answerType:'tpa',
 stem:'Alloy A is 30% copper by weight and Alloy B is 70% copper by weight. A metalworker combines the two alloys to produce 100 kilograms of an alloy that is 54% copper.\n\nSelect the number of kilograms of Alloy A and the number of kilograms of Alloy B used. Make only two selections, one in each column.',
 columns:['Kilograms of Alloy A','Kilograms of Alloy B'],choices:['30','40','50','60','70','80'],answer:[1,3],
 expl:'0.30a + 0.70(100 - a) = 54, so 70 - 0.40a = 54, a = 40, b = 60. Check with the ratio shortcut: 54 is 24 above 30 and 16 below 70, so A:B = 16:24 = 2:3.'},
// Multi-Source Reasoning
{id:'D019',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:3,passageHtml:MSR_SET1,
 stem:'How many of the five pending requests comply with the booking policy exactly as submitted, without any change?',
 choices:['0','1','2','3','4'],answer:1,
 expl:'R1: 12 in B (cap 15), 3 days notice, catering 3 days ahead in B: complies. R2: no department head approval for C: fails. R3: 12 hours notice: fails. R4: 20 exceeds B capacity: fails. R5: 10 weeks recurring exceeds 8: fails. One request.'},
{id:'D020',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:3,passageHtml:MSR_SET1,
 stem:'Request R2 would comply with the policy if which one of the following single changes were made?',
 choices:['Reduce the group to 15 people','Obtain written approval from a department head','Give at least one week\'s notice','Move the booking to Room B','Add a catering request'],answer:1,
 expl:'R2\'s only violation is the missing department head approval for Room C. B fixes it. Moving to B fails on capacity (25 > 15); reducing to 15 alone still leaves the Room C approval issue.'},
{id:'D021',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_SET1,
 stem:'Request R4 could be accommodated without reducing the size of the group by which of the following?',
 choices:['Moving the booking to Room A','Moving the booking to Room C and obtaining department head approval','Adding a catering request at least 48 hours in advance','Making the booking recurring for 8 weeks','Increasing the notice to 48 hours'],answer:1,
 expl:'20 people exceed Room B (15) and Room A (8). Only Room C (30) fits, and Room C requires department head approval. B.'}
];
