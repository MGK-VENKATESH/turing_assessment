import os
import glob

# Create output folder if it doesn't exist
os.makedirs("data/combined", exist_ok=True)

# Get all chunk files
chunk_files = glob.glob("data/chunks/*.txt")

# Group chunks by PDF base name
pdf_dict = {}
for file in chunk_files:
    # remove _chunkXX.txt from filename to get base PDF name
    base_name = "_".join(os.path.basename(file).split("_chunk")[:-1])
    pdf_dict.setdefault(base_name, []).append(file)

# Combine chunks for each PDF
for pdf_name, files in pdf_dict.items():
    files.sort()  # make sure chunks are in order
    output_file = f"data/combined/{pdf_name}_full.txt"
    with open(output_file, "w", encoding="utf-8") as outfile:
        for f in files:
            with open(f, "r", encoding="utf-8") as infile:
                outfile.write(infile.read() + "\n")
    print(f"Combined: {output_file}")

