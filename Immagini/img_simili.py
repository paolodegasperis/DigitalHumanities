import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# Caricare gli embedding dal file JSON
input_file = "embeddings.json"
with open(input_file, 'r') as f:
    embeddings_data = json.load(f)

# Estrarre i nomi dei file e gli embedding
filenames = [item['filename'] for item in embeddings_data]
embeddings = np.array([item['embedding'] for item in embeddings_data])

# Calcolare la matrice di similarità coseno
similarity_matrix = cosine_similarity(embeddings)

# Ottenere le 10 coppie di immagini più simili
n_pairs = 10
similarity_scores = []

for i in range(len(filenames)):
    for j in range(i + 1, len(filenames)):
        similarity_scores.append((filenames[i], filenames[j], similarity_matrix[i, j]))

# Ordinare le coppie per similarità decrescente e prendere le prime 10
top_pairs = sorted(similarity_scores, key=lambda x: x[2], reverse=True)[:n_pairs]

# Creare un DataFrame per visualizzare le coppie
pair_df = pd.DataFrame(top_pairs, columns=['Image1', 'Image2', 'Similarity'])

# Creare il grafico
fig = px.scatter(pair_df, x='Image1', y='Image2', text='Similarity', title='Top 10 Most Similar Image Pairs')
fig.update_traces(textposition='top center')

# Salvare il grafico come file HTML
output_file = 'top_10_similar_pairs.html'
fig.write_html(output_file)
print(f"Top 10 most similar image pairs visualization saved as {output_file}")
