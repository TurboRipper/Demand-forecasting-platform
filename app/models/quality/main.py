from fastapi import FastAPI

from app.shared.contracts import ModelPrediction, ProcessedRetailRecord
from app.shared.ml import explain_with_weights, get_stockout_model, vectorize

app = FastAPI(title="RetailPulse ML Stockout Risk Service", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "stockout-risk"}


@app.post("/predict")
def predict(payload: ProcessedRetailRecord) -> dict:
    model = get_stockout_model()
    feature_vector = vectorize(payload.model_dump()).reshape(1, -1)
    risk_score = float(model.predict_proba(feature_vector)[0][1])
    confidence = round(abs(risk_score - 0.5) * 2.0, 4)
    label = "reorder-urgent" if risk_score >= 0.78 else "watch" if risk_score >= 0.5 else "covered"
    explanation = (
        "Stockout risk is estimated from demand pressure, lead time, replenishment gap, "
        "and available stock cover."
    )
    prediction = ModelPrediction(
        model_name="stockout-risk",
        risk_score=round(risk_score, 4),
        label=label,
        confidence=confidence,
        explanation=explanation,
        factors=explain_with_weights(model.coef_[0], payload.model_dump()),
        projected_value=payload.stock_cover_days,
        unit="days cover",
    )
    return prediction.model_dump()
