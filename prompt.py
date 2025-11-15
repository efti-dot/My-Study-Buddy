import openai
import openai
import tempfile
import os
from pathlib import Path
import yt_dlp
import requests
from pydub import AudioSegment
import json


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
        Transcribes audio or video files using OpenAI Whisper.
        No ffmpeg used. Automatically handles supported formats like .mp3, .mp4, .m4a, .webm.
        """
        CHUNK_LENGTH_MS = 60 * 1000  # 60 seconds per chunk

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / uploaded_file.name
            with open(input_path, "wb") as f:
                f.write(uploaded_file.read())

            # Load audio using pydub (auto handles .mp3, .mp4, .m4a, .webm if ffmpeg is installed)
            try:
                audio = AudioSegment.from_file(input_path)
            except Exception as e:
                print("Failed to load audio:", e)
                return "Unsupported or unreadable audio format."

            chunks = [audio[i:i + CHUNK_LENGTH_MS] for i in range(0, len(audio), CHUNK_LENGTH_MS)]
            full_transcript = []

            for i, chunk in enumerate(chunks):
                chunk_path = Path(tmpdir) / f"chunk_{i}.mp3"
                chunk.export(chunk_path, format="mp3")

                try:
                    with open(chunk_path, "rb") as f:
                        result = openai.Audio.transcribe("whisper-1", file=f)
                        full_transcript.append(result["text"].strip())
                except Exception as e:
                    print(f"Transcription error on chunk {i}:", e)
                    full_transcript.append("[Untranscribed segment]")

            full_transcription = " ".join(full_transcript).replace("\n", " ").strip()

            return json.dumps({
                "transcription": full_transcription
            }, ensure_ascii=False, indent=2)

        
    def transcribe_from_url(url: str) -> str:
        """
        Downloads audio from a YouTube URL and returns transcribed text as JSON.
        """
        if not ("youtube.com" in url or "youtu.be" in url):
            return "error: Only YouTube URLs are supported."

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "media.m4a"
            downloaded = OpenAIConfig.download_youtube_audio(url, output_path)

            if not downloaded or not Path(output_path).exists():
                return "error: Failed to download media from the YouTube URL."

            with open(output_path, "rb") as f:
                class DummyFile:
                    def __init__(self, name, data):
                        self.name = name
                        self.data = data
                    def read(self):
                        return self.data

                dummy_file = DummyFile("youtube_audio.m4a", f.read())
                transcript = OpenAIConfig.transcribe_audio_to_text(dummy_file)

            cleaned_transcript = transcript.replace("\n", " ").strip()

            return json.dumps({
                "transcription": cleaned_transcript
            }, ensure_ascii=False, indent=2)

    
    
    def download_youtube_audio(url, output_path):
        """
        Downloads YouTube audio in .m4a format without using ffmpeg.
        """
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
            'postprocessors': [
                
            ]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print(f"Output patyh is here:::::: {output_path}")
            return output_path if Path(output_path).exists() else None
        except Exception as e:
            print(f"YouTube download error: {e}")
            return None

        
    
    #mcqs
    def generate_mcqs_from_text(self, text: str, num_questions, additional_instructions: str = None) -> str:
        """
        Generates MCQs with answers and reasoning from the given text using OpenAI.
        Optionally takes additional user instructions to refine the output.
        """

        word_count = len(text.split())
        min_words_required = num_questions * 20

        if word_count < min_words_required:
            return (
                f"The provided text has only {word_count} words, which is too short to generate {num_questions} MCQs reliably.\n"
                f"Please provide more content or reduce the number of questions to {word_count // 20} or fewer."
            )

        base_prompt = f"""
        Based on the following study material, generate {num_questions} multiple-choice questions.
        Each question should include:
        - The question itself
        - Four answer options labeled A to D
        - The correct answer
        - A brief reasoning for the correct answer

        IMPORTANT: You must respond ONLY with valid JSON. Do not include any text before or after the JSON.
        Generate a JSON response with this exact structure:
        [
        {{
            "question_text": "<question>",
            "correct_answer": "<correct_answer>",
            "reasoning": "<reasoning>",
            "options": [
                {{"key": "A", "text": "<option_a>"}},
                {{"key": "B", "text": "<option_b>"}},
                {{"key": "C", "text": "<option_c>"}},
                {{"key": "D", "text": "<option_d>"}}
            ]
        }},
        ...
        ]
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

    
    #True/False
    def generate_true_false_from_text(self, text: str, num_questions, additional_instructions: str = None) -> str:
        """
        Generates True/False questions with answers and reasoning from the given text using OpenAI.
        Optionally takes additional user instructions to refine the output.
        """

        word_count = len(text.split())
        min_words_required = num_questions * 10

        if word_count < min_words_required:
            return (
                f"The provided text has only {word_count} words, which is too short to generate {num_questions} True/False questions reliably.\n"
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
    

    #Matching Questions
    def generate_matching_questions_from_text(self, text: str, num_questions, additional_instructions: str = None) -> str:
        """
        Generates Matching questions with answers and reasoning from the given text using OpenAI.
        Optionally takes additional user instructions to refine the output.
        """

        word_count = len(text.split())
        min_words_required = num_questions * 15

        if word_count < min_words_required:
            return (
                f"The provided text has only {word_count} words, which is too short to generate {num_questions} Matching questions reliably.\n"
                f"Please provide more content or reduce the number of questions to {word_count // 15} or fewer."
            )

        base_prompt = f"""
        Based on the whole following study material, generate Matching questions.
        Each question should include:
        - A list of {num_questions} items on the left (left-side options)
        - A shuffled list of {num_questions} items on the right (right-side options)
        - The correct matches (with left-side item matched to right-side item)
        - A brief reasoning for the correct matches
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
                {"role": "system", "content": "You are a helpful assistant that creates educational matching quizzes."},
                {"role": "user", "content": base_prompt}
            ]
        )

        return response.choices[0].message["content"]
    