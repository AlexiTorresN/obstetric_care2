
# MatronaApp - Documentación Técnica

## Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Casos de Uso](#casos-de-uso)
4. [Diagrama de Clases](#diagrama-de-clases)
5. [Diagrama de Base de Datos](#diagrama-de-base-de-datos)
6. [API Endpoints](#api-endpoints)
7. [Configuración e Instalación](#configuración-e-instalación)

## Descripción General

MatronaApp es una aplicación diseñada para la gestión de cuidados obstétricos, permitiendo a las matronas llevar un registro digital de pacientes, citas, y seguimiento prenatal.

### Características Principales
- Gestión de pacientes embarazadas
- Registro de citas y consultas
- Seguimiento prenatal
- Historial médico
- Reportes y estadísticas

## Arquitectura del Sistema

```mermaid
graph TB
    A[Frontend - React/Vue] --> B[API Gateway]
    B --> C[Backend - Node.js/Python]
    C --> D[Base de Datos - PostgreSQL]
    C --> E[Almacenamiento - AWS S3]
    F[Autenticación - JWT] --> C
```

### Tecnologías Utilizadas
- **Frontend**: React.js / Vue.js
- **Backend**: Node.js / Python Flask
- **Base de Datos**: PostgreSQL
- **Autenticación**: JWT
- **Almacenamiento**: AWS S3

## Casos de Uso

```mermaid
graph LR
    A[Matrona] --> B[Registrar Paciente]
    A --> C[Agendar Cita]
    A --> D[Realizar Consulta]
    A --> E[Ver Historial]
    A --> F[Generar Reportes]
    
    G[Paciente] --> H[Ver Citas]
    G --> I[Ver Historial Propio]
    G --> J[Actualizar Datos]
```

## Diagrama de Clases

```mermaid
classDiagram
    class Usuario {
        +int id
        +string email
        +string password
        +string rol
        +login()
        +logout()
    }
    
    class Matrona {
        +int id
        +string nombre
        +string apellido
        +string cedula_profesional
        +crearPaciente()
        +agendarCita()
    }
    
    class Paciente {
        +int id
        +string nombre
        +string apellido
        +date fecha_nacimiento
        +string rut
        +date fecha_ultima_regla
        +verHistorial()
    }
    
    class Cita {
        +int id
        +datetime fecha_hora
        +string motivo
        +string observaciones
        +boolean realizada
    }
    
    class Consulta {
        +int id
        +date fecha
        +int semanas_gestacion
        +float peso
        +string presion_arterial
        +string observaciones
    }
    
    Usuario ||--|| Matrona
    Usuario ||--|| Paciente
    Matrona ||--o{ Paciente
    Paciente ||--o{ Cita
    Cita ||--|| Consulta
```

## Diagrama de Base de Datos

```mermaid
erDiagram
    USUARIOS {
        int id PK
        string email
        string password_hash
        string rol
        datetime created_at
        datetime updated_at
    }
    
    MATRONAS {
        int id PK
        int usuario_id FK
        string nombre
        string apellido
        string cedula_profesional
        string telefono
    }
    
    PACIENTES {
        int id PK
        int usuario_id FK
        int matrona_id FK
        string nombre
        string apellido
        string rut
        date fecha_nacimiento
        date fecha_ultima_regla
        string grupo_sanguineo
        string telefono
        string direccion
    }
    
    CITAS {
        int id PK
        int paciente_id FK
        int matrona_id FK
        datetime fecha_hora
        string motivo
        string estado
        datetime created_at
    }
    
    CONSULTAS {
        int id PK
        int cita_id FK
        int paciente_id FK
        date fecha
        int semanas_gestacion
        float peso
        string presion_arterial
        int frecuencia_cardiaca_fetal
        text observaciones
        text recomendaciones
    }
    
    USUARIOS ||--|| MATRONAS : "1:1"
    USUARIOS ||--|| PACIENTES : "1:1"
    MATRONAS ||--o{ PACIENTES : "1:N"
    PACIENTES ||--o{ CITAS : "1:N"
    MATRONAS ||--o{ CITAS : "1:N"
    CITAS ||--|| CONSULTAS : "1:1"
```

## API Endpoints

### Autenticación
```
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
```

### Pacientes
```
GET    /api/pacientes          # Listar pacientes
POST   /api/pacientes          # Crear paciente
GET    /api/pacientes/:id      # Obtener paciente
PUT    /api/pacientes/:id      # Actualizar paciente
DELETE /api/pacientes/:id      # Eliminar paciente
```

### Citas
```
GET    /api/citas              # Listar citas
POST   /api/citas              # Crear cita
GET    /api/citas/:id          # Obtener cita
PUT    /api/citas/:id          # Actualizar cita
DELETE /api/citas/:id          # Cancelar cita
```

### Consultas
```
GET    /api/consultas          # Listar consultas
POST   /api/consultas          # Crear consulta
GET    /api/consultas/:id      # Obtener consulta
PUT    /api/consultas/:id      # Actualizar consulta
```

## Configuración e Instalación

### Prerrequisitos
- Node.js 16+
- PostgreSQL 12+
- npm o yarn

### Instalación Backend
```bash
# Clonar repositorio
git clone https://github.com/your-repo/matrona-app.git
cd matrona-app/backend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp .env.example .env

# Ejecutar migraciones
npm run migrate

# Iniciar servidor
npm start
```

### Instalación Frontend
```bash
cd ../frontend

# Instalar dependencias
npm install

# Iniciar aplicación
npm start
```

### Variables de Entorno
```env
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/matrona_app
JWT_SECRET=your-secret-key
PORT=3001

# Frontend
REACT_APP_API_URL=http://localhost:3001/api
```

## Seguridad

- Autenticación JWT
- Encriptación de contraseñas con bcrypt
- Validación de datos de entrada
- Control de acceso basado en roles
- HTTPS en producción

## Testing

```bash
# Ejecutar tests unitarios
npm test

# Ejecutar tests de integración
npm run test:integration

# Coverage
npm run test:coverage
```
