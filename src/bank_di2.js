// Data Insights bank 2 (D101-D130). Types: DS, GI, TA, TPA, MSR. Reuses DS_CHOICES from bank_di.js.
// New schemas: GI -> answerType 'gi', statements:[{text,options,answer}]; TA -> answerType 'ta', statements:[{text,answer:true|false}].

// ---- Graphics Interpretation charts ----
// Chart 1: bar chart, annual rainfall (mm) 2019-2024. Scale: 0-800 mm over 160 px (0.2 px/mm), baseline y=180.
const GI_CHART1 = '<div class="dchart"><svg viewBox="0 0 420 220" width="100%" style="max-width:520px"><g font-family="Manrope,Inter,Arial" font-size="12">'+
 '<line x1="50" y1="180" x2="400" y2="180" stroke="#888"/><line x1="50" y1="20" x2="50" y2="180" stroke="#888"/>'+
 '<line x1="50" y1="140" x2="400" y2="140" stroke="#eee"/><line x1="50" y1="100" x2="400" y2="100" stroke="#eee"/><line x1="50" y1="60" x2="400" y2="60" stroke="#eee"/><line x1="50" y1="20" x2="400" y2="20" stroke="#eee"/>'+
 '<text x="44" y="184" text-anchor="end" fill="#666">0</text><text x="44" y="144" text-anchor="end" fill="#666">200</text><text x="44" y="104" text-anchor="end" fill="#666">400</text><text x="44" y="64" text-anchor="end" fill="#666">600</text><text x="44" y="24" text-anchor="end" fill="#666">800</text>'+
 '<rect x="65" y="56" width="40" height="124" fill="#2563EB"/><text x="85" y="198" text-anchor="middle">2019</text><text x="85" y="50" text-anchor="middle" fill="#333">620</text>'+
 '<rect x="120" y="72" width="40" height="108" fill="#2563EB"/><text x="140" y="198" text-anchor="middle">2020</text><text x="140" y="66" text-anchor="middle" fill="#333">540</text>'+
 '<rect x="175" y="40" width="40" height="140" fill="#2563EB"/><text x="195" y="198" text-anchor="middle">2021</text><text x="195" y="34" text-anchor="middle" fill="#333">700</text>'+
 '<rect x="230" y="48" width="40" height="132" fill="#2563EB"/><text x="250" y="198" text-anchor="middle">2022</text><text x="250" y="42" text-anchor="middle" fill="#333">660</text>'+
 '<rect x="285" y="84" width="40" height="96" fill="#2563EB"/><text x="305" y="198" text-anchor="middle">2023</text><text x="305" y="78" text-anchor="middle" fill="#333">480</text>'+
 '<rect x="340" y="30" width="40" height="150" fill="#2563EB"/><text x="360" y="198" text-anchor="middle">2024</text><text x="360" y="24" text-anchor="middle" fill="#333">750</text>'+
 '<text x="225" y="214" text-anchor="middle" fill="#666">Annual rainfall at Station K (millimeters), 2019 to 2024</text></g></svg></div>';

// Chart 2: line chart, monthly revenue ($ thousands) of two stores, Jan-Jun. Scale: 20-60 over 160 px (4 px per unit), y = 180 - (v-20)*4.
const GI_CHART2 = '<div class="dchart"><svg viewBox="0 0 420 220" width="100%" style="max-width:520px"><g font-family="Manrope,Inter,Arial" font-size="12">'+
 '<line x1="50" y1="180" x2="400" y2="180" stroke="#888"/><line x1="50" y1="20" x2="50" y2="180" stroke="#888"/>'+
 '<line x1="50" y1="140" x2="400" y2="140" stroke="#eee"/><line x1="50" y1="100" x2="400" y2="100" stroke="#eee"/><line x1="50" y1="60" x2="400" y2="60" stroke="#eee"/><line x1="50" y1="20" x2="400" y2="20" stroke="#eee"/>'+
 '<text x="44" y="184" text-anchor="end" fill="#666">20</text><text x="44" y="144" text-anchor="end" fill="#666">30</text><text x="44" y="104" text-anchor="end" fill="#666">40</text><text x="44" y="64" text-anchor="end" fill="#666">50</text><text x="44" y="24" text-anchor="end" fill="#666">60</text>'+
 '<text x="70" y="198" text-anchor="middle">Jan</text><text x="134" y="198" text-anchor="middle">Feb</text><text x="198" y="198" text-anchor="middle">Mar</text><text x="262" y="198" text-anchor="middle">Apr</text><text x="326" y="198" text-anchor="middle">May</text><text x="390" y="198" text-anchor="middle">Jun</text>'+
 // Store A (#2563EB): 30,34,38,36,42,48
 '<polyline points="70,140 134,124 198,108 262,116 326,92 390,68" fill="none" stroke="#2563EB" stroke-width="2"/>'+
 '<circle cx="70" cy="140" r="3.5" fill="#2563EB"/><circle cx="134" cy="124" r="3.5" fill="#2563EB"/><circle cx="198" cy="108" r="3.5" fill="#2563EB"/><circle cx="262" cy="116" r="3.5" fill="#2563EB"/><circle cx="326" cy="92" r="3.5" fill="#2563EB"/><circle cx="390" cy="68" r="3.5" fill="#2563EB"/>'+
 '<text x="70" y="154" text-anchor="middle" fill="#2563EB">30</text><text x="134" y="138" text-anchor="middle" fill="#2563EB">34</text><text x="198" y="100" text-anchor="middle" fill="#2563EB">38</text><text x="262" y="130" text-anchor="middle" fill="#2563EB">36</text><text x="326" y="84" text-anchor="middle" fill="#2563EB">42</text><text x="390" y="60" text-anchor="middle" fill="#2563EB">48</text>'+
 // Store B (#0D9488): 40,38,36,40,41,42
 '<polyline points="70,100 134,108 198,116 262,100 326,96 390,92" fill="none" stroke="#0D9488" stroke-width="2"/>'+
 '<circle cx="70" cy="100" r="3.5" fill="#0D9488"/><circle cx="134" cy="108" r="3.5" fill="#0D9488"/><circle cx="198" cy="116" r="3.5" fill="#0D9488"/><circle cx="262" cy="100" r="3.5" fill="#0D9488"/><circle cx="326" cy="96" r="3.5" fill="#0D9488"/><circle cx="390" cy="92" r="3.5" fill="#0D9488"/>'+
 '<text x="70" y="92" text-anchor="middle" fill="#0D9488">40</text><text x="134" y="100" text-anchor="middle" fill="#0D9488">38</text><text x="198" y="130" text-anchor="middle" fill="#0D9488">36</text><text x="262" y="92" text-anchor="middle" fill="#0D9488">40</text><text x="326" y="110" text-anchor="middle" fill="#0D9488">41</text><text x="390" y="106" text-anchor="middle" fill="#0D9488">42</text>'+
 '<rect x="60" y="24" width="10" height="10" fill="#2563EB"/><text x="74" y="33" fill="#333">Store A</text><rect x="130" y="24" width="10" height="10" fill="#0D9488"/><text x="144" y="33" fill="#333">Store B</text>'+
 '<text x="225" y="214" text-anchor="middle" fill="#666">Monthly revenue ($ thousands), January to June</text></g></svg></div>';

