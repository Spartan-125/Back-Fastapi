from datetime import timedelta
from sqlalchemy.orm import Session
from app.config.settings import get_settings
from app.infrastructure.auth.jwt import authenticate_user, create_access_token
from app.domain.entities import User

settings = get_settings()


class AuthController:
    @staticmethod
    def login(db: Session, username: str, password: str):
        """
        Autentica al usuario y genera un token JWT
        """
        user = authenticate_user(db, username, password)
        if not user:
            return None
        access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}