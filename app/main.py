from fastapi import FastAPI
from app.routes.data_routes import router as api_router

app = FastAPI(
    title="Atividade 2 - FastAPI + Pytest",
    description="API que consome dados externos e demonstra integração contínua.",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api", tags=["External Data"])


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API is running successfully 🚀"}