// Chart 3: scatter, advertising spend (x, $ thousands, 0-10 -> 35 px/unit from x=50) vs monthly sales (y, $ thousands, 0-60 -> 8/3 px/unit from y=180).
const GI_CHART3 = '<div class="dchart"><svg viewBox="0 0 420 220" width="100%" style="max-width:520px"><g font-family="Manrope,Inter,Arial" font-size="12">'+
 '<line x1="50" y1="180" x2="400" y2="180" stroke="#888"/><line x1="50" y1="20" x2="50" y2="180" stroke="#888"/>'+
 '<line x1="50" y1="126.7" x2="400" y2="126.7" stroke="#eee"/><line x1="50" y1="73.3" x2="400" y2="73.3" stroke="#eee"/><line x1="50" y1="20" x2="400" y2="20" stroke="#eee"/>'+
 '<text x="44" y="184" text-anchor="end" fill="#666">0</text><text x="44" y="130" text-anchor="end" fill="#666">20</text><text x="44" y="77" text-anchor="end" fill="#666">40</text><text x="44" y="24" text-anchor="end" fill="#666">60</text>'+
 '<text x="50" y="194" text-anchor="middle" fill="#666">0</text><text x="120" y="194" text-anchor="middle" fill="#666">2</text><text x="190" y="194" text-anchor="middle" fill="#666">4</text><text x="260" y="194" text-anchor="middle" fill="#666">6</text><text x="330" y="194" text-anchor="middle" fill="#666">8</text><text x="400" y="194" text-anchor="middle" fill="#666">10</text>'+
 '<circle cx="120" cy="126.7" r="4" fill="#7C3AED"/><text x="120" y="142" text-anchor="middle" fill="#333">A (2, 20)</text>'+
 '<circle cx="155" cy="105.3" r="4" fill="#7C3AED"/><text x="155" y="98" text-anchor="middle" fill="#333">B (3, 28)</text>'+
 '<circle cx="190" cy="110.7" r="4" fill="#7C3AED"/><text x="190" y="126" text-anchor="middle" fill="#333">C (4, 26)</text>'+
 '<circle cx="225" cy="86.7" r="4" fill="#7C3AED"/><text x="225" y="79" text-anchor="middle" fill="#333">D (5, 35)</text>'+
 '<circle cx="260" cy="92" r="4" fill="#7C3AED"/><text x="260" y="108" text-anchor="middle" fill="#333">E (6, 33)</text>'+
 '<circle cx="295" cy="62.7" r="4" fill="#7C3AED"/><text x="295" y="55" text-anchor="middle" fill="#333">F (7, 44)</text>'+
 '<circle cx="330" cy="73.3" r="4" fill="#7C3AED"/><text x="330" y="89" text-anchor="middle" fill="#333">G (8, 40)</text>'+
 '<circle cx="365" cy="46.7" r="4" fill="#7C3AED"/><text x="365" y="39" text-anchor="middle" fill="#333">H (9, 50)</text>'+
 '<text x="225" y="212" text-anchor="middle" fill="#666">Eight stores: advertising spend ($ thousands, x) vs. monthly sales ($ thousands, y)</text></g></svg></div>';

