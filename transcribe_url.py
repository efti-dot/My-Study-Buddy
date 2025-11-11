import yt_dlp
import openai
import tempfile
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# Load OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def download_youtube_audio(url, output_dir):
    """
    Download audio in .m4a format directly from YouTube using yt-dlp.
    Avoids postprocessing to eliminate ffmpeg dependency.
    """
    output_path = Path(output_dir) / "audio.m4a"

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': str(output_path),
        'quiet': True,
        'noplaylist': True,
        'extractor_args': {
            'youtube': [
                'player_client=android',
                'skip_sabr_check=True'
            ]
        },
        'postprocessors': []
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path if output_path.exists() else None
    except Exception as e:
        print(f"YouTube download error: {e}")
        return None


def download_direct_file(url, output_path):
    """
    Downloads a direct media file (e.g. MP3, MP4) from a URL.
    """
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return output_path
    except Exception as e:
        print(f"Direct download error: {e}")
        return None


def transcribe_audio(audio_path):
    """
    Transcribes an audio file using OpenAI Whisper (whisper-1).
    """
    try:
        with open(audio_path, "rb") as f:
            response = openai.Audio.transcribe("whisper-1", f)
        return response.text.strip()
    except Exception as e:
        print(f"Whisper transcription error: {e}")
        return None


def main():
    url = input("🎧 Enter YouTube or direct media URL: ").strip()

    with tempfile.TemporaryDirectory() as tmpdir:
        if "youtube.com" in url or "youtu.be" in url:
            audio_path = download_youtube_audio(url, tmpdir)
        else:
            audio_path = download_direct_file(url, Path(tmpdir) / "downloaded_file.m4a")

        if not audio_path or not Path(audio_path).exists():
            print("Failed to download or locate audio file.")
            return

        print("Media downloaded. Transcribing...")
        transcript = transcribe_audio(audio_path)

        if transcript:
            print("\nTranscribed Text:\n")
            print(transcript)
        else:
            print("Transcription failed.")


if __name__ == "__main__":
    main()
