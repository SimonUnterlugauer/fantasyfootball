import psycopg2

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

def get_player_position_name(name):
    ## get name of player
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

## function that returns opponents strength according to the position that the selected player plays
def get_opponents_strength(player_name, week):
    conn = psycopg2.connect(
        host='localhost',
        database='posty',
        user='sulu',
        password='Nadine1995'
    )
    # Create a cursor to interact with the database
    cursor = conn.cursor()
    # Retrieve position and teamname data from the database for the specified player name

    ## get player position
    position = get_player_position_name(player_name)

    ## get own team name
    cursor.execute("SELECT team FROM projections_all_diff WHERE name = %s", (player_name,))
    team = cursor.fetchone()
    team = team[0]

    ## get opponents team name
    sql_statement = "SELECT {} FROM schedule WHERE team = %s".format(week)
    cursor.execute(sql_statement, (team,))
    opponent = cursor.fetchone()
    opponent = opponent[0]
    #print(opponent)

    if opponent == "BYE" or opponent is None:
        strength = float('inf')
    else:
        ## get opponents strength as wins
        cursor.execute("SELECT projected_strength FROM team_assessment WHERE team = %s", (opponent,))
        strength_total = cursor.fetchone()
        strength_total = float(strength_total[0])/8.5
        #print(strength_total)

        ##get opponents def rush strength
        cursor.execute("SELECT rush_yards_against FROM teams_def_stats_copy WHERE team = %s", (opponent,))
        strength_def_rush = cursor.fetchone()
        strength_def_rush = strength_def_rush[0]
        cursor.execute("SELECT rush_yards_against FROM teams_def_stats_copy WHERE team = %s", ("Avg Team",))
        strength_def_rush_avg = cursor.fetchone()
        strength_def_rush_avg = strength_def_rush_avg[0]
        rush_def = float(strength_def_rush)/float(strength_def_rush_avg)
        #print(rush_def)


        ##get opponents def pass strength
        cursor.execute("SELECT pass_yards_against FROM teams_def_stats_copy WHERE team = %s", (opponent,))
        strength_def_pass = cursor.fetchone()
        strength_def_pass = strength_def_pass[0]
        cursor.execute("SELECT pass_yards_against FROM teams_def_stats_copy WHERE team = %s", ("Avg Team",))
        strength_def_pass_avg = cursor.fetchone()
        strength_def_pass_avg = strength_def_pass_avg[0]
        pass_def = float(strength_def_pass) / float(strength_def_pass_avg)
        #print(pass_def)

        strength = None
        if (position == "QB"):
            strength = pass_def
        if (position == "WR"):
            strength = pass_def
        if (position == "TE"):
            strength = pass_def
        if (position == "RB"):
            strength = rush_def
        if (position == "DEF"):
            strength = strength_total
        if (position == "KI"):
            strength = strength_total

    #print(strength)
    return strength

def calculate_player_avg_score(player_name, weight_forecast):
    conn = psycopg2.connect(
        host='localhost',
        database='posty',
        user='sulu',
        password='Nadine1995'
    )

    # Create a cursor to interact with the database
    cursor = conn.cursor()

    # Retrieve position and teamname data from the database for the specified player name
    cursor.execute("SELECT points_forecasted, average_points FROM fantasy_data_complete WHERE name = %s", (player_name,))
    data = cursor.fetchall()

    points = 0
    for row in data:
        points_forecasted = row[0]
        average_points = row[1]
        if average_points is None:
            points += (points_forecasted / 17)
        else:
            points += weight_forecast * (points_forecasted / 17) ##
            points += (1-weight_forecast) * (average_points)
    print(points)

    return points



def calculate_weekly_score(player_name, week, weight_forecast):

    ## get opponents strength
    opponent_strength = get_opponents_strength(player_name, week)

    ## get player scores
    avg_player_score = calculate_player_avg_score(player_name, weight_forecast)

    weekly_score = (avg_player_score/opponent_strength)
    print(weekly_score)
    return weekly_score


calculate_player_avg_score("Bryce Young", 0.5)
calculate_weekly_score("Patrick Mahomes", "week_18", 0.5)


