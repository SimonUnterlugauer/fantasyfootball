import requests
from bs4 import BeautifulSoup
import psycopg2

# URL of the webpage
url = 'https://www.pro-football-reference.com/years/2022/fantasy.htm'

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the fantasy football data
table = soup.find('table', id='fantasy')

# Find all the table rows within the table
rows = table.find_all('tr')

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(host='localhost', database='posty', user='sulu', password='Nadine1995')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to store the extracted data
create_table_query = '''
    CREATE TABLE IF NOT EXISTS fantasy_data (
        position TEXT,
        team_name TEXT,
        passes TEXT,
        player_name TEXT,
        games_started INTEGER,
        fantasy_points_overall INTEGER,
        players_vbd INTEGER,
        average_points FLOAT
    )
'''
cursor.execute(create_table_query)

# Iterate over the rows, skipping the header row
for row in rows[1:]:
    # Extract the data from each column in the row
    columns = row.find_all('td')

    # Check if the columns list has enough elements
    if len(columns) >= 25:
        position = columns[2].text.strip() if columns[2].text.strip() else "not specified"
        team_name = columns[1].text.strip()
        passes = columns[6].text.strip()
        player_name = columns[0].text.strip()
        games_started = columns[5].text.strip()
        fantasy_points_overall = columns[25].text.strip()
        players_vbd = columns[29].text.strip()
        # Convert empty string to 0
        passes = int(columns[6].text.strip()) if passes else 0
        games_started = int(games_started) if games_started else 0
        fantasy_points_overall = int(fantasy_points_overall) if fantasy_points_overall else 0
        players_vbd = int(players_vbd) if players_vbd else 0
        average_ftp = int(fantasy_points_overall) / int(games_started) if int(games_started) != 0 else 0

        # Insert the extracted data into the table
        insert_query = '''
            INSERT INTO fantasy_data (position, team_name, passes, player_name, games_started, fantasy_points_overall, players_vbd, average_points)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = (position, team_name, passes, player_name, games_started, fantasy_points_overall, players_vbd, average_ftp)
        cursor.execute(insert_query, data)

# Commit the changes and close the database connection
conn.commit()
conn.close()

