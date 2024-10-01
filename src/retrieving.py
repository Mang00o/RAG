#
#   This class retrieve the
#
class Retrieving:
    def __init__(self, documents_names, indexes, embedded_query):
        # Save document embeddings, file names, document texts, and FAISS indexes
        self.documents_names = documents_names
        self.indexes = indexes
        self.embedded_query = embedded_query

    # Function to search for relevant documents based on a query
    def search_documents(self):       
        # Search the FAISS indexes for the documents closest to the query embedding
        distances, indices = self.indexes.search(self.embedded_query, self.__define_k())

        # Retrieve the most relevant documents and their distances
        results = [(self.documents_names[i], distances[0][idx]) for idx, i in enumerate(indices[0])]

        return results
    
    def __define_k(self):
        # Define const numner of documents to retrieve
        DOCUMENTS_TO_RETRIEVE = 5

        # Define value of variable k
        k = min(DOCUMENTS_TO_RETRIEVE, len(self.documents_names)) # 'k' indicates the number of documents to retrieve

        return k