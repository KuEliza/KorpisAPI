from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import SessionLocal

router = APIRouter(prefix="/service_requests", tags=["Заявки на обслуживание"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ServiceRequest, status_code=status.HTTP_201_CREATED)
def create_service_request(service_request: schemas.ServiceRequestCreate, db: Session = Depends(get_db)):
    return crud.create_service_request(db=db, service_request=service_request)

@router.get("/{request_id}", response_model=schemas.ServiceRequest)
def read_service_request(request_id: str, db: Session = Depends(get_db)):
    db_request = crud.get_service_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Заявка на обслуживание не найдена")
    return db_request

@router.get("/", response_model=List[schemas.ServiceRequest])
def read_service_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_service_requests(db, skip=skip, limit=limit)
    return requests

@router.put("/{request_id}", response_model=schemas.ServiceRequest)
def update_service_request(request_id: str, service_request: schemas.ServiceRequestCreate, db: Session = Depends(get_db)):
    db_request = crud.get_service_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Заявка на обслуживание не найдена")
    return crud.update_service_request(db=db, request_id=request_id, service_request=service_request)

@router.delete("/{request_id}", response_model=schemas.ServiceRequest)
def delete_service_request(request_id: str, db: Session = Depends(get_db)):
    db_request = crud.get_service_request(db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Заявка на обслуживание не найдена")
    return crud.delete_service_request(db=db, request_id=request_id)