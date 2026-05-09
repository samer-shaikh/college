from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db, get_current_user

router = APIRouter()

@router.post("/add")
def add_to_cart(item: schemas.CartItemCreate,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    cart_item = models.Cart(user_id=user.id, **item.dict())
    db.add(cart_item)
    db.commit()
    return {"message": "Added to cart"}

@router.get("/")
def get_cart(db: Session = Depends(get_db),
             user=Depends(get_current_user)):
    return db.query(models.Cart).filter(models.Cart.user_id == user.id).all()

@router.delete("/remove/{item_id}")
def remove_item(item_id: int,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):
    item = db.query(models.Cart).filter(
        models.Cart.id == item_id,
        models.Cart.user_id == user.id
    ).first()
    if item:
        db.delete(item)
        db.commit()
    return {"message": "Removed"}