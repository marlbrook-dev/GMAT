// Start From Nowhere trainer: GMAT Focus Data Insights bank 3, original items D201 to D220.

const DS_CHOICES3 = ['Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.','Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.','BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.','EACH statement ALONE is sufficient.','Statements (1) and (2) TOGETHER are NOT sufficient.'];

const GT_TABLE5 = '<table class="dtable"><thead><tr><th>Region</th><th>Units sold 2024</th><th>Units sold 2025</th><th>Revenue 2025 ($ thousands)</th><th>Units returned 2025</th></tr></thead><tbody>'+
'<tr><td>North</td><td>800</td><td>1,000</td><td>240</td><td>25</td></tr>'+
'<tr><td>South</td><td>1,200</td><td>1,080</td><td>216</td><td>54</td></tr>'+
'<tr><td>East</td><td>500</td><td>650</td><td>169</td><td>13</td></tr>'+
'<tr><td>West</td><td>900</td><td>1,170</td><td>234</td><td>39</td></tr>'+
'<tr><td>Central</td><td>600</td><td>600</td><td>126</td><td>18</td></tr>'+
'</tbody></table><p class="dnote">Brewhaus Supply Co. sales of its single espresso machine model, by sales region, for 2024 and 2025.</p>';

const GT_TABLE6 = '<table class="dtable"><thead><tr><th>Route</th><th>Weekday riders 2023</th><th>Weekday riders 2025</th><th>Trips per weekday</th><th>Fare revenue per weekday ($)</th></tr></thead><tbody>'+
'<tr><td>A</td><td>1,500</td><td>1,800</td><td>60</td><td>2,880</td></tr>'+
'<tr><td>B</td><td>2,400</td><td>2,100</td><td>70</td><td>2,940</td></tr>'+
'<tr><td>C</td><td>900</td><td>1,170</td><td>45</td><td>1,872</td></tr>'+
'<tr><td>D</td><td>3,000</td><td>3,300</td><td>100</td><td>4,620</td></tr>'+
'<tr><td>E</td><td>1,200</td><td>1,500</td><td>50</td><td>2,400</td></tr>'+
'<tr><td>F</td><td>2,000</td><td>2,400</td><td>80</td><td>3,360</td></tr>'+
'</tbody></table><p class="dnote">Ridership and fare data for six bus routes in the Marlow City transit study; trips and revenue figures are for 2025.</p>';

