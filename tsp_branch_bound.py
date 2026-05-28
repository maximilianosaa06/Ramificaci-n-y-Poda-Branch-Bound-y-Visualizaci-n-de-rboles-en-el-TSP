"""
Implementación del algoritmo Branch & Bound para resolver el Problema del Viajante (TSP).
"""

import numpy as np
from node import Node
from utils import reduce_matrix
from collections import deque


class TSPBranchBound:
    """Implementa el algoritmo Branch & Bound para TSP."""
    
    def __init__(self, cost_matrix):
        """
        Inicializa el solver.
        
        Args:
            cost_matrix: Matriz de costos del TSP
        """
        self.cost_matrix = cost_matrix.astype(float)
        self.n = len(cost_matrix)
        self.best_cost = float('inf')
        self.best_path = None
        self.node_count = 0
        self.pruned_count = 0
        self.root = None
        self.all_nodes = []
    
    def solve(self, strategy='lifo'):
        """
        Resuelve el TSP usando Branch & Bound.
        
        Args:
            strategy: 'lifo' para DFS o 'best_first' para mejor primero
            
        Returns:
            Tupla (mejor_costo, mejor_camino, árbol_nodos)
        """
        # Crear nodo raíz
        reduced_matrix, bound = reduce_matrix(self.cost_matrix)
        self.root = Node(
            node_id=self.node_count,
            path=[0],
            cost=0,
            bound=bound
        )
        self.node_count += 1
        self.all_nodes.append(self.root)
        
        # Inicializar cola según estrategia
        if strategy == 'lifo':
            queue = [self.root]  # Pila
            get_next = lambda q: q.pop()  # LIFO
        else:  # best_first
            queue = [self.root]
            get_next = lambda q: min(q, key=lambda x: x.bound) if q else None
        
        # Branch & Bound principal
        while queue:
            current = get_next(queue)
            if current is None:
                break
            
            # Poda por cota
            if current.bound >= self.best_cost:
                current.pruned = True
                self.pruned_count += 1
                continue
            
            # Expandir nodo
            expanded = self._expand_node(current)
            
            # Procesar nodos expandidos
            for child in expanded:
                if child.is_solution:
                    # Actualizar mejor solución
                    if child.cost < self.best_cost:
                        self.best_cost = child.cost
                        self.best_path = child.path.copy()
                else:
                    # Agregar a la cola si no está podado
                    if child.bound < self.best_cost:
                        queue.append(child)
                    else:
                        child.pruned = True
                        self.pruned_count += 1
        
        return self.best_cost, self.best_path, self.root
    
    def _expand_node(self, node):
        """
        Expande un nodo generando nodos hijos.
        
        Args:
            node: Nodo a expandir
            
        Returns:
            Lista de nodos hijos
        """
        children = []
        last_city = node.path[-1]
        
        for next_city in range(self.n):
            # No visitar ciudades ya en el camino
            if next_city in node.path:
                continue
            
            # Crear nuevo camino
            new_path = node.path + [next_city]
            edge_cost = self.cost_matrix[last_city][next_city]
            new_cost = node.cost + edge_cost
            
            # Crear nodo hijo
            child = Node(
                node_id=self.node_count,
                path=new_path,
                cost=new_cost,
                bound=new_cost,
                parent=node
            )
            self.node_count += 1
            self.all_nodes.append(child)
            node.add_child(child)
            
            # Verificar si es solución completa
            if len(new_path) == self.n:
                # Agregar costo de retorno a ciudad inicial
                return_cost = self.cost_matrix[next_city][0]
                child.cost = new_cost + return_cost
                child.bound = child.cost
                child.is_solution = True
            else:
                # Calcular cota
                child.bound = self._calculate_bound(child)
            
            children.append(child)
        
        return children
    
    def _calculate_bound(self, node):
        """
        Calcula la cota inferior para un nodo.
        
        Args:
            node: Nodo para el cual calcular la cota
            
        Returns:
            Valor de la cota
        """
        # Cota simple: costo actual + mínimo para completar
        bound = node.cost
        
        # Reducir matriz parcial
        reduced, reduction = reduce_matrix(self._get_reduced_matrix(node.path))
        bound += reduction
        
        return bound
    
    def _get_reduced_matrix(self, path):
        """
        Obtiene la matriz reducida para un camino parcial.
        
        Args:
            path: Camino parcial
            
        Returns:
            Matriz reducida para ciudades no visitadas
        """
        visited = set(path)
        unvisited = [i for i in range(self.n) if i not in visited]
        
        # Crear matriz para ciudades no visitadas
        submatrix = np.full((len(unvisited), len(unvisited)), np.inf)
        
        for i, u in enumerate(unvisited):
            for j, v in enumerate(unvisited):
                if u != v:
                    submatrix[i][j] = self.cost_matrix[u][v]
        
        return submatrix
