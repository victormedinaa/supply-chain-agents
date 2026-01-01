# Automotive Supply Chain Multi-Agent System

An enterprise-grade autonomous supply chain management platform built with **LangGraph** and **Python**.

## Overview

This system orchestrates a network of specialized autonomous agents that collaborate to manage complex global supply chain operations. Each agent is responsible for a specific domain (Inventory, Procurement, Logistics, Production, Finance, Quality) and communicates through a centralized Digital Twin state.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR                            │
│                        (LangGraph Core)                         │
└───────────┬───────────────────────────────────────┬─────────────┘
            │                                       │
    ┌───────▼───────┐                       ┌───────▼───────┐
    │   Inventory   │                       │   Procurement │
    │     Agent     │                       │     Agent     │
    └───────┬───────┘                       └───────┬───────┘
            │                                       │
    ┌───────▼───────┐                       ┌───────▼───────┐
    │   Finance     │                       │   Logistics   │
    │     Agent     │                       │     Agent     │
    └───────┬───────┘                       └───────┬───────┘
            │                                       │
    ┌───────▼───────┐                       ┌───────▼───────┐
    │   Quality     │                       │   Production  │
    │     Agent     │                       │     Agent     │
    └───────────────┘                       └───────────────┘
```

## Features

### Autonomous Agents
- **Inventory Agent**: Demand forecasting (hybrid statistical + generative), multi-echelon optimization
- **Procurement Agent**: Supplier risk assessment, automated negotiation
- **Finance Agent**: Budget enforcement, variance analysis, double-entry ledger
- **Logistics Agent**: Route optimization (NetworkX), shipment tracking
- **Quality Agent**: Statistical process control, root cause analysis
- **Production Agent**: Scheduling optimization, capacity planning

### Enterprise Services
- **Alert Management**: Priority-based queue with escalation rules
- **Performance Scoring**: Supplier KPI calculation (delivery, quality, cost)
- **Location Optimizer**: Warehouse placement using center of gravity method
- **Notification Service**: Multi-channel dispatch (Email, Slack, In-App)
- **Event Bus**: Pub/Sub for decoupled inter-agent communication

### SOLID Architecture
- Abstract Base Classes for all entities
- Repository Pattern for data access
- Dependency Injection for LLM providers
- Custom exception hierarchy

## Project Structure

```
├── backend/
│   ├── src/
│   │   ├── core/           # State, Config, Interfaces, Graph
│   │   ├── agents/         # Domain-specific agents
│   │   ├── services/       # Business services
│   │   ├── repositories/   # Data access layer
│   │   └── simulation/     # Data generation, environment
│   └── tests/              # Unit and integration tests
├── frontend/
│   ├── index.html          # Dashboard
│   ├── css/                # Design system
│   └── js/                 # Client-side logic
└── docs/                   # Documentation
```

## Quick Start

### Backend

```bash
cd backend
pip install -e .
python tests/verify_system.py
```

### Frontend

Open `frontend/index.html` in a browser.

## Dependencies

- Python 3.11+
- LangGraph
- LangChain
- Pydantic
- NetworkX
- NumPy / SciPy

## License

MIT
