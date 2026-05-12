from typing import Any

from pydantic import BaseModel, Field


class RawRetailRecord(BaseModel):
    scenario_id: str = Field(..., description="Unique scenario or submission identifier")
    product_id: str
    store_id: str
    timestamp: str
    category: str
    base_price: float
    discount_pct: float
    inventory_units: float
    prior_day_sales: float
    prior_week_sales: float
    footfall_index: float
    promotion_flag: int
    holiday_flag: int
    weekday_index: int
    lead_time_days: float


class ProcessedRetailRecord(RawRetailRecord):
    effective_price: float
    effective_price_index: float
    discount_index: float
    daily_velocity: float
    weekly_velocity: float
    stock_cover_days: float
    stock_cover_index: float
    demand_pressure: float
    promo_lift: float
    seasonal_signal: float
    price_sensitivity: float
    replenishment_gap: float
    revenue_potential: float
    lead_time_index: float
    category_index: float


class ModelPrediction(BaseModel):
    model_name: str
    risk_score: float
    label: str
    confidence: float
    explanation: str
    factors: list[str]
    projected_value: float | None = None
    unit: str | None = None


class AgentInsight(BaseModel):
    agent_id: str
    role: str
    priority: str
    conclusion: str
    rationale: str
    recommended_action: str


class AgentPlan(BaseModel):
    coordination_mode: str
    supervisor_summary: str
    confidence: float
    next_actions: list[str]


class AggregateRequest(BaseModel):
    sales_record: ProcessedRetailRecord
    predictions: list[ModelPrediction]


class AggregateResponse(BaseModel):
    scenario_id: str
    product_id: str
    store_id: str
    overall_score: float
    severity: str
    headline: str
    recommended_action: str
    forecast_units: float | None = None
    model_predictions: list[ModelPrediction]
    product_snapshot: dict[str, Any]
    agent_trace: list[AgentInsight] = Field(default_factory=list)
    agent_plan: AgentPlan | None = None


class AgentOrchestrationRequest(BaseModel):
    summary: AggregateResponse
