from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import User
from app.domain.interfaces.repositories import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):
    """
    Implementación de repositorio de usuarios para PostgreSQL con SQLAlchemy
    """
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user: User) -> User:
        """
        Crea un nuevo usuario
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user: User) -> User:
        """
        Actualiza un usuario existente
        """
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario por su ID
        """
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
        
    def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lista usuarios con paginación
        """
        return self.db.query(User).offset(skip).limit(limit).all()