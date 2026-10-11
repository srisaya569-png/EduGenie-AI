const form = document.querySelector("#task-form");
const textInput = document.querySelector("#text");
const count = document.querySelector("#char-count");
const submitBtn = document.querySelector("#submit-btn");
const resultSection = document.querySelector("#result-section");
const result = document.querySelector("#result");
const copyBtn = document.querySelector("#copy-btn");
let lastPlainText = "";

textInput.addEventListener("input", () => {
  count.textContent = `${textInput.value.length} / 20000`;
});
document.querySelectorAll('input[name="task"]').forEach(radio => {
  radio.addEventListener("change", () => {
    const placeholders = {
      qa: "For example: Which is the largest ocean?",
      explain: "For example: Explain photosynthesis in simple terms...",
      quiz: "Enter a topic or paste your study notes to create a quiz...",
      summarize: "Paste the educational passage you want to summarize...",
      learn: "For example: I want to learn SQL from beginner to advanced..."
    };
    textInput.placeholder = placeholders[radio.value];
    submitBtn.firstChild.textContent = radio.value === "quiz" ? "Create quiz " : "Generate answer ";
  });
});

function renderText(value) {
  result.replaceChildren();
  const pre = document.createElement("div");
  pre.textContent = value;
  result.appendChild(pre);
  lastPlainText = value;
}
function renderQuiz(data) {
  result.replaceChildren();
  const title = document.createElement("h3");
  title.textContent = data.title || "Practice quiz";
  result.appendChild(title);
  const questions = data.questions || [];
  questions.forEach((q, i) => {
    const block = document.createElement("section");
    block.className = "quiz-question";
    const heading = document.createElement("h3");
    heading.textContent = `${i + 1}. ${q.question}`;
    block.appendChild(heading);
    const feedback = document.createElement("p");
    feedback.className = "quiz-feedback";
    feedback.hidden = true;
    q.options.forEach((option, j) => {
      const label = document.createElement("label");
      label.className = "quiz-option";
      const input = document.createElement("input");
      input.type = "radio"; input.name = `question-${i}`; input.value = String(j);
      const span = document.createElement("span");
      span.textContent = option;
      label.append(input, span);
      block.appendChild(label);
    });
    block.appendChild(feedback);
    result.appendChild(block);
  });
  const submit = document.createElement("button");
  submit.type = "button"; submit.className = "quiz-submit"; submit.textContent = "Check my answers";
  submit.addEventListener("click", () => {
    let score = 0;
    questions.forEach((q, i) => {
      const chosen = result.querySelector(`input[name="question-${i}"]:checked`);
      const feedback = result.querySelectorAll(".quiz-feedback")[i];
      feedback.hidden = false;
      const correct = Number(chosen?.value) === Number(q.answer);
      if (correct) score++;
      feedback.className = `quiz-feedback ${correct ? "correct" : "wrong"}`;
      feedback.textContent = `${correct ? "Correct!" : `Not quite. Correct answer: ${q.options[q.answer]}.`} ${q.explanation || ""}`;
    });
    let scoreNode = result.querySelector(".quiz-score");
    if (!scoreNode) { scoreNode = document.createElement("p"); scoreNode.className = "quiz-score"; result.prepend(scoreNode); }
    scoreNode.textContent = `Your score: ${score} / ${questions.length}`;
    lastPlainText = `Quiz: ${data.title || ""}\nScore: ${score}/${questions.length}\n` + questions.map((q,i)=>`${i+1}. ${q.question}\nCorrect answer: ${q.options[q.answer]}\n${q.explanation||""}`).join("\n\n");
  });
  result.appendChild(submit);
  if (data.note) { const note = document.createElement("p"); note.textContent = data.note; result.appendChild(note); }
  lastPlainText = `${data.title || "Quiz"}\n` + questions.map((q,i)=>`${i+1}. ${q.question}\n${q.options.map((o,j)=>`${String.fromCharCode(65+j)}. ${o}`).join("\n")}`).join("\n\n");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const task = new FormData(form).get("task");
  const text = textInput.value.trim();
  if (!text) { textInput.focus(); return; }
  submitBtn.disabled = true;
  submitBtn.textContent = "Working...";
  resultSection.hidden = false;
  result.replaceChildren();
  const loading = document.createElement("div");
  loading.className = "loading";
  loading.innerHTML = '<span class="spinner" aria-hidden="true"></span><span>Preparing your learning result...</span>';
  result.appendChild(loading);
  resultSection.scrollIntoView({behavior:"smooth", block:"start"});
  try {
    const response = await fetch("/api/task", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({task, text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed.");
    if (task === "quiz" && data.result && Array.isArray(data.result.questions)) renderQuiz(data.result);
    else renderText(typeof data.result === "string" ? data.result : JSON.stringify(data.result, null, 2));
  } catch (error) {
    renderText(`Sorry, something went wrong.\n${error.message}\n\nCheck that the server is running and your .env settings are correct.`);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Generate answer <span aria-hidden="true">→</span>';
  }
});
copyBtn.addEventListener("click", async () => {
  if (!lastPlainText) return;
  try {
    await navigator.clipboard.writeText(lastPlainText);
    copyBtn.textContent = "Copied!";
    setTimeout(() => copyBtn.textContent = "Copy text", 1500);
  } catch {
    copyBtn.textContent = "Copy unavailable";
  }
});
