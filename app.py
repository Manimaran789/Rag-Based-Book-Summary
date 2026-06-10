from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import time
import threading
from backend.ingest import extract_text, chunk_text
from backend.vector_store import store_chunks, retrieve
from backend.rag import generate_answer

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        start = time.time()

        content = await file.read()

        # 🔥 Step 1: extract
        text = extract_text(content)

        if not text.strip():
            return {"status": "error", "message": "No text extracted"}

        # 🔥 Step 2: chunk
        chunks = chunk_text(text)

        if not chunks:
            return {"status": "error", "message": "Chunking failed"}

        # 🔥 Step 3: store (FIXED HERE 🔴)
        threading.Thread(target=store_chunks, args=(chunks,)).start()

        print("⏱ Processing time:", time.time() - start)

        return {
            "status": "success",
            "chunks": len(chunks)
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/query")
def query(req: QueryRequest):
    try:
        # 🔥 Step 4: retrieve
        context = retrieve(req.query)

        if not context:
            return {"answer": "⚠️ No relevant content found. Try different question."}

        # 🔥 Step 5: generate
        answer = generate_answer(req.query, context)

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"❌ Error: {str(e)}"}