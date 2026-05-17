from fastapi import FastAPI

from app.interface.api.routers import document_router

app = FastAPI()

app.include_router(document_router)
