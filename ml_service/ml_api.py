from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Service - Delay Prediction")


class Task(BaseModel):
    description: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict_delay")
def predict_delay(task: Task):
    desc = task.description.lower()
    if "block" in desc or len(desc.split()) > 12:
        return {"delay_risk": "HIGH", "prob": 0.88}
    return {"delay_risk": "LOW", "prob": 0.12}
