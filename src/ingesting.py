from database_manager import DatabaseManager
import os
import PyPDF2

class Ingesting:
    def __init__(self, document_directory):
        self.document_directory = document_directory
        self.documents_names = []
        self.documents_contents = []
        self.db_manager = DatabaseManager(host="localhost", user="root", password="1234Ale!", database="My_Rag")

    def ingesting(self):
        self.__ingesting_pdf_filenames()
        self.__ingesting_pdfs_contents()
        return self.documents_names, self.documents_contents

    # Function to get the PDF filenames
    def __ingesting_pdf_filenames(self):
        self.db_manager.connect()
        db_documents_names = self.db_manager.load_documents()
        self.db_manager.close()
        for document_name in os.listdir(self.document_directory):
            if document_name.endswith(".pdf") and document_name not in db_documents_names:
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
                pdf_reader = PyPDF2.PdfReader(document_name)
                
                for page in range(len(pdf_reader.pages)):
                    page_text = pdf_reader.pages[page].extract_text()
                    
                    # Check if text was extracted from the page
                    if page_text:
                        content.append(page_text)
            
            # Join the list of text into a single string
            return "".join(content)

        except Exception as e:
            print(f"Error reading {document_name}: {e}")
            return ""