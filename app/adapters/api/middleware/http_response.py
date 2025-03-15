from typing import Any, Dict, Optional, TypeVar, Generic
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.encoders import jsonable_encoder

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    data: Optional[T] = Field(default=None)
    error: Optional[Dict[str, Any]] = Field(default=None)

class ResponseStandardizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        
        # Solo interceptamos respuestas JSON
        if response.headers.get("content-type") == "application/json":
            try:
                response_body = await response.body()
                response_json = response_body.decode()
                
                # Evitamos procesar respuestas que ya tienen el formato estándar
                if '"data":' in response_json and '"error":' in response_json:
                    return response
                
                import json
                body_dict = json.loads(response_json)
                
                # Creamos la respuesta estandarizada
                if response.status_code >= 400:
                    standardized = {"data": None, "error": body_dict}
                else:
                    standardized = {"data": body_dict, "error": None}
                
                return JSONResponse(
                    status_code=response.status_code,
                    content=standardized,
                    headers=dict(response.headers),
                )
            except Exception as e:
                # Si hay un error al procesar la respuesta, devolvemos la original
                return response
        
        return response

# Función para crear respuestas estandarizadas directamente en los endpoints
def create_response(data=None, error=None, status_code=200):
    if error is not None and status_code < 400:
        status_code = 400  # Aseguramos que respuestas con error tienen códigos apropiados
        
    content = {"data": data, "error": error}
    return JSONResponse(
        status_code=status_code,
        content=content
    )

# Ejemplo de uso en un endpoint
def example_success_endpoint():
    user_data = {"id": 1, "name": "User"}
    return create_response(data=user_data)

def example_error_endpoint():
    error = {"message": "Resource not found", "code": "NOT_FOUND"}
    return create_response(error=error, status_code=404)

# Para configurar el middleware en tu aplicación principal
def configure_app(app: FastAPI):
    app.add_middleware(ResponseStandardizationMiddleware)
    return app