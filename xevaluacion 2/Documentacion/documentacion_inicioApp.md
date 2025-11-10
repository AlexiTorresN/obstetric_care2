# Documentación - InicioApp

## Descripción General
`InicioApp` es el componente principal de inicio de la aplicación de cuidado obstétrico que gestiona la pantalla de inicio y navegación inicial.

## Arquitectura del Componente

```mermaid
graph TD
    A[InicioApp] --> B[Estado de Autenticación]
    A --> C[Interfaz de Usuario]
    A --> D[Navegación]
    
    B --> E[Usuario Logueado]
    B --> F[Usuario No Logueado]
    
    C --> G[Pantalla de Bienvenida]
    C --> H[Botones de Acción]
    C --> I[Logo/Branding]
    
    D --> J[Login Screen]
    D --> K[Register Screen]
    D --> L[Main Dashboard]
```

## Estructura del Componente

### Props
| Prop | Tipo | Descripción | Requerido |
|------|------|-------------|-----------|
| navigation | NavigationProp | Objeto de navegación de React Navigation | Sí |
| route | RouteProp | Información de la ruta actual | No |

### Estado Local
```typescript
interface InicioAppState {
  isLoading: boolean;
  userAuthenticated: boolean;
  showSplash: boolean;
}
```

## Flujo de Navegación

```mermaid
flowchart LR
    A[App Launch] --> B{Usuario Autenticado?}
    B -->|Sí| C[Dashboard Principal]
    B -->|No| D[Pantalla de Inicio]
    D --> E[Botón Login]
    D --> F[Botón Registro]
    E --> G[Pantalla Login]
    F --> H[Pantalla Registro]
    G --> I{Login Exitoso?}
    H --> J{Registro Exitoso?}
    I -->|Sí| C
    I -->|No| G
    J -->|Sí| C
    J -->|No| H
```

## Funcionalidades Principales

### 1. Verificación de Autenticación
- Verifica si el usuario tiene sesión activa
- Redirige automáticamente al dashboard si está autenticado

### 2. Pantalla de Bienvenida
- Muestra información de la aplicación
- Presenta opciones de login y registro
- Incluye branding y elementos visuales

### 3. Navegación
- Maneja la transición entre pantallas
- Gestiona el stack de navegación inicial

## Implementación Técnica

### Hooks Utilizados
- `useState` - Manejo del estado local
- `useEffect` - Verificación inicial de autenticación
- `useNavigation` - Navegación entre pantallas

### Servicios Integrados
- AuthService - Verificación de autenticación
- StorageService - Persistencia de datos de usuario
- NavigationService - Gestión de rutas

## Diagrama de Secuencia

```mermaid
sequenceDiagram
    participant U as Usuario
    participant IA as InicioApp
    participant AS as AuthService
    participant NS as NavigationService
    
    U->>IA: Abre aplicación
    IA->>AS: Verificar autenticación
    AS-->>IA: Estado de usuario
    
    alt Usuario autenticado
        IA->>NS: Navegar a Dashboard
    else Usuario no autenticado
        IA->>U: Mostrar pantalla inicial
        U->>IA: Selecciona Login/Registro
        IA->>NS: Navegar a pantalla seleccionada
    end
```

## Estilos y UI

### Elementos Visuales
- Logo de la aplicación
- Colores del tema hospitalario
- Tipografía legible y accesible
- Botones con estados hover/pressed

### Responsive Design
- Adaptable a diferentes tamaños de pantalla
- Orientación portrait y landscape
- Accesibilidad mejorada

## Testing

### Casos de Prueba
1. **Carga inicial**: Verificar renderizado correcto
2. **Usuario autenticado**: Redirección automática
3. **Usuario no autenticado**: Mostrar opciones
4. **Navegación**: Transiciones correctas
5. **Estados de carga**: Indicadores visuales

## Dependencias
- React Navigation
- AsyncStorage
- React Native Elements/UI Library
- Authentication Context

## Notas de Desarrollo
- Implementar splash screen para mejor UX
- Considerar animaciones de transición
- Manejo de errores de red
- Logs para debugging en desarrollo