import openai
import ffmpeg
import openai
import tempfile
import os
from pathlib import Path

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
        Transcribes audio or video files (any size) using Whisper by chunking.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / uploaded_file.name
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            # Step 1: Extract audio from video
            audio_path = Path(tmpdir) / "audio.mp3"
            ffmpeg.input(str(input_path)).output(
                str(audio_path),
                ac=1, ar="16000", format="mp3", loglevel="quiet"
            ).run()

            # Step 2: Split audio into ~20MB chunks
            chunks_dir = Path(tmpdir) / "chunks"
            chunks_dir.mkdir(exist_ok=True)
            chunk_pattern = str(chunks_dir / "chunk_%03d.mp3")

            # Each 600s (~10min) chunk ~20MB depending on bitrate
            ffmpeg.input(str(audio_path)).output(
                chunk_pattern,
                f="segment",
                segment_time=600,  # 10 minutes
                c="copy",
                loglevel="quiet"
            ).run()

            # Step 3: Transcribe each chunk
            transcripts = []
            for chunk_file in sorted(chunks_dir.glob("chunk_*.mp3")):
                with open(chunk_file, "rb") as audio_chunk:
                    response = openai.Audio.transcribe(
                    "whisper-1",
                    file=audio_chunk
                )
                    transcripts.append(response.text.strip())

            # Step 4: Merge results
            full_text = "\n".join(transcripts)
            return full_text
    
    
    
    #mcqs
    def generate_mcqs_from_text(self, text: str, num_questions, additional_instructions: str = None) -> str:
        """
        Generates MCQs with answers and reasoning from the given text using OpenAI.
        Optionally takes additional user instructions to refine the output.
        """

        # Heuristic: Require at least 20 words per MCQ
        word_count = len(text.split())
        min_words_required = num_questions * 20

        if word_count < min_words_required:
            return (
                f"⚠️ The provided text has only {word_count} words, which is too short to generate {num_questions} MCQs reliably.\n"
                f"Please provide more content or reduce the number of questions to {word_count // 20} or fewer."
            )

        base_prompt = f"""
        Based on the following study material, generate {num_questions} multiple-choice questions.
        Each question should include:
        - The question itself
        - Four answer options labeled A to D
        - The correct answer
        - A brief reasoning for the correct answer
        """

        if additional_instructions and additional_instructions.strip():
            base_prompt += f"\n\nFollow these additional instructions carefully:\n{additional_instructions.strip()}"

        base_prompt += f"""
        Study Material:
        \"\"\"{text}\"\"\"
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates educational quizzes."},
                {"role": "user", "content": base_prompt}
            ]
        )

        return response.choices[0].message["content"]

    
    def generate_true_false_from_text(self, text: str, num_questions, additional_instructions: str = None) -> str:
        """
        Generates True/False questions with answers and reasoning from the given text using OpenAI.
        Optionally takes additional user instructions to refine the output.
        """

        # Heuristic: Require at least 10 words per question
        word_count = len(text.split())
        min_words_required = num_questions * 10

        if word_count < min_words_required:
            return (
                f"⚠️ The provided text has only {word_count} words, which is too short to generate {num_questions} True/False questions reliably.\n"
                f"Please provide more content or reduce the number of questions to {word_count // 10} or fewer."
            )

        base_prompt = f"""
        Based on the following study material, generate {num_questions} True/False questions.
        Each question should include:
        - The question itself
        - The correct answer (True or False)
        - A brief reasoning for the correct answer
        """

        if additional_instructions and additional_instructions.strip():
            base_prompt += f"\n\nFollow these additional instructions carefully:\n{additional_instructions.strip()}"

        base_prompt += f"""
        Study Material:
        \"\"\"{text}\"\"\"
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates educational True/False."},
                {"role": "user", "content": base_prompt}
            ]
        )

        return response.choices[0].message["content"]
    