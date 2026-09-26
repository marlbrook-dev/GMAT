// bank_act_science.js - Original ACT Science items AS001-AS042.
// Four answer choices. Skills are ACT's three published reporting categories for Science:
// Interpretation of Data, Scientific Investigation, and Evaluation of Scientific Arguments and
// Models with Evidence. ACT also publishes three presentation formats and their shares of the
// section: Data Representation 26 to 32 percent, Research Summaries 50 to 56 percent, and
// Conflicting Viewpoints 18 to 21 percent. The six scenarios here are two, three and one of
// those formats respectively, which sits inside every published range.
// Data is carried as an HTML table so the numbers render as a table rather than as prose.
// Every key is readable off the data; nothing requires outside knowledge beyond an
// introductory course, which is the standard ACT sets.
const AS_S1 = '<p><b>Study 1: Infiltration and soil texture</b></p><p>Researchers measured the steady infiltration rate of water into five soils of differing clay content. Each soil was packed to the same bulk density and ponded with 20 mm of water.</p>'
 + '<table><thead><tr><th>Soil</th><th>Clay (%)</th><th>Organic matter (%)</th><th>Infiltration rate (mm/hr)</th></tr></thead><tbody>'
 + '<tr><td>Sandy loam</td><td>8</td><td>2.1</td><td>42</td></tr>'
 + '<tr><td>Loam</td><td>18</td><td>3.4</td><td>26</td></tr>'
 + '<tr><td>Silt loam</td><td>22</td><td>2.0</td><td>19</td></tr>'
 + '<tr><td>Clay loam</td><td>31</td><td>3.6</td><td>11</td></tr>'
 + '<tr><td>Clay</td><td>44</td><td>2.2</td><td>4</td></tr>'
 + '</tbody></table>';
const AS_S2 = '<p><b>Study 2: Germination of four wildflower species</b></p><p><i>Experiment 1.</i> Seeds of species W were held at six temperatures in darkness for 21 days. Percent germination was recorded.</p>'
 + '<table><thead><tr><th>Temperature (deg C)</th><th>5</th><th>10</th><th>15</th><th>20</th><th>25</th><th>30</th></tr></thead>'
 + '<tbody><tr><td>Germination (%)</td><td>4</td><td>21</td><td>58</td><td>77</td><td>63</td><td>19</td></tr></tbody></table>'
 + '<p><i>Experiment 2.</i> Seeds of four species were held at 20 deg C for 21 days, half in continuous light and half in darkness.</p>'
 + '<table><thead><tr><th>Species</th><th>Germination in light (%)</th><th>Germination in darkness (%)</th></tr></thead><tbody>'
 + '<tr><td>W</td><td>74</td><td>77</td></tr><tr><td>X</td><td>81</td><td>12</td></tr>'
 + '<tr><td>Y</td><td>9</td><td>68</td></tr><tr><td>Z</td><td>55</td><td>51</td></tr></tbody></table>'
 + '<p><i>Experiment 3.</i> Seeds of species Y were scarified (seed coat abraded) and then treated as in Experiment 2.</p>'
 + '<table><thead><tr><th>Treatment</th><th>Germination in light (%)</th><th>Germination in darkness (%)</th></tr></thead><tbody>'
 + '<tr><td>Scarified</td><td>66</td><td>71</td></tr><tr><td>Not scarified</td><td>9</td><td>68</td></tr></tbody></table>';
const AS_S3 = '<p><b>Study 3: Suspended sediment in a river</b></p><p>Discharge and suspended sediment concentration were measured at one station on 8 days spread across a year.</p>'
 + '<table><thead><tr><th>Day</th><th>Discharge (m3/s)</th><th>Suspended sediment (mg/L)</th><th>Water temperature (deg C)</th></tr></thead><tbody>'
 + '<tr><td>1</td><td>3</td><td>11</td><td>4</td></tr><tr><td>2</td><td>7</td><td>24</td><td>6</td></tr>'
 + '<tr><td>3</td><td>12</td><td>48</td><td>11</td></tr><tr><td>4</td><td>21</td><td>102</td><td>14</td></tr>'
 + '<tr><td>5</td><td>34</td><td>196</td><td>18</td></tr><tr><td>6</td><td>48</td><td>310</td><td>19</td></tr>'
 + '<tr><td>7</td><td>19</td><td>78</td><td>21</td></tr><tr><td>8</td><td>6</td><td>17</td><td>9</td></tr></tbody></table>';
