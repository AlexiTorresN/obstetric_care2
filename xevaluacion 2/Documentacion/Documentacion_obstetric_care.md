
# Documentación del Sistema Obstétrico (Obstetric Care)

## Índice
1. [Introducción](#introducción)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Diagrama de Base de Datos](#diagrama-de-base-de-datos)
4. [Casos de Uso](#casos-de-uso)
5. [Diagrama de Flujo](#diagrama-de-flujo)
6. [API Endpoints](#api-endpoints)
7. [Instalación y Configuración](#instalación-y-configuración)

## Introducción

El sistema Obstetric Care es una aplicación diseñada para la gestión integral de cuidados obstétricos, permitiendo el seguimiento de pacientes embarazadas, control de citas médicas, y monitoreo del desarrollo prenatal.

## Arquitectura del Sistema

```mermaid
graph TB
    A[Frontend - React/Vue] --> B[API Gateway]
    B --> C[Auth Service]
    B --> D[Patient Service]
    B --> E[Appointment Service]
    B --> F[Medical Records Service]
    
    C --> G[(Auth Database)]
    D --> H[(Patient Database)]
    E --> I[(Appointment Database)]
    F --> J[(Medical Records Database)]
```

## Diagrama de Base de Datos

```mermaid
erDiagram
    PATIENT {
        int patient_id PK
        string first_name
        string last_name
        date birth_date
        string phone
        string email
        date created_at
    }
    
    PREGNANCY {
        int pregnancy_id PK
        int patient_id FK
        date last_menstrual_period
        date estimated_due_date
        int gestational_weeks
        string status
    }
    
    APPOINTMENT {
        int appointment_id PK
        int patient_id FK
        int doctor_id FK
        datetime appointment_date
        string type
        string status
        text notes
    }
    
    MEDICAL_RECORD {
        int record_id PK
        int patient_id FK
        int pregnancy_id FK
        date record_date
        float weight
        int blood_pressure_sys
        int blood_pressure_dia
        text observations
    }
    
    DOCTOR {
        int doctor_id PK
        string first_name
        string last_name
        string specialization
        string license_number
    }
    
    PATIENT ||--o{ PREGNANCY : has
    PATIENT ||--o{ APPOINTMENT : schedules
    PATIENT ||--o{ MEDICAL_RECORD : has
    DOCTOR ||--o{ APPOINTMENT : attends
    PREGNANCY ||--o{ MEDICAL_RECORD : contains
```

## Casos de Uso

```mermaid
graph LR
    A[Paciente] --> B[Agendar Cita]
    A --> C[Ver Historial Médico]
    A --> D[Actualizar Información Personal]
    
    E[Doctor] --> F[Ver Citas del Día]
    E --> G[Registrar Consulta]
    E --> H[Revisar Historial Paciente]
    E --> I[Generar Reportes]
    
    J[Administrador] --> K[Gestionar Usuarios]
    J --> L[Configurar Sistema]
    J --> M[Ver Estadísticas]
```

## Diagrama de Flujo - Proceso de Consulta Prenatal

```mermaid
flowchart TD
    A[Inicio] --> B[Paciente llega a consulta]
    B --> C[Verificar cita agendada]
    C --> D{¿Cita válida?}
    D -->|No| E[Reagendar cita]
    D -->|Sí| F[Registrar llegada]
    F --> G[Tomar signos vitales]
    G --> H[Consulta médica]
    H --> I[Registrar observaciones]
    I --> J[¿Requiere exámenes?]
    J -->|Sí| K[Solicitar exámenes]
    J -->|No| L[Programar próxima cita]
    K --> L
    L --> M[Fin]
    E --> M
```

## API Endpoints

### Pacientes
```
GET    /api/patients          - Obtener lista de pacientes
POST   /api/patients          - Crear nuevo paciente
GET    /api/patients/:id      - Obtener paciente específico
PUT    /api/patients/:id      - Actualizar paciente
DELETE /api/patients/:id      - Eliminar paciente
```

### Citas
```
GET    /api/appointments      - Obtener citas
POST   /api/appointments      - Crear nueva cita
PUT    /api/appointments/:id  - Actualizar cita
DELETE /api/appointments/:id  - Cancelar cita
```

### Registros Médicos
```
GET    /api/medical-records/:patientId  - Historial del paciente
POST   /api/medical-records             - Crear nuevo registro
PUT    /api/medical-records/:id         - Actualizar registro
```

## Instalación y Configuración

### Requisitos del Sistema
- Node.js >= 14.0.0
- PostgreSQL >= 12.0
- Docker (opcional)

### Instalación
```bash
# Clonar repositorio
git clone [repository-url]
cd obstetric-care

# Instalar dependencias
npm install

# Configurar base de datos
cp .env.example .env
# Editar variables de entorno

# Ejecutar migraciones
npm run migrate

# Iniciar servidor
npm start
```

### Variables de Entorno
```env
DATABASE_URL=postgresql://user:password@localhost:5432/obstetric_care
JWT_SECRET=your_jwt_secret
PORT=3000
NODE_ENV=development
```

### Estructura del Proyecto
```
obstetric-care/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   └── utils/
├── tests/
├── docs/
├── migrations/
└── package.json
```
