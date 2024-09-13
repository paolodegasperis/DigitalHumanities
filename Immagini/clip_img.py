import os
import json
import torch
import clip
from PIL import Image

# Caricare il modello CLIP e il preprocessore
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Percorso della cartella delle immagini
images_folder = "images"

# Lista per memorizzare i risultati
embeddings = []

# Iterare su tutti i file nella cartella delle immagini
for filename in os.listdir(images_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Aggiungere altre estensioni se necessario
        image_path = os.path.join(images_folder, filename)
        
        # Caricare e preprocessare l'immagine
        image = Image.open(image_path)
        image = preprocess(image).unsqueeze(0).to(device)
        
        # Calcolare l'embedding dell'immagine
        with torch.no_grad():
            image_features = model.encode_image(image)
        
        # Convertire l'embedding in una lista di numeri
        embedding_list = image_features.squeeze().cpu().numpy().tolist()
        
        # Aggiungere il risultato alla lista
        embeddings.append({
            "filename": filename,
            "embedding": embedding_list
        })

# Salvare i risultati in un file JSON
output_file = "embeddings.json"
with open(output_file, 'w') as f:
    json.dump(embeddings, f, indent=4)

print(f"Embeddings salvati in {output_file}")
