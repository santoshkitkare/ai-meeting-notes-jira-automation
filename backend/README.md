# 🔧 Backend – AI Meeting Processor

Handles all backend processing including:
- Job creation
- Audio processing
- AI summarization
- Jira integration

---

## Tech Stack
- FastAPI
- SQLite
- AWS SQS
- OpenAI / Whisper
- Jira REST API

---

## Run Backend
```bash
uvicorn app.main:app --reload
```

---

## Environment Variables
```env
OPENAI_API_KEY=your_key
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=your_token
AWS_REGION=ap-south-1
SQS_QUEUE_URL=your_queue_url
```

---

## API Endpoints

### Create Job
POST /jobs

### Get Job Status
GET /jobs/{job_id}

### Create Jira Tickets
POST /jobs/{job_id}/jira

---

## Worker
```bash
python -m worker.worker
```

Processes:
- Audio extraction
- Transcription
- LLM summary
- Action items
