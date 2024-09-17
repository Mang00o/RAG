import os
import PyPDF2
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import warnings

# Suppress only the specific FutureWarning related to clean_up_tokenization_spaces
warnings.filterwarnings(
    "ignore", 
    category=FutureWarning, 
    message=r"`clean_up_tokenization_spaces` was not set"
)

# Passo 1: Estrai il testo dai PDF
def extract_text_from_pdfs(directory):
    documents = []
    document_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            document_names.append(filename)  # Aggiungi il nome del file alla lista
            with open(os.path.join(directory, filename), 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in range(len(reader.pages)):
                    text += reader.pages[page].extract_text()
                documents.append(text)
    return documents, document_names

# Carica i documenti PDF e salva i nomi
pdf_texts, pdf_filenames = extract_text_from_pdfs("documents")

# Stampa i nomi dei file caricati
print("Documenti caricati:")
for filename in pdf_filenames:
    print(filename)

# Passo 2: Indicare i documenti con FAISS
# Carica il modello di embedding
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Funzione per trasformare il testo dei documenti in vettori
def embed_documents(documents):
    inputs = tokenizer(documents, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).numpy()
    return embeddings

# Indica i documenti PDF
document_embeddings = embed_documents(pdf_texts)

# Crea un indice FAISS
index = faiss.IndexFlatL2(document_embeddings.shape[1])
index.add(document_embeddings)

print("Documenti indicizzati con successo!")
