"""
core/agents/planner_agent.py

Responsible for breaking a high-level task into structured, ordered steps
using the configured LLM backend.
"""

import logging
from core.llm.llama_wrapper import LlamaWrapper
from core.llm.prompt_templates import PromptTemplates
from core.llm.response_parser import ResponseParser

logger = logging.getLogger(__name__)


class PlannerAgent:
    """
    PlannerAgent takes a natural-language task and returns a structured
    JSON plan containing a goal and a list of ordered steps.
    """

    def __init__(self):
        self.llm = LlamaWrapper()
        logger.info("PlannerAgent initialized with LlamaWrapper.")

    def plan(self, task: str) -> dict:
        """
        Generate a structured plan for the given task.

        Args:
            task (str): A natural language description of the task to plan.

        Returns:
            dict: A structured plan with keys 'goal' and 'steps'.

        Raises:
            ValueError: If the LLM response cannot be parsed as valid JSON.
            RuntimeError: If the LLM call fails.
        """
        if not task or not task.strip():
            raise ValueError("Task cannot be empty.")

        logger.info(f"Planning task: {task!r}")

        messages = PromptTemplates.planner(task)
        raw_response = self.llm.generate(messages)

        logger.debug(f"Raw LLM response: {raw_response}")

        structured_output = ResponseParser.extract_json(raw_response)

        logger.info(f"Plan generated with {len(structured_output.get('steps', []))} steps.")
        return structured_output