from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import item  # ensure model imported

from app.api.routes.health import router as health_router
from app.api.routes.items import router as items_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(health_router)
app.include_router(items_router)
