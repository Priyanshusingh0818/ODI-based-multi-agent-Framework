"""
main.py

Entry point for the ODI Multi-Agent Framework.
Demonstrates a basic planner run and can be extended for CLI or app usage.
"""

import json
import logging
import sys

# ---------------------------------------------------------------------------
# Logging configuration — set up before any imports that use loggers
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    try:
        from core.agents.planner_agent import PlannerAgent
    except ImportError as e:
        logger.critical(f"Failed to import PlannerAgent: {e}")
        sys.exit(1)

    task = (
        "Build a REST API using FastAPI that allows users to register, "
        "log in, and manage a personal to-do list with full CRUD operations."
    )

    logger.info("Starting ODI Multi-Agent Framework")
    logger.info(f"Task: {task!r}")

    try:
        agent = PlannerAgent()
        plan = agent.plan(task)

        # Optionally validate the plan structure
        from core.llm.response_parser import ResponseParser
        ResponseParser.validate_plan(plan)

        print("\n" + "=" * 60)
        print("  GENERATED PLAN")
        print("=" * 60)
        print(json.dumps(plan, indent=2))
        print("=" * 60 + "\n")

    except ValueError as e:
        logger.error(f"Plan parsing/validation error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"LLM runtime error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()