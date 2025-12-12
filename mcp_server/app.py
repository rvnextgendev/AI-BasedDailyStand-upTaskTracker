from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes_tools import router as tools_router

app = FastAPI(title="MCP Tool Hub - Standup Task Tracker (Repo Pattern)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(tools_router)
