from typing import Any, Dict
import requests
from ...config import get_settings
from ...core.services import ILLMClient

settings = get_settings()


class LocalOllamaLLMClient(ILLMClient):
    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        prompt = f"{system_prompt}\n\nUser:\n{user_prompt}"
        r = requests.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60,
        )
        r.raise_for_status()
        data: Dict[str, Any] = r.json()
        return data.get("response", "")


class AzureOpenAILLMClient(ILLMClient):
    def __init__(self):
        self.endpoint = settings.AZURE_OPENAI_ENDPOINT.rstrip("/")
        self.api_key = settings.AZURE_OPENAI_API_KEY
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        url = (
            f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions"
            "?api-version=2024-05-01-preview"
        )
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        body = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        r = requests.post(url, headers=headers, json=body, timeout=60)
        r.raise_for_status()
        data: Dict[str, Any] = r.json()
        return data["choices"][0]["message"]["content"]


class BedrockLLMClient(ILLMClient):
    def __init__(self):
        # Initialize boto3 client for Bedrock when ready.
        self.model_id = "anthropic.claude-v2"

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError("BedrockLLMClient not implemented yet")


class GoogleVertexLLMClient(ILLMClient):
    def __init__(self):
        # Initialize Vertex AI client here.
        pass

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError("GoogleVertexLLMClient not implemented yet")
