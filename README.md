# clean-code-analyzer-backend

🔗 **API:** https://clean-code-analyzer-backend.onrender.com  
📖 **Swagger UI:** https://clean-code-analyzer-backend.onrender.com/docs

## Stack technologiczny

- **Python 3.10+** (zalecane 3.12): język backendu
- **FastAPI**: framework REST API
- **Uvicorn**: serwer ASGI do uruchamiania aplikacji
- **Pydantic**: modele request/response i walidacja danych
- **OpenAI SDK**: komunikacja z OpenAI (`openai`, klient `AsyncOpenAI`)
- **HTTPX**: pobieranie plików z GitHuba (async)
- **python-dotenv**: wczytywanie `.env` przy starcie
- **Starlette**: komponenty bazowe używane przez FastAPI (middleware/response)

## Wymagania wstępne

- Python **3.10 lub nowszy** (zalecane 3.12)
- Docker (opcjonalnie, ale rekomendowane)

## Zmienne środowiskowe (.env)

Backend wczytuje zmienne z pliku `.env` (przez `python-dotenv`). Startowo skopiuj przykładowy plik:

```bash
# Windows
copy .env.example.txt .env

# Linux / macOS
cp .env.example.txt .env
```

Dostępne zmienne:

| Zmienna | Opis |
|---|---|
| `CORS_RESTRICT` | Jeśli `true/1/yes`, CORS ograniczony do `CORS_ALLOW_ORIGINS`; w przeciwnym razie `allow_origins=["*"]` |
| `CORS_ALLOW_ORIGINS` | Lista originów rozdzielona przecinkami, np. `http://localhost:5173,http://127.0.0.1:5173` |

> **Uwaga:** Klucz OpenAI API **nie jest** przechowywany przez backend. Jest podawany przez użytkownika w UI frontendowym i przekazywany w body każdego żądania jako pole `api_key`.

## Jak uruchomić lokalnie

### Docker (rekomendowane)

Uruchom tylko backend z katalogu root projektu (`clean-code-analyzer-backend`):

```bash
docker build -t backend-app .
docker run -p 8000:8000 backend-app
```

Po starcie:
- backend: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- healthcheck: `http://127.0.0.1:8000/api/health`

### Bez Dockera

W katalogu `clean-code-analyzer-backend`:

```bash
# 1. Utwórz i aktywuj wirtualne środowisko

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Uruchom serwer
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Po starcie:
- Swagger UI: `http://127.0.0.1:8000/docs`
- healthcheck: `http://127.0.0.1:8000/api/health`

## Endpointy API

| Metoda | Endpoint | Opis |
|---|---|---|
| GET | `/` | Metadane serwisu (ścieżki do docs i health) |
| GET | `/health` | Alias healthcheck |
| GET | `/api/health` | Healthcheck API |
| POST | `/api/analyze-code` | Analiza kodu |
| POST | `/api/review-user-fix` | Review poprawki użytkownika |
| POST | `/api/fetch-github` | Pobranie pliku z GitHuba |

### Przykładowe body żądań

#### POST `/api/analyze-code`

```json
{
  "code": "def foo():\n    x=1\n    return x",
  "api_key": "sk-...",
  "analysis_standard": "clean_code"
}
```

#### POST `/api/review-user-fix`

```json
{
  "original_code": "def foo():\n    x=1\n    return x",
  "fixed_code": "def foo():\n    x = 1\n    return x",
  "api_key": "sk-..."
}
```

#### POST `/api/fetch-github`

```json
{
  "url": "https://github.com/user/repo/blob/main/example.py",
  "api_key": "sk-..."
}
```

> Pełna dokumentacja interaktywna dostępna w **Swagger UI** pod `/docs`.

## Jak zainstalować zależności

W katalogu `clean-code-analyzer-backend`:

```bash
pip install -r requirements.txt
```

> **Uwaga:** W katalogu `app/` znajduje się osobny `requirements.txt` używany przez Render, gdy root directory serwisu ustawiony jest na `clean-code-analyzer-backend/app`.

## Wdrożenie na Render

1. Utwórz nowy serwis typu **Web Service** na [render.com](https://render.com)
2. Połącz z repozytorium GitHub
3. Ustaw następujące opcje:

- **Root Directory:** *(puste — domyślny root repozytorium)*
- **Runtime:** Python 3
- **Build Command:** `pip install -r clean-code-analyzer-backend/requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. Dodaj zmienne środowiskowe (`CORS_RESTRICT`, `CORS_ALLOW_ORIGINS`) w zakładce **Environment**
5. Kliknij **Deploy**

Po wdrożeniu API będzie dostępne pod adresem Render, np.:  
`https://clean-code-analyzer-backend.onrender.com`
