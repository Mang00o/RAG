import faiss
from transformers import AutoTokenizer, AutoModel
import torch

class Embedding:
    def __init__(self):
        # Upload the embedding template
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Method for transforming document text into vectors and normalizing them
    def embed_texts(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).numpy()

        # Normalize the embeddings (L2 normalization)
        faiss.normalize_L2(embeddings)

        return embeddings