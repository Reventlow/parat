"""
Parat — Summary and Recommendations

Generates the post-game preparedness profile and actionable advice.
"""

from engine import (
    Color, styled, strip_ansi, get_width, clear_screen,
    print_box, print_double_box, print_centered,
    wrap_text, press_enter, get_yes_no,
    Household, PrepTracker,
)


RECOMMENDATIONS = {
    "vand": [
        "Hav altid mindst 3 liter drikkevand per person per dag "
        "— til minimum 3 dage",
        "Opbevar vand i rene, forseglede beholdere "
        "(PET-flasker holder sig i årevis)",
        "Husk vand til kæledyr (ca. 0.5 liter per dyr per dag)",
        "Overvej toilet-situationen: spande med låg og poser "
        "kan bruges som nødtoilet",
    ],
    "mad": [
        "Hav langtidsholdbar mad til mindst 3 dage: dåsemad, "
        "pasta, ris, knækbrød, nødder",
        "Hav en manuel dåseåbner",
        "Tænk over mad der kan spises UDEN opvarmning",
        "Husk specialkost: babymad, allergier, diætkrav",
        "Roter jeres nødlager — spis det ældste og køb nyt",
    ],
    "varme": [
        "Hav ekstra tæpper, soveposer og varmt tøj klar til alle",
        "Planlæg at isolere ét rum og samle familien der",
        "ALDRIG brug grill, gasblus eller åben ild til opvarmning "
        "indendørs — CO-forgiftning dræber",
        "Overvej brændeovn hvis I har mulighed",
    ],
    "forste": [
        "Anskaf en god førstehjælpskasse og tjek den hvert halvår",
        "Tag et førstehjælpskursus — hele familien. "
        "Røde Kors udbyder kurser",
        "Hav altid mindst 1 uges ekstra medicin på lager "
        "for dem der tager daglig medicin",
        "Hav basismedicin: smertestillende, febersænkende, "
        "plaster, forbindinger",
        "Hav jodtabletter til alle under 40 år",
    ],
    "komm": [
        "Anskaf en batteridrevet eller håndsving FM-radio "
        "— jeres livline til omverdenen",
        "Hav altid en opladt powerbank (eller to)",
        "Kend DR P1 frekvensen i jeres område (beredskabskanal)",
        "Aftal et fysisk mødested med familien hvis I bliver "
        "adskilt og ikke kan ringe",
    ],
    "hygiejne": [
        "Hav håndsprit, vådservietter og toiletpapir på lager",
        "Hav bleer, bind eller andre nødvendige hygiejneartikler",
        "Plastikposer og spande med låg kan bruges som nødtoilet",
        "Overvej hygiejne uden rindende vand "
        "— det er en reel udfordring",
    ],
    "lys": [
        "Hav lommelygter med friske batterier (tjek halvårligt)",
        "Hav stearinlys og tændstikker — men pas på brand!",
        "Hav ekstra batterier i de størrelser I bruger",
        "En eller to gode powerbanks kan holde telefoner "
        "kørende i dagevis",
    ],
    "penge": [
        "Hav altid kontanter derhjemme "
        "— mønter og små sedler (500-1000 kr)",
        "Kend PIN-koden til jeres betalingskort udenad",
        "Hav vigtige dokumenter samlet ét sted: "
        "pas, forsikring, sundhedskort, recepter",
        "Overvej en fysisk kopi af vigtige telefonnumre",
    ],
    "moral": [
        "Hav brætspil, kortspil, bøger og puslespil klar",
        "Tænk over aktiviteter for alle aldersgrupper i familien",
        "Faste rutiner og små ritualer hjælper med at holde "
        "humøret oppe",
        "Tal åbent om situationen — også med børn (alderstilpasset)",
    ],
    "plan": [
        "Lav en familieplan: Hvem gør hvad i en krise?",
        "Aftal et mødested hvis I bliver adskilt",
        "Kend evakueringsruter fra jeres område",
        "Pak en nødtaske med det vigtigste "
        "(dokumenter, medicin, tøj, vand, snacks)",
        "Tal med naboerne om at hjælpe hinanden "
        "— fællesskab er nøglen",
        "Gennemgå og opdater jeres plan hvert halve år",
    ],
}


