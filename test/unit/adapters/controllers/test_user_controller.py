import pytest
from unittest.mock import MagicMock, patch
from app.adapters.controllers.user_controller import UserController
from app.application.usecases.user_usecase import UserCreate, UserUpdate, UserResponse


class TestUserController:
    """Tests para el controlador de usuarios"""
    
    def test_create_user(self):
        """Test para la creación de usuario"""
        # Arrange
        mock_db = MagicMock()
        user_data = UserCreate(email="test@example.com", password="password123")
        expected_response = UserResponse(id=1, email="test@example.com", is_active=True)
        
        # Mock el caso de uso
        with patch('app.adapters.controllers.user_controller.UserUseCase') as mock_usecase_class:
            mock_usecase = mock_usecase_class.return_value
            mock_usecase.create_user.return_value = expected_response
            
            # Act
            result = UserController.create_user(mock_db, user_data)
            
            # Assert
            assert result == expected_response
            mock_usecase.create_user.assert_called_once_with(user_data)
    
    def test_get_user_by_id(self):
        """Test para obtener usuario por ID"""
        # Arrange
        mock_db = MagicMock()
        user_id = 1
        expected_response = UserResponse(id=1, email="test@example.com", is_active=True)
        
        # Mock el caso de uso
        with patch('app.adapters.controllers.user_controller.UserUseCase') as mock_usecase_class:
            mock_usecase = mock_usecase_class.return_value
            mock_usecase.get_user_by_id.return_value = expected_response
            
            # Act
            result = UserController.get_user_by_id(mock_db, user_id)
            
            # Assert
            assert result == expected_response
            mock_usecase.get_user_by_id.assert_called_once_with(user_id)
    
    def test_get_user_by_id_not_found(self):
        """Test para obtener usuario por ID cuando no existe"""
        # Arrange
        mock_db = MagicMock()
        user_id = 999
        
        # Mock el caso de uso
        with patch('app.adapters.controllers.user_controller.UserUseCase') as mock_usecase_class:
            mock_usecase = mock_usecase_class.return_value
            mock_usecase.get_user_by_id.return_value = None
            
            # Act
            result = UserController.get_user_by_id(mock_db, user_id)
            
            # Assert
            assert result is None
            mock_usecase.get_user_by_id.assert_called_once_with(user_id)