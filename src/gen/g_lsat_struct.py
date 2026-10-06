"""The parts of an argument and the role each one plays (lsat_lr_struct).

LSAC lists recognizing the parts of an argument and their relationships among the skills
Logical Reasoning measures. The category that carries it here had 30 hand written items
and no generator. Two of its questions can be generated without anyone judging the
answer, because the answer is fixed when the argument is written: an author who writes
"After all, P, so I" has made P a premise and I a conclusion, whatever P and I say.

So each argument below is authored with its parts labelled, and rendered from one of two
templates whose connecting words (but, after all, so, moreover; they are mistaken, it
follows that, in addition) put each part in its place:

  opp     a view the argument rejects, attributed to someone else
  concl   the main conclusion, which rejects that view
  p1      a premise offered for the intermediate conclusion
  ic      the intermediate conclusion, drawn from p1 and offered for concl
  p2      a second premise, offered for concl directly

Two questions are asked of each argument. The role a claim plays: five per argument, one
for each part, with the answer choices drawn from descriptions of the five roles and of
roles nothing in these arguments plays. And the main conclusion: the author writes a
paraphrase of every part and an overstatement of the conclusion, which are the wrong
answers a test writer uses, because the intermediate conclusion is the classic trap.

An argument is rendered one way only, chosen by its index, and each question is asked in
one wording only, chosen by a checksum. The same claim asked about in a second wording is
the same question, and counting it twice would inflate the category.
"""
import re
import zlib

from framework import ItemError, ListsQuestions, upfirst
from g_gmat_cr import CRBase

PARTS = ("opp", "concl", "p1", "ic", "p2")

# Each role has two descriptions, so the length of a key is not fixed by its role. The
# never list are roles no part of these arguments plays.
ROLE = {
    "opp": ("It states a view that the argument sets out to reject.",
            "It is a claim that the argument's main conclusion directly opposes."),
    "concl": ("It is the main conclusion of the argument.",
              "It is the conclusion toward which the argument as a whole is directed."),
    "p1": ("It is a premise offered in support of the argument's intermediate conclusion.",
           "It is offered as support for a claim that in turn supports the main conclusion."),
    "ic": ("It is an intermediate conclusion: it is drawn from one claim and then used to "
           "support the main conclusion.",
           "It is a conclusion supported by another claim in the argument, and it is itself "
           "offered in support of the main conclusion."),
    "p2": ("It is additional support offered directly for the main conclusion.",
           "It is a premise that supports the main conclusion independently of the "
           "argument's other reasoning."),
}
NEVER = [
    ("It is an assumption the argument depends on but never states.",
     "names an unstated assumption, and the claim is stated in the argument"),
    ("It is the only evidence the argument offers for its main conclusion.",
     "calls it the only evidence, and the argument gives two separate reasons"),
    ("It is a concession that the argument grants and then shows to be irrelevant.",
     "calls it a concession, and the argument concedes nothing to the view it rejects"),
    ("It is an example offered to illustrate a general principle the argument relies on.",
     "calls it an example of a principle, and the argument states no principle"),
    ("It is a prediction the argument raises in order to cast doubt on its own conclusion.",
     "says it casts doubt on the conclusion, and nothing in the argument does that"),
]

STEM_ROLE = ("The claim that %s plays which one of the following roles in the %s's argument?",
             "Which one of the following most accurately describes the role played in the "
             "%s's argument by the claim that %s?")
STEM_MAIN = "Which one of the following most accurately expresses the main conclusion of the %s's argument?"

