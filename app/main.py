from fastapi import FastAPI
from app.routers.database import router as database_router
from app.routers.query import router as query_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        *(
            [os.getenv("FRONTEND_URL")]
            if os.getenv("FRONTEND_URL")
            else []
        ),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(database_router)
app.include_router(query_router)

@app.get("/health")
def health():
    return {"status": "healthy"}

