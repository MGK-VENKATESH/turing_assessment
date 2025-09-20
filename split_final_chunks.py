import os

# Folder with combined PDF texts
input_folder = "data/combined"
# Folder for smaller final chunks
output_folder = "data/final_chunks"
os.makedirs(output_folder, exist_ok=True)

chunk_size = 1000  # number of words per chunk

for file_name in os.listdir(input_folder):
    if file_name.endswith("_full.txt"):
        file_path = os.path.join(input_folder, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            words = f.read().split()
        
        # Split into chunks
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i+chunk_size]
            chunk_text = " ".join(chunk_words)
            
            base_name = file_name.replace("_full.txt", "")
            out_file = os.path.join(output_folder, f"{base_name}_chunk{i//chunk_size+1}.txt")
            with open(out_file, "w", encoding="utf-8") as out_f:
                out_f.write(chunk_text)
            
        print(f"Processed: {file_name}")

