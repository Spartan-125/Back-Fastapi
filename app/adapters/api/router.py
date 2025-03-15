from fastapi import APIRouter
from app.adapters.api.routes import auth_routes, user_routes

api_router = APIRouter()

# Incluir las rutas desde los módulos de rutas
api_router.include_router(auth_routes.router, prefix="/v1")
api_router.include_router(user_routes.router, prefix="/v1")