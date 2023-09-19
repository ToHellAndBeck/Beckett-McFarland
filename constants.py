import os
DINO_DIR_ENDPOINT = 'https://www.nhm.ac.uk/discover/dino-directory/'
ALL_DINOS_ENDPOINT = 'https://www.nhm.ac.uk/api/dino-directory-api/dinosaurs?view=genus'
DINO_INFO_TAG = "dinosaur section"
SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_NAME = os.path.basename(SCRIPT_PATH)
SCRIPT_DIR = SCRIPT_PATH.replace(SCRIPT_NAME, "")
IMG_DIR_NAME = "images"
IMG_DIR = os.path.join(SCRIPT_DIR, IMG_DIR_NAME)
if not os.path.isdir(IMG_DIR):
    try:
        os.mkdir(IMG_DIR)
    except:
        f"Directory {IMG_DIR} did not exist and I tried to make it but it failed"