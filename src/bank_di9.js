// bank_di9.js - Original GMAT Focus Data Insights items D298-D305: two more Multi-Source
// Reasoning sets. MSR remained the thinnest tracked skill after bank_di8.js, so this increment
// goes there again.
const MSR_SET10 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Scheduling rules</h4><ul>'+
 '<li>A course may be placed in a room only if the room capacity is at least the course enrollment cap.</li>'+
 '<li>A course designated as a lab must be placed in a room designated as a lab.</li>'+
 '<li>No instructor may be assigned two courses that meet at the same time.</li>'+
 '<li>A course whose enrollment cap exceeds 100 must meet in the lecture hall.</li>'+
 '<li>Courses numbered 300 or above may not meet before 10:00.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: Proposed schedule</h4><table class="dtable"><thead><tr><th>Course</th><th>Cap</th><th>Type</th><th>Room</th><th>Room capacity</th><th>Time</th><th>Instructor</th></tr></thead><tbody>'+
 '<tr><td>BIO 110</td><td>90</td><td>Lab</td><td>Hale 2 (lab)</td><td>100</td><td>09:00</td><td>Okonjo</td></tr>'+
 '<tr><td>BIO 320</td><td>40</td><td>Lab</td><td>Hale 2 (lab)</td><td>100</td><td>09:00</td><td>Reyes</td></tr>'+
 '<tr><td>CHM 105</td><td>120</td><td>Lecture</td><td>Lecture Hall</td><td>300</td><td>11:00</td><td>Okonjo</td></tr>'+
 '<tr><td>PHY 210</td><td>60</td><td>Lecture</td><td>Hale 2 (lab)</td><td>100</td><td>13:00</td><td>Reyes</td></tr>'+
 '<tr><td>MTH 340</td><td>35</td><td>Lecture</td><td>Sayre 4</td><td>30</td><td>14:00</td><td>Vance</td></tr></tbody></table></div>'+
 '<div class="msrtab"><h4>Tab 3: Registrar note</h4><ul>'+
 '<li>Two courses may share a room only if they meet at different times.</li>'+
 '<li>The lecture hall is the only room on campus with capacity above 150.</li>'+
 '<li>An enrollment cap may be lowered during scheduling but never raised.</li>'+
 '<li>A lecture course may be placed in a lab room; only the reverse is restricted.</li></ul></div></div>';
const MSR_SET11 = '<div class="msr"><div class="msrtab"><h4>Tab 1: Review criteria</h4><ul>'+
 '<li>Three reviewers score each proposal from 1 to 5 on novelty, feasibility, and impact. The table reports the mean for each criterion.</li>'+
 '<li>A proposal advances to the panel only if the mean of its three criterion means is at least 3.5.</li>'+
 '<li>A proposal whose mean on any single criterion falls below 2.5 is rejected regardless of its overall mean.</li>'+
 '<li>Proposals tied at the funding line are ranked by feasibility mean, higher first.</li></ul></div>'+
 '<div class="msrtab"><h4>Tab 2: Criterion means</h4><table class="dtable"><thead><tr><th>Proposal</th><th>Novelty</th><th>Feasibility</th><th>Impact</th></tr></thead><tbody>'+
 '<tr><td>Ardent</td><td>4.6</td><td>2.2</td><td>4.4</td></tr>'+
 '<tr><td>Brisk</td><td>3.6</td><td>3.5</td><td>3.4</td></tr>'+
 '<tr><td>Cobalt</td><td>3.0</td><td>4.0</td><td>3.4</td></tr>'+
 '<tr><td>Delta</td><td>4.2</td><td>3.2</td><td>3.1</td></tr>'+
 '<tr><td>Ember</td><td>2.8</td><td>3.6</td><td>3.2</td></tr></tbody></table></div>'+
 '<div class="msrtab"><h4>Tab 3: Panel note</h4><ul>'+
 '<li>Funding is available for exactly one proposal in this round.</li>'+
 '<li>Funding goes to the advancing proposal with the highest overall mean.</li>'+
 '<li>The panel may request a revised plan from any proposal rejected solely on a single-criterion floor.</li></ul></div></div>';
