# Diagrama de Componentes

```mermaid
graph TD
    U[Usuario] -->|HTTP| A[FastAPI App]
    A --> B[Router de Vuelos]
    A --> C[Router de Reservas]
    A --> D[Router de Usuarios]
    B --> E[Servicio de Vuelos]
    C --> F[Servicio de Reservas]
    D --> G[Servicio de Autenticación]
    E --> H[(MongoDB: vuelos)]
    F --> I[(MongoDB: reservas)]
    G --> J[(MongoDB: usuarios)]
    F --> K[(MongoDB: pagos)]
```

## Explicación de Componentes
- **FastAPI App**: núcleo monolítico que agrupa todos los módulos y expone la API.
- **Routers**: separan los endpoints por dominio (vuelos, reservas, usuarios) y delegan al servicio correspondiente.
- **Servicios**: aplican las reglas de negocio y coordinan operaciones entre repositorios.
- **MongoDB**: base de datos documental con colecciones para usuarios, vuelos, reservas y pagos.

Este diagrama muestra cómo las solicitudes del usuario recorren la aplicación monolítica hasta persistir o recuperar datos de MongoDB.
