import os
import csv
from openai import OpenAI

# Inizializza il client OpenAI con la tua API Key
client = OpenAI(api_key='YOUR_API_KEY')
GPT_MODEL = "gpt-4o-mini"

# Funzione per leggere i file di testo dalla cartella "txt"
def leggi_file_da_cartella(cartella):
    file_testo = {}
    for nome_file in os.listdir(cartella):
        if nome_file.endswith('.txt'):
            percorso_file = os.path.join(cartella, nome_file)
            with open(percorso_file, 'r', encoding='utf-8') as file:
                contenuto = file.read()
                file_testo[nome_file] = contenuto
    return file_testo

# Funzione per generare il riassunto utilizzando GPT-4
def genera_riassunto(testo):
    messages = [
        {"role": "system", "content": "You are an expert at summarizing texts."},
        {"role": "user", "content": f"Summarize the following text into a concise, 2000-character abstract, ensuring that the main context and meaning are preserved. The summary should adopt a formal and academic style, remaining neutral without qualitative judgments or superlative expressions. The summary will be based solely on the provided TXT file, without inventing or utilizing other sources. Additionally, it should not search for external knowledge or use web searching capabilities. Upon receiving a TXT file, the GPT must create the abstract and extract 20 relevant keywords from the text, presenting them in a line separated by commas. It is mandatory for the GPT to rely exclusively on the content of the TXT file, without incorporating external knowledge or context:\n\n{testo}"}
    ]
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=2048  # Regola questo valore in base alle necessità
    )
    riassunto = response.choices[0].message.content
    return riassunto

# Funzione per elaborare i file e salvare i riassunti in un CSV
def salva_riassunti_in_csv(cartella, output_csv):
    file_testi = leggi_file_da_cartella(cartella)
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(['Nome File', 'Riassunto'])
        for nome_file, testo in file_testi.items():
            print(f"Generazione riassunto per {nome_file}...")
            riassunto = genera_riassunto(testo)
            writer.writerow([nome_file, riassunto])
            print(f"Riassunto di {nome_file} completato.")

# Specifica la cartella con i file di testo e il nome del file CSV di output
cartella_txt = 'txt'  # Cartella contenente i file di testo
output_csv = 'abstract.csv'  # Nome del file CSV di output

# Esecuzione dello script
salva_riassunti_in_csv(cartella_txt, output_csv)