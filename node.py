"""
Módulo que define la estructura de un nodo en el árbol de búsqueda del TSP.
"""


class Node:
    """Representa un nodo en el árbol de búsqueda del algoritmo Branch & Bound."""
    
    def __init__(self, node_id, path, cost, bound, parent=None):
        """
        Inicializa un nodo.
        
        Args:
            node_id: Identificador único del nodo
            path: Lista del camino parcial recorrido
            cost: Costo actual del camino
            bound: Cota inferior (lower bound) calculada
            parent: Nodo padre en el árbol
        """
        self.node_id = node_id
        self.path = path.copy() if path else []
        self.cost = cost
        self.bound = bound
        self.parent = parent
        self.children = []
        self.pruned = False
        self.is_leaf = False
        self.is_solution = False
    
    def add_child(self, child):
        """Agrega un nodo hijo."""
        self.children.append(child)
    
    def to_dict(self):
        """Convierte el nodo a diccionario para serialización JSON."""
        return {
            'id': self.node_id,
            'path': self.path,
            'cost': round(self.cost, 2),
            'bound': round(self.bound, 2),
            'pruned': self.pruned,
            'is_solution': self.is_solution,
            'children': [child.to_dict() for child in self.children]
        }
    
    def __repr__(self):
        return f"Node(id={self.node_id}, path={self.path}, cost={self.cost:.2f}, bound={self.bound:.2f})"
