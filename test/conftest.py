import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.config.settings import get_settings
from app.domain.entities import Base  # Importa Base desde donde esté definida la entidad User
from app.config.database import get_db

# Configuración para una base de datos SQLite en memoria para testing
@pytest.fixture(scope="session")
def test_settings():
    # Sobreescribir configuración para tests
    settings = get_settings()
    settings.DATABASE_URL = "sqlite:///:memory:"
    return settings

@pytest.fixture(scope="session")
def test_engine(test_settings):
    # Crear conexión a base de datos de prueba
    engine = create_engine(
        test_settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Crear todas las tablas en la BD de prueba
    Base.metadata.create_all(bind=engine)
    yield engine
    # Limpiar después de todos los tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db(test_engine):
    # Crear una sesión de BD independiente para cada test
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="function")
def client(test_db):
    # Crear un cliente de prueba que usa la BD de test
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Restaurar la dependencia original
    app.dependency_overrides.clear()
    
@pytest.fixture
def authenticated_client(client, auth_headers):
    """Cliente con cabeceras de autenticación"""
    client.headers.update(auth_headers)
    return client

@pytest.fixture
def db_session(test_db):
    """Alias para test_db para que coincida con el nombre usado en las pruebas"""
    return test_db

# Fixture para crear usuario de prueba
@pytest.fixture
def test_user(test_db):
    from app.domain.entities import User
    from app.infrastructure.auth.jwt import get_password_hash
    
    # Crear usuario de prueba
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

# Fixture para token de autenticación
@pytest.fixture
def auth_headers(test_user, client):
    from app.infrastructure.auth.jwt import create_access_token
    
    access_token = create_access_token(
        data={"sub": test_user.email}
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers