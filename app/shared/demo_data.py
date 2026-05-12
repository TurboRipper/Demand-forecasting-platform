from copy import deepcopy


SCENARIOS = [
    {
        "id": "steady_baseline",
        "title": "Steady Baseline",
        "description": "Normal weekday demand with balanced stock and no active promotion.",
        "payload": {
            "scenario_id": "steady_baseline",
            "product_id": "SKU-1042",
            "store_id": "STORE-A1",
            "timestamp": "2026-05-11T09:05:00Z",
            "category": "Grocery",
            "base_price": 18.5,
            "discount_pct": 5.0,
            "inventory_units": 210.0,
            "prior_day_sales": 34.0,
            "prior_week_sales": 228.0,
            "footfall_index": 0.92,
            "promotion_flag": 0,
            "holiday_flag": 0,
            "weekday_index": 1,
            "lead_time_days": 3.0,
        },
    },
    {
        "id": "promo_surge",
        "title": "Promo Surge",
        "description": "Discount-heavy promotion causing sharp demand acceleration on a fast-moving SKU.",
        "payload": {
            "scenario_id": "promo_surge",
            "product_id": "SKU-2207",
            "store_id": "STORE-B4",
            "timestamp": "2026-05-11T10:40:00Z",
            "category": "Beverages",
            "base_price": 24.0,
            "discount_pct": 28.0,
            "inventory_units": 165.0,
            "prior_day_sales": 72.0,
            "prior_week_sales": 402.0,
            "footfall_index": 1.24,
            "promotion_flag": 1,
            "holiday_flag": 0,
            "weekday_index": 4,
            "lead_time_days": 4.0,
        },
    },
    {
        "id": "festival_peak",
        "title": "Festival Peak",
        "description": "Holiday-driven spike with elevated footfall and heavy seasonal demand pressure.",
        "payload": {
            "scenario_id": "festival_peak",
            "product_id": "SKU-0789",
            "store_id": "STORE-C2",
            "timestamp": "2026-05-11T13:20:00Z",
            "category": "Snacks",
            "base_price": 12.0,
            "discount_pct": 18.0,
            "inventory_units": 148.0,
            "prior_day_sales": 84.0,
            "prior_week_sales": 476.0,
            "footfall_index": 1.48,
            "promotion_flag": 1,
            "holiday_flag": 1,
            "weekday_index": 5,
            "lead_time_days": 5.0,
        },
    },
    {
        "id": "inventory_crunch",
        "title": "Inventory Crunch",
        "description": "Demand remains healthy but inventory is thin and supplier lead time is rising.",
        "payload": {
            "scenario_id": "inventory_crunch",
            "product_id": "SKU-3054",
            "store_id": "STORE-D7",
            "timestamp": "2026-05-11T16:55:00Z",
            "category": "Personal Care",
            "base_price": 36.0,
            "discount_pct": 8.0,
            "inventory_units": 42.0,
            "prior_day_sales": 28.0,
            "prior_week_sales": 206.0,
            "footfall_index": 1.06,
            "promotion_flag": 0,
            "holiday_flag": 0,
            "weekday_index": 2,
            "lead_time_days": 8.0,
        },
    },
]


def get_scenarios() -> list[dict]:
    return deepcopy(SCENARIOS)


def get_scenario_by_id(scenario_id: str) -> dict | None:
    for scenario in SCENARIOS:
        if scenario["id"] == scenario_id:
            return deepcopy(scenario)
    return None

