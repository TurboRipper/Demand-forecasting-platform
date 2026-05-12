import math

from fastapi import FastAPI

from app.shared.contracts import ModelPrediction, ProcessedRetailRecord
from app.shared.ml import explain_with_magnitude, get_demand_anomaly_model, vectorize

app = FastAPI(title="RetailPulse ML Demand Anomaly Service", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "demand-anomaly"}


@app.post("/predict")
def predict(payload: ProcessedRetailRecord) -> dict:
    model = get_demand_anomaly_model()
    feature_vector = vectorize(payload.model_dump()).reshape(1, -1)
    decision_margin = float(model.decision_function(feature_vector)[0])
    prediction_flag = int(model.predict(feature_vector)[0])
    risk_signal = -decision_margin + (0.35 if prediction_flag == -1 else 0.0)
    risk_score = 1.0 / (1.0 + math.exp(-4.0 * risk_signal))
    confidence = round(min(abs(risk_signal), 1.0), 4)
    label = "abnormal" if risk_score >= 0.72 else "watch" if risk_score >= 0.48 else "normal"
    explanation = (
        "Sales behaviour is compared against a learned healthy retail pattern to identify unusual "
        "demand spikes, drops, or promotion-driven distortions."
    )
    prediction = ModelPrediction(
        model_name="demand-anomaly",
        risk_score=round(risk_score, 4),
        label=label,
        confidence=confidence,
        explanation=explanation,
        factors=explain_with_magnitude(payload.model_dump()),
    )
    return prediction.model_dump()
