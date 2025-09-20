import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi
from langchain.docstore.document import Document

# ------------------------------
# Load vectorstore and embeddings
# ------------------------------
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Allow dangerous deserialization (safe here because you created it)
vectorstore = FAISS.load_local("data/vectorstore", embeddings=embedding_model, allow_dangerous_deserialization=True)

# Load all texts from vectorstore
texts = [doc.page_content for doc in vectorstore.docstore._dict.values()]  # All chunks as strings
docs = [doc for doc in vectorstore.docstore._dict.values()]  # Corresponding Document objects

# ------------------------------
# Build BM25 model
# ------------------------------
tokenized_texts = [text.split() for text in texts]
bm25 = BM25Okapi(tokenized_texts)

# ------------------------------
# Ask question
# ------------------------------
query = input("Enter your question: ").strip()
query_tokens = query.split()

# ------------------------------
# Step 1: Similarity search (vectorstore)
# ------------------------------
k = 5  # top-k results
similar_docs = vectorstore.similarity_search(query, k=k)
print("\n--- Top results from FAISS similarity search ---")
for i, doc in enumerate(similar_docs):
    print(f"{i+1}. {doc.page_content[:200]}...")  # show first 200 chars

# ------------------------------
# Step 2: BM25 reranking
# ------------------------------
bm25_scores = bm25.get_scores(query_tokens)

# Combine FAISS + BM25: rerank top FAISS docs using BM25 scores
reranked_docs = []
for doc in similar_docs:
    idx = texts.index(doc.page_content)  # find original index in texts
    score = bm25_scores[idx]
    reranked_docs.append((doc, score))

reranked_docs.sort(key=lambda x: x[1], reverse=True)

print("\n--- Top results after BM25 reranking ---")
for i, (doc, score) in enumerate(reranked_docs[:3]):
    print(f"{i+1}. Score: {score:.2f}")
    print(doc.page_content[:300], "...\n")  # show first 300 chars

# ------------------------------
# Before vs After Comparison
# ------------------------------
print("\n=== Before vs After Comparison (Top 3) ===")
for i, doc in enumerate(similar_docs[:3]):
    print(f"FAISS Rank {i+1}: {doc.page_content[:120]}...\n")

for i, (doc, score) in enumerate(reranked_docs[:3]):
    print(f"Reranked Rank {i+1}: {doc.page_content[:120]}...\n")

