
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


vectorstore = FAISS.load_local(
    "data/vectorstore", 
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    allow_dangerous_deserialization=True

)


query = "Explain functional safety of machine controls"


results = vectorstore.similarity_search(query, k=5)


for i, r in enumerate(results, 1):
    print(f"Result {i}:\n{r.page_content}\n")

