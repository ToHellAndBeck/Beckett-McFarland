import win32com.client
from datetime import datetime
import os

#who all you want the email to go to and what the prefix of the message subject should be
EMAIL_CONFIG = {"To":["tanner.martin@wachter.com", "beckett.mcfarland@wachter.com"],
                "Subject":"Dino of the day"}
"""""
yolo
"""
#how the date in the subject should be formatted
DATE_FORMAT = "%m-%d-%Y"

class DinoEmail:
    def __init__(self) -> None:
        #initializ your scripts connection to the microsoft outlook appliction API
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        #MAPI is for reading the emails if you want to add on to this script.
        self.namespace = self.outlook.GetNamespace("MAPI")
        #if you want to read emails, your main inbox is this, then you could iterate over self.inbox.Items (messages)
        self.inbox = self.namespace.GetDefaultFolder(6)

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
    
    def send_dino(self, dino_name:str, dino_photos:os.PathLike|list[os.PathLike], body:str|list[str], html_body:bool=False):
        """
        if your email body is html be sure to set html_body=True when calling this function
        """

        #if the body argument is a list then go ahead and make it a string
        if isinstance(body, list):
            body = "\n\n".join(body)

        #if the dino_photos is just a string or path to one photo put in in a list
        #you can pass a list of multiple photo paths and it will attach all of them.

        if not isinstance(dino_photos, list):
            dino_photos = [dino_photos]
        
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