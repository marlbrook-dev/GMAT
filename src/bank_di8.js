// bank_di8.js - Original GMAT Focus Data Insights items D290-D297: two Multi-Source Reasoning
// sets. MSR was the thinnest skill in the bank (see ROADMAP), so this increment goes entirely there.
const MSR_SET8 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Retrofit grant rules</h4><ul>'+
 '<li>A grant covers 40 percent of verified retrofit cost, up to 60,000 dollars per building.</li>'+
 '<li>A building qualifies only if it was built before 1995 and has at least 10,000 square feet of conditioned floor area.</li>'+
 '<li>The application must include an energy audit completed within the previous 18 months.</li>'+
 '<li>A building that received a grant from this program within the previous five years is not eligible.</li>'+
 '<li>Buildings in the riverfront district are covered at 50 percent rather than 40 percent. The per-building cap is unchanged.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: Applications received</h4><table class="dtable"><thead><tr><th>Applicant</th><th>Year built</th><th>Floor area (sq ft)</th><th>Audit completed</th><th>Prior grant</th><th>District</th><th>Retrofit cost ($)</th></tr></thead><tbody>'+
 '<tr><td>Alder Mill</td><td>1972</td><td>24,000</td><td>8 months ago</td><td>None</td><td>Riverfront</td><td>180,000</td></tr>'+
 '<tr><td>Bellrose Court</td><td>1998</td><td>31,000</td><td>6 months ago</td><td>None</td><td>Central</td><td>210,000</td></tr>'+
 '<tr><td>Cedar Exchange</td><td>1988</td><td>9,200</td><td>3 months ago</td><td>None</td><td>Riverfront</td><td>60,000</td></tr>'+
 '<tr><td>Dunmore Hall</td><td>1965</td><td>45,000</td><td>26 months ago</td><td>None</td><td>Central</td><td>300,000</td></tr>'+
 '<tr><td>Eastgate Works</td><td>1981</td><td>15,000</td><td>11 months ago</td><td>2023</td><td>Central</td><td>120,000</td></tr></tbody></table></div>'+
 '<div class="msrtab"><h4>Tab 3: Committee memo</h4><ul>'+
 '<li>The current program year is 2026.</li>'+
 '<li>Council has asked for the total award value of this round before any appeal is heard.</li>'+
 '<li>An applicant found ineligible only because of the age of its audit may correct that document and be reconsidered in the same program year. Ineligibility based on a characteristic of the building itself is final for this round.</li></ul></div></div>';
const MSR_SET9 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Protocol summary</h4><ul>'+
 '<li>The trial enrolls adults aged 18 to 70 with a baseline symptom index of 12 or higher.</li>'+
 '<li>A participant must not have taken drug X within the 90 days before enrollment.</li>'+
 '<li>Each site may enroll at most 40 participants.</li>'+
 '<li>At least 35 percent of the participants enrolled at a site must come from the community clinic referral stream rather than the hospital stream.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: Site status</h4><table class="dtable"><thead><tr><th>Site</th><th>Enrolled</th><th>From community stream</th><th>Screen failures</th><th>Mean baseline index</th></tr></thead><tbody>'+
 '<tr><td>Northfield</td><td>40</td><td>12</td><td>9</td><td>16.2</td></tr>'+
 '<tr><td>Oakmere</td><td>28</td><td>14</td><td>4</td><td>14.8</td></tr>'+
 '<tr><td>Pinehurst</td><td>36</td><td>18</td><td>11</td><td>17.1</td></tr>'+
 '<tr><td>Quarry Road</td><td>22</td><td>6</td><td>3</td><td>13.4</td></tr></tbody></table></div>'+
 '<div class="msrtab"><h4>Tab 3: Monitor note</h4><ul>'+
 '<li>A site below the community stream minimum must pause hospital stream enrollment until the minimum is met.</li>'+
 '<li>Screen failure rate is screen failures divided by the sum of enrolled participants and screen failures.</li>'+
 '<li>Screen failures are not enrolled participants and do not count toward a site cap.</li></ul></div></div>';
