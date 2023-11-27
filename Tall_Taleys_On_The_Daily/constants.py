import os
DINO_DIR_ENDPOINT = 'https://www.nhm.ac.uk/discover/dino-directory/'
ALL_DINOS_ENDPOINT = 'https://www.nhm.ac.uk/api/dino-directory-api/dinosaurs?view=genus'
IMG_DIR_NAME = "images"
SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
IMG_DIR = os.path.join(SCRIPT_DIR, IMG_DIR_NAME)

# Create the directory if it does not exist
if not os.path.isdir(IMG_DIR):
    try:
        os.mkdir(IMG_DIR)
    except Exception as e:  # It's a good practice to catch specific exceptions
        print(f"Directory {IMG_DIR} did not exist and I tried to make it but it failed due to: {e}")
