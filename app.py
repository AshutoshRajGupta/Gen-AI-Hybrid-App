
import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

from modules.blog_generator import generate_blog
from modules.summarizer import summarize_file
from modules.history import save_history, load_history
from modules.rag_qa import store_embeddings, answer_question
from modules.prompts import BLOG_PROMPT, SUMMARIZER_PROMPT


st.set_page_config(page_title="GenAI Hybrid App", layout="wide")

st.title("✍️ GenAI Hybrid App")
st.write("A combination of **AI Blog Generator**, **AI Summarizer**, and **Q&A over documents** with embeddings logging.")

# Sidebar for section navigation
section = st.sidebar.radio("Choose a section:", ["Blog Generator", "AI Summarizer", "Q&A", "History"])

# ========================= BLOG GENERATOR =========================
if section == "Blog Generator":
    st.header("📝 Blog Generator")

    topic = st.text_input("Enter a blog topic", key="blog_topic")
    tone = st.selectbox("Choose a writing tone:", ["formal", "casual", "marketing", "academic"], key="blog_tone")

    # Custom prompt option
    use_custom_prompt = st.checkbox("✏️ Use custom blog prompt?")
    if use_custom_prompt:
        custom_blog_prompt = st.text_area("Edit the blog prompt template:", value=BLOG_PROMPT, height=250)
    else:
        custom_blog_prompt = BLOG_PROMPT

    if st.button("Generate Blog", key="generate_blog"):
        if topic.strip():
            with st.spinner("Generating your blog..."):
                blog = generate_blog(topic, tone, custom_blog_prompt)
                st.success("✅ Blog generated successfully!")
                st.write(blog)

                # Save to history
                save_history("blogs.json", {
                    "topic": topic,
                    "tone": tone,
                    "content": blog
                })
        else:
            st.error("⚠️ Please enter a topic.")

# ========================= AI SUMMARIZER =========================
elif section == "AI Summarizer":
    st.header("📄 AI Summarizer")

    uploaded_file = st.file_uploader("Upload a TXT or PDF file", type=["txt", "pdf"], key="upload_file")
    style = st.selectbox("Choose summary style:", ["concise", "detailed", "bullet_points"], key="summary_style")


    use_custom_prompt = st.checkbox("✏️ Use custom summarizer prompt?")
    if use_custom_prompt:
        custom_summarizer_prompt = st.text_area("Edit the summarizer prompt template:", value=SUMMARIZER_PROMPT, height=200)
    else:
        custom_summarizer_prompt = SUMMARIZER_PROMPT
    if st.button("Summarize File", key="summarize_file"):
        if uploaded_file is not None:
            with st.spinner("Summarizing file and generating embeddings..."):
                summary = summarize_file(uploaded_file, style, custom_summarizer_prompt)
                st.success("✅ Summary generated successfully!")
                st.write(summary)
                st.info("ℹ️ Embeddings for each chunk are saved in `summarizer_embeddings.txt`.")

                # Save to history
                save_history("summaries.json", {
                    "file_name": uploaded_file.name,
                    "summary_style": style,
                    "content": summary,
                    "embeddings_file": "summarizer_embeddings.txt"
                })
        else:
            st.error("⚠️ Please upload a file first.")

# ========================= Q&A OVER DOCUMENTS =========================
elif section == "Q&A":
    st.header("🤖 Ask Questions about Uploaded Document")

    uploaded_file = st.file_uploader("Upload a TXT or PDF file to enable Q&A", type=["txt", "pdf"], key="qa_file")

    if uploaded_file is not None:
        if st.button("Process Document", key="process_doc"):
            with st.spinner("Storing embeddings in Chroma..."):
                store_embeddings(uploaded_file)
                st.success("✅ Document processed! You can now ask questions.")

        question = st.text_input("Ask a question about the document:", key="qa_question")
        if st.button("Get Answer", key="get_answer"):
            if question.strip():
                with st.spinner("Retrieving answer..."):
                    answer = answer_question(question)
                    st.success("✅ Answer generated:")
                    st.write(answer)
            else:
                st.error("⚠️ Please enter a question.")

# ========================= HISTORY =========================
elif section == "History":
    st.header("📜 History of Generated Content")

    history_type = st.selectbox("Select type:", ["Blogs", "Summaries"])

    if history_type == "Blogs":
        blogs = load_history("blogs.json")
        for blog in reversed(blogs):
            st.subheader(f"{blog['topic']} ({blog['tone']}) - {blog['timestamp']}")
            st.write(blog['content'])
    elif history_type == "Summaries":
        summaries = load_history("summaries.json")
        for summary in reversed(summaries):
            st.subheader(f"{summary['file_name']} ({summary['summary_style']}) - {summary['timestamp']}")
            st.write(summary['content'])
            st.info(f"Embeddings stored in: {summary['embeddings_file']}")
