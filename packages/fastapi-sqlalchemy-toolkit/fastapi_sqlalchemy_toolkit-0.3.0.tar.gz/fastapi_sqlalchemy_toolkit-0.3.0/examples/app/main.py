from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.api import api_router

app = FastAPI(
    title="fastapi-sqlalchemy-toolkit demo",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
