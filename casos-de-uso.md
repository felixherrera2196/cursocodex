# Casos de Uso

A continuación se describen los principales casos de uso del sistema, derivados de los requerimientos funcionales.

## CU1. Búsqueda de vuelos
**Actor principal:** Pasajero

**Precondiciones:** El pasajero conoce el origen, destino y fecha del viaje.

**Flujo principal:**
1. El pasajero ingresa al sistema.
2. El pasajero introduce origen, destino y fecha exacta.
3. El sistema muestra la lista de vuelos disponibles que cumplen con los criterios.

**Postcondiciones:** Se muestran los vuelos que coinciden con la búsqueda.

## CU2. Visualización de información de vuelo
**Actor principal:** Pasajero

**Precondiciones:** El pasajero ha realizado una búsqueda de vuelos.

**Flujo principal:**
1. El pasajero selecciona un vuelo de la lista de resultados.
2. El sistema presenta código, origen, destino, fecha, hora, precio en MXN, asientos totales y asientos reservados.

**Postcondiciones:** El pasajero visualiza la información detallada del vuelo.

## CU3. Reserva de asientos
**Actor principal:** Usuario registrado

**Precondiciones:** El usuario ha iniciado sesión y ha seleccionado un vuelo con asientos disponibles.

**Flujo principal:**
1. El usuario solicita reservar un asiento en el vuelo seleccionado.
2. El sistema verifica la disponibilidad de asientos.
3. El sistema reserva un asiento para el usuario y evita la sobreventa.

**Postcondiciones:** El asiento queda reservado para el usuario.

## CU4. Cancelación de reservas
**Actor principal:** Usuario registrado

**Precondiciones:** El usuario posee una reserva confirmada y falta más de 24 horas para la salida del vuelo.

**Flujo principal:**
1. El usuario solicita cancelar la reserva.
2. El sistema verifica el tiempo restante antes del vuelo.
3. El sistema cancela la reserva y libera el asiento.

**Postcondiciones:** El asiento vuelve a estar disponible para otros usuarios.

## CU5. Proceso de pago simulado
**Actor principal:** Usuario registrado

**Precondiciones:** El usuario ha seleccionado un vuelo y está listo para confirmar la reserva.

**Flujo principal:**
1. El usuario inicia el proceso de pago.
2. El sistema simula la transacción y determina si es aprobada o declinada.
3. El sistema notifica al usuario el resultado del pago.

**Postcondiciones:** Se genera el estado de pago correspondiente a la reserva.

## CU6. Gestión de vuelos por administradores
**Actor principal:** Administrador

**Precondiciones:** El administrador ha iniciado sesión con credenciales válidas.

**Flujo principal:**
1. El administrador accede al módulo de gestión de vuelos.
2. El administrador registra un nuevo vuelo proporcionando código, origen, destino, horarios, precio y capacidad mediante el endpoint `/flights`.
3. El sistema almacena los cambios realizados.

**Postcondiciones:** El vuelo queda disponible para búsquedas y reservas.

## CU7. Registro e inicio de sesión
**Actor principal:** Usuario

**Precondiciones:** El usuario no cuenta con sesión activa.

**Flujo principal:**
1. El usuario proporciona email y contraseña para registrarse o iniciar sesión.
2. El sistema valida las credenciales y genera un token JWT si son correctas.

**Postcondiciones:** El usuario queda autenticado y puede acceder a funciones restringidas.

## CU8. Gestión de reservas
**Actor principal:** Usuario registrado

**Precondiciones:** El usuario posee una o más reservas en el sistema.

**Flujo principal:**
1. El usuario solicita ver sus reservas.
2. El sistema recupera y muestra las reservas asociadas a su cuenta.

**Postcondiciones:** El usuario visualiza la lista de sus reservas.
