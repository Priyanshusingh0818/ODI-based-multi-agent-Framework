"""
core/llm/llama_wrapper.py

Groq-hosted LLaMA LLM wrapper implementing the BaseLLM interface.
Reads configuration from environment variables via .env file.
"""

import os
import logging
from typing import List, Dict

from groq import Groq
from dotenv import load_dotenv

from .llm_interface import BaseLLM

load_dotenv()

logger = logging.getLogger(__name__)


class LlamaWrapper(BaseLLM):
    """
    Wrapper around the Groq API for LLaMA model inference.

    Configuration (via .env):
        GROQ_API_KEY   : Required. Your Groq API key.
        MODEL_NAME     : Optional. Default is 'llama-3.1-8b-instant'.
        TEMPERATURE    : Optional. Sampling temperature. Default is 0.2.
        MAX_TOKENS     : Optional. Max tokens in response. Default is 1500.
    """

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
        self.temperature = float(os.getenv("TEMPERATURE", 0.2))
        self.max_tokens = int(os.getenv("MAX_TOKENS", 1500))

        if not self.api_key:
            raise EnvironmentError(
                "GROQ_API_KEY is not set. Please add it to your .env file."
            )

        self.client = Groq(api_key=self.api_key)
        logger.info(
            f"LlamaWrapper ready | model={self.model_name} | "
            f"temperature={self.temperature} | max_tokens={self.max_tokens}"
        )

    def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Send messages to the Groq LLaMA API and return the response text.

        Args:
            messages (List[Dict[str, str]]): Chat-format messages.

        Returns:
            str: The model's text response, stripped of leading/trailing whitespace.

        Raises:
            RuntimeError: If the API call fails for any reason.
        """
        try:
            logger.debug(f"Sending {len(messages)} message(s) to Groq API.")

            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                messages=messages,
            )

            content = response.choices[0].message.content.strip()
            logger.debug(f"Received response ({len(content)} chars).")
            return content

        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            raise RuntimeError(f"LLM generation failed: {str(e)}") from e