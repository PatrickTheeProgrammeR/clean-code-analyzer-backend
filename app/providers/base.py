from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    async def complete(self, prompt: str, *, json_response: bool = False) -> str:
        """Send prompt to AI and return response as string."""
        pass