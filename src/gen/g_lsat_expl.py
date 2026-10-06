"""Resolving an apparent discrepancy (lsat_lr_expl).

LSAC lists identifying explanations among the skills Logical Reasoning measures (see the
Logical Reasoning row of data/DATA.md), and here it shares a category with parallel
reasoning. That category had 29 hand written items, 22 of them discrepancy questions, and
150 generated parallel reasoning ones, because nothing generated an explanation.

A discrepancy question gives two facts that seem not to fit: something done or expected,
and an outcome that defeats it. It asks which choice, if true, would let both be true.
Whether a choice does that is a judgement, so each scenario below is authored with its
answers sorted in advance. Four resolutions, each with the mechanism that reconciles the
facts, and six wrong answers of the three kinds a test writer uses, each with the reason
it fails:

  deepen   it makes the outcome harder to understand
  aside    it is on the topic and bears on neither fact
  half     it explains the expectation, or why something was done, and leaves the
           outcome where it was

Two questions are asked of each scenario, because a question is its stimulus and stem and
not the choices it offers (INC-0126). Which choice most helps to resolve the discrepancy,
keyed to one resolution against four wrong answers; and which choice does not help, keyed
to a deepen or aside answer against all four resolutions. Which resolution and which wrong
answer serve as keys is fixed per scenario, so a rebuild asks the same questions, and the
keys' length ranks are assigned across the scenarios so length tells a guesser nothing
(INC-0122).

No two statements a question can show together contradict each other: the EXCEPT question
shows all four resolutions beside a deepen or aside answer, so none of those is written to
deny a resolution. Every place and organisation is invented for the question and checked
against the names already in the corpus; nothing here is a claim about the world.
"""
import zlib

from framework import (ItemError, ListsQuestions, balance, buildable_ranks,
                       check_clause_splice, upfirst)
from g_gmat_cr import CRBase
from g_rc import assign_ranks

STEM_RESOLVE = ("Which one of the following, if true, most helps to resolve the apparent "
                "discrepancy described above?")
STEM_EXPLAIN = "Which one of the following, if true, most helps to explain why %s?"
STEM_EXCEPT = ("Each of the following, if true, contributes to a resolution of the apparent "
               "discrepancy described above EXCEPT:")

KINDS = ("deepen", "aside", "half")

