# 3 Døgn — Kan din familie klare sig?

Et terminalbaseret refleksionsspil om kriseberedskab i hjemmet.

Spillet sætter din familie i realistiske krisescenarier og stiller spørgsmål der får jer til at tænke over, hvor godt I er forberedt på at klare jer selv i mindst 3 døgn — uden strøm, vand, internet eller hjælp udefra.

## Hvad handler det om?

Danske myndigheder anbefaler at alle husstande kan klare sig selv i mindst 3 døgn under en krise. Men hvor mange har faktisk tænkt det igennem?

**3 Døgn** er et familieværktøj der hjælper jer med at finde ud af det — på en engagerende måde.

## Scenarier

| # | Scenarie | Sværhedsgrad | Varighed |
|---|----------|-------------|----------|
| 1 | Vinterstormen | ★☆☆☆☆ | 3 dage |
| 2 | Oversvømmelsen | ★★☆☆☆ | 3+1 dage |
| 3 | Pandemien | ★★★☆☆ | 3+2 dage |
| 4 | Cyberangrebet | ★★★★☆ | 3+2 dage |
| 5 | Mørkelægning | ★★★★★ | 3+3 dage |

Hvert scenarie tilpasser sig jeres husstand — antal personer, børn, kæledyr, boligtype, beliggenhed og medicinske behov.

## Sådan spiller I

### Krav

- Python 3.10+
- En terminal der understøtter ANSI-farver (de fleste moderne terminaler)
- Ingen eksterne afhængigheder

### Kør spillet

```bash
# Klon projektet
git clone https://github.com/Reventlow/parat.git
cd parat

# Kør spillet
python3 3doegn.py

# Eller via launcher-scriptet
./3doegn
```

### Spillets forløb

1. **Husstandsprofil** — I fortæller om jeres husstand (antal personer, børn, kæledyr, bolig, beliggenhed)
2. **Vælg scenarie** — Vælg en krise at spille igennem
3. **Dag for dag** — I oplever krisen dag for dag med begivenheder og refleksionsspørgsmål
4. **Curveball** — Nogle scenarier forlænger krisen ud over 3 dage
5. **Beredskabsprofil** — I får en opsummering af jeres beredskab med konkrete anbefalinger

### Svar

Spørgsmål besvares med:
- **J** (ja) — I er forberedt på dette
- **N** (nej) — I er ikke forberedt
- **D** (delvist) — I har noget, men måske ikke nok

## Beredskabskategorier

Spillet vurderer jer inden for 10 kategorier:

- **Drikkevand** — 3 liter per person per dag
- **Mad & Forsyninger** — Langtidsholdbar mad til 3+ dage
- **Varme & Ly** — Tæpper, soveposer, alternativ opvarmning
- **Førstehjælp & Medicin** — Førstehjælpskasse, basismedicin, daglig medicin
- **Kommunikation & Info** — FM-radio, powerbank, mødested
- **Hygiejne** — Håndsprit, toiletløsninger uden vand
- **Lys & Strøm** — Lommelygter, stearinlys, batterier
- **Kontanter & Dokumenter** — Kontanter, vigtige papirer samlet
- **Moral & Aktiviteter** — Brætspil, rutiner, familiesamtaler
- **Planlægning** — Familieplan, evakueringsrute, nabonetværk

## Projektstruktur

```
parat/
├── 3doegn             # Bash launcher
├── 3doegn.py          # Hovedprogram (titel, menu, game loop)
├── engine.py          # Terminal-hjælpere, dataklasser, spilmotor
├── summary.py         # Opsummering, anbefalinger, afslutning
└── scenarios/
    ├── __init__.py          # Scenarie-register
    ├── vinterstormen.py     # ★☆☆☆☆
    ├── oversvommelsen.py    # ★★☆☆☆
    ├── pandemien.py         # ★★★☆☆
    ├── cyberangrebet.py     # ★★★★☆
    └── moerkelaegning.py    # ★★★★★
```

## Tilføj et nyt scenarie

1. Opret en ny fil i `scenarios/`, f.eks. `scenarios/jordskælv.py`
2. Implementer en `build_scenario(h: Household) -> dict` funktion (se eksisterende scenarier)
3. Tilføj import og registrering i `scenarios/__init__.py`

## Udviklet af

[SynTech.dk](https://syntech.dk) — Digital suverænitet og kriseberedskab

## Licens

MIT — se [LICENSE](LICENSE)
