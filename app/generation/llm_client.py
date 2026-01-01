# app/generation/llm_client.py

import requests
import google.generativeai as genai

from app.core.config import settings
from app.core.exceptions import LLMGenerationError


class LLMClient:
    """
    Hybrid LLM client.

    Priority:
    1. Gemini direct API
    2. Internal Render service (Vertex AI)

    Falls back automatically.
    """

    def __init__(self):
        self._init_gemini()

    def _init_gemini(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        else:
            self.model = None

    def _generate_via_gemini(self, prompt: str) -> str:
        if not self.model:
            raise RuntimeError("Gemini not configured")

        response = self.model.generate_content(prompt)
        return response.text.strip()

    def _generate_via_internal_service(self, prompt: str) -> str:
        if not settings.INTERNAL_LLM_URL:
            raise RuntimeError("Internal LLM service not configured")

        resp = requests.post(
            settings.INTERNAL_LLM_URL,
            json={"text": prompt},
            timeout=settings.INTERNAL_LLM_TIMEOUT,
        )

        if resp.status_code != 200:
            raise RuntimeError(f"Internal LLM failed: {resp.text}")

        # Render returns: { "response": "..." }
        try:
            data = resp.json()
        except ValueError:
            return resp.text.strip()

        if isinstance(data, dict) and "response" in data:
            return data["response"].strip()

        raise RuntimeError(f"Unexpected internal LLM response: {data}")

    def generate(self, prompt: str) -> str:
        errors = []

        # Attempt 1: Gemini
        try:
            return self._generate_via_gemini(prompt)
        except Exception as e:
            errors.append(f"Gemini failed: {e}")

        # Attempt 2: Internal service
        try:
            return self._generate_via_internal_service(prompt)
        except Exception as e:
            errors.append(f"Internal LLM failed: {e}")

        raise LLMGenerationError(
            message="All LLM providers failed",
            details=errors,
        )