SCENES = [
    dict(key="roadwiden",
         setup=("To ease congestion, the town of Brackenmoor widened its main road from "
                "two lanes to four. A year after the work was finished, the average rush "
                "hour journey along the road takes longer than it did before the widening."),
         why="rush hour journeys along the widened road take longer than before",
         puzzle=("Brackenmoor widened its main road to ease congestion, yet rush hour "
                 "journeys along it take longer than before"),
         resolve=[
             (("many drivers who had avoided the road at rush hour began to use it once it "
               "was widened"),
              ("far more cars use the road at rush hour, more than the extra lanes made "
               "room for")),
             (("since the widening, a retail park has opened beside the road, and two new "
               "sets of traffic lights control its entrances"),
              ("the new lights hold up traffic that the extra lanes would otherwise have "
               "moved")),
             (("the four lanes narrow back to two at a bridge just beyond the town, where "
               "traffic now queues back along the road"),
              ("the wider road only brings cars more quickly to a bottleneck that was "
               "never widened")),
             (("since the widening, the bus service along the road has been cut, and most "
               "of its former passengers now drive"),
              "the cars of people who used to take the bus fill the extra lanes"),
         ],
         deepen=[
             (("Brackenmoor's population has not grown since the road was widened, and no "
               "new homes have been built along it"),
              ("rules out new residents as a source of extra traffic, which makes the "
               "slower journeys harder to explain")),
             ("the road's speed limit was raised when the widening was finished",
              ("would let traffic move faster, which makes the longer journeys harder to "
               "explain")),
         ],
         aside=[
             ("the widening was paid for out of the town's budget for road repairs",
              ("concerns how the work was paid for, which has no bearing on how long "
               "journeys take")),
             (("several towns near Brackenmoor are now considering widening their own main "
               "roads, and one of them has already begun the work"),
              ("is about other towns' plans and says nothing about traffic on "
               "Brackenmoor's road")),
         ],
         half=[
             (("before the widening, more traffic used the road at rush hour than its two "
               "lanes could carry"),
              ("explains why the town widened the road, not why journeys became slower "
               "afterwards")),
             ("a road with four lanes can carry more cars an hour than a road with two",
              ("is the reason the widening was expected to help, so it leaves the slower "
               "journeys unexplained")),
         ]),
    dict(key="libraryfines",
         setup=("When the Corliston public library stopped charging fines on overdue "
                "books, its staff expected to lose more books, since borrowers would have "
                "less reason to bring them back. In the first year without fines, the "
                "number of books that were never returned fell by a third."),
         why="fewer books went unreturned once the library stopped charging fines",
         puzzle=("the library expected to lose more books once it stopped charging fines, "
                 "yet fewer books went unreturned"),
         resolve=[
             (("many borrowers had kept overdue books for good because they could not "
               "afford the fines that had built up on them"),
              ("ending the fines removed those borrowers' reason to keep the books, so "
               "more came back")),
             (("in the month the fines ended, the library began sending borrowers a text "
               "message two days before each book was due"),
              ("a new reminder brought books back, outweighing any loss from ending the "
               "fines")),
             (("borrowers who owed fines had been barred from the library until they paid, "
               "so many never came back with the books they held"),
              ("ending the fines ended the bar, and borrowers who had stayed away returned "
               "with their books")),
             (("the library had counted as lost every book whose fine went unpaid for a "
               "year, even if the book was later returned"),
              ("with no fines to go unpaid, late books are no longer counted as lost, so "
               "the count falls")),
         ],
         deepen=[
             (("the library lent out more books in its first year without fines than in "
               "any earlier year, and to more borrowers than ever before"),
              ("means more books were out on loan to be lost, which makes the fall harder "
               "to explain")),
             (("borrowers surveyed after the change said they no longer felt any pressure "
               "to return books on time"),
              ("suggests borrowers became less careful about returning books, which "
               "deepens the puzzle")),
         ],
         aside=[
             (("the money raised by fines had been a small part of the library's budget, "
               "less than it spent each year on newspapers"),
              ("concerns the library's budget, which has no bearing on how many books came "
               "back")),
             (("several other libraries in the region had stopped charging fines in "
               "earlier years"),
              ("is about other libraries and says nothing about why Corliston lost fewer "
               "books")),
         ],
         half=[
             (("fines had been the library's main way of encouraging borrowers to return "
               "books"),
              ("explains why the staff expected to lose more books, not why they lost "
               "fewer")),
             ("a borrower who owes nothing has less to lose by keeping a book",
              ("supports the staff's expectation, so it leaves the fall in lost books "
               "unexplained")),
         ]),
    dict(key="handwash",
         setup=("Dunmarsh Hospital introduced a stricter hand washing rule for its staff "
                "in order to reduce infections among its patients. In the six months after "
                "the rule took effect, the hospital recorded more infections among its "
                "patients than in the six months before."),
         why="the hospital recorded more infections after the stricter rule took effect",
         puzzle=("the hospital brought in a stricter hand washing rule to reduce "
                 "infections, yet it recorded more infections afterwards"),
         resolve=[
             (("when the rule took effect, the hospital began testing every patient for "
               "infection rather than only those with symptoms"),
              ("infections that would have gone unnoticed are now found and recorded, so "
               "the count rises even if fewer patients are infected")),
             (("in the same months, the hospital took in patients from a closed hospital "
               "nearby, many of them already infected"),
              ("the extra infections were brought in from outside, which says nothing "
               "against the rule")),
             (("the rule was brought in because an outbreak had already begun on two wards "
               "and went on for months"),
              "the infections came from an outbreak already under way when the rule began"),
             (("with the new rule came a simpler form for recording infections, and staff "
               "had seldom filled in the old one"),
              ("infections that went unrecorded before are now written down, so the count "
               "rises without more patients being infected")),
         ],
         deepen=[
             ("audits on every ward found that the staff followed the new rule closely",
              "rules out the rule being ignored, which makes the rise harder to explain"),
             (("the hospital opened no new wards and began no new kinds of surgery in the "
               "six months after the rule took effect"),
              ("rules out new wards or new surgery as a source of infections, which "
               "deepens the puzzle")),
         ],
         aside=[
             (("the new hand washing stations were installed by an outside contractor, who "
               "also fitted new taps in the staff kitchens"),
              ("concerns who installed the stations, which has no bearing on how many "
               "infections were recorded")),
             ("the rule was announced to the staff in the hospital's monthly newsletter",
              ("concerns how the rule was announced, which says nothing about the "
               "infections")),
         ],
         half=[
             (("washing hands between patients reduces the spread of infection from one "
               "patient to another"),
              "explains why the rule was expected to help, not why infections rose"),
             (("the hospital adopted the rule because its infection figures had worried "
               "its board"),
              "explains why the rule was adopted, not why infections rose afterwards"),
         ]),
    dict(key="coffeeprice",
         setup=("In March the Dunlin Street café raised the price of a cup of coffee by a "
                "fifth. In April the café sold more cups of coffee than in any earlier "
                "month."),
         why="the café sold more coffee in April after raising its price in March",
         puzzle=("the café raised the price of its coffee in March, yet it sold more cups "
                 "in April than ever before"),
         resolve=[
             ("a larger café two doors away closed for good at the end of March",
              ("the closed café's customers had to buy their coffee somewhere, and many "
               "came to Dunlin Street")),
             (("in April a new office building opened across the street, bringing several "
               "hundred workers to the block"),
              ("several hundred new customers more than made up for any put off by the "
               "price")),
             (("in April the café began opening an hour earlier, before any other café "
               "nearby had opened"),
              "the café now sells to early customers who have nowhere else to go"),
             (("the café's outdoor tables open each April, and its sales have risen every "
               "April when they do"),
              "the usual April rise in sales outweighed any loss from the higher price"),
         ],
         deepen=[
             (("the other cafés on Dunlin Street kept their prices the same in April, so a "
               "cup of coffee cost less at each of them"),
              ("means the café was now dearer than its neighbours, which makes the rise in "
               "sales harder to explain")),
             (("the café's regular customers had complained about its prices even before "
               "the rise"),
              "suggests its customers mind what they pay, which deepens the puzzle"),
         ],
         aside=[
             ("the café buys its coffee beans from a roaster outside the city",
              ("concerns where the beans come from, which has no bearing on how many cups "
               "were sold")),
             (("the café's owner also runs a bakery in another part of the town, which "
               "opened two years ago"),
              ("is about the owner's other business and says nothing about the café's "
               "sales")),
         ],
         half=[
             ("customers usually buy less of a product when its price rises",
              "is why the rise in sales is surprising, so it leaves it unexplained"),
             (("the café raised its price because the cost of its milk and beans had gone "
               "up"),
              "explains why the price rose, not why sales rose with it"),
         ]),
    dict(key="classsize",
         setup=("To raise its pupils' test scores, the Pellam school district cut its "
                "average class size from thirty pupils to twenty. In the following year, "
                "the average score of the district's pupils on the state reading test "
                "fell."),
         why="the district's reading scores fell after it cut its class sizes",
         puzzle=("the district cut its class sizes to raise test scores, yet its pupils' "
                 "reading scores fell"),
         resolve=[
             (("to staff the extra classes, the district hired many teachers who had just "
               "finished their training"),
              ("the new classes were taught by less experienced teachers, which could more "
               "than undo the benefit of smaller classes")),
             ("in the same year, the state replaced its reading test with a harder one",
              "a harder test lowers scores whatever the class size"),
             (("pupils who had been excused from the test in earlier years were required "
               "to take it from that year on"),
              "pupils who would have scored low are now counted in the average"),
             (("that year a new school opened nearby and took many of the district's "
               "highest scoring pupils"),
              "losing its strongest pupils pulls the district's average down"),
         ],
         deepen=[
             (("attendance in the district's schools rose after the class sizes were cut, "
               "and fewer lessons were missed through illness"),
              ("means pupils spent more time in lessons, which makes the fall harder to "
               "explain")),
             ("the district's teachers spent more time with each pupil after the change",
              "is what smaller classes were meant to bring, so it deepens the puzzle"),
         ],
         aside=[
             ("the smaller classes were paid for by a rise in the local property tax",
              "concerns how the change was paid for, which has no bearing on the scores"),
             (("the district's schools changed their uniforms in the same year, from grey "
               "to dark blue"),
              "concerns uniforms, which have no bearing on reading scores"),
         ],
         half=[
             ("pupils in smaller classes receive more of their teacher's attention",
              "explains why the district expected scores to rise, not why they fell"),
             (("the district cut class sizes after parents complained that the classes "
               "were too large"),
              "explains why the change was made, not why scores fell afterwards"),
         ]),
    dict(key="firestation",
         setup=("To shorten the time its fire crews take to reach a fire, the town of "
                "Ashenford opened a second fire station on its east side. In the year "
                "after the station opened, the average time between an alarm and a crew's "
                "arrival at a fire was longer than in the year before."),
         why="crews took longer on average to reach fires after the second station opened",
         puzzle=("Ashenford opened a second station so that its crews would reach fires "
                 "sooner, yet they took longer on average to arrive"),
         resolve=[
             (("the new station was staffed by moving crews from the old one, which left "
               "each station with fewer engines than before"),
              ("with fewer engines at each station, a crew is more often already out when "
               "an alarm comes in")),
             (("in the same year, the town began timing a call from when the alarm was "
               "raised rather than from when an engine left"),
              ("the new timing adds the minutes before an engine leaves, so the average "
               "grows even if crews are no slower")),
             (("most of the town's new houses that year were built on its western edge, "
               "far from both stations"),
              "more alarms came from places far from either station"),
             (("for most of the year, roadworks closed the main bridge between the two "
               "halves of the town"),
              "crews had to take longer routes to reach many fires"),
         ],
         deepen=[
             (("the number of fires in Ashenford fell that year, so crews were out on "
               "calls less often than in any year before"),
              ("means crews were less often busy, which makes the slower arrivals harder "
               "to explain")),
             (("most of the fires in Ashenford over the past ten years have broken out on "
               "its east side, within a short drive of the new station"),
              ("means the new station is close to where fires happen, which deepens the "
               "puzzle")),
         ],
         aside=[
             ("the new station was built of brick from a works just outside the town",
              ("concerns what the station is built of, which has no bearing on how quickly "
               "crews arrive")),
             (("the fire service's open day drew a record crowd that year, with queues to "
               "climb aboard the new engines"),
              ("concerns the open day, which says nothing about how quickly crews reach "
               "fires")),
         ],
         half=[
             ("a second station puts an engine closer to more of the town",
              "explains why the station was expected to help, not why arrivals got slower"),
             (("the town built the station after residents of its east side complained "
               "about slow arrivals"),
              "explains why the station was built, not why arrivals got slower afterwards"),
         ]),
    dict(key="foxisland",
         setup=("To protect the ground nesting birds of Skerra Island, a conservation "
                "group removed every fox from the island before one spring's nesting "
                "season. That summer, fewer chicks fledged on the island than in any year "
                "on record."),
         why="fewer chicks fledged on the island after the foxes were removed",
         puzzle=("the foxes that eat the birds' eggs and chicks were removed, yet fewer "
                 "chicks fledged than in any year on record"),
         resolve=[
             (("the foxes had kept down the island's rats, which multiplied once the foxes "
               "were gone and ate many of the birds' eggs"),
              "a new predator took the foxes' place and took more eggs than the foxes had"),
             (("a storm in early summer flooded the low ground where most of the birds "
               "nest"),
              "the storm destroyed nests whatever happened to the foxes"),
             (("the fish the birds feed their chicks were scarce in the waters around the "
               "island that summer"),
              ("chicks starved for want of food, which removing the foxes could not "
               "prevent")),
             (("the teams that removed the foxes trampled and disturbed the nesting "
               "grounds in the weeks before the birds arrived"),
              "the removal itself damaged the nesting grounds, so fewer nests succeeded"),
         ],
         deepen=[
             (("on neighbouring islands, where foxes remain, more chicks fledged that "
               "summer than the year before"),
              ("suggests the year was a good one for the birds, which makes Skerra's fall "
               "harder to explain")),
             (("the last of the foxes was removed weeks before the first birds arrived to "
               "nest, and no fox has been seen on the island since"),
              "means the removal was finished in good time, which deepens the puzzle"),
         ],
         aside=[
             ("Skerra Island can be reached only by boat",
              "concerns how the island is reached, which has no bearing on the birds"),
             (("the fox removal was paid for by a charity based on the mainland, which has "
               "funded work on the island for years"),
              "concerns how the work was paid for, which says nothing about the chicks"),
         ],
         half=[
             ("foxes eat the eggs and chicks of birds that nest on the ground",
              ("explains why removing the foxes was expected to help, not why fewer chicks "
               "fledged")),
             (("the group removed the foxes so that more of the birds' chicks would "
               "survive"),
              "states the aim of the removal, which leaves the fall unexplained"),
         ]),
    dict(key="bookshopweb",
         setup=("The Thistlecombe Street bookshop began taking orders on a website, "
                "expecting that customers who ordered online would stop visiting the shop. "
                "In the year after the website was launched, sales at the shop's own "
                "counter rose."),
         why="sales at the shop's counter rose after it began selling online",
         puzzle=("the bookshop expected its website to draw customers away from the shop, "
                 "yet sales at its counter rose"),
         resolve=[
             (("customers who ordered on the website collected their books at the shop, "
               "and many bought more while they were there"),
              ("online orders brought people into the shop, where they bought more at the "
               "counter")),
             (("in the year the website was launched, the only other bookshop in the town "
               "closed"),
              "the closed shop's customers began buying at Thistlecombe Street"),
             (("the website listed the author readings the shop holds each month, and "
               "attendance at the readings doubled"),
              "the website drew more people to the shop's events, where they bought books"),
             (("in the same year, a school near the shop began buying its pupils' books at "
               "the shop's counter"),
              "a large new buyer more than made up for any customers who moved online"),
         ],
         deepen=[
             (("the shop's website offers every book at a lower price than its counter "
               "does, and most of its orders come from people in the town"),
              ("gives local customers a reason to buy online instead, which makes the rise "
               "at the counter harder to explain")),
             ("the shop cut its opening hours when the website was launched",
              ("means fewer hours in which to sell at the counter, which deepens the "
               "puzzle")),
         ],
         aside=[
             ("the website was designed by the owner's nephew",
              ("concerns who built the website, which has no bearing on sales at the "
               "counter")),
             (("the shop has sold books on Thistlecombe Street for more than forty years, "
               "under three different owners"),
              "concerns the shop's history, which says nothing about the rise in sales"),
         ],
         half=[
             ("a customer who buys online has less reason to visit a shop",
              "explains why the shop expected fewer visits, not why counter sales rose"),
             ("the shop launched the website to reach readers who live outside the town",
              "explains why the website was launched, not why sales at the counter rose"),
         ]),
    dict(key="waterprice",
         setup=("To persuade households to use less water during a drought, the city of "
                "Corvale raised the price of water by a third. Over the following summer, "
                "the city's daily water use rose."),
         why="the city's daily water use rose after it raised the price of water",
         puzzle="Corvale raised the price of water to cut its use, yet daily use rose",
         resolve=[
             ("the following summer was the hottest the city had recorded",
              "hot weather raised the need for water by more than the price rise cut it"),
             (("in the same months, a large new housing estate was connected to the city's "
               "supply"),
              "thousands of new users added to the total, whatever each household did"),
             (("a burst main leaked water for most of the summer, and the city counts all "
               "water that leaves its works as water used"),
              ("the leaked water was counted as use, so the total rose without households "
               "using more")),
             (("that summer a factory that had drawn water from its own well switched to "
               "the city's supply"),
              "a large new user added to the city's total"),
         ],
         deepen=[
             (("the city ran a campaign all summer urging households to save water, and "
               "most households said they had seen it"),
              ("gave households a further reason to save water, which makes the rise "
               "harder to explain")),
             (("most households cut their use once their first higher bill arrived, and "
               "many fitted water saving taps and showers"),
              "suggests households responded to the price, which deepens the puzzle"),
         ],
         aside=[
             ("the city's water comes from two reservoirs in the hills",
              ("concerns where the water comes from, which has no bearing on how much was "
               "used")),
             (("the price rise was approved by the city council in a close vote after a "
               "long debate about its effect on poorer households"),
              "concerns the council's vote, which says nothing about water use"),
         ],
         half=[
             ("people tend to use less of something when it costs more",
              "explains why the price rise was expected to work, not why use rose"),
             (("the city raised the price because its reservoirs were low after a dry "
               "winter"),
              "explains why the price was raised, not why use rose afterwards"),
         ]),
    dict(key="roadbends",
         setup=("To make the Fellmoor road safer, the county straightened its sharpest "
                "bends and resurfaced it. In the year after the work was finished, there "
                "were more crashes on the road than in any earlier year."),
         why=("there were more crashes on the road after it was straightened and "
              "resurfaced"),
         puzzle=("the county straightened and resurfaced the road to make it safer, yet "
                 "crashes on it rose"),
         resolve=[
             (("drivers on the straightened road drove much faster than they had on the "
               "old bends"),
              ("higher speeds bring more crashes, which can outweigh the gain from "
               "removing the bends")),
             (("the improved road became a shortcut, and far more vehicles used it than "
               "before"),
              "more traffic means more crashes even if each journey is safer"),
             (("the new surface had no painted lines or reflective studs for most of the "
               "year"),
              "drivers had nothing to guide them, especially at night"),
             ("the work was finished just before the wettest winter in decades",
              "the weather made every road more dangerous that year"),
         ],
         deepen=[
             (("the county put up new warning signs before each of the bends that remain "
               "on the road"),
              ("made the road safer still, which makes the rise in crashes harder to "
               "explain")),
             (("most crashes on the road before the work had happened on the bends that "
               "were straightened"),
              ("means the work removed the places where crashes happened, which deepens "
               "the puzzle")),
         ],
         aside=[
             ("the new surface was laid with stone from a quarry in the valley",
              ("concerns where the stone came from, which has no bearing on the number of "
               "crashes")),
             (("the road is maintained by the county rather than by the towns it links, "
               "which pay nothing toward it"),
              "concerns who looks after the road, which says nothing about the crashes"),
         ],
         half=[
             ("a straight road gives drivers a clearer view of what lies ahead",
              "explains why the work was expected to help, not why crashes rose"),
             ("the county carried out the work after a string of crashes on the bends",
              "explains why the work was done, not why crashes rose afterwards"),
         ]),
    dict(key="fertilizer",
         setup=("Farmers in the Amberlow Valley began using a new fertilizer that had "
                "raised wheat yields in trials elsewhere. In the first year they used it, "
                "the valley's total wheat harvest fell."),
         why=("the valley's wheat harvest fell in the first year the farmers used the "
              "fertilizer"),
         puzzle=("the farmers adopted a fertilizer that had raised yields elsewhere, yet "
                 "the valley's harvest fell"),
         resolve=[
             ("the valley had its driest spring in thirty years that year",
              "drought cut the harvest by more than the fertilizer could add"),
             (("many of the valley's farmers sowed part of their land with barley instead "
               "of wheat that year"),
              ("less land was sown with wheat, so the total fell even if each field "
               "yielded more")),
             ("a fungus new to the valley spread through its wheat fields that summer",
              "disease destroyed part of the crop whatever the fertilizer did"),
             (("on acid soils like the valley's, the new fertilizer locks up a nutrient "
               "that wheat needs"),
              "in the valley's soil the fertilizer harmed the crop instead of helping it"),
         ],
         deepen=[
             ("the same fertilizer raised wheat yields in a neighbouring valley that year",
              ("suggests the fertilizer works in the region, which makes the fall harder "
               "to explain")),
             (("the valley's farmers used the fertilizer exactly as its maker advised, at "
               "the rate and time the trials had used"),
              "rules out misuse, which deepens the puzzle"),
         ],
         aside=[
             ("the new fertilizer is made at a plant overseas",
              "concerns where the fertilizer is made, which has no bearing on the harvest"),
             (("most of the valley's farms are run by families who have farmed there for "
               "generations"),
              "concerns who runs the farms, which says nothing about the harvest"),
         ],
         half=[
             ("fertilizer supplies nutrients that wheat needs in order to grow",
              "explains why the fertilizer was expected to help, not why the harvest fell"),
             ("the farmers adopted the fertilizer after reading the results of the trials",
              "explains why the farmers adopted it, not why the harvest fell"),
         ]),
    dict(key="recycling",
         setup=("The town of Eskby began collecting recycling every week instead of every "
                "two weeks, expecting to send less rubbish to landfill. In the following "
                "year, the weight of rubbish the town sent to landfill rose."),
         why=("Eskby sent more rubbish to landfill after it began collecting recycling "
              "every week"),
         puzzle=("Eskby collected recycling more often in order to send less rubbish to "
                 "landfill, yet it sent more"),
         resolve=[
             (("a large new housing estate in the town was finished and filled with "
               "families that year"),
              "more households make more rubbish, whatever share of it is recycled"),
             (("the weekly collections began rejecting recycling bins that held the wrong "
               "materials, and their contents went to landfill"),
              "rubbish that had been counted as recycling now goes to landfill"),
             (("to pay for the weekly collections, the town ended its garden waste "
               "service, so garden waste now goes in rubbish bins"),
              "garden waste that used to be composted now goes to landfill"),
             (("a flood that winter left hundreds of homes throwing out ruined carpets and "
               "furniture"),
              "a mass of flood waste went to landfill that year"),
         ],
         deepen=[
             (("residents put out a greater weight of recycling than ever before, much of "
               "it paper and glass"),
              ("means more material was kept out of landfill, which makes the rise harder "
               "to explain")),
             (("residents told a survey that they found weekly recycling easier to keep up "
               "with than the old collections, and that they recycled more"),
              "suggests residents recycled more, which deepens the puzzle"),
         ],
         aside=[
             ("the town's recycling lorries run on electricity",
              ("concerns what the lorries run on, which has no bearing on the landfill "
               "total")),
             (("Eskby's recycling is sorted at a plant in a neighbouring county that "
               "serves several other towns as well"),
              ("concerns where the recycling is sorted, which says nothing about the "
               "landfill total")),
         ],
         half=[
             ("collecting recycling more often makes it easier for residents to recycle",
              "explains why the change was expected to help, not why landfill rose"),
             (("the town made the change after a survey found residents' recycling bins "
               "were often full"),
              "explains why the change was made, not why landfill rose afterwards"),
         ]),
    dict(key="freemuseum",
         setup=("The Calvering Museum stopped charging for admission in order to draw more "
                "visitors. In the following year, fewer people visited the museum than in "
                "the year before."),
         why="fewer people visited the museum after it stopped charging for admission",
         puzzle=("the museum dropped its admission charge to draw more visitors, yet it "
                 "had fewer"),
         resolve=[
             ("the museum closed its largest gallery for repairs for most of that year",
              ("with much of its collection out of view, the museum had less to draw "
               "visitors")),
             (("a travelling exhibition that had drawn crowds the year before ended in the "
               "month entry became free"),
              "the year before had been swollen by the exhibition's visitors"),
             (("to make up for the lost ticket income, the museum opened on four days a "
               "week instead of six"),
              "fewer opening days left fewer chances to visit"),
             (("the museum had counted visitors by tickets sold, and since entry became "
               "free it counts only those who sign its visitor book"),
              ("many visitors no longer appear in the count, so the fall may be in the "
               "counting and not in the visits")),
         ],
         deepen=[
             (("the museum advertised its free entry on buses and in newspapers across the "
               "region"),
              ("means many people knew about the change, which makes the fall harder to "
               "explain")),
             (("the region had more tourists that year than in any year before, many of "
               "them staying in the town where the museum stands"),
              "means more people who might have visited, which deepens the puzzle"),
         ],
         aside=[
             ("the museum's building is more than a century old",
              ("concerns the building's age, which has no bearing on the number of "
               "visitors")),
             (("the museum's shop sells prints of the paintings in its collection, as well "
               "as books about the town's history"),
              "concerns the museum's shop, which says nothing about the visitors"),
         ],
         half=[
             ("people are more likely to visit a place that costs nothing to enter",
              "explains why free entry was expected to draw visitors, not why visits fell"),
             (("the museum stopped charging after a review found its prices kept families "
               "away"),
              "explains why the charge was dropped, not why visits fell afterwards"),
         ]),
    dict(key="insulation",
         setup=("The Fernlow housing association insulated the walls of all its houses so "
                "that tenants would need less gas to heat them. In the following winter, "
                "the average household in those houses used more gas than in the winter "
                "before."),
         why="the households used more gas after their walls were insulated",
         puzzle=("the walls were insulated so that tenants would need less gas, yet they "
                 "used more"),
         resolve=[
             ("the following winter was the coldest in the region for twenty years",
              "the cold raised the need for heat by more than the insulation saved"),
             (("at the same time, the association replaced the houses' single gas fires "
               "with central heating that warms every room"),
              "tenants now heat every room instead of one, which uses more gas"),
             (("before the work, many tenants had left most rooms unheated to save money, "
               "and with the walls insulated they began heating them"),
              "tenants spent the saving on heating more rooms, so their total use rose"),
             (("in the same year, the association moved larger families into many of the "
               "insulated houses"),
              "larger households use more heat and hot water whatever the walls are like"),
         ],
         deepen=[
             (("the price of gas rose sharply that winter, and the tenants were told of "
               "the rise before the cold weather began"),
              "would push tenants to use less gas, which makes the rise harder to explain"),
             (("inspections found the insulation had been fitted to the standard the "
               "association set, with no gaps left in any wall"),
              "rules out poor work, which deepens the puzzle"),
         ],
         aside=[
             (("the insulation was fitted by a firm from another town, which finished the "
               "work ahead of time and under budget"),
              "concerns who fitted it, which has no bearing on how much gas was used"),
             ("the association owns houses in several villages as well as in Fernlow",
              ("concerns the association's other houses, which says nothing about this "
               "rise")),
         ],
         half=[
             ("insulated walls let less heat escape from a house",
              "explains why the insulation was expected to cut gas use, not why use rose"),
             (("the association insulated the houses after tenants complained of high "
               "heating bills"),
              "explains why the work was done, not why gas use rose afterwards"),
         ]),
    dict(key="jobcourse",
         setup=("Ormley's job training course was designed to help unemployed people find "
                "work sooner. Yet among the town's unemployed, those who completed the "
                "course took longer, on average, to find work than those who did not take "
                "it."),
         why=("people who completed the course took longer to find work than those who did "
              "not"),
         puzzle=("the course was meant to help people find work sooner, yet those who "
                 "completed it took longer to find work"),
         resolve=[
             (("places on the course went first to the people who had been out of work "
               "longest"),
              ("those who took the course were the hardest to place to begin with, so "
               "their slower progress need not be the course's doing")),
             (("the course lasts three months, and people on it could not look for work "
               "until they finished"),
              "the months on the course are counted in the time it took them to find work"),
             (("people whose skills employers were seeking usually found jobs before a "
               "place on the course came up"),
              ("the quickest to find work never took the course, which leaves the slower "
               "ones in it")),
             (("people who completed the course often turned down jobs in their old line "
               "of work to wait for jobs in the new trade"),
              ("the course's graduates chose to wait for better jobs, which lengthened "
               "their search")),
         ],
         deepen=[
             (("employers in Ormley said they would rather hire people who had completed "
               "the course than people with the same experience who had not"),
              ("means the course should have helped its graduates, which makes their "
               "slower progress harder to explain")),
             (("the people who took the course had, on average, more years of schooling "
               "than those who did not"),
              ("suggests the course's graduates were better placed to find work, which "
               "deepens the puzzle")),
         ],
         aside=[
             (("the course was taught in the town's old library building, which the "
               "council had recently restored"),
              ("concerns where the course was taught, which has no bearing on how quickly "
               "its graduates found work")),
             ("the course's teachers were paid by the hour",
              ("concerns how the teachers were paid, which says nothing about the "
               "graduates' search for work")),
         ],
         half=[
             ("training gives job seekers skills that employers want",
              ("explains why the course was expected to help, not why its graduates took "
               "longer")),
             (("the town set up the course after local firms said they could not find "
               "trained workers"),
              "explains why the course was set up, not why its graduates took longer"),
         ]),
    dict(key="toadtunnel",
         setup=("To stop toads being killed on the Brindlow road as they cross it each "
                "spring to reach their breeding pond, a tunnel was built under the road. "
                "The following spring, more toads were found dead on the road than in any "
                "earlier year."),
         why="more toads were found dead on the road after the tunnel was built",
         puzzle=("a tunnel was built so that toads could cross under the road, yet more "
                 "were found dead on it"),
         resolve=[
             (("volunteers who had carried toads across the road by hand every spring "
               "stopped doing so once the tunnel opened"),
              ("the toads the volunteers used to save now cross on their own, and many are "
               "killed")),
             (("traffic on the road doubled that year after a housing estate opened beyond "
               "it"),
              "twice the traffic kills more of the toads that still cross over the road"),
             (("the fences meant to steer the toads into the tunnel were not finished "
               "until after the spring"),
              "most toads never found the tunnel and crossed the road as before"),
             (("that spring dead toads were counted every morning, not once a week as "
               "before, when birds had taken many of the bodies"),
              ("daily counts find bodies that weekly counts missed, so the count rises "
               "without more toads dying")),
         ],
         deepen=[
             (("counters inside the tunnel recorded thousands of toads passing through it "
               "that spring, far more than were found dead on the road"),
              ("means many toads used the tunnel, which makes the rise in deaths harder to "
               "explain")),
             (("a count made in the woods beside the road before the crossing began found "
               "fewer toads there than in earlier springs"),
              "means fewer toads were waiting to cross, which deepens the puzzle"),
         ],
         aside=[
             ("the tunnel was paid for with money raised by a local school",
              "concerns how the tunnel was paid for, which has no bearing on the deaths"),
             (("the Brindlow road is named after a family that once owned the land around "
               "it, including the toads' pond"),
              "concerns the road's name, which says nothing about the toads"),
         ],
         half=[
             ("toads that pass through the tunnel never cross the road's surface",
              "explains why the tunnel was expected to help, not why deaths rose"),
             (("the tunnel was built after residents complained about the toads killed "
               "each spring"),
              "explains why the tunnel was built, not why deaths rose afterwards"),
         ]),
    dict(key="shopcameras",
         setup=("To reduce theft, the Market Square supermarket installed security cameras "
                "throughout the store. In the year after the cameras were installed, the "
                "value of the goods the store recorded as stolen was higher than in any "
                "earlier year."),
         why="the store recorded more theft after it installed security cameras",
         puzzle=("the store installed cameras to reduce theft, yet it recorded more goods "
                 "as stolen"),
         resolve=[
             (("the cameras let staff see thefts they had never noticed before, and the "
               "store records every theft its staff see"),
              "more thefts are seen and recorded, even if fewer happen"),
             (("that year a gang began stealing from shops across the town, taking goods "
               "in large amounts"),
              "a new source of theft added to the store's losses whatever the cameras did"),
             (("in the same year, the store began opening through the night with a single "
               "member of staff on the floor"),
              "the night hours gave thieves long spells with almost no one to stop them"),
             (("the store began counting its stock every week instead of once a year, and "
               "it records any missing goods as stolen"),
              "losses that once went unnoticed are now counted as theft"),
         ],
         deepen=[
             (("in the same year, the store moved the goods most often stolen, such as "
               "razor blades and spirits, behind its counters"),
              ("puts the most tempting goods out of thieves' reach, which makes the rise "
               "harder to explain")),
             (("the store stopped counting damaged goods as stolen that year, as it had "
               "done in earlier years"),
              ("removes goods that used to be counted as stolen, which makes the rise "
               "harder to explain")),
         ],
         aside=[
             ("the cameras were bought from a supplier in another country",
              "concerns where the cameras came from, which has no bearing on the thefts"),
             (("the supermarket's car park was resurfaced in the same year, and its "
               "entrance was moved to a side street"),
              "concerns the car park, which says nothing about the thefts in the store"),
         ],
         half=[
             ("people are less likely to steal where a camera may record them",
              ("explains why the cameras were expected to help, not why recorded theft "
               "rose")),
             (("the store installed the cameras after its losses from theft rose the year "
               "before"),
              ("explains why the cameras were installed, not why recorded theft rose "
               "afterwards")),
         ]),
    dict(key="bakerywages",
         setup=("The Hollybrook bakery chain raised the wages of all its staff by a tenth, "
                "although wages are its largest cost. In the following year, the chain's "
                "profits rose."),
         why="the chain's profits rose after it raised its staff's wages",
         puzzle=("the chain raised its largest cost, its staff's wages, yet its profits "
                 "rose"),
         resolve=[
             (("after the rise, far fewer staff left the chain, which saved much of what "
               "it had spent hiring and training replacements"),
              "the savings on hiring and training outweighed the cost of the higher wages"),
             ("in the same year, the price of the flour the chain uses fell by a quarter",
              "cheaper flour cut the chain's costs by more than the wage rise added"),
             ("the chain raised the prices of its bread and cakes at the same time",
              "higher prices brought in more than the wage rise cost"),
             ("a rival chain with shops on the same streets closed that year",
              "the rival's customers brought the chain more sales"),
         ],
         deepen=[
             (("the chain's rent and energy bills also rose that year, by more than the "
               "rise in wages"),
              ("adds to the chain's costs, which makes the rise in profits harder to "
               "explain")),
             (("the wage rise was paid to every member of staff, not only to the bakers, "
               "and it was paid from the first day of the year"),
              ("means the rise covered everyone for the whole year, which makes the rise "
               "in profits harder to explain")),
         ],
         aside=[
             ("the chain's shops are all painted the same shade of green",
              "concerns the shops' colour, which has no bearing on profits"),
             (("the chain was founded by two brothers who still run it from an office "
               "above its first shop"),
              "concerns who runs the chain, which says nothing about its profits"),
         ],
         half=[
             ("a business's profits fall when its costs rise and its income does not",
              "is why the rise in profits is surprising, so it leaves it unexplained"),
             ("the chain raised wages after its staff asked for a rise",
              "explains why wages were raised, not why profits rose"),
         ]),
    dict(key="lakealgae",
         setup=("To reduce the algae blooms on Lake Kestermere, the town's sewage works "
                "was upgraded so that the water it releases into the lake carries far less "
                "phosphorus, a nutrient algae need. In the following summer, blooms on the "
                "lake were more frequent than ever."),
         why="algae blooms became more frequent after the sewage works was upgraded",
         puzzle=("less phosphorus reached the lake from the sewage works, yet algae blooms "
                 "became more frequent"),
         resolve=[
             (("farms around the lake began spreading more fertilizer that year, and rain "
               "washes it into the lake"),
              "a new source of nutrients replaced what the works no longer released"),
             (("the following summer was the warmest on record, and algae grow fastest in "
               "warm water"),
              "warm water let algae bloom more often despite the lower phosphorus"),
             (("phosphorus that had built up in the lake bed over decades began to be "
               "released into the water that year"),
              "the lake had a store of phosphorus of its own, which fed the blooms"),
             (("a weir below the lake was raised that year, so water stays in the lake far "
               "longer than it did"),
              "still water that lingers in the lake gives algae more time to grow"),
         ],
         deepen=[
             (("the upgraded works removed even more phosphorus than its designers had "
               "promised, according to tests made every week"),
              ("means the works did better than planned, which makes the blooms harder to "
               "explain")),
             (("the town's population, and so the sewage it sends to the works, did not "
               "grow that year"),
              "rules out more sewage reaching the works, which deepens the puzzle"),
         ],
         aside=[
             (("the upgraded works was designed by engineers from the capital and took two "
               "years to build"),
              "concerns who designed the works, which has no bearing on the blooms"),
             (("Lake Kestermere is popular with sailors in the summer and with anglers "
               "through the rest of the year"),
              "concerns the sailors, which says nothing about the algae"),
         ],
         half=[
             ("algae cannot grow in water that carries no phosphorus",
              ("explains why the upgrade was expected to help, not why blooms became more "
               "frequent")),
             ("the works was upgraded after blooms closed the lake to swimmers",
              "explains why the upgrade was made, not why blooms became more frequent"),
         ]),
    dict(key="stadium",
         setup=("Because its old ground was often full, the Calderby Rovers football club "
                "moved to a stadium that holds twice as many people. In its first season "
                "at the new stadium, the club's average attendance was lower than in its "
                "last season at the old ground."),
         why="average attendance fell after the club moved to a larger stadium",
         puzzle=("the club moved to a larger stadium because its old ground was often "
                 "full, yet its average attendance fell"),
         resolve=[
             (("the new stadium lies outside the town, far from the bus and train routes "
               "that served the old ground"),
              "many fans could no longer reach matches easily"),
             ("to pay for the move, the club raised its ticket prices by half",
              "dearer tickets kept many fans away"),
             (("the club was relegated to a lower league at the end of its last season at "
               "the old ground"),
              "matches against weaker teams in a lower league draw smaller crowds"),
             (("the club stopped giving free tickets to local schools when it moved, and "
               "those tickets had been counted in its attendance"),
              "the old attendance figures included free tickets that the new ones do not"),
         ],
         deepen=[
             (("the population of the town grew in the year the club moved, and more of "
               "its people said they followed the club"),
              "means more people who might attend, which makes the fall harder to explain"),
             (("the club won more matches in its first season at the new stadium than in "
               "any season before"),
              "means the team was doing well, which deepens the puzzle"),
         ],
         aside=[
             (("the new stadium's pitch is laid with artificial grass, which the club says "
               "needs little upkeep"),
              "concerns the pitch, which has no bearing on attendance"),
             ("the club's colours have been red and white since it was founded",
              "concerns the club's colours, which say nothing about attendance"),
         ],
         half=[
             ("a larger stadium can hold more spectators",
              "explains why the move was expected to raise attendance, not why it fell"),
             ("fans had often been turned away from the old ground on match days",
              "explains why the club moved, not why attendance fell afterwards"),
         ]),
    dict(key="freebus",
         setup=("To encourage older people to travel, the Tavenmouth bus company made its "
                "buses free for pensioners. In the following year, pensioners made fewer "
                "journeys on the company's buses than in the year before."),
         why="pensioners made fewer bus journeys after the buses became free for them",
         puzzle=("the buses were made free for pensioners to encourage them to travel, yet "
                 "pensioners made fewer journeys"),
         resolve=[
             ("to pay for the free travel, the company cut a third of its routes",
              "many pensioners lost the buses they used, so they travelled less"),
             (("free travel applies only after half past nine in the morning, and most "
               "pensioners' journeys had been earlier"),
              ("many pensioners' usual journeys were not covered, and some stopped making "
               "them")),
             (("the town's hospital, where many pensioners had travelled for appointments, "
               "moved that year to a site no bus serves"),
              "a common reason for pensioners to take the bus disappeared"),
             (("journeys used to be counted from the tickets sold, and the free passes are "
               "often not scanned when pensioners board"),
              "many journeys are no longer counted, so the fall may be in the counting"),
         ],
         deepen=[
             (("the number of pensioners living in Tavenmouth rose that year, and more of "
               "them than before had no car of their own"),
              ("means more pensioners who could travel, which makes the fall harder to "
               "explain")),
             (("pensioners surveyed before the change said the fare was their main reason "
               "for not taking the bus more often than they did"),
              "suggests free fares should have drawn them, which deepens the puzzle"),
         ],
         aside=[
             (("the company's buses are painted in its blue and cream livery, which it has "
               "used for more than fifty years"),
              "concerns the buses' colours, which have no bearing on the journeys"),
             ("the company also runs coach trips to the coast in summer",
              "concerns the coach trips, which say nothing about bus journeys"),
         ],
         half=[
             ("people use a service more when it costs them nothing",
              "explains why free travel was expected to help, not why journeys fell"),
             ("the company made travel free after a campaign by pensioners' groups",
              "explains why travel was made free, not why journeys fell"),
         ]),
    dict(key="spamfilter",
         setup=("To save its staff time, the Pelsworth accounting office installed a "
                "filter that blocks junk email. In the following month, the office's staff "
                "said they spent more time dealing with email than before."),
         why="the staff spent more time on email after the junk filter was installed",
         puzzle=("the filter was installed to save the staff time, yet they spent more "
                 "time on email"),
         resolve=[
             (("the filter also blocked many genuine messages from clients, which staff "
               "had to look for and release by hand"),
              "searching for wrongly blocked messages took longer than deleting junk had"),
             (("in the same month, the office took on several large new clients, who send "
               "it many messages each day"),
              "more genuine email took up more time, whatever the filter saved"),
             (("the filter holds any message it is unsure about until a member of staff "
               "approves it"),
              "approving held messages became a new daily task"),
             (("staff were asked to report every junk message the filter missed by filling "
               "in a form"),
              "the reports take more time than the missed junk itself"),
         ],
         deepen=[
             (("the filter blocked almost every junk message the office received, "
               "according to the supplier's monthly report"),
              ("means the filter worked as intended, which makes the extra time harder to "
               "explain")),
             ("staff said the filter was simple to use and took no time at all to learn",
              "rules out time lost learning the filter, which deepens the puzzle"),
         ],
         aside=[
             (("the filter was chosen by the office manager after a trial of three "
               "different products"),
              "concerns who chose the filter, which has no bearing on time spent on email"),
             ("the office moved to larger premises the following year",
              "concerns the office's move, which says nothing about time spent on email"),
         ],
         half=[
             ("reading and deleting junk email takes up staff time",
              "explains why the filter was expected to save time, not why it did not"),
             (("the office installed the filter after staff complained about the junk they "
               "received"),
              "explains why the filter was installed, not why email took more time"),
         ]),
    dict(key="tomatovariety",
         setup=("In trials, a new tomato variety bore more fruit per plant than the "
                "variety it was bred to replace. Yet farms in the Haldmoor region that "
                "switched to the new variety harvested fewer tomatoes per field than "
                "before."),
         why="farms that switched to the new variety harvested fewer tomatoes per field",
         puzzle=("the new variety bore more fruit per plant in trials, yet farms that "
                 "switched to it harvested less per field"),
         resolve=[
             (("the new variety's plants are larger and must be planted further apart, so "
               "fewer of them fit in a field"),
              ("more fruit per plant can still mean less fruit per field when there are "
               "fewer plants")),
             (("the new variety is prone to a blight that is common in the Haldmoor region "
               "but was absent where the trials were held"),
              "disease cut the farms' harvests in a way the trials could not show"),
             (("the trials were grown in heated greenhouses, and the Haldmoor farms grow "
               "their tomatoes outdoors"),
              "the trial results do not carry over to fields in the open"),
             (("the new variety needs more water than the farms' irrigation could supply "
               "that year"),
              "plants short of water bear less fruit"),
         ],
         deepen=[
             (("the weather in the Haldmoor region was good for tomatoes that year, as "
               "warm and sunny as in any recent summer"),
              "rules out a bad season, which makes the smaller harvests harder to explain"),
             (("the farms that switched gave the new variety more fertilizer than they had "
               "given the old one, as the breeder had advised"),
              "means the new plants were well fed, which deepens the puzzle"),
         ],
         aside=[
             ("the new variety's fruit is a deeper red than the old variety's",
              ("concerns the fruit's colour, which has no bearing on how much was "
               "harvested")),
             (("the company that bred the new variety has bred tomatoes for forty years "
               "and sells its seed in many countries"),
              "concerns the breeder's history, which says nothing about the harvests"),
         ],
         half=[
             ("a plant that bears more fruit should yield more per field",
              "is why the smaller harvests are surprising, so it leaves them unexplained"),
             ("the farms switched to the new variety because of its results in the trials",
              "explains why the farms switched, not why their harvests fell"),
         ]),
    dict(key="shelterfee",
         setup=("The Hilbury animal shelter stopped charging a fee to adopt an animal. Its "
                "staff had feared that people who paid nothing would be quicker to give "
                "animals back, but in the following year, fewer adopted animals were "
                "returned to the shelter than in the year before."),
         why=("fewer adopted animals were returned after the shelter stopped charging a "
              "fee"),
         puzzle=("the staff feared that free adoptions would lead to more returns, yet "
                 "fewer animals were returned"),
         resolve=[
             (("at the same time, the shelter began visiting every applicant's home before "
               "agreeing to an adoption"),
              "the visits screened out unsuitable homes, so fewer animals came back"),
             (("the shelter began giving every new owner free training classes for the "
               "animal they adopted"),
              "owners who learn to handle their animals are less likely to give them up"),
             ("the shelter began charging owners a fee to return an animal",
              "a fee for returns discourages owners from bringing animals back"),
             (("most returns had been made by tenants whose landlords did not allow pets, "
               "and the shelter began asking for a landlord's consent"),
              "the most common cause of returns was screened out before adoption"),
         ],
         deepen=[
             (("far more animals were adopted in the year after the fee was dropped than "
               "in the year before"),
              ("means more animals in new homes that could be returned, which makes the "
               "fall harder to explain")),
             (("the shelter took in more animals with behaviour problems that year than "
               "ever before, many of them from homes where they had been neglected"),
              ("means more animals that new owners might find hard to keep, which deepens "
               "the puzzle")),
         ],
         aside=[
             ("the shelter is run by a charity founded by a local vet",
              "concerns who runs the shelter, which has no bearing on returns"),
             (("the shelter keeps its cats and dogs in separate buildings, each with its "
               "own outdoor run"),
              "concerns how the animals are housed, which says nothing about returns"),
         ],
         half=[
             ("people who pay nothing for something may value it less",
              "explains why the staff feared more returns, not why returns fell"),
             ("the shelter dropped the fee to find homes for more of its animals",
              "explains why the fee was dropped, not why returns fell"),
         ]),
    dict(key="seawall",
         setup=("To stop its beach from washing away, the town of Wenby built a sea wall "
                "along the back of the beach. In the years since the wall was built, the "
                "beach in front of it has narrowed faster than it did before."),
         why="the beach has narrowed faster since the sea wall was built",
         puzzle=("the sea wall was built to stop the beach washing away, yet the beach has "
                 "narrowed faster since"),
         resolve=[
             (("waves that strike the wall bounce back and carry sand from the beach out "
               "to sea"),
              "the wall itself drives the loss of sand"),
             (("the beach was once fed by sand from the cliffs behind it, which the wall "
               "now keeps from reaching the beach"),
              "the wall cut off the beach's supply of new sand"),
             (("a harbour built along the coast in the same years traps the sand that "
               "currents used to carry to Wenby"),
              "less sand reaches the beach from elsewhere"),
             (("storms have struck the coast more often in the years since the wall was "
               "built"),
              "more storms strip more sand, whatever the wall does"),
         ],
         deepen=[
             (("the wall was built to the height and strength its engineers recommended, "
               "and no storm has damaged it"),
              "rules out poor building, which makes the faster loss harder to explain"),
             (("before the wall, most of the beach's sand was lost when storm waves washed "
               "over it into the town"),
              "means the wall blocks what used to take the sand, which deepens the puzzle"),
         ],
         aside=[
             (("the wall was built of granite from a quarry inland, carried to the town by "
               "rail"),
              "concerns the stone used, which has no bearing on the beach"),
             ("the town's promenade runs along the top of the wall",
              "concerns the promenade, which says nothing about the beach"),
         ],
         half=[
             ("a sea wall stops waves from reaching the land behind it",
              ("explains why the wall was expected to help, not why the beach narrowed "
               "faster")),
             (("the town built the wall after a storm washed away part of the old "
               "promenade"),
              "explains why the wall was built, not why the beach narrowed faster"),
         ]),
    dict(key="openplan",
         setup=("The Gantry design firm moved its staff out of private offices and into "
                "one large open room, so that they would talk with one another more. In "
                "the following months, staff held fewer face-to-face conversations than "
                "before."),
         why="staff held fewer face-to-face conversations after moving into the open room",
         puzzle=("the firm moved its staff into one open room so that they would talk "
                 "more, yet they held fewer face-to-face conversations"),
         resolve=[
             ("in the open room, most staff wore headphones to shut out the noise",
              ("staff who cannot hear one another, or who signal that they want quiet, "
               "talk less")),
             (("the move came with a new messaging app that staff used to reach colleagues "
               "across the room"),
              "conversations moved from speech to messages"),
             (("knowing that they could be overheard, staff took their conversations to "
               "email"),
              "the lack of privacy pushed talk out of the room"),
             (("at the same time, the firm began letting staff work from home two days a "
               "week"),
              "fewer staff were in the room on any day to talk with"),
         ],
         deepen=[
             (("staff in the open room sit closer to their colleagues than they did in "
               "their offices"),
              ("means colleagues are nearer to talk to, which makes the fall harder to "
               "explain")),
             (("the firm hired more staff in the months after the move, and all of them "
               "sit in the open room"),
              "means more people to talk with, which deepens the puzzle"),
         ],
         aside=[
             ("the open room has large windows overlooking a park beside the river",
              "concerns the view, which has no bearing on conversations"),
             ("the firm designs packaging for food companies",
              "concerns the firm's work, which says nothing about conversations"),
         ],
         half=[
             ("people who can see one another find it easier to start a conversation",
              "explains why the move was expected to help, not why conversations fell"),
             (("the firm made the move after staff said they rarely spoke to colleagues in "
               "other teams"),
              "explains why the move was made, not why conversations fell"),
         ]),
    dict(key="honeyprice",
         setup=("This year the beekeepers of Rothmere produced more honey than in any year "
                "on record. Yet the price they received for their honey was higher than "
                "last year's."),
         why="the price of Rothmere honey rose in a year of record production",
         puzzle=("Rothmere's beekeepers produced a record amount of honey, which would be "
                 "expected to lower its price, yet the price rose"),
         resolve=[
             (("the honey harvest failed this year in the other regions that supply the "
               "same buyers"),
              "the buyers' total supply fell even though Rothmere produced more"),
             ("a large buyer in another country began importing Rothmere honey this year",
              "new demand from abroad absorbed the extra honey and more"),
             (("a widely reported study this year linked honey to good health, and demand "
               "rose sharply"),
              "demand rose by more than the supply did"),
             (("the government stopped imports of the cheap foreign honey that had "
               "competed with Rothmere's this year"),
              "Rothmere's honey no longer had to match the prices of cheaper imports"),
         ],
         deepen=[
             (("the beekeepers' costs fell this year, so they could afford to sell at a "
               "lower price"),
              ("gives the beekeepers room to cut their price, which makes the rise harder "
               "to explain")),
             ("shops across Rothmere lowered the shelf price of honey this year",
              "suggests honey was cheaper this year, which deepens the puzzle"),
         ],
         aside=[
             ("Rothmere's beekeepers keep a native breed of bee that is calmer than most",
              "concerns the breed of bee, which has no bearing on the price"),
             (("Rothmere's honey is sold in glass jars with the region's name printed on "
               "the label"),
              "concerns how the honey is packed, which says nothing about its price"),
         ],
         half=[
             ("a larger supply of a product usually lowers its price",
              "is why the higher price is surprising, so it leaves it unexplained"),
             ("the record harvest followed an unusually mild spring",
              "explains the record harvest, not the higher price"),
         ]),
    dict(key="millmachines",
         setup=("The Hendry mill installed machines that do the work its spinners once did "
                "by hand. A year later, the mill employed more people than it did before "
                "the machines arrived."),
         why=("the mill employed more people after installing machines that do its "
              "spinners' work"),
         puzzle=("the mill installed machines to do its spinners' work, yet it employed "
                 "more people afterwards"),
         resolve=[
             (("the machines spin yarn so cheaply that the mill took on large new orders "
               "and hired more weavers to fill them"),
              ("cheaper yarn brought more business, which needed more workers in other "
               "jobs")),
             ("the machines need a team of technicians to run and repair them",
              "the machines created new jobs in place of some of the old ones"),
             ("the mill added a night shift once the machines were installed",
              "a second shift needs a second set of workers"),
             ("that year the mill took over the customers of a rival mill that had closed",
              "more customers meant more work for the mill's staff"),
         ],
         deepen=[
             ("the mill paid off all of its spinners when the machines arrived",
              ("means the mill shed its spinners, which makes the rise in staff harder to "
               "explain")),
             (("the mill's spinners had been its largest group of workers, more than half "
               "of everyone it employed"),
              ("means the machines replaced most of the mill's jobs, which deepens the "
               "puzzle")),
         ],
         aside=[
             ("the machines were shipped to the mill from abroad",
              ("concerns where the machines came from, which has no bearing on the mill's "
               "staff")),
             ("the mill stands beside a canal that once carried its goods to the coast",
              "concerns the canal, which says nothing about the mill's staff"),
         ],
         half=[
             ("a machine that does a worker's job reduces the need for that worker",
              "explains why fewer staff were expected, not why there were more"),
             ("the mill bought the machines because its spinners' wages had risen",
              "explains why the machines were bought, not why the staff grew"),
         ]),
    dict(key="hotelrenovate",
         setup=("The Silverbirch Hotel renovated all of its rooms in the hope of improving "
                "its guests' ratings on a travel website. In the year after the "
                "renovation, its average guest rating was lower than in the year before."),
         why="the hotel's average rating fell after it renovated its rooms",
         puzzle=("the hotel renovated its rooms to improve its ratings, yet its average "
                 "rating fell"),
         resolve=[
             (("after the renovation, the hotel raised its room prices by a third, and "
               "guests rate a hotel against what they paid"),
              "guests expected more for their money and rated their stays lower"),
             (("building work on a new wing continued beside the guest rooms for the whole "
               "year"),
              "noise from the work spoiled stays whatever the rooms were like"),
             (("the hotel began asking every guest for a rating, where before only guests "
               "who chose to visit the website left one"),
              ("the ratings now come from a different mix of guests, so the average can "
               "change without stays getting worse")),
             (("in the same year, the hotel was taken over by a chain that cut its staff "
               "by a third"),
              "poorer service lowered the ratings despite the better rooms"),
         ],
         deepen=[
             (("guests' written comments often praised the new rooms, their furniture and "
               "their bathrooms"),
              ("suggests guests liked the change, which makes the lower ratings harder to "
               "explain")),
             (("before the renovation, guests' most common complaint by far was the worn "
               "state of the rooms, and that complaint has since disappeared"),
              "means the renovation fixed what guests disliked, which deepens the puzzle"),
         ],
         aside=[
             (("the renovation was designed by a firm from the capital that has worked on "
               "many of the region's older hotels"),
              "concerns who designed the rooms, which has no bearing on the ratings"),
             ("the hotel has a hundred rooms on four floors",
              "concerns the hotel's size, which says nothing about its ratings"),
         ],
         half=[
             ("guests rate new rooms more highly than worn ones",
              "explains why the renovation was expected to help, not why ratings fell"),
             ("the hotel renovated its rooms because its ratings had been falling",
              "explains why the work was done, not why ratings fell afterwards"),
         ]),
    dict(key="patrols",
         setup=("To make the town centre safer, the Arnmouth police doubled the number of "
                "officers patrolling it on foot. In the following year, more crimes were "
                "reported in the town centre than in the year before."),
         why=("more crimes were reported in the town centre after the foot patrols were "
              "doubled"),
         puzzle=("the police doubled the foot patrols to make the town centre safer, yet "
                 "more crimes were reported there"),
         resolve=[
             (("officers on foot see and report crimes that would otherwise never have "
               "been reported"),
              "more crimes are recorded even if fewer are committed"),
             (("in the same year, the police opened a desk in the town centre where people "
               "could report crimes in person"),
              "it became easier to report crimes, so more were reported"),
             (("that year a new nightclub opened in the town centre and drew large crowds "
               "late at night"),
              "larger crowds late at night brought more crime whatever the patrols did"),
             (("the town centre held a month-long festival that year that drew record "
               "crowds"),
              "more people in the centre meant more crime"),
         ],
         deepen=[
             (("the police stopped counting minor offences such as littering in their "
               "crime figures that year"),
              ("removes offences that used to be counted, which makes the rise harder to "
               "explain")),
             (("the number of people living in the town centre fell that year, as several "
               "blocks of flats were turned into offices"),
              "means fewer residents to commit or suffer crimes, which deepens the puzzle"),
         ],
         aside=[
             (("the officers on patrol were issued new uniforms that year, the first "
               "change in a decade"),
              "concerns the uniforms, which have no bearing on the crimes reported"),
             ("many of the town centre's streets are cobbled",
              "concerns the streets, which say nothing about crime"),
         ],
         half=[
             (("people are less likely to commit a crime where they can see a police "
               "officer"),
              ("explains why the patrols were expected to help, not why reported crime "
               "rose")),
             (("the police added the patrols after a rise in complaints about the town "
               "centre"),
              "explains why the patrols were added, not why reported crime rose"),
         ]),
]


