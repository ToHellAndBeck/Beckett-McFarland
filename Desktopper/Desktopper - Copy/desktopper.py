import os
import requests
import random
import ctypes
import time
import winreg as reg
 
PROTOCOL = 'http'
IP_ADDRESS = "184.190.104.254"
PORT = "8088"
BASE_FOLDER = "files"
PHOTO_FOLDER = "Pixel%20Art"

from portgetter import get_open_ports

open_ports = [i for i in get_open_ports()]
open_ports.append(PORT)
print(open_ports)
photo_folder_urls = [

]
for open_port in open_ports:
    photo_folder_url = f"{PROTOCOL}://{IP_ADDRESS}:{open_port}/{BASE_FOLDER}/{PHOTO_FOLDER}/"
    photo_folder_urls.append(photo_folder_url)

script_path = __file__
script_name = script_path.split(os.path.sep)[-1]
script_dir = script_path.replace(script_name, "")
image_dir = os.path.join(script_dir, 'images')
 
# Ensure the image directory exists
if not os.path.exists(image_dir):
    os.makedirs(image_dir)
 
headers = {
    "Host": "184.190.104.254:8087",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": f"{PROTOCOL}://{IP_ADDRESS}:{PORT}/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Connection": "keep-alive",
    "Sec-GPC": "1",
}
 
def set_background(image_path):
    # Registry paths for wallpaper style and tile
    key_path = r"Control Panel\Desktop"
    wall_style = "10"  # 0 = Tile, 2 = Center, 6 = Fit, 10 = Fill
    tile_wall = "0"  # 0 = False, 1 = True
 
    # Open the registry key and set the wallpaper style and tile
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(key, "WallpaperStyle", 0, reg.REG_SZ, wall_style)
        reg.SetValueEx(key, "TileWallpaper", 0, reg.REG_SZ, tile_wall)
        reg.CloseKey(key)
    except Exception as e:
        print(f"Failed to set registry for wallpaper style and tiling: {e}")
   
    # Now set the wallpaper
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
 
def download_image(image_url, image_name):
    # Construct the full path for the image to check if it exists
    image_name_with_extension = image_name  # Assuming image_name includes the extension
    image_path = os.path.join(image_dir, image_name_with_extension)
   
    # Check if the image already exists
    if os.path.exists(image_path):
        print(f"Image already exists: {image_name_with_extension}, setting as background.")
    else:
        # If the image does not exist, download it
        print(f"Downloading image: {image_name_with_extension}")
        r = requests.get(image_url, headers=headers).content
        with open(image_path, "wb") as fp:
            fp.write(r)
        print(f"Downloaded image: {image_name_with_extension}")
   
    # Set the image as the desktop background
    set_background(image_path)
 
def select_new_image_and_set_as_bg():
    for photo_folder_url in photo_folder_urls:
        try:
            random_image = select_random_image()
            random_image_url = photo_folder_url + random_image
            download_image(random_image_url, random_image)
            return True
        except:
            ...
 
def get_list_of_available_images():
    # Assuming this function correctly fetches and returns a list of image names
    for photo_folder_url in photo_folder_urls:
        try:
            return requests.get(photo_folder_url, headers=headers).json()
        except:
            ...
    return os.listdir(image_dir)

def select_random_image():
    images = get_list_of_available_images()
    return random.choice(images)
 
def select_new_image_and_set_as_bg():
    for photo_folder_url in photo_folder_urls:
        try:
            random_image = select_random_image()
            random_image_url = photo_folder_url + random_image
            download_image(random_image_url, random_image)
            return True
        except:
            ...
        
running = True

while running:
    try:
        select_new_image_and_set_as_bg()
        time.sleep(30)  # Adjust the sleep time as needed
    except Exception as e:
        print(e)
        time.sleep(10)