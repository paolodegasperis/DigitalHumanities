
# Similar Article Search Tool for *Storia dell'Arte*

## Overview

This tool provides a way to search for semantically similar articles from 50 years of published content in the *Storia dell'Arte* journal. The core functionality uses cosine similarity to compare article embeddings (vector representations) stored in a JSON file and returns a list of the most similar articles based on a selected input.

## Features

- **Cosine Similarity Search**: The tool uses cosine similarity to find articles that are semantically similar to the selected input article.
- **Autocomplete for Titles**: The input field provides an autocomplete feature that lists all available article titles from the dataset.
- **Interactive Interface**: A user-friendly interface is built using the Gradio library, allowing users to easily select an article and view the results.

## Files

- `app.py`: The main Python script containing all the functionality of the application.
- `embedded_articles.json`: A JSON file containing article embeddings and their respective titles. These embeddings represent the semantic content of each article.

## How It Works

1. **Loading the Data**: The script loads the article embeddings from the provided JSON file. Each article has a vector representation of its content, stored in the `"embedding"` field, and its title stored in the `"titolo_articolo"` field.
  
2. **Cosine Similarity Calculation**: When an article title is selected, the script compares its embedding with those of all other articles using cosine similarity. This measure indicates how similar two articles are based on their vectorized representations.

3. **Displaying Results**: The top 5 most similar articles are returned and displayed in a user-friendly table format.

## Installation & Usage

1. Clone this repository to your local machine.

   ```bash
   git clone <repository-url>
   ```

2. Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that the `embedded_articles.json` file is in the same directory as the `app.py` script, or update the file path in the script accordingly.

4. Run the application:

   ```bash
   python app.py
   ```

5. The Gradio interface will launch, and a link will be provided. Open the link in your browser to interact with the tool.

## Dependencies

- Python 3.x
- `numpy`
- `gradio`

You can install all dependencies by running:

```bash
pip install -r requirements.txt
```

## Future Improvements

- Add more customization options for the number of similar articles returned.
- Implement support for partial matching of article titles.
- Provide visual representations of similarity scores.
