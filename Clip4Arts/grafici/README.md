
# Image Clustering and Visualization Scripts

This repository contains Python scripts that help cluster image embeddings and visualize them in 2D and 3D using various techniques such as K-Means, PCA, t-SNE, and more. These scripts are designed to work with image embeddings stored in a CSV file and can generate insightful visualizations to understand the clustering of images based on their similarity.

## Prerequisites

Ensure you have the following Python packages installed:

```bash
pip install pandas numpy scikit-learn plotly matplotlib Pillow
```

## Files Overview

### 1. `plot_barchart.py`
This script generates a bar chart showing the number of images in each cluster after applying K-Means clustering.

#### How to use:
```bash
python plot_barchart.py
```

- **Input**: The script reads the embeddings from `img/embeddings.csv` and applies K-Means clustering to divide the embeddings into clusters.
- **Output**: A bar chart showing the number of images in each cluster is generated and saved as an HTML file (`cluster_counts.html`).

#### Parameters:
- `n_clusters`: Number of clusters for K-Means (default is 10).
- The chart is interactive and viewable in any web browser.

---

### 2. `plot_clip01.py`
This script performs 2D PCA (Principal Component Analysis) on the embeddings and visualizes the clusters in a scatter plot.

#### How to use:
```bash
python plot_clip01.py
```

- **Input**: The script reads the embeddings from `img/embeddings.csv`.
- **Output**: A 2D scatter plot visualizing the image clusters based on PCA-reduced embeddings, saved as `image_clusters.html`.

#### Parameters:
- `n_clusters`: Number of clusters for K-Means (default is 10).
- The output scatter plot is interactive, with hover functionality displaying the image filenames.

---

### 3. `plot_imgcluster.py`
This script visualizes images grouped by their clusters, displaying images that belong to the same cluster side by side.

#### How to use:
```bash
python plot_imgcluster.py
```

- **Input**: The script reads the embeddings from `img/embeddings.csv` and organizes the images into clusters using K-Means.
- **Output**: The images from each cluster are saved as separate image files in the `cluster_visualizations` directory. Each file (`cluster_X.png`) contains images from the respective cluster.

#### Parameters:
- `n_clusters`: Number of clusters for K-Means (default is 10).

---

### 4. `plot-tsne.py`
This script uses t-SNE (t-distributed Stochastic Neighbor Embedding) to reduce the dimensionality of the embeddings and visualize them in 2D space.

#### How to use:
```bash
python plot-tsne.py
```

- **Input**: The script reads the embeddings from `img/embeddings.csv` and applies t-SNE for dimensionality reduction.
- **Output**: A 2D scatter plot (`image_clusters_tsne.html`) visualizing the t-SNE reduced embeddings.

#### Parameters:
- `n_clusters`: Number of clusters for K-Means (default is 10).
- The output scatter plot is interactive, with hover functionality displaying image filenames.

---

### 5. `plot3d.py`
This script performs PCA on the embeddings and visualizes them in a 3D scatter plot.

#### How to use:
```bash
python plot3d.py
```

- **Input**: The script reads the embeddings from `img/embeddings.csv` and applies PCA for 3D dimensionality reduction.
- **Output**: A 3D scatter plot (`image_clusters_3d.html`) visualizing the PCA-reduced embeddings.

#### Parameters:
- `n_clusters`: Number of clusters for K-Means (default is 10).
- The 3D scatter plot is interactive, allowing you to rotate and zoom in/out.

---

## General Workflow

1. **Prepare Embeddings**: All scripts assume that the embeddings of the images are stored in a CSV file (`img/embeddings.csv`), where each row corresponds to an image, and each column corresponds to a feature.
2. **Run the Script**: Depending on the desired visualization, run one of the scripts described above. Each script clusters the embeddings using K-Means and provides a different form of visualization.

---

## License

This project is licensed under the Creative Commons Attribution-ShareAlike (CC-BY-SA) License.
