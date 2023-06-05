from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpInteger
import psycopg2

def select_best_player(risk_approach):
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




def get_player_position(player):
    ## get name of player
    name = player[0]
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




best_player = select_best_player(0.5)
print("Best player:", best_player)
