from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from dotenv import load_dotenv

from app.database.session import engine
from app.routers import brand
from app.routers import partner
from app.routers import item
from app.routers import initiative

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

@app.get("/")
def root():
    return {
        "message": "SHÉ OS backend is alive.",
        "mission": "First Light",
    }