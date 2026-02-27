# Dynamic Scenario-Driven Multi-Agent Orchestration Framework

A research-oriented framework for dynamic, scenario-driven multi-agent orchestration. The system analyzes complex real-world scenarios, synthesizes specialized agent teams on-the-fly, and coordinates their execution using structured communication protocols and memory-aware strategies.

## Research Vision

| Capability | Description |
|---|---|
| **Dynamic Agent Creation** | Runtime synthesis of role-specific agents based on LLM-driven scenario analysis |
| **Meta-Orchestrator** | Central coordinator that decomposes scenarios, delegates tasks, and aggregates results |
| **ACL-style Communication** | FIPA ACL-inspired structured messaging protocol for inter-agent dialogue |
| **CTDE Strategy** | Centralized Training, Decentralized Execution — agents train with global state but execute autonomously |
| **Memory-Aware Coordination** | Short-term working memory and long-term vector-backed knowledge persistence |
| **System-Level Evaluation** | Quantitative metrics for task completion, communication efficiency, and coordination overhead |

## Project Structure

```
project/
│
├── orchestrator/
│   └── meta_orchestrator.py
│
├── agents/
│   ├── base_agent.py
│   ├── agent_factory.py
│   └── role_templates.py
│
├── llm/
│   └── llm_service.py
│
├── factory/
│   └── agent_factory.py
│
├── registry/
│   └── agent_registry.py
│
├── dependency/
│   └── dependency_resolver.py
│
├── communication/
│   └── acl_protocol.py
│
├── memory/
│   ├── short_term.py
│   └── long_term.py
│
├── evaluation/
│   └── metrics.py
│
├── scenarios/
│   └── sample_scenarios.txt
│
├── utils/
│   ├── logger.py
│   └── config.py
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## Folder & File Reference

### 📂 `orchestrator/`
The brain of the system — coordinates the entire multi-agent pipeline.

| File | Purpose |
|------|---------|
| `meta_orchestrator.py` | Central coordinator that receives a scenario, calls the LLM service, creates agents via the factory, resolves dependencies, executes agents in order, and aggregates results into a structured JSON response. |

---

### 📂 `agents/`
Defines what an agent *is* and how it behaves.

| File | Purpose |
|------|---------|
| `base_agent.py` | The `BaseAgent` class — every dynamically created agent is an instance of this. Holds `name`, `role`, `responsibilities`, `dependencies`, `status`, and an `execute()` method that logs task completion and returns a structured result. |
| `agent_factory.py` | *(Phase 1 placeholder)* Reserved for original agent factory design. Superseded by `factory/agent_factory.py` in Phase 2. |
| `role_templates.py` | *(Placeholder)* Will store reusable role templates (e.g., "planner", "executor") for LLM-powered role inference in future phases. |

---

### 📂 `llm/`
Handles all communication with external language models.

| File | Purpose |
|------|---------|
| `llm_service.py` | `LLMService` class that sends the scenario to Groq (via OpenAI-compatible API) with a structured system prompt. Parses the LLM's JSON response, extracts agent designs, and validates the schema (name, role, responsibilities, dependencies). Handles markdown code fences and malformed output gracefully. |

---

### 📂 `factory/`
Responsible for turning LLM output into live agent objects.

| File | Purpose |
|------|---------|
| `agent_factory.py` | `create_agent()` function that takes a single agent config dictionary (from the LLM) and instantiates a `BaseAgent` with the correct name, role, responsibilities, and dependencies. |

---

### 📂 `registry/`
Centralized storage for all agents created during a scenario run.

| File | Purpose |
|------|---------|
| `agent_registry.py` | `AgentRegistry` class with `register_agent()`, `get_agent()`, and `list_agents()` methods. Backed by a dictionary for O(1) lookup by agent name. Prevents duplicate registrations. |

---

### 📂 `dependency/`
Determines the correct execution order for agents.

| File | Purpose |
|------|---------|
| `dependency_resolver.py` | `DependencyResolver` class that builds a directed acyclic graph (DAG) from agent dependency declarations and performs **Kahn's algorithm** (BFS topological sort) to compute execution order. Raises a `ValueError` if circular dependencies are detected. Gracefully skips external dependencies not in the agent set. |

---

### 📂 `communication/`
*(Placeholder for future phases)*

| File | Purpose |
|------|---------|
| `acl_protocol.py` | Will implement FIPA ACL-style structured messaging (INFORM, REQUEST, PROPOSE, etc.) for inter-agent communication. |

---

### 📂 `memory/`
Semantic memory layer — persistent execution memory + session state.

| File | Purpose |
|------|---------|
| `embedding_service.py` | Singleton `EmbeddingService` using SentenceTransformers (`all-MiniLM-L6-v2`). Converts text to dense vector embeddings for semantic similarity search. Model loaded once and reused. |
| `vector_store.py` | `VectorStore` wrapping `chromadb.PersistentClient` at `./chroma_storage`. Stores execution traces with metadata (scenario, timestamp) and retrieves semantically similar past executions via `retrieve_similar()`. |
| `short_term_memory.py` | `ShortTermMemory` — pure in-memory dict storing agent outputs and intermediate state for a single session. Cleared between runs. |
| `memory_manager.py` | `MemoryManager` — core integration layer. `retrieve_context()` fetches relevant past traces before execution. `save_execution_trace()` embeds and stores completed runs. Abstracts away ChromaDB/embeddings from the orchestrator. |
| `short_term.py` | *(Phase 1 placeholder)* Original placeholder for working memory. |
| `long_term.py` | *(Phase 1 placeholder)* Original placeholder for vector-backed persistence. |

---

### 📂 `evaluation/`
*(Placeholder for future phases)*

| File | Purpose |
|------|---------|
| `metrics.py` | Will compute system-level performance metrics: task completion rate, communication efficiency, agent utilization, coordination overhead, and adaptability score. |

---

### 📂 `scenarios/`
Test data for the framework.

| File | Purpose |
|------|---------|
| `sample_scenarios.txt` | Example scenario descriptions (urban search & rescue, collaborative research, supply chain disruption) for testing the orchestration pipeline. |

---

### 📂 `utils/`
Shared utilities used across all components.

| File | Purpose |
|------|---------|
| `logger.py` | `setup_logger()` function that creates loggers with console + file output (`logs/system.log`). Format: `[timestamp] [LEVEL] [component] message`. Supports INFO, DEBUG, ERROR levels. |
| `config.py` | `Config` class with project constants: name, version, phase, LLM provider/model, API key, embedding model, ChromaDB storage path and collection name (loaded from `.env` via `python-dotenv`). |

---

### 📄 Root Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point — prints the banner, accepts scenario input from the user, calls `MetaOrchestrator.execute()`, and prints the structured JSON response. |
| `requirements.txt` | Python dependencies (`python-dotenv`, `openai`, `chromadb`, `sentence-transformers`, `numpy`). |
| `.env` | Stores API keys (e.g., `GROQ_API_KEY`). **Not committed to version control.** |
| `README.md` | This file — project documentation, architecture overview, and implementation status. |

## Quick Start

### Prerequisites
- Python 3.9+
- Groq API key (set in `.env`)

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Running

```bash
python main.py
```

You will see:

```
================================================================
  Dynamic Scenario-Driven Multi-Agent Orchestration Framework
  Phase 2 – Dynamic Agent Synthesis Active
