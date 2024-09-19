from embedding import Embedding

class Retrieving:
    def __init__(self, document_embeddings, pdf_filenames, pdf_texts, index):
        # Save document embeddings, file names, document texts, and FAISS index
        self.document_embeddings = document_embeddings
        self.pdf_filenames = pdf_filenames
        self.pdf_texts = pdf_texts  # This should contain the raw text of the documents
        self.index = index

        # Prompt the user for the query during object initialization
        self.query = input("\n-> Enter the query to search for relevant documents: ")

    # Function to search for relevant documents based on a query
    def search_documents(self, k=1):
        embedding = Embedding()
        
        query_embedding = embedding.embed_texts([self.query])
        
        # Search the FAISS index for the documents closest to the query embedding
        distances, indices = self.index.search(query_embedding, k)

        # Retrieve the most relevant documents and their distances
        results = [(self.pdf_filenames[i], distances[0][idx]) for idx, i in enumerate(indices[0])]

        # Apply keyword relevance boost using the raw text
        boosted_results = self.boost_keyword_relevance(self.query, results)
        return boosted_results
    
    # Boost documents that contain the query keyword using the raw document text
    def boost_keyword_relevance(self, query, embedding_results):
        boosted_results = []
        for idx, (doc_name, distance) in enumerate(embedding_results):
            # Check how many times the query appears in the document text
            relevance = self.pdf_texts[idx].lower().count(query.lower())  # Use the raw text

            # Adjust the distance based on relevance
            if relevance > 0:
                adjusted_distance = distance - (relevance * 0.1)
            else:
                adjusted_distance = distance

            boosted_results.append((doc_name, adjusted_distance))

        # Sort results based on the adjusted distance
        boosted_results.sort(key=lambda x: x[1])
        return boosted_results

    def print_relevant_documents(self, result):
        # Print the header for the relevant documents
        print("\n-> Most relevant documents found:")
        print("\tDocument                                 | Distance")
        print("\t-----------------------------------------|-----------")
        
        # Loop through the result and print each document and its corresponding distance
        for doc, distance in result:
            print(f"\t{doc:<40} | {distance:.4f}")