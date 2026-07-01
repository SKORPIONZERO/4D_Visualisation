"""
polytopes.py

Defines the Polytope base class and its subclasses for 
specific 4D polytopes (e.g. Tesseract and 16-cell).
"""
import math
import numpy as np
from abc import ABC, abstractmethod

class Polytope(ABC):
    def __init__(self, unit_distance=1.0):
        self.unit_distance = unit_distance
        self.original_vertices = self._generate_vertices()
        self.vertices = self.original_vertices.copy()
        self.edges = self._generate_edges()
        self.bound = self._calculate_bound()

    @abstractmethod
    def _generate_vertices(self):
        """Generate the vertices of the polytope."""
        pass
    
    @abstractmethod
    def _generate_edges(self):
        """Generate the edges of the polytope."""
        pass
    
    @abstractmethod
    def _calculate_bound(self):
        """Calculate the bound (max distance from origin) of the polytope."""
        pass
    
class Tesseract(Polytope):
    def _generate_vertices(self):
        """Generate the vertices of a tesseract."""
        vertices = []
        for x in [-self.unit_distance, self.unit_distance]:
            for y in [-self.unit_distance, self.unit_distance]:
                for z in [-self.unit_distance, self.unit_distance]:
                    for w in [-self.unit_distance, self.unit_distance]:
                        vertices.append([x, y, z, w])
        return np.array(vertices)

    def _generate_edges(self):
        """Generate the edges of a tesseract."""
        edges = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                differences = 0
                for axis in range(4):
                    if self.vertices[i][axis] != self.vertices[j][axis]:
                        differences += 1
                if differences == 1:
                    edges.append((i, j))
        return edges

    def _calculate_bound(self):
        """Calculate the bound (max distance from origin) of the tesseract."""
        return math.sqrt(4) * self.unit_distance

class Cell16(Polytope):
    def _generate_vertices(self):
        """Generate the vertices of a 16-cell."""
        vertices = []
        for axis in range(4):
            for sign in [-self.unit_distance, self.unit_distance]:
                vertex = [0, 0, 0, 0]
                vertex[axis] = sign
                vertices.append(vertex)
        return np.array(vertices)

    def _generate_edges(self):
        """Generate the edges of a 16-cell."""
        edges = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                if self.vertices[i] != [-l for l in self.vertices[j]]:                
                    edges.append((i, j))
        return edges

    def _calculate_bound(self):
        """Calculate the bound (max distance from origin) of the 16-cell."""
        return self.unit_distance
