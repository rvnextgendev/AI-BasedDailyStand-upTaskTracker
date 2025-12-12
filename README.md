# AI-BasedDailyStand-upTaskTracker

## Developer key generation (local)
Generate a throwaway RSA pair and JWT for local testing so the services can verify requests.

0) Install local Python deps for the scripts (includes cryptography for the Python keygen path):  
```
pip install -r requirements.txt
```
If you prefer OpenSSL for key generation on Windows, install it (e.g., `winget install ShiningLight.OpenSSL.Light`).

1) Create RSA keys (requires OpenSSL):
```
openssl genrsa -out keys/dev-jwt.key 2048
openssl rsa -in keys/dev-jwt.key -pubout -out keys/jwt.pub
```

2) Mint a developer token (pyjwt is already in requirements):
```
python scripts/generate_jwt.py --sub user-1 --role ScrumMaster --name "Dev User" --key keys/dev-jwt.key
```
Use the printed string as `Authorization: Bearer <token>` when calling MCP tools or APIs.

Common ready-to-run commands:
```
# Developer
python scripts/generate_jwt.py --sub developer-1 --role Developer --name "Developer User" --key keys/dev-jwt.key --hours 24

# ScrumMaster
python scripts/generate_jwt.py --sub sm-1 --role ScrumMaster --name "Scrum Master" --key keys/dev-jwt.key --hours 24

# Admin
python scripts/generate_jwt.py --sub admin-1 --role Admin --name "Admin User" --key keys/dev-jwt.key --hours 24
```

3) Docker Compose mounts `./keys` into the mcp-server container, so `JWT_PUBLIC_KEY_PATH=/keys/jwt.pub` is picked up automatically during local runs. Avoid using these keys in production; use your real issuer/JWKS there.

## Sample stand-up prompts by role
Copy/paste into the UI “stand-up update” box:

- Developer: `Yesterday: Finished API endpoint for task creation and wrote unit tests. Today: Integrating front-end form with the new endpoint. Blockers: Waiting on QA env credentials.`
- ScrumMaster: `Yesterday: Facilitated sprint planning and confirmed scope with stakeholders. Today: Tracking progress on API integration and front-end handoff. Blockers: Pending UAT slot for demo environment.`
- Admin: `Yesterday: Reviewed access logs and rotated API keys. Today: Auditing permissions for new project members. Blockers: Need approval to provision additional monitoring alerts.`

Role-specific stand-up examples (copy/paste):
- Developer — What I did: “Finished API endpoint for task creation and wrote unit tests.” What I’m doing: “Integrating front-end form with the new endpoint.” Blockers: “Waiting on QA env credentials.”
- ScrumMaster — What I did: “Facilitated sprint planning, confirmed scope with stakeholders.” What I’m doing: “Tracking progress on API integration and front-end handoff.” Blockers: “Pending UAT slot for demo environment.”
- Admin — What I did: “Reviewed access logs and rotated API keys.” What I’m doing: “Auditing permissions for new project members.” Blockers: “Need approval to provision additional monitoring alerts.”

## End-to-end steps to save data
1) Start the stack (from repo root): `docker compose up -d`. Ensure containers `mcp-server`, `orchestrator-service`, `ui-service`, and `standup-postgres` are running.
2) Generate a token (example: Developer): `python scripts/generate_jwt.py --sub developer-1 --role Developer --name "Developer User" --key keys/dev-jwt.key --hours 24`.
3) Open the UI at http://localhost:8501. Paste the JWT in the “Bearer token” field, keep `User ID` at any value (token’s `sub` is what’s used), and enter your stand-up text (use prompts above). Submit.
4) Verify tasks saved (optional): `psql -h localhost -p 5444 -U standupuser -d standupdb -c "SELECT id, user_id, description, status, delay_risk, created_at FROM tasks ORDER BY id DESC LIMIT 5;"`.
5) Direct API test (optional):  
```
curl -X POST http://localhost:7000/tools/task-db.create_task \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"args":{"description":"test","delay_risk":"LOW"}}'
```

## Architecture (local stack)
```
[UI (Streamlit, :8501)]
       |
       v
[Orchestrator (FastAPI, :8000)]
       |  calls MCP tools with Bearer token
       v
[MCP Server (FastAPI, :7000)] --reads--> [keys/jwt.pub]
       | \
       |  \---> [Postgres (:5444->5432)]  <-- tasks, standups, users
       |  \
       |   \-> [ML Service (:8002->8000)]  delay risk
       |    \
       |     \-> [Notification Service (:8003->8000)]
       |
       \--> [LLM Service (Ollama, :11434)]  optional for extraction/summaries
```

### Diagram
```mermaid
flowchart TD
    UI[UI (Streamlit, :8501)]
    ORCH[Orchestrator (FastAPI, :8000)]
    MCP[MCP Server (FastAPI, :7000)]
    KEYS[keys/jwt.pub\n(JWT public key)]
    PG[(Postgres\n:5444->5432)]
    ML[ML Service\n:8002->8000\nDelay risk scoring]
    NOTIF[Notification Service\n:8003->8000]
    LLM[LLM Service (Ollama)\n:11434 optional]

    UI --> ORCH --> MCP
    MCP -->|reads| KEYS
    MCP --> PG
    MCP --> ML
    MCP --> NOTIF
    MCP -->|optional| LLM
```
