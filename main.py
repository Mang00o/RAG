from prittier import frame_text
from warning import manage_warning
from retriving import Retriving
from embedding import Embedding

def main():
    frame_text('Inizio dello Script')

    manage_warning()

    #################################
    #       PHASE 1 ~ RETRIVING     #
    #################################

    # Specifica la directory dove si trovano i PDF
    directory = "documents"

    # Crea un'istanza di Retriving
    retriving = Retriving(directory)

    # Estre testo da pdf nella directory
    pdf_texts, pdf_filenames = retriving.extract_text_from_pdfs()

    # Stampa i nomi dei documenti pdf da cui ha estratto il testo
    retriving.print_loaded_documents()

    
    

    # Stampa fine script
    frame_text('Fine dello Script ')

if __name__ == "__main__":
    main()