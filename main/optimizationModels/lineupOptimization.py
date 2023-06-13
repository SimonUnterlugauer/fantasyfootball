import sys

import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

sys.path.append("../helpers")  # Add the parent directory to the Python path
import lineuphelper


team = ["Patrick Mahomes", "Jalen Hurts","Josh Jacobs", "Austin Ekeler", "Davante Adams", "Stefon Diggs",
        "Cooper Kupp", "Justin Jefferson", "Nick Chubb", "Saquon Barkley", "Travis Kelce", "George Kittle", "PHI", "LV",
        "Justin Tucker"]
lineuphelper.find_optimal_lineup(team, "week_12", 0.5)