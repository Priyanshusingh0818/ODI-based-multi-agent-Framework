# 🤖 Dynamic Scenario-Driven Multi-Agent Orchestration Framework

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LLM-GPT--4%20%7C%20LLaMA--3%20%7C%20Mixtral-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Research%20Project-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  A research-oriented multi-agent system that dynamically creates and orchestrates specialized AI agents at runtime — driven entirely by natural language scenario understanding.
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Motivation](#-motivation)
- [Key Contributions](#-key-contributions)
- [System Architecture](#-system-architecture)
- [Agent Types](#-agent-types)
- [Coordination Strategy](#-coordination-strategy)
- [Memory Design](#-memory-design)
- [Evaluation Metrics](#-evaluation-metrics)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Use Case Example](#-use-case-example)
- [Limitations](#-limitations)
- [Future Work](#-future-work)
- [Research Context](#-research-context)

---

## 🧭 Overview

This framework presents a **dynamic multi-agent system** where intelligent agents are automatically created at runtime based on the semantic understanding of an input scenario. 

Unlike traditional multi-agent systems that rely on predefined agent pools or static workflows, this project introduces a **Meta-Orchestrator Agent** that interprets scenarios using a Large Language Model (LLM) and dynamically synthesizes specialized agents to collaboratively solve complex tasks.

> **Focus:** System design, orchestration, coordination, and evaluation — not commercial deployment.

---

## 🎯 Motivation

Most existing agentic AI frameworks suffer from the same structural limitations:

- Require manually defined agents
- Use static, inflexible workflows
- Lack formal orchestration and system-level evaluation
- Over-rely on prompt engineering

This project addresses these gaps by proposing a **scenario-driven agent creation paradigm** where:

- Agents are instantiated **only when required**
- Roles are **inferred dynamically** from natural language
- Coordination is **centrally governed** but **executed in a decentralized manner**

---

## 🧩 Key Contributions

| Contribution | Description |
|---|---|
| **Dynamic Agent Creation** | Agents are synthesized at runtime from natural language scenarios |
| **Meta-Orchestrator Agent** | Central controller for global planning, role inference, and task decomposition |
| **Structured Communication** | ACL (Agent Communication Language) inspired inter-agent messaging |
| **CTDE Architecture** | Centralized Planning with Decentralized Execution |
| **Memory-Aware Coordination** | Short-term and long-term memory for context-aware reasoning |
| **System-Level Evaluation** | Metrics beyond output quality — coordination overhead, failure recovery, efficiency |

---

## 🏗️ System Architecture

```
Scenario (Text Input)
        │
        ▼
┌─────────────────────┐
│  Meta-Orchestrator  │  ◄── LLM-powered scenario understanding
│       Agent         │
└─────────────────────┘
        │
        ▼
 Role Inference &
 Task Decomposition
        │
        ▼
┌─────────────────────┐
│   Agent Factory     │  ◄── Dynamic instantiation from role templates
└─────────────────────┘
        │
        ▼
┌──────────────────────────────────────────┐
│           Specialized Agents             │
│  [ Planning | Resource | Domain | ... ]  │
└──────────────────────────────────────────┘
        │
        ▼
 Inter-Agent Communication
     (ACL-style JSON)
        │
        ▼
 Task Execution & Feedback
        │
        ▼
 Evaluation & Logging
```

---

## 🤖 Agent Types

The system does **not** use fixed agents. Instead, agents are created dynamically from role templates:

| Agent Type | Responsibility |
|---|---|
| **Planning Agent** | Breaks down high-level goals into executable sub-tasks |
| **Resource Coordination Agent** | Allocates and tracks shared resources across agents |
| **Monitoring Agent** | Tracks task progress and flags failures for reassignment |
| **Domain Execution Agents** | Scenario-specific agents (e.g., Emergency, Traffic, Medical) |

Each agent:
- Has a **dedicated, scoped responsibility**
- Communicates via **structured ACL-style messages**
- Reports status back to the **Meta-Orchestrator**

---

## 🔁 Coordination Strategy

The system implements a **Centralized Training with Decentralized Execution (CTDE)** paradigm:

**Centralized Planning**
> The Meta-Orchestrator performs scenario understanding, role inference, and initial task allocation.

**Decentralized Execution**
> Individual agents operate independently, executing their assigned tasks without requiring constant orchestrator intervention.

**Dynamic Failure Handling**
> Failed or stalled tasks are detected by the Monitoring Agent and dynamically reassigned to available or newly instantiated agents.

---

## 🧠 Memory Design

| Memory Type | Purpose |
|---|---|
| **Short-Term Memory** | Stores context, task state, and agent outputs within the current execution |
| **Long-Term Memory** | Persists past scenarios, coordination patterns, and historical agent outputs |

Memory is optionally backed by a **vector database** (FAISS or ChromaDB) to enable retrieval-augmented reasoning across executions.

---

## 🧪 Evaluation Metrics

The system is evaluated with **system-level metrics** enabling quantitative comparison across scenarios:

| Metric | What It Measures |
|---|---|
| **Task Completion Time** | End-to-end time from scenario input to result |
| **Agents Instantiated** | Total number of dynamic agents created |
| **Coordination Overhead** | Message volume and synchronization cost |
| **Failure Recovery Rate** | Proportion of failed tasks successfully reassigned |
| **Agent Utilization Efficiency** | Active vs. idle time across all agents |

---

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| LLM Backend | GPT-4 / LLaMA-3 / Mixtral |
| Agent Logic | Custom Python classes |
| Orchestration | Meta-Agent Controller |
| Communication Protocol | JSON + ACL-style messaging |
| Memory / Vector Store | FAISS / ChromaDB |
| Evaluation & Analytics | Python (custom metrics module) |
| Visualization | Matplotlib / NetworkX |

---

## 📂 Project Structure

```
project/
│
├── orchestrator/
│   └── meta_orchestrator.py       # Core Meta-Orchestrator Agent
│
├── agents/
│   ├── base_agent.py              # Abstract base class for all agents
│   ├── agent_factory.py           # Dynamic agent instantiation logic
│   └── role_templates.py          # Role definitions and configurations
│
├── communication/
│   └── acl_protocol.py            # ACL-style structured messaging
│
├── memory/
│   ├── short_term.py              # In-execution context memory
│   └── long_term.py               # Persistent vector store memory
│
├── evaluation/
│   └── metrics.py                 # System-level evaluation metrics
│
├── scenarios/
│   └── sample_scenarios.txt       # Example input scenarios
│
├── main.py                        # Entry point
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- An LLM API key (OpenAI, Together.ai, Groq, etc.) or a locally running model

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/dynamic-multi-agent-framework.git
cd dynamic-multi-agent-framework

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Set your LLM API credentials in a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
# or configure for local model endpoint
LLM_BASE_URL=http://localhost:11434
```

### Running

```bash
python main.py
```

You will be prompted to enter a scenario in natural language. The system will handle the rest — inferring roles, creating agents, executing tasks, and logging evaluation metrics.

> ⚠️ **Note:** This project is designed for **research experimentation**, not production deployment.

---

## 🌆 Use Case Example

**Scenario:** *"There is a fire accident in the downtown area causing severe traffic congestion and multiple medical emergencies."*

The Meta-Orchestrator interprets this scenario and dynamically instantiates:

```
├── Fire Response Agent       → Coordinates fire suppression resources
├── Medical Coordination Agent → Dispatches ambulances and medical personnel  
└── Traffic Management Agent  → Reroutes vehicles and clears emergency lanes
```

All three agents operate concurrently under the orchestrator's global plan, communicate via ACL messages, and report task status in real time.

---

## ⚠️ Limitations

- **LLM Dependency:** Role inference and task decomposition quality is bounded by the underlying LLM's reasoning ability.
- **No Domain Training:** Agents do not possess specialized domain knowledge beyond what the LLM provides.
- **Orchestration Focus:** This project prioritizes system architecture and coordination design — not model fine-tuning or training.
- **Computational Cost:** Scenarios with high complexity will instantiate more agents, increasing inference cost.

---

## 🔭 Future Work

- **Adaptive Role Evolution** — Allow agents to modify their own roles mid-execution based on feedback
- **Reinforcement Learning Integration** — Optimize orchestration strategies through reward-based training
- **Formal Verification** — Apply formal methods to verify coordination correctness
- **Multi-Scenario Benchmarking** — Standardized evaluation across diverse, complex scenarios
- **GUI Dashboard** — Real-time visualization of agent graphs and task progress

---

## 📚 Research Context

This project draws from and contributes to the following research areas:

- **Multi-Agent Systems (MAS)** — Theoretical foundations of agent coordination
- **Hierarchical Planning** — Decomposing complex goals into structured sub-tasks
- **Agent Communication Languages (ACLs)** — Formal agent messaging standards (e.g., FIPA-ACL)
- **CTDE (Centralized Training, Decentralized Execution)** — Popular paradigm from cooperative MARL
- **LLM-based Agent Reasoning** — Emergent planning and coordination from large language models

---

## 🎓 Academic Use

This repository is intended for:

- Academic research projects
- Multi-agent system studies
- Agentic AI exploration and experimentation
- Prototyping novel orchestration paradigms

---

## 📄 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

<p align="center">
  Built for research · Not for production · Contributions and citations welcome
</p>
