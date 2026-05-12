from fastapi import FastAPI, HTTPException

from app.shared.config import get_settings
from app.shared.contracts import ProcessedRetailRecord, RawRetailRecord
from app.shared.http import post_json

app = FastAPI(title="RetailPulse ML Preprocessing Service", version="1.0.0")

CATEGORY_MAP = {
    "Grocery": 0.36,
    "Beverages": 0.44,
    "Snacks": 0.51,
    "Personal Care": 0.32,
    "Household": 0.29,
    "Electronics": 0.41,
}


def preprocess_payload(payload: RawRetailRecord) -> ProcessedRetailRecord:
    effective_price = round(payload.base_price * (1 - payload.discount_pct / 100.0), 2)
    effective_price_index = round(effective_price / 100.0, 4)
    discount_index = round(payload.discount_pct / 50.0, 4)
    daily_velocity = round(payload.prior_day_sales / 120.0, 4)
    weekly_velocity = round(payload.prior_week_sales / 700.0, 4)
    stock_cover_days = round(payload.inventory_units / max(payload.prior_day_sales, 1.0), 2)
    stock_cover_index = round(min(stock_cover_days / 14.0, 2.0), 4)
    demand_pressure = round(0.42 * daily_velocity + 0.33 * weekly_velocity + 0.25 * payload.footfall_index, 4)
    promo_lift = round(0.45 * payload.promotion_flag + 0.35 * discount_index + 0.2 * payload.holiday_flag, 4)
    weekend_signal = 1.0 if payload.weekday_index in (5, 6) else 0.0
    seasonal_signal = round(0.5 * payload.holiday_flag + 0.2 * weekend_signal + 0.3 * payload.footfall_index, 4)
    price_sensitivity = round(max((50.0 - effective_price) / 50.0, 0.0) + 0.25 * discount_index, 4)
    replenishment_gap = round(
        max(((payload.prior_week_sales / 7.0) * max(payload.lead_time_days, 1.0)) - payload.inventory_units, 0.0) / 200.0,
        4,
    )
    revenue_potential = round((effective_price * max(payload.prior_day_sales, payload.prior_week_sales / 7.0)) / 1000.0, 4)
    lead_time_index = round(payload.lead_time_days / 14.0, 4)
    category_index = CATEGORY_MAP.get(payload.category, 0.34)

    return ProcessedRetailRecord(
        **payload.model_dump(),
        effective_price=effective_price,
        effective_price_index=effective_price_index,
        discount_index=discount_index,
        daily_velocity=daily_velocity,
        weekly_velocity=weekly_velocity,
        stock_cover_days=stock_cover_days,
        stock_cover_index=stock_cover_index,
        demand_pressure=demand_pressure,
        promo_lift=promo_lift,
        seasonal_signal=seasonal_signal,
        price_sensitivity=price_sensitivity,
        replenishment_gap=replenishment_gap,
        revenue_potential=revenue_potential,
        lead_time_index=lead_time_index,
        category_index=category_index,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "preprocessing"}


@app.post("/preprocess")
def preprocess(payload: RawRetailRecord) -> dict:
    processed = preprocess_payload(payload)
    try:
        result = post_json(get_settings().router_url, processed.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Router unavailable: {exc}") from exc
    return {
        "pipeline_stage": "preprocessing",
        "processed_payload": processed.model_dump(),
        "downstream_result": result,
    }
