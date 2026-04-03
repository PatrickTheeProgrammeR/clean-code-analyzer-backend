from openai import AsyncOpenAI
from app.providers.base import AIProvider
from app.exceptions import AIProviderError


class OpenAIProvider(AIProvider):

    def __init__(self, api_key: str):
        api_key = (api_key or "").strip()
        if not api_key:
            raise AIProviderError("Brak klucza OpenAI API.")
        self.client = AsyncOpenAI(api_key=api_key)

    async def complete(self, prompt: str, *, json_response: bool = False) -> str:
        try:
            kwargs = {
                "model": "gpt-4.1-mini",
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt}
                        ]
                    }
                ]
            }

            if json_response:
                kwargs["text"] = {"format": {"type": "json_object"}}

            response = await self.client.responses.create(**kwargs)

            if not response.output:
                raise AIProviderError("Empty response from OpenAI")

            return response.output_text

        except AIProviderError:
            raise
        except Exception as e:
            raise AIProviderError(f"OpenAI request failed: {str(e)}") from e