"""
In-memory items store ( CRUD + filtering + pagination )
This module implements a simple global in-memory storage for items with:
--- auto-incrementing integer IDs
--- creae, get, list(with filters), update
--- predictable ordering (sorted by id ascending)
--- basic validation + explicit type casting where appropriate

Designed to be lint-friendly(PEP 8), testable, and easy to extend
"""

from app.schemas.items import ItemCreate, ItemRead, ItemUpdate
from typing import Dict, List,Optional

#---------------------------------------------------
# Global Store
#---------------------------------------------------

GLOBAL_STORE: Dict[int, ItemRead] = {}
NEXT_ID: int = 1

MAX_LIMIT: int = 1000 #safety cap

def reset_store() -> None:
    """ DEV/TEST helper: clears store and resets ID counter."""
    global NEXT_ID       # intentional
    GLOBAL_STORE.clear()
    NEXT_ID = 1


def generate_id() -> int:
    """
    Generate a new unique integer ID(auto-increment).

    Return:
        int: The next available ID.
    """
    global NEXT_ID         # intentional 
    new_id = NEXT_ID
    NEXT_ID += 1
    return new_id

def create_item(item_create: ItemCreate) -> ItemRead:
    """
    create and store a new item.

    Args:
       item_create: Validated payload (name, price, stock).

    Returns:
       ItemRead: stored item with generated id.
    """

    new_id = generate_id()
    item_read = ItemRead(
        id = new_id,
        name = item_create.name,
        price = item_create.price,
        stock = item_create.stock,
    )       
    GLOBAL_STORE[new_id] = item_read
    return item_read

def get_item(item_id: int) -> Optional[ItemRead]:
    """
    Get an item by ID.
    
    Args:
       item_id: Item identifier
    
    Returns:
        ItemRead | None: The item if found, otherwise None
    """
    return GLOBAL_STORE.get(item_id)

def list_items(
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 100,
    offset: int = 0, 
) -> List[ItemRead]:
    """
    List items with optional filtering and pagination.

    Filters:
        q: case-insensitive substring match in name
        min_price/max_price: inclusive range

    Pagination:
        limit: Maximum number of items to return(>=0, capped by MAX_LIMIT).
        offset: Number of items to skip(>=0)

    Returns:
        list[ItemRead]: Filtered, sorted, and paginated items.
    """

    if limit < 0:
        raise ValueError("limit must be>=0")
    if offset < 0:
        raise ValueError("offset must be>=0")
    if min_price is not None and max_price is not None and min_price>max_price:
        raise ValueError("min_price cannot be greater than max_price")
    if limit > MAX_LIMIT:
        limit=MAX_LIMIT

    items = list(GLOBAL_STORE.values())

    # Filter by name query
    if q:
        needle = q.casefold()
        if needle:
            items = [it for it in items if needle in it.name.casefold()]
    
    
    # Filter by price range
    if min_price is not None:
        items = [it for it in items if it.price >= min_price]
    if max_price is not None:
        items = [it for it in items if it.price <= max_price]

    # Sort by id ascending 
    items.sort(key=lambda it: it.id)

    # Pagination 
    start = offset
    end = offset + limit
    return items[start:end]


def update_item(item_id: int, item_update: ItemUpdate) -> Optional[ItemRead]:
    """
    Update an existing item by ID (only provided fields are updated).

    Args:
        item_id: Item identifier.
        item_update: ItemUpdate payload with optional fields.

    Return:
        ItemRead : None: Updated item if found,otherwise None
    """
    existing = get_item(item_id)
    if existing is None:
        return None
    
    # Update only provided fields
    if item_update.name is not None:
        existing.name = item_update.name
    
    if item_update.price is not None:
        existing.price = item_update.price
    
    if item_update.stock is not None:
        existing.stock = item_update.stock
    
    GLOBAL_STORE[int(item_id)] = existing
    return existing

