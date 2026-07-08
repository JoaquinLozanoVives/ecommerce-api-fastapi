from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate


def create_order(db: Session, order_data: OrderCreate) -> Order:
    existing_order = (
        db.query(Order)
        .filter(Order.external_order_id == order_data.external_order_id)
        .first()
    )

    if existing_order:
        raise ValueError("Order already exists")

    order = Order(
        external_order_id=order_data.external_order_id,
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        total=order_data.total,
        status="received",
    )

    for item in order_data.items:
        order.items.append(
            OrderItem(
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


def list_orders(db: Session) -> list[Order]:
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: int) -> Order | None:
    return db.get(Order, order_id)