# Diagramas de Secuencia

Los siguientes diagramas describen el flujo de interacción entre los actores y el sistema para cada caso de uso.

## CU1. Búsqueda de vuelos
```mermaid
sequenceDiagram
    participant P as Pasajero
    participant S as Sistema
    participant DB as Base de Datos
    P->>S: Ingresa origen, destino y fecha
    S->>DB: Consulta vuelos disponibles
    DB-->>S: Devuelve coincidencias
    S-->>P: Muestra lista de vuelos
```

## CU2. Visualización de información de vuelo
```mermaid
sequenceDiagram
    participant P as Pasajero
    participant S as Sistema
    participant DB as Base de Datos
    P->>S: Selecciona vuelo
    S->>DB: Recupera detalles del vuelo
    DB-->>S: Detalles de código, fecha, precio, asientos
    S-->>P: Presenta información del vuelo
```

## CU3. Reserva de asientos
```mermaid
sequenceDiagram
    participant U as Usuario
    participant S as Sistema
    participant DB as Base de Datos
    U->>S: Solicita reservar asiento
    S->>DB: Verifica disponibilidad
    DB-->>S: Asiento disponible
    S->>DB: Registra reserva
    S-->>U: Confirma reserva
```

## CU4. Cancelación de reservas
```mermaid
sequenceDiagram
    participant U as Usuario
    participant S as Sistema
    participant DB as Base de Datos
    U->>S: Solicita cancelar reserva
    S->>DB: Verifica tiempo restante
    S->>DB: Libera asiento
    S-->>U: Confirma cancelación
```

## CU5. Proceso de pago simulado
```mermaid
sequenceDiagram
    participant U as Usuario
    participant S as Sistema
    participant Pago as Servicio de Pago
    U->>S: Inicia proceso de pago
    S->>Pago: Simula transacción
    Pago-->>S: Resultado del pago
    S-->>U: Notifica estado de pago
```

## CU6. Gestión de vuelos por administradores
```mermaid
sequenceDiagram
    participant A as Administrador
    participant S as Sistema
    participant DB as Base de Datos
    A->>S: Crea o edita vuelo
    S->>DB: Guarda cambios
    DB-->>S: Confirmación
    S-->>A: Notifica actualización
```

## CU7. Registro e inicio de sesión
```mermaid
sequenceDiagram
    participant U as Usuario
    participant S as Sistema
    participant DB as Base de Datos
    U->>S: Envía credenciales
    S->>DB: Valida datos
    DB-->>S: Resultado de validación
    S-->>U: Retorna token JWT
```

## CU8. Gestión de reservas
```mermaid
sequenceDiagram
    participant U as Usuario
    participant S as Sistema
    participant DB as Base de Datos
    U->>S: Solicita ver reservas
    S->>DB: Recupera reservas del usuario
    DB-->>S: Lista de reservas
    S-->>U: Muestra reservas
```
