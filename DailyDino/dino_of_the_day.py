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
url = "https://www.goodreads.com/author/quotes/23920.Dwight_D_Eisenhower"

# Who you want the email to go to and what the prefix of the message subject should be
API_URL = "https://opentdb.com/api.php?amount=1"
EMAIL_CONFIG = {
    "To": ["tanner.martin@wachter.com","William.Durgin@wachter.com","Addiqric@amazon.com","jordan.matz@wachter.com","rachel.leslie@wachter.com","leighann.young@wachter.com","William.Tucker@wachter.com","chelsey.mccoy@wachter.com","shayna.egan@wachter.com","chad.miller@wachter.com","chelsea.villanueva@wachter.com","miranda.brown@wachter.com","miranda.mendoza@wachter.com","shane.landsberry@wachter.com","john.brewer@wachter.com","catarina.wolfe@wachter.com","beckett.mcfarland@wachter.com"],
    "Subject": "Daily Scaly"
}

# How the date in the subject should be formatted
DATE_FORMAT = "%m-%d-%Y"

class DinoEmail:
    def get_random_kanye_quote(self, url):
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
    
    def send_dino(self, dino_name:str, dino_photos:os.PathLike|list[os.PathLike], body:str|list[str], html_body:bool=True):
        """
        if your email body is html be sure to set html_body=True when calling this function
        """
        trivia_question = self.get_random_trivia_question()
        answers = trivia_question['incorrect_answers'] + [trivia_question['correct_answer']]
        #if the body argument is a list then go ahead and make it a string
        if isinstance(body, list):
            body = "\n\n".join(body)
        if trivia_question:
            trivia_str = "\n\n<b>Trivia Question:</b>\n"
            trivia_str = "<p>Category: " + trivia_question['category'] + "</p>"
            trivia_str += "<p>Question: " + trivia_question['question'] + "</p>"
            

# Shuffle the answers in random order
            random.shuffle(answers)

# Convert the shuffled answers list to a formatted string
            trivia_str += "<p>Options: " + ", ".join(answers) + "</p>"

            body += trivia_str
        else:
            body += "\n\nTrivia question not available."
        #if the dino_photos is just a string or path to one photo put in in a list
        #you can pass a list of multiple photo paths and it will attach all of them.
        quote = self.get_random_kanye_quote(url)
        if quote:
            quote_str = "\n\n<b>Quote:</b>\n"
            quote_str += quote + "\n"
            body += quote_str
        else:
            body += "\n\nQuote not available."
        if not isinstance(dino_photos, list):
            dino_photos = [dino_photos]
        
        heb, translit, definition = yiddish_wotd()

        if heb:
            body += f"<br><b>Yiddish Word of the Day:</b><br>{heb}"
            body += f"<br><b>Transliteration:</b><br>{translit}"
            body += f"<br><b>Definition:</b><br>{definition}<br>"
        else:
            body += "<br>Word of the Day not found or failed to retrieve.<br>"
        
        #create an empty message
        message = self.outlook.CreateItem(0)
        #add the dino subscribers
        recipients = self.list_to_recipients(EMAIL_CONFIG["To"])
        message.To = recipients
        #set the subject
        subject = self.make_subject(dino_name)
        message.Subject = subject

        #if you set the html_body flag to True, set the html body of the message
        if html_body:
            message.HTMLBODY = body
        else:
            #if the html_body flag is False then just add the regular body of the email
            message.Body = body

        #attach all of the dino photos (could fail due to a size mb limit if you attach too many)
        for photo_path in dino_photos:
            message.Attachments.Add(photo_path)
        
        #send it!
        message.send
        print(trivia_question['correct_answer'])

if __name__ == "__main__":
    """
    in another script you can import this

    from dino_of_the_day import DinoEmail
    """
    dino_name = "NAME OF DINOSAUR"
    dino_photo = "C:\\Users\\user.name\\path\\to\\dinosaur\\photo.png"
    message_body = "Brought to you by: Detailed Daily Dino, LLC, LTD, INC"
    DOTD = DinoEmail()
    DOTD.send_dino(dino_name, dino_photo, message_body)
