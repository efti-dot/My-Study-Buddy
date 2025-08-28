import openai
import ffmpeg
import openai
import tempfile
import os

class OpenAIConfig:
    def __init__(self, api_key: str = "api", model: str = "gpt-4o-mini"):
        """
        Initializes the OpenAI API configuration with the given API key and model.
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
        self.conversation_history = [{"role": "system", "content": "You are a helpful study guide assistant. Provide concise and accurate information."}]

    def get_response(self, prompt: str, history: list) -> str:
        """
        Sends a prompt to the OpenAI API and returns the response text.
        Maintains conversation history for context.
        """
        history.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=history
        )

        reply = response.choices[0].message['content']
        history.append({"role": "assistant", "content": reply})
        return reply
    

    def get_history(self):
        return self.conversation_history
    
    
    #####ViTT&VoTT
    def transcribe_audio_to_text(uploaded_file) -> str:
        """
        Transcribes audio or video file directly using OpenAI's Whisper model.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as file:
            response = openai.Audio.transcribe(model="whisper-1", file=file)

        os.remove(temp_file_path)
        return response["text"]
    
    
    
    #mcqs
    def generate_mcqs_from_text(self, text: str, num_questions) -> str:
        """
        Generates MCQs with answers and reasoning from the given text using OpenAI.
        """
        prompt = f"""
        Based on the following study material, generate {num_questions} multiple-choice questions.
        Each question should include:
        - The question itself
        - Four answer options labeled A to D
        - The correct answer
        - A brief reasoning for the correct answer

        Study Material:
        \"\"\"{text}\"\"\"
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates educational quizzes."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message["content"]
    

    