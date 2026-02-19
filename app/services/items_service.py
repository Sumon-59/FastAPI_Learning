from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.item import Item
from app.schemas.items import ItemCreate, ItemUpdate

def create_item(db: Session, payload: ItemCreate) -> Item:
    item = Item(name=payload.name, price=payload.price, stock=payload.stock)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.get(Item, item_id)

def list_items(
    db: Session,
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Item]:
    stmt = select(Item)

    if q:
        stmt = stmt.where(Item.name.ilike(f"%{q.strip()}%"))
    if min_price is not None:
        stmt = stmt.where(Item.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Item.price <= max_price)

    stmt = stmt.order_by(Item.id.asc()).offset(offset).limit(limit)
    return list(db.execute(stmt).scalars().all())

def update_item(db: Session, item_id: int, payload: ItemUpdate) -> Optional[Item]:
    item = db.get(Item, item_id)
    if item is None:
        return None

    if payload.name is not None:
        item.name = payload.name
    if payload.price is not None:
        item.price = payload.price
    if payload.stock is not None:
        item.stock = payload.stock

    db.commit()
    db.refresh(item)
    return item
