from typing import Dict, Any
import requests
from ...config import get_settings
from ...core.services import IMLClient

settings = get_settings()


class LocalMLClient(IMLClient):
    def predict_delay(self, task_description: str) -> Dict[str, Any]:
        r = requests.post(
            f"{settings.ML_URL}/predict_delay",
            json={"description": task_description},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()


class AzureMLClient(IMLClient):
    def __init__(self):
        self.endpoint = settings.AZURE_ML_ENDPOINT
        self.api_key = settings.AZURE_ML_API_KEY

    def predict_delay(self, task_description: str) -> Dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        body = {"input_text": task_description}
        r = requests.post(self.endpoint, json=body, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()


class BedrockMLClient(IMLClient):
    def __init__(self):
        # Initialize boto3 client here when wiring for Bedrock.
        pass

    def predict_delay(self, task_description: str) -> Dict[str, Any]:
        raise NotImplementedError("BedrockMLClient not implemented yet")


class GoogleVertexMLClient(IMLClient):
    def __init__(self):
        # Initialize Vertex AI client here.
        pass

    def predict_delay(self, task_description: str) -> Dict[str, Any]:
        raise NotImplementedError("GoogleVertexMLClient not implemented yet")
