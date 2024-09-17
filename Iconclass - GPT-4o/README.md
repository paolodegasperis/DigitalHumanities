
# Image Analysis System

## Descrizione
Questo sistema analizza le immagini fornendo una descrizione, una interpretazione e identificando i codici Iconclass associati. Utilizza l'API di OpenAI per elaborare le immagini e restituire i risultati.

## Funzionalità
- **Codifica delle immagini in Base64**: Converte le immagini in formato base64 per l'invio all'API.
- **Validazione delle immagini**: Verifica che i file siano immagini valide prima di processarle.
- **Analisi delle immagini**: Interroga l'API di OpenAI e ritorna una descrizione e i codici Iconclass delle immagini.
- **Registrazione degli errori**: Utilizza il logging per registrare errori e altre informazioni rilevanti.
- **Esportazione dei risultati**: Salva i risultati dell'analisi in un file CSV.

## Installazione
Per eseguire questo script, è necessario installare le seguenti dipendenze:
```bash
pip install requests asyncio csv logging tqdm
```

## Configurazione
Sostituire `YOUR_API_KEY` con la chiave API valida per OpenAI nel file di script.

## Utilizzo
Eseguire lo script dal terminale:
```bash
python nome_del_script.py
```

## Avviso di precisione
Il sistema non garantisce la precisione completa nei risultati. È fondamentale verificare manualmente i risultati per assicurarsi della loro accuratezza, specialmente in applicazioni critiche. Le risposte dell'API possono variare e dovrebbero essere utilizzate come una guida iniziale piuttosto che come una soluzione definitiva.

## Log
Tutti gli errori e le informazioni pertinenti vengono registrati nel file `image_analysis.log`.

## Contribuire
Le pull requests sono benvenute. Per modifiche maggiori, aprire prima un issue per discutere cosa vorreste cambiare.

## Licenza
Inserire qui il tipo di licenza.
