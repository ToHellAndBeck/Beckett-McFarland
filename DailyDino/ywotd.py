import requests
from bs4 import BeautifulSoup

# The URL of the website
url = 'https://verterbukh.org/vb?page=wotd&tsu=en&trns=t'

def yiddish_wotd():
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the elements you want
        wotd_heb = soup.find('div', class_='rtl')
        wotd_def = soup.find('div', class_='gloss')
        wotd_translit = soup.find('div', class_='translit')

        if wotd_heb:
            # Get the Word of the Day text
            word_of_the_day_heb = wotd_heb.text.strip() 
            word_of_the_day_translit = wotd_translit.text.strip()
            wotd_def = wotd_def.text.strip()
            return word_of_the_day_heb, word_of_the_day_translit, wotd_def
        else:
            return None, None, None  # Word of the Day not found
    else:
        return None, None, None  # Failed to retrieve the web page

# Optional: You can include code here to run the function if this module is executed directly.

if __name__ == "__main__":
    heb, translit, definition = yiddish_wotd()
    if heb:
        print("Yiddish Word of the Day (Hebrew script):", heb)
        print("Transliteration:", translit)
        print("Definition:", definition)
    else:
        print("Word of the Day not found or failed to retrieve.")
