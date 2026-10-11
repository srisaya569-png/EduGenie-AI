from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from services import run_task
from config import APP_NAME, MAX_INPUT_CHARS, DEMO_MODE

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title=APP_NAME, description="Google Gemini-powered learning assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TaskRequest(BaseModel):
    task: str = Field(..., pattern="^(qa|explain|quiz|summarize|learn)$")
    text: str = Field(..., min_length=1, max_length=MAX_INPUT_CHARS)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "app_name": APP_NAME,
        "demo_mode": DEMO_MODE,
    },
)

@app.get("/health")
async def health():
    return {"status": "ok", "app": APP_NAME, "demo_mode": DEMO_MODE}


@app.post("/api/task")
async def task_api(payload: TaskRequest):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Please enter a question, topic, or passage.")
    try:
        result = run_task(payload.task, text)
        return {"task": payload.task, "result": result, "demo_mode": DEMO_MODE}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        # Avoid exposing API keys or internal tracebacks to the browser.
        raise HTTPException(status_code=502, detail=f"AI request failed: {exc}") from exc


# Compatibility endpoints matching the project documentation.
@app.post("/qa")
async def qa(payload: TaskRequest):
    return await task_api(payload.model_copy(update={"task": "qa"}))

@app.post("/explain")
async def explain(payload: TaskRequest):
    return await task_api(payload.model_copy(update={"task": "explain"}))

@app.post("/quiz")
async def quiz(payload: TaskRequest):
    return await task_api(payload.model_copy(update={"task": "quiz"}))

@app.post("/summarize")
async def summarize(payload: TaskRequest):
    return await task_api(payload.model_copy(update={"task": "summarize"}))

@app.post("/learn/recommendations")
async def recommendations(payload: TaskRequest):
    return await task_api(payload.model_copy(update={"task": "learn"}))
