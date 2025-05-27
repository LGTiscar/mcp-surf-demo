# Tests

Esta carpeta contiene todas las pruebas para el proyecto MCP Surf Demo.

## Archivos de Test

- `test.py` - Suite completa de pruebas que incluye:
  - Test de conexión MCP
  - Test de funcionalidad básica
  - Modo interactivo para pruebas manuales

- `simple_test.py` - Test simple de integración que verifica:
  - Conexión básica con el servidor MCP
  - Chat simple con Gemini

## Cómo Ejecutar las Pruebas

### Desde el directorio raíz del proyecto:

```bash
# Ejecutar la suite completa de pruebas
python tests/test.py

# Ejecutar el test simple
python tests/simple_test.py
```

### Requisitos

Asegúrate de que:
1. Tu archivo `.env` esté configurado correctamente
2. Tengas las dependencias instaladas (`uv sync`)
3. Tengas acceso a internet para conectar con los servicios

## Tipos de Test

- **Test de Conexión**: Verifica que puedas conectarte al servidor MCP de Browserbase
- **Test de Funcionalidad**: Prueba las operaciones básicas de navegación web
- **Test de Integración**: Verifica que Gemini y MCP funcionen juntos

## Notas

- Los tests requieren claves API válidas para funcionar completamente
- Algunos tests pueden hacer llamadas reales a las APIs (ten cuidado con los límites de cuota)
- Los tests están diseñados para ser seguros y no consumir excesivos recursos
