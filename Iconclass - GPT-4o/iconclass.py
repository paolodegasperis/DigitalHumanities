import os
import base64
import requests
import asyncio
import csv
import logging
import imghdr
from tqdm import tqdm

# Configura il logging
logging.basicConfig(filename='image_analysis.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# API Key e URL per OpenAI
api_key = 'YOUR_API_KEY'
api_url = "https://api.openai.com/v1/chat/completions"

# Funzione per codificare l'immagine in base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Errore nella codifica dell'immagine {image_path}: {e}")
        return None

# Funzione per verificare se il file è un'immagine valida
def is_valid_image(image_path):
    try:
        img_type = imghdr.what(image_path)
        return img_type is not None
    except Exception as e:
        logging.error(f"Errore nel controllo dell'immagine {image_path}: {e}")
        return False

# Funzione per analizzare l'immagine
def analyze_image(image_base64, query):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response_json = response.json()

        # Log della risposta ricevuta
        logging.error(f"Risposta del modello per l'immagine: {response_json}")
        
        return response_json.get('choices', [{}])[0].get('message', {}).get('content', "")
    except Exception as e:
        logging.error(f"Errore nell'analisi dell'immagine: {e}")
        return None

# Funzione asincrona per processare ogni immagine
async def process_image(idx, image_name, sem):
    async with sem:
        image_path = os.path.join(image_folder, image_name)
        if not os.path.isfile(image_path):
            logging.error(f"{image_path} non è un file valido.")
            return None

        if not is_valid_image(image_path):
            logging.error(f"{image_path} non è un'immagine valida.")
            return None

        image_base64 = encode_image_to_base64(image_path)
        if image_base64 is None:
            logging.error(f"Impossibile codificare l'immagine {image_path}")
            return None

        query = "Descrivi questa immagine e assegna i codici Iconclass separati da virgole, con il prefisso 'Codici Iconclass:' per ogni codice."

        response_content = analyze_image(image_base64, query)
        if response_content is None:
            logging.error(f"Impossibile analizzare l'immagine {image_path}")
            return None

        # Parsing del contenuto della risposta
        description = ""
        interpretation = ""
        iconclass_codes = []

        lines = response_content.strip().split('\n')
        for line in lines:
            if line.startswith("Descrizione:"):
                description = line[len("Descrizione:"):].strip()
            elif line.startswith("Interpretazione:"):
                interpretation = line[len("Interpretazione:"):].strip()
            elif line.startswith("Codici Iconclass:"):
                codes = line[len("Codici Iconclass:"):].strip()
                iconclass_codes = [code.strip() for code in codes.split(',')]

        return {
            "Id": idx,
            "Immagine": image_name,
            "Description": description,
            "Interpretation": interpretation,
            "Iconclass01": iconclass_codes[0] if len(iconclass_codes) > 0 else "",
            "Iconclass02": iconclass_codes[1] if len(iconclass_codes) > 1 else "",
            "Iconclass03": iconclass_codes[2] if len(iconclass_codes) > 2 else ""
        }

# Funzione per scrivere i risultati su CSV
def write_results_to_csv(results, output_file):
    fieldnames = ["Id", "Immagine", "Description", "Interpretation", "Iconclass01", "Iconclass02", "Iconclass03"]
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            if result:
                writer.writerow(result)

# Funzione principale
async def main():
    global image_folder
    image_folder = "img"
    images = os.listdir(image_folder)

    # Semaforo per limitare la concorrenza e rispettare i rate limit dell'API
    sem = asyncio.Semaphore(5)  # Puoi modificare il valore in base ai limiti dell'API

    # Barra di progresso
    pbar = tqdm(total=len(images), desc="Elaborazione immagini")

    async def process_image_with_progress(idx, image_name, sem):
        result = await process_image(idx, image_name, sem)
        pbar.update(1)
        if result:
            print(f"Immagine {image_name} elaborata con successo.")
        else:
            print(f"Elaborazione dell'immagine {image_name} fallita.")
        return result

    tasks = []
    for idx, image_name in enumerate(images, start=1):
        tasks.append(process_image_with_progress(idx, image_name, sem))

    results = await asyncio.gather(*tasks)
    pbar.close()

    # Scrittura dei risultati su CSV
    output_file = "image_analysis_results.csv"
    write_results_to_csv(results, output_file)

    print(f"\nAnalisi completata. I risultati sono stati salvati in {output_file}.")

# Esecuzione del programma
if __name__ == '__main__':
    asyncio.run(main())
