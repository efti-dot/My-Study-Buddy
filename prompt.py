import openai

class OpenAIConfig:
    def __init__(self, api_key: str = "api-key", model: str = "gpt-4o-mini"):
        """
        Initializes the OpenAI API configuration with the given API key and model.
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key