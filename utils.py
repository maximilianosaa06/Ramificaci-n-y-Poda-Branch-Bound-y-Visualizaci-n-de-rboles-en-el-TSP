"""
Módulo de funciones auxiliares para el proyecto TSP Branch & Bound.
"""

import json
import numpy as np
from pathlib import Path


def export_to_json(root_node, filename):
    """
    Exporta el árbol de búsqueda a formato JSON.
    
    Args:
        root_node: Nodo raíz del árbol
        filename: Nombre del archivo de salida
    """
    tree_dict = root_node.to_dict()
    with open(filename, 'w') as f:
        json.dump(tree_dict, f, indent=2)
    print(f"Árbol exportado a {filename}")


def generate_dot_file(root_node, filename):
    """
    Genera un archivo Graphviz DOT del árbol de búsqueda.
    
    Args:
        root_node: Nodo raíz del árbol
        filename: Nombre del archivo .dot
    """
    with open(filename, 'w') as f:
        f.write("digraph TSPTree {\n")
        f.write("    node [shape=box, style=filled];\n")
        
        nodes_visited = set()
        queue = [root_node]
        
        while queue:
            node = queue.pop(0)
            if node.node_id in nodes_visited:
                continue
            
            nodes_visited.add(node.node_id)
            
            # Colorear nodos según estado
            if node.pruned:
                color = "red"
            elif node.is_solution:
                color = "green"
            else:
                color = "lightblue"
            
            label = f"N{node.node_id}\nC:{node.cost:.1f}\nB:{node.bound:.1f}"
            f.write(f'    {node.node_id} [label="{label}", fillcolor={color}];\n')
            
            for child in node.children:
                f.write(f"    {node.node_id} -> {child.node_id};\n")
                queue.append(child)
        
        f.write("}\n")
    print(f"Archivo DOT generado: {filename}")


def print_matrix(matrix, title="Matriz"):
    """
    Imprime una matriz de forma legible.
    
    Args:
        matrix: Matriz numpy a imprimir
        title: Título de la matriz
    """
    print(f"\n{title}:")
    print(matrix)


def reduce_matrix(matrix):
    """
    Reduce una matriz restando mínimos de filas y columnas.
    
    Args:
        matrix: Matriz de costos
        
    Returns:
        Tupla (matriz_reducida, costo_reducción)
    """
    mat = matrix.astype(float)
    reduction_cost = 0
    n = len(mat)
    
    # Reducir filas
    for i in range(n):
        min_val = np.min(mat[i])
        if min_val != np.inf:
            mat[i] -= min_val
            reduction_cost += min_val
    
    # Reducir columnas
    for j in range(n):
        min_val = np.min(mat[:, j])
        if min_val != np.inf:
            mat[:, j] -= min_val
            reduction_cost += min_val
    
    return mat, reduction_cost


def load_tsp_matrix(filepath):
    """
    Carga una matriz TSP desde un archivo.
    
    Args:
        filepath: Ruta al archivo con la matriz
        
    Returns:
        Matriz numpy con los costos
    """
    if filepath.endswith('.json'):
        with open(filepath, 'r') as f:
            data = json.load(f)
            return np.array(data, dtype=float)
    else:
        return np.loadtxt(filepath, dtype=float)


def save_tsp_matrix(matrix, filepath):
    """
    Guarda una matriz TSP en un archivo JSON.
    
    Args:
        matrix: Matriz a guardar
        filepath: Ruta del archivo de salida
    """
    with open(filepath, 'w') as f:
        json.dump(matrix.tolist(), f, indent=2)
