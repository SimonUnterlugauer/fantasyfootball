from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import psycopg2

# Set up the Chrome driver
options = Options()
options.headless = True  # Run Chrome in headless mode, without opening a browser window
service = Service('/path/to/chromedriver')  # Path to the chromedriver executable
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
url = 'https://www.footballdiehards.com/fantasy-football-player-projections.cfm'
driver.get(url)

# Find the table with class "sharp"
table = driver.find_element(By.CLASS_NAME, 'sharp')

# Find all the table rows
rows = table.find_elements(By.TAG_NAME, 'tr')

# Extract the data from each row
for row in rows:
    # Process each row as needed
    cells = row.find_elements(By.TAG_NAME, 'td')
    for cell in cells:
        print(cell.text)

# Close the browser
driver.quit()





