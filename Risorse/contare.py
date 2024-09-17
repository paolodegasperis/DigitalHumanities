import os
import csv

def count_words_and_characters(file_path):
    encodings = ['utf-8', 'ISO-8859-1', 'latin1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                text = file.read()
                num_words = len(text.split())
                num_characters = len(text)
            return num_words, num_characters
        except UnicodeDecodeError:
            continue
    # Se nessuna delle codifiche ha funzionato, restituisce 0 parole e 0 caratteri
    return 0, 0

def process_csv(input_csv, folder_name, output_csv):
    with open(input_csv, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
    
    for row in rows:
        file_path = os.path.join(folder_name, row['testo_txt'])
        if os.path.isfile(file_path):
            num_words, num_characters = count_words_and_characters(file_path)
            row['num_parole'] = num_words
            row['num_caratteri'] = num_characters
        else:
            row['num_parole'] = 'N/A'
            row['num_caratteri'] = 'N/A'
    
    fieldnames = reader.fieldnames + ['num_parole', 'num_caratteri']
    
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    input_csv = 'data_sa01.csv'  # Percorso del file CSV di input
    folder_name = 'txt'  # Nome della cartella principale
    output_csv = 'updated_data_sa01.csv'  # Nome del file CSV di output

    # Processa il file CSV e aggiorna i record con il conteggio delle parole e dei caratteri
    process_csv(input_csv, folder_name, output_csv)
    print(f"CSV aggiornato salvato in {output_csv}")

if __name__ == "__main__":
    main()
