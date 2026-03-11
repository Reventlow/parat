"""
Scenarie 2: Oversvømmelsen
Sværhedsgrad: ★★☆☆☆ (Let-Middel)

Ekstrem nedbør over flere dage forårsager oversvømmelser.
Vandforsyningen kompromitteres. Curveball: +1 dag.
"""

from engine import Color, styled, Household


def build_scenario(h: Household) -> dict:
    """Build the Oversvømmelsen scenario adapted to household."""

    # ─── DAG 1 ───

    day1_events = []

    e1_text = (
        "Det har regnet uafbrudt i fire dage. Åer og vandløb er gået "
        "over deres bredder. Kloakkerne kan ikke følge med. "
        "Du kigger ud af vinduet og ser vand stå på vejen. "
        "Telefonen bipper: 'Beredskabet opfordrer beboere i dit "
        "område til at forberede sig på mulig evakuering.'"
    )
    if h.is_apartment:
        e1_text += (
            " Fra jeres lejlighed kan I se vandet stige på "
            "parkeringspladsen. Kælderen er allerede oversvømmet."
        )
    elif h.housing == "landejendom":
        e1_text += (
            " Markerne omkring jeres ejendom ligner en sø. "
            "Indkørslen er ved at blive ufremkommelig."
        )

    e1_questions = [
        ("Har I en nødtaske/flugttaske klar med det vigtigste — "
         "dokumenter, medicin, tøj, vand?", "plan"),
        ("Har I vigtige dokumenter (pas, forsikring, sundhedskort) "
         "samlet ét sted, så I hurtigt kan tage dem med?", "penge"),
    ]

    # Household-specific: children pickup plan during daytime crisis
    if h.has_children:
        e1_questions.append(
            ("Har I en plan for hvem der henter børnene fra "
             "skole/institution hvis krisen rammer midt på dagen?",
             "plan"))

    # Household-specific: pet evacuation plan
    if h.has_pets:
        e1_questions.append(
            ("Hvis I skal evakuere — har I en plan for jeres kæledyr?",
             "plan"))

    # Household-specific: infant emergency supplies in go-bag
    if h.has_infants:
        e1_questions.append(
            ("Har I babymad, bleer, modermælkserstatning og andre "
             "nødvendigheder til den lille på lager til mindst "
             "3 dage?", "mad"))

    day1_events.append({
        "title": "Vandet stiger",
        "narrative": e1_text,
        "news": ("DR Nyheder: Ekstrem nedbør har forårsaget oversvømmelser "
                 "i store dele af Jylland og på Fyn. Beredskabet er "
                 "udkaldt i flere kommuner."),
        "questions": e1_questions,
        "think": (
            "Tænk over: Hvis I havde 15 minutter til at forlade "
            "huset — hvad ville I tage med? Har I talt om det "
            "som familie?"
        ),
    })

    # Event 2: Vandforsyning
    pet_str = ""
    if h.has_pets:
        pet_str = f" og {h.num_pets} kæledyr"

    day1_events.append({
        "title": "Forurenet vand",
        "narrative": (
            "Sidst på eftermiddagen kommer meldingen: Vandforsyningen "
            "i jeres område er kompromitteret. Oversvømmelserne har "
            "forurenet vandværket. Myndighederne fraråder at drikke "
            "vand fra hanen."
        ),
        "questions": [
            (f"Har I drikkevand nok på flaske eller dunk til alle "
             f"{h.total_people} personer{pet_str}? "
             f"I har brug for ca. {h.water_per_day:.0f} liter "
             "om dagen.", "vand"),
            ("Har I tænkt over hvordan I klarer toilettet uden "
             "rindende vand?", "hygiejne"),
        ],
    })

    day1 = {
        "title": "Dag 1: Regnen fortsætter",
        "intro": "Vandstanden stiger time for time. Situationen eskalerer.",
        "events": day1_events,
    }

    # ─── DAG 2 ───

    day2_events = []

    e3_text = (
        "Natten har været lang. Vandet er steget yderligere. "
        "Hele kvarteret er uden rent vand. "
    )
    if h.has_children:
        e3_text += "Skolerne er lukket på ubestemt tid. "
        if h.has_infants:
            e3_text += (
                "Daginstitutionen har også lukket. Den lille kræver "
                "konstant opmærksomhed. "
            )
    e3_text += (
        "Du kan høre sirener i det fjerne. Naboerne taler om at "
        "vandet måske stiger endnu mere."
    )

    e3_questions = []
    if h.has_children:
        e3_questions.append(
            ("Skoler og institutioner er lukket. Har I en plan for "
             "pasning af børnene, hvis begge forældre skal arbejde?",
             "plan"))
    e3_questions.append(
        ("Har I nok hygiejneartikler — toiletpapir, håndsprit, "
         "vådservietter — til at klare jer uden rindende vand?",
         "hygiejne"))

    # Household-specific: medication list
    if h.has_medication_needs:
        e3_questions.append(
            ("Har I en liste over den medicin der tages i husstanden "
             "— dosis og præparatnavn?", "forste"))

    day2_events.append({
        "title": "Hverdagen bryder sammen",
        "narrative": e3_text,
        "questions": e3_questions,
    })

    # Event: Mad
    e4_text = (
        "Supermarkederne der stadig er åbne, har lange køer. "
        "Hylderne er halvtomme — især vand, brød og dåsemad er "
        "revet væk. "
    )
    if h.is_rural:
        e4_text += ("Den nærmeste åbne butik er langt væk, og "
                    "vejene er usikre.")
    else:
        e4_text += "Folk er begyndt at hamstre."

    day2_events.append({
        "title": "Tomme hylder",
        "narrative": e4_text,
        "questions": [
            ("Har I mad nok i huset til at klare jer i 3 dage "
             "uden at handle?", "mad"),
            ("Kan I lave mad hvis strømmen også går?", "mad"),
        ],
    })

    day2 = {
        "title": "Dag 2: Under vand",
        "intro": "Oversvømmelsen breder sig. Hverdagen er sat på pause.",
        "events": day2_events,
    }

    # ─── DAG 3 ───

    day3_events = []

    day3_events.append({
        "title": "Ny regnfront",
        "narrative": (
            "Det er tredje dag. I har vænnet jer til lyden af regn "
            "mod vinduerne. Men nu melder radio og beredskab at en "
            "ny regnfront er på vej. Vandstanden kan stige yderligere."
        ),
        "questions": [
            ("Har I stadig drikkevand nok?", "vand"),
            ("Har I stadig mad nok til hele husstanden?", "mad"),
        ],
        "radio": (
            "\"...DMI varsler endnu 48 timers kraftig regn. "
            "Beredskabet opfordrer til fortsat forsigtighed. "
            "Evakuering kan blive nødvendig i flere områder...\""
        ),
    })

    # Hygiejne
    e6_text = (
        "Uden rindende vand er hygiejnen blevet en udfordring. "
        "Toilettet kan ikke skylle. Opvasken hober sig op. "
    )
    if h.has_infants:
        e6_text += "Bleerne er ved at slippe op. "
    e6_text += "Stanken fra kloakkerne udenfor er ubehagelig."

    e6_questions = [
        ("Har I en plan for affaldshåndtering og toilet "
         "uden vandforsyning?", "hygiejne"),
    ]

    # Household-specific: rural isolation neighbor check
    if h.is_rural:
        e6_questions.append(
            ("I bor isoleret — har I aftalt med naboer at tjekke "
             "op på hinanden?", "plan"))

    # Household-specific: apartment elevator dependency
    if h.is_apartment:
        e6_questions.append(
            ("Bor I i lejlighed med ældre eller gangbesværede? "
             "Kan I komme ud uden elevator?", "plan"))

    day3_events.append({
        "title": "Hygiejnekrise",
        "narrative": e6_text,
        "questions": e6_questions,
        "think": (
            "Tænk over: Simpel hygiejne som håndvask forebygger "
            "sygdom. Uden rindende vand bliver håndsprit og "
            "vådservietter livsvigtige."
        ),
    })

    day3 = {
        "title": "Dag 3: Presset stiger",
        "intro": "Ingen tegn på bedring. Ny regn er på vej.",
        "events": day3_events,
    }

    # ─── CURVEBALL ───

    # Build curveball questions conditionally
    cb_questions = [
        ("Har I stadig mad nok?", "mad"),
        ("Har I stadig drikkevand nok?", "vand"),
        ("Hvad ville I gøre for at skaffe mere? "
         "Har I en plan?", "plan"),
    ]

    # Household-specific: pet food running out on day 4
    if h.has_pets:
        cb_questions.append(
            ("Har I stadig foder nok til jeres kæledyr?", "mad"))

    # Household-specific: older children can help
    if h.has_children and any(a >= 10 for a in h.child_ages):
        cb_questions.append(
            ("Kan jeres større børn hjælpe med praktiske opgaver "
             "under krisen?", "plan"))

    curveball = {
        "narrative": (
            "I troede det var ved at være overstået. Men den nye "
            "regnfront er værre end varslet. Vandstanden stiger "
            "til nye rekorder. Myndighederne melder at situationen "
            "forventes at vare mindst ét døgn mere."
        ),
        "extra_days": 1,
        "day_events": [{
            "title": "Dag 4: Stadig under vand",
            "intro": "Fjerde dag. Jeres forsyninger var beregnet til tre.",
            "events": [{
                "title": "Ressourcetjek",
                "narrative": (
                    f"Det er nu dag 4. Jeres forsyninger var beregnet "
                    f"til 3 dage. Med {h.total_people} personer "
                    "i husstanden mærker I presset."
                ),
                "questions": cb_questions,
            }],
        }],
    }

    return {
        "name": "Oversvømmelsen",
        "difficulty": 2,
        "stars": styled("★★", Color.BRIGHT_YELLOW) + styled("☆☆☆", Color.GRAY),
        "tagline": "Ekstrem regn oversvømmer landet",
        "intro": (
            "Det er oktober. Det har regnet uafbrudt i næsten en uge. "
            "DMI har udsendt den ene varsel efter den anden, men "
            "regnens omfang overstiger alle prognoser.\n\n"
            "Åer og fjorde går over deres bredder. Kloaksystemerne "
            "bryder sammen. Veje forvandles til floder.\n\n"
            "Og nu er jeres område ramt."
        ),
        "days": [day1, day2, day3],
        "curveball": curveball,
    }
