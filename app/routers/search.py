from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import SessionLocal
from app import models

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

# ================= DATABASE =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= SEARCH =================
@router.get("/")
def search_products(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):

    products = db.query(models.Product).filter(
        or_(
            models.Product.name.ilike(f"%{q}%"),
            models.Product.description.ilike(f"%{q}%")
        )
    ).all()

    return {
        "success": True,
        "results": products
    }