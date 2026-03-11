"""
Scenarie 3: Pandemien
Sværhedsgrad: ★★★☆☆ (Middel)

En ny aggressiv virus spreder sig. Danmark lukker ned.
Karantæne, panikkøb og sygdom i hjemmet. Curveball: +2 dage.
"""

from engine import Color, styled, Household


def build_scenario(h: Household) -> dict:
    """Build the Pandemien scenario adapted to household."""

    # ─── DAG 1 ───

    day1_events = []

    e1_questions = [
        ("Havde I allerede mad nok derhjemme til mindst 3 dage "
         "inden nedlukningen?", "mad"),
        ("Har I basale hygiejneartikler — håndsprit, sæbe, "
         "engangshandsker, mundbind?", "hygiejne"),
    ]

    # Household-specific: pet food supplies for lockdown
    if h.has_pets:
        e1_questions.append(
            ("Har I foder nok til jeres kæledyr til mindst 3 dage?",
             "mad"))

    # Household-specific: infant supplies for lockdown
    if h.has_infants:
        e1_questions.append(
            ("Har I babymad, bleer, modermælkserstatning og andre "
             "nødvendigheder til den lille på lager til mindst "
             "3 dage?", "mad"))

    day1_events.append({
        "title": "Nedlukning",
        "narrative": (
            "En ny, aggressiv virus spreder sig med alarmerende "
            "hastighed i Europa. Myndighederne annoncerer øjeblikkelig "
            "nedlukning. Du når lige at se nyhederne, før panikkøbene "
            "starter. Da du kommer til supermarkedet, er hylderne med "
            "pasta, ris, dåsemad og toiletpapir næsten tomme."
        ),
        "news": (
            "BREAKING: Sundhedsstyrelsen erklærer epidemi-beredskab. "
            "Alle skoler, daginstitutioner og ikke-kritiske "
            "arbejdspladser lukker fra i morgen. Borgere opfordres "
            "til at begrænse social kontakt."
        ),
        "questions": e1_questions,
    })

    if h.has_children:
        e2_text = (
            f"Skoler og daginstitutioner lukker fra i morgen. "
            f"Jeres {h.num_children} børn skal være hjemme på "
            "ubestemt tid. "
        )
        if h.has_infants:
            e2_text += (
                "Vuggestuen er også lukket. Den lille kræver "
                "konstant opsyn. "
            )
        e2_text += (
            "Jeres arbejdsgivere forventer stadig at I arbejder "
            "— hjemmefra hvis muligt."
        )
        day1_events.append({
            "title": "Hjemmefront",
            "narrative": e2_text,
            "questions": [
                ("Har I mulighed for at arbejde hjemmefra?", "plan"),
                ("Har I en plan for hvem der passer børnene "
                 "hvis begge forældre skal arbejde?", "plan"),
            ],
            "think": (
                "Tænk over: Ville I lade jeres pligter på arbejdet "
                "gå for at tage jer af familien? Hvad ville "
                "konsekvenserne være?"
            ),
        })

    day1 = {
        "title": "Dag 1: Nedlukning",
        "intro": "Danmark lukker ned. Panikken breder sig.",
        "events": day1_events,
    }

    # ─── DAG 2 ───

    day2_events = []

    sick_who = "dit barn" if h.has_children else "et familiemedlem"
    if h.total_people == 1:
        sick_who = "du"

    e3_questions = [
        ("Har I febertermometer, smertestillende og anden "
         "basismedicin derhjemme?", "forste"),
        ("Ved I hvordan man isolerer et sygt familiemedlem "
         "i hjemmet for at beskytte de andre?", "forste"),
        ("Har I et rum i hjemmet der kan bruges som "
         "karantænerum — med eget sengetøj, håndklæder og "
         "helst adgang til eget toilet?", "plan"),
    ]
    if h.has_medication_needs:
        e3_questions.append(
            ("Nogen i husstanden tager daglig medicin. "
             "Har I et lager til mindst en uge?", "forste"))
        # Household-specific: medication documentation
        e3_questions.append(
            ("Har I en liste over den medicin der tages i husstanden "
             "— dosis og præparatnavn?", "forste"))

    # Household-specific: children know emergency number
    if h.has_children:
        e3_questions.append(
            ("Ved jeres børn hvordan man ringer 112?", "komm"))

    day2_events.append({
        "title": "Sygdom i hjemmet",
        "narrative": (
            f"Om morgenen vågner {sick_who} med feber, hoste og "
            "ondt i halsen. Er det bare en forkølelse — eller er "
            "det virusset? Sundhedsvæsenet er overbelastet. "
            "Telefonkøen til lægen er over en time."
        ),
        "questions": e3_questions,
    })

    # Event: Essential worker dilemma (multi-person households)
    if h.total_people > 1:
        essential_text = (
            "Din arbejdsgiver ringer: Du er klassificeret som "
            "kritisk personale. Sundhedsvæsenet, ældreplejen, "
            "forsyningskæder — samfundet har brug for dig. "
            "Men du har set tallene. Kollegaer er blevet syge. "
            "Hvis du tager på arbejde, risikerer du at bringe "
            "smitten med hjem til din familie."
        )
        if h.has_children:
            essential_text += (
                " Du tænker på børnene. Hvad hvis de bliver syge "
                "på grund af dig?"
            )
        if h.has_medication_needs:
            essential_text += (
                " Og hvad med dem i husstanden der tager daglig "
                "medicin — de kan være ekstra sårbare."
            )

        essential_questions = [
            ("Har I som familie talt om hvad I gør, hvis én "
             "af jer arbejder i en kritisk funktion under en "
             "pandemi — inden krisen rammer?", "plan"),
            ("Kan I indrette en karantænezone i hjemmet — "
             "et separat rum hvor den der har været ude kan "
             "skifte tøj, vaske sig og eventuelt sove adskilt "
             "fra resten af familien?", "hygiejne"),
            ("Har I tøj og håndklæder der kan bruges udelukkende "
             "til den person der går på arbejde, så smitte "
             "ikke spredes i hjemmet?", "hygiejne"),
        ]

        day2_events.append({
            "title": "Pligt mod frygt",
            "narrative": essential_text,
            "questions": essential_questions,
            "think": (
                "Tænk over: Under COVID-19 valgte nogle i "
                "sundhedsvæsenet og ældreplejen at blive hjemme "
                "af frygt for at smitte deres familie. Andre "
                "sov i garagen eller flyttede midlertidigt. "
                "Der er ikke et rigtigt svar — men det er "
                "lettere hvis I har talt om det på forhånd."
            ),
        })

    day2_events.append({
        "title": "Hvem kan man stole på?",
        "narrative": (
            "Sociale medier flyder med modstridende information. "
            "Nogen siger virusset er ufarligt. Andre deler "
            "skrækscenarier. Du ved ikke helt hvad du skal tro."
        ),
        "questions": [
            ("Ved I hvor I finder officiel, pålidelig information "
             "under en krise? (sundhedsstyrelsen.dk, DR, politi.dk)",
             "komm"),
        ],
        "think": (
            "Tænk over: Misinformation kan være lige så farlig "
            "som selve krisen. Har I talt med familien om "
            "kildekritik?"
        ),
    })

    day2 = {
        "title": "Dag 2: Sygdom rammer",
        "intro": "Virusset kommer tættere på. Usikkerheden vokser.",
        "events": day2_events,
    }

    # ─── DAG 3 ───

    day3_events = []

    day3_events.append({
        "title": "Forsyninger svinder",
        "narrative": (
            "Tredje dag i isolation. Madlagrene svinder. "
            "Online-levering har ugers ventetid. "
            "De få butikker der holder åbent har begrænsede "
            "åbningstider og rationering på basisvarer."
        ),
        "questions": [
            ("Har I stadig mad nok til hele familien?", "mad"),
            ("Har I rent drikkevand nok?", "vand"),
        ],
    })

    mental_text = "Isoleringen tærer. Dagene flyder sammen. "
    if h.has_children:
        mental_text += "Børnene savner deres venner og er frustrerede. "
    mental_text += (
        "Usikkerheden om hvornår det er overstået gør det "
        "svært at holde modet oppe."
    )

    mental_questions = [
        ("Har I skabt faste rutiner og aktiviteter for "
         "hverdagen under krisen?", "moral"),
        ("Har I talt åbent i familien om situationen — "
         "herunder bekymringer og følelser?", "moral"),
    ]

    # Household-specific: children activities during isolation
    if h.has_children:
        mental_questions.append(
            ("Har I legetøj, bøger og aktiviteter der kan holde "
             "børnene beskæftiget uden strøm?", "moral"))

    # Household-specific: apartment isolation challenges
    if h.is_apartment:
        mental_questions.append(
            ("Bor I i lejlighed med ældre eller gangbesværede? "
             "Kan I komme ud uden elevator?", "plan"))

    # Household-specific: dog exercise during lockdown
    if h.has_pets and "hund" in h.pet_types:
        mental_questions.append(
            ("Har I tænkt over hvordan I lufter/motionerer jeres "
             "hund under krisen?", "plan"))

    day3_events.append({
        "title": "Mental sundhed",
        "narrative": mental_text,
        "questions": mental_questions,
    })

    day3 = {
        "title": "Dag 3: Isolation",
        "intro": "Tredje dag bag lukkede døre. Hvornår ender det?",
        "events": day3_events,
    }

    # ─── CURVEBALL ───

    curveball = {
        "narrative": (
            "Sundhedsmyndighederne holder pressemøde: "
            "\"Smittetallene stiger fortsat. Nedlukningen forlænges "
            "med mindst yderligere fire dage.\" "
            "I troede I var ved at komme igennem. Nu starter det forfra."
        ),
        "extra_days": 2,
        "day_events": [
            {
                "title": "Dag 4: Forlænget nedlukning",
                "intro": "Nedlukningen fortsætter. Hvor længe kan I holde?",
                "events": [{
                    "title": "Ressourcetjek",
                    "narrative": (
                        f"Dag 4. Jeres forsyninger til "
                        f"{h.total_people} personer rækker ikke "
                        "meget længere."
                    ),
                    "questions": [
                        ("Har I stadig mad nok?", "mad"),
                        ("Har I stadig drikkevand nok?", "vand"),
                    ],
                    "think": (
                        "Tænk over: Hvem i jeres netværk kunne I "
                        "bede om hjælp til at skaffe forsyninger?"
                    ),
                }],
            },
            {
                "title": "Dag 5: Udmattelse",
                "intro": "Femte dag. Træthed og frustration dominerer.",
                "events": [{
                    "title": "Holde sammen",
                    "narrative": (
                        "Alle er trætte. Konflikterne ulmer. "
                        "Det er svært at se lyset for enden "
                        "af tunnelen."
                    ),
                    "questions": [
                        ("Har I strategier til at håndtere stress "
                         "og konflikter i familien under pres?",
                         "moral"),
                        ("Har I stadig mad og vand?", "mad"),
                    ] + ([("Kan jeres større børn hjælpe med praktiske "
                           "opgaver under krisen?", "plan")]
                         if h.has_children and any(a >= 10 for a in h.child_ages)
                         else []),
                }],
            },
        ],
    }

    return {
        "name": "Pandemien",
        "difficulty": 3,
        "stars": (styled("★★★", Color.BRIGHT_YELLOW) +
                 styled("☆☆", Color.GRAY)),
        "tagline": "En ny virus lukker Danmark ned",
        "intro": (
            "En ny, aggressiv virus dukker op i Sydøstasien og "
            "spreder sig med foruroligende hastighed. På tre uger "
            "er den nået Europa.\n\n"
            "WHO erklærer pandemi. EU-landene lukker grænser. "
            "I Danmark stiger smittetallene eksponentielt.\n\n"
            "Statsministeren holder pressemøde klokken 20:00: "
            "\"Vi lukker Danmark ned fra i morgen.\""
        ),
        "days": [day1, day2, day3],
        "curveball": curveball,
    }
