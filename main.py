from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import rag
from graph import graph

load_dotenv()

app = FastAPI(title="LangGraph Chatbot API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok", "rag_ready": rag.has_documents()}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    contents = await file.read()
    try:
        chunk_count = rag.ingest_pdf(contents)
        return {"message": "PDF indexed successfully", "filename": file.filename, "chunks": chunk_count}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/clear")
def clear():
    rag.clear_documents()
    return {"message": "PDF index cleared"}


@app.post("/chat")
def chat(req: ChatRequest):
    messages = [m.model_dump() for m in req.messages]
    if not messages:
        raise HTTPException(status_code=400, detail="messages list cannot be empty")
    try:
        result = graph.invoke({"messages": messages, "context": ""})
        return {"response": result["messages"][-1]["content"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

print("API ready at http://localhost:8000")