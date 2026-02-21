"""
core/llm/llm_interface.py

Defines the abstract base class for all LLM provider implementations.
Any new LLM backend (OpenAI, Anthropic, Cohere, etc.) must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseLLM(ABC):
    """
    Abstract base class for all LLM providers.

    All subclasses must implement the `generate` method, which accepts
    a list of chat-format messages and returns the model's text response.
    """

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages (List[Dict[str, str]]): A list of message dicts,
                each with 'role' ('system', 'user', or 'assistant')
                and 'content' (the message text).

        Returns:
            str: The model's response as a plain string.

        Raises:
            RuntimeError: If the LLM call fails.
        """
        pass