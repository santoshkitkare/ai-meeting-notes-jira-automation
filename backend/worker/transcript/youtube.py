import yt_dlp
import os

def download_youtube_audio(url: str, output_dir="temp"):
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "%(id)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        audio_path = filename.replace(".webm", ".wav").replace(".m4a", ".wav")

    return audio_path