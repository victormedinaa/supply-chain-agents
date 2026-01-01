"""
DEMO COMPLETA: Sistema Multi-Agente con LLM
============================================

Este script muestra el flujo COMPLETO del sistema incluyendo:
- Uso del LLM (o Mock LLM si no hay API key)
- Ejecución del Grafo LangGraph
- Comunicación entre agentes
- Decisiones inteligentes
"""

import sys
sys.path.insert(0, '.')

from datetime import datetime, timedelta

print("=" * 70)
print("   DEMO COMPLETA: SISTEMA MULTI-AGENTE CON LLM")
print("=" * 70)

# ============================================================
# PARTE 1: CONFIGURACIÓN DEL LLM
# ============================================================
print("\n📡 PARTE 1: CONFIGURANDO EL MODELO DE LENGUAJE (LLM)")
print("-" * 70)

from backend.src.core.llm_provider import get_llm

llm = get_llm(model_name="gpt-4-turbo", temperature=0.7)
print(f"   Modelo cargado: {llm._llm_type}")

# Probar el LLM directamente
from langchain_core.messages import HumanMessage

response = llm.invoke([HumanMessage(content="Analiza este riesgo de proveedor: fiabilidad 0.6, retrasos frecuentes.")])
print(f"   Respuesta del LLM: {response.content[:100]}...")

# ============================================================
# PARTE 2: CREAR UN ESCENARIO COMPLEJO
# ============================================================
print("\n🏭 PARTE 2: CREANDO UN ESCENARIO COMPLEJO")
print("-" * 70)

from backend.src.simulation.generator import DataGenerator

generator = DataGenerator()
state = generator.generate_initial_state()

print(f"   ✓ Proveedores generados: {len(state.suppliers)}")
print(f"   ✓ Piezas en catálogo: {len(state.parts_catalog)}")
print(f"   ✓ Registros de inventario: {len(state.inventory)}")
print(f"   ✓ Órdenes de producción: {len(state.production_schedule)}")
print(f"   ✓ Presupuesto total: ${state.total_budget:,.0f}")

# Calcular valor del inventario
inventory_value = sum(
    state.parts_catalog[rec.sku].cost * rec.quantity_on_hand 
    for rec in state.inventory.values() 
    if rec.sku in state.parts_catalog
)
print(f"   ✓ Valor del inventario: ${inventory_value:,.2f}")

# ============================================================
# PARTE 3: AGENTE DE NEGOCIACIÓN CON LLM
# ============================================================
print("\n🤝 PARTE 3: AGENTE NEGOCIADOR USANDO LLM")
print("-" * 70)

from backend.src.agents.procurement.negotiator import Negotiator

negotiator = Negotiator()

# Seleccionar un proveedor de bajo rendimiento
low_reliability_supplier = None
for sup in state.suppliers.values():
    if sup.reliability_score < 0.85:
        low_reliability_supplier = sup
        break

if low_reliability_supplier:
    print(f"   Proveedor problemático: {low_reliability_supplier.name}")
    print(f"   Fiabilidad: {low_reliability_supplier.reliability_score:.0%}")
    print(f"   Ubicación: {low_reliability_supplier.location}")
    
    # Generar email de negociación usando el LLM
    email = negotiator.draft_negotiation_email(
        supplier=low_reliability_supplier,
        issue_type="expedite_shipping",
        state=state
    )
    
    print(f"\n   📧 EMAIL GENERADO POR EL LLM:")
    print("   " + "-" * 50)
    for line in email.split('\n')[:8]:  # Primeras 8 líneas
        print(f"   {line}")
    print("   ...")

# ============================================================
# PARTE 4: EJECUCIÓN DEL GRAFO LANGGRAPH
# ============================================================
print("\n\n🔄 PARTE 4: EJECUTANDO EL GRAFO LANGGRAPH (1 CICLO)")
print("-" * 70)

from backend.src.core.graph import app

