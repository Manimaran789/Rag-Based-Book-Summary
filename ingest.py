from PyPDF2 import PdfReader
import io


def extract_text(file_bytes):
    try:
        pdf = PdfReader(io.BytesIO(file_bytes))
        text = ""

        for page in pdf.pages:
            text += page.extract_text() or ""

        print("📄 Extracted text length:", len(text))
        return text

    except Exception as e:
        print("❌ PDF extraction failed:", str(e))
        return ""


def chunk_text(text, chunk_size=800, overlap=100):
    if not text:
        return []

    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
            chunks = chunks[:150]  # 🔥 LIMIT chunks

    print("📦 Total chunks created:", len(chunks))
    return chunks