import requests
from bs4 import BeautifulSoup
import random

# Define the URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_cryptids'

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the tables on the page
    tables = soup.find_all('table', {'class': 'wikitable'})
    
    # Assuming the first table is the one with the cryptids
    cryptid_table = tables[0]
    
    # Find all the rows in the table
    rows = cryptid_table.find_all('tr')
    
    # Remove the header row
    rows.pop(0)
    
    # Choose a random row
    random_row = random.choice(rows)
    
    # Find all the columns in the row
    cols = random_row.find_all('td')
    
    # The first column is the name of the cryptid
    cryptid_name = cols[0].text.strip()
    
    # The image should be in the second column if it exists
    image_data = cols[1].find('img')
    
    # Get the image URL if it exists
    image_url = None
    if image_data and 'src' in image_data.attrs:
        image_url = 'https:' + image_data.attrs['src']
    
    # Print the name and the image URL
    print(f'Cryptid Name: {cryptid_name}')
    if image_url:
        print(f'Image URL: {image_url}')
else:
    print('Failed to retrieve the Wikipedia page.')
