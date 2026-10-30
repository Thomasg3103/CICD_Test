import os

import httpx

AUTHOR_SERVICE_URL = os.getenv("AUTHOR_SERVICE_URL", "http://127.0.0.1:8001")


def fetch_author(slug) -> dict:
    response = httpx.get(f"{AUTHOR_SERVICE_URL}/authors/{slug}", timeout=3.0)
    response.raise_for_status()
    return response.json()


def get_author_fetcher():
    return fetch_author
