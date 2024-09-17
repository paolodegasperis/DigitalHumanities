import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px

# Leggi il CSV con gli embeddings
embeddings_df = pd.read_csv('img/embeddings.csv', index_col='filename')

# Converte gli embeddings in un array numpy
embeddings = embeddings_df.values

# Applica K-means per trovare i cluster
n_clusters = 10  # Numero di cluster desiderato, puoi modificarlo
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(embeddings)

# Conta il numero di immagini in ciascun cluster
cluster_counts = np.bincount(labels)

# Creazione di un DataFrame per la visualizzazione
cluster_df = pd.DataFrame({'Cluster': np.arange(n_clusters), 'Count': cluster_counts})

# Creazione del grafico a barre con Plotly
fig = px.bar(
    cluster_df,
    x='Cluster',
    y='Count',
    title='Number of Images in Each Cluster',
    labels={'Cluster': 'Cluster', 'Count': 'Number of Images'}
)

# Mostra il grafico
fig.show()

# Salva il grafico come file HTML
fig.write_html("cluster_counts.html")
