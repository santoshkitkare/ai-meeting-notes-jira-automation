# 🎨 Frontend – AI Meeting Dashboard

## Streamlit-based UI for:
- Submitting meetings
- Viewing summaries
- Selecting action items
- Creating Jira tickets
- Viewing job history

## ▶️ Run Frontend

```bash
streamlit run app.py
```

## 🧩 Features
    ✔ Upload meeting link
    ✔ Select source (YouTube / Zoom / Meet)
    ✔ View AI-generated summary
    ✔ Select action items
    ✔ Create Jira tickets
    ✔ View job history

## 🖥️ UI Sections
### 1. Meeting Input
- URL input
- Source selection

### 2. AI Output
- Summary
- Action items table
- Priority + owner

### 3. Jira Integration
- Checkbox-based selection
- Ticket creation
- Jira links

### 4. Job History
- Past jobs
- Status
- Jira references

## 🧠 Notes
- Uses session_state for persistence
- Async-safe UI
- Optimized for demo & scalability

## 📌 Future Enhancements
- File upload
- Auth support
- Role-based access
- Analytics dashboard