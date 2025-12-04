from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/purchases", tags=["Закупки"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Purchase, status_code=status.HTTP_201_CREATED)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    return crud.create_purchase(db=db, purchase=purchase)

@router.get("/{purchase_id}", response_model=schemas.Purchase)
def read_purchase(purchase_id: str, db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Закупка не найдена")
    return db_purchase

@router.get("/", response_model=List[schemas.Purchase])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchases = crud.get_purchases(db, skip=skip, limit=limit)
    return purchases

@router.put("/{purchase_id}", response_model=schemas.Purchase)
def update_purchase(purchase_id: str, purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Закупка не найдена")
    return crud.update_purchase(db=db, purchase_id=purchase_id, purchase=purchase)

@router.delete("/{purchase_id}", response_model=schemas.Purchase)
def delete_purchase(purchase_id: str, db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Закупка не найдена")
    return crud.delete_purchase(db=db, purchase_id=purchase_id)