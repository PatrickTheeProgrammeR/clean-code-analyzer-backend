import json
import re
from app.services.ai_service import AIService
from app.exceptions import InvalidAIResponseError

ANALYZE_PROMPT = """
Jesteś seniorem Pythona i ekspertem Clean Code. Przeanalizuj poniższy kod pod kątem:
czytelności, nazewnictwa, małych funkcji, SRP, braku duplikacji, utrzymywalności.

Zwróć WYŁĄCZNIE jeden obiekt JSON (bez markdown, bez ```), w dokładnie tej strukturze:

{{
  "score": <liczba całkowita 1–10>,
  "summary": "<2–3 zdania po polsku: najważniejsza wskazówka ZANIM użytkownik zacznie poprawiać kod — co poprawić w pierwszej kolejności>",
  "issues": [
    {{
      "line": <numer linii w kodzie użytkownika, lub 0 jeśli uwaga dotyczy całości pliku>,
      "problem": "<konkretny problem po polsku>",
      "suggestion": "<konkretna sugestia jak poprawić, po polsku>"
    }}
  ]
}}

Zasady obowiązkowe:
- Jeśli "score" jest mniejsze niż 10, tablica "issues" MUSI mieć co najmniej 2 elementy, każdy z wypełnionymi polami problem i suggestion.
- Jeśli "score" to 10, "issues" może być pustą tablicą [].
- Nie zwracaj pustej tablicy "issues" przy ocenie poniżej 10.

Kod do analizy:
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


def _strip_json_fence(text: str) -> str:
    t = text.strip()
    if not t.startswith("```"):
        return t
    lines = t.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _parse_json_object(text: str) -> dict:
    raw = _strip_json_fence(text)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{[\s\S]*\}", raw)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    raise InvalidAIResponseError(f"AI returned invalid JSON: {raw[:200]}")


def _coerce_int_score(value) -> int:
    try:
        n = int(float(value))
    except (TypeError, ValueError):
        return 5
    return max(1, min(10, n))


def _normalize_issue_item(raw: dict) -> dict:
    line = raw.get("line", raw.get("linia"))
    try:
        line = int(line) if line is not None else 0
    except (TypeError, ValueError):
        line = 0
    problem = (
        raw.get("problem")
        or raw.get("opis")
        or raw.get("Problem")
        or ""
    )
    suggestion = (
        raw.get("suggestion")
        or raw.get("sugestia")
        or raw.get("Sugestia")
        or raw.get("jak_naprawic")
        or ""
    )
    return {
        "line": line,
        "problem": str(problem).strip() or "—",
        "suggestion": str(suggestion).strip() or "—",
    }


def _parse_analyze_response(response: str) -> dict:
    data = _parse_json_object(response)
    score = _coerce_int_score(data.get("score"))
    summary = (
        data.get("summary")
        or data.get("podsumowanie")
        or data.get("wskazowka")
        or ""
    )
    if isinstance(summary, str):
        summary = summary.strip()
    else:
        summary = ""

    issues_raw = data.get("issues") or data.get("problemy") or []
    if not isinstance(issues_raw, list):
        issues_raw = []
    issues = []
    for item in issues_raw:
        if isinstance(item, dict):
            issues.append(_normalize_issue_item(item))

    if score < 10 and len(issues) < 2:
        issues = [
            {
                "line": 0,
                "problem": "Odpowiedź modelu była niekompletna. Uruchom analizę ponownie lub skróć fragment kodu.",
                "suggestion": "Spróbuj ponownie przyciskiem „Analizuj kod”. Jeśli problem wraca, wklej mniejszy fragment pliku.",
            },
            {
                "line": 0,
                "problem": "Przy ocenie poniżej 10/10 oczekiwana jest lista konkretnych uwag (linia, problem, sugestia).",
                "suggestion": "Powtórz analizę — model powinien wypisać szczegółowe punkty do poprawy.",
            },
        ]

    return {"score": score, "summary": summary, "issues": issues}


class CodeAnalysisService:

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def analyze_code(self, code: str) -> dict:
        prompt = ANALYZE_PROMPT.format(code=code)
        response = await self.ai_service.complete(prompt, json_response=True)
        return _parse_analyze_response(response)

    async def review_user_fix(self, original_code: str, user_fix: str) -> dict:
        prompt = REVIEW_PROMPT.format(
            original_code=original_code,
            user_fix=user_fix
        )
        response = await self.ai_service.complete(prompt, json_response=True)
        return self._parse_review_response(response)

    def _parse_review_response(self, response: str) -> dict:
        return _parse_json_object(response)
