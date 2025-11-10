# PROYECTO: SISTEMA DE GESTIÓN OBSTÉTRICA
## Unidad 2: Diseño y Planificación de la Solución Informática

**Asignatura:** Análisis y Diseño de Sistemas  
**Proyecto:** Sistema de Trazabilidad Obstétrica - Hospital Clínico Herminda Martín  
**Fecha:** Noviembre 2025

---

## 📋 ÍNDICE

1. [Actividad 1: Metodología y Cronograma](#actividad-1)
2. [Actividad 2: Arquitectura 4+1](#actividad-2)
3. [Actividad 3: Diseño de Interfaces](#actividad-3)
4. [Actividad 4: Modelo de Base de Datos](#actividad-4)
5. [Actividad 5: Programación Segura](#actividad-5)
6. [Actividad 6: Plan de Pruebas](#actividad-6)

---

<a name="actividad-1"></a>
## 📊 ACTIVIDAD 1: METODOLOGÍA Y CRONOGRAMA

### 1.1 Metodología de Desarrollo Seleccionada

**Metodología:** **Desarrollo Ágil con Scrum**

#### Justificación:

1. **Complejidad del Dominio:** El sistema de gestión obstétrica es complejo y requiere iteraciones frecuentes con usuarios médicos para validar funcionalidades críticas.

2. **Requisitos Cambiantes:** El entorno hospitalario presenta requisitos que pueden evolucionar según necesidades clínicas y regulaciones.

3. **Entrega Incremental:** Se necesita implementar módulos funcionales de forma gradual (gestión de pacientes → fichas obstétricas → partos → recién nacidos).

4. **Colaboración Multidisciplinaria:** El proyecto involucra desarrolladores, matronas, médicos y personal administrativo.

5. **Feedback Rápido:** Cada sprint permite validar funcionalidades con usuarios reales antes de avanzar.

### 1.2 Cronograma del Proyecto

#### Product Backlog Priorizado

| ID | Historia de Usuario | Prioridad | Story Points | Criterios de Aceptación |
|----|---------------------|-----------|--------------|-------------------------|
| US-01 | Como matrona, necesito registrar pacientes con su información personal completa | Alta | 8 | - Validación RUT chileno<br>- Campos obligatorios completos<br>- Manejo de errores |
| US-02 | Como matrona, necesito crear fichas obstétricas con antecedentes del embarazo | Alta | 13 | - Cálculo automático FPP<br>- Validación gestas/partos<br>- Historial completo |
| US-03 | Como matrona, necesito registrar el ingreso al parto con datos de admisión | Alta | 13 | - Tamizajes obligatorios<br>- Tipo de paciente<br>- Generación número ficha |
| US-04 | Como personal médico, necesito registrar el proceso completo del parto | Alta | 21 | - Registro paso a paso<br>- Validación tiempos<br>- Clasificación Robson |
| US-05 | Como matrona, necesito registrar datos del recién nacido y APGAR | Alta | 13 | - Cálculo APGAR<br>- Ligadura cordón<br>- Apego inmediato |
| US-06 | Como médico, necesito gestionar un catálogo de patologías CIE-10 | Media | 8 | - CRUD patologías<br>- Códigos CIE-10<br>- Nivel de riesgo |
| US-07 | Como matrona, necesito asignar patologías a pacientes | Media | 5 | - Búsqueda patologías<br>- Múltiples patologías<br>- Fecha diagnóstico |
| US-08 | Como matrona, necesito prescribir medicamentos en fichas | Media | 8 | - Dosis y frecuencia<br>- Fecha inicio/fin<br>- Observaciones |
| US-09 | Como TENS, necesito registrar administración de medicamentos | Media | 5 | - Control lavado manos<br>- Reacciones adversas<br>- Registro horario |
| US-10 | Como TENS, necesito registrar signos vitales de pacientes | Media | 5 | - Temperatura, FC, PA<br>- Validación rangos<br>- Historial |
| US-11 | Como usuario, necesito consultar historial clínico completo | Baja | 8 | - Búsqueda por RUT<br>- Vista cronológica<br>- Todas las fichas |
| US-12 | Como administrador, necesito ver estadísticas de partos | Baja | 13 | - Gráficos interactivos<br>- Filtros por fecha<br>- Exportar datos |

#### Sprints Planificados (2 semanas c/u)

**SPRINT 1: Gestión Base de Usuarios y Pacientes**
- **Objetivo:** Establecer la base del sistema con gestión de personas y pacientes
- **Duración:** 2 semanas
- **Historias:** US-01
- **Story Points:** 8
- **Entregables:**
  - Modelo Persona completo
  - Modelo Paciente funcional
  - Formularios de registro validados
  - Vista de listado de pacientes

**SPRINT 2: Fichas Obstétricas**
- **Objetivo:** Implementar el módulo de fichas obstétricas
- **Duración:** 2 semanas
- **Historias:** US-02
- **Story Points:** 13
- **Entregables:**
  - CRUD completo de fichas
  - Cálculo automático de FPP
  - Validaciones médicas
  - Vista detallada de ficha

**SPRINT 3: Ingreso y Registro de Partos**
- **Objetivo:** Módulo completo de ingreso y registro de partos
- **Duración:** 2 semanas
- **Historias:** US-03, US-04
- **Story Points:** 34
- **Entregables:**
  - Ficha de ingreso al parto
  - Registro de parto por pasos
  - Clasificación de Robson
  - Validaciones de proceso

**SPRINT 4: Recién Nacidos y Documentos**
- **Objetivo:** Registro de recién nacidos y documentación
- **Duración:** 2 semanas
- **Historias:** US-05
- **Story Points:** 13
- **Entregables:**
  - Registro de RN
  - Cálculo APGAR
  - Gestión de documentos
  - Certificados de nacimiento

**SPRINT 5: Módulo Médico y Patologías**
- **Objetivo:** Sistema de gestión de patologías
- **Duración:** 2 semanas
- **Historias:** US-06, US-07
- **Story Points:** 13
- **Entregables:**
  - Catálogo patologías CIE-10
  - Asignación a pacientes
  - Seguimiento médico
  - Alertas de riesgo

**SPRINT 6: Medicamentos y TENS**
- **Objetivo:** Gestión de medicamentos y control TENS
- **Duración:** 2 semanas
- **Historias:** US-08, US-09, US-10
- **Story Points:** 18
- **Entregables:**
  - Prescripción medicamentos
  - Administración por TENS
  - Signos vitales
  - Control de lavado

**SPRINT 7: Consultas e Informes**
- **Objetivo:** Módulo de consultas y reportería
- **Duración:** 2 semanas
- **Historias:** US-11, US-12
- **Story Points:** 21
- **Entregables:**
  - Historial clínico
  - Dashboard estadístico
  - Reportes PDF
  - Exportación datos

#### Tablero Kanban

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────┐
│   BACKLOG       │   TO DO          │   IN PROGRESS    │      DONE        │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ US-11           │ US-03            │ US-02            │ US-01            │
│ US-12           │ US-04            │                  │                  │
│                 │ US-05            │                  │                  │
│                 │                  │                  │                  │
└─────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

### 1.3 Estimación de Recursos

| Recurso | Cantidad | Rol | Dedicación |
|---------|----------|-----|------------|
| Desarrollador Full Stack | 2 | Backend/Frontend | 100% |
| Desarrollador Frontend | 1 | Interfaces | 50% |
| Product Owner | 1 | Matrona Jefe | 20% |
| Scrum Master | 1 | Líder Técnico | 30% |
| Usuarios Clave | 3 | Matronas/Médicos | 10% |

### 1.4 Hitos Principales

| Hito | Fecha Estimada | Entregable |
|------|----------------|------------|
| MVP Core | Semana 4 | Módulo pacientes + fichas |
| Módulo Partos | Semana 8 | Sistema partos completo |
| Módulo Médico | Semana 12 | Patologías y medicamentos |
| Pre-Producción | Semana 14 | Testing y ajustes |
| Go Live | Semana 16 | Despliegue producción |

---

<a name="actividad-2"></a>
## 🏗️ ACTIVIDAD 2: ARQUITECTURA 4+1

### 2.1 Vista Lógica - Diagrama de Clases

```mermaid
classDiagram
    %% =========================================
    %% CAPA DE GESTIÓN BASE
    %% =========================================
    class Persona {
        +String Rut
        +String Nombre
        +String Apellido_Paterno
        +String Apellido_Materno
        +Date Fecha_Nacimiento
        +String Sexo
        +String Direccion
        +String Telefono
        +String Email
        +calcularEdad() int
    }
    
    class Paciente {
        +String GrupoSanguineo
        +Float Peso
        +Float Talla
        +Float IMC
        +String Prevision
        +Boolean Activa
        +calcularIMC() float
    }
    
    class Matrona {
        +String Especialidad
        +String Registro_medico
        +Int Años_experiencia
        +String Turno
        +Boolean Activo
    }
    
    class Medico {
        +String Especialidad
        +String Registro_medico
        +Int Años_experiencia
        +String Turno
        +Boolean Activo
    }
    
    class TENS {
        +String Registro_tens
        +String Turno
        +Boolean Activo
    }
    
    %% =========================================
    %% MÓDULO OBSTÉTRICO
    %% =========================================
    class FichaObstetrica {
        +String numero_ficha
        +Int numero_gestas
        +Int numero_partos
        +Int partos_vaginales
        +Int partos_cesareas
        +Int numero_abortos
        +Date fecha_ultima_regla
        +Date fecha_probable_parto
        +Boolean activa
        +calcularFPP() Date
        +calcularEdadGestacional() int
    }
    
    class IngresoPaciente {
        +String numero_ingreso
        +DateTime fecha_hora_ingreso
        +String motivo_ingreso
        +String sintomas
        +Boolean activo
    }
    
    class FichaParto {
        +String numero_ficha_parto
        +String tipo_paciente
        +String origen_ingreso
        +Date fecha_ingreso
        +Time hora_ingreso
        +Boolean plan_de_parto
        +Boolean vih_tomado
        +String sgb_resultado
        +Boolean activa
    }
    
    class RegistroParto {
        +String numero_registro
        +DateTime fecha_hora_admision
        +DateTime fecha_hora_parto
        +Int edad_gestacional_semanas
        +String tipo_parto
        +String clasificacion_robson
        +String posicion_materna_parto
        +Boolean activo
        +calcularDuracionParto() int
    }
    
    class RegistroRecienNacido {
        +String sexo
        +Int peso
        +Int talla
        +Int apgar_1_minuto
        +Int apgar_5_minutos
        +DateTime fecha_nacimiento
        +Boolean ligadura_tardia_cordon
        +Boolean apego_canguro
        +calcularAPGAR() string
    }
    
    %% =========================================
    %% MÓDULO MÉDICO
    %% =========================================
    class Patologias {
        +String nombre
        +String codigo_cie_10
        +String descripcion
        +String nivel_de_riesgo
        +String protocolo_seguimiento
        +String estado
    }
    
    class PatologiaPaciente {
        +Date fecha_diagnostico
        +String observaciones
        +Boolean activa
    }
    
    %% =========================================
    %% MÓDULO MEDICAMENTOS
    %% =========================================
    class MedicamentoFicha {
        +String nombre_medicamento
        +String dosis
        +String frecuencia
        +String via_administracion
        +Date fecha_inicio
        +Date fecha_fin
        +String indicaciones
        +Boolean activo
    }
    
    class AdministracionMedicamento {
        +DateTime fecha_hora_administracion
        +Boolean se_realizo_lavado
        +String observaciones
        +String reacciones_adversas
        +Boolean administrado_exitosamente
    }
    
    class RegistroTENS {
        +Date fecha
        +String turno
        +Decimal temperatura
        +Int frecuencia_cardiaca
        +Int presion_arterial_sistolica
        +Int presion_arterial_diastolica
        +String observaciones
    }
    
    %% =========================================
    %% RELACIONES
    %% =========================================
    Persona <|-- Paciente
    Persona <|-- Matrona
    Persona <|-- Medico
    Persona <|-- TENS
    
    Paciente "1" --> "*" FichaObstetrica : tiene
    Matrona "1" --> "*" FichaObstetrica : responsable
    
    FichaObstetrica "1" --> "*" IngresoPaciente : registra
    FichaObstetrica "1" --> "*" FichaParto : genera
    FichaParto "1" --> "1" RegistroParto : produce
    RegistroParto "1" --> "*" RegistroRecienNacido : registra
    
    Paciente "*" --> "*" Patologias : padece
    PatologiaPaciente "1" --> "1" Paciente
    PatologiaPaciente "1" --> "1" Patologias
    Medico "1" --> "*" PatologiaPaciente : diagnostica
    
    FichaObstetrica "1" --> "*" MedicamentoFicha : prescribe
    Matrona "1" --> "*" MedicamentoFicha : prescribe
    MedicamentoFicha "1" --> "*" AdministracionMedicamento : genera
    TENS "1" --> "*" AdministracionMedicamento : administra
    
    FichaObstetrica "1" --> "*" RegistroTENS : monitorea
    TENS "1" --> "*" RegistroTENS : registra
```

### 2.2 Vista de Desarrollo - Diagrama de Componentes

```mermaid
graph TB
    subgraph "Capa de Presentación"
        WEB[Web Browser]
        TEMPLATES[Django Templates]
        STATIC[Static Files CSS/JS/Bootstrap]
    end
    
    subgraph "Capa de Aplicación - Apps Django"
        INICIO[inicioApp<br/>Dashboard]
        GESTION[gestionApp<br/>Personas/Pacientes]
        MATRONA[matronaApp<br/>Fichas Obstétricas]
        MEDICO[medicoApp<br/>Patologías]
        TENS[tensApp<br/>Signos Vitales]
        PARTO[partosApp<br/>Registro Partos]
        INGRESO[ingresoPartoApp<br/>Ficha Ingreso]
        RN[recienNacidoApp<br/>Recién Nacidos]
    end
    
    subgraph "Capa de Negocio"
        MODELS[Models ORM]
        FORMS[Forms Validation]
        VIEWS[Views/Controllers]
        URLS[URL Routing]
    end
    
    subgraph "Capa de Datos"
        DJANGO_ORM[Django ORM]
        DB_MAIN[(MySQL<br/>obstetric_carebdd)]
        DB_LEGACY[(MySQL<br/>legacy_obstetric)]
    end
    
    subgraph "Servicios Externos"
        API_REST[REST Framework API]
        ADMIN[Django Admin]
    end
    
    WEB --> TEMPLATES
    WEB --> STATIC
    TEMPLATES --> VIEWS
    
    INICIO --> VIEWS
    GESTION --> VIEWS
    MATRONA --> VIEWS
    MEDICO --> VIEWS
    TENS --> VIEWS
    PARTO --> VIEWS
    INGRESO --> VIEWS
    RN --> VIEWS
    
    VIEWS --> URLS
    VIEWS --> FORMS
    VIEWS --> MODELS
    
    MODELS --> DJANGO_ORM
    DJANGO_ORM --> DB_MAIN
    DJANGO_ORM --> DB_LEGACY
    
    VIEWS --> API_REST
    MODELS --> ADMIN
```

### 2.3 Vista de Procesos - Diagrama BPMN

**Proceso: Registro Completo de Parto**

```mermaid
graph LR
    START([Inicio]) --> CHECK_PACIENTE{¿Paciente<br/>registrada?}
    
    CHECK_PACIENTE -->|No| REG_PERSONA[Registrar<br/>Persona]
    CHECK_PACIENTE -->|Sí| CHECK_FICHA
    
    REG_PERSONA --> REG_PACIENTE[Registrar<br/>Paciente]
    REG_PACIENTE --> CREATE_FICHA[Crear Ficha<br/>Obstétrica]
    
    CREATE_FICHA --> CHECK_FICHA{¿Tiene Ficha<br/>Activa?}
    CHECK_FICHA -->|No| ERROR1[Error:<br/>Sin Ficha]
    CHECK_FICHA -->|Sí| CREATE_INGRESO
    
    CREATE_INGRESO[Crear Ficha<br/>de Ingreso] --> TAMIZAJES[Realizar<br/>Tamizajes]
    TAMIZAJES --> REG_PARTO
    
    REG_PARTO[Iniciar Registro<br/>de Parto] --> TRABAJO_PARTO[Registrar Trabajo<br/>de Parto]
    TRABAJO_PARTO --> PARTO_DETALLE[Registrar Parto<br/>y Alumbramiento]
    
    PARTO_DETALLE --> CHECK_GEMELOS{¿Parto<br/>Gemelar?}
    CHECK_GEMELOS -->|No| REG_RN[Registrar<br/>Recién Nacido]
    CHECK_GEMELOS -->|Sí| REG_GEMELOS[Registrar<br/>Gemelos]
    
    REG_RN --> APGAR[Calcular<br/>APGAR]
    REG_GEMELOS --> APGAR
    
    APGAR --> DOCUMENTOS[Generar<br/>Documentos]
    DOCUMENTOS --> NOTIFICAR[Notificar<br/>Áreas]
    
    NOTIFICAR --> END([Fin])
    ERROR1 --> END
```

### 2.4 Vista de Casos de Uso del Sistema

```mermaid
graph TB
    subgraph "Sistema de Gestión Obstétrica"
        subgraph "Módulo Gestión"
            UC1[Gestionar Pacientes]
            UC2[Gestionar Personal]
        end
        
        subgraph "Módulo Obstétrico"
            UC3[Gestionar Fichas<br/>Obstétricas]
            UC4[Registrar Ingresos]
            UC5[Registrar Partos]
            UC6[Registrar RN]
        end
        
        subgraph "Módulo Clínico"
            UC7[Gestionar Patologías]
            UC8[Prescribir<br/>Medicamentos]
            UC9[Administrar<br/>Medicamentos]
            UC10[Registrar Signos<br/>Vitales]
        end
        
        subgraph "Módulo Reportes"
            UC11[Consultar Historial]
            UC12[Generar Estadísticas]
        end
    end
    
    ADMIN[Administrador] --> UC2
    
    MATRONA[Matrona] --> UC1
    MATRONA --> UC3
    MATRONA --> UC4
    MATRONA --> UC5
    MATRONA --> UC6
    MATRONA --> UC8
    
    MEDICO[Médico] --> UC7
    MEDICO --> UC11
    
    TENS[TENS] --> UC9
    TENS --> UC10
    
    ADMIN --> UC12
```

### 2.5 Diagrama de Secuencia Genérico

**Secuencia: Registro de Parto**

```mermaid
sequenceDiagram
    participant M as Matrona
    participant V as Vista Django
    participant C as Controller
    participant DB as Base de Datos
    
    M->>V: Accede a "Registrar Parto"
    V->>C: GET /partos/seleccionar-ficha/
    C->>DB: Buscar fichas activas
    DB-->>C: Lista de fichas
    C-->>V: Render selección
    V-->>M: Muestra fichas disponibles
    
    M->>V: Selecciona ficha + datos parto
    V->>C: POST /partos/registrar/paso1/
    C->>C: Validar formulario
    
    alt Formulario válido
        C->>DB: Crear RegistroParto
        DB-->>C: Parto guardado (ID)
        C->>C: Guardar ID en sesión
        C-->>V: Redirect paso 2
        V-->>M: Formulario trabajo de parto
        
        M->>V: Completa datos trabajo parto
        V->>C: POST /partos/registrar/paso2/
        C->>DB: Actualizar RegistroParto
        DB-->>C: OK
        C-->>V: Redirect paso 3
        V-->>M: Formulario recién nacido
        
        M->>V: Completa datos RN
        V->>C: POST /partos/rn/registrar/
        C->>DB: Crear RegistroRecienNacido
        C->>C: Calcular APGAR
        DB-->>C: RN guardado
        C-->>V: Redirect resumen
        V-->>M: Muestra resumen completo
    else Formulario inválido
        C-->>V: Render con errores
        V-->>M: Muestra errores validación
    end
```

### 2.6 Diagrama de Actividad Genérico

```mermaid
flowchart TD
    START([Inicio: Ficha Obstétrica]) --> INPUT1[Ingresar datos<br/>paciente]
    INPUT1 --> VALID1{¿Datos<br/>válidos?}
    
    VALID1 -->|No| ERROR1[Mostrar errores]
    ERROR1 --> INPUT1
    
    VALID1 -->|Sí| CALC[Calcular FPP<br/>y edad gestacional]
    CALC --> SAVE1[Guardar ficha]
    
    SAVE1 --> ASSIGN[Asignar matrona<br/>responsable]
    ASSIGN --> PATOL{¿Agregar<br/>patologías?}
    
    PATOL -->|Sí| SELECT_PAT[Seleccionar<br/>patologías]
    SELECT_PAT --> SAVE_PAT[Guardar patologías]
    SAVE_PAT --> MEDIC
    
    PATOL -->|No| MEDIC{¿Prescribir<br/>medicamentos?}
    
    MEDIC -->|Sí| SELECT_MED[Prescribir<br/>medicamentos]
    SELECT_MED --> SAVE_MED[Guardar<br/>prescripciones]
    SAVE_MED --> NOTIF
    
    MEDIC -->|No| NOTIF[Notificar áreas<br/>correspondientes]
    NOTIF --> END([Fin])
```

### 2.7 Diagrama de Despliegue

```mermaid
graph TB
    subgraph "Cliente"
        BROWSER[Navegador Web<br/>Chrome/Firefox]
    end
    
    subgraph "Servidor Web - Ubuntu Server"
        NGINX[Nginx<br/>Servidor Web/Proxy]
        GUNICORN[Gunicorn<br/>WSGI Server]
        
        subgraph "Django Application"
            APP[Django 5.2.7<br/>Python 3.11]
            STATIC_SERVE[Archivos Estáticos<br/>Bootstrap 5]
        end
    end
    
    subgraph "Servidor Base de Datos"
        MYSQL[MySQL 8.0<br/>obstetric_carebdd]
        MYSQL_LEGACY[MySQL 8.0<br/>legacy_obstetric]
    end
    
    subgraph "Servicios Externos"
        BACKUP[Backup Automático<br/>Diario]
        MONITOR[Monitoreo<br/>Sistema]
    end
    
    BROWSER -->|HTTPS:443| NGINX
    NGINX -->|Proxy Pass| GUNICORN
    GUNICORN <-->|WSGI| APP
    NGINX -->|Sirve| STATIC_SERVE
    
    APP -->|ORM| MYSQL
    APP -->|Read Only| MYSQL_LEGACY
    
    MYSQL -->|Backup| BACKUP
    APP -->|Logs| MONITOR
```

---

<a name="actividad-3"></a>
## 🎨 ACTIVIDAD 3: DISEÑO DE INTERFACES

### 3.1 Perfiles de Usuario

| Perfil | Descripción | Funcionalidades Clave | Nivel Técnico |
|--------|-------------|----------------------|---------------|
| **Matrona** | Personal responsable de atención obstétrica | - Crear fichas obstétricas<br>- Registrar partos<br>- Prescribir medicamentos<br>- Ver historial | Medio |
| **Médico** | Especialista en ginecobstetricia | - Gestionar patologías<br>- Revisar historiales<br>- Aprobar tratamientos | Medio |
| **TENS** | Técnico paramédico | - Administrar medicamentos<br>- Registrar signos vitales<br>- Control básico | Bajo |
| **Administrador** | Gestión del sistema | - Administrar usuarios<br>- Ver estadísticas<br>- Configuración | Alto |

### 3.2 Lista Priorizada de Funcionalidades

1. **Críticas (Must Have):**
   - Registro de pacientes
   - Creación de fichas obstétricas
   - Registro de partos
   - Registro de recién nacidos
   - Cálculo APGAR automático

2. **Importantes (Should Have):**
   - Gestión de patologías
   - Prescripción de medicamentos
   - Administración de medicamentos
   - Registro de signos vitales

3. **Deseables (Nice to Have):**
   - Dashboard estadístico
   - Gráficos interactivos
   - Exportación a PDF
   - Búsqueda avanzada

### 3.3 Arquitectura de Información

```
Sistema de Gestión Obstétrica
│
├── 🏠 Dashboard Principal
│   ├── Resumen del día
│   ├── Alertas/Notificaciones
│   └── Accesos rápidos
│
├── 👥 Gestión de Pacientes
│   ├── Listar pacientes
│   ├── Registrar nuevo paciente
│   ├── Buscar paciente
│   └── Ver detalle paciente
│
├── 📋 Fichas Obstétricas
│   ├── Listar fichas activas
│   ├── Crear nueva ficha
│   ├── Ver detalle ficha
│   │   ├── Antecedentes obstétricos
│   │   ├── Controles previos
│   │   ├── Patologías asignadas
│   │   └── Medicamentos prescritos
│   └── Editar ficha
│
├── 🏥 Partos
│   ├── Seleccionar ficha
│   ├── Registro de parto (multi-paso)
│   │   ├── Paso 1: Datos básicos
│   │   ├── Paso 2: Trabajo de parto
│   │   ├── Paso 3: Parto y alumbramiento
│   │   ├── Paso 4: Recién nacido
│   │   ├── Paso 5: Procedimientos
│   │   └── Paso 6: Anestesia
│   └── Ver historial de partos
│
├── 🩺 Módulo Médico
│   ├── Catálogo de patologías CIE-10
│   │   ├── Listar patologías
│   │   ├── Crear patología
│   │   └── Editar patología
│   ├── Asignar patologías a paciente
│   └── Consultar historial clínico
│
├── 💊 Medicamentos (Matrona)
│   ├── Prescribir medicamento
│   ├── Ver medicamentos activos
│   └── Editar prescripción
│
├── 💉 Módulo TENS
│   ├── Administrar medicamentos
│   ├── Registrar signos vitales
│   └── Ver historial de administración
│
└── 📊 Reportes y Estadísticas
    ├── Dashboard estadístico
    ├── Gráficos de partos
    ├── Reportes por período
    └── Exportar datos
```

### 3.4 Mapa de Navegación

```mermaid
graph TD
    HOME[🏠 Dashboard]
    
    HOME --> PACIENTES[👥 Pacientes]
    HOME --> FICHAS[📋 Fichas]
    HOME --> PARTOS[🏥 Partos]
    HOME --> MEDICO[🩺 Médico]
    HOME --> TENS[💉 TENS]
    HOME --> REPORTES[📊 Reportes]
    
    PACIENTES --> PAC_LIST[Listar]
    PACIENTES --> PAC_NEW[Registrar]
    PACIENTES --> PAC_SEARCH[Buscar]
    PAC_LIST --> PAC_DETAIL[Detalle]
    PAC_DETAIL --> PAC_EDIT[Editar]
    
    FICHAS --> FICHA_LIST[Listar Activas]
    FICHAS --> FICHA_NEW[Nueva Ficha]
    FICHA_LIST --> FICHA_DETAIL[Detalle]
    FICHA_DETAIL --> FICHA_EDIT[Editar]
    FICHA_DETAIL --> FICHA_PATOL[Patologías]
    FICHA_DETAIL --> FICHA_MED[Medicamentos]
    
    PARTOS --> PARTO_SELECT[Seleccionar Ficha]
    PARTO_SELECT --> PARTO_REG[Registrar Parto]
    PARTO_REG --> PARTO_P1[Paso 1]
    PARTO_P1 --> PARTO_P2[Paso 2]
    PARTO_P2 --> PARTO_P3[Paso 3]
    PARTO_P3 --> PARTO_RN[Recién Nacido]
    PARTO_RN --> PARTO_SUMMARY[Resumen]
    
    MEDICO --> MED_PATOL[Patologías CIE-10]
    MEDICO --> MED_HIST[Historial Clínico]
    MED_PATOL --> MED_PAT_NEW[Nueva]
    MED_PATOL --> MED_PAT_EDIT[Editar]
    
    TENS --> TENS_ADMIN[Administrar Med.]
    TENS --> TENS_SIGNOS[Signos Vitales]
    
    REPORTES --> REP_DASH[Dashboard]
    REPORTES --> REP_PARTOS[Estadísticas Partos]
```

### 3.5 Prototipos de Interfaces

#### Prototipo 1: Dashboard Principal

```
┌─────────────────────────────────────────────────────────────────────┐
│  🏥 Sistema Obstétrico - Hospital Herminda Martín                   │
├─────────────────────────────────────────────────────────────────────┤
│  [Dashboard] [Pacientes] [Fichas] [Partos] [Médico] [👤 Usuario ▼] │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐  ┌─────────────────┐
│  📊 Partos Hoy       │  │  👥 Pacientes Activos│  │  🔔 Alertas (3) │
│                      │  │                      │  │                 │
│       12             │  │        45            │  │  • Parto en     │
│   +3 vs ayer        │  │   +2 esta semana    │  │    proceso      │
└──────────────────────┘  └──────────────────────┘  │  • Medicamento  │
                                                     │    vencido      │
┌──────────────────────┐  ┌──────────────────────┐  │  • Control     │
│  🏥 Ingresos Semana  │  │  📋 Fichas Pendientes│  │    atrasado    │
│                      │  │                      │  └─────────────────┘
│  [■■■■■■■░░░] 70%   │  │         8            │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  📈 Gráfico de Partos - Últimos 30 días                              │
│                                                                       │
│   15│     █                                                          │
│   10│   █ █ █   █                                                    │
│    5│ █ █ █ █ █ █ █                                                  │
│    0└──────────────────────────────────────────────────────────────  │
│      1  5  10  15  20  25  30                                        │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🎯 Accesos Rápidos                                                  │
│                                                                      │
│  [+ Registrar Paciente]  [+ Nueva Ficha]  [🏥 Registrar Parto]     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Prototipo 2: Registro de Ficha Obstétrica

```
┌─────────────────────────────────────────────────────────────────────┐
│  📋 Nueva Ficha Obstétrica                                          │
└─────────────────────────────────────────────────────────────────────┘

  Paso 1 de 3: Información Básica
  [████████████░░░░░░░░] 60%

┌─────────────────────────────────────────────────────────────────────┐
│  👤 Datos de la Paciente                                            │
│                                                                      │
│  Paciente: [Buscar por RUT ⌕]  [María González Pérez ✓]           │
│  RUT: 18.234.567-8                                                  │
│  Edad: 28 años                                                      │
│  Previsión: FONASA                                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🤰 Antecedentes Obstétricos                                        │
│                                                                      │
│  Número de Gestas:    [2]                                           │
│  Número de Partos:    [1]                                           │
│    - Vaginales:       [1]                                           │
│    - Cesáreas:        [0]                                           │
│  Número de Abortos:   [0]                                           │
│  Nacidos Vivos:       [1]                                           │
│                                                                      │
│  📅 Fecha Última Regla (FUR):  [12/03/2025]  [📅]                  │
│  📅 Fecha Probable Parto (FPP): 17/12/2025 (calculado)             │
│                                                                      │
│  Edad Gestacional Actual: 32 semanas, 4 días                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  👩‍⚕️ Matrona Responsable                                            │
│                                                                      │
│  [Seleccionar Matrona ▼]  → Ana Martínez - Turno Mañana           │
└─────────────────────────────────────────────────────────────────────┘

  [⬅ Cancelar]                              [Siguiente: Patologías ➡]
```

#### Prototipo 3: Registro de Parto (Multi-paso)

```
┌─────────────────────────────────────────────────────────────────────┐
│  🏥 Registro de Parto - Paso 2: Trabajo de Parto                   │
└─────────────────────────────────────────────────────────────────────┘

  [✓ Datos Básicos] → [● Trabajo Parto] → [ Alumbramiento ] → [ RN ]
  
┌─────────────────────────────────────────────────────────────────────┐
│  📋 Ficha: FO-000245 - María González (32 años)                    │
│  Ingreso: 08/11/2025 14:30                                          │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  ⏱️ Tiempos del Trabajo de Parto                                    │
│                                                                      │
│  Duración Dilatación:        [4] horas [30] minutos                │
│  Duración Expulsivo:         [0] horas [25] minutos                │
│  Tiempo Membranas Rotas:     [2] horas [15] minutos                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  🩺 Procedimientos                                                   │
│                                                                      │
│  Monitorización TTC:         [✓] Sí  [ ] No                        │
│  Inducción:                  [ ] Sí  [✓] No                        │
│  Aceleración/Corrección:     [✓] Sí  [ ] No                        │
│  Número Tactos Vaginales:    [5]                                    │
│                                                                      │
│  Rotura Membranas:           (•) Espontánea  ( ) Artificial        │
│  Régimen:                    ( ) Líquido  (•) Sólido  ( ) Nada     │
│  Libertad Movimiento:        [✓] Sí  [ ] No                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  💊 Manejo del Dolor                                                 │
│                                                                      │
│  Anestesia Neuroaxial:       [✓] Sí  [ ] No                        │
│    Tiempo de espera:         [15] minutos                           │
│  Óxido Nitroso:              [ ] Sí  [✓] No                        │
│  Analgesia Endovenosa:       [ ] Sí  [✓] No                        │
│  Técnicas No Farmacológicas: [✓] Sí  [ ] No                        │
│    [✓] Balón Kinésico  [ ] Lenteja  [✓] Rebozo  [ ] Aromaterapia  │
└─────────────────────────────────────────────────────────────────────┘

  [⬅ Anterior]         [💾 Guardar Borrador]        [Siguiente ➡]
```

### 3.6 Consideraciones UX/UI

#### Principios de Diseño:

1. **Claridad Visual:**
   - Uso de Bootstrap 5 para consistencia
   - Jerarquía tipográfica clara
   - Espaciado generoso entre elementos

2. **Accesibilidad:**
   - Contraste WCAG AA mínimo
   - Etiquetas descriptivas en formularios
   - Navegación por teclado

3. **Feedback Inmediato:**
   - Validación en tiempo real
   - Mensajes de éxito/error claros
   - Indicadores de progreso

4. **Eficiencia:**
   - Atajos de teclado para acciones comunes
   - Autocompletado en búsquedas
   - Valores por defecto inteligentes

5. **Prevención de Errores:**
   - Confirmación en acciones críticas
   - Validación de datos obligatorios
   - Advertencias contextuales

#### Paleta de Colores:

```
Primarios:
- Azul Hospital:    #0d6efd (Acciones principales)
- Verde Éxito:      #198754 (Confirmaciones)
- Rojo Alerta:      #dc3545 (Advertencias)
- Amarillo Info:    #ffc107 (Información)

Neutros:
- Gris Oscuro:      #212529 (Textos)
- Gris Medio:       #6c757d (Textos secundarios)
- Gris Claro:       #f8f9fa (Fondos)
- Blanco:           #ffffff (Fondos principales)
```

---

<a name="actividad-4"></a>
## 🗄️ ACTIVIDAD 4: MODELO DE BASE DE DATOS

### 4.1 Tipo de Modelo Seleccionado

**Modelo:** Base de Datos Relacional (SQL) - MySQL 8.0

#### Justificación:

1. **Integridad de Datos:** Los datos médicos requieren relaciones estrictas y validaciones ACID
2. **Normalización:** Evita redundancia en información crítica (pacientes, fichas, partos)
3. **Consultas Complejas:** Necesidad de JOINs para historiales clínicos completos
4. **Transacciones:** Garantiza consistencia en operaciones como registro de partos
5. **Madurez:** MySQL es ampliamente usado en entornos hospitalarios

### 4.2 Diagrama Entidad-Relación

```mermaid
erDiagram
    PERSONA ||--o{ PACIENTE : "es"
    PERSONA ||--o{ MATRONA : "es"
    PERSONA ||--o{ MEDICO : "es"
    PERSONA ||--o{ TENS : "es"
    
    PACIENTE ||--o{ FICHA_OBSTETRICA : "tiene"
    MATRONA ||--o{ FICHA_OBSTETRICA : "responsable de"
    
    FICHA_OBSTETRICA ||--o{ INGRESO_PACIENTE : "genera"
    FICHA_OBSTETRICA ||--o{ FICHA_PARTO : "produce"
    FICHA_PARTO ||--|| REGISTRO_PARTO : "registra"
    
    REGISTRO_PARTO ||--o{ REGISTRO_RECIEN_NACIDO : "produce"
    REGISTRO_RECIEN_NACIDO ||--o{ DOCUMENTOS_PARTO : "genera"
    
    PACIENTE }o--o{ PATOLOGIAS : "padece"
    PATOLOGIA_PACIENTE }o--|| PACIENTE : "afecta"
    PATOLOGIA_PACIENTE }o--|| PATOLOGIAS : "describe"
    MEDICO ||--o{ PATOLOGIA_PACIENTE : "diagnostica"
    
    FICHA_OBSTETRICA ||--o{ MEDICAMENTO_FICHA : "prescribe"
    MATRONA ||--o{ MEDICAMENTO_FICHA : "prescribe"
    MEDICAMENTO_FICHA ||--o{ ADMINISTRACION_MEDICAMENTO : "produce"
    TENS ||--o{ ADMINISTRACION_MEDICAMENTO : "administra"
    
    FICHA_OBSTETRICA ||--o{ REGISTRO_TENS : "monitorea"
    TENS ||--o{ REGISTRO_TENS : "registra"
    
    PERSONA {
        bigint id PK
        varchar rut UK
        varchar nombre
        varchar apellido_paterno
        varchar apellido_materno
        date fecha_nacimiento
        varchar sexo
        varchar direccion
        varchar telefono
        varchar email
    }
    
    PACIENTE {
        bigint persona_id PK,FK
        varchar grupo_sanguineo
        decimal peso
        decimal talla
        decimal imc
        varchar prevision
        boolean activa
    }
    
    MATRONA {
        bigint id PK
        bigint persona_id FK
        varchar especialidad
        varchar registro_medico UK
        int años_experiencia
        varchar turno
        boolean activo
    }
    
    MEDICO {
        bigint id PK
        bigint persona_id FK
        varchar especialidad
        varchar registro_medico UK
        int años_experiencia
        varchar turno
        boolean activo
    }
    
    TENS {
        bigint id PK
        bigint persona_id FK
        varchar registro_tens UK
        varchar turno
        boolean activo
    }
    
    FICHA_OBSTETRICA {
        bigint id PK
        bigint paciente_id FK
        bigint matrona_responsable_id FK
        varchar numero_ficha UK
        int numero_gestas
        int numero_partos
        int partos_vaginales
        int partos_cesareas
        int numero_abortos
        date fecha_ultima_regla
        date fecha_probable_parto
        boolean activa
        datetime fecha_creacion
    }
    
    FICHA_PARTO {
        bigint id PK
        bigint ficha_obstetrica_id FK
        varchar numero_ficha_parto UK
        varchar tipo_paciente
        date fecha_ingreso
        time hora_ingreso
        boolean plan_de_parto
        boolean vih_tomado
        varchar sgb_resultado
        boolean activa
    }
    
    REGISTRO_PARTO {
        bigint id PK
        bigint ficha_id FK
        bigint ficha_ingreso_id FK
        varchar numero_registro UK
        datetime fecha_hora_admision
        datetime fecha_hora_parto
        int edad_gestacional_semanas
        varchar tipo_parto
        varchar clasificacion_robson
        varchar posicion_materna_parto
        boolean activo
    }
    
    REGISTRO_RECIEN_NACIDO {
        bigint id PK
        bigint registro_parto_id FK
        varchar sexo
        int peso
        int talla
        int apgar_1_minuto
        int apgar_5_minutos
        datetime fecha_nacimiento
        boolean ligadura_tardia_cordon
        boolean apego_canguro
    }
    
    PATOLOGIAS {
        bigint id PK
        varchar nombre
        varchar codigo_cie_10 UK
        text descripcion
        varchar nivel_de_riesgo
        text protocolo_seguimiento
        varchar estado
    }
    
    PATOLOGIA_PACIENTE {
        bigint id PK
        bigint paciente_id FK
        bigint patologia_id FK
        bigint medico_id FK
        date fecha_diagnostico
        text observaciones
        boolean activa
    }
    
    MEDICAMENTO_FICHA {
        bigint id PK
        bigint ficha_id FK
        bigint matrona_id FK
        varchar nombre_medicamento
        varchar dosis
        varchar frecuencia
        varchar via_administracion
        date fecha_inicio
        date fecha_fin
        boolean activo
    }
    
    ADMINISTRACION_MEDICAMENTO {
        bigint id PK
        bigint medicamento_ficha_id FK
        bigint tens_id FK
        datetime fecha_hora_administracion
        boolean se_realizo_lavado
        text observaciones
        boolean administrado_exitosamente
    }
    
    REGISTRO_TENS {
        bigint id PK
        bigint ficha_id FK
        bigint tens_id FK
        date fecha
        varchar turno
        decimal temperatura
        int frecuencia_cardiaca
        int presion_arterial_sistolica
        int presion_arterial_diastolica
    }
```

### 4.3 Diccionario de Datos (Tablas Principales)

#### Tabla: gestionapp_persona

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| id | BIGINT | NO | Identificador único (PK) |
| Rut | VARCHAR(12) | NO | RUT chileno (UK) |
| Nombre | VARCHAR(100) | NO | Nombre(s) |
| Apellido_Paterno | VARCHAR(100) | NO | Apellido paterno |
| Apellido_Materno | VARCHAR(100) | NO | Apellido materno |
| Fecha_Nacimiento | DATE | NO | Fecha nacimiento |
| Sexo | VARCHAR(10) | NO | M/F/Otro |
| Direccion | VARCHAR(300) | YES | Dirección completa |
| Telefono | VARCHAR(20) | YES | Teléfono contacto |
| Email | VARCHAR(100) | YES | Email |

#### Tabla: matronaapp_fichaobstetrica

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| id | BIGINT | NO | Identificador único (PK) |
| paciente_id | BIGINT | NO | FK a Paciente |
| matrona_responsable_id | BIGINT | NO | FK a Matrona |
| numero_ficha | VARCHAR(20) | NO | Número único ficha (UK) |
| numero_gestas | INT | NO | Total embarazos |
| numero_partos | INT | NO | Total partos previos |
| partos_vaginales | INT | NO | Partos vaginales |
| partos_cesareas | INT | NO | Cesáreas |
| numero_abortos | INT | NO | Abortos |
| fecha_ultima_regla | DATE | YES | FUR |
| fecha_probable_parto | DATE | YES | FPP (calculado) |
| activa | BOOLEAN | NO | Estado ficha |
| fecha_creacion | DATETIME | NO | Fecha creación |

#### Tabla: partosapp_registroparto

| Campo | Tipo | Nulo | Descripción |
|-------|------|------|-------------|
| id | BIGINT | NO | Identificador único (PK) |
| ficha_id | BIGINT | NO | FK a FichaObstetrica |
| ficha_ingreso_id | BIGINT | YES | FK a FichaParto |
| numero_registro | VARCHAR(20) | NO | Número registro (UK) |
| fecha_hora_admision | DATETIME | NO | Fecha/hora ingreso |
| fecha_hora_parto | DATETIME | YES | Fecha/hora parto |
| edad_gestacional_semanas | INT | NO | EG en semanas |
| tipo_parto | VARCHAR(20) | NO | Vaginal/Cesárea/Fórceps |
| clasificacion_robson | VARCHAR(30) | NO | Grupo Robson (1-10) |
| posicion_materna_parto | VARCHAR(20) | NO | Posición en parto |
| activo | BOOLEAN | NO | Estado registro |

### 4.4 Índices y Optimizaciones

```sql
-- Índices en gestionapp_persona
CREATE INDEX idx_persona_rut ON gestionapp_persona(Rut);
CREATE INDEX idx_persona_nombre ON gestionapp_persona(Nombre, Apellido_Paterno);

-- Índices en matronaapp_fichaobstetrica
CREATE INDEX idx_ficha_numero ON matronaapp_fichaobstetrica(numero_ficha);
CREATE INDEX idx_ficha_paciente_activa ON matronaapp_fichaobstetrica(paciente_id, activa);
CREATE INDEX idx_ficha_matrona ON matronaapp_fichaobstetrica(matrona_responsable_id);

-- Índices en partosapp_registroparto
CREATE INDEX idx_parto_ficha ON partosapp_registroparto(ficha_id);
CREATE INDEX idx_parto_fecha ON partosapp_registroparto(fecha_hora_parto DESC);
CREATE INDEX idx_parto_robson ON partosapp_registroparto(clasificacion_robson);

-- Índices en medicoapp_patologias
CREATE INDEX idx_patologia_cie10 ON medicoapp_patologias(codigo_cie_10);
CREATE INDEX idx_patologia_nombre ON medicoapp_patologias(nombre);
```

### 4.5 Relaciones y Cardinalidades

1. **Persona → Paciente** (1:1)
   - Una persona puede ser paciente
   - Una paciente es una persona

2. **Paciente → FichaObstetrica** (1:N)
   - Un paciente puede tener múltiples fichas (embarazos diferentes)
   - Una ficha pertenece a un paciente

3. **FichaObstetrica → RegistroParto** (1:N)
   - Una ficha puede generar múltiples ingresos (falsos trabajos de parto)
   - Pero solo un registro de parto exitoso por embarazo

4. **RegistroParto → RegistroRecienNacido** (1:N)
   - Un parto puede tener uno o más recién nacidos (gemelos, trillizos)
   - Un RN pertenece a un parto

5. **Paciente ↔ Patologias** (N:M)
   - Un paciente puede tener múltiples patologías
   - Una patología puede afectar a múltiples pacientes
   - Tabla intermedia: PatologiaPaciente

### 4.6 Reglas de Integridad

1. **Integridad Referencial:**
   - Todas las FK deben existir en tabla padre
   - ON DELETE PROTECT en relaciones críticas (paciente, ficha)
   - ON DELETE CASCADE en registros dependientes

2. **Validaciones:**
   - RUT único y formato válido
   - Fechas lógicas (FUR < FPP)
   - Valores positivos en mediciones (peso, talla)
   - Rangos válidos (APGAR 0-10)

3. **Restricciones:**
   - CHECK(numero_gestas >= numero_partos)
   - CHECK(apgar_1_minuto BETWEEN 0 AND 10)
   - CHECK(edad_gestacional_semanas BETWEEN 20 AND 45)

### 4.7 Estrategia de Backup

```sql
-- Backup diario automático (3am)
mysqldump -u root -p obstetric_carebdd > backup_$(date +%Y%m%d).sql

-- Backup incremental cada 6 horas
mysqlbinlog --start-datetime="$(date)" /var/log/mysql/mysql-bin.log > incremental.sql

-- Retención: 30 días backups completos, 7 días incrementales
```

---

<a name="actividad-5"></a>
## 🔒 ACTIVIDAD 5: PROGRAMACIÓN SEGURA

### 5.1 Roles y Perfiles de Usuario

#### Matriz de Permisos

| Funcionalidad | Administrador | Médico | Matrona | TENS |
|---------------|---------------|--------|---------|------|
| Gestionar Usuarios | ✅ | ❌ | ❌ | ❌ |
| Ver Estadísticas | ✅ | ✅ | ✅ | ❌ |
| Registrar Pacientes | ✅ | ❌ | ✅ | ❌ |
| Crear Fichas Obstétricas | ✅ | ❌ | ✅ | ❌ |
| Registrar Partos | ✅ | ✅ | ✅ | ❌ |
| Gestionar Patologías | ✅ | ✅ | ❌ | ❌ |
| Prescribir Medicamentos | ✅ | ✅ | ✅ | ❌ |
| Administrar Medicamentos | ✅ | ❌ | ✅ | ✅ |
| Registrar Signos Vitales | ✅ | ❌ | ✅ | ✅ |
| Ver Historial Completo | ✅ | ✅ | ✅ | ❌ |
| Modificar Datos Históricos | ✅ | ❌ | ❌ | ❌ |

#### Implementación en Django

```python
# gestionApp/decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def es_matrona(usuario):
    """Verifica si el usuario es matrona"""
    return hasattr(usuario, 'matrona')

def es_medico(usuario):
    """Verifica si el usuario es médico"""
    return hasattr(usuario, 'medico')

def es_tens(usuario):
    """Verifica si el usuario es TENS"""
    return hasattr(usuario, 'tens')

def requiere_rol(*roles_permitidos):
    """
    Decorador personalizado para verificar roles
    Uso: @requiere_rol('matrona', 'medico')
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            usuario = request.user
            
            if not usuario.is_authenticated:
                raise PermissionDenied("Debe iniciar sesión")
            
            tiene_permiso = False
            
            if 'admin' in roles_permitidos and usuario.is_staff:
                tiene_permiso = True
            if 'matrona' in roles_permitidos and hasattr(usuario, 'matrona'):
                tiene_permiso = True
            if 'medico' in roles_permitidos and hasattr(usuario, 'medico'):
                tiene_permiso = True
            if 'tens' in roles_permitidos and hasattr(usuario, 'tens'):
                tiene_permiso = True
                
            if not tiene_permiso:
                raise PermissionDenied("No tiene permisos para esta acción")
                
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Ejemplo de uso en views.py
@requiere_rol('matrona', 'admin')
def registrar_parto(request):
    # Solo matronas y admins pueden registrar partos
    pass
```

### 5.2 Estándares de Codificación Segura

#### 5.2.1 Validación de Entradas

**Problema:** Inyección SQL, XSS, datos maliciosos

**Solución:** Siempre usar ORM de Django y validar datos

```python
# ❌ MAL - Vulnerable a SQL Injection
def buscar_paciente_inseguro(request):
    rut = request.GET.get('rut')
    # NUNCA HACER ESTO
    query = f"SELECT * FROM paciente WHERE rut = '{rut}'"
    # Un atacante podría enviar: rut=' OR '1'='1

# ✅ BIEN - Uso seguro del ORM
def buscar_paciente_seguro(request):
    rut = request.GET.get('rut', '').strip()
    
    # Validar formato RUT
    if not validar_rut_chileno(rut):
        return JsonResponse({'error': 'RUT inválido'}, status=400)
    
    # ORM previene SQL injection automáticamente
    try:
        paciente = Paciente.objects.select_related('persona').get(
            persona__Rut=rut
        )
        return JsonResponse({
            'id': paciente.persona.id,
            'nombre': paciente.persona.Nombre,
            'rut': paciente.persona.Rut
        })
    except Paciente.DoesNotExist:
        return JsonResponse({'error': 'Paciente no encontrado'}, status=404)

# Validación personalizada de RUT
def validar_rut_chileno(rut):
    """
    Valida formato y dígito verificador de RUT chileno
    Retorna True si es válido
    """
    import re
    
    # Formato: 12.345.678-9 o 12345678-9
    patron = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$|^\d{7,8}-[\dkK]$'
    if not re.match(patron, rut):
        return False
    
    # Validar dígito verificador
    rut_limpio = rut.replace('.', '').replace('-', '')
    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1].upper()
    
    suma = 0
    multiplicador = 2
    
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2
    
    resto = suma % 11
    dv_calculado = 'K' if resto == 1 else ('0' if resto == 0 else str(11 - resto))
    
    return dv == dv_calculado
```

#### 5.2.2 Autenticación y Autorización

```python
# settings.py - Configuración de seguridad

# Contraseñas seguras
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}  # Mínimo 12 caracteres
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Seguridad de sesiones
SESSION_COOKIE_SECURE = True  # Solo HTTPS en producción
SESSION_COOKIE_HTTPONLY = True  # No accesible desde JavaScript
SESSION_COOKIE_SAMESITE = 'Strict'  # Protección CSRF
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Cerrar al cerrar navegador
SESSION_COOKIE_AGE = 28800  # 8 horas de sesión

# CSRF Protection
CSRF_COOKIE_SECURE = True  # Solo HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True  # Token CSRF en sesión

# Seguridad general
SECURE_SSL_REDIRECT = True  # Forzar HTTPS
SECURE_HSTS_SECONDS = 31536000  # HSTS 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'  # Prevenir clickjacking

# Login
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
```

#### 5.2.3 Gestión de Errores

```python
# utils/error_handlers.py

import logging
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

def manejar_error_personalizado(request, exception):
    """
    Manejo centralizado de errores
    No revelar información sensible al usuario
    """
    
    # ❌ MAL - Exponer detalles del error
    # return JsonResponse({'error': str(exception), 'traceback': traceback.format_exc()})
    
    # ✅ BIEN - Mensaje genérico al usuario, log detallado interno
    logger.error(f"Error en {request.path}: {str(exception)}", 
                 exc_info=True, 
                 extra={'user': request.user.username if request.user.is_authenticated else 'anónimo'})
    
    if request.is_ajax():
        return JsonResponse({
            'error': 'Ha ocurrido un error. Por favor contacte al administrador.',
            'error_code': 'ERR_INTERNAL'
        }, status=500)
    else:
        return render(request, 'error.html', {
            'mensaje': 'Ha ocurrido un error inesperado.',
            'codigo': 'ERR_500'
        }, status=500)

# En views.py
def vista_segura(request):
    try:
        # Lógica de la vista
        paciente = Paciente.objects.get(pk=paciente_id)
        # ...
    except Paciente.DoesNotExist:
        # Error esperado - mensaje específico
        return JsonResponse({'error': 'Paciente no encontrado'}, status=404)
    except Exception as e:
        # Error inesperado - manejo genérico
        return manejar_error_personalizado(request, e)
```

#### 5.2.4 Cifrado de Datos Sensibles

```python
# utils/encryption.py

from django.conf import settings
from cryptography.fernet import Fernet
import base64

class EncriptadorDatos:
    """
    Encriptador para datos médicos sensibles
    Usa Fernet (AES 128 en modo CBC)
    """
    
    def __init__(self):
        # La clave debe estar en variables de entorno, NO en código
        clave = settings.ENCRYPTION_KEY.encode()
        self.cipher = Fernet(clave)
    
    def encriptar(self, texto: str) -> str:
        """
        Encripta texto y retorna string base64
        """
        if not texto:
            return ""
        
        texto_bytes = texto.encode('utf-8')
        texto_encriptado = self.cipher.encrypt(texto_bytes)
        return base64.b64encode(texto_encriptado).decode('utf-8')
    
    def desencriptar(self, texto_encriptado: str) -> str:
        """
        Desencripta string base64 y retorna texto original
        """
        if not texto_encriptado:
            return ""
        
        try:
            texto_bytes = base64.b64decode(texto_encriptado.encode('utf-8'))
            texto_desencriptado = self.cipher.decrypt(texto_bytes)
            return texto_desencriptado.decode('utf-8')
        except Exception as e:
            logger.error(f"Error al desencriptar: {e}")
            raise ValueError("No se pudo desencriptar el dato")

# Uso en modelos para datos sensibles
from django.db import models

class FichaObstetricaSegura(models.Model):
    # Datos sensibles encriptados
    observaciones_privadas = models.TextField()  # Se encripta antes de guardar
    
    def set_observaciones(self, texto):
        """Guarda observaciones encriptadas"""
        encriptador = EncriptadorDatos()
        self.observaciones_privadas = encriptador.encriptar(texto)
    
    def get_observaciones(self):
        """Obtiene observaciones desencriptadas"""
        encriptador = EncriptadorDatos()
        return encriptador.desencriptar(self.observaciones_privadas)
```

### 5.3 Protección OWASP Top 10

| Riesgo OWASP | Medida Implementada | Código/Configuración |
|--------------|---------------------|----------------------|
| A01: Broken Access Control | Decoradores de rol, permisos Django | `@requiere_rol('matrona')` |
| A02: Cryptographic Failures | Cifrado Fernet, HTTPS obligatorio | `SECURE_SSL_REDIRECT = True` |
| A03: Injection | ORM Django, validación entradas | `Paciente.objects.filter()` |
| A04: Insecure Design | Arquitectura por capas, separación | Estructura apps Django |
| A05: Security Misconfiguration | Settings seguros, sin DEBUG en prod | `DEBUG = False` |
| A06: Vulnerable Components | Actualización dependencias | `pip list --outdated` |
| A07: Authentication Failures | Contraseñas fuertes, sesiones seguras | `SESSION_COOKIE_SECURE` |
| A08: Software Data Integrity | Integridad BD, backups | Transacciones ACID |
| A09: Logging Failures | Logging centralizado | `logger.error()` |
| A10: SSRF | Validación URLs, sin requests externos | Whitelist dominios |

### 5.4 Auditoría y Logging

```python
# middleware/audit_middleware.py

import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('audit')

class AuditMiddleware(MiddlewareMixin):
    """
    Middleware para auditar todas las acciones críticas
    """
    
    ACCIONES_CRITICAS = [
        '/partos/registrar/',
        '/pacientes/crear/',
        '/fichas/crear/',
        '/medicamentos/prescribir/',
    ]
    
    def process_request(self, request):
        """Registra cada request a endpoints críticos"""
        
        if any(ruta in request.path for ruta in self.ACCIONES_CRITICAS):
            logger.info(
                f"[AUDIT] Acción: {request.method} {request.path} | "
                f"Usuario: {request.user.username if request.user.is_authenticated else 'anónimo'} | "
                f"IP: {self.get_client_ip(request)} | "
                f"Timestamp: {datetime.now().isoformat()}"
            )
    
    def process_response(self, request, response):
        """Registra respuestas de acciones críticas"""
        
        if any(ruta in request.path for ruta in self.ACCIONES_CRITICAS):
            logger.info(
                f"[AUDIT] Respuesta: {response.status_code} | "
                f"Path: {request.path} | "
                f"Usuario: {request.user.username if request.user.is_authenticated else 'anónimo'}"
            )
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        """Obtiene IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

### 5.5 Recomendaciones para SonarQube

```yaml
# sonar-project.properties

sonar.projectKey=obstetric_care
sonar.projectName=Sistema Gestión Obstétrica
sonar.projectVersion=1.0
sonar.sources=.
sonar.exclusions=**/migrations/**,**/tests/**,**/venv/**

# Python específico
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml

# Reglas de seguridad
sonar.python.bandit.reportPaths=bandit-report.json

# Quality Gates
sonar.qualitygate.wait=true
```

**Comandos para análisis:**

```bash
# Instalar herramientas
pip install bandit safety

# Análisis de seguridad con Bandit
bandit -r . -f json -o bandit-report.json

# Verificar dependencias vulnerables
safety check --json

# Ejecutar SonarQube
sonar-scanner
```

---

<a name="actividad-6"></a>
## 🧪 ACTIVIDAD 6: PLAN DE PRUEBAS

### 6.1 Estrategia General de Pruebas

**Estándar Adoptado:** IEEE 829 (Adaptado para metodología ágil)

#### Alcance de Pruebas:

- ✅ Pruebas Unitarias (80% cobertura mínima)
- ✅ Pruebas de Integración
- ✅ Pruebas Funcionales
- ✅ Pruebas de Seguridad (OWASP)
- ✅ Pruebas de Rendimiento
- ⚠️ Pruebas de Usabilidad (con usuarios reales)

### 6.2 Plan de Pruebas IEEE 829

#### 6.2.1 Test Plan Identifier

**ID:** TP-OBSTETRIC-001  
**Versión:** 1.0  
**Fecha:** 08/11/2025

#### 6.2.2 Referencias

- Requisitos del Sistema: Documento Unidad 1
- Arquitectura: Sección 2 de este documento
- Casos de Uso: Historias de Usuario Sprint Backlog

#### 6.2.3 Introducción

El presente plan de pruebas establece la estrategia integral para validar el Sistema de Gestión Obstétrica desarrollado en Django, asegurando que cumple con los requisitos funcionales, de seguridad y rendimiento establecidos.

#### 6.2.4 Items a Probar

| Módulo | Componentes | Prioridad |
|--------|-------------|-----------|
| Gestión Personas/Pacientes | CRUD, validaciones RUT | Alta |
| Fichas Obstétricas | Cálculo FPP, EG, validaciones | Alta |
| Registro Partos | Proceso completo multi-paso | Alta |
| Recién Nacidos | Cálculo APGAR, registro gemelos | Alta |
| Patologías | CRUD, asignación a pacientes | Media |
| Medicamentos | Prescripción, administración | Media |
| TENS | Signos vitales, control | Media |
| API REST | Endpoints, autenticación | Media |
| Seguridad | Autenticación, autorización, OWASP | Alta |
| Rendimiento | Tiempo respuesta, carga | Media |

### 6.3 Tipos de Pruebas Detalladas

#### 6.3.1 Pruebas Funcionales

**Caso de Prueba: Registro de Ficha Obstétrica**

```python
# matronaApp/tests/test_ficha_obstetrica.py

from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from gestionApp.models import Persona, Paciente, Matrona
from matronaApp.models import FichaObstetrica

class FichaObstetricaTestCase(TestCase):
    """
    Suite de pruebas para FichaObstetrica
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        
        # Crear persona paciente
        self.persona_paciente = Persona.objects.create(
            Rut='18234567-8',
            Nombre='María',
            Apellido_Paterno='González',
            Apellido_Materno='Pérez',
            Fecha_Nacimiento=date(1995, 5, 15),
            Sexo='F',
            Telefono='+56912345678'
        )
        
        # Crear paciente
        self.paciente = Paciente.objects.create(
            persona=self.persona_paciente,
            GrupoSanguineo='O+',
            Peso=65.5,
            Talla=1.65,
            Prevision='FONASA',
            Activa=True
        )
        
        # Crear matrona
        persona_matrona = Persona.objects.create(
            Rut='15678234-5',
            Nombre='Ana',
            Apellido_Paterno='Martínez',
            Apellido_Materno='López',
            Fecha_Nacimiento=date(1980, 3, 20),
            Sexo='F'
        )
        
        self.matrona = Matrona.objects.create(
            persona=persona_matrona,
            Especialidad='Atención del Parto',
            Registro_medico='MAT-001',
            Años_experiencia=10,
            Turno='Mañana',
            Activo=True
        )
        
        self.client = Client()
    
    def test_crear_ficha_obstetrica_exitoso(self):
        """
        TC-FO-001: Crear ficha obstétrica con datos válidos
        Resultado Esperado: Ficha creada correctamente con FPP calculado
        """
        
        # Datos de entrada
        fur = date.today() - timedelta(days=120)  # 17 semanas atrás
        
        ficha = FichaObstetrica.objects.create(
            paciente=self.paciente,
            matrona_responsable=self.matrona,
            numero_ficha='FO-000001',
            numero_gestas=2,
            numero_partos=1,
            partos_vaginales=1,
            partos_cesareas=0,
            numero_abortos=0,
            fecha_ultima_regla=fur,
            activa=True
        )
        
        # Assertions
        self.assertIsNotNone(ficha.id)
        self.assertEqual(ficha.numero_ficha, 'FO-000001')
        
        # Verificar cálculo de FPP (FUR + 280 días)
        fpp_esperado = fur + timedelta(days=280)
        self.assertEqual(ficha.fecha_probable_parto, fpp_esperado)
        
        # Verificar edad gestacional
        edad_gestacional = ficha.calcular_edad_gestacional()
        self.assertGreaterEqual(edad_gestacional['semanas'], 17)
    
    def test_validacion_gestas_partos(self):
        """
        TC-FO-002: Validar que número de partos no supere gestas
        Resultado Esperado: ValidationError
        """
        
        from django.core.exceptions import ValidationError
        
        with self.assertRaises(ValidationError):
            ficha = FichaObstetrica(
                paciente=self.paciente,
                matrona_responsable=self.matrona,
                numero_ficha='FO-000002',
                numero_gestas=1,  # Solo 1 gesta
                numero_partos=3,  # Pero 3 partos -> INVÁLIDO
                fecha_ultima_regla=date.today() - timedelta(days=100)
            )
            ficha.full_clean()  # Ejecuta validaciones
    
    def test_numero_ficha_unico(self):
        """
        TC-FO-003: Verificar unicidad de número de ficha
        Resultado Esperado: IntegrityError al duplicar
        """
        
        from django.db import IntegrityError
        
        # Primera ficha
        FichaObstetrica.objects.create(
            paciente=self.paciente,
            matrona_responsable=self.matrona,
            numero_ficha='FO-000001',
            numero_gestas=1,
            numero_partos=0,
            fecha_ultima_regla=date.today() - timedelta(days=100)
        )
        
        # Intentar crear segunda ficha con mismo número
        with self.assertRaises(IntegrityError):
            FichaObstetrica.objects.create(
                paciente=self.paciente,
                matrona_responsable=self.matrona,
                numero_ficha='FO-000001',  # Duplicado
                numero_gestas=1,
                numero_partos=0,
                fecha_ultima_regla=date.today() - timedelta(days=80)
            )
```

#### 6.3.2 Pruebas de Integración

**Caso de Prueba: Flujo Completo de Parto**

```python
# partosApp/tests/test_flujo_parto.py

from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, date
import json

class FlujoPartoIntegracionTestCase(TestCase):
    """
    Pruebas de integración para el flujo completo de registro de parto
    """
    
    fixtures = ['personas.json', 'fichas.json']  # Datos de prueba
    
    def setUp(self):
        self.client = Client()
        # Login como matrona
        self.client.login(username='matrona1', password='test123')
    
    def test_flujo_completo_parto_vaginal(self):
        """
        TC-INT-001: Flujo completo desde selección de ficha hasta RN
        Escenario: Parto vaginal simple con 1 RN
        """
        
        # PASO 1: Seleccionar ficha obstétrica
        response = self.client.get(reverse('partos:seleccionar_ficha'))
        self.assertEqual(response.status_code, 200)
        
        # Buscar ficha activa
        ficha_id = 1  # De fixtures
        
        # PASO 2: Iniciar registro de parto
        datos_parto = {
            'ficha': ficha_id,
            'fecha_hora_admision': datetime.now().isoformat(),
            'edad_gestacional_semanas': 39,
            'edad_gestacional_dias': 2,
            'tipo_parto': 'VAGINAL',
        }
        
        response = self.client.post(
            reverse('partos:registrar_parto_paso1', kwargs={'ficha_pk': ficha_id}),
            data=datos_parto
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect a paso 2
        
        # Verificar que se creó el parto
        from partosApp.models import RegistroParto
        parto = RegistroParto.objects.latest('id')
        self.assertIsNotNone(parto)
        self.assertEqual(parto.tipo_parto, 'VAGINAL')
        
        # PASO 3: Registrar trabajo de parto
        datos_trabajo = {
            'tiempo_dilatacion': 240,  # 4 horas
            'tiempo_expulsivo': 25,    # 25 minutos
            'monitor_ttc': True,
            'libertad_movimiento': True,
        }
        
        response = self.client.post(
            reverse('partos:registrar_parto_paso2'),
            data=datos_trabajo
        )
        
        self.assertEqual(response.status_code, 302)
        
        # PASO 4: Registrar recién nacido
        datos_rn = {
            'sexo': 'M',
            'peso': 3450,  # gramos
            'talla': 51,   # cm
            'apgar_1_minuto': 9,
            'apgar_5_minutos': 10,
            'ligadura_tardia_cordon': True,
            'apego_canguro': True,
        }
        
        response = self.client.post(
            reverse('partos:registrar_rn', kwargs={'parto_pk': parto.pk}),
            data=datos_rn
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Verificar RN creado
        from recienNacidoApp.models import RegistroRecienNacido
        rn = RegistroRecienNacido.objects.filter(registro_parto=parto).first()
        
        self.assertIsNotNone(rn)
        self.assertEqual(rn.peso, 3450)
        self.assertEqual(rn.apgar_5_minutos, 10)
        self.assertTrue(rn.ligadura_tardia_cordon)
        
        # PASO 5: Verificar integridad de datos
        parto.refresh_from_db()
        self.assertIsNotNone(parto.fecha_hora_parto)
        self.assertEqual(parto.registros_rn.count(), 1)
```

#### 6.3.3 Pruebas de Seguridad

**Matriz de Pruebas OWASP**

| ID | Vulnerabilidad OWASP | Test Case | Herramienta | Prioridad |
|----|----------------------|-----------|-------------|-----------|
| SEC-01 | A03: Injection | SQL Injection en búsquedas | SQLMap, Manual | Alta |
| SEC-02 | A03: Injection | XSS en formularios | OWASP ZAP | Alta |
| SEC-03 | A01: Access Control | Acceso no autorizado a vistas | Manual, Pytest | Alta |
| SEC-04 | A07: Authentication | Fuerza bruta login | Hydra | Media |
| SEC-05 | A02: Crypto Failures | Datos sensibles sin cifrar | Manual | Alta |
| SEC-06 | A05: Config | Debug=True en producción | Bandit | Alta |
| SEC-07 | A04: Insecure Design | CSRF en formularios críticos | Manual | Alta |
| SEC-08 | A09: Logging | Logs sin información sensible | Manual | Media |

**Caso de Prueba: SQL Injection**

```python
# tests/security/test_sql_injection.py

from django.test import TestCase, Client
from django.urls import reverse

class SQLInjectionTestCase(TestCase):
    """
    Pruebas de seguridad contra SQL Injection
    """
    
    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='test123')
    
    def test_sql_injection_busqueda_paciente(self):
        """
        SEC-01: Intentar SQL injection en búsqueda de pacientes
        Resultado Esperado: Request bloqueado o sin efecto
        """
        
        # Payloads de SQL injection comunes
        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE gestionapp_paciente; --",
            "' UNION SELECT * FROM auth_user --",
            "1' AND 1=1 --",
        ]
        
        for payload in payloads:
            response = self.client.get(
                reverse('matrona:api_buscar_paciente'),
                {'q': payload}
            )
            
            # No debe causar error 500
            self.assertNotEqual(response.status_code, 500)
            
            # No debe retornar todos los registros
            if response.status_code == 200:
                data = response.json()
                self.assertLess(len(data.get('results', [])), 100)
    
    def test_xss_en_formulario_ficha(self):
        """
        SEC-02: Intentar XSS en campos de texto
        Resultado Esperado: Contenido escapado correctamente
        """
        
        payload_xss = "<script>alert('XSS')</script>"
        
        from matronaApp.models import FichaObstetrica
        from gestionApp.models import Paciente
        
        paciente = Paciente.objects.first()
        
        ficha = FichaObstetrica.objects.create(
            paciente=paciente,
            nombre_acompanante=payload_xss,  # Intento XSS
            numero_gestas=1,
            numero_partos=0,
        )
        
        # Obtener vista con la ficha
        response = self.client.get(
            reverse('matrona:detalle_ficha', kwargs={'pk': ficha.pk})
        )
        
        # Verificar que el script fue escapado
        self.assertNotContains(response, "<script>")
        self.assertContains(response, "&lt;script&gt;")  # HTML escapado
```

#### 6.3.4 Pruebas de Rendimiento

**Plan de Pruebas de Carga con Locust**

```python
# tests/performance/locustfile.py

from locust import HttpUser, task, between
import random

class ObstetricUser(HttpUser):
    """
    Simulación de usuario del sistema obstétrico
    """
    
    wait_time = between(1, 3)  # Espera entre 1-3 segundos entre tareas
    
    def on_start(self):
        """Login al iniciar"""
        self.client.post("/login/", {
            "username": "matrona1",
            "password": "test123"
        })
    
    @task(3)  # Peso 3 (más frecuente)
    def ver_dashboard(self):
        """Acceso al dashboard principal"""
        self.client.get("/dashboard/")
    
    @task(2)
    def listar_pacientes(self):
        """Listar pacientes activos"""
        self.client.get("/pacientes/listar/")
    
    @task(2)
    def buscar_paciente(self):
        """Buscar paciente por RUT"""
        ruts = [
            "18234567-8",
            "17654321-9",
            "19876543-2"
        ]
        self.client.get(f"/api/paciente/buscar/?q={random.choice(ruts)}")
    
    @task(1)  # Menos frecuente
    def ver_ficha_obstetrica(self):
        """Ver detalle de ficha obstétrica"""
        ficha_id = random.randint(1, 100)
        self.client.get(f"/fichas/{ficha_id}/")
    
    @task(1)
    def crear_parto(self):
        """Simular inicio de registro de parto"""
        self.client.get("/partos/seleccionar-ficha/")

# Ejecutar prueba:
# locust -f locustfile.py --host=http://localhost:8000 --users 50 --spawn-rate 5
```

**Criterios de Aceptación de Rendimiento:**

| Métrica | Objetivo | Límite Aceptable |
|---------|----------|------------------|
| Tiempo respuesta promedio | < 200ms | < 500ms |
| Tiempo respuesta p95 | < 500ms | < 1000ms |
| Tasa de error | < 0.1% | < 1% |
| Throughput | > 100 req/s | > 50 req/s |
| Usuarios concurrentes | 50 usuarios | 30 usuarios |

### 6.4 Matriz de Trazabilidad

| Requisito | Historia Usuario | Caso de Prueba | Estado | Prioridad |
|-----------|------------------|----------------|--------|-----------|
| REQ-01 | US-01 | TC-FO-001, TC-FO-002 | ✅ Pass | Alta |
| REQ-02 | US-02 | TC-FO-003, TC-INT-001 | ✅ Pass | Alta |
| REQ-03 | US-03 | TC-PAR-001 | ⏳ En progreso | Alta |
| REQ-04 | US-04 | TC-INT-001 | ✅ Pass | Alta |
| REQ-05 | US-05 | TC-RN-001 | ✅ Pass | Alta |
| SEG-01 | - | SEC-01, SEC-02 | ✅ Pass | Alta |
| PERF-01 | - | PERF-LOAD-001 | ⏳ En progreso | Media |

### 6.5 Ambiente de Pruebas

```yaml
# docker-compose-test.yml

version: '3.8'

services:
  db-test:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: obstetric_test
      MYSQL_ROOT_PASSWORD: testpassword
    ports:
      - "3307:3306"
  
  web-test:
    build: .
    command: python manage.py test --settings=obstetric_care.settings_test
    volumes:
      - .:/app
    depends_on:
      - db-test
    environment:
      DATABASE_URL: mysql://root:testpassword@db-test:3306/obstetric_test
      DEBUG: False
```

### 6.6 Reporte de Pruebas

**Template de Reporte:**

```
REPORTE DE PRUEBAS - SISTEMA OBSTÉTRICO
Fecha: [DD/MM/YYYY]
Sprint: [Número]
Ejecutor: [Nombre]

1. RESUMEN EJECUTIVO
   - Total casos ejecutados: XX
   - Casos exitosos: XX (XX%)
   - Casos fallidos: XX (XX%)
   - Casos bloqueados: XX (XX%)

2. COBERTURA
   - Cobertura de código: XX%
   - Cobertura de requisitos: XX/XX (XX%)

3. DEFECTOS ENCONTRADOS
   - Críticos: XX
   - Altos: XX
   - Medios: XX
   - Bajos: XX

4. RECOMENDACIONES
   [Lista de acciones]

5. ANEXOS
   - Screenshots de fallos
   - Logs de ejecución
   - Evidencias de pruebas
```

---

## 📚 CONCLUSIONES Y RECOMENDACIONES

### Logros del Documento:

1. ✅ **Metodología Ágil Definida:** Scrum con sprints de 2 semanas
2. ✅ **Arquitectura Sólida:** Paradigma 4+1 documentado completamente
3. ✅ **Interfaces Diseñadas:** Prototipos y flujos de usuario
4. ✅ **Base de Datos Normalizada:** Modelo relacional completo
5. ✅ **Seguridad Implementada:** OWASP Top 10 cubierto
6. ✅ **Plan de Pruebas Robusto:** Funcionales, integración, seguridad, rendimiento

### Próximos Pasos:

1. **Desarrollo Iterativo:** Seguir sprints planificados
2. **Pruebas Continuas:** Ejecutar suite de tests en cada commit
3. **Auditoría de Seguridad:** SonarQube y Bandit semanalmente
4. **Validación con Usuarios:** Sesiones de feedback cada sprint
5. **Documentación Técnica:** Mantener actualizada con código

### Riesgos Identificados:

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Cambio de requisitos | Media | Alto | Metodología ágil, sprints cortos |
| Problemas de rendimiento | Baja | Alto | Pruebas de carga continuas |
| Vulnerabilidades seguridad | Media | Crítico | Auditorías automatizadas |
| Rotación de personal | Media | Medio | Documentación completa |
| Integración con sistemas legacy | Alta | Alto | Capa de abstracción, pruebas |

---

## 📎 ANEXOS

### Anexo A: Glosario de Términos

- **APGAR:** Sistema de evaluación del recién nacido (0-10 puntos)
- **FPP:** Fecha Probable de Parto
- **FUR:** Fecha Última Regla
- **EG:** Edad Gestacional
- **CIE-10:** Clasificación Internacional de Enfermedades, 10ª revisión
- **Robson:** Sistema de clasificación de cesáreas (10 grupos)
- **TENS:** Técnico de Enfermería de Nivel Superior

### Anexo B: Referencias

1. Django Documentation: https://docs.djangoproject.com/
2. OWASP Top 10: https://owasp.org/www-project-top-ten/
3. IEEE 829-2008: Standard for Software Test Documentation
4. Bootstrap 5 Docs: https://getbootstrap.com/docs/5.0/
5. Clasificación de Robson: OMS, 2015

### Anexo C: Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 08/11/2025 | Equipo Desarrollo | Documento inicial completo |

---

**FIN DEL DOCUMENTO**

*Este documento fue generado basándose en el proyecto real alojado en GitHub Classroom y representa el trabajo de diseño de la Unidad 2 del curso de Análisis y Diseño de Sistemas.*
