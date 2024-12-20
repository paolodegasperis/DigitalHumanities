
# README per gli script di descrizione e clustering delle immagini

## Descrizione Generale

Questo repository contiene due script principali che consentono di lavorare con immagini in modo avanzato:

1. **Descrizione e estrazione di parole chiave dalle immagini** (`describe_img.py`):
   - Utilizza l'API di OpenAI per generare una descrizione breve e parole chiave per ogni immagine, restituendo un file CSV con i risultati.
   - L'analisi è realizzata inviando le immagini all'API OpenAI, che fornisce una descrizione e 20 parole chiave relative all'immagine.

2. **Clustering delle immagini basato sulla similarità concettuale** (`clip.py`):
   - Utilizza il modello CLIP (Contrastive Language-Image Pre-training) per generare embeddings delle immagini, calcolare la similarità coseno tra di esse e successivamente eseguire un clustering per raggruppare immagini simili.
   - Le immagini vengono organizzate in cartelle separate per ogni cluster e gli embeddings vengono esportati in un file CSV.

Entrambi gli script richiedono una configurazione iniziale, come la chiave API per l'API OpenAI nel caso di `describe_img.py`, e l'installazione delle dipendenze necessarie.

## Script 1: `clip.py` - Clustering delle Immagini

### Descrizione

Lo script `clip.py` utilizza il modello CLIP di OpenAI per generare embeddings per le immagini. Le immagini vengono poi raggruppate in cluster sulla base della loro similarità concettuale, calcolata tramite la similarità coseno tra gli embeddings.

### Funzionamento

1. **Generazione degli embeddings**: Ogni immagine nella cartella specificata viene processata per ottenere il suo embedding, che rappresenta la sua semantica in uno spazio vettoriale.
2. **Calcolo della similarità coseno**: Gli embeddings delle immagini vengono confrontati tra loro per calcolare la similarità coseno. Le immagini che sono semanticamente simili vengono quindi raggruppate insieme.
3. **Clustering**: Viene utilizzato l'algoritmo di clustering agglomerativo per raggruppare le immagini simili in cluster. La similarità tra le immagini è controllata tramite una soglia di similarità (`similarity_threshold`), che determina il numero di cluster.
4. **Salvataggio dei risultati**: Gli embeddings vengono salvati in un file CSV (`embeddings.csv`). Le immagini vengono poi organizzate in cartelle separate, con ciascun cluster di immagini salvato in una directory dedicata.

### Esecuzione dello script

Per eseguire lo script, utilizza il comando seguente, sostituendo `<path_to_images>` con il percorso della cartella contenente le immagini da analizzare e `<path_to_output>` con il percorso di destinazione per i cluster di immagini:

```bash
python clip.py --image_directory <path_to_images> --output_directory <path_to_output> --similarity_threshold 0.8
```

### Dipendenze

- `torch`
- `transformers`
- `pandas`
- `numpy`
- `sklearn`
- `PIL` (Pillow)
- `tqdm`

### Modifiche possibili

- Puoi modificare la soglia di similarità (`similarity_threshold`) per influenzare la quantità di clustering (valori più bassi creano più cluster).
- Se desideri un clustering più fine o più grossolano, puoi cambiare il metodo di clustering o la distanza utilizzata.

## Script 2: `describe_img.py` - Descrizione e Parole Chiave dalle Immagini

### Descrizione

Lo script `describe_img.py` utilizza l'API OpenAI per ottenere una descrizione breve e 20 parole chiave rilevanti per ciascuna immagine. Le immagini vengono inviate all'API OpenAI in formato base64, e il modello restituisce la descrizione e le parole chiave che vengono poi salvate in un file CSV.

### Funzionamento

1. **Codifica delle immagini**: Ogni immagine viene letta dalla cartella di input e codificata in base64 per essere inviata tramite richiesta API.
2. **Richiesta all'API di OpenAI**: Lo script invia la richiesta all'API, chiedendo una descrizione breve dell'immagine e un elenco di parole chiave.
3. **Analisi e salvataggio dei risultati**: I risultati della richiesta vengono suddivisi in descrizione e parole chiave, quindi salvati in un file CSV. Inoltre, vengono generati dei log per monitorare l'utilizzo dei token e per registrare eventuali errori.

### Esecuzione dello script

Per eseguire lo script, usa il seguente comando:

```bash
python describe_img.py
```

Lo script salverà i risultati nel file `image_analysis.csv` e registrerà i dettagli nell'output del log.

### Dipendenze

- `requests`
- `os`
- `csv`
- `time`

### Modifiche possibili

- Puoi modificare il formato della richiesta all'API per ottenere descrizioni più dettagliate o parole chiave differenti.
- Se desideri eseguire l'analisi su immagini in un altro formato, puoi modificare il filtro sui formati immagine.

---

### Supporto

Se hai domande o riscontri problemi, puoi fare riferimento ai file di log generati da ciascun script per ulteriori dettagli sugli errori. Inoltre, assicurati di aver configurato correttamente la tua chiave API per il corretto funzionamento di `describe_img.py`.
