# ReviewGuard

AI-powered review moderation that moderates wording, intent, and safety — not opinions.

ReviewGuard sits between a user writing a review and that review going live. Instead of a blunt keyword filter, it uses the Gemini API to judge tone and safety while leaving the underlying opinion untouched, and always explains its decision instead of silently blocking or altering content.

> **Moderation, not censorship.** Criticism is allowed. Personal attacks, hate speech, threats, and spam are not. Every decision comes with a plain-language reason, and suggested edits always preserve the reviewer's original meaning.

---

## How it works

1. A user writes a review in the frontend.
2. The backend sends it to Gemini with a strict, JSON-only prompt describing the moderation policy.
3. Gemini returns a decision, a reason, and (where relevant) a reworded suggestion that keeps the original opinion intact.
4. The backend validates that response before trusting it, then hands it back to the frontend.
5. The result is shown as one of three outcomes — the user always has the final say before publishing.

| Decision | Meaning |
|---|---|
| 🟢 **Approve** | Genuine experience, respectful criticism, specific feedback |
| 🟡 **Needs Adjustment** | Personal insults, excessive profanity, or overly emotional wording — the complaint itself is fine, the wording isn't |
| 🔴 **Reject** | Hate speech, threats, spam, or defamatory accusations presented as fact |

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite) + Tailwind CSS |
| Backend | Python + Flask |
| AI | Google Gemini API |

---

## Project structure

```
ReviewGuard/
├── backend/
│   ├── app.py                     # Flask app factory & entrypoint
│   ├── config.py                  # Environment-based configuration
│   ├── routes/                    # HTTP layer
│   ├── services/                  # Business logic + Gemini client
│   ├── models/                    # Shared data types
│   ├── utils/                     # Response envelope helpers
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/                 # Screen-level components (state owners)
│   │   ├── components/            # Presentational components
│   │   └── services/              # API client
│   └── package.json
├── docs/
├── prompts/
├── tests/
└── PROJECT_RULES.md               # Source-of-truth product & engineering rules
```

---

## Getting started

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Gemini API key — [get one here](https://aistudio.google.com/apikey)

### 1. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and add your GEMINI_API_KEY

python app.py
```

The API runs at `http://127.0.0.1:5000`.

### 2. Frontend

In a separate terminal:

```bash
cd frontend
npm install

cp .env.example .env
# defaults to pointing at http://127.0.0.1:5000 — edit if your backend runs elsewhere

npm run dev
```

The app runs at `http://localhost:5173`. Both the backend and frontend need to be running at the same time.

---

## API reference

### `POST /api/moderate-review`

**Request**
```json
{
  "review_text": "The staff were rude and the food was cold."
}
```

**Response — success**
```json
{
  "success": true,
  "data": {
    "decision": "needs_adjustment",
    "reason": "Contains an emotionally charged tone toward staff, though the underlying feedback is valid.",
    "suggested_review": "The staff seemed inattentive and the food arrived cold."
  }
}
```

**Response — error**
```json
{
  "success": false,
  "message": "Review text must not be empty."
}
```

| Status | Meaning |
|---|---|
| `200` | Moderation completed successfully |
| `400` | Invalid input (e.g. empty review) |
| `502` | The Gemini API failed or returned an unusable response |

---

## Environment variables

**`backend/.env`**

| Variable | Description | Default |
|---|---|---|
| `GEMINI_API_KEY` | Your Gemini API key (required) | — |
| `GEMINI_MODEL` | Which Gemini model to call | `gemini-2.0-flash` |
| `FLASK_DEBUG` | Enable Flask debug mode | `false` |

**`frontend/.env`**

| Variable | Description | Default |
|---|---|---|
| `VITE_API_URL` | Base URL of the backend API | `http://127.0.0.1:5000` |

---

## Design principles

These rules, defined in [`PROJECT_RULES.md`](./PROJECT_RULES.md), govern every part of this codebase:

- The AI moderates **wording, intent, and safety** — never grammar, spelling, slang, or regional English.
- The AI **never changes a reviewer's opinion**; suggested edits must preserve the original meaning.
- Every decision includes a **reason** — no silent moderation.
- The AI's output is a **suggestion**, not a final verdict — a human always has the final say before a review is published.

---

## Known limitations & roadmap

This project intentionally stays scoped to a single moderation endpoint for now. Not yet implemented:

- Rate limiting
- Automated test suite in CI
- Authentication
- Accounts, history, analytics dashboard
- Multi-language support
- CSV upload / bulk moderation

---

## License

Not yet licensed for public reuse. All rights reserved unless a license file is added.