# The views are attributed to "some" people and never to anyone real. Nothing here is a
# fact about the world: each argument is a stimulus to be analysed, like the test's own.
ARGS = [
    dict(speaker="transit planner", opp_who="Some residents",
         opp="the new rail line should run along the river, where land is cheapest",
         concl="the line should follow Market Street instead",
         p1="most of the jobs the line is meant to serve lie within a short walk of Market Street",
         ic="a Market Street route would carry more riders",
         p2="a river route would need a new bridge whose cost would use up the savings on land",
         concl_para="The new rail line should be routed along Market Street rather than along the river.",
         ic_para="A Market Street route would attract more riders than a route along the river.",
         p1_para="Most of the jobs the rail line will serve are close to Market Street.",
         opp_para="The new rail line should be built along the river because land there is cheapest.",
         p2_para="Building the line along the river would require an expensive new bridge.",
         over="No rail line in the city should ever be built along the river."),
    dict(speaker="library director", opp_who="Several trustees",
         opp="the library should cut its evening hours to save on staff costs",
         concl="the evening hours should be kept",
         p1="the people who use the library in the evening are mostly students and shift workers who cannot come during the day",
         ic="cutting the evening hours would shut out the people who depend on the library most",
         p2="the savings on staff would amount to less than the fines the library already waives each year",
         concl_para="The library should keep its evening opening hours.",
         ic_para="Ending the evening hours would exclude the library's most dependent users.",
         p1_para="Most evening visitors to the library are unable to visit during the day.",
         opp_para="The library should reduce its evening hours in order to lower its staff costs.",
         p2_para="Cutting the evening hours would save less than the library already waives in fines.",
         over="A public library should never reduce its opening hours for financial reasons."),
    dict(speaker="clinic manager", opp_who="Some staff members",
         opp="sending text reminders before appointments is a waste of money",
         concl="the clinic should keep sending the reminders",
         p1="patients who receive a reminder miss far fewer appointments than those who do not",
         ic="the reminders fill appointment slots that would otherwise go unused",
         p2="each reminder costs a few cents, while each missed appointment costs the clinic a full consultation fee",
         concl_para="The clinic should continue to send appointment reminders.",
         ic_para="Appointment reminders keep appointment slots from going unused.",
         p1_para="Patients who get reminders miss fewer appointments than patients who do not.",
         opp_para="Appointment reminders cost the clinic more than they are worth.",
         p2_para="A missed appointment costs the clinic far more than a reminder does.",
         over="Every clinic should send a reminder to every patient before every appointment."),
    dict(speaker="school board member", opp_who="Some parents",
         opp="moving the school day later would disrupt family schedules too much to be worth it",
         concl="the board should move the start of the school day to nine o'clock",
         p1="teenagers whose school starts later sleep longer on school nights",
         ic="a later start would leave students more alert in their morning lessons",
         p2="the bus contractor has confirmed that a later start would not raise the cost of transport",
         concl_para="The school day should begin at nine o'clock.",
         ic_para="Students would be more alert in morning lessons if school started later.",
         p1_para="Teenagers sleep longer on school nights when school starts later.",
         opp_para="A later start to the school day would disrupt families more than it would help.",
         p2_para="Starting school later would not make transport more expensive.",
         over="Every school should start at the latest hour its buses can manage."),
    dict(speaker="museum director", opp_who="Some board members",
         opp="abolishing the admission charge would ruin the museum's finances",
         concl="the museum should abolish its admission charge",
         p1="visitors who enter free spend more in the shop and restaurant than paying visitors do",
         ic="most of the lost ticket revenue would be recovered from other sales",
         p2="the city has offered a grant to any museum that stops charging for entry",
         concl_para="The museum should stop charging visitors for admission.",
         ic_para="Other sales would make up most of the revenue the museum lost from tickets.",
         p1_para="Visitors admitted free spend more in the shop and restaurant than paying visitors.",
         opp_para="Ending the admission charge would damage the museum's finances.",
         p2_para="The city will give a grant to museums that stop charging for entry.",
         over="No museum should ever charge for admission."),
    dict(speaker="fisheries biologist", opp_who="Some anglers",
         opp="the decline in the lake's trout has been caused by overfishing",
         concl="the warming of the lake is the more likely cause of the decline",
         p1="the trout have declined most in the shallow bays, where the water has warmed the most",
         ic="the decline follows water temperature rather than fishing pressure",
         p2="the number of fishing licences issued for the lake has fallen by a third over the same period",
         concl_para="The lake's warming is a likelier cause of the trout decline than overfishing is.",
         ic_para="Where the trout have declined matches where the water has warmed, not where fishing is heaviest.",
         p1_para="Trout numbers have fallen most sharply in the lake's shallow bays.",
         opp_para="Overfishing is responsible for the decline in the lake's trout.",
         p2_para="Fewer fishing licences have been issued for the lake in recent years.",
         over="Fishing has had no effect at all on the lake's trout."),
    dict(speaker="operations director", opp_who="Several managers",
         opp="the company should require everyone to work in the office five days a week",
         concl="the company should keep its hybrid schedule",
         p1="since the hybrid schedule began, the company has hired from a much wider area than before",
         ic="a full return to the office would shrink the pool the company recruits from",
         p2="the teams that come in least often have met their targets as reliably as the rest",
         concl_para="The company should continue its hybrid working arrangement.",
         ic_para="Requiring everyone to work in the office full time would narrow the company's recruiting pool.",
         p1_para="The company has recruited from a wider area since it adopted the hybrid schedule.",
         opp_para="Everyone at the company should be required to work in the office every weekday.",
         p2_para="Teams that are in the office least have met their targets as reliably as the others.",
         over="No company gains anything by requiring its staff to work in an office."),
    dict(speaker="city planner", opp_who="Some council members",
         opp="new apartment buildings should be required to provide two parking spaces for every unit",
         concl="the requirement should be reduced to one space for every unit",
         p1="the second space adds more to the price of a unit than most buyers are willing to pay for it",
         ic="the two space rule makes new apartments more expensive than the market will bear",
         p2="surveys of existing buildings show that half of their second spaces sit empty overnight",
         concl_para="New apartment buildings should have to provide one parking space per unit rather than two.",
         ic_para="Requiring two spaces per unit raises apartment prices beyond what buyers will pay.",
         p1_para="Buyers are generally unwilling to pay what a second parking space adds to a unit's price.",
         opp_para="Each new apartment should come with two parking spaces.",
         p2_para="Many second parking spaces in existing buildings are unused at night.",
         over="The city should abolish every parking requirement for every kind of building."),
    dict(speaker="historian", opp_who="Some scholars",
         opp="the diary was written by the ship's captain",
         concl="the diary was more probably written by the ship's surgeon",
         p1="the diary records the treatment of every sick sailor in detail but mentions the ship's course only twice",
         ic="the diary's author was far more occupied with medicine than with navigation",
         p2="the diary's handwriting matches that of the surgeon's surviving letters",
         concl_para="The ship's surgeon, rather than its captain, probably wrote the diary.",
         ic_para="Whoever wrote the diary was more concerned with medicine than with navigation.",
         p1_para="The diary describes medical treatment in detail and rarely mentions the ship's course.",
         opp_para="The ship's captain wrote the diary.",
         p2_para="The diary's handwriting resembles that of letters the surgeon wrote.",
         over="The captain wrote nothing at all during the voyage."),
    dict(speaker="principal", opp_who="Some teachers",
         opp="the school should assign more homework to its youngest pupils",
         concl="the school should not give its youngest pupils more homework",
         p1="pupils under ten who do more homework score no better on the school's reading tests than those who do less",
         ic="more homework would give the youngest pupils little academic benefit",
         p2="parents report that homework is already the most frequent cause of arguments at home in the evening",
         concl_para="The youngest pupils at the school should not be given additional homework.",
         ic_para="Extra homework would do little for the youngest pupils' learning.",
         p1_para="Younger pupils who do more homework do not read better than those who do less.",
         opp_para="The school's youngest pupils should be given more homework.",
         p2_para="Homework already causes frequent arguments in pupils' homes.",
         over="Schools should abolish homework for pupils of every age."),
    dict(speaker="environmental officer", opp_who="Some shop owners",
         opp="a charge for plastic bags would drive customers to shops in neighbouring towns",
         concl="the town should introduce the bag charge",
         p1="nearby towns that introduced a similar charge saw no fall in local shopping",
         ic="the fear of losing customers is not borne out by experience",
         p2="bag litter is the largest single cause of blocked drains in the town",
         concl_para="The town should introduce a charge for plastic bags.",
         ic_para="Experience elsewhere does not support the worry that the town's shops would lose customers.",
         p1_para="Nearby towns with a bag charge did not see local shopping decline.",
         opp_para="A plastic bag charge would send the town's shoppers to other towns.",
         p2_para="Plastic bag litter blocks more drains in the town than anything else does.",
         over="Plastic bags should be banned everywhere."),
    dict(speaker="court administrator", opp_who="Some lawyers",
         opp="moving minor hearings online would make them less fair",
         concl="minor hearings should be held online",
         p1="defendants in minor cases who must attend in person miss their hearings far more often than those allowed to attend online",
         ic="online hearings would let more defendants take part in their own cases",
         p2="the pilot programme found no difference in outcomes between online hearings and hearings in person",
         concl_para="Hearings in minor cases should take place online.",
         ic_para="Holding hearings online would allow more defendants to take part in their own cases.",
         p1_para="Defendants who must attend in person miss hearings more often than those who may attend online.",
         opp_para="Holding minor hearings online would make them less fair.",
         p2_para="Outcomes in the pilot programme did not differ between online hearings and hearings in person.",
         over="Every court hearing, whatever its seriousness, should be held online."),
    dict(speaker="agronomist", opp_who="Many farmers in the valley",
         opp="planting cover crops over the winter costs more than it returns",
         concl="the valley's farmers should plant cover crops",
         p1="fields planted with cover crops lose far less topsoil to winter rain than bare fields do",
         ic="cover crops protect the soil that next year's harvest depends on",
         p2="the regional grant now pays for most of the seed",
         concl_para="Farmers in the valley should grow cover crops over the winter.",
         ic_para="Cover crops preserve the soil on which future harvests depend.",
         p1_para="Fields with cover crops lose less topsoil in winter than bare fields do.",
         opp_para="Winter cover crops are not worth what they cost.",
         p2_para="A regional grant now covers most of what cover crop seed costs.",
         over="Every farmer should plant cover crops on every field every year."),
    dict(speaker="IT manager", opp_who="Some department heads",
         opp="staff should be allowed to postpone security updates for as long as they like",
         concl="security updates should be installed within a week of their release",
         p1="most of the attacks on the company last year exploited flaws for which an update had already been issued",
         ic="delaying updates leaves the company open to the attacks most likely to succeed",
         p2="installing updates overnight means that no one loses working time to them",
         concl_para="Security updates should be installed no later than a week after they are released.",
         ic_para="Postponing updates exposes the company to the attacks most likely to succeed against it.",
         p1_para="Most of last year's attacks on the company used flaws that updates had already fixed.",
         opp_para="Staff should be free to postpone security updates indefinitely.",
         p2_para="Installing updates overnight keeps them from costing staff any working time.",
         over="Every piece of software should be updated the moment an update is released."),
    dict(speaker="arts council chair", opp_who="Some councillors",
         opp="the council should fund only the town's largest arts organisations",
         concl="the council should keep funding the small arts groups as well",
         p1="most of the performers now working for the large organisations started out in the small groups",
         ic="the small groups train the talent the large organisations depend on",
         p2="the small groups reach neighbourhoods that the large organisations rarely serve",
         concl_para="The council should continue to fund small arts groups alongside the large ones.",
         ic_para="Small arts groups develop the performers that the large organisations rely on.",
         p1_para="Most performers at the large organisations began in small groups.",
         opp_para="Only the town's largest arts organisations should receive council funding.",
         p2_para="Small arts groups serve neighbourhoods that the large organisations seldom reach.",
         over="The council should fund every arts group that applies to it."),
    dict(speaker="school nurse", opp_who="Some parents",
         opp="taking sugary drinks out of the school's vending machines would make no difference",
         concl="the sugary drinks should be taken out of the machines",
         p1="pupils at schools that took such drinks out bring fewer of them from home than they used to buy at school",
         ic="taking the drinks out reduces how much pupils actually drink",
         p2="the vending contract allows the school to replace the drinks at no cost",
         concl_para="Sugary drinks should be removed from the school's vending machines.",
         ic_para="Removing the drinks from the machines lowers how much pupils drink.",
         p1_para="Pupils at schools without the drinks bring fewer from home than they had bought at school.",
         opp_para="Removing sugary drinks from the machines would not change what pupils drink.",
         p2_para="The school can replace the drinks under its vending contract without paying anything.",
         over="Sugary drinks should be banned from every place that pupils go."),
    dict(speaker="economist", opp_who="Supporters of the stadium plan",
         opp="a publicly funded stadium would bring new spending into the city",
         concl="the city should not fund the stadium",
         p1="most of the money fans spend at games is money they would otherwise spend elsewhere in the city",
         ic="the stadium would mostly move spending around the city rather than add to it",
         p2="the city would still be paying for the stadium long after its expected useful life had ended",
         concl_para="The city should not pay for the proposed stadium.",
         ic_para="The stadium would shift spending within the city more than it would create new spending.",
         p1_para="Fans mostly spend at games money they would otherwise have spent elsewhere in the city.",
         opp_para="A stadium paid for by the city would draw new spending into it.",
         p2_para="The city would be repaying the stadium's cost after the stadium had ceased to be useful.",
         over="A city should never spend public money on anything connected with sport."),
    dict(speaker="archaeologist", opp_who="Some researchers",
         opp="the settlement was abandoned because of a war",
         concl="a failure of the settlement's water supply is the more probable cause",
         p1="the settlement's wells were all filled in with sand during the same decade",
         ic="the settlement lost its water at about the time it was abandoned",
         p2="none of the settlement's buildings shows the burning or damage that attacks elsewhere in the region left behind",
         concl_para="The settlement was more probably abandoned because its water supply failed than because of a war.",
         ic_para="The settlement lost its water supply at around the time its people left.",
         p1_para="All of the settlement's wells filled with sand within a single decade.",
         opp_para="A war caused the settlement to be abandoned.",
         p2_para="The settlement's buildings show none of the damage that attacks in the region left.",
         over="No settlement in the region was ever abandoned because of a war."),
    dict(speaker="store manager", opp_who="Some customers",
         opp="the store should remove its self checkout machines",
         concl="the machines should stay, alongside the staffed tills",
         p1="at busy times the machines serve almost half of all customers",
         ic="without the machines the queues at the staffed tills would grow far longer",
         p2="customers who dislike the machines can still use a staffed till at any hour",
         concl_para="The store should keep its self checkout machines as well as its staffed tills.",
         ic_para="Removing the machines would make the queues at the staffed tills much longer.",
         p1_para="Nearly half of the store's customers use the machines when the store is busy.",
         opp_para="The store's self checkout machines should be taken out.",
         p2_para="Staffed tills remain open at all hours to customers who prefer them.",
         over="Every till in the store should be replaced with a self checkout machine."),
    dict(speaker="transport engineer", opp_who="Some shopkeepers",
         opp="replacing the parking on the high street with a cycle lane would hurt local trade",
         concl="the cycle lane should be built",
         p1="most of the high street's customers arrive on foot, by bus or by bicycle rather than by car",
         ic="losing the parking would affect only a small share of the street's customers",
         p2="streets in the region that added cycle lanes have since seen fewer of their shops stand empty",
         concl_para="The cycle lane on the high street should go ahead.",
         ic_para="Removing the parking would affect few of the high street's customers.",
         p1_para="Most customers reach the high street without using a car.",
         opp_para="A cycle lane in place of the parking would harm the high street's businesses.",
         p2_para="Fewer shops stand empty on streets in the region that gained cycle lanes.",
         over="Cars should be banned from every high street."),
    dict(speaker="health official", opp_who="Some restaurant owners",
         opp="posting calorie counts on menus would put customers off eating out",
         concl="the city should require calorie counts on menus",
         p1="in cities that already require the counts, restaurant takings have held steady while diners choose lower calorie dishes more often",
         ic="the counts change what diners order without keeping them away",
         p2="the chains that serve most of the city's meals already calculate the figures for their own records",
         concl_para="Restaurants in the city should be required to show calorie counts on their menus.",
         ic_para="Calorie counts alter what diners choose without reducing how often they eat out.",
         p1_para="Where calorie counts are required, diners pick lower calorie dishes and restaurant takings are unchanged.",
         opp_para="Calorie counts on menus would discourage people from eating out.",
         p2_para="The largest restaurant chains in the city already work out the calorie figures.",
         over="Every food sold anywhere in the city should carry a calorie count."),
    dict(speaker="head of languages", opp_who="Some governors",
         opp="the school could replace its language classes with a language learning app",
         concl="the classes should stay",
         p1="pupils at the school's partner schools who used the app on its own rarely kept using it past the first month",
         ic="an app without a teacher would leave most pupils with little practice after the first few weeks",
         p2="the examinations the pupils take include a speaking test that an app cannot prepare them for",
         concl_para="The school should keep its language classes rather than replace them with an app.",
         ic_para="Without a teacher, most pupils would stop practising within weeks.",
         p1_para="Pupils at partner schools seldom used the app beyond its first month.",
         opp_para="A language learning app could take the place of the school's language classes.",
         p2_para="The pupils' examinations include a speaking test that an app cannot prepare them for.",
         over="No school should ever use an app to teach a language."),
    dict(speaker="conservation officer", opp_who="Some engineers",
         opp="fencing the highway would protect deer from traffic well enough on its own",
         concl="the highway also needs crossings built beneath it",
         p1="fences on other roads have pushed deer to cross wherever the fencing ends",
         ic="fencing alone would move collisions to the ends of the fence rather than prevent them",
         p2="the herd's winter feeding grounds lie on the far side of the road",
         concl_para="Crossings beneath the highway are needed as well as fencing.",
         ic_para="Fencing by itself would shift where collisions happen rather than stop them.",
         p1_para="On other roads, deer have crossed at the ends of the fencing.",
         opp_para="Fencing the highway would be enough to keep deer safe from traffic.",
         p2_para="The deer spend the winter feeding on the other side of the highway.",
         over="Every road in the region should have crossings built beneath it."),
    dict(speaker="nurse manager", opp_who="Some administrators",
         opp="the ward could safely reduce its night staff by one nurse",
         concl="night staffing should stay at its present level",
         p1="most of the ward's emergencies over the past year happened between midnight and six in the morning",
         ic="the hours the proposal would thin are the ones in which the ward is busiest with emergencies",
         p2="the savings would be spent on the agency nurses the ward would need whenever a night nurse fell ill",
         concl_para="The ward should keep the number of nurses it has on duty at night.",
         ic_para="Cutting night staff would thin the ward during its most demanding hours.",
         p1_para="Most of the ward's emergencies last year occurred overnight.",
         opp_para="The ward could cut one nurse from the night shift without risk.",
         p2_para="Any savings would go on agency nurses to cover for night staff who fall ill.",
         over="No hospital ward should ever reduce its staffing at night."),
    dict(speaker="journal editor", opp_who="Some authors",
         opp="requiring authors to publish their data would discourage good researchers from submitting",
         concl="the journal should require the data",
         p1="other journals in the field that began requiring data have received more submissions since, not fewer",
         ic="the requirement has not driven authors away from the journals that adopted it",
         p2="published data has allowed readers to catch errors that reviewers missed",
         concl_para="The journal should require authors to publish the data behind their papers.",
         ic_para="Journals that require data have not lost authors as a result.",
         p1_para="Submissions to journals that require data have increased.",
         opp_para="A data requirement would deter strong researchers from submitting to the journal.",
         p2_para="Readers have found errors in published data that reviewers did not notice.",
         over="Every piece of research ever published should be accompanied by its data."),
    dict(speaker="housing officer", opp_who="Some property owners",
         opp="a tax on homes left empty would do nothing to ease the housing shortage",
         concl="the city should adopt the tax",
         p1="cities that taxed empty homes saw many of them rented out within two years",
         ic="the tax would bring empty homes back into use",
         p2="the revenue could fund the repair of the city's own vacant flats",
         concl_para="The city should tax homes that are left empty.",
         ic_para="Taxing empty homes would return them to use.",
         p1_para="In cities that taxed empty homes, many were rented out within two years.",
         opp_para="Taxing empty homes would not help with the housing shortage.",
         p2_para="The tax revenue could pay to repair the city's vacant flats.",
         over="The city should tax every home that is not occupied every day of the year."),
    dict(speaker="regional planner", opp_who="Some business groups",
         opp="a second runway is needed to meet the demand for flights",
         concl="the airport should not build the runway",
         p1="most of the airport's flights leave in two short peaks each day, and the runway sits idle for much of the rest of the time",
         ic="better scheduling could handle the growth in demand without new capacity",
         p2="the land needed for the runway includes the region's largest remaining wetland",
         concl_para="The airport should not go ahead with a second runway.",
         ic_para="Growth in demand could be met by spreading flights more evenly across the day.",
         p1_para="The airport's flights are concentrated in two daily peaks.",
         opp_para="A second runway is necessary to meet demand for flights.",
         p2_para="Building the runway would take land from the region's largest wetland.",
         over="No airport should ever build another runway."),
    dict(speaker="preservation officer", opp_who="Some developers",
         opp="the old grain store should be demolished because it is beyond repair",
         concl="the grain store should be converted rather than demolished",
         p1="the engineers' survey found the frame sound and the damage confined to the roof",
         ic="the building can be repaired at a reasonable cost",
         p2="the grain store is the last building of its kind left on the waterfront",
         concl_para="The grain store should be converted to a new use instead of being demolished.",
         ic_para="The grain store can be repaired without great expense.",
         p1_para="The engineers found the building's frame sound and only its roof damaged.",
         opp_para="The grain store is too damaged to repair and should be pulled down.",
         p2_para="No other building like the grain store survives on the waterfront.",
         over="No old building on the waterfront should ever be demolished."),
    dict(speaker="human resources director", opp_who="Some managers",
         opp="a four day week would reduce the company's output",
         concl="the company should extend the four day week to every office",
         p1="the offices in the trial produced as much as before while taking a fifth fewer sick days",
         ic="the shorter week did not cost the trial offices any output",
         p2="applications for jobs at the trial offices doubled while the trial ran",
         concl_para="Every office in the company should move to a four day week.",
         ic_para="The offices that worked a four day week lost no output by doing so.",
         p1_para="The trial offices kept their output and took fewer sick days.",
         opp_para="Working a four day week would lower the company's output.",
         p2_para="Twice as many people applied for jobs at the trial offices during the trial.",
         over="Every company should adopt a four day week at once."),
    dict(speaker="utility engineer", opp_who="Some residents",
         opp="installing water meters would only raise bills without saving any water",
         concl="the town should install meters in every home",
         p1="households in the neighbouring town used a fifth less water in the year after meters were fitted",
         ic="meters lead households to use less water",
         p2="the reservoir has fallen below its safe level in three of the last five summers",
         concl_para="Every home in the town should be fitted with a water meter.",
         ic_para="Metering causes households to reduce their water use.",
         p1_para="Households in the neighbouring town used less water once meters were installed.",
         opp_para="Water meters would increase bills without reducing water use.",
         p2_para="The reservoir has repeatedly dropped below its safe level in recent summers.",
         over="Every source of water in the region should be metered and charged for."),
    dict(speaker="harbour master", opp_who="Some boat owners",
         opp="the channel should be dredged every year to keep it deep enough for the fishing fleet",
         concl="dredging the channel every third year would be enough",
         p1="soundings taken over the last ten years show that the channel loses depth only slowly",
         ic="a yearly dredge would remove very little silt for what it costs",
         p2="each dredge disturbs the oyster beds at the harbour mouth for a whole season",
         concl_para="The channel needs dredging only once every three years.",
         ic_para="Dredging every year would cost a great deal for the small amount of silt removed.",
         p1_para="Ten years of soundings show that the channel silts up slowly.",
         opp_para="The channel should be dredged annually so that the fishing fleet can use it.",
         p2_para="Dredging upsets the oyster beds at the mouth of the harbour for a season.",
         over="No harbour should ever be dredged more than once every three years."),
    dict(speaker="curriculum coordinator", opp_who="Some parents",
         opp="the school should replace its afternoon music lessons with extra mathematics",
         concl="the music lessons should be kept",
         p1="the school's own studies show that pupils learn least in the last hour of the day, when the extra mathematics would be taught",
         ic="the extra mathematics lessons would do little to raise mathematics results",
         p2="for many pupils the music lessons are the only teaching of that kind their families could afford",
         concl_para="The school should keep its afternoon music lessons.",
         ic_para="Extra mathematics in the afternoon would barely improve mathematics results.",
         p1_para="Pupils learn least at the end of the school day, which is when the extra mathematics would fall.",
         opp_para="The school should swap its afternoon music lessons for more mathematics.",
         p2_para="Many pupils' families could not otherwise pay for the kind of teaching the music lessons give.",
         over="Schools should never cut music teaching to make time for another subject."),
    dict(speaker="newspaper editor", opp_who="Some of the paper's owners",
         opp="the paper should stop printing and publish only online",
         concl="the printed edition should continue",
         p1="most of the paper's subscribers are over seventy, and few of them read the news online",
         ic="ending the printed edition would lose the paper most of its subscribers",
         p2="advertising in the printed edition still pays for the whole newsroom",
         concl_para="The newspaper should keep publishing a printed edition.",
         ic_para="Stopping the printed edition would cost the paper the majority of its subscribers.",
         p1_para="Most subscribers are over seventy and seldom read the news online.",
         opp_para="The newspaper should give up printing and publish only on the internet.",
         p2_para="The printed edition's advertising covers the cost of the entire newsroom.",
         over="Newspapers should never stop printing, whatever their readers do."),
    dict(speaker="fire chief", opp_who="Some council members",
         opp="the town's second fire station should be closed to save money",
         concl="both stations should stay open",
         p1="the only road from the first station to the northern estates crosses a bridge that floods several times each winter",
         ic="without the second station, fires in the northern estates would sometimes be out of reach for hours",
         p2="the second station costs less to run than the town would lose in higher insurance premiums if it closed",
         concl_para="The town should keep both of its fire stations open.",
         ic_para="Closing the second station would leave the northern estates cut off from help during floods.",
         p1_para="The first station's only route to the northern estates crosses a bridge that floods in winter.",
         opp_para="The town should close its second fire station to cut costs.",
         p2_para="Running the second station is cheaper than the extra insurance the town would pay without it.",
         over="A town should never close a fire station for any reason."),
    dict(speaker="orchard owner", opp_who="Some neighbouring growers",
         opp="spraying in early spring is the best defence against the codling moth",
         concl="trapping the moths would protect the orchard better",
         p1="the moths in this valley have survived every spray used against them for the past five years",
         ic="further spraying is unlikely to reduce the number of moths",
         p2="traps catch the moths without harming the bees that pollinate the blossom",
         concl_para="Traps would protect the orchard from the codling moth better than sprays.",
         ic_para="More spraying probably would not bring the moth population down.",
         p1_para="For five years the valley's moths have survived every spray tried on them.",
         opp_para="An early spring spray is the most effective protection against the codling moth.",
         p2_para="Moth traps do not harm the bees that pollinate the orchard.",
         over="Orchards should never be sprayed against any pest at all."),
    dict(speaker="hospital administrator", opp_who="Some doctors",
         opp="the hospital should build a second car park for visitors",
         concl="a shuttle bus from the railway station would serve visitors better",
         p1="most of the visitors who complain about parking live near the railway line",
         ic="a shuttle from the station would reach most of the visitors who now struggle to park",
         p2="the land for a second car park is the only space left for the planned maternity wing",
         concl_para="A shuttle bus from the station would serve visitors better than a new car park.",
         ic_para="Most visitors who have trouble parking could use a shuttle from the station.",
         p1_para="The visitors who complain about parking mostly live close to the railway.",
         opp_para="The hospital should add another car park for its visitors.",
         p2_para="A second car park would take the only site available for the new maternity wing.",
         over="Hospitals should never provide parking for visitors."),
    dict(speaker="city arborist", opp_who="Some shop owners",
         opp="the plane trees on the high street should be felled because their roots lift the pavement",
         concl="the trees should be kept and the pavement relaid around the roots",
         p1="the trees shade the street in summer, and the city's footfall counts show that shaded streets draw more shoppers on hot days",
         ic="felling the trees would cost the shops custom on hot summer days",
         p2="relaying the pavement costs less than felling the trees and planting young ones",
         concl_para="The high street's trees should stay, with the pavement relaid around their roots.",
         ic_para="Without the trees, the shops would draw fewer customers on hot summer days.",
         p1_para="The trees give the street summer shade, and shaded streets attract more shoppers in hot weather.",
         opp_para="The high street's plane trees should be cut down because their roots damage the pavement.",
         p2_para="It is cheaper to relay the pavement than to remove the trees and replant.",
         over="No street tree in the city should ever be felled."),
    dict(speaker="parks manager", opp_who="Some dog owners",
         opp="dogs should be allowed off the lead everywhere in the nature reserve",
         concl="dogs should be kept on the lead in the reserve during the nesting season",
         p1="the rangers' surveys show that most of the reserve's ground nests lie within a few metres of the paths",
         ic="loose dogs on the paths would disturb most of the nests",
         p2="the town already provides a large fenced field where dogs can run free",
         concl_para="Dogs in the reserve should be on the lead while birds are nesting.",
         ic_para="Dogs running loose along the paths would disturb the majority of nests.",
         p1_para="Surveys show that most ground nests in the reserve are close to its paths.",
         opp_para="Dogs should be free to run off the lead throughout the reserve.",
         p2_para="The town has a fenced field set aside for dogs to run off the lead.",
         over="Dogs should be banned from every nature reserve at all times."),
    dict(speaker="bus company planner", opp_who="Some of the company's directors",
         opp="the late-night buses should be cut because they run nearly empty",
         concl="the late-night buses should continue",
         p1="most of the riders on the late buses are hospital and hotel staff going home after their shifts",
         ic="cutting the late buses would leave some night-shift workers with no way home",
         p2="the late buses cost little to run, since their drivers are already on shift for the depot's night work",
         concl_para="The company should keep running its late-night buses.",
         ic_para="Without the late buses, some night-shift workers would have no way of getting home.",
         p1_para="The late buses mostly carry hospital and hotel workers finishing their shifts.",
         opp_para="The late-night buses should be withdrawn because they carry so few passengers.",
         p2_para="The late buses are cheap to run because their drivers are already working the night shift.",
         over="A bus company should never cut any route, however few people use it."),
    dict(speaker="festival organiser", opp_who="Some local traders",
         opp="the summer festival should move from the park to the town square",
         concl="the festival should stay in the park",
         p1="the town square holds fewer than half the people who came to last year's festival",
         ic="moving to the square would force the festival to turn most of its visitors away",
         p2="the festival already holds the licences it needs for the park, and new ones for the square would take a year to obtain",
         concl_para="The summer festival should continue to be held in the park.",
         ic_para="In the square, the festival would have to turn away most of its visitors.",
         p1_para="The square can hold less than half of last year's festival crowd.",
         opp_para="The summer festival should be moved to the town square.",
         p2_para="New licences for the square would take a year, while the park's licences are already held.",
         over="No festival should ever be held in a town square."),
    dict(speaker="university librarian", opp_who="Some faculty members",
         opp="the library should cancel its print journal subscriptions and rely on online access alone",
         concl="the print subscriptions for the most used journals should be kept",
         p1="the publishers' online licences can be withdrawn at renewal, taking every back issue with them",
         ic="online access alone would leave the library with no lasting copy of those journals",
         p2="the print subscriptions cost less than a tenth of the library's journal budget",
         concl_para="The library should keep its print subscriptions to its most used journals.",
         ic_para="Relying only on online access would leave the library without a permanent copy of those journals.",
         p1_para="A publisher can withdraw online access to back issues when a licence comes up for renewal.",
         opp_para="The library should drop its print journals and depend entirely on online access.",
         p2_para="Print subscriptions account for under a tenth of what the library spends on journals.",
         over="A library should never cancel any print subscription."),
    dict(speaker="water engineer", opp_who="Some councillors",
         opp="the town's old reservoir dam should be strengthened rather than replaced",
         concl="the dam should be replaced",
         p1="the survey found cracks running through the core of the dam, not only across its face",
         ic="strengthening the face would leave the main weakness untouched",
         p2="a new dam would hold more water for a town that has grown by half since the old one was built",
         concl_para="The old reservoir dam should be replaced.",
         ic_para="Reinforcing the face of the dam would not deal with its main weakness.",
         p1_para="The survey showed that the dam's cracks run through its core as well as across its face.",
         opp_para="The old dam should be reinforced, not replaced.",
         p2_para="A new dam could store more water for the town, which has grown considerably.",
         over="Every old dam should be replaced rather than repaired."),
    dict(speaker="sports club treasurer", opp_who="Some members",
         opp="the club should raise its annual fee to pay for new floodlights",
         concl="the floodlights should be paid for with a grant instead",
         p1="the sports council pays the whole cost of floodlights for clubs that open their grounds to local schools, as this club already does",
         ic="the club could pay for the lights without asking members for more",
         p2="a higher fee would drive away the junior members on whom the club's future depends",
         concl_para="The club should fund its floodlights through a grant rather than a fee increase.",
         ic_para="The club could install the lights without charging its members more.",
         p1_para="The sports council fully funds floodlights for clubs that share their grounds with schools, as this club does.",
         opp_para="The club should put up its annual fee to pay for new floodlights.",
         p2_para="Raising the fee would lose the club its junior members.",
         over="A sports club should never raise its fees for any reason."),
    dict(speaker="restaurant owner", opp_who="Some of the staff",
         opp="the restaurant should stop taking bookings and serve diners as they arrive",
         concl="the restaurant should keep taking bookings",
         p1="most of the restaurant's customers travel in from out of town for a special occasion",
         ic="diners turned away at the door would rarely come back",
         p2="bookings let the kitchen order fresh fish in the amounts it will actually use",
         concl_para="The restaurant should continue to accept bookings.",
         ic_para="Customers who were turned away on arrival would seldom return.",
         p1_para="Most of the restaurant's diners come from out of town to mark a special occasion.",
         opp_para="The restaurant should abandon bookings and seat diners in the order they arrive.",
         p2_para="Bookings allow the kitchen to buy only as much fresh fish as it will use.",
         over="No restaurant should ever serve diners who have not booked."),
    dict(speaker="county archivist", opp_who="Some council officers",
         opp="the paper records should be destroyed once they have been scanned",
         concl="the paper records should be kept after scanning",
         p1="scanning at the speed the council is paying for misses faint pencil notes in the margins",
         ic="the scans would lose part of what the records contain",
         p2="the paper records take up one room in a building the council already owns",
         concl_para="The council should retain its paper records even after they have been scanned.",
         ic_para="Scanning would lose some of the information the records contain.",
         p1_para="The scanning the council has paid for fails to pick up faint pencil notes in the margins.",
         opp_para="Once the records have been scanned, the paper originals should be destroyed.",
         p2_para="Keeping the paper records requires only one room in a building the council owns.",
         over="No original document should ever be destroyed after it has been copied."),
    dict(speaker="farm cooperative manager", opp_who="Some members",
         opp="the cooperative should sell its grain at harvest, when it can be moved off the farms at once",
         concl="the cooperative should store its grain and sell it in the spring",
         p1="the price of grain in this region has been higher in spring than at harvest in each of the last ten years",
         ic="grain sold in the spring would usually fetch more",
         p2="the cooperative's new silos can hold the whole harvest with room to spare",
         concl_para="The cooperative should hold its grain over the winter and sell it in spring.",
         ic_para="The cooperative would generally get a better price by selling in spring.",
         p1_para="For ten years running, grain prices in the region have been higher in spring than at harvest.",
         opp_para="The cooperative should sell its grain at harvest time.",
         p2_para="The cooperative's new silos have enough space for the entire harvest.",
         over="Farmers should never sell grain at harvest time."),
    dict(speaker="theatre manager", opp_who="Some actors",
         opp="the theatre should stop its Sunday matinees",
         concl="the Sunday matinees should continue",
         p1="the Sunday audience is drawn mostly from families who cannot come on weekday evenings",
         ic="ending the matinees would lose the theatre an audience it cannot reach at any other time",
         p2="the Sunday performances sell more tickets than any weekday show",
         concl_para="The theatre should keep its Sunday matinee performances.",
         ic_para="Without the matinees the theatre would lose an audience it could not reach otherwise.",
         p1_para="Most of the Sunday audience are families who cannot attend weekday evening shows.",
         opp_para="The theatre should end its Sunday matinees.",
         p2_para="Sunday performances sell more tickets than any performance during the week.",
         over="Every theatre should hold matinees on Sundays."),
    dict(speaker="art historian", opp_who="Some dealers",
         opp="the unsigned portrait in the town hall was painted by the court painter whose style it resembles",
         concl="the portrait is more probably the work of one of the court painter's pupils",
         p1="the canvas was woven on a loom that came into use only after the court painter's death",
         ic="the portrait was painted after the court painter had died",
         p2="the court painter's pupils are known to have copied his style closely for patrons who could not afford the master himself",
         concl_para="One of the court painter's pupils probably painted the unsigned portrait.",
         ic_para="The portrait was painted after the death of the court painter.",
         p1_para="The portrait's canvas was made on a loom first used after the court painter died.",
         opp_para="The court painter whose style the portrait resembles painted it.",
         p2_para="The court painter's pupils copied his style closely for patrons who could not afford him.",
         over="Every unsigned portrait in the court painter's style was painted by one of his pupils."),
    dict(speaker="road safety officer", opp_who="Some residents",
         opp="the speed humps outside the primary school should be removed because they damage cars",
         concl="the humps should stay",
         p1="drivers on the road now pass the school at well under the limit",
         ic="the humps have made the road safer for the children who cross it",
         p2="no claim for damage to a car driven within the limit has been upheld since the humps were built",
         concl_para="The speed humps outside the primary school should be kept.",
         ic_para="The humps have made the road safer for children crossing it.",
         p1_para="Drivers now go past the school well below the speed limit.",
         opp_para="The speed humps should be taken out because they damage vehicles.",
         p2_para="No damage claim from a driver within the limit has succeeded since the humps went in.",
         over="Every road near a school should have speed humps."),
    dict(speaker="software team lead", opp_who="Some developers",
         opp="the team should rewrite the billing system from scratch",
         concl="the billing system should be improved a piece at a time",
         p1="the last two rewrites the company attempted ran years over schedule while the old systems still had to be maintained",
         ic="a full rewrite would likely leave the team supporting two billing systems for years",
         p2="most of the faults customers report come from a small part of the code that can be replaced on its own",
         concl_para="The billing system should be improved gradually rather than rewritten.",
         ic_para="Rewriting the system would probably leave the team maintaining two billing systems for years.",
         p1_para="The company's last two rewrites overran by years while the old systems still needed upkeep.",
         opp_para="The billing system should be rewritten from the beginning.",
         p2_para="Most reported faults come from a small section of code that could be replaced by itself.",
         over="No software system should ever be rewritten from scratch."),
    dict(speaker="swimming pool manager", opp_who="Some council members",
         opp="the council pool should close during the winter months to save on heating",
         concl="the pool should stay open all year",
         p1="the pool's winter swimming lessons are booked by nearly every primary school in the district",
         ic="a winter closure would leave most local children without swimming lessons for half the year",
         p2="the new solar panels on the pool roof have cut the heating bill by more than half",
         concl_para="The council pool should remain open to swimmers in every month of the year, winter included.",
         ic_para="Closing the pool in winter would deprive most local children of swimming lessons for months.",
         p1_para="Almost every primary school in the district books the pool's winter lessons.",
         opp_para="The pool should shut in winter so that the council spends less on heating.",
         p2_para="Solar panels have already reduced the pool's heating costs substantially.",
         over="No public pool should ever close for any part of the year."),
    dict(speaker="vineyard manager", opp_who="Some of the owners",
         opp="the vineyard should replace its hand harvest with machine picking",
         concl="the grapes should go on being picked by hand",
         p1="the vineyard's oldest and best vines grow on terraces too narrow for a harvesting machine",
         ic="machine picking could not harvest the vineyard's best fruit",
         p2="the vineyard's wines sell at a premium because the labels say the grapes are picked by hand",
         concl_para="The vineyard should keep harvesting all of its grapes by hand rather than by machine.",
         ic_para="A harvesting machine would be unable to pick the vineyard's best grapes.",
         p1_para="The vineyard's best vines grow on terraces too narrow for a machine.",
         opp_para="The vineyard should switch from hand picking to machine harvesting.",
         p2_para="The vineyard's wines command higher prices because their grapes are picked by hand.",
         over="No vineyard should ever use a machine to harvest its grapes."),
    dict(speaker="ferry company director", opp_who="Some councillors",
         opp="the early morning ferry should be cut because it runs half empty",
         concl="the early ferry should be kept on the timetable",
         p1="the early ferry brings most of the mainland hospital's morning nurses across from the island",
         ic="cutting the early ferry would leave the hospital short of nurses each morning",
         p2="the early ferry carries the island's post and newspapers at no extra cost to the company",
         concl_para="The company should keep the early morning ferry running on its timetable.",
         ic_para="Without the early ferry the hospital would be short of nurses in the mornings.",
         p1_para="Most of the hospital's morning nurses travel from the island on the early ferry.",
         opp_para="The early ferry should be withdrawn because it carries few passengers.",
         p2_para="The early ferry also carries the island's post and newspapers at no added cost.",
         over="No ferry service should ever be cut, however few passengers it carries."),
    dict(speaker="veterinary practice manager", opp_who="Some of the partners",
         opp="the practice should stop opening its surgery at weekends",
         concl="the weekend surgery should continue",
         p1="most of the practice's emergency cases arrive on Saturdays and Sundays",
         ic="closing at weekends would turn away the animals that most need treatment",
         p2="the weekend vets are paid from a fund that local farmers set up for that purpose",
         concl_para="The practice should go on opening its surgery on Saturdays and Sundays.",
         ic_para="A weekend closure would turn away the animals in most urgent need of care.",
         p1_para="Most of the practice's emergencies come in at weekends.",
         opp_para="The practice should end its surgery hours on weekends.",
         p2_para="A fund set up by local farmers pays for the weekend vets.",
         over="Every veterinary practice should be open every day of the week."),
    dict(speaker="planetarium director", opp_who="Several trustees",
         opp="the planetarium should replace its live shows with recorded films",
         concl="the live shows should be kept",
         p1="school groups book the live shows because a presenter can answer their pupils' questions",
         ic="dropping the live shows would lose the planetarium most of its school bookings",
         p2="the recorded films would cost more to license each year than the presenters are paid",
         concl_para="The planetarium should keep putting on its live shows rather than switch to films.",
         ic_para="Replacing the live shows would cost the planetarium most of its school bookings.",
         p1_para="Schools choose the live shows because presenters can take their pupils' questions.",
         opp_para="The planetarium should show recorded films instead of live shows.",
         p2_para="Licensing the films would cost more each year than paying the presenters.",
         over="No planetarium should ever show a recorded film."),
    dict(speaker="youth football coach", opp_who="Some parents",
         opp="the under-twelve team should play on a full-size pitch to prepare for senior football",
         concl="the team should keep playing on the smaller pitch",
         p1="on a small pitch each child touches the ball several times as often as on a full-size one",
         ic="the small pitch gives the children far more practice with the ball",
         p2="the league's own rules require under-twelve matches to be played on a reduced pitch",
         concl_para="The under-twelve team should continue to play on the smaller pitch.",
         ic_para="Playing on the smaller pitch gives the children much more time on the ball.",
         p1_para="Children touch the ball far more often on a small pitch than on a full-size one.",
         opp_para="The under-twelve team should move to a full-size pitch to prepare for senior football.",
         p2_para="League rules say under-twelve matches must use a reduced pitch.",
         over="Children should never play football on a full-size pitch."),
    dict(speaker="hotel manager", opp_who="Some of the hotel's investors",
         opp="the hotel should close its restaurant and let guests eat in town",
         concl="the restaurant should stay open",
         p1="guests who book a room with dinner stay on average two nights longer than other guests",
         ic="closing the restaurant would shorten the average guest's stay",
         p2="the nearest restaurants in town are forty minutes' drive from the hotel",
         concl_para="The hotel should continue to run its restaurant rather than closing it.",
         ic_para="Guests would stay fewer nights on average if the restaurant closed.",
         p1_para="Guests who book dinner with their room stay two nights longer on average.",
         opp_para="The hotel should shut its restaurant and send guests into town to eat.",
         p2_para="The closest restaurants in town are a long drive from the hotel.",
         over="No hotel should ever be without a restaurant of its own."),
    dict(speaker="choir director", opp_who="Some members",
         opp="the choir should drop its spring concert to save rehearsal time",
         concl="the spring concert should go ahead",
         p1="the spring concert raises most of the money the choir spends on sheet music for the year",
         ic="without the spring concert the choir could not afford its music for next season",
         p2="the hall has already been booked and the deposit cannot be refunded",
         concl_para="The choir should go ahead with its spring concert as planned.",
         ic_para="Cancelling the spring concert would leave the choir unable to pay for next season's music.",
         p1_para="Most of the choir's yearly spending on sheet music comes from the spring concert.",
         opp_para="The choir should cancel the spring concert to free up rehearsal time.",
         p2_para="The concert hall's deposit has been paid and will not be returned.",
         over="A choir should never cancel a concert for any reason."),
    dict(speaker="allotment society secretary", opp_who="Some plot holders",
         opp="the society should spray the site against slugs to protect the vegetables",
         concl="the site should not be sprayed",
         p1="the slug spray the plot holders propose is poisonous to the bees kept in the hives on the site",
         ic="spraying would put the society's bees at risk",
         p2="the frogs and beetles on the allotments already keep the slugs in check",
         concl_para="The allotment site should not be sprayed against slugs at all.",
         ic_para="Spraying the allotments would endanger the society's bees.",
         p1_para="The proposed slug spray is toxic to the bees kept on the site.",
         opp_para="The allotments should be sprayed to protect the vegetables from slugs.",
         p2_para="Frogs and beetles already control the slugs on the allotments.",
         over="No garden should ever be treated with any spray."),
    dict(speaker="county surveyor", opp_who="Some district councillors",
         opp="the old stone bridge should be demolished and replaced with a wider concrete one",
         concl="the stone bridge should be repaired instead",
         p1="the engineers' survey found the stone arches sound and only the road surface worn",
         ic="the bridge can be kept safe for many more years by resurfacing it",
         p2="a wider bridge would draw lorries onto the narrow village road beyond it",
         concl_para="The old stone bridge should be repaired and kept rather than demolished and replaced.",
         ic_para="Resurfacing the old bridge would keep it safe for many years.",
         p1_para="The survey showed that the bridge's arches are sound and only its road surface is worn.",
         opp_para="The stone bridge should be pulled down and a wider concrete bridge built.",
         p2_para="A wider bridge would bring lorries onto the narrow road through the village.",
         over="No old bridge should ever be replaced."),
    dict(speaker="market superintendent", opp_who="Some traders",
         opp="the Saturday market should move from the square to the new car park, where there is more room",
         concl="the market should stay in the square",
         p1="most of the market's customers come on foot from the shops and cafes around the square",
         ic="a market in the car park would lose much of its passing trade",
         p2="the car park is needed on Saturdays by the shoppers who drive into town",
         concl_para="The Saturday market should stay where it is in the town square rather than move to the new car park.",
         ic_para="Moving the market to the car park would cost it a large share of its passing customers.",
         p1_para="Most market customers walk over from the shops and cafes around the square.",
         opp_para="The market should be moved to the new car park because it has more space.",
         p2_para="Shoppers who drive into town need the car park on Saturdays.",
         over="No town market should ever be moved from its traditional site."),
    dict(speaker="canal trust engineer", opp_who="Some councillors",
         opp="the disused lock at the top of the flight should be filled in and grassed over",
         concl="the lock should be restored to working order",
         p1="boats cannot reach the reservoir basin above the flight without passing through that lock",
         ic="filling in the lock would cut the basin off from the rest of the canal for good",
         p2="the trust has been offered a grant that covers most of the cost of the repairs",
         concl_para="The disused lock should be repaired so that it works again.",
         ic_para="If the lock were filled in, the basin would be permanently cut off from the canal.",
         p1_para="The lock is the only way for boats to get from the canal to the reservoir basin.",
         opp_para="The old lock at the top of the flight should be filled in.",
         p2_para="A grant has been offered that would pay for most of the restoration.",
         over="Every disused lock on every canal should be restored."),
    dict(speaker="community radio manager", opp_who="Several board members",
         opp="the station should stop broadcasting overnight to cut its electricity bill",
         concl="the overnight broadcasts should continue",
         p1="the overnight programmes are the only local programmes heard by the town's night-shift workers and hospital staff",
         ic="ending the overnight broadcasts would leave many of the station's regular listeners with nothing local to hear",
         p2="the transmitter draws so little power at night that the saving would be small",
         concl_para="The station should keep broadcasting through the night rather than going off the air.",
         ic_para="Without overnight broadcasts, many regular listeners would have no local programmes to hear.",
         p1_para="The overnight programmes are the only local radio that night-shift workers and hospital staff hear.",
         opp_para="The station should go off the air at night to lower its electricity costs.",
         p2_para="Running the transmitter at night costs little in electricity.",
         over="No radio station should ever reduce its broadcasting hours."),
    dict(speaker="zoo director", opp_who="Some trustees",
         opp="the zoo should open on summer evenings to draw more visitors",
         concl="the zoo should not open in the evenings",
         p1="the keepers' observations show that several of the larger animals become restless when crowds stay past dusk",
         ic="evening opening would harm the welfare of some of the animals the zoo exists to care for",
         p2="the extra staff and lighting would cost more than the evening tickets are likely to bring in",
         concl_para="The zoo should keep its present opening hours and stay closed on summer evenings.",
         ic_para="Opening in the evening would be bad for the welfare of some of the zoo's animals.",
         p1_para="Some of the larger animals grow restless when visitors stay after dark.",
         opp_para="The zoo should open on summer evenings in order to attract more visitors.",
         p2_para="Evening opening would cost more in staff and lighting than it would earn.",
         over="No zoo should ever be open after dark."),
    dict(speaker="bakery owner", opp_who="Some of the bakers",
         opp="the bakery should switch to a cheaper flour from a supermarket supplier",
         concl="the bakery should keep buying its flour from the local mill",
         p1="in blind tastings the bakery's regular customers preferred loaves made with the mill's flour",
         ic="switching to a cheaper flour would risk losing the customers who buy the bakery's bread",
         p2="the mill delivers every morning, while the supermarket supplier delivers only twice a week",
         concl_para="The bakery should continue to buy flour from the local mill.",
         ic_para="Changing to a cheaper flour could drive away the bakery's bread customers.",
         p1_para="Regular customers preferred bread made with the mill's flour in blind tastings.",
         opp_para="The bakery should buy a cheaper flour from a supermarket supplier.",
         p2_para="The local mill delivers daily, but the supermarket supplier delivers only twice a week.",
         over="A bakery should never change its flour supplier."),
    dict(speaker="ice rink manager", opp_who="Some councillors",
         opp="the rink should close for the summer months to save on the cost of keeping the ice frozen",
         concl="the rink should stay open all year",
         p1="the figure skating and ice hockey clubs train at the rink through the summer for the winter season",
         ic="closing for the summer would force the clubs to travel to another town to train",
         p2="summer is when the rink's school holiday sessions sell out",
         concl_para="The ice rink should remain open in the summer months instead of closing until winter.",
         ic_para="A summer closure would make the skating and hockey clubs train elsewhere.",
         p1_para="The rink's skating and hockey clubs use it for summer training before their winter season.",
         opp_para="The ice rink should shut in summer to cut the cost of keeping the ice frozen.",
         p2_para="The rink's school holiday sessions sell out in the summer.",
         over="No public sports facility should ever close for part of the year."),
    dict(speaker="cycling officer", opp_who="Some shopkeepers",
         opp="the cycle lane on Castle Street should be removed to make room for parking",
         concl="the cycle lane should stay",
         p1="the number of cyclists hurt on Castle Street has fallen sharply since the lane opened",
         ic="the lane has made the street safer for the people who cycle along it",
         p2="a count of shoppers found that most of those visiting Castle Street's shops arrive on foot or by bicycle",
         concl_para="The Castle Street cycle lane should be kept.",
         ic_para="The cycle lane has made Castle Street safer for cyclists.",
         p1_para="Fewer cyclists have been injured on Castle Street since the cycle lane was opened.",
         opp_para="The Castle Street cycle lane should be taken out so that more cars can park.",
         p2_para="Most people who come to the shops on Castle Street walk or cycle there.",
         over="No cycle lane in the town should ever be removed."),
    dict(speaker="head cook", opp_who="Some governors",
         opp="the school should close its kitchen and buy in meals from a catering firm",
         concl="the school should keep cooking its own meals",
         p1="the catering firm's meals are cooked the day before and reheated at the school",
         ic="bought-in meals would be less fresh than the ones the kitchen now serves",
         p2="the kitchen already buys its vegetables from farms nearby at prices the firm cannot match",
         concl_para="The school should keep its own kitchen and go on cooking the meals it serves.",
         ic_para="Meals bought from the catering firm would not be as fresh as the school's own.",
         p1_para="The firm cooks its meals a day ahead and has them reheated at the school.",
         opp_para="The school kitchen should be closed and meals bought from a caterer.",
         p2_para="The kitchen gets its vegetables from nearby farms more cheaply than the firm could.",
         over="No school should ever buy meals from an outside caterer."),
    dict(speaker="bee inspector", opp_who="Some residents",
         opp="beehives should be banned from gardens in the town",
         concl="the hives should not be banned",
         p1="the town's beekeepers must already register their hives and keep them away from paths and fences",
         ic="the hives are already kept where they are unlikely to trouble passers-by",
         p2="the bees pollinate the fruit trees in the town's gardens and orchards",
         concl_para="Beehives should continue to be allowed in the town's gardens.",
         ic_para="The town's hives are already sited where passers-by are unlikely to be bothered.",
         p1_para="Beekeepers in the town must register their hives and site them away from paths and fences.",
         opp_para="Gardens in the town should not be allowed to have beehives.",
         p2_para="The town's bees pollinate the fruit trees in its gardens and orchards.",
         over="Beekeeping should never be restricted anywhere."),
    dict(speaker="lifeboat station chair", opp_who="Some fundraisers",
         opp="the station should sell its old launching tractor to raise money for a new boathouse",
         concl="the tractor should be kept",
         p1="the new boat is launched from the beach and cannot reach the water at low tide without the tractor",
         ic="selling the tractor would leave the new boat unable to launch for part of every day",
         p2="a new boathouse can be paid for from the legacy left to the station last year",
         concl_para="The lifeboat station should keep its old launching tractor.",
         ic_para="Without the tractor, the new lifeboat could not be launched at certain times each day.",
         p1_para="At low tide the new boat can only be launched from the beach with the tractor's help.",
         opp_para="The old launching tractor should be sold to pay for a new boathouse.",
         p2_para="Last year's legacy can pay for a new boathouse.",
         over="A lifeboat station should never sell any of its equipment."),
]


