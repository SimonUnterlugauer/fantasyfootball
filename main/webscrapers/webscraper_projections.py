import os
import pandas as pd
import psycopg2
import openpyxl

# Get the current directory
current_directory = os.getcwd()

# Construct the path to the file in the parent directory under the "extras" folder
file_path = os.path.join(os.path.dirname(current_directory), 'extras', 'mockrankings.xlsx')

# Daten aus der Excel-Datei einlesen
df = pd.read_excel(file_path)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(host='localhost', database='posty', user='sulu', password='Nadine1995')

# Create a cursor object
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
    CREATE TABLE IF NOT EXISTS mock_draft (
        id SERIAL PRIMARY KEY,
        rank INTEGER,
        team TEXT,
        player TEXT
    )
"""
cursor.execute(create_table_query)

# Save the DataFrame to the table
for _, row in df.iterrows():
    insert_query = """
        INSERT INTO mock_draft (rank, team, player)
        VALUES (%s, %s, %s)
    """
    values = (row['Rank'], row['Team'], row['Player'])
    cursor.execute(insert_query, values)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

