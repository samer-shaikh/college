from fastapi import APIRouter, Depends,Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db
from sqlalchemy.sql.expression import func

router = APIRouter()

@router.post("/")
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    return {"message": "Product added"}

@router.get("/",response_model=schemas.ProductListResponse)
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1, le=100),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    products = db.query(models.Product)\
        .offset(skip)\
        .limit(limit)\
        .all()

    total = db.query(models.Product).count()

    return {
        "data": products,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/suggestions")
def get_suggestions(
    exclude_id: int = Query(None),
    limit: int = Query(10, le=20),
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    # ❌ remove current product
    if exclude_id:
        query = query.filter(models.Product.id != exclude_id)

    # ✅ random order
    products = query.order_by(func.random()).limit(limit).all()

    return products

@router.get("/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
