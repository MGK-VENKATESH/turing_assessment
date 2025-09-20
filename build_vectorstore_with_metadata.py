import sqlite3
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DB = "data/chunks.db"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OUT_DIR = "data/vectorstore"

# load chunks and metadata
conn = sqlite3.connect(DB)
c = conn.cursor()
rows = c.execute("SELECT id, source_title, source_url, text FROM chunks").fetchall()
ids, metadatas, texts = [], [], []
for chunk_id, title, url, text in rows:
    ids.append(chunk_id)
    metadatas.append({"id": chunk_id, "source_title": title, "source_url": url})
    texts.append(text)

conn.close()

embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
# Build vectorstore with metadata
vectorstore = FAISS.from_texts(texts, embedding_model, metadatas=metadatas)
vectorstore.save_local(OUT_DIR)
print("Saved vectorstore at", OUT_DIR)

