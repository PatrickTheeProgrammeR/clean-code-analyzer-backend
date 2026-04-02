import os
import sys
from openai import AsyncOpenAI
from app.providers.base import AIProvider
from app.exceptions import AIProviderError


class OpenAIProvider(AIProvider):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            if sys.stdin.isatty():
                while True:
                    api_key = input("Podaj OPENAI_API_KEY: ").strip()
                    if api_key:
                        break
                    print("Klucz nie może być pusty!")
            else:
                raise AIProviderError("OPENAI_API_KEY is not set")
        self.client = AsyncOpenAI(api_key=api_key)

    async def complete(self, prompt: str, *, json_response: bool = False) -> str:
        try:
            kwargs = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
            }
            if json_response:
                kwargs["response_format"] = {"type": "json_object"}
            response = await self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            raise AIProviderError(f"OpenAI request failed: {str(e)}")