def render(i, a):
    """The argument, in the template its index selects."""
    if i % 2 == 0:
        body = ("%s argue that %s. But %s. After all, %s, so %s. Moreover, %s."
                % (a["opp_who"], a["opp"], a["concl"], a["p1"], a["ic"], a["p2"]))
    else:
        body = ("%s claim that %s. They are mistaken: %s. %s, and it follows that %s. In "
                "addition, %s." % (a["opp_who"], a["opp"], a["concl"], upfirst(a["p1"]),
                                   a["ic"], a["p2"]))
    return upfirst(a["speaker"]) + ": " + body


def explain(a, part):
    c = a["concl"]
    if part == "opp":
        return ("The argument opens with a view only to reject it. The view is that %s. The "
                "argument's own conclusion is that %s." % (a["opp"], c))
    if part == "concl":
        return ("Every other claim the argument makes, apart from the view it rejects, is "
                "offered as a reason to accept that %s, so that is the main conclusion." % c)
    if part == "p1":
        return ("The claim is the reason given for the intermediate conclusion, that %s, which "
                "in turn supports the main conclusion, that %s. It supports the main "
                "conclusion only through that step." % (a["ic"], c))
    if part == "ic":
        return ("The claim is drawn from the premise that %s, which makes it a conclusion, and "
                "it is then offered as a reason for the main conclusion, that %s. A claim that "
                "is both supported and supporting is an intermediate conclusion." % (a["p1"], c))
    if part == "p2":
        return ("The claim is a further reason for the main conclusion, that %s, given "
                "separately from the reasoning about whether %s. Nothing else in the argument "
                "rests on it." % (c, a["ic"]))
    raise ValueError(part)


