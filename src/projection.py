"""
projection.py

"""
import numpy as np

def project_4D_to_3D(vertex: np.ndarray, distance_4D: float) -> np.ndarray:
    x, y, z, w = vertex
    factor_4d = distance_4D/(distance_4D-w)
    x, y, z = x * factor_4d, y * factor_4d, z * factor_4d
    return np.array([x, y, z]), w

def project_3D_to_2D(vertex, distance_3D: float):
    x, y, z = vertex
    factor_3d = distance_3D/(distance_3D-z)
    x, y = x * factor_3d, y * factor_3d
    return np.array([x, y])

def project_4D_to_2D(vertex, distance_4D: float, distance_3D: float):
    x, y, z, w = vertex
    factor_4d = distance_4D/(distance_4D-w)
    x, y, z = x * factor_4d, y * factor_4d, z * factor_4d
    factor_3d = distance_3D/(distance_3D-z)
    x, y = x * factor_3d, y * factor_3d
    return np.array([x, y]), w