def said(text):
    """A statement as an answer choice."""
    return upfirst(text) + "."


def scene_index(key):
    return next(i for i, s in enumerate(SCENES) if s["key"] == key)


def pick(i, salt, n):
    """A choice fixed by the scenario and what it is for, so a rebuild makes the same one."""
    return zlib.crc32(("%s|%s" % (SCENES[i]["key"], salt)).encode()) % n


def wrongs_of(s):
    """Every wrong answer to the resolve question, as (choice, reason) pairs."""
    return [(said(t), why) for kind in KINDS for t, why in s[kind]]


def resolutions(s):
    """The four resolutions, as the EXCEPT question offers them, with the reason each is
    wrong there: it does help."""
    return [(said(t), "does help to resolve the discrepancy: if it is true, " + how)
            for t, how in s["resolve"]]


def except_keys(s):
    """The answers the EXCEPT question can be keyed to: those that plainly do not help."""
    return [(said(t), why) for kind in ("deepen", "aside") for t, why in s[kind]]


def rank_of(right, others):
    """How many of the other options are shorter than the key: balance()'s rank."""
    return sum(1 for o in others if len(o) < len(right))


class ByScene(ListsQuestions):
    """One question of each kind per scenario, so the runner knows when it has made them all
    (INC-0126)."""

    def units(self):
        return [(i, None) for i in range(len(SCENES))]


