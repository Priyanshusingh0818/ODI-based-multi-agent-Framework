"""
core/llm/prompt_templates.py

Centralised store for all LLM prompt templates used across agents.
Each static method returns a list of chat-format message dicts.
"""


class PromptTemplates:
    """
    Collection of prompt builders for each agent type.

    All methods return a List[Dict[str, str]] compatible with the
    OpenAI / Groq chat completions message format.
    """

    @staticmethod
    def planner(task: str) -> list:
        """
        Build the prompt for the PlannerAgent.

        Args:
            task (str): The user's high-level task description.

        Returns:
            list: A list of system + user messages.
        """
        return [
            {
                "role": "system",
                "content": (
                    "You are an expert AI Planner.\n"
                    "Your job is to break the given task into clear, structured, and actionable steps.\n\n"
                    "Rules:\n"
                    "- Return ONLY valid JSON. No markdown, no explanation, no preamble.\n"
                    "- Use this exact schema:\n\n"
                    "{\n"
                    '  "goal": "<concise summary of the main goal>",\n'
                    '  "steps": [\n'
                    '    {"step_number": 1, "description": "<clear action step>"},\n'
                    '    {"step_number": 2, "description": "<clear action step>"}\n'
                    "  ]\n"
                    "}\n\n"
                    "- Include between 3 and 10 steps.\n"
                    "- Each step must be specific, actionable, and non-redundant.\n"
                    "- Do NOT include any text outside the JSON object."
                ),
            },
            {
                "role": "user",
                "content": task.strip(),
            },
        ]

    @staticmethod
    def executor(step_description: str, context: str = "") -> list:
        """
        Build the prompt for an ExecutorAgent handling a single plan step.

        Args:
            step_description (str): The step to execute.
            context (str): Optional prior context or results.

        Returns:
            list: A list of system + user messages.
        """
        context_block = f"\nContext from previous steps:\n{context}\n" if context else ""

        return [
            {
                "role": "system",
                "content": (
                    "You are an expert AI Executor.\n"
                    "You will be given a single task step to carry out.\n"
                    "Respond with a clear, detailed execution of that step.\n"
                    f"{context_block}"
                ),
            },
            {
                "role": "user",
                "content": step_description.strip(),
            },
        ]

    @staticmethod
    def summariser(results: list) -> list:
        """
        Build the prompt to summarise results from multiple execution steps.

        Args:
            results (list): A list of step result strings.

        Returns:
            list: A list of system + user messages.
        """
        formatted = "\n".join(
            f"Step {i + 1}: {r}" for i, r in enumerate(results)
        )

        return [
            {
                "role": "system",
                "content": (
                    "You are an expert AI Summariser.\n"
                    "Synthesise the results of multiple completed steps into a "
                    "clear, concise final summary for the user."
                ),
            },
            {
                "role": "user",
                "content": f"Here are the completed step results:\n\n{formatted}",
            },
        ]