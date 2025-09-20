import json
import requests
import os

# Paths
json_file = "data/sources.json"
pdf_folder = "data/raw_pdfs"

# Load sources
with open(json_file, "r") as f:
    sources = json.load(f)

# Download PDFs
for item in sources:
    title = item["title"]
    url = item["url"]
    
    # Clean title to use as filename
    filename = "".join(c if c.isalnum() or c in " _-" else "_" for c in title) + ".pdf"
    path = os.path.join(pdf_folder, filename)
    
    # Download
    print(f"Downloading: {title}")
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        print("Saved:", path)
    except Exception as e:
        print("Failed:", title, e)

