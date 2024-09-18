from transformers import AutoTokenizer, AutoModel
import torch

class Embedding:
    def __init__(self):
        # Carica il modello di embedding
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Funzione per trasformare il testo dei documenti in vettori
    def embed_documents(self, documents):
        inputs = self.tokenizer(documents, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).numpy()
        return embeddings

        