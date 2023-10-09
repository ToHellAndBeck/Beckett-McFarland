import requests
import base64
import io
from PIL import Image

# DALL-E API endpoint
api_url = "https://api.dalle2.com/v1/generate"

# DALL-E API key (replace with your API key)
api_key = "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"

def generate_pixel_art_landscape():
    # Define the prompt for generating a pixel art landscape
    prompt = "Pixel art landscape"

    # Request payload for DALL-E API
    payload = {
        "prompt": prompt,
        "api_key": api_key,
        "size": "1920x1080"  # Adjust the size as needed for your wallpaper
    }

    # Send a POST request to the DALL-E API
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        # Decode the image from the API response
        image_data = base64.b64decode(response.json()["data"])
        image = Image.open(io.BytesIO(image_data))

        # Save the generated image as a pixel art landscape wallpaper
        image.save("pixel_art_landscape_wallpaper.png")

        print("Pixel art landscape wallpaper generated and saved successfully.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    generate_pixel_art_landscape()
