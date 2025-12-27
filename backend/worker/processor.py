from worker.transcript.youtube import download_audio
from worker.transcript.whisper_transcriber import transcribe_audio

def process_job(payload: dict):
    source_url = payload["source_url"]
    source_type = payload["type"]

    print("🎧 Downloading audio...")
    audio_path = download_audio(source_url)

    print("🧠 Transcribing with Whisper...")
    transcript = transcribe_audio(audio_path)

    print("🧹 Cleaning transcript...")
    transcript = transcript.strip()

    # Temporary AI output (next step we replace with GPT)
    result = {
        "transcript": transcript,
        "summary": "Auto-generated summary (placeholder)",
        "action_items": [
            {
                "title": "Review meeting notes",
                "owner": "Team",
                "priority": "Medium"
            }
        ]
    }

    return result
