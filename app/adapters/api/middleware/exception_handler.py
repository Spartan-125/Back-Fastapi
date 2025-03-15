from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def add_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "data": None,
                "error": {"message": exc.detail, "status_code": exc.status_code}
            },
            headers=exc.headers  # Importante para mantener los headers de autenticación
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "data": None,
                "error": {"message": "Validation error", "details": exc.errors()}
            }
        )
    
    # Puedes agregar más manejadores de excepciones aquí