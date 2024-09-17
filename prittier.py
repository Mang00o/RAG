def frame_text(text):
    # Calcola la lunghezza della cornice in base alla lunghezza del testo
    length = len(text) + 4  # Aggiungi 4 per gli spazi e i bordi laterali
    print("*" * length)
    print(f"* {text} *")
    print("*" * length)