def emit_lr(gen, rng, choices_n, stem, right, wrongs, expl, target):
    """CRBase.emit with a fixed key rank, as the reading schemas asked once per passage do
    (INC-0122)."""
    opts = [right] + [w for w, _ in balance(rng, right, wrongs, choices_n - 1, target=target)]
    if len(set(opts)) != choices_n:
        raise ItemError("%s could not build %d distinct options" % (gen.id, choices_n))
    why = dict(wrongs)
    rng.shuffle(opts)
    first = next(o for o in opts if o != right)
    item = {
        "id": None, "section": "LR", "type": "LR", "sub": gen.sub, "skill": gen.skill,
        "diff": gen.diff, "stem": stem, "choices": opts, "answer": opts.index(right),
        "expl": expl, "gen": gen.id, "domain": "nonmath",
        "wrong": "Choice " + "ABCDE"[opts.index(first)] + " " + why[first] + ".",
        "canon_ignores_choices": True,
    }
    check_clause_splice(gen.id, [stem] + opts + [expl], [])
    gen.verify(item, right, choices_n, fmt=str)
    return item


class Resolve(ByScene, CRBase):
    """Which choice most helps to resolve the discrepancy."""
    id = "lsat_expl_resolve"
    skill = "lsat_lr_expl"
    section = "LR"
    type = "LR"
    sub = "Resolve the discrepancy"
    diff = 3

    def assigned(self, need):
        """{scenario key: (index into resolve, rank)}. A resolution carries a mechanism and
        runs longer than most wrong answers, so a key fixed in advance is too often the
        longest option. Each scenario offers the ranks any of its four resolutions can take,
        the ranks are spread across scenarios, and each scenario then uses the first
        resolution that reaches its rank (INC-0122)."""
        cache = self.__dict__.setdefault("_assigned", {})
        if need not in cache:
            can, by_rank = [], {}
            for s in SCENES:
                ranks = {}
                for j, (text, _) in enumerate(s["resolve"]):
                    for r in buildable_ranks(said(text), wrongs_of(s), need):
                        ranks.setdefault(r, j)
                by_rank[s["key"]] = ranks
                can.append((s["key"], sorted(ranks)))
            ranks = assign_ranks(can, need)
            cache[need] = {k: (by_rank[k][r], r) for k, r in ranks.items()}
        return cache[need]

    def asks(self, i):
        s = SCENES[i]
        stem = STEM_RESOLVE if pick(i, "stem", 2) == 0 else STEM_EXPLAIN % s["why"]
        return [(s["setup"] + "\n\n" + stem, None)]

    def make(self, rng, choices_n):
        i = rng.randrange(len(SCENES))
        s = SCENES[i]
        (stem, _), = self.asks(i)
        k, rank = self.assigned(choices_n - 1)[s["key"]]
        text, how = s["resolve"][k]
        # The answer is quoted as a clause of its own: many open with a phrase of their own
        # ("to pay for the move, ..."), which reads badly spliced after "If".
        expl = ("The discrepancy is that %s. The correct answer says that %s. If that is true, "
                "%s, and the two facts no longer conflict. Each wrong answer makes the outcome "
                "harder to explain, has no bearing on it, or explains something else, such as "
                "why the change was made or why it was expected to work."
                % (s["puzzle"], text, how))
        return emit_lr(self, rng, choices_n, stem, said(text), wrongs_of(s), expl, rank)


