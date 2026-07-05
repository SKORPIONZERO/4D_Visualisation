"""
polytopes.py

Defines the Polytope base class and its subclasses for 
specific 4D polytopes (e.g. Tesseract and 16-cell).
"""
import math
import numpy as np
import itertools
from abc import ABC, abstractmethod

# Made using AI, for the 120-Cell.
def _even_permutations(seq):
    """Yield permutations of a 4-element sequence of pairwise-distinct
    values that are EVEN permutations of the original ordering."""
    for perm in itertools.permutations(range(len(seq))):
        inversions = sum(
            1 for i in range(len(perm)) for j in range(i + 1, len(perm))
            if perm[i] > perm[j]
        )
        if inversions % 2 == 0:
            yield tuple(seq[i] for i in perm)

class Polytope(ABC):
    def __init__(self, unit_distance=1.0) -> None:
        self.unit_distance = unit_distance
        self.vertices = self._generate_vertices()
        self.edges = self._generate_edges()
        self.bound = self._calculate_bound()

    @abstractmethod
    def _generate_vertices(self) -> np.ndarray:
        """Generate the vertices of the polytope."""
        pass
    
    @abstractmethod
    def _generate_edges(self) -> np.ndarray:
        """Generate the edges of the polytope."""
        pass
    
    @abstractmethod
    def _calculate_bound(self) -> float:
        """Calculate the bound (max distance from origin) of the polytope."""
        pass

class Pentachoron(Polytope):
    def _generate_vertices(self):
        # Made using AI, I still don't understand how it works, but it works.
        """Generate the vertices of a 5-cell by projecting the 5 standard
        basis vectors of R^5 onto the sum-zero (centroid-centred) hyperplane."""
        # Step 1: the 5 standard basis vectors of R^5 (rows of the identity)
        basis_vectors_5D = np.identity(5)

        # Step 2: centre them on their centroid, so each row now sums to zero
        centroid = np.mean(basis_vectors_5D, axis=0)
        centred_vectors = basis_vectors_5D - centroid  # shape (5, 5)

        # Step 3: get an orthonormal basis for the 4D hyperplane {x : sum(x) = 0}.
        # SVD of the "all ones" direction (1,1,1,1,1) returns 5 orthonormal
        # row vectors (Vt) ranked by how much they align with that direction.
        # The first row aligns with (1,1,1,1,1) itself; the other 4 rows are
        # automatically orthogonal to it (and to each other) - which means
        # they span exactly the hyperplane we want.
        _, _, Vt = np.linalg.svd(np.ones((1, 5)))
        hyperplane_basis = Vt[1:]  # shape (4, 5)

        # Step 4: project each centred 5D vector onto that basis -> 4D coords
        vertices = []
        for row in centred_vectors:
            vertex_4D = hyperplane_basis @ row
            norm = np.linalg.norm(vertex_4D)
            vertex_4D = vertex_4D / norm * self.unit_distance  # normalise
            vertices.append(vertex_4D)

        return np.array(vertices)

    def _generate_edges(self) -> np.ndarray:
        """Generate the edges of a 5-Cell."""
        edges = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                edges.append((i, j))
        return np.array(edges)

    def _calculate_bound(self) -> float:
        """Calculate the bound (max distance from origin) of the 5-Cell."""
        return math.sqrt(2) * self.unit_distance

class Tesseract(Polytope):
    def _generate_vertices(self) -> np.ndarray:
        """Generate the vertices of a tesseract(8-Cell)."""
        vertices = []
        for x in [-self.unit_distance, self.unit_distance]:
            for y in [-self.unit_distance, self.unit_distance]:
                for z in [-self.unit_distance, self.unit_distance]:
                    for w in [-self.unit_distance, self.unit_distance]:
                        vertices.append([x, y, z, w])
        return np.array(vertices)

    def _generate_edges(self) -> np.ndarray:
        """Generate the edges of a tesseract(8-Cell)."""
        edges = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                differences = 0
                for axis in range(4):
                    if self.vertices[i][axis] != self.vertices[j][axis]:
                        differences += 1
                if differences == 1:
                    edges.append((i, j))
        return np.array(edges)

    def _calculate_bound(self) -> float:
        """Calculate the bound (max distance from origin) of the tesseract(8-Cell)."""
        return math.sqrt(4) * self.unit_distance

class Hexadecachoron(Polytope):
    def _generate_vertices(self) -> np.ndarray:
        """Generate the vertices of a 16-Cell."""
        vertices = []
        for axis in range(4):
            for sign in [-self.unit_distance, self.unit_distance]:
                vertex = [0, 0, 0, 0]
                vertex[axis] = sign
                vertices.append(vertex)
        return np.array(vertices)

    def _generate_edges(self) -> np.ndarray:
        """Generate the edges of a 16-Cell."""
        edges = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                if (self.vertices[i] != [-l for l in self.vertices[j]]).any():                
                    edges.append((i, j))
                pass
        return np.array(edges)

    def _calculate_bound(self) -> float:
        """Calculate the bound (max distance from origin) of the 16-Cell."""
        return self.unit_distance

