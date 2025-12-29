from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
import uvicorn
from fastapi import UploadFile
import os
import aiofiles

from docx import Document
from fastapi.responses import FileResponse
from fastapi import UploadFile, File, Request
# from src.helper import llm_pipeline
from src.file_processing import file_process
from src.llm import generate_questions,save_output
from src.prompt_template import prompt_temp

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


GENERATED_TEXT_FILE = "generated_questions.txt"
GENERATED_WORD_FILE = "generated_questions.docx"

# @app.post("/generate")
# async def generate_questions_api(pdf_file: UploadFile = File(...)):
#     base_folder = "static"
#     os.makedirs(base_folder, exist_ok=True)

#     pdf_path = os.path.join(base_folder, pdf_file.filename)

#     async with aiofiles.open(pdf_path, "wb") as f:
#         await f.write(await pdf_file.read())

#     chunks = file_process(pdf_path)

#     response = generate_questions(
#         chunks,
#         num_questions=20,
#         words_per_answer=35
#     )

#     save_output(response, "generated_questions.txt")

#     return {
#         "output": response
#     }


import mimetypes

@app.post("/generate")
async def generate_questions_api(
    nums: int = Form(...),
    uploaded_file: UploadFile = File(...)
):
    base_folder = "static"
    os.makedirs(base_folder, exist_ok=True)

    file_path = os.path.join(base_folder, uploaded_file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(await uploaded_file.read())

    # Optional: print MIME type
    mime_type = uploaded_file.content_type
    print("Uploaded file type:", mime_type)

    chunks = file_process(file_path)

    response = generate_questions(
    document_chunks=chunks,
    filename=uploaded_file.filename,
    num_questions=nums,
    words_per_answer=35
     )


    with open(GENERATED_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(response)

    return {"status": "generated", "output": response}



@app.get("/download-word")
async def download_word():
    if not os.path.exists(GENERATED_TEXT_FILE):
        raise HTTPException(status_code=404, detail="No generated content")

    doc = Document()
    doc.add_heading("Generated Questions & Answers", level=1)

    with open(GENERATED_TEXT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    for line in content.split("\n"):
        doc.add_paragraph(line)

    doc.save(GENERATED_WORD_FILE)

    return FileResponse(
        GENERATED_WORD_FILE,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="Generated_Questions.docx"
    )



# @app.post("/upload")
# async def chat(
#     request: Request,
#     pdf_file: UploadFile = File(...)):

#     base_folder = "static"
#     os.makedirs(base_folder, exist_ok=True)
#     for filename in os.listdir(base_folder):
#         file_path = os.path.join(base_folder, filename)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#     pdf_path = os.path.join(base_folder, pdf_file.filename)
#     async with aiofiles.open(pdf_path, "wb") as f:
#         await f.write(await pdf_file.read())
#     pdf_path = pdf_path.replace("\\", "/")
#     return {
#     "file_path": pdf_path
# }



# @app.post("/generate")
# async def generate_qa(file_path: str = Form(...)):
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     chunks = file_process(file_path)

#     response = generate_questions(
#         chunks,
#         num_questions=20,
#         words_per_answer=35
#     )

#     save_output(response, "generated_questions.txt")

#     return {
#         "status": "generated",
#         "output": response
#     }


# @app.post("/upload")
# async def chat(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
#     base_folder = 'static/docs/'
#     if not os.path.isdir(base_folder):
#         os.mkdir(base_folder)
#     pdf_filename = os.path.join(base_folder, filename)

#     async with aiofiles.open(pdf_filename, 'wb') as f:
#         await f.write(pdf_file)
 
#     response_data = jsonable_encoder(json.dumps({"msg": 'success',"pdf_filename": pdf_filename}))
#     res = Response(response_data)
#     return res


# def get_csv(file_path):
#     answer_generation_chain, ques_list = llm_pipeline(file_path)
#     base_folder = 'static/output/'
#     if not os.path.isdir(base_folder):
#         os.mkdir(base_folder)
#     output_file = base_folder+"QA.csv"
#     with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(["Question", "Answer"])  # Writing the header row

#         for question in ques_list:
#             print("Question: ", question)
#             answer = answer_generation_chain.run(question)
#             print("Answer: ", answer)
#             print("--------------------------------------------------\n\n")

#             # Save answer to CSV file
#             csv_writer.writerow([question, answer])
#     return output_file




# @app.post("/analyze")
# async def chat(request: Request, pdf_filename: str = Form(...)):
#     output_file = get_csv(pdf_filename)
#     response_data = jsonable_encoder(json.dumps({"output_file": output_file}))
#     res = Response(response_data)
#     return res



if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)