import os
import glob


os.makedirs("data/combined", exist_ok=True)


chunk_files = glob.glob("data/chunks/*.txt")


pdf_dict = {}
for file in chunk_files:
    
    base_name = "_".join(os.path.basename(file).split("_chunk")[:-1])
    pdf_dict.setdefault(base_name, []).append(file)


for pdf_name, files in pdf_dict.items():
    files.sort()  
    output_file = f"data/combined/{pdf_name}_full.txt"
    with open(output_file, "w", encoding="utf-8") as outfile:
        for f in files:
            with open(f, "r", encoding="utf-8") as infile:
                outfile.write(infile.read() + "\n")
    print(f"Combined: {output_file}")

