import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
from matplotlib import pyplot as plt

# Leggi il CSV con gli embeddings
embeddings_df = pd.read_csv('img/embeddings.csv', index_col='filename')

# Converte gli embeddings in un array numpy
embeddings = embeddings_df.values

# Applica K-means per trovare i cluster
n_clusters = 10  # Numero di cluster desiderato, puoi modificarlo
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(embeddings)

# Crea una directory per visualizzare le immagini dei cluster
output_dir = 'cluster_visualizations'
os.makedirs(output_dir, exist_ok=True)

# Organizza le immagini nei cluster e salva le visualizzazioni
for cluster in range(n_clusters):
    cluster_indices = np.where(labels == cluster)[0]
    cluster_images = [embeddings_df.index[i] for i in cluster_indices]

    fig, axes = plt.subplots(1, len(cluster_images), figsize=(20, 5))
    for ax, img_path in zip(axes, cluster_images):
        img = Image.open(os.path.join('img', img_path))
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(img_path)
    
    plt.suptitle(f'Cluster {cluster}')
    plt.savefig(os.path.join(output_dir, f'cluster_{cluster}.png'))
    plt.close()