def explain_main(a):
    # Every part here is followed by punctuation, because a part can carry a comma clause of
    # its own and the words after it would read as part of that clause (INC-0195).
    return ("The argument rejects the view that %s. Its main conclusion is that %s. From the "
            "premise that %s, it draws the claim that %s. That claim is offered as a reason "
            "for the main conclusion, so it is a step on the way rather than the main point."
            % (a["opp"], a["concl"], a["p1"], a["ic"]))


def why_wrong_role(a, role):
    what = {"opp": "the view the argument rejects, which is that " + a["opp"],
            "concl": "the main conclusion, which is that " + a["concl"],
            "p1": "the premise behind the intermediate conclusion, which is that " + a["p1"],
            "ic": "the intermediate conclusion, which is that " + a["ic"],
            "p2": "the separate premise, which is that " + a["p2"]}[role]
    return "describes " + what


class ByArgument(ListsQuestions):
    """A fixed list of questions asked of each argument, so the runner knows when it has
    made them all (INC-0126)."""

    def units(self):
        return [(i, None) for i in range(len(ARGS))]


class ClaimRole(ByArgument, CRBase):
    """The role a named claim plays in an argument whose parts are fixed by its author."""
    id = "lsat_struct_role"
    skill = "lsat_lr_struct"
    section = "LR"
    type = "LR"
    sub = "Role of a claim"
    diff = 3

    def asks(self, i):
        a = ARGS[i]
        out = []
        for part in PARTS:
            claim = a[part]
            w = zlib.crc32(("%d|%s" % (i, part)).encode()) % 2
            # A claim with a comma of its own reads badly with more sentence after it, so
            # it goes at the end of the question.
            if "," in claim:
                w = 1
            q = (STEM_ROLE[0] % (claim, a["speaker"]) if w == 0
                 else STEM_ROLE[1] % (a["speaker"], claim))
            out.append((render(i, a) + "\n\n" + q, part))
        return out

    def make(self, rng, choices_n):
        i = rng.randrange(len(ARGS))
        a = ARGS[i]
        stem, part = rng.choice(self.asks(i))
        right = ROLE[part][zlib.crc32(("%d|%s|key" % (i, part)).encode()) % 2]
        # One description per other role, so no two wrong answers name the same role, and
        # at most two of the roles nothing here plays: those are eliminated at a glance, and
        # a question whose wrong answers are mostly of that kind tests nothing.
        wrongs = [(rng.choice(ROLE[other]), why_wrong_role(a, other))
                  for other in PARTS if other != part] + rng.sample(NEVER, 2)
        diff = {"opp": 2, "concl": 2, "p1": 3, "ic": 4, "p2": 3}[part]
        item = self.emit(rng, choices_n, stem, right, wrongs, explain(a, part), diff,
                         self.skill, self.sub)
        item["section"] = "LR"
        item["type"] = "LR"
        item["canon_ignores_choices"] = True
        roles = [r for c in item["choices"] for r, texts in ROLE.items() if c in texts]
        if len(roles) != len(set(roles)) or roles.count(part) != 1:
            raise ItemError("%s offered a role twice" % self.id)
        return item


