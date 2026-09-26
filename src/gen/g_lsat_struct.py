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
import zlib

from framework import ItemError, upfirst
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
        return ("The argument opens with the view that %s and then rejects it: its conclusion "
                "is that %s." % (a["opp"], c))
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


def why_wrong_role(a, role):
    what = {"opp": "the view the argument rejects, which is that " + a["opp"],
            "concl": "the main conclusion, which is that " + a["concl"],
            "p1": "the premise behind the intermediate conclusion, which is that " + a["p1"],
            "ic": "the intermediate conclusion, which is that " + a["ic"],
            "p2": "the separate premise, which is that " + a["p2"]}[role]
    return "describes " + what


class ClaimRole(CRBase):
    """The role a named claim plays in an argument whose parts are fixed by its author."""
    id = "lsat_struct_role"
    skill = "lsat_lr_struct"
    section = "LR"
    type = "LR"
    sub = "Role of a claim"
    diff = 3

    def make(self, rng, choices_n):
        i = rng.randrange(len(ARGS))
        a = ARGS[i]
        part = rng.choice(PARTS)
        claim = a[part]
        w = zlib.crc32(("%d|%s" % (i, part)).encode()) % 2
        # A claim with a comma of its own reads badly with more sentence after it, so it
        # goes at the end of the question.
        if "," in claim:
            w = 1
        q = (STEM_ROLE[0] % (claim, a["speaker"]) if w == 0
             else STEM_ROLE[1] % (a["speaker"], claim))
        stem = render(i, a) + "\n\n" + q
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


class MainConclusion(CRBase):
    """Which choice states the main conclusion, among paraphrases of every other part."""
    id = "lsat_struct_main"
    skill = "lsat_lr_struct"
    section = "LR"
    type = "LR"
    sub = "Main conclusion"
    diff = 3

    def make(self, rng, choices_n):
        i = rng.randrange(len(ARGS))
        a = ARGS[i]
        stem = render(i, a) + "\n\n" + STEM_MAIN % a["speaker"]
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
        expl = ("The argument rejects the view that %s and argues that %s. The claim that %s is "
                "drawn from the premise that %s and is offered as a reason for that conclusion, "
                "so it is a step on the way rather than the main point."
                % (a["opp"], a["concl"], a["ic"], a["p1"]))
        item = self.emit(rng, choices_n, stem, right, wrongs, expl, 3, self.skill, self.sub)
        item["section"] = "LR"
        item["type"] = "LR"
        item["canon_ignores_choices"] = True
        return item


GENS = [ClaimRole(), MainConclusion()]


def check_args():
    """Every argument renders as five sentences, and no part repeats another's wording."""
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
    return bad