const AS_S4 = '<p><b>Study 4: Corrosion of coated steel</b></p><p><i>Experiment 1.</i> Steel coupons of equal area received one of three coatings, or none, and were held in a salt spray chamber. Mass loss was measured after 200, 400 and 800 hours.</p>'
 + '<table><thead><tr><th>Coating</th><th>Mass loss at 200 h (mg)</th><th>Mass loss at 400 h (mg)</th><th>Mass loss at 800 h (mg)</th></tr></thead><tbody>'
 + '<tr><td>None</td><td>118</td><td>241</td><td>495</td></tr><tr><td>P</td><td>22</td><td>49</td><td>126</td></tr>'
 + '<tr><td>Q</td><td>9</td><td>18</td><td>151</td></tr><tr><td>R</td><td>31</td><td>63</td><td>129</td></tr></tbody></table>'
 + '<p><i>Experiment 2.</i> Coated coupons were scratched through the coating before the same exposure.</p>'
 + '<table><thead><tr><th>Coating</th><th>Mass loss at 800 h, unscratched (mg)</th><th>Mass loss at 800 h, scratched (mg)</th></tr></thead><tbody>'
 + '<tr><td>P</td><td>126</td><td>402</td></tr><tr><td>Q</td><td>151</td><td>171</td></tr>'
 + '<tr><td>R</td><td>129</td><td>158</td></tr></tbody></table>';
const AS_S5 = '<p><b>Study 5: Algal growth, light and nitrate</b></p><p><i>Experiment 1.</i> Cultures of a green alga were grown for 6 days at five light intensities with nitrate held at 40 micromol/L.</p>'
 + '<table><thead><tr><th>Light (micromol photons/m2/s)</th><th>25</th><th>50</th><th>100</th><th>200</th><th>400</th></tr></thead>'
 + '<tbody><tr><td>Growth rate (divisions/day)</td><td>0.21</td><td>0.44</td><td>0.78</td><td>0.92</td><td>0.90</td></tr></tbody></table>'
 + '<p><i>Experiment 2.</i> The procedure was repeated with nitrate reduced to 5 micromol/L.</p>'
 + '<table><thead><tr><th>Light (micromol photons/m2/s)</th><th>25</th><th>50</th><th>100</th><th>200</th><th>400</th></tr></thead>'
 + '<tbody><tr><td>Growth rate (divisions/day)</td><td>0.19</td><td>0.33</td><td>0.38</td><td>0.39</td><td>0.38</td></tr></tbody></table>';
const AS_S6 = '<p><b>Study 6: Conflicting viewpoints on a lake trout decline</b></p><p>Lake trout numbers in Lake Verrin fell by about 70 percent between 1995 and 2020. Two scientists explain the decline.</p>'
 + '<p><b>Scientist 1.</b> The cause is warming of the lake. Lake trout require water below 12 deg C with dissolved oxygen above 6 mg/L. Since 1995 the surface has warmed and the summer thermocline has deepened, so the cold layer that also holds enough oxygen has thinned from about 9 m to about 3 m. Trout are squeezed into a narrower band each summer, which reduces feeding and increases mortality. Introduced smelt have been present since the 1970s without any decline, so predation on young trout cannot be new.</p>'
 + '<p><b>Scientist 2.</b> The cause is the collapse of the deepwater sculpin, the main prey of adult trout, which fell sharply after 1995. Sculpin were displaced by smelt, whose numbers rose after a change in stocking practice in 1994. Adult trout switched to smelt, which carry an enzyme that destroys thiamine, and thiamine-deficient trout produce fry that die within weeks. Warming is real but the cold oxygenated layer, though thinner, is still wide enough to hold the historical population.</p>';
