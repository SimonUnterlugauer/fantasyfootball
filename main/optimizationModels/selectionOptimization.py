import sys

import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum

sys.path.append("../helpers")  # Add the parent directory to the Python path
import drafthelper


## function that goes over all players and drafts the best possible option
def select_best_player(risk_approach, max_position, current_number_players, exclude_players):
    # Connect to PostgreSQL database
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host='localhost',
        database='posty',
        user='sulu',
        password='Nadine1995'
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Retrieve player data from the database, excluding drafted players
    # Retrieve player data from the database, excluding drafted players
    cursor.execute(
        "SELECT name, team_name, points_forecasted, difference_forecasted, games_played, fantasy_points_overall, players_vbd, average_points FROM fantasy_data_complete"
    )

    players = cursor.fetchall()
    #print(players)
    # Erstellung des linearen Programmierungsmodells
    model = LpProblem('Fantasy_Football_Team', LpMaximize)

    # Create decision variables
    player_vars = LpVariable.dicts("Player", [player[0] for player in players], lowBound=0, cat='Binary')

    # Definieren der Zielfunktion
    model += lpSum(
        [(((risk_approach * player[3] if player[3] is not None else 1) / (risk_approach * player[2] if player[2] is not None and player[2] != 0 else 1000))+
          ((1-risk_approach) * player[6] if player[6] is not None else 1) / ((1-risk_approach) * player[5] if player[5] is not None and player[5] != 0 else 1000))
         * player_vars[player[0]] for index, player in enumerate(players)]), 'TotalPoints'


    # Create the constraint for selecting only one player
    model += lpSum(player_vars.values()) == 1, "SelectOnePlayer"

    # Add the position and player limits as constraints
    ## if causes problems exchange player[0] with player -> db structure changes when deleted and retrieved new
    for position, max_count in maxPosition.items():
        model += lpSum([player_vars[player[0]] for player in players if
                       drafthelper.get_player_position(player[0]) == position]) <= max_count - current_number_players.get(position,
                                                                                                           0), f"MaxPosition_{position}"

    # Add the already drafted players as constraints
    for player in players:
        if player[0] in exclude_players:
            model += player_vars[player[0]] == 0, f"ExcludePlayer_{player[0]}"

    print(model)
    # Solve the optimization problem
    model.solve()
    best_player = None
    # Print decision variables
    for player_name, player_var in player_vars.items():
        print(f"Player: {player_name}, Decision Variable: {player_var}, Value: {player_var.value()}")

    for player in player_vars:
        if player_vars[player].value() == 1:
            best_player = player
            break

    return best_player


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

exclude_players = [
    "Travis Kelce",
    "Justin Jefferson"
]


best_player = select_best_player(0.5, maxPosition, current_number, exclude_players)
print("Best player:", best_player)
