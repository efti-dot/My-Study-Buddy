import streamlit as st
from prompt import OpenAIConfig


api_key = "api"
openai_config = OpenAIConfig(api_key=api_key)

def naive_bar():
    with st.sidebar:
        st.title("My-Study-Buddy")
        page = st.selectbox("Select an option", ["Talk with AI", "VTT"])
    
    return page

def talk_with_AI():
    st.title("Talk with AI")
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

        response = openai_config.get_response(user_input, st.session_state.messages)
        
        with st.chat_message("assistant"):
            st.markdown(response)


def VTT():
    st.title("VTT - Video to Text")
    st.write("This is a simple Video to Text generation application.")
    st.write("Upload your video file below:")

    
    
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        st.write("File uploaded successfully!")

        
        audio_file_path = OpenAIConfig.extract_audio_from_video(uploaded_file)
        st.write("Audio extracted successfully!")

        
        transcribed_text = OpenAIConfig.transcribe_audio_to_text(audio_file_path)
        st.text_area("Transcribed Text", transcribed_text, height=400)

        
        num_of_mcq = st.selectbox("Select number of MCQs to generate", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=0)
        quiz_btn = st.button("Generate Quiz")

        if quiz_btn and transcribed_text:
            try:
                num = int(num_of_mcq)
                st.subheader(f"Generated {num} MCQs")
                mcqs = openai_config.generate_mcqs_from_text(transcribed_text, num)
                st.markdown(mcqs)
            except ValueError:
                st.error("Please enter a valid number for MCQs.")



def main():
    page = naive_bar()
    
    if page == "Talk with AI":
        talk_with_AI()
    elif page == "VTT":
        VTT()
    


main()
