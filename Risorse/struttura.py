import os
import csv

def read_folder_structure(folder_name):
    # Lista per memorizzare il percorso di file e relative cartelle
    file_structure = []

    # Cammina nella directory e le sue sottodirectory
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            # Aggiunge il nome della sottocartella e il nome del file alla lista
            relative_path = os.path.relpath(root, folder_name)
            full_path = os.path.join(relative_path, file)
            file_structure.append([relative_path, full_path])

    return file_structure

def save_to_csv(file_structure, output_file):
    # Scrive la lista nel file CSV
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Scrive l'intestazione del CSV
        writer.writerow(["Subfolder", "File"])
        # Scrive i dati
        writer.writerows(file_structure)

def main():
    folder_name = 'txt'  # Nome della cartella principale
    output_file = 'struttura.csv'  # Nome del file CSV di output

    # Legge la struttura della cartella
    file_structure = read_folder_structure(folder_name)
    # Salva la struttura in un file CSV
    save_to_csv(file_structure, output_file)
    print(f"Struttura della cartella salvata in {output_file}")

if __name__ == "__main__":
    main()
