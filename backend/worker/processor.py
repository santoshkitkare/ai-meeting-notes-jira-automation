import os
from worker.transcript.youtube import download_youtube_audio
from worker.transcript.zoom import download_zoom_audio
from worker.transcript.whisper_transcriber import transcribe_audio
from worker.llm.openai_client import generate_summary
from worker.notifier import notify_progress
import json

def process_job(payload: dict):
    source_url = payload["source_url"]

    notify_progress(payload["job_id"], "PROCESSING", 10, "Fetching transcript")
    print("🎧 Downloading audio...")
    source_type = payload["type"]

    if source_type == "youtube":
        audio_path = download_youtube_audio(source_url)
    elif source_type == "zoom":
        audio_path = download_zoom_audio(source_url)
    else:
        raise ValueError("Unsupported source type")

    print("🧠 Transcribing...")
    transcript = transcribe_audio(audio_path).strip()
    notify_progress(payload["job_id"], "PROCESSING", 40, "Transcript processed")

    print("🤖 Generating AI summary...")
    llm_output = generate_summary(transcript)
    notify_progress(payload["job_id"], "PROCESSING", 70, "Summary generated")

    try:
        result = json.loads(llm_output)
        notify_progress(payload["job_id"], 90, "Action items ready")
    except Exception:
        result = {
            "summary": llm_output,
            "decisions": [],
            "action_items": []
        }

    notify_progress(payload["job_id"], "COMPLETED",100, "Completed")
    # ❗ NO JIRA CREATION HERE ❗
    return {
        "transcript": transcript,
        "summary": result.get("summary"),
        "decisions": result.get("decisions", []),
        "action_items": result.get("action_items", [])
    }