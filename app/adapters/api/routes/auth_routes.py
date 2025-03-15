from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.infrastructure.auth.jwt import Token
from app.adapters.controllers.auth_controller import AuthController
from app.adapters.api.middleware.http_response import create_response

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        token_data = AuthController.login(db, form_data.username, form_data.password)
        if not token_data:
            return create_response(
                error={"message": "Incorrect email or password"},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        return create_response(data=token_data)
    except Exception as e:
        return create_response(
            error={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )