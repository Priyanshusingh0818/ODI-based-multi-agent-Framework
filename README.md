# Dynamic Scenario-Driven Multi-Agent Orchestration Framework
# Adaptive orchestration new novelty
A research-oriented framework for dynamic, scenario-driven multi-agent orchestration. The system analyzes complex real-world scenarios using LLMs, synthesizes specialized agent teams on-the-fly, resolves execution dependencies via topological sort, and coordinates their execution using memory-augmented reasoning — all visualized through a real-time interactive dashboard.

## Research Vision

| Capability | Description |
|---|---|
| **Dynamic Agent Creation** | Runtime synthesis of role-specific agents based on LLM-driven scenario analysis |
| **Meta-Orchestrator** | Central coordinator that decomposes scenarios, delegates tasks, and aggregates results |
| **Memory-Augmented Reasoning** | ChromaDB + SentenceTransformers RAG pipeline for adaptive, experience-informed decisions |
| **Dependency Resolution** | Kahn's algorithm (BFS topological sort) for safe multi-agent execution ordering |
| **Real-Time Dashboard** | Next.js + React Flow interactive UI with SSE streaming from FastAPI backend |
| **Multi-Model Support** | Selectable Groq LLM models (LLaMA 3.3 70B, Mixtral, Gemma 2, etc.) |

## Project Structure

