### Plan de Sprints

**Duración y alcance**  
Se propone un plan de cuatro sprints de dos semanas cada uno para cumplir con el plazo de 6–8 semanas definido para el MVP. La arquitectura monolítica basada en FastAPI y MongoDB guía la distribución de tareas y capas (routers, servicios, repositorios y modelos).

---

#### Sprint 1 (Semanas 1–2) – Fundamentos y autenticación
- Preparar la aplicación FastAPI, conexión a MongoDB y estructura de capas (routers, servicios, repositorios)  
- Implementar el módulo de autenticación con registro e inicio de sesión mediante JWT

#### Sprint 2 (Semanas 3–4) – Vuelos
- Endpoints para búsqueda de vuelos (CU1) y visualización de información de vuelo (CU2)  
- Modelos y repositorios de vuelos con fechas en formato ISO 8601 y precios en MXN

#### Sprint 3 (Semanas 5–6) – Reservas
- Lógica de reserva de asientos evitando sobreventa (CU3)  
- Proceso de pago simulado y registro de estado de pago (CU5)  
- Consulta de reservas del usuario (CU8)

#### Sprint 4 (Semanas 7–8) – Cancelaciones y administración
- Cancelación de reservas con validación de tiempo (CU4)  
- Gestión de vuelos para administradores (CU6)  
- Ajustes finales: interfaz en español, buenas prácticas de accesibilidad y verificación de requisitos no funcionales
