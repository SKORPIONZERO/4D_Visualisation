"""
rotation.py


"""
import numpy as np
import math

def define_rotation_matrices(theta):
    """Defines rotation matrices for all 6 coordinate planes in 4D (XY, XZ, XW, YZ, YW, ZW)."""
    c, s = math.cos(theta), math.sin(theta)
    Rxy = np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])
    Rxz = np.array([
        [c, 0, -s, 0],
        [0, 1,  0, 0],
        [s, 0,  c, 0],
        [0, 0,  0, 1]
    ])
    Rxw = np.array([
        [c, 0, 0, -s],
        [0, 1, 0,  0],
        [0, 0, 1,  0],
        [s, 0, 0,  c]
    ])
    Ryz = np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ])
    Ryw = np.array([
        [1, 0, 0,  0],
        [0, c, 0, -s],
        [0, 0, 1,  0],
        [0, s, 0,  c]
    ])
    Rzw = np.array([
        [1, 0, 0,  0],
        [0, 1, 0,  0],
        [0, 0, c, -s],
        [0, 0, s,  c]
    ])
    return Rxy, Rxz, Rxw, Ryz, Ryw, Rzw

def rotate_vertex(vertex, theta):
    """Rotates a single vertex in 4D space using the defined rotation matrices."""
    Rxy, Rxz, Rxw, Ryz, Ryw, Rzw = define_rotation_matrices(theta)
    rotated_vertex = Rxw @ Rxy @ Rxz @ Ryw @ Ryz @ Rzw @ vertex
    return rotated_vertex

def rotate_vertices(vertices, theta):
    """Rotates a list of vertices in 4D space using the defined rotation matrices."""
    Rxy, Rxz, Rxw, Ryz, Ryw, Rzw = define_rotation_matrices(theta)
    rotated_vertices = []
    for vertex in vertices:
        rotated_vertex = Rxw @ Rxy @ Rxz @ Ryw @ Ryz @ Rzw @ vertex
        rotated_vertices.append(rotated_vertex)
    return np.array(rotated_vertices)