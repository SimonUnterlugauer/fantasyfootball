from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import psycopg2

# Set up the Chrome driver
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode, without opening a browser window
service = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
url = 'https://www.fantasypros.com/nfl/projections/wr.php?week=draft'
driver.get(url)

# Find the table with class "sharp"
table = driver.find_element(By.CLASS_NAME, 'tablesorter')

# Find all the table rows
rows = table.find_elements(By.TAG_NAME, 'tr')

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(host='localhost', database='posty', user='sulu', password='Nadine1995')

### Do everything to set up the database
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
    CREATE TABLE IF NOT EXISTS projections_wrs (
        id SERIAL PRIMARY KEY,
        name TEXT,
        team TEXT,
        points INTEGER
    )
"""
cursor.execute(create_table_query)

# Extract the data from each row
for row in rows:
    # Process each row as needed
    cells = row.find_elements(By.TAG_NAME, 'td')
    if len(cells) >= 9:
        insert_query = """
                INSERT INTO projections_wrs (name, team, points)
                VALUES (%s, %s, %s)
            """
        values = (cells[0].text, cells[1].text, float(cells[8].text))
        cursor.execute(insert_query, values)

    # Check if the row has enough cells to access the desired indexes

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
# Close the browser
driver.quit()
