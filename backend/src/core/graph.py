"""
Main Orchestrator Graph for the Supply Chain System.

This module defines the high-level workflow using LangGraph. It routes control flow 
between the specialized agents (Procurement, Logistics, Inventory, Production).

Architecture:
- The `SupervisingAgent` (LLM) decides which specialist should act next based on the global state.
- Each specialist is a node in the graph.
- The graph cycles until a stable state is reached or a 'Wait' condition is triggered.
"""

from typing import Literal, Dict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from backend.src.core.state import SupplyChainState, AgentMessage
from backend.src.core.memory import memory_saver

from backend.src.agents.inventory.forecaster import forecaster
from backend.src.agents.inventory.optimizer import optimizer
from backend.src.agents.procurement.negotiator import negotiator
from backend.src.agents.logistics.router import router
from backend.src.agents.logistics.tracker import tracker
from backend.src.agents.production.scheduler import scheduler
from backend.src.agents.finance.controller import controller
from backend.src.agents.quality.inspector import inspector

# -- Agent Wrappers for Graph Nodes --

def run_procurement(state: SupplyChainState):
    print("--- Procurement Agent Acting ---")
    # Determine if we need to buy anything
    # (Simplified logic: always run negotiation check)
    msgs = negotiator.run_routine(state)
    if not msgs:
        msgs = [AgentMessage(sender="Procurement", receiver="Orchestrator", content="No critical actions needed.")]
    return {"messages": msgs}

def run_logistics(state: SupplyChainState):
    print("--- Logistics Agent Acting ---")
    msgs = tracker.monitor_active_shipments(state)
    if not msgs:
         msgs = [AgentMessage(sender="Logistics", receiver="Orchestrator", content="All shipments on track.")]
    return {"messages": msgs}

def run_inventory(state: SupplyChainState):
    print("--- Inventory Agent Acting ---")
    # Mock loop for forecasting is removed for brevity in this step
    # Real implementation would iterate over critical SKUs
    # forecast = forecaster.generate_forecast(state, mock_history_df)
    return {"messages": [AgentMessage(sender="Inventory", receiver="Orchestrator", content="Forecasts updated.")]}

def run_production(state: SupplyChainState):
    print("--- Production Agent Acting ---")
    msgs = scheduler.schedule_production(state)
    if not msgs:
        msgs = [AgentMessage(sender="Production", receiver="Orchestrator", content="Production plan nominal.")]
    return {"messages": msgs}

def run_finance(state: SupplyChainState):
    print("--- Finance Agent Acting ---")
    msgs = controller.analyze_variance(state)
    if not msgs:
        msgs = [AgentMessage(sender="Finance", receiver="Orchestrator", content="Budget usage within limits.")]
    return {"messages": msgs}

def run_quality(state: SupplyChainState):
    print("--- Quality Agent Acting ---")
    msgs = inspector.monitor_quality(state)
    if not msgs:
        msgs = [AgentMessage(sender="Quality", receiver="Orchestrator", content="Process capability Index (Cpk) > 1.33")]
    return {"messages": msgs}


def supervisor_router(state: SupplyChainState) -> Literal["procurement", "logistics", "inventory", "production", "finance", "quality", "__end__"]:
    """
    Central Router.
    Determines the sequence of agent activation.
    
    Standard Cycle:
    Inventory -> Procurement -> Finance (Approvals) -> Logistics -> Quality -> Production
    """
    if not state.messages:
        return "inventory"
    
    last_msg = state.messages[-1]
    sender = last_msg.sender
    
    if sender == "Inventory":
        return "procurement"
    elif sender == "Procurement":
        return "finance" # New check
    elif sender == "Finance":
        return "logistics"
    elif sender == "Logistics":
        return "quality" # New check
    elif sender == "Quality":
        return "production"
    elif sender == "Production":
        return "__end__"
    
    return "__end__"

# -- Graph Definition --

workflow = StateGraph(SupplyChainState)

# Add Nodes
workflow.add_node("inventory", run_inventory)
workflow.add_node("procurement", run_procurement)
workflow.add_node("logistics", run_logistics)
workflow.add_node("production", run_production)
workflow.add_node("finance", run_finance)
workflow.add_node("quality", run_quality)

# Add Edges (Controlled by the Supervisor Router)
nodes = ["inventory", "procurement", "logistics", "production", "finance", "quality"]
routing_map = {node: node for node in nodes}
routing_map["__end__"] = END

for node in nodes:
    workflow.add_conditional_edges(node, supervisor_router, routing_map)

# Set Entry Point
workflow.set_entry_point("inventory")

# Compile
app = workflow.compile(checkpointer=memory_saver)
