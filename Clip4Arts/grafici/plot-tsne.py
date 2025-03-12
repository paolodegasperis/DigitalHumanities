import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import plotly.express as px

# Leggi il CSV con gli embeddings
embeddings_df = pd.read_csv('img/embeddings.csv', index_col='filename')

# Converte gli embeddings in un array numpy
embeddings = embeddings_df.values

# Applica K-means per trovare i cluster
n_clusters = 10  # Numero di cluster desiderato, puoi modificarlo
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(embeddings)

# Riduzione dimensionale con t-SNE per la visualizzazione 2D
tsne = TSNE(n_components=2, random_state=42)
reduced_embeddings = tsne.fit_transform(embeddings)

# Creazione di un DataFrame per la visualizzazione
visualization_df = pd.DataFrame(reduced_embeddings, columns=['TSNE1', 'TSNE2'])
visualization_df['label'] = labels
visualization_df['filename'] = embeddings_df.index

# Creazione del grafico interattivo con Plotly
fig = px.scatter(
    visualization_df,
    x='TSNE1',
    y='TSNE2',
    color='label',
    hover_data=['filename'],
    title='t-SNE Image Clusters Visualization'
)

# Mostra il grafico
fig.show()

# Salva il grafico come file HTML
fig.write_html("image_clusters_tsne.html")
