# Writes the story scripts (scripts/NN-slug.json) for TikToks 02-45.
# Each scene: on-screen lines (*word* = highlight, ~ = small line) + "say" (voiceover).
import json, pathlib

NIGHT = "radial-gradient(120% 80% at 50% 20%,#1F2A44,#05070D)"
GREEN = "linear-gradient(160deg,#064E3B,#0B1220)"
TEAL = "linear-gradient(160deg,#0B3B4A,#0B1220)"
DEEP = "linear-gradient(160deg,#065F46,#022C22)"
BLACK = "#05070D"
PLUM = "linear-gradient(160deg,#3B1F4A,#0B1220)"
COLORS = [GREEN, TEAL, PLUM]

def T(lines, say, **kw):
    d = {"lines": lines, "say": say}; d.update(kw); return d

def L(kicker, items, say, **kw):
    d = {"type": "list", "kicker": kicker, "items": items, "say": say, "itemStart": kw.pop("start", 1.6), "itemStep": kw.pop("step", 2.2)}; d.update(kw); return d

def CTA(q, sub, say_q):
    return {"type": "cta", "color": DEEP, "lines": [q, "~" + sub], "bio": "Free guide → just search it",
            "say": say_q + " Read the free guide at viva voltia dot com."}

V = []  # (slug, article, scenes)
def add(slug, article, scenes):
    for i, sc in enumerate(scenes):
        if "bg" not in sc and "color" not in sc:
            sc["color"] = COLORS[i % len(COLORS)] if i else NIGHT
    V.append((slug, article, scenes))

