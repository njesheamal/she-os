from fastapi import FastAPI
from dotenv import load_dotenv

from app.database.base import Base
from app.database.session import engine

load_dotenv()

app = FastAPI(
    title="SHÉ OS API",
    description="Backend API for SHÉ ESTATE's operating system.",
    version="0.0.1",
)


@app.get("/")
def root():
    return {
        "message": "SHÉ OS backend is alive.",
        "mission": "First Light",
    }


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)