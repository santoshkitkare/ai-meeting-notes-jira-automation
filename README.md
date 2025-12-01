# AI Meeting Notes → Jira Automation (Transcript → Tickets)

### 🚀 Overview
Automates meeting documentation and project management by turning meeting transcripts into structured summaries and Jira tickets.

### 💡 Key Features
- Upload audio/video transcripts or paste meeting notes
- Auto-generate agenda + summary + action items
- Create Jira tickets automatically through API
- Email structured meeting report to stakeholders

### 🧠 Tech Stack
| Layer | Technology |
|-------|------------|
| Backend | FastAPI |
| LLM | GPT / Claude |
| Integrations | Jira API |
| Deployment | AWS + Docker |

### 🏗 Architecture
Transcript Input → FastAPI → GPT/Claude
      ↓
Action Item Extractor + Jira API
      ↓
AWS Deployment

### 📂 Project Structure
```
ai-meeting-notes-jira-automation/
┣ app/
┃ ┣ routers/
┃ ┣ services/
┃ ┣ utils/
┃ ┗ main.py
┣ data/
┣ Dockerfile
┣ requirements.txt
┗ README.md
```

### 📌 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload-transcript/` | Upload meeting transcript |
| POST | `/generate-report/` | Generate structured summary |
| POST | `/create-jira-tickets/` | Auto-create Jira issues |

### 🚀 Deployment
```
docker build -t meeting-jira-automation .
docker run -p 8000:8000 meeting-jira-automation
```

---

### 🤝 Ideal Use Cases
- Agile teams
- PMO departments
- SaaS product teams
- Consulting companies

### 📩 Contact
For integration with Slack/Teams, Airtable, or Trello — happy to discuss.
