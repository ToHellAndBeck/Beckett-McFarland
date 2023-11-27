import time
import requests
import json

def generate():
    url_generate = "https://api.prodia.com/v1/sdxl/generate"
    
    payload = {
        "model": "dreamshaperXL10_alpha2.safetensors [c8afe2ef]",
        "prompt": "create a retro PIXEL ART modernist building on city skyline, sunset.",
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
    time.sleep(15)
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


        # Use a GET request to retrieve information about the job
        response2 = requests.get(url_get, headers=headers)
        
        if response2.status_code == 200:
            print(response2.text)
        else:
            print(f"Error retrieving job information. Status code: {response2.status_code}")
    else:
        print(f"Error generating image. Status code: {response.status_code}")

# Call the function to run the code
generate()
