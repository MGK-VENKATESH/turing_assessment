import os, sqlite3, json, uuid

DB = "data/chunks.db"
CHUNK_DIR = "data/final_chunks"
SOURCES_JSON = "data/sources.json"

os.makedirs("data", exist_ok=True)

# load sources.json to map title -> url (if you have it)
sources = {}
if os.path.exists(SOURCES_JSON):
    with open(SOURCES_JSON, "r", encoding="utf-8") as f:
        src_list = json.load(f)
        for s in src_list:
            sources[s["title"]] = s.get("url", "")

conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS chunks (
    id TEXT PRIMARY KEY,
    filename TEXT,
    source_title TEXT,
    source_url TEXT,
    text TEXT
)
""")
conn.commit()

for fname in sorted(os.listdir(CHUNK_DIR)):
    if not fname.endswith(".txt"):
        continue
    path = os.path.join(CHUNK_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    # extract a source title from filename heuristically (before _chunk)
    source_title = fname.split("_chunk")[0].replace(".txt","")
    url = sources.get(source_title, "")
    chunk_id = str(uuid.uuid4())
    c.execute("INSERT INTO chunks (id, filename, source_title, source_url, text) VALUES (?, ?, ?, ?, ?)",
              (chunk_id, fname, source_title, url, text))
conn.commit()
conn.close()
print("Ingested chunks into", DB)

