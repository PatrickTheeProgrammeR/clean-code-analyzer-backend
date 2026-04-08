import re
from urllib.parse import unquote

import httpx

GITHUB_BLOB_OR_TREE = re.compile(
    r"^https?://github\.com/([^/]+)/([^/]+)/(?:blob|tree)/([^/]+)/(.+?)(?:\?.*)?$",
    re.IGNORECASE,
)
GITHUB_RAW = re.compile(
    r"^https?://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+?)(?:\?.*)?$",
    re.IGNORECASE,
)


class GitHubFetchError(Exception):
    pass


def github_url_to_raw(url: str) -> str | None:
    url = url.strip()
    m = GITHUB_RAW.match(url)
    if m:
        owner, repo, branch, path = m.groups()
        path = unquote(path)
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    m = GITHUB_BLOB_OR_TREE.match(url)
    if m:
        owner, repo, branch, path = m.groups()
        path = unquote(path)
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    return None


async def fetch_github_file(url: str, github_token: str | None = None) -> tuple[str, str | None]:
    raw = github_url_to_raw(url)
    if not raw:
        raise GitHubFetchError(
            "Niepoprawny link GitHub. Wklej bezpośredni link do pliku (blob/raw), a jeśli repo jest prywatne, podaj token."
        )
    filename = raw.rsplit("/", 1)[-1] if "/" in raw else None
    headers = {"Accept": "text/plain,*/*"}
    token = (github_token or "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        response = await client.get(raw, headers=headers)
    if response.status_code in (401, 403):
        raise GitHubFetchError(
            "Brak dostępu do pliku. Dla prywatnego repo podaj poprawny Personal Access Token GitHub."
        )
    if response.status_code == 404:
        raise GitHubFetchError(
            "Nie udało się pobrać pliku. Sprawdź link do konkretnego pliku albo to, czy repozytorium nie jest prywatne."
        )
    response.raise_for_status()
    text = response.text
    if not text.strip():
        raise GitHubFetchError("Pobrano pustą odpowiedź.")
    return text, filename
