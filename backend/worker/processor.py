import os
from worker.transcript.youtube import download_audio
from worker.transcript.whisper_transcriber import transcribe_audio
from worker.llm.openai_client import generate_summary
from worker.jira.jira_client import create_jira_ticket
import json

def process_job(payload: dict):
    source_url = payload["source_url"]

    print("🎧 Downloading audio...")
    audio_path = download_audio(source_url)

    print("🧠 Transcribing...")
    transcript = transcribe_audio(audio_path).strip()

    print("🤖 Generating AI summary...")
    llm_output = generate_summary(transcript)

    try:
        result = json.loads(llm_output)
    except Exception:
        result = {
            "summary": llm_output,
            "decisions": [],
            "action_items": []
        }

    # ❗ NO JIRA CREATION HERE ❗
    return {
        "transcript": transcript,
        "summary": result.get("summary"),
        "decisions": result.get("decisions", []),
        "action_items": result.get("action_items", [])
    }