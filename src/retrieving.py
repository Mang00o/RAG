import re

class Retrieving:
    def __init__(self, documents_names, documents_texts, indexes, embedded_query):
        # Save document embeddings, file names, document texts, and FAISS indexes
        self.documents_names = documents_names
        self.documents_texts = documents_texts  # This should contain the raw text of the documents
        self.indexes = indexes
        self.embedded_query = embedded_query

    # Function to search for relevant documents based on a query
    def search_documents(self):       
        # Search the FAISS indexes for the documents closest to the query embedding
        distances, indices = self.indexes.search(self.embedded_query, self.__define_k())

        # Retrieve the most relevant documents and their distances
        results = [(self.documents_names[i], distances[0][idx]) for idx, i in enumerate(indices[0])]

        # Apply keyword relevance boost using the raw text
        boosted_results = self.__boost_keyword_relevance(self.embedded_query, results)
        return boosted_results
    
    def __define_k(self):
        # Define const numner of documents to retrieve
        DOCUMENTS_TO_RETRIEVE = 5

        # Define value of variable k
        k = min(DOCUMENTS_TO_RETRIEVE, len(self.documents_names)) # 'k' indicates the number of documents to retrieve

        return k
    
    # Boost documents that contain the query keyword using the raw document text
    def __boost_keyword_relevance(self, query, embedding_results):
        boosted_results = []
        query = query.lower()

        # Use a regex to find the exact keyword
        query_regex = re.compile(r'\b' + re.escape(query) + r'\b', re.IGNORECASE)

        for idx, (doc_name, distance) in enumerate(embedding_results):
            # Check the extracted text
            doc_text = self.documents_texts[idx].lower()

            # Search for query in text using regex
            relevance = len(query_regex.findall(doc_text))

            # Change distance based on relevance    
            if relevance > 0:
                adjusted_distance = max(distance - (relevance * 0.3), 0)
            else:
                adjusted_distance = distance

            boosted_results.append((doc_name, adjusted_distance))

        # Sort results by adjusted distance
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