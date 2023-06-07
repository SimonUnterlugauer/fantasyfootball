import psycopg2
import re

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="posty",
    user="sulu",
    password="Nadine1995"
)


# Create a cursor object to interact with the database
cur = conn.cursor()

# Fetch rows from projections_qbs
cur.execute("SELECT name, team, points FROM projections_qbs")
qb_rows = cur.fetchall()

# Fetch rows from projections_wrs
cur.execute("SELECT name, team, points FROM projections_wrs")
wr_rows = cur.fetchall()

# Fetch rows from projections_rbs
cur.execute("SELECT name, team, points FROM projections_rbs")
rb_rows = cur.fetchall()

# Fetch rows from projections_te
cur.execute("SELECT name, team, points FROM projections_te")
te_rows = cur.fetchall()

# Fetch rows from projections_def
cur.execute("SELECT name, team, points FROM projections_def")
def_rows = cur.fetchall()

# Fetch rows from projections_ki
cur.execute("SELECT name, team, points FROM projections_ki")
ki_rows = cur.fetchall()

# Calculate the average points for each position
qb_total_points = sum(row[2] for row in qb_rows)
qb_num_entries = len(qb_rows)
qb_average_points = qb_total_points / qb_num_entries

wr_total_points = sum(row[2] for row in wr_rows)
wr_num_entries = len(wr_rows)
wr_average_points = wr_total_points / wr_num_entries

rb_total_points = sum(row[2] for row in rb_rows)
rb_num_entries = len(rb_rows)
rb_average_points = rb_total_points / rb_num_entries

te_total_points = sum(row[2] for row in te_rows)
te_num_entries = len(te_rows)
te_average_points = te_total_points / te_num_entries

def_total_points = sum(row[2] for row in def_rows)
def_num_entries = len(def_rows)
def_average_points = def_total_points / def_num_entries

ki_total_points = sum(row[2] for row in ki_rows)
ki_num_entries = len(ki_rows)
ki_average_points = ki_total_points / ki_num_entries

# Create a new table with the same structure as projections_qbs
cur.execute("CREATE TABLE projections_all_diff (id SERIAL PRIMARY KEY, name VARCHAR(255), team VARCHAR(255), points_forecasted INTEGER, difference_forecasted INTEGER, position VARCHAR(255))")

# Insert the data into the new table with the difference and position columns
for row in qb_rows:
    player_name = ' '.join(row[0].split()[:2])
    team_name = ' '.join(row[0].split()[2:])
    points = row[2]
    difference = points - qb_average_points
    position = "QB"

    cur.execute(
        "INSERT INTO projections_all_diff (name, team, points_forecasted, difference_forecasted, position) VALUES (%s, %s, %s, %s, %s)",
        (player_name, team_name, points, difference, position))

for row in wr_rows:
    player_name = ' '.join(row[0].split()[:2])
    team_name = ' '.join(row[0].split()[2:])
    points = row[2]
    difference = points - wr_average_points
    position = "WR"

    cur.execute(
        "INSERT INTO projections_all_diff (name, team, points_forecasted, difference_forecasted, position) VALUES (%s, %s, %s, %s, %s)",
        (player_name, team_name, points, difference, position))

for row in rb_rows:
    player_name = ' '.join(row[0].split()[:2])
    team_name = ' '.join(row[0].split()[2:])
    points = row[2]
    difference = points - rb_average_points
    position = "RB"

    cur.execute(
        "INSERT INTO projections_all_diff (name, team, points_forecasted, difference_forecasted, position) VALUES (%s, %s, %s, %s, %s)",
        (player_name, team_name, points, difference, position))

for row in te_rows:
    player_name = ' '.join(row[0].split()[:2])
    team_name = ' '.join(row[0].split()[2:])
    points = row[2]
    difference = points - te_average_points
    position = "TE"

    cur.execute(
        "INSERT INTO projections_all_diff (name, team, points_forecasted, difference_forecasted, position) VALUES (%s, %s, %s, %s, %s)",
        (player_name, team_name, points, difference, position))

for row in def_rows:
    player_name = ' '.join(row[0].split()[:2])
    team_name = ' '.join(row[0].split()[:2])
    points = row[2]
    difference = points - def_average_points
    position = "DEF"

    cur.execute(
        "INSERT INTO projections_all_diff (name, team, points_forecasted, difference_forecasted, position) VALUES (%s, %s, %s, %s, %s)",
        (player_name, team_name, points, difference, position))

for row in ki_rows:
    player_name = ' '.join(row[0].split()[:2])
    team_name = ' '.join(row[0].split()[2:])
    points = row[2]
    difference = points - ki_average_points
    position = "KI"

    cur.execute(
        "INSERT INTO projections_all_diff (name, team, points_forecasted, difference_forecasted, position) VALUES (%s, %s, %s, %s, %s)",
        (player_name, team_name, points, difference, position))

# Commit the changes to the database
conn.commit()

# Close the cursor and the database connection
cur.close()
conn.close()


