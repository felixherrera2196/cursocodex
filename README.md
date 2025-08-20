# cursocodex

Repositorio del curso Codex. Incluye documentación de análisis, diagramas de arquitectura y una aplicación de ejemplo construida con FastAPI.

## Estructura del repositorio

- `fastapi-app/`: código de la API y pruebas automatizadas.
- Documentos Markdown: casos de uso, requisitos, diagramas y plan de sprints.

## Documentos de análisis y diagramas

- [Casos de uso](casos-de-uso.md)
- [Requerimientos funcionales](requerimientos-funcionales.md)
- [Requerimientos no funcionales](requerimientos-no-funcionales.md)
- [Diagramas de flujo](diagramas-flujo.md)
- [Diagramas de secuencia](diagramas-secuencia.md)
- [Diagrama de componentes](diagrama-componentes.md)
- [Arquitectura monolítica](arquitectura-monolitica.md)
- [Plan de sprints](plan-de-sprints.md)
- [Diagrama base de datos](diagrama-base-de-datos.md)

## Requisitos

Requiere Python 3.11+ y las dependencias listadas en `fastapi-app/requirements.txt`:

```bash
pip install -r fastapi-app/requirements.txt
```

## Ejecutar la aplicación

Para iniciar el servidor de desarrollo:

```bash
cd fastapi-app
uvicorn app.main:app --reload
```

La API estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000) y la documentación interactiva (Swagger) en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Ejecutar pruebas

```bash
python -m pytest
```

## Contribuir

Las contribuciones son bienvenidas. Para proponer cambios:

1. Crea un fork del repositorio y una rama para tu aporte.
2. Ejecuta las pruebas con `python -m pytest` y asegúrate de que todas pasen.
3. Abre un Pull Request describiendo tu cambio.

