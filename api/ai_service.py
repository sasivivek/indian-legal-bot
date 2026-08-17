"""
Bharat Legal AI — Gemini AI Service
Wrapper for Google Gemini API to generate grounded legal answers from RAG prompts.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class AIService:
    """
    Google Gemini Generative AI wrapper for text completion in the RAG pipeline.
    """

    _instance: Optional["AIService"] = None

    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", model_name)
        self._model = None
        self._initialized = False

    @classmethod
    def get_instance(cls) -> "AIService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _init_gemini(self) -> bool:
        """Initialize the Gemini client once if API key is provided."""
        if self._initialized:
            return self._model is not None

        if not self.api_key or self.api_key in ("your_gemini_api_key_here", ""):
            print("[AIService] Warning: No valid GEMINI_API_KEY found. RAG will use template fallback.")
            self._initialized = True
            return False

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config={
                    "temperature": 0.2,  # Low temperature for factual legal answers
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1024,
                },
            )
            self._initialized = True
            print(f"[AIService] Gemini AI initialized with model '{self.model_name}'.")
            return True
        except Exception as e:
            print(f"[AIService] Error configuring Gemini AI: {e}")
            self._initialized = True
            self._model = None
            return False

    def is_configured(self) -> bool:
        """Check if Gemini AI is properly configured with an API key."""
        return self._init_gemini()

    async def generate(self, prompt: str) -> str:
        """
        Generate response text from Gemini given a constructed RAG prompt.
        """
        if not self.is_configured() or self._model is None:
            raise RuntimeError("Gemini AI is not configured or unavailable.")

        try:
            # Generate content synchronously or wrapped in async
            response = self._model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
            raise RuntimeError("Gemini returned an empty response.")
        except Exception as e:
            print(f"[AIService] Generation error: {e}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """Health check status."""
        configured = bool(self.api_key and self.api_key != "your_gemini_api_key_here")
        return {
            "configured": configured,
            "model": self.model_name,
            "initialized": self._model is not None,
        }


# Helper factory function
def get_ai_service() -> AIService:
    return AIService.get_instance()
