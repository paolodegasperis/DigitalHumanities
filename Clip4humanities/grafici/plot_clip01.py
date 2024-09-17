import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px

# Leggi il CSV con gli embeddings
embeddings_df = pd.read_csv('img/embeddings.csv', index_col='filename')

# Converte gli embeddings in un array numpy
embeddings = embeddings_df.values

# Applica K-means per trovare i cluster
n_clusters = 10  # Numero di cluster desiderato, puoi modificarlo
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(embeddings)

# Riduzione dimensionale con PCA per la visualizzazione 2D
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(embeddings)

# Creazione di un DataFrame per la visualizzazione
visualization_df = pd.DataFrame(reduced_embeddings, columns=['PCA1', 'PCA2'])
visualization_df['label'] = labels
visualization_df['filename'] = embeddings_df.index

# Creazione del grafico interattivo con Plotly
fig = px.scatter(
    visualization_df,
    x='PCA1',
    y='PCA2',
    color='label',
    hover_data=['filename'],
    title='Image Clusters Visualization'
)

# Mostra il grafico
fig.show()

# Salva il grafico come file HTML
fig.write_html("image_clusters.html")
