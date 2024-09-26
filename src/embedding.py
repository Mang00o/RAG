import faiss
from transformers import AutoTokenizer, AutoModel
import torch
class Embedding:
    def __init__(self):
        # Load the embedding model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Method for transforming document text into vectors and normalizing them
    def embedding(self, ingested_documentes_texts):
        # Tokenize the texts
        inputs = self.tokenizer(ingested_documentes_texts, padding=True, truncation=True, return_tensors="pt")
        
        # Compute the embeddings without gradient calculation
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).numpy()

        # Normalize the embeddings (L2 normalization)
        faiss.normalize_L2(embeddings)

        return embeddings
        # Example of the embedding array:
        # Each row represents the embedding of a single text, and each value is a dimension of the embedding.
        # The array has a shape of (num_texts, embedding_dimension).
        # For example, with 3 texts and an embedding dimension of 384, it might look like this:

        # array([
        #     [0.12, 0.34, ..., 0.45],  # Embedding of the first text
        #     [0.22, 0.56, ..., 0.34],  # Embedding of the second text
        #     [0.54, 0.23, ..., 0.67],  # Embedding of the third text
        # ])
