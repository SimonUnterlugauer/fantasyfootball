import sys

import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

sys.path.append("../helpers")
sys.path.append("../optimizationModels") # Add the parent directory to the Python path
import draftsimulationhelper
import selectionOptimization
import drafthelper


def getPlayerCount(team):
    numPlayers =  {
        "QB": 0,
        "RB": 0,
        "WR": 0,
        "TE": 0,
        "KI": 0,
        "DEF": 0,
    }
    for player in team:
        position = drafthelper.get_player_position(player)
        numPlayers[position] += 1

    return numPlayers



def simulate_draft_round(num_teams, position, teams, already_drafted, maxPosition, currentNumber, way):
    already_drafted = already_drafted
    if len(teams) == 0:
        for i in range(num_teams):
            team_array = []
            teams.append(team_array)
    for i in range(num_teams):
        if (way == "right"):
            if i != position:
                #print(already_drafted)
                drafted_player = draftsimulationhelper.draft_player(already_drafted)
                teams[i].append(drafted_player)
                already_drafted.append(drafted_player)
            else:
                ### nächstes mal eine funktion die die anzahl meiner spieler zählt und maximale spieler aufstellt
                player_count = getPlayerCount(teams[i])
                #print(player_count)
                #print(maxPosition)
                drafted_player = selectionOptimization.select_best_player_alt(0.5, maxPosition, player_count, already_drafted)
                teams[i].append(drafted_player)
                already_drafted.append(drafted_player)
        if (way == "wrong"):
            if num_teams - (i+1) != position:
                drafted_player = draftsimulationhelper.draft_player(already_drafted)
                teams[num_teams- (i+1)].append(drafted_player)
                already_drafted.append(drafted_player)
            else:
                player_count = getPlayerCount(teams[num_teams- (i+1)])
                print(player_count)
                print(maxPosition)
                drafted_player = selectionOptimization.select_best_player_alt(0.5, maxPosition, player_count, already_drafted)
                teams[num_teams- (i+1)].append(drafted_player)
                already_drafted.append(drafted_player)
    return teams


def simulate_draft(num_teams, position, draft_rounds, maxPosition, currentNumber):
    already_drafted = ["Josef Stangel"]
    already_drafted_kicker = ["Josef Stangel"]
    already_drafted_def = ["Josef Stangel"]
    teams = []
    for i in range(draft_rounds):
        if i > 0:
            for y in range(len(teams)):
                for player in teams[y]:
                    #print(player)
                    already_drafted.append(player)
        if i % 2 == 0 or i == 0:
            print("Right")
            teams = simulate_draft_round(num_teams, position, teams, already_drafted, maxPosition, currentNumber, "right")
        else:
            print("Wrong")
            teams = simulate_draft_round(num_teams, position, teams, already_drafted, maxPosition, currentNumber, "wrong")
    for y in range(len(teams)):
        drafted_def = draftsimulationhelper.draft_def(already_drafted_def)
        already_drafted_def.append(drafted_def)
        teams[y].append(drafted_def)
        drafted_kicker = draftsimulationhelper.draft_kicker(already_drafted_kicker)
        already_drafted_kicker.append(drafted_kicker)
        teams[y].append(drafted_kicker)

    print(teams)
    return teams

maxPosition = {
    "QB": 2,
    "RB": 5,
    "WR": 5,
    "TE": 2,
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
teams = simulate_draft(10, 2, 13, maxPosition, [current_number, current_number, current_number, current_number, current_number, current_number, current_number, current_number, current_number, current_number])






