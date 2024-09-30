import warnings

import os
import re
import unicodedata

from transformers import AutoTokenizer, AutoModel
import torch
import faiss

def main():   
    warnings.filterwarnings(
        "ignore", 
        category=FutureWarning, 
        message=r"`clean_up_tokenization_spaces` was not set"
    )

    query = input("\n-> Enter the query to search for relevant documents: ")
    cleaned_query = clean_string(query)
    
    pdfs_names = get_pdfs_names("documents")
    cleared_pdfs_names = clear_list(pdfs_names)

    relevant_pdfs = get_relevant_pdfs(cleaned_query, cleared_pdfs_names)

    print("\n-> Documenti rilevanti:")
    for pdf in relevant_pdfs:
        print(pdf)

    relevant_pdfs_embeddings = embedding(relevant_pdfs)
    for doc, emb in zip(relevant_pdfs, relevant_pdfs_embeddings):
        print(f"{doc:<40}: {emb[:5]}...")

    index = faiss.IndexFlatL2(relevant_pdfs_embeddings.shape[1])
    index.add(relevant_pdfs_embeddings)

    cleaned_query_embedding = embedding(cleaned_query)

    distances, indices = index.search(cleaned_query_embedding, min(3,len(relevant_pdfs)))

    result = [(relevant_pdfs[i], distances[0][idx]) for idx, i in enumerate(indices[0])]

    print()

    for doc, dis in result:
        print(f"{doc:<40}: {dis:.4f}")

    print()

######################

def get_pdfs_names(directory):
    pdfs_names = []

    for pdf_name in os.listdir(directory):
        if pdf_name.endswith(".pdf"):
            pdf_name = clean_string(pdf_name)
            pdfs_names.append(pdf_name)

    return pdfs_names

def clear_list(list):
    cleared_list = []
    for string in list:
        cleared_string = clean_string(string)
        cleared_list.append(cleared_string)
    return cleared_list

def clean_string(text):
    text = text.lower()
    text = os.path.splitext(text)[0]
    text = text.replace("_", " ")
    text = remove_single_letters(text)
    text = re.sub(r'\b\d+\b', '', text)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r"[^\w\s]", '', text)
    text = remove_single_letters(text)
    text = text.replace("  ", " ").strip()

    return text

def remove_single_letters(text):
    words = text.split()
    filtered_words = [word for word in words if len(word) > 1]
    return ' '.join(filtered_words)

def get_relevant_pdfs(cleaned_query, cleared_pdfs_names):
    relevant_pdfs = []
    query_words = cleaned_query.split()

    for pdf_name in cleared_pdfs_names:
        doc_words = pdf_name.split()

        if any(word in doc_words for word in query_words):
            relevant_pdfs.append(pdf_name)

    return relevant_pdfs

def embedding(strings):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    inputs = tokenizer(strings, padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).numpy()

    faiss.normalize_L2(embeddings)

    return embeddings

if __name__ == "__main__":
    main()    
