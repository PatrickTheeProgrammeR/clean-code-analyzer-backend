import os
from openai import AsyncOpenAI
from app.providers.base import AIProvider
from app.exceptions import AIProviderError


class OpenAIProvider(AIProvider):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise AIProviderError("OPENAI_API_KEY is not set")
        self.client = AsyncOpenAI(api_key=api_key)

    async def complete(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise AIProviderError(f"OpenAI request failed: {str(e)}")
