from fastapi import FastAPI
from pydantic import BaseModel
from answerer import ask

app = FastAPI()

class AskRequest(BaseModel):
    q: str
    k: int = 5
    mode: str = "hybrid"  # "baseline" or "hybrid"

@app.post("/ask")
def ask_endpoint(req: AskRequest):
    resp = ask(req.q, k=req.k, mode=req.mode)
    return resp

