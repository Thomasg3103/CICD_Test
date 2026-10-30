import httpx

from app.author_client import get_author_fetcher
from app.main import app


def fake_author(slug: str) -> dict:
    return {"name": "Frank Herbert", "country": "USA", "born": 1920}


def provide_fake_author():
    return fake_author


def fake_author_missing(slug: str):
    request = httpx.Request("GET", f"http://example.test/authors/{slug}")
    response = httpx.Response(404, request=request)
    raise httpx.HTTPStatusError("Not found", request=request, response=response)


def provide_missing_author():
    return fake_author_missing


def fake_author_server_error(slug: str):
    request = httpx.Request("GET", f"http://example.test/authors/{slug}")
    response = httpx.Response(500, request=request)
    raise httpx.HTTPStatusError("Server error", request=request, response=response)


def provide_server_error():
    return fake_author_server_error


def fake_author_service_down(slug: str):
    request = httpx.Request("GET", f"http://example.test/authors/{slug}")
    raise httpx.ConnectError("Connection refused", request=request)


def provide_service_down():
    return fake_author_service_down


def test_get_author(client):
    app.dependency_overrides[get_author_fetcher] = provide_fake_author
    try:
        response = client.get("/api/authors/frank-herbert")
        assert response.status_code == 200
        assert response.json()["name"] == "Frank Herbert"
    finally:
        app.dependency_overrides.pop(get_author_fetcher, None)


def test_author_not_found_returns_404(client):
    app.dependency_overrides[get_author_fetcher] = provide_missing_author
    try:
        response = client.get("/api/authors/nobody")
        assert response.status_code == 404
        assert response.json()["detail"] == "Author not found"
    finally:
        app.dependency_overrides.pop(get_author_fetcher, None)


def test_author_service_error_returns_502(client):
    app.dependency_overrides[get_author_fetcher] = provide_server_error
    try:
        response = client.get("/api/authors/frank-herbert")
        assert response.status_code == 502
    finally:
        app.dependency_overrides.pop(get_author_fetcher, None)


def test_author_service_down_returns_503(client):
    app.dependency_overrides[get_author_fetcher] = provide_service_down
    try:
        response = client.get("/api/authors/frank-herbert")
        assert response.status_code == 503
    finally:
        app.dependency_overrides.pop(get_author_fetcher, None)