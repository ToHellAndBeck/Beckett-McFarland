BUG
ELECTRIC
FIRE
GRASS
NORMAL
ROCK
DARK
FAIRY
FLYING
GROUND
POISON
DRAGON
FIGHTING
GHOST
ICE
PSYCHIC

from PIL import Image
import pandas as pd
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
 
# Open the image
img = Image.open("pngwing.com.png")
 
image_width = int(img.width/3)
image_height = int(img.height / 6)
image_x = 0
image_y = 0
# Iterate over rows in the DataFrame
for x in range(3):
    image_x = image_width * x
    for y in range(6):
        image_y = image_height * y
        print(image_x, image_y, image_width, image_height)
        new_image = img.crop((image_x, image_y, image_width+image_x, image_height+image_y))
        
        imagetext=pytesseract.image_to_string(new_image,config='--psm 6 --oem 3').replace("\n","")
        new_image.save(f"{imagetext}.png", "PNG")