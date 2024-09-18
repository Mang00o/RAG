import faiss

class Indexing:
    def __init__(self, embedding_dim):
        # Initialize a FAISS index using L2 (Euclidean) distance
        self.index = faiss.IndexFlatL2(embedding_dim)

    def add(self, embed_documents):
        # Add the document embeddings to the FAISS index
        self.index.add(embed_documents)
        return self.index