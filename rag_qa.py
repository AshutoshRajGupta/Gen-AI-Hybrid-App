# modules/rag_qa.py
import os
import tempfile
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

load_dotenv()
import streamlit as st 
google_api_key = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = google_api_key

# Initialize embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def load_file_content(uploaded_file):
    """Read file content (PDF or TXT)."""
    if uploaded_file.name.endswith(".pdf"):
        pdf = PdfReader(uploaded_file)
        text = "".join([page.extract_text() or "" for page in pdf.pages])
    else:
        text = uploaded_file.read().decode("utf-8")
    return text

def store_embeddings(uploaded_file, persist_dir="chroma_store"):
    """Chunk the document, create embeddings, and store in Chroma."""
    text = load_file_content(uploaded_file)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_text(text)

    vectordb = Chroma.from_texts(chunks, embeddings, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb

def answer_question(question, persist_dir="chroma_store"):
    """Retrieve relevant chunks and answer using Gemini."""
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
    prompt = f"Answer the question based on the context below:\n\n{context}\n\nQuestion: {question}\nAnswer:"
    response = llm.invoke(prompt)
    return response.content

