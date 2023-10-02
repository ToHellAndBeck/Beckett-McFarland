import win32com.client
from datetime import datetime
import os
import schedule
import time

# Who you want the email to go to and what the prefix of the message subject should be
EMAIL_CONFIG = {
    "To": ["rolloutsupport@wachter.com","john.brewer@wachter.com","Chad.Miller@wachter.com","catarina.wolfe@wachter.com","shane.landsberry@wachter.com","Tanner.Martin@wachter.com","logan.rose@wachter.com","jordan.matz@wachter.com","leighann.young@wachter.com","William.Tucker@wachter.com","chelsey.mccoy@wachter.com"],
    "Subject": "Daily Scaly"
}

# How the date in the subject should be formatted
DATE_FORMAT = "%m-%d-%Y"

class DinoEmail:
    def __init__(self) -> None:
        # Initialize your scripts connection to the Microsoft Outlook application API
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        # MAPI is for reading the emails if you want to add on to this script.
        self.namespace = self.outlook.GetNamespace("MAPI")
        # If you want to read emails, your main inbox is this, then you could iterate over self.inbox.Items (messages)
        self.inbox = self.namespace.GetDefaultFolder(6)

    def str_date(self) -> str:
        date = datetime.now()
        return datetime.strftime(date, DATE_FORMAT)

    def make_subject(self, dino_name: str) -> str:
        """
        Creates a proper subject line for the message by adding the date and name of the Dino
        """
        return f'{EMAIL_CONFIG["Subject"]} | {self.str_date()} | {dino_name}'

    def list_to_recipients(self, recipients_list: list[str]) -> str:
        """
        Formats a list of recipients to a string for Outlook
        """
        return "; ".join(recipients_list)

    def send_dino(self, dino_name: str, dino_photos: os.PathLike | list[os.PathLike], body: str | list[str], html_body: bool = False):
        """
        If your email body is HTML, be sure to set html_body=True when calling this function
        """

        # If the body argument is a list, then go ahead and make it a string
        if isinstance(body, list):
            body = "\n\n".join(body)

        # If the dino_photos is just a string or path to one photo put in a list
        # You can pass a list of multiple photo paths and it will attach all of them.

        if not isinstance(dino_photos, list):
            dino_photos = [dino_photos]

        # Create an empty message
        message = self.outlook.CreateItem(0)
        # Add the dino subscribers
        recipients = self.list_to_recipients(EMAIL_CONFIG["To"])
        message.To = recipients
        # Set the subject
        subject = self.make_subject(dino_name)
        message.Subject = subject

        # If you set the html_body flag to True, set the html body of the message
        if html_body:
            message.HTMLBODY = body
        else:
            # If the html_body flag is False, then just add the regular body of the email
            message.Body = body

        # Attach all of the dino photos (could fail due to a size MB limit if you attach too many)
        for photo_path in dino_photos:
            message.Attachments.Add(photo_path)

        # Send it and return the response
        return message.Send()


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

