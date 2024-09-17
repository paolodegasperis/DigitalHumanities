
# Image Clustering Using CLIP and OpenCLIP

This repository contains scripts that cluster images based on their conceptual similarity using CLIP and OpenCLIP models. It generates embeddings for images and organizes them into clusters based on cosine similarity.

## Files

- `clip_large.py`: Clusters images using the CLIP large model.
- `clip_small.py`: Clusters images using the CLIP small model.
- `openclip_large.py`: Clusters images using the OpenCLIP large model.
- `openclip_small.py`: Clusters images using the OpenCLIP small model.
- `improved_image_clustering.py`: An improved version of the clustering script with additional features.

## Requirements

Make sure you have the following installed:

- Python 3.x
- `torch`
- `transformers`
- `scikit-learn`
- `Pillow`
- `tqdm`
- `numpy`
- `pandas`

You can install the required libraries by running:

```bash
pip install torch transformers scikit-learn Pillow tqdm numpy pandas
```

## Usage

### Basic Example

1. **Run the script** for large CLIP models:

```bash
python clip_large.py --image_directory /path/to/images --output_directory /path/to/output --similarity_threshold 0.8
```

2. **Run the script** for small OpenCLIP models:

```bash
python openclip_small.py --image_directory /path/to/images --output_directory /path/to/output --similarity_threshold 0.8
```

### Arguments:

- `--image_directory`: Path to the directory containing your images (JPEG, JPG, PNG).
- `--output_directory`: Path where the clustered images will be saved. Defaults to `output/`.
- `--similarity_threshold`: Threshold for cosine similarity when clustering. Lower values will create more clusters.

### Improved Clustering

The `improved_image_clustering.py` script offers additional features such as standardized embeddings and more robust error handling.

Run it with:

```bash
python improved_image_clustering.py --image_directory /path/to/images --output_directory /path/to/output --similarity_threshold 0.8
```

## Output

- The clustered images will be saved in directories named `cluster_X` in the specified `output_directory`.
- A CSV file containing the embeddings and image filenames will be saved as `embeddings.csv`.

## License

This project is licensed under the Creative Commons Attribution-ShareAlike (CC-BY-SA) License.
