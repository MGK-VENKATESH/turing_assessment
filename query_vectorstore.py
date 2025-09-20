# Step 1: Import necessary modules
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Step 2: Load your saved vector store
vectorstore = FAISS.load_local(
    "data/vectorstore", 
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    allow_dangerous_deserialization=True

)

# Step 3: Ask a question
query = "Explain functional safety of machine controls"

# Step 4: Search top 5 relevant chunks
results = vectorstore.similarity_search(query, k=5)

# Step 5: Print results
for i, r in enumerate(results, 1):
    print(f"Result {i}:\n{r.page_content}\n")

