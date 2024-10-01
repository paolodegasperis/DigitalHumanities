import pandas as pd
import torch
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

def load_clip_model(device):
    model = CLIPModel.from_pretrained("laion/CLIP-ViT-L-14-laion2B-s32B-b82K").to(device)
    processor = CLIPProcessor.from_pretrained("laion/CLIP-ViT-L-14-laion2B-s32B-b82K")
    return model, processor

def load_embeddings(embedding_file):
    df = pd.read_csv(embedding_file)
    embeddings = df.iloc[:, 1:].values  # Escludi la prima colonna (filename)
    image_paths = df['filename'].tolist()  # Salva i nomi dei file
    return embeddings, image_paths

def query_images(text, model, processor, image_embeddings, image_paths, device):
    # Genera l'embedding per il testo
    text_inputs = processor(text=[text], return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        text_embedding = model.get_text_features(**text_inputs).cpu().numpy().flatten()
    
    # Calcola la similarità coseno tra l'embedding del testo e gli embeddings delle immagini
    similarities = cosine_similarity([text_embedding], image_embeddings)[0]
    
    # Ottieni gli indici delle tre immagini più simili
    top_indices = similarities.argsort()[-3:][::-1]
    
    # Restituisci le immagini più simili
    return [(image_paths[i], similarities[i]) for i in top_indices]

def main(embedding_file, query_text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, processor = load_clip_model(device)
    
    # Carica gli embeddings dal file CSV
    embeddings, image_paths = load_embeddings(embedding_file)
    
    # Trova le immagini più simili al testo
    similar_images = query_images(query_text, model, processor, embeddings, image_paths, device)
    
    # Stampa i risultati
    for img_path, score in similar_images:
        print(f"Image: {img_path}, Similarity Score: {score}")

if __name__ == "__main__":
    embedding_file = "embeddings.csv"  # Sostituisci con il percorso corretto
    query_text = input("The image of a dog")
    main(embedding_file, query_text)
