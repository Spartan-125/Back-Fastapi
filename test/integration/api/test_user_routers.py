import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.integration
class TestUserRoutes:
    """Tests de integración para las rutas de usuarios"""
    
    def test_create_user(self):
        """Test para crear un nuevo usuario a través de la API"""
        # Arrange
        user_data = {
            "email": "api_test@example.com",
            "password": "securePassword123"
        }
        
        # Act
        response = client.post("/api/v1/users/", json=user_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "password" not in data  # Asegurarse que no se devuelve la contraseña
        
        # Cleanup - Eliminar el usuario creado para tests futuros
        # Esto requeriría autenticación admin o un endpoint especial para tests
    
    def test_create_user_duplicate_email(self, authenticated_client, test_user):
        """Test para crear un usuario con email duplicado"""
        # Arrange
        user_data = {
            "email": test_user.email,  # Email que ya existe
            "password": "anotherPassword"
        }

        # Act
        response = client.post("/api/v1/users/", json=user_data)
        
        # Assert
        assert response.status_code == 400  # Bad Request o 409 Conflict
        assert "error" in response.json() or "detail" in response.json()
    
    def test_get_user_by_id(self, authenticated_client, test_user):
        """Test para obtener un usuario por ID"""
        # Act
        response = authenticated_client.get(f"/api/v1/users/{test_user.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email
    
    def test_get_current_user(self, authenticated_client, test_user):
        """Test para obtener el usuario actual autenticado"""
        # Act
        response = authenticated_client.get("/api/v1/users/me/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email
    
    # def test_update_user(self, authenticated_client, test_user):
    #     """Test para actualizar un usuario"""
    #     # Arrange
    #     update_data = {
    #         "email": f"updated_{test_user.email}"
    #     }
        
    #     # Act
    #     response = authenticated_client.put(f"/api/v1/users/{test_user.id}", json=update_data)
        
    #     # Assert
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["email"] == update_data["email"]
    
    # def test_update_user_unauthorized(self, test_user):
    #     """Test para actualizar un usuario sin autenticación"""
    #     # Arrange
    #     update_data = {
    #         "email": "unauthorized@example.com"
    #     }
        
    #     # Act - Intentar actualizar sin token
    #     response = client.put(f"/api/v1/users/{test_user.id}", json=update_data)
        
    #     # Assert
    #     assert response.status_code == 401  # Unauthorized
    
    # def test_delete_user(self, admin_authenticated_client, test_user_to_delete):
    #     """
    #     Test para eliminar un usuario - requiere cliente con privilegios de admin
    #     """
    #     # Act
    #     response = admin_authenticated_client.delete(f"/api/v1/users/{test_user_to_delete.id}")
        
    #     # Assert
    #     assert response.status_code == 204  # No Content
        
    #     # Verificar que el usuario fue eliminado
    #     get_response = admin_authenticated_client.get(f"/api/v1/users/{test_user_to_delete.id}")
    #     assert get_response.status_code == 404  # Not Found