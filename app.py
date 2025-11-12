import streamlit as st
from prompt import OpenAIConfig
from dotenv import load_dotenv
import os
import tempfile
from pathlib import Path
import yt_dlp


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please check the OPENAI_API_KEY.")

ai = OpenAIConfig(api_key=api_key)

def naive_bar():
    with st.sidebar:
        st.title("My-Study-Buddy")
        page = st.selectbox("Select an option", ["Talk with AI", "ViTT", "VoTT", "Link2Text"])
    
    return page

def talk_with_AI():
    st.title("My Study Buddy")
    st.write("Feel free to ask anything about your study guide!")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("You: ", key="input")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        response = ai.get_response(user_input, st.session_state.messages)
        
        with st.chat_message("assistant"):
            st.markdown(response)


def ViTT():
    st.title("VTT - Video to Text")
    st.write("This is a simple Video to Text generation application.")
    st.write("Upload your video file below:")

    
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "m4a"])

    if uploaded_file is not None:
        file_size = len(uploaded_file.getvalue())
        max_size = 50 * 1024 * 1024  # 50 MB

        if file_size > max_size:
            st.error("File too large! Please upload a video smaller than 50 MB.")
        else:
            st.video(uploaded_file)

        
        transcribed_text = OpenAIConfig.transcribe_audio_to_text(uploaded_file)
        st.text_area("Transcribed Text", transcribed_text, height=400)


        
        num_of_mcq = st.selectbox("Select number of MCQs to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], index=0)
        additional_instructions = st.text_area("Additional Instructions (optional)", height=100)
        quiz_btn = st.button("Generate Quiz")

        if quiz_btn and transcribed_text:
            try:
                num = int(num_of_mcq)
                st.subheader(f"Generated {num} MCQs")

                mcqs = ai.generate_mcqs_from_text(transcribed_text, num, additional_instructions)
                st.markdown(mcqs)
            except ValueError:
                st.error("Please enter a valid number for MCQs.")


        num_of_true_false = st.selectbox("Select number of True/False questions to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=0)
        additional_instructions_tf = st.text_area("Additional Instructions for True/False (optional)", height=100)
        tf_quiz_btn = st.button("Generate True/False Questions")

        if tf_quiz_btn and transcribed_text:
            try:
                num_tf = int(num_of_true_false)
                st.subheader(f"Generated {num_tf} True/False Questions")

                true_false_questions = ai.generate_true_false_from_text(transcribed_text, num_tf, additional_instructions_tf)
                st.markdown(true_false_questions)
            except ValueError:
                st.error("Please enter a valid number for True/False questions.")


        num_of_matching = st.selectbox("Select number of Matching questions to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=0)
        additional_instructions_matching = st.text_area("Additional Instructions for Matching (optional)", height=100)
        matching_quiz_btn = st.button("Generate Matching Questions")

        if matching_quiz_btn and transcribed_text:
            try:
                num_matching = int(num_of_matching)
                st.subheader(f"Generated {num_matching} Matching Questions")

                matching_questions = ai.generate_matching_questions_from_text(transcribed_text, num_matching, additional_instructions_matching)
                st.markdown(matching_questions)
            except ValueError:
                st.error("Please enter a valid number for Matching questions.")


def VoTT():
    st.title("VoTT - Voice to Text")
    st.write("This is a simple Voice to Text generation application.")
    st.write("Upload your audio file below:")

    
    
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

    if uploaded_file is not None:
        st.audio(uploaded_file)
        st.write("File uploaded successfully!")

        
        transcribed_text = OpenAIConfig.transcribe_audio_to_text(uploaded_file)
        st.text_area("Transcribed Text", transcribed_text, height=400)

        
        num_of_mcq = st.selectbox("Select number of MCQs to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], index=0)
        quiz_btn = st.button("Generate Quiz")

        if quiz_btn and transcribed_text:
            try:
                num = int(num_of_mcq)
                st.subheader(f"Generated {num} MCQs")
                mcqs = ai.generate_mcqs_from_text(transcribed_text, num)
                st.markdown(mcqs)
            except ValueError:
                st.error("Please enter a valid number for MCQs.")



def Link2Text():
    st.title("Link2Text - YouTube Transcription (JSON Output)")
    st.write("Paste a YouTube video link below to transcribe its audio:")

    url = st.text_input("Enter YouTube URL here:")

    if url:
        if not ("youtube.com" in url or "youtu.be" in url):
            st.error("Only YouTube URLs are supported.")
            return

        st.write("Processing YouTube URL...")
        with st.spinner("Downloading and transcribing..."):
            try:
                json_output = OpenAIConfig.transcribe_from_url(url)
                st.code(json_output, language="json")
            except Exception as e:
                st.error(f"Error during processing: {e}")



                



def main():
    page = naive_bar()
    
    if page == "Talk with AI":
        talk_with_AI()
    elif page == "ViTT":
        ViTT()
    elif page == "VoTT":
        VoTT()
    elif page == "Link2Text":
        Link2Text()
    


main()