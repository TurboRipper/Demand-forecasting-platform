from fastapi import FastAPI

from app.shared.contracts import ModelPrediction, ProcessedRetailRecord
from app.shared.ml import explain_with_weights, get_demand_model, vectorize

app = FastAPI(title="RetailPulse ML Demand Forecast Service", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "demand-forecast"}


@app.post("/predict")
def predict(payload: ProcessedRetailRecord) -> dict:
    model = get_demand_model()
    feature_vector = vectorize(payload.model_dump()).reshape(1, -1)
    projected_units = float(model.predict(feature_vector)[0])
    demand_score = min(projected_units / 220.0, 1.0)
    confidence = round(min(0.98, 0.55 + demand_score / 2.0), 4)
    label = "surge" if demand_score >= 0.72 else "steady" if demand_score >= 0.38 else "soft"
    factors = explain_with_weights(model.feature_importances_, payload.model_dump())
    explanation = (
        "Forecasted demand is driven by recent sales velocity, promotion lift, seasonal traffic, "
        "and current price sensitivity."
    )
    prediction = ModelPrediction(
        model_name="demand-forecast",
        risk_score=round(demand_score, 4),
        label=label,
        confidence=confidence,
        explanation=explanation,
        factors=factors,
        projected_value=round(projected_units, 1),
        unit="units/day",
    )
    return prediction.model_dump()