// ---- Table Analysis tables ----
const TA_TABLE1 = '<table class="dtable sortable"><thead><tr><th>Consultant</th><th>Department</th><th>Years of service</th><th>Q1 billable hours</th><th>Hourly rate ($)</th></tr></thead><tbody>'+
 '<tr><td>Alvarez</td><td>Strategy</td><td>6</td><td>410</td><td>250</td></tr>'+
 '<tr><td>Bennett</td><td>Tax</td><td>3</td><td>385</td><td>180</td></tr>'+
 '<tr><td>Chen</td><td>Strategy</td><td>9</td><td>440</td><td>300</td></tr>'+
 '<tr><td>Dube</td><td>Audit</td><td>2</td><td>360</td><td>160</td></tr>'+
 '<tr><td>Ellis</td><td>Tax</td><td>7</td><td>400</td><td>220</td></tr>'+
 '<tr><td>Farah</td><td>Audit</td><td>5</td><td>395</td><td>190</td></tr>'+
 '<tr><td>Gomez</td><td>Strategy</td><td>1</td><td>320</td><td>150</td></tr></tbody></table>'+
 '<p class="dnote">Seven consultants at a professional-services firm. Q1 billings for a consultant equal billable hours multiplied by hourly rate.</p>';

const TA_TABLE2 = '<table class="dtable sortable"><thead><tr><th>City</th><th>Population (thousands)</th><th>Area (sq km)</th><th>Median monthly rent ($)</th><th>Annual transit rides (millions)</th></tr></thead><tbody>'+
 '<tr><td>Ashford</td><td>820</td><td>410</td><td>1,450</td><td>96</td></tr>'+
 '<tr><td>Brenton</td><td>1,240</td><td>550</td><td>1,720</td><td>210</td></tr>'+
 '<tr><td>Calder</td><td>460</td><td>200</td><td>1,100</td><td>31</td></tr>'+
 '<tr><td>Dorsey</td><td>2,050</td><td>780</td><td>2,150</td><td>480</td></tr>'+
 '<tr><td>Elmwood</td><td>390</td><td>300</td><td>980</td><td>18</td></tr>'+
 '<tr><td>Fairhaven</td><td>1,010</td><td>380</td><td>1,650</td><td>150</td></tr>'+
 '<tr><td>Granger</td><td>640</td><td>400</td><td>1,300</td><td>52</td></tr>'+
 '<tr><td>Holt</td><td>275</td><td>110</td><td>1,200</td><td>22</td></tr></tbody></table>'+
 '<p class="dnote">Eight cities in a metropolitan region. Population density is population divided by area.</p>';

const TA_TABLE3 = '<table class="dtable sortable"><thead><tr><th>Fund</th><th>Category</th><th>1-year return (%)</th><th>5-year annualized return (%)</th><th>Expense ratio (%)</th><th>Assets ($ millions)</th></tr></thead><tbody>'+
 '<tr><td>Apex Growth</td><td>Equity</td><td>14.2</td><td>9.8</td><td>0.85</td><td>1,250</td></tr>'+
 '<tr><td>Beacon Income</td><td>Bond</td><td>3.6</td><td>2.9</td><td>0.45</td><td>860</td></tr>'+
 '<tr><td>Cobalt Index</td><td>Equity</td><td>9.9</td><td>10.4</td><td>0.10</td><td>4,300</td></tr>'+
 '<tr><td>Delta Balanced</td><td>Mixed</td><td>7.8</td><td>6.1</td><td>0.60</td><td>1,900</td></tr>'+
 '<tr><td>Ember Small-Cap</td><td>Equity</td><td>18.9</td><td>8.2</td><td>1.10</td><td>420</td></tr>'+
 '<tr><td>Fjord Global</td><td>Equity</td><td>9.4</td><td>7.5</td><td>0.95</td><td>2,150</td></tr></tbody></table>'+
 '<p class="dnote">Six mutual funds offered by one investment company, as of year-end.</p>';

