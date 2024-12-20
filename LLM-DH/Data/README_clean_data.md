
# README per lo script di pulizia dei dati

## Descrizione

Questo script è progettato per pulire e standardizzare un dataset contenente informazioni su persone. Le principali operazioni di pulizia includono:
- Correzione del formato dei nomi (capitalizzazione corretta).
- Standardizzazione delle date di nascita in formato `YYYY-MM-DD`.
- Pulizia dei numeri di telefono, rimuovendo caratteri non numerici e verificando che abbiano un formato valido.

Dopo aver applicato queste operazioni di pulizia, lo script salva un nuovo file CSV contenente i dati puliti.

## Requisiti

- Python 3.6 o superiore
- Librerie Python:
  - `pandas`: per la gestione dei dati tabulari.
  - `re`: per le espressioni regolari.
  - `datetime`: per la gestione delle date.

### Installazione delle dipendenze

Puoi installare la libreria `pandas` utilizzando il seguente comando:

```bash
pip install pandas
```

## Funzionamento

Lo script esegue le seguenti operazioni:

1. **Caricamento del dataset**: Il file CSV `dataset.csv` viene caricato in un DataFrame di `pandas`.
2. **Pulizia dei nomi**: La colonna `Nome` viene processata per correggere il formato dei nomi, capitalizzando correttamente ogni parola.
3. **Standardizzazione delle date**: Le date di nascita nella colonna `Data di Nascita` vengono convertite nel formato `YYYY-MM-DD`, supportando due formati di input (`DD/MM/YYYY` e `YYYY-MM-DD`).
4. **Pulizia dei numeri di telefono**: I numeri di telefono nella colonna `Numero di Telefono` vengono puliti, rimuovendo i caratteri non numerici e validando che abbiano 10 cifre.
5. **Rimozione di righe incomplete**: Se una riga contiene valori mancanti in una delle colonne chiave (Nome, Data di Nascita, Numero di Telefono), questa riga viene eliminata.
6. **Esportazione del dataset pulito**: Il dataset pulito viene salvato in un nuovo file CSV chiamato `dataset_pulito.csv`.

### Esecuzione dello script

Puoi eseguire lo script con il seguente comando:

```bash
python clean_data.py
```

Lo script salverà il risultato nel file `dataset_pulito.csv`.

## Modifiche

1. **Personalizzazione del formato delle date**: Puoi modificare il formato delle date nella funzione `standardize_date` per adattarlo alle tue esigenze.
2. **Validazione dei numeri di telefono**: La funzione `clean_phone_number` può essere modificata per accettare numeri di telefono con un formato diverso (ad esempio, con prefisso internazionale).
3. **Rimozione di righe**: Se vuoi rimuovere righe in base a altre colonne, puoi modificare la parte dello script che utilizza il metodo `dropna()`.

## Supporto

Se hai domande o riscontri problemi, puoi fare riferimento al file `dataset_pulito.csv` per i risultati puliti, o esaminare eventuali errori nel terminale.
