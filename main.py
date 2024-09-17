import os

# Funzione per caricare i nomi dei documenti da una cartella
def list_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):  # Cerca solo file PDF
            documents.append(filename)
    return documents

# Lista dei documenti dalla cartella "documents"
document_names = list_documents("documents")

# Stampa i nomi dei documenti uno per riga
print("Documenti caricati:")
for document in document_names:
    print(document)