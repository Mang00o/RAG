import os
import PyPDF2

class Ingesting:
    def __init__(self, document_directory, db_documents_names):
        self.document_directory = document_directory
        self.documents_names = []
        self.documents_contents = []
        self.db_documents_names = db_documents_names

    # Main function of the class - Ingest documents
    def ingesting(self):
        self.__ingesting_pdf_filenames()
        self.__ingesting_pdfs_contents()
        return self.documents_names, self.documents_contents

    # Function to get the PDF filenames
    def __ingesting_pdf_filenames(self):    
        for document_name in os.listdir(self.document_directory):
            if document_name.endswith(".pdf") and document_name not in self.db_documents_names:
                self.documents_names.append(document_name)
        
    def __ingesting_pdfs_contents(self):
        for document_name in self.documents_names:
            content = self.__extract_content_from_pdf(document_name)
            self.documents_contents.append(content)

    # Function to extract text from a single PDF with improvements
    def __extract_content_from_pdf(self, document_name):
        content = []  # Use a list to accumulate the content for better performance
        try:
            with open(os.path.join(self.document_directory, document_name), 'rb') as document:
                pdf_reader = PyPDF2.PdfReader(document)
                
                for page in range(len(pdf_reader.pages)):
                    page_text = pdf_reader.pages[page].extract_text()
                    
                    # Check if text was extracted from the page
                    if page_text:
                        content.append(page_text)
            
            # Join the list of text into a single string
            return "".join(content)

        except Exception as e:
            print(f"\n-> Error reading {document_name}: {e}")
            return ""

    # Prints the names of the PDF documents from which it extracted the text    
    def print_ingested_documents(self):
        if not self.documents_names:
            print("\n-> Documents already saved")
        else:
            print("\n-> Ingested Documents:")
            for document_name in self.documents_names:
                print(f"\t- {document_name}")