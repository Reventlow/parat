"""
Scenarie 5: Mørkelægning
Sværhedsgrad: ★★★★★ (Meget svær)

Hybrid krise: sabotage mod gasforsyning + cyberangreb mod el-net.
Alt bryder sammen på én gang — gas, strøm, vand, kommunikation.
Curveball: +3 dage (i alt 6 dage).
"""

from engine import Color, styled, Household


def build_scenario(h: Household) -> dict:
    """Build the Mørkelægning scenario adapted to household."""

    # ─── DAG 1 ───

    day1_events = []

    day1_events.append({
        "title": "Dobbelt slag",
        "narrative": (
            "Det starter med en eksplosion ved en vigtig gasledning "
            "i Nordjylland. Inden for timer melder myndighederne at "
            "gasforsyningen er afbrudt i store dele af landet. "
            "Samtidig rapporterer Energinet om \"uregelmæssigheder\" "
            "i el-nettet. Strømmen begynder at falde ud regionalt."
        ),
        "news": (
            "BREAKING: Eksplosion ved gasledning i Nordjylland. "
            "Sabotage kan ikke udelukkes. Samtidig meldes om "
            "ustabilitet i el-nettet. Myndighederne holder krisemøde."
        ),
        "questions": [
            ("Har I alternative varmekilder hvis gas og strøm "
             "forsvinder?", "varme"),
        ],
    })

    hamstring_questions = [
        ("Havde I allerede et lager af langtidsholdbar mad "
         "inden panikken startede?", "mad"),
        ("Har I vand på lager — dunke eller flasker?", "vand"),
    ]

    # Household-specific: pet food before panic buying
    if h.has_pets:
        hamstring_questions.append(
            ("Har I foder nok til jeres kæledyr til mindst 3 dage?",
             "mad"))

    # Household-specific: infant supplies before shops empty
    if h.has_infants:
        hamstring_questions.append(
            ("Har I babymad, bleer, modermælkserstatning og andre "
             "nødvendigheder til den lille på lager til mindst "
             "3 dage?", "mad"))

    day1_events.append({
        "title": "Hamstring",
        "narrative": (
            "Rygterne spreder sig som en steppebrand. Sociale medier "
            "— som stadig virker, for nu — er fyldt med spekulation "
            "om krig, terror og sammenbrud. Folk stormer "
            "supermarkederne. Inden for timer er hylderne tømt."
        ),
        "questions": hamstring_questions,
    })

    day1_events.append({
        "title": "Rationering",
        "narrative": (
            "Sidst på eftermiddagen melder Energinet at de indfører "
            "strømrationering. I får strøm i 4 timer ad gangen, "
            "derefter 8 timer uden. Hvornår jeres vindue er, "
            "aner I ikke."
        ),
        "questions": [
            ("Har I powerbank og batterier klar til de mørke "
             "timer?", "lys"),
            ("Har I stearinlys, lommelygter og tændstikker?", "lys"),
        ],
        "think": (
            "Tænk over: Hvis I kun har 4 timers strøm — hvad "
            "ville I prioritere? Opladning? Madlavning? Vask? "
            "Information?"
        ),
    })

    day1 = {
        "title": "Dag 1: Dobbelt slag",
        "intro": ("Gas og strøm forsvinder. Panikken breder sig. "
                  "Det er kun begyndelsen."),
        "events": day1_events,
    }

    # ─── DAG 2 ───

    day2_events = []

    pet_str = ""
    if h.has_pets:
        pet_str = f"og {h.num_pets} kæledyr "

    triple_questions = [
        (f"Har I drikkevand nok til {h.total_people} personer "
         f"{pet_str}i flere dage? I har brug for "
         f"{h.water_per_day:.0f} liter om dagen.", "vand"),
        ("Har I vand til hygiejne — håndvask, toilet?",
         "hygiejne"),
    ]

    # Household-specific: children emergency conversation in serious crisis
    if h.has_children:
        triple_questions.append(
            ("Har I talt med børnene om hvad man gør i en "
             "nødsituation — alderstilpasset?", "plan"))

    # Household-specific: apartment without elevator in total blackout
    if h.is_apartment:
        triple_questions.append(
            ("Bor I i lejlighed med ældre eller gangbesværede? "
             "Kan I komme ud uden elevator?", "plan"))

    day2_events.append({
        "title": "Tredobbelt krise",
        "narrative": (
            "Natten var lang og kold. Om morgenen er strømmen helt "
            "væk — rationeringen er ophørt, fordi nettet er brudt "
            "helt sammen. Og nu kommer næste slag: Vandforsyningen "
            "svigter også. Pumpestationerne har ingen strøm."
        ),
        "questions": triple_questions,
    })

    e5_text = (
        "Hospitalerne kører på nødgeneratorer, men de er "
        "overbelastet. Radio-meldingen er klar: \"Kun livstruende "
        "skader. Alle andre må klare sig selv.\" "
    )
    if h.has_children:
        e5_text += "Et af børnene har fået feber. Er det alvorligt?"

    hospital_questions = [
        ("Har I en førstehjælpskasse og basismedicin "
         "derhjemme?", "forste"),
        ("Har I et førstehjælpskursus — ved I hvad I skal "
         "gøre ved de mest almindelige skader og sygdomme?",
         "forste"),
    ]

    # Household-specific: medication list when hospitals are closed
    if h.has_medication_needs:
        hospital_questions.append(
            ("Har I en liste over den medicin der tages i husstanden "
             "— dosis og præparatnavn?", "forste"))

    # Household-specific: children know how to call 112
    if h.has_children:
        hospital_questions.append(
            ("Ved jeres børn hvordan man ringer 112?", "komm"))

    day2_events.append({
        "title": "Hospitalerne lukker",
        "narrative": e5_text,
        "questions": hospital_questions,
        "radio": (
            "\"...hospitalerne har indført nødprocedurer. "
            "Kun akut livstruende tilfælde behandles. "
            "Alle borgere opfordres til at yde førstehjælp "
            "i eget hjem...\""
        ),
    })

    if h.has_children or h.total_people > 1:
        e6_text = (
            "Midt i kaosset ringer din arbejdsgiver: Du er "
            "klassificeret som kritisk personale og forventes "
            "på arbejde. "
        )
        if h.has_children:
            e6_text += (
                "Men skolerne er lukket, og der er ingen pasning. "
                "Hvem passer børnene?"
            )
        else:
            e6_text += "Men hvad med resten af familien derhjemme?"

        day2_events.append({
            "title": "Pligt eller familie",
            "narrative": e6_text,
            "questions": [
                ("Har I en plan for hvem der gør hvad, hvis "
                 "krisen kræver at I deler jer?", "plan"),
            ],
            "think": (
                "Tænk over: Ville I møde på arbejde og lade "
                "familien klare sig selv? Eller blive hjemme og "
                "risikere konsekvenserne? Der er ikke et rigtigt "
                "svar."
            ),
        })

    day2 = {
        "title": "Dag 2: Total sammenbrud",
        "intro": ("Strøm, gas og vand er væk. Hospitalerne lukker. "
                  "I er på egen hånd."),
        "events": day2_events,
    }

    # ─── DAG 3 ───

    day3_events = []

    e7_text = (
        "Temperaturen i huset er faldet til under 10 grader. "
        "Det er januar, og udenfor er der frost. "
    )
    if h.has_garden:
        e7_text += (
            "Har I brænde? En grill? Noget at varme jer ved "
            "— sikkert, udendørs?"
        )
    else:
        e7_text += (
            "I en lejlighed uden alternativ opvarmning er "
            "kulden jeres værste fjende nu."
        )

    cold_questions = [
        ("Har I en plan for at overleve kulden — isolere "
         "ét rum, sove tæt sammen, bruge alle tæpper og "
         "soveposer?", "varme"),
        ("VIGTIGT: Ved I at man ALDRIG må bruge grill, "
         "gasblus eller åben ild til opvarmning indendørs "
         "(CO-forgiftning)?", "forste"),
    ]

    # Household-specific: infant warmth in extreme cold
    if h.has_infants:
        cold_questions.append(
            ("Har I varmt tøj og ekstra tæpper specifikt til "
             "den lille?", "varme"))

    # Household-specific: children without power entertainment
    if h.has_children:
        cold_questions.append(
            ("Har I legetøj, bøger og aktiviteter der kan holde "
             "børnene beskæftiget uden strøm?", "moral"))

    day3_events.append({
        "title": "Kulden bider",
        "narrative": e7_text,
        "questions": cold_questions,
    })

    day3_events.append({
        "title": "Skade uden hjælp",
        "narrative": (
            "Under forsøget på at hente vand fra en nærliggende "
            "sø eller vandløb falder et familiemedlem og brækker "
            "sandsynligvis håndleddet. Det hæver voldsomt. "
            f"Nærmeste skadestue er {h.distance_hospital_km} km "
            "væk — og de tager kun livstruende tilfælde."
        ),
        "questions": [
            ("Kan I stabilisere en mulig fraktur med det I "
             "har derhjemme — forbinding, skinne, is?", "forste"),
            ("Har I smertestillende medicin?", "forste"),
        ],
    })

    svinder_questions = [
        ("Har I stadig nok mad?", "mad"),
        ("Har I stadig nok vand?", "vand"),
        ("Har I nogen form for nødforsyningsplan — "
         "ved I hvor I kan hente vand, mad, hjælp?", "plan"),
    ]

    # Household-specific: rural isolation neighbor support
    if h.is_rural:
        svinder_questions.append(
            ("I bor isoleret — har I aftalt med naboer at tjekke "
             "op på hinanden?", "plan"))

    # Household-specific: older children helping in survival situation
    if h.has_children and any(a >= 10 for a in h.child_ages):
        svinder_questions.append(
            ("Kan jeres større børn hjælpe med praktiske opgaver "
             "under krisen?", "plan"))

    day3_events.append({
        "title": "Alt svinder",
        "narrative": (
            "Det er dag 3. I gør status: Maden svinder. Vandet "
            "er knap. Batterier og stearinlys er brugt. "
            "I har ikke hørt nyt fra myndighederne i timer."
        ),
        "questions": svinder_questions,
    })

    day3 = {
        "title": "Dag 3: Overlevelse",
        "intro": ("Alt er koldt, mørkt og stille. "
                  "Nu handler det om at overleve."),
        "events": day3_events,
    }

    # ─── CURVEBALL: +3 dage ───

    # Build curveball day 4 questions conditionally
    cb_d4_questions = [
        ("Har I stadig drikkevand?", "vand"),
        ("Har I stadig mad?", "mad"),
    ]

    # Household-specific: pet food running out after 3 days
    if h.has_pets:
        cb_d4_questions.append(
            ("Har I stadig foder nok til jeres kæledyr?", "mad"))

    # Household-specific: infant supplies running out
    if h.has_infants:
        cb_d4_questions.append(
            ("Har I stadig babymad, bleer og nødvendigheder til "
             "den lille?", "mad"))

    # Build curveball day 5 questions conditionally
    cb_d5_questions = [
        ("Har I et lokalt netværk I kan trække "
         "på i en krise?", "plan"),
        ("Har I ressourcer I kan dele?", "mad"),
    ]

    # Household-specific: pet evacuation if leaving home
    if h.has_pets:
        cb_d5_questions.append(
            ("Hvis I skal evakuere — har I en plan for jeres "
             "kæledyr?", "plan"))

    # Household-specific: dog walking on day 5 of crisis
    if h.has_pets and "hund" in h.pet_types:
        cb_d5_questions.append(
            ("Har I tænkt over hvordan I lufter/motionerer jeres "
             "hund under krisen?", "plan"))

    curveball = {
        "narrative": (
            "Via FM-radioen fanges en svag melding fra "
            "Beredskabsstyrelsen: \"Situationen er under kontrol, "
            "men genopretning af infrastruktur tager tid. "
            "Borgere må forvente yderligere 3-5 dages "
            "forstyrrelser.\" Tre til fem dage MERE."
        ),
        "extra_days": 3,
        "day_events": [
            {
                "title": "Dag 4: Ren overlevelse",
                "intro": ("Dag fire. Jeres forsyninger var til "
                          "tre dage."),
                "events": [{
                    "title": "Ressourcetjek",
                    "narrative": (
                        f"Med {h.total_people} personer har I "
                        f"brug for {h.water_per_day:.0f} liter "
                        "vand om dagen. Maden skal også række."
                    ),
                    "questions": cb_d4_questions,
                    "think": (
                        "Tænk over: Hvad ville I faktisk gøre "
                        "nu? Forlade hjemmet? Søge mod et "
                        "krisecenter? Bede naboerne om hjælp?"
                    ),
                }],
            },
            {
                "title": "Dag 5: Fællesskab",
                "intro": "Femte dag. Alene klarer I det ikke.",
                "events": [{
                    "title": "Sammen er vi stærkere",
                    "narrative": (
                        "Nogle naboer har organiseret sig. De "
                        "deler mad, vand og brænde. Men det "
                        "kræver tillid og samarbejde."
                    ),
                    "questions": cb_d5_questions,
                }],
            },
            {
                "title": "Dag 6: Lyset vender tilbage",
                "intro": ("Sjette dag. Der er en svag melding "
                          "om fremskridt."),
                "events": [{
                    "title": "Håb",
                    "narrative": (
                        "Sent på eftermiddagen flimrer lyset. "
                        "Køleskabet brummer. Radiatorerne tikker. "
                        "Strømmen er tilbage — i hvert fald for "
                        "nu. I har overlevet. Men til hvilken pris?"
                    ),
                    "questions": [
                        ("Har denne oplevelse ændret jeres syn "
                         "på beredskab?", "plan"),
                    ],
                    "think": (
                        "Tænk over: 6 dage. Kunne jeres familie "
                        "have klaret det? Hvad ville I gøre "
                        "anderledes?"
                    ),
                }],
            },
        ],
    }

    return {
        "name": "Mørkelægning",
        "difficulty": 5,
        "stars": styled("★★★★★", Color.BRIGHT_YELLOW),
        "tagline": "Alt der kan gå galt, går galt",
        "intro": (
            "Januar. De geopolitiske spændinger i Europa er på "
            "det højeste niveau i årtier. Efterretningstjenesterne "
            "har advaret om øget risiko for hybride angreb.\n\n"
            "Så sker det. En eksplosion ved en gasledning. "
            "Cyberangreb mod el-nettet. Vandforsyninger "
            "kompromitteret. Alt sammen inden for 12 timer.\n\n"
            "Danmark kastes ud i den værste krise siden "
            "2. verdenskrig. Ingen strøm. Ingen gas. Ingen vand. "
            "Ingen internet. Ingen hjælp.\n\n"
            "I er på egen hånd."
        ),
        "days": [day1, day2, day3],
        "curveball": curveball,
    }