class Icositetrachoron(Polytope):
    def _generate_vertices(self):
        """Generate the vertices of a 24-Cell."""
        vertices = []
        for axis1 in range(4):
            for axis2 in range(axis1 + 1, 4):
                for sign1 in [-self.unit_distance, self.unit_distance]:
                    for sign2 in [-self.unit_distance, self.unit_distance]:
                        vertex = [0, 0, 0, 0]
                        vertex[axis1] = sign1
                        vertex[axis2] = sign2
                        vertices.append(vertex)
        return np.array(vertices)

    def _generate_edges(self):
        """Generate the edges of a 24-Cell."""
        edges = []
        target = self.unit_distance ** 2
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                dot_product = np.dot(self.vertices[i], self.vertices[j])
                if dot_product == target:
                    edges.append((i, j))
        return np.array(edges)

    def _calculate_bound(self):
        """Calculate the bound (max distance from origin) of the 24-Cell."""
        return self.unit_distance * math.sqrt(2)

# The code for the 120-Cell is fully made using AI. At this point
# of my learning, I have no idea how, the maths behind this works,
# but it works. I will try to understand it in the future and redo it myself.
class Hecatonicosachoron(Polytope):
    def _generate_vertices(self):
        """Generate the 600 vertices of a 120-cell from the 7 standard
        H4 Coxeter-group orbits (see docstring table in accompanying notes)."""
        phi = (1 + math.sqrt(5)) / 2
        sqrt5 = math.sqrt(5)
        raw_vertices = set()

        def add_all_perms(base):
            for perm in itertools.permutations(base):
                raw_vertices.add(tuple(round(c, 9) for c in perm))

        def add_even_perms(base):
            for perm in _even_permutations(base):
                raw_vertices.add(tuple(round(c, 9) for c in perm))

        # Group 1: all permutations of (0, 0, ±2, ±2)
        for s1, s2 in itertools.product([1, -1], repeat=2):
            add_all_perms([0, 0, 2 * s1, 2 * s2])

        # Group 2: all permutations of (±1, ±1, ±1, ±sqrt(5))
        for signs in itertools.product([1, -1], repeat=4):
            add_all_perms([signs[0], signs[1], signs[2], signs[3] * sqrt5])

        # Group 3: all permutations of (±phi^-2, ±phi, ±phi, ±phi)
        for signs in itertools.product([1, -1], repeat=4):
            add_all_perms([signs[0] * phi**-2, signs[1] * phi,
                           signs[2] * phi, signs[3] * phi])

        # Group 4: all permutations of (±phi^-1, ±phi^-1, ±phi^-1, ±phi^2)
        for signs in itertools.product([1, -1], repeat=4):
            add_all_perms([signs[0] * phi**-1, signs[1] * phi**-1,
                           signs[2] * phi**-1, signs[3] * phi**2])

        # Group 5: even permutations of (0, ±phi^-2, ±1, ±phi^2)
        for signs in itertools.product([1, -1], repeat=3):
            add_even_perms([0, signs[0] * phi**-2, signs[1] * 1, signs[2] * phi**2])

        # Group 6: even permutations of (0, ±phi^-1, ±phi, ±sqrt(5))
        for signs in itertools.product([1, -1], repeat=3):
            add_even_perms([0, signs[0] * phi**-1, signs[1] * phi, signs[2] * sqrt5])

        # Group 7: even permutations of (±phi^-1, ±1, ±phi, ±2)
        for signs in itertools.product([1, -1], repeat=4):
            add_even_perms([signs[0] * phi**-1, signs[1] * 1,
                             signs[2] * phi, signs[3] * 2])

        vertices = np.array(sorted(raw_vertices))
        scale = self.unit_distance / math.sqrt(8)  # every raw vertex has norm sqrt(8)
        return vertices * scale

    def _generate_edges(self):
        """Connect every pair of vertices at the minimum pairwise distance
        (the 120-cell is edge-transitive with vertex degree 4)."""
        n = len(self.vertices)
        pair_dists = []
        for i in range(n):
            diffs = self.vertices[i + 1:] - self.vertices[i]
            dists = np.linalg.norm(diffs, axis=1)
            for offset, d in enumerate(dists):
                pair_dists.append((i, i + 1 + offset, d))

        min_dist = min(d for _, _, d in pair_dists)
        edges = [(i, j) for i, j, d in pair_dists if np.isclose(d, min_dist, rtol=1e-4)]
        return np.array(edges)

    def _calculate_bound(self):
        """All raw vertices have norm sqrt(8), scaled to unit_distance."""
        return self.unit_distance
