from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.domain.entities import User
from app.application.usecases.user_usecase import UserCreate, UserResponse
from app.infrastructure.auth.jwt import get_current_active_user
from app.adapters.controllers.user_controller import UserController
from app.adapters.api.middleware.http_response import create_response

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = UserController.create_user(db, user_data)
        if not created_user:
            return create_response(
                error={"message": "Email already registered"},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return create_response(data=created_user.model_dump())
    except Exception as e:
        return create_response(
            error={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/me/")
def read_users_me(current_user: User = Depends(get_current_active_user)):
    try:
        user_response = UserResponse.model_validate(current_user)
        return create_response(data=user_response.model_dump())
    except Exception as e:
        return create_response(
            error={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    try:
        user = UserController.get_user_by_id(db, user_id)
        if user is None:
            return create_response(
                error={"message": "User not found"},
                status_code=status.HTTP_404_NOT_FOUND
            )
        return create_response(data=user.model_dump())
    except Exception as e:
        return create_response(
            error={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )