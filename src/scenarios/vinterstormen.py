"""
Scenarie 1: Vinterstormen
Sværhedsgrad: ★☆☆☆☆ (Let)

En voldsom decemberstorm lammer Danmark med orkanstyrke.
Strømmen forsvinder, veje blokeres, og familien er isoleret.
3 dage, ingen curveball.
"""

from engine import Color, styled, Household


def build_scenario(h: Household) -> dict:
    """Build the Vinterstormen scenario adapted to household."""

    # ─── DAG 1: Stormen rammer ───

    day1_events = []

    # Event 1: Strømsvigt
    e1_text = (
        "Det er en kold decemberdag. Vejrudsigten advarede om storm, men "
        "ingen havde forestillet sig det her. Vindstødene når 140 km/t. "
        "Klokken 14:23 flimrer lyset — og så er der mørkt. "
        "Køleskabet holder op med at brumme. Radiatoren bliver langsomt kold."
    )
    if h.is_apartment:
        e1_text += (
            " I jeres lejlighed virker elevatoren ikke længere, "
            "og trappeopgangen er bælgmørk."
        )
    else:
        e1_text += (
            " Udenfor hyler vinden gennem haven, og I kan høre "
            "grene knække fra de store træer."
        )

    e1_questions = [
        ("Har I lommelygter eller batteridrevne lamper derhjemme?", "lys"),
        ("Har I stearinlys og tændstikker eller lighter?", "lys"),
        (f"Har I ekstra tæpper, soveposer eller varmt tøj "
         f"til alle {h.total_people} i husstanden?", "varme"),
    ]

    # Household-specific: infant warmth needs
    if h.has_infants:
        e1_questions.append(
            ("Har I varmt tøj og ekstra tæpper specifikt til den lille?",
             "varme"))

    # Household-specific: apartment without elevator
    if h.is_apartment:
        e1_questions.append(
            ("Bor I i lejlighed med ældre eller gangbesværede? "
             "Kan I komme ud uden elevator?", "plan"))

    day1_events.append({
        "title": "Strømsvigt",
        "narrative": e1_text,
        "news": ("DR Nyheder: Orkanen har slået strømmen ud i store dele "
                 "af landet. Over 300.000 husstande er uden strøm. "
                 "Energiselskaberne kan ikke give en tidshorisont "
                 "for genopretning."),
        "questions": e1_questions,
    })

    # Event 2: Kommunikation
    e2_questions = [
        ("Har I en powerbank eller anden alternativ strømkilde "
         "til telefonen?", "komm"),
        ("Har I en batteridrevet eller håndsving FM-radio?", "komm"),
    ]

    # Household-specific: children know how to call 112
    if h.has_children:
        e2_questions.append(
            ("Har I talt med børnene om hvad man gør i en nødsituation "
             "— alderstilpasset?", "plan"))

    day1_events.append({
        "title": "Mørket falder på",
        "narrative": (
            "Klokken er kun 15:30, men det er allerede bælgmørkt udenfor. "
            "Stormen raser videre. Du tager din telefon for at tjekke "
            "nyhederne — batteriet viser 34%. Mobilnettet er overbelastet, "
            "og det tager evigheder at indlæse noget som helst."
        ),
        "questions": e2_questions,
        "think": (
            "Tænk over: Hvis telefonen løber tør og internettet er "
            "nede — hvordan følger I så med i hvad der sker?"
        ),
    })

    day1 = {
        "title": "Dag 1: Stormen rammer",
        "intro": ("Decemberstormen rammer Danmark med fuld kraft. "
                  "Det bliver en lang aften."),
        "events": day1_events,
    }

    # ─── DAG 2: Isoleret ───

    day2_events = []

    # Event 1: Mad
    day2_events.append({
        "title": "Køleskabet tør",
        "narrative": (
            "Du vågner til en underlig stilhed. Stormen er aftaget lidt, "
            "men udenfor er verden forvandlet. Træer ligger væltet over "
            "veje, tagplader er blæst af, og der er vand overalt. "
            "Strømmen er stadig væk. Du åbner køleskabet — maden er "
            "ved at nå stuetemperatur. Fryseren er begyndt at tø op."
        ),
        "questions": [
            (f"Har I tørvarer, dåsemad og mad der kan spises uden "
             f"tilberedning til alle {h.total_people} i mindst 3 dage?", "mad"),
            ("Har I en manuel dåseåbner?", "mad"),
            ("Kan I tilberede varm mad uden strøm? "
             "F.eks. gasblus, stormkøkken, grill (kun udendørs)?", "mad"),
        ],
        "think": (
            "Tænk over: Maden i jeres fryser holder sig ca. 24-48 "
            "timer hvis I holder den lukket. Hvad ville I spise "
            "først — og i hvilken rækkefølge?"
        ),
    })

    # Event 2: Isolation
    iso_text = (
        "Du overvejer at køre til supermarkedet, men vejen er "
        "blokeret af væltede træer. "
    )
    if h.is_rural:
        iso_text += (
            f"I bor i et {h.location_display}, og den nærmeste åbne "
            "butik er sandsynligvis langt væk."
        )
    else:
        iso_text += (
            "Naboen fortæller at der ikke er strøm i hele området, "
            "og de fleste butikker er lukkede."
        )

    iso_questions = [
        ("Har I mad og fornødenheder nok til at klare jer "
         "uden at forlade hjemmet i 3 dage?", "mad"),
    ]

    # Household-specific: pet supplies during isolation
    if h.has_pets:
        iso_questions.append(
            ("Har I foder nok til jeres kæledyr til mindst 3 dage?",
             "mad"))
        if "hund" in h.pet_types:
            iso_questions.append(
                ("Har I tænkt over hvordan I lufter/motionerer jeres "
                 "hund under krisen?", "plan"))

    # Household-specific: rural isolation check-in
    if h.is_rural:
        iso_questions.append(
            ("I bor isoleret — har I aftalt med naboer at tjekke "
             "op på hinanden?", "plan"))

    day2_events.append({
        "title": "Isoleret",
        "narrative": iso_text,
        "questions": iso_questions,
        "think": (
            "Tænk over: Kender I jeres naboer godt nok til at "
            "hjælpe hinanden i en krise? Kunne I dele ressourcer?"
        ),
        "radio": (
            "\"...myndighederne opfordrer alle til at blive "
            "indendørs og undgå unødvendig kørsel. Vejene er "
            "farlige mange steder...\""
        ),
    })

    day2 = {
        "title": "Dag 2: Isoleret",
        "intro": ("Stormen er aftaget, men konsekvenserne er tydelige. "
                  "I er afskåret."),
        "events": day2_events,
    }

    # ─── DAG 3: Udholdenhed ───

    day3_events = []

    # Event 1: Moral
    moral_text = "Det er tredje dag uden strøm. "
    if h.has_children:
        moral_text += (
            f"Jeres {h.num_children} børn er urolige. Ingen skole, "
            "ingen skærme, ingen internet. "
        )
        if h.has_infants:
            moral_text += "Den mindste er ked af det og vil ikke falde til ro. "
    moral_text += (
        "Temperaturerne er faldet i huset, og stemningen er trykket. "
        "Timerne føles lange."
    )

    moral_questions = [
        ("Har I brætspil, kortspil, bøger eller andre "
         "aktiviteter der ikke kræver strøm?", "moral"),
    ]

    # Household-specific: children entertainment without power
    if h.has_children:
        moral_questions.append(
            ("Har I legetøj, bøger og aktiviteter der kan holde "
             "børnene beskæftiget uden strøm?", "moral"))

    # Household-specific: infant supplies during extended crisis
    if h.has_infants:
        moral_questions.append(
            ("Har I babymad, bleer, modermælkserstatning og andre "
             "nødvendigheder til den lille på lager til mindst "
             "3 dage?", "mad"))

    day3_events.append({
        "title": "Lange timer",
        "narrative": moral_text,
        "questions": moral_questions,
        "think": (
            "Tænk over: I en længere krise er mental sundhed "
            "lige så vigtig som fysisk. Har I tænkt over hvordan "
            "I holder humøret oppe som familie — dag efter dag?"
        ),
    })

    # Event 2: Skade
    injury_who = "et familiemedlem" if h.total_people > 1 else "du"
    injury_questions = [
        ("Har I en førstehjælpskasse derhjemme?", "forste"),
        ("Ved I hvordan man renser og forbinder et sår korrekt?", "forste"),
        (f"Jeres nærmeste skadestue er {h.distance_hospital_km} km "
         "væk. Kan I komme derhen med spærrede veje?", "plan"),
    ]

    # Household-specific: medication list in first aid context
    if h.has_medication_needs:
        injury_questions.append(
            ("Har I en liste over den medicin der tages i husstanden "
             "— dosis og præparatnavn?", "forste"))

    day3_events.append({
        "title": "Uheld",
        "narrative": (
            f"Da {injury_who} går udenfor for at tjekke skaderne "
            "efter stormen, glider vedkommende på en våd gren og "
            "river sig grimt op på underarmen. Såret bløder kraftigt "
            "og ser ud til at kræve behandling."
        ),
        "questions": injury_questions,
    })

    day3 = {
        "title": "Dag 3: Udholdenhed",
        "intro": ("Tredje dag. Strømmen er stadig væk. "
                  "Tålmodigheden bliver sat på prøve."),
        "events": day3_events,
    }

    return {
        "name": "Vinterstormen",
        "difficulty": 1,
        "stars": styled("★", Color.BRIGHT_YELLOW) + styled("☆☆☆☆", Color.GRAY),
        "tagline": "En voldsom storm lammer Danmark",
        "intro": (
            "Det er december. Meteorologerne har i dagevis advaret om en "
            "usædvanlig kraftig vinterstorm, men danskerne er vant til "
            "blæsevejr. Denne gang er det anderledes.\n\n"
            "Stormen rammer med en kraft, Danmark ikke har oplevet i "
            "mands minde. Vindstød op til 150 km/t fejer hen over "
            "landet. Elmaster knækker. Træer vælter. Veje blokeres.\n\n"
            "Og så forsvinder strømmen."
        ),
        "days": [day1, day2, day3],
        "curveball": None,
    }
