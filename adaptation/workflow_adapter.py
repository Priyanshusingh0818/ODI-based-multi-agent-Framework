import json
from typing import Any, Dict, List, Optional
from utils.logger import setup_logger

class WorkflowAdapter:
    """Adapts proven workflows to new scenarios using LLM entity substitution."""
    
    def __init__(self, llm_service):
        self.llm = llm_service
        self.logger = setup_logger("WorkflowAdapter")

    def adapt_workflow(
        self, 
        past_agent_configs: List[Dict[str, Any]], 
        old_scenario: str, 
        new_scenario: str,
        policy_hints: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Uses the LLM to intelligently modify role names, responsibilities, 
        and goals based on new scenario entities while preserving the DAG structure.
        Optionally includes CTDE policy hints for improved adaptation.
        """
        self.logger.info("Adapting past workflow to new scenario constraints...")
        
        # Phase 5: Build policy context if available
        policy_context = ""
        if policy_hints:
            policy_lines = []
            for role, policy in policy_hints.items():
                practices = policy.get("best_practices", [])[:2]
                failures = policy.get("common_failures", [])[:2]
                if practices or failures:
                    policy_lines.append(f"  {role}: Best practices: {practices}. Known failures: {failures}.")
            if policy_lines:
                policy_context = "\n\nCTDE LEARNED POLICIES (use these to improve the adaptation):\n" + "\n".join(policy_lines)
                self.logger.info(f"Including CTDE policy hints from {len(policy_hints)} roles.")
        
        prompt = f"""
        You are an expert System Architect. Your task is to adapt an existing multi-agent workflow 
        to fit a new scenario. You MUST strictly preserve the number of agents and their exact dependency structures.
        Only adapt the agent names (slightly, if needed), roles, and responsibilities to match the new context.
        
        OLD SCENARIO:
        {old_scenario}
        
        NEW SCENARIO:
        {new_scenario}
        
        PAST WORKFLOW GRAPH (JSON):
        {json.dumps(past_agent_configs, indent=2)}
        {policy_context}
        
        Provide your response as a valid JSON array matching the exact schema of the PAST WORKFLOW GRAPH.
        Ensure every agent still explicitly declares the same 'dependencies' lists mapped to the new agent names.
        Return ONLY valid JSON.
        """
        
        # We use the generic adapt_graph function from the LLM service
        response = self.llm.adapt_graph(prompt)
        
        try:
            # Strip markdown formatting if any
            clean_json = response.replace("```json", "").replace("```", "").strip()
            adapted_configs = json.loads(clean_json)
            self.logger.info(f"Successfully adapted {len(adapted_configs)} agent configurations.")
            return adapted_configs
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode adapted JSON: {e}. Falling back to original configs.")
            # Fallback to the original configs if LLM fails formatting
            return past_agent_configs
