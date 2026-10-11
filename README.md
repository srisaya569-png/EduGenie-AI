# EduGenie — Google Gemini Powered Learning Assistant

A beginner-friendly educational assistant built with FastAPI, Jinja2, HTML/CSS/JavaScript, and the Google Gemini API.

## Features
- Question answering
- Beginner-friendly concept explanations
- Three-question MCQ quiz with answer checking and explanations
- Educational text summarization
- Beginner-to-advanced learning roadmaps
- Responsive frontend, input validation, health endpoint, and API error handling
- Demo mode for trying the interface without a Gemini key

## Requirements
- Python 3.10 or newer (Python 3.11 or 3.12 is recommended)
- VS Code
- Internet connection and a Gemini API key for AI-generated responses

## Windows / VS Code setup

Open the `EduGenie-AI` folder in VS Code. Open **Terminal → New Terminal** and run:

```powershell
py -3.11 --version
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If Python 3.11 is not installed, install Python 3.11 or 3.12 and enable **Add Python to PATH** during installation. You can use `python` instead of `py -3.11` if that command points to your supported Python version.

## Configure Gemini

1. Copy `.env.example` and name the copy `.env`.
2. Get an API key from https://aistudio.google.com/apikey.
3. Open `.env` and put your key after `GEMINI_API_KEY=`:

```dotenv
GEMINI_API_KEY=your_actual_key_here
GEMINI_MODEL=gemini-3.8-flash
DEMO_MODE=false
```

Keep `.env` private. Do not upload it to GitHub or share screenshots containing your key.

### Try without an API key
In `.env`, set `DEMO_MODE=true`. Restart the server. This returns sample responses to test the UI; it does not call Gemini or generate genuinely topic-specific AI answers.

## Run the app

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser. Keep the terminal open while using the app. Press `Ctrl+C` in the terminal to stop the server.

## Test
1. Visit `/` and submit a question.
2. Select **Explain a concept** and enter a topic.
3. Select **Generate a quiz**, enter a topic, and check the answers.
4. Paste a paragraph into **Summarize notes**.
5. Ask for a learning path, e.g. `Learn SQL from beginner to advanced`.
6. Visit http://127.0.0.1:8000/health to confirm the backend is running.
7. Visit http://127.0.0.1:8000/docs to try the REST API.

## API endpoints
- `POST /api/task` — JSON body: `{"task":"qa","text":"Your question"}`
- `POST /qa`
- `POST /explain`
- `POST /quiz`
- `POST /summarize`
- `POST /learn/recommendations`
- `GET /health`

The compatibility endpoints accept the same JSON shape, for example `{"task":"qa","text":"What is SQL?"}`; the endpoint selects the task regardless of the supplied task field.

## Troubleshooting
- **`Activate.ps1 cannot be loaded`**: activation is optional. Run commands using `.\.venv\Scripts\python.exe` as shown above.
- **`No module named uvicorn`**: install with `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
- **`Attribute "app" not found in module "main"`**: confirm the file is named `main.py`, saved, and contains `app = FastAPI(...)`; run the command from the project root.
- **Gemini key missing / 401 / 403**: verify `.env` is in the same folder as `main.py`, the key is valid, and `DEMO_MODE=false`. Restart Uvicorn after editing `.env`.
- **Model not found / access error**: check the model name and API availability for your account in Google AI Studio. You can change `GEMINI_MODEL` in `.env`.
- **Port 8000 busy**: run `.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8001`, then open http://127.0.0.1:8001.

## Project structure

```text
EduGenie-AI/
├── main.py
├── config.py
├── gemini_client.py
├── services.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Important notes
- AI output can be inaccurate; verify important study information.
- The documentation mentioned a local LaMini-Flan-T5 model. This starter project uses Gemini for explanations too, avoiding a large model download and reducing setup complexity. A local model can be added later if offline explanations are a requirement.
- The API key is read on startup from `.env`; restart the server after changing it.
