import os
import csv
import logging
from openai import OpenAI

# Configurazione del logging per loggare solo gli errori
logging.basicConfig(filename='entita_log.log', 
                    level=logging.ERROR,  # Solo gli errori saranno registrati
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Inizializza il client OpenAI con la tua API Key
client = OpenAI(api_key='TUA CHIAVE API')
GPT_MODEL = "gpt-4o-mini"

# Funzione per leggere i file di testo dalla cartella "TXT" e relative sottocartelle
def leggi_file_da_cartella(cartella):
    file_testo = {}
    for root, dirs, files in os.walk(cartella):  # os.walk per navigare anche nelle sottocartelle
        for nome_file in files:
            if nome_file.endswith('.txt'):
                percorso_file = os.path.join(root, nome_file)  # Percorso completo del file
                try:
                    with open(percorso_file, 'r', encoding='ISO-8859-1') as file:
                        contenuto = file.read()
                        file_testo[percorso_file] = contenuto  # Usa il percorso completo come chiave
                except Exception as e:
                    logging.error(f"Errore nella lettura del file {percorso_file}: {e}")
    return file_testo

# Funzione per estrarre entità utilizzando GPT-4o-mini
def estrai_entita(testo):
    messages = [
        {"role": "system", "content": "You are an art historian expert in recognizing artists such as painters, architects and sculptors present in texts."},
        {"role": "user", "content": f"""Extract all the important people like artists, sculptors, architects, painters, popes, cardinals, kings, queens, dukes, counts present in the following text. DO NOT invent or create information.
                                        List them, separated by commas:\n\n{testo}"""}
    ]
    try:
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
            temperature=0.0,  # Meno variabilità possibile per mantenere i risultati consistenti
            max_tokens=600  # Regola questo valore in base alle necessità
        )
        entita = response.choices[0].message.content
        return entita
    except Exception as e:
        logging.error(f"Errore durante l'estrazione delle entità dal testo: {e}")
        return "Errore nell'estrazione"

# Funzione per elaborare i file e salvare le entità in un CSV
def salva_entita_in_csv(cartella, output_csv):
    file_testi = leggi_file_da_cartella(cartella)
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(['Nome File', 'Percorso File', 'Entità Estratte'])  # Aggiunta della colonna Percorso File
        for percorso_file, testo in file_testi.items():
            nome_file = os.path.basename(percorso_file)  # Estrai solo il nome del file
            entita = estrai_entita(testo)
            writer.writerow([nome_file, percorso_file, entita])  # Scrivi anche il percorso completo

# Specifica la cartella con i file di testo e il nome del file CSV di output
cartella_txt = 'TXT'  # Cartella contenente i file di testo
output_csv = 'entita_estratte.csv'  # Nome del file CSV di output

# Esecuzione dello script
try:
    salva_entita_in_csv(cartella_txt, output_csv)
except Exception as e:
    logging.error(f"Errore nell'esecuzione dello script: {e}")
