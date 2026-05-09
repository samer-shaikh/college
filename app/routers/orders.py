from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db, get_current_user

router = APIRouter()

@router.post("/")
def create_order(order: schemas.OrderCreate,
                 db: Session = Depends(get_db),
                 user=Depends(get_current_user)):

    total = 0
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if product:
            total += product.price * item.quantity

    db_order = models.Order(user_id=user.id, total=total)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db.add(models.OrderItem(order_id=db_order.id,
                                product_id=item.product_id,
                                quantity=item.quantity))
    db.commit()

    return {"message": "Order placed", "order_id": db_order.id}