const BANK_ACT_SCIENCE = [
// ---------- Scenario 1: Data Representation ----------
{id:'AS001',section:'S',type:'S',passageId:'ASS1',passageHtml:AS_S1,sub:'Reading a table',skill:'act_s_iod',diff:1,
 stem:'According to Study 1, the soil with the highest infiltration rate had a clay content of:',
 choices:['8%','18%','31%','44%'],answer:0,
 expl:'The highest infiltration rate in the table is 42 mm/hr, recorded for sandy loam, whose clay content is 8 percent.',
 wrong:'The other values belong to loam, clay loam and clay, whose infiltration rates are 26, 11 and 4 mm/hr.'},
{id:'AS002',section:'S',type:'S',passageId:'ASS1',passageHtml:AS_S1,sub:'Trend',skill:'act_s_iod',diff:2,
 stem:'Based on Study 1, as clay content increases across the five soils, infiltration rate:',
 choices:['increases only','decreases only','increases and then decreases','remains approximately constant'],answer:1,
 expl:'Infiltration falls from 42 to 26 to 19 to 11 to 4 mm/hr as clay rises from 8 to 44 percent, a decrease at every step.',
 wrong:'No step in the table shows an increase, and the total change from 42 to 4 rules out a constant value.'},
{id:'AS003',section:'S',type:'S',passageId:'ASS1',passageHtml:AS_S1,sub:'Interpolation',skill:'act_s_iod',diff:3,
 stem:'A sixth soil has a clay content of 26%. Based on Study 1, its infiltration rate would most likely be:',
 choices:['between 26 and 42 mm/hr','between 4 and 11 mm/hr','between 11 and 19 mm/hr','between 19 and 26 mm/hr'],answer:2,
 expl:'A clay content of 26 percent falls between silt loam at 22 percent and clay loam at 31 percent, whose rates are 19 and 11 mm/hr. Since the rate falls steadily with clay, the value lies between those two.',
 wrong:'The other ranges correspond to clay contents above 31 percent or below 22 percent.'},
{id:'AS004',section:'S',type:'S',passageId:'ASS1',passageHtml:AS_S1,sub:'Controlling variables',skill:'act_s_si',diff:3,
 stem:'Packing every soil to the same bulk density was most likely done in order to:',
 choices:['allow organic matter content to be calculated from the soil mass','guarantee that infiltration would be complete within one hour','ensure that each soil received exactly 20 mm of ponded water','prevent differences in compaction from affecting the measured rates'],answer:3,
 expl:'Bulk density controls how tightly the soil is packed, which strongly affects pore space and therefore infiltration. Holding it constant isolates texture as the variable being compared.',
 wrong:'The ponded depth is set separately, organic matter was measured rather than derived, and nothing in the design fixes a completion time.'},
{id:'AS005',section:'S',type:'S',passageId:'ASS1',passageHtml:AS_S1,sub:'Experimental design',skill:'act_s_si',diff:3,
 stem:'A student claims that organic matter content determines infiltration rate. The data in Study 1 argue against this claim mainly because:',
 choices:['the soil with the most organic matter does not have the highest infiltration rate','organic matter content was deliberately held constant across all five of the soils tested','infiltration rate was measured only once for each soil','organic matter was not measured for every soil in the study that was tested'],answer:0,
 expl:'Clay loam has the highest organic matter at 3.6 percent but an infiltration rate of only 11 mm/hr, while sandy loam has 2.1 percent and the highest rate of 42. Organic matter does not track the rate.',
 wrong:'Organic matter was reported for all five soils and clearly varies, and a single measurement per soil does not by itself speak to which variable matters.'},
{id:'AS006',section:'S',type:'S',passageId:'ASS1',passageHtml:AS_S1,sub:'Evaluating a model',skill:'act_s_esa',diff:4,
 stem:'A model predicts that infiltration rate is inversely proportional to clay content. Is this model consistent with Study 1?',
 choices:['Yes, because infiltration rate decreases as clay content increases.','No, because clay has about 5 times the clay content of sandy loam but about one tenth the rate.','No, because infiltration rate and clay content are not related in the data shown in Table 1.','Yes, because a soil with about 4 times the clay of sandy loam shows about one quarter its rate.'],answer:1,
 expl:'Inverse proportionality means the product of the two is constant. Sandy loam gives 8 times 42, which is 336; clay gives 44 times 4, which is 176. Clay has 5.5 times the clay content but roughly one tenth the rate, a steeper fall than inverse proportion allows.',
 wrong:'A decreasing relationship is necessary but not sufficient for inverse proportionality, and the data clearly do show a relationship, so denying one contradicts the table.'},
{id:'AS007',section:'S',type:'S',passageId:'ASS1',passageHtml:AS_S1,sub:'Drawing a conclusion',skill:'act_s_esa',diff:3,
 stem:'A farmer wants the field least likely to pond water during heavy rain. Based on Study 1, the best choice would be the field with soil that is:',
 choices:['31% clay, because moderate clay balances drainage and retention','18% clay, because loam is the most common agricultural soil','8% clay, because it admits water fastest','44% clay, because dense soils hold water at the surface'],answer:2,
 expl:'Ponding happens when rain arrives faster than water can enter the soil, so the soil with the highest infiltration rate ponds least. That is the sandy loam at 8 percent clay and 42 mm/hr.',
 wrong:'Higher clay means slower infiltration and therefore more ponding, and how common a soil is has no bearing on the rate.'},
// ---------- Scenario 2: Research Summaries ----------
{id:'AS008',section:'S',type:'S',passageId:'ASS2',passageHtml:AS_S2,sub:'Reading a table',skill:'act_s_iod',diff:1,
 stem:'In Experiment 1, germination of species W was highest at a temperature of:',
 choices:['25 deg C','30 deg C','15 deg C','20 deg C'],answer:3,
 expl:'The row of germination percentages peaks at 77 percent, which is recorded at 20 degrees Celsius.',
 wrong:'Germination at 15, 25 and 30 degrees was 58, 63 and 19 percent respectively, all below the peak.'},
{id:'AS009',section:'S',type:'S',passageId:'ASS2',passageHtml:AS_S2,sub:'Trend',skill:'act_s_iod',diff:2,
 stem:'Based on Experiment 1, as temperature rose from 5 to 30 deg C, germination of species W:',
 choices:['rose to a maximum and then fell','stayed near 50 percent throughout','rose steadily throughout','fell steadily throughout'],answer:0,
 expl:'Germination climbs from 4 percent at 5 degrees to 77 percent at 20 degrees, then falls to 63 and 19 percent at 25 and 30 degrees.',
 wrong:'Neither a steady rise nor a steady fall fits both halves of the curve, and the values range from 4 to 77 percent rather than hovering near 50.'},
{id:'AS010',section:'S',type:'S',passageId:'ASS2',passageHtml:AS_S2,sub:'Comparing conditions',skill:'act_s_iod',diff:3,
 stem:'In Experiment 2, which species showed the largest difference between germination in light and in darkness?',
 choices:['X','Y','Z','W'],answer:1,
 expl:'The differences are 3 for W, 69 for X, 59 for Y and 4 for Z. The largest is species X at 69 percentage points.',
 wrong:'Species Y is the second largest at 59 points, and W and Z differ by only a few points either way.'},
{id:'AS011',section:'S',type:'S',passageId:'ASS2',passageHtml:AS_S2,sub:'Purpose of a step',skill:'act_s_si',diff:3,
 stem:'Holding the seeds in Experiment 2 at 20 deg C rather than at 30 deg C was most likely intended to:',
 choices:['match the temperature at which the seeds had been stored before the trial began','test whether temperature and light interact in species X','keep germination near the maximum found in Experiment 1 so light effects would be visible','reduce the total amount of time required to complete the experiment and read the results for all four species'],answer:2,
 expl:'Experiment 1 identified 20 degrees as the temperature giving the highest germination. Running the light comparison there avoids a temperature so poor that germination is low in both treatments and any light effect is hidden.',
 wrong:'Only one temperature was used, so no interaction could be tested, and neither run time nor storage temperature is mentioned.'},
{id:'AS012',section:'S',type:'S',passageId:'ASS2',passageHtml:AS_S2,sub:'Experimental design',skill:'act_s_si',diff:4,
 stem:'Experiment 3 differs from Experiment 2 in that Experiment 3:',
 choices:['tested more species over a wider range of temperatures','measured germination after a longer period of time','used darkness only rather than both light and darkness','tested a single species and added a seed coat treatment'],answer:3,
 expl:'Experiment 3 used species Y alone and compared scarified with unscarified seeds, keeping the light and darkness comparison and the 21 days from Experiment 2.',
 wrong:'It narrowed rather than widened the species set, kept the same duration, and retained both light conditions.'},
{id:'AS013',section:'S',type:'S',passageId:'ASS2',passageHtml:AS_S2,sub:'Evaluating a claim',skill:'act_s_esa',diff:4,
 stem:'Do the results of Experiment 3 support the claim that light itself inhibits germination in species Y?',
 choices:['No, because scarification removed almost all of the difference between light and darkness.','No, because species Y germinated better in light than in darkness once scarified by the method described.','Yes, because germination in light remained below germination in darkness after scarification.','Yes, because scarification raised germination in darkness from 68 to 71 percent.'],answer:0,
 expl:'Unscarified seeds gave 9 percent in light against 68 in darkness, a gap of 59 points. After scarification the figures were 66 and 71, a gap of 5. If light itself were inhibiting, abrading the seed coat should not have removed the effect.',
 wrong:'Germination in light still sits slightly below darkness after scarification, so the last option misreads the table, and a 3 point change in darkness is not the comparison at issue.'},
{id:'AS014',section:'S',type:'S',passageId:'ASS2',passageHtml:AS_S2,sub:'Predicting a result',skill:'act_s_esa',diff:4,
 stem:'Suppose species X seeds were scarified and then tested as in Experiment 3. If the seed coat explanation that fits species Y also applied to species X, germination of scarified species X would be expected to be:',
 choices:['well below 12 percent in both light and darkness','similar in light and darkness, at a level near the higher of its two previous values','near zero in light and near 81 percent in darkness','near 81 percent in light and near 12 percent in darkness, as before'],answer:1,
 expl:'For species Y, scarification removed the gap and lifted the low condition up to meet the high one. Applying the same pattern to species X, whose low condition is darkness at 12 percent, predicts both conditions near its higher value of about 81 percent.',
 wrong:'Retaining the original gap is what scarification undid for species Y, a fall in both conditions reverses the observed effect, and reversing which condition is higher is not what the seed coat explanation predicts.'},
// ---------- Scenario 3: Data Representation ----------
{id:'AS015',section:'S',type:'S',passageId:'ASS3',passageHtml:AS_S3,sub:'Reading a table',skill:'act_s_iod',diff:1,
 stem:'On which day was suspended sediment concentration highest?',
 choices:['Day 4','Day 5','Day 6','Day 7'],answer:2,
 expl:'Day 6 records 310 mg/L, the highest value in the sediment column.',
 wrong:'Days 4, 5 and 7 record 102, 196 and 78 mg/L.'},
{id:'AS016',section:'S',type:'S',passageId:'ASS3',passageHtml:AS_S3,sub:'Relationship',skill:'act_s_iod',diff:2,
 stem:'The data in Study 3 indicate that suspended sediment concentration is most closely related to:',
 choices:['water temperature','the day number','none of the measured variables','discharge'],answer:3,
 expl:'Sediment rises and falls with discharge at every point in the table, from 11 mg/L at 3 m3/s up to 310 mg/L at 48 m3/s and back to 17 mg/L at 6 m3/s.',
 wrong:'Temperature does not track sediment, since day 7 is the warmest at 21 degrees but carries only 78 mg/L, and day number is simply the order of sampling.'},
{id:'AS017',section:'S',type:'S',passageId:'ASS3',passageHtml:AS_S3,sub:'Calculation',skill:'act_s_iod',diff:3,
 stem:'Between Day 3 and Day 6, discharge increased by a factor of about 4. Over the same interval, suspended sediment increased by a factor of about:',
 choices:['6','10','2','4'],answer:0,
 expl:'Sediment rose from 48 mg/L on day 3 to 310 mg/L on day 6. Dividing gives about 6.5, so a factor of roughly 6.',
 wrong:'A factor of 4 would give about 192 mg/L and a factor of 10 would give 480, neither of which matches the recorded 310.'},
{id:'AS018',section:'S',type:'S',passageId:'ASS3',passageHtml:AS_S3,sub:'Comparing measurements',skill:'act_s_iod',diff:3,
 stem:'Days 2 and 8 had similar discharges. Which statement about those two days is supported by the table?',
 choices:['Neither sediment nor water temperature can be compared between the two days.','Sediment was similar on the two days although water temperature differed.','Sediment differed greatly although water temperature was the same on both of the days.','Both sediment and water temperature were much higher on Day 8.'],answer:1,
 expl:'Day 2 had 7 m3/s, 24 mg/L and 6 degrees; day 8 had 6 m3/s, 17 mg/L and 9 degrees. The sediment values are close while the temperatures differ by 3 degrees.',
 wrong:'The temperatures are not the same, day 8 is lower in sediment rather than higher, and both quantities are recorded for both days.'},
{id:'AS019',section:'S',type:'S',passageId:'ASS3',passageHtml:AS_S3,sub:'Improving a design',skill:'act_s_si',diff:4,
 stem:'To test whether sediment concentration depends on water temperature independently of discharge, a researcher should collect additional samples on days when:',
 choices:['both discharge and temperature change together over a storm','discharge and temperature are both at their annual maxima','discharge is similar but water temperature differs widely','discharge varies widely while temperature is not recorded'],answer:2,
 expl:'To isolate temperature, discharge has to be held roughly constant while temperature varies. Days matching on discharge but differing in temperature provide exactly that comparison.',
 wrong:'Letting both vary together, or maximising both, confounds the two variables, and dropping the temperature record makes the test impossible.'},
{id:'AS020',section:'S',type:'S',passageId:'ASS3',passageHtml:AS_S3,sub:'Sampling',skill:'act_s_si',diff:3,
 stem:'A limitation of Study 3 as a description of the river\'s annual sediment load is that:',
 choices:['discharge and sediment were measured at the same station','water temperature was measured in degrees Celsius','sediment was reported in mg/L rather than in kilograms','only 8 days were sampled out of the whole year'],answer:3,
 expl:'Eight measurements cannot capture a year of variation, particularly since sediment rises steeply with discharge and short high-flow events can carry a large share of the annual load.',
 wrong:'Concentration units, a shared station and the temperature scale are all ordinary features of such a study rather than limitations on annual coverage.'},
{id:'AS021',section:'S',type:'S',passageId:'ASS3',passageHtml:AS_S3,sub:'Evaluating a prediction',skill:'act_s_esa',diff:4,
 stem:'A model predicts sediment of about 150 mg/L at a discharge of 28 m3/s. Is this prediction consistent with Study 3?',
 choices:['Yes, because 28 m3/s lies between Days 4 and 5, whose sediment values bracket 150 mg/L.','Yes, because sediment never exceeds 150 mg/L at any discharge in the table.','No, because a discharge of 28 m3/s was not among the days sampled.','No, because sediment at 21 m3/s was already above 150 mg/L.'],answer:0,
 expl:'Day 4 recorded 21 m3/s with 102 mg/L and day 5 recorded 34 m3/s with 196 mg/L. A discharge of 28 falls between them and 150 falls between 102 and 196, so the prediction fits the observed pattern.',
 wrong:'Sediment reaches 310 mg/L on day 6, the value at 21 m3/s is 102 rather than above 150, and a prediction between measured points is exactly what interpolation is for.'},
// ---------- Scenario 4: Research Summaries ----------
{id:'AS022',section:'S',type:'S',passageId:'ASS4',passageHtml:AS_S4,sub:'Reading a table',skill:'act_s_iod',diff:1,
 stem:'In Experiment 1, mass loss at 400 h for uncoated steel was:',
 choices:['118 mg','241 mg','495 mg','49 mg'],answer:1,
 expl:'The uncoated row lists 118, 241 and 495 mg at 200, 400 and 800 hours, so the 400 hour value is 241 mg.',
 wrong:'118 and 495 are the 200 and 800 hour values for uncoated steel, and 49 is coating P at 400 hours.'},
{id:'AS023',section:'S',type:'S',passageId:'ASS4',passageHtml:AS_S4,sub:'Comparing conditions',skill:'act_s_iod',diff:2,
 stem:'In Experiment 1, which coating gave the lowest mass loss at 200 h?',
 choices:['None of the coatings differed at 200 h','P','Q','R'],answer:2,
 expl:'At 200 hours the values were 22 mg for P, 9 mg for Q and 31 mg for R, so coating Q performed best.',
 wrong:'P and R are both higher than Q, and the three values are clearly different from one another.'},
{id:'AS024',section:'S',type:'S',passageId:'ASS4',passageHtml:AS_S4,sub:'Change over time',skill:'act_s_iod',diff:4,
 stem:'Which coating showed the largest proportional increase in mass loss between 400 h and 800 h?',
 choices:['R','None (uncoated)','P','Q'],answer:3,
 expl:'The ratios of the 800 hour to the 400 hour value are about 2.1 for uncoated, 2.6 for P, 8.4 for Q and 2.0 for R. Coating Q rises far more steeply than the others.',
 wrong:'Uncoated steel loses the most mass in absolute terms but roughly doubles, as do P and R.'},
{id:'AS025',section:'S',type:'S',passageId:'ASS4',passageHtml:AS_S4,sub:'Purpose of a step',skill:'act_s_si',diff:3,
 stem:'Including uncoated coupons in Experiment 1 served mainly to:',
 choices:['provide a baseline against which coated performance could be judged','test whether the salt spray chamber reached the intended humidity','increase the total number of coupons in the chamber','determine the composition of the steel used'],answer:0,
 expl:'Without the uncoated coupons there would be nothing to show how much corrosion the coatings prevented. It is the control condition.',
 wrong:'Chamber conditions, coupon count and steel composition are not measured by the uncoated coupons.'},
{id:'AS026',section:'S',type:'S',passageId:'ASS4',passageHtml:AS_S4,sub:'Experimental design',skill:'act_s_si',diff:3,
 stem:'Scratching the coupons in Experiment 2 was done in order to test:',
 choices:['whether the coatings adhere to steel under mechanical stress','how the coatings perform once their continuity is broken','whether mass loss can be measured on a damaged surface without removing the coating','how long each coating takes to cure before exposure'],answer:1,
 expl:'A scratch breaks the barrier and exposes bare steel at a line. Comparing scratched with unscratched coupons shows what each coating does once it is no longer continuous, which is the realistic in-service condition.',
 wrong:'Adhesion, measurement feasibility and curing time are not what the scratched comparison isolates.'},
{id:'AS027',section:'S',type:'S',passageId:'ASS4',passageHtml:AS_S4,sub:'Evaluating a recommendation',skill:'act_s_esa',diff:4,
 stem:'An engineer must choose a coating for a structure where surface damage is likely. Based on both experiments, the best choice is:',
 choices:['P, because it gave the lowest mass loss at 800 h when unscratched','Q, because it gave the lowest mass loss at 200 h','R, because its mass loss changed least when the coating was scratched','None, because uncoated steel is unaffected by scratching'],answer:2,
 expl:'Scratching raised mass loss from 126 to 402 mg for P, from 151 to 171 for Q, and from 129 to 158 for R. R is both low when intact and barely affected by damage, which is what a structure exposed to damage needs.',
 wrong:'P is the worst performer once scratched despite its intact result, Q degrades sharply by 800 hours even unscratched, and uncoated steel corrodes fastest of all.'},
{id:'AS028',section:'S',type:'S',passageId:'ASS4',passageHtml:AS_S4,sub:'Reconciling results',skill:'act_s_esa',diff:4,
 stem:'Which statement best explains why coating Q ranks first at 200 h but not at 800 h?',
 choices:['Q was applied considerably more thickly than either P or R at the start of the experiment.','Q protects only against scratching and not against salt spray.','Q performs better at lower temperatures than the chamber provided during the exposure.','Q is an excellent barrier that fails relatively abruptly once it begins to break down.'],answer:3,
 expl:'Q gives the lowest loss at 200 and 400 hours but then jumps from 18 to 151 mg by 800 hours, a far steeper rise than the others. That pattern describes a barrier that holds well and then gives way.',
 wrong:'Thickness is never reported, Q clearly resists salt spray early on, and no temperature comparison was run.'},
// ---------- Scenario 5: Research Summaries ----------
{id:'AS029',section:'S',type:'S',passageId:'ASS5',passageHtml:AS_S5,sub:'Reading a table',skill:'act_s_iod',diff:1,
 stem:'In Experiment 1, the growth rate at a light intensity of 100 micromol photons/m2/s was:',
 choices:['0.78 divisions/day','0.92 divisions/day','0.38 divisions/day','0.44 divisions/day'],answer:0,
 expl:'The Experiment 1 row gives 0.78 divisions per day at 100 micromol photons per square metre per second.',
 wrong:'0.44 and 0.92 are the values at 50 and 200 in Experiment 1, and 0.38 is from Experiment 2.'},
{id:'AS030',section:'S',type:'S',passageId:'ASS5',passageHtml:AS_S5,sub:'Trend',skill:'act_s_iod',diff:3,
 stem:'In Experiment 1, growth rate stopped increasing appreciably above a light intensity of about:',
 choices:['100','200','400','50'],answer:1,
 expl:'Growth climbs from 0.21 to 0.44 to 0.78 and then to 0.92 at 200, but falls slightly to 0.90 at 400. The curve levels off at about 200.',
 wrong:'Growth is still rising steeply between 50 and 100, and 400 is past the point where the curve has already flattened.'},
{id:'AS031',section:'S',type:'S',passageId:'ASS5',passageHtml:AS_S5,sub:'Comparing experiments',skill:'act_s_iod',diff:3,
 stem:'At which light intensity did the two experiments give the most similar growth rates?',
 choices:['200','400','25','100'],answer:2,
 expl:'At 25 the values are 0.21 and 0.19, a difference of 0.02. At 100, 200 and 400 the differences are 0.40, 0.53 and 0.52.',
 wrong:'The gap between the two nitrate levels widens as light increases, so the higher intensities are the least similar.'},
{id:'AS032',section:'S',type:'S',passageId:'ASS5',passageHtml:AS_S5,sub:'Controlling variables',skill:'act_s_si',diff:3,
 stem:'The only variable deliberately changed between Experiment 1 and Experiment 2 was:',
 choices:['the range of light intensities tested','the species of alga used','the duration of the growth period','the nitrate concentration'],answer:3,
 expl:'Both experiments ran 6 days at the same five light intensities with the same alga; nitrate was reduced from 40 to 5 micromol per litre.',
 wrong:'Duration, light range and species were all held constant so that the nitrate effect could be read off the difference.'},
{id:'AS033',section:'S',type:'S',passageId:'ASS5',passageHtml:AS_S5,sub:'Limiting factors',skill:'act_s_esa',diff:4,
 stem:'Taken together, the two experiments best support which conclusion?',
 choices:['At low light, light limits growth; at high light with little nitrate, nitrate limits growth.','Growth rate reaches its highest observed value when both the light intensity and the nitrate concentration are at their lowest.','Nitrate has no effect on growth rate at any light intensity.','Light is the only factor that limits growth in this alga.'],answer:0,
 expl:'At 25 micromol the two nitrate levels give nearly the same rate, so nitrate is not limiting there and light is. At 200 and above, the high nitrate culture reaches 0.92 while the low nitrate culture stalls near 0.39, so nitrate has become the limit.',
 wrong:'Nitrate plainly matters at high light, light is not the only limit, and the lowest values of both give the slowest growth rather than the fastest.'},
{id:'AS034',section:'S',type:'S',passageId:'ASS5',passageHtml:AS_S5,sub:'Predicting a result',skill:'act_s_esa',diff:4,
 stem:'If Experiment 2 were repeated at 800 micromol photons/m2/s with nitrate still at 5 micromol/L, growth rate would most likely be:',
 choices:['close to 0.19 divisions/day','close to 0.38 divisions/day','close to 0.90 divisions/day','close to 1.40 divisions/day'],answer:1,
 expl:'In Experiment 2 the rate is flat from 100 onward at 0.38, 0.39 and 0.38, because nitrate rather than light is limiting. Adding more light should not lift a nitrate-limited culture.',
 wrong:'0.90 is the high nitrate result, 1.40 exceeds anything observed, and 0.19 is the value at the lowest light intensity.'},
{id:'AS035',section:'S',type:'S',passageId:'ASS5',passageHtml:AS_S5,sub:'Extending the design',skill:'act_s_si',diff:4,
 stem:'To find the nitrate concentration at which nitrate stops limiting growth at 200 micromol photons/m2/s, a researcher should:',
 choices:['grow the cultures for 12 days instead of 6 at both nitrate levels','test a second algal species at the same two nitrate concentrations','repeat the 200 micromol light condition at several nitrate levels between 5 and 40 micromol/L','repeat Experiment 2 at a range of light intensities below 25 micromol photons per square metre per second'],answer:2,
 expl:'The question is about nitrate, so light should be fixed at the intensity where the nitrate difference is largest and nitrate should be varied across the untested range between the two levels already used.',
 wrong:'Lower light, longer growth and a second species each change something other than the variable in question.'},
// ---------- Scenario 6: Conflicting Viewpoints ----------
{id:'AS036',section:'S',type:'S',passageId:'ASS6',passageHtml:AS_S6,sub:'Understanding a viewpoint',skill:'act_s_iod',diff:2,
 stem:'According to Scientist 1, the layer of water suitable for lake trout has:',
 choices:['deepened from about 3 m to about 9 m','remained about 9 m thick since 1995','disappeared entirely during summer','thinned from about 9 m to about 3 m'],answer:3,
 expl:'Scientist 1 states that the cold layer holding enough oxygen has thinned from about 9 m to about 3 m since 1995.',
 wrong:'The layer has thinned rather than deepened or held steady, and Scientist 1 describes it as narrower rather than gone.'},
{id:'AS037',section:'S',type:'S',passageId:'ASS6',passageHtml:AS_S6,sub:'Understanding a viewpoint',skill:'act_s_iod',diff:2,
 stem:'Scientist 2 attributes the decline in lake trout chiefly to:',
 choices:['the loss of the deepwater sculpin and a switch to smelt as prey','a reduction in dissolved oxygen below 6 mg/L','the direct predation of smelt on adult trout','the steady rise in summer surface temperatures recorded in the lake since 1995'],answer:0,
 expl:'Scientist 2 traces the decline to the sculpin collapse after 1995, the switch to smelt, and the thiamine-destroying enzyme smelt carry.',
 wrong:'Scientist 2 grants that warming is real but denies it is the cause, says nothing about oxygen falling below the threshold, and describes predation on young trout rather than on adults.'},
{id:'AS038',section:'S',type:'S',passageId:'ASS6',passageHtml:AS_S6,sub:'Point of agreement',skill:'act_s_esa',diff:3,
 stem:'Both scientists would agree that:',
 choices:['lake trout numbers were stable until about 2010','the cold oxygenated layer in the lake has become thinner since 1995','smelt numbers rose sharply after a change in stocking practice','thiamine deficiency is the main cause of trout fry mortality'],answer:1,
 expl:'Scientist 1 makes the thinning the centre of the argument, and Scientist 2 concedes it explicitly while denying it is sufficient to explain the decline.',
 wrong:'The stocking change and the thiamine mechanism belong to Scientist 2 alone, and both accounts date the decline from 1995.'},
{id:'AS039',section:'S',type:'S',passageId:'ASS6',passageHtml:AS_S6,sub:'Point of disagreement',skill:'act_s_esa',diff:3,
 stem:'The two scientists disagree most directly about whether:',
 choices:['lake trout require water below 12 deg C','the lake has warmed since 1995','the remaining cold oxygenated layer is large enough to support the historical trout population','smelt have been present in Lake Verrin continuously since the 1970s without a decline before 1995'],answer:2,
 expl:'Scientist 1 argues the band has become too narrow, squeezing the trout. Scientist 2 says that although thinner, it is still wide enough to hold the historical population. That is the direct clash.',
 wrong:'Warming, the presence of smelt since the 1970s and the temperature requirement are all common ground.'},
{id:'AS040',section:'S',type:'S',passageId:'ASS6',passageHtml:AS_S6,sub:'Evidence and argument',skill:'act_s_esa',diff:4,
 stem:'Scientist 1 mentions that smelt have been present since the 1970s in order to:',
 choices:['establish that smelt rather than sculpin are the preferred prey of adult lake trout in the lake','show that stocking practice has little effect on smelt numbers','explain why the sculpin population collapsed after 1995','argue that a long-standing factor cannot account for a decline that began in 1995'],answer:3,
 expl:'The point is one of timing: a cause present for twenty years before the decline began cannot by itself explain why the decline started when it did.',
 wrong:'Scientist 1 rejects the sculpin account rather than explaining it, does not endorse smelt as preferred prey, and the stocking change is Scientist 2 point.'},
{id:'AS041',section:'S',type:'S',passageId:'ASS6',passageHtml:AS_S6,sub:'Weighing new evidence',skill:'act_s_si',diff:4,
 stem:'Which finding would most strengthen the position of Scientist 2 relative to Scientist 1?',
 choices:['Trout in nearby lakes that warmed similarly but retained sculpin did not decline.','The thermocline in Lake Verrin deepened by 2 m between 1995 and 2020.','Dissolved oxygen in the deepest water of the lake fell below 6 mg/L in 2018.','Summer surface temperatures in the lake rose faster after 2005 than before it.'],answer:0,
 expl:'Lakes that warmed the same amount but kept their sculpin provide the comparison that separates the two explanations. If those trout held steady, warming alone does not produce the decline and the prey change does the work.',
 wrong:'Faster warming, a deeper thermocline and falling deep oxygen all support Scientist 1.'},
{id:'AS042',section:'S',type:'S',passageId:'ASS6',passageHtml:AS_S6,sub:'Designing a test',skill:'act_s_si',diff:4,
 stem:'A researcher wants to test Scientist 2 proposed mechanism directly. The most informative measurement would be:',
 choices:['the depth of the summer thermocline measured weekly','thiamine concentration in trout eggs, compared with fry survival','the annual mean surface temperature of the lake over 25 years','the total mass of smelt harvested by anglers each season'],answer:1,
 expl:'Scientist 2 claims smelt cause thiamine deficiency and that deficient trout produce fry that die within weeks. Measuring egg thiamine against fry survival tests that causal link rather than the circumstances around it.',
 wrong:'Surface temperature and thermocline depth test Scientist 1 account, and angler harvest measures smelt abundance without touching the thiamine mechanism.'}
];
