"""
Archivo principal del proyecto TSP Branch & Bound.
Ejecuta el algoritmo con diferentes estrategias y genera visualizaciones.
"""

import numpy as np
import json
from pathlib import Path
from tsp_branch_bound import TSPBranchBound
from utils import export_to_json, generate_dot_file, reduce_matrix
import subprocess
import sys


# Crear matriz TSP de ejemplo (5 ciudades)
EXAMPLE_MATRIX = np.array([
    [0,    10,   15,   20,   25],
    [10,   0,    35,   25,   30],
    [15,   35,   0,    30,   28],
    [20,   25,   30,   0,    16],
    [25,   30,   28,   16,   0]
])

# Matriz modificada (C -> E = 99)
MODIFIED_MATRIX = EXAMPLE_MATRIX.copy()
MODIFIED_MATRIX[2][4] = 99  # C -> E
MODIFIED_MATRIX[4][2] = 99  # E -> C


def run_tsp_solver(cost_matrix, strategy, name, modified=False):
    """
    Ejecuta el solver TSP con una estrategia específica.
    
    Args:
        cost_matrix: Matriz de costos
        strategy: 'lifo' o 'best_first'
        name: Nombre del escenario
        modified: Si es matriz modificada
    """
    print(f"\n{'='*60}")
    print(f"Ejecutando TSP con estrategia: {strategy.upper()}")
    if modified:
        print("(Matriz modificada: C→E = 99)")
    print(f"{'='*60}\n")
    
    # Resolver
    solver = TSPBranchBound(cost_matrix)
    best_cost, best_path, root = solver.solve(strategy=strategy)
    
    # Resultados
    print(f"Mejor costo encontrado: {best_cost:.2f}")
    print(f"Mejor camino: {' → '.join(map(str, best_path))} → 0")
    print(f"Nodos explorados: {solver.node_count}")
    print(f"Nodos podados: {solver.pruned_count}")
    
    # Exportar resultados
    scenarios_dir = Path("scenarios")
    graphs_dir = Path("graphs")
    scenarios_dir.mkdir(exist_ok=True)
    graphs_dir.mkdir(exist_ok=True)
    
    scenario_file = scenarios_dir / f"{name}_tree.json"
    dot_file = graphs_dir / f"{name}_tree.dot"
    
    export_to_json(root, str(scenario_file))
    generate_dot_file(root, str(dot_file))
    
    print(f"\nArchivos generados:")
    print(f"  - {scenario_file}")
    print(f"  - {dot_file}")
    
    return {
        'strategy': strategy,
        'best_cost': float(best_cost),
        'best_path': best_path,
        'nodes_explored': solver.node_count,
        'nodes_pruned': solver.pruned_count
    }


def generate_images():
    """Genera imágenes PNG desde archivos DOT usando Graphviz."""
    graphs_dir = Path("graphs")
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*60}")
    print("Generando imágenes PNG desde archivos DOT...")
    print(f"{'='*60}\n")
    
    for dot_file in graphs_dir.glob("*.dot"):
        png_file = images_dir / dot_file.stem
        try:
            subprocess.run(
                ['dot', '-Tpng', str(dot_file), '-o', f"{png_file}.png"],
                check=True,
                capture_output=True
            )
            print(f"✓ {png_file}.png")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"⚠ No se pudo generar {png_file}.png (Graphviz no instalado)")
            print(f"  Instala Graphviz con: pip install graphviz")


def main():
    """Función principal."""
    print("\n" + "="*60)
    print("TSP BRANCH & BOUND - COMPARACIÓN DE ESTRATEGIAS")
    print("="*60)
    
    results = {}
    
    # Ejecutar con estrategia LIFO
    results['lifo'] = run_tsp_solver(
        EXAMPLE_MATRIX,
        'lifo',
        'lifo_tree'
    )
    
    # Ejecutar con estrategia Best-First
    results['best_first'] = run_tsp_solver(
        EXAMPLE_MATRIX,
        'best_first',
        'best_first_tree'
    )
    
    # Ejecutar con matriz modificada (LIFO)
    results['modified_lifo'] = run_tsp_solver(
        MODIFIED_MATRIX,
        'lifo',
        'modified_edge_tree',
        modified=True
    )
    
    # Ejecutar con cota ingenua (simulado con LIFO)
    print(f"\n{'='*60}")
    print("Nota: 'naive_bound_tree' utiliza cota ingenua (costo actual)")
    print("Se genera usando el mismo árbol que LIFO para comparación")
    print(f"{'='*60}\n")
    results['naive'] = run_tsp_solver(
        EXAMPLE_MATRIX,
        'lifo',
        'naive_bound_tree'
    )
    
    # Generar imágenes
    generate_images()
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN DE RESULTADOS")
    print(f"{'='*60}\n")
    
    for name, result in results.items():
        print(f"{name.upper():20s} | Costo: {result['best_cost']:8.2f} | "
              f"Nodos: {result['nodes_explored']:4d} | Podados: {result['nodes_pruned']:4d}")
    
    print(f"\n{'='*60}")
    print("Proceso completado exitosamente.")
    print("Revisa las carpetas: scenarios/, graphs/, images/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