// ---- Multi-Source Reasoning set ----
const MSR_SET2 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Travel expense reimbursement policy (Norvale Consulting)</h4><ul>'+
 '<li>Claims must be submitted within 30 days after the trip\'s end date. Late claims are not reimbursed.</li>'+
 '<li>Economy-class airfare is reimbursed in full. Business-class airfare is reimbursed in full only for flights longer than 6 hours; for shorter flights, business-class airfare is reimbursed up to $500.</li>'+
 '<li>Lodging is reimbursed up to $180 per night. Amounts above the cap are reimbursed only with the Director of Finance\'s pre-approval.</li>'+
 '<li>Meals are reimbursed as a flat per diem of $60 for each day of the trip; no receipts are required.</li>'+
 '<li>Use of a personal vehicle is reimbursed at $0.60 per mile.</li>'+
 '<li>Any claim whose reimbursable total exceeds $2,000 requires the Director of Finance\'s sign-off before payment.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: Claims submitted in March and April</h4><table class="dtable"><thead><tr><th>Claim</th><th>Employee</th><th>Trip end date</th><th>Date submitted</th><th>Trip days</th><th>Airfare</th><th>Lodging</th><th>Personal-vehicle miles</th></tr></thead><tbody>'+
 '<tr><td>C1</td><td>Ramos</td><td>Mar 3</td><td>Mar 20</td><td>3</td><td>Economy, $420</td><td>2 nights at $170</td><td>0</td></tr>'+
 '<tr><td>C2</td><td>Singh</td><td>Mar 10</td><td>Apr 15</td><td>2</td><td>Economy, $310</td><td>1 night at $150</td><td>40</td></tr>'+
 '<tr><td>C3</td><td>Okafor</td><td>Mar 14</td><td>Mar 28</td><td>4</td><td>Business (8-hour flight), $1,900</td><td>3 nights at $200</td><td>0</td></tr>'+
 '<tr><td>C4</td><td>Lindqvist</td><td>Mar 21</td><td>Apr 2</td><td>2</td><td>Business (3-hour flight), $1,150</td><td>1 night at $175</td><td>60</td></tr>'+
 '<tr><td>C5</td><td>Park</td><td>Mar 25</td><td>Apr 10</td><td>5</td><td>Economy, $530</td><td>4 nights at $180</td><td>100</td></tr></tbody></table></div>'+
 '<div class="msrtab"><h4>Tab 3: Email from the Director of Finance</h4><p>To: All consulting staff<br>Subject: Expense policy updates</p>'+
 '<p>Team: Effective for trips ending on or after March 15, the lodging cap rises from $180 to $200 per night. Separately, I have pre-approved the lodging overage on Okafor\'s Chicago trip (Claim C3), so that claim may be processed at the full nightly rate. The 30-day submission window still applies with no exceptions. Any claim over $2,000 will sit in my queue until I sign off; I will review the queue on Friday.</p><p>D. Mehta, Director of Finance</p></div></div>';

