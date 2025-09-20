import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rank_bm25 import BM25Okapi

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VSTORE = "data/vectorstore"

# load embeddings & vectorstore
embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vectorstore = FAISS.load_local(VSTORE, embeddings=embedding_model, allow_dangerous_deserialization=True)

# build BM25 over all chunks (we can reuse tokenized list)
all_texts = [d.page_content for d in vectorstore.docstore._dict.values()]
tokenized_texts = [t.split() for t in all_texts]
bm25 = BM25Okapi(tokenized_texts)

def normalize(arr):
    arr = np.array(arr, dtype=float)
    if arr.max() - arr.min() < 1e-8:
        return np.ones_like(arr)
    return (arr - arr.min()) / (arr.max() - arr.min())

def ask(q, k=5, mode="hybrid", abstain_threshold=0.25, alpha=0.6):
    # baseline: vector search with scores
    docs_with_scores = vectorstore.similarity_search_with_score(q, k=k)
    faiss_docs, faiss_scores = zip(*docs_with_scores)
    # extract text list for BM25 scoring
    query_tokens = q.split()
    bm25_scores_all = bm25.get_scores(query_tokens)
    texts = all_texts

    # get indices of the top faiss docs in all_texts
    top_indices = [texts.index(d.page_content) for d in faiss_docs]

    # get BM25 scores for these
    bm25_top = [bm25_scores_all[i] for i in top_indices]

    # normalize & combine
    faiss_norm = normalize(faiss_scores)
    bm25_norm = normalize(bm25_top)
    combined = alpha * faiss_norm + (1 - alpha) * bm25_norm

    # compute baseline top-1 score (use faiss_norm[0]) for abstain if mode==baseline
    if mode == "baseline":
        best_idx = 0
        best_score = faiss_norm[0]
        chosen_doc = faiss_docs[0]
    else:
        # mode == hybrid: pick max combined
        best_pos = int(np.argmax(combined))
        best_score = combined[best_pos]
        chosen_doc = faiss_docs[best_pos]

    # abstain check
    if best_score < abstain_threshold:
        return {
            "answer": None,
            "reason": f"Top score {best_score:.3f} < abstain_threshold {abstain_threshold}",
            "contexts": [
                {"text": d.page_content[:500], "score": faiss_scores[i], "source_title": d.metadata.get("source_title", ""), "source_url": d.metadata.get("source_url","")} 
                for i, d in enumerate(faiss_docs)
            ],
            "reranker_used": (mode!="baseline")
        }

    # produce a short extractive answer: return first 200-300 chars of chosen doc (or a sentence)
    text = chosen_doc.page_content
    snippet = text.strip().split("\n")[0][:400]  # simple extract
    contexts = []
    for i, d in enumerate(faiss_docs):
        contexts.append({"text": d.page_content[:500], "score": float(faiss_scores[i]), "source_title": d.metadata.get("source_title",""), "source_url": d.metadata.get("source_url","")})

    return {
        "answer": snippet,
        "contexts": contexts,
        "reranker_used": (mode!="baseline"),
        "score": float(best_score),
        "citation": {"source_title": chosen_doc.metadata.get("source_title",""), "source_url": chosen_doc.metadata.get("source_url","")}
    }

# sample manual test
if __name__ == "__main__":
    q = input("Question: ")
    out = ask(q, k=5, mode="hybrid")
    import json; print(json.dumps(out, indent=2))

