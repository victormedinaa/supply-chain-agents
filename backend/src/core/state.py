"""
Global State Definitions for the Automotive Supply Chain Multi-Agent System.

This module defines the complex Pydantic models that represent the shared state 
accessed by all agents in the LangGraph. It includes schemas for Inventory, 
Logistics, Procurement, and Production, as well as the standard Agent communication protocol.
"""

from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
import uuid

# --- Primitive Types ---

class Supplier(BaseModel):
    id: str
    name: str
    reliability_score: float = Field(..., ge=0, le=1, description="Normalized reliability score based on historical performance.")
    location: str
    contract_terms: Dict[str, Any]
    tier: Literal["Gold", "Silver", "Bronze", "Under Review"] = "Bronze"
    lead_time_days: int = 14
    minimum_order_quantity: int = 100


class Part(BaseModel):
    sku: str
    name: str
    category: Literal["Electronics", "Chassis", "Powertrain", "Interior"]
    cost: float
    weight_kg: float
    supplier_id: str
    unit_of_measure: str = "PCS"
    is_critical: bool = False
    hs_code: Optional[str] = None  # Harmonized System code for customs


class Warehouse(BaseModel):
    """Represents a distribution center or storage facility."""
    id: str
    name: str
    location: str
    capacity_units: int
    current_utilization: float = 0.0
    latitude: float
    longitude: float
    is_active: bool = True


class Shipment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    origin: str
    destination: str
    status: Literal["Pending", "In Transit", "Customs", "Delivered", "Delayed", "Cancelled"]
    estimated_arrival: datetime
    actual_arrival: Optional[datetime] = None
    current_coordinates: Optional[Dict[str, float]] = None
    risk_factor: float = 0.0
    carrier: str = "Default Carrier"
    transport_mode: Literal["Sea", "Air", "Rail", "Road"] = "Sea"
    cost: float = 0.0


class InventoryRecord(BaseModel):
    sku: str
    warehouse_id: str
    quantity_on_hand: int
    quantity_reserved: int
    quantity_in_transit: int = 0
    reorder_point: int
    safety_stock: int
    last_replenished: Optional[datetime] = None


class PurchaseOrder(BaseModel):
    """Represents a procurement request to a supplier."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    supplier_id: str
    items: Dict[str, int]  # SKU -> Quantity
    total_value: float
    status: Literal["Draft", "Submitted", "Acknowledged", "Shipped", "Received", "Cancelled"] = "Draft"
    created_at: datetime = Field(default_factory=datetime.now)
    expected_delivery: Optional[datetime] = None


class QualityInspectionResult(BaseModel):
    """Records the outcome of a quality inspection."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    shipment_id: str
    inspector_id: str
    passed: bool
    defect_rate: float
    notes: str = ""
    inspected_at: datetime = Field(default_factory=datetime.now)


class ProductionOrder(BaseModel):
    order_id: str
    car_model: str
    required_parts: Dict[str, int]
    deadline: datetime
    status: Literal["Planned", "Assembling", "Quality Check", "Completed", "Halted"]
    priority: int = 5  # 1=Highest, 10=Lowest
    assigned_line: Optional[str] = None


# --- Agent Communication ---

class AgentMessage(BaseModel):
    sender: str
    receiver: Literal["Orchestrator", "Procurement", "Logistics", "Inventory", "Production", "Finance", "Quality"]
    content: str
    structured_data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    priority: Literal["Low", "Medium", "High", "Critical"] = "Medium"
    correlation_id: Optional[str] = None  # For tracking related messages


# --- KPI Metrics ---

class OperationalKPIs(BaseModel):
    """Key Performance Indicators for the supply chain."""
    on_time_delivery_rate: float = 1.0
    order_fulfillment_rate: float = 1.0
    inventory_turnover: float = 0.0
    average_lead_time_days: float = 14.0
    defect_rate: float = 0.0
    budget_utilization: float = 0.0


# --- Global Graph State ---

class SupplyChainState(BaseModel):
    """
    The central source of truth for the entire supply chain Digital Twin.
    Agents read from and write to this state.
    """
    # World State
    current_time: datetime
    simulation_step: int = 0
    
    # Domain States
    suppliers: Dict[str, Supplier] = {}
    parts_catalog: Dict[str, Part] = {}
    warehouses: Dict[str, Warehouse] = {}
    inventory: Dict[str, InventoryRecord] = {}
    active_shipments: List[Shipment] = []
    purchase_orders: List[PurchaseOrder] = []
    quality_results: List[QualityInspectionResult] = []
    production_schedule: List[ProductionOrder] = []
    
    # Financials
    total_budget: float
    operating_costs: float = 0.0
    
    # Agent Memory & Communication
    messages: List[AgentMessage] = []
    errors: List[str] = []
    
    # Metrics
    kpis: OperationalKPIs = Field(default_factory=OperationalKPIs)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def log_message(self, message: AgentMessage):
        self.messages.append(message)

    def get_inventory(self, sku: str) -> int:
        """Returns total inventory for a SKU across all warehouses."""
        total = 0
        for record in self.inventory.values():
            if record.sku == sku:
                total += record.quantity_on_hand
        return total
    
    def get_available_inventory(self, sku: str) -> int:
        """Returns available (not reserved) inventory for a SKU."""
        total = 0
        for record in self.inventory.values():
            if record.sku == sku:
                total += record.quantity_on_hand - record.quantity_reserved
        return max(0, total)
    
    def get_low_stock_skus(self) -> List[str]:
        """Identifies SKUs below their reorder point."""
        low_stock = []
        for key, record in self.inventory.items():
            if record.quantity_on_hand <= record.reorder_point:
                low_stock.append(record.sku)
        return list(set(low_stock))
    
    def get_pending_orders(self) -> List[ProductionOrder]:
        """Returns production orders that are not yet completed."""
        return [o for o in self.production_schedule if o.status not in ["Completed", "Cancelled"]]
    
    def get_delayed_shipments(self) -> List[Shipment]:
        """Returns shipments that are currently delayed."""
        return [s for s in self.active_shipments if s.status == "Delayed"]
    
    def calculate_budget_remaining(self) -> float:
        """Calculates remaining budget."""
        return self.total_budget - self.operating_costs

