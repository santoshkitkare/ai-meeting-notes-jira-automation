from worker.transcript.youtube import download_audio
from worker.transcript.whisper_transcriber import transcribe_audio
from worker.llm.openai_client import generate_summary
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
    except:
        result = {
            "summary": llm_output,
            "decisions": [],
            "action_items": []
        }

    return {
        "transcript": transcript,
        **result
    }
