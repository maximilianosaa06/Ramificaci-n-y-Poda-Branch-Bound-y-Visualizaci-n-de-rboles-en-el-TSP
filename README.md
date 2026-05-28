# TSP Branch & Bound - Visualización de Árboles de Búsqueda

## Descripción del Proyecto

Este proyecto implementa el algoritmo **Branch & Bound** para resolver el **Problema del Viajante (TSP - Traveling Salesman Problem)**, comparando distintas estrategias de exploración del espacio de búsqueda. El proyecto genera árboles de búsqueda visualizables en múltiples formatos (JSON, DOT, PNG).

### Características principales:

- ✅ **Algoritmo Branch & Bound** con poda inteligente
- ✅ **Dos estrategias de exploración**: LIFO (Depth-First) y Best-First
- ✅ **Exportación a JSON** para análisis de datos
- ✅ **Generación de gráficos DOT** para visualización
- ✅ **Renderizado de árboles a PNG** (requiere Graphviz)
- ✅ **Cálculo de cotas** mediante reducción de matrices
- ✅ **Análisis comparativo** de estrategias

---

## Estructura del Proyecto

```
tsp-branch-and-bound/
│
├── README.md                      # Este archivo
├── requirements.txt               # Dependencias de Python
├── main.py                        # Archivo principal (ejecutable)
├── tsp_branch_bound.py            # Implementación del algoritmo
├── node.py                        # Estructura de nodo del árbol
├── utils.py                       # Funciones auxiliares
│
├── scenarios/                     # Árboles generados en JSON
│   ├── lifo_tree.json
│   ├── best_first_tree.json
│   ├── naive_bound_tree.json
│   └── modified_edge_tree.json
│
├── graphs/                        # Representación Graphviz (DOT)
│   ├── lifo_tree.dot
│   ├── best_first_tree.dot
│   ├── naive_bound_tree.dot
│   └── modified_edge_tree.dot
│
├── images/                        # Imágenes PNG de los árboles
│   ├── lifo_tree.png
│   ├── best_first_tree.png
│   ├── naive_bound_tree.png
│   └── modified_edge_tree.png
│
└── report/                        # Informe del laboratorio
    └── informe.pdf
```

---

## Instalación

### Requisitos previos:

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación:

1. **Clonar o descargar el repositorio:**
   ```bash
   git clone https://github.com/usuario/tsp-branch-and-bound.git
   cd tsp-branch-and-bound
   ```

2. **Crear un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar Graphviz (opcional, para generar imágenes PNG):**
   - **Windows**: Descargar desde [graphviz.org](https://graphviz.org/download/)
   - **Ubuntu/Debian**: `sudo apt-get install graphviz`
   - **macOS**: `brew install graphviz`

---

## Uso

### Ejecutar el programa completo:

```bash
python main.py
```

Esto generará:
- 4 archivos JSON con los árboles de búsqueda
- 4 archivos DOT para visualización
- 4 imágenes PNG (si Graphviz está instalado)
- Un resumen comparativo en consola

### Ejemplo de salida:

```
============================================================
TSP BRANCH & BOUND - COMPARACIÓN DE ESTRATEGIAS
============================================================

============================================================
Ejecutando TSP con estrategia: LIFO
============================================================

Mejor costo encontrado: 80.00
Mejor camino: 0 → 1 → 3 → 4 → 2 → 0
Nodos explorados: 24
Nodos podados: 8

[...]

============================================================
RESUMEN DE RESULTADOS
============================================================

LIFO                 | Costo:    80.00 | Nodos:   24 | Podados:    8
BEST_FIRST           | Costo:    80.00 | Nodos:   18 | Podados:   14
MODIFIED_LIFO        | Costo:   105.00 | Nodos:   24 | Podados:    8
NAIVE                | Costo:    80.00 | Nodos:   24 | Podados:    8

============================================================
```

---

## Descripción de Archivos

### `main.py`

Archivo principal que coordina la ejecución del programa:

- Carga la matriz de costos TSP
- Ejecuta el algoritmo con diferentes estrategias
- Genera JSON, DOT e imágenes
- Imprime comparativas de resultados

### `tsp_branch_bound.py`

Implementa el núcleo del algoritmo Branch & Bound:

- Clase `TSPBranchBound`: gestiona el proceso de búsqueda
- Método `solve()`: ejecuta el algoritmo completo
- Método `_expand_node()`: genera nodos hijos
- Método `_calculate_bound()`: calcula cotas inferiores
- Método `_get_reduced_matrix()`: obtiene submatrices reducidas

### `node.py`

Define la estructura de un nodo del árbol:

- `node_id`: identificador único
- `path`: camino parcial recorrido
- `cost`: costo actual
- `bound`: cota inferior calculada
- `children`: lista de nodos hijos
- `pruned`: indica si el nodo fue podado
- `is_solution`: indica si es solución completa

### `utils.py`

Funciones auxiliares:

- `export_to_json()`: exporta árbol a JSON
- `generate_dot_file()`: genera archivo Graphviz
- `reduce_matrix()`: reducción de matriz para cotas
- `load_tsp_matrix()`: carga matriz desde archivo
- `print_matrix()`: imprime matrices formateadas

---

## Carpetas de Salida

### `scenarios/`

Contiene los árboles de búsqueda en formato JSON:

- **lifo_tree.json**: Árbol usando estrategia LIFO (DFS)
- **best_first_tree.json**: Árbol usando Best-First (menor cota)
- **naive_bound_tree.json**: Árbol con cota ingenua
- **modified_edge_tree.json**: Árbol con matriz modificada (C→E=99)

### `graphs/`

Archivos Graphviz DOT para visualización:

- Los archivos `.dot` pueden visualizarse con herramientas como:
  - [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/)
  - Aplicación de escritorio Graphviz

### `images/`

Imágenes PNG de los árboles (requiere Graphviz instalado):

- **Colores**:
  - 🟦 Azul: nodos normales
  - 🟩 Verde: soluciones óptimas
  - 🟥 Rojo: nodos podados

### `report/`

Contiene el informe PDF del laboratorio con análisis detallado.

---

## Estrategias de Exploración

### LIFO (Depth-First Search)

```
Ventajas:
- Menor consumo de memoria
- Explora rápido hacia soluciones

Desventajas:
- Menos nodos podados
- Puede ser ineficiente en cotas débiles
```

### Best-First (Least-Cost)

```
Ventajas:
- Mayor cantidad de nodos podados
- Prioriza ramas prometedoras
- Generalmente explora menos nodos totales

Desventajas:
- Mayor consumo de memoria
- Necesita mantener toda la cola ordenada
```

---

## Algoritmo Branch & Bound

### Componentes principales:

1. **Función objetivo**: Costo total del camino
2. **Poda**: Elimina ramas con cota ≥ mejor solución actual
3. **Cota inferior**: Basada en reducción de matrices
4. **Exploración**: LIFO o Best-First

### Pseudocódigo:

```
1. Crear nodo raíz con cota inicial
2. Inicializar queue vacía
3. Mientras queue no esté vacía:
   a. Seleccionar nodo según estrategia
   b. Si cota ≥ mejor_solución actual, podar
   c. Expandir nodo generando hijos
   d. Para cada hijo:
      - Si es solución completa, actualizar mejor
      - Si no, agregar a queue si no está podado
4. Retornar mejor_solución
```

---

## Dependencias

| Librería | Versión | Uso |
|----------|---------|-----|
| numpy | 1.24.3 | Operaciones matriciales |
| graphviz | 0.20.1 | Generación de gráficos DOT |
| matplotlib | 3.7.1 | Visualización (preparado para futuro) |
| networkx | 3.1 | Análisis de grafos (preparado para futuro) |

---

## Mejoras Futuras

- [ ] Interfaz gráfica con visualización interactiva
- [ ] Soporte para matrices TSP asimétricas
- [ ] Algoritmos adicionales (A*, Held-Karp)
- [ ] Análisis de complejidad temporal
- [ ] Generador de instancias TSP aleatorias
- [ ] Benchmarking contra TSPLIB

---

## Autor

Proyecto desarrollado como parte de un laboratorio académico en algoritmos avanzados.

---

## Licencia

Este proyecto se proporciona bajo licencia MIT. Ver archivo LICENSE para más detalles.

---

## Notas

- El proyecto está diseñado para instancias pequeñas de TSP (n < 15)
- Para instancias mayores, considerar paralelización o algoritmos aproximados
- Los tiempos de ejecución se muestran en segundos

---

**Última actualización**: Mayo 2026
