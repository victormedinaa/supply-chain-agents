"""
Custom Exception Classes.

Defines domain-specific exceptions for better error handling and debugging.
Follows the Principle of Explicit Communication.
"""


class SupplyChainException(Exception):
    """Base exception for all supply chain related errors."""
    pass


class BudgetExceededException(SupplyChainException):
    """Raised when a proposed action would exceed the allocated budget."""
    def __init__(self, requested_amount: float, available_budget: float):
        self.requested_amount = requested_amount
        self.available_budget = available_budget
        super().__init__(
            f"Requested amount ${requested_amount:,.2f} exceeds available budget ${available_budget:,.2f}."
        )


class InventoryShortageException(SupplyChainException):
    """Raised when inventory is insufficient to fulfill a production order."""
    def __init__(self, sku: str, required: int, available: int):
        self.sku = sku
        self.required = required
        self.available = available
        super().__init__(
            f"Inventory shortage for {sku}: required {required}, available {available}."
        )


class SupplierUnavailableException(SupplyChainException):
    """Raised when a supplier cannot fulfill a request."""
    def __init__(self, supplier_id: str, reason: str):
        self.supplier_id = supplier_id
        self.reason = reason
        super().__init__(f"Supplier {supplier_id} unavailable: {reason}.")


class RouteNotFoundException(SupplyChainException):
    """Raised when no viable logistics route can be found."""
    def __init__(self, origin: str, destination: str):
        self.origin = origin
        self.destination = destination
        super().__init__(f"No route found from {origin} to {destination}.")


class QualityControlFailedException(SupplyChainException):
    """Raised when a batch fails quality inspection."""
    def __init__(self, batch_id: str, defect_rate: float, threshold: float):
        self.batch_id = batch_id
        self.defect_rate = defect_rate
        self.threshold = threshold
        super().__init__(
            f"Batch {batch_id} failed QC: defect rate {defect_rate:.2%} exceeds threshold {threshold:.2%}."
        )


class GraphExecutionException(SupplyChainException):
    """Raised when the agent graph encounters an unrecoverable error."""
    def __init__(self, agent_name: str, details: str):
        self.agent_name = agent_name
        self.details = details
        super().__init__(f"Graph execution failed at {agent_name}: {details}.")
