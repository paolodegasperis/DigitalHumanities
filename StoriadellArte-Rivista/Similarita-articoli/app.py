import json
import numpy as np
import gradio as gr

# Funzione per calcolare la distanza coseno
def cosine_similarity(vec_a, vec_b):
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot_product / (norm_a * norm_b)

# Carica gli embeddings dal file JSON
def load_embeddings(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except UnicodeDecodeError as e:
        return f"Errore di codifica: {e}"
    except json.JSONDecodeError as e:
        return f"Errore di parsing JSON: {e}"
    except Exception as e:
        return f"Errore: {e}"

# Trova gli articoli simili
def find_similar_articles(input_title, embeddings_data, top_n=5):
    input_embedding = None
    for article in embeddings_data:
        if article['titolo_articolo'] == input_title:
            input_embedding = article['embedding']
            break

    if input_embedding is None:
        return f"Articolo '{input_title}' non trovato."

    similarities = []
    for article in embeddings_data:
        if article['titolo_articolo'] != input_title:
            similarity = cosine_similarity(input_embedding, article['embedding'])
            similarities.append((article['titolo_articolo'], similarity))

    # Ordina per somiglianza decrescente
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_n]

# Funzione principale per Gradio
def search_articles(input_title):
    similar_articles = find_similar_articles(input_title, embeddings_data)
    return similar_articles

# Autocompletamento dei titoli
def get_titles(embeddings_data):
    return [article['titolo_articolo'] for article in embeddings_data]

# Carica gli embeddings
file_path = 'embedded_articles.json'  # Percorso del tuo file JSON
embeddings_data = load_embeddings(file_path)

# Controlla se ci sono errori nel caricamento
if isinstance(embeddings_data, str):  # Se è un messaggio di errore
    print(embeddings_data)
else:
    # Configura l'interfaccia Gradio con autocompletamento
    title_choices = get_titles(embeddings_data)  # Ottieni i titoli

    iface = gr.Interface(
        fn=search_articles,
        inputs=gr.Dropdown(label="Titolo dell'articolo", choices=title_choices, type="value"),
        outputs=gr.Dataframe(label="Articoli simili"),
        title="Ricerca Articoli Simili",
        description="Seleziona il titolo di un articolo per trovare articoli semanticamente simili."
    )

    # Avvia l'interfaccia
    iface.launch(share=True)
