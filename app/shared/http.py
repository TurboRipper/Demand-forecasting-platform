from typing import Any

import requests

from app.shared.config import get_settings


def post_json(url: str, payload: dict[str, Any]) -> Any:
    timeout = get_settings().request_timeout_seconds
    response = requests.post(url, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_json(url: str) -> Any:
    timeout = get_settings().request_timeout_seconds
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()