config = {"recursion_limit": 50, "configurable": {"thread_id": "DEMO-001"}}

print("   Iniciando ciclo de agentes...")
print()

# Ejecutar un ciclo completo
output = app.invoke(state, config=config)

print("\n   Mensajes generados por los agentes:")
if hasattr(output, 'messages'):
    for msg in output.messages[-6:]:  # Últimos 6 mensajes
        print(f"   [{msg.sender}] → {msg.content[:60]}...")

# ============================================================
# PARTE 5: FORECAST CON LLM
# ============================================================
print("\n\n📊 PARTE 5: FORECASTING HÍBRIDO (Estadístico + LLM)")
print("-" * 70)

from backend.src.agents.inventory.forecaster import DemandForecaster
import pandas as pd
import numpy as np

forecaster = DemandForecaster()

# Crear historial de demanda simulado (formato correcto)
dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
sku = "SKU-00001"
history = pd.DataFrame({
    'date': dates,
    'sku': [sku] * 30,
    'quantity': np.random.normal(100, 20, 30).astype(int)
})

print(f"   Historial de demanda para {sku}: {len(history)} días")
print(f"   Demanda promedio: {history['quantity'].mean():.0f} unidades/día")

# Generar forecast
forecast = forecaster.generate_forecast(state, history)

print(f"\n   🔮 FORECAST GENERADO:")
for sku, predicted in list(forecast.items())[:3]:
    print(f"   {sku}: {predicted} unidades predichas")

# ============================================================
# PARTE 6: ANÁLISIS DE RIESGO BAYESIANO
# ============================================================
print("\n\n🎲 PARTE 6: MODELO DE RIESGO BAYESIANO")
print("-" * 70)

from backend.src.agents.procurement.supplier_risk import SupplierRiskModel

risk_model = SupplierRiskModel()

# Analizar riesgo de todos los proveedores
risks = []
for sup in list(state.suppliers.values())[:5]:
    risk = risk_model.assess_risk(sup, state)
    risks.append((sup.name, risk))
    
print("   Evaluación de riesgo por proveedor:")
for name, risk in sorted(risks, key=lambda x: x[1], reverse=True):
    level = "🔴 ALTO" if risk > 0.5 else "🟡 MEDIO" if risk > 0.3 else "🟢 BAJO"
    print(f"   {level} {name}: {risk:.1%}")

# ============================================================
# PARTE 7: OPTIMIZACIÓN DE RUTAS
# ============================================================
print("\n\n🚚 PARTE 7: OPTIMIZACIÓN DE RUTAS (NetworkX)")
print("-" * 70)

from backend.src.agents.logistics.router import LogisticsRouter

router = LogisticsRouter()

# Encontrar ruta óptima
route = router.find_optimal_route("Shanghai", "Munich (HQ)", criterion="cost")

print(f"   Origen: Shanghai")
print(f"   Destino: Munich (HQ)")
print(f"   Optimizado por: Costo")
print(f"\n   📍 RUTA ÓPTIMA: {' → '.join(route['path'])}")
print(f"   💰 Costo total: ${route['estimated_cost']:,.0f}")
print(f"   ⏱️ Tiempo estimado: {route['estimated_transit_time']} días")

# ============================================================
# RESUMEN FINAL
# ============================================================
print("\n\n" + "=" * 70)
print("   ✅ DEMO COMPLETA FINALIZADA")
print("=" * 70)
print(f"""
   Este sistema incluye:
   
   🧠 LLM Integration
      - Negociación automática con proveedores
      - Ajuste cualitativo de forecasts
      - Análisis de situaciones complejas
   
   🤖 6 Agentes Autónomos
      - Inventory, Procurement, Finance
      - Logistics, Quality, Production
   
   📊 Modelos Analíticos
      - Forecasting híbrido (ARIMA + LLM)
      - Riesgo Bayesiano
      - Optimización de rutas (Dijkstra)
   
""")
print("=" * 70)
