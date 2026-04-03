# clean-code-analyzer-backend

## Wdrozenie na Render

1. Wypchnij projekt do GitHuba.
2. W Render utworz nowa usluge `Web Service` z tego repozytorium.
3. Ustaw konfiguracje:
   - Runtime: `Python 3`
   - Root directory: `clean-code-analyzer-backend/app`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Ustaw zmienne srodowiskowe:
   - `CORS_ALLOW_ORIGINS=https://<twoj-frontend>.vercel.app`
5. Wdroz aplikacje i sprawdz endpoint zdrowia:
   - `https://<twoj-render-url>/api/health`