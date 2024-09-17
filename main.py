import os
import PyPDF2
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import warnings
import subprocess

def main():
    print("\n***************************")
    print("*   Inizio dello Script   *")
    print("***************************")

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
    print("\n-> Documenti caricati:")
    for filename in pdf_filenames:
        print("\t- " + filename)

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

    print("\n-> Documenti indicizzati con successo!")

    # Funzione per cercare documenti rilevanti in base a una query
    def search_documents(query, k=1):
        # Genera l'embedding della query
        query_embedding = embed_documents([query])
        
        # Cerca nell'indice FAISS i documenti più vicini
        distances, indices = index.search(query_embedding, k)
        
        # Recupera i documenti più rilevanti e le loro distanze
        results = [(pdf_filenames[i], distances[0][idx]) for idx, i in enumerate(indices[0])]
        return results

    # Esegui una query per cercare documenti rilevanti
    query = input("\n-> Inserisci la query per cercare documenti rilevanti: ")
    result = search_documents(query, k=5)  # 'k' indica il numero di documenti da recuperare

    # Stampa i documenti trovati con le loro distanze
    print("\n-> Documenti più rilevanti trovati:")
    print("\tDocumento                                | Distanza")
    print("\t-----------------------------------------|-----------")
    for doc, distance in result:
        print(f"\t{doc:<40} | {distance:.4f}")

    # Funzione per inviare la query e i documenti a Ollama dentro WSL
    def generate_response_with_ollama(query, documents):
        # Costruisci il prompt da inviare a Ollama
        docs_text = " ".join([pdf_texts[pdf_filenames.index(doc)] for doc, _ in documents])[:1000]  # Prendi solo i primi 1000 caratteri
        
        # Costruisci il prompt per Ollama
        prompt = f"Domanda: {query}\n\nDocumenti:\n{docs_text}"
        
        # Esegui il comando `ollama run codellama` dentro WSL con encoding UTF-8
        process = subprocess.Popen(['wsl', 'ollama', 'run', 'codellama'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        
        # Invia il prompt e ottieni la risposta
        stdout, stderr = process.communicate(input=prompt)
        
        if stderr:
            print(f"Errore: {stderr}")
        
        return stdout.strip()  # Restituisce la risposta di Ollama

    # Genera la risposta con Ollama basata sui documenti trovati
    response = generate_response_with_ollama(query, result)
    print("\n-> Risposta generata da Ollama:\n", response)

    # Stampa fine script
    print("\n***************************")
    print("*     Fine dello Script    *")
    print("***************************\n")

if __name__ == "__main__":
    main()