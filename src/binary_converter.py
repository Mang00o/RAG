import pickle

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