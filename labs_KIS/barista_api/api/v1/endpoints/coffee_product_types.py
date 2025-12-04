from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/coffee_product_types", tags=["Типы кофейной продукции"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.CoffeeProductType])
def read_coffee_product_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_coffee_product_types(db, skip=skip, limit=limit)

@router.get("/{coffee_type_id}", response_model=schemas.CoffeeProductType)
def read_coffee_product_type(coffee_type_id: str, db: Session = Depends(get_db)):
    db_coffee_type = crud.get_coffee_product_type(db, coffee_type_id=coffee_type_id)
    if db_coffee_type is None:
        raise HTTPException(status_code=404, detail="Тип кофейной продукции не найден")
    return db_coffee_type