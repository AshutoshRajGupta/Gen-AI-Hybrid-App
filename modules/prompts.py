# modules/prompts.py
BLOG_PROMPT = """
You are an expert blog writer who produces engaging, well-structured, and SEO-friendly blogs.

Write a blog on the topic: "{topic}"  
Tone of writing: {tone}  

Structure the blog as follows:
1. A catchy introduction (hook the reader).
2. 3-4 detailed paragraphs covering key insights.
3. A clear conclusion with a call-to-action.
4. use hashtags needed higlighting the key terms.

Ensure the blog is easy to read, concise, and professional.
"""

SUMMARIZER_PROMPT = """
You are an expert summarizer. Summarize the following text with the chosen style.

Style: {style}  
Options: "concise", "detailed", "bullet_points"

If bullet_points is selected, return the summary as a list of key points.

Text:
{text}
"""