class MainConclusion(ByArgument, CRBase):
    """Which choice states the main conclusion, among paraphrases of every other part."""
    id = "lsat_struct_main"
    skill = "lsat_lr_struct"
    section = "LR"
    type = "LR"
    sub = "Main conclusion"
    diff = 3

    def asks(self, i):
        return [(render(i, ARGS[i]) + "\n\n" + STEM_MAIN % ARGS[i]["speaker"], None)]

    def make(self, rng, choices_n):
        i = rng.randrange(len(ARGS))
        a = ARGS[i]
        (stem, _), = self.asks(i)
        right = a["concl_para"]
        wrongs = [
            (a["ic_para"], "is the intermediate conclusion, which the argument draws in order "
             "to support its main point rather than as the point itself"),
            (a["p1_para"], "is a premise, offered as a reason for the intermediate conclusion"),
            (a["p2_para"], "is a premise, offered as a further reason for the conclusion"),
            (a["opp_para"], "is the view the argument rejects"),
            (a["over"], "goes further than the argument does; its conclusion concerns only the "
             "case in front of it"),
        ]
        item = self.emit(rng, choices_n, stem, right, wrongs, explain_main(a), 3, self.skill,
                         self.sub)
        item["section"] = "LR"
        item["type"] = "LR"
        item["canon_ignores_choices"] = True
        return item


