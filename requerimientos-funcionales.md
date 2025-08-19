# Requerimientos Funcionales

1. **Búsqueda de vuelos.** Los pasajeros pueden buscar vuelos por origen, destino y fecha exacta.
2. **Visualización de información de vuelo.** Cada vuelo muestra código, origen, destino, fecha y hora, precio en MXN, asientos totales y asientos reservados.
3. **Reserva de asientos.** Los usuarios pueden reservar un solo asiento por vuelo y el sistema debe impedir la sobreventa.
4. **Cancelación de reservas.** Las reservas pueden cancelarse hasta 24 horas antes de la salida y al hacerlo el asiento queda disponible nuevamente.
5. **Proceso de pago simulado.** Al reservar se simula el pago, devolviendo un estado de aprobado o declinado.
6. **Gestión de vuelos por administradores.** Los administradores pueden crear y editar vuelos manualmente mediante un endpoint dedicado.
7. **Registro e inicio de sesión.** El registro e inicio de sesión se realiza con email y contraseña utilizando JWT.
8. **Gestión de reservas.** Los usuarios pueden consultar las reservas asociadas a su cuenta.
