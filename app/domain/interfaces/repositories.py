from typing import List, Optional
from abc import ABC, abstractmethod
from app.domain.entities import User

class UserRepositoryInterface(ABC):
    """
    Interfaz que define el contrato para los repositorios de usuarios
    """
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su email"""
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Crea un nuevo usuario"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID"""
        pass
    
    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Lista usuarios con paginación"""
        pass