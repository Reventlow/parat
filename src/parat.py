#!/usr/bin/env python3
"""
Parat — Familieberedskab Simulering

Et terminalbaseret refleksionsspil om kriseberedskab i hjemmet.
Spillere konfronteres med realistiske krisescenarier og reflekterer
over deres families beredskab.

Udviklet af SynTech.dk

Usage:
    python3 parat.py

No external dependencies required — uses Python standard library only.
"""

import sys
import random
import time

from engine import (
    Color, styled, clear_screen, print_centered, print_box,
    print_double_box, get_input, get_yes_no, press_enter,
    setup_household, run_scenario,
)
from scenarios import SCENARIO_BUILDERS
from summary import show_summary, show_recommendations, show_closing


def show_title():
    """Show the game title screen."""
    clear_screen()
    print()
    print()

    title_art = [
        "",
        styled("─── ─── ─── ─── ─── ─── ─── ─── ─── ───",
               Color.DIM),
        "",
        styled("╺━━━━━━━━━━━━━━━╸",
               Color.BRIGHT_RED),
        "",
        styled("P A R A T",
               Color.BOLD, Color.BRIGHT_WHITE),
        "",
        styled("╺━━━━━━━━━━━━━━━╸",
               Color.BRIGHT_RED),
        "",
        styled("Kan din familie klare sig?",
               Color.CYAN),
        "",
        styled("─── ─── ─── ─── ─── ─── ─── ─── ─── ───",
               Color.DIM),
        "",
        styled("Et beredskabsspil for hele familien",
               Color.DIM),
        styled("Udviklet af SynTech.dk",
               Color.DIM),
        "",
        styled("Vi gemmer ikke jeres svar.",
               Color.DIM),
        styled("Vi indsamler ingen data.",
               Color.DIM),
        "",
        styled("Kildekode: github.com/Reventlow/parat",
               Color.DIM),
        "",
    ]
    for line in title_art:
        print_centered(line)
        time.sleep(0.08)

    print()
    press_enter()


def show_scenario_menu(h):
    """Show scenario selection menu and return chosen scenario."""
    scenarios = [builder(h) for builder in SCENARIO_BUILDERS]

    clear_screen()
    print()
    print_box([
        "",
        styled("  Vælg et krisescenarie at spille igennem.",
               Color.WHITE),
        styled("  Sværhedsgraden bestemmer krisens omfang.",
               Color.DIM),
        "",
    ], title="VÆLG SCENARIE", color=Color.CYAN)
    print()

    for i, sc in enumerate(scenarios, 1):
        stars = sc["stars"]
        name = styled(sc["name"], Color.BOLD, Color.WHITE)
        tag = styled(sc["tagline"], Color.DIM)
        print(f"    {styled(f'[{i}]', Color.BRIGHT_CYAN)}"
              f"  {name}  {stars}")
        print(f"         {tag}")
        print()

    print(f"    {styled('[T]', Color.BRIGHT_CYAN)}  "
          f"{styled('Tilfældigt scenarie', Color.WHITE)}")
    print()

    while True:
        val = get_input("Vælg scenarie: ").lower()
        if val == "q":
            sys.exit(0)
        if val == "t":
            return random.choice(scenarios)
        try:
            n = int(val)
            if 1 <= n <= len(scenarios):
                return scenarios[n - 1]
        except ValueError:
            pass
        print(f"    {styled('Vælg 1-5 eller T for tilfældig.', Color.RED)}")


def main():
    """Main game loop."""
    try:
        show_title()
        h = setup_household()

        while True:
            scenario = show_scenario_menu(h)
            tracker = run_scenario(scenario, h)
            show_summary(tracker, h, scenario["name"])
            show_recommendations(tracker)
            show_closing()

            print()
            if not get_yes_no("Vil I prøve et andet scenarie? (J/N) "):
                break

        clear_screen()
        print()
        print_centered(
            styled("Farvel — og husk: Forberedelse er omsorg.",
                   Color.CYAN))
        print()

    except KeyboardInterrupt:
        print()
        print()
        print_centered(styled("Spillet afsluttet.", Color.DIM))
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
