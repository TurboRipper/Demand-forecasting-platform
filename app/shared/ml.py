from functools import lru_cache

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.linear_model import LogisticRegression


FEATURE_NAMES = [
    "effective_price_index",
    "discount_index",
    "daily_velocity",
    "weekly_velocity",
    "stock_cover_index",
    "demand_pressure",
    "promo_lift",
    "seasonal_signal",
    "price_sensitivity",
    "replenishment_gap",
    "revenue_potential",
    "lead_time_index",
    "category_index",
]

DISPLAY_LABELS = {
    "effective_price_index": "price level",
    "discount_index": "discount intensity",
    "daily_velocity": "daily sales velocity",
    "weekly_velocity": "weekly sales velocity",
    "stock_cover_index": "stock cover",
    "demand_pressure": "demand pressure",
    "promo_lift": "promotion lift",
    "seasonal_signal": "seasonal demand",
    "price_sensitivity": "price sensitivity",
    "replenishment_gap": "replenishment gap",
    "revenue_potential": "revenue potential",
    "lead_time_index": "supplier lead time",
    "category_index": "category demand bias",
}


def vectorize(processed: dict) -> np.ndarray:
    return np.array([processed[name] for name in FEATURE_NAMES], dtype=float)


def explain_with_weights(weights: np.ndarray, processed: dict, top_n: int = 3) -> list[str]:
    contributions = np.abs(weights * vectorize(processed))
    ranked_indices = np.argsort(contributions)[::-1][:top_n]
    return [DISPLAY_LABELS[FEATURE_NAMES[index]] for index in ranked_indices]


def explain_with_magnitude(processed: dict, top_n: int = 3) -> list[str]:
    magnitudes = np.abs(vectorize(processed))
    ranked_indices = np.argsort(magnitudes)[::-1][:top_n]
    return [DISPLAY_LABELS[FEATURE_NAMES[index]] for index in ranked_indices]


@lru_cache
def get_demand_model() -> RandomForestRegressor:
    rng = np.random.default_rng(41)
    size = 3000
    effective_price_index = np.clip(rng.normal(0.26, 0.11, size), 0.05, 0.95)
    discount_index = np.clip(np.abs(rng.normal(0.24, 0.18, size)), 0.0, 1.0)
    daily_velocity = np.clip(rng.normal(0.42, 0.24, size), 0.02, 1.8)
    weekly_velocity = np.clip(rng.normal(0.39, 0.2, size), 0.02, 1.5)
    stock_cover_index = np.clip(np.abs(rng.normal(0.82, 0.38, size)), 0.05, 2.0)
    demand_pressure = 0.42 * daily_velocity + 0.33 * weekly_velocity + 0.25 * np.clip(rng.normal(1.0, 0.22, size), 0.4, 1.7)
    promo_lift = np.clip(0.5 * discount_index + 0.5 * rng.binomial(1, 0.36, size), 0, 1.5)
    seasonal_signal = np.clip(0.45 * rng.binomial(1, 0.2, size) + 0.55 * np.clip(rng.normal(0.38, 0.24, size), 0, 1.3), 0, 1.7)
    price_sensitivity = np.clip((0.58 - effective_price_index) + 0.35 * discount_index, 0, 1.6)
    replenishment_gap = np.clip(np.abs(rng.normal(0.16, 0.18, size)), 0, 1.5)
    revenue_potential = np.clip(0.42 * effective_price_index + 0.58 * daily_velocity, 0, 1.8)
    lead_time_index = np.clip(np.abs(rng.normal(0.28, 0.18, size)), 0.02, 1.2)
    category_index = np.clip(rng.normal(0.38, 0.2, size), 0.02, 1.2)

    X = np.column_stack(
        [
            effective_price_index,
            discount_index,
            daily_velocity,
            weekly_velocity,
            stock_cover_index,
            demand_pressure,
            promo_lift,
            seasonal_signal,
            price_sensitivity,
            replenishment_gap,
            revenue_potential,
            lead_time_index,
            category_index,
        ]
    )

    y = (
        18
        + 54 * daily_velocity
        + 46 * weekly_velocity
        + 38 * promo_lift
        + 34 * seasonal_signal
        + 22 * price_sensitivity
        + 14 * category_index
        - 19 * effective_price_index
        + rng.normal(0, 8.5, size)
    )
    y = np.clip(y, 6, 260)

    model = RandomForestRegressor(n_estimators=180, random_state=41)
    model.fit(X, y)
    return model


