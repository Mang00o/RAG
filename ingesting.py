import os
import PyPDF2

class Ingesting:
    def __init__(self, directory):
        self.directory = directory
        self.documents = []
        self.document_names = []

    # Method for extracting text from PDFs
    def extract_text_from_pdfs(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".pdf"):
                self.document_names.append(filename)  # Aggiungi il nome del file alla lista
                with open(os.path.join(self.directory, filename), 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in range(len(reader.pages)):
                        text += reader.pages[page].extract_text()
                    self.documents.append(text)
        return self.documents, self.document_names

    # Method for printing the names of uploaded files
    def print_loaded_documents(self):
        print("\n-> Documenti caricati:")
        for filename in self.document_names:
            print(f"\t- {filename}")