import pandas as pd
import torch
from transformers import CLIPProcessor, CLIPModel
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import gradio as gr
from pathlib import Path

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
    
    # Restituisci i percorsi delle immagini più simili e i loro punteggi
    return [(Path("img") / image_paths[i], similarities[i]) for i in top_indices]

def predict(query_text):
    similar_images = query_images(query_text, model, processor, embeddings, image_paths, device)
    image_outputs = []
    scores = []
    
    for img_path, score in similar_images:
        img = Image.open(img_path)
        image_outputs.append(img)
        scores.append(score)
    
    # Formatta i punteggi per il DataFrame
    scores_formatted = [[score] for score in scores]  # Converti in una lista di liste
    return image_outputs, scores_formatted  # Restituisci le immagini e i punteggi

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, processor = load_clip_model(device)

    # Carica gli embeddings dal file CSV
    embedding_file = "embeddings.csv"  # Sostituisci con il percorso corretto
    embeddings, image_paths = load_embeddings(embedding_file)

    # Crea l'interfaccia Gradio
    interface = gr.Interface(
        fn=predict,
        inputs="text",
        outputs=[
            gr.Gallery(label="Similar Images", elem_id="image_gallery"), 
            gr.Dataframe(label="Similarity Scores", headers=["Score"])  # Rimosso show_footer
        ],
        title="Find Similar Images",
        description="Insert text to find the three most similar images."
    )

    interface.launch()
