import base64
import requests
import os
import csv
import time

# OpenAI API Key
api_key = "YOUR_API_KEY"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to make the API request and get the description and keywords
def analyze_image(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Requesting both description and keywords
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please provide a short description (up to 200 characters) and 20 relevant keywords comma-separated for the given image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        # Split the response assuming the description and keywords are separated
        output = result['choices'][0]['message']['content'].strip()

        # Extract token usage from the response
        tokens_used = result['usage']['total_tokens']

        # Try to split the response into description and keywords assuming the format is clear
        if "Keywords:" in output:
            description_part = output.split("Keywords:")[0].strip()
            keywords_part = output.split("Keywords:")[1].strip()
        else:
            # Fallback in case the expected format isn't met
            description_part = output[:200].strip()
            keywords_part = output[200:].strip()

        # Clean and split keywords
        keywords = ",".join([kw.strip() for kw in keywords_part.split(",") if kw])

        return description_part, keywords, tokens_used
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None, None, None

# Main function to process all images in the folder
def process_images_in_folder(folder_path, output_csv, log_file):
    # CSV file headers
    csv_headers = ["nome_file", "description", "keywords"]
    
    # Initialize variables to store log info
    total_tokens = 0
    error_count = 0

    # Open the CSV file for writing
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

        # Loop through all files in the folder
        for image_file in os.listdir(folder_path):
            if image_file.endswith((".jpg", ".jpeg", ".png")):  # Filter for image files
                image_path = os.path.join(folder_path, image_file)
                base64_image = encode_image(image_path)

                # Analyze the image
                description, keywords, tokens_used = analyze_image(base64_image)
                
                # Write to CSV if analysis is successful
                if description and keywords and tokens_used is not None:
                    writer.writerow([image_file, description, keywords])
                    total_tokens += tokens_used
                else:
                    error_count += 1

                # Wait for 1 second before the next request
                time.sleep(1)

    # Write log file
    with open(log_file, 'w') as log:
        log.write(f"Total tokens used: {total_tokens}\n")
        log.write(f"Total errors: {error_count}\n")

# Path to the folder containing images
folder_path = "img"
# Output CSV file
output_csv = "image_analysis.csv"
# Log file to store token usage and errors
log_file = "image_analysis_log.txt"

# Process images and save to CSV
process_images_in_folder(folder_path, output_csv, log_file)

print("Image analysis completed. Results saved to image_analysis.csv and logs saved to image_analysis_log.txt.")
