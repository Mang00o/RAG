from prittier import frame_text
from warning import manage_warning
from retriving import Retriving

def main():
    frame_text('Inizio dello Script')

    manage_warning()

    #########################
    #       RETRIVING       #
    #########################
    # Specifica la directory dove si trovano i PDF
    directory = "documents"

    # Crea un'istanza di Retriving
    retriving = Retriving(directory)

    # Estrai il testo dai PDF e stampa i nomi dei documenti caricati
    
    retriving.print_loaded_documents()
    # Carica i documenti PDF e salva i nomi
    pdf_texts, pdf_filenames = retriving.extract_text_from_pdfs()

    

    # Stampa fine script
    frame_text('Fine dello Script ')

if __name__ == "__main__":
    main()