def show_summary(tracker: PrepTracker, h: Household,
                 scenario_name: str):
    """Show the final preparedness summary."""
    clear_screen()
    print()

    overall = tracker.get_overall()

    print_double_box([
        "",
        styled(f"  Scenarie: {scenario_name}", Color.WHITE),
        styled(f"  Husstand: {h.total_people} personer, "
               f"{h.housing_display}, {h.location_display}", Color.DIM),
        "",
    ], title="JERES BEREDSKABSPROFIL", color=Color.CYAN)
    print()

    # Category bars
    w = get_width() - 8
    bar_width = min(20, w - 40)
    cat_lines = []

    for cat, (score, max_score) in tracker.scores.items():
        if max_score == 0:
            continue
        pct = int(score * 100 / max_score)
        name = tracker.CATEGORY_NAMES[cat]

        filled = int(bar_width * pct / 100)
        empty = bar_width - filled

        if pct >= 70:
            bar_color = Color.BRIGHT_GREEN
            pct_color = Color.GREEN
        elif pct >= 40:
            bar_color = Color.BRIGHT_YELLOW
            pct_color = Color.YELLOW
        else:
            bar_color = Color.BRIGHT_RED
            pct_color = Color.RED

        bar = (f"{bar_color}{'█' * filled}"
               f"{Color.GRAY}{'░' * empty}{Color.RESET}")
        name_padded = f"{name:<24}"
        pct_str = styled(f"{pct:3d}%", pct_color)
        cat_lines.append(
            f"  {styled(name_padded, Color.CYAN)} {bar}  {pct_str}")

    print_box(cat_lines, title="KATEGORIER", color=Color.BLUE)
    print()

    # Overall bar
    filled = int(bar_width * overall / 100)
    empty = bar_width - filled
    if overall >= 70:
        ov_color = Color.BRIGHT_GREEN
    elif overall >= 40:
        ov_color = Color.BRIGHT_YELLOW
    else:
        ov_color = Color.BRIGHT_RED

    ov_bar = (f"{ov_color}{'█' * filled}"
              f"{Color.GRAY}{'░' * empty}{Color.RESET}")
    overall_line = (
        f"  {styled('SAMLET BEREDSKAB:        ', Color.BOLD, Color.WHITE)}"
        f" {ov_bar}  {styled(f'{overall}%', ov_color)}"
    )
    print_box(["", overall_line, ""], color=Color.MAGENTA)
    print()

    # Assessment text
    if overall >= 80:
        assessment = (
            "I er godt forberedt! Jeres familie har et solidt "
            "fundament til at klare en krise. Fortsæt det gode "
            "arbejde og husk at vedligeholde jeres beredskab."
        )
        assess_color = Color.GREEN
    elif overall >= 60:
        assessment = (
            "I har en god start, men der er plads til forbedring. "
            "Med lidt ekstra forberedelse kan I stå meget stærkere."
        )
        assess_color = Color.BRIGHT_GREEN
    elif overall >= 40:
        assessment = (
            "I har nogle dele på plads, men der er vigtige huller "
            "i jeres beredskab. Det kræver ikke meget at lukke dem."
        )
        assess_color = Color.YELLOW
    elif overall >= 20:
        assessment = (
            "Jeres beredskab har brug for opmærksomhed. "
            "En krise ville ramme jer hårdt lige nu. "
            "Men det er aldrig for sent at starte."
        )
        assess_color = Color.BRIGHT_RED
    else:
        assessment = (
            "I er sårbare. En krise ville være meget svær at "
            "håndtere med jeres nuværende forberedelse. "
            "Men husk: Selv små skridt gør en stor forskel."
        )
        assess_color = Color.RED

    lines = wrap_text(assessment, w - 4)
    colored_lines = [styled(line, assess_color) for line in lines]
    print_box([""] + colored_lines + [""],
              title="VURDERING", color=Color.GREEN)
    print()
    press_enter()


