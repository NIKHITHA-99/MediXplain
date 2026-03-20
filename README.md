# 🏥 MediXplain - Your Medical Reports, Simply Explained

MediXplain is a full-stack AI-powered web application that helps patients understand their medical reports in simple, friendly English. Simply upload your blood test, lab report, or medical image and get an instant, easy-to-understand explanation powered by LLaMA 3 and LangChain RAG.

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| 🖥️ Frontend | https://medi-xplain-wine.vercel.app |
| ⚙️ Backend API | https://medixplain.onrender.com |
| 📖 API Docs | https://medixplain.onrender.com/docs |

---

## ✨ Features

- 📄 **PDF & Image Support** — Upload blood tests, lab reports, X-rays, and more
- 🤖 **AI-Powered Explanations** — Powered by Groq's LLaMA 3 model
- ✅ **Status Indicators** — NORMAL ✅, HIGH 🔴, LOW 🟡 for each value
- 💬 **Doctor Questions** — Suggests 3-5 questions to ask your doctor
- 🧠 **RAG System** — Uses medical knowledge base for accurate explanations
- 🤝 **Friendly Tone** — Reassuring and easy to understand
- 📱 **Responsive Design** — Works on mobile and desktop

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| React 19 | UI Framework |
| Axios | API calls |
| React Dropzone | File upload |
| React Markdown | Render explanations |
| jsPDF | Export reports |

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | REST API |
| Groq LLaMA 3 | AI explanations |
| LangChain | RAG pipeline |
| ChromaDB | Vector store |
| PyPDF | PDF parsing |
| FakeEmbeddings | Text embeddings |

### Deployment
| Service | Platform |
|---------|---------|
| Frontend | Vercel |
| Backend | Render |
| Code | GitHub |

---

## 📁 Project Structure
```
MediXplain/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag.py               # RAG chain with medical knowledge
│   ├── requirements.txt     # Python dependencies
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   ├── index.js         # Entry point
│   │   └── index.css
│   ├── package.json
│   └── .gitignore
└── README.md
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API Key from [console.groq.com](https://console.groq.com)

### Backend Setup
```bash
# Clone the repo
git clone https://github.com/NIKHITHA-99/MediXplain.git
cd MediXplain/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# Run backend
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`
API Docs at: `http://localhost:8000/docs`

### Frontend Setup
```bash
cd MediXplain/frontend

# Install dependencies
npm install

# Run frontend
npm start
```

Frontend runs at: `http://localhost:3000`

---

## 🧠 How It Works
```
User uploads report
        ↓
FastAPI receives file
        ↓
PDF → extract text | Image → Groq Vision
        ↓
LangChain RAG retrieves medical knowledge
        ↓
LLaMA 3 generates simple explanation
        ↓
User sees NORMAL/HIGH/LOW with explanation
```

---

## 📊 Supported Medical Tests

- 🩸 Hemoglobin & Blood Count
- 🍬 Blood Sugar (Glucose)
- ❤️ Cholesterol (LDL, HDL)
- 🦠 White Blood Cells (WBC)
- 🩸 Platelets
- 🫘 Creatinine (Kidney)
- 🦋 Thyroid (TSH)
- ☀️ Vitamin D
- 💊 Vitamin B12
- 🦴 Uric Acid
- 🫁 Bilirubin
- 🫀 SGPT/ALT & SGOT/AST (Liver)

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key |

---

## 🚀 Deployment

### Deploy Backend (Render)
1. Connect GitHub repo to Render
2. Set Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add `GROQ_API_KEY` environment variable

### Deploy Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set Root Directory: `frontend`
3. Click Deploy

---

## ⚠️ Disclaimer

MediXplain is for **educational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

---

## 👩‍💻 Author

**NIKHITHA-99**
- GitHub: [@NIKHITHA-99](https://github.com/NIKHITHA-99)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ If you found this helpful, please star the repo!   Always consult your doctor for medical advice.
