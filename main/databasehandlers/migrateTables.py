import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="posty",
    user="sulu",
    password="Nadine1995"
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Create the fantasy_data_complete table
cur.execute("""
    CREATE TABLE fantasy_data_complete AS
    SELECT pd.name, pd.team, pd.points_forecasted, pd.difference_forecasted, fd.team_name, fd.player_name, fd.games_played, fd.fantasy_points_overall, fd.players_vbd, fd.average_points
    FROM projections_all_diff pd
    LEFT JOIN fantasy_data fd ON pd.name = fd.player_name;
""")

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
