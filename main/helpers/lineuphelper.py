import sys

import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

sys.path.append("../helpers")  # Add the parent directory to the Python path
import drafthelper

maxPosition = {
    "QB": 1,
    "RB": 3,
    "WR": 2,
    "TE": 1,
    "KI": 1,
    "DEF": 1,
}
def find_best_lineup(team, week, maxPosition):
    drafthelper.calculate_weekly_score("Patrick Mahomes", "week_18", 0.5)
