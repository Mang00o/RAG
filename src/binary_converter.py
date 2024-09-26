import pickle
import faiss
import numpy as np

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
    
    def binary_indexes_bytes(self, contents_indexes):
        # Serializza l'indice FAISS in un formato binario
        binary_indexes = faiss.serialize_index(contents_indexes)
        binary_indexes_bytes = bytes(binary_indexes)
        return binary_indexes_bytes
    
    def normal_indexes(self, binary_indexes_bytes):
        normal_indexes = faiss.deserialize_index(np.frombuffer(binary_indexes_bytes, dtype=np.uint8))
        return normal_indexes