
# Author Analysis Tool

This project provides an interactive Gradio-based interface for analyzing the writing patterns of authors from a dataset. It allows users to select an author and generate visualizations based on their articles, including word counts, keyword frequencies, and publication trends over the years.

## Features

- Visualizes word count statistics for a selected author.
- Displays the top 20 keywords and places mentioned in the author's articles.
- Shows the distribution of the author's articles over time.
- Provides a table of the author's articles with relevant metadata.

## Requirements

- Python 3.x
- Gradio
- Pandas
- Plotly

You can install the dependencies using the following command:

```bash
pip install gradio pandas plotly
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

1. The `author_analysis` function filters the dataset for the selected author and computes statistics on the number of words, keywords, places, and publication years.
2. Visualizations are generated using Plotly for easy interaction and display.
3. The Gradio interface allows users to select an author from a dropdown and view the corresponding charts and article data.

## File Structure

- `app.py`: Main application file.
- `sa_dataset.csv`: Dataset containing information about the articles and authors.

## Credits

This project uses Gradio for the interface and Plotly for data visualizations.
