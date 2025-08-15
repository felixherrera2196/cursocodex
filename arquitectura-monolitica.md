# Arquitectura Monolítica para Sistema de Reserva de Vuelos

Este documento describe una arquitectura monolítica basada en **FastAPI** y **MongoDB** para un sistema de reservas de vuelos. El diseño considera los [casos de uso](casos-de-uso.md) y los [requerimientos funcionales](requerimientos-funcionales.md) y [no funcionales](requerimientos-no-funcionales.md).

## Componentes Principales
- **API HTTP**: Expuesta mediante FastAPI, entrega endpoints REST para búsqueda de vuelos, gestión de reservas, autenticación y administración.
- **Servicios de negocio**: Implementan la lógica para cada caso de uso (búsqueda, reserva, cancelación, pagos simulados y gestión de vuelos).
- **Capa de acceso a datos**: Repositorios que interactúan con MongoDB usando modelos Pydantic para validar y serializar información.
- **Módulo de autenticación**: Maneja registro, inicio de sesión y generación de JWT.
- **Módulo de pagos simulado**: Genera estados de aprobación o declinación para las reservas.

## Capas
1. **Presentación (Routers)**: Archivos `app/api` con rutas agrupadas por dominio (vuelos, reservas, usuarios).
2. **Servicio (Use Cases)**: Clases en `app/services` que encapsulan la lógica de negocio y las reglas como evitar sobreventa o verificar ventanas de cancelación.
3. **Persistencia (Repositorios)**: Clases en `app/repositories` que encapsulan operaciones CRUD sobre colecciones de MongoDB.
4. **Modelos**: Esquemas `app/models` basados en Pydantic que aplican formato ISO&nbsp;8601 para fechas y precios en MXN.

## Colecciones de MongoDB
- `usuarios`: credenciales, roles y metadatos.
- `vuelos`: origen, destino, fecha, hora, precio y capacidad.
- `reservas`: vínculos entre usuarios y vuelos, estado de pago y timestamps.
- `pagos`: registros del resultado del proceso de pago simulado.

## Flujo de Casos de Uso
1. **Búsqueda y visualización de vuelos**: el router de vuelos invoca al servicio de vuelos, que consulta la colección `vuelos`.
2. **Reserva y cancelación**: el router de reservas utiliza el servicio de reservas para verificar disponibilidad, crear o liberar asientos y registrar pagos.
3. **Autenticación y gestión de usuarios**: el router de usuarios interactúa con el servicio de usuarios para registro e inicio de sesión mediante JWT.
4. **Administración de vuelos**: usuarios con rol administrador acceden a endpoints protegidos para crear o editar vuelos.

Esta estructura monolítica permite desplegar el sistema como una única aplicación, facilitando el cumplimiento del plazo de entrega y reduciendo complejidad operativa.

