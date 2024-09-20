import os
import PyPDF2

class Ingesting:
    def __init__(self, document_directory):
        self.document_directory = document_directory
        self.documents_content = []
        self.document_names = []

    # Function to get the PDF filenames
    def get_pdf_filenames(self):
        for document_name in os.listdir(self.document_directory):
            if document_name.endswith(".pdf"):
                self.document_names.append(document_name)
        return self.document_names

    # Function to extract text from a single PDF
    def extract_content_from_pdf(self, document_name):
        with open(os.path.join(self.document_directory, document_name), 'rb') as document:
            pdf_reader = PyPDF2.PdfReader(document)
            content = ""
            for page in range(len(pdf_reader.pages)):
                content += pdf_reader.pages[page].extract_text()
        return content

    # Main function that uses the above two functions to process all PDFs
    def extract_content_from_pdfs(self):
        pdf_filenames = self.get_pdf_filenames()
        for pdf_finemane in pdf_filenames:
            content = self.extract_content_from_pdf(pdf_finemane)
            self.documents_content.append(content)
        return self.documents_content, self.document_names

    # Method for printing the names of uploaded files
    def print_loaded_document_names(self):
        print("\n-> Load Files:")
        for document_name in self.document_names:
            print(f"\t- {document_name}")