# README: ArXiv Paper Scraper con Interfaccia Grafica (Tkinter)

## Descrizione
Questo script Python permette di **cercare e filtrare articoli accademici su arXiv.org** attraverso un'interfaccia grafica costruita con **Tkinter**. Gli utenti possono inserire **temi di ricerca personalizzati**, avviare il processo di scraping e salvare i risultati in un database **SQLite** e in un file **CSV**.

### **Funzionalità**
- Interfaccia grafica per inserire i temi di ricerca.
- Query personalizzate su arXiv.org.
- Salvataggio dei risultati in **SQLite** e **CSV**.
- Log automatico degli errori e dei processi.

---

## **Requisiti**
Assicurati di avere installati i seguenti pacchetti Python:

```bash
pip install requests feedparser openai sqlite3 csv
```

Tkinter è incluso di default in Python, quindi non necessita di installazione aggiuntiva.

---

## **Configurazione**
### **1. Impostare la chiave API di OpenAI**
Modifica la seguente riga nel codice sorgente (`OPENAI_API_KEY`) con la tua chiave API valida di OpenAI:

```python
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
client = openai.OpenAI(api_key=OPENAI_API_KEY)
```

Se non hai una chiave API, puoi ottenerne una su [OpenAI](https://platform.openai.com/).

---

## **Utilizzo dello script**
1. **Avvia lo script** eseguendo:
   ```bash
   python arxiv_scraper_gui.py
   ```
2. **Inserisci i temi di ricerca** nell'area di testo della finestra.
3. **Clicca su "Avvia Ricerca"** per interrogare arXiv.
4. **Attendi i risultati**: lo script mostrerà un messaggio quando la ricerca sarà completata.
5. **Consulta i risultati** in:
   - **Database SQLite**: `arxiv_papers.db`
   - **File CSV**: `arxiv_papers.csv`

---

## **Miglioramenti futuri**
- Aggiunta di un'interfaccia più avanzata con **Tkinter Treeview** per mostrare i risultati in tempo reale.
- Esportazione dei risultati in **JSON** oltre che in CSV.
- Possibilità di **selezionare il numero di risultati per query** direttamente dalla GUI.

---

## **Contatti**
Per segnalare problemi o suggerire miglioramenti, puoi contattarmi direttamente o contribuire al codice sorgente!
