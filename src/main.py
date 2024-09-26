from prittier import frame_text
from warning import manage_warning
from database_manager import DatabaseManager
from binary_converter import BinaryConverter
from ingesting import Ingesting
from embedding import Embedding
from indexing import Indexing
from retrieving import Retrieving
from generating import Generating

def main():
    #########################################
    #                 BEGIN                 #
    #########################################
    frame_text('Start of script')

    manage_warning()

    #########################################
    #           PHASE 0 ~ DBING             #
    #########################################

    # Create a Retriving instance
    db_manager = DatabaseManager()

    # Connect to the database
    db_manager.connect()

    # Read documents names from the database
    db_documents_names = db_manager.load_documents_names()

    #########################################
    #           PHASE 1 ~ INGESTING         #
    #########################################

    # Specify the directory where the PDFs are located
    directory = "documents"

    # Create a Retriving instance
    ingesting = Ingesting(directory, db_documents_names)

    # Extract text from pdf into the directory
    ingested_documents_names, ingested_documentes_texts = ingesting.ingesting()

    # Save ingested documents on DB
    db_manager.save_documents_ingestions(ingested_documents_names, ingested_documentes_texts)

    # Prints the names of the PDF documents from which it extracted the text
    ingesting.print_ingested_documents()

    documents_names = db_documents_names + ingested_documents_names

    documents_texts = db_manager.load_documents_contents(db_documents_names) + ingested_documentes_texts

    bi_converter = BinaryConverter()
    
    if ingested_documents_names:
        #########################################
        #           PHASE 2 ~ EMBEDDING         #
        #########################################

        # Creates an instance of the Embedding class
        embedding = Embedding()

        # Pass document contents to get embeddings
        embedded_contents = embedding.embedding(ingested_documentes_texts)

        binary_embeddings = bi_converter.binary_text(embedded_contents)

        db_manager.save_contents_embeddings(ingested_documents_names,binary_embeddings)
        
        #########################################
        #           PHASE 3 ~ INDEXING          #
        #########################################

        # Creates an instance of the Indexing class
        indexing = Indexing(embedded_contents.shape[1])

        # Add the document embeddings to the FAISS index for efficient similarity search
        contents_indexes = indexing.add(embedded_contents)
        
        binary_indexes_bytes = bi_converter.binary_indexes_bytes(contents_indexes)

        db_manager.save_indexings(ingested_documents_names,binary_indexes_bytes)
    else:
        print("\n-> Embedding already saved")
        print("\n-> Indexing already saved")
 
    #########################################
    #           PHASE 4 ~ RETRIEVING        #
    #########################################

    binary_indexes_bytes = db_manager.load_all_indices()

    indexes = bi_converter.normal_indexes(binary_indexes_bytes)

    query = input("\n-> Enter the query to search for relevant documents: ")

    embedded_query = embedding.embedding(query)

    # Creates an instance of the Retrieving class
    retrieving = Retrieving(documents_names, documents_texts, indexes, embedded_query)

    # Perform a search for the top k most relevant documents based on the query embedding
    retrieved_document = retrieving.search_documents()  

    # Print the retrieved documents along with their distances
    retrieving.print_relevant_documents(retrieved_document)

    print("\n-> Documents retrieved successfully!")

    #########################################
    #           PHASE 5 ~ GENERATING        #
    #########################################
    
    # Create an instance of the Generating class with the PDF texts and filenames
    generating = Generating(documents_texts, documents_names)

    # Generate a response using the Ollama model based on the query and the search results
    response = generating.generate_response_with_ollama(retrieving.embedded_query, retrieved_document)
    
    # Print the response generated by Ollama
    generating.print_ollama_response(response)

    print("\n-> Response generated successfully!")

    #########################################
    #           PHASE 6 ~ PROCESSING        #
    #########################################

    #not implemented

    #########################################
    #                 END                   #
    #########################################

    db_manager.close()

    frame_text('End of the Script')

if __name__ == "__main__":
    main()