"""
Meta-Orchestrator for the Multi-Agent Orchestration Framework.

The Meta-Orchestrator is the central coordination entity that implements
the full memory-augmented dynamic agent synthesis pipeline:

  1. Receive scenario description
  2. Retrieve memory context from past executions
  3. Call LLM service for scenario analysis
  4. Create agents dynamically via AgentFactory
  5. Register agents in AgentRegistry
  6. Resolve execution order via DependencyResolver
  7. Execute agents with memory context (LLM reasoning)
  8. Save execution trace to vector store
  9. Collect and return structured results
"""

from typing import Any, Dict, List

from dependency.dependency_resolver import DependencyResolver
from factory.agent_factory import create_agent
from llm.llm_service import LLMService
from memory.memory_manager import MemoryManager
from registry.agent_registry import AgentRegistry
from utils.logger import setup_logger


class MetaOrchestrator:
    """Central orchestrator that coordinates memory-augmented multi-agent execution.

    Implements the complete pipeline: memory retrieval, LLM-driven scenario
    analysis, runtime agent synthesis, dependency-ordered execution with
    memory context, result aggregation, and execution trace storage.
    """

    def __init__(self) -> None:
        """Initialize the Meta-Orchestrator and all subsystems."""
        self.logger = setup_logger("MetaOrchestrator")
        self.llm_service = LLMService()
        self.registry = AgentRegistry()
        self.dependency_resolver = DependencyResolver()
        self.memory_manager = MemoryManager()
        self.logger.info("Meta-Orchestrator initialized (Phase 3 — Memory-Augmented).")

    def execute(
        self, scenario_text: str, event_callback: Any = None
    ) -> Dict[str, Any]:
        """Run the full memory-augmented orchestration pipeline.

        Args:
            scenario_text: A natural-language scenario description.
            event_callback: Optional callable to emit real-time events.

        Returns:
            A dictionary containing the scenario, agents created,
            execution order, memory context used, and per-agent results.
        """
        self.logger.info(f"Scenario received: {scenario_text}")
        if event_callback:
            event_callback("status", {"step": "Initializing pipeline..."})

        # Step 1: Retrieve memory context from past executions
        self.logger.info("Step 1 — Retrieving memory context...")
        if event_callback:
            event_callback("status", {"step": "Retrieving memory context..."})
        memory_context: List[str] = self.memory_manager.retrieve_context(
            scenario_text
        )
        self.memory_manager.init_session(scenario_text)
        if event_callback:
            event_callback("memory_retrieved", {"context": memory_context})

        # Step 2: LLM-driven scenario analysis
        self.logger.info("Step 2 — Calling LLM for scenario analysis...")
        if event_callback:
            event_callback("status", {"step": "Analyzing scenario with LLM..."})
        agent_configs: List[Dict[str, Any]] = self.llm_service.analyze_scenario(
            scenario_text
        )
        if event_callback:
            event_callback("agents_designed", {"agents": agent_configs})

        # Step 3: Create agents via AgentFactory
        self.logger.info("Step 3 — Creating agents dynamically...")
        if event_callback:
            event_callback("status", {"step": "Creating agents..."})
        for config in agent_configs:
            agent = create_agent(config)
            self.registry.register_agent(agent)

        # Step 4: Resolve dependency-based execution order
        self.logger.info("Step 4 — Resolving dependency execution order...")
        if event_callback:
            event_callback("status", {"step": "Resolving dependencies..."})
        execution_order: List[str] = self.dependency_resolver.resolve(agent_configs)
        if event_callback:
            event_callback("dependency_resolved", {"order": execution_order})

        # Step 5: Execute agents in order with memory context
        self.logger.info("Step 5 — Executing agents with memory context...")
        results: List[Dict[str, Any]] = []
        context: Dict[str, Any] = {"scenario": scenario_text}

        for agent_name in execution_order:
            agent = self.registry.get_agent(agent_name)
            if agent is None:
                self.logger.error(f"Agent '{agent_name}' not found in registry.")
                continue

            if event_callback:
                event_callback("agent_executing", {"agent": agent_name})

            result = agent.execute(context, memory_context)
            results.append(result)

            if event_callback:
                event_callback("agent_completed", {"result": result})

            # Store in short-term memory and feed into downstream context
            self.memory_manager.short_term.store_agent_output(agent_name, result)
            context[agent_name] = result

        # Step 6: Save execution trace to persistent memory
        self.logger.info("Step 6 — Saving execution trace to vector store...")
        if event_callback:
            event_callback("status", {"step": "Saving execution trace..."})
        self.memory_manager.save_execution_trace(
            scenario=scenario_text,
            agents=execution_order,
            results=results,
        )

        # Step 7: Aggregate and return results
        response: Dict[str, Any] = {
            "scenario": scenario_text,
            "agents_created": len(agent_configs),
            "execution_order": execution_order,
            "memory_context_used": memory_context,
            "results": results,
        }

        self.logger.info(
            f"Orchestration complete — {len(results)} agent(s) executed, "
            f"memory context entries used: {len(memory_context)}."
        )
        if event_callback:
            event_callback("orchestration_completed", response)
            
        return response
