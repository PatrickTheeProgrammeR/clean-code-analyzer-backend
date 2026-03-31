from app.providers.base import AIProvider


class AIService:

    def __init__(self, provider: AIProvider):
        self.provider = provider

    async def complete(self, prompt: str) -> str:
        return await self.provider.complete(prompt)