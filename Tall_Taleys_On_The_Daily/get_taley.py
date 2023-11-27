import requests
import random
from bs4 import BeautifulSoup
import os
from Tall_Taleys_On_The_Daily import CryptidEmail  # Make sure to rename your class to CryptidEmail

IMG_DIR = "path/to/your/image/directory"  # Make sure this directory exists

def get_random_cryptid():
    url = 'https://en.wikipedia.org/wiki/List_of_cryptids'
    response = requests.get(url)
    cryptid_name, image_url = None, None

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', {'class': 'wikitable'})
        cryptid_table = tables[0]
        rows = cryptid_table.find_all('tr')[1:]  # Skip the header row
        random_row = random.choice(rows)
        cols = random_row.find_all('td')
        cryptid_name = cols[0].text.strip().split('[')[0]  # Clean the name
        image_data = cols[1].find('img')
        if image_data and 'src' in image_data.attrs:
            image_url = 'https:' + image_data.attrs['src']
    return cryptid_name, image_url

def download_cryptid_image_and_return_path(image_url:str):
    if not image_url:
        return None
    r = requests.get(image_url)
    img_name = image_url.split('/')[-1]
    img_path = os.path.join(IMG_DIR, img_name)
    with open(img_path, 'wb') as fp:
        fp.write(r.content)
    return img_path

def run_script():
    cryptid_email = CryptidEmail()
    cryptid_email.send_cryptid()

if __name__ == "__main__":
    run_script()
