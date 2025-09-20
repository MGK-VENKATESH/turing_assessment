import json
import requests
import os


json_file = "data/sources.json"
pdf_folder = "data/raw_pdfs"


with open(json_file, "r") as f:
    sources = json.load(f)


for item in sources:
    title = item["title"]
    url = item["url"]
    
    
    filename = "".join(c if c.isalnum() or c in " _-" else "_" for c in title) + ".pdf"
    path = os.path.join(pdf_folder, filename)
    
    
    print(f"Downloading: {title}")
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
        print("Saved:", path)
    except Exception as e:
        print("Failed:", title, e)

