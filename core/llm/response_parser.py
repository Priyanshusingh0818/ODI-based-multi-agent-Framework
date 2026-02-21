"""
core/llm/response_parser.py

Utilities for parsing and validating structured output from LLM responses.
"""

import json
import re
import logging
from typing import Any

logger = logging.getLogger(__name__)


class ResponseParser:
    """
    Parses raw LLM text responses into structured Python objects.
    """

    @staticmethod
    def extract_json(response: str) -> Any:
        """
        Extract and parse a JSON object from a raw LLM response string.

        Handles cases where the model wraps JSON in markdown code fences
        (e.g. ```json ... ```) or includes leading/trailing prose.

        Args:
            response (str): The raw string returned by the LLM.

        Returns:
            Any: The parsed Python object (typically a dict or list).

        Raises:
            ValueError: If no valid JSON object can be found or parsed.
        """
        if not response or not response.strip():
            raise ValueError("LLM returned an empty response.")

        # Step 1: Strip markdown code fences if present
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", response, re.DOTALL)
        if fence_match:
            json_str = fence_match.group(1)
            logger.debug("Extracted JSON from markdown code fence.")
        else:
            # Step 2: Fallback — grab the first {...} block in the response
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if not json_match:
                logger.error(f"No JSON found in response: {response!r}")
                raise ValueError(
                    "No JSON object found in LLM response. "
                    f"Raw response: {response[:300]!r}"
                )
            json_str = json_match.group()
            logger.debug("Extracted JSON via regex fallback.")

        try:
            parsed = json.loads(json_str)
            logger.debug(f"Successfully parsed JSON with keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'list'}")
            return parsed
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e} | Raw JSON string: {json_str!r}")
            raise ValueError(
                f"Failed to parse JSON from LLM response: {str(e)}\n"
                f"Raw JSON string: {json_str[:300]!r}"
            ) from e

    @staticmethod
    def validate_plan(plan: dict) -> bool:
        """
        Validate that a parsed plan dict has the expected structure.

        Args:
            plan (dict): The parsed plan from the LLM.

        Returns:
            bool: True if valid.

        Raises:
            ValueError: If required fields are missing or malformed.
        """
        if not isinstance(plan, dict):
            raise ValueError(f"Expected a JSON object (dict), got {type(plan).__name__}.")

        if "goal" not in plan:
            raise ValueError("Plan is missing required field: 'goal'.")

        if "steps" not in plan or not isinstance(plan["steps"], list):
            raise ValueError("Plan is missing required field: 'steps' (must be a list).")

        if len(plan["steps"]) == 0:
            raise ValueError("Plan must contain at least one step.")

        for i, step in enumerate(plan["steps"]):
            if "step_number" not in step or "description" not in step:
                raise ValueError(
                    f"Step {i + 1} is malformed. Expected 'step_number' and 'description'."
                )

        return True