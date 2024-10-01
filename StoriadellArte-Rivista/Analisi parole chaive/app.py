import pandas as pd
import plotly.express as px
import gradio as gr

# Funzione per l'analisi della parola chiave
def keyword_analysis(df, keyword):
    # Filtra il dataset per la parola chiave indicata
    df_filtered = df[df['keyword'].str.contains(keyword, case=False, na=False)]
    
    if df_filtered.empty:
        return (
            "Nessun articolo trovato con la parola chiave indicata.",
            None,
            None,
            None,
            pd.DataFrame()
        )

    # Distribuzione temporale (grafico interattivo degli anni)
    df_year = df_filtered['anno_pubblicazione'].value_counts().sort_index()
    fig_year = px.line(
        x=df_year.index, 
        y=df_year.values, 
        labels={'x': 'Anno', 'y': 'Frequenza'},
        title=f'Ricorrenza della parola chiave "{keyword}" per anno'
    )

    # Frequenza degli autori (grafico interattivo degli autori)
    df_authors = df_filtered['primo_autore'].value_counts()
    fig_authors = px.bar(
        x=df_authors.index, 
        y=df_authors.values, 
        labels={'x': 'Autori', 'y': 'Numero di articoli'},
        title=f'Autori che citano la parola chiave "{keyword}"',
    )
    fig_authors.update_layout(xaxis_tickangle=-45)

    # Frequenza dei luoghi (grafico interattivo dei luoghi)
    df_places = df_filtered['luoghi_citati'].dropna().str.split(',').explode().str.strip().value_counts()
    fig_places = px.bar(
        x=df_places.index[:10],  # Mostra solo i primi 10 luoghi
        y=df_places.values[:10],
        labels={'x': 'Luoghi', 'y': 'Frequenza'},
        title=f'Luoghi citati in relazione alla parola chiave "{keyword}"'
    )
    fig_places.update_layout(xaxis_tickangle=-45)

    # Tabella degli articoli associati alla parola chiave
    table_columns = ['titolo_articolo', 'primo_autore', 'anno_pubblicazione', 'luoghi_citati']
    df_table = df_filtered[table_columns].reset_index(drop=True)

    return fig_year, fig_authors, fig_places, df_table

# Funzione per creare l'interfaccia Gradio
def gradio_interface():
    dataset_path = "sa_dataset.csv"  # Percorso del dataset hardcoded
    df = pd.read_csv(dataset_path)  # Carica il dataset

    # Impostiamo l'interfaccia con layout verticale e grafici interattivi che occupano il 100% della larghezza
    with gr.Blocks() as iface:
        # Testata con input
        with gr.Row():
            gr.Markdown("# Analisi della Parola Chiave")
            keyword_input = gr.Textbox(label="Inserisci una parola chiave", placeholder="Inserisci una parola chiave per visualizzare i risultati")

        # Grafici disposti verticalmente, ognuno al 100% della larghezza disponibile
        with gr.Column(scale=100):
            keyword_year_plot = gr.Plot()
            keyword_authors_plot = gr.Plot()
            keyword_places_plot = gr.Plot()

        # Tabella articoli correlati
        keyword_table = gr.Dataframe()

        # Funzione collegata al campo di input
        def update_output(keyword):
            return keyword_analysis(df, keyword)

        # Associa l'input con i grafici e la tabella
        keyword_input.submit(update_output, inputs=keyword_input, outputs=[keyword_year_plot, keyword_authors_plot, keyword_places_plot, keyword_table])

    iface.launch(share=True)

gradio_interface()
