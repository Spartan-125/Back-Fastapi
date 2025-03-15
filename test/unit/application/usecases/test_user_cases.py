import pytest
from unittest.mock import Mock
from app.domain.entities import User
from app.application.usecases.user_usecase import UserUseCase, UserCreate, UserUpdate, UserResponse


class TestUserUseCase:
    """Tests para el caso de uso de usuarios"""
    
    def test_create_user_success(self, monkeypatch):
        """Test para crear usuario exitosamente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_email.return_value = None
        
        # Simular creación exitosa
        mock_user = User(id=1, email="test@example.com", is_active=True)
        mock_repository.create.return_value = mock_user
        
        usecase = UserUseCase(mock_repository)
        user_data = UserCreate(email="test@example.com", password="password123")
        
        # Act
        # Usar monkeypatch directamente como fixture
        monkeypatch.setattr('app.application.usecases.user_usecase.get_password_hash', 
                    lambda password: f"hashed_{password}")
            
        result = usecase.create_user(user_data)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.email == "test@example.com"
        assert result.is_active is True
        
        # Verificar que se llamó al repositorio correctamente
        mock_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_repository.create.assert_called_once()
        
    def test_create_user_email_exists(self):
        """Test para crear usuario cuando el email ya existe"""
        # Arrange
        mock_repository = Mock()
        # Simular que el email ya existe
        mock_repository.get_by_email.return_value = User(id=1, email="test@example.com")
        
        usecase = UserUseCase(mock_repository)
        user_data = UserCreate(email="test@example.com", password="password123")
        
        # Act
        result = usecase.create_user(user_data)
        
        # Assert
        assert result is None
        mock_repository.get_by_email.assert_called_once_with("test@example.com")
        mock_repository.create.assert_not_called()
        
    def test_get_user_by_id_exists(self):
        """Test para obtener usuario por ID cuando existe"""
        # Arrange
        mock_repository = Mock()
        mock_user = User(id=1, email="test@example.com", is_active=True)
        mock_repository.get_by_id.return_value = mock_user
        
        usecase = UserUseCase(mock_repository)
        
        # Act
        result = usecase.get_user_by_id(1)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.email == "test@example.com"
        mock_repository.get_by_id.assert_called_once_with(1)
        
    def test_get_user_by_id_not_exists(self):
        """Test para obtener usuario por ID cuando no existe"""
        # Arrange
        mock_repository = Mock()
        mock_repository.get_by_id.return_value = None
        
        usecase = UserUseCase(mock_repository)
        
        # Act
        result = usecase.get_user_by_id(999)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(999)
        
    def test_update_user_success(self, monkeypatch):  # Agrega monkeypatch como parámetro
        """Test para actualizar usuario exitosamente"""
        # Arrange
        mock_repository = Mock()
        mock_user = User(id=1, email="old@example.com", is_active=True)
        mock_repository.get_by_id.return_value = mock_user
        
        # Simular que el nuevo email no está en uso
        mock_repository.get_by_email.return_value = None
        
        # Simular actualización exitosa
        mock_updated_user = User(id=1, email="new@example.com", is_active=False)
        mock_repository.update.return_value = mock_updated_user
        
        usecase = UserUseCase(mock_repository)
        user_update = UserUpdate(email="new@example.com", is_active=False)
        
        # Act
        # Usa directamente el monkeypatch pasado como parámetro
        monkeypatch.setattr('app.application.usecases.user_usecase.get_password_hash', 
                    lambda password: f"hashed_{password}")
            
        result = usecase.update_user(1, user_update)
        
        # Assert
        assert result is not None
        assert result.id == 1
        assert result.email == "new@example.com"
        assert result.is_active is False
        
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.get_by_email.assert_called_once_with("new@example.com")
        mock_repository.update.assert_called_once()
        
    def test_update_user_email_exists(self):
        """Test para actualizar usuario cuando el nuevo email ya está en uso"""
        # Arrange
        mock_repository = Mock()
        mock_user = User(id=1, email="old@example.com", is_active=True)
        mock_repository.get_by_id.return_value = mock_user
        
        # Simular que el nuevo email ya está en uso por otro usuario
        other_user = User(id=2, email="new@example.com", is_active=True)
        mock_repository.get_by_email.return_value = other_user
        
        usecase = UserUseCase(mock_repository)
        user_update = UserUpdate(email="new@example.com")
        
        # Act
        result = usecase.update_user(1, user_update)
        
        # Assert
        assert result is None
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.get_by_email.assert_called_once_with("new@example.com")
        mock_repository.update.assert_not_called()
        
    def test_delete_user_success(self):
        """Test para eliminar usuario exitosamente"""
        # Arrange
        mock_repository = Mock()
        mock_repository.delete.return_value = True
        
        usecase = UserUseCase(mock_repository)
        
        # Act
        result = usecase.delete_user(1)
        
        # Assert
        assert result is True
        mock_repository.delete.assert_called_once_with(1)
        
    def test_list_users(self):
        """Test para listar usuarios"""
        # Arrange
        mock_repository = Mock()
        mock_users = [
            User(id=1, email="user1@example.com", is_active=True),
            User(id=2, email="user2@example.com", is_active=False)
        ]
        mock_repository.list.return_value = mock_users
        
        usecase = UserUseCase(mock_repository)
        
        # Act
        result = usecase.list_users(skip=0, limit=10)
        
        # Assert
        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].email == "user1@example.com"
        assert result[1].id == 2
        assert result[1].email == "user2@example.com"
        mock_repository.list.assert_called_once_with(0, 10)