# FastAPI Hexagonal Architecture Project

Este proyecto implementa una API REST con FastAPI siguiendo los principios de la arquitectura hexagonal (puertos y adaptadores) y el patrón de repositorio. Incluye autenticación JWT y conexión a PostgreSQL.

## Características

- ✅ Arquitectura hexagonal (puertos y adaptadores)
- ✅ Patrón de repositorio para acceso a datos
- ✅ Autenticación JWT
- ✅ PostgreSQL como base de datos
- ✅ Migraciones con Alembic
- ✅ Gestión de excepciones
- ✅ CORS

## Estructura del proyecto

```
app/
├── domain/              # Capa de dominio
│   ├── entities/        # Entidades de negocio
│   ├── repositories/    # Interfaces de repositorio
│   ├── services/        # Servicios de dominio
│   └── interfaces/      # Interfaces/puertos
├── infrastructure/      # Adaptadores secundarios
│   ├── datasources/     # Fuentes de datos
│   ├── repositories/    # Implementaciones concretas de repositorios
│   └── auth/            # Implementación de autenticación
├── application/         # Casos de uso
│   ├── usecases/        # Casos de uso específicos
│   └── interfaces/      # Interfaces de casos de uso
├── adapters/            # Adaptadores primarios
│   ├── api/             # API REST
│   │   ├── routes/      # Definición de rutas
│   │   └── middleware/  # Middlewares
│   └── controllers/     # Controladores (lógica de aplicación)
└── config/              # Configuración

tests/
├── conftest.py                  # Configuración y fixtures compartidos
├── unit/                        # Tests unitarios
│   ├── domain/                  # Tests para la capa de dominio
│   │   ├── test_entities.py     # Tests para entidades
│   │   └── test_services.py     # Tests para servicios de dominio
│   ├── application/             # Tests para casos de uso
│   │   └── test_usecases.py
│   └── infrastructure/          # Tests para adaptadores secundarios
│       ├── test_repositories.py
│       └── test_auth.py
├── integration/                 # Tests de integración
│   ├── test_repositories.py     # Tests para repos con DB real
│   ├── test_api_auth.py         # Tests para endpoints de autenticación
│   └── test_api_endpoints.py    # Tests para endpoints específicos
└── e2e/                         # Tests end-to-end
    └── test_api_flows.py        # Flujos completos de la API
```

## Requisitos

- Python 3.8+
- PostgreSQL

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL DEL REPOSITORIO]
cd [NOMBRE DEL DIRECTORIO]
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Crear archivo .env:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_hexagonal
JWT_SECRET_KEY=your_secret_key_here
```

5. Inicializar la base de datos:
```bash
python alembic_init.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

6. Test:
```bash
python -m pytest
python -m pytest --cov=app
```

## Ejecución

Para ejecutar la aplicación:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`
La documentación de la API estará disponible en `http://localhost:8000/docs`

## Endpoints

### Autenticación
- `POST /api/token` - Obtener token JWT

### Usuarios
- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/me/` - Obtener usuario actual
- `GET /api/v1/users/{user_id}` - Obtener usuario por ID

### Items