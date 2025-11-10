# Documentación general del proyecto: Obtetric Care

Resumen
- Nombre: Obtetric Care (nombre provisional)
- Propósito: Sistema para gestión integral de atención obstétrica: pacientes, citas, historiales clínicos, seguimiento perinatal, reportes y módulos administrativos.
- Público objetivo: personal médico (obstetras, enfermería), administrativos, desarrolladores y responsables DevOps.

Índice
1. Visión general
2. Requisitos
3. Instalación local
4. Estructura del proyecto
5. Módulos y responsabilidades
6. API y contratos
7. Base de datos y modelos de datos
8. Flujo de despliegue / DevOps
9. Pruebas
10. Seguridad y cumplimiento
11. Convenciones de código y buenas prácticas
12. Mantenimiento y troubleshooting
13. Contribuir
14. Licencia y contactos

1. Visión general
- Funcionalidades claves:
    - Registro y gestión de pacientes.
    - Gestión de citas y recordatorios.
    - Registro de controles prenatales y partos.
    - Gestión de equipos médicos y turnos.
    - Generación de reportes clínicos y estadísticos.
    - Integración con sistemas de imágenes y laboratorio (API).
- Alcance: back-end (APIs), front-end (web responsivo), base de datos relacional, servicios de notificación (email/SMS).

2. Requisitos
- Software:
    - Node.js >= 16 (si es backend JS) o especificar stack (Django/Python, .NET, etc.).
    - Gestor de paquetes: npm/yarn o pip/poetry, dotnet CLI.
    - Base de datos: PostgreSQL >= 12 (o MySQL/MSSQL según stack).
    - Docker y Docker Compose para entornos reproducibles.
- Hardware mínimo: 2 CPU, 4GB RAM para entorno de desarrollo.
- Variables de entorno: ejemplo en .env (ver más abajo).

3. Instalación local
- Clonar repositorio:
    - git clone <URL-del-repo>
    - cd <nombre-del-proyecto>
- Configurar .env (archivo de ejemplo .env.example):
    - DATABASE_URL=postgres://user:pass@localhost:5432/obtetric
    - PORT=3000
    - JWT_SECRET=changeme
    - SMTP_HOST=...
    - SMS_PROVIDER_KEY=...
- Instalar dependencias:
    - Node: npm install || yarn install
    - Python: pip install -r requirements.txt
- Levantar servicios con Docker Compose:
    - docker-compose up --build
- Migraciones / inicialización BD:
    - npm run migrate || alembic upgrade head || dotnet ef database update
- Ejecutar aplicación:
    - npm start || flask run || dotnet run

4. Estructura del proyecto (ejemplo)
- /src
    - /api — controladores y rutas
    - /services — lógica de negocio
    - /models — esquemas y modelos de datos
    - /db — migraciones y seeders
    - /scripts — utilidades
- /web — front-end (React/Vue/Angular)
- /docs — documentación adicional
- /tests — pruebas unitarias e integración
- docker-compose.yml, Dockerfile, README.md

5. Módulos y responsabilidades
- Autenticación y autorización:
    - JWT, roles: admin, medico, enfermera, recepcionista.
    - Gestión de sesiones y revocación de tokens.
- Pacientes:
    - CRUD paciente, historial clínico, adjuntos (documentos e imágenes).
- Citas:
    - Agendar, reprogramar, cancelar, notificaciones.
- Controles prenatales:
    - Registrar controles, alertas por riesgo.
- Partos y eventos perinatales:
    - Registro de evento, acta de parto.
- Reportes:
    - Estadísticas por periodo (nacimientos, emergencias, morbilidad).
- Integraciones:
    - Laboratorio, imágenes, servicios de mensajería.
- Administración:
    - Gestión de usuarios, permisos, configuración del sistema.

6. API y contratos
- Estándares:
    - RESTful JSON.
    - Versionado: /api/v1/...
    - Paginación: ?page=1&per_page=20
    - Filtros: ?from=YYYY-MM-DD&to=YYYY-MM-DD
- Autenticación:
    - POST /api/v1/auth/login -> { token, refreshToken }
    - POST /api/v1/auth/refresh -> { token }
- Endpoints ejemplo (resumen):
    - Patients:
        - GET /api/v1/patients
        - POST /api/v1/patients
        - GET /api/v1/patients/{id}
        - PUT /api/v1/patients/{id}
    - Appointments:
        - GET /api/v1/appointments
        - POST /api/v1/appointments
    - Prenatal controls:
        - POST /api/v1/prenatal/{patientId}/controls
- Errores:
    - Respuestas estándar: { code, message, details? }
    - Código HTTP apropiado (200, 201, 400, 401, 403, 404, 422, 500).

