from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_order_with_invalid_total_returns_422():
    payload = {
        "external_order_id": f"WC-{uuid4()}",
        "customer_name": "Joaquín Lozano",
        "customer_email": "joaquin@example.com",
        "total": -10,
        "items": [
            {
                "product_name": "Curso de WordPress",
                "quantity": 1,
                "unit_price": 49.99,
            }
        ],
    }

    response = client.post("/orders/", json=payload)

    assert response.status_code == 422


def test_create_order_without_items_returns_422():
    payload = {
        "external_order_id": f"WC-{uuid4()}",
        "customer_name": "Joaquín Lozano",
        "customer_email": "joaquin@example.com",
        "total": 49.99,
        "items": [],
    }

    response = client.post("/orders/", json=payload)

    assert response.status_code == 422


def test_create_order_successfully():
    payload = {
        "external_order_id": f"WC-{uuid4()}",
        "customer_name": "Joaquín Lozano",
        "customer_email": "joaquin@example.com",
        "total": 49.99,
        "items": [
            {
                "product_name": "Curso de WordPress",
                "quantity": 1,
                "unit_price": 49.99,
            }
        ],
    }

    response = client.post("/orders/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["customer_name"] == "Joaquín Lozano"
    assert data["customer_email"] == "joaquin@example.com"
    assert data["total"] == 49.99
    assert len(data["items"]) == 1
    assert data["items"][0]["product_name"] == "Curso de WordPress"