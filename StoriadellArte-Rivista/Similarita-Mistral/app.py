import json
import numpy as np
import gradio as gr
import logging

# Configurazione del logging per errori
logging.basicConfig(filename="error.log", level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Funzione per calcolare la similarità coseno
def cosine_similarity(vec_a, vec_b):
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

# Funzione per caricare gli embeddings dal file JSON
def load_embeddings(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except UnicodeDecodeError as e:
        logging.error(f"Errore di codifica nel caricamento del file JSON: {e}")
        return f"Errore: {e}"
    except json.JSONDecodeError as e:
        logging.error(f"Errore di parsing JSON: {e}")
        return f"Errore: {e}"
    except Exception as e:
        logging.error(f"Errore generico nel caricamento del file JSON: {e}")
        return f"Errore: {e}"

# Funzione per trovare gli articoli simili
def find_similar_articles(input_title, embeddings_data):
    input_embedding = None
    # Trova l'embedding dell'articolo di riferimento
    for article in embeddings_data:
        if article['titolo_articolo'] == input_title:
            input_embedding = article['embedding']
            break

    if input_embedding is None:
        error_message = f"Articolo '{input_title}' non trovato."
        logging.error(error_message)
        return None, None, error_message

    similarities = []
    # Calcola la similarità per ogni articolo (diverso dall'articolo di riferimento)
    for article in embeddings_data:
        if article['titolo_articolo'] != input_title:
            try:
                similarity = cosine_similarity(input_embedding, article['embedding'])
            except Exception as e:
                logging.error(f"Errore nel calcolo della similarità per l'articolo {article['titolo_articolo']}: {e}")
                similarity = 0.0
            # Costruzione del link per il download del PDF
            pdf_url = f"https://storiadellarterivista.it/data/pdf/{article['testo_pdf']}"
            pdf_link = f'<a href="{pdf_url}" download>{article["testo_pdf"]}</a>'
            similarities.append({
                "titolo_articolo": article['titolo_articolo'],
                "similarity": similarity,
                "pdf_link": pdf_link
            })
    # Ordina gli articoli in ordine decrescente per similarità
    similarities_sorted = sorted(similarities, key=lambda x: x['similarity'], reverse=True)
    top_5 = similarities_sorted[:5]
    # Ordina in ordine crescente per ottenere i 5 articoli con minore similarità
    bottom_5 = sorted(similarities, key=lambda x: x['similarity'])[:5]
    return top_5, bottom_5, None

# Funzione per generare una tabella HTML a partire da una lista di articoli
def generate_html_table(articles, title):
    html = f"<h3>{title}</h3>"
    html += '<table border="1" style="border-collapse: collapse; width:100%;">'
    html += "<tr><th>Titolo Articolo</th><th>Similarità</th><th>PDF</th></tr>"
    for art in articles:
        html += f"<tr><td>{art['titolo_articolo']}</td><td>{art['similarity']:.3f}</td><td>{art['pdf_link']}</td></tr>"
    html += "</table>"
    return html

# Funzione principale chiamata dall'interfaccia GRADIO
def search_articles(input_title):
    top_5, bottom_5, error = find_similar_articles(input_title, embeddings_data)
    if error:
        return error, error
    top_table = generate_html_table(top_5, "Top 5 Articoli più simili")
    bottom_table = generate_html_table(bottom_5, "Bottom 5 Articoli meno simili")
    return top_table, bottom_table

# Funzione per ottenere l'elenco dei titoli (per l'autocompletamento)
def get_titles(embeddings_data):
    return [article['titolo_articolo'] for article in embeddings_data]

# Caricamento degli embeddings
file_path = 'all_embeddings.json'  # Percorso del file JSON contenente gli embeddings
embeddings_data = load_embeddings(file_path)

# Controllo di eventuali errori nel caricamento
if isinstance(embeddings_data, str):
    logging.error(embeddings_data)
    print(embeddings_data)
else:
    title_choices = get_titles(embeddings_data)
    iface = gr.Interface(
        fn=search_articles,
        inputs=gr.Dropdown(label="Titolo dell'articolo", choices=title_choices, type="value"),
        outputs=[gr.HTML(label="Articoli più simili"), gr.HTML(label="Articoli meno simili")],
        title="Ricerca Articoli Simili",
        description=("Seleziona il titolo di un articolo per trovare quelli semanticamente simili. "
                     "Vengono mostrati i 5 articoli con maggiore similarità e i 5 con minore similarità, "
                     "con il coefficiente di similarità e un link per il download del PDF.")
    )
    iface.launch(share=True)