const BANK_DI9 = [
{id:'D298',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:3,passageHtml:MSR_SET10,
 stem:'How many of the five courses are scheduled in compliance with every rule exactly as proposed?',
 choices:['0','1','2','3','4'],answer:2,
 expl:'CHM 105 complies: its cap of 120 exceeds 100 and it is in the lecture hall, whose capacity of 300 is sufficient, and Okonjo other course meets at a different time. PHY 210 complies: a lecture course may sit in a lab room, capacity 100 covers a cap of 60, and Reyes other course meets at a different time. BIO 110 and BIO 320 both occupy Hale 2 at 09:00, which Tab 3 forbids, and BIO 320 also meets before 10:00 despite being numbered 320. MTH 340 has a cap of 35 in a room seating 30. Two comply.',
 wrong:'PHY 210 looks like a violation because a lecture sits in a lab. The last line of Tab 3 exists to settle that, and skipping it turns two compliant courses into one.'},
{id:'D299',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_SET10,
 stem:'Which single change would bring MTH 340 into compliance while keeping it in Sayre 4 at 14:00?',
 choices:['Lower its enrollment cap to 30','Raise its enrollment cap to 40','Assign Okonjo as its instructor','Designate Sayre 4 as a lab room','Renumber the course below 300'],answer:0,
 expl:'Its only violation is a cap of 35 in a room seating 30. Tab 3 permits lowering a cap but never raising one, so cutting the cap to 30 fits the room. Its 14:00 time already satisfies the rule for courses numbered 300 and above.',
 wrong:'Choice E is tempting because the course number appears in a rule, but 14:00 is after 10:00, so the number is causing no problem. Fix the rule the course actually breaks.'},
{id:'D300',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:4,passageHtml:MSR_SET10,
 stem:'Which pair of courses could not both be scheduled as proposed even if every other rule were satisfied?',
 choices:['BIO 110 and BIO 320','BIO 110 and CHM 105','CHM 105 and PHY 210','PHY 210 and MTH 340','BIO 320 and PHY 210'],answer:0,
 expl:'BIO 110 and BIO 320 are both in Hale 2 at 09:00, and Tab 3 allows two courses to share a room only at different times. No other proposed pair shares a room at the same time.',
 wrong:'Choice B pairs the two courses taught by Okonjo, but they meet at 09:00 and 11:00, so the instructor rule is satisfied. The conflict here is the room, not the instructor.'},
{id:'D301',section:'DI',type:'MSR',domain:'nonmath',skill:'di_msr',diff:5,passageHtml:MSR_SET10,
 stem:'Suppose BIO 320 is moved to 11:00 in Hale 2 and the enrollment cap for MTH 340 is lowered to 30. Which course, if any, would still fail a rule?',
 choices:['BIO 110','BIO 320','CHM 105','MTH 340','None of the five'],answer:4,
 expl:'At 11:00 BIO 320 clears the 10:00 restriction, Hale 2 is free at that hour, and Reyes other course meets at 13:00. BIO 110 then has Hale 2 to itself at 09:00. A cap of 30 fits Sayre 4. CHM 105 and PHY 210 were already compliant, so nothing fails.',
 wrong:'CHM 105 draws suspicion because Okonjo appears twice, but her courses run at 09:00 and 11:00. Re-check the full table after a change rather than assuming the course you did not touch is the problem.'},
{id:'D302',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:3,passageHtml:MSR_SET11,
 stem:'How many of the five proposals advance to the panel?',
 choices:['0','1','2','3','4'],answer:2,
 expl:'Overall means: Ardent (4.6 + 2.2 + 4.4)/3 = 3.73, Brisk 10.5/3 = 3.5, Cobalt 10.4/3 = 3.47, Delta 10.5/3 = 3.5, Ember 9.6/3 = 3.2. Brisk and Delta clear 3.5. Ardent clears the overall bar but its feasibility mean of 2.2 is below the 2.5 floor, so it is rejected. Two advance.',
 wrong:'Counting Ardent gives three. Its overall mean is the highest in the table, which is exactly why the single-criterion floor is written into Tab 1.'},
{id:'D303',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:4,passageHtml:MSR_SET11,
 stem:'Which proposal has the highest overall mean yet does not advance?',
 choices:['Ardent','Brisk','Cobalt','Delta','Ember'],answer:0,
 expl:'Ardent overall mean of about 3.73 is the highest of the five, but its feasibility mean of 2.2 falls below the 2.5 single-criterion floor, which rejects it regardless of the overall figure.',
 wrong:'Cobalt is the other proposal that fails to advance, but its overall mean of 3.47 is below the threshold and is not the highest of the five. Read which of the two conditions each proposal fails.'},
{id:'D304',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:4,passageHtml:MSR_SET11,
 stem:'Which proposal receives funding in this round?',
 choices:['Ardent','Brisk','Cobalt','Delta','Ember'],answer:1,
 expl:'Only Brisk and Delta advance, and both have an overall mean of exactly 3.5. Tab 1 breaks a tie by feasibility mean, higher first: Brisk 3.5 against Delta 3.2, so Brisk is funded.',
 wrong:'Delta has the highest novelty mean of the two, which makes it feel stronger. The tiebreak named in Tab 1 is feasibility, and reading the wrong column decides the round wrongly.'},
{id:'D305',section:'DI',type:'MSR',domain:'math',skill:'di_msr',diff:5,passageHtml:MSR_SET11,
 stem:'If Ardent submitted a revised plan that raised its feasibility mean to 2.6 with its other means unchanged, which proposal would receive funding?',
 choices:['Ardent','Brisk','Cobalt','Delta','Funding would be split between two proposals'],answer:0,
 expl:'Ardent new overall mean is (4.6 + 2.6 + 4.4)/3 = 3.87, and 2.6 clears the 2.5 floor, so it advances. At 3.87 it exceeds the 3.5 held by Brisk and Delta, and Tab 3 awards funding to the advancing proposal with the highest overall mean. No tiebreak is needed.',
 wrong:'Choice B assumes the earlier tiebreak still governs, but the tiebreak only applies to proposals that are actually tied. Ardent now stands above both.'}
];
