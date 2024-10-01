import os
import PyPDF2

#################################################################################
#   This class deals with ingesting the PDFs contained in a specific folder.    #
#   The class checks that the PDFs have not already been saved.                 #
#   Finally it returns the name and content of each unsaved PDF                 #
#################################################################################
class Ingesting:
    def __init__(self, document_directory, db_pdfs_names):
        self.document_directory = document_directory
        self.pdfs_names = []
        self.pdfs_contents = []
        self.db_pdfs_names = db_pdfs_names

    # Main function of the class - Ingest documents
    def ingesting(self):
        self.__ingesting_pdfs_names()
        self.__ingesting_pdfs_contents()
        return self.pdfs_names, self.pdfs_contents

    # Function to get the PDF filenames
    def __ingesting_pdfs_names(self):    
        for pdf_name in os.listdir(self.document_directory):
            if pdf_name.endswith(".pdf") and pdf_name not in self.db_pdfs_names:
                self.pdfs_names.append(pdf_name)
        
    def __ingesting_pdfs_contents(self):
        for pdf_name in self.pdfs_names:
            content = self.__extract_content_from_pdf(pdf_name)
            self.pdfs_contents.append(content)

    # Function to extract text from a single PDF with improvements
    def __extract_content_from_pdf(self, pdf_name):
        content = []  # Use a list to accumulate the content for better performance
        try:
            with open(os.path.join(self.document_directory, pdf_name), 'rb') as pdf:
                pdf_reader = PyPDF2.PdfReader(pdf)
                
                for page in range(len(pdf_reader.pages)):
                    page_text = pdf_reader.pages[page].extract_text()
                    
                    # Check if text was extracted from the page
                    if page_text:
                        content.append(page_text)
            
            # Join the list of text into a single string
            return "".join(content)

        except Exception as e:
            print(f"\n-> Error reading {pdf_name}: {e}")
            return ""