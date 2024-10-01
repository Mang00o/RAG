import os
import re
import unicodedata

#############################################################################
#   This class finds the relevant documents given a query.                  #
#   It works with the cleared and normalized documentes' names and query.   #
#   Return the relevant documents name after finding them                   #
#############################################################################
class Relevanting:
    def __init__(self, query, pdfs_names):
        self.cleaned_query = self.__clean_string(query)
        self.cleaned_pdfs_names = self.__clear_list(pdfs_names)
    
    def __get_relevant_cleared_pdfs_names(self):
        relevant_cleared_pdfs_names = []
        query_words = self.cleaned_query.split()

        for pdf_name in self.cleaned_pdfs_names:
            doc_words = pdf_name.split()

            if any(word in doc_words for word in query_words):
                relevant_cleared_pdfs_names.append(pdf_name)

        return relevant_cleared_pdfs_names
    
    # This method clear the string from unnecessary text
    def __clean_string(self, text):
        text = text.lower()
        text = os.path.splitext(text)[0]
        text = text.replace("_", " ")
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        text = re.sub(r"[^\w\s]", '', text)
        text = self.__remove_single_letters(text)
        text = text.replace("  ", " ").strip()

        return text
    
    # This method remove singol letter from a text
    def __remove_single_letters(self, text):
        words = text.split()
        filtered_words = [word for word in words if len(word) > 1]
        return ' '.join(filtered_words)
    
    # This method clear every string from a list of string from unnecessary text
    def __clear_list(self, list):
        cleared_list = []
        for string in list:
            cleared_string = self.__clean_string(string)
            cleared_list.append(cleared_string)
        return cleared_list

    

    