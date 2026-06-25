from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from pdf_service import extract_text
from gemini_service import (
    ask_gemini,
    generate_summary,
    generate_flashcards,
    generate_interview_questions
)


app = FastAPI(
    title="DocMind AI",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

stored_text = ""


@app.get("/")
def home():

    return {
        "message":
        "DocMind AI Backend Running"
    }


@app.get("/health")
def health():

    return {
        "status":
        "healthy"
    }


@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    global stored_text

    stored_text = extract_text(
        file.file
    )

    return {
        "message":
        "PDF uploaded successfully",

        "characters":
        len(stored_text)
    }


class QuestionRequest(
    BaseModel
):

    question: str


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    global stored_text

    if not stored_text:

        return {
            "error":
            "Upload PDF first"
        }

    answer = ask_gemini(
        stored_text,
        request.question
    )

    return {
        "answer":
        answer
    }

@app.post("/summary")
def summary():

    global stored_text

    if not stored_text:

        return {
            "error": "Upload PDF first"
        }

    result = generate_summary(
        stored_text
    )

    return {
        "summary":result
    }

@app.post("/flashcards")
def flashcards():

    global stored_text

    if not stored_text:

        return {
            "error":"Upload PDF first"
        }

    result = generate_flashcards(
        stored_text
    )

    return {
        "flashcards":result
    }

@app.post("/interview-questions")
def interview_questions():

    global stored_text

    if not stored_text:

        return {
            "error":"Upload PDF first"
        }

    result = generate_interview_questions(
        stored_text
    )

    return {
        "questions":result
    }