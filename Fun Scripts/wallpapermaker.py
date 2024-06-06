import time
import requests
from PIL import Image
from io import BytesIO
import json
import os
import random

random_number = random.randint(1, 1000000)
random_number = str(random_number)

def generate():
    url_generate = "https://api.prodia.com/v1/sdxl/generate"
    user_prompt = input("What do you want to see?: ")
    payload = {
        "model": "dreamshaperXL10_alpha2.safetensors [c8afe2ef]",
        "prompt": user_prompt,
        "width": 1280,
        "height": 720,
        "aspect_ratio": "landscape",
        "upscale": True
    }

    api_key = "67313905-dd5b-4d3a-a24d-79432b7ad44b"  # Replace with your actual API key
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": api_key
    }

    response = requests.post(url_generate, json=payload, headers=headers)
    time.sleep(10)
    
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Extract the job ID from the response
        job_id = response.json().get('job')
        url_get = f"https://api.prodia.com/v1/job/{job_id}"
        # Construct the initial response structure
        initial_response = {
            "job": job_id,
            "params": "{}",
            "imageURL": ""
        }

        # Get job status and imageURL
        while True:
            response_get = requests.get(url_get, headers=headers)
            if response_get.status_code == 200:
                job_status = response_get.json().get('status')
                initial_response['imageURL'] = response_get.json().get('imageUrl')

                # Check if the job has succeeded
                if job_status == 'succeeded':
                    break
            else:
                print(f"Error getting job status. Status code: {response_get.status_code}")
                break

        # Now try to open the image
        if initial_response['imageURL']:
            image_content = requests.get(initial_response['imageURL'])
            try:
                image = Image.open(BytesIO(image_content.content))
                # Do something with the image, e.g., save or display it

                # Save the image to a file
                user_prompt_cleaned = ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in user_prompt)
                file_name = f"{user_prompt_cleaned}_{random_number}.png"
                folder_path = r"C:\Users\beckett.mcfarland\Pictures\Verdent"
                file_path = os.path.join(folder_path, file_name)
                image.save(file_path)
                print(f"Image saved to: {file_path}")

            except Image.UnidentifiedImageError as e:
                print(f"Error opening image: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print("No imageURL found in the response.")

# Call the function to run the code
generate()
