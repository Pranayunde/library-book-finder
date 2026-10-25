import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Library Book Finder" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_books_api_returns_all_books(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert len(response.json) == 5


def test_search_books_by_title(client):
    response = client.get("/api/books?q=Alchemist")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "The Alchemist"


def test_search_books_by_author(client):
    response = client.get("/api/books?q=James Clear")
    assert response.status_code == 200
    assert response.json[0]["title"] == "Atomic Habits"


def test_search_with_no_matches(client):
    response = client.get("/api/books?q=NoSuchBook")
    assert response.status_code == 200
    assert response.json == []


def test_get_book_by_id(client):
    response = client.get("/api/books/1")
    assert response.status_code == 200
    assert response.json["title"] == "The Alchemist"


def test_unknown_book_returns_404(client):
    response = client.get("/api/books/999")
    assert response.status_code == 404
    assert response.json == {"error": "Book not found"}
