import os
import pdfplumber


pdf_folder = "data/raw_pdfs"
chunks_folder = "data/chunks"
os.makedirs(chunks_folder, exist_ok=True)


CHUNK_SIZE = 300  # words per chunk

def split_into_chunks(text, chunk_size=CHUNK_SIZE):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i + chunk_size])
        chunks.append(chunk_text)
    return chunks


for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"Processing: {pdf_file}")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() + "\n"
            
            chunks = split_into_chunks(full_text)
            
            
            base_name = os.path.splitext(pdf_file)[0]
            for idx, chunk in enumerate(chunks):
                chunk_filename = f"{base_name}_chunk{idx+1}.txt"
                chunk_path = os.path.join(chunks_folder, chunk_filename)
                with open(chunk_path, "w", encoding="utf-8") as f:
                    f.write(chunk)
        except Exception as e:
            print("Failed to process:", pdf_file, e)

