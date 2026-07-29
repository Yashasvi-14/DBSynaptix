from fastapi import FastAPI
from app.routers.database import router as database_router
from app.routers.query import router as query_router

app = FastAPI()
app.include_router(database_router)
app.include_router(query_router)

@app.get("/health")
def health():
    return {"status": "healthy"}

