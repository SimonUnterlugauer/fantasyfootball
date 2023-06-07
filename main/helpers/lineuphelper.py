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
team = [
    "Patrick Mahomes",
    "Travis Kelce",
    "Justin Jefferson",
    "Austin Ekeler",
    "Nick Chubb",
    "Jaylen Hurts",
    "Cooper Kupp",
    "Derrick Henry",
    "George Kittle"
]
def find_best_lineup(team, week, maxPosition):
    for player in team:
        drafthelper.get_player_position(player)
        drafthelper.calculate_weekly_score(player, week, 0.5)


find_best_lineup()