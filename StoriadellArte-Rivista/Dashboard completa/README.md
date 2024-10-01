
# Art History Articles Analysis Tool

This project provides an interactive Gradio-based interface for analyzing a dataset of art history articles. It includes several visualization features, such as article distribution by author, year, language, and word cloud of keywords.

## Features

- Search articles by keywords and view article metadata.
- Visualize the top 10 authors by the number of articles.
- Show the distribution of articles over time by publication year.
- Display the distribution of articles by language in a pie chart.
- Visualize the total number of words and characters used by each author.
- Show the most common keywords and places mentioned by authors.
- Generate a word cloud for keywords using Plotly.

## Requirements

- Python 3.x
- Gradio
- Pandas
- Plotly
- WordCloud

You can install the dependencies using the following command:

```bash
pip install gradio pandas plotly wordcloud
```

## How to Run

1. Clone the repository or download the code.
2. Ensure that your dataset (`sa_dataset.csv`) is in the same directory as the script.
3. Run the `app.py` script:

```bash
python app.py
```

The application will launch a Gradio interface in your browser.

## How It Works

1. The `search_by_keyword` function allows users to search for articles by keywords, displaying relevant metadata such as title, author, and publication year.
2. Various functions generate visualizations for authors, publication years, languages, and more using Plotly.
3. The Gradio interface organizes these visualizations and interactions for an intuitive experience.

## File Structure

- `app.py`: Main application file.
- `sa_dataset.csv`: Dataset containing information about the articles.

## Credits

This project uses Gradio for the interface, Plotly for data visualizations, and WordCloud for generating keyword clouds.
