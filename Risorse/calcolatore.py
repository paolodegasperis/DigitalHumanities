import os
import csv
import glob
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)  # Leggi solo i primi 10000 byte per il rilevamento
        result = chardet.detect(raw_data)
        return result['encoding']

def count_words_and_characters(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        text = file.read()
        num_words = len(text.split())
        num_characters = len(text)
    return num_words, num_characters

def analyze_txt_files(directory):
    results = []
    for file_path in glob.glob(os.path.join(directory, '**/*.txt'), recursive=True):
        num_words, num_characters = count_words_and_characters(file_path)
        results.append([os.path.basename(file_path), num_words, num_characters])
    
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['file_name', 'num_words', 'num_characters'])
        csvwriter.writerows(results)

if __name__ == "__main__":
    directory = 'txt'  # Cambia questo percorso con quello della tua cartella
    analyze_txt_files(directory)
