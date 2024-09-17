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

def load_clip_model(device):
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14-336").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14-336")
    return model, processor

def is_valid_image(image_path):
    try:
        Image.open(image_path).verify()
        return True
    except (UnidentifiedImageError, IOError):
        return False

def collect_image_paths(image_directory):
    image_extensions = ["*.jpg", "*.jpeg", "*.png"]
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(Path(image_directory).rglob(ext))
    return image_paths

def generate_embeddings(image_directory, model, processor, device):
    image_paths = collect_image_paths(image_directory)
    valid_image_paths = []
    embeddings = []

    for image_path in tqdm(image_paths, desc="Processing images", unit="image"):
        if not is_valid_image(image_path):
            print(f"Invalid image file: {image_path}")
            continue

        try:
            image = Image.open(image_path).convert("RGB")
            inputs = processor(images=image, return_tensors="pt", padding=True).to(device)
            with torch.no_grad():
                outputs = model.get_image_features(**inputs)
            embeddings.append(outputs.cpu().numpy().flatten())
            valid_image_paths.append(image_path)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            continue

    return np.array(embeddings), valid_image_paths

def cluster_images(embeddings, similarity_threshold):
    # Compute cosine similarity matrix
    cosine_sim_matrix = cosine_similarity(embeddings)

    # Convert similarity to distance matrix
    distance_matrix = 1 - cosine_sim_matrix

    # Perform agglomerative clustering
    clustering_model = AgglomerativeClustering(
        n_clusters=None,
        affinity='precomputed',
        linkage='average',
        distance_threshold=1 - similarity_threshold
    )
    labels = clustering_model.fit_predict(distance_matrix)
    return labels

def organize_images_into_clusters(labels, image_paths, output_directory):
    cluster_to_images = defaultdict(list)

    for label, image_path in zip(labels, image_paths):
        cluster_to_images[label].append(image_path)

    for cluster_label, images in tqdm(cluster_to_images.items(), desc="Organizing clusters", unit="cluster"):
        cluster_dir = output_directory / f"cluster_{cluster_label}"
        cluster_dir.mkdir(parents=True, exist_ok=True)

        for image_path in images:
            destination = cluster_dir / image_path.name
            if not destination.exists():
                shutil.move(str(image_path), destination)
            else:
                print(f"File {destination} already exists. Skipping.")

    print(f"Organized images into {len(cluster_to_images)} clusters.")

def save_embeddings_to_csv(embeddings, image_paths, output_file):
    df = pd.DataFrame(embeddings, index=[str(p) for p in image_paths])
    df.to_csv(output_file, index_label="filepath")
    print(f"Embeddings saved to {output_file}")

def main(image_directory="img", output_directory="output", similarity_threshold=0.8):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, processor = load_clip_model(device)

    embeddings, valid_image_paths = generate_embeddings(image_directory, model, processor, device)

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
    parser = argparse.ArgumentParser(description="Cluster images based on conceptual similarity using CLIP embeddings.")
    parser.add_argument("--image_directory", type=str, required=True, help="Path to the directory containing images.")
    parser.add_argument("--output_directory", type=str, default="output", help="Path to the directory to save clustered images.")
    parser.add_argument("--similarity_threshold", type=float, default=0.8, help="Threshold for clustering based on cosine similarity. Lower values create more clusters.")

    args = parser.parse_args()
    main(args.image_directory, args.output_directory, args.similarity_threshold)
