from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
import aiofiles
import json

from python_src.llm import generate_questions
from python_src.file_processing import file_process
app = FastAPI(title="Short Answer Generator API")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- FOLDERS ----------------
BASE_FOLDER = "static/docs"
OUTPUT_FOLDER = "static/output"

os.makedirs(BASE_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------- ROUTES ----------------
@app.get("/")
async def root():
    return {"status": "running", "message": "Short Answer Generator API"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = [".txt", ".pdf", ".doc", ".docx"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file_path = os.path.join(BASE_FOLDER, file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await file.read())

    return {
        "status": "success",
        "filename": file.filename,
        "filepath": file_path
    }

@app.post("/api/generate")
async def generate_qa(
    filepath: str = Form(...),
    num_questions: int = Form(5)
):
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")

    chunks = file_process(filepath)

    response = generate_questions(
        chunks,
        num_questions=num_questions,
        words_per_answer=35
    )

    if not response:
        raise HTTPException(status_code=500, detail="LLM generation failed")

    questions = parse_qa_response(response)

    output_file = os.path.join(OUTPUT_FOLDER, "qa_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    return {
        "status": "success",
        "questions": questions
    }

@app.delete("/api/cleanup")
async def cleanup():
    for folder in [BASE_FOLDER, OUTPUT_FOLDER]:
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

    return {"status": "success", "message": "Cleanup done"}

# ---------------- PARSER ----------------
def parse_qa_response(response: str):
    results = []
    lines = response.split("\n")

    q, a = None, []
    qid = 1

    for line in lines:
        line = line.strip()

        if line.lower().startswith(("q", "question")):
            if q:
                results.append({
                    "id": qid,
                    "question": q,
                    "answer": " ".join(a).strip()
                })
                qid += 1
                a = []

            q = line.split(":", 1)[-1].strip()

        elif line.lower().startswith(("a", "answer")):
            a.append(line.split(":", 1)[-1].strip())

        elif q:
            a.append(line)

    if q:
        results.append({
            "id": qid,
            "question": q,
            "answer": " ".join(a).strip()
        })

    return results

if __name__ == "__main__":
    uvicorn.run("python_src.app:app", host="0.0.0.0", port=8000, reload=True)