7. Base de datos y modelos de datos
- Recomendación: modelo relacional (PostgreSQL).
- Entidades principales:
    - User (id, name, email, role, password_hash, created_at)
    - Patient (id, document_id, name, dob, contact, address, medical_history_reference)
    - Appointment (id, patient_id, professional_id, datetime, status, reason)
    - PrenatalControl (id, patient_id, date, gestational_age, findings, vitals)
    - BirthEvent (id, patient_id, date, type, outcome, notes)
    - Attachment (id, owner_type, owner_id, file_path, mime_type)
- Índices: sobre patient.document_id, appointment.datetime, foreign keys.
- Backup y retención: políticas y cronograma.

8. Flujo de despliegue / DevOps
- Entorno: dev -> staging -> production.
- CI:
    - Build, lint, tests, security scan.
- CD:
    - Despliegue automatizado desde rama release/main.
    - Uso de Docker images versionadas (tags semánticos).
- Monitoring:
    - Logs centralizados (ELK/Prometheus+Grafana).
    - Alertas en errores críticos y uso de recursos.
- Rollback: mantener releases anteriores con tag para revertir.

9. Pruebas
- Tipos:
    - Unitarias: cobertura para lógica crítica.
    - Integración: endpoints, conexión DB, servicios externos (mocked/staging).
    - E2E (opcional): flujos clave en front-end.
- Comandos:
    - npm test
    - pytest
- Coverage target: >= 80% en módulos críticos.

10. Seguridad y cumplimiento
- Sensible a datos clínicos: aplicar normas de privacidad locales (ej. GDPR/HIPAA según jurisdicción).
- Buenas prácticas:
    - Encriptar datos sensibles en tránsito (TLS) y en reposo cuando aplique.
    - Gestión segura de secretos (Vault, Azure Key Vault, AWS Secrets Manager).
    - Políticas de acceso mínimo por rol.
    - Logs de auditoría: acceso a historiales y cambios.
    - Validación y sanitización de entradas.
    - Rate limiting en endpoints públicos y protección contra CSRF/XSS/SQLi.
- Dependencias: mantener actualizadas y ejecutar SCA (Software Composition Analysis).

11. Convenciones de código y buenas prácticas
- Estilo: ESLint/Prettier para JS; PEP8/Black para Python; reglas internas para naming.
- Commit messages: convención tipo Conventional Commits.
- Branching: Git Flow simple (feature/*, hotfix/*, main).
- Revisiones: PRs, mínimo 1 revisor, pasar CI antes de merge.

12. Mantenimiento y troubleshooting
- Logs: ubicación y formato (JSON). Cómo buscar errores comunes.
- Pasos para debug:
    1. Reproducir en entorno local.
    2. Revisar logs del servicio y de la BD.
    3. Revisar health checks y métricas.
- Operaciones de mantenimiento:
    - Migraciones: documentar proceso y backups previos.
    - Limpieza de archivos adjuntos antiguos según política de retención.

13. Contribuir
- Proceso:
    1. Abrir issue describiendo la mejora o bug.
    2. Crear branch desde main: feature/mi-feature.
    3. Tests asociados.
    4. PR con descripción y referencias.
- Código: seguir convenciones y pasar linters/tests.
- Responsables y reviewers: listar por equipo (rellenar según organización).

14. Licencia y contactos
- Licencia: especificar archivo LICENSE (MIT/Apache-2.0/privada).
- Contacto de soporte:
    - Equipo de desarrollo: dev-team@example.org
    - Soporte clínico: soporte-clinico@example.org
    - Responsable de seguridad: secops@example.org

Apéndices

A. Archivo .env.example (ejemplo)
- DATABASE_URL=postgres://user:pass@localhost:5432/obtetric
- PORT=3000
- JWT_SECRET=your_jwt_secret
- SMTP_HOST=smtp.example.com
- SMTP_PORT=587
- SMTP_USER=user
- SMTP_PASS=pass
- SENTRY_DSN=
- STORAGE_PROVIDER=s3
- S3_BUCKET=
- S3_KEY=
- S3_SECRET=

B. Comandos útiles
- Levantar dev: docker-compose up --build
- Ejecutar tests: npm test
- Migrar BD: npm run migrate
- Lint: npm run lint

C. Checklist para entrega a producción
- Backups y snapshot de BD configurados.
- Certificados TLS válidos.
- Monitoreo y alertas configuradas.
- Plan de rollback y pruebas de DR (disaster recovery).
- Revisión de seguridad y escaneo de dependencias.

D. Glosario breve
- Paciente: persona registrada para atención obstétrica.
- Control prenatal: visita programada para seguimiento del embarazo.
- Evento de parto: registro del parto y resultado perinatal.

Notas finales
- Esta documentación es plantilla inicial: completar con detalles reales (URLs, equipos, estructura exacta del código, contratos de API completos, diagramas ER y de arquitectura).
- Mantener docs en /docs y actualizar con cada cambio no retrocompatible.
