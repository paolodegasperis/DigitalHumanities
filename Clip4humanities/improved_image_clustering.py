
import os
import shutil
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from PIL import Image, UnidentifiedImageError
from tqdm.auto import tqdm
from collections import defaultdict
from transformers import CLIPProcessor, CLIPModel
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import concurrent.futures
import multiprocessing
import logging

# Setting up the logging mechanism
logging.basicConfig(filename="image_clustering.log", level=logging.ERROR)

# Improvement 1: Batch processing implementation to avoid memory consumption issues.
def load_clip_model(device):
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")
    return model, processor

def is_valid_image(image_path):
    try:
        Image.open(image_path).verify()
        return True
    except (UnidentifiedImageError, IOError):
        logging.error(f"Invalid image file: {image_path}")
        return False

def collect_image_paths(image_directory):
    image_extensions = ["*.jpg", "*.jpeg", "*.png"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(Path(image_directory).rglob(ext))
    return image_paths

# Improved batch processing for large datasets
def generate_embeddings_in_batches(image_paths, model, processor, device, batch_size=32):
    embeddings = []
    valid_image_paths = []

    def process_batch(batch):
        batch_embeddings = []
        for image_path in batch:
            try:
                image = Image.open(image_path).convert("RGB")
                inputs = processor(images=image, return_tensors="pt", padding=True).to(device)
                with torch.no_grad():
                    outputs = model.get_image_features(**inputs)
                batch_embeddings.append(outputs.cpu().numpy().flatten())
                valid_image_paths.append(image_path)
            except Exception as e:
                logging.error(f"Error processing {image_path}: {e}")
                continue
        return batch_embeddings

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(image_paths), batch_size):
            batch = image_paths[i:i + batch_size]
            futures.append(executor.submit(process_batch, batch))

        for future in tqdm(concurrent.futures.as_completed(futures), desc="Processing batches", total=len(futures)):
            embeddings.extend(future.result())

    return np.array(embeddings), valid_image_paths

# Improvement 3: More detailed logging and error handling is already integrated above.
# Improvement 2: Granular progress updates - we enhanced the progress reporting by breaking it into batches

def cluster_images(embeddings, similarity_threshold):
    cosine_sim_matrix = cosine_similarity(embeddings)
    distance_matrix = 1 - cosine_sim_matrix
    clustering_model = AgglomerativeClustering(n_clusters=None, affinity='precomputed', linkage='average', distance_threshold=1 - similarity_threshold)
    labels = clustering_model.fit_predict(distance_matrix)
    return labels

# Improvement 4: Ability to load previously saved embeddings from a CSV file.
def load_existing_embeddings(csv_file):
    try:
        df = pd.read_csv(csv_file, index_col="filename")
        embeddings = df.values
        image_paths = df.index.tolist()
        return embeddings, image_paths
    except Exception as e:
        logging.error(f"Error loading embeddings from file: {e}")
        return None, None

def save_embeddings_to_csv(embeddings, image_paths, output_file):
    df = pd.DataFrame(embeddings, index=[p.name for p in image_paths])
    df.to_csv(output_file, index_label="filename")
    print(f"Embeddings saved to {output_file}")

# Improvement 5: Parallel processing using multiprocessing for faster execution
def organize_images_into_clusters(labels, image_paths, output_directory):
    cluster_to_images = defaultdict(list)

    for label, image_path in zip(labels, image_paths):
        cluster_to_images[label].append(image_path)

    def process_cluster(cluster_label, images):
        cluster_dir = output_directory / f"cluster_{cluster_label}"
        cluster_dir.mkdir(parents=True, exist_ok=True)
        for image_path in images:
            try:
                shutil.move(str(image_path), cluster_dir / image_path.name)
            except Exception as e:
                logging.error(f"Error moving file {image_path}: {e}")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_cluster, cluster_label, images) for cluster_label, images in cluster_to_images.items()]
        for future in tqdm(concurrent.futures.as_completed(futures), desc="Organizing clusters", total=len(futures)):
            pass

def main(image_directory="img", output_directory="output", similarity_threshold=0.8, batch_size=32, embeddings_file=None):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, processor = load_clip_model(device)

    if embeddings_file and Path(embeddings_file).exists():
        print(f"Loading embeddings from {embeddings_file}")
        embeddings, valid_image_paths = load_existing_embeddings(embeddings_file)
    else:
        image_paths = collect_image_paths(image_directory)
        embeddings, valid_image_paths = generate_embeddings_in_batches(image_paths, model, processor, device, batch_size=batch_size)

        if embeddings.size == 0:
            print("No valid images found for processing.")
            return

        # Normalize embeddings
        scaler = StandardScaler()
        embeddings = scaler.fit_transform(embeddings)

        # Save embeddings to CSV
        output_file = Path(image_directory) / "embeddings.csv"
        save_embeddings_to_csv(embeddings, valid_image_paths, output_file)

    labels = cluster_images(embeddings, similarity_threshold)

    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    organize_images_into_clusters(labels, valid_image_paths, output_directory)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cluster images based on conceptual similarity using CLIP embeddings with improvements.")
    parser.add_argument("--image_directory", type=str, required=True, help="Path to the directory containing images.")
    parser.add_argument("--output_directory", type=str, default="output", help="Path to the directory to save clustered images.")
    parser.add_argument("--similarity_threshold", type=float, default=0.8, help="Threshold for clustering based on cosine similarity.")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for processing images.")
    parser.add_argument("--embeddings_file", type=str, help="Path to an existing embeddings CSV file for clustering.")
    
    args = parser.parse_args()
    main(args.image_directory, args.output_directory, args.similarity_threshold, args.batch_size, args.embeddings_file)