const BANK_DI3 = [
{id:'D201',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:1,
stem:'A fitness club charges each new member a one-time enrollment fee plus the same fixed monthly rate. In dollars, what is the monthly rate?\n\n(1) A member who keeps the membership for exactly 6 months pays $390 in total, of which $60 is the enrollment fee.\n\n(2) Keeping the membership for exactly 10 months costs $220 more in total than keeping it for exactly 6 months.',
choices:DS_CHOICES3,answer:3,
expl:'From (1), the 6 monthly payments total 390 - 60 = 330, so the rate is 330/6 = 55 dollars: sufficient. From (2), the extra 4 months cost 220 dollars, and the enrollment fee cancels in the difference, so the rate is 220/4 = 55 dollars: sufficient. Each statement alone is sufficient.',
wrong:'The tempting answer A comes from thinking (2) fails because the enrollment fee is unknown; the fee appears in both totals and cancels, so (2) works alone.'},

{id:'D202',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_rrp',diff:2,
stem:'Last year, all of a bookstore\'s revenue came from print books and e-books. What percent of last year\'s revenue came from e-books?\n\n(1) Last year, revenue from e-books was $84,000 and total revenue was $240,000.\n\n(2) Last year, revenue from print books was $156,000.',
choices:DS_CHOICES3,answer:0,
expl:'Statement (1) gives the percent directly: 84,000/240,000 = 0.35, so 35 percent: sufficient. Statement (2) gives only the print figure with no total, so the percent cannot be computed: insufficient. Answer A.',
wrong:'Choosing C is the trap of combining when one statement already suffices; (2) alone gives no total, so B and D are out.'},

{id:'D203',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_csp',diff:3,
stem:'Of the 120 employees at a consulting firm, how many are enrolled in both the dental plan and the vision plan?\n\n(1) Of the 120 employees, 75 are enrolled in the dental plan and 60 are enrolled in the vision plan.\n\n(2) Of the 120 employees, 15 are enrolled in neither plan.',
choices:DS_CHOICES3,answer:2,
expl:'Let b be the number in both plans. From (1) alone, the number in neither plan is unknown, so b can be anything from 15 to 60: insufficient. Statement (2) alone gives no plan counts: insufficient. Together: 75 + 60 - b = 120 - 15 = 105, so b = 30: sufficient. Answer C.',
wrong:'Picking A assumes everyone is in at least one plan; without (2), the overlap is not pinned down.'},

{id:'D204',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_vof',diff:3,
stem:'What is the value of the two-digit positive integer n?\n\n(1) The sum of the digits of n is 9.\n\n(2) n is divisible by 9.',
choices:DS_CHOICES3,answer:4,
expl:'Statement (1): n could be 18, 27, 36, or any other two-digit number with digit sum 9: insufficient. Statement (2): n could be any multiple of 9 from 18 through 99: insufficient. Together: every two-digit number with digit sum 9 is already divisible by 9, so the combined list is still 18, 27, ..., 90: not sufficient. Answer E.',
wrong:'The trap is picking C: statement (2) adds nothing new, because digit sum 9 already forces divisibility by 9, so combining does not narrow the list to one value.'},

{id:'D205',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_rrp',diff:2,
stem:'Forty donors each made exactly one donation to a charity drive. In dollars, what was the average (arithmetic mean) donation?\n\n(1) The median donation was $50.\n\n(2) The total amount donated was $2,600.',
choices:DS_CHOICES3,answer:1,
expl:'The mean is the total divided by 40. Statement (2) gives 2,600/40 = 65 dollars: sufficient. Statement (1) gives only the median, and sets of 40 donations with median 50 can have many different means: insufficient. Answer B.',
wrong:'Confusing median with mean makes (1) look sufficient; the median does not determine the total.'},

{id:'D206',section:'DI',type:'DS',domain:'nonmath',skill:'di_ds',diff:3,
stem:'A cafe sells exactly two kinds of sandwich: turkey and veggie. Maria and Josh each bought exactly one sandwich at the cafe this morning. Did Maria buy a turkey sandwich?\n\n(1) Exactly one of the two sandwiches bought was a veggie sandwich.\n\n(2) Josh bought a veggie sandwich.',
choices:DS_CHOICES3,answer:2,
expl:'From (1) alone, either Maria or Josh could be the veggie buyer: insufficient. From (2) alone, Maria could still have bought either kind, since both could buy veggie: insufficient. Together, exactly one sandwich was veggie and it was Josh\'s, so Maria\'s sandwich must have been turkey: sufficient. Answer C.',
wrong:'Picking B assumes Josh\'s choice constrains Maria\'s; nothing stops both from buying veggie until (1) is added.'},

{id:'D207',section:'DI',type:'DS',domain:'nonmath',skill:'di_ds',diff:4,
stem:'A five-member library board consists of Flores, Grant, Ho, Ibarra, and Katz. In a vote on extending weekend hours, each member voted either for or against the extension, and exactly three members voted for it. Did Ibarra vote for the extension?\n\n(1) Flores and Grant both voted against the extension.\n\n(2) Exactly two members voted against the extension.',
choices:DS_CHOICES3,answer:0,
expl:'From (1), the three votes in favor must have come from Ho, Ibarra, and Katz, so Ibarra voted for the extension: sufficient. Statement (2) says two members voted against, which the stem already implies (five members, exactly three in favor), so it adds nothing: insufficient. Answer A.',
wrong:'Statement (2) is the classic trap: it repeats information the question stem already gave, so it helps neither alone nor in combination.'},

{id:'D208',section:'DI',type:'DS',domain:'math',skill:'di_ds',qskill:'q_alg',diff:4,
stem:'If x and y are positive integers, what is the value of x + y?\n\n(1) xy = 36\n\n(2) x^2 + 2xy + y^2 = 169',
choices:DS_CHOICES3,answer:1,
expl:'Statement (1): xy = 36 allows (1, 36), (4, 9), (6, 6), which give different sums: insufficient. Statement (2): x^2 + 2xy + y^2 = (x + y)^2 = 169, and x + y is positive, so x + y = 13: sufficient. Answer B.',
wrong:'Some test takers solve the pair to get x = 4 and y = 9 and pick C; others reject (2) because of the root -13, but positive integers force x + y = 13.'},

{id:'D209',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:2,
passageHtml:GT_TABLE5,
stem:'From 2024 to 2025, the number of units sold in the South region changed by what percent?',
choices:['A decrease of 12%','A decrease of 10%','A decrease of 8%','An increase of 10%','An increase of 12%'],answer:1,
expl:'South units went from 1,200 in 2024 to 1,080 in 2025, a change of -120. Since 120/1,200 = 0.10, units decreased by 10 percent.',
wrong:'Dividing 120 by the 2025 figure 1,080 gives about 11 percent and points to the 12 percent trap; the base of a percent change is the earlier value.'},

{id:'D210',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,
passageHtml:GT_TABLE5,
stem:'In 2025, which region had the greatest revenue per unit sold?',
choices:['North','South','East','West','Central'],answer:2,
expl:'Revenue per unit in 2025, in dollars: North 240,000/1,000 = 240; South 216,000/1,080 = 200; East 169,000/650 = 260; West 234,000/1,170 = 200; Central 126,000/600 = 210. East is greatest at $260 per unit.',
wrong:'North has the largest total revenue, which tempts anyone who skips the division; per unit sold, East leads.'},

{id:'D211',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,
passageHtml:GT_TABLE5,
stem:'For the East and Central regions combined, 2025 revenue per unit sold was',
choices:['$230','$235','$236','$240','$245'],answer:2,
expl:'Combined revenue is 169,000 + 126,000 = 295,000 dollars, and combined units are 650 + 600 = 1,250. So revenue per unit is 295,000/1,250 = 236 dollars.',
wrong:'Averaging the two per-unit figures, (260 + 210)/2 = 235, ignores the different unit counts; the combined figure must be weighted by units, so $235 is the trap.'},

{id:'D212',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,
passageHtml:GT_TABLE6,
stem:'What was the median of the six routes\' weekday ridership figures for 2025?',
choices:['1,800','1,875','1,950','2,100','2,250'],answer:2,
expl:'Sorted 2025 ridership: 1,170; 1,500; 1,800; 2,100; 2,400; 3,300. With six values, the median is the mean of the middle two: (1,800 + 2,100)/2 = 1,950.',
wrong:'Choosing 1,800 or 2,100 takes a single middle value; with an even count the median averages the two middle values.'},

{id:'D213',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:3,
passageHtml:GT_TABLE6,
stem:'From 2023 to 2025, which route had the greatest percent increase in weekday ridership?',
choices:['Route A','Route C','Route D','Route E','Route F'],answer:1,
expl:'Percent changes from 2023 to 2025: A rose 300/1,500 = 20 percent; B fell; C rose 270/900 = 30 percent; D rose 300/3,000 = 10 percent; E rose 300/1,200 = 25 percent; F rose 400/2,000 = 20 percent. Route C had the greatest percent increase.',
wrong:'Route F has the largest absolute gain, 400 riders, the absolute-versus-percent trap; relative to its small 2023 base, Route C grew fastest.'},

{id:'D214',section:'DI',type:'GT',domain:'math',skill:'di_gt',qskill:'q_rrp',diff:4,
passageHtml:GT_TABLE6,
stem:'Fare revenue per weekday for Route D was what percent greater than fare revenue per weekday for Route F?',
choices:['27.5%','32.5%','35%','37.5%','40%'],answer:3,
expl:'Route D revenue is $4,620 and Route F revenue is $3,360 per weekday. The difference is 1,260, and 1,260/3,360 = 0.375, so Route D is 37.5 percent greater.',
wrong:'Dividing 1,260 by 4,620 gives about 27.3 percent, the wrong-base trap that points to 27.5%; percent greater than F uses F as the base.'},

{id:'D215',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_alg',diff:3,answerType:'tpa',
stem:'A print shop charges every order a one-time setup fee plus a fixed price per poster. One customer paid $95 in total for an order of 25 posters, and another customer paid $155 in total for an order of 45 posters.\n\nIn the table, select the value of the setup fee and select the value of the price per poster. Make only two selections, one in each column.',
columns:['Setup fee','Price per poster'],
choices:['$2','$3','$5','$15','$20','$25'],answer:[4,1],
expl:'Subtracting the orders: the 20 extra posters cost 155 - 95 = 60 dollars, so each poster costs 60/20 = 3 dollars. Then the setup fee is 95 - 25 x 3 = 95 - 75 = 20 dollars. Check: 20 + 45 x 3 = 155.',
wrong:'Dividing 95 by 25 to get 3.80 mixes the fee into the per-poster price; the fee must be isolated by comparing the two orders.'},

{id:'D216',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_rrp',diff:3,answerType:'tpa',
stem:'A laboratory tank holds 40 liters of solution that is 15 percent acid by volume. A technician will add pure acid, and nothing else, until the solution is 32 percent acid by volume.\n\nIn the table, select the number of liters of pure acid the technician must add and select the total volume, in liters, of the resulting solution. Make only two selections, one in each column.',
columns:['Liters of acid added','Final volume (liters)'],
choices:['8','10','12','46','50','52'],answer:[1,4],
expl:'The tank starts with 0.15 x 40 = 6 liters of acid. Adding x liters of pure acid gives (6 + x)/(40 + x) = 0.32, so 6 + x = 12.8 + 0.32x, 0.68x = 6.8, x = 10. The final volume is 40 + 10 = 50 liters. Check: 16/50 = 32 percent.',
wrong:'Setting 0.32 x 40 = 12.8 and adding 12.8 - 6 = 6.8 liters forgets that the added acid also raises the total volume.'},

{id:'D217',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_csp',diff:4,answerType:'tpa',
stem:'A project team will be formed from a group of 5 analysts and 4 associates.\n\nIn the table, select the number of different two-person teams consisting of two analysts, and select the number of different two-person teams consisting of exactly one analyst and one associate. Make only two selections, one in each column.',
columns:['Two analysts','One analyst, one associate'],
choices:['6','10','15','20','25','36'],answer:[1,3],
expl:'Two analysts from 5: C(5, 2) = (5 x 4)/2 = 10 teams. One analyst and one associate: 5 x 4 = 20 teams, since the two picks are independent.',
wrong:'Using 5 x 4 = 20 for the analyst pair double counts ordered pairs; order does not matter within a team, so divide by 2.'},

{id:'D218',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_rrp',diff:4,answerType:'tpa',
stem:'Working alone at its constant rate, pump A fills an empty storage tank in 6 hours. Working alone at its constant rate, pump B fills the same tank in 12 hours. The two pumps will work together, each at its own constant rate, to fill the empty tank.\n\nIn the table, select the number of hours the two pumps working together take to fill the tank, and select the fraction of the tank that pump A fills during that time. Make only two selections, one in each column.',
columns:['Hours to fill the tank together','Fraction filled by pump A'],
choices:['3','4','9','1/2','2/3','3/4'],answer:[1,4],
expl:'The combined rate is 1/6 + 1/12 = 3/12 = 1/4 of the tank per hour, so together the pumps need 4 hours. In those 4 hours, pump A fills 4 x 1/6 = 2/3 of the tank.',
wrong:'Averaging 6 and 12 to get 9 hours is the classic rate trap; times do not average, rates add.'},

{id:'D219',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_alg',diff:5,answerType:'tpa',
stem:'A subscription startup\'s monthly recurring revenue grew by the same percent each month. Monthly recurring revenue was $50,000 in January and $72,000 in March of the same year, and the same percent growth continued through April.\n\nIn the table, select the percent by which monthly recurring revenue increased each month, and select the monthly recurring revenue in April. Make only two selections, one in each column.',
columns:['Monthly percent increase','April revenue'],
choices:['12%','20%','22%','$84,000','$86,400','$90,000'],answer:[1,4],
expl:'Two months of growth take 50,000 to 72,000, so the monthly factor r satisfies r^2 = 72,000/50,000 = 1.44, giving r = 1.2, a 20 percent increase per month. April is one month after March: 72,000 x 1.2 = 86,400 dollars.',
wrong:'Halving the 44 percent two-month gain gives the 22 percent trap; percent growth compounds, it does not add.'},

{id:'D220',section:'DI',type:'TPA',domain:'math',skill:'di_tpa',qskill:'q_csp',diff:5,answerType:'tpa',
stem:'The integer n satisfies 0 < n < 100. When n is divided by 7, the remainder is 3, and when n is divided by 5, the remainder is 4.\n\nIn the table, select the smallest possible value of n and select the largest possible value of n. Make only two selections, one in each column.',
columns:['Smallest value of n','Largest value of n'],
choices:['24','38','59','73','87','94'],answer:[0,5],
expl:'Remainder 3 on division by 7 gives n in 3, 10, 17, 24, 31, ...; remainder 4 on division by 5 means n ends in 4 or 9. The first number satisfying both is 24, and solutions then repeat every 35: 24, 59, 94. The smallest value is 24 and the largest below 100 is 94.',
wrong:'59 satisfies both conditions but is neither extreme; 38, 73, and 87 each satisfy only the division-by-7 condition.'}
];

