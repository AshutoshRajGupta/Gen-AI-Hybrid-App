# modules/summarizer.py
import os
import tempfile
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from PyPDF2 import PdfReader
from modules.prompts import SUMMARIZER_PROMPT

load_dotenv()
import streamlit as st 
google_api_key = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = google_api_key

def read_file(file):
    """Reads uploaded TXT or PDF file and returns text content."""
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        return ""

def summarize_file(file, style: str, prompt_template: str = SUMMARIZER_PROMPT) -> str:
    """Summarize a TXT or PDF file with embeddings + custom prompt support."""
    text = read_file(file)

    # Generate embeddings for logging
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    with open("summarizer_embeddings.txt", "a", encoding="utf-8") as f:
        for chunk in chunks:
            vector = embeddings.embed_query(chunk)
            f.write(f"{chunk[:50]}... -> {vector[:5]}\n")  # log first 5 dims

    # Summarize with Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
    prompt = prompt_template.format(text=text, style=style)
    response = llm.invoke(prompt)
    return response.content

