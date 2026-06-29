"""
rotation.py


"""
import numpy as np
import math
import config

def create_rotation_matrix(plane, theta):
    c, s = math.cos(theta), math.sin(theta)
    matrix = np.identity(4)
    axis1, axis2 = config.AXES[plane[0]], config.AXES[plane[1]]
    matrix[axis1, axis1] = c
    matrix[axis1, axis2] = -s
    matrix[axis2, axis1] = s
    matrix[axis2, axis2] = c
    return matrix

def compose_rotation_matrices(angles, order=config.PLANES):
    """Composes rotation matrices for multiple planes and angles, applying
    them in the specified order, so that the vertices vector can be just
    multiplied by the resulting matrix to get the final rotated vertices."""
    composed_matrix = np.identity(4)
    for plane, angle in zip(order, angles):
        rotation_matrix = create_rotation_matrix(plane, angle)
        composed_matrix = rotation_matrix @ composed_matrix
    return composed_matrix