import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_gemini(context, question):

    prompt = f"""
You are an AI PDF Assistant.

Document Content:

{context}

Question:

{question}

Answer based only on the document.
"""

    response = model.generate_content(prompt)

    return response.text



def generate_summary(context):

    prompt = f"""
    Analyze the document and generate:

    1. Executive Summary
    2. Key Takeways
    3. Important Concepts

    Document:

    {context}
    """

    response = model.generate_content(prompt)

    return response.text


def generate_flashcards(context):

    prompt = f"""
    Create 10 study flashcards.

    Format:

    Question:
    Answer:

    Document:

    {context}
    """

    response = model.generate_content(prompt)

    return response.text

def generate_interview_questions(context):

    prompt = f"""
    Generate 20 interview questions with accurate answers form the document.

    Document:
    {context}
    """

    response = model.generate_content(prompt)

    return response.text