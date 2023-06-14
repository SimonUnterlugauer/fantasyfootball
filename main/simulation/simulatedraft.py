import sys

import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

sys.path.append("../helpers")
sys.path.append("../optimizationModels") # Add the parent directory to the Python path
import draftsimulationhelper
import selectionOptimization
import drafthelper

def simulate_draft_round(num_teams, position, teams, already_drafted, maxPosition, currentNumber):
    already_drafted = already_drafted
    if len(teams) == 0:
        for i in range(num_teams):
            team_array = []
            teams.append(team_array)
    for i in range(num_teams):
        if i != position:
            #print(already_drafted)
            drafted_player = draftsimulationhelper.draft_player(already_drafted)
            teams[i].append(drafted_player)
            already_drafted.append(drafted_player)
        else:
            drafted_player = selectionOptimization.select_best_player(0.5, maxPosition, currentNumber[i], already_drafted)
            teams[i].append(drafted_player)
            already_drafted.append(drafted_player)
    return teams


def simulate_draft(num_teams, position, draft_rounds, maxPosition, currentNumber):
    already_drafted = ["Josef Stangel"]
    teams = []
    for i in range(draft_rounds):
        if i > 0:
            for y in range(len(teams)):
                for player in teams[y]:
                    #print(player)
                    already_drafted.append(player)
        teams = simulate_draft_round(num_teams, position, teams, already_drafted, maxPosition, currentNumber)
    print(teams)
    return teams

maxPosition = {
    "QB": 1,
    "RB": 3,
    "WR": 2,
    "TE": 1,
    "KI": 1,
    "DEF": 1,
}

current_number = {
    "QB": 0,
    "RB": 0,
    "WR": 0,
    "TE": 0,
    "KI": 0,
    "DEF": 0,
}

#drafthelper.get_player_position("Ja'Marr Chase")
#simulate_draft_round(6, 2, [], ["Josef Stangel"], maxPosition, [current_number, current_number, current_number, current_number, current_number, current_number])
simulate_draft(6, 2, 9, maxPosition, [current_number, current_number, current_number, current_number, current_number, current_number])






