# 🚀 AI Meeting → Jira Automation System

An end-to-end AI-powered system that converts meeting recordings into structured summaries and actionable Jira tickets using LLMs.

---

## 🧠 Key Features
- 🎥 Supports meeting recordings (YouTube / Zoom / Google Meet)
- 🧾 Automatic transcript generation
- 🤖 AI-powered summary + action item extraction
- ✅ Manual selection of action items
- 🎫 Jira ticket creation
- 📊 Job history tracking
- 🔄 Async background processing

---

## 🏗️ Architecture

Frontend (Streamlit)
        ↓
FastAPI Backend
        ↓
AWS SQS
        ↓
Worker (Whisper + LLM + Jira)

---

## 🚀 Setup Instructions

### 1. Clone Repo
```bash
git clone <repo-url>
cd ai-meeting-notes-jira-automation
```

### 2. Setup Environment
```bash
pip install uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 3. Start Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### 4. Start Worker
```bash
cd backend
python -m worker.worker
```

### 5. Start Frontend
```bash
cd frontend
streamlit run app.py
```

---

## 📌 Notes
- Supports Zoom / YouTube / Google Meet recordings
- Zoom OAuth required for private recordings
- Jira creation is user-controlled

---

## 👨‍💻 Author
Built for learning, experimentation, and real-world architecture practice.
