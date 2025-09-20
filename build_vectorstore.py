import os
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

chunk_folder = "data/final_chunks"


texts = []
for file_name in os.listdir(chunk_folder):
    if file_name.endswith(".txt"):
        with open(os.path.join(chunk_folder, file_name), "r", encoding="utf-8") as f:
            texts.append(f.read())


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vectorstore = FAISS.from_texts(texts, embedding_model)


vectorstore.save_local("data/vectorstore")

print("Vector store created and saved in data/vectorstore")

