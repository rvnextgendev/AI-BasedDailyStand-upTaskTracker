import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Orchestrator Service (Agent Stub)")

MCP_URL = os.getenv("MCP_URL", "http://mcp-server:7000")
LLM_URL = os.getenv("OLLAMA_URL", "http://llm-service:11434")
ML_URL = os.getenv("ML_URL", "http://ml-service:8000")


class StandupInput(BaseModel):
    user_id: int
    message: str
    token: str | None = None  # bearer token to pass to MCP


@app.get("/health")
def health():
    return {"status": "ok"}


def call_llm(prompt: str):
    try:
        r = requests.post(
            f"{LLM_URL}/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=30,
        )
        r.raise_for_status()
        return r.json().get("response", "")
    except Exception as ex:
        # LLM may be unavailable (model not pulled or service down); fall back to empty string
        print(f"LLM call failed: {ex}")
        return ""


def call_mcp(tool: str, args: dict, token: str):
    try:
        r = requests.post(
            f"{MCP_URL}/tools/{tool}",
            json={"args": args},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as ex:
        # On auth failures or connectivity issues, skip persisting but continue responding.
        print(f"MCP call failed for {tool}: {ex}")
        return None


def parse_standup_sections(text: str) -> dict:
    """Lightweight parser for 'What I did / I'm doing / Blockers' sections."""
    sections = {"yesterday": "", "today": "", "blockers": ""}
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    current = None
    for ln in lines:
        low = ln.lower()
        if low.startswith("what i did:") or low.startswith("yesterday:"):
            current = "yesterday"
            sections[current] = ln.split(":", 1)[1].strip() if ":" in ln else ""
            continue
        if low.startswith("what i’m doing:") or low.startswith("what i'm doing:") or low.startswith("today:"):
            current = "today"
            sections[current] = ln.split(":", 1)[1].strip() if ":" in ln else ""
            continue
        if low.startswith("blockers:"):
            current = "blockers"
            sections[current] = ln.split(":", 1)[1].strip() if ":" in ln else ""
            continue
        if current:
            sections[current] = (sections[current] + " " + ln).strip()
    if not any(sections.values()):
        sections["today"] = text.strip()
    return sections


@app.post("/agent/standup")
def run_standup(data: StandupInput):
    # Extract tasks via LLM if available
    prompt = f"Extract bullet tasks from this stand-up text. Return as lines.\n\n{data.message}"
    tasks_raw = call_llm(prompt)
    tasks = [t.strip("- ").strip() for t in tasks_raw.splitlines() if t.strip()] if tasks_raw else []

    # Fallback extraction if LLM is unavailable or returned nothing
    if not tasks:
        sentences = []
        for line in data.message.splitlines():
            line = line.strip()
            if not line:
                continue
            for part in line.split("."):
                part = part.strip()
                if part:
                    sentences.append(part)
        tasks = sentences

    # Predict delay locally for each task
    risks = []
    for t in tasks:
        r = requests.post(f"{ML_URL}/predict_delay", json={"description": t}, timeout=10)
        r.raise_for_status()
        risks.append({"task": t, "delay_risk": r.json().get("delay_risk", "UNKNOWN")})

    # Save tasks via MCP if token provided
    if data.token:
        for each in risks:
            call_mcp(
                "task-db.create_task",
                {"description": each["task"], "delay_risk": each["delay_risk"]},
                token=data.token,
            )
        # Also save structured standup content
        sections = parse_standup_sections(data.message)
        call_mcp(
            "standup.save",
            {
                "yesterday": sections["yesterday"],
                "today": sections["today"],
                "blockers": sections["blockers"],
            },
            token=data.token,
        )

    summary_prompt = f"Summarize tasks and risks for scrum master: {risks}"
    summary = call_llm(summary_prompt)
    if not summary:
        if risks:
            task_list = "; ".join([f"{r['task']} ({r['delay_risk']})" for r in risks])
            summary = f"Summary unavailable (LLM down). Tasks: {task_list}"
        else:
            summary = "No tasks extracted."

    return {"tasks": risks, "summary": summary}
