import pandas as pd
import re
from datetime import datetime

# Carica il dataset
df = pd.read_csv('dataset.csv')

# Funzione per correggere il formato dei nomi (capitalize)
def clean_name(name):
    if isinstance(name, str):
        return ' '.join([word.capitalize() for word in name.split()])
    return name

# Funzione per standardizzare la data in formato 'YYYY-MM-DD'
def standardize_date(date):
    try:
        return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return None  # Imposta a None se la data è invalida

# Funzione per validare e pulire i numeri di telefono
def clean_phone_number(phone):
    if isinstance(phone, str):
        # Rimuove tutti i caratteri non numerici
        phone = re.sub(r'\D', '', phone)
        # Verifica che il numero sia valido (10 cifre per esempio, puoi adattare alle tue specifiche)
        if len(phone) == 10:
            return phone
    return None  # Imposta a None se il numero è invalido

# Applica le funzioni di pulizia
df['Nome'] = df['Nome'].apply(clean_name)
df['Data di Nascita'] = df['Data di Nascita'].apply(standardize_date)
df['Numero di Telefono'] = df['Numero di Telefono'].apply(clean_phone_number)

# Rimuove righe con valori mancanti in 'Nome', 'Data di Nascita' o 'Numero di Telefono' se necessario
df.dropna(subset=['Nome', 'Data di Nascita', 'Numero di Telefono'], inplace=True)

# Esporta il dataset pulito
df.to_csv('dataset_pulito.csv', index=False