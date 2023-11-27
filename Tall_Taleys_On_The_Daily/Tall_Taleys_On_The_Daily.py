import win32com.client
from datetime import datetime
import os
import schedule
import time
import helpers1
import requests
import random
from bs4 import BeautifulSoup
from ywotd import yiddish_wotd
url = "https://www.goodreads.com/author/quotes/7205668.Norm_Macdonald"

# Who you want the email to go to and what the prefix of the message subject should be
API_URL = "https://opentdb.com/api.php?amount=1"
EMAIL_CONFIG = {
    "To": ["tanner.martin@wachter.com","William.Durgin@wachter.com","Addiqric@amazon.com","jordan.matz@wachter.com","rachel.leslie@wachter.com","leighann.young@wachter.com","William.Tucker@wachter.com","chelsey.mccoy@wachter.com","shayna.egan@wachter.com","chad.miller@wachter.com","chelsea.villanueva@wachter.com","miranda.brown@wachter.com","miranda.mendoza@wachter.com","shane.landsberry@wachter.com","john.brewer@wachter.com","catarina.wolfe@wachter.com","beckett.mcfarland@wachter.com"],
    "Subject": "Tall Taleys On the Daily"
}

# How the date in the subject should be formatted

DATE_FORMAT = "%m-%d-%Y"

class CryptidEmail:
    def get_random_quote(self, url):
    # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the quote elements on the page
            quote_elements = soup.find_all("div", class_="quoteText")

            # Choose a random quote from the list
            random_quote = random.choice(quote_elements).get_text(strip=True)

            return random_quote
        else:
            return None
    
    def __init__(self) -> None:
        #initializ your scripts connection to the microsoft outlook appliction API
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        #MAPI is for reading the emails if you want to add on to this script.
        self.namespace = self.outlook.GetNamespace("MAPI")
        #if you want to read emails, your main inbox is this, then you could iterate over self.inbox.Items (messages)
        self.inbox = self.namespace.GetDefaultFolder(6)
    def get_random_trivia_question(self):
        response = helpers1.hit_api(API_URL)
        if response and 'results' in response:
            trivia_data = response['results'][0]
            return trivia_data
        else:
            return None
    def str_date(self)->str:
        date = datetime.now()
        return datetime.strftime(date, DATE_FORMAT)
    
    def make_subject(self, dino_name:str)-> str:
        """
        creates a proper subject line for the message by adding the date and name of the Dino
        """
        return f'{EMAIL_CONFIG["Subject"]} | {self.str_date()} | {dino_name}'
    
    def list_to_recipients(self, recipients_list:list[str])->str:
        """
        formats a list of recipients to a string for outlook
        """
        return "; ".join(recipients_list)
    def get_random_cryptid(self):
        url = 'https://en.wikipedia.org/wiki/List_of_cryptids'
        response = requests.get(url)
        cryptid_info = {
            'name': None,
            'other_names': None,
            'description': None,
            'location': None,
            'image_url': None
        }

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table', {'class': 'wikitable'})
            cryptid_table = tables[0]
            rows = cryptid_table.find_all('tr')[1:]  # Skip the header row

            random_row = random.choice(rows)
            cols = random_row.find_all('td')
            
            cryptid_info['name'] = cols[0].text.strip().split('[')[0]  # Clean the name
            # Assuming other names, description, and location are in the 2nd, 3rd, and 4th columns respectively
            cryptid_info['other_names'] = cols[1].text.strip()
            cryptid_info['description'] = cols[2].text.strip()
            cryptid_info['location'] = cols[3].text.strip()

            # The image might be in a different column depending on the table structure
            for col in cols:
                image_data = col.find('img')
                if image_data and 'src' in image_data.attrs:
                    img_src = image_data.attrs['src']
                    # Convert relative URLs to absolute URLs
                    if img_src.startswith('//'):
                        cryptid_info['image_url'] = 'https:' + img_src
                    elif img_src.startswith('/'):
                        cryptid_info['image_url'] = 'https://en.wikipedia.org' + img_src
                    break  # Found an image, break the loop
        else:
            print("Failed to retrieve the Wikipedia page.")

        return cryptid_info
    def send_cryptid(self):
        
        body = ""
        cryptid_info = self.get_random_cryptid()

        if cryptid_info['image_url']:
            body += f"<img src='{cryptid_info['image_url']}' alt='Image of {cryptid_info['name']}'>\n<br>"
            body += "<br>" 
        else:
            body += "No Image for this beast.\n"
        
        if cryptid_info['name']:
            body += f"<p><strong style='font-size: 20px;'>Cryptid of the Day: {cryptid_info['name']}</strong></span></p>"
        else:
            body += "Cryptid of the Day information not available.\n"
        
        # Add other names, description, and location to the email body
        if cryptid_info['other_names']:
            body += f"<p style='margin-left: 20px;'>Other Names: {cryptid_info['other_names']}\n\n<br>"
        if cryptid_info['description']:
            body += f"<p style='margin-left: 20px;'>Description: {cryptid_info['description']}\n\n<br>"
        if cryptid_info['location']:
            body += f"<p style='margin-left: 20px;'>Location: {cryptid_info['location']}\n\n<br>"

        trivia_question = self.get_random_trivia_question()
        if trivia_question:
            answers = trivia_question['incorrect_answers'] + [trivia_question['correct_answer']]
            random.shuffle(answers)  # Shuffle the answers
            trivia_str = f"<p><b>Trivia Question:</b> {trivia_question['question']}</p>"
            trivia_str += f"<p>Options: {', '.join(answers)}</p>"
            body += trivia_str
        else:
            body += "<p>Trivia question not available.</p>"
        pass
        # Add quote
        quote = self.get_random_quote(url)  # The url variable should be the quote source URL
        if quote:
            body += f"<p><b>Quote:</b> {quote}</p>"
        else:
            body += "<p>Quote not available.</p>"

        # Add Yiddish word of the day
        heb, translit, definition = yiddish_wotd()
        if heb:
            body += f"<p><b>Yiddish Word of the Day:</b> {heb}</p>"
            body += f"<p><b>Transliteration:</b> {translit}</p>"
            body += f"<p><b>Definition:</b> {definition}</p>"
        else:
            body += "<p>Word of the Day not found or failed to retrieve.</p>"

        # Create the email message
        message = self.outlook.CreateItem(0)
        message.To = self.list_to_recipients(EMAIL_CONFIG["To"])
        message.Subject = self.make_subject("Cryptid of the Day")
        message.HTMLBody = body
        message.Send()

if __name__ == "__main__":
    cryptid_email = CryptidEmail()
    cryptid_email.send_cryptid()