================================================================

Enter scenario:
```

After entering a scenario (e.g., "Massive fire outbreak in metro station"), the system:
1. Sends the scenario to the LLM for agent design
2. Dynamically creates the proposed agents
3. Resolves dependency-based execution order
4. Executes agents in order
5. Returns structured JSON results:

```json
{
  "scenario": "Massive fire outbreak in metro station",
  "agents_created": 4,
  "execution_order": [
    "Fire Suppression Agent",
    "Police Coordination Agent",
    "Medical Response Agent",
    "Evacuation Management Agent"
  ],
  "results": [
    {
      "agent": "Fire Suppression Agent",
      "status": "completed",
      "summary": "..."
    }
  ]
}
```

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│              Meta-Orchestrator              │
│  (memory → LLM → agents → execute → save) │
├──────────┬──────────┬──────────────────────┤
│  LLM     │  Agent   │  Dependency          │
│  Service │  Factory │  Resolver            │
├──────────┴──────────┴──────────────────────┤
│            Agent Registry                   │
├─────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ Agent A  │ │ Agent B  │ │ Agent N  │    │
│  │ (LLM +   │ │ (LLM +   │ │ (LLM +   │    │
│  │ memory)  │ │ memory)  │ │ memory)  │    │
│  └──────────┘ └──────────┘ └──────────┘    │
├─────────────────────────────────────────────┤
│           Memory Manager                    │
│  ┌─────────────┐  ┌──────────────────────┐  │
│  │ Short-Term  │  │  Vector Store        │  │
│  │ (session)   │  │  (ChromaDB +         │  │
│  │             │  │   SentenceTransformers│  │
│  └─────────────┘  └──────────────────────┘  │
├─────────────────────────────────────────────┤
│         Future: ACL & Metrics               │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Phase 1 Implementation Status

### ✅ Implemented in Phase 1

- Modular research-grade project architecture
- Meta-Orchestrator skeleton (scenario reception and structured logging)
- Base Agent abstraction (`receive`, `act`, `send` interface)
- Structured logging framework (console + file with `[timestamp] [LEVEL] [component]` format)
- Execution entry point (`main.py`)
- Placeholder modules aligned with research roadmap

---

## � Phase 2 Implementation Status

### ✅ Implemented in Phase 2

- **LLM Service** — Groq integration via OpenAI-compatible API for scenario analysis
- **Dynamic BaseAgent** — Runtime agent class with `name`, `role`, `responsibilities`, `dependencies`, `execute()`
- **AgentFactory** — `create_agent()` instantiates agents from LLM JSON output
- **AgentRegistry** — Centralized agent storage with `register`, `get`, `list` operations
- **DependencyResolver** — Topological sort (Kahn's algorithm) with circular dependency detection
- **Meta-Orchestrator** — Full pipeline: scenario → LLM → create → register → resolve → execute → results
- **Structured prompt engineering** for reliable JSON agent design output

### 🔲 Not Implemented Yet (as of Phase 2)

- ACL-style structured messaging
- Vector database integration → ✅ Implemented in Phase 3
- Evaluation metrics computation
- Multi-turn agent communication

> Phase 2 delivers fully dynamic, LLM-driven agent synthesis where the number and type of agents is determined entirely by the scenario at runtime.

---

## 🧠 Phase 3 Implementation Status — Memory-Augmented Intelligence

Phase 3 transforms the system from **reactive** to **adaptive**. Agents now learn from past executions and use retrieval-augmented reasoning to produce more intelligent, context-aware responses.

### ✅ Implemented in Phase 3

- **Embedding Service** — Singleton `SentenceTransformers` (`all-MiniLM-L6-v2`) for semantic text embedding
- **Vector Store** — Local persistent `ChromaDB` at `./chroma_storage` for storing and retrieving execution traces
- **Short-Term Memory** — In-memory session state tracking agent outputs within a single run
- **Memory Manager** — Core integration layer: `retrieve_context()` before execution, `save_execution_trace()` after completion
- **LLM-Driven Agent Reasoning** — Each agent calls Groq LLM with memory context + role + responsibilities (no hardcoded behavior)
- **Memory-Augmented Orchestrator** — Full pipeline: retrieve memory → LLM → create → register → resolve → execute with memory → save trace
- **Adaptive Behavior** — System improves across runs by referencing semantically similar past scenarios

### 🔲 Not Implemented Yet

- ACL-style structured messaging
- CTDE coordination logic
- Evaluation metrics computation
- Multi-turn agent communication

> Phase 3 enables retrieval-augmented agent reasoning. Each execution trace is embedded and stored in ChromaDB. On subsequent runs, semantically similar past traces are retrieved and injected into agent prompts, enabling adaptive, experience-informed behavior.

---

## Research Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Foundational Architecture Setup | ✅ Complete |
| **Phase 2** | Dynamic Agent Synthesis & LLM Integration | ✅ Complete |
| **Phase 3** | Memory Integration & RAG Reasoning | ✅ Complete |
| **Phase 4** | ACL Messaging & Evaluation Pipeline | 🔲 Planned |

## License

This project is developed for academic and research purposes.
