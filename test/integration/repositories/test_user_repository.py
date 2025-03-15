import pytest
from sqlalchemy.orm import Session
from app.domain.entities import User
from app.infrastructure.repositories.user_repository import UserRepository


@pytest.mark.integration
class TestUserRepository:
    """Tests de integración para el repositorio de usuarios"""
    
    def test_create_user(self, db_session: Session):
        """Test para crear usuario"""
        # Arrange
        repository = UserRepository(db_session)
        user = User(email="repo_test@example.com", hashed_password="hashed_password")
        
        # Act
        created_user = repository.create(user)
        
        # Assert
        assert created_user.id is not None
        assert created_user.email == "repo_test@example.com"
        assert created_user.hashed_password == "hashed_password"
        
        # Verificar que se guardó en la base de datos
        db_user = db_session.query(User).filter_by(id=created_user.id).first()
        assert db_user is not None
        assert db_user.email == "repo_test@example.com"
        
        # Limpiar
        db_session.delete(db_user)
        db_session.commit()
        
    def test_get_by_id(self, db_session: Session):
        """Test para obtener usuario por ID"""
        # Arrange
        repository = UserRepository(db_session)
        user = User(email="get_by_id@example.com", hashed_password="hashed_password")
        db_session.add(user)
        db_session.commit()
        
        # Act
        result = repository.get_by_id(user.id)
        
        # Assert
        assert result is not None
        assert result.id == user.id
        assert result.email == "get_by_id@example.com"
        
        # Limpiar
        db_session.delete(user)
        db_session.commit()
        
    def test_get_by_email(self, db_session: Session):
        """Test para obtener usuario por email"""
        # Arrange
        repository = UserRepository(db_session)
        user = User(email="get_by_email@example.com", hashed_password="hashed_password")
        db_session.add(user)
        db_session.commit()
        
        # Act
        result = repository.get_by_email("get_by_email@example.com")
        
        # Assert
        assert result is not None
        assert result.id == user.id
        assert result.email == "get_by_email@example.com"
        
        # Limpiar
        db_session.delete(user)
        db_session.commit()
        
    def test_update_user(self, db_session: Session):
        """Test para actualizar usuario"""
        # Arrange
        repository = UserRepository(db_session)
        user = User(email="before_update@example.com", hashed_password="original_password")
        db_session.add(user)
        db_session.commit()
        
        # Modificar el usuario
        user.email = "after_update@example.com"
        user.hashed_password = "new_password"
        
        # Act
        updated_user = repository.update(user)
        
        # Assert
        assert updated_user.email == "after_update@example.com"
        assert updated_user.hashed_password == "new_password"
        
        # Verificar en la base de datos
        db_user = db_session.query(User).filter_by(id=user.id).first()
        assert db_user.email == "after_update@example.com"
        
        # Limpiar
        db_session.delete(user)
        db_session.commit()
        
    def test_delete_user(self, db_session: Session):
        """Test para eliminar usuario"""
        # Arrange
        repository = UserRepository(db_session)
        user = User(email="to_delete@example.com", hashed_password="delete_me")
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        
        # Act
        result = repository.delete(user_id)
        
        # Assert
        assert result is True
        deleted_user = db_session.query(User).filter_by(id=user_id).first()
        assert deleted_user is None
        
    def test_delete_nonexistent_user(self, db_session: Session):
        """Test para eliminar un usuario que no existe"""
        # Arrange
        repository = UserRepository(db_session)
        
        # Act
        result = repository.delete(999)
        
        # Assert
        assert result is False
        
    def test_list_users(self, db_session: Session):
        """Test para listar usuarios"""
        # Arrange
        repository = UserRepository(db_session)
        
        # Crear algunos usuarios de prueba
        users = [
            User(email="list1@example.com", hashed_password="pwd1"),
            User(email="list2@example.com", hashed_password="pwd2"),
            User(email="list3@example.com", hashed_password="pwd3")
        ]
        for user in users:
            db_session.add(user)
        db_session.commit()
        
        # Act
        result = repository.list(skip=0, limit=10)
        
        # Assert - Verificar que al menos los usuarios creados están en la lista
        emails = [user.email for user in result]
        for user in users:
            assert user.email in emails
        
        # Limpiar
        for user in users:
            db_session.delete(user)
        db_session.commit()