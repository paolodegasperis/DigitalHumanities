import os
from mistralai import Mistral

# Imposta la chiave API
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

# Cartelle di input e output
input_folder = "pdf"
output_folder = "output"

# Crea la cartella di output se non esiste
os.makedirs(output_folder, exist_ok=True)

# Elabora ogni file PDF nella cartella di input
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        document_path = os.path.join(input_folder, filename)

        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_path",
                "document_path": document_path
            },
            include_image_base64=True
        )

        # Salva il risultato in un file di testo nella cartella di output
        output_filename = os.path.splitext(filename)[0] + "_output.txt"
        output_path = os.path.join(output_folder, output_filename)

        with open(output_path, "w") as output_file:
            output_file.write(str(ocr_response))

print("Elaborazione completata. I risultati sono stati salvati nella cartella 'output'.")
