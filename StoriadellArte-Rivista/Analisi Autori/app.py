import pandas as pd
import plotly.express as px
import gradio as gr

# Funzione per l'analisi dell'autore
def author_analysis(df, selected_author):
    # Filtra il dataset per l'autore selezionato
    df_author = df[df['primo_autore'] == selected_author]
    
    if df_author.empty:
        return (
            "Nessun articolo trovato per l'autore selezionato.",
            None,
            None,
            None,
            None,
            pd.DataFrame()
        )

    # Tabella degli articoli scritti dall'autore
    table_columns = ['titolo_articolo', 'anno_pubblicazione', 'luoghi_citati', 'num_parole']
    df_table = df_author[table_columns].reset_index(drop=True)

    # Statistiche sul numero di parole usate dall'autore
    max_words = df_author['num_parole'].max()
    min_words = df_author['num_parole'].min()
    mean_words = df_author['num_parole'].mean()

    stats_df = pd.DataFrame({
        'Statistiche': ['Numero massimo di parole', 'Numero medio di parole', 'Numero minimo di parole'],
        'Valore': [max_words, mean_words, min_words]
    })
    fig_stats = px.bar(
        stats_df, 
        x='Statistiche', 
        y='Valore', 
        labels={'Valore': 'Numero di parole'},
        title=f'Statistiche sul numero di parole per l\'autore "{selected_author}"',
        color='Statistiche'
    )

    # Le 20 parole chiave più frequenti nei suoi articoli
    keywords_series = df_author['keyword'].str.split(',').explode().str.strip()
    keyword_counts = keywords_series.value_counts().head(20)
    fig_keywords = px.bar(
        x=keyword_counts.index, 
        y=keyword_counts.values, 
        labels={'x': 'Parole Chiave', 'y': 'Frequenza'},
        title=f'Le 20 parole chiave più frequenti per l\'autore "{selected_author}"',
    )
    fig_keywords.update_layout(xaxis_tickangle=-45)

    # I 20 luoghi più citati nei suoi articoli
    places_series = df_author['luoghi_citati'].dropna().str.split(',').explode().str.strip()
    places_counts = places_series.value_counts().head(20)
    fig_places = px.bar(
        x=places_counts.index, 
        y=places_counts.values, 
        labels={'x': 'Luoghi', 'y': 'Frequenza'},
        title=f'I 20 luoghi più citati per l\'autore "{selected_author}"'
    )
    fig_places.update_layout(xaxis_tickangle=-45)

    # Grafico degli anni in cui l'autore ha scritto più articoli
    df_years = df_author['anno_pubblicazione'].value_counts().sort_index()
    fig_years = px.bar(
        x=df_years.index, 
        y=df_years.values, 
        labels={'x': 'Anno', 'y': 'Numero di articoli'},
        title=f'Numero di articoli per anno dell\'autore "{selected_author}"'
    )
    fig_years.update_layout(xaxis_tickangle=-45)

    return fig_stats, fig_keywords, fig_places, fig_years, df_table

# Funzione per creare l'interfaccia Gradio
def gradio_interface():
    dataset_path = "sa_dataset.csv"  # Percorso del dataset hardcoded
    df = pd.read_csv(dataset_path)  # Carica il dataset
    
    # Crea una lista unica di autori per il menu a tendina
    authors = df['primo_autore'].dropna().unique().tolist()
    authors.sort()

    # Impostiamo l'interfaccia
    with gr.Blocks() as iface:
        # Menu a tendina per selezionare l'autore
        with gr.Row():
            gr.Markdown("# Analisi dell'Autore")
            author_input = gr.Dropdown(choices=authors, label="Seleziona un autore")

        # Grafici disposti verticalmente
        with gr.Column(scale=100):
            stats_plot = gr.Plot()
            keywords_plot = gr.Plot()
            places_plot = gr.Plot()
            years_plot = gr.Plot()  # Nuovo grafico per la distribuzione degli articoli per anno

        # Tabella articoli correlati
        author_table = gr.Dataframe()

        # Funzione collegata al menu a tendina
        def update_output(selected_author):
            return author_analysis(df, selected_author)

        # Associa l'input del menu a tendina con i grafici e la tabella
        author_input.change(update_output, inputs=author_input, outputs=[stats_plot, keywords_plot, places_plot, years_plot, author_table])

    iface.launch(share=True)

gradio_interface()
