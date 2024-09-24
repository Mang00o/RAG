import faiss

class Indexing:
    def __init__(self, embedding_dimension):
        # Initialize a FAISS index using L2 (Euclidean) distance
        self.indexes = faiss.IndexFlatL2(embedding_dimension)

    def add(self, embed_documents):
        # Add the document embeddings to the FAISS index
        self.indexes.add(embed_documents)
        return self.indexes
    