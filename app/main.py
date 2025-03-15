from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import get_settings
from app.config.database import engine, Base
from app.adapters.api.router import api_router
from app.adapters.api.middleware.middleware import ExceptionMiddleware
from app.adapters.api.middleware.http_response import configure_app
from app.adapters.api.middleware.exception_handler import add_exception_handlers

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

add_exception_handlers(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom exception handling middleware
app.add_middleware(ExceptionMiddleware)

# Include API router
app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

app = configure_app(app)