# Algoritmo Genético para el Problema del Viajante (TSP)

Este proyecto implementa un algoritmo genético para resolver el clásico Problema del Viajante (Travelling Salesman Problem, TSP).  
El objetivo es encontrar la ruta más corta que visita todas las ciudades exactamente una vez y regresa al punto de origen.

El código está completamente modularizado y documentado, con una arquitectura limpia que facilita su comprensión, mantenimiento y ampliación.

---

## ¿Qué es el TSP?

El TSP (Travelling Salesman Problem) busca el camino más corto posible que permita visitar todas las ciudades de una lista y volver al inicio.  
Es un problema NP-hard ampliamente estudiado en optimización y algoritmos evolutivos.

---

## Requisitos e instalación

### Dependencias

El proyecto está implementado en **Python 3.8+**.  
Asegúrate de tener instaladas las siguientes bibliotecas:

```bash
pip install numpy pandas
```

```bash
tsp_ga/
│
├── models.py   # Define las clases municipio Aptitud (modelos base)
├── genetic_utils.py # Contiene las funciones auxiliares del algoritmo genético
├── tsp_ga.py  # Lógica principal del algoritmo genético (evolución)
└── main.py    # Punto de entrada del programa

```

## Descripción de los módulos

### 🔹 `models.py`
Contiene las **clases base** que representan los elementos principales del problema del viajante.

| Clase | Descripción |
|-------|--------------|
| **`municipio`** | Define una ciudad o punto en el mapa mediante sus coordenadas (x, y). Incluye métodos para calcular la distancia euclidiana entre municipios. |
| **`Aptitud`** | Evalúa una ruta completa calculando su distancia total y asignando un valor de “aptitud” (fitness), donde una menor distancia implica una mayor aptitud. |

---

### 🔹 `genetic_utils.py`
Incluye todas las **funciones auxiliares del algoritmo genético**, como la creación de rutas, la selección de individuos y la mutación.

| Función | Descripción |
|----------|-------------|
| **`crearRuta(poblacion)`** | Genera una ruta aleatoria a partir de la lista de municipios. |
| **`poblacionInicial(tamanoPoblacion, poblacion)`** | Crea la primera población de rutas posibles. |
| **`clasificacionRutas(poblacion)`** | Evalúa cada ruta según su aptitud y las ordena de mejor a peor. |
| **`seleccionRutas(rutasClasificadas, indivSeleccionados)`** | Selecciona las mejores rutas (elitismo) y aplica selección aleatoria ponderada por aptitud. |
| **`grupoApareamiento(poblacion, resultadosSeleccion)`** | Genera los grupos de padres que producirán la nueva generación. |
| **`reproduccion(padre1, padre2)`** | Crea un nuevo individuo combinando genes (ciudades) de dos padres mediante cruce parcial (crossover). |
| **`mutacion(individuo, razonMutacion)`** | Introduce pequeños cambios aleatorios en la ruta para evitar convergencia prematura. |
| **`mutacionPoblacion(poblacion, razonMutacion)`** | Aplica la función de mutación a toda la población de forma controlada. |

---

### 🔹 `tsp_ga.py`
Contiene el **núcleo del algoritmo genético**, responsable de la evolución de la población a lo largo de las generaciones.

| Función | Descripción |
|----------|-------------|
| **`nuevaGeneracion(actual, indivSeleccionados, razonMutacion)`** | Crea una nueva población aplicando selección, cruce y mutación. |
| **`algoritmoGenetico(poblacion, tamanoPoblacion, indivSeleccionados, razonMutacion, generaciones)`** | Ejecuta el ciclo completo del algoritmo genético: inicializa la población, la evalúa, la mejora generación tras generación y devuelve la mejor ruta final. |

---

### 🔹 `main.py`
Punto de entrada del proyecto. Integra todos los módulos y ejecuta el proceso completo.

| Elemento | Descripción |
|-----------|-------------|
| **Definición de municipios** | Lista de coordenadas que representan las ciudades del problema. |
| **Configuración de parámetros** | Ajusta el tamaño de la población, tasa de mutación, generaciones y cantidad de individuos seleccionados. |
| **Ejecución del algoritmo** | Llama a `algoritmoGenetico()` y obtiene la mejor ruta. |
