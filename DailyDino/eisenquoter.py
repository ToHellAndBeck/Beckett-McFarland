import requests
from bs4 import BeautifulSoup

# The URL of the website
url = 'https://verterbukh.org/vb?page=wotd&tsu=en&trns=t'

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the element with class 'wotd'
    wotd_heb = soup.find('div', class_='rtl')
    wotd_def = soup.find('div', class_='gloss')
    wotd_translit = soup.find('div', class_='translit')
   


    if wotd_heb:
        # Get the Word of the Day text
        word_of_the_day_heb = wotd_heb.text.strip() 
        word_of_the_day_translit = wotd_translit.text.strip()
        wotd_def = wotd_def.text.strip()
        print(word_of_the_day_heb)
        print(word_of_the_day_translit)
        print(wotd_def)
       
    else:
        print("Word of the Day not found on the page.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
