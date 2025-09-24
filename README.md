# 🧮 Solucionador Avanzado de Integrales - Versión Modular

## 📁 Estructura del Proyecto

El proyecto ha sido reorganizado en una arquitectura modular con clases especializadas:

### 🏗️ Arquitectura Modular

```
proyecto_integrales/
├── run_app.py              # Archivo principal ejecutable
├── main_app.py             # Controlador principal (MainApp)
├── math_solver.py          # Lógica matemática (MathSolver)
├── ui_manager.py           # Interfaz de usuario (UIManager)
├── step_renderer.py        # Renderización de pasos (StepRenderer)
├── graph_manager.py        # Manejo de gráficos (GraphManager)
├── calculadoraint.py       # Archivo original (mantenido para referencia)
└── README.md               # Este archivo
```

### 🔧 Clases y Responsabilidades

#### 1. **MainApp** (`main_app.py`)
- **Rol**: Controlador principal que coordina todas las funcionalidades
- **Responsabilidades**:
  - Inicializar todos los componentes
  - Coordinar la comunicación entre clases
  - Manejar el flujo principal de la aplicación
  - Delegar operaciones a las clases especializadas

#### 2. **MathSolver** (`math_solver.py`)
- **Rol**: Motor matemático para resolver integrales
- **Responsabilidades**:
  - Resolver integrales paso a paso
  - Identificar tipos de funciones
  - Aplicar métodos específicos (sustitución trigonométrica, integración por partes, etc.)
  - Generar pasos detallados con explicaciones matemáticas

#### 3. **UIManager** (`ui_manager.py`)
- **Rol**: Gestor de la interfaz de usuario
- **Responsabilidades**:
  - Crear y manejar todos los widgets de la interfaz
  - Gestionar eventos de usuario
  - Mantener el estado de la interfaz
  - Delegar acciones a MainApp

#### 4. **StepRenderer** (`step_renderer.py`)
- **Rol**: Renderizador de pasos matemáticos con LaTeX
- **Responsabilidades**:
  - Convertir fórmulas LaTeX a imágenes
  - Mostrar pasos paso a paso
  - Manejar scrollbars y navegación
  - Cachear imágenes LaTeX para mejor rendimiento

#### 5. **GraphManager** (`graph_manager.py`)
- **Rol**: Gestor de gráficos matemáticos
- **Responsabilidades**:
  - Crear gráficos de funciones e integrales
  - Manejar matplotlib y tkinter
  - Gestionar el ciclo de vida de los gráficos

## 🚀 Cómo Ejecutar

### Opción 1: Archivo Principal
```bash
cd proyecto_integrales
python run_app.py
```

### Opción 2: Directamente desde MainApp
```bash
cd proyecto_integrales
python main_app.py
```

## 🔄 Flujo de la Aplicación

1. **Inicialización**: `MainApp` crea todas las clases especializadas
2. **Interfaz**: `UIManager` crea la interfaz de usuario
3. **Entrada**: Usuario ingresa función a integrar
4. **Resolución**: `MainApp` delega a `MathSolver` para resolver
5. **Renderizado**: `StepRenderer` muestra los pasos con LaTeX
6. **Gráficos**: `GraphManager` crea gráficos si se solicita
7. **Exportación**: `MainApp` maneja la exportación de resultados

## ✨ Ventajas de la Nueva Arquitectura

### 🎯 **Separación de Responsabilidades**
- Cada clase tiene una responsabilidad específica
- Código más fácil de mantener y debuggear
- Mejor organización del código

### 🔧 **Mantenibilidad**
- Cambios en una clase no afectan otras
- Fácil agregar nuevas funcionalidades
- Código más legible y documentado

### 🚀 **Escalabilidad**
- Fácil agregar nuevos tipos de solvers matemáticos
- Posibilidad de crear diferentes interfaces
- Soporte para múltiples formatos de salida

### 🧪 **Testabilidad**
- Cada clase puede ser probada independientemente
- Mocking más fácil para pruebas unitarias
- Mejor cobertura de pruebas

## 🔧 Funcionalidades Mantenidas

- ✅ Resolución paso a paso de integrales
- ✅ Renderización LaTeX de fórmulas matemáticas
- ✅ Scrollbars horizontales y verticales funcionales
- ✅ Gráficos de funciones e integrales
- ✅ Exportación de soluciones
- ✅ Interfaz profesional estilo Wolfram Alpha
- ✅ Soporte para integrales definidas e indefinidas
- ✅ Biblioteca de funciones matemáticas

## 🆕 Mejoras Implementadas

- 🏗️ **Arquitectura modular** con clases especializadas
- 📁 **Mejor organización** del código
- 🔄 **Separación clara** de responsabilidades
- 🧪 **Mayor testabilidad** del código
- 📚 **Mejor documentación** y comentarios
- 🚀 **Facilidad de mantenimiento** y extensión

## 🔮 Posibles Extensiones Futuras

- 📊 Nuevos tipos de gráficos (3D, contornos)
- 🌐 Interfaz web usando Flask/Django
- 📱 Aplicación móvil
- 🤖 Integración con IA para sugerencias
- 📚 Base de datos de problemas resueltos
- 👥 Modo colaborativo multiusuario
