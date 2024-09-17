
# README

## Descrizione
Questa raccolta di script Python è progettata per svolgere diverse operazioni su file di testo, come la rimozione di ritorni a capo, il conteggio delle parole e dei caratteri, e la generazione di strutture di cartelle in file CSV. Ogni script ha uno scopo specifico, come descritto di seguito.

---

## Script: `rem_accapo.py`

### Scopo:
Rimuove tutti i ritorni a capo (`\n`) dai file `.txt` all'interno di una directory specifica, riscrivendo il contenuto su una sola riga.

### Istruzioni per l'uso:
1. Posiziona tutti i file di testo che desideri elaborare all'interno della cartella `txt_job`.
2. Esegui lo script:
   ```bash
   python rem_accapo.py
   ```
3. Lo script modificherà i file eliminando i ritorni a capo.

### Note:
- Assicurati che la directory `txt_job` esista e contenga i file `.txt` che desideri elaborare.

---

## Script: `calcolatore.py`

### Scopo:
Conta il numero di parole e caratteri nei file di testo (.txt) presenti in una directory, e salva i risultati in un file CSV.

### Istruzioni per l'uso:
1. Posiziona tutti i file di testo all'interno di una directory (modifica il percorso se necessario).
2. Modifica la variabile `directory` all'interno del file, se richiesto (es. `'txt'`).
3. Esegui lo script:
   ```bash
   python calcolatore.py
   ```
4. Lo script genererà un file chiamato `results.csv` contenente il nome del file, il numero di parole e il numero di caratteri per ogni file.

### Note:
- Lo script rileva automaticamente la codifica del file prima di elaborarlo, per evitare problemi di lettura con diversi set di caratteri.

---

## Script: `struttura.py`

### Scopo:
Legge la struttura di una cartella e delle sue sottocartelle, elencando tutti i file in un file CSV, includendo i percorsi relativi.

### Istruzioni per l'uso:
1. Imposta la variabile `folder_name` con il nome della directory di cui desideri salvare la struttura (es. `'txt'`).
2. Esegui lo script:
   ```bash
   python struttura.py
   ```
3. Verrà generato un file `struttura.csv` che contiene la struttura della cartella con i percorsi relativi di tutti i file.

### Note:
- Può essere utile per mappare il contenuto di una cartella e le sue sottocartelle.

---

## Script: `contare.py`

### Scopo:
Questo script legge un file CSV di input che contiene i nomi di file di testo, conta il numero di parole e caratteri in ciascun file, e aggiorna il CSV con queste informazioni.

### Istruzioni per l'uso:
1. Prepara un file CSV (`data_sa01.csv`) con una colonna chiamata `testo_txt` contenente i nomi dei file di testo (senza percorsi completi).
2. Assicurati che i file di testo siano presenti nella cartella `txt`.
3. Esegui lo script:
   ```bash
   python contare.py
   ```
4. Lo script creerà un file `updated_data_sa01.csv` che contiene il conteggio delle parole e dei caratteri per ogni file.

### Note:
- Se un file non viene trovato o non può essere letto, i valori del conteggio saranno segnati come "N/A".

---

## Requisiti

- Python 3.x
- Moduli Python aggiuntivi:
  - `os`
  - `csv`
  - `glob` (per `calcolatore.py`)
  - `chardet` (per `calcolatore.py`)
