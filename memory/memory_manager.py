"""
Memory Manager — Core Integration Layer for Semantic Memory.

Coordinates the vector store and short-term memory to provide
retrieval-augmented context for agent execution and persistent
storage of execution traces.

The MemoryManager is the single interface used by the MetaOrchestrator
to interact with the memory subsystem — it abstracts away ChromaDB,
embeddings, and short-term state.
"""

import uuid
from typing import Any, Dict, List

from memory.short_term_memory import ShortTermMemory
from memory.vector_store import VectorStore
from utils.logger import setup_logger


class MemoryManager:
    """Coordinates semantic memory retrieval and execution trace storage.

    Wraps the VectorStore and ShortTermMemory to provide a clean
    interface for the orchestration pipeline.

    Attributes:
        vector_store: The persistent ChromaDB-backed vector store.
        short_term: The session-scoped in-memory state.
    """

    def __init__(self) -> None:
        """Initialize the memory manager with vector store and short-term memory."""
        self.logger = setup_logger("MemoryManager")
        self.vector_store = VectorStore()
        self.short_term = ShortTermMemory()
        self.logger.info("Memory Manager initialized.")

    def retrieve_context(self, scenario: str) -> List[str]:
        """Retrieve relevant past execution traces for a scenario.

        Performs semantic similarity search against all stored execution
        traces to find the most relevant past scenarios.

        Args:
            scenario: The current scenario text.

        Returns:
            A list of relevant past execution trace strings.
        """
        self.logger.info("Retrieving memory context for scenario...")
        context = self.vector_store.retrieve_similar(scenario, top_k=3)
        self.logger.info(f"Memory context retrieved: {len(context)} relevant trace(s).")
        return context

    def save_execution_trace(
        self,
        scenario: str,
        agents: List[str],
        results: List[Dict[str, Any]],
    ) -> None:
        """Save a complete execution trace to persistent memory.

        Combines scenario, agent list, and results into a single text
        block, embeds it, and stores it in the vector database.

        Args:
            scenario: The executed scenario text.
            agents: List of agent names in execution order.
            results: List of per-agent result dictionaries.
        """
        # Build combined trace text
        results_text = "\n".join(
            f"  - {r.get('agent', 'Unknown')}: {r.get('summary', 'No summary')}"
            for r in results
        )

        trace_text = (
            f"Scenario: {scenario}\n"
            f"Agents: {', '.join(agents)}\n"
            f"Results:\n{results_text}"
        )

        execution_id = str(uuid.uuid4())

        self.vector_store.store_execution(
            execution_id=execution_id,
            content=trace_text,
            metadata={"scenario": scenario},
        )

        self.logger.info(
            f"Execution trace saved (id={execution_id}, {len(trace_text)} chars)."
        )

    def init_session(self, scenario: str) -> None:
        """Initialize a new short-term memory session.

        Args:
            scenario: The scenario text for this execution session.
        """
        self.short_term = ShortTermMemory(scenario=scenario)
        self.logger.debug("Short-term memory session initialized.")
