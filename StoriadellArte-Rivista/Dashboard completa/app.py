import pandas as pd
import gradio as gr
import plotly.express as px
from wordcloud import WordCloud

# Load the dataset
file_path = 'sa_dataset.csv'
data = pd.read_csv(file_path)

# Function to search articles by keyword
def search_by_keyword(keyword):
    results = data[data['keyword'].str.contains(keyword, na=False)]
    return results[['titolo_articolo', 'primo_autore', 'anno_pubblicazione']]

# Function to plot authors distribution
def plot_authors():
    author_counts = data['primo_autore'].value_counts().head(10).reset_index()
    author_counts.columns = ['Autore', 'Numero di Articoli']
    fig = px.bar(author_counts, x='Autore', y='Numero di Articoli', 
                  title='Top 10 Autori per Numero di Articoli', 
                  color='Numero di Articoli', 
                  labels={'Numero di Articoli': 'Numero di Articoli', 'Autore': 'Autore'})
    return fig

# Function to plot publication years distribution
def plot_publication_years():
    year_counts = data['anno_pubblicazione'].value_counts().sort_index().reset_index()
    year_counts.columns = ['Anno di Pubblicazione', 'Numero di Articoli']
    fig = px.bar(year_counts, x='Anno di Pubblicazione', y='Numero di Articoli', 
                  title='Numero di Articoli Pubblicati per Anno', 
                  labels={'Numero di Articoli': 'Numero di Articoli', 'Anno di Pubblicazione': 'Anno'})
    return fig

# Function to plot language distribution
def plot_language_distribution():
    language_counts = data['lingua'].value_counts().reset_index()
    language_counts.columns = ['Lingua', 'Numero di Articoli']
    fig = px.pie(language_counts, names='Lingua', values='Numero di Articoli', 
                  title='Distribuzione degli Articoli per Lingua', 
                  hole=0.3)
    return fig

# Function to plot characters and words used by each author
def plot_characters_words():
    author_stats = data.groupby('primo_autore')[['num_parole', 'num_caratteri']].sum().reset_index()
    fig = px.bar(author_stats, x='primo_autore', y=['num_parole', 'num_caratteri'], 
                  title='Numero Totale di Parole e Caratteri per Autore', 
                  labels={'value': 'Totale', 'primo_autore': 'Autore'})
    return fig

# Function to get most common keywords by author
def common_keywords_by_author():
    filtered_data = data[['primo_autore', 'keyword']].dropna()
    filtered_data['keyword'] = filtered_data['keyword'].str.split(', ')
    keywords_exploded = filtered_data.explode('keyword')
    common_keywords = keywords_exploded.groupby(['primo_autore', 'keyword']).size().reset_index(name='Count')
    common_keywords = common_keywords.sort_values(['primo_autore', 'Count'], ascending=[True, False]).groupby('primo_autore').head(5)
    fig = px.bar(common_keywords, x='keyword', y='Count', color='primo_autore',
                  title='Parole Chiave più Ricorrenti per Autore', 
                  labels={'Count': 'Occorrenze', 'keyword': 'Parole Chiave'})
    return fig

# Function to get most common places by author
def common_places_by_author():
    filtered_data = data[['primo_autore', 'luoghi_citati']].dropna()
    filtered_data['luoghi_citati'] = filtered_data['luoghi_citati'].str.split(', ')
    places_exploded = filtered_data.explode('luoghi_citati')
    common_places = places_exploded.groupby(['primo_autore', 'luoghi_citati']).size().reset_index(name='Count')
    common_places = common_places.sort_values(['primo_autore', 'Count'], ascending=[True, False]).groupby('primo_autore').head(5)
    fig = px.bar(common_places, x='luoghi_citati', y='Count', color='primo_autore',
                  title='Luoghi più Ricorrenti per Autore', 
                  labels={'Count': 'Occorrenze', 'luoghi_citati': 'Luoghi'})
    return fig

# Function to create a word cloud of keywords using Plotly
def word_cloud_keywords():
    text = ' '.join(data['keyword'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Get word frequencies
    word_frequencies = wordcloud.words_

    # Create a DataFrame for Plotly
    df_wordcloud = pd.DataFrame(word_frequencies.items(), columns=['Word', 'Frequency'])

    # Create a Plotly scatter plot for word cloud
    fig = px.scatter(df_wordcloud, x='Word', y='Frequency', size='Frequency', 
                     title='Word Cloud delle Parole Chiave',
                     labels={'Word': 'Parola', 'Frequency': 'Frequenza'},
                     hover_name='Word')

    return fig

# Function to display general statistics
def general_statistics():
    total_articles = len(data)
    unique_authors = data['primo_autore'].nunique()
    language_distribution = data['lingua'].value_counts()
    return total_articles, unique_authors, language_distribution

# Gradio Interface
with gr.Blocks() as app:
    gr.Markdown("# Analisi degli Articoli di Storia dell'Arte")

    # General Statistics
    with gr.Row():
        total_articles, unique_authors, language_distribution = general_statistics()
        gr.Markdown(f"**Numero Totale di Articoli:** {total_articles}")
        gr.Markdown(f"**Autori Unici:** {unique_authors}")

    # Keyword search
    with gr.Row():
        keyword_input = gr.Textbox(label="Inserisci una parola chiave")
        search_button = gr.Button("Cerca")
    keyword_output = gr.Dataframe()

    search_button.click(search_by_keyword, inputs=keyword_input, outputs=keyword_output)

    # Authors plot
    with gr.Row():
        gr.Markdown("## Top 10 Autori per Numero di Articoli")
        authors_output = gr.Plot(plot_authors())  # Directly call the function

    # Publication years plot
    with gr.Row():
        gr.Markdown("## Numero di Articoli Pubblicati per Anno")
        years_output = gr.Plot(plot_publication_years())  # Directly call the function

    # Language distribution plot
    with gr.Row():
        gr.Markdown("## Distribuzione degli Articoli per Lingua")
        language_output = gr.Plot(plot_language_distribution())  # Directly call the function

    # Characters and words by author
    with gr.Row():
        gr.Markdown("## Totale Parole e Caratteri per Autore")
        characters_words_output = gr.Plot(plot_characters_words())  # Directly call the function

    # Common keywords by author
    with gr.Row():
        gr.Markdown("## Parole Chiave più Ricorrenti per Autore")
        keywords_output = gr.Plot(common_keywords_by_author())  # Directly call the function

    # Common places by author
    with gr.Row():
        gr.Markdown("## Luoghi più Ricorrenti per Autore")
        places_output = gr.Plot(common_places_by_author())  # Directly call the function

    # Word Cloud of Keywords using Plotly
    with gr.Row():
        gr.Markdown("## Word Cloud delle Parole Chiave")
        wordcloud_output = gr.Plot(word_cloud_keywords())  # Use Plotly for word cloud

# Launch the Gradio app
app.launch()