class ExceptOne(ByScene, CRBase):
    """Which choice, alone of the five, does not help to resolve the discrepancy."""
    id = "lsat_expl_except"
    skill = "lsat_lr_expl"
    section = "LR"
    type = "LR"
    sub = "Resolve the discrepancy (EXCEPT)"
    diff = 4

    def assigned(self, need):
        """{scenario key: index into except_keys()}: the key each scenario uses, chosen so
        the keys' length ranks among the four resolutions spread evenly (INC-0122)."""
        cache = self.__dict__.setdefault("_assigned", {})
        if need not in cache:
            can, by_rank = [], {}
            for i, s in enumerate(SCENES):
                others = [c for c, _ in resolutions(s)]
                ranks = {}
                for j, (c, _) in enumerate(except_keys(s)):
                    ranks.setdefault(rank_of(c, others), j)
                by_rank[s["key"]] = ranks
                can.append((s["key"], sorted(ranks)))
            ranks = assign_ranks(can, need)
            cache[need] = {k: by_rank[k][r] for k, r in ranks.items()}
        return cache[need]

    def asks(self, i):
        return [(SCENES[i]["setup"] + "\n\n" + STEM_EXCEPT, None)]

    def make(self, rng, choices_n):
        i = rng.randrange(len(SCENES))
        s = SCENES[i]
        (stem, _), = self.asks(i)
        if choices_n - 1 != len(s["resolve"]):
            raise ItemError("%s needs %d resolutions for %d choices" % (self.id, choices_n - 1,
                                                                          choices_n))
        right, why = except_keys(s)[self.assigned(choices_n - 1)[s["key"]]]
        expl = ("The discrepancy is that %s. Four of the choices would each let both facts "
                "hold. The answer is the one that does not: it %s." % (s["puzzle"], why))
        return emit_lr(self, rng, choices_n, stem, right, resolutions(s), expl,
                       rank_of(right, [c for c, _ in resolutions(s)]))


