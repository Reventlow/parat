"""
Scenarie 4: Cyberangrebet
Sværhedsgrad: ★★★★☆ (Svær)

Et koordineret cyberangreb rammer dansk kritisk infrastruktur.
Strøm, vand, betalingssystemer og kommunikation falder.
Curveball: +2 dage.
"""

from engine import Color, styled, Household


def build_scenario(h: Household) -> dict:
    """Build the Cyberangrebet scenario adapted to household."""

    # ─── DAG 1 ───

    day1_events = []

    day1_events.append({
        "title": "Infrastruktur kollapser",
        "narrative": (
            "Det starter om morgenen. Først blinker lyset. Så "
            "forsvinder det helt. Men det er ikke en normal "
            "strømafbrydelse — hele nabolag, hele byer mister "
            "strømmen samtidig. Mobilnettet er overbelastet. "
            "Internettet er nede. Bankernes systemer er kollapset."
        ),
        "news": (
            "BREAKING: Et koordineret cyberangreb har ramt dansk "
            "kritisk infrastruktur. Energinet, vandforsyninger og "
            "betalingssystemer er kompromitteret. Forsvarsministeriet "
            "holder krisemøde."
        ),
        "questions": [
            ("Har I kontanter derhjemme — mønter og små sedler?",
             "penge"),
            ("Kender I PIN-koden til jeres betalingskort udenad, "
             "uden at slå den op digitalt?", "penge"),
        ],
    })

    e2_questions = [
        ("Har I en batteridrevet eller håndsving FM-radio?",
         "komm"),
        ("Har I aftalt et mødested med familien "
         "hvis I bliver adskilt og ikke kan ringe?", "plan"),
    ]

    # Household-specific: children emergency communication
    if h.has_children:
        e2_questions.append(
            ("Ved jeres børn hvordan man ringer 112?", "komm"))
        e2_questions.append(
            ("Har I en plan for hvem der henter børnene fra "
             "skole/institution hvis krisen rammer midt på dagen?",
             "plan"))

    day1_events.append({
        "title": "Kommunikation nede",
        "narrative": (
            "Mobilnettet fungerer sporadisk. Du kan sende en SMS, "
            "men opkald går sjældent igennem. Internettet er helt "
            "nede. Du aner ikke hvad der foregår — er det et angreb? "
            "En teknisk fejl? Noget værre?"
        ),
        "questions": e2_questions,
        "think": (
            "Tænk over: Uden internet og mobil er FM-radio den "
            "eneste pålidelige nyhedskilde. Har I en? Virker den?"
        ),
    })

    e3_text = (
        "Strømmen er stadig væk om aftenen. Ingen ved hvornår "
        "den kommer igen. Hele Danmark er ramt. "
    )
    if h.is_apartment:
        e3_text += (
            "I lejligheden er der ingen alternativ opvarmning. "
            "Elevatoren virker ikke. Vandtrykket falder."
        )
    elif h.housing == "landejendom":
        e3_text += (
            "Uden strøm har I ingen opvarmning — medmindre I "
            "har brændeovn. Det er koldt udenfor."
        )
    else:
        e3_text += (
            "Uden strøm har I ingen opvarmning. Det er koldt "
            "udenfor, og temperaturen indendørs falder."
        )

    day1_events.append({
        "title": "Mørke Danmark",
        "narrative": e3_text,
        "questions": [
            ("Har I lommelygter, stearinlys og batterier?", "lys"),
            ("Har I varmt tøj og ekstra tæpper til alle?", "varme"),
        ],
    })

    day1 = {
        "title": "Dag 1: Angrebet",
        "intro": ("Et koordineret cyberangreb rammer Danmark. "
                  "Alt det I tager for givet, forsvinder."),
        "events": day1_events,
    }

    # ─── DAG 2 ───

    day2_events = []

    day2_events.append({
        "title": "Vandforsyningen svigter",
        "narrative": (
            "Dag 2 starter med en ny chok-melding via FM-radioen: "
            "Vandpumpestationer er også ramt af angrebet. "
            "Vandtrykket falder over hele området. "
            "Du åbner vandhanen — der kommer en tynd stråle, "
            "så ingenting."
        ),
        "questions": [
            (f"Har I drikkevand nok til alle {h.total_people} "
             f"i husstanden? I har brug for ca. "
             f"{h.water_per_day:.0f} liter om dagen.", "vand"),
            ("Har I fyldt badekar, spande eller dunke med vand, "
             "mens I stadig kunne?", "vand"),
        ],
        "radio": (
            "\"...vandforsyningen er ramt i flere regioner. "
            "Borgere opfordres til at spare på vand og koge "
            "alt drikkevand, hvis det stadig løber...\""
        ),
    })

    e5_questions = [
        ("Har I mad der kan holde sig uden køling?", "mad"),
        ("Har I kontanter nok til at købe nødvendige "
         "forsyninger?", "penge"),
    ]

    # Household-specific: pet food when shops are closed
    if h.has_pets:
        e5_questions.append(
            ("Har I foder nok til jeres kæledyr til mindst 3 dage?",
             "mad"))

    # Household-specific: infant supplies without shops
    if h.has_infants:
        e5_questions.append(
            ("Har I babymad, bleer, modermælkserstatning og andre "
             "nødvendigheder til den lille på lager til mindst "
             "3 dage?", "mad"))

    day2_events.append({
        "title": "Fordærvet mad",
        "narrative": (
            "Maden i køleskabet er fordærvet. Fryseren har tøet "
            "helt op. Uden betalingssystemer kan I ikke bruge kort "
            "i de få butikker der er åbne — kun kontanter."
        ),
        "questions": e5_questions,
        "think": (
            "Tænk over: I et moderne samfund er vi fuldstændig "
            "afhængige af digitale systemer. Hvad ville I gøre, "
            "hvis MobilePay, Dankort og netbank var nede i en uge?"
        ),
    })

    day2 = {
        "title": "Dag 2: Kaskadeeffekt",
        "intro": "Angrebet spreder sig. System efter system svigter.",
        "events": day2_events,
    }

    # ─── DAG 3 ───

    day3_events = []

    day3_events.append({
        "title": "12 grader indendørs",
        "narrative": (
            "Tredje dag uden strøm, vand og internet. "
            "Forsvarsministeriet melder via radio at man arbejder "
            "på at genoprette systemer, men kan ikke give "
            "tidshorisont. Temperaturen i huset er faldet "
            "til 12 grader."
        ),
        "questions": [
            ("Har I en strategi for at holde varmen uden strøm "
             "— tæpper, soveposer, isolering af ét rum?", "varme"),
        ],
    })

    if h.has_medication_needs:
        day3_events.append({
            "title": "Medicin slipper op",
            "narrative": (
                "Nogen i husstanden tager daglig medicin. "
                "Apotekerne har lukket — ingen strøm, ingen "
                "systemer. Medicinen er ved at slippe op."
            ),
            "questions": [
                ("Har I altid mindst en uges ekstra medicin "
                 "på lager?", "forste"),
                # Household-specific: medication documentation
                ("Har I en liste over den medicin der tages i "
                 "husstanden — dosis og præparatnavn?", "forste"),
            ],
        })

    moral_text = (
        "Uden information er rygterne begyndt at sprede sig. "
        "Nogen siger det er Rusland. Andre siger det er en test. "
        "Ingen ved hvad der er sandt. "
    )
    if h.has_children:
        moral_text += ("Børnene er bange og forstår ikke hvad "
                       "der sker. ")
    moral_text += ("Folk er nervøse. Stemningen i kvarteret er "
                   "anspændt.")

    moral_questions = [
        ("Har I talt med familien om hvad I gør i en "
         "alvorlig krise?", "plan"),
        ("Har I aktiviteter der kan holde familien "
         "beskæftiget og humøret oppe?", "moral"),
    ]

    # Household-specific: children emergency conversation
    if h.has_children:
        moral_questions.append(
            ("Har I talt med børnene om hvad man gør i en "
             "nødsituation — alderstilpasset?", "plan"))

    # Household-specific: older children as helpers
    if h.has_children and any(a >= 10 for a in h.child_ages):
        moral_questions.append(
            ("Kan jeres større børn hjælpe med praktiske opgaver "
             "under krisen?", "plan"))

    # Household-specific: rural isolation
    if h.is_rural:
        moral_questions.append(
            ("I bor isoleret — har I aftalt med naboer at tjekke "
             "op på hinanden?", "plan"))

    day3_events.append({
        "title": "Rygter og frygt",
        "narrative": moral_text,
        "questions": moral_questions,
    })

    day3 = {
        "title": "Dag 3: Ingen ende i sigte",
        "intro": "Tredje dag. Kulden bider. Informationen er sparsom.",
        "events": day3_events,
    }

    # ─── CURVEBALL ───

    # Build curveball day 4 questions conditionally
    cb_d4_questions = [
        ("Har I stadig drikkevand nok?", "vand"),
        ("Har I stadig mad nok?", "mad"),
        ("Har I stadig brændstof til opvarmning "
         "eller varmt tøj nok?", "varme"),
    ]

    # Household-specific: infant warmth in extended cold crisis
    if h.has_infants:
        cb_d4_questions.append(
            ("Har I varmt tøj og ekstra tæpper specifikt til "
             "den lille?", "varme"))

    # Household-specific: pet food running low
    if h.has_pets:
        cb_d4_questions.append(
            ("Har I stadig foder nok til jeres kæledyr?", "mad"))

    # Build curveball day 5 questions conditionally
    cb_d5_questions = [
        ("Kender I jeres naboer godt nok til at "
         "organisere fælles hjælp?", "plan"),
        ("Har I ressourcer I kunne dele med "
         "andre?", "mad"),
    ]

    # Household-specific: dog walking during extended crisis
    if h.has_pets and "hund" in h.pet_types:
        cb_d5_questions.append(
            ("Har I tænkt over hvordan I lufter/motionerer jeres "
             "hund under krisen?", "plan"))

    curveball = {
        "narrative": (
            "Forsvarsministeriet melder at genopretningen tager "
            "længere end forventet. Angrebet var mere omfattende "
            "end først antaget. Strøm og vand forventes tidligst "
            "genoprettet om 2-3 dage. \"Vi opfordrer alle borgere "
            "til at hjælpe hinanden.\""
        ),
        "extra_days": 2,
        "day_events": [
            {
                "title": "Dag 4: Udholdenhedsprøve",
                "intro": "Fjerde dag uden strøm, vand og internet.",
                "events": [{
                    "title": "Ressourcetjek",
                    "narrative": (
                        f"Dag 4 uden basale forsyninger. "
                        f"Med {h.total_people} personer er "
                        "ressourcerne ved at slippe op."
                    ),
                    "questions": cb_d4_questions,
                }],
            },
            {
                "title": "Dag 5: Fællesskab eller kaos",
                "intro": "Femte dag. Det handler om sammenhold nu.",
                "events": [{
                    "title": "Nabohjælp",
                    "narrative": (
                        "Nogle naboer begynder at organisere sig — "
                        "dele mad, vand og information. Andre har "
                        "lukket sig inde. En ældre nabo har ikke "
                        "været set i to dage."
                    ),
                    "questions": cb_d5_questions,
                    "think": (
                        "Tænk over: I en langvarig krise er "
                        "fællesskab ofte den vigtigste ressource. "
                        "Har I et netværk I kan trække på?"
                    ),
                }],
            },
        ],
    }

    return {
        "name": "Cyberangrebet",
        "difficulty": 4,
        "stars": (styled("★★★★", Color.BRIGHT_YELLOW) +
                 styled("☆", Color.GRAY)),
        "tagline": "Hackere lammer dansk infrastruktur",
        "intro": (
            "Torsdag morgen klokken 07:14 begynder det. "
            "Et koordineret cyberangreb — det mest avancerede "
            "Europa nogensinde har set — rammer dansk kritisk "
            "infrastruktur.\n\n"
            "Strøm. Vand. Betalingssystemer. Telekommunikation. "
            "Det hele falder som dominobrikker.\n\n"
            "Inden for en time er Danmark kastet tilbage til en "
            "tilværelse uden de systemer, vi tager for givet "
            "hver eneste dag."
        ),
        "days": [day1, day2, day3],
        "curveball": curveball,
    }
