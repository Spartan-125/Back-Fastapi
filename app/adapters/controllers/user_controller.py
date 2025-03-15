from typing import Optional, List
from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repository import UserRepository
from app.application.usecases.user_usecase import UserUseCase, UserCreate, UserUpdate, UserResponse


class UserController:
    """
    Controlador para las operaciones relacionadas con usuarios
    """
    @staticmethod
    def _get_usecase(db: Session) -> UserUseCase:
        """
        Obtiene una instancia del caso de uso de usuarios
        """
        user_repository = UserRepository(db)
        return UserUseCase(user_repository)
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> Optional[UserResponse]:
        """
        Crea un nuevo usuario
        """
        usecase = UserController._get_usecase(db)
        return usecase.create_user(user_data)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserResponse]:
        """
        Obtiene un usuario por su ID
        """
        usecase = UserController._get_usecase(db)
        return usecase.get_user_by_id(user_id)
        
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[UserResponse]:
        """
        Obtiene un usuario por su email
        """
        usecase = UserController._get_usecase(db)
        return usecase.get_user_by_email(email)
        
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Actualiza los datos de un usuario
        """
        usecase = UserController._get_usecase(db)
        return usecase.update_user(user_id, user_data)
        
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Elimina un usuario
        """
        usecase = UserController._get_usecase(db)
        return usecase.delete_user(user_id)
        
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """
        Lista usuarios con paginación
        """
        usecase = UserController._get_usecase(db)
        return usecase.list_users(skip, limit)