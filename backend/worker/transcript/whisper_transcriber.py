import whisper

model = whisper.load_model("base")  # small | medium | large later

def transcribe_audio(audio_path: str) -> str:
    result = model.transcribe(audio_path)
    return result["text"]
