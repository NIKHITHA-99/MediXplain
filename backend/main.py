from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import io
import base64
from pypdf import PdfReader
from groq import Groq
from rag import create_rag_chain

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://medi-xplain-wine.vercel.app",
        "http://localhost:3000",
        "http://localhost:3008",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
rag_chain = create_rag_chain()

def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join(p.extract_text() or "" for p in reader.pages)

@app.get("/")
def root():
    return {"message": "MediXplain RAG API is running!"}

@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()

        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
            if not text.strip():
                return {"error": "Could not extract text from PDF"}
            result = rag_chain.invoke(text)
            return {"explanation": result}

        else:
            # Images — use Groq Vision
            image_data = base64.b64encode(file_bytes).decode("utf-8")
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            },
                            {
                                "type": "text",
                                "text": """You are a friendly medical assistant.
Extract all medical values from this image.
Explain each value in simple English.
Say NORMAL ✅ HIGH 🔴 or LOW 🟡 for each value.
Suggest questions to ask the doctor.
Be friendly and reassuring."""
                            }
                        ]
                    }
                ]
            )
            return {"explanation": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}