const BANK_DI2 = [
// ---- Data Sufficiency (D101-D110) ----
{id:'D101',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:3,
 stem:'If x and y are integers, is x + y even?\n\n(1) x - y is even.\n(2) xy is odd.',choices:DS_CHOICES,answer:3,
 expl:'(1) x - y even means x and y have the same parity; the sum of two same-parity integers is even. Sufficient. (2) xy odd means both x and y are odd, so x + y is even. Sufficient. Each alone works. D.',
 wrong:'Trap: assuming a product condition cannot pin down a sum. Odd product forces both factors odd.'},
{id:'D102',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_rrp',diff:3,
 stem:'A store sold a jacket at a discount from its list price. What was the discounted price of the jacket?\n\n(1) The discount was 20 percent of the list price.\n(2) The discounted price was $16 less than the list price.',choices:DS_CHOICES,answer:2,
 expl:'(1) 20% off an unknown list price: not sufficient. (2) $16 off an unknown list price: not sufficient. Together: 0.20L = 16, so L = 80 and the discounted price is 64. Sufficient. C.',
 wrong:'A percent and a dollar amount for the same quantity together fix the base.'},
{id:'D103',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_vof',diff:4,
 stem:'If n is a positive integer, what is the remainder when n is divided by 8?\n\n(1) When n is divided by 16, the remainder is 5.\n(2) When n is divided by 4, the remainder is 1.',choices:DS_CHOICES,answer:0,
 expl:'(1) n = 16k + 5 = 8(2k) + 5, so the remainder on division by 8 is 5. Sufficient. (2) n = 1, 5, 9, 13 give remainders 1, 5, 1, 5 on division by 8. Not sufficient. A.',
 wrong:'A remainder modulo a multiple of 8 determines the remainder modulo 8; a remainder modulo a divisor of 8 does not.'},
{id:'D104',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_csp',diff:3,
 stem:'A bag contains only red marbles and blue marbles. If one marble is selected at random from the bag, what is the probability that it is red?\n\n(1) There are 12 more blue marbles than red marbles in the bag.\n(2) The number of blue marbles in the bag is 3 times the number of red marbles.',choices:DS_CHOICES,answer:1,
 expl:'(1) 1 red and 13 blue gives 1/14; 12 red and 24 blue gives 1/3. Not sufficient. (2) Red : blue = 1 : 3, so red is 1/4 of the total. Sufficient. B.',
 wrong:'Probability needs the ratio, not the counts. A difference gives neither; a ratio is enough.'},
{id:'D105',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:5,
 stem:'Is x > y?\n\n(1) x^2 > y^2\n(2) x + y > 0',choices:DS_CHOICES,answer:2,
 expl:'(1) x = 3, y = 2 (yes); x = -3, y = 2 (no). Not sufficient. (2) x = 2, y = 1 (yes); x = 1, y = 2 (no). Not sufficient. Together: x^2 - y^2 = (x - y)(x + y) > 0 and x + y > 0, so x - y > 0. Sufficient. C.',
 wrong:'Factor the difference of squares; the sign of x + y unlocks the sign of x - y.'},
{id:'D106',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_csp',diff:4,
 stem:'List S consists of 5 positive integers. What is the median of S?\n\n(1) The average (arithmetic mean) of the integers in S is 20.\n(2) The greatest integer in S is 30 and the least is 10.',choices:DS_CHOICES,answer:4,
 expl:'(1) Mean 20 says nothing about the middle value alone. Not sufficient. (2) 10, ?, ?, ?, 30: the median can be anything from 10 to 30. Not sufficient. Together: sum 100 with 10 and 30 fixed leaves 60 for the three middle values: 15, 20, 25 (median 20) or 12, 18, 30 (median 18). Not sufficient. E.',
 wrong:'Mean and range constrain the middle values but do not fix them.'},
{id:'D107',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_rrp',diff:3,
 stem:'Machines A and B each work at a constant rate. Working alone, how many hours does Machine A take to complete one job?\n\n(1) Working together, Machines A and B complete the job in 6 hours.\n(2) Working alone, Machine A completes one-third of the job in 5 hours.',choices:DS_CHOICES,answer:1,
 expl:'(1) Combined time gives 1/A + 1/B = 1/6 with B unknown. Not sufficient. (2) One-third of the job in 5 hours means the whole job in 15 hours. Sufficient. B.',
 wrong:'Trap: assuming a two-machine problem needs both statements. Statement (2) is a complete rate fact on its own.'},
{id:'D108',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:2,
 stem:'What is the value of 2x + 3y?\n\n(1) 4x + 6y = 18\n(2) x + y = 4',choices:DS_CHOICES,answer:0,
 expl:'(1) Divide by 2: 2x + 3y = 9. Sufficient. (2) x = 4, y = 0 gives 8; x = 0, y = 4 gives 12. Not sufficient. A.',
 wrong:'You need the combination asked for, not the individual variables.'},
{id:'D109',section:'DI',type:'DS',domain:'nonmath',skill:'di_ds',diff:3,
 stem:'A permit committee approves an application if and only if the application is complete and at least two of the committee\'s three reviewers recommend approval. Was Application K approved?\n\n(1) Exactly one of the three reviewers recommended approval of Application K.\n(2) Application K was incomplete.',choices:DS_CHOICES,answer:3,
 expl:'(1) Only one recommendation, fewer than two, so the application was not approved. A definite "no" answers the question. Sufficient. (2) Incomplete applications are not approved. Definite "no." Sufficient. Each alone. D.',
 wrong:'Trap: treating a "No" answer as insufficient. Sufficiency means a definite answer, yes or no.'},
{id:'D110',section:'DI',type:'DS',domain:'nonmath',skill:'di_ds',diff:4,
 stem:'Each employee at a firm is assigned to exactly one of three teams: Red, Blue, or Green. Every employee on the Red team has completed safety training. Is Marta, an employee at the firm, on the Red team?\n\n(1) Marta has completed safety training.\n(2) Marta is not on the Blue team.',choices:DS_CHOICES,answer:4,
 expl:'(1) Red implies training, but training does not imply Red; a Green or Blue employee could be trained. Not sufficient. (2) Marta is Red or Green. Not sufficient. Together: a trained Green-team employee satisfies both statements, as does a Red-team employee. Not sufficient. E.',
 wrong:'Trap: reversing a conditional. "All Red are trained" is not "all trained are Red."'},

// ---- Graphics Interpretation (D111-D116) ----
{id:'D111',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_csp',diff:2,passageHtml:GI_CHART1,answerType:'gi',
 stem:'The bar chart shows annual rainfall at Station K for each year from 2019 to 2024. Complete each statement using the drop-down options.',
 statements:[
  {text:'Compared with the preceding year, the largest increase in annual rainfall occurred in ____.',options:['2020','2021','2022','2024'],answer:3},
  {text:'The median annual rainfall for the six years shown was ____ mm.',options:['600','620','640','660'],answer:2}],
 expl:'Year-over-year changes: 2020 -80, 2021 +160, 2022 -40, 2023 -180, 2024 +270; the largest increase is 2024. Sorted values 480, 540, 620, 660, 700, 750; the median is (620 + 660)/2 = 640.',
 wrong:'Trap in part 2: picking 620 or 660 (the two middle values) instead of averaging them.'},
{id:'D112',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:GI_CHART1,answerType:'gi',
 stem:'The bar chart shows annual rainfall at Station K for each year from 2019 to 2024. Complete each statement using the drop-down options.',
 statements:[
  {text:'The average (arithmetic mean) annual rainfall over the six years was ____ mm.',options:['600','625','640','650'],answer:1},
  {text:'Rainfall in 2024 was ____ percent greater than rainfall in 2023.',options:['36','45','56.25','64'],answer:2}],
 expl:'Sum: 620 + 540 + 700 + 660 + 480 + 750 = 3,750; 3,750/6 = 625. 2024 vs 2023: 750/480 = 1.5625, an increase of 56.25%.',
 wrong:'Trap in part 2: 36% is the decrease from 750 to 480 (270/750), the wrong base.'},
{id:'D113',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_csp',diff:3,passageHtml:GI_CHART2,answerType:'gi',
 stem:'The line graph shows monthly revenue for Store A and Store B from January to June. Complete each statement using the drop-down options.',
 statements:[
  {text:'Store A\'s monthly revenue first exceeded Store B\'s in ____.',options:['March','April','May','June'],answer:0},
  {text:'Over the six months, Store A\'s total revenue was ____ Store B\'s total revenue.',options:['less than','equal to','greater than','exactly twice'],answer:0}],
 expl:'March: A 38 vs B 36, the first month A is higher (Jan 30 vs 40, Feb 34 vs 38). Totals: A = 30 + 34 + 38 + 36 + 42 + 48 = 228; B = 40 + 38 + 36 + 40 + 41 + 42 = 237. A is less than B.',
 wrong:'Trap in part 2: A finishes higher and grows faster, but B led early; the totals favor B.'},
{id:'D114',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,passageHtml:GI_CHART2,answerType:'gi',
 stem:'The line graph shows monthly revenue for Store A and Store B from January to June. Complete each statement using the drop-down options.',
 statements:[
  {text:'From January to June, Store A\'s monthly revenue increased by ____ percent.',options:['40','50','60','80'],answer:2},
  {text:'The change in Store B\'s revenue from one month to the next was greatest in absolute value between ____.',options:['January and February','March and April','April and May','May and June'],answer:1}],
 expl:'A: 48/30 = 1.6, a 60% increase. B month-to-month changes: -2, -2, +4, +1, +1; the largest magnitude is +4 between March and April.',
 wrong:'Trap in part 1: 18/48 = 37.5% uses the June value as the base; the base is January.'},
{id:'D115',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:GI_CHART3,answerType:'gi',
 stem:'The scatter plot shows monthly advertising spend and monthly sales for eight stores, labeled A through H. Complete each statement using the drop-down options.',
 statements:[
  {text:'The store with the greatest ratio of sales to advertising spend is Store ____.',options:['A','B','D','H'],answer:0},
  {text:'The number of stores with sales greater than $30 thousand and advertising spend less than $7 thousand is ____.',options:['1','2','3','4'],answer:1}],
 expl:'Ratios: A 20/2 = 10, B 28/3 = 9.3, D 35/5 = 7, H 50/9 = 5.6; A is highest. Sales > 30 and spend < 7: D (5, 35) and E (6, 33). Two stores.',
 wrong:'Trap in part 1: H has the highest sales, but the ratio question rewards the lowest spend per sale.'},
{id:'D116',section:'DI',type:'GI',domain:'math',skill:'di_gt',qskill:'q_csp',diff:3,passageHtml:GI_CHART3,answerType:'gi',
 stem:'The scatter plot shows monthly advertising spend and monthly sales for eight stores, labeled A through H. Complete each statement using the drop-down options.',
 statements:[
  {text:'The relationship between advertising spend and sales shown in the plot is best described as ____.',options:['strongly negative','approximately zero','positive but not perfectly linear','perfectly linear'],answer:2},
  {text:'The median of the eight sales values is ____ thousand dollars.',options:['33','34','35','36'],answer:1}],
 expl:'Sales rise as spend rises, but not on a straight line (C is below B, G is below F): positive, not perfectly linear. Sorted sales: 20, 26, 28, 33, 35, 40, 44, 50; median (33 + 35)/2 = 34.',
 wrong:'Trap in part 2: an even count needs the average of the two middle values.'},

// ---- Table Analysis (D117-D122) ----
{id:'D117',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_csp',diff:2,passageHtml:TA_TABLE1,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'The median number of Q1 billable hours among the seven consultants is 395.',answer:true},
  {text:'The consultant with the fewest years of service also has the fewest Q1 billable hours.',answer:true},
  {text:'Every Strategy consultant has a higher hourly rate than every Tax consultant.',answer:false}],
 expl:'Hours sorted: 320, 360, 385, 395, 400, 410, 440; median 395 (Yes). Gomez has 1 year and 320 hours, both the minimum (Yes). Gomez (Strategy, $150) is below both Tax rates, $180 and $220 (No).',
 wrong:'Trap in statement 3: the two senior Strategy rates are high, but "every" requires checking Gomez.'},
{id:'D118',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,passageHtml:TA_TABLE1,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'Chen\'s Q1 billings exceed the combined Q1 billings of Dube and Gomez.',answer:true},
  {text:'The average (arithmetic mean) years of service of the Audit consultants is greater than that of the Tax consultants.',answer:false},
  {text:'Bennett\'s Q1 billings are more than 90 percent of Ellis\'s Q1 billings.',answer:false}],
 expl:'Chen: 440 x 300 = 132,000; Dube 360 x 160 = 57,600 plus Gomez 320 x 150 = 48,000 is 105,600 (Yes). Audit (2 + 5)/2 = 3.5 vs Tax (3 + 7)/2 = 5 (No). Bennett 385 x 180 = 69,300; Ellis 400 x 220 = 88,000; 90% of 88,000 is 79,200, and 69,300 is below it (No).',
 wrong:'Trap in statement 3: Bennett\'s hours are 96% of Ellis\'s, but billings also depend on rate.'},
{id:'D119',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,passageHtml:TA_TABLE2,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'Fairhaven has the highest population density of the eight cities.',answer:true},
  {text:'The city with the lowest median monthly rent also has the fewest annual transit rides.',answer:true},
  {text:'Exactly four of the cities have populations greater than 1,000,000.',answer:false}],
 expl:'Density (thousand per sq km): Fairhaven 1,010/380 = 2.66, Dorsey 2,050/780 = 2.63, Holt 2.5, Calder 2.3, Brenton 2.25, Ashford 2.0, Granger 1.6, Elmwood 1.3 (Yes). Elmwood has the lowest rent ($980) and fewest rides (18 million) (Yes). Populations over 1,000 thousand: Brenton, Dorsey, Fairhaven, three cities (No).',
 wrong:'Trap in statement 1: Dorsey is the largest city but is narrowly less dense than Fairhaven; compute rather than eyeball.'},
{id:'D120',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_csp',diff:4,passageHtml:TA_TABLE2,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'The median of the eight cities\' median monthly rents is greater than $1,400.',answer:false},
  {text:'Annual transit rides per resident are greater in Dorsey than in any other city.',answer:true},
  {text:'Ranking the cities from highest to lowest population produces the same order as ranking them from highest to lowest median rent.',answer:false}],
 expl:'Rents sorted: 980, 1,100, 1,200, 1,300, 1,450, 1,650, 1,720, 2,150; median (1,300 + 1,450)/2 = 1,375 (No). Rides per resident: Dorsey 480/2,050 = 234, Brenton 210/1,240 = 169, Fairhaven 149, Ashford 117, Granger 81, Holt 80, Calder 67, Elmwood 46 (Yes). Population order: Dorsey, Brenton, Fairhaven, Ashford, Granger, Calder, Elmwood, Holt; rent order: Dorsey, Brenton, Fairhaven, Ashford, Granger, Holt, Calder, Elmwood. The last three differ (No).',
 wrong:'Trap in statement 3: the top five match, tempting a Yes; check the tail.'},
{id:'D121',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_csp',diff:3,passageHtml:TA_TABLE3,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'The fund with the highest 1-year return has the highest expense ratio.',answer:true},
  {text:'The average (arithmetic mean) 5-year annualized return of the four Equity funds exceeds 9 percent.',answer:false},
  {text:'Total assets in the Equity funds are more than twice the total assets in all other funds combined.',answer:true}],
 expl:'Ember Small-Cap: 18.9% return, 1.10% expense ratio, both the highest (Yes). Equity 5-year mean: (9.8 + 10.4 + 8.2 + 7.5)/4 = 35.9/4 = 8.975, just under 9 (No). Equity assets 1,250 + 4,300 + 420 + 2,150 = 8,120; other funds 860 + 1,900 = 2,760; twice is 5,520 (Yes).',
 wrong:'Trap in statement 2: three of four values are near or above 9, but the mean is 8.975.'},
{id:'D122',section:'DI',type:'TA',domain:'math',skill:'di_gt',qskill:'q_csp',diff:4,passageHtml:TA_TABLE3,answerType:'ta',
 stem:'For each statement, select Yes if the statement is true based on the information in the table, otherwise select No.',
 statements:[
  {text:'For every fund listed, the 1-year return exceeded the 5-year annualized return.',answer:false},
  {text:'The fund with the lowest expense ratio has the largest assets.',answer:true},
  {text:'The median expense ratio of the six funds is 0.725 percent.',answer:true}],
 expl:'Cobalt Index: 1-year 9.9% is below its 5-year 10.4% (No). Cobalt Index has the lowest expense ratio (0.10%) and largest assets ($4,300 million) (Yes). Expense ratios sorted: 0.10, 0.45, 0.60, 0.85, 0.95, 1.10; median (0.60 + 0.85)/2 = 0.725 (Yes).',
 wrong:'Trap in statement 1: five funds satisfy the claim; "every" fails on one exception.'},

