import faiss
from transformers import AutoTokenizer, AutoModel
import torch

class Embedding:
    def __init__(self):
        # Load the embedding model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Method for transforming document text into vectors and normalizing them
    def embed_contents(self, contents):
        # Tokenize the texts
        inputs = self.tokenizer(contents, padding=True, truncation=True, return_tensors="pt")
        
        # Compute the embeddings without gradient calculation
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).numpy()

        # Normalize the embeddings (L2 normalization)
        faiss.normalize_L2(embeddings)

        return embeddings
