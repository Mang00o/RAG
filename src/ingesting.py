import os
import PyPDF2

class Ingesting:
    def __init__(self, directory):
        self.directory = directory
        self.documents = []
        self.document_names = []

    # Function to get the PDF filenames
    def get_pdf_filenames(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".pdf"):
                self.document_names.append(filename)
        return self.document_names


    # Function to extract text from a single PDF
    def extract_text_from_pdf(self, filename):
        with open(os.path.join(self.directory, filename), 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
        return text

    # Main function that uses the above two functions to process all PDFs
    def extract_text_from_pdfs(self):
        pdf_filenames = self.get_pdf_filenames()
        for filename in pdf_filenames:
            text = self.extract_text_from_pdf(filename)
            self.documents.append(text)
        return self.documents, self.document_names

    # Method for printing the names of uploaded files
    def print_loaded_documents(self):
        print("\n-> Load Files:")
        for filename in self.document_names:
            print(f"\t- {filename}")