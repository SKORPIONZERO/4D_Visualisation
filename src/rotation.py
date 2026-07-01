"""
rotation.py


"""
import numpy as np
import math
import config

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

def _create_rotation_matrix(plane: str, theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    matrix = np.identity(4)
    axis1, axis2 = config.AXES[plane[0]], config.AXES[plane[1]]
    matrix[axis1, axis1] = c
    matrix[axis1, axis2] = -s
    matrix[axis2, axis1] = s
    matrix[axis2, axis2] = c
    return matrix

def compose_rotation_matrices(angles: dict, order: dict=config.PLANES) -> np.ndarray:
    """Composes rotation matrices for multiple planes and angles, applying
    them in the specified order, so that the vertices vector can be just
    multiplied by the resulting matrix to get the final rotated vertices."""
    composed_matrix = np.identity(4)
    for plane, angle in zip(order, angles.values()):
        composed_matrix = _create_rotation_matrix(plane, angle) @ composed_matrix
    return composed_matrix
