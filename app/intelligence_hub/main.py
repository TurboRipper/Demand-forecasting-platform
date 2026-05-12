from collections import deque
from datetime import datetime, timezone

from fastapi import FastAPI

from app.shared.contracts import AggregateRequest, AggregateResponse

app = FastAPI(title="RetailPulse ML Intelligence Hub", version="1.0.0")
FORECASTS: deque[dict] = deque(maxlen=20)


def summarize(request: AggregateRequest) -> AggregateResponse:
    prediction_map = {prediction.model_name: prediction for prediction in request.predictions}
    demand_prediction = prediction_map["demand-forecast"]
    anomaly_prediction = prediction_map["demand-anomaly"]
    stockout_prediction = prediction_map["stockout-risk"]

    demand_score = demand_prediction.risk_score
    anomaly_score = anomaly_prediction.risk_score
    stockout_score = stockout_prediction.risk_score
    forecast_units = demand_prediction.projected_value
    stock_cover_days = request.sales_record.stock_cover_days

    overall_score = round(0.3 * demand_score + 0.25 * anomaly_score + 0.45 * stockout_score, 4)

    if stockout_score >= 0.82 or ((forecast_units or 0) >= 155 and stock_cover_days <= 2.5):
        severity = "critical"
        headline = f"Projected demand is {forecast_units:.0f} units/day with immediate replenishment risk"
        action = "Create an urgent purchase order, rebalance stock from nearby stores, and protect shelf availability."
    elif overall_score >= 0.58 or anomaly_score >= 0.72:
        severity = "elevated"
        headline = f"Projected demand is {forecast_units:.0f} units/day with elevated planning pressure"
        action = "Advance replenishment planning, review promotion impact, and monitor intraday sell-through."
    else:
        severity = "stable"
        headline = f"Projected demand is {forecast_units:.0f} units/day and stock position is healthy"
        action = "Maintain routine replenishment and continue standard inventory monitoring."

    if demand_score >= 0.75 and stockout_score < 0.5 and severity != "critical":
        headline = f"High demand forecast at {forecast_units:.0f} units/day without immediate stockout risk"
        action = "Monitor sales acceleration and prepare a follow-on replenishment cycle to sustain availability."

    return AggregateResponse(
        scenario_id=request.sales_record.scenario_id,
        product_id=request.sales_record.product_id,
        store_id=request.sales_record.store_id,
        overall_score=overall_score,
        severity=severity,
        headline=headline,
        recommended_action=action,
        forecast_units=forecast_units,
        model_predictions=request.predictions,
        product_snapshot={
            "category": request.sales_record.category,
            "effective_price": request.sales_record.effective_price,
            "inventory_units": request.sales_record.inventory_units,
            "prior_day_sales": request.sales_record.prior_day_sales,
            "prior_week_sales": request.sales_record.prior_week_sales,
            "stock_cover_days": request.sales_record.stock_cover_days,
            "lead_time_days": request.sales_record.lead_time_days,
            "demand_pressure": request.sales_record.demand_pressure,
        },
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "intelligence-hub", "stored_forecasts": len(FORECASTS)}


@app.get("/history")
def history() -> dict:
    return {"forecasts": list(FORECASTS)}


@app.post("/aggregate")
def aggregate(request: AggregateRequest) -> dict:
    response = summarize(request)
    summary = response.model_dump()
    summary["created_at"] = datetime.now(timezone.utc).isoformat()
    FORECASTS.appendleft(summary)
    return summary
