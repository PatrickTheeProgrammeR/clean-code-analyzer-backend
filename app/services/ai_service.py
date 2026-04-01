from app.providers.base import AIProvider


class AIService:

    def __init__(self, provider: AIProvider):
        self.provider = provider

    async def complete(self, prompt: str, *, json_response: bool = False) -> str:
        return await self.provider.complete(prompt, json_response=json_response)