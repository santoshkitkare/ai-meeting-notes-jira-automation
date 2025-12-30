# 🔧 Backend – AI Meeting Processor

This service handles:
- Job creation
- Audio processing
- AI summarization
- Jira integration
- Job history persistence

## 📦 Tech Stack

- FastAPI
- SQLite
- AWS SQS
- OpenAI / Whisper
- Jira REST API


## 🗂️ Folder Structure
```
backend/
├── app/
│ ├── main.py
│ ├── routes.py
│ ├── models.py
│ ├── db.py
│ ├── sqs_client.py
│ ├── config.py
├── worker/
│ ├── processor.py
│ ├── transcript/
│ ├── llm/
│ ├── jira/
├── README.md
```

## ▶️ Run Backend

```bash
uvicorn app.main:app --reload
```
## ⚙️ Environment Variables
### Create .env file:
```
OPENAI_API_KEY=your_key
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=you@example.com
JIRA_API_TOKEN=your_token
AWS_REGION=ap-south-1
SQS_QUEUE_URL=https://sqs...
```

## 🔄 API Endpoints
### Create Job
- POST /jobs

Get Job Status
- GET /jobs/{job_id}

Create Jira Tickets
- POST /jobs/{job_id}/jira

## ⚙️ Worker
### Start worker separately:
```
python -m worker.worker
```

### Worker handles:
- Audio extraction
- Transcription
- LLM summarization
- Status updates

## 🧠 Design Notes
- Async job handling
- Decoupled processing
- No blocking API calls
- Production-aligned architecture