```
project/
│
├── api/                          # FastAPI backend (Phase 4)
│   ├── __init__.py
│   └── main.py                   # SSE endpoint for real-time streaming
│
├── frontend/                     # Next.js dashboard (Phase 4)
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx        # Root layout with Inter font
│   │   │   ├── page.tsx          # Main dashboard UI
│   │   │   └── globals.css       # Tailwind + custom styles
│   │   └── lib/
│   │       └── utils.ts          # Utility functions
│   ├── package.json
│   └── tailwind.config.ts
│
├── orchestrator/
│   └── meta_orchestrator.py      # Core pipeline with event callbacks
│
├── agents/
│   ├── base_agent.py             # LLM-powered agent with memory context
│   ├── agent_factory.py
│   └── role_templates.py
│
├── llm/
│   └── llm_service.py            # Groq LLM integration + agent reasoning
│
├── factory/
│   └── agent_factory.py          # Agent instantiation from LLM output
│
├── registry/
│   └── agent_registry.py         # Centralized agent storage
│
├── dependency/
│   └── dependency_resolver.py    # Kahn's topological sort
│
├── execution/                    # Distributed Execution Layer (Phase 4)
│   ├── async_executor.py         # Asyncio-based topological executor
│   ├── message_broker.py         # Real-time ACL message brokering
│   ├── message_schema.py         # FIPA-ACL performative schemas
│   ├── execution_logger.py       # Centralized demo logging
│   └── performance_monitor.py    # Latency tracking and efficiency gains
│
├── communication/
│   └── acl_protocol.py           # FIPA ACL messaging (placeholder)
│
├── memory/
│   ├── embedding_service.py      # SentenceTransformers embeddings
│   ├── vector_store.py           # ChromaDB persistent store
│   ├── short_term_memory.py      # Session-scoped working memory
│   ├── memory_manager.py         # RAG integration layer
│   ├── short_term.py             # Phase 1 placeholder
│   └── long_term.py              # Phase 1 placeholder
│
├── evaluation/
│   └── metrics.py                # Performance metrics (placeholder)
│
├── scenarios/
│   └── sample_scenarios.txt      # Test scenarios
│
├── utils/
│   ├── logger.py                 # Structured logging
│   └── config.py                 # Centralized configuration
│
├── adaptation/                   # Adaptive Learning Layer (Phase 5)
│   ├── retrieval_engine.py       # Semantic similarity workflow retrieval
│   ├── workflow_adapter.py       # LLM-driven workflow adaptation
│   ├── feedback_loop.py          # Execution evaluation + CTDE feedback
│   ├── ctde_coordinator.py       # Centralized Training, Decentralized Execution
│   ├── dialogue_manager.py       # Multi-turn agent dialogue controller
│   └── learning_store.py         # Persistent policy & insight storage
│
├── chroma_storage/               # ChromaDB persistent data (auto-generated)
├── learning_data/                # CTDE learned policies (auto-generated)
├── main.py                       # CLI entry point
├── requirements.txt
├── .env                          # API keys (not committed)
└── README.md
```

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    Next.js Frontend (React Flow)             │
│   Pipeline Progress · Agent Graph · Memory Panel · Logs     │
├──────────────────────────────────────────────────────────────┤
│                  Server-Sent Events (SSE)                    │
├──────────────────────────────────────────────────────────────┤
│                    FastAPI Backend                            │
│              /api/orchestrate?scenario=...&model=...         │
├──────────────────────────────────────────────────────────────┤
│                    Meta-Orchestrator                          │
│      (memory → LLM → agents → resolve → execute → save)     │
├──────────┬──────────┬──────────┬──────────┬──────────────────┤
│  LLM     │  Agent   │  Depend. │  Async   │ Agent            │
│  Service │  Factory │  Resolver│ Executor │ Registry         │
├──────────┴──────────┴──────────┴──────────┴──────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ Agent A  │  │ Agent B  │  │ Agent N  │   (LLM + Memory)  │
│  └──────────┘  └──────────┘  └──────────┘                   │
├──────────────────────────────────────────────────────────────┤
│                    Memory Manager                            │
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │ Short-Term  │  │  Vector Store (ChromaDB +            │   │
│  │ (session)   │  │  SentenceTransformers all-MiniLM-L6) │   │
│  └─────────────┘  └─────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API key ([console.groq.com](https://console.groq.com))

### 1. Clone & Configure

```bash
# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### 2. Install Python Dependencies

```bash
python -m pip install python-dotenv openai chromadb sentence-transformers fastapi uvicorn sse-starlette
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Run the Backend (Terminal 1)

```bash
python -m uvicorn api.main:app --port 8000
```

### 5. Run the Frontend (Terminal 2)

```bash
cd frontend && npm run dev
```

### 6. Open Dashboard

Navigate to **http://localhost:3000** and enter a scenario.

### CLI Mode (without frontend)

```bash
python main.py
```

## Frontend Dashboard Features

The interactive dashboard provides real-time visibility into the orchestration pipeline:

| Feature | Description |
|---------|-------------|
| **Pipeline Progress Bar** | 6-step animated progress indicator (Initialize → Memory → Agents → Dependencies → Execute → Complete) |
| **Memory Retrieval Panel** | Shows ChromaDB vector search results with RAG context injection labels |
| **Agent Dependency Graph** | Large, interactive React Flow graph with drag, zoom, and **hover tooltips** showing responsibilities, dependencies, and execution results |
| **Topological Order Chain** | Visual representation of Kahn's algorithm output |
| **Agent Reasoning Log** | Timeline of LLM reasoning outputs with tracing beam animation |
| **Model Selector** | Dropdown to choose Groq models (LLaMA 3.3 70B, LLaMA 3.1 8B, Mixtral, Gemma 2) |
| **Completion Summary** | Stats card showing agents synthesized, executed, and trace saved |

## Supported Groq Models

| Model | Context | Best For |
|-------|---------|----------|
| LLaMA 3.3 70B Versatile | 128K | Complex scenarios (recommended) |
| LLaMA 3.1 8B Instant | 128K | Fast iteration & testing |
| LLaMA 3 70B | 8K | Strong reasoning |
| LLaMA 3 8B | 8K | Lightweight tasks |
| Gemma 2 9B | 8K | Balanced performance |
| Mixtral 8x7B | 32K | Large context scenarios |

## Folder & File Reference

### 📂 `api/` — FastAPI Backend
| File | Purpose |
|------|---------|
| `main.py` | SSE endpoint `/api/orchestrate` that runs `MetaOrchestrator` in a background thread and streams real-time events (status, memory_retrieved, agents_designed, dependency_resolved, agent_executing, agent_completed, orchestration_completed) to the frontend. Supports `model` query parameter for runtime LLM selection. |

### 📂 `frontend/` — Next.js Dashboard
| File | Purpose |
|------|---------|
| `src/app/page.tsx` | Main React component with SSE client, React Flow graph, pipeline progress bar, agent hover tooltips, model selector, and execution log |
| `src/app/layout.tsx` | Root layout with Inter font via `next/font/google` |
| `src/app/globals.css` | Tailwind CSS v4 config with custom animations |

### 📂 `orchestrator/`
| File | Purpose |
|------|---------|
| `meta_orchestrator.py` | Core pipeline: retrieve memory → LLM agent design → create agents → register → resolve dependencies → execute with memory context → save trace. Accepts `event_callback` for SSE streaming. |

### 📂 `agents/`
| File | Purpose |
|------|---------|
| `base_agent.py` | `BaseAgent` with LLM-powered `execute()` that receives memory context and delegates reasoning to `LLMService.reason_as_agent()` |

### 📂 `llm/`
| File | Purpose |
|------|---------|
| `llm_service.py` | Groq integration with structured system prompt for agent design. Includes `reason_as_agent()` for per-agent LLM reasoning with memory context. |

### 📂 `memory/`
| File | Purpose |
|------|---------|
| `embedding_service.py` | Singleton SentenceTransformers (`all-MiniLM-L6-v2`) |
| `vector_store.py` | ChromaDB persistent client for execution trace storage/retrieval |
| `short_term_memory.py` | In-memory session state |
| `memory_manager.py` | RAG integration: `retrieve_context()` + `save_execution_trace()` |

### 📂 `dependency/`
| File | Purpose |
|------|---------|
| `dependency_resolver.py` | Kahn's algorithm (BFS topological sort) with circular dependency detection |

### 📂 `execution/` (Phase 4)
| File | Purpose |
|------|---------|
| `async_executor.py` | Core engine identifying parallel execution levels and routing execution via `asyncio.gather`. Maintains strict DAG correctness while boosting efficiency. |
| `message_broker.py` | Async queue system enabling real-time Agent Communication Language (ACL) event-driven messaging. |
| `message_schema.py` | Defines `Message` format with performatives (`INFORM`, `REQUEST`, `FAIL`), sender, receiver, and timestamps. |
| `execution_logger.py` | Generates a clean, transparent log of pipeline events, group parallelism, and inter-agent messages. |
| `performance_monitor.py` | Tracks total execution time vs sequential estimation, calculating efficiency gain metrics. |

---

## Implementation Status

### ✅ Phase 1 — Foundational Architecture
- Modular project structure with logging, config, and entry point
- Base Agent abstraction and placeholder modules

### ✅ Phase 2 — Dynamic Agent Synthesis & LLM Integration
- LLM Service with Groq API for scenario analysis
- Dynamic agent creation from LLM JSON output
- Agent Registry, Factory, and Dependency Resolver
- Full Meta-Orchestrator pipeline

### ✅ Phase 3 — Memory-Augmented Intelligence (RAG)
- SentenceTransformers embeddings + ChromaDB vector store
- Memory Manager with context retrieval and trace storage
- LLM-driven per-agent reasoning with memory context
- Adaptive behavior across runs via semantic similarity

### ✅ Phase 4 — Distributed Execution & Interactive Dashboard
- **Execution Layer:** `async_executor` running decoupled multi-agent parallel workflows using topological graph levels.
- **Agent Communication (ACL):** Real-time message broking for Inter-Agent messaging via `message_broker.py`.
- **Fault-Tolerance:** Agents emit `FAIL` ACL signals handling internal LLM exceptions cleanly without pipeline crashes.
- **Monitoring:** Performance efficiency metrics and clear `execution_logger` trace generation.
- **Frontend Dashboard:** Next.js + Tailwind CSS with SSE streaming, React Flow graph with hover tooltips, multi-agent pipeline progress visualization.

### ✅ Phase 5 — Adaptive Learning, CTDE & Multi-Agent Dialogue
- **CTDE (Centralized Training, Decentralized Execution):** System learns globally from all workflow executions, then provides decentralized policy hints to individual agents. Policies include best practices, common failures, and optimal patterns stored via `learning_store.py`.
- **Multi-Turn Agent Dialogue:** Agents no longer respond in single shots — dependent agent pairs engage in iterative conversations (REQUEST → INFORM → REQUEST → CONFIRM) via `dialogue_manager.py` to collaboratively refine decisions.
- **Enhanced Feedback Loop:** `feedback_loop.py` now produces structured evaluation summaries (success rate, slow/fast agents, recommendations) and feeds data into the CTDE coordinator for centralized training.
- **Learning Store:** Persistent JSON-based storage (`learning_data/policies.json`) for CTDE policies and execution insights, enabling continuous improvement across runs.
- **Policy-Aware Workflow Adaptation:** `workflow_adapter.py` now incorporates CTDE policy hints into LLM prompts when adapting past workflows to new scenarios.
- **Enriched Agent Reasoning:** `base_agent.py` receives CTDE policy hints and dialogue history as additional LLM context for smarter, experience-informed execution.

## Research Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Foundational Architecture Setup | ✅ Complete |
| **Phase 2** | Dynamic Agent Synthesis & LLM Integration | ✅ Complete |
| **Phase 3** | Memory Integration & RAG Reasoning | ✅ Complete |
| **Phase 4** | Distributed Execution & Interactive Dashboard | ✅ Complete |
| **Phase 5** | CTDE Strategy, Multi-Turn Dialogue & Adaptive Learning | ✅ Complete |

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python, FastAPI, Uvicorn, SSE-Starlette |
| **LLM** | Groq API (OpenAI-compatible), LLaMA 3.3 70B |
| **Memory** | ChromaDB, SentenceTransformers (all-MiniLM-L6-v2) |
| **Learning** | CTDE Coordinator, Learning Store (JSON), Feedback Loop |
| **Frontend** | Next.js 16, React, TypeScript, Tailwind CSS v4 |
| **Visualization** | React Flow, Framer Motion, Lucide Icons |
| **Algorithms** | Kahn's Topological Sort, Retrieval-Augmented Generation, CTDE |

## License

This project is developed for academic and research purposes.

python -m uvicorn api.main:app --port 8000

