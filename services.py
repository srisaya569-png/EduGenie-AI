from config import DEMO_MODE
from gemini_client import generate_text, parse_json

TASK_PROMPTS = {
    "qa": "Answer the learner's question accurately and clearly. Use headings or bullets when helpful.",
    "explain": "Explain the topic to a beginner in simple language. Include an analogy and one example.",
    "summarize": "Summarize the supplied educational text. Preserve the key ideas and use concise bullet points.",
    "learn": """Create a practical learning roadmap from beginner to advanced. Include stages, estimated timeline,
key topics, a practice project for each stage, and trustworthy resource names or official URLs when known.
Do not invent specific URLs if unsure.""",
}

def _demo(task, text):
    if task == "quiz":
        return {"title": f"Practice quiz: {text[:70]}", "questions": [
            {"question": f"What is the best first step when studying {text[:45]}?", "options": ["Understand the basic definition", "Skip all fundamentals", "Memorize random facts", "Avoid practice"], "answer": 0, "explanation": "Start by understanding the basic definition and core ideas."},
            {"question": "Which approach usually improves understanding?", "options": ["Regular practice", "Never reviewing", "Guessing only", "Studying without examples"], "answer": 0, "explanation": "Practice helps you apply and retain what you learn."},
            {"question": "What should you do after making a mistake?", "options": ["Review why it happened", "Ignore the feedback", "Stop learning", "Repeat without thinking"], "answer": 0, "explanation": "Reviewing mistakes helps correct misunderstandings."}
        ], "note": "Demo questions are generic examples. Add a Gemini API key for topic-specific quizzes."}
    samples = {
        "qa": f"Demo answer for: {text}\n\nThis response is a local demonstration, not a Gemini-generated answer. Add GEMINI_API_KEY to .env for AI answers.",
        "explain": f"Beginner explanation: {text}\n\nStart with the definition, identify its main parts, and connect each part to a familiar example. This is demo content; configure Gemini for a topic-specific explanation.",
        "summarize": f"Summary of your text:\n• Identify the main idea.\n• Keep only the most important supporting points.\n• Remove repetition and minor details.\n\nDemo mode does not analyze your passage with AI. Configure Gemini for a real summary.",
        "learn": f"Learning plan for {text}:\n1. Beginner — learn definitions and fundamentals (1–2 weeks).\n2. Intermediate — practice core techniques and solve exercises (2–4 weeks).\n3. Advanced — complete a small project and review gaps (2–4 weeks).\n4. Continue with official documentation, guided lessons, and regular practice.\n\nDemo roadmap; Gemini can personalize this plan."
    }
    return samples[task]

def run_task(task: str, text: str):
    if task not in ("qa", "explain", "quiz", "summarize", "learn"):
        raise ValueError("Unknown task selected.")
    if DEMO_MODE:
        return _demo(task, text)
    if task == "quiz":
        prompt = f"""Create exactly 3 educational multiple-choice questions based on the topic or text below.
Return ONLY valid JSON with this shape:
{{"title":"short title","questions":[{{"question":"...","options":["A","B","C","D"],"answer":0,"explanation":"..."}}]}}
Each question must have exactly four options. answer must be a zero-based integer from 0 to 3.
TOPIC/TEXT:\n{text}"""
        data = parse_json(generate_text(prompt))
        if not isinstance(data, dict) or not isinstance(data.get("questions"), list) or len(data["questions"]) != 3:
            raise ValueError("The AI did not return exactly three questions. Please try again.")
        for q in data["questions"]:
            if not isinstance(q.get("options"), list) or len(q["options"]) != 4 or q.get("answer") not in (0, 1, 2, 3):
                raise ValueError("The AI returned an invalid quiz format. Please try again.")
        return data
    return generate_text(f"{TASK_PROMPTS[task]}\n\nLearner input:\n{text}")
