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
    db_documents_titles = db_manager.load_documents_names()

    #########################################
    #           PHASE 1 ~ INGESTING         #
    #########################################

    # Specify the directory where the PDFs are located
    directory = "documents"

    # Create a Retriving instance
    ingesting = Ingesting(directory, db_documents_titles)

    # Extract text from pdf into the directory
    ingested_documents_titles, ingested_documentes_contents = ingesting.ingesting()

    # Save ingested documents on DB
    db_manager.save_documents(ingested_documents_titles, ingested_documentes_contents)

    # Prints the names of the PDF documents from which it extracted the text
    ingesting.print_ingested_documents()

    documents_titles = db_documents_titles + ingested_documents_titles

    documents_contents = db_manager.load_documents_contents(db_documents_titles) + ingested_documentes_contents

    print("\n-> Documents ingested successfully!")

    #########################################
    #           PHASE 2 ~ EMBEDDING         #
    #########################################

    bi_converter = BinaryConverter()

    # Creates an instance of the Embedding class
    embedding = Embedding()

    # Pass document contents to get embeddings
    embed_contents = embedding.embedding(documents_contents)

    binary_embed = bi_converter.binary_text(embed_contents)

    db_manager.save_embeddings(ingested_documents_titles,binary_embed)
    
    print("\n-> Documents embedded successfully!")
    
    #########################################
    #           PHASE 3 ~ INDEXING          #
    #########################################

    # Creates an instance of the Indexing class
    indexing = Indexing(embed_contents.shape[1])

    # Add the document embeddings to the FAISS index for efficient similarity search
    indexes = indexing.add(embed_contents)
    
    binary_indexes = bi_converter.binary_text(indexes)

    db_manager.save_indexings(documents_titles,binary_indexes)

    print("\n-> Documents indexed successfully!")
 
    #########################################
    #           PHASE 4 ~ RETRIEVING        #
    #########################################

    # Creates an instance of the Retrieving class
    retrieving = Retrieving(documents_titles, documents_contents, indexes)

    # Perform a search for the top k most relevant documents based on the query embedding
    retrieved_document = retrieving.search_documents()  

    # Print the retrieved documents along with their distances
    retrieving.print_relevant_documents(retrieved_document)

    print("\n-> Documents retrieved successfully!")

    #########################################
    #           PHASE 5 ~ GENERATING        #
    #########################################
    
    # Create an instance of the Generating class with the PDF texts and filenames
    generating = Generating(documents_contents, documents_titles)

    # Generate a response using the Ollama model based on the query and the search results
    response = generating.generate_response_with_ollama(retrieving.query, retrieved_document)
    
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