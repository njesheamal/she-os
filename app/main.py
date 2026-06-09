from fastapi import FastAPI 

app = FastAPI(
    title="SHÉ OS API",
    description="Backend API for SHÉ ESTATE's operaing system.",
    version="0.0.1",
)

@app.get("/")
def root():
    return {
        "message": "SHÉ OS backend is alive.",
        "mission": "First Light"
    }