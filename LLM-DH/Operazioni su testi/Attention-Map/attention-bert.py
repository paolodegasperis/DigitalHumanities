import torch
from transformers import BertTokenizer, BertModel
import matplotlib.pyplot as plt
import numpy as np

# Frase disordinata da analizzare
sentence = "il io cinema andare domani voglio wars replica star lucas regia film george di fanno al dove una un"

# Carica tokenizer e modello BERT
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
model = BertModel.from_pretrained("bert-base-multilingual-cased", output_attentions=True)
model.eval()

# Tokenizza e prepara l'input
inputs = tokenizer(sentence, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# Estrai matrici di attenzione (12 layer, 12 teste per layer)
attentions = outputs.attentions  # Tuple di dimensione [num_layers x (batch_size, num_heads, seq_len, seq_len)]

# Seleziona layer e testa da visualizzare
layer_idx = 7  # Primo layer
head_idx = 7   # Prima testa

# Estrai le matrici di attenzione dal layer e testa selezionati
attn_matrix = attentions[layer_idx][0, head_idx].numpy()

# Ottieni i token
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

# Visualizza la matrice
plt.figure(figsize=(10, 10))
plt.imshow(attn_matrix, cmap="viridis")
plt.xticks(range(len(tokens)), tokens, rotation=90)
plt.yticks(range(len(tokens)), tokens)
plt.title(f'BERT Attention - Layer {layer_idx + 1}, Head {head_idx + 1}')
plt.colorbar(label="Attention weight")
plt.tight_layout()
plt.show()
