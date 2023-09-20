import win32com.client
from datetime import datetime
import os
import schedule
import time

# Who you want the email to go to and what the prefix of the message subject should be
EMAIL_CONFIG = {
    "To": ["Chelsea.Villanueva@wachter.com"],
    "Subject": "Dino of the day"
}

# How the date in the subject should be formatted
DATE_FORMAT = "%m-%d-%Y"

class DinoEmail:
    # Existing code for DinoEmail class

    def send_dino_daily():
        """
        Function to send the Dino of the Day email.
        """
        dino_name = "NAME OF DINOSAUR"
        dino_photo = "C:\\Users\\user.name\\path\\to\\dinosaur\\photo.png"
        message_body = "Brought to you by: Detailed Daily Dino, LLC, LTD, INC"
        DOTD = DinoEmail()
        DOTD.send_dino(dino_name, dino_photo, message_body)

