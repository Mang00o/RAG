import pickle
import faiss

class BinaryConverter:
    # Method for returning the binary text of a text
    def binary_text(self, text):
        # Convert text to binary 
        binary_text = pickle.dumps(text)
        return binary_text
    
    # Method for converting binary text back to normal text
    def normal_text(self, binary_text):
        # Convert binary text back to normal text
        text = pickle.loads(binary_text)
        return text
    
    def binary_indexes(self, contents_indexes):
        # Serializza l'indice FAISS in un formato binario
        binary_index = faiss.serialize_index(contents_indexes)
        return binary_index
