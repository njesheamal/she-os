from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from dotenv import load_dotenv

from app.database.session import engine
from app.routers import brand
from app.routers import partner
from app.routers import item
from app.routers import initiative
from app.routers import sourcing_trip
from app.routers import observation
from app.routers import decision
from app.routers import field_note
from app.routers import inventory_location
from app.routers import purchase_order
from app.routers import inbound_shipment
from app.routers import synthesis
from app.routers.associations import (
    brand_associations,
    decision_associations,
    initiative_associations,
    item_associations,
    observation_associations,
    sourcing_trip_associations,
)
from app.routers.inventory_movement import router as inventory_movement_router
from app.routers.inventory_movement import balances_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    yield
    # Shutdown
    engine.dispose()


app = FastAPI(
    title="SHÉ OS API",
    description="Backend API for SHÉ ESTATE's operating system.",
    version="0.0.1",
    lifespan=lifespan,
)

app.include_router(brand.router)
app.include_router(partner.router)
app.include_router(item.router)
app.include_router(initiative.router)
app.include_router(sourcing_trip.router)
app.include_router(observation.router)
app.include_router(decision.router)
app.include_router(field_note.router)
app.include_router(synthesis.router)
app.include_router(inventory_location.router)
app.include_router(purchase_order.router)
app.include_router(inbound_shipment.router)
app.include_router(brand_associations.router)
app.include_router(initiative_associations.router)
app.include_router(sourcing_trip_associations.router)
app.include_router(observation_associations.router)
app.include_router(decision_associations.router)
app.include_router(item_associations.router)
app.include_router(inventory_movement_router)
app.include_router(balances_router)


@app.get("/")
def root():
    return {
        "message": "SHÉ OS backend is alive.",
        "mission": "First Light",
    }