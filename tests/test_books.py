import pytest


def book_payload(title="Dune", author="Frank Herbert", isbn="9780441013593", year=1965):
    return {"title": title, "author": author, "isbn": isbn, "year": year}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add_books(client):
    response = client.post("/api/books", json=book_payload())
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Dune"


def test_duplicate_isbn_returns_409(client):
    client.post("/api/books", json=book_payload())
    response = client.post("/api/books", json=book_payload(title="Other"))
    assert response.status_code == 409


@pytest.mark.parametrize("bad_isbn", ["123", "97804410135931", "97804410135X3"])
def test_bad_isbn_returns_422(client, bad_isbn):
    response = client.post("/api/books", json=book_payload(isbn=bad_isbn))
    assert response.status_code == 422

@pytest.mark.parametrize("bad_year", [1449, 2027])
def test_bad_year_returns_422(client, bad_year):
    response = client.post("/api/books", json=book_payload(year=bad_year))
    assert response.status_code == 422

def test_patch_bad_year_returns_422(client):
    created = client.post("/api/books", json=book_payload()).json()
    response = client.patch(f"/api/books/{created['id']}", json={"year": 3000})
    assert response.status_code == 422

def test_get_books_filter_by_author(client):
    client.post("/api/books", json=book_payload())
    client.post("/api/books", json=book_payload(author="Ursula Le Guin", isbn="9780441478125"))
    response = client.get("/api/books", params={"author": "Ursula Le Guin"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["author"] == "Ursula Le Guin"


def test_get_book(client):
    created = client.post("/api/books", json=book_payload()).json()
    response = client.get(f"/api/books/{created['id']}")
    assert response.status_code == 200
    assert response.json()["isbn"] == "9780441013593"

def test_get_books(client):
    client.post("/api/books", json=book_payload())
    client.post("/api/books", json=book_payload(isbn="9780441478125"))
    response = client.get("/api/books")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_missing_book_returns_404(client):
    response = client.get("/api/books/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_patch_book(client):
    created = client.post("/api/books", json=book_payload()).json()
    response = client.patch(f"/api/books/{created['id']}", json={"year": 1966})
    assert response.status_code == 200
    assert response.json()["year"] == 1966
    assert response.json()["title"] == "Dune"
    assert response.json()["author"] == "Frank Herbert"


def test_patch_missing_book_returns_404(client):
    response = client.patch("/api/books/99", json={"year": 1966})
    assert response.status_code == 404


def test_delete_book(client):
    created = client.post("/api/books", json=book_payload()).json()
    response = client.delete(f"/api/books/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/api/books/{created['id']}").status_code == 404


def test_delete_missing_book_returns_404(client):
    response = client.delete("/api/books/99")
    assert response.status_code == 404
