import pickle

class BinaryConverter:
    # Method for returning the binary text of a text
    def binary_text(self, text):
        # Convert text to binary 
        binary_text = pickle.dumps(text)
        return binary_text
    
    def normal_list(self, binary_list):
        normal_list = []
        for binary in binary_list:
            normal_text = self.__normal_text(binary)
            normal_list.append(normal_text)
        return normal_list

    # Method for converting binary text back to normal text
    def __normal_text(self, binary_text):
        # Convert binary text back to normal text
        text = pickle.loads(binary_text)
        return text