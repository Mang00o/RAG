class Retrieving:
    def __init__(self, document_embeddings, pdf_filenames, index):
       # Save document embeddings, file names, FAISS index and query embedding
        self.document_embeddings = document_embeddings
        self.pdf_filenames = pdf_filenames
        self.index = index

    # Function to search for relevant documents based on a query
    def search_documents(self, query, k=1):
        # Search the FAISS index for the documents closest to the query embedding
        distances, indices = self.index.search(query, k)

        # Retrieve the most relevant documents and their distances
        results = [(self.pdf_filenames[i], distances[0][idx]) for idx, i in enumerate(indices[0])]
        return results