"""
3 Døgn — Game Engine

Terminal helpers, data classes, and the core game loop.
"""

import os
import sys
import time
import textwrap
from dataclasses import dataclass, field
from typing import Optional


# =============================================================================
# ANSI Terminal Helpers
# =============================================================================

class Color:
    """ANSI escape code constants for terminal styling."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def get_width() -> int:
    """Get terminal width, capped at 100."""
    try:
        return min(os.get_terminal_size().columns, 100)
    except OSError:
        return 80


def clear_screen():
    """Clear the terminal screen."""
    print("\033[2J\033[H", end="", flush=True)


def styled(text: str, *styles: str) -> str:
    """Apply ANSI styles to text."""
    return "".join(styles) + text + Color.RESET


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes for length calculations."""
    import re
    return re.sub(r'\033\[[0-9;]*m', '', text)


def print_centered(text: str, width: Optional[int] = None):
    """Print text centered in the terminal."""
    w = width or get_width()
    for line in text.split("\n"):
        clean = strip_ansi(line)
        padding = max(0, (w - len(clean)) // 2)
        print(" " * padding + line)


def print_box(lines: list[str], title: str = "", color: str = Color.BLUE,
              width: Optional[int] = None):
    """Print text inside a Unicode box with optional title."""
    w = width or get_width() - 4
    inner = w - 2

    if title:
        title_display = f" {title} "
        remaining = inner - len(strip_ansi(title_display))
        left = remaining // 2
        right = remaining - left
        print(f"  {color}\u250c{'─' * left}{Color.BOLD}{Color.BRIGHT_CYAN}"
              f"{title_display}{Color.RESET}{color}{'─' * right}\u2510{Color.RESET}")
    else:
        print(f"  {color}\u250c{'─' * inner}\u2510{Color.RESET}")

    for line in lines:
        clean_len = len(strip_ansi(line))
        padding = max(0, inner - clean_len - 2)
        print(f"  {color}\u2502{Color.RESET} {line}{' ' * padding} {color}\u2502{Color.RESET}")

    print(f"  {color}\u2514{'─' * inner}\u2518{Color.RESET}")


def print_double_box(lines: list[str], title: str = "", color: str = Color.RED,
                     width: Optional[int] = None):
    """Print text inside a double-line Unicode box."""
    w = width or get_width() - 4
    inner = w - 2

    if title:
        title_display = f" {title} "
        remaining = inner - len(strip_ansi(title_display))
        left = remaining // 2
        right = remaining - left
        print(f"  {color}\u2554{'═' * left}{Color.BOLD}{Color.BRIGHT_WHITE}"
              f"{title_display}{Color.RESET}{color}{'═' * right}\u2557{Color.RESET}")
    else:
        print(f"  {color}\u2554{'═' * inner}\u2557{Color.RESET}")

    for line in lines:
        clean_len = len(strip_ansi(line))
        padding = max(0, inner - clean_len - 2)
        print(f"  {color}\u2551{Color.RESET} {line}{' ' * padding} {color}\u2551{Color.RESET}")

    print(f"  {color}\u255a{'═' * inner}\u255d{Color.RESET}")


def print_divider(char: str = "─", color: str = Color.GRAY):
    """Print a horizontal divider line."""
    w = get_width() - 4
    print(f"  {color}{char * w}{Color.RESET}")


def wrap_text(text: str, width: Optional[int] = None) -> list[str]:
    """Word-wrap text to fit within a given width."""
    w = width or get_width() - 8
    result = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            result.append("")
        else:
            result.extend(textwrap.wrap(paragraph, width=w))
    return result


def print_narrative(text: str):
    """Print narrative text with wrapping and slow reveal."""
    lines = wrap_text(text, get_width() - 8)
    for line in lines:
        print(f"    {styled(line, Color.WHITE)}")
        time.sleep(0.15)
    print()


def print_news(text: str):
    """Print a news bulletin box."""
    lines = wrap_text(text, get_width() - 16)
    print_double_box(lines, title="NYHEDSBULLETIN", color=Color.RED)
    print()


def print_radio(text: str):
    """Print a radio broadcast box."""
    lines = wrap_text(text, get_width() - 16)
    print_box(lines, title="FM RADIO", color=Color.YELLOW)
    print()


def print_think(text: str):
    """Print a reflection/think-about-it prompt."""
    w = get_width() - 8
    print()
    print(f"    {styled('┈' * (w - 4), Color.YELLOW)}")
    lines = wrap_text(text, w - 6)
    for line in lines:
        print(f"      {styled(line, Color.ITALIC, Color.YELLOW)}")
    print(f"    {styled('┈' * (w - 4), Color.YELLOW)}")
    print()


def get_input(prompt: str = "> ") -> str:
    """Get user input with a styled prompt."""
    try:
        return input(f"  {Color.BRIGHT_CYAN}{prompt}{Color.RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


def get_number(prompt: str, min_val: int = 0, max_val: int = 99) -> int:
    """Get a numeric input from the user."""
    while True:
        val = get_input(prompt)
        if val.lower() == "q":
            sys.exit(0)
        try:
            n = int(val)
            if min_val <= n <= max_val:
                return n
            print(f"    {styled(f'Indtast et tal mellem {min_val} og {max_val}.', Color.RED)}")
        except ValueError:
            print(f"    {styled('Indtast venligst et tal.', Color.RED)}")


def get_yes_no(prompt: str) -> bool:
    """Get a yes/no answer."""
    while True:
        val = get_input(prompt).lower()
        if val == "q":
            sys.exit(0)
        if val in ("j", "ja", "y", "yes"):
            return True
        if val in ("n", "nej", "no"):
            return False
        print(f"    {styled('Svar venligst J (ja) eller N (nej).', Color.RED)}")


def get_reflection(prompt: str) -> str:
    """Get a reflection answer: ja/nej/delvist."""
    lines = wrap_text(prompt, get_width() - 12)
    print()
    print_box(lines + ["", f"  {styled('[J]', Color.GREEN)} Ja   "
              f"{styled('[N]', Color.RED)} Nej   "
              f"{styled('[D]', Color.YELLOW)} Delvist"],
              color=Color.CYAN)
    while True:
        val = get_input("Jeres svar: ").lower()
        if val == "q":
            sys.exit(0)
        if val in ("j", "ja"):
            return "ja"
        if val in ("n", "nej"):
            return "nej"
        if val in ("d", "delvist"):
            return "delvist"
        print(f"    {styled('Svar J (ja), N (nej) eller D (delvist).', Color.RED)}")


def press_enter():
    """Wait for user to press Enter."""
    get_input(f"{Color.DIM}Tryk Enter for at fortsætte...{Color.RESET} ")


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Household:
    """Represents the player's household."""
    total_people: int = 1
    num_children: int = 0
    child_ages: list[int] = field(default_factory=list)
    num_pets: int = 0
    pet_types: list[str] = field(default_factory=list)
    housing: str = "villa"
    location: str = "forstad"
    distance_hospital_km: int = 5
    has_medication_needs: bool = False

    @property
    def has_children(self) -> bool:
        return self.num_children > 0

    @property
    def has_infants(self) -> bool:
        return any(a < 3 for a in self.child_ages)

    @property
    def has_small_children(self) -> bool:
        return any(a < 10 for a in self.child_ages)

    @property
    def has_pets(self) -> bool:
        return self.num_pets > 0

    @property
    def is_rural(self) -> bool:
        return self.location in ("mindre_by", "land")

    @property
    def is_apartment(self) -> bool:
        return self.housing == "lejlighed"

    @property
    def has_garden(self) -> bool:
        return self.housing in ("villa", "landejendom", "raekkehus")

    @property
    def water_per_day(self) -> float:
        return self.total_people * 3.0 + self.num_pets * 0.5

    @property
    def water_3_days(self) -> float:
        return self.water_per_day * 3

    @property
    def housing_display(self) -> str:
        return {"lejlighed": "lejlighed", "raekkehus": "rækkehus",
                "villa": "villa/parcelhus", "landejendom": "landejendom"}[self.housing]

    @property
    def location_display(self) -> str:
        return {"storby": "storby", "forstad": "forstad",
                "mindre_by": "mindre by", "land": "landområde"}[self.location]


@dataclass
class PrepTracker:
    """Tracks preparedness scores across categories."""
    scores: dict = field(default_factory=lambda: {
        "vand": [0, 0],
        "mad": [0, 0],
        "varme": [0, 0],
        "forste": [0, 0],
        "komm": [0, 0],
        "hygiejne": [0, 0],
        "lys": [0, 0],
        "penge": [0, 0],
        "moral": [0, 0],
        "plan": [0, 0],
    })

    CATEGORY_NAMES = {
        "vand": "Drikkevand",
        "mad": "Mad & Forsyninger",
        "varme": "Varme & Ly",
        "forste": "Førstehjælp & Medicin",
        "komm": "Kommunikation & Info",
        "hygiejne": "Hygiejne",
        "lys": "Lys & Strøm",
        "penge": "Kontanter & Dokumenter",
        "moral": "Moral & Aktiviteter",
        "plan": "Planlægning",
    }

    def record(self, category: str, answer: str):
        """Record an answer for a category."""
        if category not in self.scores:
            return
        self.scores[category][1] += 2
        if answer == "ja":
            self.scores[category][0] += 2
        elif answer == "delvist":
            self.scores[category][0] += 1

    def get_pct(self, category: str) -> int:
        s, m = self.scores[category]
        if m == 0:
            return -1
        return int(s * 100 / m)

    def get_overall(self) -> int:
        total_s = sum(s for s, m in self.scores.values() if m > 0)
        total_m = sum(m for s, m in self.scores.values() if m > 0)
        if total_m == 0:
            return 0
        return int(total_s * 100 / total_m)

    def get_weak_categories(self, threshold: int = 50) -> list[str]:
        weak = []
        for cat, (s, m) in self.scores.items():
            if m > 0 and (s * 100 / m) < threshold:
                weak.append(cat)
        return weak


# =============================================================================
# Household Setup
# =============================================================================

def setup_household() -> Household:
    """Interactive household setup."""
    h = Household()

    clear_screen()
    print()
    print_box([
        "",
        styled("  Lad os starte med at lære jeres husstand at kende.", Color.WHITE),
        styled("  Jeres svar tilpasser scenarierne til jeres situation.", Color.DIM),
        "",
    ], title="HUSSTANDSPROFIL", color=Color.CYAN)
    print()

    h.total_people = get_number("Hvor mange personer bor i husstanden? ", 1, 20)

    if h.total_people > 1:
        h.num_children = get_number("Hvor mange af dem er børn (under 18)? ",
                                    0, h.total_people - 1)
        if h.num_children > 0:
            print(f"    {styled('Angiv alder på hvert barn:', Color.DIM)}")
            for i in range(h.num_children):
                age = get_number(f"  Barn {i+1} alder: ", 0, 17)
                h.child_ages.append(age)

    if get_yes_no("Har I kæledyr? (J/N) "):
        h.num_pets = get_number("Hvor mange kæledyr? ", 1, 20)
        print(f"    {styled('Angiv type for hvert kæledyr (hund/kat/andet):', Color.DIM)}")
        for i in range(h.num_pets):
            ptype = get_input(f"  Kæledyr {i+1}: ").lower()
            if ptype in ("hund", "kat"):
                h.pet_types.append(ptype)
            else:
                h.pet_types.append("andet")

    print()
    print_box([
        f"  {styled('[1]', Color.CYAN)} Lejlighed",
        f"  {styled('[2]', Color.CYAN)} Rækkehus",
        f"  {styled('[3]', Color.CYAN)} Villa / Parcelhus",
        f"  {styled('[4]', Color.CYAN)} Landejendom",
    ], title="BOLIGTYPE", color=Color.BLUE)
    choice = get_number("Vælg boligtype: ", 1, 4)
    h.housing = ["lejlighed", "raekkehus", "villa", "landejendom"][choice - 1]

    print()
    print_box([
        f"  {styled('[1]', Color.CYAN)} Storby (København, Aarhus, Odense, Aalborg)",
        f"  {styled('[2]', Color.CYAN)} Forstad",
        f"  {styled('[3]', Color.CYAN)} Mindre by",
        f"  {styled('[4]', Color.CYAN)} Landområde / isoleret",
    ], title="BELIGGENHED", color=Color.BLUE)
    choice = get_number("Hvor bor I? ", 1, 4)
    h.location = ["storby", "forstad", "mindre_by", "land"][choice - 1]

    h.distance_hospital_km = get_number(
        "Ca. afstand til nærmeste skadestue (km)? ", 1, 200)

    h.has_medication_needs = get_yes_no(
        "Tager nogen i husstanden daglig medicin? (J/N) ")

    # Summary
    print()
    pets_str = ""
    if h.has_pets:
        pets_str = f", {h.num_pets} kæledyr"
    kids_str = ""
    if h.has_children:
        ages = ", ".join(str(a) for a in h.child_ages)
        kids_str = f" (heraf {h.num_children} børn, alder: {ages})"

    print_box([
        "",
        f"  {styled('Husstand:', Color.CYAN)} {h.total_people} personer{kids_str}{pets_str}",
        f"  {styled('Bolig:', Color.CYAN)} {h.housing_display}",
        f"  {styled('Beliggenhed:', Color.CYAN)} {h.location_display}",
        f"  {styled('Skadestue:', Color.CYAN)} {h.distance_hospital_km} km",
        f"  {styled('Daglig medicin:', Color.CYAN)} {'Ja' if h.has_medication_needs else 'Nej'}",
        f"  {styled('Vandbehov/dag:', Color.CYAN)} {h.water_per_day:.0f} liter "
        f"({h.water_3_days:.0f} liter for 3 dage)",
        "",
    ], title="JERES HUSSTAND", color=Color.GREEN)
    print()
    press_enter()

    return h


# =============================================================================
# Game Engine
# =============================================================================

def run_event(event: dict, h: Household, tracker: PrepTracker):
    """Run a single event within a day."""
    print()
    title = styled(f">> {event['title']}", Color.BOLD, Color.BRIGHT_YELLOW)
    print(f"    {title}")
    print_divider("┄", Color.YELLOW)
    print()

    print_narrative(event["narrative"])

    if "news" in event:
        print_news(event["news"])

    if "radio" in event:
        print_radio(event["radio"])

    for q_text, q_cat in event.get("questions", []):
        answer = get_reflection(q_text)
        tracker.record(q_cat, answer)

        if answer == "ja":
            print(f"    {styled('Godt.', Color.GREEN)} Det er I forberedt på.")
        elif answer == "delvist":
            print(f"    {styled('En start.', Color.YELLOW)} "
                  "Men overvej om det er nok til alle.")
        else:
            print(f"    {styled('Noteret.', Color.RED)} "
                  "Det er noget at tænke over.")
        print()

    if "think" in event:
        print_think(event["think"])
        press_enter()


def run_day(day: dict, h: Household, tracker: PrepTracker):
    """Run a full day of events."""
    clear_screen()
    print()

    title = styled(day["title"], Color.BOLD, Color.BRIGHT_WHITE)
    print_double_box([
        "",
        f"  {title}",
        f"  {styled(day['intro'], Color.DIM)}",
        "",
    ], title="═══", color=Color.MAGENTA)
    print()
    time.sleep(0.5)

    for event in day["events"]:
        run_event(event, h, tracker)

    print()
    print_divider("═", Color.MAGENTA)
    print(f"    {styled(day['title'] + ' er overstået.', Color.DIM)}")
    print()
    press_enter()


def run_curveball(curveball: dict, h: Household, tracker: PrepTracker):
    """Run the curveball extension."""
    clear_screen()
    print()

    alert_lines = [
        "",
        styled("  KRISEN FORTSÆTTER", Color.BOLD, Color.BRIGHT_RED),
        "",
        styled("  Dag 3 er forbi — men situationen", Color.WHITE),
        styled("  er langt fra overstået...", Color.WHITE),
        "",
    ]
    print_double_box(alert_lines, title="UVENTET UDVIKLING", color=Color.RED)
    print()
    time.sleep(1.0)

    print_narrative(curveball["narrative"])
    print()
    press_enter()

    for day_data in curveball["day_events"]:
        run_day(day_data, h, tracker)


def run_scenario(scenario: dict, h: Household) -> PrepTracker:
    """Run a complete scenario and return the tracker."""
    tracker = PrepTracker()

    # Show intro
    clear_screen()
    print()
    name = styled(scenario["name"], Color.BOLD, Color.BRIGHT_WHITE)
    stars = scenario["stars"]
    print_double_box([
        "",
        f"  {name}",
        f"  Sværhedsgrad: {stars}",
        "",
    ], title="SCENARIE", color=Color.RED)
    print()
    print_narrative(scenario["intro"])
    print()
    press_enter()

    for day in scenario["days"]:
        run_day(day, h, tracker)

    if scenario.get("curveball"):
        run_curveball(scenario["curveball"], h, tracker)

    return tracker
