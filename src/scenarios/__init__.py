"""
Parat — Scenario Registry

Import and register all scenarios here.
To add a new scenario, create a new file in this package and add it to SCENARIO_BUILDERS.
"""

from scenarios.vinterstormen import build_scenario as _s1
from scenarios.oversvommelsen import build_scenario as _s2
from scenarios.pandemien import build_scenario as _s3
from scenarios.cyberangrebet import build_scenario as _s4
from scenarios.moerkelaegning import build_scenario as _s5

# Ordered list of scenario builder functions.
# Each takes a Household and returns a scenario dict.
# To add a new scenario, import its build_scenario and append here.
SCENARIO_BUILDERS = [_s1, _s2, _s3, _s4, _s5]
