import requests
from bs4 import BeautifulSoup
import os

# URL of the webpage containing dinosaur names and images
url = "https://www.nhm.ac.uk/discover/dino-directory/name/name-az-all.html"

# Send a request to the website and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Create a directory to store the images
os.makedirs("dinosaur_images", exist_ok=True)

# Find all elements with the class "dinosaur-item"
dinosaur_items = soup.find_all({"class":"dinosaurfilter--dinosaur dinosaurfilter--all-list"})
							

# Iterate through each dinosaur item and extract the image URLs
for item in dinosaur_items:
    dinosaur_name = item.find({"class":"dinosaur--name-unhyphenated"}).text.strip()
    image_url = item.find("img")["src"]
    
    # Download the image and save it in the dinosaur_images directory
    image_response = requests.get(image_url)
    image_filename = os.path.join("dinosaur_images", f"{dinosaur_name}.jpg")
    with open(image_filename, "wb") as image_file:
        image_file.write(image_response.content)
    
    print(f"Downloaded image for {dinosaur_name}")
print(soup)
print("Image download completed.")
print(dinosaur_items)