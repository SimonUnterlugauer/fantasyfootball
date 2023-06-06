import sys

import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

sys.path.append("../helpers")  # Add the parent directory to the Python path
import drafthelper

drafthelper.get_opponents_strength("Patrick Mahomes", "week_3")

def find_best_lineup(team, opponent, week):
    for player in team:
        drafthelper.get_opponents_strength(player, week)