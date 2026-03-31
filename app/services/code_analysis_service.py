import json
from app.services.ai_service import AIService
from app.exceptions import InvalidAIResponseError

ANALYZE_PROMPT = """
You are a senior software engineer and Clean Code expert.
Analyze the following Python code according to Clean Code principles.

Focus on:
- meaningful naming
- small functions
- single responsibility principle
- readability
- avoiding duplication
- maintainability

Return ONLY a JSON object, no extra text:

{{
    "score": <number from 1 to 10>,
    "issues": [
        {{
            "line": <line number>,
            "problem": "<description>",
            "suggestion": "<how to fix>"
        }}
    ]
}}

Respond in Polish language.

Code to analyze:
{code}
"""

REVIEW_PROMPT = """
You are a Clean Code expert.
The user has received feedback on their code and wrote their own improved version.

Evaluate the user's fix compared to the original code.
Then show the best possible solution and explain why it is better.

Return ONLY a JSON object, no extra text:

{{
    "score": <number from 1 to 10>,
    "feedback": "<did the user fix the issues correctly? what did they do well or wrong?>",
    "comparison": "<explain differences between original and user fix>",
    "best_solution": "<the best possible clean code version>",
    "best_solution_explanation": "<why this solution is the best>"
}}

Respond in Polish language.

Original code:
{original_code}

User's improved version:
{user_fix}
"""


class CodeAnalysisService:

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def analyze_code(self, code: str) -> dict:
        prompt = ANALYZE_PROMPT.format(code=code)
        response = await self.ai_service.complete(prompt)
        return self._parse_response(response)

    async def review_user_fix(self, original_code: str, user_fix: str) -> dict:
        prompt = REVIEW_PROMPT.format(
            original_code=original_code,
            user_fix=user_fix
        )
        response = await self.ai_service.complete(prompt)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> dict:
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise InvalidAIResponseError(
                f"AI returned invalid JSON: {response[:100]}"
            )