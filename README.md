# ⚽ FundaDT

**FundaDT** es un sistema de gestión de equipos de fútbol, mercado de pases, armado de tácticas/alineaciones y simulación de fechas, desarrollado en **Python** como parte de los Trabajos Prácticos de la materia *Fundamentos de Programación* (FIUBA).

El proyecto está estructurado de manera modular aplicando buenas prácticas de programación, manejo de estructuras de datos, validaciones robustas y procesamiento de archivos CSV (tanto en crudo como datos procesados).

---

## 📂 Estructura del Proyecto

El código fuente se encuentra organizado en módulos especializados para separar la lógica de negocio, la interfaz de usuario y las validaciones:

* **`funda_dt_user.py`**: Módulo principal de la aplicación para el usuario (menú interactivo general, importación de datos y simulación de fechas).
* **`funda_dt_parser.py`**: Procesador y parser de archivos CSV crudos (conversión de estadísticas, cálculo de puntajes generales y precios base de jugadores).
* **`equipos.py`**: Lógica de negocio y gestión para la creación de nuevos equipos.
* **`mercado.py`**: Manejo del mercado de pases (búsqueda paginada de jugadores, compra por posiciones, venta y actualización de presupuestos).
* **`alineaciones.py`**: Gestión táctica (validación de formaciones por posiciones, selección de titulares, suplentes y capitán).
* **`consultas.py`**: Módulo de visualización de planteles, esquemas tácticos actuales y estadísticas de jugadores más utilizados.
* **`constantes.py`**: Definición centralizada de mensajes, textos de plantillas, errores globales y puntajes de eventos.
* **`validaciones.py`**: Funciones auxiliares para verificar la integridad de inputs, existencia de archivos CSV, headers y reglas de negocio.

---

## ⚙️ Requisitos y Ejecución

Para ejecutar el programa, necesitás tener instalado **Python 3** en tu computadora. No requiere librerías externas adicionales.

### 1. Ejecutar el menú principal del usuario
Abrí tu terminal en la carpeta del proyecto y ejecutá:

```bash
python funda_dt_user.py
