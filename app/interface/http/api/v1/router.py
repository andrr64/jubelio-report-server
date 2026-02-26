from fastapi import APIRouter
from app.interface.http.api.v1.reports.generate.routes import router

api_router = APIRouter()
api_router.include_router(router, prefix="/reports", tags=["Reports"])
