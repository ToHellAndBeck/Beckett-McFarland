import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import requests
from random import choice
from constants import DINO_DIR_ENDPOINT, ALL_DINOS_ENDPOINT, DINO_INFO_TAG, IMG_DIR
from bs4 import BeautifulSoup
import schedule
import time

# Email configuration for Gmail
EMAIL_CONFIG = {
    "From": "bmscorch@gmail.com",
    "To": ["beckettmcfarland@gmail.com", "lyndi.chap@gmail.com"],
    "Subject": "Dino of the day",
    "Username": "bmscorch@gmail.com",
    "Password": "yyad xzir tbse rfsb"  # You should use app-specific password for security
}

DATE_FORMAT = "%m-%d-%Y"

class DinoEmail:
    def send_dino(self, dino_name, dino_photos, body, html_body=False):
        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = EMAIL_CONFIG["From"]
        message["To"] = ", ".join(EMAIL_CONFIG["To"])
        message["Subject"] = f"{EMAIL_CONFIG['Subject']} - {dino_name}"

        # Attach the body of the email
        if html_body:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))

        # Attach the dinosaur photo
        with open(dino_photos, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(dino_photos)}",
        )
        message.attach(part)

        # Send email using SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_CONFIG["Username"], EMAIL_CONFIG["Password"])
        server.sendmail(EMAIL_CONFIG["From"], EMAIL_CONFIG["To"], message.as_string())
        server.quit()

def get_all_dinos():
    r = requests.get(ALL_DINOS_ENDPOINT)
    return r.json()

def restructure_dinos(dinos):
    dino_data = {dino["genus"]: dino for dino in dinos if dino.get("genus")}
    return dino_data

def get_random_dino_name(dino_names):
    return choice(dino_names)

def get_dino_info(dino_name):
    url = f"{DINO_DIR_ENDPOINT}/{dino_name.lower()}.html"
    r = requests.get(url)
    dino_soup = BeautifulSoup(r.content, "html.parser")
    dino_info = dino_soup.find_all("div", class_=DINO_INFO_TAG)
    return dino_info

def download_dino_image(img_link, dino_name):
    r = requests.get(img_link)
    img_name = f"{dino_name}.png"
    img_path = os.path.join(IMG_DIR, img_name)
    with open(img_path, "wb") as fp:
        fp.write(r.content)
    return img_path

def create_message_body(dino_info):
    body = "\n".join(f"{k}:\t{v}" for k, v in dino_info.items())
    return body

if __name__ == "__main__":
    all_dinos = get_all_dinos()
    restructured_dinos = restructure_dinos(all_dinos)
    dino_names = list(restructured_dinos.keys())
    dino_name = get_random_dino_name(dino_names)
    dino_of_the_day = restructured_dinos.get(dino_name)
    dino_info = get_dino_info(dino_name)
    dino_img_link = dino_info[0].find("img", class_="dinosaur--image")["src"]
    dino_img_path = download_dino_image(dino_img_link, dino_name)
    message_body = create_message_body(dino_of_the_day)
    dino_email = DinoEmail()
    dino_email.send_dino(dino_name, dino_img_path, message_body)

    # Schedule the email to be sent every day at 9:24 PM
    schedule.every().day.at("21:52").do(
        dino_email.send_dino, dino_name, dino_img_path, message_body
    )

    while True:
        schedule.run_pending()
        time.sleep(1)
