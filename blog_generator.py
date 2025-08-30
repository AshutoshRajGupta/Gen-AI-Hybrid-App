# modules/blog_generator.py
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from modules.prompts import BLOG_PROMPT
import streamlit as st 
google_api_key = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = google_api_key

def generate_blog(topic: str, tone: str = "formal", prompt_template: str = BLOG_PROMPT) -> str:
    """Generate a blog given a topic, tone, and prompt template using Gemini."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    prompt = prompt_template.format(topic=topic, tone=tone)
    response = llm.invoke(prompt)
    return response.content

