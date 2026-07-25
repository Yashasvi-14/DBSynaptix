from google import genai

from app.config import GEMINI_API_KEY


class AIProvider:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_embedding(self, text):

        response = self.client.models.embed_content(
            model="gemini-embedding-2",
            contents=text
        )

        return response.embeddings[0].values
    
    def generate_text(
        self,
        prompt: str
    ) -> str:

        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text

    def generate_text_with_metadata(
        self,
        prompt: str
    ):
        return self.client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        