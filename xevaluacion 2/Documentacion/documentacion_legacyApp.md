# Legacy App Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Database Schema](#database-schema)
4. [API Documentation](#api-documentation)
5. [User Interface](#user-interface)
6. [Installation Guide](#installation-guide)
7. [Maintenance](#maintenance)

## Overview

### Project Description
Legacy application for obstetric care management system.

### Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: Node.js/PHP
- Database: MySQL/PostgreSQL
- Server: Apache/Nginx

## System Architecture

```mermaid
graph TB
    A[Client Browser] --> B[Web Server]
    B --> C[Application Layer]
    C --> D[Database Layer]
    
    subgraph "Frontend"
        A
    end
    
    subgraph "Backend"
        B
        C
    end
    
    subgraph "Data"
        D
    end
```

### Component Diagram

```mermaid
classDiagram
    class User {
        +login()
        +logout()
        +viewProfile()
    }
    
    class Patient {
        +id: string
        +name: string
        +age: number
        +medicalHistory: string
        +addRecord()
        +updateInfo()
    }
    
    class Doctor {
        +id: string
        +name: string
        +specialty: string
        +assignPatient()
        +writeReport()
    }
    
    User <|-- Patient
    User <|-- Doctor
```

## Database Schema

### Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ PATIENTS : manages
    PATIENTS ||--o{ APPOINTMENTS : has
    DOCTORS ||--o{ APPOINTMENTS : schedules
    PATIENTS ||--o{ MEDICAL_RECORDS : owns
    
    USERS {
        int id PK
        string username
        string password_hash
        string role
        datetime created_at
    }
    
    PATIENTS {
        int id PK
        string name
        date birth_date
        string address
        string phone
        int user_id FK
    }
    
    DOCTORS {
        int id PK
        string name
        string specialty
        string license_number
        int user_id FK
    }
    
    APPOINTMENTS {
        int id PK
        int patient_id FK
        int doctor_id FK
        datetime appointment_date
        string status
    }
    
    MEDICAL_RECORDS {
        int id PK
        int patient_id FK
        text diagnosis
        text treatment
        datetime created_at
    }
```

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User authentication |
| POST | `/api/auth/logout` | User logout |
| GET | `/api/auth/profile` | Get user profile |

### Patient Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients` | List all patients |
| POST | `/api/patients` | Create new patient |
| GET | `/api/patients/{id}` | Get patient details |
| PUT | `/api/patients/{id}` | Update patient |
| DELETE | `/api/patients/{id}` | Delete patient |

### Appointment System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/appointments` | List appointments |
| POST | `/api/appointments` | Schedule appointment |
| PUT | `/api/appointments/{id}` | Update appointment |
| DELETE | `/api/appointments/{id}` | Cancel appointment |

## User Interface

### Application Flow

```mermaid
flowchart TD
    A[Login Page] --> B{Authentication}
    B -->|Success| C[Dashboard]
    B -->|Failure| A
    
    C --> D[Patient Management]
    C --> E[Appointment Scheduling]
    C --> F[Medical Records]
    
    D --> G[Add Patient]
    D --> H[View Patients]
    D --> I[Edit Patient]
    
    E --> J[Schedule Appointment]
    E --> K[View Calendar]
    
    F --> L[Add Record]
    F --> M[View History]
```

### Screen Layouts

#### Dashboard Layout
```
┌─────────────────────────────────────┐
│ Header: Logo | Navigation | Profile │
├─────────────────────────────────────┤
│ Sidebar   │ Main Content Area       │
│ - Patients│ ┌─────────────────────┐ │
│ - Appts   │ │ Quick Actions       │ │
│ - Records │ │ - New Patient       │ │
│ - Reports │ │ - Schedule Appt     │ │
│           │ │ - View Records      │ │
│           │ └─────────────────────┘ │
│           │ Recent Activity         │
└─────────────────────────────────────┘
```

## Installation Guide

### Prerequisites
- Web server (Apache/Nginx)
- Database server (MySQL/PostgreSQL)
- PHP 7.4+ or Node.js 14+

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd legacyApp
   ```

2. **Database Setup**
   ```sql
   CREATE DATABASE obstetric_care;
   USE obstetric_care;
   SOURCE database/schema.sql;
   ```

3. **Configuration**
   ```bash
   cp config/config.example.php config/config.php
   # Edit database credentials
   ```

4. **Dependencies**
   ```bash
   composer install
   # or
   npm install
   ```

5. **Web Server Configuration**
   ```apache
   <VirtualHost *:80>
       ServerName legacyapp.local
       DocumentRoot /path/to/legacyApp/public
   </VirtualHost>
   ```

## Maintenance

### Backup Procedures
```bash
# Database backup
mysqldump -u user -p obstetric_care > backup_$(date +%Y%m%d).sql

# File backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/legacyApp
```

### Log Files
- Application logs: `/var/log/legacyapp/`
- Error logs: `/var/log/apache2/error.log`
- Access logs: `/var/log/apache2/access.log`

### Security Updates
- Regular security patches
- Password policy enforcement
- Session management
- Input validation
- SQL injection prevention

### Performance Monitoring
```mermaid
graph LR
    A[Monitor CPU] --> D[Performance Dashboard]
    B[Monitor Memory] --> D
    C[Monitor Database] --> D
    D --> E[Alerts & Reports]
```

## Troubleshooting

### Common Issues
1. **Database Connection Error**
   - Check credentials in config file
   - Verify database server status

2. **Session Timeout**
   - Adjust session timeout in configuration
   - Check server time settings

3. **File Upload Issues**
   - Verify file permissions
   - Check upload directory settings

### Support Contact
- Technical Support: support@hospital.com
- System Administrator: admin@hospital.com