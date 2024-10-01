
# Keyword Analysis Tool

This project provides an interactive Gradio-based interface for analyzing the occurrence and distribution of a selected keyword in a dataset. It allows users to input a keyword and visualize its temporal trends, authors who frequently use it, and the places associated with it.

## Features

- Visualizes the yearly frequency of a selected keyword.
- Displays a bar chart of authors who frequently mention the keyword.
- Shows the top 10 places mentioned in association with the keyword.
- Provides a table of articles where the keyword appears.

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

1. The `keyword_analysis` function filters the dataset for the specified keyword and generates visualizations of its yearly distribution, author frequencies, and place mentions.
2. Visualizations are generated using Plotly for interactive analysis.
3. The Gradio interface allows users to input a keyword and view the corresponding charts and article data.

## File Structure

- `app.py`: Main application file.
- `sa_dataset.csv`: Dataset containing information about the articles and keywords.

## Credits

This project uses Gradio for the interface and Plotly for data visualizations.
