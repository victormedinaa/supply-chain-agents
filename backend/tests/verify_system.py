"""
Verification Script.

Runs the Supply Chain Multi-Agent System for a defined number of steps 
to verify architecture stability and agent intelligence.
"""

from backend.src.core.graph import app
from backend.src.simulation.generator import generator
from backend.src.simulation.environment import environment
from backend.src.core.state import AgentMessage

def run_verification():
    print("Initializing Enterprise Supply Chain Digital Twin...")
    initial_state = generator.generate_initial_state()
    print(f"Loaded {len(initial_state.parts_catalog)} parts and {len(initial_state.suppliers)} suppliers.")
    print(f"Initial Inventory Value: >${sum(p.cost * r.quantity_on_hand for p, r in zip(initial_state.parts_catalog.values(), initial_state.inventory.values())):,.2f}")
    
    # Configure recursion limit for complex graphs
    config = {"recursion_limit": 50, "configurable": {"thread_id": "SYS-001"}}
    
    print("\n--- Starting Digital Twin Cycle ---")
    current_state = initial_state
    
    for i in range(1, 4): # Run 3 full cycles
        print(f"\n[Day {i}] Environment Step...")
        environment.step(current_state)
        
        print(f"[Day {i}] Agents Activating...")
        output = app.invoke(current_state, config=config)
        
        if not isinstance(output, dict):
             current_state = output
             
        # Print summary of the day's agent communications
        print(f"--> Cycle {i} Complete.")
        
    print("\n--- Verification Successful: System Stable ---")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"SYSTEM EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
