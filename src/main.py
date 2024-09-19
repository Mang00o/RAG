from prittier import frame_text
from warning import manage_warning
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
    #           PHASE 1 ~ INGESTING         #
    #########################################

    # Specify the directory where the PDFs are located
    directory = "documents"

    # Create a Retriving instance
    ingesting = Ingesting(directory)

    # Extract text from pdf into the directory
    pdf_texts, pdf_filenames = ingesting.extract_text_from_pdfs()

    # Prints the names of the PDF documents from which it extracted the text
    ingesting.print_loaded_documents()

    print("\n-> Documents ingested successfully!")
    
    #########################################
    #           PHASE 2 ~ EMBEDDING         #
    #########################################

    # Creates an instance of the Embedding class
    embedding = Embedding()

    # Pass document texts to get embeddings (e.g. from pdf_texts)
    embed_text = embedding.embed_texts(pdf_texts)
    
    print("\n-> Documents embedded successfully!")
    
    #########################################
    #           PHASE 3 ~ INDEXING          #
    #########################################

    # Creates an instance of the Indexing class
    indexing = Indexing(embed_text.shape[1])

    # Add the document embeddings to the FAISS index for efficient similarity search
    index = indexing.add(embed_text)

    print("\n-> Documents indexed successfully!")

    #########################################
    #           PHASE 4 ~ RETRIEVING        #
    #########################################

    # Prompt the user to input a query for searching relevant documents

    # Creates an instance of the Retrieving class
    retriving = Retrieving(embed_text, pdf_filenames, index)

    # Define const numner of documents to retrieve
    DOCUMENTS_TO_RETRIEVE = 5

    # Define value of variable k
    k = min(DOCUMENTS_TO_RETRIEVE, len(pdf_filenames)) # 'k' indicates the number of documents to retrieve

    # Perform a search for the top k most relevant documents based on the query embedding
    result = retriving.search_documents(k)  

    # Print the retrieved documents along with their distances
    retriving.print_relevant_documents(result)

    print("\n-> Documents retrieved successfully!")

    #########################################
    #           PHASE 5 ~ GENERATING        #
    #########################################
    
    # Create an instance of the Generating class with the PDF texts and filenames
    generating = Generating(pdf_texts, pdf_filenames)

    # Generate a response using the Ollama model based on the query and the search results
    response = generating.generate_response_with_ollama(retriving.query, result)
    
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

    frame_text('End of the Script')

if __name__ == "__main__":
    main()