GENS = [ClaimRole(), MainConclusion()]

# What may follow a part that has a comma of its own (INC-0195).
CLOSES = ("", ",", ".", ";", ":", "?")


def rendered(i, a):
    """Every text a student reads that quotes the argument's parts, labelled for errors."""
    out = [("the argument", render(i, a))]
    for gen in GENS:
        for stem, _ in gen.asks(i):
            out.append(("a question stem", stem.split("\n\n", 1)[1]))
    for k in PARTS:
        out.append(("the explanation for the %s" % k, explain(a, k)))
        out.append(("the wrong answer reason for the %s" % k,
                    "Choice A " + why_wrong_role(a, k) + "."))
    out.append(("the main conclusion explanation", explain_main(a)))
    return out


def check_args():
    """Every argument renders as five sentences, no part repeats another's wording, and no
    template runs a part with a comma of its own into the words after it."""
    bad = []
    for i, a in enumerate(ARGS):
        missing = [k for k in PARTS + ("speaker", "opp_who", "concl_para", "ic_para", "p1_para",
                                       "opp_para", "p2_para", "over") if not a.get(k)]
        if missing:
            bad.append("argument %d is missing %s" % (i, ", ".join(missing)))
            continue
        for k in PARTS:
            if a[k][0].isupper():
                bad.append("argument %d: %s starts with a capital, and it follows a word" % (i, k))
            # Each part is quoted alone in a question, so it cannot lean on a pronoun whose
            # noun is in another sentence.
            if a[k].split()[0] in ("it", "its", "they", "their", "them", "this", "these"):
                bad.append("argument %d: %s opens with a pronoun" % (i, k))
            if a[k].endswith("."):
                bad.append("argument %d: %s ends with a full stop" % (i, k))
        paras = [a[k] for k in ("concl_para", "ic_para", "p1_para", "opp_para", "p2_para", "over")]
        if len(set(paras)) != len(paras):
            bad.append("argument %d repeats a paraphrase" % i)
        for k in ("concl_para", "ic_para", "p1_para", "opp_para", "p2_para", "over"):
            if not a[k].endswith("."):
                bad.append("argument %d: %s has no full stop" % (i, k))
        # A part with a comma of its own leaves a clause open, so words a template puts
        # straight after it read as part of that clause: "the premise that the trout have
        # declined most in the shallow bays, where the water has warmed the most and is
        # offered as a reason" (INC-0195). Checking each part alone passed every part of that
        # sentence, so the check reads the sentences themselves.
        for where, text in rendered(i, a):
            for k in PARTS:
                if "," not in a[k]:
                    continue
                for v in (a[k], upfirst(a[k])):
                    for m in re.finditer(re.escape(v), text):
                        if text[m.end():m.end() + 1] not in CLOSES:
                            bad.append("argument %d (%s): the %s has a comma of its own and runs "
                                       "into '%s' in %s" % (i, a["speaker"], k,
                                                            text[m.end():m.end() + 20].strip(),
                                                            where))
    return bad
