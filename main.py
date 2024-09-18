from prittier import frame_text
from warning import manage_warning
from ingesting import Ingesting
from embedding import Embedding

def main():
    frame_text('Start of script')

    manage_warning()

    #################################
    #       PHASE 1 ~ INGESTING     #
    #################################

    # Specify the directory where the PDFs are located
    directory = "documents"

    # Create a Retriving instance
    ingesting = Ingesting(directory)

    # Extract text from pdf into the directory
    pdf_texts, pdf_filenames = ingesting.extract_text_from_pdfs()

    # Prints the names of the PDF documents from which it extracted the text
    ingesting.print_loaded_documents()

    #################################
    #       PHASE 2 ~ EMBEDDING     #
    #################################

    # Creates an instance of the Embedding class
    embedding = Embedding()

    # Pass document texts to get embeddings (e.g. from pdf_texts)
    document_embeddings = embedding.embed_documents(pdf_texts)
    
    #################################
    #       PHASE 3 ~ INDEXING      #
    #################################

    #################################
    #       PHASE 4 ~ RETRIVING     #
    #################################

    #################################
    #       PHASE 5 ~ GENERATING    #
    #################################

    #################################
    #       PHASE 6 ~ PROCESSING    #
    #################################

    # Stampa fine script
    frame_text('End of the Script')

if __name__ == "__main__":
    main()