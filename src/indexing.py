import faiss

#####################################################################
#   This class calculate the index from given contents embeddings   #
#   And return the index                                            #
#####################################################################
class Indexing:
    def __init__(self, embedded_contents):
        self.embedded_contents = embedded_contents
        # Initialize a FAISS index using L2 (Euclidean) distance
        self.index = faiss.IndexFlatL2(self.embedded_contents.shape[1])

    # Add the document embeddings to the FAISS index
    def add(self):
        self.index.add(self.embedded_contents)
        return self.index
    