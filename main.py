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
from PIL import Image, ImageDraw, ImageFont
import re


# Crear matriz TSP de ejemplo (5 ciudades) - Ciudades A, B, C, D, E
EXAMPLE_MATRIX = np.array([
    [0,    14,   4,    10,   20],
    [14,   0,    7,    8,    12],
    [4,    5,    0,    16,   3],
    [11,   7,    16,   0,    2],
    [18,   10,   4,    2,    0]
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


def parse_dot_file(dot_file):
    """
    Parsea un archivo DOT para extraer nodos y edges.
    
    Args:
        dot_file: Ruta del archivo DOT
        
    Returns:
        Tupla (nodos_dict, edges_list)
    """
    with open(dot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    nodos_dict = {}
    edges_list = []
    
    # Extraer nodos: node_id [label="..."]
    node_pattern = r'(\d+)\s*\[label="([^"]+)"'
    for match in re.finditer(node_pattern, content):
        node_id = int(match.group(1))
        label = match.group(2)
        nodos_dict[node_id] = {'label': label, 'children': []}
    
    # Extraer edges: node1 -> node2
    edge_pattern = r'(\d+)\s*->\s*(\d+)'
    for match in re.finditer(edge_pattern, content):
        parent = int(match.group(1))
        child = int(match.group(2))
        edges_list.append((parent, child))
        if parent in nodos_dict:
            nodos_dict[parent]['children'].append(child)
    
    return nodos_dict, edges_list


def calculate_tree_layout(nodos_dict, root_id=0, x=0, y=0, offset=100):
    """
    Calcula las posiciones de los nodos en el árbol.
    
    Args:
        nodos_dict: Diccionario de nodos
        root_id: ID del nodo raíz
        x, y: Posición inicial
        offset: Espaciamiento entre niveles
        
    Returns:
        Diccionario con posiciones: {node_id: (x, y)}
    """
    positions = {}
    
    def calc_positions(node_id, x, y, spacing):
        positions[node_id] = (x, y)
        children = nodos_dict[node_id]['children']
        
        if children:
            child_spacing = spacing / 2
            total_width = spacing * len(children)
            start_x = x - total_width / 2
            
            for i, child_id in enumerate(children):
                child_x = start_x + i * spacing
                calc_positions(child_id, child_x, y + offset, child_spacing)
    
    calc_positions(root_id, x, y, 100)
    return positions


def draw_tree_image(dot_file, output_file):
    """
    Dibuja un árbol usando Pillow a partir de un archivo DOT.
    
    Args:
        dot_file: Ruta del archivo DOT
        output_file: Ruta de salida de la imagen PNG
    """
    try:
        nodos_dict, edges_list = parse_dot_file(dot_file)
        
        if not nodos_dict:
            return False
        
        # Calcular layout
        positions = calculate_tree_layout(nodos_dict, root_id=0)
        
        # Calcular dimensiones
        all_x = [pos[0] for pos in positions.values()]
        all_y = [pos[1] for pos in positions.values()]
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        # Crear imagen con margen
        margin = 40
        width = int(max_x - min_x + 2 * margin + 100)
        height = int(max_y - min_y + 2 * margin + 100)
        
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 10)
        except:
            font = ImageFont.load_default()
        
        # Dibujar edges
        for parent_id, child_id in edges_list:
            if parent_id in positions and child_id in positions:
                x1, y1 = positions[parent_id]
                x2, y2 = positions[child_id]
                
                # Ajustar coordenadas
                x1 = int(x1 - min_x + margin + 50)
                y1 = int(y1 - min_y + margin + 50)
                x2 = int(x2 - min_x + margin + 50)
                y2 = int(y2 - min_y + margin + 50)
                
                draw.line([(x1, y1), (x2, y2)], fill='gray', width=1)
        
        # Dibujar nodos
        node_radius = 15
        for node_id, (x, y) in positions.items():
            x = int(x - min_x + margin + 50)
            y = int(y - min_y + margin + 50)
            
            # Color según si fue podado
            label = nodos_dict[node_id]['label']
            color = 'lightcoral' if 'Pruned' in label else 'lightblue'
            
            # Dibujar círculo
            draw.ellipse(
                [x - node_radius, y - node_radius, x + node_radius, y + node_radius],
                fill=color,
                outline='black',
                width=1
            )
            
            # Escribir ID
            text = str(node_id)
            draw.text((x - 5, y - 5), text, fill='black', font=font)
        
        img.save(output_file)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_images():
    """Genera imágenes PNG desde archivos DOT usando Pillow."""
    graphs_dir = Path("graphs")
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*60}")
    print("Generando imágenes PNG desde archivos DOT...")
    print(f"{'='*60}\n")
    
    for dot_file in graphs_dir.glob("*.dot"):
        output_file = images_dir / f"{dot_file.stem}.png"
        if draw_tree_image(str(dot_file), str(output_file)):
            print(f"✓ {dot_file.stem}.png")
        else:
            print(f"⚠ Error generando {dot_file.stem}.png")


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