add("are-solar-panels-worth-it", "are-solar-panels-worth-it", [
    T(["Your neighbor just got *solar panels.*"], "Picture this. Your neighbor just got solar panels.", kicker="Picture this…"),
    T(["Now the salesperson is *at your door.*"], "And now the same salesperson is knocking on your door."),
    T(["The big question:", "*Is solar still worth it in 2026?*"], "The big question. Is solar still worth it in twenty twenty-six?"),
    T(["The *30% federal credit* ended.", "~For systems installed after 2025."], "Here's what changed. The thirty percent federal tax credit ended for systems installed after twenty twenty-five."),
    L("Solar is usually worth it if:", ["You pay *above-average* power rates", "You have a *sunny* roof", "You'll stay *10+ years*"], "Solar is usually still worth it if: you pay above-average electricity rates. You have a sunny roof. And you plan to stay ten years or more.", bg="panels-sun.jpg"),
    T(["Typical payback now:", "*9 to 14 years.*"], "Typical payback is now about nine to fourteen years. In high-rate states, it can still be under ten."),
    CTA("Is it worth it *for you?*", "The 5 factors that decide it", "Want to know if it's worth it for you?"),
])
add("how-many-solar-panels-do-i-need", "how-many-solar-panels-do-i-need", [
    T(["Two installers.", "*Two very different* panel counts."], "Imagine this. Two installers quote your house, with two very different panel counts.", kicker="Imagine this…"),
    T(["Who's right?"], "So who's right?"),
    T(["Your *electric bill* already knows."], "The answer is already on your electric bill."),
    T(["Average US home:", "*10,800 kWh* a year."], "The average US home uses about ten thousand eight hundred kilowatt-hours a year."),
    T(["That's about *17–25 panels.*", "~400–450 W each"], "That works out to roughly seventeen to twenty-five panels of four hundred to four hundred fifty watts."),
    T(["Sunshine changes it by *30%+*"], "But your local sunshine changes the answer by thirty percent or more. The same home needs fewer panels in Arizona than in Washington."),
    CTA("How many do *you* need?", "Our simple 4-step sizing guide", "Want to size your own system?"),
])
add("solar-battery-cost", "solar-battery-cost", [
    T(["A salesperson quotes you", "*$20,000* for a home battery."], "Imagine a salesperson quotes you twenty thousand dollars for a home battery.", kicker="Imagine this…"),
    T(["Is that a *fair price?*"], "Is that a fair price?"),
    T(["Most 10–15 kWh batteries:", "*$10,000–$16,000* installed."], "In twenty twenty-six, a typical ten to fifteen kilowatt-hour battery costs about ten to sixteen thousand dollars installed.", bg="battery-wall.jpg"),
    T(["That's about *$850–$1,300*", "per kWh of storage."], "That's roughly eight hundred fifty to thirteen hundred dollars per kilowatt-hour of usable storage."),
    T(["And *no federal credit*", "~for batteries bought in 2026"], "And purchased batteries installed in twenty twenty-six get no federal tax credit."),
    L("Batteries pay off fastest with:", ["*Net billing*", "*Time-of-use* rates", "Frequent *outages*"], "Batteries pay off fastest under net billing, with time-of-use rates, or when backup power really matters to you."),
    CTA("What should *you* pay?", "2026 battery prices by size and brand", "Want to check your battery quote?"),
])
add("what-is-net-metering", "what-is-net-metering", [
    T(["Your solar panels make", "*more power* than you use."], "Picture a sunny afternoon. Your solar panels make more power than your home is using.", kicker="Picture this…"),
    T(["Where does the *extra* go?"], "So where does the extra go?"),
    T(["It flows *back to the grid.*"], "It flows back to the grid."),
    T(["With *net metering*, you get", "a credit for every kWh."], "With net metering, you get a bill credit for every kilowatt-hour, at or near the retail rate."),
    T(["The grid works like", "a *free battery.*"], "It's like using the grid as a free battery."),
    T(["But many states now use", "*net billing* — and pay less."], "But a growing number of states use net billing, which pays much less for exports. That's why self-use and batteries matter more now."),
    CTA("What does *your* state do?", "Net metering explained simply", "Want to know how your state credits solar?"),
])
add("best-solar-panels-for-homes", "best-solar-panels-for-homes", [
    T(["Premium panels.", "*Premium price.*"], "Picture this. An installer pitches premium panels, at a premium price.", kicker="Picture this…"),
    T(["Do you *really* need them?"], "Do you really need them?"),
    T(["Most quality panels are", "*20–23% efficient.*"], "Most quality home panels in twenty twenty-six are twenty to twenty-three percent efficient.", bg="panels-sun.jpg"),
    T(["The gap is *smaller*", "than marketing suggests."], "The gap between good and premium is smaller than the marketing suggests."),
    T(["Premium mainly pays off on", "*small or tricky roofs.*"], "Premium panels mainly pay off on small or complicated roofs."),
    T(["Look for a *25-year*", "product + performance warranty."], "For most homes, a reputable mid-range panel with a twenty-five year warranty is the best value."),
    CTA("Which brand fits *your* roof?", "Top panel brands compared", "Want to compare the top brands?"),
])
add("how-to-compare-solar-quotes", "how-to-compare-solar-quotes", [
    T(["Three solar quotes.", "*Thousands* of dollars apart."], "Imagine this. You get three solar quotes for the same house, and they're thousands of dollars apart.", kicker="Imagine this…"),
    T(["Which one is the *real deal?*"], "Which one is the real deal?"),
    T(["Ignore the *monthly payment.*"], "First, ignore the monthly payment."),
    T(["Compare *price per watt.*", "~Total price ÷ system watts"], "Compare price per watt. That's the total price divided by the system size in watts."),
    L("Then check:", ["A realistic *production estimate*", "A *10+ year* workmanship warranty", "No *pressure tactics*"], "Then check for a realistic production estimate, a workmanship warranty of at least ten years, and no pressure tactics."),
    T(["Red flag: a 2026 quote that", "promises the *30% federal credit.*"], "And a big red flag: any twenty twenty-six quote that still promises the thirty percent federal tax credit."),
    CTA("Got quotes on the table?", "Our 10-point checklist", "Comparing quotes right now?"),
])
add("is-solar-worth-it-california", "is-solar-worth-it-california", [
    T(["California has *30¢*", "electricity."], "Imagine this. You live in California, where power costs about thirty cents a kilowatt-hour.", kicker="Imagine this…"),
    T(["Solar should be a *no-brainer*…", "~right?"], "Solar should be a no-brainer, right?"),
    T(["Then came *NEM 3.0.*"], "Then came NEM three point oh."),
    T(["Exported solar now earns about", "*a quarter* of retail."], "Under NEM three, exported solar earns roughly a quarter of the retail rate on average."),
    T(["Solar-only payback:", "*about 9 years.*", "~instead of 5"], "So solar-only systems now pay back in about nine years, instead of five."),
    T(["Add a *battery*, and you roughly", "*double* the solar you use."], "Adding a battery roughly doubles how much of your own solar you use, and usually increases twenty-five year savings.", bg="battery-wall.jpg"),
    CTA("Solar alone or with a battery?", "Real 2026 California payback math", "Not sure which is right for you?"),
])
add("solar-panels-cloudy-rain-snow", "solar-panels-cloudy-rain-snow", [
    T(["It's a *cloudy, rainy* week."], "Picture this. It's a cloudy, rainy week.", kicker="Picture this…"),
    T(["Are your solar panels", "*doing anything?*"], "Are your solar panels doing anything at all?"),
    T(["Yes. Panels make about", "*10–25%* of normal output."], "Yes. On cloudy days, panels still make about ten to twenty-five percent of their clear-sky output."),
    T(["And *cold* actually helps.", "~Heat is what hurts output."], "And here's the surprise. Cold weather actually improves efficiency. Heat is what reduces output."),
    T(["Snow usually *slides off*", "within a day or two of sun."], "Snow usually slides off tilted panels within a day or two of sunshine. Don't climb on the roof to clear it."),
    T(["What matters is the *whole year.*"], "What really matters is annual production, and installers size systems using decades of local weather data.", bg="panels-sun.jpg"),
    CTA("Solar in *every season*", "Clouds, rain, snow and heat explained", "Curious how solar does where you live?"),
])
add("solar-lease-vs-buy", "solar-lease-vs-buy", [
    T(["*$0 down* solar.", "Sounds amazing."], "Picture this. A company offers you solar for zero dollars down. Sounds amazing.", kicker="Picture this…"),
    T(["But it's a *lease.*"], "But it's a lease."),
    T(["Is that a *good deal?*"], "Is that actually a good deal?"),
    T(["Buying with cash usually means", "the *biggest lifetime savings.*"], "Buying with cash usually delivers the highest lifetime savings."),
    T(["But in 2026, leasing companies", "still get a *federal credit.*", "~Homeowners don't."], "But in twenty twenty-six, leasing companies can still claim a federal business credit that homeowners can't. That's made leases more competitive."),
    L("Before you sign, check:", ["The yearly *price escalator*", "The *buyout* terms", "What happens if you *sell*"], "Before you sign a lease, check the yearly price escalator, the buyout terms, and what happens when you sell your home."),
    CTA("Lease, loan or cash?", "Which is the better deal in 2026", "Trying to decide how to pay?"),
])
add("is-solar-worth-it-texas", "is-solar-worth-it-texas", [
    T(["Texas has *huge sun.*"], "Imagine this. You live in Texas, with some of the best sun in the country.", kicker="Imagine this…"),
    T(["But there's *no statewide*", "net metering."], "But there's no statewide net metering."),
    T(["Your *electricity plan* decides", "what your solar is worth."], "In most of Texas, your retail electricity plan's solar buyback rate decides what your exported power is worth."),
    T(["Good buyback plan:", "*about 10 years* payback."], "With a plan that credits exports near retail, a typical system pays back in about ten years."),
    T(["Low buyback rate:", "*15+ years.*"], "With a low buyback rate, it can take fifteen years or more."),
    T(["Plus a *100% property tax*", "exemption on solar."], "The good news: there's a one hundred percent property tax exemption on solar, statewide."),
    CTA("Which plan fits *your* solar?", "Texas buyback plans explained", "Going solar in Texas?"),
])
add("solar-and-ev-charging", "solar-and-ev-charging", [
    T(["You just bought an", "*electric car.*"], "Imagine this. You just bought an electric car.", kicker="Imagine this…"),
    T(["What if the *sun* fueled it?"], "What if the sun could fuel it?"),
    T(["12,000 miles a year uses about", "*3,000–4,500 kWh.*"], "Driving about twelve thousand miles a year in a typical EV uses roughly three thousand to forty-five hundred kilowatt-hours."),
    T(["That's about *6–9 extra panels.*"], "That usually takes about six to nine extra solar panels, depending on your sunshine."),
    T(["With net metering, you can", "charge at *night* and still", "run on solar."], "With net metering, you can even charge at night and still run on solar, through bill credits."),
    T(["With net billing,", "*midday charging* matters more."], "Under net billing, charging at midday matters more."),
    CTA("Power your EV with sunshine", "How many panels you need", "Want to size solar for your EV?"),
])
add("tesla-powerwall-3-review", "tesla-powerwall-3-review", [
    T(["Everyone's talking about the", "*Tesla Powerwall 3.*"], "Picture this. You keep hearing about the Tesla Powerwall three.", kicker="Picture this…"),
    T(["Is it *worth it?*"], "But is it worth it?"),
    T(["*13.5 kWh* of storage.", "*11.5 kW* of power."], "It stores thirteen point five kilowatt-hours and delivers up to eleven point five kilowatts, enough to start most central air conditioners.", bg="battery-wall.jpg"),
    T(["Typical price:", "*$13,000–$16,500* installed."], "Typical installed price in twenty twenty-six is about thirteen to sixteen and a half thousand dollars."),
    T(["Its *built-in inverter* makes it", "great for *new* solar systems."], "Its built-in hybrid inverter makes it especially cost-effective for new solar-plus-storage installs."),
    T(["*10-year* warranty.", "~LFP battery chemistry"], "It uses lithium iron phosphate chemistry and has a ten year warranty."),
    CTA("Is it right for *your* home?", "Our honest Powerwall 3 review", "Thinking about a Powerwall?"),
])
add("federal-solar-tax-credit-guide", "federal-solar-tax-credit-guide", [
    T(["Your friend got *30% off*", "solar last year."], "Picture this. Your friend got thirty percent off their solar panels last year.", kicker="Picture this…"),
    T(["You want the *same deal.*"], "You want the same deal."),
    T(["But the *30% credit ended.*", "~Dec 31, 2025"], "But the thirty percent federal homeowner credit ended on December thirty-first, twenty twenty-five.", bg="tax-forms.jpg"),
    T(["Systems installed in 2026 get", "*no federal credit.*"], "Homeowner-owned systems placed in service after that get no federal tax credit."),
    T(["But *leasing companies* can still", "claim a business credit."], "Leasing companies can still claim a business credit, which can lower lease prices."),
    T(["State credits, rebates and", "*net metering* now matter most."], "State tax credits, rebates, property tax exemptions, and net metering are now the main incentives."),
    CTA("What's left for *you?*", "Your solar options in 2026", "Want to know what you can still get?"),
])
add("is-solar-worth-it-florida", "is-solar-worth-it-florida", [
    T(["The *Sunshine State.*"], "Imagine this. You live in the Sunshine State.", kicker="Imagine this…"),
    T(["Is solar actually", "*worth it* in Florida?"], "But is solar actually worth it in Florida?"),
    T(["FPL, Duke and TECO still credit", "solar at the *full retail rate.*"], "Here's the good news. FPL, Duke Energy Florida, and TECO still credit exported solar at the full retail rate."),
    T(["*No sales tax* on solar.", "*No property tax* on the added value."], "Solar is exempt from the six percent sales tax, and the added home value is exempt from property tax."),
    T(["Typical payback:", "*10 to 12 years.*"], "At Florida's average price, a typical system pays back in roughly ten to twelve years."),
    T(["Hurricanes? Plan your *roof*,", "*racking* and *backup.*"], "Just plan for hurricanes: a solid roof, wind-rated racking, and a backup plan."),
    CTA("Florida solar in 2026", "Payback math + hurricane tips", "Going solar in Florida?"),
])
add("cost-solar-panels-2000-sq-ft", "cost-solar-panels-2000-sq-ft", [
    T(["A *2,000 sq ft* home.", "How much is solar?"], "Picture a typical two thousand square foot home. How much does solar cost?", kicker="Picture this…", bg="house-cost.jpg"),
    T(["Most need *7–9 kW.*", "~About 17–22 panels"], "Most homes that size need seven to nine kilowatts of solar, or about seventeen to twenty-two panels."),
    T(["At *$2.60–$3.00* per watt…"], "At two sixty to three dollars per watt…"),
    T(["…that's *$19,000–$25,000.*", "~before incentives"], "That's roughly nineteen to twenty-five thousand dollars before incentives."),
    T(["*No federal credit* in 2026.", "~State incentives still help"], "There's no federal credit for homeowner purchases in twenty twenty-six, but state incentives can still cut the cost."),
    T(["Typical payback:", "*9 to 13 years.*"], "Typical payback is nine to thirteen years, faster where electricity is expensive."),
    CTA("What would *your* home cost?", "Full 2026 cost breakdown", "Want the full breakdown?"),
])
add("how-many-batteries-off-grid", "how-many-batteries-off-grid", [
    T(["You want to *go off-grid.*", "No more power bills."], "Imagine this. You want to go completely off-grid. No more power bills.", kicker="Imagine this…"),
    T(["How many batteries", "does that *really* take?"], "How many batteries does that really take?"),
    T(["Average home:", "*30 kWh a day.*"], "The average US home uses about thirty kilowatt-hours a day."),
    T(["For 2–3 cloudy days you'd need", "*60–90+ kWh* of storage."], "To get through two or three cloudy days, you'd need roughly sixty to ninety kilowatt-hours of storage, or more.", bg="battery-wall.jpg"),
    T(["That's *very expensive.*"], "That's very expensive."),
    T(["Most off-grid homes *cut usage*", "and add a *generator.*"], "Most off-grid homes cut their usage sharply and add a backup generator instead."),
    CTA("Off-grid or backup?", "Battery sizing made simple", "Dreaming of going off-grid?"),
])
add("is-solar-worth-it-new-york", "is-solar-worth-it-new-york", [
    T(["New York isn't known", "for *sunshine.*"], "Picture this. You live in New York. Not exactly famous for sunshine.", kicker="Picture this…"),
    T(["But solar pays back", "*faster* than in many sunny states."], "But solar here pays back faster than in many sunny states."),
    T(["Why? Power costs", "*28.6¢ per kWh.*"], "Why? New York power averages twenty-eight point six cents a kilowatt-hour."),
    T(["Plus a *25% state credit*", "up to *$5,000.*"], "Plus there's a twenty-five percent state tax credit, up to five thousand dollars."),
    T(["Net metering still credits", "exports at *retail.*"], "And residential net metering still credits exports at retail."),
    T(["Typical payback:", "*about 7 years.*"], "A typical system pays back in about seven years after the state credit."),
    CTA("New York solar in 2026", "The $5,000 credit + payback math", "Going solar in New York?"),
])
add("solar-incentives-by-state", "solar-incentives-by-state", [
    T(["The *federal* solar credit", "is gone."], "Picture this. The federal solar tax credit is gone.", kicker="Picture this…"),
    T(["Is there *any money left*", "for going solar?"], "Is there any money left for going solar?"),
    T(["Yes — about *a dozen states*", "have their own credits or rebates."], "Yes. About a dozen states offer their own solar tax credits or rebates."),
    T(["New York: *25%* up to *$5,000.*"], "New York's twenty-five percent credit, up to five thousand dollars, is one of the strongest."),
    T(["Some states *pay you* for", "the power you produce."], "In states like New Jersey, Massachusetts, and Illinois, programs pay you for the power you produce."),
    T(["And *tax exemptions* quietly", "save hundreds to thousands."], "And property and sales tax exemptions quietly save hundreds to thousands of dollars."),
    CTA("What does *your* state offer?", "Every state incentive, in one place", "Want to see your state's incentives?"),
])
add("do-solar-panels-increase-home-value", "do-solar-panels-increase-home-value", [
    T(["You're *selling* your home.", "It has solar panels."], "Imagine this. You're selling your home, and it has solar panels.", kicker="Imagine this…", bg="house-cost.jpg"),
    T(["Do buyers *pay more?*"], "Do buyers actually pay more?"),
    T(["Zillow found solar homes sold for", "about *4.1% more.*"], "A twenty nineteen Zillow analysis found homes with solar sold for about four point one percent more."),
    T(["Berkeley Lab: about *$4 per watt*", "of owned solar."], "Berkeley Lab research found buyers paid roughly four dollars per watt of owned solar."),
    T(["But *owned* systems add value.", "*Leased* ones can complicate a sale."], "But that's for owned systems. Leased systems can complicate a sale."),
    T(["Keep your *records* ready.", "~Production, warranties, permits"], "Tip: keep production records, warranties, and permits ready for appraisers and buyers."),
    CTA("How much could *yours* add?", "What the research says", "Thinking about resale value?"),
])
add("is-solar-worth-it-arizona", "is-solar-worth-it-arizona", [
    T(["Arizona has the", "*best sun* in the US."], "Imagine this. Arizona has the strongest sun in the country.", kicker="Imagine this…"),
    T(["So solar pays back *super fast*…", "~right?"], "So solar must pay back super fast, right?"),
    T(["Not quite. APS and TEP pay about", "*6¢* for exported solar."], "Not quite. APS and TEP pay only about six cents per kilowatt-hour for the solar you export."),
    T(["Typical payback:", "*12 to 14 years.*"], "So a typical system pays back in about twelve to fourteen years."),
    L("Make it pay faster:", ["Use more solar *at home*", "*West-facing* panels", "*Size* it right"], "To make it pay faster: use more of your solar at home, consider west-facing panels, and size the system carefully."),
    T(["Plus a *state credit*", "of 25% up to *$1,000.*"], "And the state credit, twenty-five percent up to a thousand dollars, still applies."),
    CTA("Arizona solar, sized right", "2026 payback under net billing", "Going solar in Arizona?"),
])
add("solar-with-or-without-battery", "solar-with-or-without-battery", [
    T(["Your solar quote has", "a *$12,000 battery* on it."], "Picture this. Your solar quote includes a twelve thousand dollar battery.", kicker="Picture this…"),
    T(["Do you *really* need it?"], "Do you really need it?"),
    T(["With *full net metering*:", "usually skip it."], "If your utility has full retail net metering, solar without a battery usually pays back fastest."),
    T(["With *net billing* or *time-of-use*:", "a battery can save a lot."], "Under net billing or time-of-use rates, a battery can add real savings by shifting solar to the evening.", bg="battery-wall.jpg"),
    T(["Frequent *outages?*", "Backup alone can justify it."], "And if outages are frequent or costly for you, backup value alone can justify one."),
    T(["Not sure? Go *battery-ready.*"], "Not sure yet? Choose battery-ready equipment and add storage later."),
    CTA("Battery or no battery?", "4 questions that decide it", "Still deciding?"),
])
add("how-long-do-solar-panels-last", "how-long-do-solar-panels-last", [
    T(["You spend *$20,000+*", "on solar panels."], "Imagine this. You spend over twenty thousand dollars on solar panels.", kicker="Imagine this…"),
    T(["How long until you", "*need new ones?*"], "How long until you need new ones?"),
    T(["Quality panels last", "*25–30+ years.*"], "Quality panels usually last twenty-five to thirty years or more.", bg="panels-sun.jpg"),
    T(["They lose about *0.5%* a year.", "~NREL research"], "NREL research puts typical degradation around half a percent a year."),
    T(["A 20-year-old panel still makes", "about *90%* of its power."], "So a twenty-year-old panel still makes about ninety percent of its original output."),
    T(["The part to budget for:", "a *string inverter.*", "~10–15 years"], "The part to budget for is the string inverter, which typically lasts ten to fifteen years."),
    CTA("Built to last", "Lifespan, warranties and degradation", "Want the full lifespan breakdown?"),
])
add("is-solar-worth-it-new-jersey", "is-solar-worth-it-new-jersey", [
    T(["New Jersey pays solar owners", "*twice.*"], "Here's something most people don't know. New Jersey pays solar owners twice.", kicker="Did you know?"),
    T(["*First:* full retail", "net metering."], "First, full retail net metering on your bill."),
    T(["*Second:* SREC-II payments", "for *15 years.*"], "Second, SREC-two payments: one certificate for every thousand kilowatt-hours you produce, for fifteen years."),
    T(["Power costs *24.6¢*", "~well above the US average"], "With power at twenty-four point six cents, well above average…"),
    T(["…typical payback is", "*about 7 years.*"], "A typical system pays back in about seven years. Among the fastest in the country."),
    T(["Plus *sales* and *property tax*", "exemptions."], "Plus sales tax and property tax exemptions."),
    CTA("New Jersey solar in 2026", "SREC-II explained simply", "Going solar in New Jersey?"),
])
add("solar-panel-orientation-and-tilt", "solar-panel-orientation-and-tilt", [
    T(["Your roof faces *east and west.*", "~No south side"], "Imagine this. Your roof faces east and west. No south side at all.", kicker="Imagine this…"),
    T(["Is solar *a waste?*"], "Is solar a waste?"),
    T(["South is best in the US…"], "In the US, south-facing panels produce the most energy over a year."),
    T(["…but east and west only lose", "about *10–20%.*"], "But east and west-facing panels typically produce only ten to twenty percent less. Usually still worthwhile."),
    T(["*West* panels can even be", "worth more."], "And west-facing panels can be worth even more under time-of-use rates and net billing, because they produce later in the day."),
    T(["Most roof pitches are", "*close enough* to perfect."], "Most roof pitches, from about fifteen to forty degrees, are close enough to optimal."),
    CTA("Is *your* roof good for solar?", "Direction and tilt explained", "Wondering about your roof?"),
])
add("enphase-iq-5p-vs-powerwall-3", "enphase-iq-5p-vs-powerwall-3", [
    T(["*Enphase* or *Tesla?*", "Which home battery wins?"], "Enphase or Tesla. Which home battery should you get?", kicker="Battery battle"),
    T(["*Powerwall 3:* one big", "13.5 kWh battery."], "One Powerwall three stores thirteen point five kilowatt-hours and delivers eleven point five kilowatts."),
    T(["*Enphase 5P:* 5 kWh blocks", "you can stack."], "One Enphase IQ Battery five P stores five kilowatt-hours. You stack them."),
    T(["Three 5Ps ≈ one Powerwall,", "usually for *more money.*"], "Three five Ps roughly match one Powerwall, usually at a higher total price."),
    T(["Enphase wins on *warranty:*", "*15 years* vs 10."], "Enphase wins on warranty: fifteen years versus ten, and fits Enphase systems perfectly."),
    T(["Powerwall wins for *new* systems.", "~Built-in solar inverter"], "Powerwall three is usually the better value for new solar plus storage, because its inverter is built in."),
    CTA("Which fits *your* home?", "Enphase vs Powerwall, compared", "Choosing a battery?"),
])
add("is-solar-worth-it-massachusetts", "is-solar-worth-it-massachusetts", [
    T(["Massachusetts power costs", "*30.5¢* per kWh."], "Imagine paying thirty point five cents a kilowatt-hour for electricity. That's Massachusetts.", kicker="Imagine this…"),
    T(["That's bad for bills…", "but *great for solar.*"], "That's bad for your bills. But great for solar."),
    T(["Full *retail* net metering.", "~Eversource, National Grid, Unitil"], "Eversource, National Grid, and Unitil credit exports at the full retail rate."),
    T(["SMART 3.0 pays *3¢ per kWh*", "for *20 years.*"], "The SMART three program pays three cents for every kilowatt-hour you produce, locked for twenty years."),
    T(["Plus a *15% state credit.*"], "Plus a fifteen percent state tax credit and tax exemptions."),
    T(["Typical payback:", "*6 to 7 years.*"], "Put together, a typical system pays back in about six to seven years."),
    CTA("Massachusetts solar math", "SMART 3.0 + net metering explained", "Going solar in Massachusetts?"),
])
add("do-solar-panels-need-maintenance", "do-solar-panels-need-maintenance", [
    T(["A company offers a *yearly*", "solar cleaning plan."], "Picture this. A company offers you a yearly solar panel cleaning plan.", kicker="Picture this…"),
    T(["Do you *need* it?"], "Do you actually need it?"),
    T(["Panels have *no moving parts.*"], "Solar panels have no moving parts, and need little routine maintenance."),
    T(["*Rain* usually keeps them", "clean enough."], "Rain usually keeps them clean enough."),
    T(["Cleaning helps most in", "*dusty areas* or after *pollen.*"], "Cleaning helps most in dry, dusty areas, or after heavy pollen or bird droppings."),
    T(["Best habit: check your", "*monitoring app* monthly."], "The best maintenance habit? Check your monitoring app once a month."),
    CTA("Solar care made easy", "Cleaning, monitoring and real costs", "Want the simple care guide?"),
])
add("is-solar-worth-it-north-carolina", "is-solar-worth-it-north-carolina", [
    T(["Duke Energy changed its", "*solar rules.*"], "If you live in North Carolina, Duke Energy changed its solar rules.", kicker="Heads up, North Carolina"),
    T(["New customers pick between", "*two rates.*"], "New Duke customers choose between two rates."),
    T(["The *Bridge Rate* —", "open until 2027."], "The Net Metering Bridge Rate, open until twenty twenty-seven."),
    T(["Or *Residential Solar Choice* —", "a time-of-use rate."], "Or Residential Solar Choice, a time-of-use rate."),
    T(["PowerPair: up to *$9,000*", "for solar + battery."], "And Duke's PowerPair program offers up to nine thousand dollars for new solar plus battery systems, while capacity lasts.", bg="battery-wall.jpg"),
    T(["Solar-only payback:", "*12 to 14 years.*"], "A solar-only system typically pays back in about twelve to fourteen years."),
    CTA("Which Duke rate fits you?", "PowerPair + payback math", "Going solar in North Carolina?"),
])
add("microinverters-vs-string-inverters", "microinverters-vs-string-inverters", [
    T(["Your installer asks:", "*micro or string inverter?*"], "Picture this. Your installer asks: microinverters or a string inverter?", kicker="Picture this…"),
    T(["You have *no idea.*"], "And you have no idea."),
    T(["*String inverters:* the cheapest.", "~Great for simple, sunny roofs"], "String inverters are the cheapest option, and work well on simple, unshaded roofs.", bg="inverter.jpg"),
    T(["*Microinverters:* one per panel.", "~Less shade loss + panel monitoring"], "Microinverters convert power at each panel. Less shade loss, and panel-level monitoring, at a higher price."),
    T(["*Optimizers:* the middle ground."], "Power optimizers with a string inverter are a middle ground."),
    T(["Shady roof?", "Go *panel-level.*"], "If your roof has shade, panel-level electronics are usually worth it."),
    CTA("Which inverter is right?", "Micro vs string vs optimizers", "Choosing an inverter?"),
])
add("home-solar-guide", "home-solar-guide", [
    T(["You've *never* looked", "into solar before."], "Imagine you've never looked into solar before.", kicker="Imagine this…"),
    T(["Where do you even *start?*"], "Where do you even start?"),
    T(["Typical home: *7–10 kW.*", "~About $19,000–$29,000"], "A typical US home needs a seven to ten kilowatt system, about nineteen to twenty-nine thousand dollars before incentives.", bg="panels-sun.jpg"),
    T(["The *30% federal credit* ended", "after 2025."], "The thirty percent federal homeowner credit ended after twenty twenty-five."),
    T(["Now your *power rate* and", "*state rules* decide the math."], "So now your electricity rate and your state's rules decide most of the math."),
    T(["Get *3 quotes.*", "~Compare price per watt"], "And get at least three quotes, comparing price per watt, equipment, and warranties."),
    CTA("New to solar? Start here", "The complete 2026 beginner's guide", "Just getting started?"),
])
add("is-solar-worth-it-illinois", "is-solar-worth-it-illinois", [
    T(["Illinois *cut* net metering", "in 2025."], "Imagine this. Illinois cut net metering for new solar customers in twenty twenty-five.", kicker="Imagine this…"),
    T(["Is solar *dead* there?"], "So is solar dead there?"),
    T(["No — thanks to", "*Illinois Shines.*"], "Not at all, thanks to Illinois Shines."),
    T(["It buys 15 years of credits —", "often *$7,000–$14,000.*"], "It buys fifteen years of your system's renewable energy credits, often worth seven to fourteen thousand dollars for a home."),
    T(["Plus a *$300 per kW* rebate", "~ComEd and Ameren"], "ComEd and Ameren also pay a three hundred dollar per kilowatt rebate."),
    T(["Payback with both:", "*8 to 10 years.*"], "With both, a typical system can pay back in about eight to ten years."),
    CTA("Illinois Shines explained", "Real 2026 payback numbers", "Going solar in Illinois?"),
])
add("can-hoa-stop-you-from-getting-solar", "can-hoa-stop-you-from-getting-solar", [
    T(["Your HOA says:", "*no solar panels.*"], "Picture this. You want solar, but your HOA says no.", kicker="Picture this…"),
    T(["Can they *really* stop you?"], "Can they really stop you?"),
    T(["There's *no federal* solar", "access law."], "There's no federal solar access law. It depends on your state."),
    T(["About *30 states* limit what", "HOAs can do."], "Roughly thirty states limit HOA restrictions on solar to some degree."),
    T(["Most allow only *reasonable* rules", "on placement and looks."], "Many allow only reasonable rules about placement and appearance."),
    T(["Tip: submit a *complete*,", "professional application."], "Even then, you'll usually need approval. A complete, professional application is the fastest way to a yes."),
    CTA("Know your solar rights", "HOA rules, state by state", "HOA giving you trouble?"),
])
add("is-solar-worth-it-pennsylvania", "is-solar-worth-it-pennsylvania", [
    T(["Pennsylvania power now costs", "*21.8¢* per kWh."], "If you live in Pennsylvania, your power now costs about twenty-one point eight cents a kilowatt-hour.", kicker="Pennsylvania"),
    T(["Is solar *worth it* yet?"], "So is solar worth it yet?"),
    T(["The state requires", "*1:1 net metering.*"], "Pennsylvania requires one-to-one net metering. Every exported kilowatt-hour is credited at retail."),
    T(["And *SRECs* can add", "extra income."], "And solar renewable energy credits can add extra income."),
    T(["Typical payback:", "*about 10 years.*"], "That's why a typical system pays back in about ten years."),
    T(["*PECO* vs *PPL?*", "~The details differ"], "The details differ between utilities like PECO and PPL."),
    CTA("Pennsylvania solar math", "Net metering, SRECs and payback", "Going solar in Pennsylvania?"),
])
add("portable-power-station-vs-home-battery", "portable-power-station-vs-home-battery", [
    T(["A storm is coming.", "You need *backup power.*"], "Picture this. A storm is coming, and you want backup power.", kicker="Picture this…"),
    T(["Power station or", "*home battery?*"], "Should you get a portable power station, or a home battery?"),
    T(["Power stations: *1–5 kWh.*", "~Fridge, lights, phones"], "Portable power stations hold about one to five kilowatt-hours. Perfect for a fridge, lights, and devices."),
    T(["Home batteries: *10–15+ kWh.*", "~Whole circuits, automatically"], "Home batteries hold ten to fifteen or more, and back up whole circuits automatically.", bg="battery-wall.jpg"),
    T(["Portable + panels: *under $3,000.*", "Home battery: *$10,000+.*"], "A portable unit with foldable panels can cost under three thousand dollars. An installed home battery usually costs ten thousand or more."),
    T(["Never *backfeed* your house", "without a transfer switch."], "Safety tip: never backfeed a portable unit into your house wiring without a proper transfer switch."),
    CTA("Which backup is right?", "Power station vs home battery", "Planning for outages?"),
])
add("solar-panels-on-metal-roof", "solar-panels-on-metal-roof", [
    T(["You have a *metal roof.*"], "Imagine you have a metal roof.", kicker="Imagine this…", bg="metal-roof.jpg"),
    T(["Can you even put", "*solar* on it?"], "Can you even put solar on it?"),
    T(["Yes — it's one of the", "*best roofs* for solar."], "Yes. It's one of the best roofs for solar."),
    T(["Metal roofs last *40–70 years.*", "~Longer than the panels"], "Metal roofs last forty to seventy years, longer than the panels themselves."),
    T(["Standing seam? *No drilling.*", "~Clamps grip the seams"], "On standing seam roofs, clamps grip the seams. No holes drilled through your roof."),
    T(["Install is often *faster*", "and can cost less."], "Installation is often quicker, and can cost less in labor."),
    CTA("Metal roof + solar", "Mounts, costs and what to check", "Got a metal roof?"),
])
add("nem-3-california-net-billing", "nem-3-california-net-billing", [
    T(["Your neighbor got solar", "*before April 2023.*"], "Picture this. Your neighbor in California got solar before April twenty twenty-three.", kicker="Picture this…"),
    T(["You got it *after.*"], "You got it after."),
    T(["Same panels.", "*Very different* bill credits."], "Same panels. Very different bill credits."),
    T(["That's *NEM 3.0.*", "~The Net Billing Tariff"], "That's NEM three, the net billing tariff, for new PG and E, SCE, and SDG and E customers."),
    T(["Exports earn *avoided cost* —", "far below retail."], "Exports now earn time-varying avoided-cost credits, usually far below retail."),
    T(["The fix: a *battery* that stores", "midday solar for the evening."], "What makes the numbers work? A battery that stores midday solar for evening use.", bg="battery-wall.jpg"),
    CTA("NEM 3.0 in plain English", "What changed + how to design for it", "On NEM three?"),
])
add("is-solar-worth-it-colorado", "is-solar-worth-it-colorado", [
    T(["Colorado: *high altitude*,", "*cool air*, strong sun."], "Picture Colorado. High altitude, cool air, and strong sun.", kicker="Picture this…"),
    T(["Perfect for solar panels."], "That's a great combo for solar panels."),
    T(["About *5.4 sun hours* a day.", "~Cool air boosts efficiency"], "Colorado gets about five point four peak sun hours a day, and cool air helps panels run efficiently.", bg="panels-sun.jpg"),
    T(["Xcel and Black Hills offer", "*net metering.*"], "Xcel Energy and Black Hills Energy offer net metering."),
    T(["Typical payback:", "*9 to 10 years.*"], "A typical system pays back in about nine to ten years."),
    T(["Just plan for *hail.*", "~Rated panels + good insurance"], "Just plan for hail: hail-rated panels and good insurance."),
    CTA("Colorado solar in 2026", "Payback math + hail protection", "Going solar in Colorado?"),
])
add("hybrid-vs-grid-tie-inverter", "hybrid-vs-grid-tie-inverter", [
    T(["You might want a *battery*", "in a few years."], "Imagine this. You're getting solar now, and you might want a battery in a few years.", kicker="Imagine this…"),
    T(["Your inverter choice", "*today* matters."], "Your inverter choice today really matters."),
    T(["*Grid-tie:* converts solar,", "shuts off in outages."], "A grid-tie inverter converts solar power, but shuts down in outages and can't manage a battery.", bg="inverter.jpg"),
    T(["*Hybrid:* handles solar", "*and* a battery."], "A hybrid inverter handles both solar and a battery, and can provide backup."),
    T(["Battery coming later?", "Go *hybrid* or *battery-ready.*"], "If a battery might come later, a hybrid inverter or battery-ready design can save money."),
    T(["Already have solar?", "*AC-coupled* batteries add on easily."], "Already have solar? AC-coupled batteries are the easiest to add."),
    CTA("Hybrid or grid-tie?", "Choose right the first time", "Choosing an inverter?"),
])
add("solar-panels-hail-insurance", "solar-panels-hail-insurance", [
    T(["A *hailstorm* hits", "your neighborhood."], "Picture this. A hailstorm hits your neighborhood.", kicker="Picture this…"),
    T(["What happens to your", "*solar panels?*"], "What happens to your solar panels?"),
    T(["Panels are tested with *1-inch*", "hail at about *51 mph.*"], "Panels are tested with one-inch ice balls fired at about fifty-one miles per hour."),
    T(["Many are rated for *bigger* hail.", "~35–55 mm"], "Many are tested to even larger hail. Look for enhanced ratings in hail-prone states."),
    T(["Usually covered by", "*homeowners insurance.*"], "Rooftop solar is usually covered by homeowners insurance, but confirm your limits."),
    T(["After a storm: check *production*,", "inspect from the *ground.*"], "After a storm, check your production and inspect from the ground. Don't climb on the roof."),
    CTA("Solar vs hail", "Ratings, risks and insurance", "Live in hail country?"),
])
add("tesla-solar-roof-vs-panels", "tesla-solar-roof-vs-panels", [
    T(["Solar *shingles* look", "amazing."], "Picture this. You see a house with solar shingles. They look amazing.", kicker="Picture this…"),
    T(["But what do they *cost?*"], "But what do they cost?"),
    T(["A solar roof *replaces* your", "whole roof."], "A Tesla Solar Roof replaces your entire roof. Panels sit on top of your existing one."),
    T(["Per watt: *2–3×* the cost", "of regular panels."], "Per watt of capacity, solar roofs typically cost two to three times as much as panels."),
    T(["Panels: more *efficient*,", "easier to *repair.*"], "Panels are more efficient per square foot, easier to repair, and widely available.", bg="panels-sun.jpg"),
    T(["Solar roof makes sense if you", "*need a new roof anyway.*"], "A solar roof mainly makes sense if you need a new roof anyway and love the look."),
    CTA("Solar roof or panels?", "The price gap explained", "Torn between the two?"),
])
add("monocrystalline-panels", "monocrystalline-panels", [
    T(["Mono. Poly. Thin-film.", "*What does it mean?*"], "Mono. Poly. Thin-film. Your solar quote is full of jargon.", kicker="Solar jargon"),
    T(["Here's the *simple* version."], "Here's the simple version."),
    T(["*Monocrystalline:* the standard", "for US homes."], "Monocrystalline panels are cut from a single silicon crystal, and they're the standard for US homes.", bg="panels-sun.jpg"),
    T(["About *20–25%* efficient."], "They're about twenty to twenty-five percent efficient."),
    T(["*Poly* is now rare. *Thin-film*", "is mostly for big solar farms."], "Polycrystalline is now rare on homes, and thin-film is mainly used in utility-scale projects."),
    T(["What matters more:", "*installer* + *price per watt.*"], "Panel type matters less than installer quality and price per watt."),
    CTA("Solar panel types, simply", "Mono, poly, thin-film and new cells", "Confused by panel types?"),
])
add("solar-panel-shading-optimizers", "solar-panel-shading-optimizers", [
    T(["One tree shades *one panel.*"], "Picture this. One tree shades just one of your solar panels.", kicker="Picture this…"),
    T(["Your *whole system* drops."], "And your whole system's output drops."),
    T(["In a simple string, one shaded", "panel drags down the *rest.*"], "In a simple string, shade on one panel can reduce the output of the whole string."),
    T(["*Optimizers* or *microinverters*", "fix most of that."], "Optimizers or microinverters usually recover a big share of those shade losses.", bg="inverter.jpg"),
    T(["Heavy, all-day shade?", "*Trim trees* instead."], "But heavy, all-day shade can't be fixed with electronics. Trimming trees or using another roof face matters more."),
    CTA("Shade on your roof?", "How to protect your output", "Got a shady roof?"),
])
add("solar-installation-process-timeline", "solar-installation-process-timeline", [
    T(["You *signed* the solar contract.", "Now what?"], "Imagine you just signed your solar contract. Now what?", kicker="Imagine this…"),
    T(["When will your panels", "*actually turn on?*"], "When will your panels actually turn on?"),
    T(["Most projects take", "*1–3 months.*"], "Most projects take about one to three months from contract to switch-on."),
    T(["The rooftop work?", "Only *1–3 days.*"], "The rooftop work itself usually takes just one to three days."),
    T(["*Permits*, *inspections* and", "*utility approval* cause the wait."], "Permits, inspections, and utility approval cause most of the wait."),
    T(["Don't switch on before", "*permission to operate.*"], "And don't turn the system on until the utility grants permission to operate. Tie your final payment to that too."),
    CTA("From contract to switch-on", "Every step, explained", "Getting solar installed soon?"),
])
add("powerwall-3-vs-franklinwh-apower-2", "powerwall-3-vs-franklinwh-apower-2", [
    T(["*Tesla* or *FranklinWH?*", "Whole-home battery showdown."], "Tesla Powerwall three or FranklinWH aPower two? Let's settle it.", kicker="Battery battle"),
    T(["*Storage:* FranklinWH wins.", "~15 kWh vs 13.5 kWh"], "Storage: FranklinWH wins, fifteen kilowatt-hours versus thirteen point five."),
    T(["*Power:* Powerwall wins.", "~11.5 kW vs 10 kW"], "Continuous power: Powerwall wins, eleven point five kilowatts versus ten."),
    T(["*Warranty:* FranklinWH.", "~15 years vs 10"], "Warranty: FranklinWH, fifteen years versus ten, plus built-in generator integration."),
    T(["*New solar?* Powerwall is", "usually cheaper."], "Getting new solar? Powerwall three is usually cheaper, because the inverter is built in.", bg="battery-wall.jpg"),
    T(["*Existing solar?* FranklinWH", "adds on easily."], "Already have solar? FranklinWH is a strong choice for adding storage."),
    CTA("Which battery wins for you?", "Powerwall 3 vs FranklinWH", "Choosing a whole-home battery?"),
])

out = pathlib.Path("scripts"); out.mkdir(exist_ok=True)
for i, (slug, article, scenes) in enumerate(V, start=2):
    json.dump({"assets": "../assets", "article": article, "scenes": scenes},
              open(out / f"{i:02d}-{slug}.json", "w"), indent=1, ensure_ascii=False)
print(len(V), "scripts written")
