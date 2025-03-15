from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

from app.domain.entities import User
from app.domain.interfaces.repositories import UserRepositoryInterface
from app.infrastructure.auth.jwt import get_password_hash

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class UserUseCase:
    """
    Caso de uso para operaciones relacionadas con usuarios
    """
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    def create_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """
        Crea un nuevo usuario
        """
        # Verificar si el usuario ya existe
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            return None
            
        # Crear el usuario
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password)
        )
        created_user = self.user_repository.create(user)
        return UserResponse.model_validate(created_user)
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Obtiene un usuario por su ID
        """
        user = self.user_repository.get_by_id(user_id)
        if user:
            return UserResponse.model_validate(user)
        return None
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """
        Obtiene un usuario por su email
        """
        user = self.user_repository.get_by_email(email)
        if user:
            return UserResponse.model_validate(user)
        return None
        
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Actualiza los datos de un usuario
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
            
        # Actualizar solo los campos proporcionados
        if user_data.email is not None:
            # Verificar que el nuevo email no esté en uso por otro usuario
            if user_data.email != user.email:
                existing_user = self.user_repository.get_by_email(user_data.email)
                if existing_user and existing_user.id != user_id:
                    return None  # Email ya en uso
            user.email = user_data.email
            
        if user_data.password is not None:
            user.hashed_password = get_password_hash(user_data.password)
            
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
            
        updated_user = self.user_repository.update(user)
        return UserResponse.model_validate(updated_user)
        
    def delete_user(self, user_id: int) -> bool:
        """
        Elimina un usuario
        """
        return self.user_repository.delete(user_id)
        
    def list_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """
        Lista usuarios con paginación
        """
        users = self.user_repository.list(skip, limit)
        return [UserResponse.model_validate(user) for user in users]