import os
from worker.transcript.youtube import download_audio
from worker.transcript.whisper_transcriber import transcribe_audio
from worker.llm.openai_client import generate_summary
from worker.jira.jira_client import create_jira_ticket
import json

def process_job(payload: dict):
    source_url = payload["source_url"]
    source_type = payload["type"]

    print("🎧 Downloading audio...")
    audio_path = download_audio(source_url)

    print("🧠 Transcribing with Whisper...")
    transcript = transcribe_audio(audio_path)

    print("🧹 Cleaning transcript...")
    transcript = transcript.strip()

    print("🤖 Generating AI summary...")
    llm_output = generate_summary(transcript)

    try:
        result = json.loads(llm_output)
        
        jira_issues = []
        
        print("📌 Creating Jira tickets...")
        for item in result.get("action_items", []):
            issue = create_jira_ticket(
                title=item["title"],
                description=item["description"],
                priority=item.get("priority", "Medium")
            )

            jira_issues.append({
                "key": issue["key"],
                "url": f"{os.getenv('JIRA_BASE_URL')}/browse/{issue['key']}"
            })

        return {
            "summary": result["summary"],
            "decisions": result.get("decisions", []),
            "action_items": result["action_items"],
            "jira_tickets": jira_issues
        }

        
    except:
        result = {
            "summary": llm_output,
            "decisions": [],
            "action_items": [],
            "jira_tickets": []
        }

    return {
        "transcript": transcript,
        **result
    }
