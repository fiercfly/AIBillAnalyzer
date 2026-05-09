# Perceptive Labs

Simple full-stack prototype (Flask backend + Vite/React frontend) for uploading and processing files.

## Project structure

- `backend/` — Flask app and server-side code
- `backend/uploads/` — Uploaded files storage
- `frontend/` — Vite + React frontend

## Quick start

Requirements: Python 3.8+, Node.js 16+

1) Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
# copy or create .env with required variables
python app.py
```
2) Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment

- Put secret keys and configuration in `backend/.env` (do not commit this file).
- Typical entries: `FLASK_APP`, `FLASK_ENV`, `SECRET_KEY`, `DATABASE_URL` (if used).

## Usage

- The frontend talks to the Flask backend API in `backend/app.py` for uploading files and processing.
- Uploaded files are stored under `backend/uploads/`.

## Development notes

- Backend is a minimal Flask app — add routes and validation as needed.
- Frontend is a Vite React app — extend components in `frontend/src/`.

## Future improvements

- Add user authentication and authorization (JWT / OAuth).
- Validate and sanitize uploaded files; enforce size and type limits.
- Add unit and integration tests for backend and frontend.
- Introduce a database (Postgres) and migrations for persistent data.
- Dockerize backend and frontend for easier local/dev deployment.
- Add CI pipeline (GitHub Actions) to run tests and linting.
- Improve frontend UX: better upload progress, error handling, responsive layout.
- Convert frontend to TypeScript for stronger typing.
- Add rate limiting, input sanitization, and security headers on the backend.
- Add logging, metrics, and error reporting (Sentry/Prometheus).
- Support authenticated file management (list, delete, permissions).
- Add automated deployments (staging + production) and environment-specific configs.

## Future Improvements We can -

- Add OCR preprocessing for scanned documents to improve accuracy on image-only PDFs
- Add confidence scores for extracted fields
- Add a results history page with search and download options
- Export structured output as JSON, CSV, and Excel
- Add user authentication and role-based admin controls
- Improve validation and auto-correction of malformed model JSON
- Add background job processing for large batch uploads
- Support more document types such as purchase orders, receipts, and contracts with separate schemas
- Add automated tests for the backend API and frontend upload flow
- Add deployment support with Docker and cloud hosting

---
Created for the Perceptive Lab prototype. Feel free to edit and expand.
# Perceptive Lab

An LLM-powered invoice and document extraction app with a React frontend and a Flask backend. The backend uses Groq’s OpenAI-compatible API to extract structured data from PDFs and images using admin-controlled prompts.


### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create or update `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
FLASK_ENV=development
FLASK_DEBUG=True
ADMIN_TEMPLATE=invoice
```

Start the backend:

```bash
python app.py
```

The API runs at `http://localhost:5000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

## How It Works

1. The frontend uploads a file to the Flask backend.
2. The backend validates file type and size.
3. The backend uses the admin-selected template prompt.
4. PDF text is extracted first; if needed, the backend falls back to image handling for supported workflows.
5. The model response is returned as raw text and, when possible, parsed JSON.

## Praveen Kumar
