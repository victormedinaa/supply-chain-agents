# Autonomous Supply Chain Management System

A multi-agent system for intelligent supply chain orchestration built with **LangGraph** and **Python**.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-63%20passing-success.svg)](backend/tests/)

## Overview

This project implements an autonomous supply chain management platform using a network of specialized AI agents that collaborate to optimize operations across inventory, procurement, logistics, production, finance, and quality control domains.

### Key Features

- **Multi-Agent Architecture**: Six specialized agents working in coordination
- **LLM Integration**: Generative AI for negotiation, analysis, and decision support
- **Graph-Based Orchestration**: LangGraph for stateful agent workflows
- **Real-Time Optimization**: Route planning, demand forecasting, risk assessment

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                           │
│                     (LangGraph Core)                        │
└─────────────────────────────────────────────────────────────┘
         │           │           │           │
    ┌────▼────┐ ┌────▼────┐ ┌────▼────┐ ┌────▼────┐
    │Inventory│ │Procure- │ │Logistics│ │Produc-  │
    │  Agent  │ │  ment   │ │  Agent  │ │  tion   │
    └─────────┘ └─────────┘ └─────────┘ └─────────┘
                     │           │
                ┌────▼────┐ ┌────▼────┐
                │ Finance │ │ Quality │
                │  Agent  │ │  Agent  │
                └─────────┘ └─────────┘
```

## Agents

| Agent | Responsibility |
|-------|----------------|
| **Inventory** | Demand forecasting, safety stock optimization |
| **Procurement** | Supplier risk assessment, automated negotiation |
| **Finance** | Budget enforcement, cost variance analysis |
| **Logistics** | Route optimization, shipment tracking |
| **Quality** | Statistical process control, root cause analysis |
| **Production** | Scheduling, capacity planning |

## Project Structure

```
├── backend/
│   ├── src/
│   │   ├── core/           # State, config, interfaces, graph
│   │   ├── agents/         # Domain-specific agents
│   │   ├── services/       # Alert manager, scoring, notifications
│   │   ├── repositories/   # Data access layer
│   │   └── simulation/     # Data generation, environment
│   └── tests/              # Unit and integration tests
├── frontend/
│   ├── index.html          # Dashboard UI
│   ├── css/                # Design system
│   └── js/                 # Client-side logic
└── docs/                   # Documentation
```

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/supply-chain-agents.git
cd supply-chain-agents

# Install dependencies
cd backend
pip install -e .

# Run verification
python tests/verify_system.py
```

### Run Demo

```bash
# Simple demo
python demo_simple.py

# Full demo with all components
python demo_completa.py
```

### Run Tests

```bash
pytest tests/unit/ -v
# 63 tests passing
```

### View Dashboard

Open `frontend/index.html` in your browser.

## Configuration

Set your OpenAI API key for full LLM functionality:

```bash
export OPENAI_API_KEY="your-key-here"
```

Without an API key, the system uses a mock LLM that simulates responses.

## Tech Stack

- **LangGraph**: Agent orchestration and state management
- **LangChain**: LLM integration and prompting
- **Pydantic**: Data validation and serialization
- **NetworkX**: Graph algorithms for route optimization
- **NumPy/SciPy**: Statistical analysis
- **FastAPI**: REST API (optional)

## Testing

The project includes comprehensive unit tests:

| Module | Tests |
|--------|-------|
| Alert Manager | 6 |
| Supplier Repository | 7 |
| Location Optimizer | 7 |
| Event Bus | 5 |
| Utilities | 18 |
| Exceptions | 7 |
| Performance Scoring | 9 |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- LangChain team for the excellent framework
- NetworkX for graph algorithms
- Pydantic for data validation

