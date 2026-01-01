"""
DEMO: Cómo Funciona el Sistema de Supply Chain
==============================================

Este script muestra un ejemplo simple del flujo completo del sistema.
"""

import sys
sys.path.insert(0, '.')

from datetime import datetime

# 1. ESTADO GLOBAL - El "cerebro" del sistema
print("=" * 60)
print("1. CREANDO EL ESTADO GLOBAL (Digital Twin)")
print("=" * 60)

from backend.src.core.state import SupplyChainState, Supplier, Part, InventoryRecord

# Crear un estado inicial simple
state = SupplyChainState(
    current_time=datetime.now(),
    total_budget=1_000_000.0
)

# Añadir un proveedor
supplier = Supplier(
    id="SUP-001",
    name="Acme Components",
    reliability_score=0.85,
    location="Munich, Europe",
    contract_terms={"payment": "Net30"}
)
state.suppliers[supplier.id] = supplier
print(f"   ✓ Proveedor añadido: {supplier.name} (Fiabilidad: {supplier.reliability_score:.0%})")

# Añadir una pieza
part = Part(
    sku="SKU-00001",
    name="Sensor de Temperatura",
    category="Electronics",
    cost=45.0,
    weight_kg=0.2,
    supplier_id="SUP-001"
)
state.parts_catalog[part.sku] = part
print(f"   ✓ Pieza añadida: {part.name} (${part.cost})")

# Añadir inventario
inventory = InventoryRecord(
    sku="SKU-00001",
    warehouse_id="MAIN_DC",
    quantity_on_hand=50,
    quantity_reserved=0,
    reorder_point=30,
    safety_stock=10
)
state.inventory[f"MAIN_DC_{part.sku}"] = inventory
print(f"   ✓ Inventario: {inventory.quantity_on_hand} unidades en stock")

# 2. REPOSITORIOS - Acceso a datos organizado
print("\n" + "=" * 60)
print("2. USANDO REPOSITORIOS (Patrón SOLID)")
print("=" * 60)

from backend.src.repositories.supplier_repository import SupplierRepository

repo = SupplierRepository()
repo.save(supplier)

# Buscar proveedores fiables
reliable = repo.find_by_reliability(min_score=0.8)
print(f"   ✓ Proveedores con fiabilidad > 80%: {len(reliable)}")

# 3. SERVICIOS - Lógica de negocio
print("\n" + "=" * 60)
print("3. USANDO SERVICIOS (Alertas, Scoring, etc.)")
print("=" * 60)

from backend.src.services.alert_manager import alert_manager, AlertSeverity
from backend.src.services.performance_scoring import scoring_engine

# Crear una alerta
alert = alert_manager.create_alert(
    title="Stock Bajo",
    description="SKU-00001 está cerca del punto de reorden",
    severity=AlertSeverity.WARNING,
    source_agent="Inventory"
)
print(f"   ✓ Alerta creada: [{alert.severity.value}] {alert.title}")

# Calcular puntuación del proveedor
scoring_engine.record_delivery("SUP-001", was_on_time=True)
scoring_engine.record_quality_result("SUP-001", passed=True)
scorecard = scoring_engine.get_scorecard(supplier)
print(f"   ✓ Scorecard: {supplier.name} → {scorecard.tier} ({scorecard.composite_score:.2f})")

# 4. EVENT BUS - Comunicación entre agentes
print("\n" + "=" * 60)
print("4. EVENT BUS (Comunicación Pub/Sub)")
print("=" * 60)

from backend.src.core.event_bus import event_bus, EventType

# Suscribirse a un evento
def on_low_inventory(event):
    print(f"   📢 Evento recibido: {event.event_type.value} → {event.payload}")

event_bus.subscribe(EventType.INVENTORY_LOW, on_low_inventory)

# Publicar un evento
event_bus.emit(
    event_type=EventType.INVENTORY_LOW,
    payload={"sku": "SKU-00001", "quantity": 50},
    source="InventoryAgent"
)

# 5. RESUMEN
print("\n" + "=" * 60)
print("5. RESUMEN DEL SISTEMA")
print("=" * 60)
print(f"""
   Estado Global:
   - Proveedores: {len(state.suppliers)}
   - Piezas: {len(state.parts_catalog)}
   - Presupuesto: ${state.total_budget:,.2f}
   
   Alertas activas: {len(alert_manager.get_open_alerts())}
   Eventos en historial: {len(event_bus.get_history())}
""")

print("=" * 60)
print("✅ DEMO COMPLETADA")
print("=" * 60)