// ---- Two-Part Analysis (D123-D126) ----
{id:'D123',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_rrp',diff:4,answerType:'tpa',
 stem:'A wholesaler normally sells an item at a price 25 percent above its cost. During a sale, the wholesaler takes d percent off the normal selling price and still earns a profit equal to 10 percent of cost on each item. During the sale, the wholesaler sold 200 items for a total revenue of $8,800.\n\nSelect the value of d and the cost per item, in dollars. Make only two selections, one in each column.',
 columns:['Value of d','Cost per item ($)'],choices:['10','12','15','40','44','50'],answer:[1,3],
 expl:'Sale price = 1.10c and normal price = 1.25c, so (1 - d/100)(1.25) = 1.10, giving 1 - d/100 = 0.88 and d = 12. Sale price = 8,800/200 = 44 = 1.10c, so c = 40.',
 wrong:'Trap: computing d as 25 - 10 = 15. Percent markups do not subtract; the discount is on the marked-up price.'},
{id:'D124',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_csp',diff:4,answerType:'tpa',
 stem:'A committee of 3 people is to be selected from a group of 4 managers and 5 staff members.\n\nSelect the number of possible committees that include at least one manager, and the number of possible committees that include exactly two managers. Make only two selections, one in each column.',
 columns:['At least one manager','Exactly two managers'],choices:['30','40','60','74','80','84'],answer:[3,0],
 expl:'Total committees C(9,3) = 84. Committees with no manager: C(5,3) = 10, so at least one manager: 84 - 10 = 74. Exactly two managers: C(4,2) x C(5,1) = 6 x 5 = 30.',
 wrong:'Trap: counting "at least one" directly is slow; use the complement.'},
{id:'D125',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_alg',diff:5,answerType:'tpa',
 stem:'Pipe P alone fills a tank in p hours and Pipe Q alone fills the same tank in q hours, where p and q are positive integers. Working together at their constant rates, the two pipes fill the tank in 3 hours 45 minutes, and Pipe Q alone takes 4 hours longer than Pipe P alone.\n\nSelect the value of p and the value of q. Make only two selections, one in each column.',
 columns:['p','q'],choices:['4','5','6','10','12','15'],answer:[2,3],
 expl:'1/p + 1/q = 1/3.75 = 4/15. Candidates with integer p, q: (5, 15) and (6, 10). Only (6, 10) has q - p = 4. Check: 1/6 + 1/10 = 8/30 = 4/15.',
 wrong:'Trap: (5, 15) also satisfies the combined-rate equation; the "4 hours longer" condition selects (6, 10).'},
{id:'D126',section:'DI',type:'TPA',domain:'nonmath',skill:'di_tpa',diff:4,answerType:'tpa',
 stem:'City council member: Since the city installed automated speed cameras on Main Street last year, the number of traffic accidents on Main Street has fallen by 30 percent. Therefore, installing speed cameras on Oak Avenue will reduce accidents there as well.\n\nSelect the statement that, if true, most strengthens the council member\'s argument, and the statement that, if true, most weakens it. Make only two selections, one in each column.',
 columns:['Strengthens','Weakens'],
 choices:['Oak Avenue, like Main Street, is a four-lane road on which most accidents involve vehicles exceeding the speed limit.',
  'The speed cameras on Main Street cost the city about $120,000 each to install.',
  'The speed cameras on Main Street generated roughly $400,000 in fines last year.',
  'The council member who made the argument represents the district that contains Oak Avenue.',
  'Oak Avenue is scheduled to be resurfaced next year whether or not cameras are installed.',
  'Most accidents on Oak Avenue occur at a single intersection and involve drivers failing to yield rather than speeding.'],
 answer:[0,5],
 expl:'The argument is an analogy: cameras cut speeding-related accidents on Main Street, so they will on Oak Avenue. Statement 1 makes the two roads alike in the relevant respect (speeding causes accidents), strengthening. Statement 6 says Oak Avenue\'s accidents are not about speeding, so speed cameras would not address them, weakening. Cost, fines, the member\'s district, and resurfacing plans do not bear on whether cameras would reduce accidents.',
 wrong:'Trap: the fines statement feels like a criticism of the policy but says nothing about accident reduction.'},

