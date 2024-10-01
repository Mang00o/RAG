from prittier import frame_text
from warning import manage_warning
from database_manager import DatabaseManager
from ingesting import Ingesting
from relevanting import Relevanting
from embedding import Embedding
from binary_converter import BinaryConverter
from indexing import Indexing

def main():   
    #########################################
    #                 BEGIN                 #
    #########################################
    frame_text('Start of script')

    manage_warning()

    # Specify the directory where the PDFs are located
    directory = "documents"

    query = input("\n-> Enter the query to search for relevant documents: ")

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

    # Create a Retriving instance
    ingesting = Ingesting(directory, db_documents_names)

    # Extract text from pdf into the directory
    ingested_documents_names, ingested_documentes_texts = ingesting.ingesting()

    # Save ingested documents on DB
    db_manager.save_documents_ingestions(ingested_documents_names, ingested_documentes_texts)

    # Prints the names of the PDF documents from which it extracted the text
    #ingesting.print_ingested_documents()

    #########################################
    #           PHASE 2 ~ EMBEDDING         #
    #########################################

    # Creates an instance of the Embedding class
    embedding = Embedding(ingested_documentes_texts)

    # Pass document contents to get embeddings
    embedded_contents = embedding.embedding()

    # Creates an instance of the BinaryConverter class
    bi_converter = BinaryConverter()

    # Convertes the embeddings into binary 
    binary_embeddings = bi_converter.binary_text(embedded_contents)

    # Save binary embeddings in DB
    db_manager.save_contents_embeddings(ingested_documents_names,binary_embeddings)

    #############################################
    #           PHASE 1.1 ~ RELEVANTING         #
    #############################################

    # All the documents in the directory
    documents_names = db_documents_names + ingested_documents_names

    # Creates an instance of the Relevanting class
    relevanting = Relevanting(query,documents_names)

    # The relevants pdfs names given the query
    # todo deve restituirmi il nome dei documenti rilevanti, da qui in poi lavoriamo con quelli
    relevant_pdfs_names = relevanting.get_relevant_pdfs_names() # !

    #########################################
    #           PHASE 3 ~ INDEXING          #
    #########################################

    # Creates an instance of the Indexing class
    indexing = Indexing(embedded_contents) # TODO utilizza contenuto dei documenti rilevanti

    # Add the document embeddings to the FAISS index for efficient similarity search
    contents_indexes = indexing.add()

    #########################################
    #           PHASE 4 ~ RETRIEVING        #
    #########################################

    query_embedding = embedding(query)

    distances, indices = contents_indexes.search(query_embedding, min(3,len(relevant_pdfs_names))) #!

    retrieve = [(relevant_pdfs_names[i], distances[0][idx]) for idx, i in enumerate(indices[0])]  #!

    #########################################
    #           PHASE 5 ~ GENERATING        #
    #########################################

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
