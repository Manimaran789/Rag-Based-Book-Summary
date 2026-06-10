import google.generativeai as genai
import os

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not set")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-2.0-flash-lite")


def generate_answer(query, context):
    if not context:
        return "⚠️ No relevant content retrieved. Upload document properly."

    context_text = "\n\n".join(context[:3])

    prompt = f"""
    Answer ONLY from the context below.

    Context:
    {context_text}

    Question:
    {query}

    Give a clear, factual answer.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Generation error: {str(e)}"