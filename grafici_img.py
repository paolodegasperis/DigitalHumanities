import json
import pandas as pd
import umap
import numpy as np
from sklearn.manifold import TSNE
import plotly.express as px

# Caricare gli embedding dal file JSON
input_file = "embeddings.json"
with open(input_file, 'r') as f:
    embeddings_data = json.load(f)

# Estrarre i nomi dei file e gli embedding
filenames = [item['filename'] for item in embeddings_data]
embeddings = np.array([item['embedding'] for item in embeddings_data])

# Funzione per creare il grafico e salvarlo come file HTML
def create_plot(embedding, method_name):
    df = pd.DataFrame(embedding, columns=['x', 'y'])
    df['filename'] = filenames

    fig = px.scatter(df, x='x', y='y', text='filename', title=f'{method_name} Visualization of Image Embeddings')
    fig.update_traces(textposition='top center')

    output_file = f'embeddings_{method_name}.html'
    fig.write_html(output_file)
    print(f"{method_name} visualization saved as {output_file}")

# Riduzione dimensionale con UMAP
umap_reducer = umap.UMAP(n_neighbors=15, min_dist=0.1)
embedding_umap = umap_reducer.fit_transform(embeddings)
create_plot(embedding_umap, 'UMAP')

# Riduzione dimensionale con T-SNE
tsne_reducer = TSNE(n_components=2, perplexity=30, n_iter=1000)
embedding_tsne = tsne_reducer.fit_transform(embeddings)
create_plot(embedding_tsne, 'TSNE')
