# Dynamic Scenario-Driven Multi-Agent Orchestration Framework

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
├── chroma_storage/               # ChromaDB persistent data (auto-generated)
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
├──────────┬──────────┬──────────┬─────────────────────────────┤
│  LLM     │  Agent   │  Depend. │  Agent                     │
│  Service │  Factory │  Resolver│  Registry                   │
├──────────┴──────────┴──────────┴─────────────────────────────┤
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

### ✅ Phase 4 — Interactive Dashboard & API
- FastAPI backend with SSE real-time streaming
- Next.js + Tailwind CSS + Framer Motion frontend
- React Flow interactive agent dependency graph with hover tooltips
- Pipeline progress visualization (6-step animated bar)
- Multi-model selector (6 Groq LLM models)
- Topological execution order visualization
- Agent reasoning timeline with tracing beam

### 🔲 Planned
- FIPA ACL-style structured inter-agent messaging
- CTDE coordination strategy
- Quantitative evaluation metrics
- Multi-turn agent dialogue

## Research Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | Foundational Architecture Setup | ✅ Complete |
| **Phase 2** | Dynamic Agent Synthesis & LLM Integration | ✅ Complete |
| **Phase 3** | Memory Integration & RAG Reasoning | ✅ Complete |
| **Phase 4** | Interactive Dashboard & API | ✅ Complete |
| **Phase 5** | ACL Messaging & Evaluation Pipeline | 🔲 Planned |

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python, FastAPI, Uvicorn, SSE-Starlette |
| **LLM** | Groq API (OpenAI-compatible), LLaMA 3.3 70B |
| **Memory** | ChromaDB, SentenceTransformers (all-MiniLM-L6-v2) |
| **Frontend** | Next.js 16, React, TypeScript, Tailwind CSS v4 |
| **Visualization** | React Flow, Framer Motion, Lucide Icons |
| **Algorithms** | Kahn's Topological Sort, Retrieval-Augmented Generation |

## License

This project is developed for academic and research purposes.
