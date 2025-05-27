# Arquitectura del Proyecto MCP Surf Demo

## 🎯 Objetivo
Transformar el proyecto actual a una arquitectura hexagonal (Clean Architecture) para mejorar la escalabilidad, mantenibilidad y testabilidad.

## 📐 Arquitectura Propuesta

### Estructura de Directorios
```
mcp-surf-demo/
├── src/
│   ├── domain/                    # Capa de Dominio (Core Business Logic)
│   │   ├── __init__.py
│   │   ├── entities/              # Entidades de negocio
│   │   │   ├── __init__.py
│   │   │   ├── chat_session.py
│   │   │   ├── browser_action.py
│   │   │   └── web_content.py
│   │   ├── use_cases/             # Casos de uso
│   │   │   ├── __init__.py
│   │   │   ├── chat_with_ai.py
│   │   │   ├── browse_website.py
│   │   │   └── analyze_content.py
│   │   └── ports/                 # Interfaces/Contratos
│   │       ├── __init__.py
│   │       ├── ai_provider.py
│   │       ├── web_browser.py
│   │       └── config_provider.py
│   │
│   ├── infrastructure/            # Capa de Infraestructura (Adaptadores)
│   │   ├── __init__.py
│   │   ├── adapters/
│   │   │   ├── __init__.py
│   │   │   ├── gemini_adapter.py
│   │   │   ├── browserbase_adapter.py
│   │   │   └── env_config_adapter.py
│   │   ├── mcp/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── tool_manager.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       └── session_repository.py
│   │
│   ├── application/               # Capa de Aplicación (Coordinación)
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── chat_service.py
│   │   │   └── browser_service.py
│   │   └── dto/
│   │       ├── __init__.py
│   │       ├── chat_request.py
│   │       └── browser_response.py
│   │
│   └── presentation/              # Capa de Presentación (UI/CLI)
│       ├── __init__.py
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── interactive_cli.py
│       │   └── commands/
│       │       ├── __init__.py
│       │       ├── chat_command.py
│       │       └── config_command.py
│       └── api/                   # Para futuras APIs REST/GraphQL
│           ├── __init__.py
│           └── routes/
│
├── tests/                         # Tests organizados por capas
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/
│   └── e2e/
│
├── config/                        # Configuraciones
│   ├── __init__.py
│   ├── settings.py
│   └── dependency_injection.py
│
├── scripts/                       # Scripts de utilidad
│   ├── setup.py
│   └── migration.py
│
├── main.py                        # Punto de entrada principal
├── pyproject.toml
└── README.md
```

## 🔄 Flujo de Datos

```
CLI/API → Application Service → Use Case → Domain Logic
                                    ↓
Infrastructure Adapters ← Ports ← Domain Entities
```

## 🎯 Beneficios de esta Arquitectura

### 1. **Separación de Responsabilidades**
- **Domain**: Lógica de negocio pura
- **Application**: Coordinación y orquestación
- **Infrastructure**: Detalles técnicos (APIs, DB, etc.)
- **Presentation**: Interface de usuario

### 2. **Inversión de Dependencias**
- El dominio no depende de infraestructura
- Las dependencias apuntan hacia adentro
- Fácil testing con mocks

### 3. **Escalabilidad**
- Fácil agregar nuevos adaptadores
- Cambiar proveedores sin afectar el core
- Múltiples interfaces (CLI, Web, API)

### 4. **Testabilidad**
- Tests unitarios del dominio aislados
- Tests de integración por capas
- Mocking sencillo de dependencias

## 🔧 Componentes Principales

### Domain Layer
- **Entities**: `ChatSession`, `BrowserAction`, `WebContent`
- **Use Cases**: `ChatWithAI`, `BrowseWebsite`, `AnalyzeContent`
- **Ports**: Interfaces para servicios externos

### Infrastructure Layer
- **Adapters**: Implementaciones concretas de los ports
- **MCP Client**: Manejo de conexiones MCP
- **Repositories**: Persistencia de sesiones

### Application Layer
- **Services**: Coordinación entre use cases
- **DTOs**: Objetos de transferencia de datos

### Presentation Layer
- **CLI**: Interface de línea de comandos
- **API**: Endpoints REST (futuro)

## 🚀 Plan de Migración

1. **Fase 1**: Crear estructura de directorios
2. **Fase 2**: Extraer entidades del dominio
3. **Fase 3**: Crear use cases
4. **Fase 4**: Implementar adaptadores
5. **Fase 5**: Refactorizar presentación
6. **Fase 6**: Migrar tests
7. **Fase 7**: Dependency injection

## 📋 Próximos Pasos

1. Crear la estructura de directorios
2. Extraer la lógica de negocio actual
3. Implementar los ports y adapters
4. Refactorizar el código existente
5. Mejorar los tests
