import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import requests
import feedparser
import sqlite3
import time
import openai
import csv
import logging

# Configura OpenAI API Key
OPENAI_API_KEY = "La tua API di OpenAI"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Configura logging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database setup
def setup_database():
    conn = sqlite3.connect("arxiv_papers.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            published TEXT,
            summary TEXT,
            relevance_score REAL
        )
    ''')
    conn.commit()
    conn.close()

# Funzione per interrogare arXiv
def search_arxiv(queries):
    base_url = "http://export.arxiv.org/api/query?search_query="
    results = []
    
    for query in queries:
        url = base_url + f"all:{query.replace(' ', '+')}" + "&start=0&max_results=40"
        try:
            response = requests.get(url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            
            for entry in feed.entries:
                title = entry.title
                link = entry.link
                published = entry.published
                summary = entry.summary
                results.append((title, link, published, summary))
            
            logging.info(f"Retrieved {len(feed.entries)} papers for query: {query}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from arXiv for query '{query}': {e}")
        
        time.sleep(1)  # Evita richieste troppo rapide a arXiv
    
    return results

# Funzione per salvare i paper nel database e nel file CSV
def save_to_db_and_csv(papers):
    conn = sqlite3.connect("arxiv_papers.db")
    cursor = conn.cursor()
    
    csv_filename = "arxiv_papers.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Published", "Summary"])
        
        for title, link, published, summary in papers:
            cursor.execute(
                "INSERT INTO papers (title, link, published, summary) VALUES (?, ?, ?, ?)",
                (title, link, published, summary)
            )
            writer.writerow([title, link, published, summary])
    
    conn.commit()
    conn.close()
    logging.info("Papers saved successfully in database and CSV file.")

# Funzione per avviare il processo di ricerca
def start_search():
    queries = query_text.get("1.0", tk.END).strip().split("\n")
    queries = [q.strip() for q in queries if q.strip()]
    
    if not queries:
        messagebox.showerror("Errore", "Inserisci almeno un termine di ricerca.")
        return
    
    result_label.config(text="Cercando... Attendere...")
    threading.Thread(target=run_scraper, args=(queries,), daemon=True).start()

# Funzione per eseguire lo scraping
def run_scraper(queries):
    setup_database()
    papers = search_arxiv(queries)
    if papers:
        save_to_db_and_csv(papers)
        result_label.config(text="Ricerca completata. Dati salvati in arxiv_papers.csv")
    else:
        result_label.config(text="Nessun paper trovato.")

# Creazione della GUI
root = tk.Tk()
root.title("ArXiv Paper Scraper")
root.geometry("600x400")

label = tk.Label(root, text="Inserisci i temi di ricerca (uno per riga):")
label.pack(pady=5)

query_text = scrolledtext.ScrolledText(root, width=70, height=10)
query_text.pack(pady=5)

search_button = tk.Button(root, text="Avvia Ricerca", command=start_search)
search_button.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=5)

root.mainloop()
