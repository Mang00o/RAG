import faiss
from transformers import AutoTokenizer, AutoModel
import torch

#################################################################
#   This class compute the embedding of the ingested texts.     #
#   Return the normalized embeddings of that texts              #
#################################################################
class Embedding:
    def __init__(self,ingested_documentes_texts):
        self.ingested_documentes_texts = ingested_documentes_texts
        # Load the embedding model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Method for transforming document text into vectors and normalizing them
    def embedding(self):
        # Tokenize the texts
        inputs = self.tokenizer(self.ingested_documentes_texts, padding=True, truncation=True, return_tensors="pt")
        
        # Compute the embeddings without gradient calculation
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).numpy()

        # Normalize the embeddings (L2 normalization)
        faiss.normalize_L2(embeddings)

        return embeddings