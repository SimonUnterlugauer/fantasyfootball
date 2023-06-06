import psycopg2
import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = 'https://www.pro-football-reference.com/years/2022/opp.htm'

# Send a GET request to the webpage
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the fantasy football data
table = soup.find('table', id='team_stats')

# Find all the table rows within the table
rows = table.find_all('tr')

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(host='localhost', database='posty', user='sulu', password='Nadine1995')

# Create a cursor object
cursor = conn.cursor()

# Create a table to store the extracted data
create_table_query = '''
    CREATE TABLE IF NOT EXISTS teams_def_stats (
        team TEXT,
        rush_yards_against TEXT,
        pass_yards_against TEXT
    )
'''
cursor.execute(create_table_query)

# Iterate over the rows, skipping the header row
for row in rows[1:]:
    # Extract the data from each column in the row
    columns = row.find_all('td')
    if len(columns) >= 15:
        team = columns[0].text.strip()
        rush_yards = columns[11].text.strip()
        # Convert empty string to 0
        pass_yards = columns[17].text.strip()

        # Insert the extracted data into the table
        insert_query = '''
                    INSERT INTO teams_def_stats (team, rush_yards_against, pass_yards_against)
                    VALUES (%s, %s, %s)
                '''
        data = (team, rush_yards, pass_yards)
        cursor.execute(insert_query, data)

# Commit the changes to the database
conn.commit()
conn.close()


