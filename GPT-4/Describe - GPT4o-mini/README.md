
# Image Analysis Script

## Overview

This Python script processes images in a folder by analyzing each image to generate a short description and a set of 20 relevant keywords for each image. The descriptions and keywords are saved into a CSV file, and the script also generates a log file to track the total tokens used and any errors that occurred during the API calls.

The script uses the OpenAI API (`gpt-4o-mini` model) to analyze images and generate descriptions and keywords.

## Features

- Processes all image files (JPG, JPEG, PNG) in a given folder.
- Generates a short description (up to 200 characters) and 20 relevant keywords for each image.
- Saves the output in a CSV file, including the image filename, description, and keywords.
- Tracks token usage and errors, saving this information in a log file.
- Adds a delay of 1 second between API requests to avoid exceeding API rate limits.

## Requirements

- Python 3.x
- The following Python libraries:
  - `requests`
  - `csv`
  - `base64`
  - `os`
  - `time`

You can install the required libraries using pip:

```bash
pip install requests
```

## Usage

1. **Set up your OpenAI API key**:
   Replace the placeholder in the script with your actual OpenAI API key:

   ```python
   api_key = "YOUR_API_KEY"
   ```

2. **Prepare the images**:
   Place the images you want to analyze in a folder. By default, the folder name is `img`.

3. **Run the script**:
   The script can be executed directly from the command line:

   ```bash
   python describe.py
   ```

4. **Check the output**:
   - A CSV file named `image_analysis.csv` will be generated containing the following columns:
     - `nome_file`: The name of the image file.
     - `description`: A short description of the image.
     - `keywords`: A list of 20 comma-separated keywords relevant to the image.
   - A log file named `image_analysis_log.txt` will be generated, tracking:
     - The total number of tokens used.
     - The total number of errors encountered.

## Example

If you place images in the `img` folder, the script will analyze each image and produce a CSV file like the following:

| nome_file  | description                             | keywords                             |
|------------|-----------------------------------------|--------------------------------------|
| image1.jpg | A sunset over the mountains              | sunset, mountains, nature, etc.      |
| image2.png | A dog running in the park                | dog, park, running, etc.             |

The log file will contain information such as:

```
Total tokens used: 1500
Total errors: 0
```

## Customization

- You can change the folder path by modifying the `folder_path` variable in the script.
- The output CSV file and log file names can also be changed by modifying `output_csv` and `log_file` variables.

## License

This project is open source and can be used and modified freely.