def show_recommendations(tracker: PrepTracker):
    """Show specific recommendations based on weak areas."""
    clear_screen()
    print()

    all_cats = [(cat, tracker.get_pct(cat))
                for cat in tracker.scores
                if tracker.scores[cat][1] > 0]
    all_cats.sort(key=lambda x: x[1])

    weak = [cat for cat, pct in all_cats if pct < 60]

    print_double_box([
        "",
        styled("  Baseret på jeres svar, er her de vigtigste",
               Color.WHITE),
        styled("  ting I kan gøre for at styrke jeres beredskab.",
               Color.WHITE),
        "",
    ], title="HVAD KAN I GØRE NU?", color=Color.CYAN)
    print()

    if not weak:
        print_box([
            "",
            styled("  I ser ud til at have styr på det meste!",
                   Color.GREEN),
            styled("  Her er alligevel nogle tips til "
                   "vedligeholdelse:", Color.DIM),
            "",
        ], color=Color.GREEN)
        print()
        general_tips = [
            "Tjek jeres beredskab hvert halve år "
            "— udskift mad, batterier, medicin",
            "Tal med naboerne om gensidig hjælp i "
            "krisesituationer",
            "Øv jeres familieplan — gennemgå den "
            "sammen mindst en gang om året",
        ]
        for i, tip in enumerate(general_tips, 1):
            lines = wrap_text(tip, get_width() - 14)
            print(f"    {styled(f'{i}.', Color.BRIGHT_CYAN)} "
                  f"{styled(lines[0], Color.WHITE)}")
            for line in lines[1:]:
                print(f"       {styled(line, Color.WHITE)}")
            print()
    else:
        shown = 0
        tip_num = 1
        for cat, pct in all_cats:
            if shown >= 5:
                break
            if cat not in RECOMMENDATIONS:
                continue
            cat_name = tracker.CATEGORY_NAMES[cat]

            if pct >= 70:
                pct_color = Color.GREEN
            elif pct >= 40:
                pct_color = Color.YELLOW
            else:
                pct_color = Color.RED

            print(f"    {styled(cat_name, Color.BOLD, Color.CYAN)} "
                  f"({styled(f'{pct}%', pct_color)})")
            print()

            tips = RECOMMENDATIONS[cat]
            for tip in tips[:3]:
                lines = wrap_text(tip, get_width() - 14)
                print(f"      {styled(f'{tip_num}.', Color.BRIGHT_CYAN)}"
                      f" {styled(lines[0], Color.WHITE)}")
                for line in lines[1:]:
                    print(f"         {styled(line, Color.WHITE)}")
                tip_num += 1
            print()
            shown += 1

    print()
    press_enter()


def show_closing():
    """Show the closing message."""
    clear_screen()
    print()

    closing_lines = [
        "",
        styled("  Det handler ikke om frygt.", Color.BOLD, Color.WHITE),
        styled("  Det handler om ansvar.", Color.BOLD, Color.WHITE),
        "",
        styled("  Et par timers forberedelse i dag kan gøre",
               Color.DIM),
        styled("  en kæmpe forskel for jeres familie i morgen.",
               Color.DIM),
        "",
        styled("  Start i dag:", Color.CYAN),
        styled("  - Køb vand og langtidsholdbar mad til 3 dage",
               Color.WHITE),
        styled("  - Pak en nødtaske med det vigtigste",
               Color.WHITE),
        styled("  - Anskaf en FM-radio og lommelygte",
               Color.WHITE),
        styled("  - Lav en familieplan og tal den igennem",
               Color.WHITE),
        styled("  - Lær basis førstehjælp",
               Color.WHITE),
        "",
        styled("  Del gerne dette spil med andre familier.",
               Color.DIM),
        "",
    ]
    print_double_box(closing_lines,
                     title="TAK FORDI I SPILLEDE", color=Color.CYAN)
    print()

    print_centered(styled("Udviklet af SynTech.dk", Color.DIM))
    print_centered(styled("Digital suverænitet og kriseberedskab",
                          Color.DIM))
    print()
    print()
