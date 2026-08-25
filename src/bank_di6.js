// bank_di6.js - Original GMAT Focus Data Insights items D261-D268: MSR set 3 plus TPA reinforcement
const MSR_SET3 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Vendor rules (Ridgeline Farmers Market)</h4><ul>'+
 '<li>Stalls are assigned only to vendors whose application is received at least 14 days before the market date.</li>'+
 '<li>At least 70 percent of the items a vendor lists for sale must be grown or made by the vendor. Resold items may not exceed 30 percent of listed items.</li>'+
 '<li>Vendors selling prepared food must attach a current county food-handler certificate to the application. Certificates expire 24 months after issue.</li>'+
 '<li>Standard stalls are 10 feet wide. A vendor may request a double stall; double stalls are granted only if at least one is still unassigned on the date the application is received.</li>'+
 '<li>The stall fee is 40 dollars for a standard stall and 70 dollars for a double stall. A vendor attending its first Ridgeline market pays half the stall fee.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: Applications received for the June 14 market</h4><table class="dtable"><thead><tr><th>Vendor</th><th>Received</th><th>Items listed (own / resold)</th><th>Stall requested</th><th>Notes</th></tr></thead><tbody>'+
 '<tr><td>Alder Farm</td><td>May 27</td><td>18 / 2</td><td>Standard</td><td>Returning vendor</td></tr>'+
 '<tr><td>Birch Bakery</td><td>May 30</td><td>10 / 4</td><td>Double</td><td>First market; prepared food; certificate issued 26 months ago</td></tr>'+
 '<tr><td>Cedar Orchards</td><td>June 2</td><td>12 / 6</td><td>Standard</td><td>Returning vendor</td></tr>'+
 '<tr><td>Dune Coffee</td><td>May 29</td><td>7 / 2</td><td>Double</td><td>First market; prepared food; certificate issued 8 months ago</td></tr>'+
 '<tr><td>Elm Woodcraft</td><td>June 5</td><td>15 / 0</td><td>Standard</td><td>Returning vendor</td></tr>'+
 '</tbody></table></div>'+
 '<div class="msrtab"><h4>Tab 3: Note from the market manager, June 3</h4><p>As of this morning, exactly one double stall remains unassigned for June 14. Reminder: the received date on an application is final, and rule checks use listed items only, not sales volumes.</p></div></div>';
