import os
import csv
import glob
import openai
import time

# Configura la tua chiave API di OpenAI
openai.api_key = 'YOUR_API_KEY'

def summarize_and_extract_keywords(text):
    try:
        # Richiesta per ottenere il riassunto e le parole chiave
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize a given text into a concise, 2000-character abstract, ensuring that the main context and meaning are preserved. The summary should adopt a formal and academic style, remaining neutral without qualitative judgments or superlative expressions. The summary will be based solely on the provided TXT file, without inventing or utilizing other sources. Additionally, it should not search for external knowledge or use web searching capabilities. Upon receiving a TXT file, the GPT must create the abstract and extract 20 relevant keywords from the text, presenting them in a line separated by commas. It is mandatory for the GPT to rely exclusively on the content of the TXT file, without incorporating external knowledge or context."},
                {"role": "user", "content": text}
            ],
            max_tokens=2500  # Adeguato per il riassunto e le parole chiave
        )
        
        # Analisi della risposta
        content = response['choices'][0]['message']['content'].strip()
        parts = content.split('\n')

        # Separiamo il riassunto e le parole chiave
        summary = parts[0].strip()
        keywords = parts[1].strip() if len(parts) > 1 else ''

        # Ridurre la lunghezza del riassunto a 2000 caratteri
        if len(summary) > 2000:
            summary = summary[:2000] + '...'
        
        return summary, keywords
    except Exception as e:
        return f"Error processing text: {e}", ""

def read_file_with_fallback(file_path):
    encodings = ['utf-8', 'latin-1', 'ISO-8859-1']  # Lista di codifiche da provare
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Cannot decode file {file_path} with any of the tried encodings.")

def analyze_txt_files(directory):
    results = []
    full_path = os.path.join(os.getcwd(), directory)
    
    for file_path in glob.glob(os.path.join(full_path, '**/*.txt'), recursive=True):
        try:
            text = read_file_with_fallback(file_path)
            summary, keywords = summarize_and_extract_keywords(text)
            results.append([os.path.basename(file_path), summary, keywords])
            time.sleep(10)  # Aggiunge un delay di 10 secondi tra ogni richiesta
        except Exception as e:
            results.append([os.path.basename(file_path), f"Error: {e}", ""])

    # Scrivere i risultati nel file CSV
    with open(os.path.join(os.getcwd(), 'summary_results.csv'), 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Nome_File', 'Summarization', 'Keywords'])
        csvwriter.writerows(results)

if __name__ == "__main__":
    directory = 'txt'  # Puoi modificare questo percorso se necessario
    analyze_txt_files(directory)