const BANK_DI8 = [
{id:'D290',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:3,passageHtml:MSR_SET8,
 stem:'How many of the five applications are eligible for a grant exactly as submitted?',
 choices:['0','1','2','3','4'],answer:1,
 expl:'Alder Mill clears every rule: built 1972, 24,000 square feet, audit 8 months old, no prior grant. Bellrose Court was built in 1998, after the 1995 cutoff. Cedar Exchange has 9,200 square feet, under the 10,000 minimum. Dunmore Hall submitted an audit 26 months old, past the 18-month window. Eastgate Works took a grant in 2023, inside the five-year bar for program year 2026. One application survives.',
 wrong:'Reading only Tab 2 makes four or five of these look fine. Each row fails on a different rule, so the set has to be checked against every line of Tab 1, plus the program year that only appears in Tab 3.'},
{id:'D291',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:4,passageHtml:MSR_SET8,
 stem:'What is the grant award for Alder Mill?',
 choices:['$60,000','$72,000','$90,000','$108,000','$180,000'],answer:0,
 expl:'Alder Mill is in the riverfront district, so the cover rate is 50 percent: 0.50 x 180,000 = 90,000. The per-building cap of 60,000 still applies and is not raised for riverfront buildings, so the award is 60,000 dollars.',
 wrong:'Choice C is the uncapped calculation and choice B is the 40 percent rate. The last line of Tab 1 raises the rate and explicitly leaves the cap alone, which is the whole point of the item.'},
{id:'D292',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_SET8,
 stem:'Which applicant could be reconsidered in the same program year by correcting a document?',
 choices:['Alder Mill','Bellrose Court','Cedar Exchange','Eastgate Works','Dunmore Hall'],answer:4,
 expl:'Tab 3 allows reconsideration only where the sole defect is the age of the audit. Dunmore Hall fails on that ground alone: built 1965, 45,000 square feet, no prior grant. Bellrose Court and Cedar Exchange fail on building characteristics, and Eastgate Works fails on grant history, none of which a document fixes.',
 wrong:'Eastgate Works is the tempting pick because a grant record feels like paperwork. Tab 3 names the audit specifically, and the five-year bar is a fact about the building, not a document to resubmit.'},
{id:'D293',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:5,passageHtml:MSR_SET8,
 stem:'If Dunmore Hall submits a current audit and is approved, what is the total award value for this round?',
 choices:['$60,000','$120,000','$150,000','$180,000','$240,000'],answer:1,
 expl:'Alder Mill is awarded 60,000 after the cap. Dunmore Hall is in the central district, so 40 percent of 300,000 is 120,000, which the cap reduces to 60,000. The two awards total 120,000 dollars.',
 wrong:'Choice D adds the two uncapped figures. Both buildings are expensive enough that the cap binds, which is easy to apply to the first calculation and forget on the second.'},
{id:'D294',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:3,passageHtml:MSR_SET9,
 stem:'Which sites currently meet the community stream minimum?',
 choices:['Oakmere only','Oakmere and Pinehurst','Pinehurst only','Northfield and Pinehurst','All four sites'],answer:1,
 expl:'Compare the community share with 35 percent: Northfield 12 of 40 is 30 percent, Oakmere 14 of 28 is 50 percent, Pinehurst 18 of 36 is 50 percent, Quarry Road 6 of 22 is about 27 percent. Oakmere and Pinehurst clear the bar.',
 wrong:'Northfield has the largest raw number of community enrollments and still misses. The rule is a share of that site total, so the count alone decides nothing.'},
{id:'D295',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:4,passageHtml:MSR_SET9,
 stem:'Which site has the highest screen failure rate as Tab 3 defines it?',
 choices:['Pinehurst','Northfield','Oakmere','Quarry Road','Northfield and Pinehurst are tied'],answer:0,
 expl:'Rate is failures over failures plus enrolled: Northfield 9 of 49 is about 18 percent, Oakmere 4 of 32 is 12.5 percent, Pinehurst 11 of 47 is about 23 percent, Quarry Road 3 of 25 is 12 percent. Pinehurst is highest.',
 wrong:'Dividing failures by enrolled alone still ranks Pinehurst first here, but it gives the wrong figures, and a definition buried in Tab 3 is exactly the kind of line the next question turns on.'},
{id:'D296',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:4,passageHtml:MSR_SET9,
 stem:'Quarry Road has paused hospital stream enrollment. What is the smallest number of additional community stream participants it must enroll to meet the minimum?',
 choices:['1','2','3','4','5'],answer:2,
 expl:'With x more community participants and no hospital additions, the share is (6 + x)/(22 + x), which must reach 0.35. That gives 6 + x at least 7.7 + 0.35x, so 0.65x is at least 1.7 and x is at least about 2.6. Since x is a whole number, 3 participants are needed, giving 9 of 25, or 36 percent.',
 wrong:'Choice B comes from comparing 6 with 35 percent of the current 22 and rounding down. Every participant added raises the denominator as well as the numerator, so the target moves while you chase it.'},
{id:'D297',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:5,passageHtml:MSR_SET9,
 stem:'Which of the following must be true of Northfield?',
 choices:['It has the lowest screen failure rate of the four sites.','It meets the community stream minimum once screen failures are excluded.','It cannot reach the community stream minimum by enrolling additional participants.','It may enroll up to four more community stream participants.','Its mean baseline index disqualifies it from the trial.'],answer:2,
 expl:'Northfield is at the 40-participant cap, so it cannot enroll anyone else, and 12 of 40 is 30 percent. With no additions possible, no further enrollment can lift the share to 35 percent.',
 wrong:'Choice B is the trap: Tab 3 says screen failures were never enrolled participants, so leaving them out changes nothing about the 12 of 40. Choice D ignores the cap that Tab 1 sets.'}
];