// ---- Multi-Source Reasoning (D127-D130) ----
{id:'D127',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:3,passageHtml:MSR_SET2,
 stem:'Which of the five claims, as submitted, is ineligible for any reimbursement under the policy?',
 choices:['C1','C2','C3','C4','C5'],answer:1,
 expl:'C2 ended March 10 and was submitted April 15, 36 days later, beyond the 30-day window; the email confirms no exceptions. C1 (17 days), C3 (14), C4 (12), and C5 (16) are all within 30 days.'},
{id:'D128',section:'DI',type:'MSR',domain:'math',skill:'di_msr',qskill:'q_rrp',diff:4,passageHtml:MSR_SET2,
 stem:'Based on the policy and the director\'s email, what is the total reimbursable amount for Claim C5?',
 choices:['$1,490','$1,550','$1,610','$1,670','$1,730'],answer:2,
 expl:'Airfare $530 (economy, full) + lodging 4 x $180 = $720 (within either cap) + meals 5 x $60 = $300 + mileage 100 x $0.60 = $60. Total $1,610.',
 wrong:'Trap: forgetting the per diem, which is paid without receipts, or the mileage.'},
{id:'D129',section:'DI',type:'MSR',domain:'math',skill:'di_msr',qskill:'q_rrp',diff:4,passageHtml:MSR_SET2,
 stem:'The reimbursable total for Claim C3 exceeds the $2,000 sign-off threshold by how much?',
 choices:['$580','$680','$700','$740','$1,340'],answer:3,
 expl:'The 8-hour business-class flight qualifies for full reimbursement, $1,900. The trip ended March 14, before the new cap, but the director pre-approved the overage, so lodging is 3 x $200 = $600. Meals 4 x $60 = $240. Total $2,740, which is $740 over $2,000.',
 wrong:'Trap: $680 comes from capping lodging at $180 despite the pre-approval; $1,340 comes from capping the long-haul business fare at $500.'},
{id:'D130',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_SET2,
 stem:'Which of the following statements is supported by the information in the three tabs?',
 choices:['Exactly one of the five claims requires the director\'s sign-off before it can be paid.',
  'Claim C5\'s lodging would have exceeded the cap in effect before March 15.',
  'Claim C4\'s business-class airfare is reimbursed in full because the trip ended after March 15.',
  'Claim C1 would have been reimbursed a greater amount if the trip had ended after March 15.',
  'Claim C2 will be paid on Friday when the director reviews the queue.'],answer:0,
 expl:'Only C3 ($2,740) exceeds $2,000; C1 ($940), C4 ($831), and C5 ($1,610) do not, and C2 is ineligible. A is supported. C5 lodging is $180 per night, equal to the old cap, not above it. C4\'s 3-hour business flight is capped at $500 regardless of date. C1\'s $170 nights are under both caps, so nothing changes. C2 is late and is not in the sign-off queue.',
 wrong:'Trap in C: the email changes only the lodging cap, not the airfare rule.'}
];
