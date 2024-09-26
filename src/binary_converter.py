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
        # Serialize the FAISS index into a binary format (returns numpy array of uint8)
        binary_indexes = faiss.serialize_index(contents_indexes)
        # Convert the numpy array to bytes
        binary_indexes_bytes = binary_indexes.tobytes()
        
        # Debug: stampare i primi 100 byte per vedere se sono completi
        print(f"Serialized index length: {len(binary_indexes_bytes)}, Data: {binary_indexes_bytes[:100]}")
    
        return binary_indexes_bytes
    
    def normal_indexes(self, binary_indexes_list):
        normal_indexes = []
        
        for binary_index in binary_indexes_list:
            # Print the binary data before deserializing
            print(f"Binary index (length: {len(binary_index)}):", binary_index[:50])  # Print the first 50 bytes for debugging
            
            # Convert the bytes back to a numpy array
            binary_indexes_np = np.frombuffer(binary_index, dtype=np.uint8)
            
            # Deserialize the numpy array back into a FAISS index
            try:
                index = faiss.deserialize_index(binary_indexes_np)
                normal_indexes.append(index)
            except Exception as e:
                print(f"Failed to deserialize index: {e}")
        
        return normal_indexes