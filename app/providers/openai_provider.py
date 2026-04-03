import os
import sys
from openai import AsyncOpenAI
from app.providers.base import AIProvider
from app.exceptions import AIProviderError


class OpenAIProvider(AIProvider):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            if sys.stdin.isatty():  # terminal
                api_key = input("Podaj OPENAI_API_KEY: (https://platform.openai.com/api-keys) ").strip()
            else:
                raise AIProviderError("OPENAI_API_KEY is not set")
        self.client = AsyncOpenAI(api_key=api_key)

    async def complete(self, prompt: str, *, json_response: bool = False) -> str:
        try:
            kwargs = {
                "model": "gpt-4o-mini",
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt}
                        ]
                    }
                ],
            }
            if json_response:
                kwargs["text"] = {"format": {"type": "json_object"}}
            response = await self.client.responses.create(**kwargs)
            return response.output_text
        except Exception as e:
            raise AIProviderError(f"OpenAI request failed: {str(e)}") from e