GENS = [Resolve(), ExceptOne()]


def check_scenes():
    """Every scenario is complete, its statements are written to stand alone as answer
    choices, and nothing repeats. A statement may open with a name (Skerra Island, Lake
    Tarrow), so capitals are left to upfirst(); pronouns are not, because a choice is read
    on its own."""
    bad = []
    seen = {}
    counts = {"resolve": 4, "deepen": 2, "aside": 2, "half": 2}
    for i, s in enumerate(SCENES):
        name = s.get("key") or str(i)
        for f in ("key", "setup", "why", "puzzle"):
            if not s.get(f):
                bad.append("%s is missing %s" % (name, f))
        for kind, n in counts.items():
            if len(s.get(kind) or []) != n:
                bad.append("%s has %d %s statements, not %d" % (name, len(s.get(kind) or []),
                                                                 kind, n))
        if not s.get("setup", "").endswith("."):
            bad.append("%s: the setup has no full stop" % name)
        texts = [s.get(f) or "" for f in ("setup", "why", "puzzle")]
        for kind in counts:
            for text, note in s.get(kind) or []:
                texts += [text, note]
                if text.endswith(".") or note.endswith("."):
                    bad.append("%s: %r ends with a full stop" % (name, text[:40]))
                if text.split()[0] in ("it", "its", "they", "their", "them", "this", "these"):
                    bad.append("%s: %r opens with a pronoun" % (name, text[:40]))
                words = len(text.split())
                if not 6 <= words <= 30:
                    bad.append("%s: %r has %d words" % (name, text[:40], words))
                if text in seen:
                    bad.append("%s repeats a statement of %s: %r" % (name, seen[text], text[:40]))
                seen[text] = name
        for text in texts:
            if "\u2014" in text or "\u2013" in text:
                bad.append("%s: a dash in %r" % (name, text[:40]))
    return bad
