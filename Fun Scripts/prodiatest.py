import time
import requests
import json

url = "https://api.prodia.com/v1/sdxl/generate"
payload = {
    "model": "dreamshaperXL10_alpha2.safetensors [c8afe2ef]",
    "prompt": "create a retro modernist building on city skyline, sunset.",
    "aspect_ratio": "landscape"
    
}
api_key = "67313905-dd5b-4d3a-a24d-79432b7ad44b"  # Replace with your actual API key
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Prodia-Key": api_key
    
}

response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Extract the job ID from the response
    job_id = response.json().get('job')

    # Construct the initial response structure
    initial_response = {
        "job": job_id,
        "params": "{}",
        "imageUrl": ""
    }

    print(json.dumps(initial_response))  # Print the initial response

    # Poll the API to check if the job is completed and get the image URL
    max_attempts = 4  # Set the maximum number of polling attempts
    attempts = 0

    while attempts < max_attempts:
        job_status_response = requests.get(f"https://api.prodia.com/v1/job/{job_id}", headers=headers)

        print("Job status response:", job_status_response.text)  # Print the response

        # Break the loop if the job is completed
        if job_status_response.status_code == 200:
            job_status_data = job_status_response.json()
            status = job_status_data.get('status')
            image_url = job_status_data.get('data', {}).get('imageUrl')

            if status == 'succeeded' and image_url:
                initial_response['imageUrl'] = image_url
                print(json.dumps(initial_response, indent=2))

                # Save the URL to a text file
                with open('image_urls.txt', 'a') as file:
                    file.write(image_url + '\n')

                break  # Exit the loop once we have the image URL

        time.sleep(6)  # Wait for 5 seconds before polling again
        attempts += 1

    if attempts >= max_attempts:
        print("")
else:
    print(f"Request failed with status code {response.status_code}.")