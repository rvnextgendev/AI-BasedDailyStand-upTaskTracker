FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Keep package under /app/mcp_server so relative imports work
COPY . /app/mcp_server
WORKDIR /app

EXPOSE 7000

CMD ["uvicorn", "mcp_server.app:app", "--host", "0.0.0.0", "--port", "7000"]
