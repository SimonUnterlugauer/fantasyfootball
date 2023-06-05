import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum


def select_best_player(risk_approach, exclude_players=[], maxPosition=[], currentNumberOfPlayers=[]):
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
        "SELECT name, team_name, points_forecasted, difference_forecasted, games_played, fantasy_points_overall, players_vbd, average_points FROM fantasy_data_complete WHERE name != ALL (%s)",
        (exclude_players,))

    players = cursor.fetchall()


    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Create the optimization problem
    prob = LpProblem("PlayerSelection", LpMaximize)

    # Create decision variables
    player_vars = LpVariable.dicts("Player", [player[0] for player in players], lowBound=0, upBound=1, cat="Binary")
    for player in players:
        print(player[2])
        print(player[5])
        break

    # Set the objective function
    prob += lpSum([(risk_approach * player[2] if player[2] is not None else 0) + (
        (1 - risk_approach) * player[7] if player[7] is not None else 0) - (
                       risk_approach * player[3] if player[3] is not None else 0) - (
                       (1 - risk_approach) * player[6] if player[6] is not None else 0) for player in players if
                   player[0] not in exclude_players]), "TotalScore"

    # Add the position and player limits as constraints
    for position, max_count in maxPosition.items():
        prob += lpSum([player_vars[player[0]] for player in players if
                       get_player_position(player) == position]) <= max_count - currentNumberOfPlayers.get(position,
                                                                                                           0), f"MaxPosition_{position}"

    # Add the already drafted players as constraints
    for player in players:
        if player[0] in exclude_players:
            prob += player_vars[player[0]] == 0, f"ExcludePlayer_{player[0]}"

    # Solve the optimization problem
    prob.solve()
    # Print decision variables
    for player_name, player_var in player_vars.items():
        print(f"Player: {player_name}, Decision Variable: {player_var}, Value: {player_var.value()}")

    # Retrieve the best player
    best_player = None
    for player_name, player_var in player_vars.items():
        if player_var.value() == 1:
            best_player = player_name
            break

    return best_player
##end function

def get_player_position(player):
    ## get name of player
    name = player[0]
    #name = player["name"] ####????
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host='localhost',
        database='posty',
        user='sulu',
        password='Nadine1995'
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Retrieve position and teamname data from the database for the specified player name
    cursor.execute("SELECT position FROM projections_all_diff WHERE name = %s", (name,))
    position = cursor.fetchone()
    position = position[0]

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return position
#end get_position


# Example usage
drafted_players = [
    "Player A",
    "Player B",
    "Player C",
]
maxPosition = {
    "QB": 1,
    "RB": 2,
    "WR": 2,
    "TE": 1,
    "FLEX": 1,
    "KI": 1,
    "DEF": 1,
}
currentNumberOfPlayers = {
    "QB": 0,
    "RB": 0,
    "WR": 0,
    "TE": 0,
    "FLEX": 0,
    "KI": 0,
    "DEF": 0,
}
best_player = select_best_player(0.9, drafted_players, maxPosition, currentNumberOfPlayers)
print("Best player:", best_player)

