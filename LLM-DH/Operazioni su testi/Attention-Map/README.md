# 📊 Visualizzazione della Mappa di Attenzione di BERT

Questo script Python consente di analizzare e visualizzare le **mappe di attenzione** generate dal modello `bert-base-multilingual-cased` di Hugging Face, applicate a una frase disordinata. È uno strumento utile per esplorare il funzionamento interno dei modelli basati su architettura Transformer, in particolare per osservare come l'attenzione tra parole si distribuisce nei vari strati (*layers*) e teste (*heads*).

---

## ⚙️ Requisiti

Assicurarsi di avere installato le seguenti librerie:

```bash
pip install torch transformers matplotlib
```

---

## 📥 Script incluso

Il file Python esegue i seguenti passaggi:

1. **Tokenizza** una frase disordinata.
2. Passa i token al modello `bert-base-multilingual-cased`.
3. Estrae le **matrici di attenzione** (layer × head).
4. Visualizza graficamente la matrice relativa al layer e alla testa specificati.

---

## 🧾 Modifica della frase da analizzare

Nel file `.py`, è possibile modificare la frase da analizzare cambiando il contenuto della variabile `sentence`:

```python
sentence = "il io cinema andare domani voglio wars replica star lucas regia film george di fanno al dove una un"
```

Sostituisci questa stringa con qualunque frase in italiano o altra lingua supportata dal modello multilingue, mantenendo la sintassi tra virgolette.

---

## 🔄 Navigazione tra i layer e le teste di attenzione

La rete BERT base multilingue è composta da:

- **12 layer (strati)** numerati da `0` a `11`.
- **12 head (teste di attenzione)** per ciascun layer, anch'esse numerate da `0` a `11`.

Per visualizzare una diversa mappa di attenzione, modifica i seguenti parametri nel codice:

```python
layer_idx = 7  # Seleziona lo strato desiderato (da 0 a 11)
head_idx = 7   # Seleziona la testa desiderata (da 0 a 11)
```

---

## 📈 Interpretazione del grafico

Il grafico generato mostra una **matrice quadrata** in cui:

- Le **etichette** sugli assi rappresentano i token (parole o frammenti).
- Ogni cella indica **quanto un token presta attenzione a un altro**.
- Il colore (scala *viridis*) indica il peso dell’attenzione: più è intenso, maggiore è l'influenza.

---

## 📌 Suggerimenti

- Gli **strati inferiori** (es. `layer_idx = 0`) tendono a catturare relazioni sintattiche locali.
- Gli **strati superiori** (es. `layer_idx = 11`) evidenziano strutture semantiche più astratte e relazioni più ampie.

---

## 📚 Riferimenti

- Modello: [`bert-base-multilingual-cased`](https://huggingface.co/bert-base-multilingual-cased)
- Architettura Transformer: Vaswani et al., *"Attention is All You Need"*, 2017.
- Libreria `transformers`: [https://huggingface.co/transformers](https://huggingface.co/transformers)

---
