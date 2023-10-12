import requests
import base64
import io
from PIL import Image

# DALL-E API endpoint for image generation
api_url_generate = "https://api.dalle2.com/v1/generate"

# DALL-E API key (replace with your API key)
api_key = ""

def generate_pixel_art_landscape():
    # Define the prompt for generating a pixel art landscape
    prompt = "a white siamese cat"

    # Request payload for image generation using the given prompt
    payload = {
        "prompt": prompt,
        "api_key": api_key,
        "size": "1024x1024"
    }

    # Send a POST request to the DALL-E API for image generation
    response = requests.post(api_url_generate, json=payload)

    print("API Status Code:", response.status_code)  # Print the status code

    if response.status_code == 200:
        # Decode the image from the API response
        image_data = base64.b64decode(response.json()["data"])
        image = Image.open(io.BytesIO(image_data))

        # Save the generated image as a pixel art landscape wallpaper
        image.save("generated_image.png")

        print("Image generated and saved successfully.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    generate_pixel_art_landscape()
