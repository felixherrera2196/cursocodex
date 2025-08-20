# Diagrama de Base de Datos

```mermaid
erDiagram
    USUARIOS {
        int id_usuario PK
        string nombre
        string email
    }
    VUELOS {
        int id_vuelo PK
        string numero
        string origen
        string destino
        date fecha
    }
    RESERVAS {
        int id_reserva PK
        int usuario_id FK
        int vuelo_id FK
        date fecha_reserva
    }
    PAGOS {
        int id_pago PK
        int reserva_id FK
        float monto
        date fecha_pago
    }

    USUARIOS ||--o{ RESERVAS : "realiza"
    VUELOS ||--o{ RESERVAS : "incluye"
    RESERVAS ||--|| PAGOS : "se liquida"
```

## Descripción de entidades

- **usuarios**: almacena la información de los clientes registrados.
- **vuelos**: contiene los detalles de los vuelos disponibles.
- **reservas**: vincula usuarios con vuelos y registra la fecha de reserva.
- **pagos**: guarda los registros de pago para cada reserva.

