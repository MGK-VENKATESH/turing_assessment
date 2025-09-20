import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi
from langchain.docstore.document import Document


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vectorstore = FAISS.load_local("data/vectorstore", embeddings=embedding_model, allow_dangerous_deserialization=True)


texts = [doc.page_content for doc in vectorstore.docstore._dict.values()]  
docs = [doc for doc in vectorstore.docstore._dict.values()]  


tokenized_texts = [text.split() for text in texts]
bm25 = BM25Okapi(tokenized_texts)


query = input("Enter your question: ").strip()
query_tokens = query.split()


k = 5  # top-k results
similar_docs = vectorstore.similarity_search(query, k=k)
print("\n--- Top results from FAISS similarity search ---")
for i, doc in enumerate(similar_docs):
    print(f"{i+1}. {doc.page_content[:200]}...")


bm25_scores = bm25.get_scores(query_tokens)


reranked_docs = []
for doc in similar_docs:
    idx = texts.index(doc.page_content)  
    score = bm25_scores[idx]
    reranked_docs.append((doc, score))

reranked_docs.sort(key=lambda x: x[1], reverse=True)

print("\n--- Top results after BM25 reranking ---")
for i, (doc, score) in enumerate(reranked_docs[:3]):
    print(f"{i+1}. Score: {score:.2f}")
    print(doc.page_content[:300], "...\n")  


print("\n=== Before vs After Comparison (Top 3) ===")
for i, doc in enumerate(similar_docs[:3]):
    print(f"FAISS Rank {i+1}: {doc.page_content[:120]}...\n")

for i, (doc, score) in enumerate(reranked_docs[:3]):
    print(f"Reranked Rank {i+1}: {doc.page_content[:120]}...\n")

