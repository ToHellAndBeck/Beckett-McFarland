import requests
from random import choice
from constants import DINO_DIR_ENDPOINT, ALL_DINOS_ENDPOINT, DINO_INFO_TAG, IMG_DIR
from dino_of_the_day import DinoEmail
from bs4 import BeautifulSoup
import os



def get_all_dinos():
    r = requests.get(ALL_DINOS_ENDPOINT)
    return r.json()

def restructure_dinos(dinos:list[dict]):
    dino_data = dict()
    for dino in dinos:
        dino_name = dino.get("genus")
        if dino_name:
            dino_data.update({dino_name:dino})
    return dino_data

def get_random_dino_name(dino_names:list[str]):
    return choice(dino_names)

def get_dino_html(dino_name:str):
    url_name = dino_name.lower()
    url = DINO_DIR_ENDPOINT + "/" + url_name + '.html'
    r = requests.get(url)
    return r.content.decode()

def get_dino_info_html(dino_html:str):
    dinosaur_soup = BeautifulSoup(dino_html, 'html.parser')
    dino_info = dinosaur_soup.find_all("div", {'class':DINO_INFO_TAG})
    return dino_info

def get_dino_img_link(dino_info_html):
    for result_set in dino_info_html:
        img_link = result_set.find('img', {"class":"dinosaur--image"})
        if img_link:
            return img_link.attrs.get('src')

def download_dino_image_and_return_path(img_link:str):
    r = requests.get(img_link)
    img_name = img_link.split('/')[-1]
    img_path = os.path.join(IMG_DIR, img_name)
    with open(img_path, 'wb') as fp:
        fp.write(r.content)
    return img_path

def dino_html_to_dict(dino_info_html):
    all_dls = list()
    dino_info_dict = dict()
    for result_set in dino_info_html:
        for dl in result_set.find_all("dl"):
            dino_keys = [k.text.replace(":", "").strip() for k in dl.find_all("dt")]
            dino_values = [v.text.strip() for v in dl.find_all("dd")]
            for k, v in list(zip(dino_keys, dino_values)):
                dino_info_dict[k] = v
    return dino_info_dict

def create_message_body(dino_info_dict:dict):
    body = ""
    for k,v in dino_info_dict.items():
        row = ":\t".join([k, v])
        body = body + "<p>" + row +"</p>"
    return body

all_dinos = get_all_dinos()
restructured_dinos = restructure_dinos(all_dinos)
dino_names = [i for i in restructured_dinos]
dino_name = get_random_dino_name(dino_names)
dino_of_the_day = restructured_dinos.get(dino_name)
dino_html = get_dino_html(dino_name)
dino_info_html = get_dino_info_html(dino_html)
dino_img_link = get_dino_img_link(dino_info_html)
dino_img_path = download_dino_image_and_return_path(dino_img_link)
dino_info_dict = dino_html_to_dict(dino_info_html)
message_body = create_message_body(dino_info_dict)
dino_email = DinoEmail()
dino_email.send_dino(dino_name, dino_img_path, message_body)
def run_script():
    """
    Function to run the script to send the Dino of the Day email.
    """
    all_dinos = get_all_dinos()
    restructured_dinos = restructure_dinos(all_dinos)
    dino_names = [i for i in restructured_dinos]
    dino_name = get_random_dino_name(dino_names)
    dino_of_the_day = restructured_dinos.get(dino_name)
    dino_html = get_dino_html(dino_name)
    dino_info_html = get_dino_info_html(dino_html)
    dino_img_link = get_dino_img_link(dino_info_html)
    dino_img_path = download_dino_image_and_return_path(dino_img_link)
    dino_info_dict = dino_html_to_dict(dino_info_html)
    message_body = create_message_body(dino_info_dict)
    dino_email = DinoEmail()
    dino_email.send_dino(dino_name, dino_img_path, message_body)