@lru_cache
def get_stockout_model() -> LogisticRegression:
    rng = np.random.default_rng(43)
    size = 2500
    effective_price_index = np.clip(rng.normal(0.24, 0.1, size), 0.05, 0.95)
    discount_index = np.clip(np.abs(rng.normal(0.22, 0.18, size)), 0.0, 1.0)
    daily_velocity = np.clip(rng.normal(0.46, 0.26, size), 0.02, 1.7)
    weekly_velocity = np.clip(rng.normal(0.43, 0.22, size), 0.02, 1.6)
    stock_cover_index = np.clip(np.abs(rng.normal(0.72, 0.42, size)), 0.05, 2.0)
    demand_pressure = 0.4 * daily_velocity + 0.35 * weekly_velocity + 0.25 * np.clip(rng.normal(1.0, 0.25, size), 0.4, 1.7)
    promo_lift = np.clip(0.55 * discount_index + 0.45 * rng.binomial(1, 0.34, size), 0, 1.5)
    seasonal_signal = np.clip(0.45 * rng.binomial(1, 0.18, size) + 0.55 * np.clip(rng.normal(0.34, 0.2, size), 0, 1.3), 0, 1.7)
    price_sensitivity = np.clip((0.56 - effective_price_index) + 0.32 * discount_index, 0, 1.6)
    replenishment_gap = np.clip(np.abs(rng.normal(0.22, 0.24, size)), 0, 1.5)
    revenue_potential = np.clip(0.45 * effective_price_index + 0.55 * daily_velocity, 0, 1.8)
    lead_time_index = np.clip(np.abs(rng.normal(0.34, 0.22, size)), 0.02, 1.2)
    category_index = np.clip(rng.normal(0.36, 0.18, size), 0.02, 1.2)

    X = np.column_stack(
        [
            effective_price_index,
            discount_index,
            daily_velocity,
            weekly_velocity,
            stock_cover_index,
            demand_pressure,
            promo_lift,
            seasonal_signal,
            price_sensitivity,
            replenishment_gap,
            revenue_potential,
            lead_time_index,
            category_index,
        ]
    )

    latent = (
        1.2 * demand_pressure
        + 1.1 * promo_lift
        + 1.4 * replenishment_gap
        + 1.35 * lead_time_index
        + 0.7 * seasonal_signal
        - 1.5 * stock_cover_index
        + rng.normal(0, 0.75, size)
    )
    y = (latent > 0.95).astype(int)
    model = LogisticRegression(max_iter=500)
    model.fit(X, y)
    return model


@lru_cache
def get_demand_anomaly_model() -> IsolationForest:
    rng = np.random.default_rng(47)
    size = 3000
    effective_price_index = np.clip(rng.normal(0.24, 0.08, size), 0.05, 0.8)
    discount_index = np.clip(np.abs(rng.normal(0.18, 0.12, size)), 0.0, 0.9)
    daily_velocity = np.clip(rng.normal(0.34, 0.18, size), 0.02, 1.2)
    weekly_velocity = np.clip(rng.normal(0.36, 0.16, size), 0.02, 1.1)
    stock_cover_index = np.clip(np.abs(rng.normal(0.9, 0.25, size)), 0.2, 1.8)
    demand_pressure = 0.42 * daily_velocity + 0.33 * weekly_velocity + 0.25 * np.clip(rng.normal(0.96, 0.14, size), 0.5, 1.3)
    promo_lift = np.clip(0.45 * discount_index + 0.55 * rng.binomial(1, 0.18, size), 0, 1.0)
    seasonal_signal = np.clip(0.38 * rng.binomial(1, 0.12, size) + 0.62 * np.clip(rng.normal(0.3, 0.14, size), 0, 1.0), 0, 1.2)
    price_sensitivity = np.clip((0.52 - effective_price_index) + 0.3 * discount_index, 0, 1.2)
    replenishment_gap = np.clip(np.abs(rng.normal(0.1, 0.12, size)), 0, 0.9)
    revenue_potential = np.clip(0.42 * effective_price_index + 0.58 * daily_velocity, 0, 1.2)
    lead_time_index = np.clip(np.abs(rng.normal(0.26, 0.12, size)), 0.02, 0.9)
    category_index = np.clip(rng.normal(0.32, 0.12, size), 0.02, 0.9)

    X = np.column_stack(
        [
            effective_price_index,
            discount_index,
            daily_velocity,
            weekly_velocity,
            stock_cover_index,
            demand_pressure,
            promo_lift,
            seasonal_signal,
            price_sensitivity,
            replenishment_gap,
            revenue_potential,
            lead_time_index,
            category_index,
        ]
    )

    model = IsolationForest(contamination=0.08, n_estimators=180, random_state=47)
    model.fit(X)
    return model