const BANK_DI6 = [
{id:'D261',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:3,passageHtml:MSR_SET3,
 stem:'How many of the five applications satisfy the 14-day submission rule for the June 14 market?',
 choices:['1','2','3','4','5'],answer:2,
 expl:'Fourteen days before June 14 is May 31, so applications received on or before May 31 qualify. Alder (May 27), Birch (May 30), and Dune (May 29) qualify; Cedar (June 2) and Elm (June 5) do not. Three qualify.',
 wrong:'Counting June 2 as within 14 days is the common slip: June 14 minus 14 days lands at May 31, not early June.'},
{id:'D262',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_SET3,
 stem:'Which vendor violates the resold-items limit?',
 choices:['Alder Farm','Birch Bakery','Cedar Orchards','Dune Coffee','Elm Woodcraft'],answer:2,
 expl:'Resold items may not exceed 30 percent of listed items. Cedar lists 12 own plus 6 resold, 18 in all, so resold items are 6 of 18, which is 33 percent: over the limit. Birch is at 4 of 14 (29 percent), Dune at 2 of 9 (22 percent), Alder at 2 of 20 (10 percent), and Elm resells nothing.',
 wrong:'Birch looks close at 29 percent, but the rule is exceeds 30 percent; only Cedar crosses it. Comparing resold to own items (6 vs 12 = 50 percent) instead of to total listed items is the other slip.'},
{id:'D263',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_SET3,
 stem:'Based on the three tabs, which one of the following double-stall outcomes is consistent with the rules?',
 choices:['Both Birch Bakery and Dune Coffee receive double stalls','Dune Coffee receives a double stall and Birch Bakery does not','Birch Bakery receives a double stall and Dune Coffee does not','Neither vendor can receive a double stall','Elm Woodcraft receives the remaining double stall'],answer:1,
 expl:'Only one double stall remained as of June 3, and both requests were received in May, when at least that one stall was unassigned. But Birch\'s food-handler certificate was issued 26 months ago and has expired, so Birch\'s application fails regardless of stalls. Dune\'s certificate (8 months) is current and its application met the deadline, so Dune can take the remaining double stall.',
 wrong:'Both cannot receive double stalls with one remaining; Elm requested a standard stall and missed the deadline anyway.'},
{id:'D264',section:'DI',type:'MSR',domain:'math',skill:'di_msr',qskill:'q_rrp',diff:3,passageHtml:MSR_SET3,
 stem:'If Dune Coffee is assigned the double stall it requested, what stall fee does it pay?',
 choices:['20 dollars','35 dollars','40 dollars','55 dollars','70 dollars'],answer:1,
 expl:'A double stall costs 70 dollars, and Dune is attending its first Ridgeline market, so it pays half: 35 dollars.',
 wrong:'Halving the standard fee gives 20 dollars, and forgetting the first-market discount gives 70; both misread which fee the discount applies to.'},
{id:'D265',section:'DI',type:'TPA',domain:'algebra',skill:'di_tpa',qskill:'linear_equations',diff:2,
 stem:'A climbing gym sold 12 new memberships in one day: standard memberships at 45 dollars per month and premium memberships at 70 dollars per month. The 12 memberships total 615 dollars per month.\n\nSelect the number of standard memberships and the number of premium memberships sold. Make only two selections, one in each column.',
 answerType:'tpa',columns:['Standard','Premium'],
 choices:['2','3','5','7','9','10'],answer:[4,1],
 expl:'With s standard and 12 - s premium: 45s + 70(12 - s) = 615, so 840 - 25s = 615 and s = 9, leaving 3 premium. Check: 9 x 45 + 3 x 70 = 405 + 210 = 615.',
 wrong:'Swapping the columns (3 standard, 9 premium) gives 135 + 630 = 765, which overshoots the total.'},
{id:'D266',section:'DI',type:'TPA',domain:'algebra',skill:'di_tpa',qskill:'rates_work',diff:3,
 stem:'Machine A produces 40 parts per hour. Running together for 5 hours, machines A and B produce 450 parts.\n\nSelect the number of parts per hour machine B produces, and the number of hours machine B alone would need to produce 300 parts. Make only two selections, one in each column.',
 answerType:'tpa',columns:['Parts per hour for B','Hours for 300 parts'],
 choices:['5','6','30','40','50','60'],answer:[4,1],
 expl:'Together they make 450 / 5 = 90 parts per hour, so B makes 90 - 40 = 50 per hour. Alone, B needs 300 / 50 = 6 hours.',
 wrong:'Dividing 450 by 5 and forgetting to subtract A\'s rate leads to 90, not offered; picking 40 for B assumes the machines are identical.'},
{id:'D267',section:'DI',type:'TPA',domain:'arithmetic',skill:'di_tpa',qskill:'q_rrp',diff:4,
 stem:'A chemist has 8 liters of a solution that is 25 percent acid. She wants to add pure acid to make the solution 40 percent acid.\n\nSelect the amount of acid, in liters, that the 8-liter solution already contains, and the amount of pure acid, in liters, she must add. Make only two selections, one in each column.',
 answerType:'tpa',columns:['Acid already present','Pure acid to add'],
 choices:['1','2','3','4','5','6'],answer:[1,1],
 expl:'The solution holds 0.25 x 8 = 2 liters of acid. Adding x liters of pure acid: (2 + x) / (8 + x) = 0.4, so 2 + x = 3.2 + 0.4x, giving 0.6x = 1.2 and x = 2. Check: 4 liters acid in 10 liters is 40 percent.',
 wrong:'Taking 40 percent of the original 8 liters (3.2) forgets that adding acid also grows the total volume.'},
{id:'D268',section:'DI',type:'TPA',domain:'arithmetic',skill:'di_tpa',qskill:'q_rrp',diff:4,
 stem:'An investor puts 5000 dollars into an account earning 6 percent simple annual interest, and 5000 dollars into an account earning 20 percent total over the same period with no compounding within the period.\n\nSelect the interest, in dollars, the simple-interest account earns in 3 years, and the interest, in dollars, the second account earns over the period. Make only two selections, one in each column.',
 answerType:'tpa',columns:['Simple interest, 3 years','Second account'],
 choices:['300','600','900','1000','1200','1500'],answer:[2,3],
 expl:'Simple interest: 5000 x 0.06 x 3 = 900 dollars. The second account pays 20 percent of 5000 = 1000 dollars.',
 wrong:'Taking one year of simple interest (300) or applying 20 percent per year rather than for the whole period are the two standard misreads.'}
];
