from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF
from openai import OpenAI
import os


client = OpenAI()
# openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set this

app = FastAPI()

# Enable CORS for frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MaterialRequest(BaseModel):
    content: str
    task: str  # 'quiz', 'summary', 'feedback', 'grade'

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    return {"text": text}

@app.post("/generate/")
async def generate_material(request: MaterialRequest):
    prompt_map = {
        "quiz": f"Generate 5 quiz questions based on the following text:\n{request.content}",
        "summary": f"Summarize the following content in bullet points:\n{request.content}",
        "feedback": f"Provide constructive feedback for the following student submission:\n{request.content}",
        "grade": f"Grade the following student response using a scale of 1-10 and explain:\n{request.content}"
    }
    prompt = prompt_map.get(request.task, request.content)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an educational assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"result": response.choices[0].message.content}

@app.get("/")
async def root():
    return {"message": "Teacher Doc Analyzer API is running."}
