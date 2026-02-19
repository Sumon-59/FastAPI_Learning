from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.items import ItemCreate, ItemRead, ItemUpdate
from app.services.items_service import create_item, get_item, list_items, update_item

router = APIRouter(tags=["items"])

@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(payload: ItemCreate, db: Session = Depends(get_db)) -> ItemRead:
    return create_item(db, payload)

@router.get("/items", response_model=list[ItemRead])
def list_items_endpoint(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    limit: int = Query(default=100, ge=0, le=1000),
    offset: int = Query(default=0, ge=0),
) -> list[ItemRead]:
    return list_items(db, q=q, min_price=min_price, max_price=max_price, limit=limit, offset=offset)

@router.get("/items/{item_id}", response_model=ItemRead)
def get_item_endpoint(item_id: int, db: Session = Depends(get_db)) -> ItemRead:
    item = get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.patch("/items/{item_id}", response_model=ItemRead)
def update_item_endpoint(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)) -> ItemRead:
    item = update_item(db, item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
