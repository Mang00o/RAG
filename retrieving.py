class Retrieving:
    def __init__(self, document_embeddings, pdf_filenames, index):
        # Save document embeddings, file names, FAISS index
        self.document_embeddings = document_embeddings
        self.pdf_filenames = pdf_filenames
        self.index = index

        # Prompt the user for the query during object initialization
        self.query = input("\n-> Enter the query to search for relevant documents: ")

    # Function to search for relevant documents based on a query
    def search_documents(self, k=1):
        # Search the FAISS index for the documents closest to the query embedding
        distances, indices = self.index.search(self.query, k)

        # Retrieve the most relevant documents and their distances
        results = [(self.pdf_filenames[i], distances[0][idx]) for idx, i in enumerate(indices[0])]
        return results
    
    def print_relevant_documents(result):
        # Print the header for the relevant documents
        print("\n-> Most relevant documents found:")
        print("\tDocument                                | Distance")
        print("\t-----------------------------------------|-----------")
        
        # Loop through the result and print each document and its corresponding distance
        for doc, distance in result:
            print(f"\t{doc:<40} | {distance:.4f}")