# E-commerce Orders API

Backend API built with FastAPI to validate and process e-commerce orders.

## Purpose

This project simulates a backend service for an e-commerce system. It validates incoming orders, stores them in PostgreSQL and exposes endpoints to create and retrieve orders.

The project started as a simple FastAPI proof of concept and was later refactored into a more professional structure with routers, schemas, models, services, Docker and automated tests.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker Compose
- Pydantic
- Pytest

## Features

- Create e-commerce orders.
- Store orders and order items in PostgreSQL.
- Validate request data with Pydantic.
- Return structured API responses.
- Handle duplicated external order IDs.
- Health check endpoint.
- Automated tests with Pytest.
- Dockerized local environment.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API status |
| POST | `/orders/` | Create a new order |
| GET | `/orders/` | List all orders |
| GET | `/orders/{order_id}` | Get order by ID |

## Example Request

```json
{
  "external_order_id": "WC-1001",
  "customer_name": "Joaquín Lozano",
  "customer_email": "joaquin@example.com",
  "total": 89.97,
  "items": [
    {
      "product_name": "Curso de WordPress",
      "quantity": 1,
      "unit_price": 49.99
    },
    {
      "product_name": "Curso de WooCommerce",
      "quantity": 1,
      "unit_price": 39.98
    }
  ]
}