
# README per lo script di estrazione delle entità

## Descrizione

Questo script è progettato per estrarre entità nominate (come persone, luoghi, oggetti, eventi, ecc.) da file di testo utilizzando il modello GPT-4o-mini di OpenAI. Le entità estratte vengono poi salvate in un file CSV per ulteriori analisi. Lo script esplora una cartella contenente file di testo, esegue l'estrazione delle entità e salva i risultati in un file CSV.

## Requisiti

- Python 3.6 o superiore
- Librerie Python:
  - `openai`: per interagire con l'API di OpenAI.
  - `os`: per la gestione dei file e delle cartelle.
  - `csv`: per salvare i risultati in formato CSV.
  - `logging`: per registrare gli errori.

### Installazione delle dipendenze
Puoi installare le dipendenze richieste utilizzando il seguente comando:

```bash
pip install openai
```

## Configurazione

1. **API Key**: Devi configurare la tua chiave API di OpenAI nel file. Sostituisci `'TUA CHIAVE API'` con la tua chiave personale.
   ```python
   client = OpenAI(api_key='TUA CHIAVE API')
   ```

2. **Cartella di input**: Lo script esplora i file di testo nella cartella `TXT`. Assicurati che i file di testo siano contenuti in una cartella chiamata `TXT`.

3. **File di output**: I risultati verranno salvati in un file CSV denominato `entita_estratte.csv`. Ogni riga del CSV conterrà il nome del file, il percorso del file e le entità estratte.

## Funzionamento

Lo script esegue le seguenti operazioni:

1. **Lettura dei file di testo**: Lo script esplora la cartella `TXT` e legge i contenuti di tutti i file `.txt` presenti.

2. **Estrazione delle entità**: Per ogni file di testo, lo script invia il contenuto al modello GPT-4o-mini per estrarre le entità nominate (persone, luoghi, eventi, oggetti, ecc.).

3. **Salvataggio in CSV**: Le entità estratte vengono quindi salvate in un file CSV, con ogni riga che include il nome del file, il percorso del file e le entità estratte.

### Esecuzione dello script

Puoi eseguire lo script con il seguente comando:

```bash
python entita.py
```

Lo script salverà i risultati in un file CSV nella stessa directory.

## Gestione degli errori

Gli errori verranno registrati in un file di log chiamato `entita_log.log`. Se si verifica un errore durante la lettura di un file di testo o durante l'estrazione delle entità, lo script lo registrerà nel file di log.

## Modifiche

1. **Personalizzazione dell'estrazione**: Puoi modificare la descrizione nel messaggio del sistema per adattarla ad altre esigenze di estrazione di entità.
   ```python
   {"role": "system", "content": "You are an expert in extracting named entities from texts..."}
   ```

2. **Formato di output**: Puoi modificare la struttura del CSV cambiando il formato della riga `writer.writerow([nome_file, percorso_file, entita])`.

## Supporto

Se hai domande o riscontri problemi, puoi fare riferimento al file di log (`entita_log.log`) per maggiori dettagli sugli errori.
