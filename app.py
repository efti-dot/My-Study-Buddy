import streamlit as st
import ffmpeg
import openai
import tempfile
import os


api_key = "api_key"
openai.api_key = api_key

def extract_audio_from_video(uploaded_file):
    """
    Extracts audio from the uploaded video file and saves it as a temporary MP3 file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        temp_video_path = temp_video.name

    audio_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_temp_path = audio_temp.name

    ffmpeg.input(temp_video_path).output(audio_temp_path).run()

    os.remove(temp_video_path)

    return audio_temp_path

def transcribe_audio_to_text(audio_file_path):
    """
    Transcribes audio to text using OpenAI's Whisper model.
    """
    with open(audio_file_path, "rb") as audio_file:
        response = openai.Audio.transcribe(model="whisper-1", file=audio_file)

    return response["text"]

def main():
    st.title("VTT - Video to Text")
    st.write("This is a simple Video to Text generation application.")
    st.write("Upload your video file below:")

    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        st.write("File uploaded successfully!")

        
        audio_file_path = extract_audio_from_video(uploaded_file)
        st.write("Audio extracted successfully!")

        
        transcribed_text = transcribe_audio_to_text(audio_file_path)
        st.text_area("Transcribed Text", transcribed_text, height=400)

if __name__ == "__main__":
    main()
