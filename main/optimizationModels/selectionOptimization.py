import psycopg2
from pulp import LpProblem, LpVariable, LpMaximize, lpSum


def select_best_player(risk_approach, exclude_players=[], maxPosition=[], currentNumberOfPlayers=[]):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="your_database",
        user="your_username",
        password="your_password"
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Retrieve player data from the database, excluding drafted players
    cursor.execute(
        "SELECT name, teamname, points_forecasted, difference_forecasted, games_played_last_season, fantasy_points_last_year, last_years_vbd, average_points_last_year FROM players WHERE name NOT IN %s",
        (exclude_players,))
    players = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Create the optimization problem
    prob = LpProblem("PlayerSelection", LpMaximize)

    # Create decision variables
    player_vars = LpVariable.dicts("Player", [player[0] for player in players], lowBound=0, upBound=1, cat="Binary")

    # Set the objective function
    prob += lpSum([(risk_approach * player[2]) + ((1 - risk_approach) * player[7]) for player in players if
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

    # Retrieve the best player
    best_player = None
    for player in players:
        if player_vars[player[0]].value() == 1:
            best_player = player
            break

    return best_player
##end function

def get_player_position(player):
    ## get name of player
    name = player["name"] ####????
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="your_database",
        user="your_username",
        password="your_password"
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Retrieve position and teamname data from the database for the specified player name
    cursor.execute("SELECT position FROM players WHERE name = %s", (name,))
    position = cursor.fetchone()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return position
#end get_position


# Example usage
drafted_players = [
    "Player A",
    "Player B",
    "Player C"
]  # Example array of drafted players' names
maxPosition = [
    {"QB": 1},
    {"RB": 2},
    {"WR": 2},
    {"TE": 1},
    {"FLEX": 1},
    {"KI": 1},
    {"DEF": 1},
]
currentNumberOfPlayers = [
    {"QB": 0},
    {"RB": 0},
    {"WR": 0},
    {"TE": 0},
    {"FLEX": 0},
    {"KI": 0},
    {"DEF": 0},
]
best_player = select_best_player(risk_approach=0.9, exclude_players=drafted_players, maxPosition=maxPosition, currentNumberOfPlayers=currentNumberOfPlayers)
print("Best player:", best_player)

